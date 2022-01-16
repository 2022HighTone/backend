from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response

from domains.store.serializer import ReviewSeralizer
from domains.models import Store

class ReviewCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSeralizer

    def post(self, request, *args, **kwargs):
        store_id = kwargs.get('store_id')
        store = Store.objects.get(id=store_id)
        serializer = self.get_serializer(data=request.data, context={
            'request': request,
            'store': store
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)