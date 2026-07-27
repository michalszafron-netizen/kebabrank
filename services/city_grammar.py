# services/city_grammar.py
"""
Odmiana nazw miast przez miejscownik ("w Krakowie") i dopełniacz ("Krakowa").

Powód istnienia: tytuły SEO budowane jako f"Najlepszy kebab w {city}" dawały
niegramatyczne "Najlepszy kebab w Kraków" na wszystkich stronach miast.
"""

# Miejscownik — odpowiada na "w kim? w czym?" → "w Krakowie"
LOCATIVE = {
    'Białystok': 'Białymstoku',
    'Bielsko-Biała': 'Bielsku-Białej',
    'Bydgoszcz': 'Bydgoszczy',
    'Bytom': 'Bytomiu',
    'Chorzów': 'Chorzowie',
    'Czechowice-Dziedzice': 'Czechowicach-Dziedzicach',
    'Częstochowa': 'Częstochowie',
    'Dobczyce': 'Dobczycach',
    'Dąbrowa Górnicza': 'Dąbrowie Górniczej',
    'Elbląg': 'Elblągu',
    'Gdańsk': 'Gdańsku',
    'Gdynia': 'Gdyni',
    'Gliwice': 'Gliwicach',
    'Gorzów Wielkopolski': 'Gorzowie Wielkopolskim',
    'Grudziądz': 'Grudziądzu',
    'Inowrocław': 'Inowrocławiu',
    'Jastrzębie-Zdrój': 'Jastrzębiu-Zdroju',
    'Jaworzno': 'Jaworznie',
    'Jordanów': 'Jordanowie',
    'Kalisz': 'Kaliszu',
    'Katowice': 'Katowicach',
    'Kielce': 'Kielcach',
    'Konin': 'Koninie',
    'Koszalin': 'Koszalinie',
    'Koziegłowy': 'Koziegłowach',
    'Kraków': 'Krakowie',
    'Legnica': 'Legnicy',
    'Lubin': 'Lubinie',
    'Lublin': 'Lublinie',
    'Mysłowice': 'Mysłowicach',
    'Myslowice': 'Mysłowicach',      # wariant bez znaków diakrytycznych w bazie
    'Myszków': 'Myszkowie',
    'Nowy Sącz': 'Nowym Sączu',
    'Olsztyn': 'Olsztynie',
    'Opole': 'Opolu',
    'Oświęcim': 'Oświęcimiu',
    'Oswiecim': 'Oświęcimiu',        # wariant bez znaków diakrytycznych w bazie
    'Piotrków Trybunalski': 'Piotrkowie Trybunalskim',
    'Piła': 'Pile',
    'Poraj': 'Poraju',
    'Poznań': 'Poznaniu',
    'Pszczyna': 'Pszczynie',
    'Płock': 'Płocku',
    'Radom': 'Radomiu',
    'Ruda Śląska': 'Rudzie Śląskiej',
    'Rybnik': 'Rybniku',
    'Rzeszów': 'Rzeszowie',
    'Siedlce': 'Siedlcach',
    'Skawina': 'Skawinie',
    'Sosnowiec': 'Sosnowcu',
    'Szczecin': 'Szczecinie',
    'Słupsk': 'Słupsku',
    'Tarnów': 'Tarnowie',
    'Toruń': 'Toruniu',
    'Tychy': 'Tychach',
    'Warszawa': 'Warszawie',
    'Wałbrzych': 'Wałbrzychu',
    'Wieliczka': 'Wieliczce',
    'Wolbrom': 'Wolbromiu',
    'Wrocław': 'Wrocławiu',
    'Włocławek': 'Włocławku',
    'Zabrze': 'Zabrzu',
    'Zakopane': 'Zakopanem',
    'Zielona Góra': 'Zielonej Górze',
    'Łódź': 'Łodzi',
    'Żarki': 'Żarkach',
}

# Dopełniacz — "ranking Krakowa", "mieszkańcy Krakowa"
GENITIVE = {
    'Białystok': 'Białegostoku',
    'Bielsko-Biała': 'Bielska-Białej',
    'Bydgoszcz': 'Bydgoszczy',
    'Bytom': 'Bytomia',
    'Chorzów': 'Chorzowa',
    'Czechowice-Dziedzice': 'Czechowic-Dziedzic',
    'Częstochowa': 'Częstochowy',
    'Dobczyce': 'Dobczyc',
    'Dąbrowa Górnicza': 'Dąbrowy Górniczej',
    'Elbląg': 'Elbląga',
    'Gdańsk': 'Gdańska',
    'Gdynia': 'Gdyni',
    'Gliwice': 'Gliwic',
    'Gorzów Wielkopolski': 'Gorzowa Wielkopolskiego',
    'Grudziądz': 'Grudziądza',
    'Inowrocław': 'Inowrocławia',
    'Jastrzębie-Zdrój': 'Jastrzębia-Zdroju',
    'Jaworzno': 'Jaworzna',
    'Jordanów': 'Jordanowa',
    'Kalisz': 'Kalisza',
    'Katowice': 'Katowic',
    'Kielce': 'Kielc',
    'Konin': 'Konina',
    'Koszalin': 'Koszalina',
    'Koziegłowy': 'Koziegłów',
    'Kraków': 'Krakowa',
    'Legnica': 'Legnicy',
    'Lubin': 'Lubina',
    'Lublin': 'Lublina',
    'Mysłowice': 'Mysłowic',
    'Myslowice': 'Mysłowic',
    'Myszków': 'Myszkowa',
    'Nowy Sącz': 'Nowego Sącza',
    'Olsztyn': 'Olsztyna',
    'Opole': 'Opola',
    'Oświęcim': 'Oświęcimia',
    'Oswiecim': 'Oświęcimia',
    'Piotrków Trybunalski': 'Piotrkowa Trybunalskiego',
    'Piła': 'Piły',
    'Poraj': 'Poraja',
    'Poznań': 'Poznania',
    'Pszczyna': 'Pszczyny',
    'Płock': 'Płocka',
    'Radom': 'Radomia',
    'Ruda Śląska': 'Rudy Śląskiej',
    'Rybnik': 'Rybnika',
    'Rzeszów': 'Rzeszowa',
    'Siedlce': 'Siedlec',
    'Skawina': 'Skawiny',
    'Sosnowiec': 'Sosnowca',
    'Szczecin': 'Szczecina',
    'Słupsk': 'Słupska',
    'Tarnów': 'Tarnowa',
    'Toruń': 'Torunia',
    'Tychy': 'Tychów',
    'Warszawa': 'Warszawy',
    'Wałbrzych': 'Wałbrzycha',
    'Wieliczka': 'Wieliczki',
    'Wolbrom': 'Wolbromia',
    'Wrocław': 'Wrocławia',
    'Włocławek': 'Włocławka',
    'Zabrze': 'Zabrza',
    'Zakopane': 'Zakopanego',
    'Zielona Góra': 'Zielonej Góry',
    'Łódź': 'Łodzi',
    'Żarki': 'Żarek',
}


def locative(city_name: str) -> str:
    """
    Zwraca miasto w miejscowniku — forma po przyimku "w".
    Nieznane miasto zwraca formę wyjściową (bezpieczny fallback).

    >>> locative('Kraków')
    'Krakowie'
    """
    if not city_name:
        return ''
    return LOCATIVE.get(city_name.strip(), city_name.strip())


def genitive(city_name: str) -> str:
    """
    Zwraca miasto w dopełniaczu — "ranking Krakowa".
    Nieznane miasto zwraca formę wyjściową.
    """
    if not city_name:
        return ''
    return GENITIVE.get(city_name.strip(), city_name.strip())


def missing_cities(city_names) -> list:
    """
    Diagnostyka: które miasta z bazy nie mają jeszcze odmiany.
    Użyj po dodaniu nowych miast, żeby nie wrócił błąd "w Kraków".
    """
    return [c for c in city_names if c and c.strip() not in LOCATIVE]
