from datetime import datetime
from typing import Optional
from domain.entities import Note
from enum import Enum, auto

from fsdb import QueryableNotes


class DateMode(Enum):
    CREATION = auto()
    LAST_CHANGE = auto()


class NotesRepository:

    def __init__(self, path_str) -> None:
        self.__notes_table = QueryableNotes(path_str)

    # create

    def add_note(self, note: Note):
        ...

    # read

    def get_note_by_id(self, note_id: int) -> Optional[Note]:
        ...

    def get_all_notes(self) -> list[Note]:
        ...

    def get_notes_by_title(self, title_sample: str) -> list[Note]:
        ...

    def get_notes_by_date(self, date_from: datetime, date_to: datetime, mode=DateMode.CREATION) -> list[Note]:
        ...

    # update

    def update_note(self, note: Note) -> bool:
        if note is None:
            raise ValueError(note)

        return self.__notes_table.update(note)

    # delete

    def delete_note(self, note_id: int) -> bool:
        if note_id <= 0:
            raise ValueError(note_id)
        return self.__notes_table.delete(note_id) is not None
