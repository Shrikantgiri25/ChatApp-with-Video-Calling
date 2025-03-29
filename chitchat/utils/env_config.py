import configparser

configs = configparser.ConfigParser()
configs.read("./config/local.ini")
configs.sections()


class EnviromentConfigs:
    # Default Settings
    DEBUG_VALUE = configs["DEFAULT"]["DEBUG_VALUE"]
    SECRET_KEY = configs["DEFAULT"]["SECRET_KEY"]
    ALLOWED_HOSTS = configs["DEFAULT"]["ALLOWED_HOSTS"]

    # Database Settings
    ENGINE = configs["DATABASE"]["ENGINE"]
    NAME = configs["DATABASE"]["NAME"]
    USER = configs["DATABASE"]["USER"]
    PASSWORD = configs["DATABASE"]["PASSWORD"]
    HOST = configs["DATABASE"]["HOST"]
    PORT = configs["DATABASE"]["PORT"]
