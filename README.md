# DumpReader

Reads MYSQL dump file and yields back the statements one at a time.  Automatically skips comments and
keeps multi-line statements together.

This is a decent use case of a [generator function](https://wiki.python.org/moin/Generators).
You typically want to execute these statements right away.  Read as many as you want from a
file for very little memory cost.

## Example Usage

```python
from dumpreader import DumpReader
dr = DumpReader()
for statement in dr.read_statements('somestatements.sql'):
  print(statement)
```

## License

The MIT License (MIT)

Copyright (c) 2018 Micah Brandon &lt;brandon@netsville.com&gt;

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

