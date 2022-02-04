# zápis porúch
Studentsky projekt TIS 2021

Vytvaranie virtualneho prostredia:

    python -m venv cesta/nazov_prostredia

presun do nazov_prostredia:

  => pre Window

    .\Scripts\activate 
    
  => Linux
  
    source bin/activate 
  

po otvoreni projektu treba dodrzat tuto postupnost krokov, a nastavit db v settings.py(riadok 81) podla dopredu vytvorenej db(potrebne meno db , meno a heslo pouzivatela, host a port):

  => nainstalovanie vsetkych potrebnych modulov a kniznic
  
    pip install -r requirements.txt
  
 => vytvorenie db tabuliek so stlpcami a obmedzeniami 
 
    python manage.py makemigrations 

    python manage.py sqlmigrate

    python manage.py migrate
  
=> vytvorenie pouzivatelskych skupin/ prava pre pouzivatelov

    python manage.py creategroups 

=> spustenie servera na localhoste  

    python manage.py runserver
   
 => na poslanie e-mailov
 
    python manage.py sendmail  


viac na: https://docs.djangoproject.com/en/3.2/intro/tutorial01/

pre vytvorenie prvotneho pouzivatela so vsetkymi pravami(zadat email, meno a heslo):

    python manage.py createsuperuser
    
   
