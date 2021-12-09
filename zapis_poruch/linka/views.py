import datetime
import time

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
        #run_seed("")
        priemerne_trvanie = dict()
        for object in TypChyby.objects.all():
            chyby = Chyba.objects.all().filter(typ_chyby=object)
            #oct = sum([(x.vyriesenie - x.vznik).days for x in chyby]) / len(chyby)

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


class Pouzivatelia(View):
    template = "pouzivatelia.html"

    def get(self, request):
        return render(request, self.template)

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

class PridajPouzivatela(View):
    template = "pridaj_pouzivatela.html"

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        if "id" in request.GET:
            typ = TypChyby.objects.all().filter(id=request.GET["id"])[0]
            form = TypForm(request.POST, instance=typ)
        else:
           form = TypForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("pouzivatelia")


class PridajZaznam(View):
    template = "pridaj_zaznam.html"

    def get(self, request):
        data = dict()

        if "id" not in request.GET:
            data["current_date"] = date.today().isoformat().replace("-", "/")
            data["current_time"] = datetime.datetime.now().time()
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

        elif "put" in request.GET:
            i = request.GET["id"]
            revizia = TypRevizie.objects.all().filter(id=i)
            revizia.datum_poslednej_revizie = date.today()
            revizia.datum_nadchadzajucej_revizie = date.today() + timedelta(days=revizia.exspiracia)
            revizia.save()

        data = {'revizie': TypRevizie.objects.all(), 'today': date.today(), 'weeks': date.today() + timedelta(days=28)}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')


class Grafy(View):
    template = "grafy.html"

    def get(self, request):
        data = {'list': [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]], }
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')


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
        return HttpResponse('podarilo sa')
