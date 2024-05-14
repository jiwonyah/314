import unittest
from flask_testing import TestCase
from csit314.app import db, create_app
from csit314.entity.UserAccount import User,Role
from csit314.entity.PropertyListing import PropertyListing, FloorLevel, PropertyType, Furnishing
from datetime import datetime
from flask_login import login_user

class TestViewOldPropertyListing(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        form_buyer = {
            'userid': 'buyer1',
            'password': 'qwer1234',
            'password2': 'qwer1234',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'buyer1@example.com',
            'role': Role.BUYER.value  # Choose any role you want to test without ADMIN
        }
        self.client.post('/signup/', data=form_buyer, follow_redirects=True)
        db.create_all()
        form_agent = {
            'userid': 'agent',
            'password': 'qwer1234',
            'password2': 'qwer1234',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'agent@example.com',
            'role': Role.AGENT.value  # Choose any role you want to test without ADMIN
        }
        self.client.post('/signup/', data=form_agent, follow_redirects=True)
        db.create_all()
        form_seller = {
            'userid': 'seller',
            'password': 'qwer1234',
            'password2': 'qwer1234',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'seller@example.com',
            'role': Role.SELLER.value  # Choose any role you want to test without ADMIN
        }
        self.client.post('/signup/', data=form_seller, follow_redirects=True)
        # Create a POST request with form data
        # Add only when there are no existing user with userid 'testuser'
        existing_user = User.query.filter_by(userid='testuser').first()
        # 가상의 사용자 생성 (구매자 역할)
        #self.buyer = User(userid='buyer1', password='qwer1234', email='buyer1@example.com',
                          #firstName='sample', lastName='user', role=Role.BUYER)
        #self.agent = User(userid='agent1', password='qwer1234', email='agent1@example.com',
        #                  firstName='sample', lastName='user', role=Role.AGENT)
        #self.seller = User(userid='seller1',  password='qwer1234', email='seller1@example.com',
        #                   firstName='sample', lastName='user', role=Role.SELLER)
        #db.session.add(self.buyer)
        #db.session.add(self.agent)
        #db.session.add(self.seller)
        #db.session.commit()
        buyer = User.query.filter_by(userid='buyer1').first()
        # 가상의 판매 완료된 부동산 목록 생성
        self.property1 = PropertyListing(subject='House 1', content='', price=300000,
                                         address='180D Ang Mo Kio', floorSize=50, floorLevel=FloorLevel.HIGH,
                                         propertyType=PropertyType.HDB,
                                         furnishing=Furnishing.NotFurnished, builtYear=2010,
                                        create_date=datetime(2022, 1, 1, 12, 0, 0),
                                        modify_date=datetime(2022, 1, 2, 12, 0, 0),
                                         agent_id=2, client_id='seller', view_counts=0, is_sold=True,)
        db.session.add(self.property1)
        db.session.commit()

    def tearDown(self):
        """테스트 이후 정리 작업을 수행합니다."""
        db.session.remove()
        #db.drop_all()

    #됨. 정리만 하면 될듯.
    def test_success(self):
        """인증된 구매자가 구매 완료된 부동산 목록을 조회할 수 있는지 테스트합니다."""
        with self.client as client:
            response = self.client.post('/login/', json={'userid': 'buyer1', 'password': 'qwer1234'})
            self.assertEqual(response.status_code, 200)

            # 요청을 수행하여 응답을 받습니다.
            response = self.client.get('/api/oldPropertyListing')
            data = response.get_json()

            # 응답의 상태 코드 및 데이터를 확인합니다.
            self.assertEqual(response.status_code, 200)
            # 응답 데이터의 구조 및 필드를 확인합니다.
            property_listings = data['old_property_listings']
            self.assertIsInstance(property_listings, list)
            self.assertEqual(len(property_listings), 1)
            self.assertEqual(property_listings[0]['subject'], 'House 1')
            self.assertEqual(property_listings[0]['agent_id'], 2)
            self.assertTrue(property_listings[0]['is_sold'])
            self.assertEqual(property_listings[0]['id'], self.property1.id)
            self.assertEqual(property_listings[0]['create_date'], '2022-01-01 12:00:00')
            self.assertEqual(property_listings[0]['modify_date'], '2022-01-02')

    def test_fail_1(self):
        """인증되지 않은 사용자가 부동산 목록 조회 시 401 에러를 반환하는지 테스트합니다."""
        # 로그인하지 않은 상태로 요청을 수행하여 응답을 받습니다.
        response = self.client.get('/api/oldPropertyListing')
        data = response.get_json()

        # 응답의 상태 코드 및 에러 메시지를 확인합니다.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertIn('Login required', data['error'])

    def test_fail_2(self):
        """buyer 외에 다른 역할의 유저로 접근시 403 에러 반환하는지 테스트"""
        with self.client:
            self.assertTrue(self.agent.is_authenticated)
            self.assertEqual(self.agent.role, Role.AGENT)

            # 요청을 수행하여 응답을 받습니다.
            response = self.client.get('/api/oldPropertyListing')
            data = response.get_json()

            # 응답의 상태 코드 및 에러 메시지를 확인합니다.
            self.assertEqual(response.status_code, 403)
            self.assertEqual(data['success'], False)
            self.assertIn('Only buyers can view old property listings', data['error'])

if __name__ == '__main__':
    unittest.main()