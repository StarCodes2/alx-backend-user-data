#!/usr/bin/env python3
""" User authentication model. """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Defines methods for user authentication. """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require authenticaion. """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        new_path = path
        if new_path[-1] == "/":
            new_path = new_path[:-1]
        else:
            new_path = new_path + "/"

        if path in excluded_paths or new_path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Checks the request header for authentication. """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get current user. """
        return None
