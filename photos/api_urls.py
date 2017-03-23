from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from photos.api import PhotoViewSet


# APIRouter
router = DefaultRouter(trailing_slash=False)
router.register(r'photos', PhotoViewSet)

urlpatterns = [

    # API URLs
    url(r'1.0/', include(router.urls))
]