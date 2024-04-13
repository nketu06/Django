from rest_framework.test import APIClient
from rest_framework import status
import pytest

class TestCreateCollections:
    @pytest.mark.django_db
    def test_if_uses_is_anonymous_returns_401(self):
        client=APIClient()
        response=client.post('/store/collections/',{'title':'a'})
        assert response.status_code==status.HTTP_401_UNAUTHORIZED

