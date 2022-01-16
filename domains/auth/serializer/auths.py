from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from domains.models import UserSchool, Review
from domains.school.serializer import SchoolSerializer
from domains.store.serializer import ReviewSeralizer

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


class DefaultSchoolSettingSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        user = User.objects.get(id=user_id)

        serializer = SchoolSerializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        school = serializer.save()

        return UserSchool.objects.create(user=user, school=school)


class UserProfileSerializer(serializers.ModelSerializer):
    school = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'school', 'reviews')

    def get_school(self, obj):
        user_school = UserSchool.objects.filter(user=obj)
        if not user_school.exists():
            return None
        else:
            return user_school.first().school.name

    def get_reviews(self, obj):
        reviews = Review.objects.filter(user=obj)

        data = ReviewSeralizer(reviews, many=True).data

        return data