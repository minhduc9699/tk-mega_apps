from django import forms


class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={"class": "",
                                                           "placeholder": "Username"}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "",
                                                               "placeholder": "Password"}))
  remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
