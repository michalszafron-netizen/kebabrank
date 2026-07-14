# Kebab App — Update Guide

## Źródło danych: DataForSEO (od 2026-07)

Dane o miejscach pobierane są z **DataForSEO SERP Maps API** (~$0.0006/miasto).
Poprzedni dostawca (GmapsExtractor) był 25× droższy i nie zwracał godzin otwarcia.

Wymagane zmienne środowiskowe w `.env`:
```
DATAFORSEO_LOGIN=email@domena.pl
DATAFORSEO_PASSWORD=haslo_api
DEEPSEEK_API_KEY=...
SERPER_API_KEY=...
PB_URL=...
PB_EMAIL=...
PB_PASSWORD=...
```

---

## 1. Główny skrypt: `run_updates.py`

To jest Twoje główne narzędzie. Robi update rankingów + analiza AI w jednym.

### Aktualizacja jednego miasta
```powershell
python run_updates.py --city Tychy
```

### Kilka miast na raz
```powershell
python run_updates.py --city Tychy Zakopane Krakow
```

### Wszystkie miasta w bazie
```powershell
python run_updates.py --all
```

### Zmiana limitu AI (domyślnie top 10)
```powershell
python run_updates.py --city Tychy --limit 5
```

### Tylko ranking, bez AI (szybkie odświeżenie, zero tokenów)
```powershell
python run_updates.py --city Tychy --no-ai
```

**Co robi każdy update miasta:**
1. Reset city_rank dla istniejących wpisów
2. Wyszukanie kebabów przez DataForSEO (depth=400 dla dużych miast)
3. Filtrowanie: kebaby tylko w danym mieście, bez restauracji indyjskich/greckich itp.
4. Sprawdzenie zamkniętych: miejsca bez godzin → batch-check via `my_business_info`
5. Obliczenie score i trendów (strzałki ↑↓ vs poprzedni snapshot)
6. Zapis do bazy, raport JSON do `update_reports/`

---

## 2. Co się dzieje z zamkniętymi miejscami

### Automatyczne wykrywanie (podczas każdego update'u)
Miejsca bez godzin otwarcia w wynikach DataForSEO są automatycznie sprawdzane
przez API `my_business_info`. Jeśli status to `temporarily_closed` lub
`permanently_closed` — są usuwane z rankingu i trafiają do raportu.

### Ręczne usunięcie miejsca z bazy

**Zalecane — usuwa wszystkie powiązane dane (cascade):**
```powershell
# Dry run — pokaże co zostanie usunięte, nic nie zmienia:
python remove_place.py "Bistro Bryka" --city Tychy

# Faktyczne usunięcie:
python remove_place.py "Bistro Bryka" --city Tychy --confirm
```

**Szybkie — interaktywne potwierdzenie w terminalu:**
```powershell
python remove_closed_place.py "Bistro Bryka" Tychy
```

> Używaj `remove_place.py --confirm` jeśli chcesz mieć pewność że wszystko
> (ratings, AI analysis, cached reviews) zostało usunięte razem z miejscem.

---

## 3. Godziny otwarcia

DataForSEO zwraca godziny automatycznie. Są zapisywane do pola `opening_hours`
jako JSON i wyświetlane jako badge ("Otwarte · zamyka 21:00" / "Zamknięte")
na stronie bez żadnej dodatkowej akcji.

**Edge cases obsługiwane automatycznie:**
- Brak timetable ale Google mówi "Otwarte teraz" → badge "Otwarte"
- Wszystkie dni zamknięte (np. sezonowo) → badge "Zamknięte"
- Godziny nocne przekraczające północ → poprawne porównanie z wczorajszym dniem

---

## 4. Duże miasta (automatyczna paginacja)

Dla poniższych miast DataForSEO pobiera automatycznie depth=400 zamiast 100:

`Kraków, Warszawa, Katowice, Poznań, Wrocław, Gdańsk, Gdynia, Łódź`

Jeśli wyników jest ≥ depth — dorzuca dodatkowe wyszukiwania: "döner" i "shawarma"
(z deduplikacją po place_id).

---

## 5. Skrypty indywidualne

### `update_city_gmaps.py` — tylko ranking i dane z Google Maps
```powershell
python update_city_gmaps.py Tychy
```
Generuje raport w `update_reports/Tychy_YYYY-MM-DD.json`.

### `update_city_review_ai.py` — tylko analiza AI

Re-uruchomienie po przerwaniu (Ctrl+C):
```powershell
python update_city_review_ai.py Krakow --limit 10
```

Pomiń miejsca które już mają AI (np. dogranie brakujących po przerwaniu):
```powershell
python update_city_review_ai.py Krakow --limit 10 --skip-existing
```

---

## 6. Weryfikacja wyników

```powershell
python verify_ai.py Tychy
```

---

## 7. Raporty update'ów

Po każdym update'cie miasta powstaje plik JSON w `update_reports/`:
```
update_reports/Krakow_2026-07-13.json
```

Zawiera:
- `new_places` — nowe miejsca wykryte w tym update'cie
- `closed_temporarily` — tymczasowo zamknięte (usunięte z rankingu)
- `closed_permanently` — na stałe zamknięte
- `disappeared_from_search` — były w bazie, nie pojawiły się w wynikach DataForSEO
