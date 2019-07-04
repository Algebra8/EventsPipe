from django.contrib import admin
from pipe.models import Event, Ticket

# Register model with admin
admin.site.register(Event)
admin.site.register(Ticket)
