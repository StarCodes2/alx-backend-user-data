#!/usr/bin/env python3
"""
    Defines a class that creates and handles session id
    with expiration date.
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
        Defines methods and attributes to create and handle session id with
        expiration date.
    """
    def __init__(self):
        """ Initialise an instance. """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Creates a session id. """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Gets the user's id from a session id. """
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0 or\
             "user_id" not in self.user_id_by_session_id[session_id]:
            return self.user_id_by_session_id[session_id]["user_id"]
        if "created_at" not in self.user_id_by_session_id[session_id]:
            return None

        created_at = self.user_id_by_session_id[session_id]["created_at"]
        if created_at + timedelta(seconds=self.session_duration)\
                < datetime.now():
            return None

        return self.user_id_by_session_id[session_id]["user_id"]
