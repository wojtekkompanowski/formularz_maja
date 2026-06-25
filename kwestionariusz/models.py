from django.db import models


class Pacjent(models.Model):
    kod = models.CharField(max_length=20, unique=True)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.kod

class Badanie(models.Model):
    ETAP_CHOICES = [
        ('0', 'Etap 0 (Początek obserwacji)'),
        ('1', 'Etap I (6 miesięcy od pierwszego badania)'),
        ('2', 'Etap II (12 miesięcy od pierwszego badania)'),
    ]

    PLEC_CHOICES = [
        ('kobieta', 'Kobieta'),
        ('mezczyzna', 'Mężczyzna'),
    ]

    pacjent = models.ForeignKey(Pacjent, on_delete=models.CASCADE, related_name='badania')
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
    fizjoterapia = models.CharField(max_length=100, blank=True)
    charakter_aktywnosci = models.CharField(max_length=100, blank=True)
    alkohol_przed_snem = models.CharField(max_length=100, blank=True)
    palenie = models.BooleanField(default=False)
    pozycja_snu = models.CharField(max_length=100, blank=True)
    obwod_szyi = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.pacjent.kod} - {self.data_badania.strftime('%d.%m.%Y %H:%M')}"


class Epworth(models.Model):
    badanie = models.OneToOneField(Badanie, on_delete=models.CASCADE, related_name='epworth')

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
            self.pytanie_1 +
            self.pytanie_2 +
            self.pytanie_3 +
            self.pytanie_4 +
            self.pytanie_5 +
            self.pytanie_6 +
            self.pytanie_7 +
            self.pytanie_8
        )

    def okresl_interpretacje(self):
        if self.wynik <= 10:
            return "wynik prawidłowy"
        elif self.wynik <= 14:
            return "łagodna senność"
        elif self.wynik <= 18:
            return "umiarkowana senność"
        return "ciężka senność"

    def save(self, *args, **kwargs):
        self.wynik = self.oblicz_wynik()
        self.interpretacja = self.okresl_interpretacje()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Epworth - {self.badanie.pacjent.kod} - {self.wynik} pkt"


class IPAQ(models.Model):
    badanie = models.OneToOneField(Badanie, on_delete=models.CASCADE, related_name='ipaq')

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
        elif self.wynik_met < 3000:
            return "dostateczna"
        return "wysoka"

    def save(self, *args, **kwargs):
        self.wynik_met = self.oblicz_wynik_met()
        self.kategoria = self.okresl_kategorie()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"IPAQ - {self.badanie.pacjent.kod} - {self.kategoria}"


class Pittsburgh(models.Model):
    badanie = models.OneToOneField(Badanie, on_delete=models.CASCADE, related_name='pittsburgh')

    godzina_polozenia = models.TimeField(null=True, blank=True)
    czas_zasypiania_minuty = models.IntegerField(default=0)
    godzina_wstawania = models.TimeField(null=True, blank=True)
    godziny_snu = models.FloatField(default=0)

    nie_zasnal_30_min = models.IntegerField(default=0)
    pobudka_w_nocy = models.IntegerField(default=0)
    toaleta = models.IntegerField(default=0)
    problemy_z_oddychaniem = models.IntegerField(default=0)
    kaszel_chrapanie = models.IntegerField(default=0)
    za_zimno = models.IntegerField(default=0)
    za_cieplo = models.IntegerField(default=0)
    zle_sny = models.IntegerField(default=0)
    bol = models.IntegerField(default=0)
    inne_powody = models.IntegerField(default=0)
    inne_powody_opis = models.TextField(blank=True)

    jakosc_snu = models.IntegerField(default=0)
    leki_nasenne = models.IntegerField(default=0)
    problemy_z_czuwaniem = models.IntegerField(default=0)
    brak_energii = models.IntegerField(default=0)

    wynik = models.IntegerField(default=0)
    data_wypelnienia = models.DateTimeField(auto_now_add=True)

    def oblicz_wynik(self):
        return (
            self.jakosc_snu +
            self.nie_zasnal_30_min +
            self.pobudka_w_nocy +
            self.toaleta +
            self.problemy_z_oddychaniem +
            self.kaszel_chrapanie +
            self.za_zimno +
            self.za_cieplo +
            self.zle_sny +
            self.bol +
            self.inne_powody +
            self.leki_nasenne +
            self.problemy_z_czuwaniem +
            self.brak_energii
        )

    def save(self, *args, **kwargs):
        self.wynik = self.oblicz_wynik()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pittsburgh - {self.badanie.pacjent.kod} - {self.wynik} pkt"