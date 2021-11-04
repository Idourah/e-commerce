import re
from django import forms
from .models import Order


def strip_non_numbers(data):
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)


class CheckoutForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['payment'].widget.attrs['class'] = 'form-select form-control'

    class Meta:
        model = Order
        exclude = ('status', 'ip_address',)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 10:
            raise forms.ValidationError('Enter a valid phone number with area code. (e.g 555-555-5555)')
        return self.cleaned_data['phone']
