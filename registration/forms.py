from allauth.account.forms import SignupForm
from django import forms
from .models import User
from phonenumber_field.formfields import PhoneNumberField


class SignUp(SignupForm):
    name = forms.CharField(label="Name", required=True, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': "span11"}))
    phone = PhoneNumberField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Phone', 'class': "span11"}))
    email = forms.EmailField(label="email", required=True, widget=forms.EmailInput(attrs={'placeholder': 'email', 'class': "span11"}))

    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'email']

    def save(self, request):
        user = super(SignUp, self).save(request)
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.save()
        return user

