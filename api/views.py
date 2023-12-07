from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Vendor, PurchaseOrder
from .serializers import CreateVendorSerializer, VendorSerializer, PurchaseOrderSerializer
from rest_framework import status



#List all vendors
@api_view(['GET'])
def getData(request):
    vendor = Vendor.objects.all()
    serializer = VendorSerializer(vendor, many=True)
    return Response(serializer.data)

#Create a new vendor
@api_view(['POST'])
def create_vendor(request):
    if request.method == 'POST':
        serializer = CreateVendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Retrieve a specific vendor's details.
@api_view(['GET'])
def get_vendor_details(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = VendorSerializer(vendor)
    return Response(serializer.data)

#Update a vendor's details
@api_view(['PUT'])
def update_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = VendorSerializer(vendor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete vendor
@api_view(['DELETE'])
def delete_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
        vendor.delete()
        return Response({'message': 'Vendor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)


#Create purcahse order
@api_view(['POST'])
def create_purchase_order(request):
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#List Purchase order
@api_view(['GET'])
def list_purchase_orders(request):
    vendor_id = request.query_params.get('vendor_id', None)

    if vendor_id is not None:
        # If vendor_id is provided, filter purchase orders by vendor
        purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id)
    else:
        # If no vendor_id is provided, retrieve all purchase orders
        purchase_orders = PurchaseOrder.objects.all()

    serializer = PurchaseOrderSerializer(purchase_orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Retrieve details of a specific purchase order
@api_view(['GET'])
def get_purchase_order_details(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
    

#Update purchase order
@api_view(['PUT'])
def update_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
#Delete purchase order
@api_view(['DELETE'])
def delete_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        purchase_order.delete()
        return Response({'message': 'Purchase Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
    

#Performance metrics
@api_view(['GET'])
def get_vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
        performance_data = {
            'Vendor':vendor.name,
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_data, status=status.HTTP_200_OK)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)