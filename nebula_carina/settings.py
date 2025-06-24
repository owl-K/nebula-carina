from typing import Set, Optional, Union
import typing
from pydantic_settings import BaseSettings, SettingsConfigDict


try:
    # for django
    from django.conf import settings

    class DjangoCarinaDatabaseSettings(object):
        max_connection_pool_size: int = 10
        servers: Set[str] = set()
        user_name: str
        password: str
        default_space: str = "main"
        auto_create_default_space_with_vid_desc: Optional[str]

        model_paths: Set[str] = set()
        timezone_name: str = "UTC"

        @staticmethod
        def is_optional(tp):
            return typing.get_origin(tp) is Union and type(None) in typing.get_args(tp)

        def __init__(self, **kwargs):
            for key, type_ in DjangoCarinaDatabaseSettings.__dict__[
                "__annotations__"
            ].items():
                if not self.is_optional(type_) and not hasattr(
                    DjangoCarinaDatabaseSettings, key
                ):
                    assert (
                        key in kwargs
                    ), f"Setting {key} is required but not provided in CARINA_SETTINGS."
                key in kwargs and setattr(self, key, kwargs[key])

    database_settings = DjangoCarinaDatabaseSettings(**settings.CARINA_SETTINGS)
except ModuleNotFoundError:

    class DatabaseSettings(BaseSettings):
        max_connection_pool_size: int = 10
        servers: Set[str] = {"101.35.211.56:9669"}
        user_name: Optional[str] = "root"
        password: Optional[str] = "rkRK123@"
        default_space: str = "main"
        auto_create_default_space_with_vid_desc: Optional[str] = None

        model_paths: Set[str] = set()
        timezone_name: str = "UTC"
        model_config = SettingsConfigDict(env_prefix="nebula_")

    database_settings = DatabaseSettings()
