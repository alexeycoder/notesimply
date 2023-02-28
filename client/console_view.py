
import os
import sys
from typing import Callable, Iterable, AbstractSet, Optional

PROMPT_ENTER = "\nНажмите Ввод чтобы продолжить..."
PLEASE_REPEAT = "Пожалуйста попробуйте снова."
WARN_WRONG_MENU_ITEM = "Некорректный ввод: требуется выбрать пункт меню. "
N_RETURNS_TO_FINISH_MULTILINE = 3
HOW_TO_FINISH_MULTILINE = "Три пустые строки подряд завершают ввод!"
MULTILINE_PROMPT_SIGN = "\u276f"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def wait_to_proceed():
    input(PROMPT_ENTER)


def show(view_model=None):
    if view_model:
        print(view_model)
    else:
        print()


def show_list(lst: Iterable, title: str):
    ...


def ask_yes_no(prompt: str, is_yes_default: bool) -> bool:
    answer = input(prompt).strip()

    if not answer:
        return is_yes_default

    answer = answer.lower()
    if answer.startswith('y') or answer.startswith('д'):
        return True
    elif answer.startswith('n') or answer.startswith('н'):
        return False
    else:
        return is_yes_default


def ask_user_choice(prompt: str, options: AbstractSet):

    def find_appropriate(raw: str):
        raw = raw.lower()
        for opt in options:
            if isinstance(opt, tuple):
                if raw in (str(o).lower() for o in opt):
                    return opt
            if raw == opt:
                return opt
        return None

    out_of_range = False

    while True:
        if out_of_range:
            out_of_range = False
            print(WARN_WRONG_MENU_ITEM, file=sys.stderr)

        raw_choice = input(prompt)
        related_option = find_appropriate(raw_choice)
        if related_option:
            return related_option

        out_of_range = True


def ask_integer_in_range(prompt: str, min: int, max: int):
    ...


def ask_integer(prompt: str, check_validity: Callable[[int], bool], wrong_msg):
    ...


def ask_string(prompt: str, check_validity: Optional[Callable[[str], bool]] = None, warn_wrong: Optional[str] = None):
    out_of_range = False

    while True:
        if out_of_range:
            out_of_range = False
            if warn_wrong:
                print(warn_wrong, file=sys.stderr)

        inp = input(prompt)
        if check_validity is None or check_validity(inp):
            return inp

        out_of_range = True


def ask_multiline_text(prompt: str):
    print(prompt)
    print(HOW_TO_FINISH_MULTILINE)
    print()

    lines = []
    returns_count = 0
    while returns_count < N_RETURNS_TO_FINISH_MULTILINE:
        print(MULTILINE_PROMPT_SIGN, end='')
        line = input()
        lines.append(line)
        if line == '':
            returns_count += 1
        else:
            returns_count = 0

    return '\n'.join(lines[:-3])
