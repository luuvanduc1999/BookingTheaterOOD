from django import forms
from .models import dashboard, Ticket


class UpdateDashboardForm(forms.ModelForm):
    class Meta:
        model = dashboard
        fields = ['name','email','age']


class CreateTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['slot', 'type']
        exclude = ['user' , 'room', 'time', 'date', 'movie']
        widgets = {
            'type': forms.RadioSelect(),
        }

class ConfirmTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['confirm_code']

