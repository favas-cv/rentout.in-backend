from django.urls import path
from .views import AddDocsView,ListDocsView


urlpatterns = [
    path('add-docs/',AddDocsView.as_view()),
    path('docs/',ListDocsView.as_view()),

]
  