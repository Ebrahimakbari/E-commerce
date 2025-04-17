from django import forms


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1 or quantity > 9:
            raise forms.ValidationError('invalid quantity for product!!')
        return quantity