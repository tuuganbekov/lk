from django.urls import path

from .views import (
    ServiceListView,
    UserCurrentServiceView,
    ChangeServiceView,
    UserServiceHistoryView,
)


urlpatterns = [
    path('list/', ServiceListView.as_view(), name='service-list'),
    path('current/', UserCurrentServiceView.as_view(), name='service-current'),
    path('change/', ChangeServiceView.as_view(), name='service-change'),
    path('history/', UserServiceHistoryView.as_view(), name='service-history'),
]
