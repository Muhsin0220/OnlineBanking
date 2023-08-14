"""
URL configuration for bank project.

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
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from accounts.views import register,verify_otp,login,forgetpassword,changePassword,wallet_detail,wallet_update,transaction_create,transaction_list




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/',register,name='register'),
    path('api/verify/',verify_otp,name='verify'),
    path('api/login/',login,name='login'),
    path('api/forgetpassword/',forgetpassword,name='forget'),
    path('api/changepassword/',changePassword,name='changepassword'),
    path('api/wallet/', wallet_detail, name='wallet_detail'),
    path('api/wallet/update/',wallet_update, name='wallet_update'),
    path('api/transaction/create/',transaction_create,name='transaction_create'),
    path('api/transaction/list/',transaction_list,name='transaction_list'),
    path('api/token/',ObtainAuthToken.as_view())
]
