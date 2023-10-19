from rest_framework.serializers import ModelSerializer, ListField
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def create(self, validated_data, product, order):
        return OrderItem.objects.create(
            quantity=validated_data['quantity'],
            price=(validated_data['quantity'] * product.price),
            product=product,
            order=order
        )


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
        return Order.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber'],
            address=validated_data['address']
        )
