---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/reference
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: d00b0b672b290059bda6ff17efc07be5b83f586c93ba3ac0f637c70f697875cb
---

# Referensi

Tipe event, flag CLI worker self-hosted, tipe server MCP yang didukung, batas laju, dan panduan branding untuk Claude Managed Agents.

---

Halaman ini mengumpulkan materi referensi untuk Claude Managed Agents. Untuk panduan yang berorientasi pada tugas, ikuti tautan di setiap bagian. Untuk operasi pada resource session, lihat [Operasi session](/docs/id/managed-agents/session-operations).

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Tipe event

String tipe event yang dipersistenkan mengikuti konvensi penamaan `{domain}.{action}`; event delta yang hanya untuk stream (lihat tab Event deltas) adalah pengecualiannya. Lihat [Stream event session](/docs/id/managed-agents/events-and-streaming) untuk mengirim, melakukan streaming, dan menampilkan daftar event.

<Tabs>
  <Tab title="User events">
    | Tipe                      | Deskripsi                                                                                                                                                                                                                          |
    | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `user.message`            | Pesan pengguna dengan konten teks, gambar, atau dokumen.                                                                                                                                                                           |
    | `user.interrupt`          | Menghentikan agen di tengah eksekusi.                                                                                                                                                                                              |
    | `user.custom_tool_result` | Respons terhadap panggilan custom tool dari agen.                                                                                                                                                                                  |
    | `user.tool_confirmation`  | Menyetujui atau menolak panggilan alat agen atau MCP ketika kebijakan izin memerlukan konfirmasi.                                                                                                                                  |
    | `user.define_outcome`     | Mendefinisikan sebuah [outcome](/docs/id/managed-agents/define-outcomes) yang menjadi tujuan kerja agen.                                                                                                                           |
    | `user.tool_result`        | Hanya untuk session dengan [environment](/docs/id/managed-agents/self-hosted-sandboxes) `self_hosted`, integrasi Anda bertanggung jawab untuk menyediakan hasil `agent_toolset`. Helper SDK dan CLI melakukan ini secara otomatis. |
  </Tab>

  <Tab title="Agent events">
    | Tipe                             | Deskripsi                                                                                                                                                                                                                              |
    | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `agent.message`                  | Respons agen yang berisi blok konten teks.                                                                                                                                                                                             |
    | `agent.thinking`                 | Menandakan agen sedang membuat kemajuan melalui "extended thinking" (pemikiran diperpanjang). Ini hanya sinyal kemajuan dan tidak membawa konten pemikiran.                                                                            |
    | `agent.tool_use`                 | Agen memanggil alat agen bawaan (bash, operasi file, dan sebagainya).                                                                                                                                                                  |
    | `agent.tool_result`              | Hasil dari eksekusi alat agen bawaan.                                                                                                                                                                                                  |
    | `agent.mcp_tool_use`             | Agen memanggil alat server MCP.                                                                                                                                                                                                        |
    | `agent.mcp_tool_result`          | Hasil dari eksekusi alat MCP.                                                                                                                                                                                                          |
    | `agent.custom_tool_use`          | Agen memanggil salah satu custom tool Anda. Balas dengan event `user.custom_tool_result`.                                                                                                                                              |
    | `agent.thread_context_compacted` | Riwayat percakapan dipadatkan agar muat dalam "context window" (jendela konteks).                                                                                                                                                      |
    | `agent.thread_message_received`  | Dalam session [multiagent](/docs/id/managed-agents/multiagent-orchestration), pesan dari thread lain tiba di thread yang stream-nya membawa event ini; pada thread utama, sebuah agen mengirim laporan atau pertanyaan ke koordinator. |
    | `agent.thread_message_sent`      | Dalam session [multiagent](/docs/id/managed-agents/multiagent-orchestration), thread yang stream-nya membawa event ini mengirim pesan ke thread lain; pada thread utama, koordinator mengirim tugas atau pesan lanjutan ke agen lain.  |
  </Tab>

  <Tab title="Session events">
    | Tipe                                | Deskripsi                                                                                                                                                                                                                                |
    | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `session.status_running`            | Agen sedang aktif memproses.                                                                                                                                                                                                             |
    | `session.status_idle`               | Agen menyelesaikan tugasnya saat ini dan sedang menunggu input. Menyertakan `stop_reason` yang menunjukkan mengapa agen berhenti.                                                                                                        |
    | `session.status_rescheduled`        | Terjadi error sementara dan session sedang mencoba ulang secara otomatis.                                                                                                                                                                |
    | `session.status_terminated`         | Session berakhir, baik karena error yang tidak dapat dipulihkan maupun karena selesai.                                                                                                                                                   |
    | `session.deleted`                   | Session dihapus. Mengakhiri setiap stream event yang aktif; tidak ada event lebih lanjut yang dikeluarkan untuk session ini.                                                                                                             |
    | `session.updated`                   | Permintaan pembaruan session mengubah setidaknya satu field. Hanya menyertakan field yang berubah. Pembaruan berlaku pada giliran berikutnya.                                                                                            |
    | `session.error`                     | Terjadi error selama pemrosesan. Menyertakan objek `error` bertipe dengan `retry_status`.                                                                                                                                                |
    | `session.thread_created`            | Sebuah thread [multiagent](/docs/id/managed-agents/multiagent-orchestration) dibuat.                                                                                                                                                     |
    | `session.thread_status_running`     | Sebuah thread session mulai dieksekusi. Setiap session mengeluarkan ini untuk thread utamanya; dalam session [multiagent](/docs/id/managed-agents/multiagent-orchestration), transisi thread anak juga diposting silang ke stream utama. |
    | `session.thread_status_idle`        | Sebuah thread session menyelesaikan gilirannya dan sedang menunggu input. Menyertakan `stop_reason`.                                                                                                                                     |
    | `session.thread_status_rescheduled` | Sebuah thread session mengalami error sementara dan sedang mencoba ulang secara otomatis.                                                                                                                                                |
    | `session.thread_status_terminated`  | Sebuah thread session diarsipkan atau mencapai error terminal.                                                                                                                                                                           |
  </Tab>

  <Tab title="Span events">
    Span event adalah penanda observabilitas yang membungkus aktivitas untuk pelacakan waktu dan penggunaan.

    | Tipe                              | Deskripsi                                                                                                                                                                                                                         |
    | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `span.model_request_start`        | Panggilan inferensi model telah dimulai.                                                                                                                                                                                          |
    | `span.model_request_end`          | Panggilan inferensi model telah selesai. Menyertakan `model_usage` dengan jumlah token.                                                                                                                                           |
    | `span.outcome_evaluation_start`   | Evaluasi [outcome](/docs/id/managed-agents/define-outcomes) telah dimulai.                                                                                                                                                        |
    | `span.outcome_evaluation_ongoing` | Heartbeat selama evaluasi [outcome](/docs/id/managed-agents/define-outcomes) yang sedang berlangsung.                                                                                                                             |
    | `span.outcome_evaluation_end`     | Siklus evaluasi [outcome](/docs/id/managed-agents/define-outcomes) telah selesai. Hasil `needs_revision` berarti siklus lain akan menyusul; `satisfied`, `max_iterations_reached`, `failed`, dan `interrupted` bersifat terminal. |
  </Tab>

  <Tab title="System events">
    | Tipe             | Deskripsi                                                                                                                                                                                                                                                                                                                                  |
    | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | `system.message` | Menambahkan konteks tingkat sistem yang memiliki hak istimewa yang berlaku untuk giliran yang menyertainya dan semua giliran berikutnya. Didukung pada Claude Opus 4.8, Claude Sonnet 5, Claude Fable 5, dan Claude Mythos 5; pada model utama yang tidak didukung, event ditolak dengan `model_does_not_support_mid_conversation_system`. |
  </Tab>

  <Tab title="Event deltas">
    Event delta adalah event pratinjau yang hanya untuk stream. Event ini dikeluarkan pada koneksi stream (tingkat session atau per-thread) yang memilih ikut serta dengan parameter `event_deltas[]`, dan tidak pernah dipersistenkan ke riwayat event session. Lihat [Event deltas](/docs/id/managed-agents/events-and-streaming#event-deltas) untuk memilih ikut serta, mengakumulasi, dan merekonsiliasinya.

    | Tipe          | Deskripsi                                                                                                                                               |
    | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `event_start` | Event yang dipratinjau telah mulai dihasilkan. Membawa `type` dan `id` dari event yang akan datang. Hanya untuk stream dan tidak pernah dipersistenkan. |
    | `event_delta` | Konten inkremental untuk event yang dipratinjau, diidentifikasi dengan `event_id`. Hanya untuk stream dan tidak pernah dipersistenkan.                  |
  </Tab>
</Tabs>

## Worker self-hosted

Berikut adalah flag CLI `ant beta:worker` untuk worker bawaan yang menjalankan environment `self_hosted`. Lihat [Sandbox self-hosted](/docs/id/managed-agents/self-hosted-sandboxes) untuk menyiapkan environment, menjalankan worker, dan opsi helper SDK.

| Flag                   | Deskripsi                                                                                                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--environment-id`     | Environment yang akan di-poll untuk pekerjaan. Juga membaca dari `ANTHROPIC_ENVIRONMENT_ID`.                                                                                    |
| `--environment-key`    | Mengautentikasi worker dengan environment ini. Juga membaca dari `ANTHROPIC_ENVIRONMENT_KEY`.                                                                                   |
| `--workdir`            | Direktori tempat skill diunduh dan alat membaca serta menulis file. Default-nya adalah `.` (direktori saat ini); direktori kerja default sistem adalah `/workspace`.            |
| `--on-work`            | Skrip yang dipanggil untuk setiap item pekerjaan yang diklaim alih-alih menjalankan alat secara in-process. Menerima detail session sebagai variabel lingkungan.                |
| `--unrestricted-paths` | Mengizinkan alat file untuk membaca dan menulis path di luar `--workdir`. Pemeriksaan workdir hanyalah pagar pengaman untuk alat file, bukan sandbox; ini tidak membatasi bash. |
| `--max-idle`           | Berapa lama menunggu setelah session menjadi idle dengan [stop reason](/docs/id/api/handling-stop-reasons) `end_turn` sebelum dimatikan. Default-nya adalah `60s`.              |
| `--log-format`         | Format output log. Gunakan `json` untuk ingesti log terstruktur. Default-nya adalah `text`.                                                                                     |

## Tipe server MCP yang didukung

Claude Managed Agents terhubung ke [server MCP jarak jauh](/docs/id/agents-and-tools/remote-mcp-servers) yang mengekspos endpoint HTTP, atau ke server MCP privat melalui [tunnel MCP](/docs/id/agents-and-tools/mcp-tunnels/overview). Server harus mendukung transport streamable HTTP dari protokol MCP; server yang hanya mendukung transport SSE yang sudah usang tetap berfungsi melalui fallback otomatis. Lihat [Konektor MCP](/docs/id/managed-agents/mcp-connector) untuk mendeklarasikan server pada sebuah agen.

Untuk informasi lebih lanjut tentang MCP dan membangun server MCP, lihat [dokumentasi MCP](https://modelcontextprotocol.io).

## Batas laju

Endpoint Managed Agents dibatasi lajunya per organisasi:

| Operasi                                                     | Batas                      |
| ----------------------------------------------------------- | -------------------------- |
| Endpoint pembuatan (seperti agen, session, dan environment) | 300 permintaan per menit   |
| Endpoint pembacaan (seperti retrieve, list, dan stream)     | 1.200 permintaan per menit |

[Batas pengeluaran dan batas laju tingkat penggunaan](/docs/id/api/rate-limits) di tingkat organisasi juga berlaku.

## Panduan branding

Untuk mitra yang mengintegrasikan Claude Managed Agents, penggunaan branding Claude bersifat opsional. Saat merujuk Claude dalam produk Anda:

**Diizinkan:**

* "Claude Agent" (lebih disukai untuk menu dropdown)
* "Claude" (ketika berada dalam menu yang sudah berlabel "Agents")
* "\{YourAgentName} Powered by Claude" (jika Anda sudah memiliki nama agen)

**Tidak diizinkan:**

* "Claude Code" atau "Claude Code Agent"
* "Claude Cowork" atau "Claude Cowork Agent"
* ASCII art ber-branding Claude Code atau elemen visual yang meniru Claude Code

Produk Anda harus mempertahankan branding-nya sendiri dan tidak boleh tampak seperti Claude Code, Claude Cowork, atau produk Anthropic lainnya. Untuk pertanyaan tentang kepatuhan branding, hubungi [tim penjualan](https://www.anthropic.com/contact-sales) Anthropic.
