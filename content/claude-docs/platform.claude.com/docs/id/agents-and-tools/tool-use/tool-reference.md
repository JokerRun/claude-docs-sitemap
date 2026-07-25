---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: 3754aa74ee8e655c95a56952077ee4543093f88516e846a3ae68684e8b866e76
---

# Referensi alat

Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.

---

Halaman ini adalah referensi untuk alat-alat yang disediakan Anthropic dan properti opsional yang dapat Anda tetapkan pada definisi alat apa pun. Untuk pengenalan konseptual tentang penggunaan alat, lihat [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview). Untuk panduan tentang mengimplementasikan penggunaan alat dalam aplikasi Anda, lihat [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools).

## Alat yang disediakan Anthropic

Anthropic menyediakan dua jenis alat: **server tools** (alat server) yang dieksekusi pada infrastruktur Anthropic, dan **client tools** (alat klien) di mana Anthropic mendefinisikan skemanya tetapi aplikasi Anda yang menangani eksekusinya. Kedua jenis ini muncul dalam array `tools` pada permintaan Anda bersama dengan alat yang didefinisikan pengguna.

| Alat                                                                             | `type`                                                                              | Eksekusi | Status                                                    |
| -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------- | --------------------------------------------------------- |
| [Alat pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool)         | `web_search_20260318` `web_search_20260209` `web_search_20250305`                   | Server   | GA                                                        |
| [Alat pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool)        | `web_fetch_20260318` `web_fetch_20260309` `web_fetch_20260209` `web_fetch_20250910` | Server   | GA                                                        |
| [Alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool)     | `code_execution_20260521` `code_execution_20260120` `code_execution_20250825`       | Server   | GA                                                        |
| [Alat advisor](/docs/id/agents-and-tools/tool-use/advisor-tool)                  | `advisor_20260301`                                                                  | Server   | Beta: `advisor-tool-2026-03-01`                           |
| [Alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool)       | `tool_search_tool_regex_20251119` `tool_search_tool_bm25_20251119`                  | Server   | GA                                                        |
| [Konektor MCP](/docs/id/agents-and-tools/mcp-connector)                          | `mcp_toolset`                                                                       | Server   | Beta: `mcp-client-2025-11-20`                             |
| [Alat memori](/docs/id/agents-and-tools/tool-use/memory-tool)                    | `memory_20250818`                                                                   | Klien    | GA                                                        |
| [Alat bash](/docs/id/agents-and-tools/tool-use/bash-tool)                        | `bash_20250124`                                                                     | Klien    | GA                                                        |
| [Alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool)          | `text_editor_20250728` `text_editor_20250124`                                       | Klien    | GA                                                        |
| [Alat penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) | `computer_20251124` `computer_20250124`                                             | Klien    | Beta: `computer-use-2025-11-24` `computer-use-2025-01-24` |

Untuk kompatibilitas model, lihat halaman masing-masing alat. Model yang didukung bervariasi menurut alat dan versi alat.

<Note>
  Nilai `type` untuk pencarian alat juga menerima alias tanpa tanggal: `tool_search_tool_regex` dan `tool_search_tool_bm25`. Alias ini mengarah ke versi bertanggal terbaru.
</Note>

### Pemversian alat

Sebagian besar alat yang disediakan Anthropic memiliki akhiran `_YYYYMMDD` dalam string `type`. Versi baru dirilis ketika perilaku, skema, atau dukungan model alat berubah. Versi yang lebih lama tetap tersedia sehingga integrasi yang sudah ada terus berfungsi.

Ketika sebuah alat memiliki beberapa versi aktif, hubungan di antara versi-versi tersebut bervariasi:

* **Berbasis kemampuan:** `web_search_20260209` dan `web_fetch_20260209` menambahkan pemfilteran konten dinamis dibandingkan pendahulunya; `web_fetch_20260309` menambahkan opsi pelewatan cache; `web_search_20260318` dan `web_fetch_20260318` menambahkan kontrol penyertaan respons. `code_execution_20260120` menambahkan [pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) dari dalam sandbox; `code_execution_20260521` mengungkapkan batas waktu per sel dalam deskripsi alat. Dalam setiap kasus, baik versi baru maupun lama sama-sama terkini; versi mana yang Anda gunakan bergantung pada apakah Anda memerlukan kemampuan baru tersebut.
* **Berbasis model:** `text_editor_20250728` untuk model Claude 4 dan yang lebih baru, dan `text_editor_20250124` untuk model yang lebih lama. Versi yang Anda gunakan bergantung pada model yang Anda targetkan.
* **Varian, bukan versi:** `tool_search_tool_regex_20251119` dan `tool_search_tool_bm25_20251119` adalah dua algoritma pencarian yang dirilis bersamaan. Tidak ada yang menggantikan yang lain.
* **Warisan:** `code_execution_20250522` hanya mendukung Python. `code_execution_20250825` menambahkan Bash dan operasi file.

Tipe `mcp_toolset` tidak diversikan berdasarkan tanggal; pemversian dilakukan melalui header `anthropic-beta`.

## Properti definisi alat

Setiap alat dalam array `tools`, termasuk alat yang didefinisikan pengguna, menerima properti opsional yang mengontrol bagaimana alat dimuat, siapa yang dapat memanggilnya, dan bagaimana inputnya divalidasi. Properti-properti ini dapat dikombinasikan: Anda dapat menetapkan `defer_loading` dan `cache_control` dan `strict` pada alat yang sama.

| Properti                | Tujuan                                                                                                                                | Tersedia pada                                                                                                                 | Panduan terperinci                                                                                                    |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `cache_control`         | Menetapkan breakpoint cache prompt pada definisi alat ini                                                                             | Semua alat                                                                                                                    | [Caching prompt](/docs/id/build-with-claude/prompt-caching)                                                           |
| `strict`                | Menjamin validasi skema pada nama dan input alat                                                                                      | Semua alat kecuali `mcp_toolset`                                                                                              | [Penggunaan alat ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use)                                           |
| `defer_loading`         | Mengecualikan alat dari prompt sistem awal; memuatnya sesuai permintaan ketika pencarian alat mengembalikan `tool_reference` untuknya | Semua alat (untuk `mcp_toolset`, lihat [konfigurasi alat](/docs/id/agents-and-tools/mcp-connector#mcp-toolset-configuration)) | [Alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool)                                            |
| `allowed_callers`       | Membatasi pemanggil mana yang dapat memanggil alat                                                                                    | Semua alat kecuali `mcp_toolset`                                                                                              | [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#the-allowed-callers-field) |
| `input_examples`        | Menyediakan contoh objek input untuk membantu Claude memahami cara memanggil alat                                                     | Alat yang didefinisikan pengguna dan alat klien berskema Anthropic. Tidak tersedia pada alat server.                          | [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples)                    |
| `eager_input_streaming` | Mengaktifkan streaming input berbutir halus (`true`) atau mempertahankan streaming buffer standar (`false`) untuk alat ini            | Hanya alat yang didefinisikan pengguna                                                                                        | [Streaming alat berbutir halus](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming)                       |

### Nilai `allowed_callers`

`allowed_callers` adalah array yang menerima kombinasi apa pun dari:

| Nilai                       | Arti                                                                                                                         |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `"direct"`                  | Model dapat memanggil alat ini secara langsung dalam blok `tool_use`. Ini adalah default jika `allowed_callers` dihilangkan. |
| `"code_execution_20260120"` | Kode yang berjalan di dalam sandbox `code_execution_20260120` atau yang lebih baru dapat memanggil alat ini.                 |

Baik `"code_execution_20260120"` maupun `"code_execution_20260521"` diterima dalam `allowed_callers` dan dapat dipertukarkan: permintaan yang menggunakan salah satu versi alat eksekusi kode memenuhi alat yang mencantumkan salah satu pemanggil tersebut. Blok respons selalu menandai pemanggil sebagai `code_execution_20260120` terlepas dari versi mana yang dideklarasikan oleh permintaan.

Menghilangkan `"direct"` dari array (misalnya, `"allowed_callers": ["code_execution_20260120"]`) mengarahkan Claude untuk memanggil alat hanya dari dalam eksekusi kode. Blok `tool_use` pada respons menyertakan bidang `caller` yang mengidentifikasi pemanggil mana yang memanggil alat tersebut. Lihat [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#the-allowed-callers-field) untuk pembahasan lengkap, termasuk bentuk respons `caller` dan perilaku kesalahan.

### `defer_loading` dan caching prompt

Alat dengan `defer_loading: true` dihapus dari bagian alat yang dirender sebelum kunci cache dihitung. Alat tersebut sama sekali tidak muncul dalam prefiks prompt sistem. Ketika pencarian alat menemukan alat yang ditangguhkan dan mengembalikan `tool_reference` untuknya, definisi lengkap alat tersebut diperluas secara inline pada titik tersebut dalam badan percakapan, bukan dalam prefiks.

Ini berarti `defer_loading: true` mempertahankan cache prompt Anda. Anda dapat menambahkan alat yang ditangguhkan ke permintaan tanpa membatalkan entri cache yang sudah ada, dan cache tetap valid di sepanjang giliran di mana alat ditemukan dan giliran di mana alat tersebut dipanggil.

Untuk cara menggabungkan `defer_loading` dengan breakpoint `cache_control`, lihat [panduan caching prompt alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool#prompt-caching).
