from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm , UserModel
from .models import Employee, VacationModel


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = UserCreationForm.Meta.fields + ('matricule', 'cnss', 'service', 'post', 'chef1', 'chef2', 'type', 'nombreConge')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Employee
        fields = UserChangeForm.Meta.fields


class VacationCreateForm(forms.ModelForm):

    class Meta:
        model = VacationModel
        fields = [
            'nature',
            'dateDebut',
            'dateFin',
        ]

    def __init__(self, *args, **kwargs):
        super(VacationCreateForm, self).__init__(*args, **kwargs)
        self.fields['dateDebut'].widget = forms.TextInput(attrs={
            'class': 'datepicker',})
        self.fields['dateFin'].widget = forms.TextInput(attrs={
            'class': 'datepicker', })



class ReactVacationForm(forms.ModelForm):

    nature = forms.CharField(disabled=True)
    dateDebut = forms.DateField(disabled=True)
    dateFin = forms.DateField(disabled=True)

    class Meta:
        model = VacationModel
        fields = [
            'nature',
            'dateDebut',
            'dateFin',
            'valide',
            'id',
        ]

