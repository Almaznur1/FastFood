from rest_framework.serializers import ModelSerializer, ListField
from phonenumber_field.serializerfields import PhoneNumberField
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
    phonenumber = PhoneNumberField()

    class Meta:
        model = Order
        fields = [
            'id', 'firstname', 'lastname', 'phonenumber', 'address', 'products'
        ]

    def create(self, validated_data):
        items = validated_data.pop('products')

        order = Order.objects.create(**validated_data)

        for item in items:
            OrderItem.objects.create(
                order=order,
                price=(item['quantity'] * item['product'].price),
                **item
            )

        return order
