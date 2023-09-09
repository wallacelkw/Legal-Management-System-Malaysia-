from django.db import models
from django.contrib.auth.models import User


class ClientRecord(models.Model):
    GENDER_CHOICE = [("male", "Male"), ("female", "Female"), ("other", "Other")]

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    identity = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    remark = models.CharField(max_length=500, blank=True, null=True)

    agent_fullname = models.CharField(max_length=100, blank=True, null=True)
    agent_ph = models.CharField(max_length=50, blank=True, null=True)
    agent_identity = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}"


class CaseType(models.Model):
    # created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    case_type = models.CharField(max_length=100)
    case_description = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.case_type}"

class CourtType(models.Model):
    # created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    court_type = models.CharField(max_length=100)
    court_description = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.court_type}"


class Case(models.Model):
    CLIENT_ROLE = [
    ('Petitioner','Petitioner'),
    ('Respondent','Respondent')
    ]


    case_type = models.ForeignKey(CaseType, on_delete=models.CASCADE)
    case_no = models.CharField(max_length=255, unique=True)
    stage_of_case = models.CharField(max_length=100)
    clients = models.ForeignKey(ClientRecord,on_delete=models.CASCADE)
    respondent_name = models.CharField(max_length=255)
    respondent_advocate = models.CharField(max_length=255)
    client_role = models.CharField(max_length=255, choices=CLIENT_ROLE)
    case_description = models.TextField(blank=True, null=True)
    sense_of_urgent = models.CharField(max_length=20)
    court_no = models.CharField(max_length=40)
    court_type = models.ForeignKey(CourtType, on_delete=models.CASCADE)
    judge_name =  models.CharField(max_length=100, blank=True, null=True)
    court_remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.case_no} - {self.case_type, self.court_no}"


# class CaseClient(models.Model):
#     case_no = models.ForeignKey(Case, on_delete=models.CASCADE)
#     clients = models.ForeignKey(ClientRecord, on_delete=models.CASCADE)
#     respondent_name = models.CharField(max_length=255)
#     respondent_advocate = models.CharField(max_length=255)
#     client_role = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.clients} - {self.case_no}"
