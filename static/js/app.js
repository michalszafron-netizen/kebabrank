// static/js/app.js
const $id = (id) => document.getElementById(id);

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
        'show-top': 'Show top:',
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
        'show-top': 'Pokaż top:',
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

        // Auto-load Kraków as default city - fixed approach
        setTimeout(() => {
            console.log('🔄 Checking if Kraków should auto-load...');
            const searchInput = $id('city-search');
            const cityRankings = $id('city-tab');

            // Check if we're on home page (no city-specific URL)
            const isHomePage = window.location.pathname === '/' || window.location.pathname === '';

            // Check if rankings are empty (showing search prompt)
            const hasEmptyRankings = cityRankings && cityRankings.innerHTML.includes('search-prompt');

            // Check if search field is empty OR contains Kraków but rankings aren't loaded
            const searchValue = searchInput ? searchInput.value.trim() : '';
            const hasKrakowInSearch = searchValue === 'Kraków';
            const shouldLoadKrakow = !searchValue || (hasKrakowInSearch && hasEmptyRankings);

            console.log('📊 Auto-load conditions:', {
                isHomePage,
                hasEmptyRankings,
                searchInputValue: searchValue,
                hasKrakowInSearch,
                shouldLoadKrakow
            });

            if (isHomePage && shouldLoadKrakow) {
                console.log('✅ Auto-loading Kraków as default city');
                autoLoadKrakowAsDefault();
            } else {
                console.log('❌ Skipping auto-load - conditions not met');
            }
        }, 1000); // Wait 1 second for other initialization to complete
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
    $id('city-search').value = cityName;

    // Hide dropdown on both desktop and mobile
    if (dropdown) {
        dropdown.classList.remove('active');
        dropdown.classList.add('hidden');
        dropdown.style.display = 'none';
        dropdown.style.visibility = 'hidden';
        dropdown.style.opacity = '0';
    }


    isDropdownOpen = false;

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
        const response = await fetch(`/api/rankings/global?limit=${limit}`);
        const data = await response.json();
        if (data.status === 'success') {
            displayRankings(data.data, container, null, true);
            // Update global map with markers
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

// Robust auto-load function for Kraków as default city
function autoLoadKrakowAsDefault() {
    console.log('🚀 autoLoadKrakowAsDefault() function called');

    // Wait a bit for other initialization to complete
    setTimeout(() => {
        console.log('🔍 Starting auto-load check after timeout');

        // Check desktop version first
        const searchInput = $id('city-search');
        const cityRankings = $id('city-tab');

        // Check if search field is empty OR contains Kraków but rankings aren't loaded
        const searchValue = searchInput ? searchInput.value.trim() : '';
        const hasKrakowInSearch = searchValue === 'Kraków';
        const hasEmptyRankings = cityRankings && cityRankings.innerHTML.includes('search-prompt');
        const shouldLoadKrakow = !searchValue || (hasKrakowInSearch && hasEmptyRankings);

        if (searchInput && shouldLoadKrakow) {
            console.log('✅ Auto-loading Kraków as default city');

            // Set Kraków as default value in search field if empty
            if (!searchValue) {
                searchInput.value = 'Kraków';
                console.log('✅ Set search input value to "Kraków"');
            } else {
                console.log('ℹ️ Search field already has "Kraków"');
            }

            // Switch to City Rankings tab if not already there
            const cityTabButton = document.querySelector('.tab-button[onclick*="city"]');
            console.log('📝 City tab button found:', !!cityTabButton);
            if (cityTabButton) {
                console.log('📝 City tab button active status:', cityTabButton.classList.contains('active'));
                if (!cityTabButton.classList.contains('active')) {
                    console.log('✅ Switching to City Rankings tab');
                    cityTabButton.click();
                } else {
                    console.log('ℹ️ City tab already active');
                }
            }

            // Load Kraków rankings
            const limit = $id('kebab-count')?.value || 10;
            console.log('📝 Loading Kraków rankings with limit:', limit);
            checkAndLoadRankings('Kraków', limit);

            // Update URL for sharing
            updateCityUrl('Kraków');
        }
    }, 1000); // 1 second delay to ensure other initialization completes
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

// Initialize the city map
function initializeMap() {
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

    console.log('City map initialized successfully');
}

// Initialize the global map
function initializeGlobalMap() {
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

    console.log('Global map initialized successfully');
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


// Center map on specific kebab place
function centerMapOnKebab(index) {
    if (!kebabMap || !mapMarkers[index]) return;

    const marker = mapMarkers[index];
    const latLng = marker.getLatLng();
    kebabMap.setView(latLng, 15);
    marker.openPopup();
}

// Initialize map when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize map on desktop immediately to save TBT on mobile
    if (window.innerWidth > 768) {
        initializeMap();
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

            // Smoothly hide banner
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

    const icons = ['store', 'restaurant', 'local_dining', 'location_city', 'business', 'apartment', 'domain', 'location_on', 'map', 'place', 'fastfood', 'dinner_dining'];

    cities.forEach(city => {
        const citySlug = city.toLowerCase()
            .replace(/ /g, '-')
            .replace(/ł/g, 'l').replace(/ó/g, 'o').replace(/ą/g, 'a')
            .replace(/ę/g, 'e').replace(/ć/g, 'c').replace(/ń/g, 'n')
            .replace(/ś/g, 's').replace(/ź/g, 'z').replace(/ż/g, 'z');

        const btn = document.createElement('a');
        btn.href = `/kebab-${citySlug}`;
        btn.className = 'tab-button flex flex-col items-center gap-2 group min-w-[64px] snap-start';
        btn.onclick = (e) => {
            e.preventDefault();
            selectCity(city);
        };

        // Determine icon based on city name hash to be consistent but varied
        let hash = 0;
        for (let i = 0; i < city.length; i++) {
            hash = city.charCodeAt(i) + ((hash << 5) - hash);
        }
        const iconIndex = Math.abs(hash) % icons.length;
        const icon = icons[iconIndex];

        // Specific overrides for major cities
        let finalIcon = icon;
        if (city === 'Kraków') finalIcon = 'castle';
        else if (city === 'Warszawa') finalIcon = 'location_city';
        else if (city === 'Wrocław') finalIcon = 'apartment';
        else if (city === 'Gdańsk' || city === 'Gdynia' || city === 'Sopot') finalIcon = 'sailing';

        const isSelected = window.currentCity && city === window.currentCity;
        const activeClass = isSelected ? 'active' : '';

        btn.className = `tab-button flex flex-col items-center gap-2 group min-w-[56px] md:min-w-[64px] snap-start ${activeClass}`;
        btn.onclick = (e) => {
            e.preventDefault();
            selectCity(city);
        };

        btn.innerHTML = `
                <div class="tab-icon-wrapper w-12 h-12 md:w-16 md:h-16 rounded-full bg-surface-dark border border-white/10 flex items-center justify-center relative transition-all duration-300 group-hover:scale-105">
                    <span class="material-icons ${isSelected ? 'text-primary' : 'text-gray-400'} text-xl md:text-2xl">${finalIcon}</span>
                </div>
                <span class="text-[10px] md:text-xs font-bold tracking-wide uppercase text-center w-16 md:w-20 leading-tight transition-colors duration-300 px-1 truncate">
                    ${city}
                </span>
            `;

        // Add prefetch on hover
        btn.addEventListener('mouseenter', () => prefetchCity(city));

        selector.appendChild(btn);
    });
}

// Regular rankings display function
function displayRankings(rankings, container, cityName, isGlobal = false) {
    if (rankings.length === 0) {
        container.innerHTML = `<p class="text-center text-gray-500 py-4">${translations[currentLang]['no-kebabs']}</p>`;
        return;
    }

    // Ensure rankings are properly sorted by rank_score descending
    const sortedRankings = [...rankings].sort((a, b) => {
        if (b.rank_score !== a.rank_score) {
            return b.rank_score - a.rank_score;
        }
        // Secondary sort by rating if scores are equal
        return b.rating - a.rating;
    });

    let html = '';

    sortedRankings.forEach((kebab, index) => {
        const rank = kebab.rank || index + 1;
        const hasAI = kebab.has_ai_analysis === true || (kebab.ai_summary && kebab.ai_summary.length > 0);

        // Rank Colors/Styles
        let rankBadgeClass = "bg-surface-dark text-gray-400";
        if (rank === 1) rankBadgeClass = "bg-yellow-500 text-black";
        else if (rank === 2) rankBadgeClass = "bg-gray-400 text-black";
        else if (rank === 3) rankBadgeClass = "bg-orange-700 text-white";

        // Rank change indicator
        let rankChangeHtml = '';
        if (kebab.is_new) {
            rankChangeHtml = `<span class="rank-badge-mini rank-new ml-2">NEW</span>`;
        } else if (kebab.rank_change_indicator === 'up' && kebab.rank_change) {
            rankChangeHtml = `<span class="rank-badge-mini rank-up ml-2"><span class="text-[8px]">▲</span> +${kebab.rank_change}</span>`;
        } else if (kebab.rank_change_indicator === 'down' && kebab.rank_change) {
            const absChange = Math.abs(kebab.rank_change);
            rankChangeHtml = `<span class="rank-badge-mini rank-down ml-2"><span class="text-[8px]">▼</span> -${absChange}</span>`;
        } else {
            rankChangeHtml = `<span class="rank-badge-mini rank-neutral ml-2">-</span>`;
        }

        const photoUrl = kebab.photo_url;
        const hasValidPhoto = photoUrl && photoUrl !== 'NONE' && photoUrl.length > 10;
        const kebabImage = hasValidPhoto ? photoUrl : (kebab.image_url || "https://lh3.googleusercontent.com/aida-public/AB6AXuAPZml7HBCvOmxHc3pErimDG6i7ruSOL6NrxB8S8CkUtAIZ9sjOe5U0TSzY4AbGN8NSPkGQZHCdrnALIQoLgGNrze3MwVl9x7OGSn2Gz7CvsUTB4izX8Xatv_tIbLYX6kiuSDVdT3HoS7MKLCnQparIKmg8UVIl7QU1CTAKEBVF9M8_NiLS2ccsanJPm-7kevE10rqP_NKMyBgiXUpcsUtj4e9eJlwKM02h-oL83bYxG2QwVRiuDKWgPfePcvFNWLVGzfpHYYn_Nl4");

        html += `
            <div class="glass-card rounded-xl p-3 md:p-4 flex gap-3 md:gap-4 relative overflow-hidden group cursor-pointer hover:bg-white/5 hover:border-primary/30 mb-2 md:mb-3 transition-all duration-300"
                 onclick="${isGlobal ? `centerGlobalMapOnKebab(${index})` : `centerMapOnKebab(${index})`}"
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
                             onerror="console.warn('⚠️ Photo load error'); this.onerror=null; this.src='https://lh3.googleusercontent.com/aida-public/AB6AXuAPZml7HBCvOmxHc3pErimDG6i7ruSOL6NrxB8S8CkUtAIZ9sjOe5U0TSzY4AbGN8NSPkGQZHCdrnALIQoLgGNrze3MwVl9x7OGSn2Gz7CvsUTB4izX8Xatv_tIbLYX6kiuSDVdT3HoS7MKLCnQparIKmg8UVIl7QU1CTAKEBVF9M8_NiLS2ccsanJPm-7kevE10rqP_NKMyBgiXUpcsUtj4e9eJlwKM02h-oL83bYxG2QwVRiuDKWgPfePcvFNWLVGzfpHYYn_Nl4'"/>
                    </div>
                    <p class="text-[9px] text-gray-400 text-center leading-tight break-words w-full opacity-80">
                        ${kebab.address}, ${kebab.city || window.currentCity || ''}
                    </p>
                </div>

                <!-- Content -->
                <div class="flex-1 flex flex-col min-w-0">
                    <div>
                        <div class="flex justify-between items-start">
                             <!-- Middle Column: Title & Button -->
                             <div class="flex flex-col gap-1 min-w-0 flex-1 pr-2">
                                 <h3 class="text-xs md:text-lg font-bold text-white group-hover:text-primary transition-colors mb-0.5 md:truncate leading-tight">${kebab.name} ${rankChangeHtml}</h3>
                                 
                                 <!-- Navigate Button -->
                                 ${kebab.latitude && kebab.longitude ? `
                                <a href="https://www.google.com/maps/dir/?api=1&destination=${kebab.latitude},${kebab.longitude}" 
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

    container.classList.remove('ranking-fade-in');
    void container.offsetWidth; // Force reflow to restart animation
    container.innerHTML = html;
    container.classList.add('ranking-fade-in');
}

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
