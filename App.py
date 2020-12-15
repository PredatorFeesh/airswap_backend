from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["DEBUG"] = True
app.config[
    "JWT_SECRET_KEY"
] = "*&F78gg7878SG787g787&*G8gG**(G^*(&*G8gg78;l[po[[oin9h])23g.[.]"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///airswap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
)

from flask_cors import CORS
import models

CORS(app)

jwt = JWTManager(app)


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

    # Listing Info
    listing_address = request_json["address"]
    listing_location = request_json["location"]
    listing_image = request_json["image"]
    listing_description = request_json["description"]

    # Now we need to split first and second.
    first, second = name.split(" ")

    # Check whether user is in our database
    user_db = models.User.query.filter_by(email=email).first()
    if user_db is not None:
        return jsonify({"err_type": "user", "err_msg": "exists"}), 400

    # Now add the user to the database
    # @IFTIME: Encrypt password
    user_db = models.User(email, password, first, second)
    models.User.add_listing(
        user_db, listing_address, listing_location, listing_image, listing_description
    )

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
    cur_user = get_jwt_identity()
    return jsonify({"access_token": create_access_token(identity=cur_user)}), 200


# @TODO REMOVE THIS. Keeping it temporarily for reference
@app.route("/test", methods=["POST"])
@jwt_required
def test():
    print(get_jwt_identity())
    return "Secret"


@app.route("/", methods=["GET"])
def home():
    return "Welcome home!"


@app.route("/users", methods=["GET"])
@jwt_required
def get_users():
    users = models.User.query.all()
    return jsonify({"Users": [result.to_json() for result in users]})


@app.route("/get_profile", methods=["GET"])
@jwt_required
def get_profile():
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()

    return models.User.get_profile(user)


@app.route("/get_profile/<user_id>", methods=["GET"])
@jwt_required
def get_profile_by_user_id(user_id):
    user = models.User.query.filter_by(id=user_id).first()

    return models.User.get_profile_by_id(user)


@app.route("/update_profile", methods=["PUT"])
@jwt_required
def update_profile():
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()

    request_json = request.json
    name = request_json["name"]
    first, last = name.split(" ")
    image = request_json["image"]
    phone_number = request_json["phone_number"]
    description = request_json["description"]

    return models.User.update_profile(
        user, first, last, image, phone_number, description
    )


@app.route("/update_listing", methods=["PUT"])
@jwt_required
def update_listing():
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()
    listing = models.Listing.query.filter_by(owner=user).first()

    request_json = request.json
    address = request_json["address"]
    location = request_json["location"]
    image = request_json["image"]
    description = request_json["description"]

    return models.Listing.update_listing(listing, address, location, image, description)


@app.route("/get_listing/<user_id>", methods=["GET"])
@jwt_required
def get_listing(user_id):
    user = models.User.query.filter_by(id=user_id).first()
    listing = models.Listing.query.filter_by(owner=user).first()

    return listing.to_json()


@app.route("/request/<requested_user_id>", methods=["POST"])
@jwt_required
def request_user(requested_user_id):
    requesting_user_id = get_jwt_identity()["id"]
    requesting_user = models.User.query.filter_by(id=requesting_user_id).first()
    requested_user = models.User.query.filter_by(id=requested_user_id).first()

    return models.User.request(requesting_user, requested_user)


@app.route("/sent_requests", methods=["GET"])
@jwt_required
def sent_requests():
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()

    user_sent_requests = user.requested.all()

    return jsonify({"Requested": [result.to_json() for result in user_sent_requests[:]]})


@app.route("/received_requests", methods=["GET"])
@jwt_required
def received_requests():
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()

    user_received_requests = models.User.query.filter(models.User.requested.contains(user)).all()

    return jsonify({"Requested by": [result.to_json() for result in user_received_requests[:]]})


@app.route("/remove_request/<requested_user_id>", methods=["DELETE"])
@jwt_required
def remove_request(requested_user_id):
    requesting_user_id = get_jwt_identity()["id"]
    requesting_user = models.User.query.filter_by(id=requesting_user_id).first()
    requested_user = models.User.query.filter_by(id=requested_user_id).first()

    return models.User.remove_request(requesting_user, requested_user)


@app.route("/follow/<city_name>", methods=["POST"])
@jwt_required
def follow_city(city_name):
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()

    return models.User.follow(user, city_name)


@app.route("/unfollow/<city_name>", methods=["DELETE"])
@jwt_required
def unfollow_city(city_name):
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()

    return models.User.unfollow(user, city_name)


@app.route("/listings", methods=["GET"])
@jwt_required
def get_listings_in_followed_cities():
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()

    return models.User.get_listings_in_followed_cities(user)


@app.route("/listings/<selected_city>", methods=["GET"])
@jwt_required
def get_listings_in_selected_city(selected_city):
    city = models.City.query.filter_by(name=selected_city).first()
    listings = []

    for listing in city.listings.all():
        if listing.is_listed:
            listings.append(listing)

    return jsonify({"Listings": [result.to_json() for result in listings]})


@app.route("/open_listing", methods=["PUT"])
@jwt_required
def open_listing():
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()

    return models.User.open_listing(user)


@app.route("/close_listing", methods=["PUT"])
@jwt_required
def close_listing():
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()

    return models.User.close_listing(user)


@app.route("/followed_cities", methods=["GET"])
@jwt_required
def get_followed_cities():
    user_id = get_jwt_identity()["id"]
    user = models.User.query.filter_by(id=user_id).first()

    cities = user.cities

    return jsonify({"Cities": [result.to_json() for result in cities]})


@app.route("/cities", methods=["GET"])
@jwt_required
def cities():
    all_cities = models.City.query.all()
    return jsonify({"Cities": [result.to_json() for result in all_cities]})


if __name__ == "__main__":
    app.run(port=5001)
