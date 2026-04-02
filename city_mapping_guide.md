# City Mapping Guide - English-Friendly City Names

## 🎯 **PROBLEM SOLVED**

You can now use **English-friendly city names** instead of struggling with Polish characters like "ę", "ł", "ń", "ó", "ś", "ź", "ż" in the terminal.

## 📋 **ENGLISH-FRIENDLY CITY NAMES**

Here are the English-friendly names you can use:

### **Cities with Polish Characters (Use These Instead):**

| Polish Name | English-Friendly Name |
|-------------|----------------------|
| **Warszawa** | `warszawa` |
| **Kraków** | `krakow` |
| **Łódź** | `lodz` |
| **Wrocław** | `wroclaw` |
| **Poznań** | `poznan` |
| **Gdańsk** | `gdansk` |
| **Białystok** | `bialystok` |
| **Częstochowa** | `czestochowa` |
| **Rzeszów** | `rzeszow` |
| **Toruń** | `torun` |
| **Gliwice** | `glowice` |
| **Bielsko-Biała** | `bielsko-biala` |
| **Zielona Góra** | `zielona-gora` |
| **Ruda Śląska** | `ruda-slaska` |
| **Elbląg** | `elblag` |
| **Płock** | `plock` |
| **Wałbrzych** | `walbrzych` |
| **Włocławek** | `wloclawek` |
| **Tarnów** | `tarnow` |
| **Chorzów** | `chorzow` |
| **Grudziądz** | `grudziadz` |
| **Słupsk** | `slupsk` |
| **Jastrzębie-Zdrój** | `jastrzebie-zdroj` |
| **Nowy Sącz** | `nowy-sacz` |
| **Piotrków Trybunalski** | `piotrkow-trybunalski` |
| **Inowrocław** | `inowroclaw` |
| **Ostrów Wielkopolski** | `ostrow-wielkopolski` |
| **Głogów** | `glogow` |
| **Przemyśl** | `przemysl` |
| **Zamość** | `zamosc` |
| **Żory** | `zory` |
| **Chełm** | `chelm` |
| **Tarnowskie Góry** | `tarnowskie-gory` |
| **Ełk** | `elk` |
| **Pruszków** | `pruszkow` |
| **Ostrołęka** | `ostroleka` |
| **Pszczyna** | `pszczyna` |
| **Myszków** | `myszkow` |
| **Koziegłowy** | `kozieglowy` |
| **Czechowice-Dziedzice** | `czechowice-dziedzice` |
| **Żarki** | `zarki` |
| **Jordanów** | `jordanow` |
| **Mysłowice** | `myslowice` |
| **Wieliczka** | `wieliczka` |
| **Oświęcim** | `oswiecim` |

## 🚀 **HOW TO USE**

### **1. Detect City Mixing Issues**
```bash
# Detect all cities
python detect_all_city_mixing.py

# Detect specific city (use English-friendly name)
python detect_all_city_mixing.py --city czestochowa
```

### **2. Fix City Mixing Issues**
```bash
# Fix all cities
python fix_all_city_mixing.py

# Fix specific city (use English-friendly name)
python fix_all_city_mixing.py --city czestochowa

# Fix with high confidence only
python fix_all_city_mixing.py --city czestochowa --confidence high

# Preview fixes without applying
python fix_all_city_mixing.py --city czestochowa --dry-run
```

### **3. Generate Reports**
```bash
# Summary report
python city_mixing_report.py

# City-specific report
python city_mixing_report.py --city czestochowa

# Pattern analysis
python city_mixing_report.py --patterns
```

## 💡 **EXAMPLES**

### **Instead of typing:**
```bash
python fix_all_city_mixing.py --city "Częstochowa"
```

### **You can now type:**
```bash
python fix_all_city_mixing.py --city czestochowa
```

### **Instead of typing:**
```bash
python fix_all_city_mixing.py --city "Żarki"
```

### **You can now type:**
```bash
python fix_all_city_mixing.py --city zarki
```

## 🔧 **AUTOMATIC MAPPING**

The system automatically maps your English-friendly input to the proper Polish names:

- **Input**: `czestochowa` → **Maps to**: `Częstochowa`
- **Input**: `zarki` → **Maps to**: `Żarki`
- **Input**: `krakow` → **Maps to**: `Kraków`

## 📊 **SEE ALL AVAILABLE NAMES**

To see all available English-friendly names:
```bash
python -c "import json; data = json.load(open('city_mapping.json')); print('Available English-friendly names:'); [print(f'{eng:20} → {pol}') for eng, pol in data['city_mapping'].items()]"
```

## 🎉 **BENEFITS**

- ✅ **No Polish characters needed** in terminal
- ✅ **Case-insensitive** (works with `CZESTOCHOWA`, `czestochowa`, `Czestochowa`)
- ✅ **Automatic mapping** to proper Polish names
- ✅ **Works with all 62 cities**
- ✅ **Safe and reliable** - same functionality as before

Now you can easily work with Polish city names without struggling with special characters!
