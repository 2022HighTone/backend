from os import stat
from typing import List
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response

from domains.category.serializer import CategorySerializer
from domains.models import Category


class CategoryListView(GenericAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)