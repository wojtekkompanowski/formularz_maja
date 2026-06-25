from django.contrib import admin
from .models import Pacjent, Badanie, Epworth, IPAQ, Pittsburgh


@admin.register(Pacjent)
class PacjentAdmin(admin.ModelAdmin):
    list_display = ('kod', 'data_utworzenia')
    search_fields = ('kod',)


@admin.register(Badanie)
class BadanieAdmin(admin.ModelAdmin):
    list_display = ('pacjent', 'data_badania')
    search_fields = ('pacjent__kod',)
    list_filter = ('data_badania',)


@admin.register(Epworth)
class EpworthAdmin(admin.ModelAdmin):
    list_display = ('badanie', 'wynik', 'interpretacja', 'data_wypelnienia')
    search_fields = ('badanie__pacjent__kod',)


@admin.register(IPAQ)
class IPAQAdmin(admin.ModelAdmin):
    list_display = ('badanie', 'wynik_met', 'kategoria', 'data_wypelnienia')
    search_fields = ('badanie__pacjent__kod',)
    list_filter = ('kategoria',)


@admin.register(Pittsburgh)
class PittsburghAdmin(admin.ModelAdmin):
    list_display = ('badanie', 'wynik', 'data_wypelnienia')
    search_fields = ('badanie__pacjent__kod',)