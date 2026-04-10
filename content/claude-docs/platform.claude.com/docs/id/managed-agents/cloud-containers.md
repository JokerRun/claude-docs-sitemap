---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/cloud-containers
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: a94d2a42b739ae2e4e799d98abc4e4e911b49f5b73b077067a704f76529c4918
---

# Referensi container

Paket pra-instal, database, dan utilitas yang tersedia di cloud container.

---

Cloud container di Claude Managed Agents dilengkapi dengan serangkaian lengkap bahasa pemrograman, database, dan utilitas yang sudah diinstal sebelumnya. Agen dapat menggunakan ini segera tanpa langkah instalasi apa pun.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis.
</Note>

## Bahasa pemrograman

| Bahasa | Versi | Pengelola paket |
|----------|---------|-----------------|
| Python | 3.12+ | pip, uv |
| Node.js | 20+ | npm, yarn, pnpm |
| Go | 1.22+ | go modules |
| Rust | 1.77+ | cargo |
| Java | 21+ | maven, gradle |
| Ruby | 3.3+ | bundler, gem |
| PHP | 8.3+ | composer |
| C/C++ | GCC 13+ | make, cmake |

## Database

| Database | Deskripsi |
|----------|-------------|
| SQLite | Pra-instal, tersedia segera |
| PostgreSQL client | Klien `psql` untuk terhubung ke database eksternal |
| Redis client | `redis-cli` untuk terhubung ke instans eksternal |

<Note>
Server database (PostgreSQL, Redis, dll.) tidak berjalan di container secara default. Container mencakup alat klien untuk terhubung ke instans database eksternal. SQLite sepenuhnya tersedia untuk penggunaan lokal.
</Note>

## Utilitas

### Alat sistem

- `git` - Kontrol versi
- `curl`, `wget` - Klien HTTP
- `jq` - Pemrosesan JSON
- `tar`, `zip`, `unzip` - Alat arsip
- `ssh`, `scp` - Akses jarak jauh (memerlukan jaringan diaktifkan)
- `tmux`, `screen` - Multiplexer terminal

### Alat pengembangan

- `make`, `cmake` - Sistem build
- `docker` - Manajemen container (ketersediaan terbatas)
- `ripgrep` (`rg`) - Pencarian file cepat
- `tree` - Visualisasi direktori
- `htop` - Pemantauan proses

### Pemrosesan teks

- `sed`, `awk`, `grep` - Editor aliran
- `vim`, `nano` - Editor teks
- `diff`, `patch` - Perbandingan file

## Spesifikasi container

| Properti | Nilai |
|----------|-------|
| Sistem operasi | Ubuntu 22.04 LTS |
| Arsitektur | x86_64 (amd64) |
| Memori | Hingga 8 GB |
| Ruang disk | Hingga 10 GB |
| Jaringan | Dinonaktifkan secara default (aktifkan di konfigurasi lingkungan) |