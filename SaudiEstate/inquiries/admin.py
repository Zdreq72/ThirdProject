from django.contrib import admin
from .models import Inquiry, InquiryReply, VisitRequest

admin.site.register(Inquiry)
admin.site.register(VisitRequest)
admin.site.register(InquiryReply)
