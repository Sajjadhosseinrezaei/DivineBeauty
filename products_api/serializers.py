from rest_framework.serializers import ModelSerializer
from products.models import Product



class ProductSerializer(ModelSerializer):
    model = Product
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id','slug', 'created_at', 'updated_at']