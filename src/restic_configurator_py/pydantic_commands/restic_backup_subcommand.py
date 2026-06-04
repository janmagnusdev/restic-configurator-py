from pydantic_settings import BaseSettings


class ResticBackupSubcommand(BaseSettings):
    def cli_cmd(self):
        pass
