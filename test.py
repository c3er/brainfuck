#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json

import bfi


EXAMPLE_DIR = "examples"
EXAMPLES_FILE = "examples.json"


class Example:
    def __init__(self, filename, inputdata="", outputdata=""):
        self.filename = filename
        self.inputdata = inputdata
        self.outputdata = outputdata

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["file"],
            cls._tryaccess(d, "input"),
            cls._tryaccess(d, "output")
        )

    @staticmethod
    def _tryaccess(d, key):
        try:
            return d[key]
        except KeyError:
            return ""


def getscriptpath(script):
    return os.path.dirname(os.path.realpath(script))


def parse_json(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)
    return [Example.from_dict(d) for d in data["examples"]]


def run2msg(example, actual_output):
    succeeded = example.outputdata == actual_output
    inputdata = example.inputdata
    return "{}\nFile: {}\nOutput: {} {} {}\n{}".format(
        "OK" if succeeded else "FAIL",
        example.filename,
        example.outputdata,
        "==" if succeeded else "!=",
        actual_output,
        "(Input: {})\n".format(inputdata) if inputdata else ""
    )


def main():
    basepath = getscriptpath(__file__)
    example_dir = os.path.join(basepath, EXAMPLE_DIR)
    examples_file = os.path.join(basepath, EXAMPLES_FILE)

    processor = bfi.Processor(istest=True)
    examples = parse_json(examples_file)
    for example in examples:
        path = os.path.join(example_dir, example.filename)
        with open(path, encoding="utf8") as f:
            program = f.read()
        processor.run(program, example.inputdata)
        print(run2msg(example, processor.outputdata))


if __name__ == "__main__":
    main()
