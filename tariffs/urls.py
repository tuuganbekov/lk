from django.urls import path

from .views import (
    TariffListAPIView,
    CurrentTariffAPIView,
    ChangeTariffAPIView,
    UserTariffHistoryAPIView,
    SimpleAPIView,
)


urlpatterns = [
    path('list/', TariffListAPIView.as_view(), name='tariff-list'),
    path('current/', CurrentTariffAPIView.as_view(), name='tariff-current'),
    path('change/', ChangeTariffAPIView.as_view(), name='tariff-change'),
    path('history/', UserTariffHistoryAPIView.as_view(), name='tariff-history'),
    path('simple/', SimpleAPIView.as_view())
]