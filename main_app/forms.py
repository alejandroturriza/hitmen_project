from django import forms
from .models import Hit

HITMAN_STATUS_CHOICES = (
    (1, 'Active'),
    (0, 'Inactive')
)

class_general = {'class': 'form-control format-input'}


class HitForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = ['assignee', 'description', 'title', 'status', 'assigned_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'assignee': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'required'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_by': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
        }


class HitmenForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs=class_general))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs=class_general), required=False)
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs=class_general), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}))
    status = forms.IntegerField(widget=forms.Select(choices=HITMAN_STATUS_CHOICES, attrs=class_general))
    manager = forms.IntegerField(widget=forms.Select(attrs=class_general), required=False)