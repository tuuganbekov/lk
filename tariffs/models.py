from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Tariff(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class UserTariff(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='current_tariff'
    )
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT)
    activated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.tariff.name}"


class UserTariffHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tariff_history'
    )
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT)
    changed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.tariff.name} - {self.changed_at}"