from rest_framework import serializers
import datetime

from .models import (
        Category,
        Brand,
        Product,
        Firm,
        Purchases,
        Sales,
    )

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "product_count",
        )

    def get_product_count(self, obj):
        return Product.objects.filter(category_id=obj.id).count()

class ProductSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    brand_id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "category_id",
            "brand",
            "brand_id",
            "stock",
            "createds",
            "updated",
        )

        read_only_fields = ("stock",)

class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "product_count",
            "products",
        )

    def get_product_count(self, obj):
        return Product.objects.filter(category_id=obj.id).count()

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "image",
        )

class FirmSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Firm
        fields = (
            "id",
            "name",
            "phone",
            "image",
            "address",
        )

class PurchasesSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    firm = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    firm_id = serializers.IntegerField()
    brand_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    category = serializers.SerializerMethodField()
    createds_time_hour = serializers.SerializerMethodField()
    updated_time_hour = serializers.SerializerMethodField()

    class Meta:
        model = Purchases
        fields = (
            "id",
            "user",
            "user_id",
            "category",
            "firm",
            "firm_id",
            "brand",
            "brand_id",
            "product",
            "product_id",
            "quantity",
            "price",
            "price_total",
            "createds_time_hour",
            "updated_time_hour",
        )

    def get_category(self, obj):
        product = Product.objects.get(id=obj.product_id)
        return Category.objects.get(id=product.category_id).name

    def get_createds_time_hour(self, obj):
        return datetime.datetime.strftime(obj.createds, "%d.%m.%y %H:%M")
    
    def get_updated_time_hour(self, obj):
        return datetime.datetime.strftime(obj.createds, "%d.%m.%y %H:%M")








