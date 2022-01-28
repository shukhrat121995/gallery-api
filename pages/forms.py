from django import forms
from forceartsapi.models import ContactUs


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = [
            'full_name',
            'email',
            'message',
        ]