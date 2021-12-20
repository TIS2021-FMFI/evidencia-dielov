
import datetime
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
from .models import *
from datetime import date, timedelta
from django.contrib.auth.views import LoginView



class TypyChyb(LoginRequiredMixin, View):
    template = "chyby_typy.html"

    def get(self, request):
        #run_seed("")
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
            revizia.datum_nadchadzajucej_revizie = date.today() + timedelta(days=revizia.exspiracia)
            revizia.save()

        data = {'revizie': TypRevizie.objects.all(), 'today': date.today(), 'weeks': date.today() + timedelta(days=28)}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')


class Grafy(LoginRequiredMixin, View):
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