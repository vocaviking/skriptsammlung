from __future__ import unicode_literals


from django import forms
from django.utils.translation  import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from nocaptcha_recaptcha.fields     import NoReCaptchaField

from registration.users import UserModel, UsernameField

User = UserModel()

class RegistrationForm(UserCreationForm):
    required_css_class = 'required'
    email = forms.EmailField(label=_("E-mail"),help_text='Your university mail address. (e.g. jon.doe@uni-jena.de)')
    captcha = NoReCaptchaField(help_text   = 'Commencing Turing-Test...')
    class Meta:
        model = User
        fields = ("email",)

class RegistrationFormUniqueEmail(RegistrationForm):
    def clean_email(self):
        #Check if Mailadresse is already used
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        #Check if it is a @uni-jena.de adresse
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain != 'uni-jena.de':
            raise forms.ValidationError(_("Please supply your university mail address. Other providers are prohibited."))
        return self.cleaned_data['email']