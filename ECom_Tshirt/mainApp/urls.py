from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ProductView.as_view(), name='index'),
    path('home/', views.ProductView.as_view(), name='index'),
    path('product-detail/<int:pk>',
         views.ProductDetailView.as_view(), name='product-detail'),
    path('shop', views.ShopView.as_view(), name='shop'),
    path('shop-category/<slug:item>',
         views.ShopCetegoryView.as_view(), name='shop-category'),
    path('register_page/', views.register_page,
         name="register_page"),
    path('login_page', views.login_page, name="login_page"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_page'), name="logout"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('cart/', views.addcart, name="cart"),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('showcart/', views.show_cart, name="showcart"),
    path('checkout/', views.checkout, name="checkout"),
    path('paymentdone/', views.payment_done, name="paymentdone"),
    path('oders/', views.oders, name="oders"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
