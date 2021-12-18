from django.contrib import admin
from django.urls import path, include
from linka.views import TypyChyb, Zaznamy, Grafy, Revizia, PridajTyp, PridajZaznam, Pouzivatelia

from linka.views import PridajRevizia

urlpatterns = [
    path('admin/', admin.site.urls),
    path('typy/', TypyChyb.as_view(), name='typy'),
    path('zaznamy/', Zaznamy.as_view(), name='zaznamy'),
    path('grafy/', Grafy.as_view(), name='grafy'),
    path('typy/pridaj', PridajTyp.as_view(), name='pridaj_typ'),
    path('zaznamy/pridaj', PridajZaznam.as_view(), name='pridaj_zaznam'),
    path('revizia/pridaj', PridajRevizia.as_view(), name='pridaj_zaznam'),
    path('revizia/', Revizia.as_view(), name='revizia'),
    path('pouzivatelia/', Pouzivatelia.as_view(), name='pouzivatelia'),

]