#!/usr/bin/env python3

from abc import ABC, abstractmethod
import sys


class LineInterpreter(ABC):
    '''
    Интерпретатор произвольного языка c 1 операцией на строку
    '''

    def __init__(self, source_file_name: str) -> None:
        '''
        Создать интерпретатор для данного исходного файла

        :param str source_file_name: Имя исходного файла
        '''
        self.source_file_name: str = source_file_name
        with open(source_file_name, 'r', encoding='utf8') as source_file:
            self._lines: list[str] = [l.rstrip() for l in source_file]
        self._current_line_idx: int = 0 if len(self._lines) else -1
        if len(self._lines) == 0:
            self.quit(f"Empty source file: {source_file_name}")

    def quit(self, message: str = ""):
        '''
        Завершить работу интерпретатора
        '''
        if message != "":
            print(message, file=sys.stderr)
        sys.exit(0)

    def current_line(self) -> str:
        if not (0 <= self._current_line_idx < len(self._lines)):
            self.quit("Program is over")
        return self._lines[self._current_line_idx]

    def abs_jump(self, line_no: int) -> None:
        self._current_line_idx = line_no

    def rel_jump(self, offset: int) -> None:
        self._current_line_idx += offset

    def step(self) -> None:
        self.rel_jump(1)

    @abstractmethod
    def execute_current_line(self) -> None:
        ...

    def run(self) -> None:
        while True:
            self.execute_current_line()
            self.step()


class NedoForth(LineInterpreter):
    def __init__(self, source_file_name: str) -> None:
        super().__init__(source_file_name)
        self.stack: list[float] = []

    def execute_current_line(self) -> None:
        # print(f"{self._current_line_idx}: {self.current_line()}")
        l = self.current_line()

        if len(l) == 0 or l.startswith('#'):
            return  # Пустая строка или комментарий или shebang
        else:
            match l:
                case 'стек' | 'stack':
                    print(self.stack)
                case 'вершина' | 'top':
                    print(self.stack[-1])
                case 'ввод' | 'input':
                    self.stack.append(float(input()))
                case '+':
                    y = self.stack.pop()
                    x = self.stack.pop()
                    self.stack.append(x + y)
                case other:
                    self.stack.append(float(l))


if __name__ == '__main__':
    fi = NedoForth(sys.argv[1])
    fi.run()
