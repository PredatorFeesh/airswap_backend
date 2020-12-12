from datetime import datetime
from flask import jsonify

from App import db

follows = db.Table(
    "follows",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("city_id", db.Integer, db.ForeignKey("city.id")),
    db.Column("date", db.Date),
)

requests = db.Table(
    "requests",
    db.Column("requester", db.Integer, db.ForeignKey("user.id")),
    db.Column("requestee", db.Integer, db.ForeignKey("user.id")),
)


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    email = db.Column("email", db.String(), unique=True, nullable=False)
    password = db.Column("password", db.String(60), nullable=False)
    first_name = db.Column("first_name", db.String(50), nullable=False)
    last_name = db.Column("last_name", db.String(50), nullable=False)

    image = db.Column("image", db.String(100), nullable=True, default="default.jpg")
    phone_number = db.Column("phone_number", db.String(10), nullable=True)
    description = db.Column("description", db.Text, nullable=True)

    listing = db.relationship("Listing", backref="owner", uselist=False)
    requested = db.relationship(
        "User",
        secondary=requests,
        primaryjoin=(requests.c.requester == id),
        secondaryjoin=(requests.c.requestee == id),
        backref=db.backref("requests", lazy="dynamic"),
        lazy="dynamic",
    )
    cities = db.relationship(
        "City", secondary=follows, back_populates="followers", lazy="dynamic"
    )

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.date = datetime.now()

    def to_json(self, original=True):
        return {
            "UserID": self.id,
            "Email": self.email,
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Image": self.image,
            "Phone Number": self.phone_number,
            "UserDescription": self.description,
            "Listing": self.listing.to_json(False) if original else {},
        }

    def get_profile(self):
        return self.to_json()

    def get_profile_by_id(self):
        return self.to_json()

    def update_profile(
        self, password, first_name, last_name, image, phone_number, description
    ):
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.image = image
        self.phone_number = phone_number
        self.description = description

        db.session.add(self)
        db.session.commit()

        return self.to_json()

    def request(self, user):
        if not self.has_requested(user):
            self.requested.append(user)
        return "Successfully requested"

    def remove_request(self, user):
        if self.has_requested(user):
            self.requested.remove(user)
        return "Request removed"

    def has_requested(self, user):
        return self.requested.filter(requests.c.requestee == user.id).count() > 0

    def view_requests(self):
        return self.requested.all()

    def follow(self, city_name):
        city = City.query.filter_by(name=city_name).first()

        if not self.has_followed(city):
            self.cities.append(city)
            db.session.commit()
            return jsonify({"City": city.name})

        return jsonify({"Followed": city.name})

    def unfollow(self, city_name):
        city = City.query.filter_by(name=city_name).first()
        if city is None:
            return jsonify({"City doesn't exist": city.name})

        if self.has_followed(city):
            self.cities.remove(city)
            db.session.commit()
            return jsonify({"City unfollowed": city.name})

        return jsonify({"City not followed": city.name})

    def has_followed(self, city):
        return self.cities.filter(follows.c.city_id == city.id).count() > 0

    def add_listing(self, address, location, image, description):
        city = City.query.filter_by(name=location).first()

        if city is None:
            city = City(location)
            db.session.add(city)
            db.session.commit()

        listing = Listing(address, image, description, True, datetime.now())
        listing.location = city
        self.listing = listing

        db.session.add(listing)
        db.session.commit()

    def get_listings_in_followed_cities(self):
        listings_to_view = []
        for city in self.cities:
            for listing in city.listings.all():
                listings_to_view.append(listing)

        try:
            listings_to_view.sort(key=lambda listing: listing.date)
        except TypeError:
            print("No date provided.")

        return jsonify({"Listings": [result.to_json() for result in listings_to_view]})


class Listing(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    address = db.Column("address", db.String(150), nullable=False)
    image = db.Column("image", db.String(100), nullable=False, default="default.jpg")
    description = db.Column("description", db.Text, nullable=False)
    is_listed = db.Column("is_listed", db.Boolean)
    date = db.Column("date", db.Date())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))

    def __init__(self, address, image, description, is_listed, date):
        self.address = address
        self.image = image
        self.description = description
        self.is_listed = is_listed
        self.date = date

    def to_json(self, original=True):
        return {
            "ListingID": self.id,
            "Owner": self.owner.to_json(False) if original else {},
            "Address": self.address,
            "City": self.location.name,
            "Image": self.image,
            "Description": self.description,
            "is_listed": self.is_listed,
            "Date": self.date,
        }

    def listing_clicked(self):
        return self.user_id

    def update_listing(self, address, location, image, description):
        city = City.query.filter_by(name=location).first()
        if city is None:
            city = City(location)
            db.session.add(city)
            db.session.commit()

        self.address = address
        self.location = city
        self.image = image
        self.description = description

        db.session.add(self)
        db.session.commit()

        return self.to_json()


class City(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(25))
    listings = db.relationship("Listing", backref="location", lazy="dynamic")
    followers = db.relationship(
        "User", secondary=follows, back_populates="cities", lazy="dynamic"
    )

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            "Name": self.name,
        }
