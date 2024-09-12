#!/usr/bin/env python3
""" Model to authenticate and register a user. """
import bcrypt
import uuid
from db import DB, User, NoResultFound


def _hash_password(password: str) -> bytes:
    """ Hashes a password. """
    if not password:
        return None
    text = password.encode()

    return bcrypt.hashpw(text, bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generate a uuid and return a string represenation of the uuid. """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """ Create a session. """
        if not email:
            return None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = str(uuid.uuid4())
        self._db.update_user(user.id, session_id=session_id)

        return session_id
