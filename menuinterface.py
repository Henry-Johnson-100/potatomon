from os import name as os_name
from os import system
from typing import Any


def clear() -> None:
    clear_string = {
        "nt": "cls",
        "posix": "clear"
    }.setdefault(os_name, "clear")
    system(clear_string)


class MenuLine:
    def __init__(self, line_obj: Any, pad_delimiter: str = " ", length_to_pad_rear: int = 120, length_to_pad_front: int = 0):
        self.line_obj = line_obj
        self.pad_delimiter = pad_delimiter
        self.length_to_pad_rear = length_to_pad_rear
        self.length_to_pad_front = length_to_pad_front

    def __pad_menu_element(self, str_to_pad: str):
        padded_str = f"|{str().join([self.pad_delimiter * self.length_to_pad_front])}{str_to_pad}"
        while len(padded_str) < self.length_to_pad_rear:
            padded_str += self.pad_delimiter
        padded_str += "|"
        return padded_str

    def __str__(self):
        return self.__pad_menu_element(str(self.line_obj))


class Menu:
    def __init__(self):
        self.__menu_width = 120
        self.menu_lines = list()
        self.len_of_static_menu = int()
        self.append(self.__get_menu_header())
        self.append("")
        self.append(self.__get_menu_header())
        self.staticise()

    def __get_menu_header(self) -> str:
        return "".join(["-"] * (self.__menu_width - 1))

    def set_menu_width(self, width: int) -> None:
        self.__menu_width = width

    def append(self, line_obj: Any, **kwargs) -> None:
        self.menu_lines.append(self.__new_menu_line(line_obj, **kwargs))

    def write_line(self, line_object: Any, **kwargs) -> None:
        self.menu_lines.insert(-1, self.__new_menu_line(line_object, **kwargs))

    def write_lines(self, lines: list[Any]) -> None:
        for line in lines:
            self.write_line(line)

    def clear_text(self) -> None:
        self.menu_lines = self.menu_lines[0:self.len_of_static_menu]
        self.menu_lines.append(self.menu_lines[0])

    def update_menu(self):
        clear()
        print(self)

    def staticise(self):
        self.len_of_static_menu = len(self.menu_lines) - 1

    def choose_from_list(self, choices: list[Any]) -> Any:
        index_iter = 1
        for choice_option in choices:
            self.write_line(f"{index_iter}: {str(choice_option)}")
            index_iter += 1
        choice = "0"
        while not choice.isnumeric() or int(choice) not in range(1, len(choices) + 1):
            self.update_menu()
            choice = input()
        return choices[int(choice) - 1]

    def prompt_for_continue(self):
        self.write_line("")
        self.write_line("...")
        self.update_menu()
        _ = input("Press ENTER to continue")

    def __new_menu_line(self, line_obj: Any, **kwargs) -> MenuLine:
        return MenuLine(line_obj, **kwargs, length_to_pad_rear=self.__menu_width)

    def __getitem__(self, key):
        return self.menu_lines[key]

    def __str__(self) -> str:
        return "\n".join([str(x) for x in self.menu_lines])


if __name__ == "__main__":
    test = Menu()
    test.prompt_for_continue()
