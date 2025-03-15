from django.db import models
from django.core.exceptions import ValidationError

from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
import math



class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)  # Primary key (auto-incremented)
    name = models.CharField(max_length=255)
    can_number = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} (Can Number: {self.can_number})"


class MilkRecord(models.Model):
    SHIFT_CHOICES = [
        ("M", "M"),  # Morning
        ("E", "E"),  # Evening
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)  # System-generated date
    milk_entry_date = models.DateField()  # User-provided date (no default)
    fat_value = models.DecimalField(max_digits=5, decimal_places=3)  # Up to 99.999
    rate_per_liter = models.DecimalField(max_digits=6, decimal_places=3)  # Up to 999.999
    quantity = models.DecimalField(max_digits=7, decimal_places=3)  # Up to 9999.999
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.000)
    shift = models.CharField(max_length=1, choices=SHIFT_CHOICES, null=False, blank=False)  # Mandatory field

    def save(self, *args, **kwargs):
        # Validate shift before saving
        if self.shift not in dict(self.SHIFT_CHOICES):
            raise ValidationError("Invalid shift. Choose 'M' for Morning or 'E' for Evening.")
        
        # Always recalculate total_price before saving
        self.total_price = math.floor((self.fat_value * self.rate_per_liter * self.quantity) / Decimal("10"))

        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.name} - {self.milk_entry_date} - {self.get_shift_display()}"