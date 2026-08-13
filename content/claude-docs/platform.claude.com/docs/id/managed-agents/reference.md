---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/reference
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: d6cfaf154c8ed890b9b1d333cdca77b82fbfb570b703cddb16ecb78688f57522
---

---
title: Referensi
url: https://platform.claude.com/docs/id/managed-agents/reference
description: Jenis event, flag CLI worker self-hosted, jenis server MCP yang didukung, batas laju, dan pedoman branding untuk Claude Managed Agents.
---

Halaman ini mengumpulkan materi referensi untuk Claude Managed Agents. Untuk panduan berorientasi tugas, ikuti tautan di setiap bagian. Untuk operasi pada resource session, lihat [Operasi session](https://platform.claude.com/docs/id/managed-agents/session-operations).

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Jenis event

String jenis event yang dipersistensi mengikuti konvensi penamaan `{domain}.{action}`; event delta yang hanya muncul di stream (lihat tab Event delta) adalah pengecualian. Lihat [Stream event session](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) untuk mengirim, melakukan streaming, dan mencantumkan event.

<Tabs>
  <Tab title="Event pengguna">
    | Jenis                     | Deskripsi                                                                                                                                                                                                                                                     |
    | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `user.message`            | Pesan pengguna dengan konten teks, gambar, atau dokumen.                                                                                                                                                                                                      |
    | `user.interrupt`          | Menghentikan agen di tengah eksekusi.                                                                                                                                                                                                                         |
    | `user.custom_tool_result` | Respons terhadap panggilan alat kustom dari agen.                                                                                                                                                                                                             |
    | `user.tool_confirmation`  | Menyetujui atau menolak panggilan alat agen atau MCP ketika kebijakan izin memerlukan konfirmasi.                                                                                                                                                             |
    | `user.define_outcome`     | Mendefinisikan [outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) yang menjadi tujuan kerja agen.                                                                                                                                  |
    | `user.tool_result`        | Hanya untuk session dengan [environment](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) `self_hosted`, integrasi Anda bertanggung jawab untuk menyediakan hasil `agent_toolset`. Helper SDK dan CLI melakukan ini secara otomatis. |
  </Tab>

  <Tab title="Event agen">
    | Jenis                            | Deskripsi                                                                                                                                                                                                                                                             |
    | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `agent.message`                  | Blok konten respons agen.                                                                                                                                                                                                                                             |
    | `agent.thinking`                 | Menandakan agen sedang membuat kemajuan melalui pemikiran diperpanjang. Ini hanya sinyal kemajuan dan tidak membawa konten pemikiran.                                                                                                                                 |
    | `agent.tool_use`                 | Agen memanggil alat agen bawaan (bash, operasi file, dan sebagainya).                                                                                                                                                                                                 |
    | `agent.tool_result`              | Hasil dari eksekusi alat agen bawaan.                                                                                                                                                                                                                                 |
    | `agent.mcp_tool_use`             | Agen memanggil alat server MCP.                                                                                                                                                                                                                                       |
    | `agent.mcp_tool_result`          | Hasil dari eksekusi alat MCP.                                                                                                                                                                                                                                         |
    | `agent.custom_tool_use`          | Agen memanggil salah satu alat kustom Anda. Respons dengan event `user.custom_tool_result`.                                                                                                                                                                           |
    | `agent.thread_context_compacted` | Riwayat percakapan dipadatkan agar sesuai dengan jendela konteks.                                                                                                                                                                                                     |
    | `agent.thread_message_received`  | Dalam session [multiagent](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), pesan dari thread lain tiba di thread yang stream-nya membawa event ini; pada thread utama, sebuah agen mengirim laporan atau pertanyaan ke koordinator.     |
    | `agent.thread_message_sent`      | Dalam session [multiagent](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), thread yang stream-nya membawa event ini mengirim pesan ke thread lain; pada thread utama, koordinator mengirim tugas atau pesan tindak lanjut ke agen lain. |

    Konten pesan dalam event ini dapat menyertakan blok konten `redacted`, `{"type": "redacted"}`: placeholder untuk konten yang ditahan oleh kebijakan model Anthropic. Blok ini tidak membawa field lain. Blok redacted hanya muncul dalam konten yang dikeluarkan oleh platform; event pengguna yang menyertakannya akan ditolak dengan error 400.
  </Tab>

  <Tab title="Event session">
    | Jenis                               | Deskripsi                                                                                                                                                                                                                                                 |
    | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `session.status_running`            | Agen sedang aktif memproses.                                                                                                                                                                                                                              |
    | `session.status_idle`               | Agen menyelesaikan tugasnya saat ini dan menunggu input. Menyertakan `stop_reason` yang menunjukkan mengapa agen berhenti.                                                                                                                                |
    | `session.status_rescheduled`        | Terjadi error sementara dan session mencoba ulang secara otomatis.                                                                                                                                                                                        |
    | `session.status_terminated`         | Session berakhir, baik karena error yang tidak dapat dipulihkan atau karena diarsipkan.                                                                                                                                                                   |
    | `session.deleted`                   | Session dihapus. Mengakhiri stream event aktif apa pun; tidak ada event lebih lanjut yang dikeluarkan untuk session ini.                                                                                                                                  |
    | `session.updated`                   | Permintaan pembaruan session mengubah setidaknya satu field. Hanya menyertakan field yang berubah. Pembaruan diterapkan pada giliran berikutnya.                                                                                                          |
    | `session.error`                     | Terjadi error selama pemrosesan. Menyertakan objek `error` bertipe dengan `retry_status`.                                                                                                                                                                 |
    | `session.usage`                     | Snapshot penggunaan kumulatif session dan biaya daftar yang dilacak. Membawa total penggunaan session dan salinan [budget](https://platform.claude.com/docs/id/managed-agents/budgets) session, atau `null` jika session tidak memilikinya.               |
    | `session.thread_created`            | Thread [multiagent](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) telah dibuat.                                                                                                                                            |
    | `session.thread_status_running`     | Thread session mulai dieksekusi. Setiap session mengeluarkan ini untuk thread utamanya; dalam session [multiagent](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), transisi thread anak juga di-cross-post ke stream utama. |
    | `session.thread_status_idle`        | Thread session menyelesaikan gilirannya dan menunggu input. Menyertakan `stop_reason`.                                                                                                                                                                    |
    | `session.thread_status_rescheduled` | Thread session mengalami error sementara dan mencoba ulang secara otomatis.                                                                                                                                                                               |
    | `session.thread_status_terminated`  | Thread session diarsipkan atau mencapai error terminal.                                                                                                                                                                                                   |
  </Tab>

  <Tab title="Event span">
    Event span adalah penanda observabilitas yang membungkus aktivitas untuk pelacakan waktu dan penggunaan.

    | Jenis                             | Deskripsi                                                                                                                                                                                                                                                     |
    | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `span.model_request_start`        | Panggilan inferensi model telah dimulai.                                                                                                                                                                                                                      |
    | `span.model_request_end`          | Panggilan inferensi model telah selesai. Menyertakan `model_usage` dengan jumlah token.                                                                                                                                                                       |
    | `span.outcome_evaluation_start`   | Evaluasi [outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) telah dimulai.                                                                                                                                                         |
    | `span.outcome_evaluation_ongoing` | Heartbeat selama evaluasi [outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) yang sedang berlangsung.                                                                                                                              |
    | `span.outcome_evaluation_end`     | Siklus evaluasi [outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) telah selesai. Hasil `needs_revision` berarti siklus lain akan mengikuti; `satisfied`, `max_iterations_reached`, `failed`, dan `interrupted` bersifat terminal. |
  </Tab>

  <Tab title="Event sistem">
    | Jenis            | Deskripsi                                                                                                                                                                                                                                                                                                                             |
    | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `system.message` | Menambahkan konteks tingkat sistem dengan hak istimewa yang berlaku untuk giliran yang menyertainya dan semua giliran berikutnya. Didukung pada Claude Opus 4.8, Claude Fable 5, Claude Mythos 5, dan Claude Opus 5; pada model utama yang tidak didukung, event ini ditolak dengan `model_does_not_support_mid_conversation_system`. |
  </Tab>

  <Tab title="Event delta">
    Event delta adalah event pratinjau yang hanya muncul di stream. Event ini dikeluarkan pada koneksi stream (tingkat session atau per-thread) yang memilih ikut serta dengan parameter `event_deltas[]`, dan tidak pernah dipersistensi ke riwayat event session. Lihat [Event delta](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#event-deltas) untuk memilih ikut serta, mengakumulasi, dan merekonsiliasinya.

    | Jenis         | Deskripsi                                                                                                                                                  |
    | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `event_start` | Event yang dipratinjau telah mulai dihasilkan. Membawa `type` dan `id` dari event yang akan datang. Hanya muncul di stream dan tidak pernah dipersistensi. |
    | `event_delta` | Konten inkremental untuk event yang dipratinjau, diidentifikasi oleh `event_id`. Hanya muncul di stream dan tidak pernah dipersistensi.                    |
  </Tab>
</Tabs>

## Worker self-hosted

Berikut adalah flag CLI `ant beta:worker` untuk worker bawaan yang menjalankan environment `self_hosted`. Lihat [Sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) untuk menyiapkan environment, menjalankan worker, dan opsi helper SDK.

| Flag                   | Deskripsi                                                                                                                                                                                     |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--environment-id`     | Environment yang akan di-poll untuk pekerjaan. Juga membaca dari `ANTHROPIC_ENVIRONMENT_ID`.                                                                                                  |
| `--environment-key`    | Mengautentikasi worker dengan environment ini. Juga membaca dari `ANTHROPIC_ENVIRONMENT_KEY`.                                                                                                 |
| `--workdir`            | Direktori tempat skill diunduh dan alat membaca serta menulis file. Default-nya adalah `.` (direktori saat ini); direktori kerja default sistem adalah `/workspace`.                          |
| `--on-work`            | Skrip yang dipanggil untuk setiap item pekerjaan yang diklaim alih-alih menjalankan alat dalam proses. Menerima detail session sebagai variabel environment.                                  |
| `--unrestricted-paths` | Mengizinkan alat file untuk membaca dan menulis path di luar `--workdir`. Pemeriksaan workdir hanya merupakan pagar pengaman untuk alat file, bukan sandbox; ini tidak membatasi bash.        |
| `--max-idle`           | Berapa lama menunggu setelah session menjadi idle dengan [stop reason](https://platform.claude.com/docs/id/api/handling-stop-reasons) `end_turn` sebelum dimatikan. Default-nya adalah `60s`. |
| `--log-format`         | Format output log. Gunakan `json` untuk ingesti log terstruktur. Default-nya adalah `text`.                                                                                                   |

## Jenis server MCP yang didukung

Claude Managed Agents terhubung ke [server MCP jarak jauh](https://platform.claude.com/docs/id/agents-and-tools/remote-mcp-servers) yang mengekspos endpoint HTTP, atau ke server MCP privat melalui [MCP tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview). Server harus mendukung transport HTTP yang dapat di-stream dari protokol MCP; server yang hanya mendukung transport SSE yang sudah tidak digunakan lagi tetap berfungsi melalui fallback otomatis. Lihat [Konektor MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector) untuk mendeklarasikan server pada agen.

Untuk informasi lebih lanjut tentang MCP dan membangun server MCP, lihat [dokumentasi MCP](https://modelcontextprotocol.io).

## Batas laju

Endpoint Managed Agents dibatasi lajunya per organisasi:

| Operasi                                                     | Batas                      |
| ----------------------------------------------------------- | -------------------------- |
| Endpoint pembuatan (seperti agen, session, dan environment) | 300 permintaan per menit   |
| Endpoint pembacaan (seperti retrieve, list, dan stream)     | 1.200 permintaan per menit |

[Batas pengeluaran dan batas laju tingkat penggunaan](https://platform.claude.com/docs/id/api/rate-limits) tingkat organisasi juga berlaku.

## Pedoman branding

Untuk mitra yang mengintegrasikan Claude Managed Agents, penggunaan branding Claude bersifat opsional. Saat mereferensikan Claude dalam produk Anda:

**Diizinkan:**

* "Claude Agent" (lebih disukai untuk menu dropdown)
* "Claude" (ketika berada dalam menu yang sudah berlabel "Agents")
* "\{NamaAgenAnda} Powered by Claude" (jika Anda memiliki nama agen yang sudah ada)

**Tidak diizinkan:**

* "Claude Code" atau "Claude Code Agent"
* "Claude Cowork" atau "Claude Cowork Agent"
* Seni ASCII bermerek Claude Code atau elemen visual yang meniru Claude Code

Produk Anda harus mempertahankan branding-nya sendiri dan tidak tampak seperti Claude Code, Claude Cowork, atau produk Anthropic lainnya. Untuk pertanyaan tentang kepatuhan branding, hubungi [tim penjualan](https://www.anthropic.com/contact-sales) Anthropic.
