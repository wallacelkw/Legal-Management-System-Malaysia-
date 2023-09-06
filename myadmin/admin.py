from django.contrib import admin
from .models import Record, cusRecord, CaseType, CourtType, Case, Client

admin.site.register(Record)
admin.site.register(cusRecord)
admin.site.register(CaseType)
admin.site.register(CourtType)

admin.site.register(Case)
admin.site.register(Client)
