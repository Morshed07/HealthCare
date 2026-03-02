from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView,
    ClearCartView,
    CartWaiverUpdateView
)

urlpatterns = [
    path("user-cart/", CartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="add-to-cart"),
    path("update/<str:item_id>/", UpdateCartItemView.as_view(), name="update-cart-item"),
    path("remove/<str:item_id>/", RemoveCartItemView.as_view(), name="remove-cart-item"),
    path("clear/", ClearCartView.as_view(), name="clear-cart"),
    path("waiver-update/", CartWaiverUpdateView.as_view(), name="cart-waiver-update")
]
