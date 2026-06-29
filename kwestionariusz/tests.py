from django.test import TestCase

from .dashboard import build_dashboard_context, build_record_view, classify_neck_circumference
from .models import Badanie, Epworth, IPAQ, Pacjent, Pittsburgh


class DashboardHelpersTests(TestCase):
    def test_classify_neck_circumference_for_woman(self):
        result = classify_neck_circumference("kobieta", 34)
        self.assertEqual(result["key"], "w_normie")
        self.assertEqual(result["label"], "W normie")

    def test_classify_neck_circumference_for_man(self):
        result = classify_neck_circumference("mezczyzna", 44)
        self.assertEqual(result["key"], "wysokie_ryzyko")
        self.assertEqual(result["label"], "Wysokie ryzyko")


class FosqModelTests(TestCase):
    def test_fosq_scores_are_calculated(self):
        pacjent = Pacjent.objects.create(kod="TEST01")
        badanie = Badanie.objects.create(pacjent=pacjent)

        kwargs = {f"pytanie_{index}": 4 for index in range(1, 31)}
        fosq = Pittsburgh.objects.create(badanie=badanie, **kwargs)

        self.assertEqual(fosq.produktywnosc_wynik, 4)
        self.assertEqual(fosq.kontakty_spoleczne_wynik, 4)
        self.assertEqual(fosq.aktywnosc_wynik, 4)
        self.assertEqual(fosq.czujnosc_wynik, 4)
        self.assertEqual(fosq.intymnosc_wynik, 4)
        self.assertEqual(fosq.wynik, 20)

    def test_dashboard_context_handles_complete_record(self):
        pacjent = Pacjent.objects.create(kod="TEST02")
        badanie = Badanie.objects.create(
            pacjent=pacjent,
            plec="kobieta",
            masa_ciala=100,
            wzrost=170,
            obwod_szyi=34,
        )

        Epworth.objects.create(
            badanie=badanie,
            pytanie_1=0,
            pytanie_2=0,
            pytanie_3=0,
            pytanie_4=0,
            pytanie_5=0,
            pytanie_6=0,
            pytanie_7=0,
            pytanie_8=0,
        )

        IPAQ.objects.create(
            badanie=badanie,
            szpital=False,
            choroba=False,
            rehabilitacja=False,
            urlop=False,
            rekonwalescencja=False,
            ciaza=False,
            intensywne_dni=0,
            intensywne_minuty=0,
            umiarkowane_dni=0,
            umiarkowane_minuty=0,
            chodzenie_dni=0,
            chodzenie_minuty=0,
            siedzenie_minuty_dziennie=0,
        )

        kwargs = {f"pytanie_{index}": 4 for index in range(1, 31)}
        Pittsburgh.objects.create(badanie=badanie, **kwargs)

        record = build_record_view(Badanie.objects.get(pk=badanie.pk))
        ctx = build_dashboard_context(Badanie.objects.filter(pk=badanie.pk))

        self.assertEqual(record["fosq_score"], 20)
        self.assertEqual(record["obwod_szyi_status"], "W normie")
        self.assertEqual(len(ctx["records"]), 1)

    def test_dashboard_context_handles_choroby_lists(self):
        pacjent = Pacjent.objects.create(kod="TEST03")
        badanie = Badanie.objects.create(
            pacjent=pacjent,
            plec="kobieta",
            choroby="nadcisnienie, inne",
            choroby_inne="Hashimoto",
        )

        Epworth.objects.create(
            badanie=badanie,
            pytanie_1=0,
            pytanie_2=0,
            pytanie_3=0,
            pytanie_4=0,
            pytanie_5=0,
            pytanie_6=0,
            pytanie_7=0,
            pytanie_8=0,
        )

        IPAQ.objects.create(
            badanie=badanie,
            szpital=False,
            choroba=False,
            rehabilitacja=False,
            urlop=False,
            rekonwalescencja=False,
            ciaza=False,
            intensywne_dni=0,
            intensywne_minuty=0,
            umiarkowane_dni=0,
            umiarkowane_minuty=0,
            chodzenie_dni=0,
            chodzenie_minuty=0,
            siedzenie_minuty_dziennie=0,
        )

        kwargs = {f"pytanie_{index}": 4 for index in range(1, 31)}
        Pittsburgh.objects.create(badanie=badanie, **kwargs)

        record = build_record_view(Badanie.objects.get(pk=badanie.pk))
        ctx = build_dashboard_context(Badanie.objects.filter(pk=badanie.pk))

        self.assertEqual(record["choroby_display"], ["Nadciśnienie tętnicze", "Inne: Hashimoto"])
        self.assertEqual(ctx["charts"][-1]["items"][0]["label"], "Nadciśnienie tętnicze")
        self.assertEqual(len(ctx["records"]), 1)
