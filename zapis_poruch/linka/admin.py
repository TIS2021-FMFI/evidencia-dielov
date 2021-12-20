from django.contrib import admin
from .models import TypChyby, Chyba, TypRevizie,DruhChyby,SposobenaKym,MiestoNaLinke

# Register your models here.
admin.site.register(Chyba)
admin.site.register(TypChyby)
admin.site.register(TypRevizie)
admin.site.register(SposobenaKym)
admin.site.register(DruhChyby)
admin.site.register(MiestoNaLinke)