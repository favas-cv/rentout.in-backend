import pytest

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_order_unauthorized():

    client = APIClient()

    response = client.post(
        "/api/booking/create-razorpay-order/",
        {},
        format="json"
    )

    assert response.status_code == 401
@pytest.mark.django_db
def test_create_order_missing_reservation_ids():

    user = User.objects.create_user(
        email="test@gmail.com",
        password="12345678",
        username="testuser"
    )

    client = APIClient()

    client.force_authenticate(user=user)

    response = client.post(
        "/api/booking/create-razorpay-order/",
        {},
        format="json"
    )

    print(response.data)

    assert response.status_code == 400
    assert response.data["error"] == "reservation_ids must be a list"
    
    
    
@pytest.mark.django_db
def test_invalid_reservation():

    user = User.objects.create_user(
        email="test@gmail.com",
        password="12345678",
        username="testuser"
    )

    client = APIClient()

    client.force_authenticate(user=user)

    payload = {
        "reservation_ids": [999]
    }

    response = client.post(
        "/api/booking/create-razorpay-order/",
        payload,
        format="json"
    )

    print(response.data)

    assert response.status_code == 200
    assert response.data["error"] == "Invalid reservation"
    
    
@pytest.mark.django_db
def test_verify_payment_missing_fields():

    user = User.objects.create_user(
        email="test@gmail.com",
        password="12345678",
        username="testuser"
    )

    client = APIClient()

    client.force_authenticate(user=user)

    response = client.post(
        "/api/booking/verify-payment/",
        {},
        format="json"
    )

    print(response.data)

    assert response.status_code == 400
    assert response.data["error"] == "Missing payment details"
    
    
@pytest.mark.django_db
def test_invalid_payment_signature():

    user = User.objects.create_user(
        email="test@gmail.com",
        password="12345678",
        username="testuser"
    )

    client = APIClient()

    client.force_authenticate(user=user)

    payload = {
        "razorpay_order_id": "fake_order",
        "razorpay_payment_id": "fake_payment",
        "razorpay_signature": "fake_signature"
    }

    response = client.post(
        "/api/booking/verify-payment/",
        payload,
        format="json"
    )

    print(response.data)

    assert response.status_code == 400
    assert response.data["error"] == "Payment verification failed"