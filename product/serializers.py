from rest_framework import serializers
from rest_framework.fields import CharField
from django.utils import timezone
from .models import Product, Category,Order, OrderItem, PricingPrediction, PricingAdjustment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    image_url = CharField(source='image.url', read_only=True)
    # Dynamically calculate price_ratio (current_price / cost_price) if not stored
    price_ratio = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_price_ratio(self, obj):
        # Calculate price ratio as current_price / cost_price (ensure it's not zero)
        if obj.cost_price and obj.cost_price != 0:
            return obj.current_price / obj.cost_price
        return 0
     
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
   items = serializers.JSONField()  # ✅ Items stored as JSON
   user = serializers.CharField(source='user.username', read_only=True)  # ✅ Replace customer with user

   class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'items']

class PricingPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPrediction
        fields = '__all__'
 
class PricingAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingAdjustment
        fields = '__all__'
