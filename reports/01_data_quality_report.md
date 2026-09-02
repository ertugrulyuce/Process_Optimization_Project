# Faz 1 - Data Quality Report

Kaynak: `data/raw/continuous_factory_process.csv`  
Uretildi: `python src/data_processing/audit.py`

## 1. Sema

- Boyut: **14,088 satir x 116 kolon**
- Eksik deger (NaN): **0**
- Tam duplicate satir: **0**
- Veri tipleri: {dtype('float64'): 108, dtype('int64'): 7, dtype('<M8[ns]'): 1}

Degisken rolleri (bkz. `src/data_processing/schema.py`, VARSAYIM A1):

| role | adet |
|---|---|
| ambient | 2 |
| controlled | 25 |
| measured | 16 |
| output_actual | 30 |
| output_setpoint | 30 |
| raw_material | 12 |
| time | 1 |

## 2. Zaman ekseni

- Aralik: **2019-03-06 10:52:33 -> 2019-03-06 14:47:20**
- Toplam sure: **0 days 03:54:47** (~3.9 saat)
- Ornekleme: 1 Hz. Adim dagilimi (sn): {1.0: 14059, 0.0: 14, 2.0: 14}
- Monotonik artan: True
- **Duplicate timestamp: 14**
- 60 sn'den buyuk bosluk: 0

> **BULGU Z1 - Veri tek bir ~4 saatlik pencereden geliyor.** 14.088 satir
> cok gorunuyor ama bagimsiz gozlem sayisi degil. Long-term process
> capability, vardiya/rejim karsilastirmasi ve gun-ici trend analizi bu
> veriyle YAPILAMAZ. Faz 2 short-term capability ile sinirlidir.

## 3. Sabit ve dusuk-kardinaliteli kolonlar

- Tek degerli (sifir varyans): **15 kolon** - tamami Stage2 setpoint'leri
- Iki degerli: **19 kolon**
- Kardinalitesi 10 altinda olan digerleri: {'Machine1.RawMaterial.Property1': 4, 'Machine1.RawMaterial.Property2': 4, 'Machine1.RawMaterial.Property3': 5, 'Machine1.RawMaterial.Property4': 4, 'Machine3.RawMaterial.Property1': 3, 'Machine3.RawMaterial.Property2': 3, 'Machine3.RawMaterial.Property3': 3, 'Machine3.RawMaterial.Property4': 3}

> **BULGU S1 - Setpoint'ler degisken degil, sabit hedeftir.** Stage2'nin
> 15 setpoint'i tek deger; Stage1'inkiler sabit + durus blogunda 0.
> Sonuc: setpoint bir MODEL GIRDISI olarak kullanilamaz (sifir bilgi).
> Tek rolu, deviation KPI'sinin referans noktasi olmaktir.

> **BULGU S2 - Hammadde ozellikleri neredeyse sabit.** Machine2'nin 4
> Property'si 2, Machine3'unkiler 3 farkli deger aliyor. Hammadde
> varyasyonu bu veri setinde zayif bir aciklayici degiskendir.

## 4. Output olcum kalitesi

| output | setpoint | sp_unique | zero_pct | zero_runs | neg_count | valid_pct | nz_mean | nz_std | cv_pct | bias_pct | modelable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Stage1.M0 | 13.75 | 2 | 0.5 | 5 | 0 | 99.5 | 12.961 | 0.2058 | 1.6 | -5.7 | evet |
| Stage1.M1 | 22.74 | 2 | 41.9 | 124 | 5 | 58.1 | 13.851 | 1.2893 | 9.3 | -39.1 | evet |
| Stage1.M2 | 13.02 | 2 | 0.6 | 10 | 1 | 99.4 | 11.426 | 0.5721 | 5.0 | -12.2 | evet |
| Stage1.M3 | 21.88 | 2 | 1.0 | 11 | 0 | 99.0 | 21.532 | 0.2322 | 1.1 | -1.6 | evet |
| Stage1.M4 | 32.55 | 2 | 1.2 | 51 | 2 | 98.8 | 33.288 | 1.2151 | 3.7 | 2.3 | evet |
| Stage1.M5 | 2.74 | 2 | 95.1 | 314 | 19 | 4.9 | 2.544 | 0.7087 | 27.9 | -7.2 | HAYIR |
| Stage1.M6 | 4.25 | 2 | 33.4 | 638 | 10 | 66.6 | 2.008 | 0.7677 | 38.2 | -52.8 | evet |
| Stage1.M7 | 2.97 | 2 | 62.2 | 39 | 6 | 37.8 | 2.91 | 0.1404 | 4.8 | -2.0 | HAYIR |
| Stage1.M8 | 21.3 | 2 | 5.5 | 23 | 2 | 94.5 | 20.907 | 0.3727 | 1.8 | -1.8 | evet |
| Stage1.M9 | 19.52 | 2 | 5.1 | 21 | 3 | 94.9 | 18.936 | 0.4361 | 2.3 | -3.0 | evet |
| Stage1.M10 | 8.65 | 2 | 1.9 | 54 | 1 | 98.1 | 7.831 | 0.1858 | 2.4 | -9.5 | evet |
| Stage1.M11 | 6.16 | 2 | 74.3 | 68 | 9 | 25.7 | 5.8 | 0.3732 | 6.4 | -5.8 | HAYIR |
| Stage1.M12 | 2.02 | 2 | 22.6 | 185 | 7 | 77.4 | 1.555 | 0.1493 | 9.6 | -23.0 | evet |
| Stage1.M13 | 3.16 | 2 | 2.4 | 46 | 2 | 97.6 | 2.953 | 0.8345 | 28.3 | -6.6 | evet |
| Stage1.M14 | 17.72 | 2 | 35.5 | 673 | 11 | 64.5 | 15.418 | 0.9252 | 6.0 | -13.0 | evet |
| Stage2.M0 | 12.05 | 1 | 8.7 | 367 | 1 | 91.3 | 12.808 | 0.3193 | 2.5 | 6.3 | evet |
| Stage2.M1 | 11.71 | 1 | 4.8 | 243 | 3 | 95.2 | 6.577 | 0.798 | 12.1 | -43.8 | evet |
| Stage2.M2 | 11.0 | 1 | 4.3 | 111 | 2 | 95.7 | 10.71 | 0.8142 | 7.6 | -2.6 | evet |
| Stage2.M3 | 20.73 | 1 | 5.5 | 51 | 2 | 94.5 | 20.423 | 0.645 | 3.2 | -1.5 | evet |
| Stage2.M4 | 31.36 | 1 | 90.5 | 203 | 15 | 9.5 | 30.928 | 4.6471 | 15.0 | -1.4 | HAYIR |
| Stage2.M5 | 2.71 | 1 | 1.3 | 15 | 2 | 98.7 | 2.781 | 0.227 | 8.2 | 2.6 | evet |
| Stage2.M6 | 0.01 | 1 | 1.3 | 15 | 1 | 98.7 | 0.539 | 0.1965 | 36.5 | 5290.0 | evet |
| Stage2.M7 | 2.75 | 1 | 2.5 | 80 | 1 | 97.5 | 2.986 | 0.2366 | 7.9 | 8.6 | evet |
| Stage2.M8 | 19.39 | 1 | 6.9 | 194 | 2 | 93.1 | 19.716 | 0.5186 | 2.6 | 1.7 | evet |
| Stage2.M9 | 16.47 | 1 | 29.8 | 276 | 7 | 70.2 | 16.589 | 0.6713 | 4.0 | 0.7 | evet |
| Stage2.M10 | 7.93 | 1 | 4.5 | 48 | 2 | 95.5 | 7.892 | 0.1707 | 2.2 | -0.5 | evet |
| Stage2.M11 | 5.65 | 1 | 4.5 | 48 | 2 | 95.5 | 5.669 | 0.1741 | 3.1 | 0.3 | evet |
| Stage2.M12 | 1.85 | 1 | 1.8 | 38 | 2 | 98.2 | 2.009 | 0.3189 | 15.9 | 8.6 | evet |
| Stage2.M13 | 2.89 | 1 | 1.4 | 13 | 2 | 98.6 | 3.584 | 0.2335 | 6.5 | 24.0 | evet |
| Stage2.M14 | 11.71 | 1 | 6.5 | 243 | 4 | 93.5 | 8.036 | 0.6771 | 8.4 | -31.4 | evet |

> **BULGU O1 - Sifirlar eksik veridir, olcum degil.** Sifirlar bitisik tek
> bir durus blogunda degil, yuzlerce kisa kesinti halinde dagilmis
> (ornegin Stage1.M14: 673 ayri kesinti). Setpoint'i 2.74 olan bir
> boyutun %95 oraninda tam 0 olmasi fiziksel degil, sensor dropout'tur.
> Bu degerler NaN'a cevrilmeli, sifir olarak modele girmemelidir.

> **BULGU O2 - 4 output modellenemez** (gecerli veri < %50): Stage1.M5, Stage1.M7, Stage1.M11, Stage2.M4. Kapsam disi birakilir.

> **BULGU O3 - Negatif olcumler var.** Boyutsal olcum negatif olamaz;
> impossible value olarak isaretlenmelidir.

> **BULGU O4 - Bazi output'lar setpoint'ten sistematik sapiyor** (bias):
>   - `Stage2.M6`: hedef 0.01, gerceklesen ort. 0.539 (**+5290.0%**)
>   - `Stage1.M6`: hedef 4.25, gerceklesen ort. 2.008 (**-52.8%**)
>   - `Stage2.M1`: hedef 11.71, gerceklesen ort. 6.577 (**-43.8%**)
>   - `Stage1.M1`: hedef 22.74, gerceklesen ort. 13.851 (**-39.1%**)
>   - `Stage2.M14`: hedef 11.71, gerceklesen ort. 8.036 (**-31.4%**)
> Bu bir merkezleme (centering) problemidir; variability'den ayri ele alinir.

## 5. Otokorelasyon

| column | lag1 | lag30 | lag60 | lag300 | lag600 |
|---|---|---|---|---|---|
| Machine1.Zone1Temperature.C.Actual | 0.993 | 0.835 | 0.565 | 0.19 | 0.435 |
| Machine1.Zone2Temperature.C.Actual | 0.996 | 0.508 | -0.47 | -0.527 | -0.393 |
| Machine1.MotorRPM.C.Actual | 0.998 | 0.997 | 0.995 | 0.973 | 0.942 |
| Machine1.ExitZoneTemperature.C.Actual | 1.0 | 0.986 | 0.955 | 0.83 | 0.776 |
| Machine2.Zone1Temperature.C.Actual | 0.923 | 0.297 | -0.014 | -0.004 | -0.01 |
| Machine2.Zone2Temperature.C.Actual | 0.9 | 0.043 | -0.077 | -0.049 | -0.015 |
| AmbientConditions.AmbientHumidity.U.Actual | 1.0 | 0.999 | 0.998 | 0.99 | 0.981 |
| AmbientConditions.AmbientTemperature.U.Actual | 1.0 | 0.992 | 0.985 | 0.922 | 0.787 |
| Stage1.Output.Measurement0.U.Actual | 0.929 | 0.138 | 0.029 | 0.004 | 0.001 |
| Stage2.Output.Measurement0.U.Actual | 0.683 | 0.52 | 0.484 | 0.386 | 0.203 |

> **BULGU A1 - Ardisik gozlemler bagimsiz degil.** Karar degiskenlerinde
> lag-1 otokorelasyonu 0.99'a ulasiyor. **Rastgele train/test split
> kullanilirsa test seti train setinin neredeyse kopyasi olur ve R2
> sahte sekilde yuksek cikar.** Bloklu / zaman-sirali split zorunludur.
