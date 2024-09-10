#!/usr/bin/env python3
""" Defines the UserSession class. """
from models.base import Base


class UserSession(Base):
    """ Defines method to create and save session. """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialise a new instance. """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
