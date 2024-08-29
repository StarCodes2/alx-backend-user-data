#!/usr/bin/env python3
""" Filtering and Logging data. """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns a log message obfuscated. """
    pattern = r'(' + r'|'.join(fields) + r')=(.*?)' + separator
    return re.sub(pattern, r'\1=' + redaction + separator, message)
