from django.urls import path
from . import views

app_name = "shorturl"

urlpatterns = [
    path("<str:slug>/", views.Redirect.as_view(), name="redirect")  # while editing url check shorturl.models.create_qr
]
