from django.db import models
from core.models import Employee
from products.models import Product
from suppliers.models import Supplier

# Create your models here.


class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("canceled", "Canceled"),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('credit', 'Credit Card'),
        ('bank', 'Bank Transfer'),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="orders")
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_orders")
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_orders")
    
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')
    notes = models.TextField(blank=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_total_amount(self):
        self.total_amount = sum(item.total_price for item in self.items.all())
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.order_number:
            last_order = PurchaseOrder.objects.all().order_by('id').last()
            if last_order and last_order.order_number:
                try:
                    last_id = int(last_order.order_number.split('-')[1])
                except:
                    last_id = 0
                self.order_number = f"ORDER-{last_id + 1}"
            else:
                self.order_number = "ORDER-1"
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Purchase Orders'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-created_date']

    def __str__(self):
        return f"Order {self.order_number} - {self.supplier.name}"


class PurchaseOrderItem(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def unit_price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
