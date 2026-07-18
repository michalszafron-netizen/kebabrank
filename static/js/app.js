// static/js/app.js
const $id = (id) => document.getElementById(id);

// List of available images discovered in static/img/cities/
const availableCityImages = [
    "Bydgoszcz.webp", "Czestochowa.webp", "Dobczyce.webp", "Gdansk.webp", "Gdynia.webp",
    "Grudziądz.webp", "Jastrzebie_zdroj.webp", "Katowice.webp", "Konin.webp", "Kozieglowy.webp",
    "Krakow.webp", "Legnica.webp", "Lubin.webp", "Lublin.webp", "Myszkow.webp", "Olsztyn.webp",
    "Opole.webp", "Pila.webp", "Pszczyna.webp", "Radom.webp", "Rybnik.webp", "Slupsk.webp",
    "Szczecin.webp", "Tarnow.webp", "Torun.webp", "Tychy.webp", "Warsaw.webp", "Wieliczka.webp",
    "Wroclaw.webp", "Zabrze.webp", "Zarki.webp", "bialystok.webp", "bielsko-biala.webp",
    "bytom.webp", "chorzow.webp", "czechowice-dziedzice.webp", "dabrawa-gornicza.webp",
    "elbląg.webp", "gliwice.webp", "gorzów-wielkopolski.webp", "jaworzno.webp", "jordanow.webp",
    "kalisz.webp", "kielce.webp", "koszalin.webp", "lodz.webp", "myslowice.webp", "nowy-sacz.webp",
    "oswiecim.webp", "piotrkow-trybunalski.webp", "plock.webp", "poraj.webp", "poznan.webp",
    "ruda-slaska.webp", "rzeszow.webp", "siedlce.webp", "skawina.webp", "sosnowiec.webp",
    "walbrzych.webp", "wlocalwek.webp", "wolbrom.webp", "włocławek.webp", "zakopane.webp",
    "zielona-gora.webp"
];

/**
 * Finds the best matching image for a given city name.
 * Handles Polish characters, case sensitivity, and common variations.
 */
const getCityImageFile = (cityName) => {
    // Standardize city name for comparison (remove diacritics, lowercase)
    const normalize = (str) => {
        return str.toLowerCase()
            .replace(/ł/g, 'l').replace(/ó/g, 'o').replace(/ą/g, 'a')
            .replace(/ę/g, 'e').replace(/ć/g, 'c').replace(/ń/g, 'n')
            .replace(/ś/g, 's').replace(/ź/g, 'z').replace(/ż/g, 'z');
    }

    if (!cityName) return null;
    
    const normalizedCity = normalize(cityName);
    const slug = normalizedCity.replace(/ /g, '-');
    const underscoreSlug = normalizedCity.replace(/ /g, '_').replace(/-/g, '_');

    // 1. Direct match with exact name + .webp
    let m = availableCityImages.find(img => img === cityName + '.webp');
    if (m) return m;

    // 2. Case-insensitive exact match
    m = availableCityImages.find(img => img.toLowerCase() === cityName.toLowerCase() + '.webp');
    if (m) return m;

    // 3. Match normalized versions (slugs with hyphens or underscores)
    m = availableCityImages.find(img => {
        const normalizedImgName = normalize(img.split('.')[0]).replace(/_/g, '-');
        return normalizedImgName === slug || normalizedImgName === underscoreSlug.replace(/_/g, '-');
    });
    if (m) return m;

    // 4. Special case: Warszawa -> Warsaw.webp
    if (slug === 'warszawa' || slug === 'warsaw') {
        m = availableCityImages.find(img => img.toLowerCase() === 'warsaw.webp');
        if (m) return m;
    }

    return m || null;
};

// Translation object
const translations = {
    en: {
        'header-title': 'Kebab Rank Poland',
        'header-subtitle-1': 'First AI-powered kebab ranking in Poland',
        'header-subtitle-2': 'Check out our articles',
        'header-subtitle-3': 'Ranking data refreshed every 7 days',
        'header-subtitle': 'Discover the best kebabs in Poland based on Google ratings',
        'header-refresh': 'Data refreshed every 6 days to ensure accuracy while conserving resources',
        'next-update': 'Next update in:',
        'refreshing': 'Refreshing data...',
        'tab-city': 'City Rankings',
        'tab-global': 'Global Top 10',
        'search-label': 'Search for a city',
        'search-button': 'Search',
        'popular': 'Popular:',
        'search-prompt': 'Search for a city to see the best kebabs',
        'global-title': 'Top 10 Kebabs in Poland',
        'global-subtitle': 'Ranked by Google ratings and review count',
        'loading': 'Loading...',
        'score': 'Score',
        'rating': 'Rating',
        'reviews': 'Reviews',
        'rank': 'Rank',
        'go-to-kebab': 'Go to kebab',
        'no-kebabs': 'No kebab places found.',
        'error-loading': 'Error loading rankings. Please try again.',
        'city-not-found': 'City not found. Try one of the available cities or contact us to add it.',
        'top-kebabs': 'Top {count} Kebabs in {city}',
        'ranking-subtitle': 'Ranked by Google ratings and review count',
        'nav-blog': 'Blog',
        'kebab-count-label': 'Number of kebabs to show:',
        'all-cities': 'All Available Cities',
        'loading-cities': 'Loading cities...',
        'view-rankings': 'View rankings',
        'ai-badge-title': 'AI POWERED KEBAB RANK',
        'ai-badge-desc': 'Poland\'s first AI-powered kebab ranking, analyzing thousands of Google Maps reviews in real-time.',
        'ai-badge-subdesc': 'Discover the best spots for doner and artisan tortillas based on sentiment and meat quality.',
        'live-analysis': 'LIVE ANALYSIS',
        'update-in': 'Update in:',
        'top-poland': 'Top 10<br />In Poland',
        'show-top': 'Filter kebab count:',
        'explore-cities': 'Select City',
        'footer-blog': 'Blog',
        'footer-privacy': 'Privacy Policy',
        'footer-rights': '© 2026 KebabRank',
        'google-rating': 'Google Rating',
        'ai-forthcoming': 'AI analysis forthcoming...',
        'sentiment': 'Sentiment',
        'trend': 'Trend',
        'footer-terms': 'Terms of Use',
        'legal-terms-nav': 'Terms',
        'view-list': 'List',
        'view-map': 'Map',
        'back': 'Back',
        'back-to-rankings': 'Back to rankings',
        'blog-title': 'Kebab Knowledge Base',
        'article-label': 'Article',
        'read-more': 'Read',
        'latest-articles': 'Latest Articles',
        'legal-privacy-title': 'Privacy Policy and Cookies of KebabRank.com',
        'legal-admin-title': '1. Data Administrator',
        'legal-admin-desc': 'The data administrator is Michal Szafron, contact: kebabrank@gmail.com (hereinafter: "Administrator").',
        'legal-data-purpose-title': '2. What data do we process and for what purpose?',
        'legal-privacy-first': 'We respect your privacy. The service was designed in the spirit of "Privacy First".',
        'legal-no-personal-title': 'No personal data:',
        'legal-no-personal-desc': 'We do not actively collect any personal data. There are no contact forms, registration forms, or the possibility of leaving comments directly on our servers. We do not collect e-mail addresses or names of Users.',
        'legal-logs-title': 'Server logs:',
        'legal-logs-desc': 'Like any website, our server automatically records requests sent by the browser (IP address, date and time, information about the browser and operating system). This data is not associated with specific people and serves only technical purposes (diagnostics, server security). The legal basis is the legitimate interest of the Administrator (Art. 6(1)(f) GDPR).',
        'legal-cookies-title': '3. Cookies',
        'legal-cookies-desc': 'The Service uses cookies (small text files saved on the User\'s device) in a limited scope:',
        'legal-cookies-tech': 'Technical cookies: Necessary for the proper functioning of the site (e.g., remembering map settings or ranking view).',
        'legal-cookies-third-party': 'Third-party cookies:',
        'legal-cookies-maps': 'Maps: The Service uses maps provided by external providers (OpenStreetMap / CartoDB). These providers may save their own cookies to handle the map.',
        'legal-cookies-analytics': 'Analytics: We use anonymous Google Analytics statistics to analyze website traffic. Users\' IPs are anonymized.',
        'legal-manage-cookies-title': '4. Cookie Management',
        'legal-manage-cookies-desc': 'The User can at any time change the settings regarding cookies in their web browser (block or delete them). This may, however, affect the functionality of the map in the Service.',
        'legal-share-title': '5. Data Transfer',
        'legal-share-desc': 'Technical data (logs) may be entrusted to the hosting company operating the Service only for the purpose of maintaining the site\'s continuity. We do not sell or share any data with marketing entities.',
        'legal-changes-title': '6. Changes to the Policy',
        'legal-changes-desc': 'In the event of a change in the Service\'s functionality, this Policy may change. The current version is always available at this address.',
        'legal-terms-title': 'Terms of Service KebabRank.com',
        'legal-provision-1-title': '§ 1. General Provisions',
        'legal-provision-1-1': 'These Terms of Service define the rules for using the website available at https://kebabrank.com (hereinafter: "Service").',
        'legal-provision-1-2': 'The owner and administrator of the Service is Michal Szafron, contact: kebabrank@gmail.com (hereinafter: "Administrator").',
        'legal-provision-1-3': 'Use of the Service is free and voluntary.',
        'legal-provision-1-4': 'The Service is for information and hobby purposes only. Its purpose is to present subjective rankings of catering points.',
        'legal-provision-2-title': '§ 2. Type and scope of services',
        'legal-provision-2-1': 'The Service allows Users to: a) view the kebab ranking generated using artificial intelligence (AI) algorithms; b) view point locations on the map; c) read ratings and statistics of premises.',
        'legal-provision-2-2': 'The Service does not sell products, does not mediate in ordering food, and does not charge fees from Users.',
        'legal-provision-2-3': 'There is no possibility to create a user account (registration) or sign up for a newsletter in the Service.',
        'legal-provision-3-title': '§ 3. Responsibility and exclusions',
        'legal-provision-3-1': 'The Administrator makes every effort to ensure that the data in the Service is up to date, however, the ranking is generated automatically (supported by AI) based on publicly available data. The Administrator does not guarantee the full correctness of address data, opening hours of premises, or menu availability.',
        'legal-provision-3-2': 'The "TOP 10" ranking and "AI Score" indicators are the result of automatic analysis and constitute a subjective evaluation of the algorithm. The Administrator is not responsible for the User\'s dissatisfaction with the quality of services provided by the catering premises listed in the Service.',
        'legal-provision-3-3': 'The decision to use the services of a given premises is made by the User at their own risk.',
        'legal-provision-4-title': '§ 4. Technical requirements',
        'legal-provision-4-desc': 'To use the Service, the following are necessary:',
        'legal-provision-4-1': 'A device with Internet access.',
        'legal-provision-4-2': 'A web browser that supports HTML5, JavaScript, and cookies (e.g., Chrome, Firefox, Safari).',
        'legal-provision-5-title': '§ 5. Copyright',
        'legal-provision-5-1': 'All content, graphics (including the KebabRank logo), page layout, and data presentation algorithms are the property of the Administrator and are subject to legal protection.',
        'legal-provision-5-2': 'Copying, reproducing, or using elements of the Service without the Administrator\'s consent is prohibited.',
        'cookie-text': 'This website uses cookies for technical and analytical purposes. By using the service, you agree to their use.',
        'cookie-ok': 'OK'
    },
    pl: {
        'header-title': 'Kebab Rank Polska',
        'header-subtitle-1': 'Pierwszy w Polsce ranking kebabów wspierany sztuczną inteligencją',
        'header-subtitle-2': 'Zapraszamy do zapoznania się z naszymi artykułami',
        'header-subtitle-3': 'Dane rankingowe odświeżane co 7 dni',
        'header-subtitle': 'Odkryj najlepsze kebaby w Polsce na podstawie ocen Google',
        'header-refresh': 'Dane odświeżane co 6 dni dla zapewnienia dokładności przy oszczędności zasobów',
        'next-update': 'Następna aktualizacja za:',
        'refreshing': 'Odświeżanie danych...',
        'tab-city': 'Ranking miast',
        'tab-global': 'Top 10 w Polsce',
        'search-label': 'Szukaj miasta',
        'search-button': 'Szukaj',
        'popular': 'Popularne:',
        'search-prompt': 'Wyszukaj miasto, aby zobaczyć najlepsze kebaby',
        'global-title': 'Top 10 kebabów w Polsce',
        'global-subtitle': 'Ranking według ocen Google i liczby opinii',
        'loading': 'Ładowanie...',
        'score': 'Wynik',
        'rating': 'Ocena',
        'reviews': 'Opinie',
        'rank': 'Ranking',
        'go-to-kebab': 'Idź do kebaba',
        'no-kebabs': 'Nie znaleziono kebabów.',
        'error-loading': 'Błąd ładowania rankingu. Spróbuj ponownie.',
        'city-not-found': 'Nie znaleziono miasta. Spróbuj jednego z dostępnych miast lub skontaktuj się z nami.',
        'top-kebabs': 'Top {count} kebabów w mieście {city}',
        'ranking-subtitle': 'Ranking według ocen Google i liczby opinii',
        'nav-blog': 'Blog',
        'kebab-count-label': 'Liczba kebabów do wyświetlenia:',
        'all-cities': 'Wszystkie dostępne miasta',
        'loading-cities': 'Ładowanie miast...',
        'view-rankings': 'Zobacz ranking',
        'ai-badge-title': 'AI POWERED KEBAB RANK',
        'ai-badge-desc': 'Pierwszy w Polsce ranking kebabów wspierany sztuczną inteligencją, analizujący tysiące opinii Google Maps w czasie rzeczywistym.',
        'ai-badge-subdesc': 'Odkryj najlepsze lokale serwujące doner i rzemieślniczą tortillę na podstawie sentymentu i jakości mięsa.',
        'live-analysis': 'ANALIZA LIVE',
        'update-in': 'Aktualizacja za:',
        'top-poland': 'Top 10<br />W Polsce',
        'explore-cities': 'Wybierz Miasto',
        'show-top': 'Filtruj ilość Kebabów',
        'footer-blog': 'Blog',
        'footer-privacy': 'Polityka Prywatności',
        'footer-rights': '© 2026 KebabRank',
        'google-rating': 'Ocena Google',
        'ai-forthcoming': 'Analiza AI wkrótce...',
        'sentiment': 'Sentyment',
        'trend': 'Trend',
        'footer-terms': 'Regulamin',
        'legal-terms-nav': 'Regulamin',
        'view-list': 'Lista',
        'view-map': 'Mapa',
        'back': 'Powrót',
        'back-to-rankings': 'Wróć do rankingu',
        'blog-title': 'Baza wiedzy o Kebabach',
        'article-label': 'Artykuł',
        'read-more': 'Czytaj',
        'latest-articles': 'Najnowsze Artykuły',
        'legal-privacy-title': 'Polityka Prywatności i Plików Cookies Serwisu KebabRank.com',
        'legal-admin-title': '1. Administrator Danych',
        'legal-admin-desc': 'Administratorem danych jest Michal Szafron, kontakt: kebabrank@gmail.com (dalej: "Administrator").',
        'legal-data-purpose-title': '2. Jakie dane przetwarzamy i w jakim celu?',
        'legal-privacy-first': 'Szanujemy Twoją prywatność. Serwis został zaprojektowany w duchu "Privacy First".',
        'legal-no-personal-title': 'Brak danych osobowych:',
        'legal-no-personal-desc': 'Nie zbieramy aktywnie żadnych danych osobowych. W serwisie nie ma formularzy kontaktowych, formularzy rejestracji ani możliwości pozostawiania komentarzy bezpośrednio na naszych serwerach. Nie zbieramy adresów e-mail ani imion Użytkowników.',
        'legal-logs-title': 'Logi serwera:',
        'legal-logs-desc': 'Jak każda strona internetowa, nasz serwer automatycznie zapisuje zapytania wysyłane przez przeglądarkę (adres IP, data i czas, informacje o przeglądarce i systemie operacyjnym). Dane te nie są kojarzone z konkretnymi osobami i służą wyłącznie celom technicznym (diagnostyka, bezpieczeństwo serwera). Podstawą prawną jest uzasadniony interes Administratora (art. 6 ust. 1 lit. f RODO).',
        'legal-cookies-title': '3. Pliki Cookies (Ciasteczka)',
        'legal-cookies-desc': 'Serwis wykorzystuje pliki cookies (małe pliki tekstowe zapisywane na urządzeniu Użytkownika) w ograniczonym zakresie:',
        'legal-cookies-tech': 'Cookies techniczne: Niezbędne do prawidłowego działania strony (np. zapamiętanie ustawień mapy czy widoku rankingu).',
        'legal-cookies-third-party': 'Cookies podmiotów trzecich:',
        'legal-cookies-maps': 'Mapy: Serwis wykorzystuje mapy dostarczane przez zewnętrznych dostawców (OpenStreetMap / CartoDB). Dostawcy ci mogą zapisywać własne pliki cookies w celu obsługi mapy.',
        'legal-cookies-analytics': 'Analityka: Korzystamy z anonimowych statystyk Google Analytics w celu analizy ruchu na stronie. IP użytkowników jest anonimizowane.',
        'legal-manage-cookies-title': '4. Zarządzanie plikami cookies',
        'legal-manage-cookies-desc': 'Użytkownik może w każdej chwili zmienić ustawienia dotyczące plików cookies w swojej przeglądarce internetowej (zablokować je lub usunąć). Może to jednak wpłynąć na funkcjonalność mapy w Serwisie.',
        'legal-share-title': '5. Przekazywanie danych',
        'legal-share-desc': 'Dane techniczne (logi) mogą być powierzone firmie hostingowej obsługującej Serwis wyłącznie w celu utrzymania ciągłości działania strony. Nie sprzedajemy ani nie udostępniamy żadnych danych podmiotom marketingowym.',
        'legal-changes-title': '6. Zmiany w polityce',
        'legal-changes-desc': 'W przypadku zmiany funkcjonalności Serwisu, niniejsza Polityka może ulec zmianie. Aktualna wersja zawsze znajduje się pod tym adresem.',
        'legal-terms-title': 'Regulamin Serwisu KebabRank.com',
        'legal-provision-1-title': '§ 1. Postanowienia ogólne',
        'legal-provision-1-1': 'Niniejszy Regulamin określa zasady korzystania z serwisu internetowego dostępnego pod adresem https://kebabrank.com (dalej: "Serwis").',
        'legal-provision-1-2': 'Właścicielem i administratorem Serwisu jest Michal Szafron, kontakt: kebabrank@gmail.com (dalej: "Administrator").',
        'legal-provision-1-3': 'Korzystanie z Serwisu jest bezpłatne i dobrowolne.',
        'legal-provision-1-4': 'Serwis ma charakter wyłącznie informacyjny i hobbystyczny. Jego celem jest prezentacja subiektywnych rankingów punktów gastronomicznych.',
        'legal-provision-2-title': '§ 2. Rodzaj i zakres usług',
        'legal-provision-2-1': 'Serwis umożliwia Użytkownikom: a) przeglądanie rankingu kebabów generowanego przy użyciu algorytmów sztucznej inteligencji (AI); b) przeglądanie lokalizacji punktów na mapie; c) zapoznawanie się z ocenami i statystykami lokali.',
        'legal-provision-2-2': 'Serwis nie prowadzi sprzedaży produktów, nie pośredniczy w zamawianiu jedzenia ani nie pobiera opłat od Użytkowników.',
        'legal-provision-2-3': 'W Serwisie nie ma możliwości zakładania konta użytkownika (rejestracji) ani zapisu na newsletter.',
        'legal-provision-3-title': '§ 3. Odpowiedzialność i wyłączenia',
        'legal-provision-3-1': 'Administrator dokłada wszelkich starań, aby dane w Serwisie były aktualne, jednakże ranking jest generowany automatycznie (wspierany przez AI) na podstawie ogólnodostępnych danych. Administrator nie gwarantuje pełnej poprawności danych adresowych, godzin otwarcia lokali ani dostępności menu.',
        'legal-provision-3-2': 'Ranking "TOP 10" oraz wskaźniki "Wynik AI" są rezultatem analizy automatycznej i stanowią subiektywną ocenę algorytmu. Administrator nie ponosi odpowiedzialności za niezadowolenie Użytkownika z jakości usług świadczonych przez lokale gastronomiczne wymienione w Serwisie.',
        'legal-provision-3-3': 'Decyzję o skorzystaniu z usług danego lokalu Użytkownik podejmuje na własną responsabilidad.',
        'legal-provision-4-title': '§ 4. Wymagania techniczne',
        'legal-provision-4-desc': 'Do korzystania z Serwisu niezbędne są:',
        'legal-provision-4-1': 'Urządzenie z dostępem do Internetu.',
        'legal-provision-4-2': 'Przeglądarka internetowa obsługująca HTML5, JavaScript oraz pliki cookies (np. Chrome, Firefox, Safari).',
        'legal-provision-5-title': '§ 5. Prawa autorskie',
        'legal-provision-5-1': 'Wszelkie treści, grafiki (w tym logo KebabRank), układ strony oraz algorytmy prezentacji danych są własnością Administratora i podlegają ochronie prawnej.',
        'legal-provision-5-2': 'Kopiowanie, powielanie lub wykorzystywanie elementów Serwisu bez zgody Administratora jest zabronione.',
        'cookie-text': 'Strona korzysta z plików cookies w celach technicznych i analitycznych. Korzystając z serwisu, wyrażasz zgodę na ich użycie.',
        'cookie-ok': 'OK'
    }
};

const aiTranslations = {
    en: {
        'ai-powered': '🤖 AI-Powered-Kebab-Ranking',
        'ai-score': 'AI Score',
        'ai-insights': 'AI Insights',
        'sentiment': 'Customer Sentiment',
        'authenticity': 'Review Authenticity',
        'trending': 'Trending',
        'improving': '📈 Improving',
        'declining': '📉 Declining',
        'stable': '➡️ Stable',
        'dynamiczny wzrost': '📈 Strong Growth',
        'lekka poprawa': '📈 Slight Improvement',
        'pełna stabilizacja': '➡️ Stable',
        'niepokojący spadek': '📉 Slight Decline',
        'wyraźny regres': '📉 Clear Decline',
        'insufficient_data': '— No Data',
        'very-positive': '😍 Very Positive',
        'positive': '😊 Positive',
        'neutral': '😐 Neutral',
        'negative': '😞 Negative',
        'very-negative': '😡 Very Negative',
        'ai-summary': 'AI Summary',
        'confidence': 'Confidence',
        'analyzing': 'Analyzing with AI...',
        'no-ai-data': 'AI analysis not available yet'
    },
    pl: {
        'ai-powered': '🤖 Wspierane przez AI',
        'ai-score': 'Wynik AI',
        'ai-insights': 'Analiza AI',
        'sentiment': 'Nastroje klientów',
        'authenticity': 'Autentyczność opinii',
        'trending': 'Trend',
        'improving': '📈 Poprawia się',
        'declining': '📉 Spada',
        'stable': '➡️ Stabilny',
        'very-positive': '😍 Bardzo pozytywne',
        'positive': '😊 Pozytywne',
        'neutral': '😐 Neutralne',
        'negative': '😞 Negatywne',
        'very-negative': '😡 Bardzo negatywne',
        'ai-summary': 'Podsumowanie AI',
        'confidence': 'Pewność',
        'analyzing': 'Analizowanie przez AI...',
        'no-ai-data': 'Analiza AI jeszcze niedostępna'
    }
};

// Merge with existing translations
Object.keys(aiTranslations).forEach(lang => {
    Object.assign(translations[lang], aiTranslations[lang]);
});


// Current language - initialize from localStorage or HTML lang attribute
const storedLang = localStorage.getItem('preferredLang');
window.currentLang = storedLang || document.documentElement.lang || 'pl';
let currentLang = window.currentLang;
window.rankingCache = {};
// rankingCache will be declared below with map variables

let countdownInterval;
let availableCities = [];
let allCities = []; // Global variable for city search

// Map variables
window.kebabMap = null;
window.globalKebabMap = null;
let mapMarkers = [];
let globalMapMarkers = [];
window.currentCityBounds = null;
window.globalCityBounds = null;
const rankingCache = window.rankingCache;
window.activeFilters = { city: {}, global: {} };

const CITY_VOIVODESHIP = {
    'Warszawa': 'Mazowieckie', 'Radom': 'Mazowieckie', 'Płock': 'Mazowieckie',
    'Pruszków': 'Mazowieckie', 'Ostrołęka': 'Mazowieckie',
    'Kraków': 'Małopolskie', 'Tarnów': 'Małopolskie', 'Nowy Sącz': 'Małopolskie',
    'Zakopane': 'Małopolskie', 'Skawina': 'Małopolskie', 'Wieliczka': 'Małopolskie',
    'Dobczyce': 'Małopolskie', 'Oświęcim': 'Małopolskie', 'Jordanów': 'Małopolskie',
    'Łódź': 'Łódzkie', 'Piotrków Trybunalski': 'Łódzkie',
    'Wrocław': 'Dolnośląskie', 'Legnica': 'Dolnośląskie', 'Wałbrzych': 'Dolnośląskie',
    'Lubin': 'Dolnośląskie', 'Głogów': 'Dolnośląskie',
    'Poznań': 'Wielkopolskie', 'Kalisz': 'Wielkopolskie', 'Konin': 'Wielkopolskie',
    'Ostrow Wielkopolski': 'Wielkopolskie', 'Leszno': 'Wielkopolskie',
    'Gdańsk': 'Pomorskie', 'Gdynia': 'Pomorskie', 'Słupsk': 'Pomorskie',
    'Szczecin': 'Zachodniopomorskie', 'Koszalin': 'Zachodniopomorskie', 'Stargard': 'Zachodniopomorskie',
    'Bydgoszcz': 'Kujawsko-Pomorskie', 'Toruń': 'Kujawsko-Pomorskie',
    'Grudziądz': 'Kujawsko-Pomorskie', 'Włocławek': 'Kujawsko-Pomorskie', 'Inowrocław': 'Kujawsko-Pomorskie',
    'Lublin': 'Lubelskie', 'Zamość': 'Lubelskie', 'Chełm': 'Lubelskie',
    'Białystok': 'Podlaskie', 'Suwalki': 'Podlaskie',
    'Ełk': 'Warmińsko-Mazurskie', 'Olsztyn': 'Warmińsko-Mazurskie', 'Elbląg': 'Warmińsko-Mazurskie',
    'Rzeszów': 'Podkarpackie', 'Przemyśl': 'Podkarpackie',
    'Kielce': 'Świętokrzyskie', 'Starachowice': 'Świętokrzyskie',
    'Katowice': 'Śląskie', 'Zabrze': 'Śląskie', 'Gliwice': 'Śląskie',
    'Bytom': 'Śląskie', 'Rybnik': 'Śląskie', 'Ruda Śląska': 'Śląskie',
    'Tychy': 'Śląskie', 'Chorzów': 'Śląskie', 'Jaworzno': 'Śląskie',
    'Jastrzębie-Zdrój': 'Śląskie', 'Bielsko-Biała': 'Śląskie', 'Mysłowice': 'Śląskie',
    'Czechowice-Dziedzice': 'Śląskie', 'Żarki': 'Śląskie', 'Myszków': 'Śląskie',
    'Zawiercie': 'Śląskie', 'Pszczyna': 'Śląskie', 'Tarnowskie Góry': 'Śląskie',
    'Koziegłowy': 'Śląskie', 'Zory': 'Śląskie',
    'Opole': 'Opolskie',
    'Zielona Góra': 'Lubuskie', 'Gorzów Wielkopolski': 'Lubuskie',
};

// Search city function (moved to global scope)
function searchCity() {
    const cityName = $id('city-search')?.value.trim();
    const dropdown = $id('city-dropdown');

    if (dropdown) {
        dropdown.style.display = 'none';
        dropdown.style.visibility = 'hidden';
        dropdown.style.opacity = '0';
    }
    isDropdownOpen = false;

    if (!cityName) {
        console.log('No city name entered');
        return;
    }

    // Validate if city exists in available cities (case-insensitive)
    const normalizedCityName = cityName.toLowerCase();
    const cityExists = allCities.some(city =>
        city.toLowerCase() === normalizedCityName
    );

    if (!cityExists) {
        console.log(`City "${cityName}" not found in available cities`);
        const container = $id('city-tab');
        if (container) {
            container.innerHTML = `<p class="info-message">${translations[currentLang]['city-not-found']}</p>`;
        }
        return;
    }

    console.log(`Searching for city: ${cityName}`);

    // If currently in Global Top 10, automatically switch to City Rankings
    const globalTab = $id('global-tab');
    if (globalTab && globalTab.classList.contains('active')) {
        console.log('Auto-switching from Global Top 10 to City Rankings');
        showTab('city');
    }

    const limit = $id('kebab-count')?.value || 10;
    // Set active city for UI highlighting
    window.currentCity = cityName;
    checkAndLoadRankings(cityName, limit);

    // Re-populate selector to show highlight
    if (typeof availableCities !== 'undefined' && availableCities.length > 0) {
        populateCitySelector(availableCities);
    }

    // Update URL for sharing (same as in selectCity)
    updateCityUrl(cityName);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Sync UI with initial language
    document.querySelectorAll('.lang-flag').forEach(f => f.classList.remove('active'));
    document.querySelector(`.lang-flag[data-lang="${currentLang}"]`)?.classList.add('active');

    setupLanguageSwitcher();
    const hasRankingWidgets = $id('global-tab') || $id('city-tab');
    if (hasRankingWidgets) {
        loadCities();
        loadGlobalRankings();
        startCountdown();

        // Handle URL routing and initial city
        handleUrlRouting();

        // Auto-load Kraków as default city on home page
        const isHomePage = window.location.pathname === '/' || window.location.pathname === '';
        if (isHomePage) {
            const cityRankings = $id('city-tab');
            const searchInput = $id('city-search');
            const searchValue = searchInput ? searchInput.value.trim() : '';
            const hasEmptyRankings = cityRankings && cityRankings.innerHTML.includes('search-prompt');
            const shouldLoadKrakow = !searchValue || (searchValue === 'Kraków' && hasEmptyRankings);
            if (shouldLoadKrakow) {
                autoLoadKrakowAsDefault();
            }
        }
    }
    const searchInput = $id('city-search');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') searchCity();
        });
    }

    // Initialize kebab count slider
    const kebabCountSlider = $id('kebab-count');
    const kebabCountValue = $id('kebab-count-value');
    if (kebabCountSlider && kebabCountValue) {
        let debounceTimer;
        kebabCountSlider.addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            kebabCountValue.textContent = value;
            console.log(`Slider value changed to: ${value}`);

            // Debounce API calls
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const currentCity = $id('city-search')?.value;
                const globalTab = $id('global-tab');
                if (currentCity && globalTab && !globalTab.classList.contains('active')) {
                    console.log(`Loading ${value} kebabs for ${currentCity}`);
                    checkAndLoadRankings(currentCity, value);
                } else {
                    console.log(`Loading Top ${value} for Poland`);
                    loadGlobalRankings(value);
                }
            }, 500); // 500ms delay
        });
    }

    // Add event listener for search button
    const searchButton = $id('search-button');
    if (searchButton) {
        searchButton.addEventListener('click', searchCity);
        console.log('Search button event listener added');
    }

    // URGENT FIX: Move kebab count slider to map bottom on mobile
    if (window.innerWidth <= 768) {
        const slider = document.querySelector('.kebab-count-slider');
        const mapContainer = document.querySelector('.map-container');

        if (slider && mapContainer) {
            console.log('Moving slider to map container for mobile');

            // Move slider into map container
            mapContainer.appendChild(slider);

            // Apply overlay styling
            slider.style.position = 'absolute';
            slider.style.bottom = '15px';
            slider.style.left = '50%';
            slider.style.transform = 'translateX(-50%)';
            slider.style.zIndex = '1000';
            slider.style.background = 'rgba(255,255,255,0.95)';
            slider.style.borderRadius = '20px';
            slider.style.padding = '10px 20px';
            slider.style.boxShadow = '0 3px 12px rgba(0,0,0,0.25)';
            slider.style.fontSize = '12px';
            slider.style.width = 'auto';
            slider.style.margin = '0';
            slider.style.minWidth = '260px';

            // Style the slider input
            const sliderInput = slider.querySelector('input[type="range"]');
            if (sliderInput) {
                sliderInput.style.height = '6px';
                sliderInput.style.margin = '3px 0';
            }

            // Style the value display
            const valueDisplay = slider.querySelector('#kebab-count-value');
            if (valueDisplay) {
                valueDisplay.style.fontSize = '12px';
                valueDisplay.style.padding = '2px 6px';
                valueDisplay.style.minWidth = '20px';
            }

            console.log('Slider successfully moved and styled for mobile');
        } else {
            console.log('Slider or map container not found for mobile relocation');
        }
    }
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        const dropdown = $id('city-dropdown');
        const searchInput = $id('city-search');
        const dropdownArrow = document.querySelector('.dropdown-arrow');

        if (dropdown &&
            !searchInput.contains(e.target) &&
            !dropdown.contains(e.target) &&
            (!dropdownArrow || !dropdownArrow.contains(e.target))) {
            dropdown.style.display = 'none';
            dropdown.style.visibility = 'hidden';
            dropdown.style.opacity = '0';
            isDropdownOpen = false;
        }
    });

    // --- Mega Menu Interactivity ---
    const megaMenu = $id('mega-menu');
    const megaMenuTrigger = $id('mega-menu-trigger');
    const closeMegaMenu = $id('close-mega-menu');

    function toggleMegaMenu(show) {
        if (!megaMenu) return;
        if (show) {
            megaMenu.classList.remove('hidden');
            megaMenu.classList.add('flex');
            document.body.style.overflow = 'hidden';
            setTimeout(() => {
                megaMenu.style.opacity = '1';
                megaMenu.style.transform = 'translateY(0)';
                const si = document.getElementById('city-search-input');
                if (si) { clearCitySearch(); si.focus(); }
            }, 10);
        } else {
            megaMenu.style.opacity = '0';
            megaMenu.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                megaMenu.classList.add('hidden');
                megaMenu.classList.remove('flex');
                document.body.style.overflow = '';
            }, 300);
        }
    }

    if (megaMenuTrigger) {
        megaMenuTrigger.onclick = (e) => {
            e.preventDefault();
            toggleMegaMenu(true);
        };
    }
    
    if (closeMegaMenu) {
        closeMegaMenu.onclick = () => toggleMegaMenu(false);
    }

    const megaMenuTop10 = $id('mega-menu-top10');
    if (megaMenuTop10) {
        megaMenuTop10.onclick = () => {
            toggleMegaMenu(false);
            showTab('global');
        };
    }
    
    // Close on background click
    if (megaMenu) {
        megaMenu.onclick = (e) => {
            if (e.target === megaMenu) toggleMegaMenu(false);
        };
    }

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && megaMenu && !megaMenu.classList.contains('hidden')) {
            toggleMegaMenu(false);
        }
    });

    // Close mega menu when clicking any link inside it
    const megaMenuLinks = document.querySelectorAll('#mega-menu a');
    megaMenuLinks.forEach(link => {
        link.addEventListener('click', () => {
            toggleMegaMenu(false);
        });
    });
});

// Countdown timer functionality
async function startCountdown() {
    const cd = $id('countdown');
    if (!cd) {
        console.warn('Countdown element not found');
        return;
    }

    console.log('Initializing countdown timer...');

    // Try to get last update from localStorage first
    try {
        const storedLastUpdate = localStorage.getItem('lastUpdate');
        const storedInterval = localStorage.getItem('updateInterval');

        if (storedLastUpdate && storedInterval) {
            console.log('Found cached timer data in localStorage');
            const lastUpdate = new Date(storedLastUpdate);
            const interval = parseInt(storedInterval);

            if (!isNaN(lastUpdate.getTime()) && !isNaN(interval)) {
                startCountdownTimer(lastUpdate, interval);
            } else {
                console.warn('Invalid date or interval in localStorage');
            }
        }
    } catch (err) {
        console.error('Error reading localStorage:', err);
    }

    // Always fetch fresh data from API
    try {
        console.log('Fetching fresh timer data from API...');
        const res = await fetch('/api/last-update');

        if (!res.ok) {
            throw new Error(`API request failed with status ${res.status}`);
        }

        const data = await res.json();
        console.log('API response:', data);

        if (data.status !== 'success' || !data.last_update) {
            throw new Error('Invalid API response format');
        }

        let lastUpdate = new Date(data.last_update);
        const interval = data.update_interval_days || 6;

        // If the timestamp is in the future (just refreshed), use current time
        if (lastUpdate > new Date()) {
            lastUpdate = new Date();
        }

        if (isNaN(lastUpdate.getTime())) {
            throw new Error('Invalid date from API');
        }

        // Store in localStorage
        try {
            localStorage.setItem('lastUpdate', data.last_update);
            localStorage.setItem('updateInterval', interval.toString());
            console.log('Stored timer data in localStorage');
        } catch (err) {
            console.error('Error saving to localStorage:', err);
        }

        // If API indicates refresh was initiated, show message
        if (data.message && data.message.includes('refresh')) {
            console.log('Data refresh initiated by API');
            cd.textContent = translations[currentLang]['refreshing'];
            setTimeout(() => startCountdownTimer(lastUpdate, interval), 2000);
        } else {
            startCountdownTimer(lastUpdate, interval);
        }
    } catch (err) {
        console.error('Error initializing countdown:', err);
        cd.textContent = '--:--:--';
    }
}

function startCountdownTimer(lastUpdate, intervalDays) {
    clearInterval(countdownInterval);
    countdownInterval = setInterval(() => updateCountdownDisplay(lastUpdate, intervalDays), 1000);
    updateCountdownDisplay(lastUpdate, intervalDays);
}

function updateCountdownDisplay(lastUpdate, intervalDays) {
    const cd = $id('countdown');
    if (!cd) {
        console.warn('Countdown element not found in update');
        return;
    }

    try {
        const now = new Date();
        const nextUpdate = new Date(lastUpdate.getTime() + intervalDays * 864e5);
        const diff = nextUpdate - now;

        if (diff <= 0) {
            cd.textContent = translations[currentLang]['refreshing'];
            console.log('Countdown reached zero - triggering refresh');
            // Force refresh when countdown expires
            if ($id('global-tab')?.classList.contains('active')) {
                loadGlobalRankings();
            } else {
                const cityName = $id('city-search')?.value;
                if (cityName) checkAndLoadRankings(cityName, $id('kebab-count')?.value || 10);
            }
            // Restart countdown after 2 seconds
            setTimeout(() => {
                const now = new Date();
                // Fetch fresh API data instead of arbitrarily adding intervalDays
                startCountdown();
            }, 2000);
            return;
        }

        const d = Math.floor(diff / 864e5);
        const h = Math.floor((diff % 864e5) / 36e5);
        const m = Math.floor((diff % 36e5) / 6e4);
        const s = Math.floor((diff % 6e4) / 1000);

        // Enhanced format: 03d 12:45:09
        const days = d > 0 ? `${d}d ` : '';
        const hours = h.toString().padStart(2, '0');
        const minutes = m.toString().padStart(2, '0');
        const seconds = s.toString().padStart(2, '0');

        cd.textContent = `${days}${hours}:${minutes}:${seconds}`;
    } catch (err) {
        console.error('Error updating countdown display:', err);
        cd.textContent = '--:--:--';
    }
}

// Setup language switcher
function setupLanguageSwitcher() {
    // Initial sync
    switchLanguage(currentLang, false); // Don't reload if initial

    document.querySelectorAll('.lang-flag').forEach(f =>
        f.addEventListener('click', () => switchLanguage(f.dataset.lang))
    );
}

// Switch language
function switchLanguage(lang, save = true) {
    console.log(`Switching language to: ${lang}`);
    currentLang = lang;
    if (save) {
        localStorage.setItem('preferredLang', lang);
    }

    document.documentElement.lang = lang; // Update HTML lang tag
    document.querySelectorAll('.lang-flag').forEach(f => f.classList.remove('active'));
    document.querySelector(`.lang-flag[data-lang="${lang}"]`)?.classList.add('active');
    document.querySelectorAll('[data-translate]').forEach(el => {
        const key = el.dataset.translate;
        if (translations[lang][key]) el.textContent = translations[lang][key];
    });
    const searchInput = $id('city-search');
    if (searchInput) {
        searchInput.placeholder = translations[lang]['search-label'] ||
            searchInput.dataset[`placeholder${lang.charAt(0).toUpperCase() + lang.slice(1)}`];
    }

    // Refresh count label if exists
    const countLabel = document.querySelector('label[for="kebab-count"]');
    if (countLabel && translations[lang]['show-top']) {
        countLabel.textContent = translations[lang]['show-top'];
    }

    // Handle HTML translations (like Top 10 button)
    document.querySelectorAll('[data-translate-html]').forEach(el => {
        const key = el.dataset.translateHtml;
        if (translations[lang][key]) el.innerHTML = translations[lang][key];
    });

    // Refresh city grid with new language
    if (allCities && allCities.length > 0) {
        populateCityGrid();
    }

    // Re-render city rankings with new language
    const cityName = $id('city-search')?.value;
    if (cityName) {
        const limit = $id('kebab-count')?.value || 10;
        checkAndLoadRankings(cityName, limit);
    }
    if ($id('global-tab')?.classList.contains('active')) loadGlobalRankings();
}

// Tab switching
function showTab(tabName) {
    console.log(`Switching to tab: ${tabName}`);

    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
        tab.classList.add('hidden');
    });

    // Deactivate all tab buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });

    // Show selected tab content
    const targetTab = $id(tabName + '-tab');
    if (targetTab) {
        targetTab.classList.remove('hidden');
        targetTab.classList.add('active');
    }

    // Activate the clicked button
    if (event && event.currentTarget) {
        event.currentTarget.classList.add('active');
    } else {
        // Fallback for programmatic calls
        const btn = document.querySelector(`.tab-button[onclick*="${tabName}"]`);
        if (btn) btn.classList.add('active');
    }

    // Handle map visibility based on active tab
    const cityMap = document.getElementById('kebab-map');
    const globalMap = document.getElementById('kebab-map-global');

    if (tabName === 'global') {
        if (cityMap) cityMap.style.display = 'none';
        if (globalMap) globalMap.style.display = 'block';
        if (globalKebabMap) {
            setTimeout(() => globalKebabMap.invalidateSize(), 100);
        }

        // Clear active city to remove highlight from city selector
        window.currentCity = null;
        if (typeof availableCities !== 'undefined' && availableCities.length > 0) {
            populateCitySelector(availableCities);
        }

        loadGlobalRankings();
    } else {
        if (cityMap) cityMap.style.display = 'block';
        if (globalMap) globalMap.style.display = 'none';
        if (kebabMap) {
            setTimeout(() => kebabMap.invalidateSize(), 100);
        }

        // Show search prompt ONLY if no city is currently selected or being searched
        const searchInput = $id('city-search');
        const cityName = searchInput ? searchInput.value.trim() : '';
        const cityTab = $id('city-tab');

        // Final check: don't clear if rankings are currently loading or have data
        const currentlyLoading = cityTab && cityTab.innerHTML.includes('loading');
        const hasRankings = cityTab && cityTab.querySelector('.glass-card');

        if (!cityName && !hasRankings && !currentlyLoading && cityTab) {
            cityTab.innerHTML = `<p class="info-message">${translations[currentLang]['search-prompt']}</p>`;
        }
    }
}

// Load cities for autocomplete and city grid with caching
async function loadCities() {
    try {
        console.log('Loading cities from API with caching...');

        // Check if we have cached cities in localStorage
        const cachedCities = localStorage.getItem('cachedCities');
        const cacheTimestamp = localStorage.getItem('citiesCacheTimestamp');
        // Use cached data if it's fresh (extended to 24 hours to prevent "turning off after a day" issue)
        const cacheExpiry = 86400000; // 24 hours in milliseconds
        if (cachedCities && cacheTimestamp) {
            const age = Date.now() - parseInt(cacheTimestamp);
            if (age < cacheExpiry) {
                console.log('Using cached cities data (age:', age, 'ms)');
                const data = JSON.parse(cachedCities);
                processCitiesData(data);
                return;
            } else {
                console.log('Cache expired, fetching fresh data');
            }
        }

        // Fetch fresh data from API
        const response = await fetch('/api/cities');
        const data = await response.json();

        if (data.status === 'success') {
            console.log('Successfully loaded', data.data.length, 'cities');

            // Cache the data
            try {
                localStorage.setItem('cachedCities', JSON.stringify(data));
                localStorage.setItem('citiesCacheTimestamp', Date.now().toString());
                console.log('Cities data cached in localStorage');
            } catch (err) {
                console.error('Error caching cities data:', err);
            }

            processCitiesData(data);
        } else {
            console.log('Failed to load cities:', data.message);
        }
    } catch (error) {
        console.error('Error loading cities:', error);

        // Try to use cached data as fallback even if expired
        const cachedCities = localStorage.getItem('cachedCities');
        if (cachedCities) {
            console.log('Using expired cached data as fallback');
            const data = JSON.parse(cachedCities);
            processCitiesData(data);
        }
    }
}

// Process cities data and update UI
function processCitiesData(data) {
    availableCities = data.data.map(city => city.name);
    allCities = [...availableCities]; // Initialize allCities

    // Sort by population (major cities first) then alphabetically
    const majorCities = [
        'Warszawa', 'Kraków', 'Wrocław', 'Łódź', 'Poznań',
        'Gdańsk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Białystok',
        'Katowice', 'Gdynia', 'Częstochowa', 'Radom', 'Toruń',
        'Sosnowiec', 'Kielce', 'Rzeszów', 'Gliwice', 'Zabrze',
        'Olsztyn', 'Bielsko-Biała', 'Bytom', 'Zielona Góra', 'Rybnik',
        'Ruda Śląska', 'Opole', 'Tychy', 'Gorzów Wielkopolski', 'Elbląg'
    ];

    availableCities.sort((a, b) => {
        const indexA = majorCities.indexOf(a);
        const indexB = majorCities.indexOf(b);

        if (indexA !== -1 && indexB !== -1) return indexA - indexB; // Both in major list
        if (indexA !== -1) return -1; // Only A is major
        if (indexB !== -1) return 1; // Only B is major
        return a.localeCompare(b, 'pl'); // Neither is major, sort alphabetically
    });
    console.log('Cities initialized and sorted by population priority');

    // Populate city grid
    populateCityGrid();

    // Populate top horizontal selector
    populateCitySelector(availableCities);
}

// Populate city grid with all available cities using lazy loading
function populateCityGrid() {
    const cityGrid = document.getElementById('city-grid');
    if (!cityGrid) {
        console.log('City grid element not found');
        return;
    }

    if (!allCities || allCities.length === 0) {
        console.log('No cities available for grid');
        cityGrid.innerHTML = '<div class="loading">No cities available</div>';
        return;
    }

    console.log(`Populating city grid with ${allCities.length} cities using lazy loading`);

    // Sort cities alphabetically
    const sortedCities = [...allCities].sort((a, b) => a.localeCompare(b, 'pl'));

    // Clear the grid first
    cityGrid.innerHTML = '';

    // Create a document fragment for better performance
    const fragment = document.createDocumentFragment();

    // Create initial batch of cities (first 20)
    const initialBatchSize = Math.min(20, sortedCities.length);

    for (let i = 0; i < initialBatchSize; i++) {
        const city = sortedCities[i];
        const cityElement = createCityGridItem(city);
        fragment.appendChild(cityElement);
    }

    // Add the initial batch to the grid
    cityGrid.appendChild(fragment);

    // If there are more cities, set up lazy loading
    if (sortedCities.length > initialBatchSize) {
        setupLazyLoading(cityGrid, sortedCities, initialBatchSize);
    }

    console.log('City grid populated successfully with lazy loading');
}

// Create a single city grid item element
function createCityGridItem(city) {
    const citySlug = city.toLowerCase()
        .replace(/ /g, '-')
        .replace(/ł/g, 'l')
        .replace(/ó/g, 'o')
        .replace(/ą/g, 'a')
        .replace(/ę/g, 'e')
        .replace(/ć/g, 'c')
        .replace(/ń/g, 'n')
        .replace(/ś/g, 's')
        .replace(/ź/g, 'z')
        .replace(/ż/g, 'z');

    const item = document.createElement('a');
    item.className = 'city-grid-item text-center';
    item.href = `/kebab-${citySlug}`;
    item.onclick = (e) => {
        e.preventDefault();
        selectCity(city);
    };

    const nameDiv = document.createElement('div');
    nameDiv.className = 'city-name';
    nameDiv.textContent = city;

    const link = document.createElement('a');
    link.href = `/${citySlug}`;
    link.className = 'city-link';
    link.textContent = currentLang === 'en' ? 'View rankings' : 'Zobacz ranking';
    link.onclick = (e) => {
        e.stopPropagation();
        selectCity(city);
        return false;
    };

    item.appendChild(nameDiv);
    item.appendChild(link);

    return item;
}

// Set up lazy loading for remaining cities
function setupLazyLoading(cityGrid, sortedCities, loadedCount) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && loadedCount < sortedCities.length) {
                // Load next batch of cities
                const batchSize = 10;
                const endIndex = Math.min(loadedCount + batchSize, sortedCities.length);

                const fragment = document.createDocumentFragment();
                for (let i = loadedCount; i < endIndex; i++) {
                    const city = sortedCities[i];
                    const cityElement = createCityGridItem(city);
                    fragment.appendChild(cityElement);
                }

                cityGrid.appendChild(fragment);
                loadedCount = endIndex;

                // If all cities are loaded, disconnect the observer
                if (loadedCount >= sortedCities.length) {
                    observer.disconnect();
                    console.log('All cities loaded via lazy loading');
                }
            }
        });
    }, {
        rootMargin: '100px', // Start loading when within 100px of viewport
        threshold: 0.1
    });

    // Create a sentinel element at the end of the grid
    const sentinel = document.createElement('div');
    sentinel.className = 'lazy-load-sentinel';
    sentinel.style.height = '1px';
    sentinel.style.width = '1px';
    sentinel.style.opacity = '0';
    sentinel.style.pointerEvents = 'none';
    cityGrid.appendChild(sentinel);

    // Observe the sentinel
    observer.observe(sentinel);
}

// Filter cities as user types
let isDropdownOpen = false;

function toggleCityDropdown() {
    console.log('Toggling dropdown...');
    const dropdown = document.getElementById('city-dropdown');
    const searchInput = document.getElementById('city-search');

    if (!dropdown || !searchInput) {
        console.error('Dropdown or search input elements not found');
        return;
    }

    // Force load cities if not loaded
    if (!allCities || allCities.length === 0) {
        console.log('Cities not loaded, loading...');
        loadCities();
        return;
    }

    // Check current state
    const isCurrentlyOpen = dropdown.style.display === 'block';
    console.log('Current state:', isCurrentlyOpen ? 'open' : 'closed');

    if (!isCurrentlyOpen) {
        console.log('Opening dropdown with', allCities.length, 'cities');
        dropdown.innerHTML = '';
        allCities.sort().forEach(city => {
            const item = document.createElement('div');
            item.className = 'px-4 py-3 hover:bg-white/5 cursor-pointer text-sm text-gray-300 hover:text-white transition-colors border-b border-white/5 last:border-0';
            item.textContent = city;
            item.onclick = () => {
                console.log('Selected city:', city);
                selectCity(city);
            };
            dropdown.appendChild(item);
        });

        dropdown.classList.remove('hidden');
        dropdown.classList.add('active');
        searchInput.focus();
    } else {
        console.log('Closing dropdown');
        dropdown.classList.remove('active');
        dropdown.classList.add('hidden');
        dropdown.style.display = 'none'; // Ensure it's hidden for older browsers too
    }


    // Update global state
    isDropdownOpen = !isCurrentlyOpen;
    console.log('New state:', isDropdownOpen ? 'open' : 'closed');
}

function filterCities(searchTerm) {
    console.log(`Filtering cities for: "${searchTerm}"`);
    const dropdown = document.getElementById('city-dropdown');

    if (!dropdown) {
        console.error('City dropdown element not found');
        return;
    }

    dropdown.innerHTML = '';

    // Check if allCities is available
    if (!allCities || allCities.length === 0) {
        console.log('Cities not loaded yet, loading...');
        loadCities();
        return;
    }

    console.log(`Searching through ${allCities.length} cities`);

    const filtered = allCities.filter(city =>
        city.toLowerCase().includes(searchTerm.toLowerCase())
    );

    console.log(`Found ${filtered.length} matching cities`);

    if (filtered.length > 0) {
        filtered.forEach(city => {
            const item = document.createElement('div');
            item.className = 'px-4 py-3 hover:bg-white/5 cursor-pointer text-sm text-gray-300 hover:text-white transition-colors border-b border-white/5 last:border-0';
            item.textContent = city;
            item.onclick = () => {
                console.log(`Selected city: ${city}`);
                selectCity(city);
            };
            dropdown.appendChild(item);
        });

        dropdown.classList.remove('hidden');
        dropdown.classList.add('active');
        console.log('Dropdown shown with filtered cities');
    } else {
        dropdown.classList.remove('active');
        dropdown.classList.add('hidden');
        dropdown.style.display = 'none';
        console.log('No matching cities found, hiding dropdown');
    }

}

// --- START: UPDATED AND NEW FUNCTIONS ---

// Update your existing selectCity function
function selectCity(cityName) {
    const dropdown = $id('city-dropdown');
    const searchInput = $id('city-search');
    if (searchInput) searchInput.value = cityName;

    // Hide dropdown on both desktop and mobile
    if (dropdown) {
        dropdown.classList.remove('active');
        dropdown.classList.add('hidden');
        dropdown.style.display = 'none';
        dropdown.style.visibility = 'hidden';
        dropdown.style.opacity = '0';
    }

    // Close Mega Menu if it's open
    const megaMenu = $id('mega-menu');
    if (megaMenu) {
        megaMenu.classList.add('hidden');
        megaMenu.classList.remove('flex');
    }

    isDropdownOpen = false;

    // If currently in Global Top 10, automatically switch to City Rankings
    const globalTab = $id('global-tab');
    if (globalTab && globalTab.classList.contains('active')) {
        console.log('Auto-switching from Global Top 10 to City Rankings');
        showTab('city');
    }

    const limit = $id('kebab-count')?.value || 10;
    // Reset city filters only when switching to a different city
    if (cityName !== window.currentCity) {
        window.activeFilters.city = {};
    }
    // Set active city for UI highlighting
    window.currentCity = cityName;
    checkAndLoadRankings(cityName, limit);

    // Re-populate selector to show highlight
    if (typeof availableCities !== 'undefined' && availableCities.length > 0) {
        populateCitySelector(availableCities);
    }

    // Update URL for sharing
    updateCityUrl(cityName);
}

// Load rankings with AI insights but preserve rank_score ordering
async function checkAndLoadRankings(cityName, limit = 10) {
    const cacheKey = `${cityName}_${limit}_${currentLang}`;
    const container = $id('city-tab');

    // 1. Start Transition (Blur & Fade existing content)
    const hasExistingContent = container.children.length > 0 && !container.innerHTML.includes('search-prompt');
    if (hasExistingContent) {
        container.classList.remove('ranking-fade-in');
        container.classList.add('rankings-transitioning');
    }

    // Reset scroll position of sidebar to top immediately
    const sidebarContent = $id('sidebar-content');
    if (sidebarContent) {
        sidebarContent.scrollTo({ top: 0, behavior: 'auto' });
    }

    // Return from cache if available for instant loading
    if (rankingCache[cacheKey]) {
        console.log(`Loading ${cityName} from cache (INSTANT)...`);
        const cachedData = rankingCache[cacheKey];

        // Update map first (it's fast)
        if (typeof updateMapWithKebabs === 'function') {
            updateMapWithKebabs(cachedData);
        }

        // Render instantly without any timeout
        displayRankings(cachedData, container, cityName, false);
        container.classList.remove('rankings-transitioning');
        return;
    }

    console.log(`Fetching rankings for ${cityName} with limit: ${limit}`);

    // 2. Smart Skeleton Loading
    // Instead of replacing innerHTML instantly and causing a flash, we only show skeletons
    // if the request takes more than 400ms.
    let skeletonsShown = false;
    const skeletonTimer = setTimeout(() => {
        skeletonsShown = true;
        container.classList.remove('rankings-transitioning');
        container.innerHTML = renderSkeletons(5);
        container.classList.add('ranking-fade-in');
    }, 400);

    try {
        const url = `/api/rankings/${encodeURIComponent(cityName)}/ai?lang=${currentLang}&limit=${limit}`;

        // SINGLE FETCH: The /ai endpoint already returns merged rankings
        const response = await fetch(url);
        const result = await response.json();

        if (result.status !== 'success') {
            throw new Error('Failed to load rankings data');
        }

        const mergedData = result.data;
        clearTimeout(skeletonTimer);

        // Store in cache
        rankingCache[cacheKey] = mergedData;

        // 3. Final Render
        if (skeletonsShown) {
            // Skeletons are visible, blur them out briefly, then render
            container.classList.remove('ranking-fade-in');
            container.classList.add('rankings-transitioning');
            setTimeout(() => {
                if (typeof updateMapWithKebabs === 'function') updateMapWithKebabs(mergedData);
                container.classList.remove('rankings-transitioning');
                displayRankings(mergedData, container, cityName, false);
            }, 50); // Faster transition from skeleton to data
        } else {
            // Data loaded fast. Render immediately as we didn't show skeletons.
            if (typeof updateMapWithKebabs === 'function') updateMapWithKebabs(mergedData);
            container.classList.remove('rankings-transitioning');
            displayRankings(mergedData, container, cityName, false);
        }

    } catch (error) {
        clearTimeout(skeletonTimer);
        console.error('Error loading rankings:', error);
        container.classList.remove('rankings-transitioning');
        container.innerHTML = `<p class="info-message">${translations[currentLang]['error-loading']}</p>`;
    }
}

// Load rankings for selected city (used as a fallback)
async function loadCityRankings(cityName) {
    if (!cityName) {
        $id('city-tab').innerHTML = `<p class="info-message">${translations[currentLang]['search-prompt']}</p>`;
        return;
    }
    const container = $id('city-tab');
    container.innerHTML = `<div class="loading">${translations[currentLang]['loading']}</div>`;
    try {
        const response = await fetch(`/api/rankings/${encodeURIComponent(cityName)}`);
        const data = await response.json();
        if (data.status === 'success') {
            displayRankings(data.data, container, cityName);
        } else {
            container.innerHTML = `<p class="info-message">${translations[currentLang]['error-loading']}</p>`;
        }
    } catch (error) {
        console.error('Error loading rankings:', error);
        container.innerHTML = `<p class="info-message">${translations[currentLang]['error-loading']}</p>`;
    }
}

// Load global top rankings
async function loadGlobalRankings(limit = null) {
    if (!limit) {
        limit = $id('kebab-count')?.value || 10;
    }
    const container = $id('global-tab');
    try {
        const [rankResp, statsResp] = await Promise.all([
            fetch(`/api/rankings/global?limit=${limit}`),
            fetch('/api/stats'),
        ]);
        const data = await rankResp.json();
        const stats = await statsResp.json();

        if (data.status === 'success') {
            // Stats bar
            const isEn = (window.currentLang || 'pl') === 'en';
            const placesLabel = isEn
                ? `<strong>${(stats.total_places || 0).toLocaleString()}</strong> kebab spots analyzed`
                : `Zbadano <strong>${(stats.total_places || 0).toLocaleString()}</strong> kebabów`;
            const citiesLabel = isEn
                ? `across <strong>${stats.total_cities || 0}</strong> cities in Poland`
                : `w <strong>${stats.total_cities || 0}</strong> miastach w Polsce`;

            const statsBar = `<div style="display:flex;align-items:center;gap:10px;padding:10px 16px;margin-bottom:12px;border-radius:12px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);font-size:13px;color:#cbd5e1;">
                <span style="position:relative;display:inline-flex;width:10px;height:10px;flex-shrink:0;">
                    <span style="position:absolute;display:inline-flex;width:100%;height:100%;border-radius:50%;background:#f97316;opacity:0.75;animation:kebab-ping 1.4s cubic-bezier(0,0,0.2,1) infinite;"></span>
                    <span style="position:relative;display:inline-flex;width:10px;height:10px;border-radius:50%;background:#ea580c;"></span>
                </span>
                <span>${placesLabel} ${citiesLabel}</span>
            </div>
            <style>@keyframes kebab-ping{75%,100%{transform:scale(2);opacity:0;}}</style>`;

            container.innerHTML = statsBar;
            const listWrapper = document.createElement('div');
            container.appendChild(listWrapper);
            displayRankings(data.data, listWrapper, null, true);

            window.globalRankingCache = data.data;
            updateGlobalMapWithKebabs(data.data);
        } else {
            container.innerHTML = '<p class="info-message">Error loading global rankings. Please try again.</p>';
        }
    } catch (error) {
        console.error('Error loading global rankings:', error);
        container.innerHTML = '<p class="info-message">Error loading global rankings. Please try again.</p>';
    }
}

// Update map when city rankings are loaded
function updateMapWithKebabs(kebabPlaces) {
    // Only initialize if not already done AND either desktop or explicitly requested
    if (!kebabMap) {
        if (window.innerWidth > 768) {
            initializeMap();
        } else {
            // On mobile, we don't auto-init here. 
            // Marker addition will happen when user clicks 'Mapa' and triggers init.
            return;
        }
    }
    addKebabMarkers(kebabPlaces);
}

// Update global map when global rankings are loaded
function updateGlobalMapWithKebabs(kebabPlaces) {
    if (!globalKebabMap) {
        if (window.innerWidth > 768) {
            initializeGlobalMap();
        } else {
            return;
        }
    }
    addGlobalKebabMarkers(kebabPlaces);
}

// Helper functions consolidated below



// --- URL ROUTING FUNCTIONS ---

// Handle URL routing for city-specific pages
function handleUrlRouting() {
    console.log('🔄 handleUrlRouting() called');

    // Check if we have an initial city from the Flask template
    if (window.initialCity && window.initialCity.trim() !== '') {
        console.log(`✅ Loading initial city from Flask template: ${window.initialCity}`);
        // Set the search input value
        const searchInput = $id('city-search');
        if (searchInput) {
            searchInput.value = window.initialCity;
        }
        // Set active city for UI highlighting
        window.currentCity = window.initialCity;
        if (typeof availableCities !== 'undefined' && availableCities.length > 0) {
            populateCitySelector(availableCities);
        }

        // Load the rankings for this city
        const limit = $id('kebab-count')?.value || 10;
        checkAndLoadRankings(window.initialCity, limit);
        return;
    }

    // Check if we're on a city-specific URL
    const path = window.location.pathname;
    console.log(`🔍 Current path: ${path}`);

    if (path !== '/' && path !== '/blog' && !path.startsWith('/blog/')) {
        // Extract city slug from URL (remove leading slash)
        const citySlug = path.substring(1);
        console.log(`📍 Detected city slug in URL: ${citySlug}`);

        // Handle kebab- prefix URLs
        let actualCitySlug = citySlug;
        if (citySlug.startsWith('kebab-')) {
            actualCitySlug = citySlug.substring(6); // Remove 'kebab-' prefix
            console.log(`🥙 Removed 'kebab-' prefix, actual slug: ${actualCitySlug}`);
        }

        // Wait for cities to load, then try to match
        if (allCities && allCities.length > 0) {
            handleCitySlug(actualCitySlug);
        } else {
            console.log('⏳ Cities not loaded yet, waiting...');
            // If cities aren't loaded yet, wait for them
            const checkCities = setInterval(() => {
                if (allCities && allCities.length > 0) {
                    clearInterval(checkCities);
                    console.log('✅ Cities loaded, now handling slug');
                    handleCitySlug(actualCitySlug);
                }
            }, 100);
        }
    } else {
        console.log('🏠 Home page or blog, no city-specific routing needed');
    }
}

// Handle city slug from URL
function handleCitySlug(citySlug) {
    // Try to find matching city
    const matchingCity = allCities.find(city => {
        // Try direct match
        if (city.toLowerCase() === citySlug.toLowerCase()) {
            return true;
        }
        // Try slugified match
        const slugifiedCity = city.toLowerCase()
            .replace(/ /g, '-')
            .replace(/ł/g, 'l')
            .replace(/ó/g, 'o')
            .replace(/ą/g, 'a')
            .replace(/ę/g, 'e')
            .replace(/ć/g, 'c')
            .replace(/ń/g, 'n')
            .replace(/ś/g, 's')
            .replace(/ź/g, 'z')
            .replace(/ż/g, 'z');
        return slugifiedCity === citySlug.toLowerCase();
    });

    if (matchingCity) {
        console.log(`Found matching city: ${matchingCity}`);
        // Set the search input value
        const searchInput = $id('city-search');
        if (searchInput) {
            searchInput.value = matchingCity;
        }
        // Set active city for UI highlighting
        window.currentCity = matchingCity;

        // Load the rankings for this city
        const limit = $id('kebab-count')?.value || 10;
        checkAndLoadRankings(matchingCity, limit);

        // Re-populate selector to show highlight
        if (typeof availableCities !== 'undefined' && availableCities.length > 0) {
            populateCitySelector(availableCities);
        }

        // Update page title for SEO
        document.title = `🥙 Kebab Rank ${matchingCity} - Najlepsze kebaby w ${matchingCity}`;
    } else {
        console.log(`No matching city found for slug: ${citySlug}`);
    }
}


// Update URL when city is selected
function updateCityUrl(cityName) {
    if (!cityName) return;

    // Create slug for the city
    const citySlug = cityName.toLowerCase()
        .replace(/ /g, '-')
        .replace(/ł/g, 'l')
        .replace(/ó/g, 'o')
        .replace(/ą/g, 'a')
        .replace(/ę/g, 'e')
        .replace(/ć/g, 'c')
        .replace(/ń/g, 'n')
        .replace(/ś/g, 's')
        .replace(/ź/g, 'z')
        .replace(/ż/g, 'z');

    // Update URL without page reload
    const newUrl = `/${citySlug}`;
    window.history.pushState({ city: cityName }, '', newUrl);

    // Update page title for SEO
    document.title = `🥙 Kebab Rank ${cityName} - Najlepsze kebaby w ${cityName}`;
}

// Handle browser back/forward buttons
window.addEventListener('popstate', (event) => {
    if (event.state && event.state.city) {
        console.log(`Browser navigation to city: ${event.state.city}`);
        const searchInput = $id('city-search');
        if (searchInput) {
            searchInput.value = event.state.city;
        }
        const limit = $id('kebab-count')?.value || 10;
        checkAndLoadRankings(event.state.city, limit);
    } else {
        // If going back to home page
        console.log('Returning to home page');
        const searchInput = $id('city-search');
        if (searchInput) {
            searchInput.value = '';
        }
        $id('city-tab').innerHTML = `<p class="info-message">${translations[currentLang]['search-prompt']}</p>`;
        document.title = '🥙 Kebab Rank Poland';
    }
});

// Auto-load Kraków immediately on page load
function autoLoadKrakowImmediately() {
    console.log('🚀 Auto-loading Kraków immediately');

    // Check if Kraków is already set as default value
    const searchInput = $id('city-search');
    if (searchInput && searchInput.value === 'Kraków') {
        console.log('✅ Kraków is default value, loading rankings immediately');

        // Switch to City Rankings tab
        const cityTabButton = document.querySelector('.tab-button[onclick*="city"]');
        if (cityTabButton) {
            cityTabButton.click();
        }

        // Load Kraków rankings
        const limit = $id('kebab-count')?.value || 10;
        checkAndLoadRankings('Kraków', limit);

        // Update URL for sharing
        updateCityUrl('Kraków');
    } else {
        console.log('❌ Kraków not found as default value, using fallback');
        autoLoadKrakowAsDefault();
    }
}

// Auto-load Kraków as default city on home page
function autoLoadKrakowAsDefault() {
    const searchInput = $id('city-search');
    const cityRankings = $id('city-tab');
    const searchValue = searchInput ? searchInput.value.trim() : '';
    const hasEmptyRankings = cityRankings && cityRankings.innerHTML.includes('search-prompt');
    const shouldLoadKrakow = !searchValue || (searchValue === 'Kraków' && hasEmptyRankings);

    if (searchInput && shouldLoadKrakow) {
        if (!searchValue) searchInput.value = 'Kraków';

        const cityTabButton = document.querySelector('.tab-button[onclick*="city"]');
        if (cityTabButton && !cityTabButton.classList.contains('active')) {
            cityTabButton.click();
        }

        checkAndLoadRankings('Kraków', $id('kebab-count')?.value || 10);
        updateCityUrl('Kraków');
    }
}


// Helper function for ranking display
function isTopThree(rank) {
    return rank <= 3;
}

// Update helper functions to handle numbers properly
// Consolidated hub for sentiment and trend labeling
function getSentimentClass(sentiment) {
    if (typeof sentiment === 'number') {
        if (sentiment > 0.5) return 'sentiment-very-positive';
        if (sentiment > 0.2) return 'sentiment-positive';
        if (sentiment < -0.5) return 'sentiment-very-negative';
        if (sentiment < -0.2) return 'sentiment-negative';
        return 'sentiment-neutral';
    }
    const label = sentiment?.label || 'neutral';
    return `sentiment-${label}`;
}

function getSentimentLabel(sentiment) {
    if (typeof sentiment === 'number') {
        if (sentiment > 0.5) return translations[currentLang]['very-positive'] || '😍 Bardzo pozytywne';
        if (sentiment > 0.2) return translations[currentLang]['positive'] || '😊 Pozytywne';
        if (sentiment < -0.5) return translations[currentLang]['very-negative'] || '😡 Bardzo negatywne';
        if (sentiment < -0.2) return translations[currentLang]['negative'] || '😞 Negatywne';
        return translations[currentLang]['neutral'] || '😐 Neutralne';
    }
    const label = sentiment?.label || 'neutral';
    return translations[currentLang][label] || label;
}

function getTrendLabel(trend) {
    const value = (typeof trend === 'object' ? trend?.trend : trend) || 'stable';
    const key = value.toLowerCase();
    return translations[currentLang][key] || value;
}

// --- MAP FUNCTIONS ---

function loadLeafletCSS() {
    if (!document.querySelector('link[href*="leaflet.css"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/static/js/leaflet/leaflet.css';
        document.head.appendChild(link);
    }
}

// Queue-based loader: only one <script> ever created; all callers share the same onload
let _leafletLoadCallbacks = [];
let _leafletLoading = false;

function loadLeafletJS(callback) {
    if (window.L) { callback(); return; }
    _leafletLoadCallbacks.push(callback);
    if (_leafletLoading) return;
    _leafletLoading = true;
    const script = document.createElement('script');
    script.src = '/static/js/leaflet/leaflet.js';
    script.onload = function() {
        _leafletLoadCallbacks.forEach(function(cb) { cb(); });
        _leafletLoadCallbacks = [];
    };
    document.head.appendChild(script);
}

// Initialize the city map
function initializeMap() {
    if (window.kebabMap) return;
    loadLeafletCSS();
    loadLeafletJS(function() {
        if (window.kebabMap) return;
        const mapContainer = document.getElementById('kebab-map');
        if (!mapContainer) return;

        // Remove placeholder if it exists
        const placeholder = mapContainer.querySelector('.map-placeholder');
        if (placeholder) {
            placeholder.style.display = 'none';
        }

        // Initialize map centered on Poland
        kebabMap = L.map('kebab-map').setView([52.2370, 21.0175], 6);

        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        }).addTo(kebabMap);

        // Auto-populate markers from cache (fixes race condition when map init is async)
        if (window.currentCity && window.rankingCache) {
            const limit = document.getElementById('kebab-count')?.value || 10;
            const lang = window.currentLang || 'pl';
            const cacheKey = `${window.currentCity}_${limit}_${lang}`;
            if (window.rankingCache[cacheKey]) {
                addKebabMarkers(window.rankingCache[cacheKey]);
            }
        }

        console.log('City map initialized successfully');
    });
}

// Initialize the global map
function initializeGlobalMap() {
    if (window.globalKebabMap) return;
    loadLeafletCSS();
    loadLeafletJS(function() {
        if (window.globalKebabMap) return;
        const mapContainer = document.getElementById('kebab-map-global');
        if (!mapContainer) return;

        // Remove placeholder if it exists
        const placeholder = mapContainer.querySelector('.map-placeholder');
        if (placeholder) {
            placeholder.style.display = 'none';
        }

        // Initialize map with better view for Poland
        globalKebabMap = L.map('kebab-map-global').setView([52.0, 19.0], 6);

        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        }).addTo(globalKebabMap);

        // Auto-populate markers from cache (fixes race condition when map init is async)
        if (window.globalRankingCache) {
            addGlobalKebabMarkers(window.globalRankingCache);
        }

        console.log('Global map initialized successfully');
    });
}

// Clear all existing markers from the city map
function clearMapMarkers() {
    mapMarkers.forEach(marker => {
        kebabMap.removeLayer(marker);
    });
    mapMarkers = [];
}

// Clear all existing markers from the global map
function clearGlobalMapMarkers() {
    globalMapMarkers.forEach(marker => {
        globalKebabMap.removeLayer(marker);
    });
    globalMapMarkers = [];
}

// Add markers for kebab places to city map
function addKebabMarkers(kebabPlaces) {
    if (!kebabMap) {
        console.error('City map not initialized');
        return;
    }

    clearMapMarkers();

    if (!kebabPlaces || kebabPlaces.length === 0) {
        console.log('No kebab places to display on city map');
        return;
    }

    // Filter places with valid coordinates
    const placesWithCoords = kebabPlaces.filter(place =>
        place.latitude && place.longitude &&
        !isNaN(parseFloat(place.latitude)) &&
        !isNaN(parseFloat(place.longitude))
    );

    if (placesWithCoords.length === 0) {
        console.log('No kebab places with valid coordinates for city map');
        return;
    }

    console.log(`Adding ${placesWithCoords.length} markers to city map`);

    // Create bounds for all markers
    const bounds = L.latLngBounds();

    placesWithCoords.forEach((place, index) => {
        const lat = parseFloat(place.latitude);
        const lng = parseFloat(place.longitude);

        // Determine size based on rank
        let markerSize = 38;
        if (index === 0) markerSize = 52;
        else if (index === 1) markerSize = 46;
        else if (index === 2) markerSize = 42;

        // Create custom icon based on rank
        const winnerClass = (index + 1 <= 3) ? `pin-winner-${index + 1}` : '';
        const iconHtml = `
            <div class="premium-pin ${winnerClass}">
                <span class="pin-number">${index + 1}</span>
            </div>
        `;

        const customIcon = L.divIcon({
            html: iconHtml,
            className: 'custom-marker-transparent',
            iconSize: [markerSize, markerSize],
            iconAnchor: [markerSize / 2, markerSize],
            popupAnchor: [0, -markerSize]
        });

        // Create marker
        const marker = L.marker([lat, lng], { icon: customIcon })
            .addTo(kebabMap)
            .bindPopup(`
                <div style="padding: 12px; min-width: 240px; font-family: 'Inter', sans-serif;">
                    <div style="margin-bottom: 8px;">
                         <strong style="font-size: 16px; display: block; margin-bottom: 4px; color: #1e293b;">${place.name}</strong>
                         <span style="font-size: 12px; color: #64748b; display: flex; align-items: center; gap: 4px;">
                            <span style="font-size: 14px;">📍</span> ${place.address}
                         </span>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: ${place.has_ai_analysis ? '1fr 1fr 1fr' : '1fr 1fr'}; gap: 8px; margin-bottom: 8px; background: #f8fafc; padding: 8px; border-radius: 8px;">
                        <div style="text-align: center; border-right: 1px solid #e2e8f0;">
                            <div style="font-size: 10px; color: #64748b; text-transform: uppercase; font-weight: bold;">${translations[currentLang]['score'] || 'Score'}</div>
                            <div style="font-size: 16px; font-weight: 900; color: #ea580c;">${place.rank_score.toFixed(1)}</div>
                        </div>
                        <div style="text-align: center; ${place.has_ai_analysis ? 'border-right: 1px solid #e2e8f0;' : ''}">
                            <div style="font-size: 10px; color: #64748b; text-transform: uppercase; font-weight: bold;">${translations[currentLang]['rating'] || 'Rating'}</div>
                            <div style="font-size: 14px; font-weight: bold; color: #1e293b;">⭐ ${place.rating.toFixed(1)}</div>
                        </div>
                        ${place.has_ai_analysis ? `<div style="text-align: center;">
                            <div style="font-size: 10px; color: #3b82f6; text-transform: uppercase; font-weight: bold;">${translations[currentLang]['ai-score'] || 'AI Score'}</div>
                            <div style="font-size: 16px; font-weight: 900; color: #3b82f6;">${place.ai_score ? place.ai_score.toFixed(1) : '—'}</div>
                        </div>` : ''}
                    </div>
                    
                     <div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #1e293b; border-top: 1px solid #e2e8f0; padding-top: 8px; font-weight: 600;">
                        <span style="display: flex; align-items: center; gap: 4px;">
                            <span style="color: #3b82f6;">💬</span> ${place.total_reviews.toLocaleString()} ${translations[currentLang]['reviews']}
                        </span>
                        <span style="padding: 2px 8px; border-radius: 4px; background: ${getMarkerColor(index + 1)}15; color: ${getMarkerColor(index + 1)};">${translations[currentLang]['rank']} #${index + 1}</span>
                    </div>

                    ${(() => { const s = getOpenNowStatus(place.opening_hours); return s ? `<div style="margin-top:8px; padding:5px 8px; border-radius:6px; font-size:12px; font-weight:700; background:${s.open ? '#dcfce7' : '#fee2e2'}; color:${s.open ? '#16a34a' : '#dc2626'};">● ${s.label}</div>` : ''; })()}

                    <div style="text-align: center; margin-top: 8px;">
                        <a href="https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}"
                           target="_blank" rel="noopener"
                           class="navigate-btn">
                            <span class="material-icons">directions</span>
                            ${translations[currentLang]['go-to-kebab']}
                        </a>
                    </div>
                </div>
            `);

        mapMarkers.push(marker);
        bounds.extend([lat, lng]);

        // Add click event to center map on marker
        marker.on('click', function () {
            kebabMap.setView([lat, lng], 15);
        });
    });

    // Fit map to show all markers with padding
    if (placesWithCoords.length > 0) {
        kebabMap.fitBounds(bounds, { padding: [20, 20] });
        window.currentCityBounds = bounds;
    }
}

// Add markers for kebab places to global map
function addGlobalKebabMarkers(kebabPlaces) {
    if (!globalKebabMap) {
        console.error('Global map not initialized');
        return;
    }

    clearGlobalMapMarkers();

    if (!kebabPlaces || kebabPlaces.length === 0) {
        console.log('No kebab places to display on global map');
        return;
    }

    // Filter places with valid coordinates
    const placesWithCoords = kebabPlaces.filter(place =>
        place.latitude && place.longitude &&
        !isNaN(parseFloat(place.latitude)) &&
        !isNaN(parseFloat(place.longitude))
    );

    if (placesWithCoords.length === 0) {
        console.log('No kebab places with valid coordinates for global map');
        return;
    }

    console.log(`Adding ${placesWithCoords.length} markers to global map`);

    // Create bounds for all markers
    const bounds = L.latLngBounds();

    placesWithCoords.forEach((place, index) => {
        const lat = parseFloat(place.latitude);
        const lng = parseFloat(place.longitude);

        // Determine size based on rank
        let markerSize = 38;
        if (index === 0) markerSize = 52;
        else if (index === 1) markerSize = 46;
        else if (index === 2) markerSize = 42;

        // Create custom icon based on rank
        const winnerClass = (index + 1 <= 3) ? `pin-winner-${index + 1}` : '';
        const iconHtml = `
            <div class="premium-pin ${winnerClass}">
                <span class="pin-number">${index + 1}</span>
            </div>
        `;

        const customIcon = L.divIcon({
            html: iconHtml,
            className: 'custom-marker-transparent',
            iconSize: [markerSize, markerSize],
            iconAnchor: [markerSize / 2, markerSize],
            popupAnchor: [0, -markerSize]
        });

        // Create marker
        const marker = L.marker([lat, lng], { icon: customIcon })
            .addTo(globalKebabMap)
            .bindPopup(`
                <div style="padding: 12px; min-width: 240px; font-family: 'Inter', sans-serif;">
                    <div style="margin-bottom: 8px;">
                         <strong style="font-size: 16px; display: block; margin-bottom: 4px; color: #1e293b;">${place.name}</strong>
                         <span style="font-size: 12px; color: #64748b; display: flex; align-items: center; gap: 4px;">
                            <span style="font-size: 14px;">📍</span> ${place.address}
                         </span>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: ${place.has_ai_analysis ? '1fr 1fr 1fr' : '1fr 1fr'}; gap: 8px; margin-bottom: 8px; background: #f8fafc; padding: 8px; border-radius: 8px;">
                        <div style="text-align: center; border-right: 1px solid #e2e8f0;">
                            <div style="font-size: 10px; color: #64748b; text-transform: uppercase; font-weight: bold;">${translations[currentLang]['score'] || 'Score'}</div>
                            <div style="font-size: 16px; font-weight: 900; color: #ea580c;">${place.rank_score.toFixed(1)}</div>
                        </div>
                        <div style="text-align: center; ${place.has_ai_analysis ? 'border-right: 1px solid #e2e8f0;' : ''}">
                            <div style="font-size: 10px; color: #64748b; text-transform: uppercase; font-weight: bold;">${translations[currentLang]['rating'] || 'Rating'}</div>
                            <div style="font-size: 14px; font-weight: bold; color: #1e293b;">⭐ ${place.rating.toFixed(1)}</div>
                        </div>
                        ${place.has_ai_analysis ? `<div style="text-align: center;">
                            <div style="font-size: 10px; color: #3b82f6; text-transform: uppercase; font-weight: bold;">${translations[currentLang]['ai-score'] || 'AI Score'}</div>
                            <div style="font-size: 16px; font-weight: 900; color: #3b82f6;">${place.ai_score ? place.ai_score.toFixed(1) : '—'}</div>
                        </div>` : ''}
                    </div>
                    
                     <div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #1e293b; border-top: 1px solid #e2e8f0; padding-top: 8px; font-weight: 600;">
                        <span style="display: flex; align-items: center; gap: 4px;">
                            <span style="color: #3b82f6;">💬</span> ${place.total_reviews.toLocaleString()} ${translations[currentLang]['reviews']}
                        </span>
                        <span style="padding: 2px 8px; border-radius: 4px; background: ${getMarkerColor(index + 1)}15; color: ${getMarkerColor(index + 1)};">${translations[currentLang]['rank']} #${index + 1}</span>
                    </div>

                    ${(() => { const s = getOpenNowStatus(place.opening_hours); return s ? `<div style="margin-top:8px; padding:5px 8px; border-radius:6px; font-size:12px; font-weight:700; background:${s.open ? '#dcfce7' : '#fee2e2'}; color:${s.open ? '#16a34a' : '#dc2626'};">● ${s.label}</div>` : ''; })()}

                    <div style="text-align: center; margin-top: 8px;">
                        <a href="https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}"
                           target="_blank" rel="noopener"
                           class="navigate-btn">
                            <span class="material-icons">directions</span>
                            ${translations[currentLang]['go-to-kebab']}
                        </a>
                    </div>
                </div>
            `);

        globalMapMarkers.push(marker);
        bounds.extend([lat, lng]);

        // Add click event to center map on marker
        marker.on('click', function () {
            globalKebabMap.setView([lat, lng], 15);
        });
    });

    // Fit map to show all markers with padding, but ensure full Poland is visible
    if (placesWithCoords.length > 0) {
        // Create bounds for Poland to ensure full country is visible
        const polandBounds = L.latLngBounds(
            [49.0, 14.0], // Southwest corner (southwest Poland)
            [55.0, 24.0]  // Northeast corner (northeast Poland)
        );

        // Combine marker bounds with Poland bounds to ensure everything is visible
        const combinedBounds = bounds.extend(polandBounds);
        window.globalCityBounds = combinedBounds;

        // Fit map with more padding and max zoom limit
        globalKebabMap.fitBounds(combinedBounds, {
            padding: [50, 50],
            maxZoom: 8 // Don't zoom in too much
        });

        // If markers are too clustered, set a minimum zoom level
        setTimeout(() => {
            if (globalKebabMap.getZoom() > 8) {
                globalKebabMap.setZoom(6); // Show more of Poland
            }
        }, 100);
    } else {
        // If no markers, show full Poland
        globalKebabMap.setView([52.0, 19.0], 6);
    }
}

// Get marker color based on rank - Standardized colors matching ranking badges
function getMarkerColor(rank) {
    switch (rank) {
        case 1:
            return '#FFD700'; // Gold for #1
        case 2:
            return '#C0C0C0'; // Silver for #2
        case 3:
            return '#CD7F32'; // Bronze for #3
        default:
            if (rank <= 10) {
                return '#E67E22'; // Orange for ranks 4-10
            } else {
                return '#3498db'; // Blue for ranks 11+
            }
    }
}

// Update map when city rankings are loaded
// MOVED UP to line 1222 for better organization


// Center map on specific kebab place (identified by lat/lng)
function centerMapOnKebab(lat, lng) {
    if (!kebabMap || !mapMarkers.length) return;
    const marker = mapMarkers.find(m => {
        const ll = m.getLatLng();
        return Math.abs(ll.lat - lat) < 0.0002 && Math.abs(ll.lng - lng) < 0.0002;
    });
    if (!marker) return;
    kebabMap.setView([lat, lng], 15);
    marker.openPopup();
}

function centerGlobalMapOnKebab(lat, lng) {
    if (!globalKebabMap || !globalMapMarkers.length) return;
    const marker = globalMapMarkers.find(m => {
        const ll = m.getLatLng();
        return Math.abs(ll.lat - lat) < 0.0002 && Math.abs(ll.lng - lng) < 0.0002;
    });
    if (!marker) return;
    globalKebabMap.setView([lat, lng], 15);
    marker.openPopup();
}

// Initialize map when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Delay map init on desktop to prevent Leaflet tiles from becoming LCP element.
    // requestIdleCallback defers until after main content paints; setTimeout fallback for Safari.
    if (window.innerWidth > 768) {
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => initializeMap(), { timeout: 2000 });
        } else {
            setTimeout(initializeMap, 300);
        }
    }

    // Add Intersection Observer for map containers
    setupMapVisibilityObserver();

    // --- Cookie Banner Logic ---
    const cookieBanner = $id('cookie-banner');
    const cookieOkBtn = $id('cookie-ok-btn');

    if (cookieBanner && cookieOkBtn) {
        // Check if already consented
        if (localStorage.getItem('cookie-consent') === 'true') {
            cookieBanner.style.display = 'none';
        }

        cookieOkBtn.addEventListener('click', () => {
            // Visual feedback: Change button state
            cookieOkBtn.innerHTML = '<span class="material-icons text-sm mr-1">check_circle</span> OK';
            cookieOkBtn.classList.remove('bg-primary');
            cookieOkBtn.classList.add('bg-green-600');

            // Save consent
            localStorage.setItem('cookie-consent', 'true');

            // Apply close transition only at dismiss time (kept off initial paint to help LCP)
            cookieBanner.style.transition = 'transform 500ms, opacity 500ms';
            cookieBanner.style.transform = 'translateY(100%)';
            cookieBanner.style.opacity = '0';

            setTimeout(() => {
                cookieBanner.style.display = 'none';
            }, 500);
        });
    }
});

// Setup Intersection Observer for map containers
function setupMapVisibilityObserver() {
    const mapContainers = [
        document.getElementById('kebab-map'),
        document.getElementById('kebab-map-global')
    ];

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Map container became visible
                const containerId = entry.target.id;
                console.log(`Map container ${containerId} became visible`);

                // Invalidate size for the appropriate map
                if (containerId === 'kebab-map' && kebabMap) {
                    setTimeout(() => {
                        kebabMap.invalidateSize();
                        console.log('City map size invalidated via observer');
                    }, 100);
                } else if (containerId === 'kebab-map-global' && globalKebabMap) {
                    setTimeout(() => {
                        globalKebabMap.invalidateSize();
                        console.log('Global map size invalidated via observer');
                    }, 100);
                }
            }
        });
    }, {
        threshold: 0.1 // Trigger when at least 10% of container is visible
    });

    // Observe both map containers
    mapContainers.forEach(container => {
        if (container) {
            observer.observe(container);
            console.log(`Observing map container: ${container.id}`);
        }
    });
}

// Toggle function for collapsible sections
function toggleSection(id) {
    const content = document.getElementById(id);
    const button = event.currentTarget; // The button that was clicked
    const arrow = button.querySelector('.arrow');

    if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        if (arrow) arrow.textContent = 'expand_less';
    } else {
        content.classList.add('hidden');
        if (arrow) arrow.textContent = 'expand_more';
    }
}

// Populate the top horizontal city selector
function populateCitySelector(cities) {
    const selector = document.getElementById('city-selector');
    if (!selector) return;

    // Keep the first element (Global Top 10 button) and the divider
    const globalButton = selector.firstElementChild;
    const divider = selector.children[1];

    selector.innerHTML = '';
    if (globalButton) selector.appendChild(globalButton);
    if (divider) selector.appendChild(divider);

    // Render ALL Cities as Cards
    let firstCard = true;
    cities.forEach(city => {
        const imageFile = getCityImageFile(city);
        const card = document.createElement('button');
        const isActive = window.currentCity === city;
        card.className = `compact-city-card group ${isActive ? 'active' : ''}`;
        card.onclick = () => selectCity(city);
        card.setAttribute('data-city', city);

        if (imageFile) {
            const smFile = imageFile.replace('.webp', '-sm.webp');
            const priority = firstCard ? 'fetchpriority="high" loading="eager"' : 'loading="lazy"';
            firstCard = false;
            card.innerHTML = `
                <img src="/static/img/cities/${imageFile}"
                     srcset="/static/img/cities/${smFile} 400w, /static/img/cities/${imageFile} 800w"
                     sizes="(max-width: 767px) 180px, 140px"
                     width="800" height="500"
                     ${priority}
                     alt="${city}">
                <div class="overlay"></div>
                <div class="label">${city}</div>
            `;
        } else {
            // Fallback for cities without an image: Premium Glassmorphism Gradient
            card.innerHTML = `
                <div class="absolute inset-0 bg-gradient-to-br from-surface-dark to-surface-dark/40 flex items-center justify-center">
                    <div class="absolute inset-0 bg-primary/5 mix-blend-overlay"></div>
                    <span class="material-icons text-primary/20 text-2xl">location_city</span>
                </div>
                <div class="overlay"></div>
                <div class="label">${city}</div>
            `;
        }

        card.addEventListener('mouseenter', () => prefetchCity(city));
        selector.appendChild(card);
    });

}

// Handle horizontal scrolling of cities
function scrollCities(direction) {
    const selector = document.getElementById('city-selector');
    if (!selector) return;
    
    const scrollAmount = 200;
    if (direction === 'left') {
        selector.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    } else {
        selector.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
}

// Toggle the mobile map filter panel (remembers open state across re-renders)
if (!window.mobileFilterPanelOpen) window.mobileFilterPanelOpen = { city: false, global: false };
function toggleMobileFilterPanel(scope) {
    window.mobileFilterPanelOpen[scope] = !window.mobileFilterPanelOpen[scope];
    const panel  = document.getElementById(`mob-${scope}-panel`);
    const arrow  = document.getElementById(`mob-${scope}-arrow`);
    if (panel) panel.style.display = window.mobileFilterPanelOpen[scope] ? 'block' : 'none';
    if (arrow) arrow.style.transform = window.mobileFilterPanelOpen[scope] ? 'rotate(180deg)' : '';
}

// Sync the mobile map filter overlay (shown above map on mobile map view)
function syncMobileMapFilter(isGlobal) {
    const overlay = document.getElementById('mobile-map-filterbar');
    if (!overlay) return;
    const scope = isGlobal ? 'global' : 'city';
    const filters = window.activeFilters[scope] || {};
    const anyFilter = !!(filters.open_now || filters.nocne || (isGlobal && filters.voivodeship));
    const sort = filters.sort || 'score';
    const anySort = sort !== 'score';
    const anyNon = anyFilter || anySort;
    const isEn = (window.currentLang || 'pl') === 'en';
    const panelOpen = !!(window.mobileFilterPanelOpen && window.mobileFilterPanelOpen[scope]);

    const allData = isGlobal ? window.globalRankingData : window.cityRankingData;
    const total = allData ? allData.length : 0;
    let cnt = total;
    if (allData && anyFilter) {
        let f = [...allData];
        if (filters.open_now) f = f.filter(k => getOpenNowStatus(k.opening_hours)?.open === true);
        if (filters.nocne) f = f.filter(k => isNightKebab(k.opening_hours));
        if (isGlobal && filters.voivodeship) f = f.filter(k => CITY_VOIVODESHIP[k.city] === filters.voivodeship);
        cnt = f.length;
    }

    const mInfo = (k) => `<span onclick="event.stopPropagation();showFilterTooltip(event,'${k}')" style="display:inline-flex;align-items:center;justify-content:center;width:13px;height:13px;border-radius:50%;border:1px solid currentColor;font-size:8px;opacity:0.55;cursor:help;flex-shrink:0;margin-left:1px;">i</span>`;
    const pill = (type, label, active, tipKey) => {
        const s = active
            ? 'background:rgba(52,211,153,0.2);color:#34d399;border:1px solid #34d399;font-weight:700'
            : 'background:rgba(255,255,255,0.06);color:#94a3b8;border:1px solid rgba(255,255,255,0.15)';
        return `<button onclick="applyRankingFilter('${type}',${isGlobal})" style="flex-shrink:0;display:inline-flex;align-items:center;gap:3px;padding:6px 13px;border-radius:20px;font-size:12px;cursor:pointer;${s}">${label}${tipKey ? mInfo(tipKey) : ''}</button>`;
    };
    const spill = (type, label, active, tipKey) => {
        const s = active
            ? 'background:rgba(96,165,250,0.18);color:#60a5fa;border:1px solid #60a5fa;font-weight:700'
            : 'background:rgba(255,255,255,0.04);color:#64748b;border:1px solid rgba(255,255,255,0.12)';
        return `<button onclick="applyRankingFilter('${type}',${isGlobal})" style="flex-shrink:0;display:inline-flex;align-items:center;gap:3px;padding:6px 13px;border-radius:20px;font-size:12px;cursor:pointer;${s}">${label}${tipKey ? mInfo(tipKey) : ''}</button>`;
    };

    const triggerBorder = anyNon ? '#34d399' : 'rgba(255,255,255,0.15)';
    const triggerBg     = anyNon ? 'rgba(52,211,153,0.12)' : 'rgba(255,255,255,0.05)';
    const triggerColor  = anyNon ? '#34d399' : '#94a3b8';

    // Trigger row
    let html = `<div style="display:flex;align-items:center;gap:8px;">`;
    html += `<button onclick="toggleMobileFilterPanel('${scope}')" style="display:inline-flex;align-items:center;gap:6px;padding:7px 14px;border-radius:9999px;font-size:13px;font-weight:700;border:1px solid ${triggerBorder};background:${triggerBg};color:${triggerColor};cursor:pointer;">
        <span style="font-size:15px;">⚙</span>
        ${isEn ? 'Filters' : 'Filtry'}
        <span id="mob-${scope}-arrow" style="font-size:10px;transition:transform 0.2s;${panelOpen ? 'transform:rotate(180deg)' : ''}">▾</span>
        ${anyNon ? `<span style="color:#34d399;font-size:16px;line-height:0.8;">●</span>` : ''}
    </button>`;
    if (anyNon) {
        html += `<button onclick="applyRankingFilter('all',${isGlobal})" style="display:inline-flex;align-items:center;gap:4px;padding:6px 12px;border-radius:9999px;font-size:12px;font-weight:700;border:1px solid rgba(248,113,113,0.4);background:rgba(248,113,113,0.08);color:#f87171;cursor:pointer;">✕ ${isEn ? 'Clear' : 'Kasuj'}</button>`;
    }
    if (anyFilter) {
        html += `<span style="font-size:11px;color:#34d399;font-weight:700;">${cnt}/${total}</span>`;
    }
    html += `<div style="margin-left:auto;display:flex;gap:6px;">`;
    if (!isGlobal) {
        html += `<button onclick="openWatchCityModal(window.currentCity||'')" style="display:inline-flex;align-items:center;gap:4px;padding:7px 12px;border-radius:9999px;font-size:13px;font-weight:700;border:1px solid rgba(96,165,250,0.35);background:rgba(96,165,250,0.07);color:#60a5fa;cursor:pointer;">🔔</button>`;
    }
    html += `<button onclick="openRouletteModal(${isGlobal})" style="display:inline-flex;align-items:center;gap:4px;padding:7px 12px;border-radius:9999px;font-size:13px;font-weight:700;border:1px solid rgba(251,191,36,0.4);background:rgba(251,191,36,0.08);color:#fbbf24;cursor:pointer;">🎲</button>`;
    html += `</div>`;
    html += `</div>`;

    // Expandable panel (floating over map)
    html += `<div id="mob-${scope}-panel" style="display:${panelOpen ? 'block' : 'none'};margin-top:10px;padding:12px;background:#111827;border:1px solid rgba(255,255,255,0.1);border-radius:14px;">`;
    html += `<div style="margin-bottom:10px;">`;
    html += `<div style="font-size:10px;color:#475569;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">${isEn ? 'Filter' : 'Filtruj'}</div>`;
    html += `<div style="display:flex;flex-wrap:wrap;gap:7px;">`;
    html += pill('all',      isEn ? '✕ All' : '✕ Wszystkie',  !anyFilter);
    html += pill('open_now', isEn ? '● Open' : '● Otwarte',   !!filters.open_now, 'open_now');
    html += pill('nocne',    isEn ? '🌙 Night' : '🌙 Nocne',  !!filters.nocne,    'nocne');
    html += `</div></div>`;
    html += `<div>`;
    html += `<div style="font-size:10px;color:#475569;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">${isEn ? 'Sort by' : 'Sortuj wg'}</div>`;
    html += `<div style="display:flex;flex-wrap:wrap;gap:7px;">`;
    html += spill('sort_score',   isEn ? '↕ Score'  : '↕ Wynik',  sort === 'score',   'sort_score');
    html += spill('sort_rating',  isEn ? '★ Rating' : '★ Ocena',  sort === 'rating',  'sort_rating');
    html += spill('sort_reviews', isEn ? '💬 Pop'   : '💬 Pop',   sort === 'reviews', 'sort_reviews');
    html += `</div></div>`;
    html += `</div>`;

    overlay.innerHTML = html;
}

// Regular rankings display function
function displayRankings(rankings, container, cityName, isGlobal = false) {
    if (rankings.length === 0) {
        container.innerHTML = `<p class="text-center text-gray-500 py-4">${translations[currentLang]['no-kebabs']}</p>`;
        return;
    }

    // Store full data; do NOT reset filters here — city change reset happens in selectCity
    if (isGlobal) {
        window.globalRankingData = rankings;
    } else {
        window.cityRankingData = rankings;
    }

    // Apply any currently active filters + sort to initial render
    const scope = isGlobal ? 'global' : 'city';
    const filters = window.activeFilters[scope];
    let dataToRender = rankings;
    if (filters.open_now) dataToRender = dataToRender.filter(k => getOpenNowStatus(k.opening_hours)?.open === true);
    if (filters.nocne) dataToRender = dataToRender.filter(k => isNightKebab(k.opening_hours));
    if (isGlobal && filters.voivodeship) dataToRender = dataToRender.filter(k => CITY_VOIVODESHIP[k.city] === filters.voivodeship);
    dataToRender = applySortToData(dataToRender, filters.sort);

    const cardsId = isGlobal ? 'global-ranking-cards' : 'city-ranking-cards';
    const filterBarHtml = buildFilterBar(isGlobal, rankings);

    container.classList.remove('ranking-fade-in');
    void container.offsetWidth;
    container.innerHTML = filterBarHtml + `<div id="${cardsId}"></div>`;
    container.classList.add('ranking-fade-in');

    const cardsEl = document.getElementById(cardsId);
    renderRankingCards(dataToRender, cardsEl, isGlobal, cityName);

    // Sync map with filtered data (overrides the full-dataset map update from checkAndLoadRankings)
    if (!isGlobal) {
        if (window.kebabMap) updateMapWithKebabs(dataToRender);
    } else {
        if (window.globalKebabMap) updateGlobalMapWithKebabs(dataToRender);
    }

    // Update count badge if filters are active
    const anyActive = !!(filters.open_now || filters.nocne || (isGlobal && filters.voivodeship));
    const countEl = document.getElementById(`${scope}-fb-count`);
    if (countEl) {
        countEl.style.display = anyActive ? '' : 'none';
        if (anyActive) countEl.textContent = `${dataToRender.length}/${rankings.length}`;
    }

    updateFilterBarHeader(scope, isGlobal);
    syncMobileMapFilter(isGlobal);
}

function getOpenNowStatus(openingHoursJson) {
    if (!openingHoursJson) return null;
    let hours;
    try { hours = typeof openingHoursJson === 'string' ? JSON.parse(openingHoursJson) : openingHoursJson; }
    catch(e) { return null; }

    const isEn = (window.currentLang || currentLang) === 'en';
    const T = {
        open:        isEn ? 'Open'   : 'Otwarte',
        closed:      isEn ? 'Closed' : 'Zamknięte',
        closes:      isEn ? 'closes' : 'zamyka',
        opens:       isEn ? 'opens'  : 'otwiera',
    };

    // Fallback: place has no timetable but known current status (e.g. all-days-closed or open-now-no-hours)
    if (hours._status) {
        const isOpen = hours._status === 'open';
        return { open: isOpen, label: isOpen ? T.open : T.closed };
    }

    const now = new Date();
    const todayDay = now.getDay();
    const curMin = now.getHours() * 60 + now.getMinutes();

    function parseRange(s) {
        if (!s) return null;
        const dash = s.lastIndexOf('-');
        if (dash < 1) return null;
        const [oh, om] = s.slice(0, dash).trim().split(':').map(Number);
        const [ch, cm] = s.slice(dash + 1).trim().split(':').map(Number);
        return { openMin: oh * 60 + om, closeMin: ch * 60 + cm, openStr: s.slice(0, dash).trim(), closeStr: s.slice(dash + 1).trim() };
    }

    // Check yesterday's crossover (e.g. open 22:00–03:00, now it's 01:00)
    const yDay = (todayDay + 6) % 7;
    const yRange = parseRange(hours[String(yDay)]);
    if (yRange && yRange.closeMin < yRange.openMin && curMin < yRange.closeMin) {
        return { open: true, label: `${T.open} · ${T.closes} ${yRange.closeStr}` };
    }

    const tRange = parseRange(hours[String(todayDay)]);
    if (!tRange) return { open: false, label: T.closed };

    const closeAdj = tRange.closeMin < tRange.openMin ? tRange.closeMin + 1440 : tRange.closeMin;
    if (curMin >= tRange.openMin && curMin < closeAdj) {
        return { open: true, label: `${T.open} · ${T.closes} ${tRange.closeStr}` };
    }
    if (curMin < tRange.openMin) {
        return { open: false, label: `${T.closed} · ${T.opens} ${tRange.openStr}` };
    }
    return { open: false, label: T.closed };
}

function isNightKebab(openingHoursJson) {
    if (!openingHoursJson) return false;
    let hours;
    try { hours = typeof openingHoursJson === 'string' ? JSON.parse(openingHoursJson) : openingHoursJson; }
    catch(e) { return false; }
    if (hours._status) return false;
    for (let d = 0; d <= 6; d++) {
        const s = hours[String(d)];
        if (!s) continue;
        const dash = s.lastIndexOf('-');
        if (dash < 1) continue;
        const openMin = s.slice(0, dash).trim().split(':').reduce((h, m, i) => i === 0 ? h + Number(m) * 60 : h + Number(m), 0);
        const closeMin = s.slice(dash + 1).trim().split(':').reduce((h, m, i) => i === 0 ? h + Number(m) * 60 : h + Number(m), 0);
        if (closeMin < openMin && closeMin > 0 && closeMin <= 540) return true; // closes strictly after 00:00 and before 09:00
    }
    return false;
}

const FILTER_TIPS = {
    pl: {
        sort_score:   'Wynik KebabRank — ważona kombinacja gwiazdek, liczby recenzji i analizy AI. W większości przypadków pokrywa się z Oceną. Najlepszy punkt startowy.',
        sort_rating:  'Czyste gwiazdki Google. Przy remisie wygrywa to z większą liczbą recenzji — trudniej utrzymać wysoką ocenę przy dużej popularności.',
        sort_reviews: 'Popularność — liczba komentarzy Google. Więcej recenzji = więcej odwiedzin. Nie zawsze najlepszy jakościowo, ale sprawdzony przez tłumy.',
        open_now:     'Pokazuje tylko miejsca otwarte w tej chwili. W nocy może się pokrywać z filtrem Nocne.',
        nocne:        'Miejsca z nocnymi godzinami — zamykają się po północy (max do 9:00). W nocy filtr Nocne pokrywa się z Otwarte.',
    },
    en: {
        sort_score:   'KebabRank Score — weighted blend of stars, reviews and AI. Usually close to Rating. Best starting point.',
        sort_rating:  'Pure Google stars. Ties broken by review count — harder to keep a high rating with more reviews.',
        sort_reviews: 'Popularity — number of Google reviews. More reviews = more visits. Not always top quality, but proven by crowds.',
        open_now:     'Shows only places open right now. At night may overlap with the Night filter.',
        nocne:        'Places with night hours — close after midnight (max 9 AM). At night overlaps with Open Now.',
    }
};

function showFilterTooltip(event, key) {
    event.stopPropagation();
    const lang = window.currentLang || 'pl';
    const text = (FILTER_TIPS[lang] || FILTER_TIPS.pl)[key];
    if (!text) return;
    let tip = document.getElementById('filter-tooltip');
    if (!tip) {
        tip = document.createElement('div');
        tip.id = 'filter-tooltip';
        tip.style.cssText = 'position:fixed;z-index:9999;max-width:240px;padding:10px 14px;background:#1e293b;color:#e2e8f0;font-size:12px;line-height:1.6;border-radius:10px;border:1px solid rgba(255,255,255,0.12);box-shadow:0 8px 32px rgba(0,0,0,0.6);pointer-events:none;display:none;';
        document.body.appendChild(tip);
    }
    tip.textContent = text;
    tip.style.display = 'block';
    const rect = event.target.closest('span,button').getBoundingClientRect();
    let left = rect.left;
    let top = rect.bottom + 8;
    if (left + 240 > window.innerWidth - 12) left = window.innerWidth - 252;
    if (left < 8) left = 8;
    if (top + 100 > window.innerHeight) top = rect.top - 108;
    tip.style.left = left + 'px';
    tip.style.top = top + 'px';
    clearTimeout(tip._t);
    tip._t = setTimeout(() => { tip.style.display = 'none'; }, 5000);
    const hide = () => { tip.style.display = 'none'; document.removeEventListener('click', hide); };
    setTimeout(() => document.addEventListener('click', hide), 50);
}

function applySortToData(data, sort) {
    if (!sort || sort === 'score') return data;
    return [...data].sort((a, b) => {
        if (sort === 'rating') {
            const diff = (b.rating || 0) - (a.rating || 0);
            return diff !== 0 ? diff : (b.total_reviews || 0) - (a.total_reviews || 0);
        }
        if (sort === 'reviews') {
            const diff = (b.total_reviews || 0) - (a.total_reviews || 0);
            return diff !== 0 ? diff : (b.rating || 0) - (a.rating || 0);
        }
        return 0;
    });
}

function toggleFilterPanel(scope) {
    const panel = document.getElementById(`${scope}-filter-panel`);
    if (!panel) return;
    const opening = panel.style.display === 'none';
    panel.style.display = opening ? 'block' : 'none';
    const arrow = document.getElementById(`${scope}-fb-arrow`);
    if (arrow) arrow.style.transform = opening ? 'rotate(180deg)' : 'rotate(0deg)';
    if (opening) {
        const close = (e) => {
            const bar = document.getElementById(`${scope}-filter-bar`);
            if (bar && !bar.contains(e.target)) {
                panel.style.display = 'none';
                if (arrow) arrow.style.transform = 'rotate(0deg)';
                document.removeEventListener('click', close);
            }
        };
        setTimeout(() => document.addEventListener('click', close), 50);
    }
}

function updateFilterBarHeader(scope, isGlobal) {
    const filters = window.activeFilters[scope] || {};
    const anyFilter = !!(filters.open_now || filters.nocne || (isGlobal && filters.voivodeship));
    const anySort   = (filters.sort || 'score') !== 'score';
    const anyNon    = anyFilter || anySort;
    const trigger = document.getElementById(`${scope}-fb-trigger`);
    if (trigger) {
        trigger.style.borderColor = anyNon ? '#34d399' : 'rgba(255,255,255,0.15)';
        trigger.style.background  = anyNon ? 'rgba(52,211,153,0.12)' : 'rgba(255,255,255,0.05)';
        trigger.style.color       = anyNon ? '#34d399' : '#94a3b8';
        const dot = trigger.querySelector('.fb-dot');
        if (dot) dot.style.display = anyNon ? '' : 'none';
    }
    const kasuj = document.getElementById(`${scope}-fb-kasuj`);
    if (kasuj) kasuj.style.display = anyNon ? 'inline-flex' : 'none';
}

function buildFilterBar(isGlobal, rankings) {
    const isEn = (window.currentLang || 'pl') === 'en';
    const scope = isGlobal ? 'global' : 'city';
    const filters = window.activeFilters[scope] || {};
    const anyFilter = !!(filters.open_now || filters.nocne || (isGlobal && filters.voivodeship));
    const sort = filters.sort || 'score';
    const anySort = sort !== 'score';
    const anyNon = anyFilter || anySort;

    const infoIcon = (tipKey) =>
        `<span onclick="event.stopPropagation();showFilterTooltip(event,'${tipKey}')" style="display:inline-flex;align-items:center;justify-content:center;width:13px;height:13px;border-radius:50%;border:1px solid currentColor;font-size:8px;font-style:normal;opacity:0.55;cursor:help;flex-shrink:0;margin-left:1px;">i</span>`;

    const pill = (id, label, active, onclick, tipKey) => {
        const border = active ? '#34d399' : 'rgba(255,255,255,0.15)';
        const bg     = active ? 'rgba(52,211,153,0.18)' : 'rgba(255,255,255,0.06)';
        const color  = active ? '#34d399' : '#94a3b8';
        return `<button id="${id}" onclick="${onclick}" style="cursor:pointer;display:inline-flex;align-items:center;gap:4px;padding:6px 14px;border-radius:9999px;font-size:12px;font-weight:700;border:1px solid ${border};background:${bg};color:${color};transition:all 0.2s;white-space:nowrap;">${label}${tipKey ? infoIcon(tipKey) : ''}</button>`;
    };
    const sortPill = (id, label, active, onclick, tipKey) => {
        const border = active ? '#60a5fa' : 'rgba(255,255,255,0.12)';
        const bg     = active ? 'rgba(96,165,250,0.15)' : 'rgba(255,255,255,0.04)';
        const color  = active ? '#60a5fa' : '#64748b';
        return `<button id="${id}" onclick="${onclick}" style="cursor:pointer;display:inline-flex;align-items:center;gap:4px;padding:6px 14px;border-radius:9999px;font-size:12px;font-weight:700;border:1px solid ${border};background:${bg};color:${color};transition:all 0.2s;white-space:nowrap;">${label}${tipKey ? infoIcon(tipKey) : ''}</button>`;
    };

    // Outer sticky wrapper
    let bar = `<div id="${scope}-filter-bar" style="position:sticky;top:0;z-index:50;background:#0b1121;border-bottom:1px solid rgba(255,255,255,0.06);padding:8px 0 10px;margin-bottom:8px;">`;

    // Header row: trigger + count badge + kasuj
    bar += `<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">`;
    bar += `<button id="${scope}-fb-trigger" onclick="toggleFilterPanel('${scope}')" style="display:inline-flex;align-items:center;gap:6px;padding:7px 16px;border-radius:9999px;font-size:13px;font-weight:700;border:1px solid ${anyNon ? '#34d399' : 'rgba(255,255,255,0.15)'};background:${anyNon ? 'rgba(52,211,153,0.12)' : 'rgba(255,255,255,0.05)'};color:${anyNon ? '#34d399' : '#94a3b8'};cursor:pointer;transition:all 0.2s;">
        <span style="font-size:15px;">⚙</span>
        ${isEn ? 'Filters' : 'Filtry'}
        <span id="${scope}-fb-arrow" style="font-size:10px;transition:transform 0.2s;">▾</span>
        <span class="fb-dot" style="display:${anyNon ? '' : 'none'};color:#34d399;font-size:16px;line-height:0.8;">●</span>
    </button>`;
    bar += `<span id="${scope}-fb-count" style="display:${anyFilter ? '' : 'none'};font-size:12px;font-weight:700;color:#34d399;"></span>`;
    bar += `<button id="${scope}-fb-kasuj" onclick="applyRankingFilter('all',${isGlobal})" style="display:${anyNon ? 'inline-flex' : 'none'};align-items:center;gap:4px;padding:6px 12px;border-radius:9999px;font-size:12px;font-weight:700;border:1px solid rgba(248,113,113,0.4);background:rgba(248,113,113,0.08);color:#f87171;cursor:pointer;">✕ ${isEn ? 'Clear' : 'Kasuj'}</button>`;
    bar += `<div style="margin-left:auto;display:flex;gap:6px;align-items:center;">`;
    if (!isGlobal) {
        bar += `<button onclick="openWatchCityModal(window.currentCity||'')" style="display:inline-flex;align-items:center;gap:5px;padding:7px 14px;border-radius:9999px;font-size:13px;font-weight:700;border:1px solid rgba(96,165,250,0.35);background:rgba(96,165,250,0.07);color:#60a5fa;cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(96,165,250,0.16)'" onmouseout="this.style.background='rgba(96,165,250,0.07)'">🔔 ${isEn ? 'Follow' : 'Obserwuj'}</button>`;
    }
    bar += `<button onclick="openRouletteModal(${isGlobal})" style="display:inline-flex;align-items:center;gap:6px;padding:7px 16px;border-radius:9999px;font-size:13px;font-weight:700;border:1px solid rgba(251,191,36,0.4);background:rgba(251,191,36,0.08);color:#fbbf24;cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(251,191,36,0.18)'" onmouseout="this.style.background='rgba(251,191,36,0.08)'">🎲 ${isEn ? 'Roulette' : 'Ruletka'}</button>`;
    bar += `</div>`;
    bar += `</div>`;

    // Expandable panel (inline, not floating)
    bar += `<div id="${scope}-filter-panel" style="display:none;margin-top:10px;padding:14px;background:#111827;border:1px solid rgba(255,255,255,0.1);border-radius:14px;">`;

    // Filter section
    bar += `<div style="margin-bottom:12px;">`;
    bar += `<div style="font-size:10px;color:#475569;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">${isEn ? 'Filter' : 'Filtruj'}</div>`;
    bar += `<div style="display:flex;flex-wrap:wrap;gap:8px;">`;
    bar += pill(`${scope}-fb-all`,   isEn ? '✕ All' : '✕ Wszystkie',  !anyFilter,         `applyRankingFilter('all',${isGlobal})`);
    bar += pill(`${scope}-fb-open`,  isEn ? '● Open Now' : '● Otwarte', !!filters.open_now, `applyRankingFilter('open_now',${isGlobal})`, 'open_now');
    bar += pill(`${scope}-fb-night`, isEn ? '🌙 Night' : '🌙 Nocne',   !!filters.nocne,    `applyRankingFilter('nocne',${isGlobal})`,    'nocne');
    if (isGlobal) {
        const voivs = [...new Set(rankings.map(k => CITY_VOIVODESHIP[k.city]).filter(Boolean))].sort();
        if (voivs.length > 0) {
            const active = filters.voivodeship || '';
            const selBorder = active ? '#34d399' : 'rgba(255,255,255,0.15)';
            const selColor  = active ? '#34d399' : '#94a3b8';
            bar += `<select id="global-fb-voiv" onchange="applyRankingFilter('voivodeship',true)" style="cursor:pointer;background:#111827;border:1px solid ${selBorder};color:${selColor};border-radius:9999px;padding:6px 12px;font-size:12px;font-weight:700;outline:none;">
                <option value="">${isEn ? '🗺️ Region' : '🗺️ Województwo'}</option>
                ${voivs.map(v => `<option value="${v}" ${v === active ? 'selected' : ''}>${v}</option>`).join('')}
            </select>`;
        }
    }
    bar += `</div></div>`;

    // Sort section
    bar += `<div>`;
    bar += `<div style="font-size:10px;color:#475569;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">${isEn ? 'Sort by' : 'Sortuj wg'}</div>`;
    bar += `<div style="display:flex;flex-wrap:wrap;gap:8px;">`;
    bar += sortPill(`${scope}-fb-sort-score`,   isEn ? '↕ Score'  : '↕ Wynik',  sort === 'score',   `applyRankingFilter('sort_score',${isGlobal})`,   'sort_score');
    bar += sortPill(`${scope}-fb-sort-rating`,  isEn ? '★ Rating' : '★ Ocena',  sort === 'rating',  `applyRankingFilter('sort_rating',${isGlobal})`,  'sort_rating');
    bar += sortPill(`${scope}-fb-sort-reviews`, isEn ? '💬 Pop'   : '💬 Pop',   sort === 'reviews', `applyRankingFilter('sort_reviews',${isGlobal})`, 'sort_reviews');
    bar += `</div></div>`;

    bar += `</div>`; // end panel
    bar += `</div>`; // end bar
    return bar;
}

function renderRankingCards(rankings, cardsContainer, isGlobal, cityName) {
    if (!rankings || rankings.length === 0) {
        const isEn = (window.currentLang || 'pl') === 'en';
        cardsContainer.innerHTML = `<p class="text-center text-gray-500 py-4">${isEn ? 'No kebabs match the current filter.' : 'Brak kebabów spełniających filtr.'}</p>`;
        return;
    }

    let html = '';
    rankings.forEach((kebab, index) => {
        const rank = kebab.rank || kebab.global_rank || index + 1;
        const hasAI = kebab.has_ai_analysis === true || (kebab.ai_summary && kebab.ai_summary.length > 0);

        let rankBadgeClass = "bg-surface-dark text-gray-400";
        if (rank === 1) rankBadgeClass = "bg-yellow-500 text-black";
        else if (rank === 2) rankBadgeClass = "bg-gray-400 text-black";
        else if (rank === 3) rankBadgeClass = "bg-orange-700 text-white";

        let rankChangeHtml = '';
        if (kebab.is_new) {
            rankChangeHtml = `<span class="rank-badge-mini rank-new ml-2">NEW</span>`;
        } else if (kebab.rank_change_indicator === 'up' && kebab.rank_change) {
            rankChangeHtml = `<span class="rank-badge-mini rank-up ml-2"><span class="text-[8px]">▲</span> +${kebab.rank_change}</span>`;
        } else if (kebab.rank_change_indicator === 'down' && kebab.rank_change) {
            rankChangeHtml = `<span class="rank-badge-mini rank-down ml-2"><span class="text-[8px]">▼</span> -${Math.abs(kebab.rank_change)}</span>`;
        } else {
            rankChangeHtml = `<span class="rank-badge-mini rank-neutral ml-2">-</span>`;
        }

        const photoUrl = kebab.photo_url;
        const hasValidPhoto = photoUrl && photoUrl !== 'NONE' && photoUrl.length > 10;
        const kebabImage = hasValidPhoto ? photoUrl : (kebab.image_url || "https://lh3.googleusercontent.com/aida-public/AB6AXuAPZml7HBCvOmxHc3pErimDG6i7ruSOL6NrxB8S8CkUtAIZ9sjOe5U0TSzY4AbGN8NSPkGQZHCdrnALIQoLgGNrze3MwVl9x7OGSn2Gz7CvsUTB4izX8Xatv_tIbLYX6kiuSDVdT3HoS7MKLCnQparIKmg8UVIl7QU1CTAKEBVF9M8_NiLS2ccsanJPm-7kevE10rqP_NKMyBgiXUpcsUtj4e9eJlwKM02h-oL83bYxG2QwVRiuDKWgPfePcvFNWLVGzfpHYYn_Nl4");

        const kLat = isGlobal ? (kebab.lat || 0) : (kebab.latitude || 0);
        const kLng = isGlobal ? (kebab.lng || 0) : (kebab.longitude || 0);
        const mapFn = isGlobal ? `centerGlobalMapOnKebab(${kLat},${kLng})` : `centerMapOnKebab(${kLat},${kLng})`;

        html += `
            <div class="glass-card rounded-xl p-3 md:p-4 flex gap-3 md:gap-4 relative overflow-hidden group cursor-pointer hover:bg-white/5 hover:border-primary/30 mb-2 md:mb-3 transition-all duration-300"
                 onclick="${mapFn}"
                 data-rank="${rank}">

                <!-- Rank Badge -->
                <div class="absolute top-3 left-3 md:top-4 md:left-4 ${rankBadgeClass} font-black text-[10px] md:text-xs px-1.5 md:px-2 py-0.5 rounded flex items-center gap-1 z-20 shadow-lg">
                    <span class="material-icons text-[10px] md:text-xs">emoji_events</span> #${rank}
                </div>

                <!-- Left Column: Image + Address -->
                <div class="flex flex-col items-center gap-2 shrink-0 w-20 md:w-24">
                    <div class="w-20 h-20 md:w-24 md:h-24 rounded-lg overflow-hidden shadow-lg bg-surface-dark mt-1 relative">
                        <img alt="${kebab.name}"
                             class="w-full h-full object-cover transition-transform duration-500"
                             src="${kebabImage}"
                             loading="lazy"
                             width="96" height="96"
                             onerror="this.onerror=null; this.src='https://lh3.googleusercontent.com/aida-public/AB6AXuAPZml7HBCvOmxHc3pErimDG6i7ruSOL6NrxB8S8CkUtAIZ9sjOe5U0TSzY4AbGN8NSPkGQZHCdrnALIQoLgGNrze3MwVl9x7OGSn2Gz7CvsUTB4izX8Xatv_tIbLYX6kiuSDVdT3HoS7MKLCnQparIKmg8UVIl7QU1CTAKEBVF9M8_NiLS2ccsanJPm-7kevE10rqP_NKMyBgiXUpcsUtj4e9eJlwKM02h-oL83bYxG2QwVRiuDKWgPfePcvFNWLVGzfpHYYn_Nl4'"/>
                    </div>
                    <p class="text-[9px] text-gray-400 text-center leading-tight break-words w-full opacity-80">
                        ${kebab.address}, ${kebab.city || cityName || window.currentCity || ''}
                    </p>
                    ${(() => { const s = getOpenNowStatus(kebab.opening_hours); return s ? `<span style="display:inline-block;font-size:9px;font-weight:700;padding:2px 7px;border-radius:9999px;background:${s.open ? '#16a34a' : '#dc2626'};color:#fff;">● ${s.label}</span>` : ''; })()}
                </div>

                <!-- Content -->
                <div class="flex-1 flex flex-col min-w-0">
                    <div>
                        <div class="flex justify-between items-start">
                             <!-- Middle Column: Title & Button -->
                             <div class="flex flex-col gap-1 min-w-0 flex-1 pr-2">
                                 <h3 class="text-xs md:text-lg font-bold text-white group-hover:text-primary transition-colors mb-0.5 md:truncate leading-tight">${kebab.name} ${rankChangeHtml}</h3>

                                 <!-- Navigate Button -->
                                 ${kLat && kLng ? `
                                <a href="https://www.google.com/maps/dir/?api=1&destination=${kLat},${kLng}"
                                   target="_blank" rel="noopener"
                                   onclick="event.stopPropagation()"
                                   class="premium-navigate-btn" title="${translations[currentLang]['go-to-kebab']}">
                                    <span class="material-icons text-sm">directions</span>
                                    <span>${translations[currentLang]['go-to-kebab']}</span>
                                </a>
                                ` : ''}
                             </div>

                              <!-- Right Column: Scores & Stats Matrix -->
                              <div class="flex flex-col items-center gap-1 shrink-0 ml-1">
                                  <div class="flex flex-row items-center gap-2">
                                    <div class="px-1 py-0.5 md:px-2 md:py-1 rounded bg-[#1e293b] border border-white/10 flex flex-col items-center justify-center w-[52px] md:w-[70px] h-[34px] md:h-[42px]">
                                        <span class="text-[8px] md:text-[10px] text-gray-400 uppercase font-bold leading-none mb-0.5">${translations[currentLang]['score'] || 'Wynik'}</span>
                                        <span class="text-sm md:text-base font-black text-primary leading-none">${kebab.rank_score ? kebab.rank_score.toFixed(1) : 'N/A'}</span>
                                    </div>
                                     ${hasAI && kebab.ai_score ? `
                                     <div class="px-1 py-0.5 md:px-2 md:py-1 rounded bg-indigo-500/10 border border-indigo-500/30 flex flex-col items-center justify-center shadow-[0_0_10px_rgba(99,102,241,0.15)] w-[52px] md:w-[70px] h-[34px] md:h-[42px]">
                                         <span class="text-[8px] md:text-[10px] text-indigo-300 uppercase font-bold tracking-tight leading-none mb-0.5">${translations[currentLang]['ai-score'] || 'AI'}</span>
                                         <span class="text-sm md:text-base font-black text-indigo-400 drop-shadow-[0_0_8px_rgba(129,140,248,0.4)] leading-none">${kebab.ai_score.toFixed(1)}</span>
                                     </div>
                                     ` : ''}
                                 </div>
                                 <div class="flex flex-row items-start gap-2 w-full mt-1">
                                    <div class="flex items-center justify-center gap-1 w-[52px] md:w-[70px]">
                                        <span class="font-bold text-white text-xs md:text-sm">${kebab.rating.toFixed(1)}</span>
                                        <span class="material-icons text-yellow-500 text-[10px] md:text-xs">star</span>
                                    </div>
                                    <div class="flex items-center justify-center gap-1 w-[52px] md:w-[70px]">
                                        <span class="font-bold text-white text-xs md:text-sm">${kebab.total_reviews.toLocaleString()}</span>
                                        <span class="material-icons text-blue-400 text-[10px] md:text-xs">reviews</span>
                                    </div>
                                </div>
                             </div>
                        </div>
                    </div>

                    <!-- AI Sections -->
                     <div class="space-y-1 md:space-y-2 mt-auto pt-2">
                        ${hasAI ? `
                         <div class="border border-indigo-500/20 bg-indigo-500/5 rounded overflow-hidden">
                            <button onclick="event.stopPropagation(); toggleSection('ai-summary-${index}-${isGlobal ? 'g' : 'c'}')"
                                    class="w-full flex items-center justify-between px-2 py-1 md:px-3 md:py-1.5 hover:bg-white/5 transition-colors">
                                <span class="text-[9px] md:text-[11px] font-bold uppercase tracking-widest text-indigo-300 flex items-center gap-1 md:gap-2">
                                    <span class="material-icons text-[10px] md:text-xs">auto_awesome</span> ${aiTranslations[currentLang]['ai-summary'] || 'Podsumowanie AI'}
                                </span>
                                <span class="material-icons text-indigo-300/50 text-[10px] md:text-xs arrow">expand_more</span>
                            </button>
                            <div id="ai-summary-${index}-${isGlobal ? 'g' : 'c'}" class="hidden ai-summary-box border-t border-indigo-500/20 p-2 italic text-gray-300 text-[10px] md:text-xs leading-relaxed">
                                ${kebab.ai_summary ? `"${kebab.ai_summary}"` : `<em class="text-gray-500 opacity-60">${translations[currentLang]['ai-forthcoming'] || 'Analiza AI wkrótce...'}</em>`}
                            </div>
                         </div>
                        ` : ''}

                        ${hasAI && kebab.ai_insights ? `
                            <div class="border border-fuchsia-500/20 bg-fuchsia-500/5 rounded overflow-hidden">
                                <button onclick="event.stopPropagation(); toggleSection('ai-insights-${index}-${isGlobal ? 'g' : 'c'}')"
                                        class="w-full flex items-center justify-between px-2 py-1 md:px-3 md:py-1.5 hover:bg-white/5 transition-colors">
                                    <span class="text-[9px] md:text-[11px] font-bold uppercase tracking-widest text-fuchsia-300 flex items-center gap-1 md:gap-2">
                                        <span class="material-icons text-[10px] md:text-xs">analytics</span> ${aiTranslations[currentLang]['ai-insights'] || 'Analiza AI'}
                                    </span>
                                    <span class="material-icons text-fuchsia-300/50 text-[10px] md:text-xs arrow">expand_more</span>
                                </button>
                                <div id="ai-insights-${index}-${isGlobal ? 'g' : 'c'}" class="hidden ai-insights-box border-t border-fuchsia-500/20 p-2">
                                    <div class="grid grid-cols-3 gap-1 md:gap-2">
                                        <div class="flex flex-col items-center text-center">
                                            <span class="text-[8px] text-gray-500 uppercase font-bold tracking-tighter mb-0.5">${aiTranslations[currentLang]['sentiment'] || 'Nastroje'}</span>
                                            <span class="text-[9px] md:text-[10px] font-black px-1.5 py-0.5 rounded-full bg-white/5 ${getSentimentColorClass(kebab.ai_insights.sentiment)}">
                                                ${getSentimentLabel(kebab.ai_insights.sentiment)}
                                            </span>
                                        </div>
                                        <div class="flex flex-col items-center text-center">
                                            <span class="text-[8px] text-gray-500 uppercase font-bold tracking-tighter mb-0.5">${aiTranslations[currentLang]['trending'] || 'Trend'}</span>
                                            <span class="text-[9px] md:text-[10px] font-black text-gray-100 italic">
                                                ${getTrendLabel(kebab.ai_insights.trend)}
                                            </span>
                                        </div>
                                        <div class="flex flex-col items-center text-center">
                                            <span class="text-[8px] text-gray-500 uppercase font-bold tracking-tighter mb-0.5">${aiTranslations[currentLang]['authenticity'] || 'Autentyczność'}</span>
                                            <span class="text-[9px] md:text-[10px] font-black text-blue-400">
                                                ${kebab.ai_insights.authenticity || '100'}%
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    });

    cardsContainer.innerHTML = html;
}

function applyRankingFilter(type, isGlobal) {
    const scope = isGlobal ? 'global' : 'city';
    const filters = window.activeFilters[scope];

    if (type === 'sort_score' || type === 'sort_rating' || type === 'sort_reviews') {
        filters.sort = type.replace('sort_', '');
    } else if (type === 'all') {
        filters.open_now = false;
        filters.nocne = false;
        filters.sort = 'score';
        if (isGlobal) {
            filters.voivodeship = '';
            const voivSel = document.getElementById('global-fb-voiv');
            if (voivSel) voivSel.value = '';
        }
    } else if (type === 'voivodeship') {
        const sel = document.getElementById('global-fb-voiv');
        filters.voivodeship = sel ? sel.value : '';
    } else {
        filters[type] = !filters[type];
    }

    // Update filter pill visual states in-place
    const anyActive = !!(filters.open_now || filters.nocne || (isGlobal && filters.voivodeship));
    const updatePill = (id, active) => {
        const btn = document.getElementById(id);
        if (!btn) return;
        btn.style.border = active ? '1px solid #34d399' : '1px solid rgba(255,255,255,0.15)';
        btn.style.background = active ? 'rgba(52,211,153,0.18)' : 'rgba(255,255,255,0.05)';
        btn.style.color = active ? '#34d399' : '#94a3b8';
    };
    updatePill(`${scope}-fb-all`, !anyActive);
    updatePill(`${scope}-fb-open`, !!filters.open_now);
    updatePill(`${scope}-fb-night`, !!filters.nocne);
    if (isGlobal) {
        const voivSel = document.getElementById('global-fb-voiv');
        if (voivSel) {
            const active = !!filters.voivodeship;
            voivSel.style.border = active ? '1px solid #34d399' : '1px solid rgba(255,255,255,0.15)';
            voivSel.style.color = active ? '#34d399' : '#94a3b8';
        }
    }

    // Update sort pill visual states
    const sort = filters.sort || 'score';
    const updateSortPill = (id, active) => {
        const btn = document.getElementById(id);
        if (!btn) return;
        btn.style.border = active ? '1px solid #60a5fa' : '1px solid rgba(255,255,255,0.12)';
        btn.style.background = active ? 'rgba(96,165,250,0.15)' : 'rgba(255,255,255,0.04)';
        btn.style.color = active ? '#60a5fa' : '#64748b';
    };
    updateSortPill(`${scope}-fb-sort-score`,   sort === 'score');
    updateSortPill(`${scope}-fb-sort-rating`,  sort === 'rating');
    updateSortPill(`${scope}-fb-sort-reviews`, sort === 'reviews');

    const allData = isGlobal ? window.globalRankingData : window.cityRankingData;
    if (!allData) return;

    let filtered = allData;
    if (filters.open_now) filtered = filtered.filter(k => getOpenNowStatus(k.opening_hours)?.open === true);
    if (filters.nocne) filtered = filtered.filter(k => isNightKebab(k.opening_hours));
    if (isGlobal && filters.voivodeship) filtered = filtered.filter(k => CITY_VOIVODESHIP[k.city] === filters.voivodeship);
    filtered = applySortToData(filtered, sort);

    // Re-render cards
    const cardsId = isGlobal ? 'global-ranking-cards' : 'city-ranking-cards';
    const cardsEl = document.getElementById(cardsId);
    if (cardsEl) renderRankingCards(filtered, cardsEl, isGlobal, null);

    // Update map to reflect filter
    if (isGlobal) {
        if (window.globalKebabMap) updateGlobalMapWithKebabs(filtered);
    } else {
        if (window.kebabMap) updateMapWithKebabs(filtered);
    }

    // Update count badge
    const countEl = document.getElementById(`${scope}-fb-count`);
    if (countEl) {
        countEl.style.display = anyActive ? '' : 'none';
        if (anyActive) countEl.textContent = `${filtered.length}/${allData.length}`;
    }

    updateFilterBarHeader(scope, isGlobal);
    syncMobileMapFilter(isGlobal);
}

// ─── KEBAB ROULETTE ──────────────────────────────────────────────────────────

function openRouletteModal(isGlobal) {
    const isEn = (window.currentLang || 'pl') === 'en';
    const allData = isGlobal ? window.globalRankingData : window.cityRankingData;
    if (!allData || allData.length === 0) return;

    // Inject keyframe CSS once
    if (!document.getElementById('roulette-styles')) {
        const s = document.createElement('style');
        s.id = 'roulette-styles';
        s.textContent = `
@keyframes roulette-spin {
  0%   { transform: rotate(0deg) scale(1); }
  40%  { transform: rotate(720deg) scale(1.15); }
  70%  { transform: rotate(1040deg) scale(0.95); }
  85%  { transform: rotate(1080deg) scale(1.05); }
  100% { transform: rotate(1080deg) scale(1); }
}
@keyframes roulette-reveal {
  from { opacity:0; transform: translateY(18px) scale(0.95); }
  to   { opacity:1; transform: translateY(0) scale(1); }
}
.roulette-spinning { animation: roulette-spin 1.6s cubic-bezier(.36,.07,.19,.97) forwards; }
.roulette-reveal   { animation: roulette-reveal 0.45s ease forwards; }`;
        document.head.appendChild(s);
    }

    // Smart topN options
    const n = allData.length;
    let topOptions;
    if (n <= 5)       topOptions = null;           // too few — always all
    else if (n <= 15) topOptions = [5, n];
    else if (n <= 25) topOptions = [5, 10, n];
    else              topOptions = [5, 10, 20, n];

    const stored = window._rouletteTopN || (topOptions ? topOptions[1] : n);
    const defaultTopN = Math.min(stored, n);

    // Build modal
    const overlay = document.createElement('div');
    overlay.id = 'roulette-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;z-index:9000;background:rgba(0,0,0,0.75);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;padding:16px;';
    overlay.onclick = (e) => { if (e.target === overlay) closeRouletteModal(); };

    const optionsHtml = topOptions
        ? topOptions.map(v => {
            const label = v === n ? (isEn ? `All (${n})` : `Wszystkie (${n})`) : `Top ${v}`;
            return `<button onclick="window._rouletteTopN=${v};document.querySelectorAll('.roul-opt').forEach(b=>b.classList.remove('roul-sel'));this.classList.add('roul-sel');spinRoulette(${isGlobal})"
                class="roul-opt${v === defaultTopN ? ' roul-sel' : ''}"
                style="padding:7px 16px;border-radius:9999px;font-size:13px;font-weight:700;cursor:pointer;border:1px solid rgba(251,191,36,${v===defaultTopN?'0.7':'0.25'});background:rgba(251,191,36,${v===defaultTopN?'0.18':'0.05'});color:${v===defaultTopN?'#fbbf24':'#94a3b8'};transition:all 0.2s;"
                onmouseover="this.style.borderColor='rgba(251,191,36,0.5)';this.style.color='#fbbf24'"
                onmouseout="if(!this.classList.contains('roul-sel')){this.style.borderColor='rgba(251,191,36,0.25)';this.style.color='#94a3b8'}"
            >${label}</button>`;
          }).join('')
        : `<span style="font-size:13px;color:#64748b;">${isEn ? `Picking from all ${n} places` : `Losuję ze wszystkich ${n} miejsc`}</span>`;

    overlay.innerHTML = `
    <div style="background:#0f172a;border:1px solid rgba(255,255,255,0.1);border-radius:24px;padding:28px 24px;max-width:420px;width:100%;position:relative;box-shadow:0 25px 60px rgba(0,0,0,0.6);">
        <button onclick="closeRouletteModal()" style="position:absolute;top:16px;right:16px;background:none;border:none;color:#475569;font-size:22px;cursor:pointer;line-height:1;">✕</button>
        <div style="text-align:center;margin-bottom:20px;">
            <div style="font-size:13px;color:#64748b;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:6px;">${isEn ? 'Kebab Roulette' : 'Kebab Ruletka'}</div>
            <div style="font-size:22px;font-weight:800;color:#f1f5f9;">${isEn ? 'Where to eat?' : 'Gdzie zjeść?'} 🥙</div>
        </div>
        ${topOptions ? `
        <div style="margin-bottom:18px;">
            <div style="font-size:11px;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;">${isEn ? 'Pick from:' : 'Losuj z:'}</div>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">${optionsHtml}</div>
        </div>` : `<div style="margin-bottom:16px;text-align:center;">${optionsHtml}</div>`}
        <label style="display:flex;align-items:center;gap:10px;cursor:pointer;margin-bottom:14px;padding:10px 14px;background:#111827;border:1px solid rgba(255,255,255,0.08);border-radius:12px;">
            <input type="checkbox" id="roul-only-open" checked style="width:18px;height:18px;accent-color:#34d399;cursor:pointer;flex-shrink:0;" />
            <span style="font-size:13px;color:#cbd5e1;font-weight:600;">🟢 ${isEn ? 'Open now only' : 'Tylko otwarte teraz'}</span>
        </label>
        <button onclick="spinRoulette(${isGlobal})" id="roul-spin-btn"
            style="width:100%;padding:14px;border-radius:14px;font-size:16px;font-weight:800;border:none;background:linear-gradient(135deg,#f59e0b,#ef4444);color:#fff;cursor:pointer;letter-spacing:0.02em;transition:opacity 0.2s;"
            onmouseover="this.style.opacity='0.88'" onmouseout="this.style.opacity='1'">
            🎲 ${isEn ? 'Spin!' : 'Losuj!'}
        </button>
        <div id="roul-result" style="margin-top:20px;"></div>
    </div>`;

    document.body.appendChild(overlay);
    window._rouletteTopN = window._rouletteTopN || defaultTopN;
}

function closeRouletteModal() {
    const el = document.getElementById('roulette-overlay');
    if (el) el.remove();
}

function spinRoulette(isGlobal) {
    const isEn = (window.currentLang || 'pl') === 'en';
    const allData = isGlobal ? window.globalRankingData : window.cityRankingData;
    if (!allData || allData.length === 0) return;

    const topN = Math.min(window._rouletteTopN || allData.length, allData.length);
    let pool = allData.slice(0, topN);
    const onlyOpenChk = document.getElementById('roul-only-open');
    if (onlyOpenChk && onlyOpenChk.checked) {
        const openPool = pool.filter(k => getOpenNowStatus(k.opening_hours)?.open === true);
        if (openPool.length === 0) {
            const btn2 = document.getElementById('roul-spin-btn');
            const res2 = document.getElementById('roul-result');
            if (res2) res2.innerHTML = `<div style="text-align:center;padding:14px;color:#f87171;font-size:13px;font-weight:600;">😴 ${isEn ? 'No open places in top ' + topN + ' right now. Try unchecking "Open now".' : 'Brak otwartych miejsc w top ' + topN + ' w tej chwili. Odznacz "Tylko otwarte".'}</div>`;
            if (btn2) { btn2.disabled = false; btn2.innerHTML = `🎲 ${isEn ? 'Spin again!' : 'Losuj jeszcze raz!'}`; }
            return;
        }
        pool = openPool;
    }
    const pick = pool[Math.floor(Math.random() * pool.length)];

    const btn = document.getElementById('roul-spin-btn');
    const resultEl = document.getElementById('roul-result');
    if (!btn || !resultEl) return;

    // Animate button
    btn.disabled = true;
    btn.innerHTML = `<span class="roulette-spinning" style="display:inline-block;font-size:22px;">🎲</span>`;
    resultEl.innerHTML = '';

    setTimeout(() => {
        btn.disabled = false;
        btn.innerHTML = `🎲 ${isEn ? 'Spin again!' : 'Losuj jeszcze raz!'}`;

        const rank = (allData.indexOf(pick) + 1);
        const rating = pick.rating ? pick.rating.toFixed(1) : '–';
        const reviews = pick.total_reviews ? pick.total_reviews.toLocaleString() : '–';
        const mapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${pick.latitude},${pick.longitude}`;
        window._roulettePick = {
            name: pick.name,
            rating: pick.rating ? pick.rating.toFixed(1) : null,
            address: pick.address || pick.formatted_address || null,
            gmaps_url: mapsUrl
        };
        const openStatus = getOpenNowStatus(pick.opening_hours);
        const openBadge = openStatus
            ? `<span style="display:inline-block;padding:3px 10px;border-radius:9999px;font-size:11px;font-weight:700;background:${openStatus.open ? 'rgba(52,211,153,0.15)' : 'rgba(248,113,113,0.12)'};color:${openStatus.open ? '#34d399' : '#f87171'};border:1px solid ${openStatus.open ? 'rgba(52,211,153,0.3)' : 'rgba(248,113,113,0.3)'}">${openStatus.label}</span>`
            : '';

        resultEl.innerHTML = `
        <div class="roulette-reveal" style="background:#111827;border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:18px 16px;">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:12px;">
                <div>
                    <div style="font-size:11px;color:#64748b;font-weight:600;margin-bottom:4px;">#${rank} ${isEn ? 'in ranking' : 'w rankingu'}${pick.city ? ' · ' + pick.city : ''}</div>
                    <div style="font-size:18px;font-weight:800;color:#f1f5f9;line-height:1.2;">${pick.name}</div>
                </div>
                <div style="text-align:right;flex-shrink:0;">
                    <div style="font-size:22px;font-weight:900;color:#fbbf24;">★ ${rating}</div>
                    <div style="font-size:11px;color:#475569;">${reviews} ${isEn ? 'reviews' : 'recenzji'}</div>
                </div>
            </div>
            ${openBadge ? `<div style="margin-bottom:12px;">${openBadge}</div>` : ''}
            <a href="${mapsUrl}" target="_blank" rel="noopener"
               style="display:flex;align-items:center;justify-content:center;gap:8px;width:100%;padding:12px;border-radius:12px;background:linear-gradient(135deg,#1d4ed8,#7c3aed);color:#fff;font-size:14px;font-weight:700;text-decoration:none;margin-bottom:10px;">
               🗺️ ${isEn ? 'Navigate' : 'Prowadź'}
            </a>
            <div id="roul-email-area" style="border-top:1px solid rgba(255,255,255,0.07);padding-top:12px;margin-top:2px;">
                <div style="font-size:12px;color:#475569;margin-bottom:8px;">${isEn ? '📱 Send to your phone (email):' : '📱 Wyślij na maila:'}</div>
                <div style="display:flex;gap:8px;">
                    <input id="roul-email-input" type="email" placeholder="${isEn ? 'your@email.com' : 'twoj@email.pl'}"
                        style="flex:1;background:#1e293b;border:1px solid rgba(255,255,255,0.12);border-radius:10px;padding:9px 12px;font-size:13px;color:#f1f5f9;outline:none;"
                        onfocus="this.style.borderColor='rgba(251,191,36,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.12)'" />
                    <button onclick="rouletteSubscribe('${encodeURIComponent(pick.name)}')"
                        style="padding:9px 16px;border-radius:10px;border:1px solid rgba(251,191,36,0.4);background:rgba(251,191,36,0.1);color:#fbbf24;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap;">
                        ${isEn ? 'Send' : 'Wyślij'}
                    </button>
                </div>
                <div style="font-size:10px;color:#334155;margin-top:6px;">${isEn ? 'By subscribing you accept our <a href="/privacy" style="color:#475569;text-decoration:underline;">privacy policy</a>.' : 'Zapisując się akceptujesz <a href="/privacy" style="color:#475569;text-decoration:underline;">politykę prywatności</a>.'}</div>
            </div>
        </div>`;
    }, 1650);
}

function rouletteSubscribe(kebabName) {
    const isEn = (window.currentLang || 'pl') === 'en';
    const input = document.getElementById('roul-email-input');
    if (!input) return;
    const email = input.value.trim();
    if (!email || !email.includes('@')) {
        input.style.borderColor = '#f87171';
        return;
    }
    const pick = window._roulettePick || {};
    fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email,
            source: 'roulette',
            kebab_name:    pick.name || decodeURIComponent(kebabName || ''),
            kebab_rating:  pick.rating || null,
            kebab_address: pick.address || null,
            kebab_gmaps_url: pick.gmaps_url || null
        })
    }).then(r => r.json()).then(data => {
        const area = document.getElementById('roul-email-area');
        if (area) area.innerHTML = `<div style="text-align:center;color:#34d399;font-size:13px;font-weight:700;padding:8px 0;">✓ ${isEn ? 'Saved! Bon appétit 🥙' : 'Zapisano! Smacznego 🥙'}</div>`;
    }).catch(() => {
        const area = document.getElementById('roul-email-area');
        if (area) area.innerHTML = `<div style="color:#f87171;font-size:12px;text-align:center;">${isEn ? 'Error, try again.' : 'Błąd, spróbuj ponownie.'}</div>`;
    });
}

// ─── END ROULETTE ─────────────────────────────────────────────────────────────

// ─── EMAIL CAPTURE ────────────────────────────────────────────────────────────

function _subscribeEmail(email, source, onSuccess, onError) {
    fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, source })
    }).then(r => r.json()).then(d => {
        if (d.ok) onSuccess();
        else onError(d.error || 'error');
    }).catch(() => onError('network'));
}

// Footer newsletter
function footerSubscribe() {
    const isEn = (window.currentLang || 'pl') === 'en';
    const input = document.getElementById('footer-nl-email');
    const btn   = document.getElementById('footer-nl-btn');
    if (!input || !btn) return;
    const email = input.value.trim();
    if (!email || !email.includes('@')) {
        input.style.borderColor = '#f87171';
        input.focus();
        return;
    }
    btn.disabled = true;
    btn.textContent = '...';
    _subscribeEmail(email, 'footer',
        () => { btn.textContent = isEn ? '✓ Done!' : '✓ Zapisano!'; btn.style.color = '#34d399'; input.value = ''; input.disabled = true; },
        () => { btn.textContent = isEn ? 'Error' : 'Błąd'; btn.disabled = false; }
    );
}

// "Obserwuj miasto" modal
function openWatchCityModal(cityName) {
    if (document.getElementById('watch-city-overlay')) return;
    const isEn = (window.currentLang || 'pl') === 'en';
    const overlay = document.createElement('div');
    overlay.id = 'watch-city-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;z-index:9000;background:rgba(0,0,0,0.72);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;padding:16px;';
    overlay.onclick = e => { if (e.target === overlay) overlay.remove(); };
    overlay.innerHTML = `
    <div style="background:#0f172a;border:1px solid rgba(255,255,255,0.1);border-radius:24px;padding:28px 24px;max-width:380px;width:100%;position:relative;box-shadow:0 25px 60px rgba(0,0,0,0.6);">
        <button onclick="document.getElementById('watch-city-overlay').remove()" style="position:absolute;top:14px;right:16px;background:none;border:none;color:#475569;font-size:22px;cursor:pointer;">✕</button>
        <div style="font-size:28px;margin-bottom:8px;">🔔</div>
        <div style="font-size:20px;font-weight:800;color:#f1f5f9;margin-bottom:6px;">${isEn ? 'Follow' : 'Obserwuj'} ${cityName || 'ranking'}</div>
        <div style="font-size:13px;color:#64748b;margin-bottom:20px;line-height:1.5;">${isEn ? 'Get an email when the ranking changes — new #1, new entry, big rise or drop.' : 'Wyślemy maila gdy zmieni się ranking — nowy nr 1, nowe miejsce, duży wzrost lub spad.'}</div>
        <div style="display:flex;gap:8px;margin-bottom:12px;">
            <input id="watch-email-input" type="email" placeholder="${isEn ? 'your@email.com' : 'twoj@email.pl'}"
                style="flex:1;background:#1e293b;border:1px solid rgba(255,255,255,0.12);border-radius:10px;padding:11px 14px;font-size:14px;color:#f1f5f9;outline:none;"
                onfocus="this.style.borderColor='rgba(52,211,153,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.12)'"
                onkeydown="if(event.key==='Enter')watchCitySubscribe('${(cityName||'').replace(/'/g,"\\'")}')"/>
            <button onclick="watchCitySubscribe('${(cityName||'').replace(/'/g,"\\'")}') "
                style="padding:11px 18px;border-radius:10px;border:none;background:linear-gradient(135deg,#34d399,#059669);color:#fff;font-size:14px;font-weight:700;cursor:pointer;">
                ${isEn ? 'Follow' : 'Śledź'}
            </button>
        </div>
        <div id="watch-city-msg" style="min-height:18px;font-size:12px;text-align:center;"></div>
        <div style="font-size:11px;color:#334155;text-align:center;margin-top:10px;">${isEn ? 'No spam. By subscribing you accept our <a href="/privacy" style="color:#475569;text-decoration:underline;">privacy policy</a>.' : 'Zero spamu. Zapisując się akceptujesz <a href="/privacy" style="color:#475569;text-decoration:underline;">politykę prywatności</a>.'}</div>
    </div>`;
    document.body.appendChild(overlay);
    setTimeout(() => { const inp = document.getElementById('watch-email-input'); if (inp) inp.focus(); }, 80);
}

function watchCitySubscribe(cityName) {
    const isEn = (window.currentLang || 'pl') === 'en';
    const input = document.getElementById('watch-email-input');
    const msg   = document.getElementById('watch-city-msg');
    if (!input) return;
    const email = input.value.trim();
    if (!email || !email.includes('@')) { input.style.borderColor = '#f87171'; return; }
    _subscribeEmail(email, 'city_watch:' + (cityName || ''),
        () => {
            if (msg) { msg.style.color = '#34d399'; msg.textContent = isEn ? '✓ Done! We\'ll notify you.' : '✓ Zapisano! Poinformujemy Cię.'; }
            input.disabled = true;
            setTimeout(() => { const ov = document.getElementById('watch-city-overlay'); if (ov) ov.remove(); }, 2200);
        },
        () => { if (msg) { msg.style.color = '#f87171'; msg.textContent = isEn ? 'Error, try again.' : 'Błąd, spróbuj ponownie.'; } }
    );
}

// Exit intent popup
(function initExitIntent() {
    let shown = false;
    const COOLDOWN_KEY = 'kr_exit_intent_ts';
    function shouldShow() {
        if (shown) return false;
        const last = parseInt(localStorage.getItem(COOLDOWN_KEY) || '0', 10);
        return Date.now() - last > 7 * 24 * 60 * 60 * 1000; // raz na 7 dni
    }
    function showExitIntent() {
        if (!shouldShow()) return;
        shown = true;
        localStorage.setItem(COOLDOWN_KEY, Date.now().toString());
        const isEn = (window.currentLang || 'pl') === 'en';
        const overlay = document.createElement('div');
        overlay.id = 'exit-intent-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;z-index:9100;background:rgba(0,0,0,0.65);backdrop-filter:blur(5px);display:flex;align-items:center;justify-content:center;padding:16px;animation:roulette-reveal 0.3s ease forwards;';
        overlay.onclick = e => { if (e.target === overlay) overlay.remove(); };
        overlay.innerHTML = `
        <div style="background:#0f172a;border:1px solid rgba(255,255,255,0.1);border-radius:24px;padding:28px 24px;max-width:400px;width:100%;position:relative;box-shadow:0 25px 60px rgba(0,0,0,0.7);text-align:center;">
            <button onclick="document.getElementById('exit-intent-overlay').remove()" style="position:absolute;top:14px;right:16px;background:none;border:none;color:#475569;font-size:22px;cursor:pointer;">✕</button>
            <div style="font-size:36px;margin-bottom:10px;">🥙</div>
            <div style="font-size:21px;font-weight:800;color:#f1f5f9;margin-bottom:8px;">${isEn ? 'Before you go...' : 'Zanim wyjdziesz…'}</div>
            <div style="font-size:13px;color:#64748b;margin-bottom:22px;line-height:1.6;">${isEn ? 'Rankings update monthly. Leave your email and be the first to know when a new #1 appears in your city.' : 'Rankingi aktualizujemy co miesiąc. Zostaw maila i dowiedz się pierwszy, gdy pojawi się nowy nr 1 w Twoim mieście.'}</div>
            <div style="display:flex;gap:8px;margin-bottom:12px;">
                <input id="exit-email-input" type="email" placeholder="${isEn ? 'your@email.com' : 'twoj@email.pl'}"
                    style="flex:1;background:#1e293b;border:1px solid rgba(255,255,255,0.12);border-radius:10px;padding:11px 14px;font-size:14px;color:#f1f5f9;outline:none;"
                    onfocus="this.style.borderColor='rgba(52,211,153,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.12)'"
                    onkeydown="if(event.key==='Enter')exitIntentSubscribe()" />
                <button onclick="exitIntentSubscribe()"
                    style="padding:11px 18px;border-radius:10px;border:none;background:linear-gradient(135deg,#f59e0b,#ef4444);color:#fff;font-size:14px;font-weight:700;cursor:pointer;white-space:nowrap;">
                    ${isEn ? 'Notify me' : 'Zapisz'}
                </button>
            </div>
            <div id="exit-intent-msg" style="min-height:18px;font-size:12px;"></div>
            <div style="font-size:11px;color:#334155;margin-top:8px;">${isEn ? 'By subscribing you accept our <a href="/privacy" style="color:#475569;text-decoration:underline;">privacy policy</a>.' : 'Zapisując się akceptujesz <a href="/privacy" style="color:#475569;text-decoration:underline;">politykę prywatności</a>.'}</div>
            <button onclick="document.getElementById('exit-intent-overlay').remove()" style="background:none;border:none;color:#334155;font-size:12px;cursor:pointer;margin-top:8px;">${isEn ? 'No thanks' : 'Nie, dziękuję'}</button>
        </div>`;
        document.body.appendChild(overlay);
        setTimeout(() => { const inp = document.getElementById('exit-email-input'); if (inp) inp.focus(); }, 80);
    }
    // Desktop: cursor leaves viewport near top
    document.addEventListener('mouseleave', e => {
        if (e.clientY < 8) showExitIntent();
    });
    // Mobile: page visibility hidden (switch tab / home button)
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') showExitIntent();
    });
})();

function exitIntentSubscribe() {
    const isEn = (window.currentLang || 'pl') === 'en';
    const input = document.getElementById('exit-email-input');
    const msg   = document.getElementById('exit-intent-msg');
    if (!input) return;
    const email = input.value.trim();
    if (!email || !email.includes('@')) { input.style.borderColor = '#f87171'; return; }
    _subscribeEmail(email, 'exit_intent',
        () => {
            if (msg) { msg.style.color = '#34d399'; msg.textContent = isEn ? '✓ Done! Talk soon 🥙' : '✓ Zapisano! Do zobaczenia 🥙'; }
            input.disabled = true;
            setTimeout(() => { const ov = document.getElementById('exit-intent-overlay'); if (ov) ov.remove(); }, 2500);
        },
        () => { if (msg) { msg.style.color = '#f87171'; msg.textContent = isEn ? 'Error, try again.' : 'Błąd, spróbuj ponownie.'; } }
    );
}

// ─── END EMAIL CAPTURE ────────────────────────────────────────────────────────

// Add CSS Helper for sentiment color if not exists
function getSentimentColorClass(sentiment) {
    if (typeof sentiment === 'number') {
        if (sentiment > 0.5) return 'text-green-400';
        if (sentiment > 0.2) return 'text-green-200';
        if (sentiment < -0.5) return 'text-red-500';
        if (sentiment < -0.2) return 'text-red-300';
    }
    return 'text-gray-300';
}

// Render skeleton loaders to prevent CLS
function renderSkeletons(count = 5) {
    let html = '';
    for (let i = 0; i < count; i++) {
        html += `
            <div class="skeleton-card">
                <div class="skeleton-img skeleton-loader"></div>
                <div class="skeleton-content">
                    <div class="skeleton-text skeleton-loader"></div>
                    <div class="skeleton-text-short skeleton-loader"></div>
                    <div class="flex gap-2 mt-2">
                        <div class="skeleton-badge skeleton-loader"></div>
                        <div class="skeleton-badge skeleton-loader"></div>
                    </div>
                </div>
            </div>
            `;
    }
    return html;
}


// Alias for backward compatibility if needed, though checkAndLoadRankings now calls displayRankings directly
function displayAIRankings(rankings, container, cityName, limit) {
    displayRankings(rankings, container, cityName);
}

// Prefetch city data to make the transition feel instant
async function prefetchCity(cityName) {
    const limit = $id('kebab-count')?.value || 10;
    const cacheKey = `${cityName}_${limit}_${currentLang}`;

    // Don't prefetch if already in cache or if it's the current city
    if (rankingCache[cacheKey] || window.currentCity === cityName) return;

    console.log(`Prefetching data for ${cityName}...`);
    try {
        const url = `/api/rankings/${encodeURIComponent(cityName)}/ai?lang=${currentLang}&limit=${limit}`;
        const response = await fetch(url);
        const result = await response.json();

        if (result.status === 'success') {
            rankingCache[cacheKey] = result.data;
            console.log(`Prefetched data for ${cityName} stored in cache.`);
        }
    } catch (e) {
        console.warn(`Prefetch failed for ${cityName}:`, e);
    }
}

// --- Mega Menu Visuals ---
/**
 * Renders high-end city images in the Mega Menu (Popular Cities)
 * Replaces generic icons with custom photography where available.
 */
function refreshCityPhotography() {
    console.log("🏙️ Refreshing City Photography...");
    const modalCards = document.querySelectorAll(".city-modal-card");
    if (!modalCards.length) {
        console.warn("⚠️ No city-modal-cards found to refresh.");
        return;
    }

    modalCards.forEach(card => {
        const cityName = card.getAttribute("data-city");
        const imgWrapper = card.querySelector(".city-card-image-wrapper");
        const icon = card.querySelector(".city-card-icon");
        
        if (!cityName || !imgWrapper) return;

        // Use our now-global intelligent mapping logic
        const imageFile = getCityImageFile(cityName);
        
        if (imageFile) {
            // Apply high-res background
            const smFile = imageFile.replace('.webp', '-sm.webp');
            imgWrapper.innerHTML = `
                <img src="/static/img/cities/${imageFile}"
                     srcset="/static/img/cities/${smFile} 400w, /static/img/cities/${imageFile} 800w"
                     sizes="(max-width: 767px) 220px, 400px"
                     width="800" height="500"
                     alt="${cityName}"
                     class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110">
            `;
            // Hide generic icons for a premium look
            if (icon) {
                icon.style.opacity = "0";
                icon.style.visibility = "hidden";
            }
            imgWrapper.classList.remove("bg-gradient-to-br");
        } else {
            // Glassmorphism Fallback if no specific photo exists
            imgWrapper.classList.add("bg-gradient-to-br", "from-surface-dark/40", "to-background-dark/80");
            if (icon) {
                icon.style.opacity = "0.4";
                icon.style.visibility = "visible";
            }
        }
    });
}

// Global handle for modal triggers
window.initMegaMenuVisuals = function() {
    // Immediate call and a slightly delayed one to catch any DOM injection
    refreshCityPhotography();
    setTimeout(refreshCityPhotography, 100);
};

// Auto-bind to the search trigger (Mega Menu opening button)
document.addEventListener("DOMContentLoaded", () => {
    const searchBtn = document.getElementById("mega-menu-trigger");
    if (searchBtn) {
        console.log("🔗 Binding mega-menu-trigger to initMegaMenuVisuals");
        searchBtn.addEventListener("click", () => {
            // Show the menu handled by CSS/Alpine or standard JS
            const menu = document.getElementById('mega-menu');
            if (menu) {
                menu.classList.remove('hidden');
                menu.classList.add('flex');
            }
            window.initMegaMenuVisuals();
        });
    }

    const closeBtn = document.getElementById("close-mega-menu");
    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            const menu = document.getElementById('mega-menu');
            if (menu) {
                menu.classList.add('hidden');
                menu.classList.remove('flex');
            }
        });
    }
});

// ─── CITY SEARCH ──────────────────────────────────────────────────────────────

function filterCitySearch(query) {
    const q = (query || '').trim().toLowerCase();
    const popularSection = document.getElementById('popular-section');
    const azHeader       = document.getElementById('az-header');
    const noResults      = document.getElementById('az-no-results');
    const clearBtn       = document.getElementById('city-search-clear');
    const links          = document.querySelectorAll('.city-az-link');

    if (clearBtn) clearBtn.style.display = q ? '' : 'none';

    if (!q) {
        links.forEach(el => el.style.display = '');
        if (popularSection) popularSection.style.display = '';
        if (azHeader)       azHeader.style.display = '';
        if (noResults)      noResults.style.display = 'none';
        return;
    }

    if (popularSection) popularSection.style.display = 'none';
    if (azHeader)       azHeader.style.display = 'none';

    let count = 0;
    links.forEach(el => {
        const city = (el.dataset.city || el.textContent).toLowerCase();
        const match = city.includes(q);
        el.style.display = match ? '' : 'none';
        if (match) count++;
    });
    if (noResults) noResults.style.display = 'none';
    if (count === 0) showCityRequestForm(q);
    else hideCityRequestForm();
}

function showCityRequestForm(cityName) {
    const existing = document.getElementById('city-request-box');
    if (existing) { document.getElementById('city-req-city').value = cityName; return; }
    const box = document.createElement('div');
    box.id = 'city-request-box';
    box.style.cssText = 'grid-column:1/-1;padding:24px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;margin-top:8px;';
    box.innerHTML = `
        <div style="font-size:15px;font-weight:700;color:#f1f5f9;margin-bottom:4px;">Nie ma jeszcze tego miasta 😔</div>
        <div style="font-size:13px;color:#64748b;margin-bottom:18px;">Zgłoś swoje miasto — dodamy je do rankingu i poinformujemy Cię mailem!</div>
        <div style="display:flex;flex-direction:column;gap:10px;">
            <input id="city-req-city" type="text" placeholder="Nazwa miasta" value="${cityName}"
                style="background:#1e293b;border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:10px 14px;font-size:14px;color:#f1f5f9;outline:none;width:100%;box-sizing:border-box;"
                onfocus="this.style.borderColor='rgba(255,106,0,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'"/>
            <select id="city-req-voiv"
                style="background:#1e293b;border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:10px 14px;font-size:14px;color:#94a3b8;outline:none;width:100%;box-sizing:border-box;"
                onfocus="this.style.borderColor='rgba(255,106,0,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
                <option value="">Wybierz województwo…</option>
                <option>Dolnośląskie</option><option>Kujawsko-Pomorskie</option>
                <option>Lubelskie</option><option>Lubuskie</option>
                <option>Łódzkie</option><option>Małopolskie</option>
                <option>Mazowieckie</option><option>Opolskie</option>
                <option>Podkarpackie</option><option>Podlaskie</option>
                <option>Pomorskie</option><option>Śląskie</option>
                <option>Świętokrzyskie</option><option>Warmińsko-Mazurskie</option>
                <option>Wielkopolskie</option><option>Zachodniopomorskie</option>
            </select>
            <input id="city-req-email" type="email" placeholder="Twój e-mail (powiadomimy Cię o dodaniu)"
                style="background:#1e293b;border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:10px 14px;font-size:14px;color:#f1f5f9;outline:none;width:100%;box-sizing:border-box;"
                onfocus="this.style.borderColor='rgba(255,106,0,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'"
                onkeydown="if(event.key==='Enter')submitCityRequest()"/>
            <button onclick="submitCityRequest()"
                style="padding:11px;border-radius:10px;border:none;background:linear-gradient(135deg,#ff6a00,#ee0979);color:#fff;font-size:14px;font-weight:700;cursor:pointer;">
                Zgłoś miasto →
            </button>
        </div>
        <div id="city-req-msg" style="min-height:16px;font-size:12px;margin-top:10px;text-align:center;"></div>
        <div style="font-size:10px;color:#334155;margin-top:8px;text-align:center;">Zapisując się akceptujesz <a href="/privacy" style="color:#475569;text-decoration:underline;">politykę prywatności</a>.</div>`;
    const grid = document.getElementById('az-grid');
    if (grid) grid.appendChild(box);
}

function hideCityRequestForm() {
    const box = document.getElementById('city-request-box');
    if (box) box.remove();
}

function submitCityRequest() {
    const city  = (document.getElementById('city-req-city')?.value || '').trim();
    const voiv  = (document.getElementById('city-req-voiv')?.value || '').trim();
    const email = (document.getElementById('city-req-email')?.value || '').trim();
    const msg   = document.getElementById('city-req-msg');
    if (!city)  { document.getElementById('city-req-city').style.borderColor  = '#f87171'; return; }
    if (!voiv)  { document.getElementById('city-req-voiv').style.borderColor  = '#f87171'; return; }
    if (!email || !email.includes('@')) { document.getElementById('city-req-email').style.borderColor = '#f87171'; return; }
    fetch('/api/request-city', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ city, voivodeship: voiv, email })
    }).then(r => r.json()).then(d => {
        if (msg) { msg.style.color = '#34d399'; msg.textContent = '✓ Zgłoszono! Poinformujemy Cię gdy miasto zostanie dodane.'; }
        ['city-req-city','city-req-voiv','city-req-email'].forEach(id => { const el = document.getElementById(id); if (el) el.disabled = true; });
        const btn = document.querySelector('#city-request-box button');
        if (btn) btn.disabled = true;
    }).catch(() => {
        if (msg) { msg.style.color = '#f87171'; msg.textContent = 'Błąd, spróbuj ponownie.'; }
    });
}

function clearCitySearch() {
    const inp = document.getElementById('city-search-input');
    if (inp) { inp.value = ''; inp.focus(); }
    filterCitySearch('');
}

function filterCitySearchEnter() {
    const links = Array.from(document.querySelectorAll('.city-az-link'))
                       .filter(el => el.style.display !== 'none');
    if (links.length === 1) links[0].click();
}
