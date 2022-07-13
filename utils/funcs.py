import re
from functools import wraps
from os import environ

import jwt
from jwt import PyJWTError

from constants import MISSING_TOKEN, INVALID_TOKEN
from exceptions.exceptions import ValidationException
from flask import request, jsonify

from models.user import User


def password_check(password):
    if len(password) < 6 or len(password) > 12:
        raise ValidationException(
            "Password length should be at least 6 and at most 12 characters long"
        )
    elif not re.search(r"[a-z]", password):
        raise ValidationException("Password should include letters")
    elif not re.search(r"[0-9]", password):
        raise ValidationException("Password should include numbers")
    elif not re.search(r"[A-Z]", password):
        raise ValidationException("Password should include capital letters")
    elif not re.search(r"[$#@!]", password):
        raise ValidationException("Password should include unique symbols")
    elif re.search(r"\s", password):
        raise ValidationException("Password should contain any whitespace")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": MISSING_TOKEN}), 401

        try:
            data = jwt.decode(token, environ.get("SECRET_KEY"))
            current_user = User.query.filter_by(
                public_id=data["public_id"]).first()
        except PyJWTError:
            return jsonify({"message": INVALID_TOKEN}), 401
        return f(current_user, *args, **kwargs)

    return decorated
