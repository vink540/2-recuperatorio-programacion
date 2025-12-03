from django import forms

class SearchForm(forms.Form):
    palabra_clave = forms.CharField(label="Palabra clave", max_length=200)
