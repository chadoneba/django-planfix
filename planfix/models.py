from django.db import models

class PlanfixContacts(models.Model):
    id_contact = models.IntegerField()
    email = models.CharField \
        (max_length=254
         , null=True
         , blank=True
         )