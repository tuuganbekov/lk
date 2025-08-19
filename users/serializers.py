from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'phone'

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        phone = phone.replace(' ', '').replace('+', '')
        user = authenticate(phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("Неверный номер телефона или пароль")
        return super().validate(attrs)


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'phone',
            'password1',
            'password2',
            'full_name',
            'email',
            'profile_photo',
        ]

    def validate_phone(self, value):
        value = value.replace(' ', '').replace('+', '')
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Пользователб с таким номером уже существует")
        return value
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        validate_password(attrs['password1'])
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    