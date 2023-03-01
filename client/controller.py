from datetime import datetime, date, time
from client.view_models import MenuViewModel, NoteViewModel
from domain.entities import Note
from .entities import MenuItem, MenuModel
from . import console_view as view
from domain.repository import AttributeKind, NotesRepository
from typing import Any, Callable, Iterator, NamedTuple, Optional
import re

CMD_GO_BACK = ('0',)
CMD_EXIT = ('й', 'q')
MENU_MAKE_YOUR_CHOICE = "Выберите пункт меню: "
GOODBYE = "Вы завершили программу.\nСпасибо что пользуетесь Notesimply!"
SHORT_HR = "\u2014"

MAIN_MENU = MenuModel(
    header="ЗАМЕТКИ: Главное меню",
    items={
        '1': MenuItem("Новая", lambda: __add_new()),
        '2': MenuItem("Смотреть все \u2026", lambda: __show_all()),
        '3': MenuItem("Поиск по идентификатору \u2026", lambda: __select_by_id()),
        '4': MenuItem("Поиск по заголовку", lambda: __select_by_title()),
        '5': MenuItem("Поиск по диапазону дат", lambda: __select_by_date_range()),
        '6': MenuItem("Поиск по диапазону времени суток", lambda: __select_by_daytime_range()),
        '7': MenuItem("Редактировать", lambda: __edit()),
        '8': MenuItem("Удалить", lambda: __delete()),
        ' ': None,
        CMD_EXIT: MenuItem("Завершить работу", None)
    })

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
    })

SINGLE_NOTE_ACTION_MENU = MenuModel(
    header="Найденная заметка",
    items={
        '1': MenuItem("Редактировать", lambda n: __edit(n)),
        '2': MenuItem("Удалить", lambda n: __delete(n)),
        ' ': None,
        CMD_GO_BACK: MenuItem("Продолжить...", None),
    })


notes_repo: NotesRepository
__exit_flag = False


def run_lifecycle(notes_data_provider: NotesRepository):
    global notes_repo
    notes_repo = notes_data_provider
    __menu_lifecycle(MAIN_MENU)


# def __dummy(*args, **kwargs):
#     view.show("Скоро, но не сейчас...\n"
#               "Данная функция будет доступна в следующей версии.")
#     view.wait_to_proceed()


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
            return user_choice
        elif user_choice == CMD_GO_BACK:
            return user_choice
        else:
            menu_item = menu.items.get(user_choice)
            assert menu_item is not None
            if menu_item.handler is not None:
                menu_item.handler(*args, **kwargs)

            if onetime:
                return user_choice

            if __exit_flag:
                return user_choice


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
        do_repeat = view.ask_yes_no("Добавить ещё заметку (д/Н)(y/N)? ", False)


def __show_all(notes: Optional[list[Note]] = None):
    if notes:
        for note in notes:
            view.show(NoteViewModel(note))
        view.show(f"\u2211 Найдено заметок: {len(notes)}")
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


def __select_by_id(header="ЗАМЕТКИ: Поиск по идентификатору", return_found=False) -> Optional[Note]:
    do_repeat = True

    while do_repeat:
        view.clear()
        view.show(header)
        view.show()

        note_id = view.ask_integer_in_range(
            "Введите ID заметки (пустой Ввод чтобы отменить): ", min=NotesRepository.NOTES_MIN_ID)
        view.show(SHORT_HR)

        if note_id is None:
            if return_found:
                return None
            view.show("Поиск отменён.")
            view.wait_to_proceed()
            break

        note = notes_repo.get_note_by_id(note_id)
        if note:
            view.show(NoteViewModel(note))
            if return_found:
                return note

            return_state = __menu_lifecycle(SINGLE_NOTE_ACTION_MENU, note,
                                            onetime=True, clear=False)
            if return_state != CMD_GO_BACK:
                break

        else:
            view.show(
                "Не найдено заметки с указанным ID.")

        do_repeat = view.ask_yes_no("Повторить поиск (Д/н)(Y/n)? ", True)


def __select_by_title():
    do_repeat = True

    while do_repeat:
        view.clear()
        view.show("ЗАМЕТКИ: Поиск по заголовку")
        view.show()

        title_sample = view.ask_string("Введите текст заголовка частично или полностью"
                                       " (пустой Ввод чтобы отменить):\n")
        view.show(SHORT_HR)

        if not title_sample:
            view.show("Поиск отменён.")
            view.wait_to_proceed()
            return

        notes = list(notes_repo.get_notes_by_title(title_sample))
        if notes:
            __show_all_sort_by_creation_recent_last(notes)
        else:
            view.show(
                "Не найдено заметок, содержащих в заголовке заданный текст.")

        view.show(SHORT_HR)
        do_repeat = view.ask_yes_no("Повторить поиск (Д/н)(Y/n)? ", True)


def __select_by_date_range():

    def check_date_str_validity(date_str: str):
        if not re.fullmatch("^\\d{4}-([0][1-9]|1[0-2])-([0-2][1-9]|[1-3]0|3[01])$", date_str):
            return False

        try:
            res = date.fromisoformat(date_str)
            if res:
                return True
        except:
            pass

        return False

    do_repeat = True

    while do_repeat:
        view.clear()
        view.show("ЗАМЕТКИ: Поиск по диапазону дат")
        view.show()

        attr_kind = view.ask_user_choice(
            ("Выберите:"
             "\n1 \u2014 использовать дату создания,"
             "\n2 \u2014 дату последнего изменения"
             "\n(или 0 \u2014 чтобы отменить поиск): "), set((0, 1, 2)))
        if attr_kind == 0:
            view.show("\nПоиск отменён.")
            view.wait_to_proceed()
            return

        attribute_kind = AttributeKind.CREATION if attr_kind == 1 else AttributeKind.LAST_CHANGE
        view.show()

        wrong_format_msg = "Ошибка ввода: Пожалуйста вводите дату в указанном формате."

        first_date_str = view.ask_string(
            "Введите первую дату диапазона в формате ГГГГ-ММ-ДД (пустой Ввод чтобы отменить): ",
            check_date_str_validity,
            wrong_format_msg)

        if not first_date_str:
            view.show("\nПоиск отменён.")
            view.wait_to_proceed()
            return

        second_date_str = view.ask_string(
            "\nВведите вторую дату диапазона в формате ГГГГ-ММ-ДД (пустой Ввод чтобы отменить): ",
            check_date_str_validity,
            wrong_format_msg)

        if not second_date_str:
            view.show("\nПоиск отменён.")
            view.wait_to_proceed()
            return

        first_date = date.fromisoformat(first_date_str)
        second_date = date.fromisoformat(second_date_str)
        if second_date < first_date:
            first_date, second_date = second_date, first_date

        view.show(f"\nЗадан диапазон {first_date}\u2014{second_date}.\n")

        notes = list(notes_repo.get_notes_by_date_range(
            first_date, second_date, attribute_kind))
        if notes:
            if attribute_kind == AttributeKind.CREATION:
                __show_all_sort_by_creation_recent_last(notes)
            else:
                __show_all_sort_by_change_recent_last(notes)
        else:
            view.show(
                f"Не найдено заметок в указанном диапазоне дат {first_date}\u2014{second_date}.")

        view.show(SHORT_HR)
        do_repeat = view.ask_yes_no("Повторить поиск (Д/н)(Y/n)? ", True)


def __select_by_daytime_range():

    def check_time_str_validity(time_str: str):
        if not re.fullmatch("^[0-2]\\d:[0-5]\\d(:[0-5]\\d)?$", time_str):
            return False

        try:
            res = time.fromisoformat(time_str)
            if res:
                return True
        except:
            pass

        return False

    do_repeat = True

    while do_repeat:
        view.clear()
        view.show("ЗАМЕТКИ: Поиск по диапазону времени суток")
        view.show()

        attr_kind = view.ask_user_choice(
            ("Выберите:"
             "\n1 \u2014 использовать время создания,"
             "\n2 \u2014 время последнего изменения"
             "\n(или 0 \u2014 чтобы отменить поиск): "), set((0, 1, 2)))
        if attr_kind == 0:
            view.show("\nПоиск отменён.")
            view.wait_to_proceed()
            return

        attribute_kind = AttributeKind.CREATION if attr_kind == 1 else AttributeKind.LAST_CHANGE
        view.show()

        wrong_format_msg = "Ошибка ввода: Пожалуйста вводите время в указанном формате."

        first_time_str = view.ask_string(
            "Введите начальное время диапазона в формате ЧЧ:ММ:СС (секунды можно опустить; пустой Ввод чтобы отменить): ",
            check_time_str_validity,
            wrong_format_msg)

        if not first_time_str:
            view.show("\nПоиск отменён.")
            view.wait_to_proceed()
            return

        second_time_str = view.ask_string(
            "\nВведите конечное время диапазона в формате ЧЧ:ММ:СС (секунды можно опустить; пустой Ввод чтобы отменить): ",
            check_time_str_validity,
            wrong_format_msg)

        if not second_time_str:
            view.show("\nПоиск отменён.")
            view.wait_to_proceed()
            return

        first_time = time.fromisoformat(first_time_str)
        second_time = time.fromisoformat(second_time_str)
        if second_time < first_time:
            first_time, second_time = second_time, first_time

        view.show(f"\nЗадан диапазон {first_time}\u2014{second_time}.\n")

        notes = list(notes_repo.get_notes_by_daytime_range(
            first_time, second_time, attribute_kind))
        if notes:
            if attribute_kind == AttributeKind.CREATION:
                __show_all_sort_by_creation_recent_last(notes)
            else:
                __show_all_sort_by_change_recent_last(notes)
        else:
            view.show(
                f"Не найдено заметок в указанном диапазоне времени дня {first_time}\u2014{second_time}.")

        view.show(SHORT_HR)
        do_repeat = view.ask_yes_no("Повторить поиск (Д/н)(Y/n)? ", True)


def __edit(note: Optional[Note] = None):
    if note and note.id is not None:

        if view.ask_yes_no(f"Редактировать заметку {note.id} (Д/н)(Y/n)? ", True):

            title = view.ask_string(
                "Введите заголовок заметки (пустой Ввод чтобы оставить без изменений):\n")
            if title:
                note.title = title
            else:
                view.show(note.title)
                view.show()

            replace_text = view.ask_yes_no(
                (f"Выберите: Д(Y) \u2014 ввести новый текст заметки,"
                 "\nили н(n) \u2014 добавить к уже имеющемуся? "), True)

            body = view.ask_multiline_text(
                f"\nВведите {'новый' if replace_text else 'добавочный'} текст заметки:"
                "\nДопускается многострочный текст."
                " Нажмите Ввод для перевода строки.")

            if replace_text:
                note.body = body
            else:
                note.body += '\n' + body

            note.last_change_date = datetime.now()

            view.show(SHORT_HR)
            view.show("Предварительный просмотр:")
            view.show(NoteViewModel(note))

            if view.ask_yes_no("Сохранить изменения (Д/н)(Y/n)? ", True):
                if notes_repo.update_note(note):
                    view.show(
                        f"Изменения заметки {note.id} успешно сохранены.")
                else:
                    view.show(f"Не удалось сохранить изменения заметки {note.id}!"
                              " Ошибка при работе с хранилищем.")
            else:
                view.show("Изменения отменены.")
        else:
            view.show("Редактирование отменено.")

        view.show(SHORT_HR)

        if not view.ask_yes_no("Редактировать другую заметку (д/Н)(y/N)? ", False):
            return

    note = __select_by_id("ЗАМЕТКИ: Редактирование", return_found=True)
    if not note:
        view.show("Редактирование отменено.")
        view.wait_to_proceed()
        return

    __edit(note)


def __delete(note: Optional[Note] = None):
    if note and note.id is not None:

        if view.ask_yes_no(f"Удалить заметку {note.id} (д/Н)(y/N)? ", False):
            if notes_repo.delete_note(note.id):
                view.show(f"Заметка {note.id} успешно удалена.")
            else:
                view.show(f"Не удалось удалить заметку {note.id}!"
                          " Ошибка при работе с хранилищем.")
        else:
            view.show("Удаление отменено.")

        view.show(SHORT_HR)

        if not view.ask_yes_no("Удалить другую заметку (д/Н)(y/N)? ", False):
            return

    note = __select_by_id("ЗАМЕТКИ: Удаление", return_found=True)
    if not note:
        view.show("Удаление отменено.")
        view.wait_to_proceed()
        return

    __delete(note)
