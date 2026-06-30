import contextlib
import copy
import os
import shlex
import subprocess
import tempfile
import tomllib
import typing
from pathlib import Path
from typing import Annotated, Optional

from pydantic import Field, computed_field, model_validator, SecretStr, EmailStr
from pydantic_settings import BaseSettings


class PostBackup(BaseSettings, frozen=True):
    forget_dry: Annotated[bool, Field()]
    check: Annotated[bool, Field()]
    forget: Annotated[bool, Field()]
    shutdown: Annotated[bool, Field()]


class ForgetOptions(BaseSettings, frozen=True):
    prune: Annotated[bool, Field(default=False)]
    keep_policy: Annotated[
        typing.Literal["within", "default"] | None, Field(default=None)
    ]


class RcyPaths(BaseSettings, frozen=True):
    log_folder: Path
    include_patterns: list[str]
    exclude_patterns: list[str]


class SystemConfiguration(BaseSettings, frozen=True):
    file_path: Annotated[Path, Field()]

    name: Annotated[str, Field()]
    password: Annotated[SecretStr, Field()]
    notify_mail: Annotated[EmailStr | None, Field(default=None)]
    restic_repo_url: Annotated[str, Field()]
    restic_bin: Annotated[str, Field()]
    include_patterns: Annotated[Optional[list[str]], Field(default=[])]
    exclude_patterns: Annotated[Optional[list[str]], Field(default=[])]

    paths: Annotated[RcyPaths, Field()]
    post_backup: Annotated[PostBackup, Field()]
    verbosity: Annotated[int, Field(default=2, ge=0, le=2)]
    envs: Annotated[dict[str, str], Field(default={})]

    forget_options: Annotated[
        ForgetOptions, Field(alias="forget", default_factory=ForgetOptions)
    ]

    @model_validator(mode="after")
    def model_validator(self) -> typing.Self:
        absolute_from_relative = (
            self.file_path.parent / self.paths.log_folder
        ).resolve()
        object.__setattr__(self.paths, "log_folder", absolute_from_relative)
        return self

    @computed_field
    def secrets_file(self) -> Path:
        return self.get_secrets_file(self.file_path)

    @staticmethod
    def get_secrets_file(file_path: Path) -> Path:
        file_name = file_path.name
        split = file_name.split(".")
        split.insert(2, "secrets")
        return file_path.with_name(".".join(split))

    @staticmethod
    def get_secrets_commands_file(file_path: Path) -> Path:
        file_name = file_path.name
        split = file_name.split(".")
        split.insert(2, "secrets")
        return file_path.with_name(".".join(split))

    def get_password_cmd(self):
        sf = self.get_secrets_file(self.file_path)
        toml_secret_dict = tomllib.loads(sf.read_text(encoding="utf-8"))
        return toml_secret_dict["repo"]["password-cmd"]

    @classmethod
    def populate_from_secrets_file(cls, path, toml_dict: dict):
        sf = cls.get_secrets_file(path)
        toml_secret_dict = tomllib.loads(sf.read_text(encoding="utf-8"))

        with contextlib.suppress(KeyError):
            if toml_secret_dict["repo"]["password-cmd"]:
                toml_dict["repo"]["password"] = subprocess.run(
                    shlex.split(toml_secret_dict["repo"]["password-cmd"]),
                    check=True,
                    text=True,
                    capture_output=True,
                ).stdout.strip()
            del toml_secret_dict["repo"]["password-cmd"]
            for secret_env_name, secret_env_command in toml_secret_dict["repo"]["envs"][
                "cmds"
            ].items():
                toml_secret_dict["repo"]["envs"][secret_env_name] = subprocess.run(
                    shlex.split(secret_env_command),
                    check=True,
                    text=True,
                    capture_output=True,
                ).stdout.strip()
            del toml_secret_dict["repo"]["envs"]["cmds"]

        return cls.deep_merge(toml_dict, toml_secret_dict)

    @classmethod
    def from_toml_file(cls, path: Path) -> "SystemConfiguration":
        toml_dict = tomllib.loads(path.read_text(encoding="utf-8"))
        toml_dict = cls.populate_from_secrets_file(path, toml_dict)
        model = cls(**toml_dict["repo"], file_path=path)
        return model

    def _common_restic_cli_params(self) -> list[str]:
        return [f"-{'v' * self.verbosity}"]

    def make_environment(self):
        env = {}
        env.update(self.envs)
        env["RESTIC_PROGRESS_FPS"] = "0.1"
        return env

    def pepper_with_base_command(self, command: list[str]):
        new_command = [*command]
        new_command.insert(0, self.restic_bin)

        for i, cp in enumerate(self._common_restic_cli_params()):
            new_command.insert(1 + i, cp)
        return new_command

    def is_peppered(self, command: list[str]) -> bool:
        return command[0] == self.restic_bin

    @staticmethod
    def deep_merge(base, override):
        result = copy.deepcopy(base)
        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = SystemConfiguration.deep_merge(result[key], value)
            else:
                result[key] = copy.deepcopy(value)
        return result

    def get_log_file(self) -> Path:
        return (self.file_path.parent / "logs/rcy.log").resolve()

    @contextlib.contextmanager
    def tmpfile_with(
        self,
        path_property_name: typing.Literal[
            "include_patterns", "exclude_patterns", "password"
        ],
    ) -> typing.Generator[str, None, None]:
        if path_property_name == "password":
            content = self.password.get_secret_value()
        else:
            content_list: list[str] = getattr(self.paths, path_property_name)
            content = "\n".join(content_list)

        def abs(path: Path) -> str:
            return str(path.resolve())

        fd, path = tempfile.mkstemp(prefix="restic-files-", suffix=".lst")
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
                f.write(content)
            yield abs(
                Path(path)
            )  # fd is closed and flushed here, file is now safely readable
        finally:
            os.unlink(path)
