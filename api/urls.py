from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('vendors/create_vendor/', views.create_vendor, name='create_vendor'),
    path('vendors/<int:vendor_id>/', views.get_vendor_details, name='get_vendor_details'),
    path('vendors/<int:vendor_id>/update_vendor/', views.update_vendor, name='update_vendor'),
    path('vendors/<int:vendor_id>/delete_vendor', views.delete_vendor, name='delete_vendor'),
    path('purchase_orders/create_order', views.create_purchase_order, name='create_purchase_order'),
    path('purchase_orders/', views.list_purchase_orders, name='list_purchase_orders'),
    path('purchase_orders/<int:po_id>/get_purchase_order_details', views.get_purchase_order_details, name='get_purchase_order_details'),
    path('purchase_orders/<int:po_id>/update_purchase_order', views.update_purchase_order, name='update_purchase_order'),
    path('purchase_orders/<int:po_id>/delete_purchase_order', views.delete_purchase_order, name='delete_purchase_order'),
    path('vendors/<int:vendor_id>/performance/', views.get_vendor_performance, name='get_vendor_performance'),
]

