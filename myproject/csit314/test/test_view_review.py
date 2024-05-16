import unittest
from flask import json, g
from csit314.app import create_app, db
from csit314.entity.Review import Review
from csit314.entity.User import User, Role
from datetime import datetime
import bcrypt

class ReviewDetailTestCase(unittest.TestCase):

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

        # Create test review
        self.test_review = Review(
            author_userid=self.test_user.userid,
            agent_id=self.test_agent.id,
            create_date=datetime.now(),
            rating=5,
            content="Great service!"
        )
        db.session.add(self.test_review)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        #db.drop_all()
        self.app_context.pop()

    def login_test_agent(self):
        with self.client as c:
            response = c.post('/login/', json={
                'userid': 'testagent123',
                'password': 'password'
            })
            self.assertEqual(response.status_code, 200)
            with c.session_transaction() as sess:
                sess['user_id'] = self.test_agent.id

    def test_review_detail_success(self):
        self.login_test_agent()
        response = self.client.get(f'/api/agent/reviewDetail/{self.test_review.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        expected_date = self.test_review.create_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        self.assertEqual(data['id'], self.test_review.id)
        self.assertEqual(data['author_name'], f"{self.test_user.firstName} {self.test_user.lastName}")
        self.assertEqual(data['create_date'], expected_date)
        self.assertEqual(data['rating'], self.test_review.rating)
        self.assertEqual(data['content'], self.test_review.content)

    def test_review_detail_not_found(self):
        self.login_test_agent()
        response = self.client.get('/api/agent/reviewDetail/9999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "The review ID doesn't exist")

    def test_review_detail_permission_denied(self):
        # Create another agent user
        self.other_agent = User(
            userid='some_other_agent',
            password=bcrypt.hashpw('password'.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8'),
            email='otheragent@example.com',
            firstName='Other',
            lastName='Agent',
            role=Role.AGENT
        )
        db.session.add(self.other_agent)
        db.session.commit()

        # Log in as the other agent
        with self.client as c:
            response = c.post('/login/', json={
                'userid': 'some_other_agent',
                'password': 'password'
            })
            self.assertEqual(response.status_code, 200)
            with c.session_transaction() as sess:
                sess['user_id'] = self.other_agent.id

        response = self.client.get(f'/api/agent/reviewDetail/{self.test_review.id}')
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'You do not have permission to access the review detail page.')


if __name__ == '__main__':
    unittest.main()
