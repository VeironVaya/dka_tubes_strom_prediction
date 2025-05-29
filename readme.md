# Tugas Besar Dasar Kecerdasan Artifisial

## Storm Prediction Warning

### 103012300100 Veiron Vaya Yarief

### 103012300288 Muhammad Ihsan Naufal

## Hasil

1. Dataset hasil prediksi
   Dataset akhir akan memiliki kolom tambahan seperti storm_score_sugeno (nilai angka 0–100) dan storm_label_sugeno (kategori: low, likely, high) sebagai hasil prediksi dari metode fuzzy Sugeno.
2. Visualisasi fungsi keanggotaan
   Gambar fungsi keanggotaan (seperti suhu rendah/sedang/tinggi, kelembaban rendah/sedang/tinggi) serta skema aturan fuzzy yang digunakan untuk prediksi akan dibuat untuk memperjelas cara kerja sistem.
3. Evaluasi model
   Evaluasi dilakukan untuk mengetahui seberapa baik prediksi sistem. Jika tersedia data kebenaran (label asli badai), maka akan digunakan confusion matrix dan nilai akurasi, precision, recall, dan F1-score. Jika tidak ada, evaluasi dilakukan dengan membandingkan pola hasil prediksi terhadap kondisi cuaca ekstrim.
4. Perbandingan metode
   Perbandingan antar metode mambadani dan sugeno
5. Notebook atau skrip
   Akan dibuat notebook (seperti Jupyter Notebook) yang berisi seluruh proses mulai dari persiapan data, pembuatan fuzzy system, hingga hasil akhir. Notebook ini bisa dijalankan ulang untuk data baru.
6. Fungsi prediksi siap pakai
   Akan dibuat fungsi Python sederhana seperti sugeno_predict(row) yang dapat menerima input data cuaca dan langsung memberikan output prediksi kemungkinan badai.
