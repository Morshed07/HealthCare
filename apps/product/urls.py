from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView
)

urlpatterns = [
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product-detail')
]
