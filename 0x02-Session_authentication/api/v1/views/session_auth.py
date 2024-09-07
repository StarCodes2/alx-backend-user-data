#!/usr/bin/env python3
""" Handles all routes for session authentication. """
from api.v1.views import app_views
from flask import jsonify, make_response, request
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def sessionLogin():
    """ Handles session login. """
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400
    from models.user import User
    user = User.search({"email": email})
    if not user or not user[0]:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    SESSION_NAME = os.getenv("SESSION_NAME")
    resp = make_response(user[0].to_json())
    resp.set_cookie(SESSION_NAME, session_id)

    return resp
