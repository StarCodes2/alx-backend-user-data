#!/usr/bin/env python3
"""
    Defines functions that hash a password and check if a string matches a
    hashed password.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Returns an encrypted string(password). """
    text = password.encode('utf-8')
    return bcrypt.hashpw(text, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validates if password matches the hashed password. """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
