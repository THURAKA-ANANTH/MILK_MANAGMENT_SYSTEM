from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html
from django import forms
from .models import Customer, MilkRecord
from django.utils.timezone import now

from django.contrib import admin
from .models import MilkRecord

@admin.register(MilkRecord)
class MilkRecordAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'customer', 'milk_entry_date', 'formatted_shift', 'fat_value', 'rate_per_liter', 'quantity', 'formatted_total_price')
    list_filter = ('milk_entry_date', 'customer', 'shift')
    search_fields = ('customer__name', 'customer__can_number')

    def serial_number(self, obj):
        """ Generate serial number dynamically based on queryset order """
        queryset = MilkRecord.objects.order_by('id')  # Order by primary key to maintain consistency
        return list(queryset).index(obj) + 1  # Generates S. No dynamically

    serial_number.short_description = "S. No"  # Rename column in the admin panel

    def formatted_shift(self, obj):
        return obj.get_shift_display()  # Converts "M" to "Morning" and "E" to "Evening"

    formatted_shift.short_description = "Shift"

    def formatted_total_price(self, obj):
        return f"{obj.total_price:.2f}"

    formatted_total_price.short_description = "Total Price (₹)"



# Date range form for invoice selection
class InvoiceDateRangeForm(forms.Form):
    from_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    to_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        # If one date is provided, the other must also be provided
        if (from_date and not to_date) or (to_date and not from_date):
            raise forms.ValidationError("Both 'From Date' and 'To Date' must be provided together.")

        # Ensure from_date is not after to_date
        if from_date and to_date and from_date > to_date:
            raise forms.ValidationError("'From Date' cannot be later than 'To Date'.")

        return cleaned_data

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name', 'can_number', 'address', 'generate_invoice_button')
    search_fields = ('name', 'can_number')

    def serial_number(self, obj):
        """ Generate serial number dynamically based on queryset order """
        queryset = Customer.objects.order_by('customer_id')
        return list(queryset).index(obj) + 1  # Generates S. No dynamically

    serial_number.short_description = "S. No"  # Rename column in the admin panel

    def get_urls(self):
        """Register custom admin URL for invoice generation."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "milk_management/invoice/<int:customer_id>/",
                self.admin_site.admin_view(self.generate_invoice_view),
                name="generate_invoice_admin",
            ),
        ]
        return custom_urls + urls  # Ensure custom URLs come first

    def generate_invoice_button(self, obj):
        """Add a button in the admin panel to generate an invoice."""
        url = reverse("admin:generate_invoice_admin", args=[obj.customer_id])
        return format_html('<a class="btn btn-primary" href="{}">Generate Invoice</a>', url)

    generate_invoice_button.short_description = "Invoice"

    def generate_invoice_view(self, request, customer_id):
        """Render a form to select invoice date range."""
        customer = get_object_or_404(Customer, customer_id=customer_id)

        if request.method == "POST":
            form = InvoiceDateRangeForm(request.POST)
            if form.is_valid():
                from_date = form.cleaned_data["from_date"]
                to_date = form.cleaned_data["to_date"]
                return redirect(f"/milk_management/invoice/{customer_id}/?from_date={from_date}&to_date={to_date}")
        else:
            form = InvoiceDateRangeForm(initial={"from_date": now().date(), "to_date": now().date()})

        return render(request, "admin/invoice_date_form.html", {"form": form, "customer": customer})
