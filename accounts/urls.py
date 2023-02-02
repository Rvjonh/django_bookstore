from django.urls import path

from .views import UpdateProfileView

urlpatterns = [
    path("profile/", UpdateProfileView.as_view(), name="account_profile"),
]
