from datetime import datetime
from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class SystemStatusTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/status/"

    def test_status_endpoint_returns_200(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "updated_at" in data
        assert "components" in data

    def test_status_contains_updated_at_in_iso_format(self):
        response = self.client.get(self.url)
        data = response.json()
        parsed = datetime.fromisoformat(data["updated_at"])
        assert isinstance(parsed, datetime)

    def test_status_contains_database_component(self):
        response = self.client.get(self.url)
        data = response.json()
        db = data["components"]["database"]
        assert db["status"] == "healthy"
        assert isinstance(db["latency_ms"], (int, float))
        assert db["latency_ms"] >= 0

    def test_status_contains_api_component(self):
        response = self.client.get(self.url)
        data = response.json()
        api = data["components"]["api"]
        assert api["status"] == "healthy"
        assert "version" in api

    @patch("apps.core.views.connection")
    def test_status_returns_503_when_database_unhealthy(self, mock_connection):
        mock_connection.ensure_connection.side_effect = Exception("connection refused")
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["components"]["database"]["status"] == "unhealthy"
        assert "error" in data["components"]["database"]
