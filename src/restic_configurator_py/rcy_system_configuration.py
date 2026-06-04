from pathlib import Path
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings


class PostBackup(BaseSettings, frozen=True):
    forget_dry: Annotated[bool, Field()]
    check: Annotated[bool, Field()]
    forget: Annotated[bool, Field()]
    shutdown: Annotated[bool, Field()]


class RcyPaths(BaseSettings, frozen=True):
    pass_file_path: Path
    files_list_path: Path
    exclude_patterns_path: Path
    log_folder: Path


class SystemConfiguration(BaseSettings, frozen=True):
    name: Annotated[str, Field()]
    paths: Annotated[RcyPaths, Field()]
    env_filenames: Annotated[list[Path], Field()]
    restic_repo_url: Annotated[str, Field()]
    restic_exe: Annotated[str, Field()]
    post_backup: Annotated[PostBackup, Field()]
