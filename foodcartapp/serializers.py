from rest_framework.serializers import ModelSerializer, ListField
from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = ListField(
        child=OrderItemSerializer(),
        allow_empty=False,
        write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'firstname', 'lastname', 'phonenumber', 'address', 'products'
        ]
