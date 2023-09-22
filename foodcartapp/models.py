from django.db import models
from django.db.models import Sum, F
from django.core.validators import MinValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=500,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def total_price(self):
        order = self.annotate(
            total_price=Sum(F('items__quantity') * F('items__product__price'))
        )
        return order


class Order(models.Model):
    MANAGER = 'MANAGER'
    RESTAURANT = 'RESTAURANT'
    COURIER = 'COURIER'
    COMPLETED = 'COMPLETED'

    STATUS_CHOICES = (
        (MANAGER, 'Необработанный'),
        (RESTAURANT, 'В ресторане'),
        (COURIER, 'У курьера'),
        (COMPLETED, 'Выполнен'),
    )

    CASH = 'CASH'
    NON_CASH = 'NON_CASH'

    PAYMENT_METHOD_CHOICES = (
        (CASH, 'Наличный'),
        (NON_CASH, 'Безналичный'),
    )

    firstname = models.CharField(
        'имя',
        max_length=25
    )
    lastname = models.CharField(
        'фамилия',
        max_length=25
    )
    phonenumber = PhoneNumberField(
        'номер телефона',
    )
    address = models.CharField(
        'адрес',
        max_length=200
    )
    status = models.CharField(
        'статус заказа',
        max_length=10,
        choices=STATUS_CHOICES,
        db_index=True,
        default=MANAGER
    )
    comment = models.TextField(
        'комментарий',
        blank=True,
    )
    registered_at = models.DateTimeField(
        'время создания заказа',
        default=timezone.now,
        db_index=True
    )
    called_at = models.DateTimeField(
        'время звонка клиенту',
        null=True,
        blank=True
    )
    delivered_at = models.DateTimeField(
        'время доставки',
        null=True,
        blank=True
    )
    payment_method = models.CharField(
        'способ оплаты',
        max_length=15,
        choices=PAYMENT_METHOD_CHOICES,
        db_index=True
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name='товар',
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        'количество'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        return f'{self.product} {self.order} {self.order.address}'
