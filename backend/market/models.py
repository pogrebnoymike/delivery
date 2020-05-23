from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from image_cropping.fields import ImageRatioField, ImageCropField
from easy_thumbnails.files import get_thumbnailer


class Provider(User):
    name = models.CharField(max_length=250, default='')
    phone = models.CharField(max_length=250, default='')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'


class Consumer(User):
    name = models.CharField(max_length=250, default='')
    phone = models.CharField(max_length=250, default='')
    address = models.TextField(default='')
    geo_location = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Consumer'
        verbose_name_plural = 'Consumers'


class Category(models.Model):
    name = models.CharField(max_length=250, default='')
    image = models.ImageField(upload_to='category', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def icon(self):
        try:
            return mark_safe('<img src={}/>'.format(self.image.url))
        except:
            'None'


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=250, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Sub-category'
        verbose_name_plural = 'Sub-categories'


class Product(models.Model):
    name = models.CharField(max_length=250, default='')
    image = ImageCropField(upload_to='product', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    cropping = ImageRatioField('image', '100x100')

    def __str__(self):
        return '{} ({})'.format(self.name, self.category)

    @property
    def image_tag(self):
        try:
            return mark_safe('<img src={}/>'.format(self.image.url))
        except:
            'None'

    @property
    def icon(self):
        return mark_safe('<img src="{}"'.format(get_thumbnailer(self.image).get_thumbnail({
            'size': (100, 100),
            'box': self.cropping,
            'crop': 'smart'
        }).url))

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Store(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'


class Order(models.Model):

    STATUS = (
        ('new', 'New order'),
        ('pending', 'Pending order'),
        ('in_progress', 'In progress'),
        ('delivery', 'Order being delivered'),
        ('delivered', 'Delivered'),
    )

    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, default='New', choices=STATUS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderProduct(models.Model):
    pass
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Order Product'
        verbose_name_plural = 'Order Products'