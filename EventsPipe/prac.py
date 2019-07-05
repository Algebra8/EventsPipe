import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventsPipe.settings')
django.setup()

from django.utils import timezone
from django.utils.dateparse import parse_date
date_str = "2018-03-11"
temp_date = parse_date(date_str)
print(type(dateparse.parse_datetime("2018-03-11")))
