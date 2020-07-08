from .models import Page
from django import forms

class FormPage(forms.ModelForm):
    
    class Meta:
        model = Page
        fields=['title', 'content', 'order']
        widgets= {
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : "Título"}),
            'content' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : "Contenido del Texto"}),
            'order' : forms.NumberInput(attrs={'class' : 'form-control'}),

        }
        labels= {
            'title' : "",
            'content' : "",
            'order' : "",            
        }
