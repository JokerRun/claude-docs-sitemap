---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/cloud-sandboxes-reference
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 805c48bb4434e9cf598a7bb03a03635efe2e9c84e797897577c66d96c5df1037
---

# Referensi sandbox cloud

Paket, database, dan utilitas yang sudah terinstal dan tersedia di sandbox cloud.

---

Sandbox cloud berjalan sebagai kontainer Linux yang terisolasi pada infrastruktur yang dikelola Anthropic. Sandbox ini sudah dilengkapi dengan serangkaian lengkap bahasa pemrograman, database, dan utilitas yang terinstal sebelumnya. Agen dapat langsung menggunakannya tanpa langkah instalasi apa pun.

Spesifikasi ini berlaku untuk lingkungan `cloud`. Sandbox yang di-host sendiri (self-hosted) berjalan pada infrastruktur Anda dengan apa pun yang disediakan oleh worker Anda.

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Bahasa pemrograman

| Bahasa  | Versi   | Package manager |
| ------- | ------- | --------------- |
| Python  | 3.12+   | pip, uv         |
| Node.js | 20+     | npm, yarn, pnpm |
| Go      | 1.22+   | go modules      |
| Rust    | 1.77+   | cargo           |
| Java    | 21+     | maven, gradle   |
| Ruby    | 3.3+    | bundler, gem    |
| PHP     | 8.3+    | composer        |
| C/C++   | GCC 13+ | make, cmake     |

## Database

| Database         | Deskripsi                                          |
| ---------------- | -------------------------------------------------- |
| SQLite           | Sudah terinstal, tersedia langsung                 |
| Klien PostgreSQL | Klien `psql` untuk terhubung ke database eksternal |
| Klien Redis      | `redis-cli` untuk terhubung ke instance eksternal  |

<Note>
  Server database (seperti PostgreSQL dan Redis) tidak berjalan di sandbox secara default. Sandbox menyertakan alat klien untuk terhubung ke instance database eksternal. SQLite sepenuhnya tersedia untuk penggunaan lokal.
</Note>

## Utilitas

### Alat sistem

* `git` - Kontrol versi
* `curl`, `wget` - Klien HTTP
* `jq` - Pemrosesan JSON
* `tar`, `zip`, `unzip` - Alat arsip
* `ssh`, `scp` - Akses jarak jauh (memerlukan jaringan yang diaktifkan)
* `tmux`, `screen` - Terminal multiplexer

### Alat pengembangan

* `make`, `cmake` - Sistem build
* `docker` - Manajemen kontainer (ketersediaan terbatas)
* `ripgrep` (`rg`) - Pencarian file cepat
* `tree` - Visualisasi direktori
* `htop` - Pemantauan proses

### Pemrosesan teks

* `sed`, `awk`, `grep` - Editor stream
* `vim`, `nano` - Editor teks
* `diff`, `patch` - Perbandingan file

## Spesifikasi sandbox

| Properti       | Nilai                                                             |
| -------------- | ----------------------------------------------------------------- |
| Sistem operasi | Ubuntu 22.04 LTS                                                  |
| Arsitektur     | x86\_64 (amd64)                                                   |
| Memori         | Hingga 8 GB                                                       |
| Ruang disk     | Hingga 10 GB                                                      |
| Jaringan       | Dinonaktifkan secara default (aktifkan di konfigurasi lingkungan) |
