import os
import sys
from typing import AbstractSet, Callable, Optional

PROMPT_ENTER = "\nНажмите Ввод чтобы продолжить..."
PLEASE_REPEAT = "Пожалуйста попробуйте снова."

WARN_WRONG_MENU_ITEM = "Некорректный ввод: требуется выбрать пункт меню. "

N_RETURNS_TO_FINISH_MULTILINE = 3
HOW_TO_FINISH_MULTILINE = "Три пустые строки подряд завершают ввод!"
MULTILINE_PROMPT_SIGN = "\u276f"

ERR_NOT_INT = "Некорректный ввод: Требуется целое число. " + PLEASE_REPEAT
ERR_INT_MUST_BE_IN_RANGE = "Число должно быть в интервале от {} до {}! " + PLEASE_REPEAT
ERR_INT_TOO_LOW = "Число не должно быть меньше {}! " + PLEASE_REPEAT
ERR_INT_TOO_HIGH = "Число не должно быть больше {}! " + PLEASE_REPEAT


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def safe_input(prompt=None) -> str:
    try:
        if prompt is None:
            return input()
        else:
            return input(prompt)
    except EOFError:
        exit(1)
    except Exception:
        print(("Предупреждение: Возникло исключение при обработке ввода."
              "Возможно эмулятор терминала не настроен для работы в кодировке utf-8."),
              file=sys.stderr)
        return ''


def wait_to_proceed():
    safe_input(PROMPT_ENTER)


def show(view_model=None):
    if view_model:
        print(view_model)
    else:
        print()


def ask_yes_no(prompt: str, is_yes_default: bool) -> bool:
    answer = safe_input(prompt).strip()

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
            if raw == str(opt).lower():
                return opt
        return None

    out_of_range = False

    while True:
        if out_of_range:
            out_of_range = False
            print(WARN_WRONG_MENU_ITEM, file=sys.stderr)

        raw_choice = safe_input(prompt)
        if not raw_choice:
            out_of_range = True
            continue

        related_option = find_appropriate(raw_choice)
        if related_option is not None:
            return related_option

        out_of_range = True


def is_out_of_range(value: int, min: Optional[int], max: Optional[int]):
    return (min is not None and value < min) or (max is not None and value > max)


def ask_integer_in_range(prompt: str, min: Optional[int] = None, max: Optional[int] = None) -> Optional[int]:
    wrong_type = False
    out_of_range = False

    while True:
        if wrong_type:
            wrong_type = False
            print(ERR_NOT_INT, file=sys.stderr)
        if out_of_range:
            out_of_range = False
            err_msg: str
            if min is not None and max is not None:
                err_msg = ERR_INT_MUST_BE_IN_RANGE.format(min, max)
            elif min is not None:
                err_msg = ERR_INT_TOO_LOW.format(min)
            else:
                err_msg = ERR_INT_TOO_HIGH.format(max)
            print(err_msg, file=sys.stderr)

        try:
            raw_inp = input(prompt)
            if not raw_inp:
                return None

            num = int(raw_inp)
            out_of_range = is_out_of_range(num, min, max)
            if not out_of_range:
                return num

        except:
            wrong_type = True


def ask_string(prompt: str, check_validity: Optional[Callable[[str], bool]] = None, warn_wrong: Optional[str] = None):
    out_of_range = False

    while True:
        if out_of_range:
            out_of_range = False
            if warn_wrong:
                print(warn_wrong, file=sys.stderr)

        inp = safe_input(prompt)
        if (not inp) or check_validity is None or check_validity(inp):
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
        line = safe_input()
        lines.append(line)
        if line == '':
            returns_count += 1
        else:
            returns_count = 0

    return '\n'.join(lines[:-3])
