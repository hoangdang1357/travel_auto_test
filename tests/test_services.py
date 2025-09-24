import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

class TestServices:
    def test_get_services(self, client):
        res = client.get("/services/")
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_search_by_destination(self, client):
        res = client.get("/services/search?destination=Sapa")
        data = res.get_json()
        assert res.status_code == 200
        assert all(s["destination"].lower() == "sapa" for s in data)

    def test_search_by_price(self, client):
        res = client.get("/services/search?max_price=100")
        data = res.get_json()
        assert res.status_code == 200
        assert all(s["price"] <= 100 for s in data)

    def test_service_details(self, client):
        res = client.get("/services/1")
        assert res.status_code == 200
        assert res.get_json()["id"] == 1

    def test_service_not_found(self, client):
        res = client.get("/services/999")
        assert res.status_code == 404

import unittest
import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import init_db, add_sample_data

class ServicesTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'test.db'
        self.app = app.test_client()
        with app.app_context():
            init_db()
            add_sample_data()

    def tearDown(self):
        os.remove('test.db')

    def test_get_services(self):
        response = self.app.get('/services/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A trip to Paris', response.data)
        self.assertIn(b'A trip to Tokyo', response.data)

    def test_search_by_destination(self):
        response = self.app.get('/services/?destination=Tokyo', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A trip to Tokyo', response.data)
        self.assertNotIn(b'A trip to Paris', response.data)

    def test_search_by_price(self):
        response = self.app.get('/services/?min_price=200&max_price=300', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A trip to Tokyo', response.data)
        self.assertNotIn(b'A trip to Paris', response.data)

    def test_service_details(self):
        response = self.app.get('/services/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A trip to Paris', response.data)

if __name__ == '__main__':
    unittest.main()
