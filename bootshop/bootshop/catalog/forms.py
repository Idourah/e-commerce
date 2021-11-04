from django import forms
from .models import Category, Product
from django.template.defaultfilters import slugify # new


class ProductAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        self.fields['categories'].widget.attrs['class'] = 'form-select form-control'

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('slug', 'meta_keywords', 'meta_description',)

    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price must be greater than zero')
        return self.cleaned_data['price']


class CategoryPostForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ('is_active', 'description', 'slug', 'meta_keywords', 'meta_description')

    def save(self, commit=True):
        instance = super().save(commit=False)
        name = self.cleaned_data.get('name')
        Category.objects.create(name=name, slug=slugify(name), meta_keywords=name, meta_description=name, description=name)
        return instance
