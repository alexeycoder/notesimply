from datetime import datetime, date, time
from client.view_models import NoteViewModel
from client import controller
import settings
from domain.repository import AttributeKind, NotesRepository


def run_app():
    data_path = settings.get_data_path()
    notes_repo = NotesRepository(data_path)
    controller.run_lifecycle(notes_repo)

def __test():
    notes_repo = NotesRepository('data')
    notes = notes_repo.get_all_notes()
    for note in notes:
        print("~~~~~")
        print(note)
        print("~~~~~")

    print("==========\n==========")
    found_notes = notes_repo.get_notes_by_title("тка")
    for note in found_notes:
        print(note)

    print("\n\nselect by date:\n")
    found_notes = notes_repo.get_notes_by_date_range(
        date.fromisoformat("2023-01-30"),
        date.fromisoformat("2023-02-15"),
        AttributeKind.CREATION
    )
    [print(n) for n in found_notes]

    print("\n\nselect by time:\n")
    found_notes = notes_repo.get_notes_by_daytime_range(
        time.fromisoformat("00:30"),
        time.fromisoformat("03:00"),
        AttributeKind.CREATION
    )
    [print(NoteViewModel(n)) for n in found_notes]


if __name__ == '__main__':
    # __test()
    run_app()
