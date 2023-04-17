from pydantic import BaseSettings


class AppSettings(BaseSettings):
    dev_server_address: str = '0.0.0.0'
    dev_server_port: int = 8080

    class Config:
        env_prefix = 'nm_'
