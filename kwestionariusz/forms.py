from django import forms


class KodPacjentaForm(forms.Form):
    kod = forms.CharField(
        label='Indywidualny kod pacjenta',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'np. ANJA05',
            'class': 'input'
        })
    )

EPWORTH_CHOICES = [
    (0, '0 - zerowe prawdopodobieństwo zaśnięcia'),
    (1, '1 - małe prawdopodobieństwo zaśnięcia'),
    (2, '2 - średnie prawdopodobieństwo zaśnięcia'),
    (3, '3 - duże prawdopodobieństwo zaśnięcia'),
]


class EpworthForm(forms.Form):
    pytanie_1 = forms.ChoiceField(
        label='Siedzenie i czytanie',
        choices=EPWORTH_CHOICES,
        widget=forms.RadioSelect
    )

    pytanie_2 = forms.ChoiceField(
        label='Oglądanie telewizji',
        choices=EPWORTH_CHOICES,
        widget=forms.RadioSelect
    )

    pytanie_3 = forms.ChoiceField(
        label='Bierne siedzenie w miejscach publicznych, np. w teatrze lub na zebraniu',
        choices=EPWORTH_CHOICES,
        widget=forms.RadioSelect
    )

    pytanie_4 = forms.ChoiceField(
        label='Jako pasażer w samochodzie, jadąc przez godzinę bez odpoczynku',
        choices=EPWORTH_CHOICES,
        widget=forms.RadioSelect
    )

    pytanie_5 = forms.ChoiceField(
        label='Leżenie i odpoczywanie po południu, jeśli okoliczności na to pozwalają',
        choices=EPWORTH_CHOICES,
        widget=forms.RadioSelect
    )

    pytanie_6 = forms.ChoiceField(
        label='W czasie rozmowy, siedząc',
        choices=EPWORTH_CHOICES,
        widget=forms.RadioSelect
    )

    pytanie_7 = forms.ChoiceField(
        label='Spokojne siedzenie po obiedzie bez alkoholu',
        choices=EPWORTH_CHOICES,
        widget=forms.RadioSelect
    )

    pytanie_8 = forms.ChoiceField(
        label='W samochodzie, podczas kilkuminutowego postoju w korku lub na czerwonym świetle',
        choices=EPWORTH_CHOICES,
        widget=forms.RadioSelect
    )

TAK_NIE_CHOICES = [
    (False, 'Nie'),
    (True, 'Tak'),
]


class IPAQForm(forms.Form):
    szpital = forms.ChoiceField(
        label='Czy w ciągu ostatnich 7 dni przebywałeś/aś w szpitalu?',
        choices=TAK_NIE_CHOICES,
        widget=forms.RadioSelect
    )

    choroba = forms.ChoiceField(
        label='Czy w ciągu ostatnich 7 dni byłeś/aś chory/a?',
        choices=TAK_NIE_CHOICES,
        widget=forms.RadioSelect
    )

    rehabilitacja = forms.ChoiceField(
        label='Czy w ciągu ostatnich 7 dni uczestniczyłeś/aś w rehabilitacji?',
        choices=TAK_NIE_CHOICES,
        widget=forms.RadioSelect
    )

    urlop = forms.ChoiceField(
        label='Czy w ciągu ostatnich 7 dni byłeś/aś na urlopie?',
        choices=TAK_NIE_CHOICES,
        widget=forms.RadioSelect
    )

    rekonwalescencja = forms.ChoiceField(
        label='Czy w ciągu ostatnich 7 dni byłeś/aś w okresie rekonwalescencji?',
        choices=TAK_NIE_CHOICES,
        widget=forms.RadioSelect
    )

    ciaza = forms.ChoiceField(
        label='Czy w ciągu ostatnich 7 dni byłaś w ciąży?',
        choices=TAK_NIE_CHOICES,
        widget=forms.RadioSelect
    )

    intensywne_dni = forms.IntegerField(
        label='1. W ciągu ostatnich 7 dni, przez ile dni wykonywałeś/aś intensywny wysiłek fizyczny, taki jak dźwiganie ciężkich przedmiotów, kopanie ziemi, aerobik, szybka jazda rowerem?',
        min_value=0,
        max_value=7,
        widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Liczba dni'})
    )

    intensywne_minuty = forms.IntegerField(
        label='2. Ile czasu przeciętnie poświęcałeś/aś na intensywny wysiłek fizyczny w jednym takim dniu?',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Liczba minut dziennie'})
    )

    umiarkowane_dni = forms.IntegerField(
        label='3. W ciągu ostatnich 7 dni, przez ile dni wykonywałeś/aś umiarkowany wysiłek fizyczny, taki jak noszenie lekkich przedmiotów, jazda rowerem w zwykłym tempie lub gra podwójna w tenisa?',
        min_value=0,
        max_value=7,
        widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Liczba dni'})
    )

    umiarkowane_minuty = forms.IntegerField(
        label='4. Ile czasu przeciętnie poświęcałeś/aś na umiarkowany wysiłek fizyczny w jednym takim dniu?',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Liczba minut dziennie'})
    )

    chodzenie_dni = forms.IntegerField(
        label='5. W ciągu ostatnich 7 dni, przez ile dni chodziłeś/aś co najmniej 10 minut bez przerwy?',
        min_value=0,
        max_value=7,
        widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Liczba dni'})
    )

    chodzenie_minuty = forms.IntegerField(
        label='6. Ile czasu przeciętnie poświęcałeś/aś na chodzenie w jednym takim dniu?',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Liczba minut dziennie'})
    )

    siedzenie_minuty_dziennie = forms.IntegerField(
        label='7. Ile czasu spędziłeś/aś siedząc w typowym dniu roboczym w ciągu ostatnich 7 dni?',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Liczba minut dziennie'})
    )

PITTSBURGH_CZESTOTLIWOSC = [
    (0, 'Ani razu w ciągu ostatniego miesiąca'),
    (1, 'Rzadziej niż raz w tygodniu'),
    (2, 'Raz lub dwa razy w tygodniu'),
    (3, 'Trzy lub więcej razy w tygodniu'),
]


class PittsburghForm(forms.Form):
    godzina_polozenia = forms.TimeField(
        label='1. O której godzinie zwykle kładł(a) się Pan/Pani spać wieczorem?',
        widget=forms.TimeInput(attrs={'class': 'input', 'type': 'time'})
    )

    czas_zasypiania_minuty = forms.IntegerField(
        label='2. Ile minut zwykle zajmowało Panu/Pani zaśnięcie każdej nocy?',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Liczba minut'})
    )

    godzina_wstawania = forms.TimeField(
        label='3. O której godzinie zwykle wstawał(a) Pan/Pani rano?',
        widget=forms.TimeInput(attrs={'class': 'input', 'type': 'time'})
    )

    godziny_snu = forms.FloatField(
        label='4. Ile godzin rzeczywistego snu miał(a) Pan/Pani przeciętnie w ciągu nocy?',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'input', 'step': '0.5', 'placeholder': 'Np. 7.5'})
    )

    nie_zasnal_30_min = forms.ChoiceField(
        label='5a. Nie mógł/mogła Pan/Pani zasnąć w ciągu 30 minut',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    pobudka_w_nocy = forms.ChoiceField(
        label='5b. Budził(a) się Pan/Pani w środku nocy lub wcześnie rano',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    toaleta = forms.ChoiceField(
        label='5c. Musiał(a) Pan/Pani wstać, aby skorzystać z toalety',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    problemy_z_oddychaniem = forms.ChoiceField(
        label='5d. Miał(a) Pan/Pani trudności z oddychaniem',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    kaszel_chrapanie = forms.ChoiceField(
        label='5e. Kaszlał(a) Pan/Pani lub głośno chrapał(a)',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    za_zimno = forms.ChoiceField(
        label='5f. Było Panu/Pani zbyt zimno',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    za_cieplo = forms.ChoiceField(
        label='5g. Było Panu/Pani zbyt gorąco',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    zle_sny = forms.ChoiceField(
        label='5h. Miał(a) Pan/Pani złe sny',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    bol = forms.ChoiceField(
        label='5i. Odczuwał(a) Pan/Pani ból',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    inne_powody = forms.ChoiceField(
        label='5j. Inne powody zakłócające sen',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    inne_powody_opis = forms.CharField(
        label='Jeśli zaznaczono inne powody, proszę je opisać',
        required=False,
        widget=forms.Textarea(attrs={'class': 'input', 'rows': 3})
    )

    jakosc_snu = forms.ChoiceField(
        label='6. Jak ocenił(a)by Pan/Pani ogólną jakość swojego snu w ciągu ostatniego miesiąca?',
        choices=[
            (0, 'Bardzo dobra'),
            (1, 'Raczej dobra'),
            (2, 'Raczej zła'),
            (3, 'Bardzo zła'),
        ],
        widget=forms.RadioSelect
    )

    leki_nasenne = forms.ChoiceField(
        label='7. Jak często zażywał(a) Pan/Pani leki nasenne?',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    problemy_z_czuwaniem = forms.ChoiceField(
        label='8. Jak często miał(a) Pan/Pani trudności z utrzymaniem czuwania podczas prowadzenia pojazdu, jedzenia posiłków lub uczestniczenia w spotkaniach?',
        choices=PITTSBURGH_CZESTOTLIWOSC,
        widget=forms.RadioSelect
    )

    brak_energii = forms.ChoiceField(
        label='9. Jak dużym problemem było dla Pana/Pani utrzymanie wystarczającej energii do wykonywania codziennych czynności?',
        choices=[
            (0, 'Żaden problem'),
            (1, 'Bardzo mały problem'),
            (2, 'Dość duży problem'),
            (3, 'Bardzo duży problem'),
        ],
        widget=forms.RadioSelect
    )

class DaneBadaniaForm(forms.Form):
    etap = forms.ChoiceField(
        label='Na którym etapie badania się Pan/Pani obecnie znajduje?',
        choices=[
            ('0', 'Etap 0 (Początek obserwacji)'),
            ('1', 'Etap I (6 miesięcy od pierwszego badania)'),
            ('2', 'Etap II (12 miesięcy od pierwszego badania)'),
        ],
        widget=forms.RadioSelect
    )

    plec = forms.ChoiceField(
        label='Płeć',
        choices=[
            ('kobieta', 'Kobieta'),
            ('mezczyzna', 'Mężczyzna'),
        ],
        widget=forms.RadioSelect
    )

    wiek = forms.IntegerField(label='Wiek', min_value=0, widget=forms.NumberInput(attrs={'class': 'input'}))
    masa_ciala = forms.FloatField(label='Aktualna masa ciała', min_value=0, widget=forms.NumberInput(attrs={'class': 'input', 'step': '0.1'}))
    wzrost = forms.FloatField(label='Wzrost (w cm)', min_value=0, widget=forms.NumberInput(attrs={'class': 'input', 'step': '0.1'}))

    operacja_bariatryczna = forms.ChoiceField(
        label='Czy przeszedł(szła) Pan/Pani operację bariatryczną?',
        choices=[
            ('tak', 'Tak'),
            ('nie', 'Nie, nigdy nie miałem(am) operacji bariatrycznej'),
        ],
        widget=forms.RadioSelect
    )

    data_operacji_bariatrycznej = forms.CharField(
        label='Data wykonania operacji bariatrycznej (miesiąc i rok)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'np. 05.2024'})
    )

    maksymalna_masa_przed_operacja = forms.FloatField(
        label='Maksymalna masa ciała PRZED operacją bariatryczną (kg)',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'input', 'step': '0.1'})
    )
    cpap = forms.ChoiceField(
        label='Czy korzysta Pan/Pani z aparatu CPAP?',
        choices=[
            ('regularnie', 'Tak, używam regularnie do teraz'),
            ('w_przeszlosci', 'Używałem(am) w przeszłości, ale po operacji bariatrycznej lekarz zalecił odstawienie aparatu'),
            ('nigdy', 'Nie, nigdy nie używałem(am) aparatu CPAP'),
        ],
        widget=forms.RadioSelect
    )

    cpap_czas_stosowania = forms.CharField(
        label='Od ilu miesięcy/lat łącznie stosuje Pan/Pani aparat CPAP?',
        required=False,
        widget=forms.TextInput(attrs={'class': 'input'})
    )

    cpap_godziny_snu = forms.ChoiceField(
        label='Ile średnio godzin w ciągu nocy śpi Pan/Pani z użytkowaniem CPAP w ostatnim czasie?',
        choices=[
            ('mniej_4', 'Mniej niż 4 godziny'),
            ('4_6', 'Od 4 do 6 godzin'),
            ('powyzej_6', 'Powyżej 6 godzin'),
        ],
        required=False,
        widget=forms.RadioSelect
    )

    cpap_zmiana_cisnienia = forms.ChoiceField(
        label='Czy lekarz zmienił ciśnienie w aparacie CPAP?',
        choices=[
            ('zmniejszone', 'Tak, ciśnienie zostało zmniejszone'),
            ('odstawiony', 'Tak, aparat został całkowicie odstawiony za zgodą lekarza'),
            ('bez_zmian', 'Nie, parametry aparatu są bez zmian'),
            ('nie_wiem', 'Nie wiem / Nie pamiętam'),
        ],
        required=False,
        widget=forms.RadioSelect
    )

    choroby = forms.MultipleChoiceField(
        label='Na jakie inne schorzenia Pan/Pani choruje?',
        choices=[
            ('nadcisnienie', 'Nadciśnienie tętnicze'),
            ('cukrzyca', 'Cukrzyca typu 2 lub insulinooporność'),
            ('stawy_kregoslup', 'Zwyrodnienia stawów lub kręgosłupa'),
            ('astma_pochp', 'Astma / POChP'),
            ('brak', 'Żadne z powyższych'),
            ('inne', 'Inne'),
        ],
        widget=forms.CheckboxSelectMultiple
    )

class DanePodstawoweForm(forms.Form):
    etap = forms.ChoiceField(
        label='Na którym etapie badania się Pan/Pani obecnie znajduje?',
        choices=[
            ('0', 'Etap 0 (Początek obserwacji)'),
            ('1', 'Etap I (6 miesięcy od pierwszego badania)'),
            ('2', 'Etap II (12 miesięcy od pierwszego badania)'),
        ],
        widget=forms.RadioSelect
    )

    plec = forms.ChoiceField(
        label='Płeć',
        choices=[
            ('kobieta', 'Kobieta'),
            ('mezczyzna', 'Mężczyzna'),
        ],
        widget=forms.RadioSelect
    )

    wiek = forms.IntegerField(
        label='Wiek',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'input'})
    )

    masa_ciala = forms.FloatField(
        label='Aktualna masa ciała (kg)',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'input', 'step': '0.1'})
    )

    wzrost = forms.FloatField(
        label='Wzrost (cm)',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'input', 'step': '0.1'})
    )

class OperacjaBariatrycznaForm(forms.Form):
    operacja_bariatryczna = forms.ChoiceField(
        label='Czy przeszedł(szła) Pan/Pani operację bariatryczną?',
        choices=[
            ('tak', 'Tak'),
            ('nie', 'Nie, nigdy nie miałem(am) operacji bariatrycznej'),
        ],
        widget=forms.RadioSelect
    )

    data_operacji_bariatrycznej = forms.CharField(
        label='Data wykonania operacji bariatrycznej (miesiąc i rok)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'np. 05.2024'
        })
    )

    maksymalna_masa_przed_operacja = forms.FloatField(
        label='Jaka była Pana/Pani maksymalna masa ciała PRZED operacją bariatryczną? (kg)',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'input',
            'step': '0.1'
        })
    )

class CPAPZdrowieForm(forms.Form):
    cpap = forms.ChoiceField(
        label='Czy korzysta Pan/Pani z aparatu CPAP?',
        choices=[
            ('regularnie', 'Tak, używam regularnie do teraz'),
            ('w_przeszlosci', 'Używałem(am) w przeszłości, ale po operacji bariatrycznej lekarz zalecił odstawienie aparatu'),
            ('nigdy', 'Nie, nigdy nie używałem(am) aparatu CPAP'),
        ],
        widget=forms.RadioSelect
    )

    cpap_czas_stosowania = forms.CharField(
        label='Od ilu miesięcy/lat łącznie stosuje Pan/Pani aparat CPAP?',
        required=False,
        widget=forms.TextInput(attrs={'class': 'input'})
    )
    cpap_godziny_snu = forms.ChoiceField(
        label='Ile średnio godzin w ciągu nocy śpi Pan/Pani z użytkowaniem CPAP w ostatnim czasie?',
        choices=[
            ('mniej_4', 'Mniej niż 4 godziny'),
            ('4_6', 'Od 4 do 6 godzin'),
            ('powyzej_6', 'Powyżej 6 godzin'),
        ],
        required=False,
        widget=forms.RadioSelect
    )

    cpap_zmiana_cisnienia = forms.ChoiceField(
        label='Czy w ciągu ostatnich miesięcy lekarz zmienił ciśnienie w aparacie CPAP?',
        choices=[
            ('zmniejszone', 'Tak, ciśnienie zostało zmniejszone'),
            ('odstawiony', 'Tak, aparat został całkowicie odstawiony za zgodą lekarza'),
            ('bez_zmian', 'Nie, parametry aparatu są bez zmian'),
            ('nie_wiem', 'Nie wiem / Nie pamiętam'),
        ],
        required=False,
        widget=forms.RadioSelect
    )

    choroby = forms.MultipleChoiceField(
        label='Na jakie inne schorzenia Pan/Pani choruje? (Zaznacz wszystkie pasujące)',
        choices=[
            ('nadcisnienie', 'Nadciśnienie tętnicze'),
            ('cukrzyca', 'Cukrzyca typu 2 lub insulinooporność'),
            ('stawy_kregoslup', 'Zwyrodnienia stawów lub kręgosłupa'),
            ('astma_pochp', 'Astma / POChP'),
            ('brak', 'Żadne z powyższych'),
            ('inne', 'Inne'),
        ],
        widget=forms.CheckboxSelectMultiple
    )

    fizjoterapia = forms.ChoiceField(
        label='Czy w okresie objętym tym etapem badania korzystał(a) Pan/Pani z pomocy fizjoterapeuty, rehabilitanta lub trenera medycznego?',
        choices=[
            ('regularnie', 'Tak, regularnie (minimum raz w tygodniu)'),
            ('sporadycznie', 'Tak, sporadycznie (kilka razy w tym okresie)'),
            ('nie', 'Nie, w ogóle nie korzystałem(am)'),
        ],
        widget=forms.RadioSelect
    )

    charakter_aktywnosci = forms.ChoiceField(
        label='Jaki jest główny charakter Pana/Pani codziennej aktywności?',
        choices=[
            ('siedzacy', 'Głównie siedzący'),
            ('mieszany', 'Mieszany'),
            ('ciezki_fizyczny', 'Ciężki fizyczny'),
            ('nie_pracuje', 'Nie pracuję / Jestem na emeryturze lub rencie'),
        ],
        widget=forms.RadioSelect
    )

    alkohol_przed_snem = forms.ChoiceField(
        label='Czy zdarza się Panu/Pani spożywać alkohol w ciągu 2-3 godzin przed pójściem spać?',
        choices=[
            ('czesto', 'Często'),
            ('rzadko', 'Rzadko'),
            ('nigdy', 'Nigdy'),
        ],
        widget=forms.RadioSelect
    )

    palenie = forms.ChoiceField(
        label='Czy pali Pan/Pani wyroby tytoniowe lub e-papierosy?',
        choices=[
            ('tak', 'Tak'),
            ('nie', 'Nie'),
        ],
        widget=forms.RadioSelect
    )

    pozycja_snu = forms.ChoiceField(
        label='W jakiej pozycji najczęściej Pan/Pani sypia?',
        choices=[
            ('plecy', 'Głównie na plecach'),
            ('bok_brzuch', 'Głównie na boku lub na brzuchu'),
            ('zmienna', 'Trudno powiedzieć / Często zmieniam pozycję'),
        ],
        widget=forms.RadioSelect
    )

    obwod_szyi = forms.FloatField(
        label='Jaki jest Pana/Pani obwód szyi? Wynik podaj w centymetrach (cm), z dokładnością do 0,5 cm.',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'input', 'step': '0.5'})
    )