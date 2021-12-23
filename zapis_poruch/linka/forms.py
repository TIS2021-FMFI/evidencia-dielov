import datetime

from django import forms

from .models import TypChyby, Chyba, TypRevizie


class TypForm(forms.ModelForm):
    class Meta:
        model = TypChyby
        fields = ['popis', 'miesto_na_linke', 'druh_chyby', 'sposobena_kym']


class ZaznamForm(forms.ModelForm):
    vznik = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Dátum vzniku")
    vyriesenie = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Dátum vyriešenia", required=False)
    vznik_cas = forms.DateField(widget=forms.TimeInput(attrs={'type': 'time'}))
    vyriesenie_cas = forms.DateField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    class Meta:
        model = Chyba
        fields = ['vznik', 'vznik_cas',  'vyriesena', 'miesto_na_linke', 'popis',
                  'vyriesenie', 'vyriesenie_cas', 'sposobena_kym', 'opatrenia',
                  'druh_chyby', 'nahradny_diel', 'dovod']


class RevizieForm(forms.ModelForm):
    class Meta:
        model = TypRevizie
        fields = ['nazov_revizie', 'datum_poslednej_revizie', 'exspiracia',
                  'datum_nadchadzajucej_revizie']
