from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User

from my_app.models import Profile, InterpreterApplication

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class InterpreterApplicationForm(forms.ModelForm):
    class Meta:
        model = InterpreterApplication
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "county",
            "address",
            "experience_years",
            "languages",
            "cover_letter",
            "resume",
            "profile_image",
            "facebook",
            "twitter",
            "linkedin",
            "instagram",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "county": forms.TextInput(attrs={"class": "form-control", "placeholder": "County"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address"}),
            "experience_years": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Years of Experience"}),
            "languages": forms.Textarea(attrs={"class": "form-control", "placeholder": "Languages you interpret e.g Swahili, English..."}),
            "cover_letter": forms.Textarea(attrs={"class": "form-control", "placeholder": "Cover Letter"}),
            "resume": forms.FileInput(attrs={"class": "form-control"}),
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "facebook": forms.URLInput(attrs={"class": "form-control", "placeholder": "Facebook Profile URL"}),
            "twitter": forms.URLInput(attrs={"class": "form-control", "placeholder": "Twitter Profile URL"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control", "placeholder": "LinkedIn Profile URL"}),
            "instagram": forms.URLInput(attrs={"class": "form-control", "placeholder": "Instagram Profile URL"}),

        }
class ApplicantRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message', 'rows': 5})

    )

class AppointmentForm(forms.Form):
    SERVICE_CHOICES = [
        ("onsite", "Onsite Interpretation"),
        ("virtual", "Virtual Interpretation"),
    ]

    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    service_type = forms.ChoiceField(choices=SERVICE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter details including location or link', 'rows': 5}),
        required=False
    )

class MpesaDonationForm(forms.Form):
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2547XXXXXXXX'}),
    )
    amount = forms.DecimalField(
        label="Amount (KES)",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
    )