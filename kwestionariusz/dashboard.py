from __future__ import annotations

from collections import Counter
from statistics import fmean

from django import forms
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from .forms import (
    CPAPZdrowieForm,
    DanePodstawoweForm,
    EpworthForm,
    FOSQ_ACTIVITY_CHOICES,
    FOSQ_DIFFICULTY_CHOICES,
    FOSQ_QUESTION_DEFINITIONS,
    FOSQ_SECTION_DEFINITIONS,
    IPAQForm,
    OperacjaBariatrycznaForm,
    PittsburghForm,
    TAK_NIE_CHOICES,
    CHOROBY_CHOICES,
)
from .models import Badanie, FOSQ_SECTION_ITEMS


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

NECK_STATUS_CHOICES = [
    ("", "Wszystkie"),
    ("w_normie", "W normie"),
    ("ponizej_normy", "Poniżej normy"),
    ("podwyzszone_ryzyko", "Podwyższone ryzyko"),
    ("wysokie_ryzyko", "Wysokie ryzyko"),
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
    ("obwod_szyi", "Obwód szyi rosnąco"),
    ("-obwod_szyi", "Obwód szyi malejąco"),
    ("epworth__wynik", "Epworth rosnąco"),
    ("-epworth__wynik", "Epworth malejąco"),
    ("ipaq__wynik_met", "IPAQ rosnąco"),
    ("-ipaq__wynik_met", "IPAQ malejąco"),
    ("pittsburgh__wynik", "FOSQ rosnąco"),
    ("-pittsburgh__wynik", "FOSQ malejąco"),
]

SORT_VALUE_MAP = {value: value for value, _label in SORT_CHOICES}


def _choice_map(form_class, field_name):
    return dict(form_class.base_fields[field_name].choices)


FOSQ_FIELD_META = {}
for index, (field_name, label, scale, section_key) in enumerate(FOSQ_QUESTION_DEFINITIONS, start=1):
    FOSQ_FIELD_META[field_name] = {
        "number": index,
        "label": label,
        "scale": scale,
        "section": section_key,
    }

FOSQ_CHOICE_MAPS = {
    "difficulty": dict(FOSQ_DIFFICULTY_CHOICES),
    "activity": dict(FOSQ_ACTIVITY_CHOICES),
}

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
    "choroby": dict(CHOROBY_CHOICES),
    "tak_nie": dict(TAK_NIE_CHOICES),
    "epworth_interpretacja": dict(EPWORTH_INTERPRETATION_CHOICES),
    "ipaq_kategoria": dict(IPAQ_CATEGORY_CHOICES),
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
        choices=[("", "Wszystkie"), ("tak", "Tak"), ("nie", "Nie")],
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
        choices=[("", "Wszystkie"), ("tak", "Tak"), ("nie", "Nie")],
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
    fosq_min = forms.FloatField(
        label="FOSQ min.",
        required=False,
        widget=forms.NumberInput(attrs={"class": "input", "step": "0.1"}),
    )
    fosq_max = forms.FloatField(
        label="FOSQ max.",
        required=False,
        widget=forms.NumberInput(attrs={"class": "input", "step": "0.1"}),
    )
    neck_status = forms.ChoiceField(
        label="Obwód szyi",
        required=False,
        choices=NECK_STATUS_CHOICES,
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


def classify_neck_circumference(plec, obwod):
    if obwod in (None, ""):
        return {
            "key": "brak_danych",
            "label": "-",
            "class": "badge--muted",
            "reference": "Brak pomiaru",
        }

    try:
        value = float(obwod)
    except (TypeError, ValueError):
        return {
            "key": "brak_danych",
            "label": "-",
            "class": "badge--muted",
            "reference": "Brak pomiaru",
        }

    if plec == "kobieta":
        if value < 33:
            return {
                "key": "ponizej_normy",
                "label": "Poniżej normy",
                "class": "badge--warning",
                "reference": "Kobiety: 33-35 cm w normie, 36-40 cm podwyższone ryzyko, powyżej 40 cm wysokie ryzyko.",
            }
        if value <= 35:
            return {
                "key": "w_normie",
                "label": "W normie",
                "class": "badge--success",
                "reference": "Kobiety: 33-35 cm w normie, 36-40 cm podwyższone ryzyko, powyżej 40 cm wysokie ryzyko.",
            }
        if value <= 40:
            return {
                "key": "podwyzszone_ryzyko",
                "label": "Podwyższone ryzyko",
                "class": "badge--warning",
                "reference": "Kobiety: 33-35 cm w normie, 36-40 cm podwyższone ryzyko, powyżej 40 cm wysokie ryzyko.",
            }
        return {
            "key": "wysokie_ryzyko",
            "label": "Wysokie ryzyko",
            "class": "badge--danger",
            "reference": "Kobiety: 33-35 cm w normie, 36-40 cm podwyższone ryzyko, powyżej 40 cm wysokie ryzyko.",
        }

    if plec == "mezczyzna":
        if value < 37:
            return {
                "key": "ponizej_normy",
                "label": "Poniżej normy",
                "class": "badge--warning",
                "reference": "Mężczyźni: 37-40 cm w normie, 41-43 cm podwyższone ryzyko, powyżej 43 cm wysokie ryzyko.",
            }
        if value <= 40:
            return {
                "key": "w_normie",
                "label": "W normie",
                "class": "badge--success",
                "reference": "Mężczyźni: 37-40 cm w normie, 41-43 cm podwyższone ryzyko, powyżej 43 cm wysokie ryzyko.",
            }
        if value <= 43:
            return {
                "key": "podwyzszone_ryzyko",
                "label": "Podwyższone ryzyko",
                "class": "badge--warning",
                "reference": "Mężczyźni: 37-40 cm w normie, 41-43 cm podwyższone ryzyko, powyżej 43 cm wysokie ryzyko.",
            }
        return {
            "key": "wysokie_ryzyko",
            "label": "Wysokie ryzyko",
            "class": "badge--danger",
            "reference": "Mężczyźni: 37-40 cm w normie, 41-43 cm podwyższone ryzyko, powyżej 43 cm wysokie ryzyko.",
        }

    return {
        "key": "brak_danych",
        "label": "-",
        "class": "badge--muted",
        "reference": "Brak danych o płci do oceny.",
    }


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

    fosq_min = data.get("fosq_min")
    if fosq_min is not None:
        queryset = queryset.filter(pittsburgh__wynik__gte=fosq_min)

    fosq_max = data.get("fosq_max")
    if fosq_max is not None:
        queryset = queryset.filter(pittsburgh__wynik__lte=fosq_max)

    neck_status = data.get("neck_status")
    if neck_status == "w_normie":
        queryset = queryset.filter(
            Q(plec="kobieta", obwod_szyi__gte=33, obwod_szyi__lte=35)
            | Q(plec="mezczyzna", obwod_szyi__gte=37, obwod_szyi__lte=40)
        )
    elif neck_status == "ponizej_normy":
        queryset = queryset.filter(
            Q(plec="kobieta", obwod_szyi__lt=33)
            | Q(plec="mezczyzna", obwod_szyi__lt=37)
        )
    elif neck_status == "podwyzszone_ryzyko":
        queryset = queryset.filter(
            Q(plec="kobieta", obwod_szyi__gte=36, obwod_szyi__lte=40)
            | Q(plec="mezczyzna", obwod_szyi__gte=41, obwod_szyi__lte=43)
        )
    elif neck_status == "wysokie_ryzyko":
        queryset = queryset.filter(
            Q(plec="kobieta", obwod_szyi__gt=40)
            | Q(plec="mezczyzna", obwod_szyi__gt=43)
        )

    status = data.get("status")
    if status == "kompletne":
        queryset = queryset.filter(epworth__isnull=False, ipaq__isnull=False, pittsburgh__isnull=False)
    elif status == "niekompletne":
        queryset = queryset.exclude(epworth__isnull=False, ipaq__isnull=False, pittsburgh__isnull=False)

    sort = data.get("sort") or "-data_badania"
    return queryset.order_by(SORT_VALUE_MAP.get(sort, "-data_badania"))


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


def _safe_related(instance, attr):
    try:
        return getattr(instance, attr)
    except ObjectDoesNotExist:
        return None


def _format_number(value, precision=1):
    if value in (None, ""):
        return "-"
    if isinstance(value, bool):
        return "Tak" if value else "Nie"
    formatted = f"{float(value):.{precision}f}"
    return formatted.rstrip("0").rstrip(".")


def _format_choice(field_name, value):
    if value in (None, ""):
        return "-"

    mapping = FIELD_CHOICE_MAPS.get(field_name, {})
    if field_name == "choroby":
        codes = [part.strip() for part in str(value).split(",") if part.strip()]
        labels = [mapping.get(code, code) for code in codes]
        return labels or ["-"]

    return mapping.get(value, mapping.get(str(value), str(value)))


def _format_choroby_list(value):
    if value in (None, ""):
        return []

    mapping = FIELD_CHOICE_MAPS.get("choroby", {})
    codes = [part.strip() for part in str(value).split(",") if part.strip()]
    labels = []
    for code in codes:
        if code == "inne":
            continue
        label = mapping.get(code, code)
        if label and label != "-":
            labels.append(label)
    return labels


def _format_fosq_value(field_name, value):
    if value in (None, ""):
        return "-"

    meta = FOSQ_FIELD_META.get(field_name)
    if not meta:
        return str(value)

    return FOSQ_CHOICE_MAPS[meta["scale"]].get(value, FOSQ_CHOICE_MAPS[meta["scale"]].get(str(value), str(value)))


def _display_value(field_name, value):
    if field_name in {"godzina_polozenia", "godzina_wstawania"}:
        if value in (None, ""):
            return "-"
        return value.strftime("%H:%M")

    if field_name in {"masa_ciala", "wzrost", "maksymalna_masa_przed_operacja", "obwod_szyi", "godziny_snu", "intensywne_minuty", "umiarkowane_minuty", "chodzenie_minuty"}:
        return _format_number(value, 1)

    if field_name in {"wiek", "czas_zasypiania_minuty", "intensywne_dni", "umiarkowane_dni", "chodzenie_dni", "siedzenie_minuty_dziennie"}:
        if value in (None, ""):
            return "-"
        return str(int(value))

    if field_name == "bmi":
        return _format_number(value, 1)

    if field_name in FOSQ_FIELD_META:
        return _format_fosq_value(field_name, value)

    if field_name in FIELD_CHOICE_MAPS:
        return _format_choice(field_name, value)

    if value in (None, ""):
        return "-"
    if isinstance(value, bool):
        return "Tak" if value else "Nie"
    return str(value)


def _list_value(*parts):
    values = [part for part in parts if part not in (None, "", [], "-")]
    return values or ["-"]


def _build_section(title, items, meta=None, summary=None):
    return {
        "title": title,
        "meta": meta,
        "summary": summary,
        "items": items,
    }


def _build_items(instance, fields):
    items = []
    for field_name, label in fields:
        raw_value = getattr(instance, field_name, None)
        value = _display_value(field_name, raw_value)
        items.append({
            "label": label,
            "value": value,
            "is_list": isinstance(value, list),
        })
    return items


def _fosq_section_summary(record, section_key):
    score_map = {
        "produktywność": record.get("produktywnosc_wynik"),
        "kontakty_spoleczne": record.get("kontakty_spoleczne_wynik"),
        "aktywność": record.get("aktywnosc_wynik"),
        "czujność": record.get("czujnosc_wynik"),
        "intymnosc": record.get("intymnosc_wynik"),
    }
    score = score_map.get(section_key)
    if score is None:
        return "Brak danych"
    return f"{_format_number(score, 2)} / 4"


def build_record_view(badanie: Badanie):
    pacjent = badanie.pacjent
    bmi = calculate_bmi(badanie.masa_ciala, badanie.wzrost)

    epworth = _safe_related(badanie, "epworth")
    ipaq = _safe_related(badanie, "ipaq")
    fosq = _safe_related(badanie, "pittsburgh")

    neck = classify_neck_circumference(badanie.plec, badanie.obwod_szyi)

    choroby_display = _format_choroby_list(badanie.choroby)
    if badanie.choroby_inne:
        choroby_display.append(f"Inne: {badanie.choroby_inne}")
    choroby_display = choroby_display if choroby_display else []

    sections = [
        _build_section(
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
            meta=f"Obwód szyi: {neck['label']}",
            summary=f"BMI {_format_number(bmi, 1)} · {neck['label']}",
        ),
        _build_section(
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
                ("choroby_inne", "Inne schorzenia"),
                ("fizjoterapia", "Fizjoterapia / rehabilitacja"),
                ("charakter_aktywnosci", "Charakter aktywności"),
                ("alkohol_przed_snem", "Alkohol przed snem"),
                ("palenie", "Palenie"),
                ("pozycja_snu", "Pozycja snu"),
            ],
            summary=_display_value("cpap", badanie.cpap),
        ),
    ]

    if epworth:
        sections.append(
            _build_section(
                "Skala Epworth",
                [
                    {"label": "Wynik całkowity", "value": f"{epworth.wynik} pkt", "is_list": False},
                    {"label": "Interpretacja", "value": epworth.interpretacja or "-", "is_list": False},
                ]
                + [
                    {
                        "label": label,
                        "value": _display_value(field_name, getattr(epworth, field_name)),
                        "is_list": False,
                    }
                    for field_name, label in [
                        ("pytanie_1", "Siedzenie i czytanie"),
                        ("pytanie_2", "Oglądanie telewizji"),
                        ("pytanie_3", "Bierne siedzenie w miejscach publicznych"),
                        ("pytanie_4", "Jako pasażer w samochodzie"),
                        ("pytanie_5", "Leżenie i odpoczywanie po południu"),
                        ("pytanie_6", "W czasie rozmowy, siedząc"),
                        ("pytanie_7", "Spokojne siedzenie po obiedzie bez alkoholu"),
                        ("pytanie_8", "W samochodzie podczas postoju"),
                    ]
                ],
                meta=f"Uzupełniono: {epworth.data_wypelnienia.strftime('%d.%m.%Y %H:%M')}",
                summary=f"{epworth.wynik} pkt · {epworth.interpretacja}",
            )
        )
    else:
        sections.append(_build_section("Skala Epworth", [], summary="Brak danych"))

    if ipaq:
        sections.append(
            _build_section(
                "IPAQ",
                [
                    {"label": "Wynik MET", "value": f"{_format_number(ipaq.wynik_met, 0)} MET-min/tydzień", "is_list": False},
                    {"label": "Kategoria", "value": ipaq.kategoria or "-", "is_list": False},
                ]
                + [
                    {
                        "label": label,
                        "value": _display_value("tak_nie" if field_name in {"szpital", "choroba", "rehabilitacja", "urlop", "rekonwalescencja", "ciaza"} else field_name, getattr(ipaq, field_name)),
                        "is_list": False,
                    }
                    for field_name, label in [
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
                ],
                meta=f"Uzupełniono: {ipaq.data_wypelnienia.strftime('%d.%m.%Y %H:%M')}",
                summary=f"{_format_number(ipaq.wynik_met, 0)} MET · {ipaq.kategoria}",
            )
        )
    else:
        sections.append(_build_section("IPAQ", [], summary="Brak danych"))

    fosq_score_fields = {
        "produktywność": "produktywnosc_wynik",
        "kontakty_spoleczne": "kontakty_spoleczne_wynik",
        "aktywność": "aktywnosc_wynik",
        "czujność": "czujnosc_wynik",
        "intymnosc": "intymnosc_wynik",
    }

    fosq_answered_sections = 0
    fosq_section_values = {}
    if fosq:
        for section_key, section_title, field_names in FOSQ_SECTION_DEFINITIONS:
            section_score = getattr(fosq, fosq_score_fields[section_key])
            fosq_section_values[section_key] = section_score
            if section_score is not None:
                fosq_answered_sections += 1

            items = [
                {
                    "label": FOSQ_FIELD_META[field_name]["label"],
                    "value": _display_value(field_name, getattr(fosq, field_name)),
                    "is_list": False,
                }
                for field_name in field_names
            ]
            sections.append(
                _build_section(
                    f"FOSQ - {section_title}",
                    items,
                    meta=f"Uzupełniono: {fosq.data_wypelnienia.strftime('%d.%m.%Y %H:%M')}",
                    summary=_fosq_section_summary(
                        {
                            "produktywnosc_wynik": fosq.produktywnosc_wynik,
                            "kontakty_spoleczne_wynik": fosq.kontakty_spoleczne_wynik,
                            "aktywnosc_wynik": fosq.aktywnosc_wynik,
                            "czujnosc_wynik": fosq.czujnosc_wynik,
                            "intymnosc_wynik": fosq.intymnosc_wynik,
                        },
                        section_key,
                    ),
                )
            )
    else:
        sections.append(_build_section("FOSQ", [], summary="Brak danych"))

    missing_formularze = [
        label
        for label, present in (
            ("Epworth", epworth is not None),
            ("IPAQ", ipaq is not None),
            ("FOSQ", fosq is not None),
        )
        if not present
    ]

    status_label = "Kompletne" if not missing_formularze else f"Brakuje: {', '.join(missing_formularze)}"
    status_class = "badge--success" if not missing_formularze else "badge--warning"

    fosq_score_display = _format_number(fosq.wynik, 2) if fosq and fosq.wynik is not None else "-"
    fosq_status = f"{fosq_answered_sections}/5 sekcji" if fosq else "-"
    if fosq:
        fosq_status_class = "badge--success" if fosq_answered_sections == 5 else "badge--warning"
    else:
        fosq_status_class = "badge--muted"

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
        "obwod_szyi": _display_value("obwod_szyi", badanie.obwod_szyi),
        "obwod_szyi_status": neck["label"],
        "obwod_szyi_status_class": neck["class"],
        "obwod_szyi_reference": neck["reference"],
        "operacja_bariatryczna": _display_value("operacja_bariatryczna", badanie.operacja_bariatryczna),
        "cpap": _display_value("cpap", badanie.cpap),
        "choroby": choroby_display,
        "choroby_display": choroby_display,
        "choroby_inne": badanie.choroby_inne or "-",
        "fizjoterapia": _display_value("fizjoterapia", badanie.fizjoterapia),
        "charakter_aktywnosci": _display_value("charakter_aktywnosci", badanie.charakter_aktywnosci),
        "alkohol_przed_snem": _display_value("alkohol_przed_snem", badanie.alkohol_przed_snem),
        "palenie": _display_value("tak_nie", badanie.palenie),
        "pozycja_snu": _display_value("pozycja_snu", badanie.pozycja_snu),
        "epworth_score": epworth.wynik if epworth else None,
        "epworth_score_display": str(epworth.wynik) if epworth else "-",
        "epworth_interpretacja": epworth.interpretacja if epworth else "-",
        "ipaq_score": ipaq.wynik_met if ipaq else None,
        "ipaq_score_display": _format_number(ipaq.wynik_met, 0) if ipaq else "-",
        "ipaq_kategoria": ipaq.kategoria if ipaq else "-",
        "fosq_score": fosq.wynik if fosq else None,
        "fosq_score_display": fosq_score_display,
        "fosq_status": fosq_status,
        "fosq_status_class": fosq_status_class,
        **{f"{section_key}_score": value for section_key, value in fosq_section_values.items()},
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


def _chart_items_from_scores(scores, ordered_keys, labels):
    max_value = max((scores.get(key, 0) or 0 for key in ordered_keys), default=0)
    items = []
    for key in ordered_keys:
        value = scores.get(key)
        width = int(round((float(value) / max_value) * 100)) if max_value and value is not None else 0
        items.append({"label": labels[key], "count": _format_number(value, 2), "width": width})
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
    fosq_scores = [record["fosq_score"] for record in records if record["fosq_score"] is not None]
    neck_values = [float(record["obwod_szyi"]) for record in records if record["obwod_szyi"] != "-"]

    stage_counter = Counter(record["etap"] for record in records if record["etap"] != "-")
    epworth_counter = Counter(record["epworth_interpretacja"] for record in records if record["epworth_interpretacja"] != "-")
    ipaq_counter = Counter(record["ipaq_kategoria"] for record in records if record["ipaq_kategoria"] != "-")
    neck_counter = Counter(record["obwod_szyi_status"] for record in records if record["obwod_szyi_status"] != "-")

    choroby_counter = Counter()
    for record in records:
        for choroba in record["choroby"] if isinstance(record["choroby"], list) else []:
            if choroba != "-":
                choroby_counter[choroba] += 1

    fosq_section_scores = Counter()
    fosq_section_labels = {}
    for section_key, section_title, _fields in FOSQ_SECTION_DEFINITIONS:
        fosq_section_labels[section_key] = section_title

    if records:
        for record in records:
            for section_key, section_title, _fields in FOSQ_SECTION_DEFINITIONS:
                key = f"{section_key}_score"
                value = record.get(key)
                if value is not None:
                    fosq_section_scores[section_key] += float(value)

    fosq_section_averages = {}
    for section_key, section_title, _fields in FOSQ_SECTION_DEFINITIONS:
        scores = [record.get(f"{section_key}_score") for record in records if record.get(f"{section_key}_score") is not None]
        fosq_section_averages[section_key] = _mean(scores)

    neck_counter_order = ["w normie", "Podwyższone ryzyko", "Wysokie ryzyko", "Poniżej normy"]
    neck_counter_map = Counter()
    for record in records:
        neck_counter_map[record["obwod_szyi_status"]] += 1

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
            "title": "Obwód szyi",
            "items": _chart_items(
                neck_counter_map,
                ["W normie", "Podwyższone ryzyko", "Wysokie ryzyko", "Poniżej normy"],
            ),
        },
        {
            "title": "Sekcje FOSQ",
            "items": _chart_items_from_scores(
                fosq_section_averages,
                [section_key for section_key, _title, _fields in FOSQ_SECTION_DEFINITIONS],
                fosq_section_labels,
            ),
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
        {"label": "Kompletne", "value": len(complete_records), "note": "Epworth, IPAQ i FOSQ"},
        {"label": "Średni wiek", "value": _format_number(_mean(ages), 1), "note": "lata"},
        {"label": "Średnie BMI", "value": _format_number(_mean(bmis), 1), "note": "kg/m²"},
        {"label": "Śr. FOSQ", "value": _format_number(_mean(fosq_scores), 2), "note": "pkt"},
        {"label": "Śr. obwód szyi", "value": _format_number(_mean(neck_values), 1), "note": "cm"},
        {"label": "Wysokie ryzyko szyi", "value": neck_counter_map.get("Wysokie ryzyko", 0), "note": "wg norm"},
    ]

    return {
        "filter_form": filter_form,
        "records": records,
        "stats": stats,
        "charts": charts,
    }
