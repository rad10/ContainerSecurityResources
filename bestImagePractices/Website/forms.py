from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
from .models import Upload, FileUpload


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=150, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', "password1", "password2")
    # Clear the help text

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field in ['password1', 'password2']:
            self.fields[field].help_text = None

    # Whitelist fit.edu and my.fit.edu e-mail domains only
    def clean_email(self):
        submitted_email = self.cleaned_data['email']
        domain = submitted_email.split('@')[1]
        if domain not in ['fit.edu', 'my.fit.edu']:
            raise forms.ValidationError('Not a valid Florida Tech email')
        return submitted_email


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = [
            'title',
            'quantity'
        ]

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        if "CFE" in title:
            return clean_title
        else:
            raise forms.ValidationError("this is not a valid title")


class RawUploadForm(forms.Form):
    title = forms.CharField(required=True)
    number = forms.CharField(label='')
    date = forms.CharField()
    quantity = forms.IntegerField(initial=1)


class FileForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('title', 'file', )

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        if len(title) < 64:
            return title
        else:
            raise forms.ValidationError(
                "Title is over the 64 character limit!")
