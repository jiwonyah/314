import unittest
from flask_testing import TestCase
from csit314.app import db, create_app
from flask import json

class TestSignUpController(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        with self.client as client:
            # set to logged in
            client.post('/login/', json={'userid': 'user4', 'password': 'testpassword'})

    def test_creating_property_success(self):


    def test_creating_property_failure(self):


    def test_creating_property_failure2(self):


if __name__ == '__main__':
    unittest.main()
