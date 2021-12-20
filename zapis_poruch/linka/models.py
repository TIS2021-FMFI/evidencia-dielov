import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DruhChyby(models.Model):
    nazov = models.CharField(max_length=256)

    def __str__(self):
        return self.nazov


class MiestoNaLinke(models.Model):
    miesto = models.CharField(max_length=256)

    def __str__(self):
        return self.miesto



class SposobenaKym(models.Model):
    kym = models.CharField(max_length=256)

    def __str__(self):
        return self.kym



class TypChyby(models.Model):
    popis = models.CharField(verbose_name="Popis typu chyby", max_length=256)
    miesto_na_linke = models.ForeignKey(MiestoNaLinke, verbose_name="Pozícia", on_delete=models.CASCADE,  default=None)
    druh_chyby = models.ForeignKey(DruhChyby, verbose_name="Druh chyby", on_delete=models.CASCADE, default=None)
    sposobena_kym = models.ForeignKey(SposobenaKym, verbose_name="Chybu spôsobuje", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.popis


class TypChybyWrapper:
    def __init__(self, object):
        self.id = object.id
        self._object = object
        self.popis = object.popis
        self.miesto_na_linke = object.miesto_na_linke
        self.druh_chyby = object.druh_chyby
        self.sposobena_kym = object.sposobena_kym
        self.frekvencie = dict()
        self.vyskyt = dict()
        self.trvanie = 0

    def json(self):
        return {
            "id": str(self.id),
            "popis": str(self.popis),
            "miesto_na_linke": str(self.miesto_na_linke),
            "druh_chyby": str(self.druh_chyby),
            "sposobena_kym": str(self.sposobena_kym),
            "frekvencie": self.frekvencie,
            "vyskyt": self.vyskyt,
            "trvanie": str(self.trvanie)
        }

    def _increase_dict(self, dictionary, rozdiel):
        if rozdiel.days <= 7:
            dictionary["week"] += 1
        if rozdiel.days <= 28:
            dictionary["month"] += 1
        if rozdiel.days <= 182:
            dictionary["6months"] += 1
        if rozdiel.days <= 365:
            dictionary["year"] += 1

    def fill(self, objects):
        count = 0
        pocet_vsetkych = {"week": 0, "month": 0, "6months": 0, "year": 0}
        pocet_nasich = {"week": 0, "month": 0, "6months": 0, "year": 0}

        today = datetime.datetime.now()
        today = today.replace(tzinfo=None)
        for object in objects:
            vznik = object.vznik.replace(tzinfo=None)
            rozdiel = today - vznik
            self._increase_dict(pocet_vsetkych, rozdiel)

            if object.typ_chyby != self._object:
                continue
            count += 1

            self.trvanie += object.trvanie.days
            self._increase_dict(pocet_nasich, rozdiel)

        self.trvanie = round(self.trvanie / count)
        self.vyskyt = pocet_nasich
        for key in pocet_nasich:
            self.frekvencie[key] = 0 if pocet_vsetkych[key] == 0 else pocet_nasich[key] / pocet_vsetkych[key]

    @staticmethod
    def all():
        objects = TypChyby.objects.all()
        return [TypChybyWrapper(x) for x in objects]



class TypRevizie(models.Model):
    nazov_revizie = models.CharField('Názov revízie', max_length=256,  default=None)
    typ_revizie = models.CharField('Typ revízie', max_length=256,  default=None)
    datum_poslednej_revizie = models.DateField('Dátum poslednej revízie')
    exspiracia = models.IntegerField()
    datum_nadchadzajucej_revizie = models.DateField('Dátum nadchádzajúcej revízie')

    def __str__(self):
        return self.nazov_revizie


class Pouzivatel(User):
    pass


class Chyba(models.Model):
    vznik = models.DateTimeField(verbose_name="Čas", default=None)
    pouzivatel = models.ForeignKey(Pouzivatel, verbose_name="Uživateľ", on_delete=models.CASCADE,  default=None)
    schvalena = models.BooleanField(verbose_name="Schválená")
    vyriesena = models.BooleanField(verbose_name="Vyriešená")
    vyriesenie = models.DateTimeField(verbose_name="Dátum vyriešenia", default=None)
    miesto_na_linke = models.ForeignKey(MiestoNaLinke, verbose_name="Pozícia",  on_delete=models.CASCADE,  default=None)
    druh_chyby = models.ForeignKey(DruhChyby, verbose_name="Druh chyby",  on_delete=models.CASCADE,   default=None)
    sposobena_kym = models.ForeignKey(SposobenaKym, verbose_name="Chybu spôsobil",  on_delete=models.CASCADE, default=None)
    typ_chyby = models.ForeignKey(TypChyby, verbose_name="Dôvod",  on_delete=models.CASCADE,  default=None)
    opatrenia = models.CharField(verbose_name="Opatrenia/ Oprava", max_length=256,  default=None)
    nahradny_diel = models.CharField(verbose_name="Náhradný diel", max_length=128,  default=None)
    popis = models.CharField(verbose_name="Popis", max_length=128,  default=None)


class ChybaWrapper:
    def __init__(self, object):
        self.id = object.id
        self.vznik = object.vznik
        self.pouzivatel = object.pouzivatel
        self.schvalena = object.schvalena
        self.vyriesena = object.vyriesena
        self.vyriesenie = object.vyriesenie
        self.miesto_na_linke = object.miesto_na_linke
        self.druh_chyby = object.druh_chyby
        self.sposobena_kym = object.sposobena_kym
        self.typ_chyby = object.typ_chyby
        self.opatrenia = object.opatrenia
        self.nahradny_diel = object.nahradny_diel
        self.popis = object.popis
        self.trvanie = self.vyriesenie - self.vznik

    @staticmethod
    def all():
        objects = Chyba.objects.all()
        return [ChybaWrapper(x) for x in objects]
