---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/choosing-a-model
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: a6141b17671a40dd3f47f7cedc98da020371affbb632c38f03a0e6299e36edb7
---

# Memilih model yang tepat

Memilih model Claude yang optimal untuk aplikasi Anda melibatkan penyeimbangan tiga pertimbangan utama: kemampuan, kecepatan, dan biaya. Panduan ini membantu Anda membuat keputusan berdasarkan informasi sesuai dengan kebutuhan spesifik Anda.

---

## Tetapkan kriteria utama

Saat memilih model Claude, kami merekomendasikan untuk terlebih dahulu mengevaluasi faktor-faktor berikut:
- **Kemampuan:** Fitur atau kemampuan spesifik apa yang akan Anda butuhkan dari model untuk memenuhi kebutuhan Anda?
- **Kecepatan:** Seberapa cepat model perlu merespons dalam aplikasi Anda?
- **Biaya:** Berapa anggaran Anda untuk penggunaan pengembangan dan produksi?

Mengetahui jawaban ini sebelumnya akan membuat penyempitan dan keputusan model mana yang akan digunakan menjadi jauh lebih mudah.

***

## Pilih model terbaik untuk memulai

Ada dua pendekatan umum yang dapat Anda gunakan untuk mulai menguji model Claude mana yang paling sesuai dengan kebutuhan Anda.

### Opsi 1: Mulai dengan model yang cepat dan hemat biaya

Untuk banyak aplikasi, memulai dengan model yang lebih cepat dan hemat biaya seperti Claude Haiku 4.5 dapat menjadi pendekatan yang optimal:

1. Mulai implementasi dengan Claude Haiku 4.5
2. Uji kasus penggunaan Anda secara menyeluruh
3. Evaluasi apakah kinerja memenuhi persyaratan Anda
4. Tingkatkan hanya jika diperlukan untuk kesenjangan kemampuan tertentu

Pendekatan ini memungkinkan iterasi cepat, biaya pengembangan lebih rendah, dan sering kali cukup untuk banyak aplikasi umum. Pendekatan ini paling baik untuk:
- Prototyping dan pengembangan awal
- Aplikasi dengan persyaratan latensi ketat
- Implementasi yang sensitif terhadap biaya
- Tugas-tugas bervolume tinggi yang sederhana

### Opsi 2: Mulai dengan model yang paling mampu

Untuk tugas-tugas kompleks di mana kecerdasan dan kemampuan lanjutan adalah yang terpenting, Anda mungkin ingin memulai dengan model yang paling mampu dan kemudian mempertimbangkan untuk mengoptimalkan ke model yang lebih efisien di kemudian hari:

1. Implementasikan dengan Claude Opus 4.6
2. Optimalkan prompt Anda untuk model-model ini
3. Evaluasi apakah kinerja memenuhi persyaratan Anda
4. Pertimbangkan untuk meningkatkan efisiensi dengan menurunkan kecerdasan seiring waktu dengan optimasi alur kerja yang lebih besar

Pendekatan ini paling baik untuk:
- Tugas-tugas penalaran kompleks
- Aplikasi ilmiah atau matematis
- Tugas-tugas yang memerlukan pemahaman bernuansa
- Aplikasi di mana akurasi mengungguli pertimbangan biaya
- Pengkodean lanjutan

## Matriks pemilihan model

| Ketika Anda membutuhkan... | Kami merekomendasikan untuk memulai dengan... | Contoh kasus penggunaan |
|------------------|-------------------|-------------------|
| Claude Opus 4.6 adalah versi terbaru dari model paling cerdas kami, dan model terbaik di dunia untuk pengkodean, agen perusahaan, dan pekerjaan profesional. | Claude Opus 4.6 | Rekayasa perangkat lunak profesional, agen lanjutan untuk tugas kantor, penggunaan komputer dan browser dalam skala besar, tugas penelitian berdurasi multi-jam, aplikasi visi perubahan langkah |
| Kombinasi terbaik dari kecepatan dan kecerdasan untuk tugas-tugas sehari-hari | Claude Sonnet 4.5 | Pembuatan kode, analisis data, pembuatan konten, pemahaman visual, penggunaan alat agentic |
| Kinerja mendekati frontier dengan kecepatan kilat dan pemikiran yang diperluas pada titik harga paling ekonomis | Claude Haiku 4.5 | Aplikasi real-time, pemrosesan cerdas bervolume tinggi, penerapan sensitif biaya yang memerlukan penalaran kuat, tugas sub-agen |

***

## Tentukan apakah akan meningkatkan atau mengubah model

Untuk menentukan apakah Anda perlu meningkatkan atau mengubah model, Anda harus:
1. [Buat tes benchmark](/docs/id/test-and-evaluate/develop-tests) yang spesifik untuk kasus penggunaan Anda - memiliki set evaluasi yang baik adalah langkah paling penting dalam proses
2. Uji dengan prompt dan data aktual Anda
3. Bandingkan kinerja di seluruh model untuk:
   - Akurasi respons
   - Kualitas respons
   - Penanganan kasus tepi
4. Pertimbangkan pertukaran kinerja dan biaya

## Langkah berikutnya

<CardGroup cols={3}>
  <Card title="Bagan perbandingan model" icon="settings" href="/docs/id/about-claude/models/overview">
    Lihat spesifikasi terperinci dan harga untuk model Claude terbaru
  </Card>
  <Card title="Apa yang baru di Claude 4.6" icon="sparkle" href="/docs/id/about-claude/models/whats-new-claude-4-6">
    Jelajahi peningkatan terbaru dalam model Claude 4.6
  </Card>
  <Card title="Mulai membangun" icon="code" href="/docs/id/get-started">
    Mulai dengan panggilan API pertama Anda
  </Card>
</CardGroup>