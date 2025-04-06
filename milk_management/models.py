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
    rate_per_liter_person = models.DecimalField(
        max_digits=6, decimal_places=3, default=Decimal("0.000"), null=False, blank=False
    ) 
    def __str__(self):
         return f"{self.name} (Can Number: {self.can_number}) - Rate: ₹ {format(self.rate_per_liter_person, '.2f')}"

class MilkRecord(models.Model):
    SHIFT_CHOICES = [
        ("M", "Morning"),
        ("E", "Evening"),
    ]

    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)  # Link to Customer model
    date = models.DateField(auto_now_add=True)  # System-generated date
    milk_entry_date = models.DateField()  # User-provided date
    fat_value = models.DecimalField(max_digits=5, decimal_places=3)  # Up to 99.999
    quantity = models.DecimalField(max_digits=7, decimal_places=3)  # Up to 9999.999
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    shift = models.CharField(max_length=1, choices=SHIFT_CHOICES, null=False, blank=False)  # Mandatory field

    def save(self, *args, **kwargs):
        # Validate shift before saving
        if self.shift not in dict(self.SHIFT_CHOICES):
            raise ValidationError("Invalid shift. Choose 'M' for Morning or 'E' for Evening.")

        # Get rate_per_liter_person from the related Customer
        rate_per_liter = self.customer.rate_per_liter_person

        # Calculate total price based on fat_value, rate, and quantity
        total_price_value = (self.fat_value * rate_per_liter * self.quantity) / Decimal("10")

        # Truncate total_price to 2 decimal places without rounding
        total_price_str = str(total_price_value).split(".")
        if len(total_price_str) == 2:
            truncated_value = total_price_str[0] + "." + total_price_str[1][:2]  # Keep first two decimal places
        else:
            truncated_value = total_price_str[0]  # No decimal part

        # Convert back to Decimal and store
        self.total_price = Decimal(truncated_value)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.name} - {self.milk_entry_date} - {self.get_shift_display()}"