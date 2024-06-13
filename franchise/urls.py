from django.urls import path
from . import views

urlpatterns = [
    path("", views.franchisePage, name="franchise"),
    path("sell-a-kit", views.sellKit, name="sell-kit"),
    path("login", views.index, name="franchise-login"),
    path("purchase-history", views.purchaseHistory, name="purchase-history"),
    path("sell-history", views.sellHistory, name="sell-history"),
    path("repurchase", views.repurchase, name="repurchase"),
    path("repurchase/sell-a-product", views.sellProduct, name="sell-product"),
    path("repurchase/purchase-history", views.repurchasePurchaseHistory, name="purchase-history"),
    path("repurchase/sell-history", views.repurchaseSellHistory, name="sell-history"),
]
