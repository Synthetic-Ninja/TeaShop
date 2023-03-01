from django.db import models
from django.core.validators import MaxValueValidator


class ProductCategories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория: {self.id} | Название: [{self.name}]'


class Brands(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return f'Бренд: {self.id} | Название: {self.name}'


class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_available = models.BooleanField()
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    discount = models.PositiveBigIntegerField(default=0, validators=[MaxValueValidator(100)])
    quantity = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategories, on_delete=models.CASCADE)
    brand = models.ForeignKey(to=Brands, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name} | Бренд {self.brand.name}'

    def get_discounted_price(self):
        price = float(self.price)
        return price - (price * (self.discount / 100))
