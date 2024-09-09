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

    def current_user(self, request=None):
        """ Returns the current user. """
        if request is None:
            return None
        cookie_id = self.session_cookie(request)
        if cookie_id is None:
            return None
        user_id = self.user_id_for_session_id(cookie_id)
        from models.user import User
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Deletes a user session(logout). """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False

        del self.user_id_by_session_id[session_id]
        return True
