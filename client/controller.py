from datetime import datetime
from client.view_models import MenuViewModel, NoteViewModel
from domain.entities import Note
from .entities import MenuItem, MenuModel
from . import console_view as view
from domain.repository import NotesRepository
from typing import Any, Callable, Iterator, NamedTuple, Optional

CMD_GO_BACK = ('0',)
CMD_EXIT = ('й', 'q')
MENU_MAKE_YOUR_CHOICE = "Выберите пункт меню: "
GOODBYE = "Вы завершили программу.\nСпасибо что пользуетесь Notesimply!"
SHORT_HR = "\u2014"

MAIN_MENU = MenuModel(
    header="ЗАМЕТКИ: Главное меню",
    items={
        '1': MenuItem("Новая", lambda: __add_new()),
        '2': MenuItem("Смотреть все", lambda: __show_all()),
        '3': MenuItem("Поиск по заголовку", lambda: __dummy()),
        '4': MenuItem("Поиск по диапазону дат", lambda: __dummy()),
        '5': MenuItem("Поиск по диапазону времени суток", lambda: __dummy()),
        '6': MenuItem("Поиск по идентификатору", lambda: __dummy()),
        '7': MenuItem("Редактировать", lambda: __dummy()),
        '8': MenuItem("Удалить", lambda: __dummy()),
        ' ': None,
        CMD_EXIT: MenuItem("Завершить работу", None)
    }
)

SORT_MENU = MenuModel(
    header="Просмотр заметок: Как сортировать?",
    items={
        '1': MenuItem("По времени создания - от старых к новым", lambda ns: __show_all_sort_by_creation_recent_last(ns)),
        '2': MenuItem("По времени создания - от новых к старым", lambda ns: __show_all_sort_by_creation_older_last(ns)),
        '3': MenuItem("По времени последнего изменения - от давних к недавним", lambda ns: __show_all_sort_by_change_recent_last(ns)),
        '4': MenuItem("По времени последнего изменения - от недавних к давним", lambda ns: __show_all_sort_by_change_older_last(ns)),
        '5': MenuItem("По заголовку - А..Я", lambda ns: __show_all_sort_by_title_natural(ns)),
        '6': MenuItem("По заголовку - Я..А", lambda ns: __show_all_sort_by_title_reverse(ns)),
        ' ': None,
        CMD_GO_BACK: MenuItem("Вернуться в предыдущее меню", None),
        CMD_EXIT: MenuItem("Завершить работу", None)
    }
)


notes_repo: NotesRepository
__exit_flag = False


def run_lifecycle(notes_data_provider: NotesRepository):
    global notes_repo
    notes_repo = notes_data_provider
    __menu_lifecycle(MAIN_MENU)


def __dummy(*args, **kwargs):
    view.show("Скоро, но не сейчас...\n"
              "Данная функция будет доступна в следующей версии.")
    view.wait_to_proceed()


def __menu_lifecycle(menu: MenuModel, *args,
                     onetime: bool = False, clear: bool = True, **kwargs):
    global __exit_flag
    if __exit_flag:
        return

    menu_view_model = MenuViewModel(menu)

    while True:
        if clear:
            view.clear()
        view.show(menu_view_model)
        user_choice = view.ask_user_choice(
            MENU_MAKE_YOUR_CHOICE, menu.items.keys())
        view.show(SHORT_HR)

        if user_choice == CMD_EXIT:
            __exit_flag = True
            view.show(GOODBYE)
            break
        elif user_choice == CMD_GO_BACK:
            break
        else:
            menu_item = menu.items.get(user_choice)
            assert menu_item is not None
            if menu_item.handler is not None:
                menu_item.handler(*args, **kwargs)

            if onetime:
                break

            if __exit_flag:
                break


def __add_new():
    do_repeat = True

    while do_repeat:
        view.clear()
        view.show("ЗАМЕТКИ: Создание новой")
        view.show()

        title = view.ask_string(
            "Введите заголовок заметки (пустой Ввод чтобы отменить):\n")
        if not title:
            view.show(SHORT_HR)
            view.show("Добавление заметки отменено.")
            view.wait_to_proceed()
            return

        body = view.ask_multiline_text("\nВведите текст заметки:"
                                       "\nДопускается многострочный текст."
                                       " Нажмите Ввод для перевода строки.")

        dt = datetime.now()
        note_to_save = Note(None, dt, dt, title, body)
        view.show(SHORT_HR)
        result_note = notes_repo.add_note(note_to_save)
        if result_note is None:
            view.show("Не удалось сохранить заметку!"
                      " Ошибка при работе с хранилищем."
                      "\nВы можете скопировать содержимое заметки"
                      " из вывода ниже чтобы не потерять его.")
            view.show(NoteViewModel(note_to_save))
        else:
            view.show(NoteViewModel(result_note))
            view.show("\nЗаметка успешно добавлена.")

        view.show(SHORT_HR)
        do_repeat = view.ask_yes_no("Добавить ещё заметку (д/Н)? ", False)


def __show_all(notes: Optional[list[Note]] = None):
    if notes:
        for note in notes:
            view.show(NoteViewModel(note))
        view.show(SHORT_HR)
        view.wait_to_proceed()
        return

    notes = list(notes_repo.get_all_notes())
    if not notes:
        view.show("Вы ещё не создали ни одной заметки. Список заметок пуст.")
        view.wait_to_proceed()
        return

    __menu_lifecycle(SORT_MENU, notes)  # onetime=True)


def __show_all_sort_by_creation_recent_last(notes: list[Note]):
    notes.sort(key=lambda n: n.creation_date)
    __show_all(notes)


def __show_all_sort_by_creation_older_last(notes: list[Note]):
    notes.sort(key=lambda n: n.creation_date, reverse=True)
    __show_all(notes)


def __show_all_sort_by_change_recent_last(notes: list[Note]):
    notes.sort(key=lambda n: n.last_change_date)
    __show_all(notes)


def __show_all_sort_by_change_older_last(notes: list[Note]):
    notes.sort(key=lambda n: n.last_change_date, reverse=True)
    __show_all(notes)


def __show_all_sort_by_title_natural(notes: list[Note]):
    notes.sort(key=lambda n: n.title)
    __show_all(notes)


def __show_all_sort_by_title_reverse(notes: list[Note]):
    notes.sort(key=lambda n: n.title, reverse=True)
    __show_all(notes)
