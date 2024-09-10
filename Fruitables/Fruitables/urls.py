
from django.contrib import admin
from django.urls import path
from fruitable import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('contact', views.contact, name='contact'),
    path('product/<str:Name>', views.product, name='product'),
    path('shop', views.shop, name='shop'),
    path('testimonial', views.testimonial, name='testimonial'),
    path('update-cart-quantity', views.update_cart_quantity, name='update_cart_quantity'),
    path('delete-cart-quantity', views.delete_cart_quantity, name='delete_cart_quantity'),
    path('add-cart-quantity', views.add_cart_quantity, name='add_cart_quantity'),
    path('account', views.account, name='account'),
    path('login/', views.loginuser, name='loginuser'),
    path('account/logout', views.logoutuser, name='logoutuser'),
]
handler404 = views.custom404
handler500 = views.custom500