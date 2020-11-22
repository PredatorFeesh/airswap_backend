from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////airswap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["DEBUG"] = True
app.config[
    "SECRET_AUTH"
] = "*&F78gg7878SG787g787&*G8gG**(G^*(&*G8gg78;l[po[[oin9h])23g.[.]"

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    email = db.Column("email", db.String())
    password = db.Column("password")

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.route("/login", methods=["POST"])
def login():
    request_json = request.get_json()

    email = request_json["email"]
    password = request_json["password"]

    if email is None:
        return {"err_type": "email", "err_msg": "empty"}
    if password is None:
        return {"err_type": "password", "err_msg": "empty"}

    # Otherwise now we want to actually verify

    # @TODO: GET ALL USERS AND ACTUALLY VERIFY VIA THE DATABASE HERE

    # @TODO: END CHECKING THE DATABASE
    # Otherwise, user auth failed!
    return {"err_type": "auth", "err_msg": "failed"}


@app.route("/register", methods=["POST"])
def register():
    request_json = request.get_json()

    email = request_json["email"]
    password = request_json["password"]
    name = request_json["name"]

    if email is None:
        return {"err_type": "email", "err_msg": "empty"}
    if password is None:
        return {"err_type": "password", "err_msg": "empty"}
    if name is None:
        return {"err_type": "name", "err_msg": "empty"}

    # The other fields for user as set in the Profile

    # @TODO: VERIFY USER DOESN'T YET EXIST FROM DATABASE
    # @TODO: ADD USER IF DOESN'T EXIST
    # Otherwise, fail:

    return {"err_type": "auth", "err_msg": "failed"}


@app.route("/", methods=["GET"])
def home():
    return "Welcome home!"


if __name__ == "__main__":
    app.run(port=5001)
