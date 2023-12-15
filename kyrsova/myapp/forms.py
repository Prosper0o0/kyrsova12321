from django import forms
from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['mark_name', 'model_name', 'generation_name',
                  'equipment_name', 'year', 'price']
   