from statistics import fmean

from django.db import models


FOSQ_SECTION_ITEMS = {
    "produktywnosc": [1, 2, 3, 4, 8, 9, 10, 11],
    "kontakty_spoleczne": [12, 13],
    "aktywność": [5, 14, 15, 16, 21, 22, 23, 24, 30],
    "czujność": [6, 7, 17, 18, 19, 20],
    "intymnosc": [25, 26, 27, 28, 29],
}


class Pacjent(models.Model):
    kod = models.CharField(max_length=20, unique=True)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.kod


class Badanie(models.Model):
    ETAP_CHOICES = [
        ("0", "Etap 0 (Początek obserwacji)"),
        ("1", "Etap I (6 miesięcy od pierwszego badania)"),
        ("2", "Etap II (12 miesięcy od pierwszego badania)"),
    ]

    PLEC_CHOICES = [
        ("kobieta", "Kobieta"),
        ("mezczyzna", "Mężczyzna"),
    ]

    pacjent = models.ForeignKey(Pacjent, on_delete=models.CASCADE, related_name="badania")
    data_badania = models.DateTimeField(auto_now_add=True)

    etap = models.CharField(max_length=10, choices=ETAP_CHOICES, blank=True)
    plec = models.CharField(max_length=20, choices=PLEC_CHOICES, blank=True)
    wiek = models.PositiveIntegerField(null=True, blank=True)
    masa_ciala = models.FloatField(null=True, blank=True)
    wzrost = models.FloatField(null=True, blank=True)

    operacja_bariatryczna = models.BooleanField(default=False)
    data_operacji_bariatrycznej = models.CharField(max_length=50, blank=True)
    maksymalna_masa_przed_operacja = models.FloatField(null=True, blank=True)

    cpap = models.CharField(max_length=100, blank=True)
    cpap_czas_stosowania = models.CharField(max_length=100, blank=True)
    cpap_godziny_snu = models.CharField(max_length=50, blank=True)
    cpap_zmiana_cisnienia = models.CharField(max_length=100, blank=True)

    choroby = models.TextField(blank=True)
    choroby_inne = models.TextField(blank=True)
    fizjoterapia = models.CharField(max_length=100, blank=True)
    charakter_aktywnosci = models.CharField(max_length=100, blank=True)
    alkohol_przed_snem = models.CharField(max_length=100, blank=True)
    palenie = models.BooleanField(default=False)
    pozycja_snu = models.CharField(max_length=100, blank=True)
    obwod_szyi = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.pacjent.kod} - {self.data_badania.strftime('%d.%m.%Y %H:%M')}"


class Epworth(models.Model):
    badanie = models.OneToOneField(Badanie, on_delete=models.CASCADE, related_name="epworth")

    pytanie_1 = models.IntegerField()
    pytanie_2 = models.IntegerField()
    pytanie_3 = models.IntegerField()
    pytanie_4 = models.IntegerField()
    pytanie_5 = models.IntegerField()
    pytanie_6 = models.IntegerField()
    pytanie_7 = models.IntegerField()
    pytanie_8 = models.IntegerField()

    wynik = models.IntegerField(default=0)
    data_wypelnienia = models.DateTimeField(auto_now_add=True)
    interpretacja = models.CharField(max_length=100, blank=True)

    def oblicz_wynik(self):
        return (
            self.pytanie_1
            + self.pytanie_2
            + self.pytanie_3
            + self.pytanie_4
            + self.pytanie_5
            + self.pytanie_6
            + self.pytanie_7
            + self.pytanie_8
        )

    def okresl_interpretacje(self):
        if self.wynik <= 10:
            return "wynik prawidłowy"
        if self.wynik <= 14:
            return "łagodna senność"
        if self.wynik <= 18:
            return "umiarkowana senność"
        return "ciężka senność"

    def save(self, *args, **kwargs):
        self.wynik = self.oblicz_wynik()
        self.interpretacja = self.okresl_interpretacje()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Epworth - {self.badanie.pacjent.kod} - {self.wynik} pkt"


class IPAQ(models.Model):
    badanie = models.OneToOneField(Badanie, on_delete=models.CASCADE, related_name="ipaq")

    szpital = models.BooleanField(default=False)
    choroba = models.BooleanField(default=False)
    rehabilitacja = models.BooleanField(default=False)
    urlop = models.BooleanField(default=False)
    rekonwalescencja = models.BooleanField(default=False)
    ciaza = models.BooleanField(default=False)

    intensywne_dni = models.IntegerField(default=0)
    intensywne_minuty = models.IntegerField(default=0)
    umiarkowane_dni = models.IntegerField(default=0)
    umiarkowane_minuty = models.IntegerField(default=0)
    chodzenie_dni = models.IntegerField(default=0)
    chodzenie_minuty = models.IntegerField(default=0)
    siedzenie_minuty_dziennie = models.IntegerField(default=0)

    wynik_met = models.FloatField(default=0)
    kategoria = models.CharField(max_length=50, blank=True)
    data_wypelnienia = models.DateTimeField(auto_now_add=True)

    def oblicz_wynik_met(self):
        intensywne = 8.0 * self.intensywne_minuty * self.intensywne_dni
        umiarkowane = 4.0 * self.umiarkowane_minuty * self.umiarkowane_dni
        chodzenie = 3.3 * self.chodzenie_minuty * self.chodzenie_dni
        return intensywne + umiarkowane + chodzenie

    def okresl_kategorie(self):
        if self.wynik_met < 600:
            return "niewystarczająca"
        if self.wynik_met < 3000:
            return "dostateczna"
        return "wysoka"

    def save(self, *args, **kwargs):
        self.wynik_met = self.oblicz_wynik_met()
        self.kategoria = self.okresl_kategorie()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"IPAQ - {self.badanie.pacjent.kod} - {self.kategoria}"


class Pittsburgh(models.Model):
    badanie = models.OneToOneField(Badanie, on_delete=models.CASCADE, related_name="pittsburgh")

    pytanie_1 = models.PositiveSmallIntegerField(default=0)
    pytanie_2 = models.PositiveSmallIntegerField(default=0)
    pytanie_3 = models.PositiveSmallIntegerField(default=0)
    pytanie_4 = models.PositiveSmallIntegerField(default=0)
    pytanie_5 = models.PositiveSmallIntegerField(default=0)
    pytanie_6 = models.PositiveSmallIntegerField(default=0)
    pytanie_7 = models.PositiveSmallIntegerField(default=0)
    pytanie_8 = models.PositiveSmallIntegerField(default=0)
    pytanie_9 = models.PositiveSmallIntegerField(default=0)
    pytanie_10 = models.PositiveSmallIntegerField(default=0)
    pytanie_11 = models.PositiveSmallIntegerField(default=0)
    pytanie_12 = models.PositiveSmallIntegerField(default=0)
    pytanie_13 = models.PositiveSmallIntegerField(default=0)
    pytanie_14 = models.PositiveSmallIntegerField(default=0)
    pytanie_15 = models.PositiveSmallIntegerField(default=0)
    pytanie_16 = models.PositiveSmallIntegerField(default=0)
    pytanie_17 = models.PositiveSmallIntegerField(default=0)
    pytanie_18 = models.PositiveSmallIntegerField(default=0)
    pytanie_19 = models.PositiveSmallIntegerField(default=0)
    pytanie_20 = models.PositiveSmallIntegerField(default=0)
    pytanie_21 = models.PositiveSmallIntegerField(default=0)
    pytanie_22 = models.PositiveSmallIntegerField(default=0)
    pytanie_23 = models.PositiveSmallIntegerField(default=0)
    pytanie_24 = models.PositiveSmallIntegerField(default=0)
    pytanie_25 = models.PositiveSmallIntegerField(default=0)
    pytanie_26 = models.PositiveSmallIntegerField(default=0)
    pytanie_27 = models.PositiveSmallIntegerField(default=0)
    pytanie_28 = models.PositiveSmallIntegerField(default=0)
    pytanie_29 = models.PositiveSmallIntegerField(default=0)
    pytanie_30 = models.PositiveSmallIntegerField(default=0)

    produktywnosc_wynik = models.FloatField(null=True, blank=True)
    kontakty_spoleczne_wynik = models.FloatField(null=True, blank=True)
    aktywnosc_wynik = models.FloatField(null=True, blank=True)
    czujnosc_wynik = models.FloatField(null=True, blank=True)
    intymnosc_wynik = models.FloatField(null=True, blank=True)

    wynik = models.FloatField(null=True, blank=True)
    data_wypelnienia = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "FOSQ"
        verbose_name_plural = "FOSQ"

    def _question_value(self, number):
        return getattr(self, f"pytanie_{number}", 0) or 0

    def _section_score(self, item_numbers):
        values = [self._question_value(number) for number in item_numbers if self._question_value(number) > 0]
        if not values:
            return None
        return round(fmean(values), 2)

    def oblicz_wyniki(self):
        self.produktywnosc_wynik = self._section_score(FOSQ_SECTION_ITEMS["produktywnosc"])
        self.kontakty_spoleczne_wynik = self._section_score(FOSQ_SECTION_ITEMS["kontakty_spoleczne"])
        self.aktywnosc_wynik = self._section_score(FOSQ_SECTION_ITEMS["aktywność"])
        self.czujnosc_wynik = self._section_score(FOSQ_SECTION_ITEMS["czujność"])
        self.intymnosc_wynik = self._section_score(FOSQ_SECTION_ITEMS["intymnosc"])

        section_scores = [
            score
            for score in [
                self.produktywnosc_wynik,
                self.kontakty_spoleczne_wynik,
                self.aktywnosc_wynik,
                self.czujnosc_wynik,
                self.intymnosc_wynik,
            ]
            if score is not None
        ]

        self.wynik = round(fmean(section_scores) * len(section_scores), 2) if section_scores else None

    def save(self, *args, **kwargs):
        self.oblicz_wyniki()
        super().save(*args, **kwargs)

    def __str__(self):
        wynik = f"{self.wynik:.2f}" if self.wynik is not None else "-"
        return f"FOSQ - {self.badanie.pacjent.kod} - {wynik} pkt"
