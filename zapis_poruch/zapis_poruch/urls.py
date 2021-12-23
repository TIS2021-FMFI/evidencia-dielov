from django.contrib import admin
from django.urls import path, include

from linka.views import TypyChyb, Zaznamy, Grafy, Revizia, PridajTyp, PridajZaznam,\
    Email, Login, Logout, PridajRevizia, PotvrdZaznam



urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('', Zaznamy.as_view(), name='typy'),
    path('typy/', TypyChyb.as_view(), name='typy'),
    path('typy/pridaj', PridajTyp.as_view(), name='pridaj_typ'),
    path('zaznamy/', Zaznamy.as_view(), name='zaznamy'),
    path('zaznamy/pridaj', PridajZaznam.as_view(), name='pridaj_zaznam'),
    path('zaznamy/potvrd', PotvrdZaznam.as_view(), name='potvrd_zaznam'),
    path('grafy/', Grafy.as_view(), name='grafy'),
    path('revizia/', Revizia.as_view(), name='revizia'),
    path('revizia/pridaj', PridajRevizia.as_view(), name='pridaj_zaznam'),
    path('email/', Email.as_view(), name='email'),

]