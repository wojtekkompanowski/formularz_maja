from __future__ import annotations

from collections import Counter
from statistics import fmean

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .forms import (
    CPAPZdrowieForm,
    DanePodstawoweForm,
    EpworthForm,
    IPAQForm,
    OperacjaBariatrycznaForm,
    PittsburghForm,
    PITTSBURGH_CZESTOTLIWOSC,
    TAK_NIE_CHOICES,
)
from .models import Badanie


EPWORTH_INTERPRETATION_CHOICES = [
    ("wynik prawidłowy", "Wynik prawidłowy"),
    ("łagodna senność", "Łagodna senność"),
    ("umiarkowana senność", "Umiarkowana senność"),
    ("ciężka senność", "Ciężka senność"),
]

IPAQ_CATEGORY_CHOICES = [
    ("niewystarczająca", "Niewystarczająca"),
    ("dostateczna", "Dostateczna"),
    ("wysoka", "Wysoka"),
]

PSQI_CATEGORY_CHOICES = [
    ("do_5", "Wynik do 5 pkt"),
    ("powyzej_5", "Powyżej 5 pkt"),
]

SORT_CHOICES = [
    ("-data_badania", "Najnowsze badania"),
    ("data_badania", "Najstarsze badania"),
    ("pacjent__kod", "Kod pacjenta A-Z"),
    ("-pacjent__kod", "Kod pacjenta Z-A"),
    ("wiek", "Wiek rosnąco"),
    ("-wiek", "Wiek malejąco"),
    ("masa_ciala", "Masa ciała rosnąco"),
    ("-masa_ciala", "Masa ciała malejąco"),
    ("epworth__wynik", "Epworth rosnąco"),
    ("-epworth__wynik", "Epworth malejąco"),
    ("ipaq__wynik_met", "IPAQ rosnąco"),
    ("-ipaq__wynik_met", "IPAQ malejąco"),
    ("pittsburgh__wynik", "PSQI rosnąco"),
    ("-pittsburgh__wynik", "PSQI malejąco"),
]

SORT_VALUE_MAP = {value: value for value, _label in SORT_CHOICES}


def _choice_map(form_class, field_name):
    return dict(form_class.base_fields[field_name].choices)


FIELD_CHOICE_MAPS = {
    "etap": _choice_map(DanePodstawoweForm, "etap"),
    "plec": _choice_map(DanePodstawoweForm, "plec"),
    "operacja_bariatryczna": _choice_map(OperacjaBariatrycznaForm, "operacja_bariatryczna"),
    "cpap": _choice_map(CPAPZdrowieForm, "cpap"),
    "cpap_godziny_snu": _choice_map(CPAPZdrowieForm, "cpap_godziny_snu"),
    "cpap_zmiana_cisnienia": _choice_map(CPAPZdrowieForm, "cpap_zmiana_cisnienia"),
    "fizjoterapia": _choice_map(CPAPZdrowieForm, "fizjoterapia"),
    "charakter_aktywnosci": _choice_map(CPAPZdrowieForm, "charakter_aktywnosci"),
    "alkohol_przed_snem": _choice_map(CPAPZdrowieForm, "alkohol_przed_snem"),
    "pozycja_snu": _choice_map(CPAPZdrowieForm, "pozycja_snu"),
    "choroby": _choice_map(CPAPZdrowieForm, "choroby"),
    "epworth_answer": dict(EpworthForm.base_fields["pytanie_1"].choices),
    "tak_nie": dict(TAK_NIE_CHOICES),
    "ipaq_kategoria": dict(IPAQ_CATEGORY_CHOICES),
    "pittsburgh_freq": dict(PITTSBURGH_CZESTOTLIWOSC),
    "jakosc_snu": _choice_map(PittsburghForm, "jakosc_snu"),
    "psqi": dict(PSQI_CATEGORY_CHOICES),
}


class PanelFilterForm(forms.Form):
    q = forms.CharField(
        label="Kod pacjenta",
        required=False,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "np. ANJA05"}),
    )
    od = forms.DateField(
        label="Od",
        required=False,
        widget=forms.DateInput(attrs={"class": "input", "type": "date"}),
    )
    do = forms.DateField(
        label="Do",
        required=False,
        widget=forms.DateInput(attrs={"class": "input", "type": "date"}),
    )
    etap = forms.ChoiceField(
        label="Etap",
        required=False,
        choices=[("", "Wszystkie etapy")] + list(DanePodstawoweForm.base_fields["etap"].choices),
        widget=forms.Select(attrs={"class": "input"}),
    )
    plec = forms.ChoiceField(
        label="Płeć",
        required=False,
        choices=[("", "Wszystkie płcie")] + list(DanePodstawoweForm.base_fields["plec"].choices),
        widget=forms.Select(attrs={"class": "input"}),
    )
    operacja = forms.ChoiceField(
        label="Operacja bariatryczna",
        required=False,
        choices=[
            ("", "Wszystkie"),
            ("tak", "Tak"),
            ("nie", "Nie"),
        ],
        widget=forms.Select(attrs={"class": "input"}),
    )
    cpap = forms.ChoiceField(
        label="CPAP",
        required=False,
        choices=[("", "Wszystkie CPAP")] + list(CPAPZdrowieForm.base_fields["cpap"].choices),
        widget=forms.Select(attrs={"class": "input"}),
    )
    palenie = forms.ChoiceField(
        label="Palenie",
        required=False,
        choices=[
            ("", "Wszystkie"),
            ("tak", "Tak"),
            ("nie", "Nie"),
        ],
        widget=forms.Select(attrs={"class": "input"}),
    )
    epworth = forms.ChoiceField(
        label="Epworth",
        required=False,
        choices=[("", "Wszystkie")] + EPWORTH_INTERPRETATION_CHOICES,
        widget=forms.Select(attrs={"class": "input"}),
    )
    ipaq = forms.ChoiceField(
        label="IPAQ",
        required=False,
        choices=[("", "Wszystkie")] + IPAQ_CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "input"}),
    )
    psqi = forms.ChoiceField(
        label="PSQI",
        required=False,
        choices=[("", "Wszystkie")] + PSQI_CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "input"}),
    )
    status = forms.ChoiceField(
        label="Kompletność",
        required=False,
        choices=[
            ("", "Wszystkie"),
            ("kompletne", "Kompletne badania"),
            ("niekompletne", "Braki w formularzach"),
        ],
        widget=forms.Select(attrs={"class": "input"}),
    )
    sort = forms.ChoiceField(
        label="Sortowanie",
        required=False,
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={"class": "input"}),
    )


def apply_panel_filters(queryset, data):
    q = data.get("q")
    if q:
        queryset = queryset.filter(pacjent__kod__icontains=q)

    od = data.get("od")
    if od:
        queryset = queryset.filter(data_badania__date__gte=od)

    do = data.get("do")
    if do:
        queryset = queryset.filter(data_badania__date__lte=do)

    etap = data.get("etap")
    if etap:
        queryset = queryset.filter(etap=etap)

    plec = data.get("plec")
    if plec:
        queryset = queryset.filter(plec=plec)

    operacja = data.get("operacja")
    if operacja == "tak":
        queryset = queryset.filter(operacja_bariatryczna=True)
    elif operacja == "nie":
        queryset = queryset.filter(operacja_bariatryczna=False)

    cpap = data.get("cpap")
    if cpap:
        queryset = queryset.filter(cpap=cpap)

    palenie = data.get("palenie")
    if palenie == "tak":
        queryset = queryset.filter(palenie=True)
    elif palenie == "nie":
        queryset = queryset.filter(palenie=False)

    epworth = data.get("epworth")
    if epworth:
        queryset = queryset.filter(epworth__interpretacja=epworth)

    ipaq = data.get("ipaq")
    if ipaq:
        queryset = queryset.filter(ipaq__kategoria=ipaq)

    psqi = data.get("psqi")
    if psqi == "do_5":
        queryset = queryset.filter(pittsburgh__wynik__lte=5)
    elif psqi == "powyzej_5":
        queryset = queryset.filter(pittsburgh__wynik__gt=5)

    status = data.get("status")
    if status == "kompletne":
        queryset = queryset.filter(epworth__isnull=False, ipaq__isnull=False, pittsburgh__isnull=False)
    elif status == "niekompletne":
        queryset = queryset.exclude(epworth__isnull=False, ipaq__isnull=False, pittsburgh__isnull=False)

    sort = data.get("sort") or "-data_badania"
    return queryset.order_by(SORT_VALUE_MAP.get(sort, "-data_badania"))


CORE_SECTIONS = [
    (
        "Dane podstawowe",
        [
            ("etap", "Etap badania"),
            ("plec", "Płeć"),
            ("wiek", "Wiek"),
            ("masa_ciala", "Aktualna masa ciała"),
            ("wzrost", "Wzrost"),
            ("bmi", "BMI"),
            ("obwod_szyi", "Obwód szyi"),
        ],
    ),
    (
        "Operacja i CPAP",
        [
            ("operacja_bariatryczna", "Operacja bariatryczna"),
            ("data_operacji_bariatrycznej", "Data operacji"),
            ("maksymalna_masa_przed_operacja", "Maksymalna masa przed operacją"),
            ("cpap", "CPAP"),
            ("cpap_czas_stosowania", "Czas stosowania CPAP"),
            ("cpap_godziny_snu", "Sen z CPAP"),
            ("cpap_zmiana_cisnienia", "Zmiana ciśnienia CPAP"),
            ("choroby", "Choroby współistniejące"),
        ],
    ),
    (
        "Styl życia",
        [
            ("fizjoterapia", "Fizjoterapia / rehabilitacja"),
            ("charakter_aktywnosci", "Charakter aktywności"),
            ("alkohol_przed_snem", "Alkohol przed snem"),
            ("palenie", "Palenie"),
            ("pozycja_snu", "Pozycja snu"),
        ],
    ),
]


EPWORTH_QUESTIONS = [
    ("pytanie_1", "Siedzenie i czytanie"),
    ("pytanie_2", "Oglądanie telewizji"),
    ("pytanie_3", "Bierne siedzenie w miejscach publicznych"),
    ("pytanie_4", "Jako pasażer w samochodzie"),
    ("pytanie_5", "Leżenie i odpoczywanie po południu"),
    ("pytanie_6", "W czasie rozmowy, siedząc"),
    ("pytanie_7", "Spokojne siedzenie po obiedzie bez alkoholu"),
    ("pytanie_8", "W samochodzie podczas postoju"),
]


IPAQ_QUESTIONS = [
    ("szpital", "Szpital"),
    ("choroba", "Choroba"),
    ("rehabilitacja", "Rehabilitacja"),
    ("urlop", "Urlop"),
    ("rekonwalescencja", "Rekonwalescencja"),
    ("ciaza", "Ciąża"),
    ("intensywne_dni", "Intensywny wysiłek - dni"),
    ("intensywne_minuty", "Intensywny wysiłek - minuty"),
    ("umiarkowane_dni", "Umiarkowany wysiłek - dni"),
    ("umiarkowane_minuty", "Umiarkowany wysiłek - minuty"),
    ("chodzenie_dni", "Chodzenie - dni"),
    ("chodzenie_minuty", "Chodzenie - minuty"),
    ("siedzenie_minuty_dziennie", "Siedzenie - minuty dziennie"),
]


PITTSBURGH_QUESTIONS = [
    ("godzina_polozenia", "Godzina położenia się spać"),
    ("czas_zasypiania_minuty", "Czas zasypiania"),
    ("godzina_wstawania", "Godzina wstawania"),
    ("godziny_snu", "Rzeczywisty czas snu"),
    ("nie_zasnal_30_min", "Nie mógł/mogła zasnąć w 30 minut"),
    ("pobudka_w_nocy", "Pobudka w nocy / wcześnie rano"),
    ("toaleta", "Toaleta"),
    ("problemy_z_oddychaniem", "Problemy z oddychaniem"),
    ("kaszel_chrapanie", "Kaszel lub chrapanie"),
    ("za_zimno", "Za zimno"),
    ("za_cieplo", "Za ciepło"),
    ("zle_sny", "Złe sny"),
    ("bol", "Ból"),
    ("inne_powody", "Inne powody"),
    ("inne_powody_opis", "Opis innych powodów"),
    ("jakosc_snu", "Ogólna jakość snu"),
    ("leki_nasenne", "Leki nasenne"),
    ("problemy_z_czuwaniem", "Problemy z czuwaniem"),
    ("brak_energii", "Brak energii"),
]


INT_FIELDS = {
    "wiek",
    "czas_zasypiania_minuty",
    "intensywne_dni",
    "umiarkowane_dni",
    "chodzenie_dni",
    "siedzenie_minuty_dziennie",
    "nie_zasnal_30_min",
    "pobudka_w_nocy",
    "toaleta",
    "problemy_z_oddychaniem",
    "kaszel_chrapanie",
    "za_zimno",
    "za_cieplo",
    "zle_sny",
    "bol",
    "inne_powody",
    "jakosc_snu",
    "leki_nasenne",
    "problemy_z_czuwaniem",
    "brak_energii",
}

FLOAT_FIELDS = {
    "masa_ciala",
    "wzrost",
    "maksymalna_masa_przed_operacja",
    "obwod_szyi",
    "godziny_snu",
    "intensywne_minuty",
    "umiarkowane_minuty",
    "chodzenie_minuty",
}

TIME_FIELDS = {"godzina_polozenia", "godzina_wstawania"}


def _safe_related(instance, attr):
    try:
        return getattr(instance, attr)
    except ObjectDoesNotExist:
        return None


def _format_number(value, precision=1):
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "Tak" if value else "Nie"
    if precision == 0:
        return f"{int(round(value))}"
    formatted = f"{float(value):.{precision}f}"
    return formatted.rstrip("0").rstrip(".")


def _format_choice(field_name, value):
    if value in (None, ""):
        return "-"

    if field_name == "choroby":
        codes = [part.strip() for part in str(value).split(",") if part.strip()]
        labels = [FIELD_CHOICE_MAPS["choroby"].get(code, code) for code in codes]
        return labels or ["-"]

    mapping = FIELD_CHOICE_MAPS.get(field_name, {})
    return mapping.get(value, mapping.get(str(value), str(value)))


def _display_value(field_name, value):
    if field_name in TIME_FIELDS:
        if value in (None, ""):
            return "-"
        return value.strftime("%H:%M")

    if field_name in FLOAT_FIELDS:
        return _format_number(value, 1)

    if field_name in INT_FIELDS:
        if value in (None, ""):
            return "-"
        return str(int(value))

    if field_name == "bmi":
        return _format_number(value, 1)

    if field_name in FIELD_CHOICE_MAPS:
        return _format_choice(field_name, value)

    if value in (None, ""):
        return "-"
    return str(value)


def calculate_bmi(weight, height_cm):
    if weight in (None, "") or height_cm in (None, ""):
        return None

    try:
        height_m = float(height_cm) / 100.0
        if height_m <= 0:
            return None
        return float(weight) / (height_m * height_m)
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def _build_section(instance, title, fields):
    items = []
    for field_name, label in fields:
        raw_value = getattr(instance, field_name, None)
        value = _display_value(field_name, raw_value)
        items.append(
            {
                "label": label,
                "value": value,
                "is_list": isinstance(value, list),
            }
        )

    return {"title": title, "items": items}


def build_record_view(badanie: Badanie):
    pacjent = badanie.pacjent
    bmi = calculate_bmi(badanie.masa_ciala, badanie.wzrost)

    epworth = _safe_related(badanie, "epworth")
    ipaq = _safe_related(badanie, "ipaq")
    pittsburgh = _safe_related(badanie, "pittsburgh")

    sections = [_build_section(badanie, title, fields) for title, fields in CORE_SECTIONS]

    epworth_section = {
        "title": "Skala Epworth",
        "meta": f"Uzupełniono: {epworth.data_wypelnienia.strftime('%d.%m.%Y %H:%M')}" if epworth else None,
        "summary": f"{epworth.wynik} pkt · {epworth.interpretacja}" if epworth else "Brak danych",
        "items": [],
    }
    if epworth:
        epworth_section["items"] = [
            {"label": "Wynik całkowity", "value": f"{epworth.wynik} pkt", "is_list": False},
            {"label": "Interpretacja", "value": epworth.interpretacja or "-", "is_list": False},
        ] + [
            {
                "label": label,
                "value": _display_value("epworth_answer", getattr(epworth, field_name)),
                "is_list": False,
            }
            for field_name, label in EPWORTH_QUESTIONS
        ]
    sections.append(epworth_section)

    ipaq_section = {
        "title": "IPAQ",
        "meta": f"Uzupełniono: {ipaq.data_wypelnienia.strftime('%d.%m.%Y %H:%M')}" if ipaq else None,
        "summary": f"{_format_number(ipaq.wynik_met, 0) if ipaq else '-'} MET · {ipaq.kategoria if ipaq else 'Brak danych'}",
        "items": [],
    }
    if ipaq:
        ipaq_section["items"] = [
            {"label": "Wynik MET", "value": f"{_format_number(ipaq.wynik_met, 0)} MET-min/tydzień", "is_list": False},
            {"label": "Kategoria", "value": ipaq.kategoria or "-", "is_list": False},
        ] + [
            {
                "label": label,
                "value": _display_value("tak_nie" if field_name in {"szpital", "choroba", "rehabilitacja", "urlop", "rekonwalescencja", "ciaza"} else field_name, getattr(ipaq, field_name)),
                "is_list": False,
            }
            for field_name, label in IPAQ_QUESTIONS
        ]
    sections.append(ipaq_section)

    pittsburgh_section = {
        "title": "Pittsburgh / PSQI",
        "meta": f"Uzupełniono: {pittsburgh.data_wypelnienia.strftime('%d.%m.%Y %H:%M')}" if pittsburgh else None,
        "summary": f"{pittsburgh.wynik} pkt" if pittsburgh else "Brak danych",
        "items": [],
    }
    if pittsburgh:
        pittsburgh_section["items"] = [
            {"label": "Wynik całkowity", "value": f"{pittsburgh.wynik} pkt", "is_list": False},
            {"label": "Ocena jakości snu", "value": "wynik podwyższony" if pittsburgh.wynik > 5 else "wynik w normie", "is_list": False},
        ] + [
            {
                "label": label,
                "value": _display_value(field_name, getattr(pittsburgh, field_name)),
                "is_list": False,
            }
            for field_name, label in PITTSBURGH_QUESTIONS
        ]
    sections.append(pittsburgh_section)

    missing_formularze = [
        label
        for label, present in (
            ("Epworth", epworth is not None),
            ("IPAQ", ipaq is not None),
            ("Pittsburgh", pittsburgh is not None),
        )
        if not present
    ]

    status_label = "Kompletne" if not missing_formularze else f"Brakuje: {', '.join(missing_formularze)}"
    status_class = "badge--success" if not missing_formularze else "badge--warning"

    return {
        "id": badanie.id,
        "kod": pacjent.kod,
        "data_badania": badanie.data_badania,
        "etap": _display_value("etap", badanie.etap),
        "plec": _display_value("plec", badanie.plec),
        "wiek": badanie.wiek,
        "wiek_display": _display_value("wiek", badanie.wiek),
        "masa_ciala": _display_value("masa_ciala", badanie.masa_ciala),
        "wzrost": _display_value("wzrost", badanie.wzrost),
        "bmi": _format_number(bmi, 1),
        "operacja_bariatryczna": _display_value("operacja_bariatryczna", badanie.operacja_bariatryczna),
        "cpap": _display_value("cpap", badanie.cpap),
        "choroby": _display_value("choroby", badanie.choroby),
        "fizjoterapia": _display_value("fizjoterapia", badanie.fizjoterapia),
        "charakter_aktywnosci": _display_value("charakter_aktywnosci", badanie.charakter_aktywnosci),
        "alkohol_przed_snem": _display_value("alkohol_przed_snem", badanie.alkohol_przed_snem),
        "palenie": _display_value("tak_nie", badanie.palenie),
        "pozycja_snu": _display_value("pozycja_snu", badanie.pozycja_snu),
        "obwod_szyi": _display_value("obwod_szyi", badanie.obwod_szyi),
        "epworth_score": epworth.wynik if epworth else None,
        "epworth_score_display": str(epworth.wynik) if epworth else "-",
        "epworth_interpretacja": epworth.interpretacja if epworth else "-",
        "ipaq_score": ipaq.wynik_met if ipaq else None,
        "ipaq_score_display": _format_number(ipaq.wynik_met, 0) if ipaq else "-",
        "ipaq_kategoria": ipaq.kategoria if ipaq else "-",
        "pittsburgh_score": pittsburgh.wynik if pittsburgh else None,
        "pittsburgh_score_display": str(pittsburgh.wynik) if pittsburgh else "-",
        "pittsburgh_status": "wynik podwyższony" if pittsburgh and pittsburgh.wynik > 5 else ("wynik w normie" if pittsburgh else "-"),
        "status_label": status_label,
        "status_class": status_class,
        "missing_formularze": missing_formularze,
        "sections": sections,
    }


def build_badanie_list(queryset):
    return [build_record_view(badanie) for badanie in queryset]


def _mean(values):
    values = [value for value in values if value is not None]
    if not values:
        return None
    return fmean(values)


def _chart_items(counter, ordered_labels):
    max_count = max((counter.get(label, 0) for label in ordered_labels), default=0)
    items = []
    for label in ordered_labels:
        count = counter.get(label, 0)
        width = int(round((count / max_count) * 100)) if max_count else 0
        items.append({"label": label, "count": count, "width": width})
    return items


def build_dashboard_context(queryset, filter_form=None):
    records = build_badanie_list(queryset)
    patients = {record["kod"] for record in records}
    complete_records = [record for record in records if record["status_class"] == "badge--success"]

    ages = [record["wiek"] for record in records if record["wiek"] is not None]
    masses = [float(record["masa_ciala"]) for record in records if record["masa_ciala"] != "-"]
    bmis = [float(record["bmi"]) for record in records if record["bmi"] != "-"]
    epworth_scores = [record["epworth_score"] for record in records if record["epworth_score"] is not None]
    ipaq_scores = [record["ipaq_score"] for record in records if record["ipaq_score"] is not None]
    pittsburgh_scores = [record["pittsburgh_score"] for record in records if record["pittsburgh_score"] is not None]

    stage_counter = Counter(record["etap"] for record in records if record["etap"] != "-")
    epworth_counter = Counter(record["epworth_interpretacja"] for record in records if record["epworth_interpretacja"] != "-")
    ipaq_counter = Counter(record["ipaq_kategoria"] for record in records if record["ipaq_kategoria"] != "-")

    choroby_counter = Counter()
    for record in records:
        for choroba in record["choroby"] if isinstance(record["choroby"], list) else []:
            choroby_counter[choroba] += 1

    charts = [
        {
            "title": "Etapy badania",
            "items": _chart_items(stage_counter, [label for _value, label in DanePodstawoweForm.base_fields["etap"].choices]),
        },
        {
            "title": "Interpretacja Epworth",
            "items": _chart_items(epworth_counter, [label for _value, label in EPWORTH_INTERPRETATION_CHOICES]),
        },
        {
            "title": "Kategorie IPAQ",
            "items": _chart_items(ipaq_counter, [label for _value, label in IPAQ_CATEGORY_CHOICES]),
        },
        {
            "title": "Najczęstsze choroby",
            "items": [
                {
                    "label": label,
                    "count": count,
                    "width": int(round((count / max(choroby_counter.values())) * 100)) if choroby_counter else 0,
                }
                for label, count in choroby_counter.most_common(5)
            ],
        },
    ]

    stats = [
        {"label": "Badania", "value": len(records), "note": "po filtrach"},
        {"label": "Pacjenci", "value": len(patients), "note": "unikalne kody"},
        {"label": "Kompletne", "value": len(complete_records), "note": "z 3 kwestionariuszami"},
        {"label": "Braki", "value": len(records) - len(complete_records), "note": "bez pełnego zestawu"},
        {"label": "Średni wiek", "value": _format_number(_mean(ages), 1), "note": "lata"},
        {"label": "Średnia masa", "value": _format_number(_mean(masses), 1), "note": "kg"},
        {"label": "Średni BMI", "value": _format_number(_mean(bmis), 1), "note": "kg/m²"},
        {"label": "Śr. Epworth", "value": _format_number(_mean(epworth_scores), 1), "note": "pkt"},
        {"label": "Śr. IPAQ", "value": _format_number(_mean(ipaq_scores), 0), "note": "MET-min/tydzień"},
        {"label": "Śr. PSQI", "value": _format_number(_mean(pittsburgh_scores), 1), "note": "pkt"},
    ]

    return {
        "filter_form": filter_form,
        "records": records,
        "stats": stats,
        "charts": charts,
    }

