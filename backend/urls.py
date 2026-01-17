from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Authentication
    path("webauthn/", include("django_otp_webauthn.urls", namespace="otp_webauthn")),
    path("logout/", views.logout, name="logout"),
    # Admin views
    path("admin/", admin.site.urls, name="admin"),
]
