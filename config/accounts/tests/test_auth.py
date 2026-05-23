import pytest

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_login_success():

    User.objects.create_user(
        email="test@gmail.com",
        password="12345678",
        username="testuser"
    )

    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {
            "email": "test@gmail.com",
            "password": "12345678"
        },
        format="json"
    )

    print(response.data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_profile():

    user = User.objects.create_user(
        email="test@gmail.com",
        password="12345678",
        username="testuser"
    )

    client = APIClient()

    # login user
    client.force_authenticate(user=user)

    response = client.get("/api/auth/me/")

    print(response.status_code)
    print(response.data)

    assert response.status_code == 200
    
@pytest.mark.django_db
def test_profile_unauthorized():

    client = APIClient()

    response = client.get("/api/auth/me/")

    assert response.status_code == 401