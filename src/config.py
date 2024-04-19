from configparser import ConfigParser


def config(filename='database.ini', section="postgresql"):
    """Возвращает параметры подключения к локальной ДБ, записанные в файл 'database.ini'
    :param filename: файл с конфигом
    :param section: раздел хранения параметров подключения """
    parser = ConfigParser()
    parser.read(filename)
    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file.')
    return db_params
