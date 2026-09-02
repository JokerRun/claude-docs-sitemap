---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 34dd4472a9e87d3974dc7473ac22f4064453ca2994f8735ea93ed554501604e5
---

---
title: Referensi alat
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference
description: Direktori alat server, alat klien, dan toolset klien yang disediakan Anthropic, beserta referensi untuk properti definisi alat opsional.
---

Halaman ini adalah referensi untuk alat-alat yang disediakan Anthropic dan properti opsional yang dapat Anda atur pada definisi alat apa pun. Untuk pengantar konseptual tentang "tool use" (penggunaan alat), lihat [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview). Untuk panduan mengimplementasikan penggunaan alat dalam aplikasi Anda, lihat [Mendefinisikan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools).

## Alat yang disediakan Anthropic

Anthropic menyediakan dua jenis alat: **alat server** yang dieksekusi di infrastruktur Anthropic, dan **alat klien** di mana Anthropic mendefinisikan skemanya tetapi aplikasi Anda yang menangani eksekusinya. Kedua jenis ini muncul dalam array `tools` pada permintaan Anda bersama alat-alat yang didefinisikan pengguna.

| Alat                                                                                                        | `type`                                                                              | Eksekusi | [Header beta](https://platform.claude.com/docs/id/api/beta-headers) |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------- |
| [Alat pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool)         | `web_search_20260318` `web_search_20260209` `web_search_20250305`                   | Server   | Tidak ada                                                           |
| [Alat pengambilan web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool)        | `web_fetch_20260318` `web_fetch_20260309` `web_fetch_20260209` `web_fetch_20250910` | Server   | Tidak ada                                                           |
| [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool)     | `code_execution_20260521` `code_execution_20260120` `code_execution_20250825`       | Server   | Tidak ada                                                           |
| [Alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool)                  | `advisor_20260301`                                                                  | Server   | `advisor-tool-2026-03-01`                                           |
| [Alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool)       | `tool_search_tool_regex_20251119` `tool_search_tool_bm25_20251119`                  | Server   | Tidak ada                                                           |
| [Konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector)                          | `mcp_toolset`                                                                       | Server   | `mcp-client-2025-11-20`                                             |
| [Alat memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool)                    | `memory_20250818`                                                                   | Klien    | Tidak ada                                                           |
| [Alat Bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool)                        | `bash_20250124`                                                                     | Klien    | Tidak ada                                                           |
| [Alat editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool)          | `text_editor_20250728` `text_editor_20250124`                                       | Klien    | Tidak ada                                                           |
| [Alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) | `computer_toolset_20260801` `computer_20251124` `computer_20250124`                 | Klien    | Tidak ada `computer-use-2025-11-24` `computer-use-2025-01-24`       |
| [Alat penggunaan browser](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool)   | `browser_toolset_20260801`                                                          | Klien    | Tidak ada                                                           |

Untuk kompatibilitas model, lihat halaman masing-masing alat. Model yang didukung bervariasi menurut alat dan versi alat.

<Note>
  Nilai `type` pencarian alat juga menerima alias tanpa tanggal: `tool_search_tool_regex` dan `tool_search_tool_bm25`. Alias ini mengarah ke versi bertanggal terbaru.
</Note>

### Pemversian alat

Sebagian besar alat yang disediakan Anthropic memiliki akhiran `_YYYYMMDD` dalam string `type`. Versi baru dirilis ketika perilaku, skema, atau dukungan model alat tersebut berubah. Versi lama tetap tersedia agar integrasi yang sudah ada terus berfungsi.

Ketika sebuah alat memiliki beberapa versi aktif, hubungan di antaranya bervariasi:

* **Berbasis kapabilitas:** `web_search_20260209` dan `web_fetch_20260209` menambahkan pemfilteran konten dinamis dibandingkan pendahulunya; `web_fetch_20260309` menambahkan opsi bypass cache; `web_search_20260318` dan `web_fetch_20260318` menambahkan kontrol penyertaan respons. `code_execution_20260120` menambahkan [pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) dari dalam sandbox; `code_execution_20260521` mengungkapkan batas waktu per sel dalam deskripsi alat. Dalam setiap kasus, baik versi baru maupun lama sama-sama terkini; versi mana yang Anda gunakan bergantung pada apakah Anda memerlukan kapabilitas baru tersebut.
* **Berbasis model:** `text_editor_20250728` ditujukan untuk model Claude 4 dan yang lebih baru, sedangkan `text_editor_20250124` untuk model yang lebih lama. Versi yang Anda gunakan bergantung pada model yang Anda targetkan.
* **Varian, bukan versi:** `tool_search_tool_regex_20251119` dan `tool_search_tool_bm25_20251119` adalah dua algoritma pencarian yang dirilis bersamaan. Tidak ada yang menggantikan yang lain.
* **Legacy:** `code_execution_20250522` hanya mendukung Python. `code_execution_20250825` menambahkan Bash dan operasi file.
* **Penerus:** `computer_toolset_20260801` adalah penerus stabil dari versi beta `computer_20251124` dan `computer_20250124`, yang tetap tersedia untuk integrasi yang sudah ada dan untuk model yang tidak mendukung toolset tersebut ([Versi alat sebelumnya](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#earlier-tool-versions)). `browser_toolset_20260801` adalah versi pertama dari alat penggunaan browser. Keduanya adalah [toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets).

Tipe `mcp_toolset` tidak diberi versi berdasarkan tanggal; pemversiannya dibawa dalam header `anthropic-beta`.

### Toolset klien

[Alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) dan [alat penggunaan browser](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) adalah toolset klien yang didefinisikan Anthropic: satu entri dalam `tools` mendeklarasikan sekumpulan alat anggota tetap yang nama, deskripsi, dan skema inputnya didefinisikan oleh Anthropic, dan aplikasi Anda mengeksekusi setiap panggilan. Entri ini tidak menerima `name`, karena `type` bertanggal sudah menetapkan nama-nama anggotanya. `configs`, `cache_control`, dan `allowed_callers` (yang hanya menerima `["direct"]`) bersifat opsional.

Toolset klien adalah alat Messages API. Saat ini toolset ini tidak tersedia sebagai alat agen di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/tools), yang menyediakan toolset agen bawaan, toolset MCP, dan alat kustomnya sendiri.

```json
{
  "type": "browser_toolset_20260801",
  "configs": {
    "javascript_exec": { "enabled": true }
  },
  "cache_control": { "type": "ephemeral" }
}
```

`configs` menyesuaikan anggota secara individual:

* Kuncinya adalah nama anggota, dan setiap nilai hanya menerima `enabled` dan `defer_loading`.
* Anggota yang Anda hilangkan mempertahankan nilai defaultnya. Nilai yang tidak ada, `{}`, dan default yang dinyatakan ulang adalah setara.
* Nama anggota yang tidak dikenal atau field lain apa pun dalam nilai anggota akan ditolak, demikian pula `configs` yang menonaktifkan setiap anggota (hilangkan entrinya saja).
* Anggota yang dinonaktifkan dihapus dari alat yang dilihat Claude. Jika Claude masih menyebutnya, kembalikan `tool_result` berisi error.

Atur `defer_loading` per anggota, jangan pernah pada entri, dan berikan nilai yang sama untuk setiap anggota yang diaktifkan: di bawah [pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#deferred-tool-loading), toolset dimuat dan diperluas sebagai satu definisi. Ketika setiap anggota yang diaktifkan ditangguhkan, hanya [alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool) yang tidak ditangguhkan sendiri yang dapat memunculkan toolset tersebut, jadi deklarasikan satu dalam permintaan yang sama. Jangan letakkan `cache_control` pada entri toolset yang anggotanya ditangguhkan; atur breakpoint pada alat yang tidak ditangguhkan, karena definisi yang ditangguhkan bukan bagian dari prefiks yang di-cache.

`cache_control` hanya diletakkan pada entri; untuk mengetahui di mana breakpoint berada, termasuk penanda di dalam aksi batch, lihat [Penggunaan alat dengan caching prompt](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching#cache-control-on-tool-definitions).

**Menangani panggilan alat anggota.** Claude memanggil anggota dengan blok `tool_use` yang `name`-nya adalah nama anggota dan `toolset_name`-nya adalah `computer` atau `browser`; `input` berisi parameter anggota tersebut dan tanpa field `action`. Lakukan dispatch berdasarkan pasangan `toolset_name` dan `name`, karena alat kustom mungkin memiliki nama yang sama dengan anggota dan kedua toolset berbagi nama seperti `screenshot`. Hanya hasil anggota yang menggemakan `toolset_name`. Beberapa panggilan anggota dalam satu giliran membentuk aksi batch yang Anda jalankan secara berurutan ([penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions), [penggunaan browser](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions)). Anggota baru hanya hadir bersama `type` bertanggal yang baru.

**Tidak didukung pada entri toolset.** API menolak masing-masing hal berikut dengan `invalid_request_error`:

* `strict: true` atau `input_examples`.
* `defer_loading` pada entri, atau anggota yang diaktifkan dengan nilai `defer_loading` yang berbeda (atur per anggota dalam `configs`, semuanya dengan nilai yang sama).
* Pemanggil eksekusi kode dalam `allowed_callers` (tidak ada [pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling)).
* Header beta legacy `fine-grained-tool-streaming-2025-05-14`. Saat Anda melakukan streaming, `input` setiap anggota tiba sebagai satu `input_json_delta` yang lengkap.
* `tool_choice` bertipe `tool` yang menyebut toolset atau anggota (gunakan `auto`, `any`, atau `none`).
* Dua entri dari toolset yang sama, atau alat lain yang membawa nama toolset tersebut: alat bernama `computer` bersama `computer_toolset_20260801`, atau alat bernama `browser` bersama `browser_toolset_20260801`. Kedua toolset dapat dideklarasikan bersama.

## Properti definisi alat

Setiap alat dalam array `tools`, termasuk alat yang didefinisikan pengguna, menerima properti opsional yang mengontrol bagaimana alat dimuat, siapa yang dapat memanggilnya, dan bagaimana inputnya divalidasi. Properti-properti ini dapat dikombinasikan: Anda dapat mengatur `defer_loading`, `cache_control`, dan `strict` pada alat yang sama.

| Properti                | Tujuan                                                                                                                                | Tersedia pada                                                                                                                                                                                                                                                                                                                                                                | Panduan terperinci                                                                                                                               |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cache_control`         | Mengatur breakpoint cache prompt pada definisi alat ini                                                                               | Semua alat (pada `computer_toolset_20260801` dan `browser_toolset_20260801`, atur pada entri toolset itu sendiri, bukan di dalam `configs` anggota)                                                                                                                                                                                                                          | [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)                                                           |
| `strict`                | Menjamin validasi skema pada nama dan input alat                                                                                      | Semua alat kecuali `mcp_toolset`, `computer_toolset_20260801`, dan `browser_toolset_20260801`                                                                                                                                                                                                                                                                                | [Penggunaan alat strict](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use)                                          |
| `defer_loading`         | Mengecualikan alat dari prompt sistem awal; memuatnya sesuai permintaan ketika pencarian alat mengembalikan `tool_reference` untuknya | Semua alat (untuk `mcp_toolset`, lihat [konfigurasi alat](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#mcp-toolset-configuration)). Pada toolset penggunaan komputer dan penggunaan browser, atur per anggota di dalam `configs`; lihat [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets). | [Alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool)                                            |
| `allowed_callers`       | Membatasi pemanggil mana yang dapat memanggil alat                                                                                    | Semua alat kecuali `mcp_toolset` (pada `computer_toolset_20260801` dan `browser_toolset_20260801`, hanya `["direct"]` yang diterima; lihat [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets))                                                                                                                    | [Pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#the-allowed-callers-field) |
| `input_examples`        | Menyediakan contoh objek input untuk membantu Claude memahami cara memanggil alat                                                     | Alat klien yang didefinisikan pengguna dan berskema Anthropic, kecuali `computer_toolset_20260801` dan `browser_toolset_20260801`. Tidak tersedia pada alat server.                                                                                                                                                                                                          | [Mendefinisikan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples)                    |
| `eager_input_streaming` | Mengaktifkan streaming input fine-grained (`true`) atau mempertahankan streaming buffer standar (`false`) untuk alat ini              | Hanya alat yang didefinisikan pengguna                                                                                                                                                                                                                                                                                                                                       | [Streaming alat fine-grained](https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming)                         |

### Nilai `allowed_callers`

`allowed_callers` adalah array yang menerima kombinasi apa pun dari:

| Nilai                       | Arti                                                                                                                         |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `"direct"`                  | Model dapat memanggil alat ini secara langsung dalam blok `tool_use`. Ini adalah default jika `allowed_callers` dihilangkan. |
| `"code_execution_20260120"` | Kode yang berjalan di dalam sandbox `code_execution_20260120` atau yang lebih baru dapat memanggil alat ini.                 |

Baik `"code_execution_20260120"` maupun `"code_execution_20260521"` diterima dalam `allowed_callers` dan dapat saling menggantikan: permintaan yang menggunakan salah satu versi alat eksekusi kode memenuhi alat yang mencantumkan salah satu pemanggil tersebut. Blok respons selalu menandai pemanggil sebagai `code_execution_20260120` terlepas dari versi mana yang dideklarasikan permintaan.

Menghilangkan `"direct"` dari array (misalnya, `"allowed_callers": ["code_execution_20260120"]`) mengarahkan Claude untuk memanggil alat hanya dari dalam eksekusi kode. Blok `tool_use` pada respons menyertakan field `caller` yang mengidentifikasi pemanggil mana yang memanggil alat tersebut. Lihat [Pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#the-allowed-callers-field) untuk pembahasan lengkap, termasuk bentuk respons `caller` dan perilaku error.

### `defer_loading` dan caching prompt

Alat dengan `defer_loading: true` dihapus dari bagian alat yang dirender sebelum kunci cache dihitung. Alat tersebut sama sekali tidak muncul dalam prefiks prompt sistem. Ketika pencarian alat menemukan alat yang ditangguhkan dan mengembalikan `tool_reference` untuknya, definisi lengkap alat tersebut diperluas secara inline pada titik itu dalam isi percakapan, bukan dalam prefiks.

Ini berarti `defer_loading: true` mempertahankan cache prompt Anda. Anda dapat menambahkan alat yang ditangguhkan ke permintaan tanpa membatalkan entri cache yang sudah ada, dan cache tetap valid sepanjang giliran saat alat ditemukan dan giliran saat alat dipanggil.

Untuk mempelajari cara menggabungkan `defer_loading` dengan breakpoint `cache_control`, lihat [panduan caching prompt alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#prompt-caching).
