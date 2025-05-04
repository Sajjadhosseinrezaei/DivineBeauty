from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = 'order'
urlpatterns = [
    path('cart/', TemplateView.as_view(template_name='order/cart_detail.html'), name='cart_detail'),
    path('remove_from_cart/<int:product_id>/', views.RemoveCartItemView.as_view(), name='remove_from_cart'),
    path('add_to_cart/<int:id>/', views.AddCartItem.as_view(), name='add_cart'),
    path('update_quantity/<int:cart_item_id>/', views.UpdateCartQuantityView.as_view(), name='update_quantity'),
    path('resume_add_to_cart/', views.ResumeAddToCartView.as_view(), name='resume_add_to_cart'),
    path('add_cart_item_to_order/', views.AddCartItemToOrderView.as_view(), name='add_cart_item_to_order'),
    path('order_detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order_payment/<int:order_id>/', views.OrderPaymentView.as_view(), name='order_payment'),

]
