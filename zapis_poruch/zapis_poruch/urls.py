from django.contrib import admin
from django.urls import path, include
from linka.views import TypyChyb, Zaznamy, Grafy, Revizia, PridajTyp, PridajZaznam

urlpatterns = [
    path('admin/', admin.site.urls),
    path('typy/', TypyChyb.as_view(), name='typy'),
    path('zaznamy/', Zaznamy.as_view(), name='zaznamy'),
    path('grafy/', Grafy.as_view(), name='grafy'),
    path('typy/', PridajTyp.as_view(), name='pridaj_typ'),
    path('zaznamy/', PridajZaznam.as_view(), name='pridaj_zaznam'),
    path('revizia/', Revizia.as_view(), name='revizia'),


]