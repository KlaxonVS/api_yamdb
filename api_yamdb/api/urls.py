from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (UserSignupOrTokenViewSet, EditForUserViewSet,
                    AdminUserEditViewSet,)

router_v1 = DefaultRouter()
router_v1.register('me', EditForUserViewSet, basename='edit-for-user')
router_v1.register(r'auth/signup', UserSignupOrTokenViewSet,
                   basename='register')
router_v1.register(r'auth/token/', UserSignupOrTokenViewSet,
                   basename='token')
router_v1.register('users', AdminUserEditViewSet, basename='edit-for-admin')
router_v1.register('users', AdminUserEditViewSet, basename='edit-for-admin')

urlpatterns = [
    path('v1/', include(router_v1.urls), name='review-api'),
]
