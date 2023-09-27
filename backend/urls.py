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
from app.views import home, OrderConfirmation, \
    PartnerUpdate, ConfirmRegistration, social_auth_callback
from drf_spectacular.views import SpectacularAPIView, \
    SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views\
    import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/schema/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='docs'),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'),
    path('social/token/', social_auth_callback),
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
    path(
        'api/user/confirm/<str:task_id>/',
        ConfirmRegistration.as_view(),
        name='confirm-registration'),
    path('api/shop/upload/<str:task_id>/', PartnerUpdate.as_view()),
    path('silk/', include('silk.urls', namespace='silk')),
    path('social/', include('social_django.urls', namespace='social')),
    path('api/', include('app.urls')),
]
