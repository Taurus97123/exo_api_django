from django.urls import path, include

from rest_framework import routers
from sales.views import ArticleViewSet, SaleViewSet, StatViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register('articles', ArticleViewSet, 'article')
router.register('sales', SaleViewSet, 'sale')
router.register('stats', StatViewSet, 'stat')

urlpatterns = [
    
    path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
            ]
        ),
    ),
]
