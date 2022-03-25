from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Article, Sale
from .serializers import ArticleSerializer, SaleSerializer, StatSerializer
from .permissions import IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, permission_classes
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum
from django.db.models import F

# Create your views here.

class ArticleViewSet(viewsets.ViewSet):
    """
    Allow authenticated user to create an article
    """

    def create(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
@permission_classes((IsAuthorOrReadOnly, ))
class SaleViewSet(viewsets.ViewSet):
    """
    Allow authenticated user to create, list or retreive a sale and allow only to article author to update and delete sales
    """

    def list(self, request):
        sales = Sale.objects.all()
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(sales, request)
        if page is not None:
            serializer = SaleSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = SaleSerializer(page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        queryset = Sale.objects.all()
        sale = get_object_or_404(queryset, pk=pk)
        serializer = SaleSerializer(sale)
        return Response(serializer.data)

    
    def partial_update(self, request, pk=None):
        sale = Sale.objects.get(pk=pk)
        serializer = SaleSerializer(instance=sale, data=request.data, partial=True )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        sale = Sale.objects.get(pk=pk)
        sale.delete()
        return Response(status=204)
        





class StatViewSet(viewsets.ViewSet):
    """
    allow authenticated user to see the sales statisctic of each article
    """
    def list(self, request):
        agg_sale = Sale.objects.all().values('article_id', 'article__category__display_name', ).annotate(total_earn=Sum(F('quantity') * F('unit_selling_price')), total_qty = Sum('quantity')).order_by('-total_earn')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(agg_sale, request)

        if page is not None:
            serializer = StatSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = StatSerializer(page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)