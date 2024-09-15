#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """ Sends a request to register a new user. """
    payload = {"email": email, "password": password}
    res = requests.post("http://localhost:5000/users", data=payload)
    j_res = res.json()
    assert res.status_code == 200, "error: {}".format(res.status_code)
    assert j_res["email"] == email, "Email should be {}".format(email)
    assert j_res["message"] == "user created", "Wrong message in json response"


def log_in_wrong_password(email: str, password: str) -> None:
    """ Logging in with the wrong password. """
    payload = {"email": email, "password": password}
    res = requests.post("http://localhost:5000/sessions", data=payload)
    assert res.status_code == 401, "error code: 401 expected got {}"\
        .format(res.status_code)


def log_in(email: str, password: str) -> str:
    """ Login with correct email. """
    payload = {"email": email, "password": password}
    res = requests.post("http://localhost:5000/sessions", data=payload)
    assert res.status_code == 200, "error: {}".format(res.status_code)
    return res.cookies["session_id"]


def profile_unlogged() -> None:
    """ Try to get a profile without logging in. """
    cookies = {"session_id": "Nope"}
    res = requests.get("http://localhost:5000/profile", cookies=cookies)
    assert res.status_code == 403, "error code: {}".format(res.status_code)


def profile_logged(session_id: str) -> None:
    """ View profile while logged in. """
    cookies = {"session_id": session_id}
    res = requests.get("http://localhost:5000/profile", cookies=cookies)
    assert res.status_code == 200, "error code: {}".format(res.status_code)


def log_out(session_id: str) -> None:
    """ Log out and destory session. """
    cookies = {"session_id": session_id}
    res = requests.delete("http://localhost:5000/sessions", cookies=cookies)
    assert res.status_code == 200, "error code: {}".format(res.status_code)


def reset_password_token(email: str) -> str:
    """ Get the user's password reset token. """
    payload = {"email": email}
    res = requests.post("http://localhost:5000/reset_password", data=payload)
    j_res = res.json()
    assert res.status_code == 200, "error: {}".format(res.status_code)
    assert j_res["email"] == email, "Email should be {}".format(email)
    return j_res["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update user password. """
    payload = {"email": email,
               "new_password": new_password,
               "reset_token": reset_token}
    res = requests.put("http://localhost:5000/reset_password", data=payload)
    j_res = res.json()
    assert res.status_code == 200, "error: {}".format(res.status_code)
    assert j_res.get("email") == email, "Email should be {}".format(email)
    assert j_res.get("message") == "Password updated",\
        "Wrong response message."


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
