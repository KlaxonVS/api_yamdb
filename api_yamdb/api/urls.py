from django.urls import path, include
from rest_framework.routers import DefaultRouter

#from .views import ()

router_v1 = DefaultRouter()


urlpatterns = [
    path('v1/', include(router_v1.urls), name='review-api'),
]
