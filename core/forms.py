from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Faculty, Publication, DESIGNATION_CHOICES, DEPARTMENT_CHOICES, MONTH_CHOICES, TYPE_CHOICES
import datetime

YEAR_CHOICES = [(y, y) for y in range(2000, datetime.date.today().year + 1)][::-1]


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class FacultyRegisterForm(UserCreationForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    designation = forms.ChoiceField(
        choices=DESIGNATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    joining_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control', 'type': 'date'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'email', 'password1', 'password2']:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PublicationForm(forms.ModelForm):
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Publication
        fields = [
            'faculty', 'type', 'title', 'month', 'year', 'pages', 'pdf_file',
            # Journal
            'journal_name', 'issn', 'volume', 'issue',
            # Conference
            'conference_name', 'location', 'conference_isbn',
            # Book
            'book_name', 'publisher', 'book_isbn', 'chapter_number',
        ]
        widgets = {
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={
                'class': 'form-control', 'id': 'id_type',
                'onchange': 'showFields(this.value)'
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'pages': forms.TextInput(attrs={'class': 'form-control'}),
            'journal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'issn': forms.TextInput(attrs={'class': 'form-control'}),
            'volume': forms.TextInput(attrs={'class': 'form-control'}),
            'issue': forms.TextInput(attrs={'class': 'form-control'}),
            'conference_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'conference_isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'book_name': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'book_isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'chapter_number': forms.TextInput(attrs={'class': 'form-control'}),
        }