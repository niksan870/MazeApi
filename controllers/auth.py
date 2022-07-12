import uuid
from datetime import datetime, timedelta
from os import environ

import jwt
from flask import Blueprint
from flask import request, jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash

from db.database import db
from dtos.mappers import UserMapper
from models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def signin():
    auth = request.json

    if not auth or not auth.get("name") or not auth.get("password"):
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm ="Login required !!"'},
        )

    user = User.query.filter_by(name=auth.get("name")).first()

    if not user:
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm ="User does not exist !!"'},
        )

    if check_password_hash(user.password, auth.get("password")):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.utcnow() + timedelta(minutes=30),
            },
            environ.get("SECRET_KEY"),
        )

        return make_response(jsonify({"token": token.decode("UTF-8")}), 201)

    return make_response(
        "Could not verify",
        403,
        {"WWW-Authenticate": 'Basic realm ="Wrong Password !!"'},
    )


@auth.route("/user", methods=["POST"])
def signup():
    mapped_user = UserMapper.map_2_dto(request.json)

    if not User.query.filter_by(name=mapped_user.name).first():
        user = User(
            public_id=str(uuid.uuid4()),
            name=mapped_user.name,
            password=generate_password_hash(mapped_user.password),
        )
        db.session.add(user)
        db.session.commit()

        return make_response("Successfully registered.", 201)
    return make_response("User already exists. Please Log in.", 202)
