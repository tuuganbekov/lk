from django.utils import timezone
from .models import User, Tariff, UserTariff, UserTariffHistory


def change_user_tariff(user: User, new_tariff: Tariff):
    try:
        user_tariff = user.current_tariff
        old_tariff = user_tariff.tariff
        user_tariff.tariff = new_tariff
        user_tariff.activated_at = timezone.now()
        user_tariff.save()
    except UserTariff.DoesNotExist:
        user_tariff = UserTariff.objects.create(
            user=user,
            tariff=new_tariff,
            activated_at=timezone.now()
        )
        old_tariff = None

    UserTariffHistory.objects.create(
        user=user,
        tariff=new_tariff,
        changed_at=timezone.now()
    )
    return old_tariff, new_tariff