from rest_framework.serializers import ModelSerializer
from products.models import Product, Comment, Category



class ProductSerializer(ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock', 'brand', 'attributes']
        read_only_fields = ['id']


class CommentSerializer(ModelSerializer):
    

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CategorySerializer(ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['name', 'parent']

