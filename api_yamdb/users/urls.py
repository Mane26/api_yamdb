from django.urls import path

from .views import APISignUp, APIToken

urlpatterns = [
    path('signup/', APISignUp.as_view(), name='signup'),
    path('token/', APIToken.as_view(), name='token'),
]
