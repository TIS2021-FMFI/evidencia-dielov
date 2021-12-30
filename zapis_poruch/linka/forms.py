from django import forms
import datetime

from .models import TypChyby, Chyba, TypRevizie


class TypForm(forms.ModelForm):
    class Meta:
        model = TypChyby
        fields = ['popis', 'miesto_na_linke', 'druh_chyby', 'sposobena_kym']


class ZaznamForm(forms.ModelForm):
    class Meta:
        model = Chyba
        fields = ['pouzivatel', 'vznik', 'schvalena', 'vyriesena', 'miesto_na_linke', 'popis',
                  'vyriesenie', 'sposobena_kym', 'typ_chyby', 'opatrenia',
                  'druh_chyby', 'nahradny_diel']


class RevizieForm(forms.ModelForm):
    class Meta:
        model = TypRevizie
        fields = ['nazov_revizie','exspiracia','typ_revizie','datum_poslednej_revizie',
                  'datum_nadchadzajucej_revizie']
        widgets = {
            'datum_poslednej_revizie': forms.DateInput(attrs={'type': 'date'}),
            'datum_nadchadzajucej_revizie': forms.DateInput(attrs={'type': 'date'})
        }



