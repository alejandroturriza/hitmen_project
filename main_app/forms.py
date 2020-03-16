from django import forms
from .models import Hit


class HitForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = ['assignee', 'description', 'title', 'status', 'assigned_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'assignee': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_by': forms.Select(attrs={'class': 'form-control'}),
        }
