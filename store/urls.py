from django.urls import path
from . import views
from pprint import pprint
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('carts',views.CartViewSet)
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)

# pprint(router.urls)

products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

urlpatterns =router.urls+products_router.urls