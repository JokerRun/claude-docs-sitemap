---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/cloud-sandboxes-reference
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 3798ccb83f5f19464d9b68d7816f19037602875a2a0463ebe6da511f0d1873d2
---

# Referensi cloud sandbox

Paket, database, dan utilitas yang sudah terpasang sebelumnya yang tersedia di cloud sandbox.

---

Cloud sandbox berjalan sebagai kontainer Linux terisolasi pada infrastruktur yang dikelola Anthropic. Sandbox ini sudah dilengkapi dengan serangkaian bahasa pemrograman, database, dan utilitas yang komprehensif. Agen dapat langsung menggunakannya tanpa langkah instalasi apa pun.

Spesifikasi ini berlaku untuk lingkungan `cloud`. Sandbox yang di-hosting sendiri berjalan pada infrastruktur Anda dengan apa pun yang disediakan oleh worker Anda.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Bahasa pemrograman

| Bahasa  | Versi   | Manajer paket   |
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
| SQLite           | Sudah terpasang sebelumnya, langsung tersedia      |
| Klien PostgreSQL | Klien `psql` untuk terhubung ke database eksternal |
| Klien Redis      | `redis-cli` untuk terhubung ke instans eksternal   |

<Note>
  Server database (seperti PostgreSQL dan Redis) tidak berjalan di sandbox secara default. Sandbox menyertakan alat klien untuk terhubung ke instans database eksternal. SQLite sepenuhnya tersedia untuk penggunaan lokal.
</Note>

## Utilitas

### Alat sistem

* `git` - Kontrol versi
* `curl`, `wget` - Klien HTTP
* `jq` - Pemrosesan JSON
* `tar`, `zip`, `unzip` - Alat arsip
* `ssh`, `scp` - Akses jarak jauh (memerlukan mode jaringan yang mengizinkan host tujuan)
* `tmux`, `screen` - Multiplexer terminal

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

| Properti       | Nilai                                                                                                                                                                                                                        |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem operasi | Ubuntu 22.04 LTS                                                                                                                                                                                                             |
| Arsitektur     | x86\_64 (amd64)                                                                                                                                                                                                              |
| Memori         | Hingga 8 GB                                                                                                                                                                                                                  |
| Ruang disk     | Hingga 10 GB                                                                                                                                                                                                                 |
| Jaringan       | Lingkungan yang dibuat melalui API secara default menggunakan [jaringan `unrestricted`](/docs/id/managed-agents/environments#networking); sandbox yang disediakan melalui Claude Studio secara default menggunakan `limited` |
