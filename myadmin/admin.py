from django.contrib import admin
from .models import ClientRecord, CaseType, CourtType, Case, Invoice,ProfService,ReimburService

# admin.site.register(Record)
# admin.site.register(cusRecord)
admin.site.register(ClientRecord)
admin.site.register(CaseType)
admin.site.register(CourtType)
admin.site.register(Case)

admin.site.register(Invoice)
admin.site.register(ProfService)
admin.site.register(ReimburService)
