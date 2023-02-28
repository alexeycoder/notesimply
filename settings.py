import os
from typing import Optional
import warnings
import json
import utils

SETTINGS_FILE_PATH = "settings.json"
WARN_CANNOT_OPEN = ("Предупреждение:"
                    f"Не удалось открыть файл настроек \'{SETTINGS_FILE_PATH}\'."
                    "Будут использованы настройки по молчанию.")
WARN_CANNOT_SAVE = ("Ошибка:"
                    f"Не удалось сохранить настройки в \'{SETTINGS_FILE_PATH}\'."
                    "Возможно доступ к файлу заблокирован.")

__settings = {
    "data_path": ".data.d"
}


# settings api

def get_data_path():
    return __settings["data_path"]


def save() -> bool:
    "Сохраняет настройки в файл. Возвращает False, если не удалось сохранить."
    try:
        with open(SETTINGS_FILE_PATH, 'wt', encoding='UTF-8') as file:
            json.dump(__settings, file, indent=2)
    except Exception:
        warnings.warn(WARN_CANNOT_SAVE)
        return False

    return True


# aux

@utils.once
def __init():
    """Перезаписывает параметры по-умолчанию значениями из файла настроек,
    если таковой имеется.
    """
    if not os.path.isfile(SETTINGS_FILE_PATH):
        return

    raw_settings: Optional[dict] = None
    try:
        with open(SETTINGS_FILE_PATH, 'rt', encoding='UTF-8') as file:
            raw_settings = json.load(file)
    except OSError:
        warnings.warn(WARN_CANNOT_OPEN)

    if raw_settings is None:
        return

    for k in (__settings.keys() & raw_settings.keys()):
        __settings[k] = raw_settings[k]


# initialize the module

__init()

if __name__ == '__main__':
    # save()
    ...
