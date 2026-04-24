from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, TourDateViewSet

router = DefaultRouter()
router.register(r'dates', TourDateViewSet, basename='tour-date')
router.register(r'', TourViewSet, basename='tour')

urlpatterns = [
    path('', include(router.urls)),
]
