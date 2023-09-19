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

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

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
        return f"{self.case_no}"


class Invoice(models.Model):
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
    # save_by = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    final_total = models.DecimalField(max_digits=10, decimal_places=2)
    paid  = models.BooleanField(default=False)
    short_descriptions = models.TextField(max_length=100 , null=True)
    total_unit_price = models.DecimalField(max_digits=1000, decimal_places=2)
    total_prof_service_price = models.DecimalField(max_digits=1000, decimal_places=2)


    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
           return f"{self.case.case_no}_{self.invoice_date_time}"
    
    @property
    def get_total(self):
        articles = self.article_set.all()   
        total = sum(article.get_total for article in articles)
        return total 
    

class ProfService(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    prof_service = models.CharField(max_length=100)
    prof_service_price = models.DecimalField(max_digits=1000, decimal_places=2)
    

    class Meta:
        verbose_name = 'ProfService'
        verbose_name_plural = 'ProfService'

    @property
    def get_total(self):
        total = self.prof_service_price   
        return total 

    
class ReimburService(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    service = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=1000, decimal_places=2)
    

    class Meta:
        verbose_name = 'ReimburService'
        verbose_name_plural = 'ReimburService'

    @property
    def get_total(self):
        total = self.unit_price   
        return total
    

    