from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import (
    ProductSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework import status


# Create your views here.


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )

        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class ProductDetailView(APIView):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(
            product,
            context={'request': request}
        )

        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK

        )
