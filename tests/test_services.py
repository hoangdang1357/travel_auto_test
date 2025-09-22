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
