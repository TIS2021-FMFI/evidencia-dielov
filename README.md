# zápis porúch
Studentsky projekt TIS 2021

Vytvaranie virtualneho prostredia:

python -m venv cesta/nazov_prostredia

presun do nazov_prostredia

.\Scripts\activate => pre Windows

source bin/activate => Linux

po otvoreni projektu treba dodrzat tuto postupnost krokov, a nastavit db v settings.py(riadok 81) podla dopredu vytvorenej db(potrebne meno db , meno a heslo pouzivatela, host a port):

pip install -r requirements.txt

python manage.py makemigrations 

python manage.py sqlmigrate

python manage.py migrate

python manage.py creategroups  => vytvorenie pouzivatelskych skupin

python manage.py runserver

python manage.py sendmail   => na poslanie e-mailov

viac na: https://docs.djangoproject.com/en/3.2/intro/tutorial01/

pre vytvorenie prvotneho pouzivatela so vsetkymi pravami:

python manage.py createsuperuser
