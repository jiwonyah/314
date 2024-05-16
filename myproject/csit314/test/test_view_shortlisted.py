import unittest
import json
from datetime import datetime
from csit314.app import create_app, db
from csit314.entity.User import User, Role
from csit314.entity.PropertyListing import PropertyListing, FloorLevel, PropertyType, Furnishing
from csit314.entity.Favourite import Favourite
import bcrypt

class ViewFavouritesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.test_user = User(
            userid='test_user12345',
            password=bcrypt.hashpw('password'.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8'),
            email='testuser111@gmail.com',
            firstName='Test',
            lastName='User',
            role=Role.BUYER
        )
        db.session.add(self.test_user)
        db.session.commit()

        # Create test agent user
        self.test_agent = User(
            userid='testagent123',
            password=bcrypt.hashpw('password'.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8'),
            email='testagent123@example.com',
            firstName='Test',
            lastName='Agent',
            role=Role.AGENT
        )
        db.session.add(self.test_agent)
        db.session.commit()

        # Create test seller user
        self.test_seller = User(
            userid='test_seller123',
            password=bcrypt.hashpw('password'.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8'),
            email='testseller3333@gmail.com',
            firstName='Test',
            lastName='Seller',
            role=Role.SELLER
        )
        db.session.add(self.test_seller)
        db.session.commit()

        # Create test property
        self.test_property = PropertyListing(
            subject='Test Property',
            content='Test Content',
            price=1000000,
            address='123 Test St',
            floorSize=100,
            floorLevel=FloorLevel.LOW,
            propertyType=PropertyType.HDB,
            furnishing=Furnishing.FullyFurnished,
            builtYear=2020,
            create_date=datetime.now(),
            agent_id=self.test_agent.id,
            client_id=self.test_seller.userid
        )
        db.session.add(self.test_property)
        db.session.commit()

        # Create test favourite
        self.test_favourite = Favourite(
            user_userid=self.test_user.userid,
            propertyListing_id=self.test_property.id,
            create_date=datetime.now()
        )
        db.session.add(self.test_favourite)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_test_user(self):
        response = self.client.post('/login/', json={
            'userid': 'test_user12345',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
    '''
    def test_view_my_favourites_index(self):
        self.login_test_user()
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.test_user.id

            response = c.get('/shortlisted')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Property', response.data)
    '''
    def test_view_my_shortlisted(self):
        self.login_test_user()
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.test_user.id

            response = c.get('/api/shortlisted')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['subject'], 'Test Property')
            self.assertEqual(data[0]['create_date'], self.test_favourite.create_date.strftime('%Y-%m-%d'))

if __name__ == '__main__':
    unittest.main()
