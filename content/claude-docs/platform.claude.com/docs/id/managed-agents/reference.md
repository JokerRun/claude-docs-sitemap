---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/reference
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: 071d65c5200bf7f81bf7687d4c35aeb23046ad898140d769585ffb741d319618
---

---
title: Referensi
url: https://platform.claude.com/docs/id/managed-agents/reference
description: Tipe event, flag CLI worker self-hosted, tipe server MCP yang didukung, batas laju, dan pedoman branding untuk Claude Managed Agents.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Halaman ini mengumpulkan materi referensi untuk Claude Managed Agents. Untuk panduan berorientasi tugas, ikuti tautan di setiap bagian. Untuk operasi pada resource sesi, lihat [Operasi sesi](https://platform.claude.com/docs/id/managed-agents/session-operations).

## Tipe event

String tipe event yang dipersistenkan mengikuti konvensi penamaan `{domain}.{action}`; event delta yang hanya tersedia di stream (lihat tab Event deltas) adalah pengecualiannya. Lihat [Stream event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) untuk mengirim, melakukan streaming, dan mendaftar event. Tipe event webhook didaftarkan secara terpisah di [Berlangganan webhook](https://platform.claude.com/docs/id/managed-agents/webhooks#supported-event-types), dan beberapa namanya berbeda dari nama di stream (misalnya, `session.status_idled` alih-alih `session.status_idle`).

<Tabs>
  <Tab title="Event pengguna">
    | Tipe                      | Deskripsi                                                                                                                                                                                                                                                  |
    | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `user.message`            | Pesan pengguna dengan konten teks, gambar, atau dokumen.                                                                                                                                                                                                   |
    | `user.interrupt`          | Menghentikan agen di tengah eksekusi. Event ini tidak mengakhiri [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open) apa pun.                                                         |
    | `user.custom_tool_result` | Respons terhadap panggilan alat kustom dari agen.                                                                                                                                                                                                          |
    | `user.tool_confirmation`  | Menyetujui atau menolak panggilan alat agen atau MCP ketika kebijakan izin memerlukan konfirmasi.                                                                                                                                                          |
    | `user.define_outcome`     | Mendefinisikan [outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) yang akan dikerjakan oleh agen.                                                                                                                               |
    | `user.tool_result`        | Hanya untuk sesi dengan [environment](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) `self_hosted`, integrasi Anda bertanggung jawab untuk menyediakan hasil `agent_toolset`. Helper SDK dan CLI melakukan ini secara otomatis. |
  </Tab>

  <Tab title="Event agen">
    | Jenis                            | Deskripsi                                                                                                                                                                                                                                                                                 |
    | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `agent.message`                  | Blok konten respons agen.                                                                                                                                                                                                                                                                 |
    | `agent.thinking`                 | Menandakan bahwa agen sedang membuat kemajuan melalui "extended thinking" (pemikiran diperpanjang). Ini hanya sinyal kemajuan dan tidak membawa konten pemikiran.                                                                                                                         |
    | `agent.tool_use`                 | Agen memanggil alat agen bawaan (bash, operasi file, dan sebagainya). Membawa `evaluated_permission` dan, biasanya, `evaluation` (lihat [bagaimana setiap panggilan dievaluasi](https://platform.claude.com/docs/id/managed-agents/permission-policies#see-how-each-call-was-evaluated)). |
    | `agent.tool_result`              | Hasil eksekusi alat agen bawaan.                                                                                                                                                                                                                                                          |
    | `agent.mcp_tool_use`             | Agen memanggil alat server MCP. Membawa `evaluated_permission` dan, biasanya, `evaluation` (lihat [bagaimana setiap panggilan dievaluasi](https://platform.claude.com/docs/id/managed-agents/permission-policies#see-how-each-call-was-evaluated)).                                       |
    | `agent.mcp_tool_result`          | Hasil eksekusi alat MCP.                                                                                                                                                                                                                                                                  |
    | `agent.custom_tool_use`          | Agen memanggil salah satu alat kustom Anda. Tanggapi dengan event `user.custom_tool_result`.                                                                                                                                                                                              |
    | `agent.thread_context_compacted` | Riwayat percakapan dipadatkan agar muat dalam "context window" (jendela konteks).                                                                                                                                                                                                         |
    | `agent.thread_message_received`  | Dalam sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), pesan dari thread lain tiba di thread yang alirannya membawa event ini; pada thread utama, sebuah agen mengirim laporan atau pertanyaan kepada agen yang dijalankan oleh sesi.       |
    | `agent.thread_message_sent`      | Dalam sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), thread yang alirannya membawa event ini mengirim pesan ke thread lain; pada thread utama, agen yang dijalankan oleh sesi mengirim tugas atau pesan tindak lanjut ke agen lain.       |

    Konten pesan dalam event-event ini dapat menyertakan blok konten `redacted`, `{"type": "redacted"}`: sebuah placeholder untuk konten yang ditahan oleh kebijakan model Anthropic. Blok ini tidak membawa field lain. Blok redacted hanya muncul dalam konten yang dikeluarkan platform; event pengguna yang menyertakannya akan ditolak dengan error 400.
  </Tab>

  <Tab title="Event sesi">
    | Tipe                                | Deskripsi                                                                                                                                                                                                                                                                                                                           |
    | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `session.status_running`            | Agen sedang aktif memproses.                                                                                                                                                                                                                                                                                                        |
    | `session.status_idle`               | Agen telah menyelesaikan tugasnya saat ini dan sedang menunggu input. Menyertakan `stop_reason` yang menunjukkan mengapa agen berhenti.                                                                                                                                                                                             |
    | `session.status_rescheduled`        | Terjadi error sementara dan sesi sedang mencoba ulang secara otomatis.                                                                                                                                                                                                                                                              |
    | `session.status_terminated`         | Sesi berakhir, baik karena error yang tidak dapat dipulihkan maupun karena sesi diarsipkan.                                                                                                                                                                                                                                         |
    | `session.deleted`                   | Sesi telah dihapus. Mengakhiri aliran event yang aktif; tidak ada event lebih lanjut yang dipancarkan untuk sesi ini.                                                                                                                                                                                                               |
    | `session.updated`                   | Permintaan pembaruan sesi mengubah setidaknya satu field. Hanya menyertakan field yang berubah. Pembaruan berlaku pada giliran berikutnya.                                                                                                                                                                                          |
    | `session.error`                     | Terjadi error selama pemrosesan. Menyertakan objek `error` bertipe dengan `retry_status`.                                                                                                                                                                                                                                           |
    | `session.usage`                     | Snapshot penggunaan kumulatif sesi dan biaya daftar yang dilacak. Membawa total penggunaan sesi dan salinan [anggaran](https://platform.claude.com/docs/id/managed-agents/budgets) sesi, atau `null` jika sesi tidak memilikinya.                                                                                                   |
    | `session.thread_created`            | Sebuah thread [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) telah dibuat. Event ini menyertakan `workflow_run_id`: ID eksekusi untuk thread milik [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs#a-runs-threads), dan `null` untuk thread lainnya. |
    | `session.thread_status_running`     | Sebuah thread sesi mulai dieksekusi. Setiap sesi memancarkan ini untuk thread utamanya; dalam sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), transisi thread anak juga diposting silang ke aliran utama.                                                                            |
    | `session.thread_status_idle`        | Sebuah thread sesi telah menyelesaikan gilirannya dan sedang menunggu input. Menyertakan `stop_reason`.                                                                                                                                                                                                                             |
    | `session.thread_status_rescheduled` | Sebuah thread sesi mengalami error sementara dan sedang mencoba ulang secara otomatis.                                                                                                                                                                                                                                              |
    | `session.thread_status_terminated`  | Sebuah thread sesi berakhir dan tidak menerima input lebih lanjut, misalnya karena diarsipkan atau mengalami error yang tidak dapat dipulihkan. Thread advisor juga berakhir ketika konsultasinya selesai. Server mengarsipkan sendiri thread milik eksekusi workflow.                                                              |

    Dalam sesi yang agennya mengaktifkan [alur kerja dinamis](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#dynamic-workflows), event `workflow_run.*` berikut tiba di aliran sesi:

    | Tipe                          | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                   |
    | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `workflow_run.created`        | Sebuah eksekusi workflow telah dibuat. Menyertakan `workflow_run_id`, `name` dan `description` eksekusi, serta `phases`, yaitu fase-fase yang dideklarasikan untuk eksekusi tersebut. Event status menyusul, meskipun setelah interupsi mungkin tidak.                                                                                                                                                      |
    | `workflow_run.status_running` | Sebuah eksekusi workflow sedang berjalan. Dikirim ketika eksekusi mulai dijalankan, yang bisa terjadi beberapa saat setelah `workflow_run.created`, dan lagi ketika eksekusi dilanjutkan setelah jeda karena anggaran. Pelanjutan setelah interupsi mungkin tidak mengirimkannya. Eksekusi yang idle sejak awal mungkin menerima `workflow_run.status_idle` terlebih dahulu. Menyertakan `workflow_run_id`. |
    | `workflow_run.status_idle`    | Sebuah eksekusi workflow menjadi idle: eksekusi dijeda, misalnya karena mencapai anggaran sesi. Jeda setelah interupsi mungkin tidak mengirimkannya. Menyertakan `workflow_run_id`.                                                                                                                                                                                                                         |
    | `workflow_run.status_ended`   | Sebuah eksekusi workflow berakhir. Menyertakan `workflow_run_id` dan `result`, yang `type`-nya menyatakan bagaimana eksekusi berakhir.                                                                                                                                                                                                                                                                      |
    | `workflow_run.error`          | Error dari sebuah eksekusi workflow, atau permulaan yang ditolak oleh server. Eksekusi yang berakhir dengan error menerimanya, dengan error yang sama, sebelum `workflow_run.status_ended`-nya. Menyertakan `error` dan `workflow_run_id`, yang bernilai `null` ketika tidak ada eksekusi yang dibuat.                                                                                                      |
    | `workflow_run.phase_started`  | Sebuah eksekusi workflow memasuki salah satu fasenya. Menyertakan `workflow_run_id` dan `workflow_run_phase_id`.                                                                                                                                                                                                                                                                                            |
    | `workflow_run.phase_ended`    | Sebuah eksekusi workflow meninggalkan sebuah fase. Menyertakan `workflow_run_id`, `workflow_run_phase_id`, dan `phase_started_id`.                                                                                                                                                                                                                                                                          |
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
    | Tipe             | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                       |
    | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `system.message` | Menambahkan konteks tingkat sistem yang memiliki hak istimewa, yang berlaku untuk giliran yang menyertainya dan semua giliran berikutnya. Untuk model yang menerimanya, lihat [Model yang didukung](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#supported-models). Pada model utama yang tidak didukung, event ini ditolak dengan `model_does_not_support_mid_conversation_system`. |
  </Tab>

  <Tab title="Event deltas">
    Event delta adalah event pratinjau khusus stream. Event ini dikeluarkan pada koneksi stream (tingkat sesi atau per thread) yang memilih ikut serta dengan parameter `event_deltas[]`, dan tidak pernah dipersistenkan ke riwayat event sesi. Lihat [Pratinjau respons dengan event delta](https://platform.claude.com/docs/id/managed-agents/event-deltas) untuk cara ikut serta, mengakumulasi, dan merekonsiliasinya.

    | Tipe          | Deskripsi                                                                                                                                                   |
    | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `event_start` | Sebuah event yang dipratinjau telah mulai dihasilkan. Membawa `type` dan `id` dari event yang akan datang. Hanya di stream dan tidak pernah dipersistenkan. |
    | `event_delta` | Konten inkremental untuk event yang dipratinjau, diidentifikasi oleh `event_id`. Hanya di stream dan tidak pernah dipersistenkan.                           |
  </Tab>
</Tabs>

## Worker self-hosted

Lihat [Referensi worker self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference) untuk flag CLI `ant beta:worker`, variabel lingkungan, path sistem file, dan opsi helper SDK dari worker bawaan yang menggerakkan environment `self_hosted`.

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
