from django.shortcuts import render, redirect
from .models import Offender, Violation
import uuid
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# from twilio.rest import Client
from django.conf import settings

# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect('/login/')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dash')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

@login_required(login_url='/login/')
def dash(request):
    violations = Violation.objects.select_related('offender').order_by('-date_reported')
    return render(request, 'dash.html', {'violations': violations})

@login_required(login_url='/login/')
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

        return redirect('dash')

    return render(request, 'add-violation.html')

# def send_sms(phone_number, ticket_details):
#     """Helper function to send SMS to the offender"""
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
#     message = client.messages.create(
#         body=ticket_details,
#         from_=settings.TWILIO_PHONE_NUMBER,  # Twilio phone number
#         to=phone_number
#     )
#     return message.sid 

# def add_violation(request):
#     if request.method == 'POST':
#         full_name = request.POST['full_name']
#         plate_number = request.POST['plate_number']
#         phone_number = request.POST['phone_number']
#         offense_type = request.POST['offense_type']
#         location = request.POST['location']
#         fine_amount = request.POST['fine_amount']

#         offender, _ = Offender.objects.get_or_create(
#             plate_number=plate_number,
#             defaults={'full_name': full_name, 'phone_number': phone_number}
#         )

#         violation = Violation.objects.create(
#             offender=offender,
#             offense_type=offense_type,
#             location=location,
#             fine_amount=fine_amount,
#             ticket_id=str(uuid.uuid4()).replace('-', '')[:10].upper()
#         )

#         # Send SMS to the offender with ticket details
#         ticket_details = (
#             f"Your traffic ticket details:\n"
#             f"Ticket ID: {violation.ticket_id}\n"
#             f"Plate Number: {offender.plate_number}\n"
#             f"Offense: {violation.offense_type}\n"
#             f"Location: {violation.location}\n"
#             f"Fine Amount: ₦{violation.fine_amount}\n"
#             f"Please make sure to pay your fine promptly."
#         )
        
#         send_sms(phone_number, ticket_details)

#         return redirect('dash')

#     return render(request, 'add-violation.html')


def landing_page(request):
    ticket = None

    if 'ticket_id' in request.GET or 'plate_number' in request.GET:
        ticket_id = request.GET.get('ticket_id')
        plate_number = request.GET.get('plate_number')

        if ticket_id:
            ticket = Violation.objects.filter(ticket_id=ticket_id).first()
        elif plate_number:
            ticket = Violation.objects.filter(offender__plate_number=plate_number).first()

    return render(request, 'search.html', {'ticket': ticket})

def update_status(request, id):
    violation_id = Violation.objects.get(id=id)
    violation_id.status = True
    violation_id.save()
    return redirect("/dash/")