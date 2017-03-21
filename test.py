#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import unittest

import bfi


class Example:
    def __init__(self, expected, inputdata):
        self.expected = expected
        self.inputdata = inputdata


def getscriptpath(script):
    return os.path.dirname(os.path.realpath(script))


EXAMPLE_DIR = "examples"


examples = {
    "hello1.bf": Example("Hello World!\n", ""),
    "hello2.bf": Example("Hello World!\n", ""),
    "add-to-7.bf": Example("7", ""),
    "rot13.bf": Example("Uryyb Jbeyq!", "Hello World!"),
}


class BasicTests(unittest.TestCase):
    def setUp(self):
        self._processor = bfi.Processor(istest=True)

    def test_examples(self):
        basepath = getscriptpath(__file__)
        example_dir = os.path.join(basepath, EXAMPLE_DIR)
        for file in os.listdir(example_dir):
            path = os.path.join(example_dir, file)
            with open(path, encoding="utf8") as f:
                program = f.read()
            example = examples[file]
            self._processor.run(program, example.inputdata)
            print(self._processor._outputdata)
            self.assertEqual(self._processor._outputdata, example.expected)


def main():
    unittest.main(verbosity=1)


if __name__ == "__main__":
    main()
