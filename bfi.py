#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

import msvcrt


_helptext = """Brainfuck interpreter

Reference:
>  increment the data pointer (to point to the next cell to the right).
<  decrement the data pointer (to point to the next cell to the left).
+  increment (increase by one) the byte at the data pointer.
-  decrement (decrease by one) the byte at the data pointer.
.  output the byte at the data pointer.
,  accept one byte of input, storing its value in the byte at the data pointer.
[  if the byte at the data pointer is zero, then instead of moving the
   instruction pointer forward to the next command, jump it forward to the
   command after the matching ] command.
]  if the byte at the data pointer is nonzero, then instead of moving the
   instruction pointer forward to the next command, jump it back to the command
   after the matching [ command.
"""


class Processor:
    def __init__(self, ramsize=1024):
        self._mapping = {
            ">": self._incptr,
            "<": self._decptr,
            "+": self._incval,
            "-": self._decval,
            ".": self._output,
            ",": self._input,
            "[": self._loopstart,
            "]": self._loopend,
        }
        self._ramsize = ramsize
        self._reset()

    def run(self, program):
        self._reset()
        self._program = program
        proglen = len(program)
        while self._pc < proglen:
            try:
                self._mapping[program[self._pc]]()
            except KeyError:
                pass
            finally:
                self._pc += 1

    def _reset(self):
        self._ram = list([0] * self._ramsize)
        self._pointer = 0
        self._pc = 0

    def _incptr(self):
        self._pointer += 1

    def _decptr(self):
        self._pointer -= 1

    def _incval(self):
        self._ram[self._pointer] += 1

    def _decval(self):
        self._ram[self._pointer] -= 1

    def _output(self):
        byte = self._ram[self._pointer]
        print(chr(byte), end="")

    def _input(self):
        self._ram[self._pointer] = msvcrt.getch()[0]

    def _loopstart(self):
        self._setpc(True)

    def _loopend(self):
        self._setpc(False)

    def _setpc(self, isloopstart):
        if isloopstart:
            value = 1
            condition = self._ram[self._pointer] == 0
        else:
            value = -1
            condition = self._ram[self._pointer] != 0

        if condition:
            pc = self._pc
            program = self._program
            count = 1
            while count > 0:
                pc += value
                if program[pc] == "[":
                    count += value
                elif program[pc] == "]":
                    count -= value
            self._pc = pc


def main():
    args = sys.argv
    arglen = len(args)
    if arglen == 1:
        program = input("$ ")
    elif arglen == 2:
        with open(args[1], encoding="utf8") as f:
            program = f.read()
    else:
        print(_helptext)
        sys.exit(1)

    Processor().run(program)


if __name__ == "__main__":
    main()
