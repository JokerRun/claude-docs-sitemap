---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 38657654bdadab969130282b732180ab41de034b7ddef84608bd1ab4b36c7f0d
---

# Referensi alat

Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.

---

Halaman ini adalah referensi untuk alat yang disediakan Anthropic dan properti opsional yang dapat Anda atur pada definisi alat apa pun. Untuk pengenalan konseptual tentang penggunaan alat, lihat [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview). Untuk panduan tentang mengimplementasikan penggunaan alat di aplikasi Anda, lihat [Tentukan alat](/docs/id/agents-and-tools/tool-use/define-tools).

## Alat yang disediakan Anthropic

Anthropic menyediakan dua jenis alat: **alat server** yang dijalankan pada infrastruktur Anthropic, dan **alat klien** di mana Anthropic mendefinisikan skema tetapi aplikasi Anda menangani eksekusi. Kedua jenis muncul dalam array `tools` permintaan Anda bersama dengan alat yang ditentukan pengguna.

| Alat                                                                          | `type`                                                                 | Eksekusi | Status                                                        |
| ----------------------------------------------------------------------------- | ---------------------------------------------------------------------- | --------- | ------------------------------------------------------------- |
| [Alat pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool)         | `web_search_20260209`<br/>`web_search_20250305`                        | Server    | GA                                                            |
| [Alat pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool)           | `web_fetch_20260209`<br/>`web_fetch_20250910`                          | Server    | GA                                                            |
| [Alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) | `code_execution_20260120`<br/>`code_execution_20250825`                | Server    | GA                                                            |
| [Alat Advisor](/docs/id/agents-and-tools/tool-use/advisor-tool)               | `advisor_20260301`                                                     | Server    | Beta: `advisor-tool-2026-03-01`                               |
| [Alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool)       | `tool_search_tool_regex_20251119`<br/>`tool_search_tool_bm25_20251119` | Server    | GA                                                            |
| [Konektor MCP](/docs/id/agents-and-tools/mcp-connector)                      | `mcp_toolset`                                                          | Server    | Beta: `mcp-client-2025-11-20`                                 |
| [Alat Memori](/docs/id/agents-and-tools/tool-use/memory-tool)                 | `memory_20250818`                                                      | Client    | GA                                                            |
| [Alat Bash](/docs/id/agents-and-tools/tool-use/bash-tool)                     | `bash_20250124`                                                        | Client    | GA                                                            |
| [Alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool)       | `text_editor_20250728`<br/>`text_editor_20250124`                      | Client    | GA                                                            |
| [Alat penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool)     | `computer_20251124`<br/>`computer_20250124`                            | Client    | Beta: `computer-use-2025-11-24`<br/>`computer-use-2025-01-24` |

Untuk kompatibilitas model, lihat halaman setiap alat. Model yang didukung bervariasi menurut alat dan versi alat.

<Note>
  Nilai `type` pencarian alat juga menerima alias tanpa tanggal:
  `tool_search_tool_regex` dan `tool_search_tool_bm25`. Ini menyelesaikan ke
  versi tertanggal terbaru.
</Note>

### Versioning alat

Sebagian besar alat yang disediakan Anthropic memiliki akhiran `_YYYYMMDD` dalam string `type`. Versi baru dirilis ketika perilaku alat, skema, atau dukungan model berubah. Versi yang lebih lama tetap tersedia sehingga integrasi yang ada terus berfungsi.

Ketika alat memiliki beberapa versi aktif, hubungan di antara mereka bervariasi:

- **Capability-keyed:** `web_search_20260209` dan `web_fetch_20260209` menambahkan penyaringan konten dinamis dibandingkan pendahulu mereka. `code_execution_20260120` menambahkan [pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) dari dalam sandbox. Dalam setiap kasus, versi baru dan lama adalah versi terkini; versi mana yang Anda gunakan tergantung pada apakah Anda memerlukan kemampuan baru.
- **Model-keyed:** `text_editor_20250728` untuk model Claude 4 dan `text_editor_20250124` untuk model sebelumnya. Versi yang Anda gunakan tergantung pada model yang Anda targetkan.
- **Varian, bukan versi:** `tool_search_tool_regex_20251119` dan `tool_search_tool_bm25_20251119` adalah dua algoritma pencarian yang dirilis bersama. Tidak ada yang menggantikan yang lain.
- **Legacy:** `code_execution_20250522` hanya mendukung Python. `code_execution_20250825` menambahkan Bash dan operasi file.

Tipe `mcp_toolset` tidak memiliki versi bertanggal; versioning dibawa dalam header `anthropic-beta` sebagai gantinya.

## Properti definisi alat

Setiap alat dalam array `tools`, termasuk alat yang ditentukan pengguna, menerima properti opsional yang mengontrol cara alat dimuat, siapa yang dapat memanggilnya, dan bagaimana inputnya divalidasi. Properti ini dapat digabungkan: Anda dapat mengatur `defer_loading` dan `cache_control` dan `strict` pada alat yang sama.

| Properti                | Tujuan                                                                                                               | Tersedia di                                                                                                               | Panduan terperinci                                                                                                      |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `cache_control`         | Atur titik breakpoint cache prompt pada definisi alat ini                                                                 | Semua alat                                                                                                                  | [Prompt caching](/docs/id/build-with-claude/prompt-caching)                                                         |
| `strict`                | Jamin validasi skema pada nama dan input alat                                                                  | Semua alat kecuali `mcp_toolset`                                                                                             | [Penggunaan alat ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use)                                               |
| `defer_loading`         | Kecualikan alat dari prompt sistem awal; muat sesuai permintaan ketika pencarian alat mengembalikan `tool_reference` untuknya | Semua alat (untuk `mcp_toolset`, lihat [konfigurasi alat](/docs/id/agents-and-tools/mcp-connector#mcp-toolset-configuration)) | [Alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool)                                             |
| `allowed_callers`       | Batasi pemanggil mana yang dapat memanggil alat                                                                              | Semua alat kecuali `mcp_toolset`                                                                                             | [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#the-allowed-callers-field) |
| `input_examples`        | Berikan contoh objek input untuk membantu Claude memahami cara memanggil alat                                          | Alat yang ditentukan pengguna dan alat klien skema Anthropic. Tidak tersedia pada alat server.                                             | [Tentukan alat](/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples)                         |
| `eager_input_streaming` | Aktifkan streaming input berbutir halus (`true`) atau pertahankan streaming buffered standar (`false`) untuk alat ini              | Alat yang ditentukan pengguna saja                                                                                                    | [Streaming alat berbutir halus](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming)                       |

### Nilai `allowed_callers`

`allowed_callers` adalah array yang menerima kombinasi apa pun dari:

| Nilai                       | Arti                                                                                                           |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `"direct"`                  | Model dapat memanggil alat ini secara langsung dalam blok `tool_use`. Ini adalah default jika `allowed_callers` dihilangkan. |
| `"code_execution_20260120"` | Kode yang berjalan di dalam sandbox `code_execution_20260120` dapat memanggil alat ini.                                       |

Menghilangkan `"direct"` dari array (misalnya, `"allowed_callers": ["code_execution_20260120"]`) berarti alat hanya dapat dipanggil dari dalam eksekusi kode. Blok `tool_use` respons menyertakan bidang `caller` yang mengidentifikasi pemanggil mana yang memanggil alat. Lihat [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#the-allowed-callers-field) untuk perlakuan lengkap, termasuk bentuk respons `caller` dan perilaku kesalahan.

### `defer_loading` dan prompt caching

Alat dengan `defer_loading: true` dilepas dari bagian alat yang dirender sebelum kunci cache dihitung. Mereka tidak muncul dalam awalan prompt sistem sama sekali. Ketika pencarian alat menemukan alat yang ditunda dan mengembalikan `tool_reference` untuknya, definisi lengkap alat diperluas inline pada titik itu dalam badan percakapan, bukan dalam awalan.

Ini berarti `defer_loading: true` melestarikan cache prompt Anda. Anda dapat menambahkan alat yang ditunda ke permintaan tanpa membatalkan entri cache yang ada, dan cache tetap valid di seluruh giliran di mana alat ditemukan dan giliran di mana alat dipanggil.

Untuk cara menggabungkan `defer_loading` dengan breakpoint `cache_control`, lihat [panduan prompt caching Alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool#prompt-caching).