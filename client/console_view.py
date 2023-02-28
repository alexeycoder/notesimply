
import os
from typing import Callable, Iterable, AbstractSet


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def wait_to_proceed():
    ...


def show(view_model):
    print(view_model)



def show_list(lst: Iterable, title: str):
    ...


def ask_yes_no(prompt: str, is_yes_default: bool) -> bool:
    ...


def ask_user_choice(prompt: str, options: AbstractSet):
    ...


def ask_integer_in_range(prompt: str, min: int, max: int):
    ...


def ask_integer(prompt: str, check_validity: Callable[[int], bool], wrong_msg):
    ...


def ask_string(prompt: str, check_validity: Callable[[str], bool], wrong_msg):
    ...
