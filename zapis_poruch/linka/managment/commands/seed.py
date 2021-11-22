from django.core.management.base import BaseCommand
from datetime import datetime
import random
from linka.models import *

MODE_REFRESH = 'refresh'

MODE_CLEAR = 'clear'

HESLO = 'secret'

def random_date():
    den = random.choice(list(range(1,29)))
    mesiac = random.choice(list(range(1,13)))
    rok = random.choice(list(range(2020,2024)))
    return str(rok)+'-'+str(mesiac)+'-'+str(den)

def random_time():
    hodina = random.choice(list(range(0,24)))
    minuta = random.choice(list(range(0,60)))
    sekunda = random.choice(list(range(0,60)))
    return str(hodina)+':'+str(minuta)+':'+str(sekunda)


class Command(BaseCommand):
    help = 'seed database for testing and development'

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help='Mode')

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')



def create_druhy_chyb(id):
    druh = Druh_chyby(nazov=str(id) + '. chyba')
    druh.save()
    return druh

def create_miesto_na_linke(id):
    miesto = Miesto_na_linke(miesto=str(id) + '. miesto')
    miesto.save()
    return miesto

def create_typ_chyby(id):
    typ_chyby = Typ_chyby(popis=str(id) + '. popis typu chyby')
    typ_chyby.save()
    return typ_chyby

def create_pravo(id):
    pravo = Pravo(nazov=str(id) + '. pravo')
    pravo.save()
    return pravo

def create_sposobena_kym(id):
    sposobena_kym = Sposobena_kym(kym=str(id)+'. kym')
    sposobena_kym.save()
    return sposobena_kym

def create_pouzivatel(id):
    mena = ['Liam', 'Olivia','Noah','Emma','Oliver','Ava']
    priezviska = ['Smith', 'Johnson','Williams','Brown', 'Jones','Garcia','Miller','Davis']

    meno = random.choice(mena)
    priezvisko = random.choice(priezviska)
    email = meno.lower()+'.'+priezvisko.lower()+'@poruchy.sk'
    pouzivatel = Pouzivatel(meno=meno,priezvisko=priezvisko,email=email,heslo=HESLO)
    pouzivatel.save()
    return pouzivatel

def create_ma_prava(pouzivatel, pravo):
    ma_pravo = Ma_pouzivatel_pravo(id_pouzivatela=pouzivatel, id_prava=pravo)
    ma_pravo.save()
    return ma_pravo

def create_zariadenie(id):
    zariadenie = Zariadenie(nazov_revizie=str(id)+'. revizia',datum_poslednej_revizie=random_date(),datum_nadchadzajucej_revizie=random_date(),exspiracia='interval 1 day')
    zariadenie.save()
    return zariadenie

def clear_data():
    Druh_chyby.objects.all().delete()
    Miesto_na_linke.objects.all().delete()
    Typ_chyby.objects.all().delete()
    Pravo.objects.all().delete()
    Pouzivatel.objects.all().delete()
    Ma_pouzivatel_pravo.objects.all().delete()
    Zariadenie.objects.all().delete()


def create_zaznam(miesto_na_linke,druh_chyby,pouzivatel,sposobena_kym,typ_chyby):
    zaznam = Zaznam(
        id_miesto_na_linke=miesto_na_linke,
        id_druh_chyby=druh_chyby,
        cas_vzniku=random_time(),
        datum_vzniku=random_date(),
        id_pouzivatela=pouzivatel,
        schvalena=random.choice([True, False]),
        vyriesena=random.choice([True, False]),
        cas_vyriesenia=random_time(),
        datum_vyriesenia=random_date(),
        id_sposobena_kym=sposobena_kym,
        id_typ_chyby=typ_chyby
    )
    zaznam.save()
    return zaznam

def run_seed(self, mode):
    clear_data()
    if mode == MODE_CLEAR:
        return

    druhy = []
    miesta_na_linke = []
    typy_chyb = []
    sposobene_kym = []
    zariadenia = []
    prava = []
    pouzivatelia = []
    ma_prava = []
    zaznamy = []
    for i in range(1, 11):
        druhy.append(create_druhy_chyb(i))
        miesta_na_linke.append(create_miesto_na_linke(i))
        prava.append(create_pravo(i))
        typy_chyb.append(create_typ_chyby(i))
        zariadenia.append(create_zariadenie(i))
        sposobene_kym.append(create_sposobena_kym(i))

    for i in range(1,10):
        pouzivatelia.append(create_pouzivatel(i))

    for pouz in pouzivatelia:
        ma_prava.append(create_ma_prava(pouz, random.choice(prava)))

    for i in range(1,50):
        zaznamy.append(create_zaznam(
            random.choice(miesta_na_linke),
            random.choice(druhy),
            random.choice(pouzivatelia),
            random.choice(sposobene_kym),
            random.choice(typy_chyb)
        ))