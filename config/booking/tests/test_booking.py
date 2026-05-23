import pytest

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_check_availability_missing_cart():

    user = User.objects.create_user(
        email="test@gmail.com",
        password="12345678",
        username="testuser"
    )

    client = APIClient()

    client.force_authenticate(user=user)

    payload = {
        "start_date": "2026-05-20",
        "end_date": "2026-05-25"
    }

    response = client.post(
        "/api/booking/check-availability/",
        payload,
        format="json"
    )

    print(response.data)

    assert response.status_code == 200
    assert response.data["error"] == "Missing cart"
    
    
@pytest.mark.django_db
def test_check_availability_missing_start_date():

    user = User.objects.create_user(
        email="test@gmail.com",
        password="12345678",
        username="testuser"
    )

    client = APIClient()

    client.force_authenticate(user=user)

    payload = {
        "cart_id": 1,
        "end_date": "2026-05-25"
    }

    response = client.post(
        "/api/booking/check-availability/",
        payload,
        format="json"
    )

    assert response.data["error"] == "Missing start-date"
    
@pytest.mark.django_db
def test_invalid_date_format():

    user = User.objects.create_user(
        email="test@gmail.com",
        password="12345678",
        username="testuser"
    )

    client = APIClient()

    client.force_authenticate(user=user)

    payload = {
        "cart_id": 1,
        "start_date": "wrong-date",
        "end_date": "2026-05-25"
    }

    response = client.post(
        "/api/booking/check-availability/",
        payload,
        format="json"
    )

    assert response.data["error"] == "Invalid date format"