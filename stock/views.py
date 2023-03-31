from rest_framework import viewsets, filters, status
from rest_framework.response import Response
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
    BrandSerializer,
    FirmSerializer,
    ProductSerializer,
    PurchasesSerializer,
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

class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

class FirmView(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["category", "brand"]
    search_fields = ["name"]

class PurchasesView(viewsets.ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["firm", "product"]
    search_fields = ["firm"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #! Adding Stock for Product Table
        purchase = request.data
        product = Product.objects.get(id=purchase["product_id"])
        product.stock += purchase["quantity"]
        product.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) #! Adding USER for PURCHASES Table

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        #! Updating Stock for Product Table
        purchase = request.data
        product = Product.objects.get(id=instance.product_id)
        difference = purchase["quantity"] - instance.quantity
        product.stock += difference
        product.save()

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        #! Updating Stock for Product Table
        product = Product.objects.get(id=instance.product_id)
        product.stock -= instance.quantity
        product.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)









