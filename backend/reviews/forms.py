from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'dealer', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'dealer': forms.Select(attrs={'class': 'form-control'}),
        }
