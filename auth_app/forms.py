from allauth.account.forms import SignupForm
from django import forms
from .models import Profile
from .utils import validateEmailAddress


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    profile_photo = forms.ImageField(required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        new_user = Profile(
            user=user,
            first_name = self.cleaned_data["first_name"],
            last_name = self.cleaned_data["last_name"],
            profile_photo = self.cleaned_data["profile_photo"],
        )
        new_user.save()
        return user

    def emailVal(self, ip, ua):
        return validateEmailAddress(self.cleaned_data["email"], ip, ua)

class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    profile_photo = forms.ImageField(required=False)
    email = forms.EmailField()

    def emailVal(self, ip, ua):
        return validateEmailAddress(self.cleaned_data["email"], ip, ua)