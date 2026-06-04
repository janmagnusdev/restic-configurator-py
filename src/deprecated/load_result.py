import argparse
from dataclasses import astuple, dataclass


# TODO: migrate this to a pydantic BaseSettings class
@dataclass
class LoadResult:
    pass_file_path: str
    log_folder: str
    restic_path: str
    repo: str
    environment: dict
    files_list_path: str
    exclude_patterns_path: str
    system_config: dict
    current_sys: str
    args: argparse.Namespace

    def __iter__(self):
        return iter(astuple(self))

    def __getitem__(self, keys):
        return iter(getattr(self, k) for k in keys)
