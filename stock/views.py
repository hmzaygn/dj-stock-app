from rest_framework import viewsets, filters

from .models import (
        Category,
        Brand,
        Product,
        Firm,
        Purchases,
        Sales,
    )
from .serializers import (
    CategorySerializer
)

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']














