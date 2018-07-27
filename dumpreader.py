#!/usr/bin/env python3
import os
import sys
import re

class DumpReader:
    """ Reads MYSQL dump file and yields back the statements one at a time 

        from dumpreader import DumpReader
        dr = DumpReader()
        for statement in dr.read_statements('mysqldump.sql'):
            print(statement)

    """
    def __init__(self, bufsize = 4096):
        self.bufsize = bufsize

    def _readchunk_file(self):
        with open(self.dumpfile, 'r') as f:
            chunk = f.read(self.bufsize)
            while chunk:
                yield chunk  # ret. generator then continues...
                chunk = f.read(self.bufsize)

    def _readchar_chunks(self):
        for chunk in self._readchunk_file():
            for char in chunk:
                yield char  # ret. generator then continues...

    def read_statements(self, dumpfile):
        self.dumpfile = dumpfile
        newbuff = ''
        lastchar = ''
        idx_in_line = 0
        SKIP_TILL_EOL = False
        IN_COMMENT = False
        DISABLE_SEMICOLON = False
        IN_SINGLE_QUOTE = False
        IN_DOUBLE_QUOTE = False
        IN_BACK_QUOTE = False
        re_space = re.compile(r'\s+')
        for char in self._readchar_chunks():
            if SKIP_TILL_EOL: # eats chars. till '\n'
                if char == '\n':
                    lastchar = char
                    SKIP_TILL_EOL = False
                continue
            if IN_COMMENT: # eats EVERYTHING till a close comment
                if lastchar+char == '*/':
                    IN_COMMENT = False
                lastchar = char
                continue

            # single quote end check
            if IN_SINGLE_QUOTE and (char == '\''):
                newbuff+=char
                lastchar = char
                idx_in_line+=1
                IN_SINGLE_QUOTE = False
                DISABLE_SEMICOLON = False
                continue

            # double quote end check
            if IN_DOUBLE_QUOTE and (char == '"'):
                newbuff+=char
                lastchar = char
                idx_in_line+=1
                IN_DOUBLE_QUOTE = False
                DISABLE_SEMICOLON = False
                continue

            # back quote end check
            if IN_BACK_QUOTE and (char == '`'):
                newbuff+=char
                lastchar = char
                idx_in_line+=1
                IN_BACK_QUOTE = False
                DISABLE_SEMICOLON = False
                continue

            # eats blank spaces and spaces at beg-of-line
            if ((idx_in_line == 0 or lastchar == '\n') and re_space.match(char) and
                (not IN_SINGLE_QUOTE and not IN_DOUBLE_QUOTE and not IN_BACK_QUOTE)):
                continue

            # slurp a character into the buffer
            newbuff+=char

            # single quote check
            if (not IN_SINGLE_QUOTE) and (len(newbuff) > 1) and (char == '\''):
                IN_SINGLE_QUOTE = True
                DISABLE_SEMICOLON = True

            # double quote check
            if (not IN_DOUBLE_QUOTE) and (len(newbuff) > 1) and (char == '"'):
                IN_DOUBLE_QUOTE = True
                DISABLE_SEMICOLON = True

            # back quote check
            if (not IN_BACK_QUOTE) and (len(newbuff) > 1) and (char == '`'):
                IN_BACK_QUOTE = True
                DISABLE_SEMICOLON = True

            # semicolon ends newbuff and yields statement back (unless disabled by IN_*_QUOTE)
            if char == ';' and not DISABLE_SEMICOLON:
                if len(newbuff) > 1:
                    yield newbuff
                newbuff = ''
                idx_in_line = 0
                continue

            # checks for '--' or '/*' comment lines
            if idx_in_line == 1:
                if newbuff == '--':
                    newbuff = ''
                    idx_in_line = 0
                    SKIP_TILL_EOL = True
                    continue
                if newbuff == '/*':
                    newbuff = ''
                    idx_in_line = 0
                    IN_COMMENT = True
                    continue

            lastchar = char
            idx_in_line+=1
