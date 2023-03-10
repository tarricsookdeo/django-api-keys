from dj_rest_auth.views import LoginView, LogoutView
from django.urls import path

from .views import APIKeysView, ValidateAPIKeysView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api-keys/', APIKeysView.as_view(), name='api-keys'),
    path('validate-api-keys/', ValidateAPIKeysView.as_view(),
         name='validate-api-keys')
]
