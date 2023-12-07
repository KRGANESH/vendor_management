from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .serializers import CreateVendorSerializer

class VendorAPITest(TestCase):
    def test_create_vendor(self):
        client = APIClient()

        # Data for creating a new vendor
        vendor_data = {
            "name": "New Vendor",
            "contact_details": "Vendor Contact",
            "address": "Vendor Address",
            "vendor_code": "111"
        }

        # Make a POST request to create a new vendor
        response = client.post('/vendors/create_vendor/', data=vendor_data, format='json')

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the vendor was created successfully
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], vendor_data['name'])
        # Add more assertions based on your serializer and expected data

    # Add more test methods for other endpoints if needed
