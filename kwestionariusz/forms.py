from django import forms


def _build_form_class(class_name, field_definitions):
    attrs = {"__module__": __name__}
    for field_name, field in field_definitions:
        attrs[field_name] = field
    return type(class_name, (forms.Form,), attrs)


def _radio_choice_field(label, choices, required=True, attrs=None):
    widget_attrs = {"class": "input"}
    if attrs:
        widget_attrs.update(attrs)
    return forms.ChoiceField(
        label=label,
        choices=choices,
        required=required,
        widget=forms.RadioSelect(attrs=widget_attrs) if attrs else forms.RadioSelect,
    )


def _select_field(label, choices, required=True):
    return forms.ChoiceField(
        label=label,
        choices=choices,
        required=required,
        widget=forms.Select(attrs={"class": "input"}),
    )


def _text_field(label, required=True, placeholder="", rows=None):
    attrs = {"class": "input"}
    if placeholder:
        attrs["placeholder"] = placeholder
    if rows is not None:
        attrs["rows"] = rows
    widget = forms.Textarea(attrs=attrs) if rows is not None else forms.TextInput(attrs=attrs)
    return forms.CharField(label=label, required=required, widget=widget)


TAK_NIE_CHOICES = [
    (False, "Nie"),
    (True, "Tak"),
]


KOD_PACJENTA_FIELD = forms.CharField(
    label="Indywidualny kod pacjenta",
    max_length=20,
    widget=forms.TextInput(attrs={
        "placeholder": "np. ANJA05",
        "class": "input",
    }),
)


KodPacjentaForm = _build_form_class("KodPacjentaForm", [("kod", KOD_PACJENTA_FIELD)])


EPWORTH_CHOICES = [
    (0, "0 - zerowe prawdopodobieństwo zaśnięcia"),
    (1, "1 - małe prawdopodobieństwo zaśnięcia"),
    (2, "2 - średnie prawdopodobieństwo zaśnięcia"),
    (3, "3 - duże prawdopodobieństwo zaśnięcia"),
]

EPWORTH_FIELD_DEFINITIONS = [
    ("pytanie_1", forms.ChoiceField(label="Siedzenie i czytanie", choices=EPWORTH_CHOICES, widget=forms.RadioSelect)),
    ("pytanie_2", forms.ChoiceField(label="Oglądanie telewizji", choices=EPWORTH_CHOICES, widget=forms.RadioSelect)),
    ("pytanie_3", forms.ChoiceField(label="Bierne siedzenie w miejscach publicznych, np. w teatrze lub na zebraniu", choices=EPWORTH_CHOICES, widget=forms.RadioSelect)),
    ("pytanie_4", forms.ChoiceField(label="Jako pasażer w samochodzie, jadąc przez godzinę bez odpoczynku", choices=EPWORTH_CHOICES, widget=forms.RadioSelect)),
    ("pytanie_5", forms.ChoiceField(label="Leżenie i odpoczywanie po południu, jeśli okoliczności na to pozwalają", choices=EPWORTH_CHOICES, widget=forms.RadioSelect)),
    ("pytanie_6", forms.ChoiceField(label="W czasie rozmowy, siedząc", choices=EPWORTH_CHOICES, widget=forms.RadioSelect)),
    ("pytanie_7", forms.ChoiceField(label="Spokojne siedzenie po obiedzie bez alkoholu", choices=EPWORTH_CHOICES, widget=forms.RadioSelect)),
    ("pytanie_8", forms.ChoiceField(label="W samochodzie, podczas kilkuminutowego postoju w korku lub na czerwonym świetle", choices=EPWORTH_CHOICES, widget=forms.RadioSelect)),
]

EpworthForm = _build_form_class("EpworthForm", EPWORTH_FIELD_DEFINITIONS)


IPAQ_FIELD_DEFINITIONS = [
    ("szpital", forms.ChoiceField(label="Czy w ciągu ostatnich 7 dni przebywałeś/aś w szpitalu?", choices=TAK_NIE_CHOICES, widget=forms.RadioSelect)),
    ("choroba", forms.ChoiceField(label="Czy w ciągu ostatnich 7 dni byłeś/aś chory/a?", choices=TAK_NIE_CHOICES, widget=forms.RadioSelect)),
    ("rehabilitacja", forms.ChoiceField(label="Czy w ciągu ostatnich 7 dni uczestniczyłeś/aś w rehabilitacji?", choices=TAK_NIE_CHOICES, widget=forms.RadioSelect)),
    ("urlop", forms.ChoiceField(label="Czy w ciągu ostatnich 7 dni byłeś/aś na urlopie?", choices=TAK_NIE_CHOICES, widget=forms.RadioSelect)),
    ("rekonwalescencja", forms.ChoiceField(label="Czy w ciągu ostatnich 7 dni byłeś/aś w okresie rekonwalescencji?", choices=TAK_NIE_CHOICES, widget=forms.RadioSelect)),
    ("ciaza", forms.ChoiceField(label="Czy w ciągu ostatnich 7 dni byłaś w ciąży?", choices=TAK_NIE_CHOICES, widget=forms.RadioSelect)),
    ("intensywne_dni", forms.IntegerField(label="1. Przez ile dni wykonywałeś/aś intensywny wysiłek fizyczny?", min_value=0, max_value=7, widget=forms.NumberInput(attrs={"class": "input", "placeholder": "Liczba dni"}))),
    ("intensywne_minuty", forms.IntegerField(label="2. Ile minut średnio poświęcałeś/aś na intensywny wysiłek fizyczny w jednym takim dniu?", min_value=0, widget=forms.NumberInput(attrs={"class": "input", "placeholder": "Liczba minut dziennie"}))),
    ("umiarkowane_dni", forms.IntegerField(label="3. Przez ile dni wykonywałeś/aś umiarkowany wysiłek fizyczny?", min_value=0, max_value=7, widget=forms.NumberInput(attrs={"class": "input", "placeholder": "Liczba dni"}))),
    ("umiarkowane_minuty", forms.IntegerField(label="4. Ile minut średnio poświęcałeś/aś na umiarkowany wysiłek fizyczny w jednym takim dniu?", min_value=0, widget=forms.NumberInput(attrs={"class": "input", "placeholder": "Liczba minut dziennie"}))),
    ("chodzenie_dni", forms.IntegerField(label="5. Przez ile dni chodziłeś/aś co najmniej 10 minut bez przerwy?", min_value=0, max_value=7, widget=forms.NumberInput(attrs={"class": "input", "placeholder": "Liczba dni"}))),
    ("chodzenie_minuty", forms.IntegerField(label="6. Ile minut średnio poświęcałeś/aś na chodzenie w jednym takim dniu?", min_value=0, widget=forms.NumberInput(attrs={"class": "input", "placeholder": "Liczba minut dziennie"}))),
    ("siedzenie_minuty_dziennie", forms.IntegerField(label="7. Ile czasu spędziłeś/aś siedząc w typowym dniu roboczym w ciągu ostatnich 7 dni?", min_value=0, widget=forms.NumberInput(attrs={"class": "input", "placeholder": "Liczba minut dziennie"}))),
]

IPAQForm = _build_form_class("IPAQForm", IPAQ_FIELD_DEFINITIONS)


FOSQ_DIFFICULTY_CHOICES = [
    (4, "4 - brak trudności"),
    (3, "3 - małe trudności"),
    (2, "2 - umiarkowane trudności"),
    (1, "1 - duże trudności"),
    (0, "0 - nie dotyczy / nie wykonuję tej czynności"),
]

FOSQ_ACTIVITY_CHOICES = [
    (1, "1 - bardzo niski"),
    (2, "2 - niski"),
    (3, "3 - średni"),
    (4, "4 - wysoki"),
]

FOSQ_QUESTION_DEFINITIONS = [
    ("pytanie_1", "Czy ogólnie masz trudności z koncentracją na wykonywanych czynnościach, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "produktywność"),
    ("pytanie_2", "Czy ogólnie masz trudności z zapamiętywaniem różnych rzeczy, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "produktywność"),
    ("pytanie_3", "Czy masz trudności z dokończeniem posiłku, ponieważ robisz się senny/senna lub zmęczony/zmęczona?", "difficulty", "produktywność"),
    ("pytanie_4", "Czy masz trudności z zajmowaniem się hobby, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "produktywność"),
    ("pytanie_5", "Czy masz trudności z wykonywaniem prac domowych, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "aktywność"),
    ("pytanie_6", "Czy masz trudności z prowadzeniem pojazdu mechanicznego na krótkich dystansach, ponieważ robisz się senny/senna lub zmęczony/zmęczona?", "difficulty", "czujność"),
    ("pytanie_7", "Czy masz trudności z prowadzeniem pojazdu mechanicznego na długich dystansach, ponieważ robisz się senny/senna lub zmęczony/zmęczona?", "difficulty", "czujność"),
    ("pytanie_8", "Czy masz trudności z załatwianiem spraw, ponieważ jesteś zbyt senny/senna lub zmęczony/zmęczona, aby prowadzić samochód albo korzystać z transportu publicznego?", "difficulty", "produktywność"),
    ("pytanie_9", "Czy masz trudności z zajmowaniem się sprawami finansowymi i wypełnianiem dokumentów, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "produktywność"),
    ("pytanie_10", "Czy masz trudności z wykonywaniem pracy zawodowej lub wolontariatu, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "produktywność"),
    ("pytanie_11", "Czy masz trudności z prowadzeniem rozmowy telefonicznej, ponieważ robisz się senny/senna lub zmęczony/zmęczona?", "difficulty", "produktywność"),
    ("pytanie_12", "Czy masz trudności z odwiedzaniem rodziny/znajomych w swoim domu, ponieważ robisz się senny/senna lub zmęczony/zmęczona?", "difficulty", "kontakty_spoleczne"),
    ("pytanie_13", "Czy masz trudności z odwiedzaniem rodziny/znajomych w ich domu, ponieważ robisz się senny/senna lub zmęczony/zmęczona?", "difficulty", "kontakty_spoleczne"),
    ("pytanie_14", "Czy masz trudności z robieniem rzeczy dla rodziny lub znajomych, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "aktywność"),
    ("pytanie_15", "Czy masz trudności z ćwiczeniami lub udziałem w aktywności sportowej, ponieważ jesteś zbyt senny/senna lub zmęczony/zmęczona?", "difficulty", "aktywność"),
    ("pytanie_16", "Czy masz trudności z oglądaniem filmu lub nagrania wideo, ponieważ robisz się senny/senna lub zmęczony/zmęczona?", "difficulty", "aktywność"),
    ("pytanie_17", "Czy masz trudności z korzystaniem z teatru lub wykładu, ponieważ robisz się senny/senna lub zmęczony/zmęczona?", "difficulty", "czujność"),
    ("pytanie_18", "Czy masz trudności z korzystaniem z koncertu, ponieważ robisz się senny/senna lub zmęczony/zmęczona?", "difficulty", "czujność"),
    ("pytanie_19", "Czy masz trudności z oglądaniem telewizji, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "czujność"),
    ("pytanie_20", "Czy masz trudności z uczestniczeniem w nabożeństwach, spotkaniach albo grupie/klubie, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "czujność"),
    ("pytanie_21", "Czy masz trudności z byciem tak aktywnym/aktywną wieczorem, jak chcesz, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "aktywność"),
    ("pytanie_22", "Czy masz trudności z byciem tak aktywnym/aktywną rano, jak chcesz, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "aktywność"),
    ("pytanie_23", "Czy masz trudności z byciem tak aktywnym/aktywną po południu, jak chcesz, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "aktywność"),
    ("pytanie_24", "Czy masz trudności z dotrzymywaniem tempa osobom w swoim wieku, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "aktywność"),
    ("pytanie_25", "Czy Twoja relacja intymna lub seksualna została pogorszona, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "intymnosc"),
    ("pytanie_26", "Czy Twoja ochota na intymność lub seks została zmniejszona, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "intymnosc"),
    ("pytanie_27", "Czy Twoja zdolność do podniecenia seksualnego została pogorszona, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "intymnosc"),
    ("pytanie_28", "Czy Twoja zdolność do osiągnięcia orgazmu została pogorszona, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "intymnosc"),
    ("pytanie_29", "Czy Twoje relacje z rodziną lub współpracownikami zostały pogorszone, ponieważ jesteś senny/senna lub zmęczony/zmęczona?", "difficulty", "intymnosc"),
    ("pytanie_30", "Jak oceniasz swój ogólny poziom aktywności?", "activity", "aktywność"),
]

FOSQ_SECTION_DEFINITIONS = [
    ("produktywność", "Produktywność i zadania", [field_name for field_name, _label, _scale, section in FOSQ_QUESTION_DEFINITIONS if section == "produktywność"]),
    ("kontakty_spoleczne", "Kontakty społeczne", [field_name for field_name, _label, _scale, section in FOSQ_QUESTION_DEFINITIONS if section == "kontakty_spoleczne"]),
    ("aktywność", "Aktywność dnia codziennego", [field_name for field_name, _label, _scale, section in FOSQ_QUESTION_DEFINITIONS if section == "aktywność"]),
    ("czujność", "Czujność i prowadzenie pojazdów", [field_name for field_name, _label, _scale, section in FOSQ_QUESTION_DEFINITIONS if section == "czujność"]),
    ("intymnosc", "Intymność i relacje", [field_name for field_name, _label, _scale, section in FOSQ_QUESTION_DEFINITIONS if section == "intymnosc"]),
]

FOSQ_FIELD_DEFINITIONS = []
for field_name, label, scale, _section in FOSQ_QUESTION_DEFINITIONS:
    FOSQ_FIELD_DEFINITIONS.append(
        (
            field_name,
            forms.ChoiceField(
                label=label,
                choices=FOSQ_ACTIVITY_CHOICES if scale == "activity" else FOSQ_DIFFICULTY_CHOICES,
                widget=forms.RadioSelect,
            ),
        )
    )

FOSQForm = _build_form_class("FOSQForm", FOSQ_FIELD_DEFINITIONS)
PittsburghForm = FOSQForm


ETAP_CHOICES = [
    ("0", "Etap 0 (Początek obserwacji)"),
    ("1", "Etap I (6 miesięcy od pierwszego badania)"),
    ("2", "Etap II (12 miesięcy od pierwszego badania)"),
]

PLEC_CHOICES = [
    ("kobieta", "Kobieta"),
    ("mezczyzna", "Mężczyzna"),
]

OPERACJA_CHOICES = [
    ("tak", "Tak"),
    ("nie", "Nie, nigdy nie miałem(am) operacji bariatrycznej"),
]

CPAP_CHOICES = [
    ("regularnie", "Tak, używam regularnie do teraz"),
    ("w_przeszlosci", "Używałem(am) w przeszłości, ale po operacji bariatrycznej lekarz zalecił odstawienie aparatu"),
    ("nigdy", "Nie, nigdy nie używałem(am) aparatu CPAP"),
]

CPAP_GODZINY_CHOICES = [
    ("mniej_4", "Mniej niż 4 godziny"),
    ("4_6", "Od 4 do 6 godzin"),
    ("powyzej_6", "Powyżej 6 godzin"),
]

CPAP_ZMIANA_CHOICES = [
    ("zmniejszone", "Tak, ciśnienie zostało zmniejszone"),
    ("odstawiony", "Tak, aparat został całkowicie odstawiony za zgodą lekarza"),
    ("bez_zmian", "Nie, parametry aparatu są bez zmian"),
    ("nie_wiem", "Nie wiem / Nie pamiętam"),
]

CHOROBY_CHOICES = [
    ("nadcisnienie", "Nadciśnienie tętnicze"),
    ("cukrzyca", "Cukrzyca typu 2 lub insulinooporność"),
    ("stawy_kregoslup", "Zwyrodnienia stawów lub kręgosłupa"),
    ("astma_pochp", "Astma / POChP"),
    ("brak", "Żadne z powyższych"),
    ("inne", "Inne"),
]

FIZJOTERAPIA_CHOICES = [
    ("regularnie", "Tak, regularnie (minimum raz w tygodniu)"),
    ("sporadycznie", "Tak, sporadycznie (kilka razy w tym okresie)"),
    ("nie", "Nie, w ogóle nie korzystałem(am)"),
]

CHARAKTER_AKTYWNOSCI_CHOICES = [
    ("siedzacy", "Głównie siedzący"),
    ("mieszany", "Mieszany"),
    ("ciezki_fizyczny", "Ciężki fizyczny"),
    ("nie_pracuje", "Nie pracuję / Jestem na emeryturze lub rencie"),
]

ALKOHOL_PRZED_SNEM_CHOICES = [
    ("czesto", "Często"),
    ("rzadko", "Rzadko"),
    ("nigdy", "Nigdy"),
]

PALENIE_CHOICES = [
    ("tak", "Tak"),
    ("nie", "Nie"),
]

POZYCJA_SNU_CHOICES = [
    ("plecy", "Głównie na plecach"),
    ("bok_brzuch", "Głównie na boku lub na brzuchu"),
    ("zmienna", "Trudno powiedzieć / Często zmieniam pozycję"),
]


class DaneBadaniaForm(forms.Form):
    etap = forms.ChoiceField(label="Na którym etapie badania się Pan/Pani obecnie znajduje?", choices=ETAP_CHOICES, widget=forms.RadioSelect)
    plec = forms.ChoiceField(label="Płeć", choices=PLEC_CHOICES, widget=forms.RadioSelect)
    wiek = forms.IntegerField(label="Wiek", min_value=0, widget=forms.NumberInput(attrs={"class": "input"}))
    masa_ciala = forms.FloatField(label="Aktualna masa ciała", min_value=0, widget=forms.NumberInput(attrs={"class": "input", "step": "0.1"}))
    wzrost = forms.FloatField(label="Wzrost (w cm)", min_value=0, widget=forms.NumberInput(attrs={"class": "input", "step": "0.1"}))


class DanePodstawoweForm(forms.Form):
    etap = forms.ChoiceField(label="Na którym etapie badania się Pan/Pani obecnie znajduje?", choices=ETAP_CHOICES, widget=forms.RadioSelect)
    plec = forms.ChoiceField(label="Płeć", choices=PLEC_CHOICES, widget=forms.RadioSelect)
    wiek = forms.IntegerField(label="Wiek", min_value=1, widget=forms.NumberInput(attrs={"class": "input"}))
    masa_ciala = forms.FloatField(label="Aktualna masa ciała (kg)", min_value=1, widget=forms.NumberInput(attrs={"class": "input", "step": "0.1"}))
    wzrost = forms.FloatField(label="Wzrost (cm)", min_value=1, widget=forms.NumberInput(attrs={"class": "input", "step": "0.1"}))


class OperacjaBariatrycznaForm(forms.Form):
    operacja_bariatryczna = forms.ChoiceField(label="Czy przeszedł(szła) Pan/Pani operację bariatryczną?", choices=OPERACJA_CHOICES, widget=forms.RadioSelect)
    data_operacji_bariatrycznej = forms.CharField(
        label="Data wykonania operacji bariatrycznej (miesiąc i rok)",
        required=False,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "np. 05.2024"}),
    )
    maksymalna_masa_przed_operacja = forms.FloatField(
        label="Jaka była Pana/Pani maksymalna masa ciała PRZED operacją bariatryczną? (kg)",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "input", "step": "0.1"}),
    )


class CPAPZdrowieForm(forms.Form):
    cpap = forms.ChoiceField(label="Czy korzysta Pan/Pani z aparatu CPAP?", choices=CPAP_CHOICES, widget=forms.RadioSelect)
    cpap_czas_stosowania = forms.CharField(
        label="Od ilu miesięcy/lat łącznie stosuje Pan/Pani aparat CPAP?",
        required=False,
        widget=forms.TextInput(attrs={"class": "input"}),
    )
    cpap_godziny_snu = forms.ChoiceField(
        label="Ile średnio godzin w ciągu nocy śpi Pan/Pani z użytkowaniem CPAP w ostatnim czasie?",
        choices=CPAP_GODZINY_CHOICES,
        required=False,
        widget=forms.RadioSelect,
    )
    cpap_zmiana_cisnienia = forms.ChoiceField(
        label="Czy w ciągu ostatnich miesięcy lekarz zmienił (zmniejszył lub całkowicie wyłączył) ciśnienie w Pana/Pani aparacie CPAP?",
        choices=CPAP_ZMIANA_CHOICES,
        required=False,
        widget=forms.RadioSelect,
    )
    choroby = forms.MultipleChoiceField(
        label="Na jakie inne schorzenia Pan/Pani choruje? (Zaznacz wszystkie pasujące).",
        choices=CHOROBY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )
    choroby_inne = forms.CharField(
        label="Inne schorzenie",
        required=False,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Wpisz nazwę schorzenia"}),
    )
    fizjoterapia = forms.ChoiceField(label="Czy w okresie objętym tym etapem badania korzystał(a) Pan/Pani z pomocy fizjoterapeuty, rehabilitanta lub trenera medycznego?", choices=FIZJOTERAPIA_CHOICES, widget=forms.RadioSelect)
    charakter_aktywnosci = forms.ChoiceField(label="Jaki jest główny charakter Pana/Pani codziennej aktywności?", choices=CHARAKTER_AKTYWNOSCI_CHOICES, widget=forms.RadioSelect)
    alkohol_przed_snem = forms.ChoiceField(label="Czy zdarza się Panu/Pani spożywać alkohol w ciągu 2-3 godzin przed pójściem spać?", choices=ALKOHOL_PRZED_SNEM_CHOICES, widget=forms.RadioSelect)
    palenie = forms.ChoiceField(label="Czy pali Pan/Pani wyroby tytoniowe lub e-papierosy?", choices=PALENIE_CHOICES, widget=forms.RadioSelect)
    pozycja_snu = forms.ChoiceField(label="W jakiej pozycji najczęściej Pan/Pani sypia?", choices=POZYCJA_SNU_CHOICES, widget=forms.RadioSelect)
    obwod_szyi = forms.FloatField(
        label="Jaki jest Pana/Pani obwód szyi? Wynik podaj w centymetrach (cm), z dokładnością do 0,5 cm.",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "input", "step": "0.5"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        choroby = cleaned_data.get("choroby") or []
        choroby_inne = (cleaned_data.get("choroby_inne") or "").strip()

        if "brak" in choroby and len(choroby) > 1:
            self.add_error("choroby", 'Opcja "Żadne z powyższych" nie może być zaznaczona razem z innymi odpowiedziami.')

        if "inne" in choroby and not choroby_inne:
            self.add_error("choroby_inne", 'Jeśli wybierasz "Inne", wpisz jakie schorzenie.')

        if choroby_inne and "inne" not in choroby:
            self.add_error("choroby_inne", 'Opis innych schorzeń podaj tylko po zaznaczeniu opcji "Inne".')

        return cleaned_data
