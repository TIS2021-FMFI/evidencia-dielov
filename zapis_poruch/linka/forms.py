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
    vznik_cas = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}),
                                initial=(datetime.datetime.utcnow() + datetime.timedelta(hours=1)).strftime("%H:%M:%S"))

    vyriesenie = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Dátum vyriešenia",
                                 required=False)
    vyriesenie_cas = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)

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

    def clean(self):
        super(ZaznamForm, self).clean()

        startDate = self.cleaned_data.get('vznik')
        startTime = self.cleaned_data.get('vznik_cas')
        endDate = self.cleaned_data.get('vyriesenie')
        endTime = self.cleaned_data.get('vyriesenie_cas')

        if (endDate is not None) and startDate > endDate:
            self.add_error('vyriesenie', "Dátum vzniku je väčší ako dátum vyriešenia")
            self.add_error('vznik', "Dátum vzniku je väčší ako dátum vyriešenia")
            raise forms.ValidationError('Dátum vzniku je väčší ako dátum vyriešenia')
        if ((endDate is not None) and startDate == endDate) and (endTime is not None) and startTime > endTime:
            self.add_error('vyriesenie_cas', "Čas vzniku je väčší ako čas vyriešenia")
            self.add_error('vznik_cas', "Čas vzniku je väčší ako čas vyriešenia")
            raise forms.ValidationError('Čas vzniku je väčší ako čas vyriešenia')

        print(self.cleaned_data)

        return self.cleaned_data


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



