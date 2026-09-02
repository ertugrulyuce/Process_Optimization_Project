"""
Faz 2 - Proses Kararliligi ve Short-Term Capability.

Kapsam ici 25 output icin:
  - I-MR (individuals & moving range) kontrol grafigi istatistikleri
  - short-term sigma (MR_bar / d2) ve long-term sigma (overall std)
  - kararlilik gostergesi: sigma_lt / sigma_st orani
  - Cp / Cpk -- varsayimsal spec limitleriyle, birden fazla senaryoda

ONEMLI UYARI (raporda da ayrica isleniyor):
I-MR kontrol grafigi ardisik gozlemlerin BAGIMSIZ oldugunu varsayar. Bu veride
lag-1 otokorelasyonu 0.93-0.99 (K5). Otokorelasyonlu seride MR_bar kucuk cikar,
kontrol limitleri gercekte olmasi gerekenden dar olur ve neredeyse her nokta
"out of control" gorunur. Bu yuzden asagidaki out-of-control sayilari
PROSES DEGIL, YONTEM ARTIFAKTIDIR ve oyle raporlanir.

Calistirma:  python src/analysis/capability.py
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "data_processing"))
import schema  # noqa: E402,F401

PROC = ROOT / "data" / "processed" / "clean_v1.csv"
KPI_SUM = ROOT / "reports" / "output_kpi_summary.csv"
OUT = ROOT / "reports" / "03_capability_report.md"

# I-MR sabiti: n=2 icin d2. sigma_st = MR_bar / d2
D2_N2 = 1.128

# A4: veride spec limit YOK. Cp/Cpk mutlak hukum icin degil, output'lar arasi
# karsilastirma icin uretiliyor. Tek bir keyfi limit yerine uc senaryo:
SPEC_SCENARIOS = {"dar (+/-%1)": 0.01, "orta (+/-%2)": 0.02, "genis (+/-%5)": 0.05}


def load():
    df = pd.read_csv(PROC)
    summary = pd.read_csv(KPI_SUM)
    return df, summary


def imr_stats(x: pd.Series) -> dict:
    """I-MR kontrol grafigi istatistikleri. NaN'lar atlanir."""
    v = x.dropna()
    if len(v) < 10:
        return {}
    mr = v.diff().abs().dropna()
    mr_bar = float(mr.mean())
    sigma_st = mr_bar / D2_N2          # short-term (within) sigma
    sigma_lt = float(v.std())          # long-term (overall) sigma
    mu = float(v.mean())

    ucl, lcl = mu + 3 * sigma_st, mu - 3 * sigma_st
    ooc = int(((v > ucl) | (v < lcl)).sum())

    return dict(
        n=len(v), mean=mu, sigma_st=sigma_st, sigma_lt=sigma_lt,
        # >1 ise long-term yayilim short-term'den genis: kayma/surukleme isareti.
        # Otokorelasyon bu orani sisirdigi icin tek basina delil sayilmaz.
        lt_st_ratio=sigma_lt / sigma_st if sigma_st else np.nan,
        ucl=ucl, lcl=lcl, ooc=ooc, ooc_pct=100 * ooc / len(v),
        mr_bar=mr_bar,
    )


def capability(mu, sigma_st, setpoint, tol_frac):
    """Cp/Cpk. Spec limitleri setpoint etrafinda simetrik varsayiliyor (A4)."""
    if not sigma_st or np.isnan(setpoint):
        return np.nan, np.nan
    usl = setpoint * (1 + tol_frac)
    lsl = setpoint * (1 - tol_frac)
    cp = (usl - lsl) / (6 * sigma_st)
    cpk = min(usl - mu, mu - lsl) / (3 * sigma_st)
    return cp, cpk


def main():
    df, summary = load()
    ins = summary[summary.in_scope == "evet"].copy()

    rows = []
    for _, r in ins.iterrows():
        st, m = r.output.split(".")
        col = f"{st}.Output.Measurement{m[1:]}.U.Actual"
        s = imr_stats(df[col])
        if not s:
            continue
        rec = dict(output=r.output, setpoint=r.setpoint,
                   error_type=r.error_type, **s)
        for label, tol in SPEC_SCENARIOS.items():
            cp, cpk = capability(s["mean"], s["sigma_st"], r.setpoint, tol)
            rec[f"Cp {label}"] = round(cp, 2)
            rec[f"Cpk {label}"] = round(cpk, 2)
        rows.append(rec)

    t = pd.DataFrame(rows)
    for c in ["mean", "sigma_st", "sigma_lt", "lt_st_ratio", "ucl", "lcl",
              "ooc_pct", "mr_bar"]:
        t[c] = t[c].round(4)

    lines = []
    w = lines.append
    w("# Faz 2 - Proses Kararliligi ve Short-Term Capability\n")
    w("Kaynak: `data/processed/clean_v1.csv`  ")
    w("Uretildi: `python src/analysis/capability.py`\n")
    w(f"Kapsam: {len(t)} output (Faz 1'de kapsam ici sayilanlar).\n")

    w("## Onemli uyari - kontrol grafiklerinin gecerliligi\n")
    w("I-MR kontrol grafigi **ardisik gozlemlerin bagimsiz oldugunu varsayar.**")
    w("Bu veride lag-1 otokorelasyonu 0.93-0.99 (K5). Otokorelasyonlu bir seride:\n")
    w("- Ardisik farklar kucuk oldugu icin `MR_bar` kucuk cikar,")
    w("- dolayisiyla `sigma_st` oldugundan kucuk tahmin edilir,")
    w("- kontrol limitleri gercekte olmasi gerekenden **dar** olur,")
    w("- ve seri, gercekte kararli olsa bile surekli limit disina tasar.\n")
    med_ooc = t.ooc_pct.median()
    w(f"> **BULGU C1 - Out-of-control oranlari yontem artifaktidir.** Medyan")
    w(f"> out-of-control orani **%{med_ooc:.1f}**. Gercek bir prosesde bu oran")
    w("> %0.3 civarinda olmali. Bu fark prosesin kontrolsuz oldugunu degil,")
    w("> **I-MR grafiginin bu veri icin uygun arac olmadigini** gosterir.")
    w("> Asagidaki `ooc` sutunlari bu nedenle proses hukmu olarak kullanilmaz.\n")
    w("> *Dogru yaklasim:* otokorelasyonlu proses icin EWMA / CUSUM grafigi veya")
    w("> once bir zaman serisi modeli kurup **artiklar** uzerinde kontrol grafigi")
    w("> (residual chart). Bu, Faz 3'te model kurulduktan sonra yapilabilir hale")
    w("> gelecek; simdilik kararlilik hukmu askiya alinir.\n")

    w("## Short-term vs long-term yayilim\n")
    w("`lt_st_ratio` = sigma_lt / sigma_st. 1'e yakinsa seri kararli; buyukse")
    w("seride kayma/surukleme var demektir. **Ancak** otokorelasyon `sigma_st`'yi")
    w("kucuk gosterdigi icin bu oran yukari saplidir; siralama icin kullanilabilir,")
    w("mutlak deger olarak degil.\n")
    top = t.nlargest(8, "lt_st_ratio")[
        ["output", "error_type", "sigma_st", "sigma_lt", "lt_st_ratio"]]
    w("| output | hata tipi | sigma_st | sigma_lt | lt/st |")
    w("|---|---|---|---|---|")
    for _, r in top.iterrows():
        w(f"| `{r.output}` | {r.error_type} | {r.sigma_st} | {r.sigma_lt} | "
          f"**{r.lt_st_ratio}** |")
    w("")
    w(f"> **BULGU C2 - Kayma en belirgin {top.iloc[0].output}'de** "
      f"(lt/st = {top.iloc[0].lt_st_ratio}). Sirali liste, Faz 3'te hangi")
    w("> output'larin zaman bagimli davranis gosterdigini onceliklendirmek icin")
    w("> kullanilacak.\n")

    w("## Capability (Cp / Cpk)\n")
    w("**Veride spesifikasyon limiti YOK** (A4). Asagidaki degerler setpoint")
    w("etrafinda simetrik varsayimsal toleranslarla hesaplandi. Amac *mutlak*")
    w('bir "proses yeterli/yetersiz" hukmu vermek degil -- output\'lari **ayni')
    w("olcute gore siralamak.** Uc senaryo, sonucun tolerans secimine ne kadar")
    w("duyarli oldugunu gosteriyor.\n")
    cols = (["output", "error_type", "setpoint", "sigma_st"]
            + [f"Cpk {k}" for k in SPEC_SCENARIOS])
    w("| " + " | ".join(cols) + " |")
    w("|" + "|".join("---" for _ in cols) + "|")
    for _, r in t.sort_values(f"Cpk {list(SPEC_SCENARIOS)[1]}").iterrows():
        w("| " + " | ".join(
            "" if pd.isna(r[c]) else str(r[c]) for c in cols) + " |")
    w("")

    mid = f"Cpk {list(SPEC_SCENARIOS)[1]}"
    worst = t.nsmallest(5, mid)
    w(f"> **BULGU C3 - En dusuk capability'ye sahip output'lar** (orta senaryo,")
    w("> +/-%2 tolerans):")
    for _, r in worst.iterrows():
        w(f">   - `{r.output}` ({r.error_type}): Cpk = **{r[mid]}**")
    w(">")
    w("> Cpk'nin negatif olmasi, proses ortalamasinin varsayilan tolerans")
    w("> bandinin **disinda** kalmasi demektir -- yani bias o kadar buyuk ki")
    w("> urun sistematik olarak spec disinda uretiliyor olurdu. Bu, Faz 1'deki")
    w("> bias bulgusunun capability diliyle tekrari.\n")

    var_dom = t[t.error_type == "variability"].nsmallest(5, mid)
    w("> **BULGU C4 - Optimizasyon hedefi output'larin capability'si.**")
    w("> Variability-baskin olanlar arasinda en dusuk Cpk:")
    for _, r in var_dom.iterrows():
        w(f">   - `{r.output}`: Cpk = {r[mid]}, sigma_st = {r.sigma_st}")
    w("> Bunlar Faz 3/4'un birincil hedefi: bias'i degil **yayilimi** kucultmek.\n")

    w("## Tam tablo\n")
    cols = ["output", "error_type", "n", "mean", "setpoint", "sigma_st",
            "sigma_lt", "lt_st_ratio", "ooc", "ooc_pct"] + \
           [f"{k} {s}" for s in SPEC_SCENARIOS for k in ("Cp", "Cpk")]
    w("| " + " | ".join(cols) + " |")
    w("|" + "|".join("---" for _ in cols) + "|")
    for _, r in t.iterrows():
        w("| " + " | ".join(
            "" if pd.isna(r[c]) else str(r[c]) for c in cols) + " |")
    w("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    t.to_csv(ROOT / "reports" / "capability_table.csv", index=False)
    print(f"yazildi: {OUT}")
    print("yazildi: reports/capability_table.csv\n")
    print(f"medyan out-of-control orani: %{med_ooc:.1f}  (yontem artifakti)")
    print(f"\nen dusuk Cpk (orta senaryo):")
    print(worst[["output", "error_type", mid]].to_string(index=False))


if __name__ == "__main__":
    main()
