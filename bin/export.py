#!/usr/bin/env python

import sys
import json
import argparse

import phtest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="JSON file to export into")
    args = parser.parse_args()

    questions = phtest.db.get_all_questions()
    dump = [q.to_dict() for q in questions]

    try:
        json.dump(dump, open(args.output, "w"))
    except IOError as err:
        print(f"Could not write to '{err.filename}': {err.strerror}")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
