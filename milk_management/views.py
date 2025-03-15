
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_date
from .models import Customer, MilkRecord

def generate_invoice(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)

    # Get date range from GET parameters (default to None)
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    # Initialize milk records queryset
    milk_records = MilkRecord.objects.filter(customer=customer)

    # Apply date filtering if both dates are provided
    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        if from_date and to_date:  # Ensure parsed dates are valid
            milk_records = milk_records.filter(milk_entry_date__range=[from_date, to_date])

    # Ensure records are ordered by `milk_entry_date` in ascending order
    milk_records = milk_records.order_by("milk_entry_date")

    # Calculate total amount
    total_amount = sum(record.total_price for record in milk_records)

    return render(request, "invoice_template.html", {
        "customer": customer,
        "milk_records": milk_records,
        "from_date": from_date,
        "to_date": to_date,
        "total_amount": total_amount
    })
