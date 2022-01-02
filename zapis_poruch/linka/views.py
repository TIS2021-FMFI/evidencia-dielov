import datetime
from datetime import date, timedelta

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import Permission
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
            return render(request, 'pristup_zakazany.html', {})


        all_errors = ChybaWrapper.all()
        all_types = TypChybyWrapper.all()
        for object in all_types:
            object.fill(all_errors)

        data = {'errors': [x.json() for x in all_types],
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
            return render(request, 'pristup_zakazany.html', {})

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
            return render(request, 'pristup_zakazany.html', {})

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
            return render(request, 'pristup_zakazany.html', {})

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
            return render(request, 'pristup_zakazany.html', {})

        data = dict()
        data["permissions"] = permissions

        if "id" not in request.GET:
            data["form"] = ZaznamForm()
            data["cas"] = False
            return render(request, self.template, data)

        i = request.GET["id"]
        data["form"] = ZaznamForm(instance=Chyba.objects.all().filter(id=i)[0])
        data["datum"] = data["form"]["vznik"]
        data["cas"] = data["form"]["vznik"]
        return render(request, self.template, data)

    def post(self, request):
        permissions = get_user_permissions(request.user)

        if 'add_chyba' not in permissions and 'change_chyba' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {})

        if "id" in request.GET:
            typ = Chyba.objects.all().filter(id=request.GET["id"])[0]
            form = ZaznamForm(request.POST, instance=typ)
        else:
            form = ZaznamForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("zaznamy")


class PridajRevizia(LoginRequiredMixin, View):
    template = "pridaj_revizia.html"

    def get(self, request):
        permissions = get_user_permissions(request.user)

        if 'add_typrevizie' not in permissions and 'change_typrevizie' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {})

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
            return render(request, 'pristup_zakazany.html', {})

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
            return render(request, 'pristup_zakazany.html', {})

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
            return render(request, 'pristup_zakazany.html', {})

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
            return render(request, 'pristup_zakazany.html', {})

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


class Email(LoginRequiredMixin, View):
    template = "email.html"

    def get(self, request):
        if not request.user.is_superuser:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {})

        return render(request, self.template, {})

    def post(self, request):
        if not request.user.is_superuser:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {})

        mail_list = ['namova9094@pyrelle.com']  # , 'freyer.viktor@gmail.com']
        now = datetime.datetime.now()

        start = now + datetime.timedelta(days=27)
        end = now + datetime.timedelta(days=28)
        revizie = TypRevizie.objects.all().filter(datum_nadchadzajucej_revizie__gte=start,
                                                  datum_nadchadzajucej_revizie__lte=end)

        print("pocet", revizie.count())
        if revizie.count() > 0:
            message = ""
            for revizia in revizie:
                message += f"Názov revízie: \"{revizia.nazov_revizie}\"\n" \
                           f"Typ revízie: \"{revizia.typ_revizie}\"\n" \
                           f"Dátum blížiacej sa revízie: " + revizia.datum_nadchadzajucej_revizie.strftime(
                                "%d.%m.%Y") + "\n-------------------------------\n"
            print(message.strip())
            send_mail(
                'Blíži sa dátum revízie!',
                message.strip(),
                'noReplyRevizie@gmail.com',
                mail_list,
                fail_silently=False,
            )
        revizie = TypRevizie.objects.all().filter(datum_nadchadzajucej_revizie__gte=datetime.date.today(),
                                                  datum_nadchadzajucej_revizie__lte=datetime.date.today() + datetime.timedelta(days=1))

        print("pocet", revizie.count())
        if revizie.count() > 0:
            message = ""
            for revizia in revizie:
                message += f"Názov revízie: \"{revizia.nazov_revizie}\"\n" \
                           f"Typ revízie: \"{revizia.typ_revizie}\"\n" \
                           f"Dátum blížiacej sa revízie: " + revizia.datum_nadchadzajucej_revizie.strftime(
                                "%d.%m.%Y") + "\n-------------------------------\n"

            print(message.strip())
            send_mail(
                'Prišiel stanovený dátum revízie!',
                message,
                'noReplyRevizie@gmail.com',
                mail_list,
                fail_silently=False,
            )
        return redirect('email')


class PotvrdZaznam(LoginRequiredMixin, View):
    template = "potvrd_zaznam.html"

    def get(self, request):
        permissions = get_user_permissions(request.user)

        if 'approve_chyba' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {})

        if "put" in request.GET:
            i = request.GET["id"]
            zaznam = Chyba.objects.all().filter(id=i)[0]
            zaznam.schvalena = True
            zaznam.save()
            return redirect('zaznamy')
        else:
            i = request.GET["id"]
            data = dict()
            data["form"] = ZaznamForm(instance=Chyba.objects.all().filter(id=i)[0])
            data['typy'] = TypChyby.objects.all()
            data['id'] = i
            data["permissions"] = permissions
            return render(request, self.template, data)

    def post(self, request):
        permissions = get_user_permissions(request.user)

        if 'approve_chyba' not in permissions:
            print('Prístup odmietnutý')
            return render(request, 'pristup_zakazany.html', {})

        i = request.GET["id"]
        zaznam = Chyba.objects.all().filter(id=i)[0]
        typ = request.GET["list"]
        zaznam.typ_chyby = TypChyby.objects.all().filter(id=typ)[0]
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

