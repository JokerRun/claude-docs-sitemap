---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/secure-deployment-monitoring
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: 13c5078045b33b16961e4af07158a72e5b41c4a2a1c52213b6064d50db52549e
---

---
title: Tinjau dan pantau sesi agen
url: https://platform.claude.com/docs/id/managed-agents/secure-deployment-monitoring
description: Secara opsional, tinjau event setiap sesi dengan job offline. Pantau webhook untuk sesi yang memerlukan perhatian, dan lihat apa yang disimpan Managed Agents serta berapa lama.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Secara opsional, tinjau event setiap sesi dengan job offline. Pantau webhook untuk sesi yang memerlukan perhatian, dan hapus sesi yang tidak lagi Anda perlukan. Untuk membatasi apa yang dapat dilakukan agen sebelum dijalankan, lihat [Amankan deployment Managed Agents Anda](https://platform.claude.com/docs/id/managed-agents/secure-deployment).

## Secara opsional, minta peninjau offline membaca setiap transkrip

“Offline reviewer” (peninjau offline) adalah job yang Anda jalankan, terpisah dari sesi yang ditinjaunya, yang membaca event setiap sesi setelah event tersebut ditulis. Sesi yang panjang memiliki terlalu banyak event untuk dibaca oleh seseorang, sehingga job tersebut meminta Claude untuk membacanya. Tinjauan ini menandai perilaku di luar apa yang diberikan kepada agen. Untuk prompt tinjauan, langkah penyiapan, dan kode yang berfungsi, lihat [resep tinjauan keamanan](https://platform.claude.com/cookbook/managed-agents-cma-agent-security-review) di Claude Cookbook.

## Pantau sesi dan tinjau retensi

Berlangganan webhook yang memberi tahu Anda ketika sebuah sesi memerlukan perhatian, dan hapus sesi yang tidak lagi Anda perlukan. Verifikasi tanda tangan pada setiap pengiriman. Lihat [Memverifikasi tanda tangan](https://platform.claude.com/docs/id/managed-agents/webhooks#verify-the-signature).

| Apa yang dipantau                                           | Di mana melihatnya                                                                                                                                                                                                                                                                                   |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sesi yang menjadi idle, misalnya untuk menunggu persetujuan | Webhook `session.status_idled`. Webhook ini dipicu setiap kali sesi menjadi idle, karena alasan apa pun                                                                                                                                                                                              |
| Sesi yang mencapai anggaran atau berhenti                   | Webhook `session.budget_reached` dan `session.status_terminated`                                                                                                                                                                                                                                     |
| Eksekusi terjadwal yang gagal memulai sesi                  | Webhook `deployment_run.failed` dan `deployment.paused`                                                                                                                                                                                                                                              |
| Kredensial OAuth MCP yang tidak dapat diperbarui            | Webhook `vault_credential.refresh_failed`                                                                                                                                                                                                                                                            |
| Panggilan alat yang ditolak atau dijeda oleh server         | `evaluated_permission` pada event `agent.tool_use` dan `agent.mcp_tool_use`. Dalam sesi multiagen, daftarkan juga event setiap thread                                                                                                                                                                |
| Apa yang dilakukan agen dalam sebuah sesi                   | Penampil sesi Claude Console                                                                                                                                                                                                                                                                         |
| Perilaku di luar apa yang diberikan kepada agen             | Job tinjauan offline opsional yang Anda jalankan yang membaca event setiap sesi. Lihat [Secara opsional, minta peninjau offline membaca setiap transkrip](https://platform.claude.com/docs/id/managed-agents/secure-deployment-monitoring#optionally-have-an-offline-reviewer-read-every-transcript) |

Untuk melihat mengapa sebuah sesi menjadi idle, daftarkan event-nya dengan `types` diatur ke `session.status_idle`, `order` diatur ke `desc`, dan `limit` diatur ke `1`. Event tersebut bernama `session.status_idle`, dan webhook-nya bernama `session.status_idled`. Jika `stop_reason.type` adalah `requires_action`, sesi sedang menunggu Anda, dan `stop_reason.event_ids` mencantumkan event yang sedang ditunggunya. Untuk menjawabnya, lihat [Menjawab panggilan alat yang menjeda sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#answer-tool-calls-that-pause-the-session). Dalam sandbox self-hosted, event `agent.tool_use` dapat menunggu sandbox Anda mengembalikan hasil alat. Dengan eksekusi workflow yang terbuka, panggilan alat dapat menunggu jawaban Anda sementara sesi tetap `running`. Jawab setiap panggilan ketika event-nya tiba. Lihat [Selama eksekusi terbuka](https://platform.claude.com/docs/id/managed-agents/workflow-runs#while-a-run-is-open).

Pengiriman webhook bisa terlewat, jadi daftarkan juga sesi Anda sesuai jadwal dan periksa sesi yang idle.

Lihat [Berlangganan webhook](https://platform.claude.com/docs/id/managed-agents/webhooks) dan [Memeriksa sesi dan melacak penggunaan](https://platform.claude.com/docs/id/managed-agents/session-observability#inspect-a-session-in-the-console).

Daftar ini menunjukkan apa yang disimpan Managed Agents, dan berapa lama:

* **Riwayat sesi:** Disimpan hingga Anda menghapus sesi. Mengarsipkan sesi tetap menyimpan riwayatnya. Untuk menyimpan event sesi, salin event tersebut ke log Anda sendiri dengan API events sebelum Anda menghapusnya. Sesi yang berstatus `running` tidak dapat dihapus. Lihat [Menghapus sesi](https://platform.claude.com/docs/id/managed-agents/session-operations#deleting-a-session).
* **Status sandbox:** Disimpan selama 30 hari setelah sandbox dibuat.
* **File yang dihasilkan sesi:** Dihapus bersama sesi. Unduh terlebih dahulu file yang ingin Anda simpan.
* **File yang Anda unggah, memory store, dan vault:** Tidak dihapus bersama sesi. Hapus secara terpisah.

Dengan sandbox self-hosted, salinan input dan output alat di infrastruktur Anda sendiri menjadi milik Anda untuk disimpan atau dihapus.

Managed Agents saat ini tidak memenuhi syarat untuk cakupan Zero Data Retention atau HIPAA Business Associate Agreement (BAA). Lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).
