from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryView,
    BrandView,
    FirmView,
)

router = DefaultRouter()
router.register("categories", CategoryView)
router.register("brands", BrandView)
router.register("firms", FirmView)

urlpatterns = [] + router.urls
