import datetime

from django.db.models import Q
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import TypForm, ZaznamForm, RevizieForm
from .managment.commands.seed import run_seed
from .models import *
from datetime import date, timedelta


# Create your views here.
class TypyChyb(View):
    template = "chyby_typy.html"

    def get(self, request):
        # run_seed("")
        priemerne_trvanie = dict()
        for object in TypChyby.objects.all():
            chyby = Chyba.objects.all().filter(typ_chyby=object)
            oct = sum([(x.vyriesenie - x.vznik).days for x in chyby]) / len(chyby)

        data = {'errors': TypChyby.objects.all(), 'zaznamy': Chyba.objects.all()}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')


class Zaznamy(View):
    template = "zaznamy.html"

    def get(self, request):
        if "delete" in request.GET:
            i = request.GET["id"]
            chyba = Chyba.objects.all().filter(id=i)
            chyba.delete()
        data = {'zaznamy': Chyba.objects.all()}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')


class PridajTyp(View):
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


class PridajZaznam(View):
    template = "pridaj_zaznam.html"

    def get(self, request):
        data = dict()

        if "id" not in request.GET:
            data["form"] = ZaznamForm()
            return render(request, self.template, data)

        i = request.GET["id"]
        data["form"] = ZaznamForm(instance=Chyba.objects.all().filter(id=i)[0])
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


class PridajRevizia(View):
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


class Revizia(View):
    template = "revizia.html"

    def get(self, request):
        if "delete" in request.GET:
            i = request.GET["id"]
            revizia = TypRevizie.objects.all().filter(id=i)
            revizia.delete()
        data = {'revizie': TypRevizie.objects.all(), 'today': date.today(), 'weeks': date.today() + timedelta(days=28)}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')


class Grafy(View):
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
        grafColors = ['#C7980A', '#F4651F', '#82D8A7', '#CC3A05', '#575E76', '#156943', '#0BD055', '#ACD338'][:count]

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
