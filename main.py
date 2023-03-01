import settings
from client import controller
from domain.repository import NotesRepository


def run_app():
    data_path = settings.get_data_path()
    notes_repo = NotesRepository(data_path)
    controller.run_lifecycle(notes_repo)


if __name__ == '__main__':
    run_app()
