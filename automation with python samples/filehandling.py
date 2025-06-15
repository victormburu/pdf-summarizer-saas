#!/usr/bin/env python
def read_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
            return "File not found"
    finally:
            print("finished reading file")
