from django import forms
from . models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import Notes

class NotesGroupForm(forms.ModelForm):
    class Meta:
        model = NotesGroup
        fields = ['name', 'description', 'color']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional description for this group...'}),
            'color': forms.Select(choices=[
                ('primary', 'Blue'),
                ('success', 'Green'),
                ('danger', 'Red'),
                ('warning', 'Yellow'),
                ('info', 'Light Blue'),
                ('secondary', 'Gray'),
            ]),
        }

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['group', 'title', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your note or leave blank if uploading an image...'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
        }


class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter your search ")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']

class ConversionForm(forms.Form):
    CHOICES = [
        ('length', 'Length'),
        ('mass', 'Mass'),
        ('volume', 'Volume'),
        ('currency', 'Currency')
    ]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class ConversionLengthForm(forms.Form):
    CHOICES = [('yard', 'Yard'), ('foot', 'Foot')]
    input = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
        ))
    measure1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )

class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    input = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
        ))
    measure1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )

class ConversionVolumeForm(forms.Form):
    CHOICES = [('liter', 'Liter'), ('gallon', 'Gallon')]
    input = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

class ConversionCurrencyForm(forms.Form):
    # Use ISO currency codes as values (these match exchange rate API expectations)
    CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('AUD', 'Australian Dollar'),
        ('CAD', 'Canadian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('CNY', 'Chinese Yuan'),
        ('INR', 'Indian Rupee'),
        ('NGN', 'Nigerian Naira'),
        ('ZAR', 'South African Rand'),
        ('BRL', 'Brazilian Real'),
        ('RUB', 'Russian Ruble'),
        ('SEK', 'Swedish Krona'),
        ('NOK', 'Norwegian Krone'),
        ('DKK', 'Danish Krone'),
        ('MXN', 'Mexican Peso'),
        ('SGD', 'Singapore Dollar'),
        ('HKD', 'Hong Kong Dollar'),
        ('NZD', 'New Zealand Dollar'),
        ('KRW', 'South Korean Won'),
        ('TRY', 'Turkish Lira')
    ]

    # Use DecimalField to validate numeric input cleanly
    amount = forms.DecimalField(
        required=False,  # allow displaying the form before user enters an amount
        min_value=0,
        label='',
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount', 'step': 'any'})
    )

    from_currency = forms.ChoiceField(label='', choices=CHOICES)
    to_currency = forms.ChoiceField(label='', choices=CHOICES)




class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Form for updating basic User fields (username, first/last name, email)."""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']
