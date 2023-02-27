import os
import json
from datetime import datetime
from entities import Note
from typing import Iterator, Generator, Optional
import pathlib
import warnings

FILENAME_BLANK = "note{}.json"
FILENAME_DIGITS = 5
FILENAME_FILTER = FILENAME_BLANK.format('?'*FILENAME_DIGITS)
FILENAME_TEMPLATE = FILENAME_BLANK.format(f"{{0:0{FILENAME_DIGITS}d}}")
FILENAME_ID_SLICE = slice(4, 4+FILENAME_DIGITS)
NOTE_ATTRIBUTES = set(
    vars(Note(None, datetime.min, datetime.min, "", "")).keys())


class QueryableNotes:

    def __init__(self, path_str) -> None:
        path = pathlib.Path(path_str)
        if path.exists():
            if not path.is_dir():
                raise FileExistsError(
                    f"Path '{path_str}' must be a directory, not a file.")
        else:
            path.mkdir(parents=True)

        self.__path = path

    def __get_filepaths(self):
        """Генератор выдаёт пути без сортировки по имени,
        а в соответствии с их физическим расположением (см. ls -Ul)."""
        return pathlib.Path(self.__path).glob(FILENAME_FILTER)

    def __get_next_id(self):
        filepaths = self.__get_filepaths()
        id = max(map(lambda p: filename_to_id(p.name), filepaths), default=0)
        return id + 1

    def add(self, entry: Note) -> Optional[Note]:
        assert entry is not None
        id = self.__get_next_id()
        entry.id = id
        filename = id_to_filename(id)
        try:
            entry_path = self.__path.joinpath(filename)
            assert not entry_path.exists()
            with entry_path.open('w') as file:
                json.dump(entry,
                          file,
                          ensure_ascii=False,
                          indent=2,
                          default=encode_note
                          )
            return entry
        except Exception:
            warnings.warn(
                f"Ошибка: Не удалось создать файл заметки {filename}.")
        return None

    def queryAll(self) -> Iterator[Note]:
        """Внимание: генератор выдаёт пути без сортировки по имени,
        а в соответствии с их физическим расположением (см. ls -Ul)."""
        filepaths = self.__get_filepaths()
        # return NotesIterator(filepaths_gen)

        def step():
            nonlocal filepaths
            while not (path := next(filepaths)).is_file() or path.stat().st_size == 0:
                pass
            id = filename_to_id(path.name)
            note: Optional[Note] = None
            try:
                with path.open('r', encoding='UTF-8') as file:
                    note = json.load(file, object_hook=decode_note)
                    if note is None:
                        return step()
                    note.id = id
            except Exception as e:
                warnings.warn(
                    f"Ошибка: Не удалось прочитать файл заметки {id}.")
                return step()
            return note

        return iter(step, None)

    def get(self, id: int) -> Optional[Note]:
        ...

    def update(self, entry: Note) -> bool:
        ...

    def delete(self, id: int) -> Optional[Note]:
        ...


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
    print("*****")
    loaded_note = json.loads(str_data, object_hook=decode_note)
    print(type(loaded_note))
    print(loaded_note)
    print("=====")
    print(NOTE_ATTRIBUTES)
    print("=====")
    qn = QueryableNotes('data')
    lst = list(qn.queryAll())
    print(lst)
    for n in qn.queryAll():
        print("~~~~~")
        print(n)
        print("~~~~~")

    # print(qn.__get_next_id())
    # print(qn._QueryableNotes__get_next_id())
    # print(qn.get_next_id_public())


# class NotesIterator(Iterator[Note]):
#     def __init__(self, filepaths: Generator[pathlib.Path, None, None]) -> None:
#         self._filepaths = filepaths

#     def __iter__(self):
#         return self

#     def __next__(self):
#         while not (path := next(self._filepaths)).is_file() or path.stat().st_size == 0:
#             pass
#         id = filename_to_id(path.name)
#         note: Optional[Note] = None
#         try:
#             with path.open('r', encoding='UTF-8') as file:
#                 note = json.load(file, object_hook=decode_note)
#                 if note is None:
#                     return self.__next__()
#                 note.id = id
#         except Exception as e:
#             warnings.warn(f"Ошибка: Не удалось прочитать файл заметки {id}.")
#             return self.__next__()
#         return note
