import pytest

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_product_list():

    client = APIClient()

    response = client.get("/api/products/")

    print(response.data)

    assert response.status_code == 200
    
    
from products.models import Product, Category


@pytest.mark.django_db
def test_product_detail():

    owner = User.objects.create_user(
        email="owner@gmail.com",
        password="12345678",
        username="owner"
    )

    category = Category.objects.create(
        category="Camera"
    )

    product = Product.objects.create(
        owner=owner,
        category=category,
        title="Canon Camera",
        price_per_day=1000,
        brand_name="Canon"
    )

    client = APIClient()

    response = client.get(
        f"/api/products/{product.id}/"
    )

    print(response.data)

    assert response.status_code == 200
    
    
    
@pytest.mark.django_db
def test_invalid_product_detail():

    client = APIClient()

    response = client.get("/api/products/9999/")

    assert response.status_code == 404
    
    
@pytest.mark.django_db
def test_product_search():

    client = APIClient()

    response = client.get(
        "/api/products/?search=canon"
    )

    assert response.status_code == 200




@pytest.mark.django_db
def test_product_ordering():

    client = APIClient()

    response = client.get(
        "/api/products/?ordering=-price_per_day"
    )

    assert response.status_code == 200
    
@pytest.mark.django_db
def test_category_list():

    client = APIClient()

    response = client.get(
        "/api/products/category/"
    )

    print(response.data)

    assert response.status_code == 200
    
    

@pytest.mark.django_db
def test_product_filter():

    client = APIClient()

    response = client.get(
        "/api/products/?price_per_day_min=100"
    )

    assert response.status_code == 200
    
