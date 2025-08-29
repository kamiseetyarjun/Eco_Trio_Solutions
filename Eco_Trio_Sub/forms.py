# from django import forms
# from .models import Registration

# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Registration
#         exclude = ['signup_time']  
#         fields = '__all__'

from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        exclude = ['signup_time']  # ✅ signup_time won't be in the form
