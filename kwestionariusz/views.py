from django.shortcuts import render, redirect, get_object_or_404
from .forms import KodPacjentaForm, DanePodstawoweForm, EpworthForm, IPAQForm, PittsburghForm, OperacjaBariatrycznaForm, CPAPZdrowieForm
from .models import Pacjent, Badanie, Epworth, IPAQ, Pittsburgh
from django.contrib.auth.decorators import login_required
from .dashboard import PanelFilterForm, apply_panel_filters, build_dashboard_context, build_record_view


def start(request):
    if request.method == 'POST':
        form = KodPacjentaForm(request.POST)

        if form.is_valid():
            kod = form.cleaned_data['kod']

            pacjent, created = Pacjent.objects.get_or_create(kod=kod)
            badanie = Badanie.objects.create(pacjent=pacjent)

            request.session['badanie_id'] = badanie.id
            request.session['kod_pacjenta'] = kod

            return redirect('dane_podstawowe')

    else:
        form = KodPacjentaForm()

    return render(request, 'kwestionariusz/start.html', {'form': form})

def epworth(request):
    kod_pacjenta = request.session.get('kod_pacjenta')

    if not kod_pacjenta:
        return redirect('start')

    badanie_id = request.session.get('badanie_id')

    if not badanie_id:
        return redirect('start')

    badanie = Badanie.objects.get(id=badanie_id)

    if request.method == 'POST':
        form = EpworthForm(request.POST)

        if form.is_valid():
            Epworth.objects.update_or_create(
                badanie=badanie,
                defaults={
                    'pytanie_1': int(form.cleaned_data['pytanie_1']),
                    'pytanie_2': int(form.cleaned_data['pytanie_2']),
                    'pytanie_3': int(form.cleaned_data['pytanie_3']),
                    'pytanie_4': int(form.cleaned_data['pytanie_4']),
                    'pytanie_5': int(form.cleaned_data['pytanie_5']),
                    'pytanie_6': int(form.cleaned_data['pytanie_6']),
                    'pytanie_7': int(form.cleaned_data['pytanie_7']),
                    'pytanie_8': int(form.cleaned_data['pytanie_8']),
                }
            )

            return redirect('ipaq')

    else:
        form = EpworthForm()

    return render(
        request,
        'kwestionariusz/epworth.html',
        {
            'form': form,
            'kod_pacjenta': kod_pacjenta,
        }
    )

def ipaq(request):
    kod_pacjenta = request.session.get('kod_pacjenta')

    if not kod_pacjenta:
        return redirect('start')

    badanie_id = request.session.get('badanie_id')

    if not badanie_id:
        return redirect('start')

    badanie = Badanie.objects.get(id=badanie_id)

    if request.method == 'POST':
        form = IPAQForm(request.POST)

        if form.is_valid():
            IPAQ.objects.update_or_create(
                badanie=badanie,
                defaults={
                    'szpital': form.cleaned_data['szpital'] == 'True',
                    'choroba': form.cleaned_data['choroba'] == 'True',
                    'rehabilitacja': form.cleaned_data['rehabilitacja'] == 'True',
                    'urlop': form.cleaned_data['urlop'] == 'True',
                    'rekonwalescencja': form.cleaned_data['rekonwalescencja'] == 'True',
                    'ciaza': form.cleaned_data['ciaza'] == 'True',
                    'intensywne_dni': form.cleaned_data['intensywne_dni'],
                    'intensywne_minuty': form.cleaned_data['intensywne_minuty'],
                    'umiarkowane_dni': form.cleaned_data['umiarkowane_dni'],
                    'umiarkowane_minuty': form.cleaned_data['umiarkowane_minuty'],
                    'chodzenie_dni': form.cleaned_data['chodzenie_dni'],
                    'chodzenie_minuty': form.cleaned_data['chodzenie_minuty'],
                    'siedzenie_minuty_dziennie': form.cleaned_data['siedzenie_minuty_dziennie'],
                }
            )

            return redirect('pittsburgh')

    else:
        form = IPAQForm()

    return render(
        request,
        'kwestionariusz/ipaq.html',
        {
            'form': form,
            'kod_pacjenta': kod_pacjenta,
        }
    )

def pittsburgh(request):
    kod_pacjenta = request.session.get('kod_pacjenta')

    if not kod_pacjenta:
        return redirect('start')

    badanie_id = request.session.get('badanie_id')

    if not badanie_id:
        return redirect('start')

    badanie = Badanie.objects.get(id=badanie_id)

    if request.method == 'POST':
        form = PittsburghForm(request.POST)

        if form.is_valid():
            Pittsburgh.objects.update_or_create(
                badanie=badanie,
                defaults={
                    'godzina_polozenia': form.cleaned_data['godzina_polozenia'],
                    'czas_zasypiania_minuty': form.cleaned_data['czas_zasypiania_minuty'],
                    'godzina_wstawania': form.cleaned_data['godzina_wstawania'],
                    'godziny_snu': form.cleaned_data['godziny_snu'],

                    'nie_zasnal_30_min': int(form.cleaned_data['nie_zasnal_30_min']),
                    'pobudka_w_nocy': int(form.cleaned_data['pobudka_w_nocy']),
                    'toaleta': int(form.cleaned_data['toaleta']),
                    'problemy_z_oddychaniem': int(form.cleaned_data['problemy_z_oddychaniem']),
                    'kaszel_chrapanie': int(form.cleaned_data['kaszel_chrapanie']),
                    'za_zimno': int(form.cleaned_data['za_zimno']),
                    'za_cieplo': int(form.cleaned_data['za_cieplo']),
                    'zle_sny': int(form.cleaned_data['zle_sny']),
                    'bol': int(form.cleaned_data['bol']),
                    'inne_powody': int(form.cleaned_data['inne_powody']),
                    'inne_powody_opis': form.cleaned_data['inne_powody_opis'],

                    'jakosc_snu': int(form.cleaned_data['jakosc_snu']),
                    'leki_nasenne': int(form.cleaned_data['leki_nasenne']),
                    'problemy_z_czuwaniem': int(form.cleaned_data['problemy_z_czuwaniem']),
                    'brak_energii': int(form.cleaned_data['brak_energii']),
                }
            )

            return redirect('koniec')

    else:
        form = PittsburghForm()

    return render(
        request,
        'kwestionariusz/pittsburgh.html',
        {
            'form': form,
            'kod_pacjenta': kod_pacjenta,
        }
    )

def koniec(request):
    return render(request, 'kwestionariusz/koniec.html')

@login_required
def panel(request):
    badania = Badanie.objects.select_related('pacjent', 'epworth', 'ipaq', 'pittsburgh')
    filter_form = PanelFilterForm(request.GET or None)

    if filter_form.is_valid():
        cleaned_data = filter_form.cleaned_data
    else:
        cleaned_data = getattr(filter_form, "cleaned_data", {})

    badania = apply_panel_filters(badania, cleaned_data)
    context = build_dashboard_context(badania, filter_form=filter_form)
    return render(request, 'kwestionariusz/panel.html', context)

@login_required
def szczegoly_badania(request, badanie_id):
    badanie = get_object_or_404(
        Badanie.objects.select_related('pacjent', 'epworth', 'ipaq', 'pittsburgh'),
        id=badanie_id
    )

    badanie_view = build_record_view(badanie)

    return render(
        request,
        'kwestionariusz/szczegoly_badania.html',
        {'badanie': badanie_view}
    )

def dane_podstawowe(request):
    badanie_id = request.session.get('badanie_id')
    kod_pacjenta = request.session.get('kod_pacjenta')

    if not badanie_id:
        return redirect('start')

    badanie = Badanie.objects.get(id=badanie_id)

    if request.method == 'POST':
        form = DanePodstawoweForm(request.POST)

        if form.is_valid():
            badanie.etap = form.cleaned_data['etap']
            badanie.plec = form.cleaned_data['plec']
            badanie.wiek = form.cleaned_data['wiek']
            badanie.masa_ciala = form.cleaned_data['masa_ciala']
            badanie.wzrost = form.cleaned_data['wzrost']
            badanie.save()

            return redirect('operacja_bariatryczna')

    else:
        form = DanePodstawoweForm()

    return render(
        request,
        'kwestionariusz/dane_podstawowe.html',
        {
            'form': form,
            'kod_pacjenta': kod_pacjenta,
        }
    )

def operacja_bariatryczna(request):
    badanie_id = request.session.get('badanie_id')
    kod_pacjenta = request.session.get('kod_pacjenta')

    if not badanie_id:
        return redirect('start')

    badanie = Badanie.objects.get(id=badanie_id)

    if request.method == 'POST':
        form = OperacjaBariatrycznaForm(request.POST)

        if form.is_valid():
            badanie.operacja_bariatryczna = form.cleaned_data['operacja_bariatryczna'] == 'tak'
            badanie.data_operacji_bariatrycznej = form.cleaned_data['data_operacji_bariatrycznej']
            badanie.maksymalna_masa_przed_operacja = form.cleaned_data['maksymalna_masa_przed_operacja']
            badanie.save()

            return redirect('cpap_zdrowie')

    else:
        form = OperacjaBariatrycznaForm()

    return render(
        request,
        'kwestionariusz/operacja_bariatryczna.html',
        {
            'form': form,
            'kod_pacjenta': kod_pacjenta,
        }
    )

def cpap_zdrowie(request):
    badanie_id = request.session.get('badanie_id')
    kod_pacjenta = request.session.get('kod_pacjenta')

    if not badanie_id:
        return redirect('start')

    badanie = Badanie.objects.get(id=badanie_id)

    if request.method == 'POST':
        form = CPAPZdrowieForm(request.POST)

        if form.is_valid():
            badanie.cpap = form.cleaned_data['cpap']
            badanie.cpap_czas_stosowania = form.cleaned_data['cpap_czas_stosowania']
            badanie.cpap_godziny_snu = form.cleaned_data['cpap_godziny_snu']
            badanie.cpap_zmiana_cisnienia = form.cleaned_data['cpap_zmiana_cisnienia']
            badanie.choroby = ', '.join(form.cleaned_data['choroby'])
            badanie.fizjoterapia = form.cleaned_data['fizjoterapia']
            badanie.charakter_aktywnosci = form.cleaned_data['charakter_aktywnosci']
            badanie.alkohol_przed_snem = form.cleaned_data['alkohol_przed_snem']
            badanie.palenie = form.cleaned_data['palenie'] == 'tak'
            badanie.pozycja_snu = form.cleaned_data['pozycja_snu']
            badanie.obwod_szyi = form.cleaned_data['obwod_szyi']
            badanie.save()

            return redirect('epworth')

    else:
        form = CPAPZdrowieForm()

    return render(request, 'kwestionariusz/cpap_zdrowie.html', {
        'form': form,
        'kod_pacjenta': kod_pacjenta,
    })
