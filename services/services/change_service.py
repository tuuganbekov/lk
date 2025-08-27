from django.utils import timezone

from mixins.base import BaseService
from services.models import Service, UserService, UserServiceHistory


class ChangeUserServiceService(BaseService):
    """
    Смена услуги у пользователя
    """

    def run(self):
        service_id = self.kwargs.get("service_id")

        try:
            new_service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return {
                "success": False,
                "message": "Услуга не найдена",
                "old_service": None,
                "new_service": None
            }
        
        try:
            user_service = self.user.current_service
            old_service = user_service.service
            user_service.service = new_service
            user_service.activated_at = timezone.now()
            user_service.save()
        except UserService.DoesNotExist:
            user_service = UserService.objects.create(
                user=self.user,
                service=new_service,
                activated_at=timezone.now(),
            )
            old_service = None

        UserServiceHistory.objects.create(
            user=self.user,
            service=new_service,
            changed_at=timezone.now()
        )

        return {
            "message": "Услуга успешно изменена",
            "old_service": old_service.name if old_service else None,
            "new_service": new_service.name,
        }