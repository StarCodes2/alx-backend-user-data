#!/usr/bin/env python3
""" Basic Authentication """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Define methods to authrnticate users using basic authentication. """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ To extract Base64 authentication string. """
        if authorization_header is None or type(authorization_header) != str:
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]
