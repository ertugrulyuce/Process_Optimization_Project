# KARANTINA — KULLANMAYIN

`continuous_factory_process_EXCEL_BOZUK.csv`

Bu dosya, ham CSV'nin Excel'de Turkce locale ile acilip kaydedilmis halidir.
Excel ondalikli sayilari tarih olarak yorumlamis:

    11.54  ->  Kas.54
    21.03  ->  21.Mar
    13.5   ->  13.May      <-- geri cevrilemez

Olcum: 556.563 / 1.620.120 hucre bozuk (%34,4). 115 sayisal kolonun 94'u etkilenmis.

Geri cevirme KAYIPLIDIR: `13.5` ve `13.05` ikisi de `13.May` olarak yazilmis;
geri donusturuldugunde ayirt edilemez. Bu yuzden dosya onarilmadi, karantinaya alindi.

Dogru kaynak: data/raw/continuous_factory_process.csv (UTF-8, virgul ayrac, Kaggle orijinali)

KURAL: Ham CSV hicbir zaman Excel'de acilmayacak. pandas ile okunacak.
