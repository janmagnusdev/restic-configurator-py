import copy
import tomllib
import typing
from pathlib import Path
from typing import Annotated, Optional

from pydantic import Field, PrivateAttr, SecretStr, model_validator
from pydantic_settings import BaseSettings


class PostBackup(BaseSettings, frozen=True):
    forget_dry: Annotated[bool, Field()]
    check: Annotated[bool, Field()]
    forget: Annotated[bool, Field()]
    shutdown: Annotated[bool, Field()]


class RcyPaths(BaseSettings, frozen=True):
    log_folder: Path
    include_patterns: list[str]
    exclude_patterns: list[str]


class SystemConfiguration(BaseSettings, frozen=True):
    file_path: Annotated[Path, Field()]

    name: Annotated[str, Field()]
    password: Annotated[SecretStr, Field()]
    restic_repo_url: Annotated[str, Field()]
    restic_bin: Annotated[str, Field()]
    include_patterns: Annotated[Optional[list[str]], Field(default=[])]
    exclude_patterns: Annotated[Optional[list[str]], Field(default=[])]

    paths: Annotated[RcyPaths, Field()]
    post_backup: Annotated[PostBackup, Field()]
    envs: Annotated[dict[str, str], Field(default={})]

    @model_validator(mode="after")
    def model_validator(self) -> typing.Self:
        absolute_from_relative = (
            self.file_path.parent / self.paths.log_folder
        ).resolve()
        object.__setattr__(self.paths, "log_folder", absolute_from_relative)
        return self

    @classmethod
    def from_toml_file(cls, path: Path) -> "SystemConfiguration":
        file_name = path.name
        split = file_name.split(".")
        split.insert(2, "secrets")
        secrets_file = path.with_name(".".join(split))

        toml_dict = tomllib.loads(path.read_text(encoding="utf-8"))
        toml_secret_dict = tomllib.loads(secrets_file.read_text(encoding="utf-8"))
        toml_dict = cls.deep_merge(toml_dict, toml_secret_dict)
        model = cls(**toml_dict["repo"], file_path=path)
        return model

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
