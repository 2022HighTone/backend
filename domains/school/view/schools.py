from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response

from domains.school.serializer import (
    SchoolSerializer, school_list_method
)
from domains.models import Category, Distance, UserSchool, School


User = get_user_model()


class DefaultSchoolView(GenericAPIView):
    serializer_class = SchoolSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        if self.request.user.id is not None:
            user_school = UserSchool.objects.filter(user=self.request.user.id)
            if user_school.exists():
                school = user_school.first().school
            else:
                school = School.objects.get(is_default=True)
        else:
            school = School.objects.get(is_default=True)

        return school

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset()

        categories = request.GET.get('categories')
        distance = request.GET.get('distance')
        price = request.GET.get('price')

        if categories is not None and categories != '':
            category_list = categories.split(',')
            categories = Category.objects.filter(name__in=category_list)
        else:
            categories = Category.objects.all()

        if distance is not None:
            distance = Distance.objects.filter(name=distance)
        else:
            distance=Distance.objects.all()
        
        serializer = self.get_serializer(instance, context={
            'categories': categories,
            'distance': distance,
            'price': price,
        })

        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultSchoolView(GenericAPIView):
    serializer_class = SchoolSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        name = request.GET.get('name')
        address = request.GET.get('address')
        categories = request.GET.get('categories')
        distance = request.GET.get('distance')
        price = request.GET.get('price')

        if categories is not None and categories != '':
            category_list = categories.split(',')
            categories = Category.objects.filter(name__in=category_list)
        else:
            categories = Category.objects.all()

        if distance is not None:
            distance = Distance.objects.filter(name=distance)
        else:
            distance=Distance.objects.all()

        data = {
            'name': name,
            'address': address
        }

        serializer = self.get_serializer(data=data, context={
            'categories': categories,
            'distance': distance,
            'price': price,
        })
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchSchoolListView(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        name = request.GET.get('name')
        data = school_list_method(name)

        if not data:
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data, status=status.HTTP_200_OK)