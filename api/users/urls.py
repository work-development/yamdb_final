from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import RegisterView, ObtainAuthToken, UserViewSet

user_routers = DefaultRouter()
user_routers.register('', UserViewSet)

urlpatterns = [
    path('users/', include(user_routers.urls)),
    path('auth/email/', RegisterView.as_view()),
    path('auth/token/', ObtainAuthToken.as_view())
]
