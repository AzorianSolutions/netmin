from pydantic import BaseSettings


class AppSettings(BaseSettings):
    dev_server_address: str = '0.0.0.0'
    dev_server_port: int = 8080
    graylog_url: str | None
    graylog_token: str | None

    class Config:
        env_prefix = 'mn_'
