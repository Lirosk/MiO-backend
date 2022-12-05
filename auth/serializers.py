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

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(f'{validated_data = }')

        user = User(**validated_data)
        user.save()

        return user

    def validate(self, attrs):
        # user = User(**attrs)
        print(f'{attrs = }')

        # password = user.get('password')

        return super().validate(attrs)