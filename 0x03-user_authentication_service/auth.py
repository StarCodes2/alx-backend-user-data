#!/usr/bin/env python3
""" Model to authenticate and register a user. """
import bcrypt
from db import DB, User, NoResultFound


def _hash_password(password: str) -> bytes:
    """ Hashes a password. """
    if not password:
        return None
    text = password.encode()

    return bcrypt.hashpw(text, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user if email doesn't exist in the database. """
        if not email or not password:
            return None
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if a login credential is valid. """
        if not email or not password:
            return False

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode(), user.hashed_password)
