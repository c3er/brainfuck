#!/usr/bin/env python
# -*- coding: utf-8 -*-


import bfi

import unittest


examples = [
"++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.",
]


class BasicTests(unittest.TestCase):
    def setUp(self):
        self._processor = bfi.Processor()


def main():
    unittest.main()


if __name__ == "__main__":
    main()
