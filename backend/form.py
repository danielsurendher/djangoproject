from django . forms import ModelForm
from backend.models import student
from django import forms
class UserForm(ModelForm):
    class Meta:
        model = student
        fields = '__all__'

"""widgets = {
    'studentname': forms.TextInput(attrs={'class': 'form-control'}),
    'education': forms.TextInput(attrs={'class': 'form-control'}),
    'phone': forms.TextInput(attrs={'class': 'form-control'}),
    'city': forms.TextInput(attrs={'class': 'form-control'}),
}"""