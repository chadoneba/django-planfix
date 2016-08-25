from __future__ import unicode_literals

from django.contrib import admin
from .models import PlanfixContacts


@admin.register(PlanfixContacts)
class PlanfixContactsAdmin(admin.ModelAdmin):
    list_display = ['id_contact','email']

