# Faz 4 - Dar Kapsamli Optimizasyon

Kaynak: `data/processed/clean_v1.csv`  
Uretildi: `python src/optimization/optimize.py`

## Kapsam ve neden bu kadar dar

Faz 3 (K15), karar degiskenlerinin 25 output'un yalnizca **5**'inde
persistence baseline'ini gectigini gosterdi; hicbirinde R2 pozitif degil.
Optimizasyon bu yuzden tum prosese degil, yalnizca **modelin gercekten bir
sey yakaladigi output'lara** ve **gercekten oynatilmis parametrelere**
kuruluyor.

- Hedef output: **5** (S1'de persistence gecilenler)
- Karar degiskeni: **5** aktif CPP (K7: CV >= %1)
- Arama uzayi: her parametre yalnizca **gozlenen min-max araliginda**
  (K1 geregi ekstrapolasyon yok)

| CPP | gozlenen aralik | CV % |
|---|---|---|
| `Machine1.MotorRPM` | 10.39 – 12.24 | 5.74 |
| `Machine1.ExitZoneTemperature` | 69.70 – 80.00 | 2.71 |
| `Machine3.MotorRPM` | 11.96 – 14.00 | 3.28 |
| `Machine4.Pressure` | 14.00 – 25.00 | 5.46 |
| `Machine4.Temperature3` | 268.00 – 327.00 | 1.15 |

## Yontem: iki bagimsiz yol

Model R2'si negatif oldugu icin model-tabanli optimizasyon **tek basina**
dayanak sayilmadi. Ayni soru modele hic guvenmeden de soruldu:

| Yol | Nasil | Guclu yani | Zayif yani |
|---|---|---|---|
| **Model-tabanli** | egitilmis model uzerinde 4.000 aday nokta | parametreleri birlikte degerlendirir | modelin R2'si negatif |
| **Ampirik** | gozlenen veride kantil bolgeleri | gercek olculere dayanir | parametreleri tek tek gorur |

> Ikisi ayni bolgeyi isaret ederse oneri guclenir. Ayrisirsa bu da
> raporlanir ve oneri **zayif** sayilir.

## Model-tabanli optimum noktalar

| output | error_type | skill_vs_pers | mevcut_bias | mevcut_mutlak | model_tahmini | Machine1.MotorRPM | Machine1.ExitZoneTemperature | Machine3.MotorRPM | Machine4.Pressure | Machine4.Temperature3 |
|---|---|---|---|---|---|---|---|---|---|---|
| Stage2.M9 | variability | 0.2553 | 0.1692 | 0.1834 | 0.0003 | 12.02 | 70.52 | 13.71 | 16.13 | 313.01 |
| Stage2.M0 | bias | 0.2253 | 0.8822 | 0.8866 | 0.0046 | 11.95 | 79.12 | 13.29 | 17.26 | 313.19 |
| Stage2.M7 | belirsiz | 0.165 | 0.2537 | 0.2537 | 0.0001 | 11.33 | 72.6 | 13.93 | 16.84 | 314.04 |
| Stage2.M8 | belirsiz | 0.1108 | 0.3315 | 0.4113 | 0.0 | 11.49 | 71.53 | 13.2 | 19.66 | 326.44 |
| Stage2.M10 | variability | 0.1004 | -0.0916 | 0.0947 | 0.0 | 10.73 | 70.87 | 12.57 | 19.15 | 318.63 |

> `mevcut_bias` test blogundaki gerceklesen ortalama sapma;
> `model_tahmini` ise modelin onerilen noktada bekledigi sapma.
> **Bu iki sayi ayni olcegi paylasmiyor** -- biri gozlem, digeri zayif bir
> modelin tahmini. Aralarindaki fark bir "iyilesme yuzdesi" olarak
> okunmamalidir; oyle okumak projenin bastan reddettigi seydir.

## Ampirik kontrol: veride gercekte ne olmus?

Her CPP kantillere bolundu ve o dilimde **gerceklesen** sapma olculdu.
Modele hic guvenilmiyor. En az 200 gozlemi olan dilimler alindi.

### Stage2.M9

| parametre | en iyi dilim | mutlak sapma | en kotu dilim | mutlak sapma | fark |
|---|---|---|---|---|---|
| `Machine1.ExitZoneTemperature` | 69.70 – 75.00 | 0.1666 | 75.10 – 80.00 | 0.4266 | **+0.2600** |
| `Machine1.MotorRPM` | 10.73 – 11.77 | 0.1561 | 11.77 – 12.24 | 0.4124 | **+0.2563** |
| `Machine3.MotorRPM` | 12.97 – 13.35 | 0.1713 | 11.96 – 12.97 | 0.4044 | **+0.2331** |
| `Machine4.Pressure` | 14.00 – 17.00 | 0.1817 | 17.00 – 18.00 | 0.2 | **+0.0183** |
| `Machine4.Temperature3` | 268.00 – 321.00 | 0.155 | 321.00 – 324.00 | 0.2055 | **+0.0505** |

### Stage2.M0

| parametre | en iyi dilim | mutlak sapma | en kotu dilim | mutlak sapma | fark |
|---|---|---|---|---|---|
| `Machine1.ExitZoneTemperature` | 75.00 – 75.10 | 0.7375 | 75.10 – 80.00 | 0.8726 | **+0.1351** |
| `Machine1.MotorRPM` | 10.39 – 10.52 | 0.6713 | 11.77 – 12.24 | 0.8923 | **+0.2210** |
| `Machine3.MotorRPM` | 13.63 – 14.00 | 0.6539 | 11.96 – 12.97 | 0.8797 | **+0.2258** |
| `Machine4.Pressure` | 14.00 – 17.00 | 0.7438 | 18.00 – 25.00 | 0.8547 | **+0.1109** |
| `Machine4.Temperature3` | 268.00 – 321.00 | 0.6245 | 324.00 – 325.00 | 0.8597 | **+0.2352** |

### Stage2.M7

| parametre | en iyi dilim | mutlak sapma | en kotu dilim | mutlak sapma | fark |
|---|---|---|---|---|---|
| `Machine1.ExitZoneTemperature` | 75.10 – 80.00 | 0.2429 | 75.00 – 75.10 | 0.2739 | **+0.0310** |
| `Machine1.MotorRPM` | 11.77 – 12.24 | 0.2528 | 10.73 – 11.77 | 0.2742 | **+0.0214** |
| `Machine3.MotorRPM` | 11.96 – 12.97 | 0.2479 | 12.97 – 13.35 | 0.2737 | **+0.0258** |
| `Machine4.Pressure` | 14.00 – 17.00 | 0.2598 | 17.00 – 18.00 | 0.2698 | **+0.0100** |
| `Machine4.Temperature3` | 321.00 – 324.00 | 0.2486 | 268.00 – 321.00 | 0.2875 | **+0.0389** |

### Stage2.M8

| parametre | en iyi dilim | mutlak sapma | en kotu dilim | mutlak sapma | fark |
|---|---|---|---|---|---|
| `Machine1.ExitZoneTemperature` | 75.10 – 80.00 | 0.3859 | 75.00 – 75.10 | 0.4186 | **+0.0327** |
| `Machine1.MotorRPM` | 10.39 – 10.52 | 0.3608 | 10.73 – 11.77 | 0.4795 | **+0.1187** |
| `Machine3.MotorRPM` | 13.63 – 14.00 | 0.3789 | 12.97 – 13.35 | 0.4656 | **+0.0867** |
| `Machine4.Pressure` | 14.00 – 17.00 | 0.4011 | 17.00 – 18.00 | 0.4296 | **+0.0285** |
| `Machine4.Temperature3` | 321.00 – 324.00 | 0.3698 | 324.00 – 325.00 | 0.4482 | **+0.0784** |

### Stage2.M10

| parametre | en iyi dilim | mutlak sapma | en kotu dilim | mutlak sapma | fark |
|---|---|---|---|---|---|
| `Machine1.ExitZoneTemperature` | 69.70 – 75.00 | 0.0558 | 75.10 – 80.00 | 0.098 | **+0.0422** |
| `Machine1.MotorRPM` | 10.52 – 10.73 | 0.0524 | 11.77 – 12.24 | 0.0934 | **+0.0410** |
| `Machine3.MotorRPM` | 13.35 – 13.63 | 0.0569 | 11.96 – 12.97 | 0.0957 | **+0.0388** |
| `Machine4.Pressure` | 14.00 – 17.00 | 0.0668 | 18.00 – 25.00 | 0.0856 | **+0.0188** |
| `Machine4.Temperature3` | 321.00 – 324.00 | 0.0473 | 325.00 – 327.00 | 0.0956 | **+0.0483** |

## Iki yol uzlasiyor mu?

Faz 4'un asil ciktisi bu tablo. Model-tabanli aramanin onerdigi deger,
ampirik olarak **en iyi cikan dilimin icinde** mi?

| output | parametre | model onerisi | ampirik en iyi dilim | uzlasma |
|---|---|---|---|---|
| Stage2.M9 | `Machine1.ExitZoneTemperature` | 70.52 | 69.70 – 75.00 | EVET |
| Stage2.M9 | `Machine1.MotorRPM` | 12.02 | 10.73 – 11.77 | hayir |
| Stage2.M9 | `Machine3.MotorRPM` | 13.71 | 12.97 – 13.35 | hayir |
| Stage2.M9 | `Machine4.Pressure` | 16.13 | 14.00 – 17.00 | EVET |
| Stage2.M9 | `Machine4.Temperature3` | 313.01 | 268.00 – 321.00 | EVET |
| Stage2.M0 | `Machine1.ExitZoneTemperature` | 79.12 | 75.00 – 75.10 | hayir |
| Stage2.M0 | `Machine1.MotorRPM` | 11.95 | 10.39 – 10.52 | hayir |
| Stage2.M0 | `Machine3.MotorRPM` | 13.29 | 13.63 – 14.00 | hayir |
| Stage2.M0 | `Machine4.Pressure` | 17.26 | 14.00 – 17.00 | hayir |
| Stage2.M0 | `Machine4.Temperature3` | 313.19 | 268.00 – 321.00 | EVET |
| Stage2.M7 | `Machine1.ExitZoneTemperature` | 72.6 | 75.10 – 80.00 | hayir |
| Stage2.M7 | `Machine1.MotorRPM` | 11.33 | 11.77 – 12.24 | hayir |
| Stage2.M7 | `Machine3.MotorRPM` | 13.93 | 11.96 – 12.97 | hayir |
| Stage2.M7 | `Machine4.Pressure` | 16.84 | 14.00 – 17.00 | EVET |
| Stage2.M7 | `Machine4.Temperature3` | 314.04 | 321.00 – 324.00 | hayir |
| Stage2.M8 | `Machine1.ExitZoneTemperature` | 71.53 | 75.10 – 80.00 | hayir |
| Stage2.M8 | `Machine1.MotorRPM` | 11.49 | 10.39 – 10.52 | hayir |
| Stage2.M8 | `Machine3.MotorRPM` | 13.2 | 13.63 – 14.00 | hayir |
| Stage2.M8 | `Machine4.Pressure` | 19.66 | 14.00 – 17.00 | hayir |
| Stage2.M8 | `Machine4.Temperature3` | 326.44 | 321.00 – 324.00 | hayir |
| Stage2.M10 | `Machine1.ExitZoneTemperature` | 70.87 | 69.70 – 75.00 | EVET |
| Stage2.M10 | `Machine1.MotorRPM` | 10.73 | 10.52 – 10.73 | EVET |
| Stage2.M10 | `Machine3.MotorRPM` | 12.57 | 13.35 – 13.63 | hayir |
| Stage2.M10 | `Machine4.Pressure` | 19.15 | 14.00 – 17.00 | hayir |
| Stage2.M10 | `Machine4.Temperature3` | 318.63 | 321.00 – 324.00 | hayir |

> **BULGU O1 - 7 / 25 durumda (%28) iki yol ayni
> bolgeyi isaret ediyor.** Model ve ham gozlem birbirinden bagimsiz
> yontemler; ayni yere isaret ettikleri parametreler icin oneri
> **desteklenmis** sayilir.
>
> Uzlasmayan satirlar oneri listesinden **cikarilmadi, isaretlendi.**
> Bir modelin R2'si negatifken onun onerisini ampirik kanita ragmen
> savunmak, projenin bastan reddettigi seydir. Uzlasmayan yerlerde
> **ampirik bulgu esas alinir.**

### Ampirik olarak en guclu bulgular

Modele hic guvenmeden, yalnizca gozlenen veriden:

| output | parametre | iyi dilim | mutlak sapma | kotu dilim | mutlak sapma | kat fark |
|---|---|---|---|---|---|---|
| Stage2.M9 | `Machine1.MotorRPM` | 10.73 – 11.77 | 0.1561 | 11.77 – 12.24 | 0.4124 | **2.64x** |
| Stage2.M9 | `Machine1.ExitZoneTemperature` | 69.70 – 75.00 | 0.1666 | 75.10 – 80.00 | 0.4266 | **2.56x** |
| Stage2.M9 | `Machine3.MotorRPM` | 12.97 – 13.35 | 0.1713 | 11.96 – 12.97 | 0.4044 | **2.36x** |
| Stage2.M10 | `Machine4.Temperature3` | 321.00 – 324.00 | 0.0473 | 325.00 – 327.00 | 0.0956 | **2.02x** |
| Stage2.M10 | `Machine1.MotorRPM` | 10.52 – 10.73 | 0.0524 | 11.77 – 12.24 | 0.0934 | **1.78x** |
| Stage2.M10 | `Machine1.ExitZoneTemperature` | 69.70 – 75.00 | 0.0558 | 75.10 – 80.00 | 0.098 | **1.76x** |
| Stage2.M10 | `Machine3.MotorRPM` | 13.35 – 13.63 | 0.0569 | 11.96 – 12.97 | 0.0957 | **1.68x** |
| Stage2.M0 | `Machine4.Temperature3` | 268.00 – 321.00 | 0.6245 | 324.00 – 325.00 | 0.8597 | **1.38x** |

> **BULGU O2 - En guclu ampirik bulgu: `Machine1.MotorRPM` / Stage2.M9.** Iyi dilimde mutlak
> sapma 0.1561, kotu dilimde 0.4124 -- **2.64 kat** fark.
>
> **Bu bir nedensellik iddiasi DEGILDIR.** Gozlemsel veriden geliyor;
> parametre ile output arasinda ucuncu bir degisken araciligi
> olabilir. Dogru okuma su: *bu bolgede calisildiginda gecmiste daha
> iyi sonuc alinmis.* Nedenselligi dogrulamanin tek yolu kontrollu
> deneydir (DOE) -- Faz 5'te oneri olarak yer alacak.

### Output'lar arasi tutarlilik

Tek bir output'ta bulunan bir bolge rastlanti olabilir. Ama **farkli
output'lar ayni parametre icin ayni bolgeyi isaret ediyorsa**, bu
rastlanti olma ihtimalini ciddi sekilde azaltir. Ampirik en iyi
dilimlerin orta noktalari:

| parametre | Stage2.M0 | Stage2.M10 | Stage2.M7 | Stage2.M8 | Stage2.M9 | yayilim |
|---|---|---|---|---|---|---|
| `Machine1.ExitZoneTemperature` | 75.00 – 75.10 | 69.70 – 75.00 | 75.10 – 80.00 | 75.10 – 80.00 | 69.70 – 75.00 | dagilmis |
| `Machine1.MotorRPM` | 10.39 – 10.52 | 10.52 – 10.73 | 11.77 – 12.24 | 10.39 – 10.52 | 10.73 – 11.77 | dagilmis |
| `Machine3.MotorRPM` | 13.63 – 14.00 | 13.35 – 13.63 | 11.96 – 12.97 | 13.63 – 14.00 | 12.97 – 13.35 | dagilmis |
| `Machine4.Pressure` | 14.00 – 17.00 | 14.00 – 17.00 | 14.00 – 17.00 | 14.00 – 17.00 | 14.00 – 17.00 | **tutarli** |
| `Machine4.Temperature3` | 268.00 – 321.00 | 321.00 – 324.00 | 321.00 – 324.00 | 321.00 – 324.00 | 268.00 – 321.00 | dagilmis |

> **BULGU O3 - Su parametrelerde output'lar birbirini dogruluyor:** `Machine4.Pressure`.
> Farkli olcumler bagimsiz olarak ayni calisma bolgesini isaret
> ediyor.

#### Ne kadar guclu bir bulgu?

"Hepsi ayni dilimi secti" tek basina yeterli degil: dilimler esit
buyuklukte olmayabilir ve etki kucuk olabilir. Her ikisi de kontrol
edildi.

**`Machine4.Pressure`** — istenen 4 dilim, olusan **3** (bagli degerler nedeniyle). Dilim paylari: %65.5, %26.4, %8.1.

| output | en iyi dilim | mutlak sapma | digerlerinin en iyisi | goreli fark |
|---|---|---|---|---|
| Stage2.M0 | (13.999, 17.0] | 0.7438 | 0.8363 | **+%12.4** |
| Stage2.M10 | (13.999, 17.0] | 0.0668 | 0.0840 | **+%25.8** |
| Stage2.M7 | (13.999, 17.0] | 0.2598 | 0.2643 | **+%1.7** |
| Stage2.M8 | (13.999, 17.0] | 0.4011 | 0.4271 | **+%6.5** |
| Stage2.M9 | (13.999, 17.0] | 0.1817 | 0.1889 | **+%4.0** |

> 5 output'un **5'i de ayni dilimi** en iyi
> buluyor. Output'lar bagimsiz olsaydi bunun sans eseri olma
> olasiligi `0.5^5` = **%3.1**.
>
> **Ama bu isaret testinin varsayimi burada tam saglanmiyor:**
> ayni hattin ayni anindaki olcumleri tamamen bagimsiz degil.
> Yani gercek olasilik %3.1'den yuksek. Yon tutarliligi bir isarettir,
> kanit degil.
>
> **Etki buyuklugu kucuk** (yukaridaki goreli fark sutunu) ve
> en iyi dilim gozlemlerin buyuk cogunlugunu iceriyor -- yani
> "iyi bolge" aslinda prosesin zaten calistigi yer.
> Pratik okuma: **mevcut calisma bolgesinden cikmamak**,
> yeni bir optimum kesfetmek degil.

## A1 duyarlilik analizi

K9: `.C.` / `.U.` ekinin anlami dogrulanamadi. A1 yanlissa karar
degiskeni seti degisir. Sonucun bu varsayima ne kadar bagli oldugu:

**Stage2.M9**

| varyant | ozellik sayisi | R2 | skill vs persistence |
|---|---|---|---|
| dar (yalnizca aktif CPP) | 5 | -0.0351 | 0.2479 |
| genis (tum controlled) | 24 | -0.0149 | 0.2553 |
| A1 yanlissa (measured dahil) | 21 | -0.0425 | 0.2452 |

**Stage2.M0**

| varyant | ozellik sayisi | R2 | skill vs persistence |
|---|---|---|---|
| dar (yalnizca aktif CPP) | 5 | -0.0516 | 0.2234 |
| genis (tum controlled) | 24 | -0.0466 | 0.2253 |
| A1 yanlissa (measured dahil) | 21 | -0.3799 | 0.1104 |

**Stage2.M7**

| varyant | ozellik sayisi | R2 | skill vs persistence |
|---|---|---|---|
| dar (yalnizca aktif CPP) | 5 | -0.1451 | 0.1375 |
| genis (tum controlled) | 24 | -0.0732 | 0.165 |
| A1 yanlissa (measured dahil) | 21 | -2.3141 | -0.4673 |

**Stage2.M8**

| varyant | ozellik sayisi | R2 | skill vs persistence |
|---|---|---|---|
| dar (yalnizca aktif CPP) | 5 | -0.2452 | 0.0199 |
| genis (tum controlled) | 24 | -0.0248 | 0.1108 |
| A1 yanlissa (measured dahil) | 21 | -1.349 | -0.3462 |

**Stage2.M10**

| varyant | ozellik sayisi | R2 | skill vs persistence |
|---|---|---|---|
| dar (yalnizca aktif CPP) | 5 | -1.5424 | -0.3579 |
| genis (tum controlled) | 24 | -0.1158 | 0.1004 |
| A1 yanlissa (measured dahil) | 21 | -3.9881 | -0.902 |

> **BULGU O4 - `measured` degiskenleri eklemek modeli 5/5 output'ta KOTULESTIRIYOR.**
> A1 yanlis olsaydi -- yani `.U.` kolonlar da ayarlanabilir olsaydi --
> onlari eklemek tahmin gucunu artirmaliydi. Tersi oluyor.
>
> Bu, A1'i **kanitlamaz**; o kolonlarin tahmin gucu katmadigini
> gosterir. Ama pratik sonuc ayni: karar degiskeni setini `.C.`
> kolonlarla sinirlamak, veriye gore savunulabilir bir tercih.
> **K9 riski dusuruldu, kapatilmadi.**

> **BULGU O5 - 5 CPP'ye daralmak bazi output'lara zarar veriyor.**
>   - `Stage2.M10`: dar set -0.358 vs genis set +0.100
>   - `Stage2.M8`: dar set +0.020 vs genis set +0.111
> Bu output'lar icin 5 aktif CPP yetersiz; tahmin gucu diger
> `controlled` kolonlardan geliyor. Optimizasyon onerisi bu
> output'lar icin **gecerli sayilmamali** -- dar set uzerinde
> kurulan arama, modelin zaten beceremedigi bir uzayda yapiliyor.

## Faz 4 sonucu

| Ne soruldu | Cevap |
|---|---|
| Kac output icin optimizasyon kurulabildi? | 5 / 25 |
| Model ve ampirik yol uzlasti mi? | 7/25 durumda (%28) |
| Output'lar arasi tutarli parametre | `Machine4.Pressure` |
| A1 varsayimina duyarlilik | dusuk (BULGU O4) |

**Dürüst ozet:** Bu veriden "su parametreleri su degerlere cekin, sapma
su kadar azalir" turu bir oneri **cikmiyor.** Cikan sey daha mutevazi ama
gercek:

1. Proses zaten iyi calistigi bolgede duruyor; `Machine4.Pressure` icin
   5 output'un 5'i de mevcut ana calisma araligini (14–17) en iyi buluyor.
   Bu bir **kesif** degil, mevcut ayarin **dogrulanmasi**dir.
2. Etki buyuklukleri kucuk (%2–26) ve gozlemsel; nedensellik iddia edilemez.
3. Asil kisit veri: 4 saatlik pencerede karar degiskenleri yeterince
   oynatilmamis (K7), dolayisiyla optimizasyonun ogrenecegi kontrast yok.

> **Faz 5'e devredilen:** Bu sonucun kendisi bir bulgudur. Optimizasyonun
> onunu acacak sey daha iyi model degil, **daha iyi veri**: kontrollu bir
> deney (DOE) ile parametreleri bilincli olarak genis araliklarda oynatmak.
> Faz 5 bunu somut bir veri toplama onerisine cevirecek.
