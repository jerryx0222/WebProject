from django import forms
from .models import runningtables

class MyModelForm(forms.ModelForm):
    class Meta:
        model = runningtables
        fields = ['SumCount']
