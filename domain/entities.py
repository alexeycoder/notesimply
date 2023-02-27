import textwrap
from datetime import datetime
from typing import Optional


class Note:
    def __init__(self, id: Optional[int], creation_date: datetime, last_change_date: datetime,  title: str,  body: str) -> None:
        self.id = id
        self.creation_date = creation_date
        self.last_change_date = last_change_date
        self.title = title
        self.body = body

    def __str__(self) -> str:
        return (f"Note {self.id}: \"{self.title}\""
                f"\nCreated: {self.creation_date}"
                f"\nChanged: {self.last_change_date}"
                f"\n\"{self.body}\""
                )


test_note = Note(123, datetime.today(), datetime.now(), "Тестовая заметка",
                 textwrap.dedent("""\
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                    Tenetur accusamus optio ipsum voluptatibus commodi
                    ad nihil numquam dolorum asperiores!
                    Nesciunt expedita possimus recusandae alias numquam
                    maiores, impedit illo corporis eveniet."""))


if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(test_note)
