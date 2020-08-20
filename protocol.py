"""
This protocol allows to format a data in the form of a string, keeping track of the original data type.

Supported data types are:
- Integer
- String

The resulting string (from now on "packet") is made of two parts:
-----------------
| HEADER | DATA |
-----------------

The HEADER contains an identifier for the original data type, while the DATA field contains the original data.
The HEADER values are:
-------------------
|  TYPE   | VALUE |
-------------------
| Integer |   i   |
| String  |   s   |
-------------------

EXAMPLES:
123   -> "i123"
"123" -> "s123"
"foo" -> "sfoo"
"""

DTYPEREFS = {
    "<class 'int'>": 'i',
    "<class 'str'>": 's'
}

DTYPEREVS = {
    'i': int,
    's': str
}

def encode(data):
    dtype = str(type(data))
    if not dtype in DTYPEREFS:
        raise Exception(f'Type {dtype} not suported')
    return f'{DTYPEREFS[dtype]}{data}'


def decode(payload):
    header = payload[0]
    if not header in DTYPEREVS:
        raise Exception(f'Header {header} not suported')
    return DTYPEREVS[header](payload[1:])