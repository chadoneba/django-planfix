from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
from planfix.api import PlanFix

class Command(BaseCommand):
    help = "Load contacts from planfix"

    def handle(self, *args, **options):
        params = \
            { 'host': settings.PLANFIX_HOST
            , 'api_key': settings.PLANFIX_API_KEY
            , 'private_key': settings.PLANFIX_PRIVATE_KEY
            , 'project_id': ''
            , 'user': settings.PLANFIX_USER
            , 'password': settings.PLANFIX_PASS
            , 'account': settings.PLANFIX_ACCOUNT
             }
        planfix = PlanFix(**params)
        Contacts = apps.get_app_config("planfix").get_model("PlanfixContacts")
        if Contacts.objects.all().count() > 0:
            self.stdout.write(self.style.SUCCESS('Contacts downloaded'))
            return
        counter = 1
        while True:
            res = planfix.contact_get_list(cur_page=counter)
            self.stdout.write(self.style.SUCCESS('%s - %s ' % (counter,res.__len__())))
            if res.__len__() > 0 and res:
                for i in res:
                    contact = Contacts()
                    contact.email = i[1]
                    contact.id_contact = i[0]
                    contact.save()
                counter+=1
            else:
                break
        self.stdout.write(self.style.SUCCESS('Have been added %s items' % counter))





