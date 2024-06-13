from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Home"),
    path('about', views.about, name="About"),
    path('products', views.products, name="Products"),
    path('mission', views.mission, name="Mission"),
    path('faqs', views.faqs, name="Faqs"),
    path('contact', views.contact, name="Contact"),
    path('login', views.login, name="Login"),
    path('logout', views.user_logout, name="Logout"),
    path('register', views.register, name="Register"),
    path('forgot-password', views.forgotPassword, name="Forgot-Password"),
]