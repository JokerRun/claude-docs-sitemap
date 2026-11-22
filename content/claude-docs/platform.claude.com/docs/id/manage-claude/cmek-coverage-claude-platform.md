---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform
fetched_at: 2026-11-22T02:13:35.406200Z
sha256: 8f0d0af8c46e0549e05477a739a0697fe2ea570a342e27960c6f9312ba7407f7
---

---
title: Apa yang dicakup CMEK di Claude Platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform
description: Cari tahu data Claude Platform mana yang dienkripsi dengan kunci Anda, apa yang dinonaktifkan atau berubah, dan apa yang tetap berada di bawah kunci Anthropic.
---

Untuk Claude Enterprise, lihat [Apa yang dicakup CMEK di Claude Enterprise](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise).

## Dienkripsi dengan kunci Anda

* Konten pesan.
* File dan lampiran, baik yang dikirim inline bersama permintaan maupun yang diunggah dengan Files API.
* Konfigurasi MCP dan alat.
* Data [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) (beta), termasuk konfigurasi agen, environment, webhook, sesi beserta event-nya, [penyimpanan memori](https://platform.claude.com/docs/id/managed-agents/memory) (beta) beserta memori dan versi memorinya, serta [dreams](https://platform.claude.com/docs/id/managed-agents/dreams) (pratinjau riset).
* [Webhook organisasi](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#if-your-default-workspace-uses-an-encryption-key) (beta): nama endpoint, deskripsi, dan signing secret, jika [workspace default](https://platform.claude.com/docs/id/manage-claude/workspaces#how-workspaces-work) Anda menggunakan kunci.
* Data Batch API dan Skills API yang disimpan saat diam (at rest).
* Data alat yang disimpan saat diam oleh pencarian web, pengambilan web, eksekusi kode, bash, editor teks, konektor MCP (beta), output terstruktur, alat advisor (beta), penggunaan komputer, penggunaan browser, dan manajemen konteks (beta).
* Backup dan snapshot, yang mewarisi kunci tersebut.

## Dinonaktifkan atau berubah

Fitur beta dan pratinjau riset yang tidak tercantum di halaman ini mungkin tidak dilindungi oleh “customer-managed encryption keys” (kunci enkripsi yang dikelola pelanggan), atau CMEK.

Daftar ini tidak lengkap. Tinjau daftar ini bersama tim Anda sebelum Anda menyiapkan CMEK.

| Fitur | Apa yang berubah |
| ----- | ----- |
| Playground di Claude Console | Dinonaktifkan. |
| Output terstruktur, termasuk `strict: true` pada alat, dengan model Claude Fable atau Claude Mythos | Dinonaktifkan di organisasi CMEK. Dengan model lain, data yang disimpan saat diam oleh output terstruktur [dienkripsi dengan kunci Anda](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform#encrypted-with-your-key). |
| [Webhook organisasi](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#if-your-default-workspace-uses-an-encryption-key) (beta) | Tetap tersedia di Claude API. Selama Anthropic tidak dapat menggunakan kunci workspace default Anda, endpoint webhook organisasi yang bergantung pada kunci tersebut akan kehilangan event-nya. |
| Tanpa retensi data (ZDR) | Workspace dengan kunci Anda meretensi data. Lihat [CMEK, retensi data, dan ZDR](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention). |

## Dienkripsi dengan kunci Anthropic

Fitur yang menyimpan data ini tetap tersedia, tetapi datanya tidak dienkripsi dengan kunci Anda. Anda dapat menonaktifkan beberapa fitur ini di **Pengaturan**.

| Data | Detail |
| ----- | ----- |
| Data yang sudah ada sebelum penyiapan kunci | Ditulis sebelum [kunci Anda mulai berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect). |
| Data yang tidak dalam keadaan diam (at rest), dan data dengan TTL lebih pendek dari 24 jam | Misalnya, cache. |
| Activity Feed, log audit, dan lalu lintas jaringan telemetri seperti OpenTelemetry (beta) | Tetap berada di bawah kunci Anthropic agar Anda dapat mempertahankan kepatuhan bahkan jika kunci Anda tidak dapat digunakan. |
| Nilai [kredensial vault](https://platform.claude.com/docs/id/managed-agents/vaults) Claude Managed Agents (beta), seperti token OAuth dan client secret | Hanya-tulis dan tidak pernah dikembalikan dalam respons API. |
| [Profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) | Field profil seperti `name` dan `metadata`. Jangan simpan data pribadi sensitif di `metadata` profil. |
| [Webhook organisasi](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#if-your-default-workspace-uses-an-encryption-key) (beta): URL endpoint dan jenis event | Setiap field selain nama, deskripsi, dan signing secret. |
| Umpan balik Claude Console | Rating dan komentar yang dipilih anggota untuk dikirim melalui opsi **Masukan**. Tidak ada pengaturan yang menonaktifkannya. |
| Header permintaan [destinasi OpenTelemetry](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#add-a-destination) (beta), seperti header kunci API platform observabilitas Anda | Hanya-tulis dan tidak pernah dikembalikan dalam respons API. |
| Data akun untuk pengguna di organisasi Anda | Mencakup nama, alamat email, dan foto profil. |
| Catatan yang dipreservasi | Anthropic dapat mempreservasi catatan tertentu [dalam tiga kasus sempit](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#limited-preservation-outside-your-key). |
| Telemetri Claude Code | Saat Claude Code terhubung melalui gateway atau proxy LLM (`ANTHROPIC_BASE_URL` kustom), CMEK tidak berlaku untuk telemetri operasional Claude Code. Untuk menonaktifkan telemetri ini, atur variabel lingkungan `DISABLE_TELEMETRY` ke `1`, sebagaimana dijelaskan di bagian [Layanan telemetri](https://code.claude.com/docs/id/data-usage#telemetry-services) dalam dokumentasi Claude Code. |
