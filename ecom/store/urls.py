from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.home , name = 'home'),
    path('login/' , views.login_user , name = 'login'),
    path('logout/' , views.logout_user , name = 'logout'),
    path('register/' , views.register , name = 'register'),
    path('product/<int:pk>' , views.product , name = 'product'),
    path('products/', views.product_list, name='product_list'), 
]
