from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (UserSignupOrTokenViewSet, EditForUserViewSet,
                    AdminUserEditViewSet,)

router_v1 = DefaultRouter()
router_v1.register('me', EditForUserViewSet, basename='edit-for-user')
router_v1.register('users', AdminUserEditViewSet, basename='edit-for-admin')

urlpatterns = [
    path('v1/', include(router_v1.urls), name='review-api'),
    path(
        'v1/auth/signup/',
        UserSignupOrTokenViewSet.as_view(),
        name='register'
    ),
    path('v1/auth/token/', UserSignupOrTokenViewSet.as_view(), name='token')
]