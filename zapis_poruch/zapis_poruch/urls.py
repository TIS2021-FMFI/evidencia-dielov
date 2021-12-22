from django.contrib import admin
from django.urls import path, include

from linka.views import TypyChyb, Zaznamy, Grafy, Revizia, PridajTyp, PridajZaznam,\
    Email, Pouzivatelia, Login, Logout, Seed, PridajRevizia, PotvrdZaznam



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Zaznamy.as_view(), name='typy'),
    path('typy/', TypyChyb.as_view(), name='typy'),
    path('login/', Login.as_view(), name='login'),
    path('zaznamy/', Zaznamy.as_view(), name='zaznamy'),
    path('grafy/', Grafy.as_view(), name='grafy'),
    path('typy/pridaj', PridajTyp.as_view(), name='pridaj_typ'),
    path('zaznamy/pridaj', PridajZaznam.as_view(), name='pridaj_zaznam'),
    path('zaznamy/potvrd', PotvrdZaznam.as_view(), name='potvrd_zaznam'),
    path('revizia/pridaj', PridajRevizia.as_view(), name='pridaj_zaznam'),
    path('revizia/', Revizia.as_view(), name='revizia'),
    path('email/', Email.as_view(), name='email'),
    path('pouzivatelia/', Pouzivatelia.as_view(), name='pouzivatelia'),
    path('logout/', Logout.as_view(), name='logout'),
    path('seed/', Seed.as_view(), name='logout'),
    path('email/', Email.as_view(), name='email'),



]