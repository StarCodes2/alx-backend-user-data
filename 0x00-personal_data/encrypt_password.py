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
