from django.contrib import admin
from .models import ClientRecord, CaseType, CourtType, Case

# admin.site.register(Record)
# admin.site.register(cusRecord)
admin.site.register(ClientRecord)
admin.site.register(CaseType)
admin.site.register(CourtType)
admin.site.register(Case)
