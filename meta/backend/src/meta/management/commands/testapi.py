from django.core.management import BaseCommand
from django.conf import settings

from restapi.client import API

import code
import math
import datetime
import time


class Command(BaseCommand):

    def handle(self, **options):
        local_objects = {
            'api': API(settings.API_SERVER if hasattr(settings, 'API_SERVER') else '127.0.0.1:8000'),
            'math': math,
            'datetime': datetime,
            'time': time
        }

        code.interact(local=local_objects)