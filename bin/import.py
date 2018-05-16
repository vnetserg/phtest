#!/usr/bin/env python

import sys
import json
import argparse

import phtest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON file to import from")
    args = parser.parse_args()

    try:
        dump = json.load(open(args.input, "r"))
    except IOError as err:
        print(f"Could not read from '{err.filename}': {err.strerror}")
        sys.exit(1)

    questions = [phtest.db.Question.from_dict(d) for d in dump]
    phtest.db.save_question(questions)

if __name__ == "__main__":
    main()
