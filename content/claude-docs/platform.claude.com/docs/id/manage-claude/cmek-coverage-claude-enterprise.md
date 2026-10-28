---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: 2512f9bef798c5102e4a7abcc2e98e8c2e14bf96a38483fdcea3286c7e0259f7
---

---
title: Cakupan CMEK di Claude Enterprise
url: https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise
description: Cari tahu data Claude Enterprise mana yang dienkripsi oleh kunci Anda, apa yang dinonaktifkan atau berubah, dan apa yang tetap berada di bawah kunci Anthropic.
---

Untuk Claude Platform, lihat [Cakupan CMEK di Claude Platform](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform). Fitur beta dan pratinjau riset mungkin tidak dilindungi oleh “customer-managed encryption keys” (kunci enkripsi yang dikelola pelanggan), atau CMEK, dan dapat mengalami gangguan di organisasi CMEK.

## Dienkripsi dengan kunci Anda

* Konten chat, termasuk skill dan plugin.
* Lampiran chat dan lampiran proyek.
* Artifacts, termasuk Claude Design, Claude Slides, dan Claude Docs dalam percakapan dan tab **Artifacts**.
* Claude Code di CLI, termasuk konten pesan.
* Cowork di Claude Desktop.
* Office agents.
* Claude in Chrome.
* Claude Science, yang masih dalam versi beta.
* Versi plugin [Plugins API](https://platform.claude.com/docs/id/manage-claude/plugins-api#customer-managed-encryption-keys) (beta): deskripsi, catatan rilis, komponen, dan file setiap versi. Halaman tersebut mencantumkan permintaan mana yang tetap berfungsi selama kunci Anda tidak dapat digunakan.
* [Transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) Compliance API dari sesi di mesin pengguna. Jika kunci Anda tidak dapat digunakan, endpoint messages mengembalikan [503 Service Unavailable](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-sessions-temporarily-unavailable) alih-alih konten transkrip. Metadata sesi tetap dicantumkan.
* Backup dan snapshot, yang mewarisi kunci tersebut.

## Dinonaktifkan atau berubah

Daftar ini tidak lengkap. Tinjau daftar ini bersama tim Anda sebelum Anda menyiapkan CMEK.

| Fitur                                                                                                                                       | Yang dilihat pengguna                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Code on the web                                                                                                                      | Nonaktif. Sesi baru tidak dapat dimulai, meskipun admin mengaktifkan produk tersebut.                                                                                                                                                                                                         |
| Claude in Slack                                                                                                                             | Nonaktif. Claude menolak permintaan, meskipun admin mengaktifkan produk tersebut.                                                                                                                                                                                                             |
| Claude Code Desktop                                                                                                                         | Nonaktif hingga admin mengaktifkannya. Tersedia untuk sesi lokal setelah diaktifkan di [claude.ai > Organization settings > Claude Code](https://claude.ai/admin-settings/claude-code).                                                                                                       |
| Artifacts                                                                                                                                   | Berubah. Artifacts, termasuk Claude Design, Claude Slides, dan Claude Docs dalam percakapan dan tab **Artifacts**, tidak dapat diaktifkan di organisasi yang juga menggunakan ZDR. Di organisasi dengan HIPAA readiness, Owner harus terlebih dahulu menerima ketentuan penggunaan Artifacts. |
| Publikasi dan berbagi artifact                                                                                                              | Berubah. Claude Code tidak dapat [memublikasikan artifact](https://code.claude.com/docs/id/artifacts#availability). Namun, artifact yang dibuat di chat atau Cowork dapat dibagikan di dalam organisasi Anda, tetapi tidak secara publik.                                                     |
| Aplikasi Claude Design mandiri                                                                                                              | Tidak didukung. Lihat [Dienkripsi dengan kunci Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#encrypted-with-anthropics-key).                                                                                                                   |
| Analitik: smart reports dan metrik kontribusi                                                                                               | Nonaktif. Analitik tertentu dinonaktifkan, terlepas dari pengaturan admin: Claude smart reports (beta, di claude.ai/analytics/insights) dan metrik kontribusi Claude Code dari GitHub (beta, di claude.ai/analytics/claude-code).                                                             |
| Analitik: skill dan konektor                                                                                                                | Berubah. Analitik admin untuk skill dan konektor, di dasbor analitik claude.ai dan melalui [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api), tidak mencakup penggunaan di chat, dan menyembunyikan nama skill, plugin, dan konektor kustom. |
| Penilaian respons (jempol ke atas dan jempol ke bawah)                                                                                      | Nonaktif. Anggota tidak dapat menilai respons Claude.                                                                                                                                                                                                                                         |
| [Pemindaian keamanan skill dan plugin](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/enterprise#skill-content-scanning) | Nonaktif. Pengaturan ini tidak dapat diaktifkan, dan skill serta plugin diinstal tanpa pemindaian.                                                                                                                                                                                            |
| Claude Security dan routines                                                                                                                | Nonaktif. Fitur beta dan pratinjau riset, dinonaktifkan terlepas dari pengaturan admin.                                                                                                                                                                                                       |

## Dienkripsi dengan kunci Anthropic

Fitur yang menyimpan data ini tetap tersedia, tetapi data tersebut tidak dienkripsi dengan kunci Anda. Anda dapat menonaktifkan beberapa fitur ini di **Settings**.

| Data                                                | Detail                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Data yang sudah ada                                 | Ditulis sebelum [kunci Anda mulai berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect).                                                                                                                                                                                                                                                                                      |
| Aplikasi Claude Design mandiri                      | Aplikasi Claude Design mandiri di claude.ai/design tidak didukung dengan CMEK, dan datanya mungkin tidak dienkripsi dengan kunci Anda. Aplikasi mandiri ini akan ditutup. Claude Design dalam percakapan dan tab **Artifacts** dienkripsi dengan kunci Anda, sebagaimana tercantum di [Dienkripsi dengan kunci Anda](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#encrypted-with-your-key). |
| Personal preferences dan Cowork Global instructions | [Personal preferences - bagian Instructions for Claude](https://claude.ai/new#settings/account) dan Cowork Global instructions. Keduanya diatur di tingkat akun dan dibagikan ke semua organisasi milik seorang pengguna.                                                                                                                                                                                                        |
| Data akun untuk pengguna di organisasi Anda         | Mencakup nama, alamat email, dan foto profil.                                                                                                                                                                                                                                                                                                                                                                                    |
| Catatan yang dipreservasi                           | Anthropic dapat mempreservasi catatan tertentu [dalam tiga kasus sempit](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#limited-preservation-outside-your-key).                                                                                                                                                                                                                                           |

## Tempat CMEK tidak berlaku: telemetri Claude Code

Saat Claude Code terhubung melalui gateway atau proxy LLM (`ANTHROPIC_BASE_URL` kustom), CMEK tidak berlaku untuk telemetri operasional Claude Code. Untuk menonaktifkan telemetri ini, atur variabel lingkungan `DISABLE_TELEMETRY` ke `1`, sebagaimana dijelaskan di bagian [Layanan telemetri](https://code.claude.com/docs/id/data-usage#telemetry-services) dalam dokumentasi Claude Code.
