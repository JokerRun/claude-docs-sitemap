---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/choosing-a-model
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 0b758fe2f893c45745f2194caeffcf51f8c0a499bed85c6f012d65359a488adc
---

---
title: Memilih model yang tepat
url: https://platform.claude.com/docs/id/about-claude/models/choosing-a-model
description: Memilih model Claude berarti menyeimbangkan kemampuan, kecepatan, dan biaya. Panduan ini membahas pertanyaan yang perlu diajukan, dua cara untuk memilih model awal, dan cara menguji pilihan tersebut.
---

## Tetapkan kriteria utama

Saat memilih model Claude, pertimbangkan untuk mengevaluasi faktor-faktor berikut terlebih dahulu:

* **Kemampuan:** Fitur atau kemampuan spesifik apa yang Anda perlukan dari model untuk memenuhi kebutuhan Anda?
* **Kecepatan:** Seberapa cepat model perlu merespons dalam aplikasi Anda? Claude Opus 5 dan Claude Opus 4.8 mendukung [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset), yang memberikan kecepatan output hingga 2,5x lebih tinggi dengan harga premium.
* **Biaya:** Berapa anggaran Anda untuk penggunaan pengembangan maupun produksi?
* **Effort:** Beberapa model Claude mendukung [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang menukar kecerdasan dengan latensi dan biaya dalam satu model. Menyetel effort sering kali merupakan tuas yang lebih baik daripada berganti model. Pada Claude Fable 5.1 dan Claude Opus 5, mulailah dengan nilai default (`high`) dan sesuaikan naik atau turun berdasarkan evaluasi Anda. Pada Claude Opus 4.8 dan Claude Opus 4.7, tingkat effort `xhigh`, di antara `high` dan `max`, adalah pengaturan terbaik untuk sebagian besar kasus penggunaan coding dan agentik.

***

## Pilih model terbaik untuk memulai

Ada dua pendekatan umum yang dapat Anda gunakan untuk mulai menguji model Claude mana yang paling sesuai dengan kebutuhan Anda.

### Opsi 1: Mulai dengan mengutamakan efisiensi

Untuk banyak aplikasi, memulai dengan model yang lebih cepat dan lebih hemat biaya seperti Claude Haiku 4.5 dapat menjadi pendekatan yang optimal:

1. Mulai implementasi dengan Claude Haiku 4.5.
2. Uji kasus penggunaan Anda secara menyeluruh.
3. Evaluasi apakah kinerja memenuhi persyaratan Anda.
4. Tingkatkan hanya jika diperlukan untuk kesenjangan kemampuan tertentu.

Pendekatan ini memungkinkan iterasi cepat, biaya pengembangan yang lebih rendah, dan sering kali sudah memadai untuk banyak aplikasi umum. Pendekatan ini paling cocok untuk:

* Pembuatan prototipe dan pengembangan awal
* Aplikasi dengan persyaratan latensi yang ketat
* Implementasi yang sensitif terhadap biaya
* Tugas bervolume tinggi yang sederhana

### Opsi 2: Mulai dengan mengutamakan kemampuan

Untuk tugas kompleks di mana kecerdasan dan kemampuan tingkat lanjut sangat penting, Anda mungkin ingin memulai dengan mengutamakan kemampuan: implementasikan dengan titik awal terkuat untuk tugas Anda, lalu optimalkan ke model yang lebih efisien di kemudian hari:

1. Implementasikan dengan Claude Opus 5.
2. [Optimalkan prompt Anda](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5) untuk model ini.
3. Evaluasi apakah kinerja memenuhi persyaratan Anda.
4. Pertimbangkan untuk meningkatkan efisiensi dengan menurunkan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) atau menurunkan tingkat model seiring waktu dengan optimalisasi alur kerja yang lebih baik.
5. Jika evaluasi Anda pada effort `xhigh` atau `max` masih belum memadai untuk penalaran yang berat atau pekerjaan agentik berjangka panjang, beralihlah ke [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1).

Pendekatan ini paling cocok untuk:

* Tugas penalaran yang kompleks
* Aplikasi ilmiah atau matematika
* Tugas yang memerlukan pemahaman bernuansa
* Aplikasi di mana akurasi lebih penting daripada pertimbangan biaya
* Coding tingkat lanjut dan pekerjaan agentik dengan otonomi tinggi

**Claude Opus 5** (`claude-opus-5`) dibangun untuk coding agentik yang kompleks dan pekerjaan enterprise, dengan penalaran mendalam, tugas berjangka panjang, dan penskalaan komputasi saat pengujian (test-time compute scaling).

**Claude Fable 5.1** (`claude-fable-5-1`) adalah model Anthropic paling mumpuni yang dirilis secara luas. Model ini memperluas Claude Fable 5 dengan coding agentik jangka panjang, pekerjaan berbasis pengetahuan, dan riset yang lebih kuat dengan harga input dan output yang sama, dengan pembacaan cache seperempat dari biayanya. **Claude Mythos 5.1** (`claude-mythos-5-1`) menawarkan kemampuan yang sama hanya untuk peserta [Project Glasswing](https://anthropic.com/glasswing). Kedua model menggunakan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) yang selalu aktif. Lihat [Yang baru di Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1) untuk detailnya.

Claude Fable 5 dan Claude Mythos 5 juga tersedia. Lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5) untuk detailnya. Untuk "context window" (jendela konteks), batas output, dan harga, lihat [tabel perbandingan model](https://platform.claude.com/docs/id/models/overview#latest-models-comparison).

## Matriks pemilihan model

Sebagian besar beban kerja dimulai dengan Claude Opus 5.

| Ketika Anda membutuhkan...                                                         | Pertimbangkan untuk memulai dengan... | Contoh kasus penggunaan                                                                                                                                         |
| ---------------------------------------------------------------------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Kemampuan tertinggi yang tersedia                                                  | Claude Fable 5.1                      | Sesi agen yang berjalan selama berjam-jam, riset mendalam multilangkah, analisis yang dituntaskan hingga menjadi dokumen, spreadsheet, atau dek presentasi jadi |
| Coding agentik yang kompleks dan pekerjaan enterprise                              | Claude Opus 5                         | Agen coding otonom yang berjalan berjam-jam, refactoring skala besar, rekayasa sistem yang kompleks, alur kerja yang sarat visi, penggunaan komputer            |
| Kecepatan dan kemampuan untuk beban kerja coding, agen, dan enterprise sehari-hari | Claude Sonnet 5                       | Pembuatan kode, analisis data, pembuatan konten, pemahaman visual, penggunaan alat agentik                                                                      |
| Latensi dan harga terendah, dengan pemikiran diperpanjang                          | Claude Haiku 4.5                      | Aplikasi real-time, pemrosesan cerdas bervolume tinggi, deployment sensitif biaya yang membutuhkan penalaran kuat, tugas sub-agen                               |

***

## Putuskan apakah perlu meningkatkan atau mengganti model

Untuk menentukan apakah Anda perlu meningkatkan atau mengganti model, Anda sebaiknya:

1. [Membuat pengujian benchmark](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests) yang spesifik untuk kasus penggunaan Anda - memiliki set evaluasi yang baik adalah langkah terpenting dalam proses ini.

2. Menguji dengan prompt dan data aktual Anda.

3. Membandingkan kinerja antarmodel untuk:

   * Akurasi respons
   * Kualitas respons
   * Penanganan kasus tepi (edge case)

4. Menimbang tradeoff antara kinerja dan biaya.

## Gabungkan model

Strategi multi-model memasangkan model berbiaya lebih rendah dengan model frontier sehingga sebagian besar token ditagih dengan tarif yang lebih rendah. Dua pola yang umum adalah eksekutor yang mengeskalasi keputusan sulit ke penasihat, dan orkestrator yang mendelegasikan pekerjaan massal ke pekerja berbiaya lebih rendah. Lihat [Mengoptimalkan biaya dan kecerdasan](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence) untuk kedua strategi tersebut, contoh terukur, dan opsi implementasi.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Bagan perbandingan model" icon="settings" href="https://platform.claude.com/docs/id/models/overview">
    Lihat spesifikasi terperinci dan harga untuk model Claude terbaru
  </Card>

  <Card title="Yang baru di Claude Fable 5.1" icon="sparkle" href="https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1">
    Dibangun untuk penalaran yang berat dan pekerjaan agentik berjangka panjang
  </Card>

  <Card title="Yang baru di Claude Opus 5" icon="sparkle" href="https://platform.claude.com/docs/id/models/opus-5/whats-new-opus-5">
    Jelajahi peningkatan di Claude Opus 5
  </Card>

  <Card title="Yang baru di Claude Sonnet 5" icon="sparkle" href="https://platform.claude.com/docs/id/models/sonnet-5/whats-new-sonnet-5">
    Untuk beban kerja sehari-hari yang menyeimbangkan kecepatan dan kemampuan
  </Card>

  <Card title="Mulai membangun" icon="code" href="https://platform.claude.com/docs/id/get-started">
    Mulai dengan panggilan API pertama Anda
  </Card>
</CardGroup>
