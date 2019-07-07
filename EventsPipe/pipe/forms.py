from django import forms
from pipe.models import Event, Ticket

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'





class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
