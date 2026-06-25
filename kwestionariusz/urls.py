from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('epworth/', views.epworth, name='epworth'),
    path('ipaq/', views.ipaq, name='ipaq'),
    path('pittsburgh/', views.pittsburgh, name='pittsburgh'),
    path('koniec/', views.koniec, name='koniec'),
    path('panel/', views.panel, name='panel'),
    path('panel/badanie/<int:badanie_id>/', views.szczegoly_badania, name='szczegoly_badania'),
    path('dane-podstawowe/', views.dane_podstawowe, name='dane_podstawowe'),
    path('operacja-bariatryczna/', views.operacja_bariatryczna, name='operacja_bariatryczna'),
    path('cpap-zdrowie/', views.cpap_zdrowie, name='cpap_zdrowie'),
]