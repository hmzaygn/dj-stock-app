from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryView,
    BrandView,
    FirmView,
    ProductView,
)

router = DefaultRouter()
router.register("categories", CategoryView)
router.register("brands", BrandView)
router.register("firms", FirmView)
router.register("products", ProductView)

urlpatterns = [] + router.urls
