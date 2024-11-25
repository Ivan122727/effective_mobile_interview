import os
import platform
import shutil
from .router import Router

class CommandInterFaceRouter(Router):
    def __init__(self):
        super().__init__()

    def print_centered(self, text: str):
        """Метод для печати текста по середине экрана

        Args:
            text (str): текст для печати
        """
        terminal_size = shutil.get_terminal_size()
        width = terminal_size.columns
        centered_text = text.center(width)
        print(centered_text)

    def clear_console(self):
        """Метод для очистки экрана"""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')