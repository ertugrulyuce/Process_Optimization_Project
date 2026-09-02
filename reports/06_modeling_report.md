# Faz 3 - Tahmin Modelleri ve Root Cause

Kaynak: `data/processed/clean_v1.csv`  
Uretildi: `python src/modeling/train.py`

## Yontem: iki ayri soru

| Soru | Girdi seti | Ne icin |
|---|---|---|
| **S1** Karar degiskenleri deviation'i acikliyor mu? | `controlled` (24 kolon) | Optimizasyonun dayanagi |
| **S1+** Proses tepkileri eklenince? | `ctrl+measured` (40 kolon) | Aciklama ust siniri |
| **S2** Deviation tahmin edilebilir mi? | `ctrl+lag` (+ gecmis degerler) | Erken uyari / izleme |

Bu ayrim sart: gecmis degerlerle yuksek R2 elde edip "prosesi anladik"
sanmak bu veri setindeki en kolay tuzak. S2'nin basarisi S1'in yerine gecmez.

## Split stratejisi ve sizinti

Embargo **49 satir** olarak secildi -- keyfi degil, karar
degiskenlerinin otokorelasyonunun 0.2 altina indigi mesafenin medyani.

Ayni model (`RandomForest`), ayni veri (`Stage1.M4.dev`), yalnizca bolme yontemi degisiyor:

| Bolme yontemi | R2 | RMSE |
|---|---|---|
| Rastgele split (**YANLIS**) | 0.9715 | 0.1784 |
| Bloklu split, embargo yok | -6.3574 | 0.6459 |
| Bloklu split + embargo (49) | -6.8931 | 0.6690 |
| *baseline:* persistence | 0.8464 | 0.0933 |

> **BULGU M1 - Rastgele split %97'lik sahte bir basari uretiyor.**
> Ayni model dogru bolmede R2 = -6.89 veriyor, yani
> sabit ortalama tahminden bile kotu. Aradaki fark modelin degil,
> **degerlendirme yonteminin** sonucu: rastgele bolmede test satirinin
> komsulari train'de kaliyor ve model tahmin degil hatirlama yapiyor.
>
> Bu, ayni veri setiyle yapilan calismalarda en yaygin hatadir ve
> literaturde yuksek R2 bildiren sonuclarin bir kismini aciklar.

> **BULGU M2 - Persistence baseline R2 = 0.8464.**
> "Onceki degeri tekrarla" tahmini, hicbir sey ogrenmeden bu skoru
> aliyor. Bir modelin bu esigi gecemedigi her durumda, ham R2 ne olursa
> olsun, model prosese dair bilgi tasimıyor demektir. Bu yuzden asagida
> **beceri skoru** raporlaniyor:
>
> `skill = 1 - RMSE_model / RMSE_baseline`  (0 = baseline kadar, <0 = daha kotu)

## S1 - Karar degiskenleri deviation'i acikliyor mu?

### Once bir okuma notu: R2 neden negatif, skill neden pozitif?

Asagidaki tabloda `r2 = -2.04` ile `skill_vs_mean = +0.79` yan yana
gorunuyor. Celiski degil; iki olcut **farkli referans** kullaniyor:

- `R2`, test blogunun **kendi ortalamasini** referans alir. Ama o ortalama
  gercek hayatta bilinmez -- gelecegi bilmek demektir.
- `skill_vs_mean`, **train ortalamasini** referans alir. Modeli kurarken
  elde olan tek bilgi budur; gercekci olan bu.

> **BULGU M2b - Ikisi arasindaki fark dagilim kaymasinin olcusudur.**
> Neredeyse tum output'larda R2 negatif ama skill pozitif olmasi, test
> blogundaki deviation dagiliminin train'den **kaydigini** gosterir.
> Proses 4 saatlik pencere icinde bile sabit kalmiyor (K1 ile tutarli).
> Pratik sonucu: train doneminde kalibre edilen bir model, birkac saat
> sonra merkezi kaymis tahminler uretir -- Faz 5'te bu, yeniden kalibrasyon
> ihtiyaci olarak raporlanacak.

Her output icin en iyi modelin skorlari (25 output):

- Sabit ortalamayi geceni: **13 / 25**
- Persistence'i geceni: **5 / 25**

| output | error_type | model | r2 | skill_vs_mean | skill_vs_pers |
|---|---|---|---|---|---|
| Stage1.M13 | variability | hgb | -2.0394 | 0.7887 | -1.6977 |
| Stage1.M12 | bias | rf | -0.3379 | 0.6251 | -0.6068 |
| Stage1.M4 | variability | hgb | -5.5327 | 0.5716 | -5.5206 |
| Stage2.M5 | variability | ridge | -0.4995 | 0.568 | -0.0134 |
| Stage1.M10 | bias | ridge | -0.2011 | 0.5625 | -1.8063 |
| Stage2.M13 | bias | hgb | -0.8557 | 0.5249 | -0.4457 |
| Stage2.M10 | variability | hgb | -0.1158 | 0.36 | 0.1004 |
| Stage2.M14 | bias | hgb | -0.1146 | 0.3394 | -0.0606 |
| Stage2.M11 | variability | hgb | -3.9576 | 0.3311 | -0.9146 |
| Stage2.M3 | variability | ridge | -3.5987 | 0.2757 | -3.1176 |
| Stage2.M0 | bias | hgb | -0.0466 | 0.2436 | 0.2253 |
| Stage2.M2 | variability | rf | -0.7601 | 0.1131 | -0.4194 |
| Stage2.M12 | variability | hgb | -0.626 | 0.0533 | -0.2065 |
| Stage2.M9 | variability | hgb | -0.0149 | -0.0008 | 0.2553 |
| Stage2.M8 | belirsiz | rf | -0.0248 | -0.0123 | 0.1108 |
| Stage2.M7 | belirsiz | hgb | -0.0732 | -0.0154 | 0.165 |
| Stage1.M1 | bias | rf | -0.1091 | -0.0229 | -1.4183 |
| Stage1.M6 | bias | rf | -0.4644 | -0.1085 | -0.5751 |
| Stage1.M14 | bias | hgb | -0.6905 | -0.1884 | -0.0788 |
| Stage1.M3 | bias | ridge | -0.932 | -0.3746 | -0.8854 |
| Stage2.M1 | bias | rf | -3.1136 | -0.4802 | -2.5722 |
| Stage1.M9 | bias | ridge | -1.8451 | -0.6508 | -2.1943 |
| Stage1.M8 | bias | rf | -2.4563 | -0.7524 | -2.1152 |
| Stage1.M2 | bias | rf | -7.9463 | -1.8739 | -3.17 |
| Stage1.M0 | bias | ridge | -21.0862 | -2.3653 | -10.4051 |

> **BULGU M3 - Optimizasyon hedefi output'lar icin durum.** 9 variability-baskin output'un **8**'inde karar degiskenleri sabit
> ortalamadan iyi tahmin veriyor; persistence'i gecen **2** tane.
> Faz 2'nin dogrusal korelasyonla bulamadigi guclu surukleyiciyi (K12)
> dogrusal olmayan modeller de bulamadiysa, bu artik yontem sorunu degil
> **verinin soyledigi sey** olarak kabul edilir.

## Girdi setleri karsilastirmasi

Her sette output basina en iyi model secilip medyani alindi:

| girdi seti | medyan R2 | medyan skill vs ortalama | medyan skill vs persistence |
|---|---|---|---|
| `controlled` | -0.6905 | +0.0533 | -0.6068 |
| `ctrl+measured` | -0.7832 | +0.0361 | -0.7735 |
| `ctrl+lag` | 0.4340 | +0.4466 | +0.0425 |

> **BULGU M4 - S2 (izleme sorusu) ile S1 (optimizasyon sorusu) ayrisiyor.**
> Gecmis degerler girdiye eklendiginde 17 / 25 output'ta
> model persistence'i geciyor. Bu, **izleme icin** degerli bir sonuc:
> deviation kisa vadede tahmin edilebiliyor.
>
> Ama bu tahmin gucu **optimizasyona cevrilemez** -- 'deviation'in bir
> sonraki degeri onceki degerine benziyor' bilgisi hangi parametrenin
> degistirilecegini soylemez. S1'in cevabi neyse Faz 4 ona dayanir.

## Critical Process Parameters (CPP)

Permutation importance, yalnizca `controlled` girdi seti uzerinde
(S1 sorusu) ve **test blogunda** hesaplandi -- train uzerinde
hesaplanan onem degerleri ezberi olcer, genellemeyi degil.

**Onem degerleri yalnizca modelin gercekten tahmin gucu oldugu
output'lardan toplandi.** Skill skoru negatif olan bir output'ta
"onem siralamasi", gurultunun siralamasidir.

Guvenilen output sayisi: **13 / 25** (skill vs ortalama > 0).

| parametre | toplam onem | ortalama | output sayisi | CV % | durum |
|---|---|---|---|---|---|
| `Machine5.Temperature6` | 1.6403 | 0.2343 | 7 | 0.63 | PASIF |
| `Machine5.Temperature4` | 1.1792 | 0.1965 | 6 | 0.66 | PASIF |
| `Machine4.Temperature3` | 0.4040 | 0.0449 | 9 | 1.15 | aktif |
| `Machine1.ExitZoneTemperature` | 0.3385 | 0.0484 | 7 | 2.71 | aktif |
| `Machine1.Zone2Temperature` | 0.1531 | 0.0255 | 6 | 0.56 | PASIF |
| `Combiner.Temperature3` | 0.0719 | 0.0180 | 4 | 0.15 | PASIF |
| `Machine1.MotorRPM` | 0.0564 | 0.0188 | 3 | 5.74 | aktif |
| `Machine2.Zone1Temperature` | 0.0461 | 0.0058 | 8 | 0.08 | PASIF |
| `Machine4.Temperature5` | 0.0391 | 0.0078 | 5 | 0.92 | PASIF |
| `Machine3.MotorRPM` | 0.0377 | 0.0094 | 4 | 3.28 | aktif |
| `Machine4.Temperature2` | 0.0281 | 0.0031 | 9 | 0.82 | PASIF |
| `Machine5.Temperature2` | 0.0195 | 0.0033 | 6 | 0.02 | PASIF |

> **BULGU M5 - Onem siralamasinin ust siralari pasif degiskenlerle dolu.**
> `Machine5.Temperature6` (CV %0.63), `Machine5.Temperature4` (CV %0.66), `Machine1.Zone2Temperature` (CV %0.56) gibi parametreler yuksek onem aliyor ama 4 saatlik pencerede
> pratikte hic oynatilmamislar (K7).
>
> Bir degisken neredeyse sabitken modelin ona onem atfetmesi genellikle
> **zaman vekilligi**dir: degisken yavasca surukleniyor ve model onun
> uzerinden zaman trendini yakaliyor. Bu nedensel bir etki degildir ve
> **o parametreyi degistirmenin output'u degistirecegi anlamina gelmez.**
>
> Bu yuzden CPP adaylari yalnizca **aktif** degiskenler arasindan secilir:
>   - `Machine4.Temperature3` (CV %1.15, 9 output'ta)
>   - `Machine1.ExitZoneTemperature` (CV %2.71, 7 output'ta)
>   - `Machine1.MotorRPM` (CV %5.74, 3 output'ta)
>   - `Machine3.MotorRPM` (CV %3.28, 4 output'ta)
>   - `Machine4.Pressure` (CV %5.46, 2 output'ta)

## Faz 3 sonucu

| Soru | Cevap |
|---|---|
| S1 - Karar degiskenleri aciklıyor mu? | 13/25 output'ta ortalamadan iyi, 5/25 output'ta persistence'tan iyi |
| S2 - Deviation tahmin edilebilir mi? | 17/25 output'ta persistence gecildi |
| Sizinti kontrolu | Rastgele split R2 0.97 -> dogru split -6.89 |

**Faz 4'e etkisi:** Optimizasyon yalnizca S1'in olumlu cevap verdigi
output'lar icin kurulabilir. S1 zayif kaldigi olcude, Faz 4'un cikti
iddiasi da o kadar dar tutulacak: veri neyi destekliyorsa o kadari
onerilecek, daha fazlasi degil.
