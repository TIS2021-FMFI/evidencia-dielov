
import datetime
from django.db.models import Q
import time
import django.contrib.auth.models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import TypForm, ZaznamForm, RevizieForm
from .managment.commands.seed import run_seed
from .models import TypChyby, Chyba, TypRevizie, Pouzivatel, ChybaWrapper, TypChybyWrapper
from datetime import date, timedelta
from django.contrib.auth.views import LoginView

from django.core.mail import send_mail


class Seed(View):
    def get(self, request):
        run_seed("")
        next = request.POST.get('next', '/')
        return redirect(next)


class TypyChyb(LoginRequiredMixin, View):
    template = "chyby_typy.html"

    def get(self, request):
        all_errors = ChybaWrapper.all()
        all_types = TypChybyWrapper.all()
        for object in all_types:
            object.fill(all_errors)

        data = {'errors': [x.json() for x in all_types]}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')


class Zaznamy(LoginRequiredMixin, View):
    template = "zaznamy.html"

    def get(self, request):
        if "delete" in request.GET:
            i = request.GET["id"]
            chyba = Chyba.objects.all().filter(id=i)
            chyba.delete()
        data = {'zaznamy': ChybaWrapper.all()}
        return render(request, self.template, data)

    def post(self, request):
        return redirect("zaznamy")


class PridajTyp(LoginRequiredMixin, View):
    template = "pridaj_typ.html"

    def get(self, request):
        data = dict()

        if "id" not in request.GET:
            data["form"] = TypForm()
            return render(request, self.template, data)

        i = request.GET["id"]
        data["form"] = TypForm(instance=TypChyby.objects.all().filter(id=i)[0])
        return render(request, self.template, data)

    def post(self, request):
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
        data = dict()

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
        data = dict()

        if "id" not in request.GET:
            data["form"] = RevizieForm()
            return render(request, self.template, data)

        i = request.GET["id"]
        data["form"] = RevizieForm(instance=TypRevizie.objects.all().filter(id=i)[0])
        return render(request, self.template, data)

    def post(self, request):
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

        data = {'revizie': TypRevizie.objects.all(), 'today': date.today(), 'weeks': date.today() + timedelta(days=28)}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')


class Grafy(LoginRequiredMixin, View):
    template = "grafy.html"

    def get(self, request):
        data = {
            "druhyChyb" : DruhChyby.objects.all(),
            "zariadenia" : MiestoNaLinke.objects.all(),
            "sposobeneKym" : SposobenaKym.objects.all(),
            "popisyTypovChyby" : TypChyby.objects.all()
        }
        return render(request, self.template, data)

    def post(self, request):
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
        grafColors = ['#E28C05', '#4A501A', '#8F5BCA', '#B7E30B', '#BAB1EB', '#979EF9', '#6B2F11', '#622590', '#D03C3F', '#96A321', '#A6994E', '#93B8B9', '#8EFD82', '#EE239D', '#3834A7', '#BE561D', '#29FEB9', '#0AC84D', '#0BDC93', '#BACFBA', '#46227D', '#504FD5', '#00DC0E', '#CF1A54', '#955DC2', '#705678', '#DAED28', '#B694C3', '#413707', '#A59E7E', '#523087', '#B365DF', '#F2DE74', '#F00C9A', '#22459D', '#E61080', '#AAA3D1', '#CCE9E1', '#2FE622', '#3281D6'][:count]

        grafData = [0]*count
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
            "grafLabels" : grafLabels,
            "grafColors" : grafColors,
            "grafData" : grafData
        }
        return render(request, self.template, data)


class Email(View):
    template = "email.html"

    def get(self, request):

        return render(request, self.template, {})

    def post(self, request):
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=28)
        end = now - datetime.timedelta(days=27)
        revizie = TypRevizie.objects.all().filter(datum_nadchadzajucej_revizie__gte=start, datum_nadchadzajucej_revizie__lte=end)
        revizia = None
        print("pocet", revizie.count())
        if revizie.count() > 0:
            revizia = revizie[0]
        if revizia is None:
            return redirect('email')
        send_mail(
            'Blizi sa revizia',
            revizia.nazov_revizie + ', ' + revizia.typ_revizie + ', ' + revizia.datum_nadchadzajucej_revizie.strftime("%d.%m.%Y"),
            'noReplyRevizie@gmail.com',
            ['freyer.viktor@gmail.com'],
            fail_silently=False,
        )
        revizie = TypRevizie.objects.all().filter(datum_nadchadzajucej_revizie__gte=datetime.date.today(),
                                                  datum_nadchadzajucej_revizie__lte=now)
        revizia = None
        print("pocet", revizie.count())
        if revizie.count() > 0:
            revizia = revizie[0]
        if revizia is None:
            return redirect('email')
        send_mail(
            'Je cas na reviziu',
            revizia.nazov_revizie + ', ' + revizia.typ_revizie + ', ' + revizia.datum_nadchadzajucej_revizie.strftime(
                "%d.%m.%Y"),
            'noReplyRevizie@gmail.com',
            ['freyer.viktor@gmail.com'],
            fail_silently=False,
        )
        return redirect('email')



class PotvrdZaznam(View):
    template = "potvrd_zaznam.html"

    def get(self, request):
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
            return render(request, self.template, data)

    def post(self, request):
        i = request.GET["id"]
        zaznam = Chyba.objects.all().filter(id=i)[0]
        typ = request.GET["list"]
        zaznam.typ_chyby = TypChyby.objects.all().filter(id=typ)[0]
        zaznam.save()
        return redirect("zaznamy")

class Pouzivatelia(LoginRequiredMixin, View):
    template = "pouzivatelia.html"

    def get(self, request):
        if "delete" in request.GET and request.GET["delete"]:
            i = request.GET["id"]
            pouzivatel = Pouzivatel.objects.all().filter(id=i)
            pouzivatel.delete()
        data = {"pouzivatelia": Pouzivatel.objects.all()}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')

class Login(LoginView):
    template_name = "login.html"

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("login")
