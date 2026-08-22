---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/choosing-a-model
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: 84e8c8b505978a78c0c8447937b96b027992c1bcb1df8ed11d8df91b76730c98
---

---
title: Memilih model yang tepat
url: https://platform.claude.com/docs/id/about-claude/models/choosing-a-model
description: "Memilih model Claude yang optimal untuk aplikasi Anda melibatkan penyeimbangan tiga pertimbangan utama: kemampuan, kecepatan, dan biaya. Panduan ini membantu Anda membuat keputusan yang tepat berdasarkan kebutuhan spesifik Anda."
---

## Tetapkan kriteria utama

Saat memilih model Claude, pertimbangkan untuk mengevaluasi faktor-faktor berikut terlebih dahulu:

* **Kemampuan:** Fitur atau kemampuan spesifik apa yang Anda perlukan dari model untuk memenuhi kebutuhan Anda?
* **Kecepatan:** Seberapa cepat model perlu merespons dalam aplikasi Anda? Claude Opus 5 dan Claude Opus 4.8 mendukung [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset), yang memberikan kecepatan output hingga 2,5x lebih tinggi dengan harga premium.
* **Biaya:** Berapa anggaran Anda untuk penggunaan pengembangan maupun produksi?
* **Effort:** Model Opus dan Sonnet terbaru mendukung [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang menukar kecerdasan dengan latensi dan biaya dalam satu model. Menyetel effort sering kali merupakan tuas yang lebih baik daripada berganti model. Pada Claude Opus 5, mulailah dengan default (`high`) dan sesuaikan naik atau turun berdasarkan evaluasi Anda. Pada Claude Opus 4.8 dan Claude Opus 4.7, tingkat effort `xhigh`, di antara `high` dan `max`, adalah pengaturan terbaik untuk sebagian besar kasus penggunaan coding dan agentik.

Mengetahui jawaban-jawaban ini sebelumnya akan membuat proses mempersempit pilihan dan memutuskan model mana yang akan digunakan menjadi jauh lebih mudah.

***

## Pilih model terbaik untuk memulai

Ada dua pendekatan umum yang dapat Anda gunakan untuk mulai menguji model Claude mana yang paling sesuai dengan kebutuhan Anda.

### Opsi 1: Mulai dengan mengutamakan efisiensi

Untuk banyak aplikasi, memulai dengan model yang lebih cepat dan lebih hemat biaya seperti Claude Haiku 4.5 dapat menjadi pendekatan yang optimal:

1. Mulai implementasi dengan Claude Haiku 4.5.
2. Uji kasus penggunaan Anda secara menyeluruh.
3. Evaluasi apakah kinerja memenuhi kebutuhan Anda.
4. Tingkatkan hanya jika diperlukan untuk kesenjangan kemampuan tertentu.

Pendekatan ini memungkinkan iterasi yang cepat, biaya pengembangan yang lebih rendah, dan sering kali sudah memadai untuk banyak aplikasi umum. Pendekatan ini paling cocok untuk:

* Pembuatan prototipe dan pengembangan awal
* Aplikasi dengan persyaratan latensi yang ketat
* Implementasi yang sensitif terhadap biaya
* Tugas bervolume tinggi yang sederhana

### Opsi 2: Mulai dengan mengutamakan kemampuan

Untuk tugas kompleks di mana kecerdasan dan kemampuan tingkat lanjut sangat penting, Anda mungkin ingin memulai dengan mengutamakan kemampuan: implementasikan dengan titik awal terkuat untuk tugas Anda, lalu optimalkan ke model yang lebih efisien di kemudian hari:

1. Implementasikan dengan Claude Opus 5.
2. [Optimalkan prompt Anda](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5) untuk model ini.
3. Evaluasi apakah kinerja memenuhi kebutuhan Anda.
4. Pertimbangkan untuk meningkatkan efisiensi dengan menurunkan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) atau menurunkan tingkat model seiring waktu dengan optimalisasi alur kerja yang lebih baik.

Pendekatan ini paling cocok untuk:

* Tugas penalaran yang kompleks
* Aplikasi ilmiah atau matematis
* Tugas yang memerlukan pemahaman bernuansa
* Aplikasi di mana akurasi lebih penting daripada pertimbangan biaya
* Coding tingkat lanjut dan pekerjaan agentik dengan otonomi tinggi

<Note>
  [Parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) secara default bernilai `high` pada Claude Opus 5 dan Claude Opus 4.8, termasuk di Claude Code dan Messages API. Pada Claude Opus 5, mulailah dari default dan naikkan ke `xhigh` untuk pekerjaan coding dan agentik yang paling menuntut. Pada Claude Opus 4.8, gunakan `xhigh` untuk coding, pekerjaan dengan otonomi tinggi, dan tugas yang paling menuntut kecerdasan.
</Note>

**Claude Opus 5** (`claude-opus-5`) adalah peningkatan besar dibandingkan Claude Opus 4.8, unggul dalam penalaran mendalam, tugas agentik dan berjangka panjang, serta penskalaan komputasi saat pengujian (test-time compute scaling). Claude Opus 5 mendukung "context window" (jendela konteks) 1 juta token secara default dan hingga 128 ribu token output, dengan harga $5 USD per juta token input dan $25 USD per juta token output.

**Claude Fable 5** (`claude-fable-5`) adalah model Anthropic paling mumpuni yang dirilis secara luas, menghadirkan kecerdasan generasi berikutnya untuk agen yang berjalan lama. **Claude Mythos 5** (`claude-mythos-5`) tersedia melalui [Project Glasswing](https://anthropic.com/glasswing). Kedua model mendukung jendela konteks 1 juta token secara default, hingga 128 ribu token output, dan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) yang selalu aktif. Lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) untuk detail peluncuran.

Claude Fable 5 dan Claude Mythos 5 dihargai $10 USD per juta token input dan $50 USD per juta token output.

## Matriks pemilihan model

| Ketika Anda membutuhkan...                                                                                            | Pertimbangkan untuk memulai dengan... | Contoh kasus penggunaan                                                                                                                                                                                                 |
| --------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Kemampuan tertinggi yang tersedia                                                                                     | Claude Fable 5                        | Agen yang berjalan lama, penalaran mendalam, tugas agentik berjangka panjang, riset tingkat lanjut                                                                                                                      |
| Coding agentik yang kompleks dan pekerjaan enterprise                                                                 | Claude Opus 5                         | Agen coding otonom yang berjalan berjam-jam, refactoring skala besar, rekayasa sistem yang kompleks, riset tingkat lanjut, pekerjaan berbasis pengetahuan, alur kerja yang banyak menggunakan visi, penggunaan komputer |
| Kecerdasan terdepan dalam skala besar, dibangun untuk coding, agen, dan alur kerja enterprise                         | Claude Sonnet 5                       | Pembuatan kode, analisis data, pembuatan konten, pemahaman visual, penggunaan alat agentik                                                                                                                              |
| Kinerja mendekati terdepan dengan kecepatan sangat tinggi dan pemikiran diperpanjang pada titik harga paling ekonomis | Claude Haiku 4.5                      | Aplikasi real-time, pemrosesan cerdas bervolume tinggi, deployment sensitif biaya yang membutuhkan penalaran kuat, tugas sub-agen                                                                                       |

***

## Putuskan apakah perlu meningkatkan atau mengganti model

Untuk menentukan apakah Anda perlu meningkatkan atau mengganti model, Anda sebaiknya:

1. [Membuat pengujian benchmark](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests) yang spesifik untuk kasus penggunaan Anda - memiliki set evaluasi yang baik adalah langkah terpenting dalam proses ini.

2. Menguji dengan prompt dan data Anda yang sebenarnya.

3. Membandingkan kinerja antar model untuk:

   * Akurasi respons
   * Kualitas respons
   * Penanganan kasus tepi (edge case)

4. Menimbang tradeoff antara kinerja dan biaya.

## Kombinasikan model

Strategi multi-model memasangkan model berbiaya lebih rendah dengan model terdepan sehingga sebagian besar token ditagih dengan tarif yang lebih rendah. Dua pola yang umum adalah eksekutor yang mengeskalasi keputusan sulit ke penasihat, dan orkestrator yang mendelegasikan pekerjaan massal ke pekerja berbiaya lebih rendah. Lihat [Mengoptimalkan biaya dan kecerdasan](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence) untuk kedua strategi tersebut, contoh terukur, dan opsi implementasi.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Bagan perbandingan model" icon="settings" href="https://platform.claude.com/docs/id/about-claude/models/overview">
    Lihat spesifikasi terperinci dan harga untuk model Claude terbaru
  </Card>

  <Card title="Yang baru di Claude Opus 5" icon="sparkle" href="https://platform.claude.com/docs/id/about-claude/models/whats-new-opus-5">
    Jelajahi peningkatan terbaru di Claude Opus 5
  </Card>

  <Card title="Yang baru di Claude Sonnet 5" icon="sparkle" href="https://platform.claude.com/docs/id/about-claude/models/whats-new-sonnet-5">
    Kombinasi terbaik antara kecepatan dan kecerdasan
  </Card>

  <Card title="Mulai membangun" icon="code" href="https://platform.claude.com/docs/id/get-started">
    Mulai dengan panggilan API pertama Anda
  </Card>
</CardGroup>
