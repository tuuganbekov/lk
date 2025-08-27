from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Service
from .serializers import (
    ServiceSerializer,
    UserServiceSerializer,
    UserServiceHistorySerializer,
    ChangeServiceInputSerializer,
    ChangeServiceOutputSerializer,
)
from .services.change_service import ChangeUserServiceService
from mixins.base import ServiceAPIViewMixin


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]


class UserCurrentServiceView(generics.RetrieveAPIView):
    serializer_class = UserServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.current_service


class UserServiceHistoryView(generics.ListAPIView):
    serializer_class = UserServiceHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.service_history.all().order_by("-changed_at")


class ChangeServiceView(ServiceAPIViewMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    input_serializer_class = ChangeServiceInputSerializer
    output_serializer_class = ChangeServiceOutputSerializer
    service_class = ChangeUserServiceService
