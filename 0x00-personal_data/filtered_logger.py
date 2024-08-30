#!/usr/bin/env python3
""" Filtering and Logging data. """
import re
import logging
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection
from typing import List, Tuple

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


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
    logger.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(sh)
    return logger


def get_db() -> MySQLConnection:
    """
        Returns a connector to a database using credentails stored
        environment variables.
    """
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pass = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "holberton")

    conn = mysql.connector.connect(
        user=db_user,
        password=db_pass,
        host=db_host,
        database=db_name
    )
    return conn


def main() -> None:
    """
        Retrieve all rows from a table and log each row while filtering
        out sensitive information.
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    for row in rows:
        msg = "; ".join("{}={}".format(col, val)
                        for col, val in zip(cursor.column_names, row)) + ";"
        logger.info(msg)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
