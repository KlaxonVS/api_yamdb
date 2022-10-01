from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserEditViewSet, get_token,
                    register_or_confirm_code)

router_v1 = DefaultRouter()
router_v1.register(r'users', UserEditViewSet, basename='users')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')

extra_patterns = [
    path('signup/', register_or_confirm_code, name='register_or_code'),
    path('token/', get_token, name='get_token'),
]


urlpatterns = [
    path('v1/', include(router_v1.urls), name='review-api'),
    path('v1/auth/', include(extra_patterns), name='auth'),
]
