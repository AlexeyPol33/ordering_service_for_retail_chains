from rest_framework.routers import DefaultRouter

from rest_framework.routers import DefaultRouter
from app.views import UserViewSet,ShopViewSet,\
ShopsCategoriesViewSet,CategoryViewSet,ProductViewSet,\
ProductInfoViewSet,ParameterViewSet,ProductParameterViewSet,\
OrderViewSet,OrderItemViewSet,ContactViewSet

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('shop', ShopViewSet)
router.register('shopsCategories',ShopsCategoriesViewSet)
router.register('category',CategoryViewSet)
router.register('product',ProductViewSet)
router.register('productinfo',ProductInfoViewSet)
router.register('parameter',ParameterViewSet)
router.register('productparameter',ProductParameterViewSet)
router.register('order',OrderViewSet)
router.register('orderitem',OrderItemViewSet)
router.register('user/contact',ContactViewSet)

urlpatterns = router.urls