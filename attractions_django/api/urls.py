from rest_framework.routers import DefaultRouter
from .views import AttractionViewSet
from django.urls import path, include

app_name = 'api'

router = DefaultRouter()
router.register(r"attractions", AttractionViewSet, basename="attraction")

urlpatterns = [
    path("", include(router.urls)),
]
