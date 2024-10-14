import configparser
import os

from infrastructure.settings.models import (
    AppConfig,
    Config,
    DatabaseConfig,
)


DEFAULT_CONFIG_PATH: str = "./infrastructure/settings/local.ini"


def load_config(path: str | None = None) -> Config:
    """
    Reads configuration from a file and returns a Config object.

    If the `path` parameter is not provided, the function will try to read the configuration from
    the following locations, in order:

    1. The value of the `CONFIG_PATH` environment variable.
    2. The file at `./infrastructure/settings/local.ini`.

    The configuration file must contain two sections: `application` and `database`.

    The `application` section must contain the following keys:

    - `debug`: A boolean value indicating whether the application should run in debug mode.
    - `major_version`, `minor_version`, `patch_version`: The version number of the application.

    The `database` section must contain the following keys:

    - `host`: The hostname or IP address of the database server.
    - `port`: The port number of the database server.
    - `database`: The name of the database to use.
    - `user`: The username to use when connecting to the database.
    - `password`: The password to use when connecting to the database.
    - `echo`: A boolean value indicating whether SQL statements should be echoed to the console.

    :param path: The path to the configuration file.
    :return: A Config object containing the parsed configuration.
    """
    if path is None:
        path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    parser = configparser.ConfigParser()
    parser.read(path)

    application_data, database_data = parser["application"], parser["database"]

    application_config = AppConfig(
        debug=application_data.getboolean("debug", True),
        major_version=application_data.getint("major_version"),
        minor_version=application_data.getint("minor_version"),
        patch_version=application_data.getint("patch_version"),
    )
    database_config = DatabaseConfig(
        host=database_data.get("host"),
        port=database_data.getint("port"),
        database=database_data.get("database"),
        user=database_data.get("user"),
        password=database_data.get("password"),
        echo=database_data.getboolean("echo"),
    )

    return Config(application_config, database_config)