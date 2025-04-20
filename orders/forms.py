from django import forms
from .models import Coupon
import datetime
import pytz

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1 or quantity > 9:
            raise forms.ValidationError('invalid quantity for product!!')
        return quantity


class CouponForm(forms.Form):
    code = forms.IntegerField(label='Discount Code: ')
    
    def clean_code(self):
        code = self.cleaned_data['code']
        now = datetime.datetime.now(tz=pytz.timezone('Asia/Tehran'))
        try:
            coupon = Coupon.objects.get(
                code__exact=code, 
                valid_from__lte=now, 
                valid_to__gte=now, 
                is_active=True
                )
            self.cleaned_data['coupon_data'] = {
                'pk':coupon.id,
                'discount':coupon.discount,
            }
        except:
            raise forms.ValidationError('given code does not exists!!')
        return code
        