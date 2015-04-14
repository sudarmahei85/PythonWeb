from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,error_messages={'required': 'Email is Required'})
    first_name = forms.CharField(required=True,error_messages={'required': 'First name is Required'})
    last_name = forms.CharField(required=True,error_messages={'required': 'Last name is Required'})
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters."),'required': 'User Name is Required'})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput,error_messages={'required': 'Password is Required'})
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,error_messages={'required': 'Retype Password is Required'},
        help_text=_("Enter the same password as above, for verification."))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        #raise forms.ValidationError(self.error_messages['duplicate_email'])
        raise forms.ValidationError('Email is already registered.')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            