#!/usr/bin/env python3

from dumpreader import DumpReader
dr = DumpReader()
for statement in dr.read_statements('somestatements.sql'):
    print(statement)
