from django.db import models


# Create your models here.
class DruhChyby(models.Model):
    """typ chyby

    mechanicka/elektricka"""
    nazov = models.CharField(max_length=256)

    def __str__(self):
        return self.nazov


class MiestoNaLinke(models.Model):
    """typ chyby

    nazov zariadenia, pripadne jej etapa (umyvacka draha 1 atd)"""
    miesto = models.CharField(max_length=256)

    def __str__(self):
        return self.miesto


class SposobenaKym(models.Model):
    """typ chyby

    stroj/clovek"""
    kym = models.CharField(max_length=256)

    def __str__(self):
        return self.kym


class TypChyby(models.Model):
    """
    riadky v tabulke
    """
    popis = models.CharField(verbose_name="Popis typu chyby", max_length=256)
    miesto_na_linke = models.ForeignKey(MiestoNaLinke, verbose_name="Pozícia", on_delete=models.CASCADE, default=None)
    druh_chyby = models.ForeignKey(DruhChyby, verbose_name="Druh chyby", on_delete=models.CASCADE, default=None)
    sposobena_kym = models.ForeignKey(SposobenaKym, verbose_name="Chybu spôsobuje", on_delete=models.CASCADE,
                                      default=None)

    def __str__(self):
        return self.popis


class Revizia(models.Model):
    nazov_revizie = models.CharField('Názov revízie', max_length=256, default=None)
    typ_revizie = models.CharField('Typ revízie', max_length=256, default=None)
    datum_poslednej_revizie = models.DateField('Dátum poslednej revízie')
    exspiracia = models.CharField(max_length=256, default=None)
    datum_nadchadzajucej_revizie = models.DateField('Dátum nadchádzajúcej revízie')

    def __str__(self):
        return self.nazov_revizie


class Pravo(models.Model):
    nazov = models.CharField(max_length=256)


class Pouzivatel(models.Model):
    meno = models.CharField(verbose_name="Meno", max_length=256)
    priezvisko = models.CharField(verbose_name="Priezvisko", max_length=256)
    email = models.CharField(verbose_name="E-mail", max_length=256)
    heslo = models.CharField(verbose_name="Heslo", max_length=256)

    prava = models.ManyToManyField(Pravo, through='MaPouzivatelPravo')

    def __str__(self):
        return str(self.meno) + " " + str(self.priezvisko)


class MaPouzivatelPravo(models.Model):
    pouzivatel = models.ForeignKey(Pouzivatel, on_delete=models.CASCADE, default=None)
    pravo = models.ForeignKey(Pravo, on_delete=models.CASCADE)


class Chyba(models.Model):
    vznik = models.DateTimeField(verbose_name="Čas", default=None)
    pouzivatel = models.ForeignKey(Pouzivatel, verbose_name="Uživateľ", on_delete=models.CASCADE, default=None)
    schvalena = models.BooleanField(verbose_name="Schválená")
    vyriesena = models.BooleanField(verbose_name="Vyriešená")
    vyriesenie = models.DateTimeField(verbose_name="Dátum vyriešenia", default=None)
    miesto_na_linke = models.ForeignKey(MiestoNaLinke, verbose_name="Pozícia", on_delete=models.CASCADE, default=None)
    druh_chyby = models.ForeignKey(DruhChyby, verbose_name="Druh chyby", on_delete=models.CASCADE, default=None)
    sposobena_kym = models.ForeignKey(SposobenaKym, verbose_name="Chybu spôsobil", on_delete=models.CASCADE,
                                      default=None)
    typ_chyby = models.ForeignKey(TypChyby, verbose_name="Dôvod", on_delete=models.CASCADE, default=None)
    opatrenia = models.CharField(verbose_name="Opatrenia/ Oprava", max_length=256, default=None)
    nahradny_diel = models.CharField(verbose_name="Náhradný diel", max_length=128, default=None)
    popis = models.CharField(verbose_name="Popis", max_length=128, default=None)
