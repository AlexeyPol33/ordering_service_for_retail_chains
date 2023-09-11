"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from app.views import home, OrderConfirmation, PartnerUpdate, social_auth_callback
from rest_framework_simplejwt.views\
    import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('social/', include('social_django.urls', namespace='social')),
    path('social/token/',social_auth_callback),
    path('', home),
    path('admin/', admin.site.urls),
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
        ),
    path(
        'api/order/confirm/',
        OrderConfirmation.as_view(),
        name='confirm_order'
        ),
    path('api/shop/upload/', PartnerUpdate.as_view()),
    path('api/shop/upload/<int:number>/', PartnerUpdate.as_view()),
    path('api/', include('app.urls')),
]
