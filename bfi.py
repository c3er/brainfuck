#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Brainfuck interpreter

Usage:

bfi
Type in the program to eecute directly.

bfi <file>
The program to execute will be read from the given file.

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


import sys

import msvcrt


class Processor:
    def __init__(self, ramsize=30000, istest=False):
        self._operation_mapping = {
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
        self._prepare_testing(istest)

    def run(self, program, inputdata=""):
        self._reset(inputdata)
        self._brace_mapping = self._get_braces(program)
        proglen = len(program)
        while self._pc < proglen and not self._halted:
            try:
                self._operation_mapping[program[self._pc]]()
            except KeyError:
                pass
            finally:
                self._pc += 1
        self.halt()

    def halt(self):
        self._halted = True

    def _reset(self, inputdata=""):
        self._ram = [0] * self._ramsize
        self._pointer = 0
        self._pc = 0
        self._halted = False

        # Testing related
        self._inputdata = inputdata
        self._inputindex = 0
        self.outputdata = ""

    def _prepare_testing(self, istest):
        self._istest = istest

    @staticmethod
    def _get_braces(program):
        opening_braces = []
        brace_mapping = {}
        for i, c in enumerate(program):
            if c == "[":
                opening_braces.append(i)
            elif c == "]":
                matching_brace = opening_braces.pop()
                brace_mapping[matching_brace] = i
                brace_mapping[i] = matching_brace
        return brace_mapping

    def _incptr(self):
        self._pointer += 1

    def _decptr(self):
        self._pointer -= 1

    def _incval(self):
        self._ram[self._pointer] += 1

    def _decval(self):
        self._ram[self._pointer] -= 1

    def _output(self):
        char = chr(self._ram[self._pointer])
        if self._istest:
            self.outputdata += char
        else:
            print(char, end="")

    def _input(self):
        if self._istest:
            try:
                byte = ord(self._inputdata[self._inputindex])
                self._inputindex += 1
            except IndexError:
                self.halt()
                return
        else:
            byte = msvcrt.getch()[0]
            if byte == 13:
                # Most Brainfuck programs expect value 10 as newline character
                byte = 10
            elif byte == 3:
                # Ctrl+C was pressed
                raise KeyboardInterrupt()
        self._ram[self._pointer] = byte

    def _loopstart(self):
        self._setpc(True)

    def _loopend(self):
        self._setpc(False)

    def _setpc(self, isloopstart):
        if (self._ram[self._pointer] == 0) == isloopstart:
            self._pc = self._brace_mapping[self._pc]


def main():
    args = sys.argv
    arglen = len(args)
    if arglen == 1:
        program = input("$ ")
    elif arglen == 2:
        with open(args[1], encoding="utf8") as f:
            program = f.read()
    else:
        print(__doc__)
        sys.exit(1)

    Processor().run(program)


if __name__ == "__main__":
    main()
