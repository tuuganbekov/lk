from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Tariff, UserTariff, UserTariffHistory
from .serializers import (
    TariffSerializer,
    UserTariffSerializer,
    UserTariffHistorySerializer,
    ChangeTariffSerializer
)
from .services import change_user_tariff
from .filters import TariffFilter
from .pagination import (
    DefaultPageNumberPagination,
    DefaultLimitOffsetPagination,
)


class TariffListAPIView(generics.ListAPIView):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter, )
    filterset_class = TariffFilter  # FILTER
    search_fields = ('name', 'description', )  # SEARCH
    ordering_fields = ('price', 'name',)
    pagination_class = DefaultPageNumberPagination


class CurrentTariffAPIView(generics.RetrieveAPIView):
    serializer_class = UserTariffSerializer

    def get_object(self):
        return get_object_or_404(UserTariff, user=self.request.user)


class UserTariffHistoryAPIView(generics.ListAPIView):
    serializer_class = UserTariffHistorySerializer

    def get_queryset(self):
        return UserTariffHistory.objects.filter(user=self.request.user)


class ChangeTariffAPIView(generics.GenericAPIView):
    serializer_class = ChangeTariffSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            new_tariff = Tariff.objects.get(
                id=serializer.validated_data['tariff_id']
            )
        except Tariff.DoesNotExist:
            return Response({"detail": "Tariff not found"}, status=status.HTTP_404_NOT_FOUND)

        old_tariff, new_tariff = change_user_tariff(request.user, new_tariff)

        return Response({
            "detail": "Tariff changed successfully",
            "old_tariff": old_tariff.name if old_tariff else None,
            "new_tariff": new_tariff.name,
        }, status=status.HTTP_200_OK)
