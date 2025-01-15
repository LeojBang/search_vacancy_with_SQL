import os
from configparser import ConfigParser
from os.path import dirname

database_name = os.path.join(dirname(__file__), "../database.ini")


def config(filename: str = database_name, section: str = "postgresql") -> dict:
    """
    Читает конфигурационный файл и извлекает параметры для подключения к базе данных.
    Метод ищет в файле конфигурации секцию, указанную в параметре `section` (по умолчанию "postgresql"),
    и извлекает все параметры, определенные в этой секции.
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} is not found in the {1} file.".format(section, filename))
    return db
