from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("clients/", views.clients, name="clients"),
    path("add-client/", views.add_client, name="add_client"),
    path("edit-client/", views.edit_client, name="edit_client"),
    path("delete-client/", views.delete_client, name="delete_client"),
    # Authentication
    path("webauthn/", include("django_otp_webauthn.urls", namespace="otp_webauthn")),
    path("logout/", views.logout, name="logout"),
    # Admin views
    path("admin/", admin.site.urls, name="admin"),
]
