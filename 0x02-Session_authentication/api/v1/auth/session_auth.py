#!/usr/bin/env python3
""" Session Authentication """
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ Define methods to authenticate users using session authentication. """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session id for a given user. """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a user id based on a session id. """
        if session_id is None and not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)