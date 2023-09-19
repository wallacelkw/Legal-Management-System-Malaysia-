from django.contrib import admin
from .models import ClientRecord, ClientRole, CourtType, Case, Invoice,ProfService,ReimburService

# admin.site.register(Record)
# admin.site.register(cusRecord)
admin.site.register(ClientRecord)
admin.site.register(ClientRole)
admin.site.register(CourtType)
admin.site.register(Case)

admin.site.register(Invoice)
admin.site.register(ProfService)
admin.site.register(ReimburService)
