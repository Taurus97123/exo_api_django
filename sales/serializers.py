from rest_framework import serializers
from .models import Article, Sale


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__' 


class SaleSerializer(serializers.ModelSerializer):
    name_article = serializers.CharField(source='article.name')
    category_article = serializers.CharField(source='article.category')
    code_article = serializers.CharField(source='article.code')

    #field that refer to get_total_price method
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Sale
        fields = [
            'id', 'date', 'quantity','name_article', 'category_article', 'code_article', 'unit_selling_price', 'total_price'
            
        ]

    def get_total_price(self, obj):
        price = obj.quantity * obj.unit_selling_price
        return price



class StatSerializer(serializers.ModelSerializer):
    #display the asked statistic on the sales

    #REfer to StatViewSet annotate(). Used to know the total amount earn by each article
    total_earn = serializers.DecimalField(max_digits=15, decimal_places=2)
    article__category__display_name = serializers.CharField(max_length=255)
    last_sale = serializers.SerializerMethodField()
    
    total_qty = serializers.CharField()


 
    class Meta:
        model = Sale
        fields = [
            'article_id', 'total_earn', 'article__category__display_name', 'last_sale', 'total_qty'
            
        ] 

    def get_last_sale(self, obj):
        #display the last sale date
        last_sale = Sale.objects.values('date').order_by('-date')[:1]
        return last_sale

