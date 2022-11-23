from api.views import APISignUp, APIToken
from django.urls import path

urlpatterns = [
    path('signup/', APISignUp.as_view(), name='signup'),
    path('token/', APIToken.as_view(), name='token'),
]
