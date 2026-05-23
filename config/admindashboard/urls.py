from django.urls import path
from .views import (AdminKYCListView,UpdateKYCStatusView,
                    AdminProductsListView,UpdateProductstatusView,
                    AdminUsersListView,UpdateUserActiveView
                    )




urlpatterns = [
    path('kyc/',AdminKYCListView.as_view()),
    path('kyc/docs-update/<int:pk>/',UpdateKYCStatusView.as_view()),
    path('products/',AdminProductsListView.as_view()),
    path('products/<int:pk>/',UpdateProductstatusView.as_view()),
    path('users/',AdminUsersListView.as_view()),
    path('users/<int:pk>/',UpdateUserActiveView.as_view()),
]
 