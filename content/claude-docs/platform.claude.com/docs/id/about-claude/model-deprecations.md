---
source: platform
url: https://platform.claude.com/docs/id/about-claude/model-deprecations
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 625b77a6619220a907f0cfc7cc03567b2b28a8350d0f505d5af1b4da9bf557e3
---

# Penghentian model

Informasi tentang penghentian model Anthropic, status model, dan panduan migrasi ke model pengganti yang direkomendasikan.

---

Seiring dengan peluncuran model yang lebih aman dan lebih mampu, Anthropic secara teratur menghentikan model yang lebih lama. Aplikasi yang mengandalkan model Anthropic mungkin memerlukan pembaruan sesekali untuk terus berfungsi. Pelanggan yang terdampak akan selalu diberitahu melalui email dan dalam dokumentasi.

Halaman ini mencantumkan semua penghentian API, beserta pengganti yang direkomendasikan.

## Ikhtisar

Anthropic menggunakan istilah berikut untuk menggambarkan siklus hidup model:
- **Aktif**: Model sepenuhnya didukung dan direkomendasikan untuk digunakan.
- **Warisan**: Model tidak akan lagi menerima pembaruan dan mungkin akan dihentikan di masa depan.
- **Dihentikan**: Model masih berfungsi tetapi tidak lagi direkomendasikan. Anthropic menyediakan pengganti yang direkomendasikan dan menetapkan tanggal penghentian.
- **Pensiun**: Model tidak lagi tersedia untuk digunakan. Permintaan ke model yang pensiun akan gagal.

<Warning>
Model yang dihentikan kemungkinan akan kurang andal daripada model aktif. Pindahkan beban kerja ke model aktif untuk mempertahankan tingkat dukungan dan keandalan tertinggi.
</Warning>

## Migrasi ke pengganti

Setelah model dihentikan, migrasikan semua penggunaan ke pengganti yang sesuai sebelum tanggal penghentian. Permintaan ke model setelah tanggal penghentian akan gagal.

Untuk membantu mengukur kinerja model pengganti pada tugas Anda, pertimbangkan pengujian menyeluruh aplikasi Anda dengan model baru jauh sebelum tanggal penghentian.

Untuk instruksi spesifik tentang migrasi ke model Claude terbaru, lihat [Panduan migrasi](/docs/id/about-claude/models/migration-guide).

## Pemberitahuan

Anthropic memberitahu pelanggan dengan penerapan aktif untuk model dengan penghentian yang akan datang, memberikan pemberitahuan minimal 60 hari sebelum penghentian model untuk model yang dirilis secara publik.

## Audit penggunaan model

Untuk membantu mengidentifikasi penggunaan model yang dihentikan, pelanggan dapat mengakses audit penggunaan API mereka. Ikuti langkah-langkah berikut:

1. Buka halaman [Penggunaan](/usage) di Console
2. Klik tombol "Ekspor"
3. Tinjau CSV yang diunduh untuk melihat penggunaan yang dipecah berdasarkan kunci API dan model

Audit ini akan membantu Anda menemukan instans apa pun di mana aplikasi Anda masih menggunakan model yang dihentikan, memungkinkan Anda memprioritaskan pembaruan ke model yang lebih baru sebelum tanggal penghentian.

## Praktik terbaik

1. Periksa dokumentasi secara teratur untuk pembaruan tentang penghentian model.
2. Uji aplikasi Anda dengan model yang lebih baru jauh sebelum tanggal penghentian model saat ini Anda.
3. Perbarui kode Anda untuk menggunakan model pengganti yang direkomendasikan sesegera mungkin.
4. Hubungi tim dukungan jika Anda memerlukan bantuan dengan migrasi atau memiliki pertanyaan apa pun.

## Kelemahan penghentian dan mitigasi

Anthropic saat ini menghentikan dan menonaktifkan model untuk memastikan kapasitas untuk rilis model baru. Ini datang dengan kelemahan:
- Pengguna yang menghargai model tertentu harus bermigrasi ke versi baru
- Peneliti kehilangan akses ke model untuk studi berkelanjutan dan komparatif
- Penghentian model memperkenalkan risiko terkait keselamatan dan kesejahteraan model

Pada suatu titik, Anthropic berharap dapat membuat model masa lalu tersedia untuk publik lagi. Sementara itu, Anthropic telah berkomitmen untuk pelestarian jangka panjang bobot model dan langkah-langkah lain untuk membantu mengurangi dampak ini. Untuk detail lebih lanjut, lihat [Komitmen pada Penghentian dan Pelestarian Model](https://www.anthropic.com/research/deprecation-commitments).

## Status model

Semua model yang dirilis secara publik tercantum di bawah dengan statusnya:

| Nama Model API              | Status Saat Ini | Dihentikan        | Tanggal Penghentian Tentatif |
|:----------------------------|:--------------------|:------------------|:-------------------------|
| `claude-opus-4-7`               | Aktif              | N/A               | Tidak lebih awal dari 16 April 2027 |
| `claude-opus-4-6`             | Aktif              | N/A               | Tidak lebih awal dari 5 Februari 2027 |
| `claude-opus-4-5-20251101`  | Aktif              | N/A               | Tidak lebih awal dari 24 November 2026 |
| `claude-opus-4-1-20250805`  | Aktif              | N/A               | Tidak lebih awal dari 5 Agustus 2026 |
| `claude-opus-4-20250514`    | Dihentikan          | 14 April 2026    | 15 Juni 2026            |
| `claude-sonnet-4-6`         | Aktif              | N/A               | Tidak lebih awal dari 17 Februari 2027 |
| `claude-sonnet-4-5-20250929`| Aktif              | N/A               | Tidak lebih awal dari 29 September 2026 |
| `claude-sonnet-4-20250514`  | Dihentikan          | 14 April 2026    | 15 Juni 2026            |
| `claude-3-7-sonnet-20250219`| Pensiun             | 28 Oktober 2025  | 19 Februari 2026          |
| `claude-haiku-4-5-20251001` | Aktif              | N/A               | Tidak lebih awal dari 15 Oktober 2026 |
| `claude-3-5-haiku-20241022` | Pensiun             | 19 Desember 2025 | 19 Februari 2026          |
| `claude-3-haiku-20240307`   | Dihentikan          | 19 Februari 2026 | 20 April 2026             |

## Riwayat penghentian

Semua penghentian tercantum di bawah, dengan pengumuman terbaru di bagian atas.

### 2026-04-14: Model Claude Sonnet 4 dan Claude Opus 4

Pada 14 April 2026, Anthropic memberitahu pengembang yang menggunakan model Claude Sonnet 4 dan Claude Opus 4 tentang penghentian mereka yang akan datang di Claude API.

| Tanggal Penghentian             | Model yang Dihentikan            | Pengganti yang Direkomendasikan         |
|:----------------------------|:----------------------------|:--------------------------------|
| 15 Juni 2026               | `claude-sonnet-4-20250514`  | `claude-sonnet-4-6`             |
| 15 Juni 2026               | `claude-opus-4-20250514`    | `claude-opus-4-7`               |

### 2026-02-19: Model Claude Haiku 3

Pada 19 Februari 2026, Anthropic memberitahu pengembang yang menggunakan model Claude Haiku 3 tentang penghentiannya yang akan datang di Claude API.

| Tanggal Penghentian             | Model yang Dihentikan            | Pengganti yang Direkomendasikan         |
|:----------------------------|:----------------------------|:--------------------------------|
| 20 April 2026              | `claude-3-haiku-20240307`   | `claude-haiku-4-5-20251001`     |

### 2025-12-19: Model Claude Haiku 3.5

<Note>
Model ini pensiun pada 19 Februari 2026.
</Note>

Pada 19 Desember 2025, Anthropic memberitahu pengembang yang menggunakan model Claude Haiku 3.5 tentang penghentiannya yang akan datang di Claude API.

| Tanggal Penghentian             | Model yang Dihentikan            | Pengganti yang Direkomendasikan         |
|:----------------------------|:----------------------------|:--------------------------------|
| 19 Februari 2026           | `claude-3-5-haiku-20241022` | `claude-haiku-4-5-20251001`     |

### 2025-10-28: Model Claude Sonnet 3.7

<Note>
Model ini pensiun pada 19 Februari 2026.
</Note>

Pada 28 Oktober 2025, Anthropic memberitahu pengembang yang menggunakan model Claude Sonnet 3.7 tentang penghentiannya yang akan datang di Claude API.

| Tanggal Penghentian             | Model yang Dihentikan            | Pengganti yang Direkomendasikan         |
|:----------------------------|:----------------------------|:--------------------------------|
| 19 Februari 2026           | `claude-3-7-sonnet-20250219`| `claude-sonnet-4-6`               |

### 2025-08-13: Model Claude Sonnet 3.5

<Note>
Model ini pensiun pada 28 Oktober 2025.
</Note>

Pada 13 Agustus 2025, Anthropic memberitahu pengembang yang menggunakan model Claude Sonnet 3.5 tentang penghentian mereka yang akan datang.

| Tanggal Penghentian             | Model yang Dihentikan            | Pengganti yang Direkomendasikan         |
|:----------------------------|:----------------------------|:--------------------------------|
| 28 Oktober 2025            | `claude-3-5-sonnet-20240620`| `claude-sonnet-4-6`               |
| 28 Oktober 2025            | `claude-3-5-sonnet-20241022`| `claude-sonnet-4-6`               |

### 2025-06-30: Model Claude Opus 3

<Note>
Model ini pensiun pada 5 Januari 2026.
</Note>

Pada 30 Juni 2025, Anthropic memberitahu pengembang yang menggunakan model Claude Opus 3 tentang penghentiannya yang akan datang.

| Tanggal Penghentian             | Model yang Dihentikan            | Pengganti yang Direkomendasikan         |
|:----------------------------|:----------------------------|:--------------------------------|
| 5 Januari 2026             | `claude-3-opus-20240229`    | `claude-opus-4-7`      |

### 2025-01-21: Model Claude 2, Claude 2.1, dan Claude Sonnet 3

<Note>
Model ini pensiun pada 21 Juli 2025.
</Note>

Pada 21 Januari 2025, Anthropic memberitahu pengembang yang menggunakan model Claude 2, Claude 2.1, dan Claude Sonnet 3 tentang penghentian mereka yang akan datang.

| Tanggal Penghentian             | Model yang Dihentikan            | Pengganti yang Direkomendasikan         |
|:----------------------------|:----------------------------|:--------------------------------|
| 21 Juli 2025               | `claude-2.0`                | `claude-opus-4-7`                  |
| 21 Juli 2025               | `claude-2.1`                | `claude-opus-4-7`                  |
| 21 Juli 2025               | `claude-3-sonnet-20240229`  | `claude-sonnet-4-6`                |

### 2024-09-04: Model Claude 1 dan Instant

<Note>
Model ini pensiun pada 6 November 2024.
</Note>

Pada 4 September 2024, Anthropic memberitahu pengembang yang menggunakan model Claude 1 dan Instant tentang penghentian mereka yang akan datang.

| Tanggal Penghentian             | Model yang Dihentikan          | Pengganti yang Direkomendasikan    |
|:----------------------------|:--------------------------|:---------------------------|
| 6 November 2024            | `claude-1.0`              | `claude-haiku-4-5-20251001`|
| 6 November 2024            | `claude-1.1`              | `claude-haiku-4-5-20251001`|
| 6 November 2024            | `claude-1.2`              | `claude-haiku-4-5-20251001`|
| 6 November 2024            | `claude-1.3`              | `claude-haiku-4-5-20251001`|
| 6 November 2024            | `claude-instant-1.0`      | `claude-haiku-4-5-20251001`|
| 6 November 2024            | `claude-instant-1.1`      | `claude-haiku-4-5-20251001`|
| 6 November 2024            | `claude-instant-1.2`      | `claude-haiku-4-5-20251001`|