import unittest
from flask import g, session
import bcrypt
from flask_testing import TestCase
from csit314.app import create_app, db
from csit314.entity.Review import Review
from csit314.entity.User import User, Role

class WriteReviewTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    def setUp(self):
        self.app = self.create_app()
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

    def test_show_review_form(self):
        response = self.client.get('/write-review/3')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please write review', response.data)
        self.assertIn(b'Rating', response.data)

    def test_show_review_form_user_not_found(self):
        response = self.client.get('/write-review/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Agent not found', response.data)

    def test_submit_review(self):
        self.login_test_user()

        with self.client:
            with self.client.session_transaction() as sess:
                sess['user_id'] = self.test_seller.userid  # Simulate user login
            response = self.client.post('/write-review/3', json={
                'rating': '5',
                'content': 'Great service!'
            })
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Review is submitted successfully', response.data)

            review = Review.query.filter_by(agent_id=3).first()
            self.assertIsNotNone(review)
            self.assertEqual(review.rating, 5)
            self.assertEqual(review.content, 'Great service!')
            self.assertEqual(review.author_userid, 'test_seller123')

    def test_submit_review_validation_error(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['user_id'] = self.test_seller.userid  # Simulate user login
            response = self.client.post('/write-review/3', json={
                'rating': '',
                'content': ''
            })
            self.assertEqual(response.status_code, 422)
            self.assertIn(b'Rating is mandatory field', response.data)
            self.assertIn(b'Content is a mandatory field', response.data)

if __name__ == '__main__':
    unittest.main()

