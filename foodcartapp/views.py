from django.http import JsonResponse
from django.templatetags.static import static
from json import loads
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
import phonenumbers

from .models import Product, Order, OrderItem


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
    order = request.data
    print(order)

    try:
        products = order['products']
    except KeyError:
        raise APIException(detail='products key not presented')
    if products is None:
        raise APIException(detail='the products field cannot be empty')
    if not isinstance(products, list):
        raise APIException(detail='products key must be a list')
    if not products:
        raise APIException(detail='the products list cannot be empty')
    products_id = Product.objects.all().values_list('id', flat=True)

    for product in products:
        if product['product'] not in products_id:
            return Response(f'invalid product primary key "{product["product"]}"', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # raise APIException(
            #     detail=f'invalid product primary key "{product["product"]}"'
            #     )
    try:
        order['firstname']
        order['lastname']
        order['address']
    except KeyError:
        raise APIException(detail='one or more order keys are not present')

    try:
        order['phonenumber']
    except KeyError:
        raise APIException(detail='the phone number is not present')

    if (order['firstname'] or order['lastname'] or
            order['address'] or order['phonenumber']) is None:
        raise APIException(
            detail='the value of one or more order keys is None'
            )

    try:
        parsed_phonenumber = phonenumbers.parse(
            order['phonenumber'],
            'RU'
        )
    except phonenumbers.NumberParseException:
        raise APIException(
            detail='incorrect value entered in the "phonenumber" key'
            )

    if phonenumbers.is_valid_number(parsed_phonenumber):
        order['phonenumber'] = phonenumbers.format_number(
            parsed_phonenumber,
            phonenumbers.PhoneNumberFormat.E164
        )
    else:
        raise APIException(
            detail='incorrect number entered in the "phonenumber" key'
            )

    if isinstance(order['firstname'], list):
        raise APIException(detail='the key "firstname" must be str not list')
    if not isinstance(order['firstname'], str):
        raise APIException(detail='the key "firstname" must be str')
    if not order['firstname']:
        raise APIException(detail='the key "firstname" is not specified')

    new_order = Order.objects.create(
        first_name=order['firstname'],
        last_name=order['lastname'],
        phonenumber=order['phonenumber'],
        address=order['address'],
    )

    for product in products:
        requested_product = Product.objects.get(pk=product['product'])
        OrderItem.objects.create(
            product=requested_product,
            quantity=product['quantity'],
            order=new_order
        )
    return Response()
