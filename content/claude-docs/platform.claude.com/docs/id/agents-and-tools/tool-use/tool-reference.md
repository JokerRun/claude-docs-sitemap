---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: e55f27815187060ca88bec4ffc8b8665da794a03c0073104c8926b6c2e884514
---

# Referensi alat

Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.

---

Halaman ini adalah referensi untuk alat yang disediakan Anthropic dan properti opsional yang dapat Anda atur pada definisi alat apa pun. Untuk pengantar konseptual tentang penggunaan alat, lihat [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview). Untuk panduan mengimplementasikan penggunaan alat dalam aplikasi Anda, lihat [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools).

## Alat yang disediakan Anthropic \{#anthropic-provided-tools}

Anthropic menyediakan dua jenis alat: **server tools** (alat server) yang dieksekusi pada infrastruktur Anthropic, dan **client tools** (alat klien) di mana Anthropic mendefinisikan skemanya tetapi aplikasi Anda yang menangani eksekusinya. Kedua jenis ini muncul dalam array `tools` pada permintaan Anda bersama dengan alat yang didefinisikan pengguna.

| Alat                                                                          | `type`                                                                 | Eksekusi  | Status                                                        |
| ----------------------------------------------------------------------------- | ---------------------------------------------------------------------- | --------- | ------------------------------------------------------------- |
| [Alat pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool)      | `web_search_20260209`<br/>`web_search_20250305`                        | Server    | GA                                                            |
| [Alat pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool)     | `web_fetch_20260209`<br/>`web_fetch_20250910`                          | Server    | GA                                                            |
| [Alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool)  | `code_execution_20260120`<br/>`code_execution_20250825`                | Server    | GA                                                            |
| [Alat advisor](/docs/id/agents-and-tools/tool-use/advisor-tool)               | `advisor_20260301`                                                     | Server    | Beta: `advisor-tool-2026-03-01`                               |
| [Alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool)    | `tool_search_tool_regex_20251119`<br/>`tool_search_tool_bm25_20251119` | Server    | GA                                                            |
| [Konektor MCP](/docs/id/agents-and-tools/mcp-connector)                       | `mcp_toolset`                                                          | Server    | Beta: `mcp-client-2025-11-20`                                 |
| [Alat memori](/docs/id/agents-and-tools/tool-use/memory-tool)                 | `memory_20250818`                                                      | Klien     | GA                                                            |
| [Alat Bash](/docs/id/agents-and-tools/tool-use/bash-tool)                     | `bash_20250124`                                                        | Klien     | GA                                                            |
| [Alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool)       | `text_editor_20250728`<br/>`text_editor_20250124`                      | Klien     | GA                                                            |
| [Alat penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) | `computer_20251124`<br/>`computer_20250124`                            | Klien     | Beta: `computer-use-2025-11-24`<br/>`computer-use-2025-01-24` |

Untuk kompatibilitas model, lihat halaman masing-masing alat. Model yang didukung bervariasi berdasarkan alat dan versi alat.

<Note>
  Nilai `type` untuk pencarian alat juga menerima alias tanpa tanggal:
  `tool_search_tool_regex` dan `tool_search_tool_bm25`. Alias ini akan
  diarahkan ke versi bertanggal terbaru.
</Note>

### Versi alat \{#tool-versioning}

Sebagian besar alat yang disediakan Anthropic memiliki akhiran `_YYYYMMDD` dalam string `type`. Versi baru dirilis ketika perilaku, skema, atau dukungan model alat berubah. Versi lama tetap tersedia agar integrasi yang sudah ada tetap berfungsi.

Ketika sebuah alat memiliki beberapa versi aktif, hubungan di antara versi-versi tersebut bervariasi:

- **Berdasarkan kapabilitas:** `web_search_20260209` dan `web_fetch_20260209` menambahkan pemfilteran konten dinamis dibandingkan pendahulunya. `code_execution_20260120` menambahkan [pemanggilan alat secara terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) dari dalam sandbox. Dalam setiap kasus, baik versi baru maupun lama sama-sama terkini; versi mana yang Anda gunakan bergantung pada apakah Anda membutuhkan kapabilitas baru tersebut.
- **Berdasarkan model:** `text_editor_20250728` ditujukan untuk model Claude 4 dan `text_editor_20250124` untuk model yang lebih lama. Versi yang Anda gunakan bergantung pada model yang Anda targetkan.
- **Varian, bukan versi:** `tool_search_tool_regex_20251119` dan `tool_search_tool_bm25_20251119` adalah dua algoritma pencarian yang dirilis bersamaan. Tidak ada yang menggantikan yang lain.
- **Legacy:** `code_execution_20250522` hanya mendukung Python. `code_execution_20250825` menambahkan Bash dan operasi file.

Tipe `mcp_toolset` tidak diversikan berdasarkan tanggal; penentuan versi dilakukan melalui header `anthropic-beta`.

## Properti definisi alat \{#tool-definition-properties}

Setiap alat dalam array `tools`, termasuk alat yang didefinisikan pengguna, menerima properti opsional yang mengontrol bagaimana alat dimuat, siapa yang dapat memanggilnya, dan bagaimana inputnya divalidasi. Properti-properti ini dapat dikombinasikan: Anda dapat mengatur `defer_loading`, `cache_control`, dan `strict` pada alat yang sama.

| Properti                | Tujuan                                                                                                                | Tersedia pada                                                                                                              | Panduan terperinci                                                                                                  |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `cache_control`         | Menetapkan breakpoint cache prompt pada definisi alat ini                                                            | Semua alat                                                                                                                 | [Caching prompt](/docs/id/build-with-claude/prompt-caching)                                                        |
| `strict`                | Menjamin validasi skema pada nama dan input alat                                                                     | Semua alat kecuali `mcp_toolset`                                                                                           | [Penggunaan alat strict](/docs/id/agents-and-tools/tool-use/strict-tool-use)                                       |
| `defer_loading`         | Mengecualikan alat dari prompt sistem awal; memuatnya sesuai permintaan ketika pencarian alat mengembalikan `tool_reference` untuknya | Semua alat (untuk `mcp_toolset`, lihat [konfigurasi alat](/docs/id/agents-and-tools/mcp-connector#mcp-toolset-configuration)) | [Alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool)                                         |
| `allowed_callers`       | Membatasi pemanggil mana yang dapat memanggil alat                                                                   | Semua alat kecuali `mcp_toolset`                                                                                           | [Pemanggilan alat secara terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#the-allowed-callers-field) |
| `input_examples`        | Menyediakan contoh objek input untuk membantu Claude memahami cara memanggil alat                                    | Alat yang didefinisikan pengguna dan alat klien dengan skema Anthropic. Tidak tersedia pada alat server.                  | [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples)                 |
| `eager_input_streaming` | Mengaktifkan streaming input fine-grained (`true`) atau mempertahankan streaming buffered standar (`false`) untuk alat ini | Hanya alat yang didefinisikan pengguna                                                                                     | [Streaming alat fine-grained](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming)                      |

### Nilai `allowed_callers` \{#allowed-callers-values}

`allowed_callers` adalah array yang menerima kombinasi apa pun dari:

| Nilai                       | Arti                                                                                                              |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `"direct"`                  | Model dapat memanggil alat ini secara langsung dalam blok `tool_use`. Ini adalah default jika `allowed_callers` dihilangkan. |
| `"code_execution_20260120"` | Kode yang berjalan di dalam sandbox `code_execution_20260120` dapat memanggil alat ini.                          |

Menghilangkan `"direct"` dari array (misalnya, `"allowed_callers": ["code_execution_20260120"]`) mengarahkan Claude untuk memanggil alat hanya dari dalam eksekusi kode. Blok `tool_use` pada respons menyertakan field `caller` yang mengidentifikasi pemanggil mana yang memanggil alat tersebut. Lihat [Pemanggilan alat secara terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#the-allowed-callers-field) untuk penjelasan lengkap, termasuk bentuk respons `caller` dan perilaku error.

### `defer_loading` dan caching prompt \{#defer-loading-and-prompt-caching}

Alat dengan `defer_loading: true` dihapus dari bagian alat yang dirender sebelum kunci cache dihitung. Alat tersebut tidak muncul sama sekali dalam prefiks prompt sistem. Ketika pencarian alat menemukan alat yang ditangguhkan dan mengembalikan `tool_reference` untuknya, definisi lengkap alat tersebut diperluas secara inline pada titik tersebut dalam badan percakapan, bukan dalam prefiks.

Ini berarti `defer_loading: true` mempertahankan cache prompt Anda. Anda dapat menambahkan alat yang ditangguhkan ke permintaan tanpa membatalkan entri cache yang sudah ada, dan cache tetap valid di seluruh giliran saat alat ditemukan dan giliran saat alat dipanggil.

Untuk cara menggabungkan `defer_loading` dengan breakpoint `cache_control`, lihat [panduan caching prompt alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool#prompt-caching).