from datetime import datetime, time, date
from typing import Iterator, Optional, Callable
from enum import Enum, auto
from .entities import Note
from .fsdb import QueryableNotes


class AttributeKind(Enum):
    CREATION = auto()
    LAST_CHANGE = auto()


class NotesRepository:

    def __init__(self, path_str) -> None:
        self.__notes_table = QueryableNotes(path_str)

    # create

    def add_note(self, note: Note):
        if note is None:
            raise TypeError(note)

        return self.__notes_table.add(note)

    # read

    def get_note_by_id(self, note_id: int) -> Optional[Note]:
        if note_id <= 0:
            raise ValueError(note_id)

        return self.__notes_table.get(note_id)

    def get_all_notes(self) -> Iterator[Note]:
        return self.__notes_table.queryAll()

    def get_notes_by_title(self, title_sample: str) -> Iterator[Note]:
        if not title_sample:
            return iter(())

        title_sample = title_sample.lower()
        notes_iter = self.get_all_notes()
        return filter(lambda n: title_sample in n.title.lower(), notes_iter)

    def get_notes_by_date_range(self,
                                date_from: date, date_to: date,
                                kind=AttributeKind.CREATION,
                                ) -> Iterator[Note]:
        """Выборка заметок по диапазону дат.\n
        kind - временной атрибута: время создания или последнего изменения.
        """
        if date_to < date_from:
            date_from, date_to = date_to, date_from

        # get_date: Callable[[Note], datetime]
        if kind == AttributeKind.CREATION:
            def get_date(n: Note): return n.creation_date.date()
        else:
            def get_date(n: Note): return n.last_change_date.date()

        def is_in_range(note: Note):
            return date_from <= get_date(note) <= date_to

        notes_iter = self.get_all_notes()
        return filter(is_in_range, notes_iter)

    def get_notes_by_daytime_range(self,
                                   time_from: time, time_to: time,
                                   kind=AttributeKind.CREATION,
                                   ) -> Iterator[Note]:
        """Выборка заметок по диапазону времени суток.\n
        kind - временной атрибута: время создания или последнего изменения.
        """
        if time_to < time_from:
            time_from, time_to = time_to, time_from

        # get_date: Callable[[Note], datetime]
        if kind == AttributeKind.CREATION:
            def get_time(n: Note): return n.creation_date.time()
        else:
            def get_time(n: Note): return n.last_change_date.time()

        def is_in_range(note: Note):
            return time_from <= get_time(note) <= time_to

        notes_iter = self.get_all_notes()
        return filter(is_in_range, notes_iter)

    # update

    def update_note(self, note: Note) -> bool:
        if note is None:
            raise TypeError(note)

        return self.__notes_table.update(note)

    # delete

    def delete_note(self, note_id: int) -> bool:
        if note_id <= 0:
            raise ValueError(note_id)
        return self.__notes_table.delete(note_id) is not None
