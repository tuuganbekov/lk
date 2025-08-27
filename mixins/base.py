import logging
from rest_framework import status
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class BaseService:
    """
    Базовый класс для сервисов.
    Все сервисы должны реализовать метод `run`.
    """

    def __init__(self, user=None, **kwargs):
        self.user = user
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError("Метод run() должен быть реализован в сервисе")

    def execute(self):
        """
        Единая точка входа:
        - логирование
        - обработка ошибок
        - возврат результата
        """
        try:
            logger.info(f"[SERVICE START] {self.__class__.__name__} user={self.user} args={self.kwargs}")
            result = self.run()
            logger.info(f"[SERVICE SUCCESS] {self.__class__.__name__}: result={result}")
            return {"success": True, **result}
        except Exception as e:
            logger.exception(f"[SERVICE ERROR] {self.__class__.__name__}: {str(e)}")
            return {"success": False, "message": str(e)}
        

class ServiceAPIViewMixin:
    """
    Миксин для вызова сервисов, унаследованных от BaseService.
    """

    service_class = None
    input_serializer_class = None
    output_serializer_class = None
    http_method_names = ["post"]

    def get_serializer_class(self):
        if self.input_serializer_class:
            return self.input_serializer_class
        return super().get_serializer_class()
    
    def execute_service(self, request, *args, **kwargs):
        if not self.service_class:
            raise NotImplementedError("Необходимо указать service_class во views")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = self.service_class(user=request.user, **serializer.validated_data)
        result = service.execute()

        if not result.get("success"):
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        if self.output_serializer_class:
            return Response(self.output_serializer_class(result).data)
        
        return Response(result, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        return self.execute_service(request, *args, **kwargs)
