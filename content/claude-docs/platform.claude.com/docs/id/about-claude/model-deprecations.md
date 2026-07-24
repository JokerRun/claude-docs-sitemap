---
source: platform
url: https://platform.claude.com/docs/id/about-claude/model-deprecations
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: cfc392ae38c79409b29ac1abd79b73daf1eee8cc4299e58d9a7a3ba98de74776
---

# Penghentian model

Lihat model Claude mana yang aktif, usang, atau dihentikan, dan temukan tanggal penghentian serta pengganti yang direkomendasikan untuk model dan parameter API.

---

Seiring diluncurkannya model yang lebih aman dan lebih mumpuni, Anthropic secara berkala menghentikan model yang lebih lama. Aplikasi yang bergantung pada model Anthropic mungkin memerlukan pembaruan sesekali agar tetap berfungsi. Pelanggan yang terdampak akan selalu diberi tahu melalui email dan di dokumentasi.

Halaman ini mencantumkan semua penghentian API, beserta pengganti yang direkomendasikan.

## Ikhtisar

Anthropic menggunakan istilah berikut untuk menggambarkan siklus hidup model:

* **Active:** Model didukung sepenuhnya dan direkomendasikan untuk digunakan.
* **Legacy:** Model tidak akan lagi menerima pembaruan dan mungkin akan diusangkan di masa mendatang.
* **Deprecated:** Model masih berfungsi tetapi tidak lagi direkomendasikan. Anthropic menyediakan pengganti yang direkomendasikan dan menetapkan tanggal penghentian.
* **Retired:** Model tidak lagi tersedia untuk digunakan. Permintaan ke model yang telah dihentikan akan gagal.

<Warning>
  Model yang usang (deprecated) kemungkinan kurang andal dibandingkan model aktif. Pindahkan beban kerja ke model aktif untuk mempertahankan tingkat dukungan dan keandalan tertinggi.
</Warning>

Tanggal-tanggal di halaman ini berlaku untuk platform yang dioperasikan Anthropic: Claude API, [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Platform yang dioperasikan mitra (Amazon Bedrock dan Google Cloud) menetapkan jadwal penghentian mereka sendiri, sehingga status siklus hidup dan tanggal suatu model dapat berbeda. Lihat tabel model [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock#supported-models), [Amazon Bedrock (Opus 4.6 dan sebelumnya)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#api-model-ids), dan [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai#api-model-ids).

## Bermigrasi ke pengganti

Setelah sebuah model diusangkan, migrasikan semua penggunaan ke pengganti yang sesuai sebelum tanggal penghentian. Permintaan ke model yang telah melewati tanggal penghentian akan gagal.

Untuk membantu mengukur kinerja model pengganti pada tugas-tugas Anda, pertimbangkan untuk melakukan pengujian menyeluruh terhadap aplikasi Anda dengan model baru jauh sebelum tanggal penghentian.

Untuk instruksi spesifik tentang migrasi ke model Claude terbaru, lihat [Panduan migrasi](/docs/id/about-claude/models/migration-guide).

## Notifikasi

Anthropic memberi tahu pelanggan dengan deployment aktif untuk model yang akan segera dihentikan, dengan memberikan pemberitahuan setidaknya 60 hari sebelum penghentian model untuk model yang dirilis secara publik.

## Mengaudit penggunaan model

Untuk membantu mengidentifikasi penggunaan model yang usang, pelanggan dapat mengakses audit penggunaan API mereka. Ikuti langkah-langkah berikut:

1. Buka halaman [Usage](/usage) di Claude Console.
2. Klik **Export**.
3. Tinjau CSV yang diunduh untuk melihat penggunaan yang dirinci berdasarkan kunci API dan model.

Audit ini akan membantu Anda menemukan setiap bagian di mana aplikasi Anda masih menggunakan model yang usang, sehingga Anda dapat memprioritaskan pembaruan ke model yang lebih baru sebelum tanggal penghentian.

## Praktik terbaik

1. Periksa dokumentasi secara berkala untuk pembaruan tentang penghentian model.
2. Uji aplikasi Anda dengan model yang lebih baru jauh sebelum tanggal penghentian model Anda saat ini.
3. Perbarui kode Anda untuk menggunakan model pengganti yang direkomendasikan sesegera mungkin.
4. Hubungi tim dukungan jika Anda memerlukan bantuan dengan migrasi atau memiliki pertanyaan.

## Kekurangan penghentian dan mitigasinya

Anthropic saat ini mengusangkan dan menghentikan model untuk memastikan kapasitas bagi rilis model baru. Hal ini memiliki kekurangan:

* Pengguna yang menghargai model tertentu harus bermigrasi ke versi baru
* Peneliti kehilangan akses ke model untuk studi yang sedang berlangsung dan studi komparatif
* Penghentian model menimbulkan risiko terkait keselamatan dan kesejahteraan model

Pada suatu saat, Anthropic berharap dapat membuat model-model lama tersedia kembali untuk publik. Sementara itu, Anthropic telah berkomitmen pada pelestarian jangka panjang bobot model dan langkah-langkah lain untuk membantu memitigasi dampak ini. Untuk detail lebih lanjut, lihat [Commitments on Model Deprecation and Preservation](https://www.anthropic.com/research/deprecation-commitments).

## Status model

<Note>
  [Claude Mythos Preview](https://anthropic.com/glasswing) (`claude-mythos-preview`) akan dihentikan pada 21 Juli 2026. Untuk bermigrasi ke [Claude Mythos 5](https://anthropic.com/glasswing) (`claude-mythos-5`), lihat [panduan migrasi](/docs/id/about-claude/models/migration-guide#migrating-from-claude-mythos-preview).
</Note>

Model saat ini dan yang baru saja dihentikan tercantum dalam tabel berikut beserta statusnya:

| Nama model API             | Status saat ini | Diusangkan       | Tanggal penghentian tentatif             |
| -------------------------- | --------------- | ---------------- | ---------------------------------------- |
| claude-fable-5             | Active          | N/A              | Tidak lebih cepat dari 9 Juni 2027       |
| claude-opus-4-8            | Active          | N/A              | Tidak lebih cepat dari 28 Mei 2027       |
| claude-opus-4-7            | Active          | N/A              | Tidak lebih cepat dari 16 April 2027     |
| claude-opus-4-6            | Active          | N/A              | Tidak lebih cepat dari 5 Februari 2027   |
| claude-opus-4-5-20251101   | Active          | N/A              | Tidak lebih cepat dari 24 November 2026  |
| claude-opus-4-1-20250805   | Deprecated      | 5 Juni 2026      | 5 Agustus 2026                           |
| claude-opus-4-20250514     | Retired         | 14 April 2026    | 15 Juni 2026                             |
| claude-sonnet-5            | Active          | N/A              | Tidak lebih cepat dari 30 Juni 2027      |
| claude-sonnet-4-6          | Active          | N/A              | Tidak lebih cepat dari 17 Februari 2027  |
| claude-sonnet-4-5-20250929 | Active          | N/A              | Tidak lebih cepat dari 29 September 2026 |
| claude-sonnet-4-20250514   | Retired         | 14 April 2026    | 15 Juni 2026                             |
| claude-3-7-sonnet-20250219 | Retired         | 28 Oktober 2025  | 19 Februari 2026                         |
| claude-haiku-4-5-20251001  | Active          | N/A              | Tidak lebih cepat dari 15 Oktober 2026   |
| claude-3-5-haiku-20241022  | Retired         | 19 Desember 2025 | 19 Februari 2026                         |
| claude-3-haiku-20240307    | Retired         | 19 Februari 2026 | 20 April 2026                            |

## Riwayat penghentian

Semua penghentian tercantum di bagian berikut, dengan pengumuman terbaru terlebih dahulu.

### 2026-06-05: Model Claude Opus 4.1

Pada 5 Juni 2026, Anthropic memberi tahu pengembang yang menggunakan Claude Opus 4.1 tentang penghentiannya yang akan datang di Claude API.

| Tanggal penghentian | Model yang diusangkan      | Pengganti yang direkomendasikan |
| ------------------- | -------------------------- | ------------------------------- |
| 5 Agustus 2026      | `claude-opus-4-1-20250805` | `claude-opus-4-8`               |

### 2026-04-14: Model Claude Sonnet 4 dan Claude Opus 4

<Note>
  Model-model ini dihentikan pada 15 Juni 2026.
</Note>

Pada 14 April 2026, Anthropic memberi tahu pengembang yang menggunakan model Claude Sonnet 4 dan Claude Opus 4 tentang penghentiannya yang akan datang di Claude API.

| Tanggal penghentian | Model yang diusangkan      | Pengganti yang direkomendasikan |
| ------------------- | -------------------------- | ------------------------------- |
| 15 Juni 2026        | `claude-sonnet-4-20250514` | `claude-sonnet-4-6`             |
| 15 Juni 2026        | `claude-opus-4-20250514`   | `claude-opus-4-8`               |

### 2026-02-19: Model Claude Haiku 3

<Note>
  Model ini dihentikan pada 20 April 2026.
</Note>

Pada 19 Februari 2026, Anthropic memberi tahu pengembang yang menggunakan model Claude Haiku 3 tentang penghentiannya yang akan datang di Claude API.

| Tanggal penghentian | Model yang diusangkan     | Pengganti yang direkomendasikan |
| ------------------- | ------------------------- | ------------------------------- |
| 20 April 2026       | `claude-3-haiku-20240307` | `claude-haiku-4-5-20251001`     |

### 2025-12-19: Model Claude Haiku 3.5

<Note>
  Model ini dihentikan pada 19 Februari 2026.
</Note>

Pada 19 Desember 2025, Anthropic memberi tahu pengembang yang menggunakan model Claude Haiku 3.5 tentang penghentiannya yang akan datang di Claude API.

| Tanggal penghentian | Model yang diusangkan       | Pengganti yang direkomendasikan |
| ------------------- | --------------------------- | ------------------------------- |
| 19 Februari 2026    | `claude-3-5-haiku-20241022` | `claude-haiku-4-5-20251001`     |

### 2025-10-28: Model Claude Sonnet 3.7

<Note>
  Model ini dihentikan pada 19 Februari 2026.
</Note>

Pada 28 Oktober 2025, Anthropic memberi tahu pengembang yang menggunakan model Claude Sonnet 3.7 tentang penghentiannya yang akan datang di Claude API.

| Tanggal penghentian | Model yang diusangkan        | Pengganti yang direkomendasikan |
| ------------------- | ---------------------------- | ------------------------------- |
| 19 Februari 2026    | `claude-3-7-sonnet-20250219` | `claude-sonnet-4-6`             |

### 2025-08-13: Model Claude Sonnet 3.5

<Note>
  Model-model ini dihentikan pada 28 Oktober 2025.
</Note>

Pada 13 Agustus 2025, Anthropic memberi tahu pengembang yang menggunakan model Claude Sonnet 3.5 tentang penghentiannya yang akan datang.

| Tanggal penghentian | Model yang diusangkan        | Pengganti yang direkomendasikan |
| ------------------- | ---------------------------- | ------------------------------- |
| 28 Oktober 2025     | `claude-3-5-sonnet-20240620` | `claude-sonnet-4-6`             |
| 28 Oktober 2025     | `claude-3-5-sonnet-20241022` | `claude-sonnet-4-6`             |

### 2025-06-30: Model Claude Opus 3

<Note>
  Model ini dihentikan pada 5 Januari 2026.
</Note>

Pada 30 Juni 2025, Anthropic memberi tahu pengembang yang menggunakan model Claude Opus 3 tentang penghentiannya yang akan datang.

| Tanggal penghentian | Model yang diusangkan    | Pengganti yang direkomendasikan |
| ------------------- | ------------------------ | ------------------------------- |
| 5 Januari 2026      | `claude-3-opus-20240229` | `claude-opus-4-8`               |

### 2025-01-21: Model Claude 2, Claude 2.1, dan Claude Sonnet 3

<Note>
  Model-model ini dihentikan pada 21 Juli 2025.
</Note>

Pada 21 Januari 2025, Anthropic memberi tahu pengembang yang menggunakan model Claude 2, Claude 2.1, dan Claude Sonnet 3 tentang penghentiannya yang akan datang.

| Tanggal penghentian | Model yang diusangkan      | Pengganti yang direkomendasikan |
| ------------------- | -------------------------- | ------------------------------- |
| 21 Juli 2025        | `claude-2.0`               | `claude-opus-4-8`               |
| 21 Juli 2025        | `claude-2.1`               | `claude-opus-4-8`               |
| 21 Juli 2025        | `claude-3-sonnet-20240229` | `claude-sonnet-4-6`             |

### 2024-09-04: Model Claude 1 dan Instant

<Note>
  Model-model ini dihentikan pada 6 November 2024.
</Note>

Pada 4 September 2024, Anthropic memberi tahu pengembang yang menggunakan model Claude 1 dan Instant tentang penghentiannya yang akan datang.

| Tanggal penghentian | Model yang diusangkan | Pengganti yang direkomendasikan |
| ------------------- | --------------------- | ------------------------------- |
| 6 November 2024     | `claude-1.0`          | `claude-haiku-4-5-20251001`     |
| 6 November 2024     | `claude-1.1`          | `claude-haiku-4-5-20251001`     |
| 6 November 2024     | `claude-1.2`          | `claude-haiku-4-5-20251001`     |
| 6 November 2024     | `claude-1.3`          | `claude-haiku-4-5-20251001`     |
| 6 November 2024     | `claude-instant-1.0`  | `claude-haiku-4-5-20251001`     |
| 6 November 2024     | `claude-instant-1.1`  | `claude-haiku-4-5-20251001`     |
| 6 November 2024     | `claude-instant-1.2`  | `claude-haiku-4-5-20251001`     |

## Penghentian parameter API

Anthropic sesekali mengusangkan parameter permintaan yang tidak lagi berlaku untuk model saat ini. Parameter yang usang tetap ada dalam tipe permintaan SDK sehingga kode yang ada tetap lolos pemeriksaan tipe, tetapi perilakunya berubah per model.

| Parameter                       | Status                                           | Perilaku                                                                                                                                                 | Pengganti yang direkomendasikan                                                                                                                |
| ------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `temperature`, `top_p`, `top_k` | Deprecated (Claude Opus 4.7 dan yang lebih baru) | Mengembalikan error 400 ketika diatur ke nilai non-default pada Claude Opus 4.7 dan yang lebih baru, termasuk Claude Opus 4.8, dan pada Claude Sonnet 5. | Hilangkan dan gunakan [prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk memandu perilaku model. |

Untuk langkah-langkah migrasi, lihat [panduan migrasi](/docs/id/about-claude/models/migration-guide).
