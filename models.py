from App import db

follows = db.Table("follows",
                   db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                   db.Column("city_id", db.Integer, db.ForeignKey("city.id"))
                   )

requests = db.Table("requests",
                    db.Column("requester", db.Integer, db.ForeignKey("user.id")),
                    db.Column("requestee", db.Integer, db.ForeignKey("user.id"))
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
    requested = db.relationship("User", secondary=requests,
                                primaryjoin=(requests.c.requester == id),
                                secondaryjoin=(requests.c.requestee == id),
                                backref=db.backref("requests", lazy="dynamic"), lazy="dynamic")

    def __init__(self, email, password, first_name, last_name, image, phone_number, description):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.image = image
        self.phone_number = phone_number
        self.description = description

    # I wrote the following methods to test requests
    # We will probably move this logic elsewhere
    def request(self, user):
        if not self.has_requested(user):
            self.requested.append(user)

    def remove_request(self, user):
        if self.has_requested(user):
            self.requested.remove(user)

    def has_requested(self, user):
        return self.requested.filter(
            requests.c.requestee == user.id).count() > 0


class Listing(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    address = db.Column("address", db.String(150), nullable=False)
    image = db.Column("image", db.String(100), nullable=False, default="default.jpg")
    description = db.Column("description", db.Text, nullable=False)
    is_listed = db.Column("is_listed", db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))

    def __init__(self, address, image, description, is_listed):
        self.address = address
        self.image = image
        self.description = description
        self.is_listed = is_listed


class City(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(25))
    listings = db.relationship("Listing", backref="location", lazy="dynamic")

    def __init__(self, name):
        self.name = name
