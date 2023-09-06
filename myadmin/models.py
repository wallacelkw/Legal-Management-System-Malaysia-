from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class cusRecord(models.Model):
    GENDER_CHOICE = [("male", "Male"), ("female", "Female"), ("other", "Other")]

    RELATIONSHIP_CHOICE = [
        ("parent", "Parent"),
        ("spouse", "Spouse"),
        ("sibling", "Sibling"),
        ("friend", "Friend"),
        ("other", "Other"),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    emergency_contact_full_name = models.CharField(max_length=100)
    emergency_contact_relationship = models.CharField(
        max_length=20, choices=RELATIONSHIP_CHOICE
    )
    emergency_contact_email = models.EmailField()
    emergency_contact_phone_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CaseType(models.Model):
    # created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    case_type = models.CharField(max_length=100)
    case_description = models.CharField(max_length=500)


class CourtType(models.Model):
    # created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    court_type = models.CharField(max_length=100)
    court_description = models.CharField(max_length=500)


# class Case(models.Model):
#     case_id = models.CharField(primary_key=True, max_length=50, default='CASE-00001')
#     case_name = models.CharField(max_length=255)
#     # Add other fields related to your case

# class Client(models.Model):
#     case = models.ForeignKey(Case, on_delete=models.CASCADE)
#     client_name = models.CharField(max_length=255)
#     role = models.CharField(max_length=255)
#     respondent_name = models.CharField(max_length=255)
#     respondent_advocate = models.CharField(max_length=255)


# models.py


# from django.db import models


class Case(models.Model):
    case_name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(default='SOME STRING')  # Default value



class Client(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    client_role = models.CharField(max_length=255)  # Updated field name for clarity
    respondent_name = models.CharField(max_length=255)
    respondent_advocate = models.CharField(max_length=255)
