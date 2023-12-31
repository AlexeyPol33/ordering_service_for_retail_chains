from rest_framework.routers import DefaultRouter
from app.views import UserViewSet, ShopViewSet, \
    ProductViewSet, ProductInfoViewSet, \
    OrderViewSet, OrderItemViewSet, ContactViewSet

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('shop',  ShopViewSet)
router.register('product', ProductViewSet)
router.register('productinfo', ProductInfoViewSet)
router.register('order', OrderViewSet)
router.register('orderitem', OrderItemViewSet)
router.register('user/contact', ContactViewSet)

urlpatterns = router.urls
