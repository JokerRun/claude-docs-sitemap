---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/choosing-a-model
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: ed5a7b3cfa8201e080167e97490617b78559a5a6619d0e4b54a250a98c737a7b
---

# Memilih model yang tepat

Memilih model Claude yang optimal untuk aplikasi Anda melibatkan keseimbangan tiga pertimbangan utama: kemampuan, kecepatan, dan biaya. Panduan ini membantu Anda membuat keputusan yang tepat berdasarkan kebutuhan spesifik Anda.

---

## Tetapkan kriteria utama

Saat memilih model Claude, pertimbangkan untuk terlebih dahulu mengevaluasi faktor-faktor berikut:

* **Kemampuan:** Fitur atau kemampuan spesifik apa yang Anda perlukan dari model untuk memenuhi kebutuhan Anda?
* **Kecepatan:** Seberapa cepat model perlu merespons dalam aplikasi Anda? Claude Opus 4.8 dan Claude Opus 4.7 mendukung [fast mode](/docs/id/build-with-claude/fast-mode) (pratinjau riset), yang memberikan kecepatan output hingga 2,5x lebih tinggi dengan harga premium. Fast mode pada Claude Opus 4.7 sudah tidak digunakan lagi (deprecated), dengan penghapusan pada 24 Juli 2026.
* **Biaya:** Berapa anggaran Anda untuk penggunaan pengembangan dan produksi?
* **Effort:** Model Opus dan Sonnet terbaru mendukung [parameter effort](/docs/id/build-with-claude/effort) yang menukar kecerdasan dengan latensi dan biaya dalam satu model. Menyetel effort sering kali merupakan tuas yang lebih baik daripada berganti model. Pada Claude Opus 4.8 dan Claude Opus 4.7, tingkat effort `xhigh`, antara `high` dan `max`, adalah pengaturan terbaik untuk sebagian besar kasus penggunaan coding dan agentik.

Mengetahui jawaban-jawaban ini sebelumnya akan membuat proses mempersempit dan memutuskan model mana yang akan digunakan menjadi jauh lebih mudah.

***

## Pilih model terbaik untuk memulai

Ada dua pendekatan umum yang dapat Anda gunakan untuk mulai menguji model Claude mana yang paling sesuai dengan kebutuhan Anda.

### Opsi 1: Mulai dengan model yang cepat dan hemat biaya

Untuk banyak aplikasi, memulai dengan model yang lebih cepat dan lebih hemat biaya seperti Claude Haiku 4.5 dapat menjadi pendekatan yang optimal:

1. Mulai implementasi dengan Claude Haiku 4.5.
2. Uji kasus penggunaan Anda secara menyeluruh.
3. Evaluasi apakah kinerjanya memenuhi kebutuhan Anda.
4. Tingkatkan hanya jika diperlukan untuk kesenjangan kemampuan tertentu.

Pendekatan ini memungkinkan iterasi yang cepat, biaya pengembangan yang lebih rendah, dan sering kali sudah cukup untuk banyak aplikasi umum. Pendekatan ini paling cocok untuk:

* Pembuatan prototipe dan pengembangan awal
* Aplikasi dengan persyaratan latensi yang ketat
* Implementasi yang sensitif terhadap biaya
* Tugas bervolume tinggi dan sederhana

### Opsi 2: Mulai dengan model yang paling mumpuni

Untuk tugas kompleks di mana kecerdasan dan kemampuan tingkat lanjut adalah yang terpenting, Anda mungkin ingin memulai dengan model yang paling mumpuni dan kemudian mempertimbangkan untuk mengoptimalkan ke model yang lebih efisien di kemudian hari:

1. Implementasikan dengan Claude Opus 4.8.
2. Optimalkan prompt Anda untuk model-model ini.
3. Evaluasi apakah kinerjanya memenuhi kebutuhan Anda.
4. Pertimbangkan untuk meningkatkan efisiensi dengan menurunkan [effort](/docs/id/build-with-claude/effort) atau menurunkan tingkat model seiring waktu dengan optimalisasi alur kerja yang lebih baik.

Pendekatan ini paling cocok untuk:

* Tugas penalaran yang kompleks
* Aplikasi ilmiah atau matematis
* Tugas yang memerlukan pemahaman bernuansa
* Aplikasi di mana akurasi lebih penting daripada pertimbangan biaya
* Coding tingkat lanjut dan pekerjaan agentik dengan otonomi tinggi

<Note>
  [Parameter effort](/docs/id/build-with-claude/effort) secara default diatur ke `high` pada Claude Opus 4.8 di semua permukaan, termasuk Claude Code dan Messages API. Gunakan `xhigh` untuk coding, pekerjaan dengan otonomi tinggi, dan tugas yang paling menuntut kecerdasan.
</Note>

**Claude Fable 5** (`claude-fable-5`) adalah model Anthropic yang paling mumpuni yang dirilis secara luas, menghadirkan kecerdasan generasi berikutnya untuk agen yang berjalan lama. **Claude Mythos 5** (`claude-mythos-5`) tersedia melalui [Project Glasswing](https://anthropic.com/glasswing). Kedua model mendukung jendela konteks 1M token secara default, hingga 128k token output, dan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) yang selalu aktif. Lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) untuk detail peluncuran.

Claude Fable 5 dan Claude Mythos 5 dihargai $10 per juta token input dan $50 per juta token output.

## Matriks pemilihan model

| Ketika Anda membutuhkan...                                                                                            | Pertimbangkan untuk memulai dengan... | Contoh kasus penggunaan                                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Coding agentik kompleks dan pekerjaan enterprise                                                                      | Claude Opus 4.8                       | Agen coding otonom selama berjam-jam, refactoring skala besar, rekayasa sistem kompleks, riset tingkat lanjut, pekerjaan pengetahuan, alur kerja yang banyak menggunakan visi, penggunaan komputer |
| Kecerdasan terdepan dalam skala besar, dibangun untuk coding, agen, dan alur kerja enterprise                         | Claude Sonnet 5                       | Pembuatan kode, analisis data, pembuatan konten, pemahaman visual, penggunaan alat agentik                                                                                                         |
| Kinerja mendekati terdepan dengan kecepatan sangat tinggi dan pemikiran diperpanjang pada titik harga paling ekonomis | Claude Haiku 4.5                      | Aplikasi real-time, pemrosesan cerdas bervolume tinggi, penerapan yang sensitif terhadap biaya yang membutuhkan penalaran kuat, tugas sub-agen                                                     |

***

## Putuskan apakah akan meningkatkan atau mengganti model

Untuk menentukan apakah Anda perlu meningkatkan atau mengganti model, Anda harus:

1. [Membuat pengujian tolok ukur](/docs/id/test-and-evaluate/develop-tests) yang spesifik untuk kasus penggunaan Anda - memiliki set evaluasi yang baik adalah langkah terpenting dalam proses ini.

2. Menguji dengan prompt dan data Anda yang sebenarnya.

3. Membandingkan kinerja antar model untuk:

   * Akurasi respons
   * Kualitas respons
   * Penanganan kasus tepi (edge case)

4. Menimbang pertukaran antara kinerja dan biaya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Bagan perbandingan model" icon="settings" href="/docs/id/about-claude/models/overview">
    Lihat spesifikasi dan harga terperinci untuk model Claude terbaru
  </Card>

  <Card title="Apa yang baru di Claude Opus 4.8" icon="sparkle" href="/docs/id/about-claude/models/whats-new-claude-4-8">
    Jelajahi peningkatan terbaru di Claude Opus 4.8
  </Card>

  <Card title="Apa yang baru di Claude Sonnet 5" icon="sparkle" href="/docs/id/about-claude/models/whats-new-sonnet-5">
    Kombinasi terbaik antara kecepatan dan kecerdasan
  </Card>

  <Card title="Mulai membangun" icon="code" href="/docs/id/get-started">
    Mulai dengan panggilan API pertama Anda
  </Card>
</CardGroup>
