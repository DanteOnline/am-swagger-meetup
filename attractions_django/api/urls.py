from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AttractionViewSet


app_name = 'api'  # pylint:disable=invalid-name

router = DefaultRouter()
router.register(r"attractions", AttractionViewSet, basename="attraction")

urlpatterns = [
    path("", include(router.urls)),
]
