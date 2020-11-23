from App import app, db
from models import User, Listing, City
import unittest


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_requests(self):
        user1 = User(email="testone@email.com", first_name="John", last_name="Doe", password="test123")

        user2 = User(email="testtwo@email.com", first_name="Jane", last_name="Smith", password="test123")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertEqual(user1.requested.all(), [])
        self.assertEqual(user2.requested.all(), [])

        user1.request(user2)
        db.session.commit()
        self.assertTrue(user1.has_requested(user2))
        self.assertEqual(user1.requested.count(), 1)
        self.assertEqual(user1.requested.first().email, "testtwo@email.com")
        self.assertEqual(user2.requests.count(), 1)
        self.assertEqual(user2.requests.first().email, "testone@email.com")

        user1.remove_request(user2)
        db.session.commit()
        self.assertFalse(user1.has_requested(user2))
        self.assertEqual(user1.requested.count(), 0)
        self.assertEqual(user2.requests.count(), 0)

    def test_listings(self):
        user = User(email="testone@email.com", first_name="John", last_name="Doe", password="test123")
        city = City(name="New York")
        listing = Listing(address="Test address", image="default.jpg", description="Test description",
                          is_listed=True)

        db.session.add(user)
        db.session.add(city)
        db.session.add(listing)
        db.session.commit()
        self.assertEqual(listing.owner, None)
        self.assertEqual(listing.location, None)

        listing.location = city
        self.assertEqual(listing.location, city)
        self.assertEqual(listing.location.id, city.id)
        self.assertEqual(listing.location.name, "New York")

        listing.owner = user
        self.assertEqual(listing.owner.id, user.id)
        self.assertEqual(user.listing, listing)

        self.assertEqual(city.listings.first(), listing)

    def test_follows(self):
        user1 = User(email="testone@email.com", first_name="John", last_name="Doe", password="test123")
        user2 = User(email="testtwo@email.com", first_name="Jane", last_name="Smith", password="test123")
        city1 = City(name="New York")
        city2 = City(name="London")

        db.session.add(user1)
        db.session.add(city1)
        db.session.add(user2)
        db.session.add(city2)
        db.session.commit()

        user1.cities.append(city1)
        self.assertEqual(user1.cities.count(), 1)
        self.assertEqual(user1.cities.first(), city1)
        self.assertEqual(city1.followers.count(), 1)
        user1.cities.append(city2)
        self.assertEqual(user1.cities.count(), 2)
        self.assertEqual(city2.followers.count(), 1)
        self.assertEqual(city2.followers.first(), user1)

        user2.cities.append(city1)
        self.assertEqual(user2.cities.count(), 1)
        self.assertEqual(city1.followers.count(), 2)

        user2.cities.remove(city1)
        self.assertEqual(user2.cities.count(), 0)
        self.assertEqual(city1.followers.count(), 1)


if __name__ == '__main__':
    unittest.main()
