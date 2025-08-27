from django.contrib import admin

from .models import Service, UserService, UserServiceHistory


admin.site.register(Service)
admin.site.register(UserService)
admin.site.register(UserServiceHistory)
