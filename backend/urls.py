from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Clients
    path("clients/", views.clients, name="clients"),
    path("add-client/", views.add_client, name="add_client"),
    path("edit-client/", views.edit_client, name="edit_client"),
    path("delete-client/", views.delete_client, name="delete_client"),
    # Timers
    path("start", views.start_timer, name="start_timer"),
    path("stop", views.stop_timer, name="stop_timer"),
    # Entries
    path("delete-entry/", views.delete_entry, name="delete_entry"),
    # Authentication
    path("webauthn/", include("django_otp_webauthn.urls", namespace="otp_webauthn")),
    path("logout/", views.logout, name="logout"),
    # Admin views
    path("admin/", admin.site.urls, name="admin"),
]
