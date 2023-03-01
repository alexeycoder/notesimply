import re
from client.view_models import MenuViewModel
from client import view_models, controller
from client.entities import MenuItem, MenuModel


if __name__ == '__main__':
    # t = ('0',)
    # print(t)
    # print(type(t))
    # print(isinstance(t, tuple))

    # mvm = MenuViewModel
    # print(mvm.key_to_str(('0',)))
    # print(mvm.key_to_str(('й', 'q')))
    # print(mvm.key_to_str(('й', 'q', 'фы')))

    # menu_as_str_pairs = tuple((mvm.key_to_str(k), v)
    #                           for k, v in controller.MAIN_MENU.items.items())
    # print(menu_as_str_pairs)
    # print("=====")
    # print(max(map(lambda t: len(t[0]), menu_as_str_pairs)))
    # print(max(len(pair[0]) for pair in menu_as_str_pairs))
    # print(max(map(lambda t: len(t[1]), menu_as_str_pairs)))

    # menu = controller.MAIN_MENU
    # print(max(len(mvm.key_to_str(k)) for k in menu.items.keys()))

    # print("=====")
    # print(view_models.MenuViewModel(menu))

    res = re.fullmatch("^\\d{4}-([0][1-9]|1[0-2])-([0-2][1-9]|[1-3]0|3[01])$", "2023-02-01")
    print(res)
