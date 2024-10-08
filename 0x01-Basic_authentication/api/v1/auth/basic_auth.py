#!/usr/bin/env python3
""" Basic Authentication """
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Define methods to authenticate users using basic authentication. """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ To extract Base64 authentication string. """
        if authorization_header is None or type(authorization_header) != str:
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decodes a Base64 authentication string """
        if base64_authorization_header is None\
           or type(base64_authorization_header) != str:
            return None
        coded_str = base64_authorization_header.encode("utf-8")
        try:
            decoded_str = base64.b64decode(coded_str).decode("utf-8")
        except Exception:
            return None

        return decoded_str

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ To extract the user credentials from a string. """
        if decoded_base64_authorization_header is None\
                or type(decoded_base64_authorization_header) != str:
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        col_pos = decoded_base64_authorization_header.find(":")
        email = decoded_base64_authorization_header[:col_pos]
        pwd = decoded_base64_authorization_header[col_pos + 1:]
        return (email, pwd)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Checks if user with specified credentials exist. """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        use = User()  # To ensure that the class name is in the Dataset
        users = User.search({"email": user_email})
        if not users or len(users) == 0:
            return None
        if users[0] and users[0].is_valid_password(user_pwd):
            return users[0]

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the user instance if it exists in DB. """
        if not request:
            return None

        header = self.authorization_header(request)
        if header is None:
            return None

        b64_header = self.extract_base64_authorization_header(header)
        if b64_header is None:
            return None

        decoded = self.decode_base64_authorization_header(b64_header)
        if decoded is None:
            return None

        user_cred = self.extract_user_credentials(decoded)
        if user_cred[0] is None or user_cred[1] is None:
            return None

        return self.user_object_from_credentials(user_cred[0], user_cred[1])
