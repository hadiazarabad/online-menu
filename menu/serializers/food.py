from rest_framework import serializers
from menu.models import Food, FoodImage
from menu.serializers.category import CategorySerializer
from menu.serializers.food_topping import FoodToppingSerializer


def _absolute_uri(serializer, url):
    if not url:
        return url
    request = serializer.context.get('request')
    if request:
        return request.build_absolute_uri(url)
    return url


class FoodImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = FoodImage
        fields = ['id', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image(self, obj):
        url = obj.image.url if obj.image else None
        return _absolute_uri(self, url)


class FoodSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=True)
    final_price = serializers.SerializerMethodField()
    header_image = serializers.SerializerMethodField()
    images = FoodImageSerializer(many=True, read_only=True)
    toppings = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = [
            'id', 'category', 'category_id', 'name', 'description', 'price',
            'final_price', 'header_image', 'images', 'toppings',
            'is_available', 'discount', 'available_from', 'available_to',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_header_image(self, obj):
        url = obj.header_image.url if obj.header_image else None
        return _absolute_uri(self, url)

    def get_final_price(self, obj):
        if obj.discount and obj.discount > 0:
            return round(float(obj.price) * (1 - obj.discount / 100), 2)
        return float(obj.price)

    def get_toppings(self, obj):
        available_toppings = obj.food_toppings.filter(topping__is_available=True)
        return FoodToppingSerializer(available_toppings, many=True).data

class FoodDetailSerializer(FoodSerializer):
    all_toppings = serializers.SerializerMethodField()
    
    class Meta(FoodSerializer.Meta):
        fields = FoodSerializer.Meta.fields + ['all_toppings']
    
    def get_all_toppings(self, obj):
        return FoodToppingSerializer(obj.food_toppings.all(), many=True).data
