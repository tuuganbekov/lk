from django.contrib import admin

from .models import Tariff, UserTariff, UserTariffHistory


# Register your models here.
admin.site.register(Tariff)
admin.site.register(UserTariff)
admin.site.register(UserTariffHistory)
