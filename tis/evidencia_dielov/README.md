Vytvaranie virtualneho prostredia:

python -m venv cesta/nazov_prostredia

presun do nazov_prostredia

.\Scripts\activate => pre Windows

source bin/activate => Linux

po otvoreni projektu treba dodrzat tuto postupnost krokov:

pip install -r requirements.txt

python manage.py makemigrations 

python manage.py sqlmigrate

python manage.py migrate

python manage.py runserver

viac na: https://docs.djangoproject.com/en/3.2/intro/tutorial01/

