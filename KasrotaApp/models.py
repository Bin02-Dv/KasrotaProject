from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Offender(models.Model):
    full_name = models.CharField(max_length=100, blank=True)
    plate_number = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.plate_number}"


class Violation(models.Model):
    offender = models.ForeignKey(Offender, on_delete=models.CASCADE)
    offense_type = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.BooleanField(default=False) 

    ticket_id = models.CharField(max_length=200, blank=True, unique=True)

    def __str__(self):
        return f"{self.offense_type} - {self.ticket_id}"
