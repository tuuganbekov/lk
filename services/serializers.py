from rest_framework import serializers

from .models import Service, UserService, UserServiceHistory


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "price", "description"]


class UserServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = UserService
        fields = ["service", "activated_at"]


class UserServiceHistorySerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = UserServiceHistory
        fields = ["service", "changed_at"]


class ChangeServiceInputSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()


class ChangeServiceOutputSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    old_service = serializers.CharField(allow_null=True)
    new_service = serializers.CharField(allow_null=True)