import pytest

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_owner_dashboard_unauthorized():

    client = APIClient()

    response = client.get("/api/owner/dashboard/")

    assert response.status_code == 401
    
    
@pytest.mark.django_db
def test_owner_dashboard_success():

    owner = User.objects.create_user(
        email="owner@gmail.com",
        password="12345678",
        username="owner"
    )

    client = APIClient()

    client.force_authenticate(user=owner)

    response = client.get("/api/owner/dashboard/")

    print(response.data)

    assert response.status_code == 200
    
    
@pytest.mark.django_db
def test_owner_products_list():

    owner = User.objects.create_user(
        email="owner@gmail.com",
        password="12345678",
        username="owner"
    )

    client = APIClient()

    client.force_authenticate(user=owner)

    response = client.get("/api/owner/products/")

    print(response.data)

    assert response.status_code == 200
    
@pytest.mark.django_db
def test_owner_orders_list():

    owner = User.objects.create_user(
        email="owner@gmail.com",
        password="12345678",
        username="owner"
    )

    client = APIClient()

    client.force_authenticate(user=owner)

    response = client.get("/api/owner/orders/")

    print(response.data)

    assert response.status_code == 200
    
    
@pytest.mark.django_db
def test_owner_orders_search():

    owner = User.objects.create_user(
        email="owner@gmail.com",
        password="12345678",
        username="owner"
    )

    client = APIClient()

    client.force_authenticate(user=owner)

    response = client.get(
        "/api/owner/orders/?search=test@gmail.com"
    )

    assert response.status_code == 200
    
    
@pytest.mark.django_db
def test_owner_orders_filter():

    owner = User.objects.create_user(
        email="owner@gmail.com",
        password="12345678",
        username="owner"
    )

    client = APIClient()

    client.force_authenticate(user=owner)

    response = client.get(
        "/api/owner/orders/?status=PENDING"
    )

    assert response.status_code == 200
    
    
@pytest.mark.django_db
def test_owner_orders_ordering():

    owner = User.objects.create_user(
        email="owner@gmail.com",
        password="12345678",
        username="owner"
    )

    client = APIClient()

    client.force_authenticate(user=owner)

    response = client.get(
        "/api/owner/orders/?ordering=-created_at"
    )

    assert response.status_code == 200