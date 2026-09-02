---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/reference
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: d9c4aa6e50355d752d2edb8af6314331330257d845936829fd9d26473af151a0
---

---
title: Referensi
url: https://platform.claude.com/docs/id/managed-agents/reference
description: Tipe event, flag CLI worker self-hosted, tipe server MCP yang didukung, batas laju, dan pedoman branding untuk Claude Managed Agents.
---

Halaman ini mengumpulkan materi referensi untuk Claude Managed Agents. Untuk panduan berorientasi tugas, ikuti tautan di setiap bagian. Untuk operasi pada resource sesi, lihat [Operasi sesi](https://platform.claude.com/docs/id/managed-agents/session-operations).

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK menetapkan header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Tipe event

String tipe event yang dipersistenkan mengikuti konvensi penamaan `{domain}.{action}`; event delta yang hanya tersedia di stream (lihat tab Event deltas) adalah pengecualiannya. Lihat [Stream event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) untuk mengirim, melakukan streaming, dan mendaftar event. Tipe event webhook didaftarkan secara terpisah di [Berlangganan webhook](https://platform.claude.com/docs/id/managed-agents/webhooks#supported-event-types), dan beberapa namanya berbeda dari nama di stream (misalnya, `session.status_idled` alih-alih `session.status_idle`).

<Tabs>
  <Tab title="Event pengguna">
    | Tipe                      | Deskripsi                                                                                                                                                                                                                                                  |
    | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `user.message`            | Pesan pengguna dengan konten teks, gambar, atau dokumen.                                                                                                                                                                                                   |
    | `user.interrupt`          | Menghentikan agen di tengah eksekusi.                                                                                                                                                                                                                      |
    | `user.custom_tool_result` | Respons terhadap panggilan alat kustom dari agen.                                                                                                                                                                                                          |
    | `user.tool_confirmation`  | Menyetujui atau menolak panggilan alat agen atau MCP ketika kebijakan izin memerlukan konfirmasi.                                                                                                                                                          |
    | `user.define_outcome`     | Mendefinisikan [outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) yang akan dikerjakan oleh agen.                                                                                                                               |
    | `user.tool_result`        | Hanya untuk sesi dengan [environment](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) `self_hosted`, integrasi Anda bertanggung jawab untuk menyediakan hasil `agent_toolset`. Helper SDK dan CLI melakukan ini secara otomatis. |
  </Tab>

  <Tab title="Event agen">
    | Tipe                             | Deskripsi                                                                                                                                                                                                                                                                 |
    | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `agent.message`                  | Blok konten respons agen.                                                                                                                                                                                                                                                 |
    | `agent.thinking`                 | Menandakan bahwa agen sedang membuat kemajuan melalui "extended thinking" (pemikiran diperpanjang). Ini hanya sinyal kemajuan dan tidak membawa konten pemikiran.                                                                                                         |
    | `agent.tool_use`                 | Agen memanggil alat agen bawaan (bash, operasi file, dan sebagainya).                                                                                                                                                                                                     |
    | `agent.tool_result`              | Hasil eksekusi alat agen bawaan.                                                                                                                                                                                                                                          |
    | `agent.mcp_tool_use`             | Agen memanggil alat server MCP.                                                                                                                                                                                                                                           |
    | `agent.mcp_tool_result`          | Hasil eksekusi alat MCP.                                                                                                                                                                                                                                                  |
    | `agent.custom_tool_use`          | Agen memanggil salah satu alat kustom Anda. Respons dengan event `user.custom_tool_result`.                                                                                                                                                                               |
    | `agent.thread_context_compacted` | Riwayat percakapan dipadatkan agar muat dalam "context window" (jendela konteks).                                                                                                                                                                                         |
    | `agent.thread_message_received`  | Dalam sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), sebuah pesan dari thread lain tiba di thread yang stream-nya membawa event ini; pada thread utama, seorang agen mengirim laporan atau pertanyaan kepada koordinator. |
    | `agent.thread_message_sent`      | Dalam sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), thread yang stream-nya membawa event ini mengirim pesan ke thread lain; pada thread utama, koordinator mengirim tugas atau pesan tindak lanjut ke agen lain.         |

    Konten pesan dalam event-event ini dapat menyertakan blok konten `redacted`, `{"type": "redacted"}`: sebuah placeholder untuk konten yang ditahan oleh kebijakan model Anthropic. Blok ini tidak membawa field lain. Blok redacted hanya muncul dalam konten yang dikeluarkan platform; event pengguna yang menyertakannya akan ditolak dengan error 400.
  </Tab>

  <Tab title="Event sesi">
    | Tipe                                | Deskripsi                                                                                                                                                                                                                                                 |
    | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `session.status_running`            | Agen sedang aktif memproses.                                                                                                                                                                                                                              |
    | `session.status_idle`               | Agen menyelesaikan tugasnya saat ini dan sedang menunggu input. Menyertakan `stop_reason` yang menunjukkan mengapa agen berhenti.                                                                                                                         |
    | `session.status_rescheduled`        | Terjadi error sementara dan sesi sedang mencoba ulang secara otomatis.                                                                                                                                                                                    |
    | `session.status_terminated`         | Sesi berakhir, baik karena error yang tidak dapat dipulihkan maupun karena diarsipkan.                                                                                                                                                                    |
    | `session.deleted`                   | Sesi dihapus. Mengakhiri stream event aktif apa pun; tidak ada event lebih lanjut yang dikeluarkan untuk sesi ini.                                                                                                                                        |
    | `session.updated`                   | Permintaan pembaruan sesi mengubah setidaknya satu field. Hanya menyertakan field yang berubah. Pembaruan berlaku pada giliran berikutnya.                                                                                                                |
    | `session.error`                     | Terjadi error selama pemrosesan. Menyertakan objek `error` bertipe dengan `retry_status`.                                                                                                                                                                 |
    | `session.usage`                     | Snapshot penggunaan kumulatif sesi dan biaya daftar yang dilacak. Membawa total penggunaan sesi dan gema dari [anggaran](https://platform.claude.com/docs/id/managed-agents/budgets) sesi, atau `null` ketika sesi tidak memilikinya.                     |
    | `session.thread_created`            | Sebuah thread [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) dibuat.                                                                                                                                            |
    | `session.thread_status_running`     | Sebuah thread sesi mulai dieksekusi. Setiap sesi mengeluarkan ini untuk thread utamanya; dalam sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), transisi thread anak juga diposting silang ke stream utama. |
    | `session.thread_status_idle`        | Sebuah thread sesi menyelesaikan gilirannya dan sedang menunggu input. Menyertakan `stop_reason`.                                                                                                                                                         |
    | `session.thread_status_rescheduled` | Sebuah thread sesi mengalami error sementara dan sedang mencoba ulang secara otomatis.                                                                                                                                                                    |
    | `session.thread_status_terminated`  | Sebuah thread sesi diarsipkan atau mencapai error terminal.                                                                                                                                                                                               |
  </Tab>

  <Tab title="Event span">
    Event span adalah penanda observabilitas yang membungkus aktivitas untuk pelacakan waktu dan penggunaan.

    | Tipe                              | Deskripsi                                                                                                                                                                                                                                                           |
    | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `span.model_request_start`        | Panggilan inferensi model telah dimulai.                                                                                                                                                                                                                            |
    | `span.model_request_end`          | Panggilan inferensi model telah selesai. Menyertakan `model_usage` dengan jumlah token.                                                                                                                                                                             |
    | `span.outcome_evaluation_start`   | Evaluasi [outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) telah dimulai.                                                                                                                                                               |
    | `span.outcome_evaluation_ongoing` | Heartbeat selama evaluasi [outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) yang sedang berlangsung.                                                                                                                                    |
    | `span.outcome_evaluation_end`     | Sebuah siklus evaluasi [outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) telah selesai. Hasil `needs_revision` berarti siklus lain akan menyusul; `satisfied`, `max_iterations_reached`, `failed`, dan `interrupted` bersifat terminal. |
  </Tab>

  <Tab title="Event sistem">
    | Tipe             | Deskripsi                                                                                                                                                                                                                                                                                                                                                             |
    | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `system.message` | Menambahkan konteks tingkat sistem yang diistimewakan yang berlaku untuk giliran yang menyertainya dan semua giliran berikutnya. Didukung pada Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5, dan Claude Opus 4.8. Pada model utama yang tidak didukung, event ditolak dengan `model_does_not_support_mid_conversation_system`. |
  </Tab>

  <Tab title="Event deltas">
    Event delta adalah event pratinjau yang hanya tersedia di stream. Event ini dikeluarkan pada koneksi stream (tingkat sesi atau per thread) yang memilih ikut serta dengan parameter `event_deltas[]`, dan tidak pernah dipersistenkan ke riwayat event sesi. Lihat [Event delta](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#event-deltas) untuk cara ikut serta, mengakumulasi, dan merekonsiliasinya.

    | Tipe          | Deskripsi                                                                                                                                                   |
    | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `event_start` | Sebuah event yang dipratinjau telah mulai dihasilkan. Membawa `type` dan `id` dari event yang akan datang. Hanya di stream dan tidak pernah dipersistenkan. |
    | `event_delta` | Konten inkremental untuk event yang dipratinjau, diidentifikasi oleh `event_id`. Hanya di stream dan tidak pernah dipersistenkan.                           |
  </Tab>
</Tabs>

## Worker self-hosted

Berikut adalah flag CLI `ant beta:worker` untuk worker bawaan yang menggerakkan environment `self_hosted`. Lihat [Sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) untuk menyiapkan environment, menjalankan worker, dan opsi helper SDK.

| Flag                   | Deskripsi                                                                                                                                                                                      |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--environment-id`     | Environment yang akan di-poll untuk pekerjaan. Juga dibaca dari `ANTHROPIC_ENVIRONMENT_ID`.                                                                                                    |
| `--environment-key`    | Mengautentikasi worker dengan environment ini. Juga dibaca dari `ANTHROPIC_ENVIRONMENT_KEY`.                                                                                                   |
| `--workdir`            | Direktori tempat skill diunduh dan alat membaca serta menulis file. Default-nya `.` (direktori saat ini); direktori kerja default sistem adalah `/workspace`.                                  |
| `--on-work`            | Skrip yang dipanggil untuk setiap item pekerjaan yang diklaim alih-alih menjalankan alat dalam proses. Menerima detail sesi sebagai variabel environment.                                      |
| `--unrestricted-paths` | Mengizinkan alat file untuk membaca dan menulis path di luar `--workdir`. Pemeriksaan workdir adalah pagar pengaman untuk alat file saja, bukan sandbox; pemeriksaan ini tidak membatasi bash. |
| `--max-idle`           | Berapa lama menunggu setelah sesi menjadi idle dengan [stop reason](https://platform.claude.com/docs/id/api/handling-stop-reasons) `end_turn` sebelum dimatikan. Default-nya `60s`.            |
| `--log-format`         | Format output log. Gunakan `json` untuk ingesti log terstruktur. Default-nya `text`.                                                                                                           |

Worker CLI tidak me-mount [memory store](https://platform.claude.com/docs/id/managed-agents/memory): sesi yang melampirkannya tetap berjalan, tetapi agen tidak menemukan apa pun di `mount_path` store tersebut dan tidak ada perubahan yang disinkronkan kembali ke store. Untuk menggunakan memory store dalam sesi pada environment self-hosted, jalankan worker SDK sebagai gantinya; lihat [Menggunakan memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores).

## Tipe server MCP yang didukung

Claude Managed Agents terhubung ke [server MCP jarak jauh](https://platform.claude.com/docs/id/agents-and-tools/remote-mcp-servers) yang mengekspos endpoint HTTP, atau ke server MCP privat melalui [tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview). Server harus mendukung transport streamable HTTP dari protokol MCP; server yang hanya mendukung transport SSE yang sudah deprecated tetap berfungsi melalui fallback otomatis. Lihat [Konektor MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector) untuk mendeklarasikan server pada agen.

Untuk informasi lebih lanjut tentang MCP dan membangun server MCP, lihat [dokumentasi MCP](https://modelcontextprotocol.io).

## Batas laju

Endpoint Managed Agents dikenai "rate limit" (batas laju) per organisasi:

| Operasi                                                  | Batas                      |
| -------------------------------------------------------- | -------------------------- |
| Endpoint pembuatan (seperti agen, sesi, dan environment) | 300 permintaan per menit   |
| Endpoint pembacaan (seperti retrieve, list, dan stream)  | 1.200 permintaan per menit |

[Batas pengeluaran dan batas laju tingkat penggunaan](https://platform.claude.com/docs/id/api/rate-limits) di tingkat organisasi juga berlaku.

## Pedoman branding

Bagi mitra yang mengintegrasikan Claude Managed Agents, penggunaan branding Claude bersifat opsional. Saat mereferensikan Claude dalam produk Anda:

**Diizinkan:**

* "Claude Agent" (lebih disukai untuk menu dropdown)
* "Claude" (ketika berada dalam menu yang sudah berlabel "Agents")
* "\{YourAgentName} Powered by Claude" (jika Anda sudah memiliki nama agen)

**Tidak diizinkan:**

* "Claude Code" atau "Claude Code Agent"
* "Claude Cowork" atau "Claude Cowork Agent"
* Seni ASCII bermerek Claude Code atau elemen visual yang meniru Claude Code

Produk Anda harus mempertahankan branding-nya sendiri dan tidak tampak sebagai Claude Code, Claude Cowork, atau produk Anthropic lainnya. Untuk pertanyaan tentang kepatuhan branding, hubungi [tim penjualan](https://www.anthropic.com/contact-sales) Anthropic.
