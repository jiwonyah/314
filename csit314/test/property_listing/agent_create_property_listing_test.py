import unittest
from flask_testing import TestCase
from csit314.app import db, create_app
from flask import json,request, g, session
from csit314.entity.PropertyListing import FloorLevel, Furnishing, PropertyType
import logging

class TestSignUpController(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        self.login()

    def login(self):
        return self.client.post('/login/', json={'userid': 'user4', 'password': 'testpassword'})

    def test_create_property_listing(self):
        with self.client as client:
            response = client.post('/propertyListing/create/', data={
                'subject': 'Test Property',
                'content': 'This is a test property listing.',
                'price': 1000000,
                'address': '123 Test Street',
                'floorSize': 1000,
                'floorLevel': 'low',
                'propertyType': 'hdb',
                'furnishing': 'fully_furnished',
                'builtYear': 2020,
                'client_id': 'user3',
                'images': []
            })

            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertIn('Property listing created successfully', data['message'])

if __name__ == '__main__':
    unittest.main()
