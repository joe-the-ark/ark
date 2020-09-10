from django.core.management import BaseCommand
from django.conf import settings

from meta.models import Product


class Command(BaseCommand):

    def handle(self, **options):
        company = 'META'
        category = 'Member'
        
        name = 'TEST'
        price = 0.5

        product = Product.objects.create(name=name, price=price, company=company, category=category)

