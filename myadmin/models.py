from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4

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



    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}"
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.full_name, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.full_name, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(ClientRecord, self).save(*args, **kwargs)


class ClientRole(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    client_role = models.CharField(max_length=100)
    client_role_description = models.CharField(max_length=500, blank=True)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.client_role}"
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.client_role, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.client_role, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(ClientRole, self).save(*args, **kwargs)

class CourtType(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    court_type = models.CharField(max_length=100)
    court_description = models.CharField(max_length=500, blank=True)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.court_type}"
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.court_type, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.court_type, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(CourtType, self).save(*args, **kwargs)


class Case(models.Model):
    CASE_TYPE = [
    ('MISC','MISC'),
    ('CRI','CRI'),
    ('LIT','LIT'),
    ('CONV','CONV'),
    ]

    ref_no = models.CharField(max_length=255, unique=True)
    client_role = models.ForeignKey(ClientRole, on_delete=models.CASCADE)
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

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.ref_no}"
    

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.ref_no, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.ref_no, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Case, self).save(*args, **kwargs)


class Invoice(models.Model):
    # case = models.OneToOneField(Case, on_delete=models.CASCADE)
    # save_by = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_date_time = models.DateField(auto_now_add=True, null=True, blank=True)
    final_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid  = models.BooleanField(default=False, null=True, blank=True)
    short_descriptions = models.TextField(max_length=1000, null=True, blank=True)
    total_reimbur_service_price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    total_prof_service_price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)

    number = models.CharField(null=True, blank=True, max_length=100)

    #RELATED fields
    case = models.OneToOneField(Case, blank=True, null=True, on_delete=models.SET_NULL)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
           return f"{self.case}_{self.invoice_date_time}"
    
    @property
    def get_total(self):
        articles = self.article_set.all()   
        total = sum(article.get_total for article in articles)
        return total
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.number, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.number, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Invoice, self).save(*args, **kwargs)

class ProfService(models.Model):

    prof_service = models.CharField(max_length=100)
    prof_service_price = models.DecimalField(max_digits=1000, decimal_places=2)
    

    #Related Fields
    invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.CASCADE)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'ProfService'
        verbose_name_plural = 'ProfService'

    @property
    def get_total(self):
        total = self.prof_service_price   
        return total

    def save(self, *args, **kwargs):
            if self.date_created is None:
                self.date_created = timezone.localtime(timezone.now())
            if self.uniqueId is None:
                self.uniqueId = str(uuid4()).split('-')[4]
                self.slug = slugify('{} {}'.format(self.prof_service, self.uniqueId))

            self.slug = slugify('{} {}'.format(self.prof_service, self.uniqueId))
            self.last_updated = timezone.localtime(timezone.now())

            super(ProfService, self).save(*args, **kwargs)
    
class ReimburService(models.Model):
   
    reimbur_service = models.CharField(null=True, blank=True, max_length=100)
    reimbur_service_price = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
 
    #Related Fields
    invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.CASCADE)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'ReimburService'
        verbose_name_plural = 'ReimburService'

    @property
    def get_total(self):
        total = self.reimbur_service_price   
        return total
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.reimbur_service, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.reimbur_service, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(ReimburService, self).save(*args, **kwargs)
    



# class Transaction(models.Model):

#     transaction_data = models.DateField(auto_now_add=True, null=True, blank=True)
#     transaction_description = models.CharField(null=True, blank=True, max_length=100)
#     debit_transaction = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
#     credit_transaction = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
#     balance = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)

#     paid  = models.BooleanField(default=False, null=True, blank=True)
#     invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.CASCADE)

#     #Utility fields
#     uniqueId = models.CharField(null=True, blank=True, max_length=100)
#     slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
#     date_created = models.DateTimeField(blank=True, null=True)
#     last_updated = models.DateTimeField(blank=True, null=True)

#     def save(self, *args, **kwargs):
#         if self.date_created is None:
#             self.date_created = timezone.localtime(timezone.now())
#         if self.uniqueId is None:
#             self.uniqueId = str(uuid4()).split('-')[4]
#             self.slug = slugify('{} {}'.format(self.reimbur_service, self.uniqueId))

#         self.slug = slugify('{} {}'.format(self.reimbur_service, self.uniqueId))
#         self.last_updated = timezone.localtime(timezone.now())

#         super(Transaction, self).save(*args, **kwargs)