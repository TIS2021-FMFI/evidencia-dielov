from django.contrib import admin
from django.urls import path, include
from linka.views import TypyChyb_view, Zaznamy_view, Grafy_view, PridajTyp_view, \
    PridajZaznam_view, PridajReviziu_view, Revizia_view, Pouzivatelia_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('typy/', TypyChyb_view.as_view(), name='typy'),
    path('zaznamy/', Zaznamy_view.as_view(), name='zaznamy'),
    path('grafy/', Grafy_view.as_view(), name='grafy'),
    path('typy/pridaj', PridajTyp_view.as_view(), name='pridaj_typ'),
    path('zaznamy/pridaj', PridajZaznam_view.as_view(), name='pridaj_zaznam'),
    path('revizia/pridaj', PridajReviziu_view.as_view(), name='pridaj_zaznam'),
    path('revizia/', Revizia_view.as_view(), name='revizia'),
    path('pouzivatelia/', Pouzivatelia_view.as_view(), name='pouzivatelia'),

]