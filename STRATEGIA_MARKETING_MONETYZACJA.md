# 🥙 KebabRank — Audyt, Strategia Marketingowa i Monetyzacja

> **Data analizy:** 2026-07-27
> **Zakres:** audyt kodu i SEO (zweryfikowany na żywej stronie), plan marketingowy przy zerowym budżecie, ocena ścieżek monetyzacji
> **Status:** dokument decyzyjny — do wyboru kierunku, nie do wykonania w całości naraz

---

## Spis treści

1. [TL;DR — wnioski w 60 sekund](#1-tldr--wnioski-w-60-sekund)
2. [Audyt stanu faktycznego](#2-audyt-stanu-faktycznego)
3. [Trzy blockery SEO](#3-trzy-blockery-seo)
4. [Prawda o algorytmie rankingowym](#4-prawda-o-algorytmie-rankingowym)
5. [Ocena monetyzacji](#5-ocena-monetyzacji)
6. [Nisze produktowe](#6-nisze-produktowe)
7. [Kampania marketingowa 90 dni](#7-kampania-marketingowa--90-dni-zero-budżetu)
8. [Priorytety wykonawcze](#8-priorytety-wykonawcze)
9. [Otwarte pytania](#9-otwarte-pytania--czego-nie-wiem)
10. [Jak zweryfikować te wnioski ponownie](#10-jak-zweryfikować-te-wnioski-ponownie)

---

## 1. TL;DR — wnioski w 60 sekund

| Obszar | Werdykt |
|---|---|
| **Produkt** | Realny, rozbudowany, ładny. Ranking + AI + radar + mapa + ruletka + filtry działają. |
| **SEO** | 🔴 **Zepsute na poziomie fundamentu.** 71 stron miast jest dla Google praktycznie puste. |
| **Blog** | 🟢 Działa i przynosi zasięg — bo to statyczny HTML z prawdziwą treścią. Skalować. |
| **Monetyzacja B2C** (reklamy, affiliate) | ⚠️ Słaba. Realnie kilkaset zł/mc. |
| **Monetyzacja B2B** (właściciele lokali, dostawcy) | ⭐ **Tu są prawdziwe pieniądze.** |
| **Co robić najpierw** | Naprawić SEO (pkt 1–3 z priorytetów). Marketing przed tym = strata pracy. |

**Zdanie, które trzeba zapamiętać:**
> Strona konsumencka monetyzuje się słabo. Strona B2B — właściciele ~3 000 kebabowni w Polsce — monetyzuje się dobrze. Deklaracja „rankingu nie da się kupić" to nie ograniczenie, tylko produkt: to ona daje odznace wartość.

---

## 2. Audyt stanu faktycznego

### Co jest zbudowane i działa

| Element | Stan |
|---|---|
| Stack | Flask + PocketBase (SQLite) + DeepSeek + DataForSEO/GmapsExtractor |
| Miasta | **71** w sitemapie |
| Lokale | ~120 na miasto |
| Blog | 14 artykułów (statyczny HTML) |
| Analityka | GA4 (`G-CMSKM4X7XD`) + Ahrefs Analytics — **oba zainstalowane** |
| Email capture | `subscribers.db`, endpoint `/api/subscribe`, źródła: roulette / city_watch / footer |
| Funkcje | Ranking, radar (geolokalizacja), mapa Leaflet, ruletka, filtry (otwarte teraz / nocne / województwo), sortowanie, deep-link „Prowadź" do Google Maps |
| Deployment | Docker Compose na Hostinger VPS |

### Struktura URL

```
/                       → strona główna (SPA)
/kebab-<miasto>         → strona miasta (SPA, 71 sztuk)
/<miasto>               → 301 redirect na /kebab-<miasto>
/blog, /blog/<slug>     → blog (statyczny HTML) ✅ TO DZIAŁA
/api/*                  → API (zablokowane w robots.txt)
```

**Czego brakuje:** `/kebab-<miasto>/<lokal>` — stron pojedynczych lokali. Zero. To ~1 400 nieistniejących landing page'y.

---

## 3. Trzy blockery SEO

> To jest sekcja, która przesądza o skuteczności **całego** marketingu.
> Wszystkie trzy zweryfikowane na żywej stronie przez pobranie `kebabrank.com/kebab-krakow` jako Googlebot.

### 🔴 Blocker #1 — strony miast są puste dla Google

Cały **widoczny** tekst strony miasta to **2 025 znaków**, i wygląda tak:

```
Najlepszy kebab w Kraków · Kebab Rank · search · location_on · Kraków ·
Search for a city above to see the best kebabs · Filter kebab count: 120 ...
```

Nazwy kebabów (`Soltan`, `U Wiśni`, `Layali`, `Hamis`) występują w HTML **wyłącznie wewnątrz JSON-LD**. W treści strony — zero.

**Przyczyna techniczna:**
- `displayRankings()` w `static/js/app.js` dorysowuje wszystko z JS-a po `/api/rankings/<city>`
- `seo_rankings` przekazywane z `app.py:189` jest użyte **tylko** w schema.org w `templates/base.html:71`
- `templates/index.html` (439 linii) nie ma **ani jednej** pętli Jinja — zero renderowania po stronie serwera

**Skutek:** 71 stron miast to dla Google niemal identyczne, puste szkielety. Konkurencja (blogi foodie, Pyszne.pl) ma tam pełne listy w HTML.

**To wyjaśnia obserwację:** blog łapie zasięgi (statyczny HTML z treścią), strony produktowe nie (pusty SPA).

**Fix:** wyrenderować TOP 10 serwerowo w `index.html` (Jinja `{% for %}`), zostawiając JS do interakcji.

---

### 🔴 Blocker #2 — błąd gramatyczny w `<title>` na wszystkich 71 stronach

```html
<title>Najlepszy Kebab w Kraków - Ranking Kraków 2026 | Kebab Rank</title>
```

**„w Kraków"** zamiast **„w Krakowie"** — brak odmiany przez miejscownik.

Ten sam błąd występuje w:
- `<title>` → `app.py:191`
- `page_description` → `app.py:192`
- `page_keywords` → `app.py:193`
- `page_h1` → `app.py:194`
- oraz w drugim bloku (fallback dla dopasowania przybliżonego) → `app.py:204-207`

**Podwójny koszt:**
1. Polak w SERP czyta to jako stronę robioną automatem → spada CTR
2. Nie trafiasz we frazę „najlepszy kebab **w Krakowie**", którą ludzie realnie wpisują

**Fix:** jednorazowa mapa odmiany miejscownika dla 71 miast (~30 min roboty).
Uwaga na nieregularne: Kraków→Krakowie, Łódź→Łodzi, Gdańsk→Gdańsku, Bydgoszcz→Bydgoszczy, Zakopane→Zakopanem, Nowy Sącz→Nowym Sączu, Jastrzębie-Zdrój→Jastrzębiu-Zdroju, Bielsko-Biała→Bielsku-Białej, Gorzów Wielkopolski→Gorzowie Wielkopolskim.

---

### 🟠 Blocker #3 — ukryty `<h1>` + brak stron lokali

```html
<h1 class="sr-only">Najlepszy kebab w Kraków</h1>
```

`sr-only` = wizualnie ukryty (tylko dla czytników ekranu). Działa, ale to zmarnowany najmocniejszy sygnał treściowy na stronie.

**Ważniejsze:** brak stron pojedynczych lokali. Każdy lokal to potencjalna strona docelowa na frazy long-tail:
- „kebab soltan kraków opinie"
- „soltan godziny otwarcia"
- „czy soltan jest otwarty"

To frazy o **najwyższej konwersji** i **najniższej konkurencji**. Obecnie: 0 stron. Potencjał: ~1 400.

---

## 4. Prawda o algorytmie rankingowym

> ⚠️ To jest ryzyko reputacyjne. Trzeba je rozbroić **przed** wyjściem do mediów.

### `rank_score` nie zawiera AI

W `services/ranking.py:11` jest to napisane wprost:

```python
# Note: Positive percentage is ignored as it's not real data
```

AI (DeepSeek) generuje **streszczenia opinii**, ale **nie wpływa na ranking**. Wzór:

```
rank_score = (rating / 5) * 100 * 0.85          # 85% — ocena Google
           + min(log10(min(reviews,1000)+1)/3*100, 100) * 0.15   # 15% — liczba opinii
```

### Skutek: liczba opinii jest ograniczona do 1000 → masowe remisy

Ponieważ `min(total_reviews, 1000)` saturuje przy 1000 opinii, **każdy lokal z ≥1000 opinii dostaje identyczne 15 pkt**. Wynik staje się wtedy czystą funkcją oceny:

| Ocena Google | ≥1000 opinii | Wynik |
|---|---|---|
| 4.7 | tak | 94.9 |
| 4.8 | tak | **96.6** — zawsze |
| 4.9 | tak | **98.3** — zawsze |

**To dlatego** Soltan (Kraków), Tonir (Poznań), Mag Shaurma (Katowice) i Weld Kebab (Toruń) mają identyczne **96.6**.

### Konsekwencja, którą wytknie pierwszy dziennikarz

Habibi ze Słupska (ocena 5.0, ~770 opinii) → **99.43**
Kebab DRWAL z Gdańska (ocena 4.8, **16 831** opinii) → **96.6**

Lokal z 770 opiniami bije lokal z 17 000 opinii. Da się to obronić („jakość > popularność"), ale komunikat **„AI-powered ranking" jest na wyrost**.

### Rekomendacja — wybierz jedno

**Opcja A (uczciwsza, szybsza):** zmień komunikat na *„ranking oparty na danych Google + opisy generowane przez AI"*.

**Opcja B (mocniejsza produktowo):** faktycznie wciągnij `ai_sentiment` do wzoru jako trzeci składnik (np. 70/15/15) — wtedy „AI-powered" jest prawdą, ranking przestaje mieć remisy i zyskujesz realną przewagę, której nikt nie skopiuje z Google Maps.

**Opcja B jest lepsza biznesowo** — bo dopiero ona czyni ranking *Twoim*, a nie przesortowanym Google.

---

## 5. Ocena monetyzacji

### Ranking ścieżek

| Ścieżka | Realny potencjał / mc | Wysiłek | Werdykt |
|---|---|---|---|
| **Płatny profil lokalu** (bez wpływu na ranking) | 750 – 3 500 zł | średni | ⭐ **Główna ścieżka** |
| **Certyfikat / naklejka na witrynę** (one-off 99–199 zł) | 500 – 2 000 zł | niski | ⭐ **Zrób od razu** |
| **B2B: dostawcy mięsa, sosów, opakowań, franczyzy** | 1 000 – 5 000 zł | średni | ⭐ Niedoceniona żyła |
| Affiliate Pyszne / Bolt Food / Glovo | 100 – 300 zł | średni | ⚠️ Przereklamowane |
| AdSense / display | 250 – 750 zł przy 50k PV | niski | ⚠️ Psuje premium look |

> **Uwaga:** to szacunki oparte na założeniach (konwersja 2–5% z outreachu do TOP 10 w 71 miastach; RPM 5–15 zł dla polskiego ruchu food/local). Bez danych o realnym ruchu są to widełki, nie prognoza. Patrz sekcja 9.

### Dlaczego affiliate rozczaruje

**Konflikt intencji.** Killer-feature KebabRank to radar + „Prowadź" → intencja *„stoję na ulicy, idę pieszo, chcę teraz"*.
Affiliate dowozowy łapie intencję *„leżę w domu, zamawiam"*. To dwa różne momenty i dwa różne stany użytkownika.

Do tego: znaczna część lokali z topki to małe budki, których **nie ma** na Pyszne.pl / Glovo. Mapowanie lokal→platforma to praca ręczna dla setek pozycji.

**Werdykt:** zrób to (to darmowy przychód dodatkowy), ale nie buduj na tym modelu biznesowego.

### Dlaczego B2B to żyła złota

Masz coś, czego **nie ma nikt w Polsce**:

> Uporządkowaną, aktualizowaną listę wszystkich kebabowni w kraju, z rankingiem jakości, liczbą opinii, lokalizacją i godzinami otwarcia.

Dla producenta mięsa kebab, dystrybutora sosów, dostawcy opakowań czy sieci franczyzowej to **gotowa baza leadów posegmentowana po jakości i skali**. Reklama docierająca do 3 000 właścicieli kebabowni jest warta wielokrotnie więcej niż baner do przypadkowego konsumenta.

### Zasada, która to wszystko spina

> **Sprzedajesz wszystko oprócz pozycji w rankingu.**

| Sprzedajesz ✅ | Nigdy nie sprzedajesz ❌ |
|---|---|
| Rozbudowany profil (zdjęcia, menu, opis) | Pozycję w rankingu |
| Panel statystyk dla właściciela | Wpływ na `rank_score` |
| Fizyczny certyfikat / naklejka | Usunięcie konkurenta |
| Odznakę „Zweryfikowany" | Ukrycie negatywnej oceny |
| Przycisk „Zamów" / link do menu | |

To nie jest ograniczenie — to **produkt marketingowy**. Hasło *„jedyny ranking w Polsce, którego nie da się kupić"* jest mocniejsze niż cokolwiek, co mógłbyś sprzedać za 200 zł. **To ono nadaje odznace wartość.** Gdyby dało się kupić pozycję, naklejka w oknie nie znaczyłaby nic.

---

## 6. Nisze produktowe

### 🥙📈 Indeks Kebaba — najmocniejszy pomysł w tym dokumencie

**Obserwacja:** nikt w Polsce nie śledzi systematycznie cen kebaba. A to temat, który media biorą **zawsze** — bo dotyczy inflacji, codzienności i jest zabawny. Wzorzec: Big Mac Index.

**Jak zbudować za zero:**
1. Dodaj do karty lokalu pole „cena dużego kebaba"
2. Crowdsourcing od użytkowników — jeden tap, ta sama mechanika UX co ruletka
3. Licz średnią krajową i per-miasto
4. Publikuj co miesiąc:
   > *„Kebab w Polsce podrożał o 4,2% — najtaniej w Wałbrzychu (18 zł), najdrożej w Warszawie (32 zł)"*

**Dlaczego to jest tak wartościowe:**
- Gotowy komunikat prasowy **co miesiąc**, bez wysiłku
- Lokalne portale biorą to chętnie (tekst o *ich* mieście)
- → backlinki z portali informacyjnych, **których nie da się kupić**
- → trwały wzrost autorytetu domeny → rośnie **całe** SEO, nie tylko jedna strona
- Przy okazji: cena to realna potrzeba użytkownika i naturalny filtr w aplikacji

### 📊 Panel właściciela lokalu

> „Twój lokal wyświetlono **1 240** razy w tym miesiącu. **89** osób kliknęło »Prowadź«."

To jest dokładnie to, za co lokal zapłaci abonament — bo **widzi zwrot z inwestycji w liczbach**. Bez tego panelu sprzedajesz obietnicę; z nim sprzedajesz dowód.

### Inne kierunki warte rozważenia

| Pomysł | Uzasadnienie |
|---|---|
| Filtr „otwarte do rana" jako osobna strona | Masz `opening_hours` — **nikt w Polsce tego nie ma**. Fraza „kebab w nocy [miasto]" jest niezagospodarowana. |
| Ulubione / lista życzeń | Powód do powrotu + podstawa pod konto użytkownika |
| Powiadomienia o zmianie w rankingu | „Twój ulubiony kebab spadł na #4" — retencja |
| Ranking sieci/franczyz | Dara Kebab zajął #1–#5 w Rzeszowie — to gotowa historia |

---

## 7. Kampania marketingowa — 90 dni, zero budżetu

### Faza 0 (tydzień 1–2): napraw fundament

> **Bez tego reszta leje wodę do dziurawego wiadra.**

1. Odmiana miast w `title` / `h1` / `description` (71 stron)
2. Server-side render TOP 10 w `index.html` + odkryty `<h1>`
3. Strony pojedynczych lokali `/kebab-<miasto>/<lokal>` + aktualizacja sitemapy
4. Zgłoś nową sitemapę w Google Search Console

---

### Faza 1 (tydzień 3–6): treść, która sama się roznosi

#### Blog — 2 artykuły / tydzień

Działa (statyczny HTML), więc skalujesz. Priorytet na frazy, na które **masz dane, ale nie masz treści**:

| Typ artykułu | Potencjał |
|---|---|
| „Najlepszy kebab w [miasto]" | ~60 miast wciąż bez artykułu |
| „Kebab do 20 zł w [miasto]" | wymaga Indeksu Kebaba |
| **„Kebab otwarty do rana w [miasto]"** | ⭐ masz `opening_hours`, nikt tego nie ma |
| „Gdzie zjeść kebab w nocy w Warszawie" | potężna, niezagospodarowana fraza |

#### Social — plemienność, nie estetyka

Kebab to temat, o który ludzie się **kłócą** — i to jest paliwo zasięgowe.

**Stały format postu:**
> *„TOP 5 kebabów w [miasto] wg 12 400 opinii Google. Zgadzasz się? 👇"*

Komentarze typu „a gdzie XYZ?!" **to nie krytyka — to zasięg**. Odpowiadaj danymi:
> „XYZ ma 4.6 przy 300 opiniach — jest na #8. Ranking liczy ocenę i liczbę opinii."

**1 miasto dziennie = 71 postów = ponad 2 miesiące contentu z danych, które już masz.**

#### Facebook: grupy miejskie — największy nieodkryty kanał

Grupy typu „Spotted: Kraków", „Wrocław — co słychać", grupy foodie.

- **Nie spamuj linkiem.** Wrzuć sam ranking jako grafikę, link daj w pierwszym komentarzu.
- Jeden dobry post w grupie 80 000 osób **>** miesiąc postowania na własnym fanpage'u z 200 followersami.

#### Reddit

r/Polska, r/krakow, r/wroclaw, r/gastronomia.
Format „zrobiłem stronę, która…" działa tam bardzo dobrze — ale **tylko raz na subreddit** i tylko szczerze, z przyznaniem się do ograniczeń.

---

### Faza 2 (tydzień 5–10): outreach do lokali = dystrybucja + pierwsze przychody

Masz gotowy `outreach_social_media.md` z DM-ami do TOP 5 w kilkunastu miastach. **Ten dokument jest dobry** — ale obecnie to czysty koszt. Dorób do niego lejek:

**Krok 1 — darmowa odznaka (dystrybucja)**
Wyślij grafikę → lokal wrzuca na swój IG/FB → **jego** obserwujący poznają KebabRank.
To najtańszy kanał dystrybucji jaki masz: kebabownia z 5 000 followersów robi Ci zasięg za darmo.

**Krok 2 — certyfikat fizyczny (pierwszy przychód)**
W tej samej wiadomości:
> *„Mam też fizyczny certyfikat na witrynę — 149 zł, jednorazowo."*

Naklejka w oknie to najstarszy i najskuteczniejszy produkt w gastronomii (TripAdvisor zbudował na tym biznes).
**Lokal, który powiesi Twoją naklejkę, reklamuje Cię offline każdemu przechodniowi — na zawsze.**

**Krok 3 — abonament (po 30 dniach)**
> *„Twój lokal wyświetlono X razy w KebabRank w tym miesiącu."*
→ sprzedaż płatnego profilu 49–99 zł/mc.

---

### Faza 3 (tydzień 8–12): media + wideo

**Indeks Kebaba → komunikat prasowy**
Pierwsza edycja rozesłana do redakcji lokalnych. Portale regionalne biorą takie rzeczy chętnie, bo to gotowy tekst o ich mieście.

**TikTok / Reels / Shorts — brakujący kanał**
To dziś główne miejsce odkrywania jedzenia w Polsce, a nie masz tam nic.

> 💡 **Zainstalowany jest HyperFrames** (31 skilli, `.agents/skills/`) — framework renderujący wideo z HTML.
> Można wygenerować **71 automatycznych filmów** „TOP 5 kebabów w [miasto]": odliczanie, dane z bazy, spójny branding, zero kosztu produkcji.
> **To 2 miesiące codziennego contentu wideo z jednego skryptu.**

---

## 8. Priorytety wykonawcze

| # | Zadanie | Czas | Dlaczego teraz |
|---|---|---|---|
| 1 | Odmiana miast w title / h1 / description | 1 h | Trywialne, natychmiastowy zysk CTR |
| 2 | SSR TOP 10 na stronach miast | 3–4 h | **Odblokowuje 71 stron w Google** |
| 3 | Strony lokali + sitemap | 1 dzień | +1 400 stron long-tail |
| 4 | Generator wideo (HyperFrames) | 1 dzień | 71 filmów na TikTok / Reels |
| 5 | Certyfikat + cennik profilu | pół dnia | Pierwsze realne przychody |
| 6 | Indeks Kebaba (pole cena) | 2 dni | Silnik PR i backlinków |
| 7 | Decyzja: AI we wzorze czy zmiana komunikatu | — | Ryzyko reputacyjne przed wyjściem do mediów |

> **Kolejność jest nieprzypadkowa.** Pozycje 1–3 to warunek konieczny.
> Kampania przed nimi = wpuszczasz ludzi na strony, których Google i tak nie pokaże. Cały wysiłek wyparuje razem z zasięgiem posta.

**Rekomendacja startowa: 1 + 2.** Kilka godzin pracy, odblokowuje wszystko inne.

---

## 9. Otwarte pytania / czego nie wiem

| Pytanie | Dlaczego to ważne | Gdzie sprawdzić |
|---|---|---|
| **Ile realnie masz ruchu?** (sesje/mc, organic vs direct) | Przesądza, czy zaczynamy od monetyzacji (masz ruch) czy wyłącznie od SEO (nie masz) | GA4 `G-CMSKM4X7XD` lub Ahrefs |
| Ile pozycji w `subscribers.db`? | Czy newsletter jest już kanałem, czy dopiero będzie | `/api/subscribers/export?key=...` |
| Ile miast ma aktualne dane AI? | Wpływa na jakość treści do SEO | PocketBase, pole `ai_summary` |
| Czy outreach z `outreach_social_media.md` był już wysłany? | Nie palić bazy dwa razy tą samą wiadomością | — |
| Koszt jednego pełnego update'u danych | Próg opłacalności całego modelu | DataForSEO billing |

---

## 10. Jak zweryfikować te wnioski ponownie

```bash
curl -sS --ssl-no-revoke -A "Googlebot" https://www.kebabrank.com/kebab-krakow -o kr.html
```

Następnie sprawdź:

```bash
grep -o "<title>[^<]*</title>" kr.html
```

```bash
grep -c "Soltan" kr.html
```

Interpretacja:
- **`<title>` zawiera „w Kraków"** → Blocker #2 wciąż aktualny
- **`Soltan` występuje 1 raz** → tylko w JSON-LD, Blocker #1 wciąż aktualny
- **`Soltan` występuje ≥2 razy** → treść jest już renderowana serwerowo ✅

Sprawdzenie renderowania serwerowego w kodzie:

```bash
grep -n "{% for" templates/index.html
```

Pusty wynik = brak SSR = Blocker #1 aktualny.

---

## Notatki do decyzji

Trzy kierunki, między którymi trzeba wybrać — **nie da się zrobić wszystkich naraz**:

**A. Kierunek SEO/ruch** — napraw blockery, skaluj blog, buduj strony lokali.
Wolniejszy zwrot, ale to jedyny fundament, na którym stoi wszystko inne. *Bez tego pozostałe dwa kierunki mają dużo niższy sufit.*

**B. Kierunek B2B/przychód** — certyfikaty, profile, outreach do lokali, sprzedaż dostępu do bazy.
Najszybsze realne pieniądze, działa nawet przy niskim ruchu, bo sprzedajesz status i widoczność, nie kliknięcia.

**C. Kierunek media/marka** — Indeks Kebaba, PR, wideo, social.
Najwyższy sufit i najlepsze wsparcie dla A (backlinki) — ale efekt rozłożony w czasie i najtrudniejszy do przewidzenia.

**Moja rekomendacja:** **A → B → C**, przy czym A skrócone do minimum (pozycje 1–2 z priorytetów, ~5 godzin pracy), żeby jak najszybciej przejść do B, gdzie są pieniądze. C uruchamiaj równolegle w tle, gdy tylko A jest gotowe.

---

*Dokument wygenerowany na podstawie audytu kodu (`app.py`, `services/ranking.py`, `templates/`, `static/sitemap.xml`) oraz weryfikacji żywej strony jako Googlebot, 2026-07-27.*
