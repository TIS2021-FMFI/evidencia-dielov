from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import TypForm, ZaznamForm
from .managment.commands.seed import run_seed
from .models import *


# Create your views here.
class TypyChyb(View):
    template = "chyby_typy.html"

    def get(self, request):
        #run_seed("")
        priemerne_trvanie = dict()
        for object in TypChyby.objects.all():
            chyby = Chyba.objects.all().filter(typ_chyby=object)
            # priemerne_trvanie[object] = sum([x.trvanie])



        data = {'errors': TypChyby.objects.all()}
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

class Revizia(View):
    template = "revizia.html"

    def get(self, request):
        data = {'revizie': TypRevizie.objects.all()}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')

class Grafy(View):
    template = "grafy.html"

    def get(self, request):
        data = {'list': [[1, 2, 3, 4, 5, 6],[1, 2, 3, 4, 5, 6]],}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')