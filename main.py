from datetime import datetime
import settings
from domain.repository import NotesRepository


def run_app():
    data_path = settings.get_data_path()


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

    dt = datetime.now()
    print(dt)
    print(dt.date())
    print(dt.day)
    print(dt.time())



if __name__ == '__main__':
    __test()

    # def func(note):
    #     if note is None:
    #         raise TypeError(note)
    # func(None)
