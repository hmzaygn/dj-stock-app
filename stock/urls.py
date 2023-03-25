from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryView,
)

router = DefaultRouter()
router.register("categories", CategoryView)

urlpatterns = [] + router.urls
