from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, RoomViewSet

router = DefaultRouter()
router.register(r'event',EventViewSet,basename='event')
router.register(r'room',RoomViewSet,basename='room')

urlpatterns = [
    path('',include(router.urls)),
    
]