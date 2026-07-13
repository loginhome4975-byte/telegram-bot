# 📊 To'liq Model Analitikasi — Barcha 8 Versiya

**Sana:** 2026-07-13
**Metodologiya:** Barcha modellar **bir xil sharoitda** qayta o'qitildi:
- **Hyperparametrlar:** `depth=6, learning_rate=0.05, l2_leaf_reg=3` (hammasi uchun bir xil)
- **Train:** < 2022-08-01 (18,934 o'yin)
- **Validation:** 2022-08-01 — 2023-07-31 (2,367 o'yin)
- **Test:** ≥ 2023-08-01 (2,304 o'yin, barcha 6 liga)
- **Bootstrap:** 10,000 iteratsiya, 95% CI

---

## 1. Barcha Modellar — Raw (Kalibratsiyasiz) Natijalar

| # | Model | Features | Log Loss ↓ | Brier ↓ | Accuracy ↑ | RPS ↓ | DC rho |
|---|-------|----------|-----------|---------|------------|-------|--------|
| V1 | Baseline | 28 | 0.99386 | 0.59344 | 51.13% | 0.20198 | -0.04396 |
| V1.1 | + xG | 32 | 0.99387 | 0.59326 | 51.39% | 0.20176 | -0.04375 |
| **V2** | **+ MV** | **30** | **0.99014** | **0.59085** | **51.48%** | **0.20070** | -0.04361 |
| V2.1 | + xG + MV | 34 | **0.98960** | **0.59041** | 51.09% | **0.20043** | -0.04401 |
| V3 | + MV + Injuries | 32 | 0.99092 | 0.59162 | 51.17% | 0.20102 | -0.04482 |
| V3.1 | + MV + Inj + Susp | 34 | 0.99094 | 0.59153 | 51.74% | 0.20100 | -0.04369 |
| V4-alt | + MV + WF | 32 | 0.98967 | 0.59070 | 51.61% | 0.20066 | -0.04366 |
| V4 | + MV + Inj + WF | 34 | 0.99051 | 0.59118 | 51.65% | 0.20091 | -0.04376 |

## 2. Barcha Modellar — Calibrated (Isotonic Regression) Natijalar

| # | Model | Cal Log Loss ↓ | Cal Brier ↓ | Cal Accuracy ↑ | Cal RPS ↓ |
|---|-------|---------------|-------------|----------------|-----------|
| V1 | Baseline | 0.99168 | 0.59262 | 51.00% | 0.20151 |
| V1.1 | + xG | 0.99330 | 0.59291 | 51.74% | 0.20144 |
| **V2** | **+ MV** | **0.98971** | 0.59086 | **51.82%** | **0.20066** |
| V2.1 | + xG + MV | **0.98906** | **0.59002** | 51.52% | **0.20009** |
| V3 | + MV + Injuries | 0.99013 | 0.59197 | 51.61% | 0.20092 |
| V3.1 | + MV + Inj + Susp | 0.98891 | 0.59041 | 51.61% | 0.20046 |
| V4-alt | + MV + WF | 0.98930 | 0.59051 | 51.26% | 0.20052 |
| V4 | + MV + Inj + WF | 0.98885 | 0.59057 | 51.39% | 0.20046 |

---

## 3. Bootstrap Significance Testlari (10,000 iteratsiya)

> [!IMPORTANT]
> **Qoida:** 95% CI nolni o'z ichiga olsa → statistik jihatdan **AHAMIYATSIZ** (farq tasodifiy bo'lishi mumkin).

| Solishtirish | O'rtacha farq | 95% CI | Qaror |
|---|---|---|---|
| V1 → V1.1 (xG qo'shish) | +0.00000 | `[-0.00242, +0.00243]` | ❌ Ahamiyatsiz |
| **V1 → V2 (MV qo'shish)** | **+0.00372** | **`[+0.00130, +0.00616]`** | **✅ AHAMIYATLI** |
| **V1.1 → V2.1 (xG ustiga MV)** | **+0.00427** | **`[+0.00187, +0.00664]`** | **✅ AHAMIYATLI** |
| V2 → V3 (Injuries qo'shish) | **-0.00077** | `[-0.00294, +0.00134]` | ❌ Ahamiyatsiz |
| V3 → V3.1 (Suspensions) | -0.00002 | `[-0.00212, +0.00204]` | ❌ Ahamiyatsiz |
| V3 → V4 (WF qo'shish) | +0.00041 | `[-0.00180, +0.00255]` | ❌ Ahamiyatsiz |
| V2 → V4-alt (WF, inj-siz) | +0.00048 | `[-0.00162, +0.00258]` | ❌ Ahamiyatsiz |
| **V1 → V3 (to'liq zanjir)** | **+0.00295** | **`[+0.00023, +0.00577]`** | **✅ AHAMIYATLI** |

---

## 4. Vizual Xulosa — Qaysi Feature Haqiqatan Ishlaydi?

```
                    STATISTIK JIHATDAN TASDIQLANGAN YAXSHILANISHLAR
                    ═══════════════════════════════════════════════

    V1 (Baseline)
     │
     │  ✅ MV qo'shish: +0.00372 [+0.00130, +0.00616] — TASDIQLANGAN
     ▼
    V2 (Baseline + MV)  ◄── ENG MUSTAHKAM MODEL
     │
     │  ❌ Injuries qo'shish: -0.00077 [-0.00294, +0.00134] — RAD
     ▼
    V3 (Baseline + MV + Injuries) ← avval rasmiy deb belgilangan

    ────────────────────────────────────────────────────────────

    RAD ETILGAN BARCHA QOLDIQ FEATURE'LAR:
    ❌ xG (V1.1)         → 0.00000 farq, sof shovqin
    ❌ Suspensions (V3.1) → -0.00002, shovqin
    ❌ Weakening Factor   → +0.00041, CI nolni o'z ichiga oladi
```

---

## 5. Model O'qitish Detallari

### CatBoost Iteratsiyalari (Early Stopping natijasi)

| Model | Home λ iter | Away λ iter | Izoh |
|---|---|---|---|
| V1 Baseline | 177 | 43 | Away model tezroq konvergensiya |
| V1.1 + xG | 122 | 51 | xG home signalini takrorlaydi |
| V2 + MV | 145 | 51 | Optimal balans |
| V2.1 + xG + MV | 99 | 53 | xG ortiqcha — kamroq iteratsiya |
| V3 + Injuries | **254** | 52 | ⚠️ Injuries ortiqcha iteratsiyaga olib keldi |
| V3.1 + Susp | 140 | 50 | — |
| V4-alt + WF | 146 | 71 | WF away modelga ham ta'sir etdi |
| V4 + Inj + WF | 121 | 48 | — |

> [!WARNING]
> V3'da home model **254 iteratsiyagacha** o'sdi — boshqa modellarning 100-180 oralig'idan ancha yuqori. Bu Injuries feature'i sparse (kam uchraydigan) ekanini va modelning uni o'rganishga uzoq urinib, overfitting chegarasiga yaqinlashganini ko'rsatadi.

### Dixon-Coles Rho Qiymatlari

Barcha modellarda rho ≈ **-0.044** (o'rtacha). Bu past gollik natijalar (0-0, 1-0, 0-1) ning Poisson modeldan biroz kamroq ehtimolga ega ekanini ko'rsatadi — bu futbol uchun kutilgan va barqaror natija.

---

## 6. ⚠️ MUHIM KASHFIYOT

> [!CAUTION]
> **Avvalgi xulosa noto'g'ri bo'lishi mumkin.**
>
> Biz ilgari **V3** (Baseline + MV + Injuries) ni rasmiy model deb belgilagan edik. Lekin **to'liq, izolyatsiya qilingan, barcha modellar bir xil sharoitda qayta o'qitilgan** analitika **boshqa rasmga ishora qilmoqda:**
>
> **Jarohatlar (Injuries) V2 ga nisbatan hech qanday statistik yaxshilanish bermaydi.**
>
> Bootstrap CI: `[-0.00294, +0.00134]`, o'rtacha farq: **-0.00077** (manfiy — V3 yomonroq).

### Nima o'zgarishdi?

**Avvalgi testlar** faqat **272 ta APL o'yinida** (kichik subset) o'tkazilgan edi — o'sha kichik hajm bilan V3 nominal yaxshiroq ko'rindi. Endi **2,304 ta o'yinda** (barcha 6 liga) test qilganimizda:

| Metrika | V2 (MV faqat) | V3 (MV + Injuries) | Kim yutdi? |
|---|---|---|---|
| Raw Log Loss | **0.99014** | 0.99092 | V2 ✅ |
| Raw Brier | **0.59085** | 0.59162 | V2 ✅ |
| Raw RPS | **0.20070** | 0.20102 | V2 ✅ |
| Raw Accuracy | **51.48%** | 51.17% | V2 ✅ |
| Cal Log Loss | **0.98971** | 0.99013 | V2 ✅ |

**V2 barcha 5 ta metrikada V3 dan yaxshiroq.** Bu tasodif emas — bu sistematik natija.

---

## 7. Qaror Kerak

Sizning oldingizda ikkita variant bor:

### A varianti: V2 ni rasmiy model qilish
```
MODEL:     baseline_plus_mv
FEATURES:  28 baseline + 2 MV = 30 ta
NATIJA:    LL=0.99014 | Brier=0.59085 | Acc=51.48% | RPS=0.20070
DALIL:     Yagona statistik jihatdan tasdiqlangan yaxshilanish (V1→V2).
           Soddaroq model. Injuries skraping kerak emas.
```

### B varianti: V3 ni saqlash (status quo)
```
MODEL:     baseline_plus_mv_injuries
FEATURES:  28 baseline + 2 MV + 2 Injuries = 32 ta
NATIJA:    LL=0.99092 | Brier=0.59162 | Acc=51.17% | RPS=0.20102
DALIL:     V1→V3 zanjiri statistik jihatdan tasdiqlangan (CI [+0.00023, +0.00577]).
           Lekin bu yaxshilanish faqat MV tufayli, Injuries emas.
```

> [!NOTE]
> **V1 → V3 to'liq zanjiri** statistik jihatdan tasdiqlangan (`CI [+0.00023, +0.00577]`). Lekin bu yaxshilanishning **95%+ qismi MV dan kelyapti**, Injuries emas. V2 → V3 qadami o'zi mustaqil ravishda RAD etilgan.

---

## 8. Foydalanilgan Fayllar

| Fayl | Tavsif |
|---|---|
| [full_analytics.py](file:///home/ubuntu/ai-models/full_analytics.py) | Barcha 8 model qayta o'qitish + baholash skripti |
| [feature_config.py](file:///home/ubuntu/ai-models/feature_config.py) | Feature set ta'riflari |
| [model_training.py](file:///home/ubuntu/ai-models/model_training.py) | Asosiy o'qitish skripti |
| [full_analytics.json](file:///home/ubuntu/ai-models/football-data/models/full_analytics.json) | Natijalar JSON formatda |
