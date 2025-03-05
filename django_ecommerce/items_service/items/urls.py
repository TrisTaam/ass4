from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<str:id>/', views.item_detail, name='item_detail'),
]