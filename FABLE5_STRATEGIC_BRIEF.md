# Brief strategiczny dla Claude Fable 5 — KebabRank.com

> **Jak z tego korzystać:** przełącz model na Fable 5 (`/model fable`) w tej samej sesji Claude Code (w tym repo) i wklej całą treść poniżej jako polecenie. Fable ma dostęp do tych samych narzędzi (Read/Grep/Bash/WebSearch), więc może sam zweryfikować kod, a nie tylko polegać na tym opisie.

---

## 0. Kontekst — kim jesteś i czego od Ciebie oczekuję

Jesteś moim strategicznym doradcą produktowym, technicznym i marketingowym dla projektu **KebabRank** (www.kebabrank.com) — polskiej platformy rankingującej kebaby w 50+ miastach na podstawie danych z Google Maps + analizy sentymentu AI.

Wracam do tego projektu po ~2 miesiącach przerwy i częściowo się pogubiłem. Chcę, żebyś:
1. **Sam zweryfikował realny stan projektu** czytając kod i dokumentację — nie ufaj mi w 100%, bo część moich obserwacji poniżej to subiektywny ogląd ("mogę żyć w swojej bańce"). Wypunktuj, jeśli się ze mną nie zgadzasz.
2. Zaproponował konkretny, ambitny plan wyniesienia projektu na zupełnie inny poziom — produktowo, wizualnie, biznesowo i marketingowo.

Nie ograniczaj się do tego co niżej opisuję — to moje priorytety, ale masz pełną swobodę dorzucenia własnych pomysłów, o których nie pomyślałem.

---

## 1. Stan faktyczny — od czego zacząć

Dokumentacja projektu jest częściowo nieaktualna i zaśmiecona. Zanim cokolwiek zaproponujesz, przeczytaj:

- [`kebabrank_comprehensive_readme.md`](kebabrank_comprehensive_readme.md) — najbardziej aktualny opis architektury (Flask + PocketBase + GmapsExtractor/Serper + OpenAI), ale zweryfikuj go względem realnego kodu w `app.py` i `services/`.
- [`HOW_TO_UPDATE.md`](HOW_TO_UPDATE.md) — opisuje jak odpalać update danych, **ale plik zawiera przypadkowo wklejony śmieciowy fragment** (tekst z UI edytora typu "Open Editor / Workspaces / Antigravity1..."). Zignoruj tę część, potraktuj jako błąd do naprawienia przy okazji.
- **Prawdziwy, aktualny flow update'u danych to `run_updates.py`** (koordynuje `update_city_gmaps.py` + `update_city_review_ai.py`, zapisuje do PocketBase). To jedyny skrypt, którego powinienem używać na co dzień.

### Ważne: masakra martwego kodu w root repo
W katalogu głównym jest **~150 luźnych skryptów `.py`**, z czego **~58 wciąż odwołuje się do Supabase** — bazy danych, z której projekt już dawno zmigrował na PocketBase (`migrate_to_pocketbase.py` to świadek tej migracji). Te skrypty (`check_supabase.py`, `backup_supabase_sql.py`, dziesiątki `check_*`, `debug_*`, `fix_*`, `test_*`, `rank_batch_1..13.py`, `ai_batch_1..7.py` itp.) to najpewniej jednorazowe narzędzia diagnostyczne z różnych etapów rozwoju projektu — część nie zadziała już wcale, część działa ale operuje na nieaktualnym modelu danych.

**Zadanie dla Ciebie:** zrób szybki audyt tych skryptów (możesz grupować po wzorcu nazwy) i zaproponuj plan porządkowania — co przenieść do `archive/` lub skasować, co realnie jeszcze służy (np. `generate_sitemap.py`, `restart_flask_clean.py` wyglądają na used), żebym po kolejnym powrocie do projektu nie gubił się w tym bałaganie. Nie musisz robić tego jako pierwszy priorytet, ale ujmij to w planie.

---

## 2. Cel główny: wynieść projekt na zupełnie inny poziom

Chcę ambitnej wizji — nie kosmetycznych poprawek. Rozbij to na te obszary:

### A. Alternatywny front-end — "super UI"
Obecny frontend to Vanilla JS + PocketBase SDK, stylizowany na glassmorphism. Zaproponuj śmiałą alternatywną wizję UI/UX dla użytkownika końcowego — coś co realnie wyróżni KebabRank na tle prostych stron z rankingami. Możesz zaproponować zmianę stacku (np. framework JS) jeśli uzasadnisz korzyść, albo zostać przy obecnym z dużo mocniejszym designem. Zwróć uwagę na to, że to ranking lokalny/mobilny — użytkownik często szuka "na już", stojąc na ulicy.

### B. Nowe funkcje — darmowe i płatne (model freemium)
Zaproponuj konkretny podział funkcji na darmowe vs płatne (subskrypcja / one-off / co uznasz za sensowne). Mam dwa konkretne braki, które uważam za priorytetowe — ale rozbuduj to swoimi pomysłami:

1. **Geolokalizacja użytkownika + sortowanie po odległości.** Obecnie użytkownik może wejść w mapę, ale aplikacja nie wie, gdzie on jest, i nie pokazuje odległości do kebabów z rankingu. Chcę: system lokalizuje użytkownika (za jego zgodą) i pokazuje np. **TOP 3 najbliższe kebaby z topki z odległością**, z możliwością rozwinięcia listy o kolejne najbliższe. To powinno być realnym game-changerem UX-owym — pomyśl, jak to zaimplementować (przeglądarkowe Geolocation API + sortowanie po dystansie z lat/lng, które zapewne już mamy w bazie z Google Places).
2. **Godziny otwarcia — brakujący, priorytetowy filtr.** System w ogóle nie pokazuje, czy lokal jest teraz otwarty. To poważny brak. Prawdopodobnie trzeba pobrać te dane z Google (sprawdź, czy `services/google_places.py` / `google_places_enhanced.py` już to obsługuje częściowo, czy trzeba dociągać nowe pole). Zaproponuj też **ogólnie brakujące filtry** w systemie (np. "otwarte teraz", cena, typ kebaba, dystans, ocena minimalna) — obecnie systemu filtrowania praktycznie nie ma.

Dorzuć swoje pomysły na dodatkowe funkcje płatne/darmowe, których nie wymieniłem (np. powiadomienia, ulubione miejsca, personalizacja, program dla właścicieli lokali, weryfikowane odznaki, etc.) — potraktuj to jako brainstorm, nie ograniczaj się do mojej listy.

### C. Plan marketingowy
Obecność w social media jest obecnie słabo rozwinięta (zobacz `outreach_social_media.md` jako punkt wyjścia, ale to raczej luźne notatki niż plan). Zaproponuj konkretny, realistyczny plan marketingowy zakładający zerowy/mały istniejący budżet i słaby start w social media — kanały, częstotliwość, rodzaj treści, ewentualne partnerstwa z lokalami z rankingu, SEO (projekt ma już blog i strony miast pod SEO — oceń, czy to wykorzystane dobrze).

### D. Alternatywne, tańsze źródła danych do aktualizacji (ważny problem kosztowy)
To realny problem biznesowy: każdy update danych kosztuje pieniądze z powodu płatnych API.
- **Serper.dev** — bardzo korzystny, prawie darmowy, zostaje.
- **GmapsExtractor** (`cloud.gmapsextractor.com`) — główne źródło danych do rankingu (recenzje, oceny, lista miejsc), ale **drogi** przy każdym update. To główny problem do rozwiązania.
- **Natywne Google Maps API** — odpada całkowicie, koszty zaporowe.

**Zadanie:** znajdź (użyj WebSearch, ceny się zmieniają) realne, aktualne alternatywy do GmapsExtractor, tańsze lub darmowe, np. rozważ i zweryfikuj aktualność/ceny takich kierunków:
- Scrapery/API typu Apify (Google Maps Scraper actors), Outscraper, SerpApi, DataForSEO, Bright Data — porównaj ich cennik per-request/per-place do GmapsExtractor.
- Dane crowdsourcowane (OpenStreetMap/Overpass API) jako darmowe uzupełnienie dla podstawowych danych (lokalizacja, godziny otwarcia) — z zastrzeżeniem, że recenzje/oceny nadal trzeba będzie brać z Google.
- Foursquare Places API / Yelp Fusion API — czy mają dane o kebabach w Polsce w ogóle sensowne, i jaki mają model cenowy (darmowy tier?).
- Możliwość zmniejszenia częstotliwości/zakresu update'ów zamiast szukania tańszego API (np. update rzadziej dla mniej popularnych miast).

Zaznacz wyraźnie: to nie musi być rozwiązanie na już — z czasem, jeśli projekt zacznie zarabiać, można wrócić do droższych, lepszych jakościowo źródeł (włącznie z natywnym Google Maps API). Chcę wariantów rozłożonych na "teraz przy zerowym budżecie" vs "gdy projekt zarabia".

---

## 3. Czego oczekuję na wyjściu

Ustrukturyzowany raport/plan działania, z jasnym rozdzieleniem na:
1. Audyt stanu obecnego (co potwierdziłeś, z czym się nie zgadzasz).
2. Wizja produktowa (UI + funkcje darmowe/płatne).
3. Plan marketingowy.
4. Rekomendacja źródeł danych (z realnymi, zweryfikowanymi cenami/linkami, nie z pamięci).
5. Priorytetyzacja — co robić najpierw, biorąc pod uwagę, że to prawdopodobnie projekt jednoosobowy/mało-zasobowy.

Bądź konkretny i śmiały. Wolę odważną, dobrze uzasadnioną wizję niż listę oczywistości.
