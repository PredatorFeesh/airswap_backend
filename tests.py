from App import app, db
from models import User, Listing, City
import unittest


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_requests(self):
        user1 = User(
            email="testone@email.com",
            first_name="John",
            last_name="Doe",
            password="test123",
        )
        user1.add_listing("Address", "Boston", "image", "Description")

        user2 = User(
            email="testtwo@email.com",
            first_name="Jane",
            last_name="Smith",
            password="test123",
        )
        user2.add_listing("Address", "New York", "image", "Description")

        user3 = User(
            email="testthree@email.com",
            first_name="Kate",
            last_name="Green",
            password="test123",
        )
        user3.add_listing("Address", "London", "image", "Description")

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        self.assertEqual(user1.requested.all(), [])
        self.assertEqual(user2.requested.all(), [])
        self.assertEqual(user3.requested.all(), [])

        user1.request(user2)
        self.assertTrue(user1.has_requested(user2))
        self.assertEqual(user1.requested.count(), 1)
        self.assertEqual(user1.requested.first().email, "testtwo@email.com")
        self.assertEqual(user2.requests.count(), 1)
        self.assertEqual(user2.requests.first().email, "testone@email.com")

        # test view_request
        user1.request(user3)
        self.assertListEqual(user1.view_requests(), [user2, user3])

        user1.remove_request(user2)
        self.assertFalse(user1.has_requested(user2))
        self.assertEqual(user1.requested.count(), 1)
        self.assertEqual(user2.requests.count(), 0)

    def test_listings(self):
        user = User(
            email="testone@email.com",
            first_name="John",
            last_name="Doe",
            password="test123",
        )
        user.add_listing("Test address", "London", "default.jpg", "Test description", )

        db.session.add(user)
        db.session.commit()

        listing = user.listing
        city = City.query.filter_by(name="London").first()

        self.assertEqual(listing.owner.id, user.id)
        self.assertEqual(listing.city_id, city.id)

        listing.update_listing("Updated address", "Paris", "UpdatedImage", "Updated Description")
        db.session.commit()

        self.assertEqual(listing.address, "Updated address")
        self.assertEqual(listing.image, "UpdatedImage")
        self.assertEqual(listing.description, "Updated Description")
        city = City.query.filter_by(name="Paris").first()
        self.assertEqual(listing.city_id, city.id)

    def test_follows(self):
        user1 = User(
            email="testone@email.com",
            first_name="John",
            last_name="Doe",
            password="test123",
        )
        user2 = User(
            email="testtwo@email.com",
            first_name="Jane",
            last_name="Smith",
            password="test123",
        )

        city1 = City(name="London")
        city2 = City(name="New York")

        db.session.add(user1)
        db.session.add(city1)
        db.session.add(user2)
        db.session.add(city2)

        db.session.commit()

        with app.app_context():
            user1.follow(city1.name)
            self.assertEqual(user1.cities.count(), 1)
            self.assertEqual(user1.cities.first(), city1)
            self.assertEqual(city1.followers.count(), 1)
            user1.follow(city2.name)
            self.assertEqual(user1.cities.count(), 2)
            self.assertEqual(city2.followers.count(), 1)
            self.assertEqual(city2.followers.first(), user1)

            user2.follow(city1.name)
            self.assertEqual(user2.cities.count(), 1)
            self.assertEqual(city1.followers.count(), 2)

            user2.unfollow(city1.name)
            self.assertEqual(user2.cities.count(), 0)
            self.assertEqual(city1.followers.count(), 1)
    #
    # def test_view_listings(self):
    #     user1 = User(
    #         email="testone@email.com",
    #         first_name="John",
    #         last_name="Doe",
    #         password="test123",
    #     )
    #     user1.add_listing("John's address", "London", "default.jpg", "John's listing description", )
    #
    #     user2 = User(
    #         email="testtwo@email.com",
    #         first_name="Anna",
    #         last_name="Green",
    #         password="test123",
    #     )
    #     user2.add_listing("Anna's address", "Paris", "default.jpg", "Anna's listing description", )
    #
    #     user3 = User(
    #         email="testthree@email.com",
    #         first_name="James",
    #         last_name="Smith",
    #         password="test123",
    #     )
    #     user3.add_listing("James's address", "Paris", "default.jpg", "John's listing description", )
    #
    #     city1 = City(name="London")
    #     city2 = City(name="Paris")
    #
    #     db.session.add(user1)
    #     db.session.add(user2)
    #     db.session.add(city1)
    #     db.session.add(city2)
    #     db.session.commit()
    #
    #     with app.app_context():
    #         user1.follow(city2.name)
    #         self.assertEqual(user1.get_listings_in_followed_cities().length, 2)
    #
    #     # user1.unfollow(city1)
        # self.assertListEqual(user1.get_listings_in_followed_cities(), [])


if __name__ == "__main__":
    unittest.main()
