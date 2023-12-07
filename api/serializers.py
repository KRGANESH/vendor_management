from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance



#Serializer for create vendor
class CreateVendorSerializer(serializers.ModelSerializer):
    class Meta :
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code']

#Serializer for vendor
class VendorSerializer(serializers.ModelSerializer):
    class Meta :
        model = Vendor
        fields = '__all__'


#Serializer for purchase order
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta :
        model = PurchaseOrder
        fields = '__all__'

