from rest_framework import serializers
from .models import Item
from .models import ItemUser
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemUser
        fields = ('name', 'email', 'mobile', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = ItemUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            mobile=validated_data['mobile'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
