from django.shortcuts import render, redirect
from .models import Offender, Violation
import uuid

# Create your views here.


def login(request):
    return render(request, 'login.html')

def dash(request):
    return render(request, 'dash.html')

def add_violation(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        plate_number = request.POST['plate_number']
        phone_number = request.POST['phone_number']
        offense_type = request.POST['offense_type']
        location = request.POST['location']
        fine_amount = request.POST['fine_amount']

        offender, _ = Offender.objects.get_or_create(
            plate_number=plate_number,
            defaults={'full_name': full_name, 'phone_number': phone_number}
        )

        violation = Violation.objects.create(
            offender=offender,
            offense_type=offense_type,
            location=location,
            fine_amount=fine_amount,
            ticket_id=str(uuid.uuid4()).replace('-', '')[:10].upper()
        )

        return redirect('dashboard')

    return render(request, 'add-violation.html')
