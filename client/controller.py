from client.view_models import MenuViewModel
from .entities import MenuItem, MenuModel
from . import console_view as view
from domain.repository import NotesRepository
from typing import Any, Callable, NamedTuple, Optional


def dummy():
    view.show("Скоро, но не сейчас...\n"
              "Данная функция будет доступна в следующей версии.")


CMD_GO_BACK = ('0',)
CMD_EXIT = ('й', 'q')
MENU_MAKE_YOUR_CHOICE = "Выберите пункт меню: "

MAIN_MENU = MenuModel(
    header="ЗАМЕТКИ: Главное меню",
    items={
        '1': MenuItem("Новая", dummy),
        '2': MenuItem("Смотреть все", dummy),
        '3': MenuItem("Поиск по заголовку", dummy),
        '4': MenuItem("Поиск по диапазону дат", dummy),
        '5': MenuItem("Поиск по диапазону времени суток", dummy),
        '6': MenuItem("Поиск по номеру", dummy),
        '7': MenuItem("Редактировать", dummy),
        '8': MenuItem("Удалить", dummy),
        CMD_EXIT: MenuItem("Завершить работу", dummy)
    }
)

notes_repo: NotesRepository


def run_lifecycle(notes_data_provider: NotesRepository):
    global notes_repo
    notes_repo = notes_data_provider

    # __main_lifecycle()


def __lifecycle(menu: MenuModel):

    menu_view_model = MenuViewModel(menu)

    finish = False
    while True:

        view.show(menu_view_model)
        user_choice = view.ask_user_choice(MENU_MAKE_YOUR_CHOICE, menu.items.keys())
