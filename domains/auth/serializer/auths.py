from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user =  User.objects.create_user(**validated_data)
        Token.objects.create(user=user)

        return user


class GetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        token = Token.objects.get(user=instance)

        return {'token': token.key}


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = User.objects.filter(email=email)

        if not user.exists():
            raise serializers.ValidationError({'detail': 'not user exist'})

        user = user.first()

        hash_password = check_password(password, user.password)

        if not hash_password:
            raise serializers.ValidationError({'detail': 'wrong password'})

        return user