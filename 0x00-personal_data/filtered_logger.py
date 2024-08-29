#!/usr/bin/env python3
""" Filtering and Logging data. """
import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns a log message obfuscated. """
    pattern = r'(' + r'|'.join(fields) + r')=(.*?)' + separator
    return re.sub(pattern, r'\1=' + redaction + separator, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self._fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Returns a string of redacted log records. """
        rec = filter_datum(self._fields, self.REDACTION,
                           super().format(record), self.SEPARATOR)
        return re.sub(r'' + self.SEPARATOR, self.SEPARATOR + " ", rec)
