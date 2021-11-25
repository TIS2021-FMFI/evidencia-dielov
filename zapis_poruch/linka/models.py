from django.db import models

# Create your models here.
class Druh_chyby(models.Model):
    nazov = models.CharField(max_length=256)


class Miesto_na_linke(models.Model):
    miesto = models.CharField(max_length=256)


class Typ_chyby(models.Model):
    popis = models.CharField(max_length=256)


class Sposobena_kym(models.Model):
    kym = models.CharField(max_length=256)


class TypRevizie(models.Model):
    nazov_revizie = models.CharField(max_length=256)
    datum_poslednej_revizie = models.DateField()
    exspiracia = models.CharField(max_length=256)
    datum_nadchadzajucej_revizie = models.DateField()


class Pravo(models.Model):
    nazov = models.CharField(max_length=256)


class Pouzivatel(models.Model):
    meno = models.CharField(max_length=256)
    priezvisko = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    heslo = models.CharField(max_length=256)


class Ma_pouzivatel_pravo(models.Model):
    id_pouzivatela = models.ForeignKey(Pouzivatel, on_delete=models.CASCADE)
    id_prava = models.ForeignKey(Pravo, on_delete=models.CASCADE)


class Chyba(models.Model):
    id_miesto_na_linke = models.ForeignKey(Miesto_na_linke, on_delete=models.CASCADE)
    id_druh_chyby = models.ForeignKey(Druh_chyby, on_delete=models.CASCADE)
    cas_vzniku = models.TimeField()
    datum_vzniku = models.DateField()
    id_pouzivatela = models.ForeignKey(Pouzivatel, on_delete=models.CASCADE)
    schvalena = models.BooleanField()
    vyriesena = models.BooleanField()
    cas_vyriesenia = models.TimeField()
    datum_vyriesenia = models.DateField()
    id_sposobena_kym = models.ForeignKey(Sposobena_kym, on_delete=models.CASCADE)
    id_typ_chyby = models.ForeignKey(Typ_chyby, on_delete=models.CASCADE)