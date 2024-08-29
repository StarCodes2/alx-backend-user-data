#!/usr/bin/env python3
""" Filtering and Logging data. """
import re
import logging
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
        return rec


def get_logger() -> logging.Logger:
    """ Returns a logger. """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(fields))
    logger.addHandler(sh)
    return logger
