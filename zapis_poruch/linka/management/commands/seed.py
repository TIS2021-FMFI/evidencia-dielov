from django.core.management.base import BaseCommand
from datetime import datetime
import random

from django.contrib.auth.models import User
from linka.models import Chyba, DruhChyby, MiestoNaLinke, TypChyby, \
    TypRevizie, SposobenaKym, DruhRevizie

MODE_REFRESH = 'refresh'

MODE_CLEAR = 'clear'

HESLO = 'secret'


def random_date():
    den = random.choice(list(range(1, 29)))
    mesiac = random.choice(list(range(1, 13)))
    rok = random.choice(list(range(2020, 2024)))
    return str(rok) + '-' + str(mesiac) + '-' + str(den)


def random_time():
    hodina = random.choice(list(range(0, 24)))
    minuta = random.choice(list(range(0, 60)))
    sekunda = random.choice(list(range(0, 60)))
    return str(hodina) + ':' + str(minuta) + ':' + str(sekunda)


def random_date_time():
    return random_date() + "T" + random_time()


class Command(BaseCommand):
    help = 'seed database for testing and development'

    def handle(self, *args, **options):
        run_seed("")


def create_druh_chyby():
    ret = []
    for druh in ('mechanická', 'elektronická'):
        chyba = DruhChyby(nazov=druh)
        chyba.save()
        ret.append(chyba)
    return ret


def create_miesto_na_linke(id):
    miesto = MiestoNaLinke(miesto=str(id) + '. miesto')
    miesto.save()
    return miesto


def create_typ_chyby(id, miesto, druh, sposobena_kym):
    typ_chyby = TypChyby(popis=str(id) + '. popis typu chyby', miesto_na_linke=miesto, druh_chyby=druh,
                         sposobena_kym=sposobena_kym)
    typ_chyby.save()
    return typ_chyby


def create_sposobena_kym():
    ret = []
    for kym in ('stroj', 'človek'):
        sposobena = SposobenaKym(kym=kym)
        sposobena.save()
        ret.append(sposobena)
    return ret


def create_pouzivatel(i):
    mena = ['Liam', 'Olivia', 'Noah', 'Emma', 'Oliver', 'Ava']
    priezviska = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']

    username = f'user{i}'
    email = f'{username}@poruchy.com'
    pouzivatel = User.objects.create_user(username, email, HESLO)
    pouzivatel.first_name = random.choice(mena)
    pouzivatel.last_name = random.choice(priezviska)
    pouzivatel.save()
    return pouzivatel


def create_zariadenie(id,typ):
    zariadenie = TypRevizie(
        nazov_revizie=str(id) + '. revizia',
        typ_revizie=typ,
        datum_poslednej_revizie=random_date(),
        datum_nadchadzajucej_revizie=random_date(),
        exspiracia=30)
    zariadenie.save()
    return zariadenie


def clear_data():
    DruhChyby.objects.all().delete()
    DruhRevizie.objects.all().delete()
    MiestoNaLinke.objects.all().delete()
    TypChyby.objects.all().delete()
    # Pravo.objects.all().delete()
    User.objects.all().delete()
    # MaPouzivatelPravo.objects.all().delete()
    TypRevizie.objects.all().delete()
    SposobenaKym.objects.all().delete()


def create_zaznam(miesto_na_linke, druh_chyby, pouzivatel, sposobena_kym, typ_chyby):
    vyriesena = random.choice([True, False])
    zaznam = Chyba(
        miesto_na_linke=miesto_na_linke,
        druh_chyby=druh_chyby,
        vznik=random_date_time(),
        pouzivatel=pouzivatel,
        schvalena=random.choice([True, False]),
        vyriesena=vyriesena,
        vyriesenie=random_date_time(),
        sposobena_kym=sposobena_kym,
        typ_chyby=typ_chyby,
        opatrenia=f'opatrenie #{typ_chyby.id}',
        nahradny_diel='' if not vyriesena else f"diel #{random.randrange(1, 10)}",
        popis=f'popis #{typ_chyby.id}',
        dovod='' if not vyriesena else f"dovod #{typ_chyby.id}",
    )
    zaznam.save()
    return zaznam

def create_typy_revizii():
    ret = []
    for druh in ('elektrické','plynové','tlakové'):
        typ = DruhRevizie(nazov=druh)
        typ.save()
        ret.append(typ)
    return ret

def run_seed(mode):
    clear_data()
    if mode == MODE_CLEAR:
        return

    druhy = create_druh_chyby()
    typy_revizii = create_typy_revizii()
    miesta_na_linke = []
    typy_chyb = []
    sposobene_kym = create_sposobena_kym()
    zariadenia = []
    pouzivatelia = []
    zaznamy = []

    for i in range(1, 11):
        miesta_na_linke.append(create_miesto_na_linke(i))
        # prava.append(create_pravo(i))
        zariadenia.append(create_zariadenie(i,random.choice(typy_revizii)))
        typy_chyb.append(create_typ_chyby(i, miesta_na_linke[-1], random.choice(druhy), random.choice(sposobene_kym)))

    admin = User.objects.create_user(username='admin',
                                     email='admin@poruchy.com',
                                     password='admin',
                                     is_staff=True,
                                     is_active=True,
                                     is_superuser=True
                                     )
    pouzivatelia.append(admin)

    for i in range(1, 10):
        pouzivatelia.append(create_pouzivatel(i))

    # for pouz in pouzivatelia:
    #     ma_prava.append(create_ma_prava(pouz, random.choice(prava)))

    for i in range(1, 50):
        zaznamy.append(create_zaznam(
            random.choice(miesta_na_linke),
            random.choice(druhy),
            random.choice(pouzivatelia),
            random.choice(sposobene_kym),
            random.choice(typy_chyb)
        ))
