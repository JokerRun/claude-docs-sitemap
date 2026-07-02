---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/reference
fetched_at: 2026-07-02T03:13:49.360020Z
sha256: da80b9747c5221357b9658167bd2fb1e56ae8c4388eedae1b60a50db11470fd8
---

# Referensi

Tipe event, flag CLI worker self-hosted, tipe server MCP yang didukung, batas laju, dan panduan branding untuk Claude Managed Agents.

---

Halaman ini mengumpulkan materi referensi untuk Claude Managed Agents. Untuk panduan berorientasi tugas, ikuti tautan di setiap bagian. Untuk operasi pada resource sesi, lihat [Operasi sesi](/docs/id/managed-agents/session-operations).

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Tipe event

String tipe event yang dipersistensi mengikuti konvensi penamaan `{domain}.{action}`; delta event yang hanya muncul di stream (lihat tab Delta event) adalah pengecualian. Lihat [Stream event sesi](/docs/id/managed-agents/events-and-streaming) untuk mengirim, melakukan streaming, dan mencantumkan event.

<Tabs>
  <Tab title="Event pengguna">
    | Tipe                      | Deskripsi                                                                                                                                                                                                                       |
    | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `user.message`            | Pesan pengguna dengan konten teks.                                                                                                                                                                                              |
    | `user.interrupt`          | Menghentikan agen di tengah eksekusi.                                                                                                                                                                                           |
    | `user.custom_tool_result` | Respons terhadap panggilan alat kustom dari agen.                                                                                                                                                                               |
    | `user.tool_confirmation`  | Menyetujui atau menolak panggilan alat agen atau MCP ketika kebijakan izin memerlukan konfirmasi.                                                                                                                               |
    | `user.define_outcome`     | Mendefinisikan [outcome](/docs/id/managed-agents/define-outcomes) yang menjadi target kerja agen.                                                                                                                               |
    | `user.tool_result`        | Hanya untuk sesi dengan [environment](/docs/id/managed-agents/self-hosted-sandboxes) `self_hosted`, integrasi Anda bertanggung jawab untuk menyediakan hasil `agent_toolset`. Helper SDK dan CLI melakukan ini secara otomatis. |
  </Tab>

  <Tab title="Event agen">
    | Tipe                             | Deskripsi                                                                                                      |
    | -------------------------------- | -------------------------------------------------------------------------------------------------------------- |
    | `agent.message`                  | Respons agen yang berisi blok konten teks.                                                                     |
    | `agent.thinking`                 | Konten pemikiran agen, dikeluarkan secara terpisah dari pesan.                                                 |
    | `agent.tool_use`                 | Agen memanggil alat agen bawaan (bash, operasi file, dan sebagainya).                                          |
    | `agent.tool_result`              | Hasil eksekusi alat agen bawaan.                                                                               |
    | `agent.mcp_tool_use`             | Agen memanggil alat server MCP.                                                                                |
    | `agent.mcp_tool_result`          | Hasil eksekusi alat MCP.                                                                                       |
    | `agent.custom_tool_use`          | Agen memanggil salah satu alat kustom Anda. Respons dengan event `user.custom_tool_result`.                    |
    | `agent.thread_context_compacted` | Riwayat percakapan dipadatkan agar sesuai dengan jendela konteks.                                              |
    | `agent.thread_message_received`  | Dalam sesi [multi-agen](/docs/id/managed-agents/multi-agent), sebuah agen mengirimkan hasilnya ke koordinator. |
    | `agent.thread_message_sent`      | Dalam sesi [multi-agen](/docs/id/managed-agents/multi-agent), koordinator mengirim tindak lanjut ke agen lain. |
  </Tab>

  <Tab title="Event sesi">
    | Tipe                                | Deskripsi                                                                                                                                     |
    | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
    | `session.status_running`            | Agen sedang aktif memproses.                                                                                                                  |
    | `session.status_idle`               | Agen menyelesaikan tugasnya saat ini dan menunggu input. Menyertakan `stop_reason` yang menunjukkan mengapa agen berhenti.                    |
    | `session.status_rescheduled`        | Terjadi error sementara dan sesi mencoba ulang secara otomatis.                                                                               |
    | `session.status_terminated`         | Sesi berakhir karena error yang tidak dapat dipulihkan.                                                                                       |
    | `session.deleted`                   | Sesi telah dihapus. Mengakhiri stream event aktif apa pun; tidak ada event lebih lanjut yang dikeluarkan untuk sesi ini.                      |
    | `session.updated`                   | Permintaan pembaruan sesi mengubah setidaknya satu field. Hanya menyertakan field yang berubah. Pembaruan diterapkan pada giliran berikutnya. |
    | `session.error`                     | Terjadi error selama pemrosesan. Menyertakan objek `error` bertipe dengan `retry_status`.                                                     |
    | `session.thread_created`            | Sebuah thread [multi-agen](/docs/id/managed-agents/multi-agent) telah dibuat.                                                                 |
    | `session.thread_status_running`     | Sebuah thread [multi-agen](/docs/id/managed-agents/multi-agent) memulai aktivitas.                                                            |
    | `session.thread_status_idle`        | Sebuah thread [multi-agen](/docs/id/managed-agents/multi-agent) menyelesaikan gilirannya dan menunggu input. Menyertakan `stop_reason`.       |
    | `session.thread_status_rescheduled` | Sebuah thread [multi-agen](/docs/id/managed-agents/multi-agent) mengalami error sementara dan mencoba ulang secara otomatis.                  |
    | `session.thread_status_terminated`  | Sebuah thread [multi-agen](/docs/id/managed-agents/multi-agent) diarsipkan atau mencapai error terminal.                                      |
  </Tab>

  <Tab title="Event span">
    Event span adalah penanda observabilitas yang membungkus aktivitas untuk pelacakan waktu dan penggunaan.

    | Tipe                              | Deskripsi                                                                                             |
    | --------------------------------- | ----------------------------------------------------------------------------------------------------- |
    | `span.model_request_start`        | Panggilan inferensi model telah dimulai.                                                              |
    | `span.model_request_end`          | Panggilan inferensi model telah selesai. Menyertakan `model_usage` dengan jumlah token.               |
    | `span.outcome_evaluation_start`   | Evaluasi [outcome](/docs/id/managed-agents/define-outcomes) telah dimulai.                            |
    | `span.outcome_evaluation_ongoing` | Heartbeat selama evaluasi [outcome](/docs/id/managed-agents/define-outcomes) yang sedang berlangsung. |
    | `span.outcome_evaluation_end`     | Evaluasi [outcome](/docs/id/managed-agents/define-outcomes) telah selesai.                            |
  </Tab>

  <Tab title="Event sistem">
    | Tipe             | Deskripsi                                                                              |
    | ---------------- | -------------------------------------------------------------------------------------- |
    | `system.message` | Memperbarui prompt sistem agen di antara giliran. Hanya didukung pada Claude Opus 4.8. |
  </Tab>

  <Tab title="Delta event">
    Delta event adalah event pratinjau yang hanya muncul di stream. Event ini dikeluarkan pada koneksi stream event sesi yang memilih untuk ikut serta dengan parameter `event_deltas[]`, dan tidak pernah dipersistensi ke riwayat event sesi. Lihat [Delta event](/docs/id/managed-agents/events-and-streaming#event-deltas) untuk memilih ikut serta, mengakumulasi, dan merekonsiliasinya.

    | Tipe          | Deskripsi                                                                                                                                                  |
    | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `event_start` | Event yang dipratinjau telah mulai dihasilkan. Membawa `type` dan `id` dari event yang akan datang. Hanya muncul di stream dan tidak pernah dipersistensi. |
    | `event_delta` | Konten inkremental untuk event yang dipratinjau, diidentifikasi oleh `event_id`. Hanya muncul di stream dan tidak pernah dipersistensi.                    |
  </Tab>
</Tabs>

## Worker self-hosted

Berikut adalah flag CLI `ant beta:worker` untuk worker bawaan yang menjalankan environment `self_hosted`. Lihat [Sandbox self-hosted](/docs/id/managed-agents/self-hosted-sandboxes) untuk menyiapkan environment, menjalankan worker, dan opsi helper SDK.

| Flag                   | Deskripsi                                                                                                                                                            |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--environment-id`     | Environment yang akan di-poll untuk pekerjaan. Juga membaca dari `ANTHROPIC_ENVIRONMENT_ID`.                                                                         |
| `--environment-key`    | Mengautentikasi worker dengan environment ini. Juga membaca dari `ANTHROPIC_ENVIRONMENT_KEY`.                                                                        |
| `--workdir`            | Direktori tempat skill diunduh dan alat membaca serta menulis file. Default-nya adalah `.` (direktori saat ini); direktori kerja default sistem adalah `/workspace`. |
| `--on-work`            | Skrip yang dipanggil untuk setiap item pekerjaan yang diklaim alih-alih menjalankan alat secara in-process. Menerima detail sesi sebagai variabel environment.       |
| `--unrestricted-paths` | Mengizinkan panggilan alat untuk mengakses path di luar `--workdir`.                                                                                                 |
| `--max-idle`           | Berapa lama menunggu setelah sesi menjadi idle dengan [stop reason](/docs/id/api/handling-stop-reasons) `end_turn` sebelum dimatikan. Default-nya adalah `60s`.      |
| `--log-format`         | Format output log. Gunakan `json` untuk ingesti log terstruktur. Default-nya adalah `text`.                                                                          |

## Tipe server MCP yang didukung

Claude Managed Agents terhubung ke [server MCP remote](/docs/id/agents-and-tools/remote-mcp-servers) yang mengekspos endpoint HTTP, atau ke server MCP privat melalui [MCP tunnel](/docs/id/agents-and-tools/mcp-tunnels/overview). Server harus mendukung transport HTTP streamable dari protokol MCP. Lihat [Konektor MCP](/docs/id/managed-agents/mcp-connector) untuk mendeklarasikan server pada agen.

Untuk informasi lebih lanjut tentang MCP dan membangun server MCP, lihat [dokumentasi MCP](https://modelcontextprotocol.io).

## Batas laju

Endpoint Managed Agents dibatasi lajunya per organisasi:

| Operasi                                                  | Batas                      |
| -------------------------------------------------------- | -------------------------- |
| Endpoint pembuatan (seperti agen, sesi, dan environment) | 300 permintaan per menit   |
| Endpoint pembacaan (seperti retrieve, list, dan stream)  | 1.200 permintaan per menit |

[Batas pengeluaran dan batas laju tingkat penggunaan](/docs/id/api/rate-limits) di tingkat organisasi juga berlaku.

## Panduan branding

Untuk mitra yang mengintegrasikan Claude Managed Agents, penggunaan branding Claude bersifat opsional. Saat mereferensikan Claude dalam produk Anda:

**Diizinkan:**

* "Claude Agent" (lebih disukai untuk menu dropdown)
* "Claude" (ketika berada dalam menu yang sudah diberi label "Agents")
* "\{NamaAgenAnda} Powered by Claude" (jika Anda memiliki nama agen yang sudah ada)

**Tidak diizinkan:**

* "Claude Code" atau "Claude Code Agent"
* "Claude Cowork" atau "Claude Cowork Agent"
* Seni ASCII bermerek Claude Code atau elemen visual yang meniru Claude Code

Produk Anda harus mempertahankan branding-nya sendiri dan tidak tampak seperti Claude Code, Claude Cowork, atau produk Anthropic lainnya. Untuk pertanyaan tentang kepatuhan branding, hubungi [tim penjualan](https://www.anthropic.com/contact-sales) Anthropic.
