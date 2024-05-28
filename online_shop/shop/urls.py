from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('view_product/<int:pk>', views.ProductView.as_view(), name='view_product'),
    path('add_to_cart/<pk>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('delete_cart_product/<int:pk>/<str:size>/', views.delete_cart_item, name='delete_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('Success', views.order_success, name='order_success'),
    path('Orders/', views.order_view, name='user_orders'),
    path('search-query/', views.search_results, name='search_results'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)