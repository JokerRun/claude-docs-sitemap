---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/reference
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 341b408f9fd9a4fc602cd5fdf953f324dcacb45f485d62de33501bb75de93507
---

# Referensi

Jenis event, flag CLI worker self-hosted, jenis server MCP yang didukung, batas laju, dan pedoman branding untuk Claude Managed Agents.

---

Halaman ini mengumpulkan materi referensi untuk Claude Managed Agents. Untuk panduan berorientasi tugas, ikuti tautan di setiap bagian. Untuk operasi pada resource sesi, lihat [Operasi sesi](/docs/id/managed-agents/session-operations).

<Note>
Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Jenis event \{#event-types}

String jenis event mengikuti konvensi penamaan `{domain}.{action}`. Lihat [Stream event sesi](/docs/id/managed-agents/events-and-streaming) untuk mengirim, melakukan streaming, dan mencantumkan event.

<Tabs>
  <Tab title="Event pengguna">

| Jenis | Deskripsi |
|------|-------------|
| `user.message` | Pesan pengguna dengan konten teks. |
| `user.interrupt` | Menghentikan agen di tengah eksekusi. |
| `user.custom_tool_result` | Respons terhadap panggilan alat kustom dari agen. |
| `user.tool_confirmation` | Menyetujui atau menolak panggilan alat agen atau MCP ketika kebijakan izin memerlukan konfirmasi. |
| `user.define_outcome` | Mendefinisikan [outcome](/docs/id/managed-agents/define-outcomes) yang menjadi target kerja agen.  |
| `user.tool_result` | Hanya untuk sesi dengan [environment](/docs/id/managed-agents/self-hosted-sandboxes) `self_hosted`, integrasi Anda bertanggung jawab untuk menyediakan hasil `agent_toolset`. Helper SDK dan CLI melakukan ini secara otomatis. |

  </Tab>
  <Tab title="Event agen">

| Jenis | Deskripsi |
|------|-------------|
| `agent.message` | Respons agen yang berisi blok konten teks. |
| `agent.thinking` | Konten pemikiran agen, dikeluarkan secara terpisah dari pesan. |
| `agent.tool_use` | Agen memanggil alat agen bawaan (bash, operasi file, dan sebagainya). |
| `agent.tool_result` | Hasil dari eksekusi alat agen bawaan. |
| `agent.mcp_tool_use` | Agen memanggil alat server MCP. |
| `agent.mcp_tool_result` | Hasil dari eksekusi alat MCP. |
| `agent.custom_tool_use` | Agen memanggil salah satu alat kustom Anda. Respons dengan event `user.custom_tool_result`. |
| `agent.thread_context_compacted` | Riwayat percakapan dipadatkan agar sesuai dengan jendela konteks. |
| `agent.thread_message_received` | Dalam sesi [multiagent](/docs/id/managed-agents/multi-agent), sebuah agen mengirimkan hasilnya ke koordinator. |
| `agent.thread_message_sent` | Dalam sesi [multiagent](/docs/id/managed-agents/multi-agent), koordinator mengirim tindak lanjut ke agen lain. |

  </Tab>
  <Tab title="Event sesi">

| Jenis | Deskripsi |
|------|-------------|
| `session.status_running` | Agen sedang aktif memproses. |
| `session.status_idle` | Agen menyelesaikan tugasnya saat ini dan menunggu input. Menyertakan `stop_reason` yang menunjukkan mengapa agen berhenti. |
| `session.status_rescheduled` | Terjadi error sementara dan sesi mencoba ulang secara otomatis. |
| `session.status_terminated` | Sesi berakhir karena error yang tidak dapat dipulihkan. |
| `session.deleted` | Sesi telah dihapus. Mengakhiri stream event aktif apa pun; tidak ada event lebih lanjut yang dikeluarkan untuk sesi ini. |
| `session.updated` | Permintaan pembaruan sesi mengubah setidaknya satu field. Hanya menyertakan field yang berubah. Pembaruan diterapkan pada giliran berikutnya. |
| `session.error` | Terjadi error selama pemrosesan. Menyertakan objek `error` bertipe dengan `retry_status`. |
| `session.thread_created` | Thread [multiagent](/docs/id/managed-agents/multi-agent) telah dibuat. |
| `session.thread_status_running` | Thread [multiagent](/docs/id/managed-agents/multi-agent) memulai aktivitas. |
| `session.thread_status_idle` | Thread [multiagent](/docs/id/managed-agents/multi-agent) menyelesaikan gilirannya dan menunggu input. Menyertakan `stop_reason`. |
| `session.thread_status_rescheduled` | Thread [multiagent](/docs/id/managed-agents/multi-agent) mengalami error sementara dan mencoba ulang secara otomatis. |
| `session.thread_status_terminated` | Thread [multiagent](/docs/id/managed-agents/multi-agent) diarsipkan atau mencapai error terminal. |

  </Tab>
  <Tab title="Event span">

Event span adalah penanda observabilitas yang membungkus aktivitas untuk pelacakan waktu dan penggunaan.

| Jenis | Deskripsi |
|------|-------------|
| `span.model_request_start` | Panggilan inferensi model telah dimulai. |
| `span.model_request_end` | Panggilan inferensi model telah selesai. Menyertakan `model_usage` dengan jumlah token. |
| `span.outcome_evaluation_start` | Evaluasi [outcome](/docs/id/managed-agents/define-outcomes) telah dimulai.  |
| `span.outcome_evaluation_ongoing` | Heartbeat selama evaluasi [outcome](/docs/id/managed-agents/define-outcomes) yang sedang berlangsung.  |
| `span.outcome_evaluation_end` | Evaluasi [outcome](/docs/id/managed-agents/define-outcomes) telah selesai.  |

  </Tab>
  <Tab title="Event sistem">

| Jenis | Deskripsi |
|------|-------------|
| `system.message` | Memperbarui prompt sistem agen di antara giliran. Hanya didukung pada Claude Opus 4.8. |

  </Tab>
</Tabs>

## Worker self-hosted \{#self-hosted-worker}

Berikut adalah flag CLI `ant beta:worker` untuk worker bawaan yang menjalankan environment `self_hosted`. Lihat [Sandbox self-hosted](/docs/id/managed-agents/self-hosted-sandboxes) untuk menyiapkan environment, menjalankan worker, dan opsi helper SDK.

| Flag | Deskripsi |
|------|-------------|
| `--environment-id` | Environment yang akan di-poll untuk pekerjaan. Juga membaca dari `ANTHROPIC_ENVIRONMENT_ID`. |
| `--environment-key` | Mengautentikasi worker dengan environment ini. Juga membaca dari `ANTHROPIC_ENVIRONMENT_KEY`. |
| `--workdir` | Direktori tempat skill diunduh dan alat membaca serta menulis file. Default-nya adalah `.` (direktori saat ini); direktori kerja default sistem adalah `/workspace`. |
| `--on-work` | Skrip yang dipanggil untuk setiap item pekerjaan yang diklaim alih-alih menjalankan alat dalam proses. Menerima detail sesi sebagai variabel environment. |
| `--unrestricted-paths` | Mengizinkan panggilan alat untuk mengakses path di luar `--workdir`. |
| `--max-idle` | Berapa lama menunggu setelah sesi menjadi idle dengan [stop reason](/docs/id/api/handling-stop-reasons) `end_turn` sebelum dimatikan. Default-nya adalah `60s`. |
| `--log-format` | Format output log. Gunakan `json` untuk ingesti log terstruktur. Default-nya adalah `text`. |

## Jenis server MCP yang didukung \{#supported-mcp-server-types}

Claude Managed Agents terhubung ke [server MCP jarak jauh](/docs/id/agents-and-tools/remote-mcp-servers) yang mengekspos endpoint HTTP, atau ke server MCP privat melalui [MCP tunnel](/docs/id/agents-and-tools/mcp-tunnels/overview). Server harus mendukung transport HTTP yang dapat di-stream dari protokol MCP. Lihat [Konektor MCP](/docs/id/managed-agents/mcp-connector) untuk mendeklarasikan server pada agen.

Untuk informasi lebih lanjut tentang MCP dan membangun server MCP, lihat [dokumentasi MCP](https://modelcontextprotocol.io).

## Batas laju \{#rate-limits}

Endpoint Managed Agents memiliki batas laju per organisasi:

| Operasi | Batas |
|-----------|-------|
| Endpoint pembuatan (seperti agen, sesi, dan environment) | 300 permintaan per menit |
| Endpoint pembacaan (seperti retrieve, list, dan stream) | 600 permintaan per menit |

[Batas pengeluaran dan batas laju berbasis tier](/docs/id/api/rate-limits) tingkat organisasi juga berlaku.

## Pedoman branding \{#branding-guidelines}

Untuk mitra yang mengintegrasikan Claude Managed Agents, penggunaan branding Claude bersifat opsional. Saat mereferensikan Claude dalam produk Anda:

**Diizinkan:**
- "Claude Agent" (lebih disukai untuk menu dropdown)
- "Claude" (ketika berada dalam menu yang sudah diberi label "Agents")
- "{YourAgentName} Powered by Claude" (jika Anda sudah memiliki nama agen)

**Tidak diizinkan:**
- "Claude Code" atau "Claude Code Agent"
- "Claude Cowork" atau "Claude Cowork Agent"
- Seni ASCII bermerek Claude Code atau elemen visual yang meniru Claude Code

Produk Anda harus mempertahankan branding-nya sendiri dan tidak tampak seperti Claude Code, Claude Cowork, atau produk Anthropic lainnya. Untuk pertanyaan tentang kepatuhan branding, hubungi [tim penjualan](https://www.anthropic.com/contact-sales) Anthropic.