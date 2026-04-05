from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import (
    ProductSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


# Create your views here.


class ProductPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()

        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(
            paginated_products,
            many=True,
            context={"request": request}
        )

        return paginator.get_paginated_response({
            "success": True,
            "data": serializer.data
        })


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
