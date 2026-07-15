# 🥙 KebabRank Poland — AI-Powered Kebab Ranking Platform

[![Website](https://img.shields.io/badge/Website-kebabrank.com-orange)](https://kebabrank.com)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com/)
[![PocketBase](https://img.shields.io/badge/Database-PocketBase-blue)](https://pocketbase.io)

> Ostatnia aktualizacja dokumentu: **2026-07-15**

---

## 📋 Spis treści

1. [Overview](#overview)
2. [Architektura](#architektura)
3. [Stack techniczny](#stack-techniczny)
4. [Struktura projektu](#struktura-projektu)
5. [Frontend — co zostało zbudowane](#frontend--co-zostało-zbudowane)
6. [Filtry i sortowanie](#filtry-i-sortowanie)
7. [Kebab Ruletka](#kebab-ruletka)
8. [System zbierania emaili](#system-zbierania-emaili)
9. [Scoring — algorytm rankingowy](#scoring--algorytm-rankingowy)
10. [Aktualizacja danych — skrypty](#aktualizacja-danych--skrypty)
11. [Konfiguracja środowiska](#konfiguracja-środowiska)
12. [Deployment (Hostinger VPS)](#deployment-hostinger-vps)
13. [Przydatne komendy](#przydatne-komendy)
14. [Troubleshooting](#troubleshooting)

---

## 🌟 Overview

KebabRank to pierwszy w Polsce AI-powered ranking kebabów. Łączy dane z Google Maps z analizą sentymentu (DeepSeek) i dostarcza rankingi dla 64+ miast.

**Trzy filary systemu:**
1. **Smart Filtering** — weryfikacja adresów przez regex (kod pocztowy) eliminuje "duchy" z sąsiednich miast
2. **Historical Trends** — timestampowane rekordy historyczne zapewniają dokładne strzałki trendu
3. **AI Sentiment Analysis** — DeepSeek analizuje recenzje klientów i generuje polskie podsumowania

---

## 🏗️ Architektura

```
┌──────────────────────────────────────────────────────────┐
│                        Frontend                           │
│        Vanilla JS (app.js) + Tailwind + Leaflet.js        │
│   Filtry · Sortowanie · Mapa · Ruletka · Email capture    │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│                   Flask Backend (app.py)                   │
│   API Routes · Ranking Logic · AI Processing · Subscribe  │
└────────┬──────────────┬──────────────────┬───────────────┘
         │              │                  │
┌────────▼───────┐ ┌────▼──────┐ ┌────────▼────────┐
│  DataForSEO /  │ │ PocketBase│ │  DeepSeek API   │
│ GmapsExtractor │ │ (SQLite)  │ │  (DeepSeek-R1)  │
└────────────────┘ └───────────┘ └─────────────────┘
                                         +
                                  ┌──────▼──────────┐
                                  │ subscribers.db  │
                                  │ (email list)    │
                                  └─────────────────┘
```

---

## 💻 Stack techniczny

### Backend
- **Framework**: Flask 2.3.3 (Python 3.10+)
- **WSGI Server**: Gunicorn (produkcja), Werkzeug dev server (lokalnie)
- **Baza danych rankingów**: PocketBase (Go backend, silnik SQLite)
- **Baza emaili**: `subscribers.db` — osobny plik SQLite w katalogu projektu
- **AI**: DeepSeek-R1 (analiza sentymentu + polskie streszczenia)
- **Dane GMaps**: DataForSEO ($0.60/1k req) lub GmapsExtractor ($15/1k req) jako backup

### Frontend
- **Core**: Vanilla JavaScript ES6+ (`static/js/app.js` ~3000 linii)
- **Build**: Terser minifier → `app.min.js` (`npm run build:js`)
- **Mapy**: Leaflet.js (OpenStreetMap tiles, zero kosztów)
- **Stylowanie**: Tailwind CSS (utility classes) + `style.min.css` (custom)
- **Cache busting**: `app.js?v=18` — inkrementuj przy każdym deploy

---

## 📁 Struktura projektu

```
kebsioronredesign/
│
├── app.py                        # Flask app: routing, API, subscribe endpoint
├── requirements.txt
├── .env                          # Klucze API (nigdy nie commituj!)
├── subscribers.db                # Lista emaili (nigdy nie commituj! — w .gitignore)
│
├── services/
│   ├── pocketbase_db.py          # PocketBase: CRUD + trend preservation
│   ├── gmaps_extractor.py        # GmapsExtractor API integration
│   ├── ranking.py                # Algorytm scoringowy 85/15
│   ├── ai_service.py             # DeepSeek: sentiment + AI summary
│   └── ai_data_updater.py        # Batch AI processing
│
├── templates/
│   ├── base.html                 # Layout bazowy, <script app.js?v=18>
│   ├── index.html                # Główna SPA (filtry, mapa, ruletka)
│   └── blog/                     # Artykuły SEO (HTML)
│
├── static/
│   ├── js/
│   │   ├── app.js                # GŁÓWNY PLIK FRONTENDU
│   │   └── app.min.js            # Zminifikowany (generowany, nie edytuj!)
│   ├── css/
│   │   ├── tailwind.min.css
│   │   └── style.min.css
│   └── img/cities/               # Webp thumbnails miast
│
├── update_city_gmaps.py          # Aktualizacja rankingu dla 1 miasta
├── rank_batch.py                 # Batch update wielu miast
├── debug_gmaps_fields.py         # Debugowanie pól z API GMaps
├── package.json                  # { "build:js": "terser app.js -o app.min.js --compress --mangle" }
└── .claude/launch.json           # Dev server config dla Claude Code preview
```

---

## 🖥️ Frontend — co zostało zbudowane

Cały frontend żyje w `static/js/app.js`. Kluczowe zmienne globalne:

```javascript
window.cityRankingData    // tablica miejsc dla aktywnego miasta
window.globalRankingData  // tablica TOP miejsc globalnie
window.activeFilters      // { city: {open_now, nocne, sort}, global: {..., voivodeship} }
window.kebabMap           // instancja Leaflet (mapa miasta)
window.globalKebabMap     // instancja Leaflet (mapa globalna)
```

### Główne funkcje

| Funkcja | Co robi |
|---|---|
| `displayRankings(rankings, container, city, isGlobal)` | Renderuje karty rankingu + filter bar |
| `buildFilterBar(isGlobal, rankings)` | Buduje sticky header z przyciskiem Filtry + rozwijany panel |
| `applyRankingFilter(type, isGlobal)` | Obsługuje klik filtra/sortu — filtruje dane, re-renderuje karty i mapę |
| `syncMobileMapFilter(isGlobal)` | Renderuje overlay filtrów nad mapą w widoku mobilnym |
| `openRouletteModal(isGlobal)` | Otwiera modal Ruletki |
| `spinRoulette(isGlobal)` | Losuje miejsce (z uwzględnieniem topN i trybu "tylko otwarte") |
| `updateMapWithKebabs(data)` | Aktualizuje markery na mapie miasta |
| `updateGlobalMapWithKebabs(data)` | Aktualizuje markery na mapie globalnej |
| `isNightKebab(openingHoursJson)` | Zwraca true jeśli lokal zamyka się po północy |
| `getOpenNowStatus(openingHoursJson)` | Zwraca `{open: bool, label: string}` na podstawie aktualnej godziny |
| `applySortToData(data, sort)` | Sortuje tablicę wg 'score' / 'rating' / 'reviews' |

---

## 🔽 Filtry i sortowanie

### Stan filtrów

```javascript
window.activeFilters = {
    city:   { open_now: false, nocne: false, sort: 'score' },
    global: { open_now: false, nocne: false, sort: 'score', voivodeship: '' }
}
```

Reset następuje przy zmianie miasta (`selectCity()`). Filtr i sort nakładają się — np. "Otwarte" + "★ Ocena" = otwarte miejsca posortowane po gwiazdkach.

### Dostępne filtry

| ID | Co robi |
|---|---|
| `open_now` | Tylko miejsca otwarte w tej chwili (liczy z `opening_hours` JSON) |
| `nocne` | Miejsca zamykające się po północy (do 9:00) |
| `voivodeship` | Tylko w trybie globalnym — filtruje po województwie |

### Dostępne sorty

| Wartość `sort` | Logika |
|---|---|
| `'score'` | Domyślny — wg `rank_score` (wynik KebabRank) |
| `'rating'` | Wg gwiazdek Google; remis → wygrywa więcej recenzji |
| `'reviews'` | Wg liczby recenzji (`total_reviews`); remis → wygrywa wyższa ocena |

### UI — jak działa filter bar

**Sidebar (desktop + mobile lista):**
- Sticky header z przyciskiem `⚙ Filtry ▾`
- Klik → panel inline z sekcją FILTRUJ i SORTUJ WG
- Aktywny filtr/sort → przycisk zielony + dot ●
- `✕ Kasuj` pojawia się gdy cokolwiek aktywne — resetuje WSZYSTKO (filtry + sort)
- Klik poza panelem → zamknięcie

**Mobile widok mapy (`#mobile-map-filterbar`):**
- Overlay `position:absolute` nad mapą
- Ten sam design trigger+panel
- Stan otwarcia panelu zapamiętany w `window.mobileFilterPanelOpen`
- Re-renderowany przez `syncMobileMapFilter(isGlobal)` po każdej zmianie filtra

### Tooltips (ⓘ)

```javascript
const FILTER_TIPS = { pl: { sort_score, sort_rating, sort_reviews, open_now, nocne }, en: {...} }
function showFilterTooltip(event, key)  // tworzy #filter-tooltip, auto-hide po 5s
```

---

## 🎲 Kebab Ruletka

Funkcja wirusowa — losuje kebab z aktualnego rankingu.

### Jak uruchomić
Przycisk `🎲 Ruletka` pojawia się w nagłówku filter bara każdego rankingu (miasto + globalny).

### Logika

```javascript
openRouletteModal(isGlobal)   // buduje modal HTML, wstrzykuje do body
spinRoulette(isGlobal)        // losuje z puli, animuje 1.6s, pokazuje wynik
closeRouletteModal()          // usuwa #roulette-overlay z DOM
rouletteSubscribe(kebabName)  // wysyła email na /api/subscribe
```

### Smart Top N

Automatycznie dobiera opcje do rozmiaru rankingu:

| Liczba miejsc | Opcje selekcji |
|---|---|
| ≤ 5 | brak selekcji — losuje ze wszystkich |
| 6–15 | Top 5 / Wszystkie (N) |
| 16–25 | Top 5 / Top 10 / Wszystkie (N) |
| 26+ | Top 5 / Top 10 / Top 20 / Wszystkie (N) |

### Checkbox "Tylko otwarte teraz"

Domyślnie zaznaczony. Filtruje pulę losowania do miejsc aktualnie otwartych.
Jeśli żadne miejsce w wybranej puli nie jest otwarte → komunikat zamiast kręcenia.

### Wynik ruletki zawiera
- Pozycja w rankingu + nazwa + miasto (tryb globalny)
- Gwiazdki + liczba recenzji
- Status otwarcia (z `getOpenNowStatus`)
- Przycisk `🗺️ Prowadź` → Google Maps navigation deep-link (bezpłatny, zero API)
- Pole email → `📱 Wyślij na maila` → zapisuje do `subscribers.db`

---

## 📧 System zbierania emaili

### Endpoint

```
POST /api/subscribe
Content-Type: application/json
{ "email": "user@example.com", "source": "roulette" }
```

Odpowiedź: `{ "ok": true }` lub `{ "error": "invalid_email" }`

Duplikaty są ignorowane (INSERT OR IGNORE). Źródła: `roulette`, `city_watch`, `footer` (rozszerzaj w miarę dodawania punktów zapisu).

### Podgląd listy

```
GET /api/subscribers/export?key=<ADMIN_KEY>
```

Zwraca JSON z listą emaili. Klucz pochodzi z `.env`:
```env
ADMIN_KEY=kebab2024adminkey
```

**W przeglądarce lokalnie:**
```
http://localhost:5001/api/subscribers/export?key=kebab2024adminkey
```

**Na produkcji:**
```
https://kebabrank.com/api/subscribers/export?key=kebab2024adminkey
```

### Baza danych `subscribers.db`

Plik SQLite w katalogu projektu (`/`). Schemat:
```sql
CREATE TABLE subscribers (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    email      TEXT UNIQUE NOT NULL,
    source     TEXT,
    created_at TEXT
);
```

> **WAŻNE:** `subscribers.db` jest w `.gitignore` — nigdy nie trafi na GitHub.
> Na Hostingerze plik żyje na serwerze niezależnie od deploymentów.

### Skrypt eksportu emaili (Python)

```python
import sqlite3
conn = sqlite3.connect('subscribers.db')
rows = conn.execute('SELECT email, source, created_at FROM subscribers ORDER BY id').fetchall()
for r in rows:
    print(f"{r[2][:10]} | {r[1]:12} | {r[0]}")
conn.close()
```

### Migracja do Resend (gdy lista > 50 emaili)

1. Załóż konto na resend.com (darmowy plan: 3000 maili/mc)
2. Eksportuj: `GET /api/subscribers/export?key=...` → skopiuj emaile
3. Zaimportuj do Resend Audiences
4. Wyślij pierwszy "KebabRank Update" z podsumowaniem nowych miejsc

---

## 📊 Scoring — algorytm rankingowy

### Formuła (85/15)

```
rank_score = (rating / 5.0 * 100 * 0.85) + (min(log10(reviews + 1) / 3 * 100, 100) * 0.15)
```

- **85%** — znormalizowana ocena Google (0–5 gwiazdek → 0–85 pkt)
- **15%** — logarytmiczna skala liczby recenzji (wiarygodność)
- Efekt: 4.9 przy 500 recenzjach > 5.0 przy 2 recenzjach

### Pola w PocketBase (`kebab_places`)

| Pole | Typ | Opis |
|---|---|---|
| `name` | string | Nazwa lokalu |
| `city` | string | Miasto |
| `address` | string | Adres |
| `rating` | float | Ocena Google (0–5) |
| `total_reviews` | int | Liczba recenzji |
| `rank_score` | float | Wynik KebabRank (wyższy = lepszy) |
| `latitude` | float | Szerokość geograficzna |
| `longitude` | float | Długość geograficzna |
| `opening_hours` | JSON | Godziny otwarcia (wg dni tygodnia) |
| `ai_summary` | string | AI streszczenie po polsku |
| `ai_sentiment` | float | Sentyment (-1 do 1) |
| `place_id` | string | Google Place ID |

### Format `opening_hours` JSON

```json
{
  "0": { "openMin": 600,  "closeMin": 1320 },
  "1": { "openMin": 600,  "closeMin": 1320 },
  "5": { "openMin": 600,  "closeMin": 90   },
  "6": { "openMin": 600,  "closeMin": 90   }
}
```

Dni: 0=pon, 1=wt, ..., 6=nd. `closeMin < openMin` = zamknięcie po północy.
Brak klucza dla danego dnia = lokal zamknięty.

---

## 🔄 Aktualizacja danych — skrypty

### Aktualizacja 1 miasta

```bash
python update_city_gmaps.py "Kraków"
```

Co robi:
1. Pobiera dane z GmapsExtractor / DataForSEO
2. Filtruje po kodzie pocztowym (eliminacja duchów)
3. Oblicza rank_score
4. Porównuje z poprzednim rankingiem → strzałki trendu
5. Zapisuje do PocketBase

### Batch update wielu miast

```bash
python rank_batch.py
```

Konfiguracja listy miast wewnątrz pliku.

### Debug pól z API

```bash
python debug_gmaps_fields.py
```

Pokazuje surowe pola zwracane przez GmapsExtractor — przydatne przy sprawdzeniu czy `opening_hours` jest w payloadzie.

### Build frontendu (po każdej zmianie app.js)

```bash
npm run build:js
```

Terser minifikuje `static/js/app.js` → `static/js/app.min.js`.

**Po buildzie:** zaktualizuj wersję w `templates/base.html`:
```html
<script src="{{ url_for('static', filename='js/app.js') }}?v=19" defer></script>
```
Inkrementuj `v=` przy każdym deploy na produkcję.

---

## ⚙️ Konfiguracja środowiska

### `.env` (wymagane klucze)

```env
# PocketBase
PB_URL=https://your-pocketbase-url.com
PB_EMAIL=admin@kebabrank.com
PB_PASSWORD=your_secure_password

# Dane GMaps (wybierz jedno źródło)
GMAPS_EXTRACTOR_API_KEY=your_key     # $15/1k req
DATAFORSEO_LOGIN=your_login          # $0.60/1k req (tańsze)
DATAFORSEO_PASSWORD=your_password

# AI
DEEPSEEK_API_KEY=your_deepseek_key

# Admin
ADMIN_KEY=kebab2024adminkey          # Klucz do /api/subscribers/export
```

### `.claude/launch.json` (dev server)

```json
{
  "version": "0.0.1",
  "configurations": [{
    "name": "kebabrank-dev",
    "runtimeExecutable": "C:\\Users\\krypt\\Projekty\\kebsioronredesign\\venv\\Scripts\\python.exe",
    "runtimeArgs": ["app.py"],
    "port": 5001,
    "autoPort": false
  }]
}
```

---

## 🚢 Deployment (Hostinger VPS)

```bash
# Pull zmian
git pull origin master

# Rebuild JS (jeśli zmieniałeś app.js)
npm run build:js

# Restart Dockera
docker-compose -f docker-compose.prod.yml up -d --build

# Sprawdź logi
docker logs -f kebabrank_app
```

**Po deploymencie sprawdź:**
- [ ] `https://kebabrank.com/api/subscribers/export?key=...` — endpoint emaili działa
- [ ] `subscribers.db` istnieje na serwerze (nie jest kasowany przy deployu!)
- [ ] Wersja `app.js?v=X` jest zaktualizowana w `base.html`

> **Ważne:** `subscribers.db` żyje na serwerze. Przy `docker-compose up --build`
> upewnij się że volume jest zamontowany tak, żeby plik przeżył rebuild kontenera.
> Dodaj do `docker-compose.prod.yml`:
> ```yaml
> volumes:
>   - ./subscribers.db:/app/subscribers.db
> ```

---

## 🛠️ Przydatne komendy

```bash
# Podgląd wszystkich maili subskrybentów (lokalnie)
python -c "
import sqlite3
conn = sqlite3.connect('subscribers.db')
rows = conn.execute('SELECT id, email, source, created_at FROM subscribers ORDER BY id DESC').fetchall()
print(f'Łącznie: {len(rows)} emaili')
for r in rows:
    print(f'  #{r[0]} | {r[3][:10]} | {r[2]:12} | {r[1]}')
conn.close()
"

# Eksport emaili do pliku .txt
python -c "
import sqlite3
conn = sqlite3.connect('subscribers.db')
rows = conn.execute('SELECT email FROM subscribers ORDER BY id').fetchall()
with open('emails_export.txt', 'w') as f:
    f.write('\n'.join(r[0] for r in rows))
print(f'Wyeksportowano {len(rows)} emaili do emails_export.txt')
conn.close()
"

# Sprawdź czy port 5001 jest zajęty (Windows)
netstat -ano | findstr :5001

# Build JS + podgląd rozmiaru
npm run build:js && ls -lh static/js/app.min.js
```

---

## 🔧 Troubleshooting

**Mapa nie aktualizuje się po filtrze:**
Filtrowanie odbywa się w `displayRankings` — upewnij się że `updateMapWithKebabs(dataToRender)` jest wywoływane po filtrowaniu, nie przed.

**Filtry nie działają po zmianie miasta:**
`window.activeFilters.city` jest resetowane w `selectCity()`. Globalne filtry (`activeFilters.global`) przeżywają zmianę miasta.

**Modal Ruletki nie losuje otwartych:**
Sprawdź czy `opening_hours` jest w danych PocketBase. Pole musi być poprawnym JSON-em. Debug: `console.log(window.cityRankingData[0].opening_hours)`.

**Google Maps deep-link nie działa:**
Pola `latitude`/`longitude` muszą być liczbami (nie null). Sprawdź przez `window.cityRankingData[0].latitude`.

**`/api/subscribers/export` zwraca 401 Unauthorized:**
Sprawdź klucz `ADMIN_KEY` w `.env`. Domyślna wartość w kodzie to `'kebab2026'`, ale jeśli masz inną wartość w `.env`, ona wygrywa.

**Strzałki trendu są wszystkie neutralne (-):**
System potrzebuje minimum 2 osobnych aktualizacji z różnymi timestampami. Uruchom `update_city_gmaps.py` dwa razy w różnym czasie.

**Port 5001 zajęty (Windows ghost socket):**
```powershell
Get-Process python | Stop-Process -Force
```

---

Made with ❤️ and 🥙 in Poland.
© 2026 kebabrank.com | All rights reserved.
