from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'password', )
#         extra_kwargs = {'password': {'write_only: True'}}
    
#     def create(self, validated_data):
#         user = User(**validated_data)
#         user.save()
#         return user

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
