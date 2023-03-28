from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions

from .models import (
        Category,
        Brand,
        Product,
        Firm,
        Purchases,
        Sales,
    )
from .serializers import (
    CategorySerializer,
    CategoryProductSerializer,
)

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    # filter field is case sensitive
    filterset_fields = ["name"]
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.query_params.get("name"):
            return CategoryProductSerializer
        return super().get_serializer_class()














