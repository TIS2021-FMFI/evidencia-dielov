from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
class TypyChyb(View):
    template = "chyby_typy.html"

    def get(self, request):
        data = {'list': [[1, 2, 3, 4, 5, 6],[1, 2, 3, 4, 5, 6]],}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')

class Zaznamy(View):
    template = "zaznamy.html"

    def get(self, request):
        data = {'list': [[1, 2, 3, 4, 5, 6],[1, 2, 3, 4, 5, 6]],}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')

class PridajTyp(View):
    template = "pridaj_typ.html"

    def get(self, request):
        data = {'list': [[1, 2, 3, 4, 5, 6],[1, 2, 3, 4, 5, 6]],}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')

class PridajZaznam(View):
    template = "pridaj_zaznam.html"

    def get(self, request):
        data = {'list': [[1, 2, 3, 4, 5, 6],[1, 2, 3, 4, 5, 6]],}
        return render(request, self.template, data)

    def post(self, request):
        return HttpResponse('podarilo sa')

class Revizia(View):
    template = "revizia.html"

    def get(self, request):
        data = {'list': [[1, 2, 3, 4, 5, 6],[1, 2, 3, 4, 5, 6]],}
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