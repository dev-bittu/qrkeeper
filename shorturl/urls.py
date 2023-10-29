from django.urls import path
from . import views

app_name = "shorturl"

urlpatterns = [
    path("<str:slug>/", views.Redirect.as_view(), name="redirect")
]
