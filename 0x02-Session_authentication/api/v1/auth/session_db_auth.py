#!/usr/bin/env python3
""" Defines the class SessionDBAuth. """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Defines methods that creates and save user sessions in a file. """
    def create_session(self, user_id=None):
        """ Creates a session. """
        if not user_id:
            return None

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession({"user_id": user_id,
                                    "session_id": session_id})
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
            Returns a user id by requesting UserSession in the database
            based on session_id.
        """
        if not session_id:
            return None
        print("Step 1")

        try:
            user_session = UserSession.search({"session_id": session_id})
        except KeyError:
            return None
        print("Step 2")
        print(user_session)
        if not user_session:
            return None
        print("Step 3")
        return user_session[0].user_id

    def destroy_session(self, request=None):
        """ Destroy session (Logout). """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        if not super().destroy_session(request):
            return False

        user_session = UserSession.search({"session_id": session_id})
        if not user_session or not user_session[0]:
            return False
        return user_session[0].remove()
