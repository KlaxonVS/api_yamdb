from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import register_or_confirm_code, get_token, AdminUserEditViewSet


router_v1 = DefaultRouter()
router_v1.register('users', AdminUserEditViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls), name='review-api'),
    path('v1/auth/signup/', register_or_confirm_code, name='register_or_code'),
    path('v1/auth/token/', get_token, name='get_token'),
]
