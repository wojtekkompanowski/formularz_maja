# Formularz Maja

Aplikacja Django do zbierania danych pacjentów i panelu z wynikami, filtrami oraz statystykami.

## Uruchomienie lokalne

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

## Wdrożenie na VPS

1. Skopiuj projekt na serwer, najlepiej do `/srv/formularz_maja`.
2. Utwórz plik środowiskowy na bazie `.env.example`, np. `/etc/formularz_maja/formularz_maja.env`.
3. Ustaw co najmniej:
   - `DEBUG=0`
   - `SECRET_KEY=...`
   - `ALLOWED_HOSTS=twojadomena.pl,www.twojadomena.pl`
   - `CSRF_TRUSTED_ORIGINS=https://twojadomena.pl,https://www.twojadomena.pl`
4. Jeśli chcesz PostgreSQL, ustaw `DATABASE_URL`.
5. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
6. Wykonaj migracje i zbierz statyczne pliki:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
7. Utwórz konto administracyjne:
   ```bash
   python manage.py createsuperuser
   ```
8. Włącz usługę `gunicorn` i skonfiguruj Nginx z plików w `deploy/`.

## Domeny i HTTPS

1. Ustaw rekord `A` domeny na adres IP VPS.
2. Skonfiguruj Nginx jako reverse proxy do `127.0.0.1:8000`.
3. Wygeneruj certyfikat SSL, np. przez Certbot.
4. Po wdrożeniu sprawdź panel pod domeną i potwierdź, że `ALLOWED_HOSTS` oraz `CSRF_TRUSTED_ORIGINS` zawierają właściwe adresy.

## Pliki wdrożeniowe

- `deploy/systemd/gunicorn.service`
- `deploy/nginx/formularz_maja.conf`
