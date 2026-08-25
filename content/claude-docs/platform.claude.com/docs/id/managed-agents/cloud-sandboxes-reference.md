---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/cloud-sandboxes-reference
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: c201f39b6d249fd8580df7d15b95101da7aa386ea1b2494c312a422b98a94c2e
---

---
title: Referensi cloud sandbox
url: https://platform.claude.com/docs/id/managed-agents/cloud-sandboxes-reference
description: Paket, database, dan utilitas yang telah terinstal sebelumnya dan tersedia di cloud sandbox.
---

Cloud sandbox berjalan sebagai kontainer Linux terisolasi pada infrastruktur yang dikelola Anthropic. Sandbox ini telah dilengkapi dengan serangkaian lengkap bahasa pemrograman, database, dan utilitas yang terinstal sebelumnya. Agen dapat langsung menggunakannya tanpa langkah instalasi apa pun.

Spesifikasi ini berlaku untuk lingkungan `cloud`. Sandbox self-hosted berjalan pada infrastruktur Anda dengan apa pun yang disediakan oleh worker Anda.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Bahasa pemrograman

| Bahasa  | Versi                       | Manajer paket        |
| ------- | --------------------------- | -------------------- |
| Python  | 3.10, 3.11, 3.12, dan 3.13  | pip, uv, poetry      |
| Node.js | 20, 21, dan 22 (default)    | npm, yarn, pnpm, bun |
| Go      | 1.24 (default) dan 1.25     | go modules           |
| Rust    | Toolchain stable (rustup)   | cargo                |
| Java    | OpenJDK 21                  | maven, gradle        |
| Ruby    | 3.1, 3.2, dan 3.3 (default) | bundler, gem         |
| PHP     | 8.3                         | composer             |
| C/C++   | GCC 13 dan Clang            | make, cmake, ninja   |

Library data dan dokumen Python yang umum, termasuk NumPy, pandas, Matplotlib, openpyxl, python-docx, python-pptx, dan pypdf, terinstal untuk interpreter `python3`.

## Database

| Database      | Deskripsi                                                                |
| ------------- | ------------------------------------------------------------------------ |
| PostgreSQL 16 | Server dan klien `psql` terinstal. Server tidak berjalan secara default. |
| Redis 7       | Server dan `redis-cli` terinstal. Server tidak berjalan secara default.  |
| SQLite        | Tersedia melalui binding bahasa, seperti modul `sqlite3` Python.         |

## Utilitas

### Alat sistem

* `git` - Kontrol versi
* `curl`, `wget` - Klien HTTP
* `jq`, `yq` - Pemrosesan JSON dan YAML
* `tar`, `zip`, `unzip` - Alat arsip
* `tmux` - Terminal multiplexer

### Alat pengembangan

* `make`, `cmake` - Sistem build
* `docker` - Manajemen kontainer (ketersediaan terbatas)
* `ripgrep` (`rg`) - Pencarian file cepat

### Pemrosesan teks

* `sed`, `awk`, `grep` - Editor stream
* `vim`, `nano` - Editor teks
* `diff`, `patch` - Perbandingan file

### Pemrosesan dokumen dan media

* `ffmpeg` - Pemrosesan audio dan video
* ImageMagick (`convert`, `identify`) - Manipulasi gambar
* `pandoc` - Konversi dokumen
* LibreOffice (headless) - Konversi dokumen office
* Utilitas Poppler (`pdftotext`, `pdftoppm`) dan `qpdf` - Pemrosesan PDF
* `tesseract` - Pengenalan karakter optik (data bahasa Inggris)
* TeX Live (`pdflatex`, `xelatex`, `latexmk`) - Typesetting

### Otomatisasi browser

* Playwright (Python dan Node.js) - Library otomatisasi browser
* Chromium (`/opt/pw-browsers/chromium`) - Browser yang digunakan oleh Playwright, tidak ada di `PATH`

Sandbox menetapkan `PLAYWRIGHT_BROWSERS_PATH` ke `/opt/pw-browsers`, sehingga paket Playwright yang telah terinstal sebelumnya menemukan Chromium di sana tanpa konfigurasi. Paket Python terinstal untuk interpreter `python3`. Gunakan paket yang telah terinstal sebelumnya daripada menginstal versi Playwright lain, yang akan mencari build browser yang tidak tersedia. Firefox dan WebKit tidak terinstal.

## Spesifikasi sandbox

| Properti       | Nilai                                                                                                                                                                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem operasi | Ubuntu 24.04 LTS                                                                                                                                                                                                                                        |
| Arsitektur     | x86\_64 (amd64)                                                                                                                                                                                                                                         |
| Memori         | Hingga 8 GB                                                                                                                                                                                                                                             |
| Ruang disk     | Hingga 10 GB                                                                                                                                                                                                                                            |
| Jaringan       | Lingkungan yang dibuat melalui API secara default menggunakan [jaringan `unrestricted`](https://platform.claude.com/docs/id/managed-agents/environments#networking); sandbox yang disediakan melalui Claude Studio secara default menggunakan `limited` |
