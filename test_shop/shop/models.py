from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
        help_text="Введите название продукта",
    )

    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание продукта",
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
        verbose_name="Цена",
        help_text="Введите цену продукта",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} - {self.price}"
