from django.core.management.base import BaseCommand
from datetime import datetime
import random

from linka.models import Chyba, DruhChyby, MiestoNaLinke, TypChyby, Pravo, Pouzivatel, MaPouzivatelPravo, \
    TypRevizie, SposobenaKym

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

def random_date_time():
    return random_date() + "T" + random_time()


class Command(BaseCommand):
    help = 'seed database for testing and development'

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help='Mode')

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(options['mode'])
        self.stdout.write('done.')



def create_druh_chyby(id):
    druh = DruhChyby(nazov=str(id) + '. chyba')
    druh.save()
    return druh

def create_miesto_na_linke(id):
    miesto = MiestoNaLinke(miesto=str(id) + '. miesto')
    miesto.save()
    return miesto

def create_typ_chyby(id, miesto, druh, sposobena_kym ):
    typ_chyby = TypChyby(popis=str(id) + '. popis typu chyby', miesto_na_linke=miesto, druh_chyby=druh, sposobena_kym=sposobena_kym)
    typ_chyby.save()
    return typ_chyby

def create_pravo(id):
    pravo = Pravo(nazov=str(id) + '. pravo')
    pravo.save()
    return pravo

def create_sposobena_kym(id):
    sposobena_kym = SposobenaKym(kym=str(id)+'. kym')
    sposobena_kym.save()
    return sposobena_kym

def create_pouzivatel():
    mena = ['Liam', 'Olivia','Noah','Emma','Oliver','Ava']
    priezviska = ['Smith', 'Johnson','Williams','Brown', 'Jones','Garcia','Miller','Davis']

    meno = random.choice(mena)
    priezvisko = random.choice(priezviska)
    email = meno.lower()+'.'+priezvisko.lower()+'@poruchy.sk'
    pouzivatel = Pouzivatel(meno=meno,priezvisko=priezvisko,email=email,heslo=HESLO)
    pouzivatel.save()
    return pouzivatel

def create_ma_prava(pouzivatel, pravo):
    ma_pravo = MaPouzivatelPravo(pouzivatel=pouzivatel, pravo=pravo)
    ma_pravo.save()
    return ma_pravo

def create_zariadenie(id):
    zariadenie = TypRevizie(nazov_revizie=str(id)+'. revizia',typ_revizie='mechanicka' ,datum_poslednej_revizie=random_date(), datum_nadchadzajucej_revizie=random_date(), exspiracia='interval 1 day')
    zariadenie.save()
    return zariadenie

def clear_data():
    DruhChyby.objects.all().delete()
    MiestoNaLinke.objects.all().delete()
    TypChyby.objects.all().delete()
    Pravo.objects.all().delete()
    Pouzivatel.objects.all().delete()
    MaPouzivatelPravo.objects.all().delete()
    TypRevizie.objects.all().delete()
    SposobenaKym.objects.all().delete()


def create_zaznam(miesto_na_linke, druh_chyby, pouzivatel, sposobena_kym, typ_chyby):
    zaznam = Chyba(
        miesto_na_linke=miesto_na_linke,
        druh_chyby=druh_chyby,
        vznik=random_date_time(),
        pouzivatel=pouzivatel,
        schvalena=random.choice([True, False]),
        vyriesena=random.choice([True, False]),
        vyriesenie=random_date_time(),
        sposobena_kym=sposobena_kym,
        typ_chyby=typ_chyby,
        opatrenia='nic',
        nahradny_diel='ahaha',
        popis='babksb'
    )
    zaznam.save()
    return zaznam

def run_seed(mode):
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
        druhy.append(create_druh_chyby(i))
        miesta_na_linke.append(create_miesto_na_linke(i))
        prava.append(create_pravo(i))
        zariadenia.append(create_zariadenie(i))
        sposobene_kym.append(create_sposobena_kym(i))
        typy_chyb.append(create_typ_chyby(i, miesta_na_linke[-1], druhy[-1], sposobene_kym[-1] ))

    for i in range(1,10):
        pouzivatelia.append(create_pouzivatel())

    for pouz in pouzivatelia:
        ma_prava.append(create_ma_prava(pouz, random.choice(prava)))

    for i in range(1, 50):
        zaznamy.append(create_zaznam(
            random.choice(miesta_na_linke),
            random.choice(druhy),
            random.choice(pouzivatelia),
            random.choice(sposobene_kym),
            random.choice(typy_chyb)
        ))