---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/choosing-a-model
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: d277781b90159e88f57f98317d9724b0239ecd839e4edb27633a900c974f7cc1
---

# Memilih model yang tepat

Memilih model Claude yang optimal untuk aplikasi Anda melibatkan penyeimbangan tiga pertimbangan utama: kapabilitas, kecepatan, dan biaya. Panduan ini membantu Anda membuat keputusan yang tepat berdasarkan kebutuhan spesifik Anda.

---

## Tetapkan kriteria utama

Saat memilih model Claude, pertimbangkan untuk mengevaluasi faktor-faktor berikut terlebih dahulu:

* **Kapabilitas:** Fitur atau kapabilitas spesifik apa yang Anda perlukan dari model untuk memenuhi kebutuhan Anda?
* **Kecepatan:** Seberapa cepat model perlu merespons dalam aplikasi Anda? Claude Opus 4.8 dan Claude Opus 4.7 mendukung [fast mode](/docs/id/build-with-claude/fast-mode) (pratinjau riset), yang memberikan kecepatan output hingga 2,5x lebih tinggi dengan harga premium. Fast mode pada Claude Opus 4.7 sudah tidak digunakan lagi (deprecated), dengan penghapusan pada 24 Juli 2026.
* **Biaya:** Berapa anggaran Anda untuk penggunaan pengembangan dan produksi?
* **Effort:** Model Opus dan Sonnet terbaru mendukung [parameter effort](/docs/id/build-with-claude/effort) yang menukar kecerdasan dengan latensi dan biaya dalam satu model. Menyesuaikan effort sering kali merupakan tuas yang lebih baik daripada beralih model. Pada Claude Opus 4.8 dan Claude Opus 4.7, level effort `xhigh`, yang berada di antara `high` dan `max`, adalah pengaturan terbaik untuk sebagian besar kasus penggunaan coding dan agentic.

Mengetahui jawaban-jawaban ini sebelumnya akan membuat proses mempersempit pilihan dan memutuskan model mana yang akan digunakan menjadi jauh lebih mudah.

***

## Pilih model terbaik untuk memulai

Ada dua pendekatan umum yang dapat Anda gunakan untuk mulai menguji model Claude mana yang paling sesuai dengan kebutuhan Anda.

### Opsi 1: Mulai dengan model yang cepat dan hemat biaya

Untuk banyak aplikasi, memulai dengan model yang lebih cepat dan lebih hemat biaya seperti Claude Haiku 4.5 dapat menjadi pendekatan yang optimal:

1. Mulai implementasi dengan Claude Haiku 4.5.
2. Uji kasus penggunaan Anda secara menyeluruh.
3. Evaluasi apakah performa memenuhi kebutuhan Anda.
4. Tingkatkan hanya jika diperlukan untuk mengatasi kesenjangan kapabilitas tertentu.

Pendekatan ini memungkinkan iterasi yang cepat, biaya pengembangan yang lebih rendah, dan sering kali sudah memadai untuk banyak aplikasi umum. Pendekatan ini paling cocok untuk:

* Pembuatan prototipe awal dan pengembangan
* Aplikasi dengan persyaratan latensi yang ketat
* Implementasi yang sensitif terhadap biaya
* Tugas bervolume tinggi yang sederhana

### Opsi 2: Mulai dengan model yang paling mumpuni

Untuk tugas kompleks di mana kecerdasan dan kapabilitas tingkat lanjut sangat penting, Anda mungkin ingin memulai dengan model yang paling mumpuni, lalu mempertimbangkan untuk mengoptimalkan ke model yang lebih efisien di kemudian hari:

1. Implementasikan dengan Claude Opus 4.8.
2. Optimalkan prompt Anda untuk model-model ini.
3. Evaluasi apakah performa memenuhi kebutuhan Anda.
4. Pertimbangkan untuk meningkatkan efisiensi dengan menurunkan [effort](/docs/id/build-with-claude/effort) atau menurunkan tingkat model seiring waktu dengan optimasi alur kerja yang lebih baik.

Pendekatan ini paling cocok untuk:

* Tugas penalaran yang kompleks
* Aplikasi ilmiah atau matematis
* Tugas yang memerlukan pemahaman bernuansa
* Aplikasi di mana akurasi lebih penting daripada pertimbangan biaya
* Coding tingkat lanjut dan pekerjaan agentic dengan otonomi tinggi

<Note>
  [Parameter effort](/docs/id/build-with-claude/effort) secara default diatur ke `high` pada Claude Opus 4.8 di semua antarmuka, termasuk Claude Code dan Messages API. Gunakan `xhigh` untuk coding, pekerjaan dengan otonomi tinggi, dan tugas yang paling menuntut kecerdasan.
</Note>

**Claude Fable 5** (`claude-fable-5`) adalah model Anthropic paling mumpuni yang dirilis secara luas, menghadirkan kecerdasan generasi berikutnya untuk agen yang berjalan dalam jangka panjang. **Claude Mythos 5** (`claude-mythos-5`) tersedia melalui [Project Glasswing](https://anthropic.com/glasswing). Kedua model mendukung jendela konteks 1 juta token secara default, hingga 128 ribu token output, dan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) yang selalu aktif. Lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) untuk detail peluncuran.

Claude Fable 5 dan Claude Mythos 5 dihargai $10 per juta token input dan $50 per juta token output.

## Matriks pemilihan model

| Ketika Anda membutuhkan...                                                                                             | Pertimbangkan untuk memulai dengan... | Contoh kasus penggunaan                                                                                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Coding agentic yang kompleks dan pekerjaan enterprise                                                                  | Claude Opus 4.8                       | Agen coding otonom yang berjalan berjam-jam, refactoring skala besar, rekayasa sistem yang kompleks, riset tingkat lanjut, pekerjaan berbasis pengetahuan, alur kerja yang banyak menggunakan visi, penggunaan komputer |
| Kecerdasan terdepan dalam skala besar, dibangun untuk coding, agen, dan alur kerja enterprise                          | Claude Sonnet 5                       | Pembuatan kode, analisis data, pembuatan konten, pemahaman visual, penggunaan alat agentic                                                                                                                              |
| Performa mendekati terdepan dengan kecepatan sangat tinggi dan pemikiran diperpanjang pada titik harga paling ekonomis | Claude Haiku 4.5                      | Aplikasi real-time, pemrosesan cerdas bervolume tinggi, deployment yang sensitif terhadap biaya namun membutuhkan penalaran yang kuat, tugas sub-agen                                                                   |

***

## Tentukan apakah perlu meningkatkan atau mengganti model

Untuk menentukan apakah Anda perlu meningkatkan atau mengganti model, Anda harus:

1. [Membuat pengujian benchmark](/docs/id/test-and-evaluate/develop-tests) yang spesifik untuk kasus penggunaan Anda - memiliki set evaluasi yang baik adalah langkah terpenting dalam proses ini.

2. Menguji dengan prompt dan data aktual Anda.

3. Membandingkan performa antar model untuk:

   * Akurasi respons
   * Kualitas respons
   * Penanganan kasus tepi (edge case)

4. Menimbang trade-off antara performa dan biaya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Bagan perbandingan model" icon="settings" href="/docs/id/about-claude/models/overview">
    Lihat spesifikasi detail dan harga untuk model Claude terbaru
  </Card>

  <Card title="Yang baru di Claude Opus 4.8" icon="sparkle" href="/docs/id/about-claude/models/whats-new-claude-4-8">
    Jelajahi peningkatan terbaru di Claude Opus 4.8
  </Card>

  <Card title="Yang baru di Claude Sonnet 5" icon="sparkle" href="/docs/id/about-claude/models/whats-new-sonnet-5">
    Kombinasi terbaik antara kecepatan dan kecerdasan
  </Card>

  <Card title="Mulai membangun" icon="code" href="/docs/id/get-started">
    Mulai dengan panggilan API pertama Anda
  </Card>
</CardGroup>
