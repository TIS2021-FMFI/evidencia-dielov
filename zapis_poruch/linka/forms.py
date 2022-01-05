import datetime

from django import forms
import datetime

from .models import TypChyby, Chyba, TypRevizie


class TypForm(forms.ModelForm):
    class Meta:
        model = TypChyby
        fields = ['popis', 'miesto_na_linke', 'druh_chyby', 'sposobena_kym']


class ZaznamForm(forms.ModelForm):
    vznik = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Dátum vzniku",
                            initial=datetime.date.today)
    vznik_cas = forms.DateField(widget=forms.TimeInput(attrs={'type': 'time'}),
                                initial=(datetime.datetime.utcnow() + datetime.timedelta(hours=1)).strftime("%H:%M:%S"))

    vyriesenie = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Dátum vyriešenia",
                                 required=False)
    vyriesenie_cas = forms.DateField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)

    vyriesena = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onChange': 'onReviziaCheckboxToggle()'}), required=False)

    def __init__(self, *args, **kwargs):
        super(ZaznamForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            chyba = kwargs["instance"]
            print(chyba.vznik)
            if chyba.vznik:
                self.initial['vznik_cas'] = chyba.vznik.time()
            if chyba.vyriesenie:
                self.initial['vyriesenie_cas'] = chyba.vyriesenie.time()

    class Meta:
        model = Chyba
        fields = ['vznik', 'vznik_cas',  'vyriesena', 'miesto_na_linke', 'popis',
                  'vyriesenie', 'vyriesenie_cas', 'sposobena_kym', 'opatrenia',
                  'druh_chyby', 'nahradny_diel', 'dovod']


class RevizieForm(forms.ModelForm):
    class Meta:
        model = TypRevizie
        fields = ['nazov_revizie','exspiracia','typ_revizie','datum_poslednej_revizie',
                  'datum_nadchadzajucej_revizie']
        widgets = {
            'datum_poslednej_revizie': forms.DateInput(attrs={'type': 'date', 'id': 'datum_poslednej', 'onchange': 'nastavDatumNasledujucej()'}),
            'datum_nadchadzajucej_revizie': forms.DateInput(attrs={'type': 'date', 'id': 'datum_nasledujucej'}),
            'exspiracia': forms.NumberInput(attrs={'id': 'exspiracia', 'onchange': 'nastavDatumNasledujucej()'})
        }



