from domain.entities import Note
from .entities import MenuItem, MenuModel


class NoteViewModel:

    DIVIDER_THICK = '\u2550'
    DIVIDER_THIN = '\u2500'
    DT_FORMAT = '%Y-%m-%d %H:%M'

    def __init__(self, note: Note) -> None:
        header = f"\u25a4 Заметка {note.id} : {note.title}"
        c_datetime = f"Создана:             {note.creation_date.strftime(NoteViewModel.DT_FORMAT)}"
        m_datetime = f"Последнее изменение: {note.last_change_date.strftime(NoteViewModel.DT_FORMAT)}"
        body_lst = note.body.splitlines()
        max_len = max(max(map(len, body_lst)),
                      len(header), len(c_datetime), len(m_datetime))
        thick_div = NoteViewModel.DIVIDER_THICK*max_len
        thin_div = NoteViewModel.DIVIDER_THIN*max_len
        repr_lines = [thick_div, header, thin_div, c_datetime,
                      m_datetime, thin_div, note.body, thick_div]

        self.repr_str = '\n'.join(repr_lines)

    def __str__(self) -> str:
        return self.repr_str


class MenuViewModel:

    FRAME_H = '\u2501'
    FRAME_V = '\u2502'
    FRAME_TOP_L = '\u250d'
    FRAME_TOP_R = '\u2511'
    FRAME_BTM_L = '\u2515'
    FRAME_BTM_R = '\u2519'
    FRAME_MID_L = '\u251c'
    FRAME_MID_R = '\u2524'
    FRAME_MID_H = '\u2500'
    SEP = '\u25b8'
    PADDING = ' '

    def __init__(self, menu: MenuModel) -> None:
        c = MenuViewModel
        keys_max_len = max(len(c.key_to_str(k))
                           for k in menu.items.keys())
        names_max_len = max(len(str(v.name)) for v in menu.items.values())

        h_frame_width = len(c.PADDING)*4 \
            + len(c.SEP) \
            + keys_max_len+names_max_len

        repr_lines = [c.FRAME_TOP_L
                      + c.FRAME_H * h_frame_width
                      + c.FRAME_TOP_R]

        if menu.header:
            repr_lines.append(
                c.FRAME_V+menu.header.center(h_frame_width)+c.FRAME_V)
            repr_lines.append(
                c.FRAME_MID_L+c.FRAME_MID_H*h_frame_width+c.FRAME_MID_R)

        repr_lines.extend((c.FRAME_V+c.PADDING
                           + c.key_to_str(k).center(keys_max_len)
                           + c.PADDING+c.SEP+c.PADDING
                           + mi.name.ljust(names_max_len)
                           + c.PADDING + c.FRAME_V)
                          for k, mi in menu.items.items())

        repr_lines.append(c.FRAME_BTM_L
                          + c.FRAME_H * h_frame_width
                          + c.FRAME_BTM_R)

        self.repr_str = '\n'.join(repr_lines)

    @staticmethod
    def key_to_str(key):
        if isinstance(key, tuple):
            key_len = len(key)
            if key_len == 0:
                return ''
            else:
                res = str(key[0])
                if key_len == 1:
                    return res
                else:
                    return f"{res} ({', '.join(key[1:])})"

        return str(key)

    def __str__(self) -> str:
        return self.repr_str
