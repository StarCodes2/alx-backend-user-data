#!/usr/bin/env python3
""" Basic Authentication """
import base64
from api.v1.auth.auth import Auth


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
            decoded_str = base64.b64decode(coded_str)
        except Exception:
            return None

        return decoded_str.decode("utf-8")

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ To extract the user credentials from a string. """
        if decoded_base64_authorization_header is None\
                or type(decoded_base64_authorization_header) != str:
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        new_split = decoded_base64_authorization_header.split(":")
        return (new_split[0], new_split[1])
