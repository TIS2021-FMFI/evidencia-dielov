from django import forms

from .models import TypChyby, Chyba, Revizia


class TypForm(forms.ModelForm):
    class Meta:
        model = TypChyby
        fields = ['popis', 'miesto_na_linke', 'druh_chyby', 'sposobena_kym']


class ZaznamForm(forms.ModelForm):
    class Meta:
        model = Chyba
        fields = ['pouzivatel', 'schvalena', 'vyriesena',
                  'miesto_na_linke', 'druh_chyby',
                  'sposobena_kym', 'typ_chyby', 'opatrenia', 'nahradny_diel']


class RevizieForm(forms.ModelForm):
    class Meta:
        model = Revizia
        fields = ['nazov_revizie', 'datum_poslednej_revizie', 'exspiracia',
                  'datum_nadchadzajucej_revizie']

