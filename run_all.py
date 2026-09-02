"""
Tum pipeline'i sirayla calistirir.

Neden var: pipeline'i elle `rm -f reports/*.md` ile temizlerken elle yazilan
`assumptions.md` de silindi (hicbir script onu uretmiyordu). Bu script yalnizca
URETILEN ciktilari temizler ve sirayi tek yerde tutar.

Kural: `reports/` altindaki her sey script ciktisidir, silinebilir.
       Elle yazilan dokumanlar `docs/` altindadir, asla silinmez.

Calistirma:
    python run_all.py            # temizle + hepsini calistir
    python run_all.py --keep     # temizlemeden calistir
"""
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent

# Sira onemli: her adim oncekinin ciktisini kullanir.
STEPS = [
    ("src/data_processing/audit.py", "veri kalitesi teshisi"),
    ("src/data_processing/verify_a1.py", "A1 varsayimi + ornekleme frekansi"),
    ("src/data_processing/clean.py", "temizlik + deviation KPI'lari"),
    ("src/data_processing/data_dictionary.py", "degisken sozlugu"),
    ("src/analysis/capability.py", "control chart + Cp/Cpk"),
    ("src/analysis/correlation.py", "otokorelasyon + FDR duzeltmeli korelasyon"),
    ("src/analysis/stage_link.py", "transport delay aramasi"),
    ("src/modeling/train.py", "tahmin modelleri + CPP"),
    ("src/optimization/optimize.py", "dar kapsamli optimizasyon"),
    ("src/analysis/validation.py", "walk-forward validation + drift"),
    ("src/analysis/recommendations.py", "endustriyel oneri + DOE"),
    ("src/analysis/figures.py", "gorseller"),
]

# Yalnizca bunlar uretilen ciktidir; temizlikte silinir.
GENERATED = ["reports/*.md", "reports/*.csv", "reports/figures/*.png",
             "data/processed/*.csv"]


def clean_outputs():
    n = 0
    for pattern in GENERATED:
        for p in ROOT.glob(pattern):
            p.unlink()
            n += 1
    print(f"temizlendi: {n} uretilen dosya")
    print("korundu   : docs/ (elle yazilan dokumanlar), data/raw, data/_quarantine\n")


def main():
    if "--keep" not in sys.argv:
        clean_outputs()

    failed = []
    t0 = time.time()
    for script, desc in STEPS:
        name = Path(script).stem
        print(f"  {name:<16} {desc:<42}", end="", flush=True)
        t = time.time()
        r = subprocess.run([sys.executable, str(ROOT / script)],
                           capture_output=True, text=True)
        if r.returncode == 0:
            print(f"OK  ({time.time() - t:.1f}s)")
        else:
            print("HATA")
            failed.append((name, r.stderr.strip().splitlines()[-1:]))

    print(f"\ntoplam {time.time() - t0:.1f}s")
    if failed:
        print("\nBASARISIZ:")
        for name, err in failed:
            print(f"  {name}: {' '.join(err)}")
        return 1
    print("pipeline tamam.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
