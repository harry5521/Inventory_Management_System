from django.db import models
from core.models import Employee
from products.models import Product
from suppliers.models import Supplier

# Create your models here.


class PurchaseOrder(models.Model):
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('credit', 'Credit Card'),
        ('bank', 'Bank Transfer'),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="orders")
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_orders")
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_orders")
    
    order_date = models.DateField(auto_now_add=True)
    
    status = models.CharField(max_length=10, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')
    notes = models.TextField(blank=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_total_amount(self):
        self.total_amount = sum(item.total_price for item in self.items.all())
        self.save()

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
