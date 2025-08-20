from rest_framework import serializers

from .models import Tariff, UserTariff, UserTariffHistory


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ["id", "name", "price", "description"]


class UserTariffSerializer(serializers.ModelSerializer):
    tariff = TariffSerializer()

    class Meta:
        model = UserTariff
        fields = ["tariff", "activated_at"]


class UserTariffHistorySerializer(serializers.ModelSerializer):
    tariff = TariffSerializer()

    class Meta:
        model = UserTariffHistory
        fields = ["tariff", "changed_at"]


class ChangeTariffSerializer(serializers.Serializer):
    tariff_id = serializers.IntegerField()
