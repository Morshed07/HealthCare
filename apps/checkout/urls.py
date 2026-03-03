from django.urls import path
from .views import (
    CheckoutAPIView,
    MyOrdersAPIView,
    OrderDetailAPIView,
    # UpdateOrderStatusAPIView
)

urlpatterns = [
    path("place-order/", CheckoutAPIView.as_view()),
    path("orders/my-orders/", MyOrdersAPIView.as_view()),
    path("order-detail/<str:order_id>/", OrderDetailAPIView.as_view()),
    # path("<str:order_id>/update-status/", UpdateOrderStatusAPIView.as_view()),
]