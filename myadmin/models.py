from django.db import models
from django.contrib.auth.models import User


class ClientRecord(models.Model):
    GENDER_CHOICE = [("male", "Male"), ("female", "Female"), ("other", "Other")]

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    identity = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    remark = models.CharField(max_length=500, blank=True,)

    agent_fullname = models.CharField(max_length=100, blank=True)
    agent_ph = models.CharField(max_length=50, blank=True)
    agent_identity = models.CharField(max_length=50, blank=True)

    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)

    def __str__(self):
        return f"{self.full_name}"


class ClientRole(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    client_role = models.CharField(max_length=100)
    client_role_description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.client_role}"

class CourtType(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    court_type = models.CharField(max_length=100)
    court_description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.court_type}"


class Case(models.Model):
    CASE_TYPE = [
    ('MISC','MISC'),
    ('CRI','CRI'),
    ('LIT','LIT'),
    ('CONV','CONV'),
    ]


    client_role = models.ForeignKey(ClientRole, on_delete=models.CASCADE)
    ref_no = models.CharField(max_length=255, unique=True)
    clients = models.ForeignKey(ClientRecord,on_delete=models.CASCADE)
    respondent_name = models.CharField(max_length=255,blank=True)
    respondent_advocate = models.CharField(max_length=255,blank=True)
    case_type = models.CharField(max_length=255, choices=CASE_TYPE)
    case_description = models.TextField(blank=True)
    sense_of_urgent = models.CharField(max_length=20)

    # Court is Optional
    court_no = models.CharField(max_length=40, blank=True)
    court_type = models.ForeignKey(CourtType, on_delete=models.CASCADE, null=True, blank=True)
    judge_name =  models.CharField(max_length=100, blank=True)
    court_remark = models.TextField(blank=True)

    def __str__(self):
        return f"{self.ref_no}"


class Invoice(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE)
    # save_by = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    final_total = models.DecimalField(max_digits=10, decimal_places=2)
    paid  = models.BooleanField(default=False)
    short_descriptions = models.TextField(max_length=100 , blank=True)
    total_unit_price = models.DecimalField(max_digits=100, decimal_places=2)
    total_prof_service_price = models.DecimalField(max_digits=100, decimal_places=2)


    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
           return f"{self.case.ref_no}_{self.invoice_date_time}"
    
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
    

    