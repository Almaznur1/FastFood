from django.http import JsonResponse
from django.templatetags.static import static
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderItem
from addresses.models import Address
from addresses.fetch_coordinates import fetch_coordinates
from .serializers import OrderSerializer, OrderItemSerializer


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    order_serializer = OrderSerializer(data=request.data)
    order_serializer.is_valid(raise_exception=True)

    products = request.data['products']

    with transaction.atomic():
        new_order = order_serializer.save()

        for product in products:
            requested_product = Product.objects.get(pk=product['product'])

            order_item_serializer = OrderItemSerializer(data=product)
            order_item_serializer.is_valid(raise_exception=True)
            order_item_serializer.create(
                validated_data=order_item_serializer.validated_data,
                product=requested_product,
                order=new_order
            )

        lon, lat = fetch_coordinates(order_serializer.validated_data['address'])
        Address.objects.update_or_create(
            address=order_serializer.validated_data['address'],
            defaults={
                'lon': lon,
                'lat': lat
            }
        )

    serializer = OrderSerializer(new_order)
    return Response(serializer.data)
