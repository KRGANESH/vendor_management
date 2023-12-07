
# Vendor Management System

This repository contains the source code for a Vendor Management System developed using Django and Django REST Framework. The system handles vendor profiles, tracks purchase orders, and calculates vendor performance metrics.

## Getting Started
**Prerequisites**
* Python (3.8 or higher)
* Django
* Django REST Framework

## Installation

1. Clone the repository
2. ``` cd vendor-management-system ```
3. Run ```python manage.py migrate```
4. Create superuser ```python manage.py createsuperuser```
5. Run ```python manage.py runserver```
6. Use http://127.0.0.1:8000/admin to add initial data.



## API Reference
**Vendor Profile Management**

#### Create a new vendor
Request are send to the following endpoint:
```http
  http://127.0.0.1:8000/vendors/create_vendor/
```
with the following body:
``` 
{
    "name": "New Vendor",
    "contact_details": "Vendor Contact",
    "address": "Vendor Address",
    "vendor_code": "111"
} 
 ```

#### List all vendor
Request are send to the following endpoint:
```http
  http://127.0.0.1:8000
```
#### Retrieve a specific vendor's details
Request are send to the following endpoint:
```http
  http://127.0.0.1:8000/vendors/<int:vendor_id>/
```
vendor_id is the id of required vendor

#### Update a vendor's details.
Request are send to the following endpoint:
```http
  http://127.0.0.1:8000/vendors/<int:vendor_id>/update_vendor/
```
with the following body:
``` 
{
    "name": "New Vendor",
    "contact_details": "Vendor Contact",
    "address": "Vendor Address",
    "vendor_code": "111"
} 
 ```
 vendor_id is the id of required vendor

#### Delete a vendor
Request are send to the following endpoint:
```http
  http://127.0.0.1:8000/vendors/<int:vendor_id>/delete_vendor
```
vendor_id is the id of required vendor

**Purchase Order Tracking**

#### Create a purchase order
Request are send to the following endpoint:
```http
  http://127.0.0.1:8000/purchase_orders/create_order
```
with the following body:
``` 
{
    "po_number": "",
    "order_date": "",
    "delivery_date": "",
    "items": [
        {
            "item_name": "",
            "price":
        },
        {
            "item_name": "",
            "price": 
        }
    ],
    "quantity": ,
    "status": "",
    "quality_rating": ,
    "issue_date": "",
    "acknowledgment_date": ,
    "vendor": 
}

 ```
#### List all purchase orders with an option to filter by vendor
Request are send to the following endpoint:
```http
  http://127.0.0.1:8000/purchase_orders/
```
To filter by vendor use the endpoint for passing the required vendor_id:
```http
  http://127.0.0.1:8000/purchase_orders/?vendor_id=vendor_id
```
#### Retrieve details of a specific purchase order

Request are send to the following endpoint:
```http
  http://127.0.0.1:8000/purchase_orders/<int:po_id>/get_purchase_order_details
```
po_id is the id of the required purchase order.

#### Update a purchase order

Request are send to the following endpoint:
```http
  http://127.0.0.1:8000/purchase_orders/<int:po_id>/update_purchase_order
```
po_id is the id of required purchase order.

#### Delete purchase order

Request are send to the following endpoint:
```http
  http://127.0.0.1:8000/purchase_orders/<int:po_id>/delete_purchase_order
```
po_id is the id of required purchase order.

**Vendor Performance Evaluation**

#### Retrieve a vendor's performance metrics

Request are send to the following endpoint:
```http
  http://127.0.0.1:8000/vendors/<int:vendor_id>/performance
```
vendor_id is the id of required vendor

## Test Suit ##
Run ``` python manage.py test ```
