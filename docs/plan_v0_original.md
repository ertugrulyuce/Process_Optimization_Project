# Continuous Manufacturing Process Optimization

## Proje Amacı

Gerçek bir multistage continuous-flow manufacturing prosesinden alınan veriyi kullanarak uçtan uca bir **Process Optimization** çalışması yürütmek.

**Ana problem:** Üretim prosesindeki kontrol edilebilir parametrelerin ürün boyutsal çıktılarının hedef değerlerinden sapmasına etkisini belirlemek ve proses variability/deviation'ını azaltabilecek optimum çalışma koşullarını ortaya çıkarmak.

**Ana akış:**

Raw Data → Data Engineering → Process Mapping → KPI Definition → EDA → Process Capability & Stability → Root Cause Analysis → Predictive Modeling → Optimization → Scenario Analysis → Validation → Industrial Recommendations → Dashboard → Documentation

### Temel prensipler
- Sonuçlar önceden belirlenmeyecek.
- Veri istenen sonucu verecek şekilde manipüle edilmeyecek.
- Varsayımlar gerçek veriden ayrı tutulacak.
- Korelasyon doğrudan nedensellik olarak yorumlanmayacak.
- ML amaç değil, mühendislik problemini çözmek için araç olacak.
- Her önemli kararın teknik gerekçesi dokümante edilecek.
- Sprintler sırayla tamamlanacak.

---

## Veri ve Proses

**Dataset:** Multistage Continuous-Flow Manufacturing Process  
**Kaynak:** Kaggle — https://www.kaggle.com/datasets/supergus/multistage-continuousflow-manufacturing-process

Yaklaşık **14.088 gözlem ve 116 değişken** içerir.

### Proses

```text
                    ┌── Machine 1 ──┐
                    │               │
Raw Material ───────┼── Machine 2 ──┼──→ Combiner → Stage 1 Output
                    │               │
                    └── Machine 3 ──┘
                                           │
                                           ↓
                                      Machine 4
                                           │
                                           ↓
                                      Machine 5
                                           │
                                           ↓
                                    Stage 2 Output
```

### Stage 1
Machine 1–3 paralel proseslerdir. Değişkenler arasında raw material properties, feeder parameters, zone temperatures, motor amperage/RPM, material pressure/temperature ve exit temperature bulunur. Combiner değişkenleri ayrıca incelenecektir.

Stage 1 sonunda **15 output measurement** için Actual + Setpoint bulunur.

### Stage 2
Stage 1 output sonrasında Machine 4 ve Machine 5 seri çalışır.

Stage 2 sonunda yine **15 output measurement** için Actual + Setpoint bulunur.

---

# Sprint Planı

## Sprint 0 — Project Definition & Scope

**Amaç:** Projenin sınırlarını ve mühendislik problemini kesinleştirmek.

### Yapılacaklar
- [ ] Dataset ve kaynak dokümantasyonunu doğrula
- [ ] Proses akışını çıkar
- [ ] Stage 1 / Stage 2 ayrımını netleştir
- [ ] Input / Process / Output değişkenlerini tanımla
- [ ] Optimization problem statement oluştur
- [ ] KPI'ları belirle
- [ ] Varsayımları dokümante et
- [ ] Kapsam / kapsam dışı konuları belirle

### Çıktılar
- Project Charter
- Process Flow
- KPI Framework
- Assumptions Log

---

## Sprint 1 — Data Audit & Data Engineering

**Amaç:** Ham veriyi güvenilir ve analiz edilebilir hale getirmek.

### Yapılacaklar
- [ ] CSV import
- [ ] Dataset dimensions
- [ ] Data types
- [ ] Timestamp analizi
- [ ] Duplicate kontrolü
- [ ] Missing value analizi
- [ ] Constant / near-constant variable analizi
- [ ] Impossible value kontrolü
- [ ] Zero value analizi
- [ ] Outlier ön incelemesi
- [ ] Bozuk numeric değerlerin kaynağını araştır
- [ ] Numeric conversion
- [ ] Cleaning rules oluştur
- [ ] Raw / processed dataset ayrımı
- [ ] Data dictionary oluştur

### Çıktılar
- Clean Dataset v1
- Data Dictionary
- Data Quality Report
- Cleaning Pipeline

---

## Sprint 2 — Process Mapping & KPI Construction

**Amaç:** Dataseti fiziksel prosesle eşleştirmek ve performans metriklerini oluşturmak.

### Yapılacaklar
- [ ] Machine 1–5 değişkenlerini kategorize et
- [ ] Stage 1 inputs
- [ ] Combiner variables
- [ ] Stage 1 outputs
- [ ] Stage 2 inputs
- [ ] Stage 2 outputs
- [ ] Actual / Setpoint eşleştirmesi
- [ ] Deviation hesapla
- [ ] Absolute deviation
- [ ] Relative deviation
- [ ] Output bazında KPI tablosu
- [ ] Out-of-spec kriterini belirle

### KPI adayları
- Mean Absolute Deviation
- RMSE
- Relative Deviation
- % Within Specification
- Standard Deviation
- Coefficient of Variation
- Out-of-Specification Rate
- Target Achievement Rate

### Çıktılar
- Process Variable Map
- KPI Dataset
- Output Performance Table

---

## Sprint 3 — Exploratory Data Analysis

**Amaç:** Prosesin veri üzerinden davranışını anlamak.

### Yapılacaklar
- [ ] Distribution analysis
- [ ] Time-series analysis
- [ ] Machine parameter distributions
- [ ] Stage 1 output distributions
- [ ] Stage 2 output distributions
- [ ] Actual vs Setpoint
- [ ] Correlation analysis
- [ ] Parameter variability
- [ ] Measurement relationships
- [ ] Stage 1 → Stage 2 ilişkisi
- [ ] Problemli output'ları belirle

### Çıktılar
- EDA Notebook
- EDA Report
- Problematic Output List

---

## Sprint 4 — Process Capability & Stability

**Amaç:** Prosesin ortalamasını, değişkenliğini ve stabilitesini değerlendirmek.

### Yapılacaklar
- [ ] Control charts
- [ ] Moving range
- [ ] Process variation
- [ ] Stability analysis
- [ ] Specification limits
- [ ] Cp / Cpk (uygunsa)
- [ ] Out-of-control periods
- [ ] Time/regime bazlı değişim analizi

### Çıktılar
- Process Capability Report
- Stability Analysis
- Control Charts

---

## Sprint 5 — Root Cause Analysis

**Amaç:** Output deviation'ın hangi proses parametreleriyle ilişkili olduğunu belirlemek.

### Stage 1
Machine 1 + Machine 2 + Machine 3 → Combiner → Stage 1 Output

### Stage 2
Stage 1 Output → Machine 4 → Machine 5 → Stage 2 Output

### Yapılacaklar
- [ ] Correlation screening
- [ ] Feature relationships
- [ ] Lag relationships
- [ ] Multicollinearity
- [ ] Feature importance
- [ ] Sensitivity analysis
- [ ] Proses bilgisi ile istatistiksel sonuçları karşılaştır
- [ ] Critical Process Parameters (CPP) belirle

### Çıktılar
- Root Cause Analysis
- Critical Process Parameters List
- Feature Relationship Analysis

---

## Sprint 6 — Predictive Modeling

**Amaç:** Kritik proses parametrelerinin output deviation'ını ne ölçüde açıklayabildiğini modellemek.

### Modeller
**Baseline**
- [ ] Linear Regression

**Non-linear**
- [ ] Random Forest
- [ ] Gradient Boosting / XGBoost

### Yapılacaklar
- [ ] Target selection
- [ ] Feature selection
- [ ] Train/test split
- [ ] Time-aware validation
- [ ] Baseline model
- [ ] Non-linear models
- [ ] MAE
- [ ] RMSE
- [ ] R²
- [ ] Feature importance
- [ ] Model interpretation

### Çıktılar
- Predictive Model
- Model Comparison
- Feature Importance Analysis

---

## Sprint 7 — Process Optimization

**Amaç:** Kritik parametreler için optimum çalışma koşullarını belirlemek.

### Yapılacaklar
- [ ] Optimization objective tanımla
- [ ] Decision variables belirle
- [ ] Process constraints belirle
- [ ] Operating limits belirle
- [ ] Physical feasibility constraints
- [ ] Objective function oluştur
- [ ] Optimization modelini kur
- [ ] Optimum operating points/ranges belirle
- [ ] Sensitivity analysis

### Olası objective

```text
Minimize:
Output Deviation
+ Process Variability
+ Out-of-Spec Probability
```

Kesin objective veri analizi sonrasında belirlenecek.

### Çıktılar
- Optimization Model
- Optimal Operating Conditions
- Constraint Set
- Sensitivity Analysis

---

## Sprint 8 — Scenario / What-if Analysis

**Amaç:** Mevcut proses ile önerilen proses koşullarını karşılaştırmak.

### Senaryolar
- [ ] Current Settings
- [ ] Optimized Settings
- [ ] Conservative Optimization
- [ ] Aggressive Optimization

### KPI karşılaştırması
- Mean deviation
- Standard deviation
- OOS rate
- Target achievement
- Process variability

### Çıktılar
- Scenario Analysis
- Before / After Comparison
- Management-level Recommendation Table

---

## Sprint 9 — Validation

**Amaç:** Model ve optimization sonuçlarının farklı veri üzerinde de geçerli olup olmadığını kontrol etmek.

### Yapılacaklar
- [ ] Holdout / test validation
- [ ] Time-aware validation
- [ ] Optimization validation
- [ ] Sensitivity analysis
- [ ] Robustness test
- [ ] Extreme parameter scenarios
- [ ] Model limitations
- [ ] Assumption limitations

### Çıktılar
- Validation Report
- Robustness Analysis
- Limitations Section

---

## Sprint 10 — Industrial Engineering Interpretation

**Amaç:** Analitik sonuçları uygulanabilir proses iyileştirme önerilerine çevirmek.

### Yapılacaklar
- [ ] Process improvement recommendations
- [ ] Critical parameter control recommendations
- [ ] Monitoring recommendations
- [ ] Operator recommendations
- [ ] Maintenance implications
- [ ] Data collection recommendations
- [ ] Implementation considerations

### Çıktı

```text
Finding
→ Engineering Interpretation
→ Recommended Action
→ Expected Impact
→ Implementation Risk
```

**Industrial Improvement Proposal**

---

## Sprint 11 — Dashboard

**Amaç:** Sonuçları teknik olmayan kullanıcıların da anlayabileceği şekilde sunmak.

### Dashboard

**Process Overview**
- Stage 1 performance
- Stage 2 performance
- Process status

**Quality**
- Deviation
- OOS
- Variability

**Critical Parameters**
- CPP ranking
- Current range
- Recommended range

**Optimization**
- Current vs Optimized
- Improvement %

### Araçlar
- Python
- Power BI veya Tableau

### Çıktı
Interactive Process Optimization Dashboard

---

## Sprint 12 — Documentation & Portfolio

**Amaç:** Projeyi profesyonel, tekrar üretilebilir ve CV/GitHub'a uygun hale getirmek.

### Repository

```text
continuous-manufacturing-optimization/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_process_capability.ipynb
│   ├── 05_root_cause_analysis.ipynb
│   ├── 06_predictive_modeling.ipynb
│   ├── 07_optimization.ipynb
│   └── 08_validation.ipynb
│
├── src/
│   ├── data_processing/
│   ├── analysis/
│   ├── modeling/
│   └── optimization/
│
├── dashboard/
├── reports/
├── README.md
└── requirements.txt
```

### Dokümantasyon
- [ ] README
- [ ] Project methodology
- [ ] Data dictionary
- [ ] Technical report
- [ ] Results
- [ ] Limitations
- [ ] Future work
- [ ] Reproducibility instructions

### Final portfolio çıktıları
- GitHub Repository
- Technical Report
- Dashboard
- Process Flow
- Optimization Results
- Before/After KPI comparison
- CV project entry
- Interview case study

---

# Nihai Proje Hikayesi

```text
REAL MANUFACTURING DATA
        ↓
DATA QUALITY
        ↓
PROCESS UNDERSTANDING
        ↓
KPI DEFINITION
        ↓
PROCESS PERFORMANCE
        ↓
ROOT CAUSE ANALYSIS
        ↓
CRITICAL PROCESS PARAMETERS
        ↓
PREDICTIVE MODEL
        ↓
OPTIMIZATION
        ↓
SCENARIO ANALYSIS
        ↓
VALIDATION
        ↓
INDUSTRIAL RECOMMENDATION
```

Proje tamamlandığında amaç sadece “XGBoost kullandım” demek değil; gerçek bir continuous manufacturing prosesini analiz edip, kritik proses parametrelerini belirleyip, output deviation'ını modelleyip, proses kısıtları altında daha iyi çalışma koşullarını optimize edip doğrulayabilmek.

---

# Proje Başarı Kriterleri

- [ ] Ham verinin güvenilir şekilde temizlenmesi
- [ ] Prosesin doğru modellenmesi
- [ ] Ölçülebilir KPI framework
- [ ] Problemli output'ların belirlenmesi
- [ ] Critical Process Parameters tespiti
- [ ] Predictive model
- [ ] Optimization model
- [ ] Validation
- [ ] Quantitative before/after comparison
- [ ] Industrial recommendations
- [ ] Dashboard
- [ ] Technical documentation

**Improvement yüzdesi veya başarı miktarı önceden belirlenmeyecek.** Nihai sonuç analizden çıkacak.

---

# Çalışma Prensibimiz

1. Önce problemi anlayacağız.
2. Sonra veriyi anlayacağız.
3. Sonra analiz edeceğiz.
4. Sonra modelleyeceğiz.
5. En son optimize edeceğiz.

**Data → Insight → Model → Decision**

ML veya optimization sonucu beklediğimiz gibi çıkmazsa projeyi zorlamayacağız; sonucu olduğu gibi raporlayacağız.

---

# Mevcut Durum

**Sprint 0 — Process Mapping aşaması tamamlandı.**

**Sıradaki:** Sprint 1 — Data Audit & Data Engineering

İlk teknik hedef:

> Ham CSV'nin veri kalitesini sistematik olarak incelemek ve reproducible bir cleaning pipeline oluşturmak.
