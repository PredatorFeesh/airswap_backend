from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
)
from flask_cors import CORS
from werkzeug.security import safe_str_cmp


import models


app = Flask(__name__)
app.config["DEBUG"] = True
app.config[
    "JWT_SECRET_KEY"
] = "*&F78gg7878SG787g787&*G8gG**(G^*(&*G8gg78;l[po[[oin9h])23g.[.]"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///airswap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)

jwt = JWTManager(app)

db = SQLAlchemy(app)


@app.route("/register", methods=["POST"])
def register():
    request_json = request.json

    if (
        request_json is None
        or request_json["email"] is None
        or request_json["password"] is None
        or request_json["name"] is None
    ):
        return jsonify({"err_type": "credentials", "err_msg": "empty"}), 400

    email = request_json["email"]
    password = request_json["password"]
    name = request_json["name"]

    # Now we need to split first and second.
    first, second = name.split(" ")

    # Check whether user is in our database
    user_db = models.User.query.filter_by(email=email).first()
    if user_db is not None:
        return jsonify({"err_type": "user", "err_msg": "exists"}), 400

    # Now add the user to the database
    # @IFTIME: Encrypt password
    user_db = models.User(email, password, first, second)
    db.session.add(user_db)
    db.session.commit()

    access_token = create_access_token(identity={"id": user_db.id})
    refresh_token = create_refresh_token(identity={"id": user_db.id})

    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@app.route("/login", methods=["POST"])
def login():
    request_json = request.json

    if (
        request_json is None
        or request_json["email"] is None
        or request_json["password"] is None
    ):
        return jsonify({"err_type": "credentials", "err_msg": "empty"}), 400

    email = request_json["email"]
    password = request_json["password"]

    # The other fields for user as set in the Profile
    user = models.User.query.filter_by(email=email, password=password).first()

    # If we have no user
    if user is None:
        return jsonify({"err_type": "auth", "err_msg": "bad login"}), 400

    access_token = create_access_token(identity={"id": user.id})
    refresh_token = create_refresh_token(identity={"id": user.id})

    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@app.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    uid = get_jwt_identity()["id"]
    return jsonify({"access_token": create_access_token(identity=uid)}), 200


# @TODO REMOVE THIS. Keeping it temporarily for reference
@app.route("/test", methods=["POST"])
@jwt_required
def test():
    print(get_jwt_identity())
    return "Secret"


@app.route("/", methods=["GET"])
def home():
    return "Welcome home!"


if __name__ == "__main__":
    app.run(port=5001)
