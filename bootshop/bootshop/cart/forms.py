from django import forms
from .models import CartItem


class ProductAddToCartForm(forms.Form):
    quantity = forms.CharField(widget=forms.TextInput(attrs={'size': '2',
                                                             'value': '1', 'class': 'quantity', 'maxlength': '5'}),
                               error_messages={'invalid': 'Please enter a valid quantity.'})
    product_slug = forms.CharField(widget=forms.HiddenInput())

    # override the default _init_ so we can set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    # custom validation to check cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must to be enabled")
        return self.cleaned_data
