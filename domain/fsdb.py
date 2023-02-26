import os
import json
from datetime import datetime
from entities import Note

FILENAME_BLANK = "note{}.json"
FILENAME_DIGITS = 5
FILENAME_FILTER = FILENAME_BLANK.format('?'*FILENAME_DIGITS)
FILENAME_TEMPLATE = FILENAME_BLANK.format(f"{{0:0{FILENAME_DIGITS}d}}")
FILENAME_ID_SLICE = slice(4, 4+FILENAME_DIGITS)
NOTE_ATTRIBUTES = set(vars(Note(None, None, None, None, None)).keys())

data_path: str


def init(path):
    global data_path
    data_path = path


def id_to_filename(id: int) -> str:
    return FILENAME_TEMPLATE.format(id)


def filename_to_id(filename: str) -> int:
    try:
        id_str = filename[FILENAME_ID_SLICE]
        return int(id_str)
    except:
        raise ValueError("Bad Note filename")


def encode_note(obj: Note):
    """Сериализация экземпляра Note в удобочитаемый вариант JSON
    (id не участвует, поскольку кодируется именем файла заметки).
    """

    if isinstance(obj, Note):
        return {
            'creation_date': obj.creation_date,
            'last_change_date': obj.last_change_date,
            'title': obj.title,
            'body': obj.body.splitlines()
        }
    elif isinstance(obj, datetime):
        return str(obj)
    else:
        type_name = obj.__class__.__name__
        raise TypeError(
            f"Object of type '{type_name}' is not JSON serializable")


def decode_note(dct: dict):
    """Де-сериализация JSON в экземпляр Note
    (без инициализации атрибута id, поскольку он не кодируется в JSON,
    а кодируется именем файла заметки, ввиду уникальности имён файлов).
    """
    dct_len = len(dct)
    if dct_len != len(NOTE_ATTRIBUTES)-1 or dct_len != len(dct.keys() & NOTE_ATTRIBUTES):
        raise ValueError(
            f"Deserialized dictionary {dct} does not correspond Note dataclass")
    return Note(
        None,
        datetime.fromisoformat(dct['creation_date']),
        datetime.fromisoformat(dct['last_change_date']),
        dct['title'],
        '\n'.join(dct['body'])
    )


if __name__ == '__main__':

    import entities

    str_data = json.dumps(entities.test_note,
                          ensure_ascii=False,
                          indent=2,
                          default=encode_note
                          )
    print(str_data)
    print("**********************")
    loaded_note = json.loads(str_data, object_hook=decode_note)
    print(type(loaded_note))
    print(loaded_note)
    print("======================")
    print(NOTE_ATTRIBUTES)
    print("======================")
