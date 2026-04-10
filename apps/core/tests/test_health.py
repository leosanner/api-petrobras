from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class HealthCheckTest(APITestCase):
    def test_health_endpoint_returns_200(self):
        client = APIClient()
        response = client.get("/api/health/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "ok"}
