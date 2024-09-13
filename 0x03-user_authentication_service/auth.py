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

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Search for a user using session id. """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: str) -> None:
        """ Delete a session/logout. """
        if not user_id:
            return None

        try:
            self._db.update_user(user_id, session_id=None)
        except (NoResultFound, ValueError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Generate a password reset token. """
        if not email:
            return None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update a user's password. """
        if not reset_token or not password:
            raise ValueError
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        self._db.update_user(user.id, reset_token=None,
                             hashed_password=_hash_password(password))
