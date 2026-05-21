from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Publication, TYPE_CHOICES, INDEXED_CHOICES, QUARTILE_CHOICES, YEAR_CHOICES


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
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        }),
        help_text='Enter your full name as it appears in publications.'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ExcelUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx',
        }),
        help_text='Upload an Excel (.xlsx) file. Row 1 = Title, Row 2 = Column Headers, Row 3+ = Data.'
    )

    def clean_file(self):
        f = self.cleaned_data['file']
        if not f.name.endswith('.xlsx'):
            raise forms.ValidationError('Only .xlsx files are allowed.')
        
        # Validate MIME type
        valid_mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        if f.content_type != valid_mime:
            raise forms.ValidationError('Invalid file type. Ensure it is a genuine Excel file.')
            
        # Validate file size (5MB limit)
        if f.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File too large. Maximum size is 5MB.')
            
        return f


class PublicationForm(forms.ModelForm):
    publication_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2024, May 2024, or 12/05/2024'}),
        help_text='Enter Year, Month Year, or Full Date'
    )
    type = forms.ChoiceField(
        choices=[('', 'Select Type')] + list(TYPE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    indexed = forms.ChoiceField(
        choices=[('', 'Select Indexing')] + list(INDEXED_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quartile = forms.ChoiceField(
        choices=[('', 'None')] + list(QUARTILE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Publication
        fields = [
            'title', 'type', 'journal_conference',
            'page_no', 'vol_issue', 'publication_date',
            'doi', 'indexed', 'quartile', 'pdf_file',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of the paper'}),
            'journal_conference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of journal or conference'}),
            'page_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10-25'}),
            'vol_issue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Vol.5/Issue 2'}),
            'doi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10.1000/xyz123'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }

    def clean_pdf_file(self):
        pdf = self.cleaned_data.get('pdf_file')
        if pdf:
            if not pdf.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only .pdf files are allowed.')
            if pdf.content_type != 'application/pdf':
                raise forms.ValidationError('The uploaded file does not appear to be a valid PDF.')
        return pdf