from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

#vendor model
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
#purchase order model
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])
    quality_rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO #{self.po_number} for {self.vendor.name}"

#Historical performance model
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"Historical Performance for {self.vendor.name} on {self.date}"
    

#django signal for calculating On-Time Delivery Rate
def update_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.delivery_date <= timezone.now():
        completed_orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed',
            delivery_date__lte=timezone.now()
        )
        on_time_delivery_count = completed_orders.count()
        total_completed_orders = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').count()

        if total_completed_orders > 0:
            on_time_delivery_rate = (on_time_delivery_count / total_completed_orders) * 100

            # Update on_time_delivery_rate in Vendor model
            instance.vendor.on_time_delivery_rate = on_time_delivery_rate
            instance.vendor.save()

            # Create or update HistoricalPerformance record
            historical_performance, created = HistoricalPerformance.objects.get_or_create(
                vendor=instance.vendor,
                date=timezone.now(),
                defaults={
                    'on_time_delivery_rate': on_time_delivery_rate,
                    'quality_rating_avg': instance.vendor.quality_rating_avg,
                    'average_response_time': instance.vendor.average_response_time,
                    'fulfillment_rate': instance.vendor.fulfillment_rate,
                }
            )

            # If the record already exists, update the on_time_delivery_rate
            if not created:
                historical_performance.on_time_delivery_rate = on_time_delivery_rate
                historical_performance.save()

# Connect the signal
post_save.connect(update_on_time_delivery_rate, sender=PurchaseOrder)

#django signal for calculating quality rating avarage
def update_quality_rating_avg(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        completed_orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed',
            quality_rating__isnull=False
        )
        total_completed_orders = completed_orders.count()

        if total_completed_orders > 0:
            quality_rating_sum = completed_orders.aggregate(sum_rating=models.Sum('quality_rating'))['sum_rating']
            quality_rating_avg = quality_rating_sum / total_completed_orders

            # Update quality_rating_avg in Vendor model
            instance.vendor.quality_rating_avg = quality_rating_avg
            instance.vendor.save()

            # Create or update HistoricalPerformance record
            historical_performance, created = HistoricalPerformance.objects.get_or_create(
                vendor=instance.vendor,
                date=timezone.now(),
                defaults={
                    'on_time_delivery_rate': instance.vendor.on_time_delivery_rate,
                    'quality_rating_avg': quality_rating_avg,
                    'average_response_time': instance.vendor.average_response_time,
                    'fulfillment_rate': instance.vendor.fulfillment_rate,
                }
            )

            # If the record already exists, update the quality_rating_avg
            if not created:
                historical_performance.quality_rating_avg = quality_rating_avg
                historical_performance.save()

# Connect the signal
post_save.connect(update_quality_rating_avg, sender=PurchaseOrder)

#django signal for calculating average response time
def update_average_response_time(sender, instance, **kwargs):
    if instance.acknowledgment_date is not None:
        completed_orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            acknowledgment_date__isnull=False
        )
        total_completed_orders = completed_orders.count()

        if total_completed_orders > 0:
            response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_orders]
            average_response_time = sum(response_times) / total_completed_orders

            # Update average_response_time in Vendor model
            instance.vendor.average_response_time = average_response_time
            instance.vendor.save()

            # Create or update HistoricalPerformance record
            historical_performance, created = HistoricalPerformance.objects.get_or_create(
                vendor=instance.vendor,
                date=timezone.now(),
                defaults={
                    'on_time_delivery_rate': instance.vendor.on_time_delivery_rate,
                    'quality_rating_avg': instance.vendor.quality_rating_avg,
                    'average_response_time': average_response_time,
                    'fulfillment_rate': instance.vendor.fulfillment_rate,
                }
            )

            # If the record already exists, update the average_response_time
            if not created:
                historical_performance.average_response_time = average_response_time
                historical_performance.save()

# Connect the signal
post_save.connect(update_average_response_time, sender=PurchaseOrder)

#django signal for calculating and updating fulfillment rate
def update_fulfilment_rate(sender, instance, **kwargs):
    all_completed_orders = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed')
    successfully_fulfilled_orders = all_completed_orders.exclude(quality_rating__isnull=True)

    total_orders = PurchaseOrder.objects.filter(vendor=instance.vendor).count()
    total_fulfilled_orders = successfully_fulfilled_orders.count()

    if total_orders > 0:
        fulfilment_rate = (total_fulfilled_orders / total_orders) * 100

        # Update fulfilment_rate in Vendor model
        instance.vendor.fulfillment_rate = fulfilment_rate
        instance.vendor.save()

        # Create or update HistoricalPerformance record
        historical_performance, created = HistoricalPerformance.objects.get_or_create(
            vendor=instance.vendor,
            date=instance.delivery_date,  # Use delivery_date as the date for fulfilment_rate
            defaults={
                'on_time_delivery_rate': instance.vendor.on_time_delivery_rate,
                'quality_rating_avg': instance.vendor.quality_rating_avg,
                'average_response_time': instance.vendor.average_response_time,
                'fulfillment_rate': fulfilment_rate,
            }
        )

        # If the record already exists, update the fulfilment_rate
        if not created:
            historical_performance.fulfillment_rate = fulfilment_rate
            historical_performance.save()

# Connect the signal
post_save.connect(update_fulfilment_rate, sender=PurchaseOrder)