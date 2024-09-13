#!/usr/bin/env python3
""" Flask App """
from auth import Auth
from flask import Flask, abort, make_response, redirect, request, jsonify
from flask import url_for
app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """ Returns a payload. """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def req_user():
    """ Register a new user. """
    if not request.form:
        return jsonify({"error": "missing form data"}), 400
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "missing email"}), 400
    if not password:
        return jsonify({"error": "missing password"}), 400

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": user.email, "message": "user created"}), 200


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """ Login using form data. """
    if not request.form:
        return jsonify({"error": "missing form data"}), 400

    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "missing email"}), 400
    if not password:
        return jsonify({"error": "missing password"}), 400

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
    else:
        abort(401)

    res = make_response({"email": email, "message": "logged in"})
    res.set_cookie("session_id", session_id)
    return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """ Log a user out. """
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return jsonify({"error": "missing data"}), 403
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("home"))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """ Returns a user's profile. """
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return jsonify({"error": "Forbidden"}), 403
    print("step 1")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return jsonify({"error": "Forbidden"}), 403
    return jsonify({"email": user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
