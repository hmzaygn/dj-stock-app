from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryView,
    BrandView,
)

router = DefaultRouter()
router.register("categories", CategoryView)
router.register("brands", BrandView)

urlpatterns = [] + router.urls
