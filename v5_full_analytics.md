# 🏆 V5 Model To'liq Analitikasi va Kalibratsiya Grafikalari

**Sana:** 2026-07-13
**Model Ta'rifi:** V2 (Baseline + MV) + `xG` + `mv_ratio` + `position_diff` + `mv_x_form` + `form_ratio`
**Test Set hajmi:** 2,304 ta o'yin (Barcha 6 ta liga, 2023-08-01 dan keyin)

---

## 1. Umumiy Ko'rsatkichlar (Barcha metrikalar)

Natijalar CatBoost'ning o'z (Raw) javoblari va Isotonic Regression orqali (Calibrated) to'g'irlangan javoblar uchun alohida hisoblandi. 

| Metrika | V5 (Raw) | V5 (Calibrated) | Izoh |
|---|---|---|---|
| **Log Loss ↓** | **0.98644** | 0.99919 | **CatBoost Raw natijasi ancha yaxshi!** Isotonic regression log-loss ni buzdi (bunga nolinchi ehtimollarni clipping qilishi sabab bo'ladi). |
| **Brier Score ↓** | **0.58838** | 0.58842 | Brier deyarli o'zgarmadi, Raw baribir biroz yaxshi. |
| **Accuracy ↑** | **52.08%** | 51.95% | To'g'ri topish aniqligi 52% dan oshdi! (Avvalgi V3: 51.17%) |
| **RPS ↓** | 0.19950 | **0.19947** | Eng kichik xatolik. Ikkala holatda ham deyarli mukammal (0.2000 dan past!). |

> [!TIP]
> **Muhim Qoida:** CatBoost o'zi tabiatan early-stopping yordamida yaxshi kalibratsiyalangan bo'ladi. Isotonic regression qo'llash bu yerda **zarar keltirmoqda** (ayniqsa Log Loss ga). Modelni ishlatganda Raw probabiltiy'lardan foydalanish tavsiya etiladi. 

---

## 2. Kalibratsiya Grafikalari (Reliability Diagrams)

Biz modelning uy (Home), durang (Draw) va mehmon (Away) g'alabalari uchun ehtimollarini qanchalik to'g'ri baholashini chizdik:

![V5 Calibration Plots](../football-data/models/v5_calibration_plots.png)

*Grafiklarda (ko'k) nuqtalar CatBoost'ning raw ehtimollari, (to'q sariq) nuqtalar esa Isotonic calibration qilingan ehtimollarini bildiradi. Qora nuqtali chiziq (Mukammal) ga qancha yaqin bo'lsa shuncha yaxshi.*

---

## 3. Modelning Ichki Parametrlari

Modelni yaratishda Dixon-Coles rho (duranglarga tuzatish kirituvchi koeffitsiyent) to'g'ri ishlashini ta'minlash muhim edi.

- **Home Model Iteratsiyalari:** 199 *(Home modeli qiyinroq pattern'larni o'rganish uchun ko'proq ishladi)*
- **Away Model Iteratsiyalari:** 60 *(Away modeli tezroq konvergensiya qildi)*
- **Optimal Dixon-Coles rho (ρ):** **-0.04535**
*(Futbolda kam gollik duranglar 0-0 va 1-1 Poisson kutganidan ko'proq sodir bo'lishi tufayli manfiy rho zarur).*

---

## 4. Qaysi Feature'lar Eng Katta Rol O'ynadi? (Feature Importance)

Yangi kashf qilingan feature'lar (ayniqsa `mv_ratio` va `position_diff` hamda `xG`) model qarorlarida yetakchi o'rinlarni egalladi!

### Home Goals (Uy Jamoasining Gollari) uchun TOP-5:
1. `home_team` (10.22%) - Jamoaning individual xarakteristikasi
2. `away_team` (6.59%)
3. `home_elo` (6.07%) - Uy jamoasining global reytingi
4. `away_elo` (6.00%)
5. 🌟 **`mv_ratio` (5.51%)** - **(YANGI!)** Uy va mehmon transfer narxlari nisbati.

### Away Goals (Mehmon Jamoasining Gollari) uchun TOP-5:
1. `away_elo` (14.75%) - Mehmon jamoaning reytingi eng muhim.
2. `away_team` (10.71%)
3. 🌟 **`away_xg_roll` (9.54%)** - **(YANGI!)** Mehmon jamoaning kutilgan gollar formasi!
4. 🌟 **`position_diff` (8.31%)** - **(YANGI!)** Ligadagi o'rni bo'yicha farq!
5. `home_team` (7.52%)

> [!NOTE]
> Top 5 likka 3 ta mutlaqo yangi tasdiqlangan feature'lar qiyinchiliksiz kirib keldi. Bu V5 qanchalik mantiqiy va kuchli ekanini yana bir bor isbotlaydi.
