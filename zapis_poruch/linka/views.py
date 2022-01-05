import datetime
import time
from datetime import date, timedelta

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import Permission, User
from .forms import TypForm, ZaznamForm, RevizieForm
from .models import TypChyby, Chyba, TypRevizie, ChybaWrapper, TypChybyWrapper, DruhChyby, \
    MiestoNaLinke, SposobenaKym


def get_user_permissions(user):
    if user.is_superuser:
        return {perm.codename for perm in Permission.objects.all()}

    user_perms = {x.codename for x in user.user_permissions.all()}
    group_perms = {x.codename for x in Permission.objects.filter(group__user=user)}
    return user_perms | group_perms


class TypyChyb(LoginRequiredMixin, View):
    template = "chyby_typy.html"

    def get(self, request):
        permissions = get_user_permissions(request.user)

        if 'view_typchyby' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        all_errors = ChybaWrapper.all()
        all_types = TypChybyWrapper.all()
        for typ in all_types:
            typ.fill(all_errors)

        data = {'chyby': [x.json() for x in all_types],
                'permissions': permissions
                }

        if "order_by" in request.GET:
            order_by = request.GET.get('order_by', 'defaultOrderField')
            print(order_by)
            if order_by == "pozicia":
                data['errors'] = sorted(data['errors'], key=lambda obj: obj['miesto_na_linke'])
            if order_by == "povod":
                data['errors'] = sorted(data['errors'], key=lambda obj: obj['sposobena_kym'])
            if order_by == "druh":
                data['errors'] = sorted(data['errors'], key=lambda obj: obj['druh_chyby'])
            if order_by == "popis":
                data['errors'] = sorted(data['errors'], key=lambda obj: obj['popis'])
            if order_by == "trvanie":
                data['errors'] = sorted(data['errors'], key=lambda obj: obj['trvanie'])

        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')


class Zaznamy(LoginRequiredMixin, View):
    template = "zaznamy.html"

    def get(self, request):
        permissions = get_user_permissions(request.user)

        if 'view_chyba' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        if "delete" in request.GET:
            i = request.GET["id"]
            chyba = Chyba.objects.all().filter(id=i)
            chyba.delete()

        data = {'zaznamy': ChybaWrapper.all(),
                'permissions': permissions
                }

        if "order_by" in request.GET:
            order_by = request.GET.get('order_by', 'defaultOrderField')
            print(order_by)
            if order_by == "stav":
                data['zaznamy'] = sorted(data['zaznamy'], key=lambda obj: (obj.schvalena, obj.vyriesena))
            if order_by == "cas":
                data['zaznamy'] = sorted(data['zaznamy'], key=lambda obj: obj.vznik)
            if order_by == "trvanie":
                data['zaznamy'] = sorted(data['zaznamy'], key=lambda obj: obj.trvanie)
            if order_by == "pozicia":
                data['zaznamy'] = sorted(data['zaznamy'], key=lambda obj: obj.miesto_na_linke.id)
            if order_by == "sposobena_kym":
                data['zaznamy'] = sorted(data['zaznamy'], key=lambda obj: obj.sposobena_kym.id)
            if order_by == "popis":
                data['zaznamy'] = sorted(data['zaznamy'], key=lambda obj: obj.popis)
            if order_by == "uzivatel":
                data['zaznamy'] = sorted(data['zaznamy'], key=lambda obj: obj.pouzivatel.id)
            if order_by == "dovod":
                data['zaznamy'] = sorted(data['zaznamy'], key=lambda obj: obj.dovod)
            if order_by == "opatrenie":
                data['zaznamy'] = sorted(data['zaznamy'], key=lambda obj: obj.opatrenia)
        else:
            data['zaznamy'] = sorted(data['zaznamy'], key=lambda obj: (obj.schvalena, obj.vyriesena))

        return render(request, self.template, data)

    def post(self, request):
        return redirect("zaznamy")


class PridajTyp(LoginRequiredMixin, View):
    template = "pridaj_typ.html"

    def get(self, request):
        permissions = get_user_permissions(request.user)

        if 'add_typchyby' not in permissions and 'change_typchyby' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        data = dict()
        data["permissions"] = permissions

        if "id" not in request.GET:
            data["form"] = TypForm()
            return render(request, self.template, data)

        i = request.GET["id"]
        data["form"] = TypForm(instance=TypChyby.objects.all().filter(id=i)[0])
        return render(request, self.template, data)

    def post(self, request):
        permissions = get_user_permissions(request.user)

        if 'add_typchyby' not in permissions and 'change_typchyby' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        if "id" in request.GET:
            typ = TypChyby.objects.all().filter(id=request.GET["id"])[0]
            form = TypForm(request.POST, instance=typ)
        else:
            form = TypForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("typy")


class PridajZaznam(LoginRequiredMixin, View):
    template = "pridaj_zaznam.html"

    def get(self, request):
        permissions = get_user_permissions(request.user)

        if 'add_chyba' not in permissions and 'change_chyba' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        data = dict()
        data["permissions"] = permissions

        if "id" not in request.GET:
            form = ZaznamForm()

            data["form"] = form

            return render(request, self.template, data)

        i = request.GET["id"]
        data["form"] = ZaznamForm(instance=Chyba.objects.all().filter(id=i)[0])
        return render(request, self.template, data)

    def post(self, request):
        permissions = get_user_permissions(request.user)

        if 'add_chyba' not in permissions and 'change_chyba' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        if "id" in request.GET:
            typ = Chyba.objects.all().filter(id=request.GET["id"])[0]
            form = ZaznamForm(request.POST, instance=typ)
        else:
            form = ZaznamForm(request.POST)
            typ = Chyba()

        if form.is_valid():
            print('valid')
        else:
            print('not valid')
            return render(request, self.template, {'form': form,'permissions':permissions})

        typ.pouzivatel = User.objects.all().filter(id=request.user.id)[0]
        typ.vznik = form['vznik'].value() + 'T' + form['vznik_cas'].value()

        try:
            print('vyriesenie', time.strptime(form['vyriesenie'].value(), '%Y-%m-%d'))
            print('vyriesenie_cas', time.strptime(form['vyriesenie_cas'].value(), '%H:%M:%S'))
            typ.vyriesenie = form['vyriesenie'].value() + 'T' + form['vyriesenie_cas'].value()
        except ValueError:
            typ.vyriesenie = None

        typ.vyriesena = True if form['vyriesena'].value() else False
        typ.miesto_na_linke = MiestoNaLinke.objects.all().filter(id=form['miesto_na_linke'].value())[0]
        typ.popis = form['popis'].value()
        typ.sposobena_kym = SposobenaKym.objects.all().filter(id=form['sposobena_kym'].value())[0]
        typ.opatrenia = form['opatrenia'].value()
        typ.druh_chyby = DruhChyby.objects.all().filter(id=form['druh_chyby'].value())[0]
        typ.nahradny_diel = form['nahradny_diel'].value()
        typ.dovod = form['dovod'].value()

        typ.save()

        return redirect("zaznamy")


class PridajRevizia(LoginRequiredMixin, View):
    template = "pridaj_revizia.html"

    def get(self, request):
        permissions = get_user_permissions(request.user)

        if 'add_typrevizie' not in permissions and 'change_typrevizie' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        data = dict()
        data["permissions"] = permissions

        if "id" not in request.GET:
            empty = TypRevizie(datum_poslednej_revizie=datetime.date.today)
            empty.datum_nadchadzajucej_revizie = date.today() + timedelta(days=int(empty.exspiracia))
            data["form"] = RevizieForm(instance=empty)
            return render(request, self.template, data)

        i = request.GET["id"]
        data["form"] = RevizieForm(instance=TypRevizie.objects.all().filter(id=i)[0])
        return render(request, self.template, data)

    def post(self, request):
        permissions = get_user_permissions(request.user)

        if 'add_typrevizie' not in permissions and 'change_typrevizie' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        if "id" in request.GET:
            typ = TypRevizie.objects.all().filter(id=request.GET["id"])[0]
            form = RevizieForm(request.POST, instance=typ)
        else:
            form = RevizieForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("revizia")


class Revizia(LoginRequiredMixin, View):
    template = "revizia.html"

    def get(self, request):
        permissions = get_user_permissions(request.user)

        if 'view_typrevizie' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        if "delete" in request.GET:
            i = request.GET["id"]
            revizia = TypRevizie.objects.all().filter(id=i)[0]
            revizia.delete()

        elif "put" in request.GET:
            i = request.GET["id"]
            revizia = TypRevizie.objects.all().filter(id=i)[0]
            revizia.datum_poslednej_revizie = date.today()
            revizia.datum_nadchadzajucej_revizie = date.today() + timedelta(days=int(revizia.exspiracia))
            revizia.save()

        data = {'revizie': TypRevizie.objects.all(),
                'today': date.today(),
                'weeks': date.today() + timedelta(days=28),
                'permissions': permissions
                }

        if "order_by" in request.GET:
            order_by = request.GET.get('order_by', 'defaultOrderField')
            print(order_by)
            if order_by == "nazov":
                data['revizie'] = sorted(data['revizie'], key=lambda obj: obj.nazov_revizie)
            if order_by == "typ":
                data['revizie'] = sorted(data['revizie'], key=lambda obj: obj.typ_revizie.nazov)
            if order_by == "datum_poslednej":
                data['revizie'] = sorted(data['revizie'], key=lambda obj: obj.datum_poslednej_revizie)
            if order_by == "datum_dalsej":
                data['revizie'] = sorted(data['revizie'], key=lambda obj: obj.datum_nadchadzajucej_revizie)

        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')


class Grafy(LoginRequiredMixin, View):
    template = "grafy.html"

    def get(self, request):
        permissions = get_user_permissions(request.user)

        if 'view_grafy' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        data = {
            "druhyChyb": DruhChyby.objects.all(),
            "zariadenia": MiestoNaLinke.objects.all(),
            "sposobeneKym": SposobenaKym.objects.all(),
            "popisyTypovChyby": TypChyby.objects.all(),
            "permissions": permissions,
        }

        return render(request, self.template, data)

    def post(self, request):
        permissions = get_user_permissions(request.user)

        if 'view_grafy' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        def getInt(val):
            try:
                return int(val)
            except:
                return 0

        grafLabels = []
        start_date = datetime.datetime.strptime(request.POST['beginDate'], "%Y-%m-%d")
        end_date = datetime.datetime.strptime(request.POST['endDate'], "%Y-%m-%d") + datetime.timedelta(days=1)
        diff = abs((end_date - start_date).days)
        count = 0
        for i in range(0, diff, int(request.POST['casoveObdobie'])):
            grafLabels.append((start_date + datetime.timedelta(days=i)).strftime("%d.%m.%Y"))
            count += 1
        grafColors = ['#E28C05', '#4A501A', '#8F5BCA', '#B7E30B', '#BAB1EB', '#979EF9', '#6B2F11', '#622590', '#D03C3F',
                      '#96A321', '#A6994E', '#93B8B9', '#8EFD82', '#EE239D', '#3834A7', '#BE561D', '#29FEB9', '#0AC84D',
                      '#0BDC93', '#BACFBA', '#46227D', '#504FD5', '#00DC0E', '#CF1A54', '#955DC2', '#705678', '#DAED28',
                      '#B694C3', '#413707', '#A59E7E', '#523087', '#B365DF', '#F2DE74', '#F00C9A', '#22459D', '#E61080',
                      '#AAA3D1', '#CCE9E1', '#2FE622', '#3281D6'][:count]

        grafData = [0] * count
        chyby = Chyba.objects.filter(
            vznik__gte=start_date,
            vznik__lte=end_date
        )
        print("druh chyby", type(request.POST.get('druhChyby', 0)))
        for chyba in chyby:
            if request.POST.get("druhChyby", '') != '':
                if str(chyba.druh_chyby_id) != request.POST.get('druhChyby'):
                    continue
            if request.POST.get("chybuSposobil", '') != '':
                if str(chyba.sposobena_kym_id) != request.POST.get('chybuSposobil'):
                    continue
            if request.POST.get("cisloZariadenia", '') != '':
                if str(chyba.miesto_na_linke_id) != request.POST.get('cisloZariadenia'):
                    continue
            if request.POST.get("popisTypuChyby", '') != '':
                if str(chyba.typ_chyby_id) != request.POST.get('popisTypuChyby'):
                    continue
            index = (chyba.vznik.replace(tzinfo=None) - start_date).days // int(request.POST['casoveObdobie'])
            grafData[index] += 1
        data = {
            "casoveObdobieOld": getInt(request.POST.get("casoveObdobie", 0)),
            "druhChybyOld": getInt(request.POST.get("druhChyby", 0)),
            "cisloZariadeniaOld": getInt(request.POST.get("cisloZariadenia", 0)),
            "beginDateOld": request.POST["beginDate"],
            "endDateOld": request.POST["endDate"],
            "chybuSposobilOld": getInt(request.POST.get("chybuSposobil", 0)),
            "popisTypuChyby": getInt(request.POST.get("popisTypuChyby", 0)),
            "druhyChyb": DruhChyby.objects.all(),
            "zariadenia": MiestoNaLinke.objects.all(),
            "sposobeneKym": SposobenaKym.objects.all(),
            "popisyTypovChyby": TypChyby.objects.all(),
            "grafLabels": grafLabels,
            "grafColors": grafColors,
            "grafData": grafData,
            "permissions": permissions
        }
        return render(request, self.template, data)


class PotvrdZaznam(LoginRequiredMixin, View):
    template = "potvrd_zaznam.html"

    def get(self, request):
        permissions = get_user_permissions(request.user)

        if 'approve_chyba' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        i = request.GET["id"]
        data = dict()
        zaznam = Chyba.objects.all().filter(id=i)[0]

        if zaznam.schvalena or not zaznam.vyriesena:
            return redirect('zaznamy')

        data["form"] = ZaznamForm(instance=zaznam)

        for pole in ['vznik', 'vznik_cas', 'vyriesena', 'miesto_na_linke', 'popis',
                     'vyriesenie', 'vyriesenie_cas', 'sposobena_kym', 'opatrenia',
                     'druh_chyby', 'nahradny_diel', 'dovod']:
            data['form'][pole].field.disabled = True

        data['typy'] = TypChyby.objects.all().filter(sposobena_kym=zaznam.sposobena_kym).filter(
            druh_chyby=zaznam.druh_chyby).filter(miesto_na_linke=zaznam.miesto_na_linke)
        data['id'] = i
        data["permissions"] = permissions
        return render(request, self.template, data)

    def post(self, request):
        permissions = get_user_permissions(request.user)

        if 'approve_chyba' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {'permissions': permissions})

        i = request.GET["id"]
        zaznam = Chyba.objects.all().filter(id=i)[0]

        typID = int(request.POST["typ"])
        zaznam.typ_chyby = TypChyby.objects.all().filter(id=typID)[0]
        zaznam.schvalena = True

        zaznam.save()
        return redirect("zaznamy")


class Login(LoginView):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().get(request, args, kwargs)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("login")
