#!/usr/bin/env python3
""" Model to authenticate and register a user. """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Hashes a password. """
    if not password:
        return None
    text = password.encode()

    return bcrypt.hashpw(text, bcrypt.gensalt())
