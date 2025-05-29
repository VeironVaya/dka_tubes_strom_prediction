# Analisis Laporan Klasifikasi Random Forest

## 1. Support (Jumlah Data per Kelas)

Jumlah data asli untuk tiap kelas di data uji:

- **High:** 2 data
- **Low:** 12 data
- **Medium:** 86 data

**Total data uji:** 100

---

## 2. Confusion Matrix

| Actual \ Predicted | High | Low | Medium |
| ------------------ | ---- | --- | ------ |
| **High**           | 0    | 0   | 2      |
| **Low**            | 0    | 7   | 5      |
| **Medium**         | 0    | 0   | 86     |

- Dari 2 data **High**, semuanya salah prediksi jadi **Medium**.
- Dari 12 data **Low**, 7 benar, 5 salah ke **Medium**.
- Dari 86 data **Medium**, semuanya benar.

---

## 3. Hasil Per Kelas

| Kelas  | Precision | Recall | F1-Score | Jumlah Data |
| ------ | --------- | ------ | -------- | ----------- |
| High   | 0.00      | 0.00   | 0.00     | 2           |
| Low    | 1.00      | 0.58   | 0.74     | 12          |
| Medium | 0.92      | 1.00   | 0.96     | 86          |

**Penjelasan singkat:**

- **Precision:** Seberapa tepat prediksi untuk kelas tersebut (berapa dari prediksi kelas itu benar).
- **Recall:** Seberapa banyak data asli kelas itu yang berhasil ditemukan.
- **F1-Score:** Kombinasi precision dan recall jadi satu angka.

**Catatan penting:**

- Model **tidak pernah memprediksi kelas 'High'**, jadi precision dan recall-nya nol.
- Prediksi untuk kelas **'Low' sangat tepat** (precision 1.0), tapi banyak data asli Low yang tidak terdeteksi (recall 0.58).
- Prediksi untuk kelas **'Medium' sangat baik**, semua data Medium terdeteksi (recall 1.0).

---

## 4. Hasil Keseluruhan

- **Akurasi total:** (7 data Low + 86 data Medium yang benar) / 100 = **93%**
- **Rata-rata Macro** (rata tanpa mempertimbangkan proporsi):

  - Precision: 0.64
  - Recall: 0.53
  - F1-Score: 0.57

- **Rata-rata Weighted** (mempertimbangkan proporsi kelas):

  - Precision: 0.92
  - Recall: 0.93
  - F1-Score: 0.91

---

## 5. Kesimpulan

- Model sangat bagus mengenali kelas **Medium** (kelas yang paling banyak datanya).
- Model gagal mengenali kelas **High** karena data sangat sedikit (hanya 2 sampel).
- Model cukup sering salah mengenali kelas **Low**, menganggapnya sebagai **Medium**.
