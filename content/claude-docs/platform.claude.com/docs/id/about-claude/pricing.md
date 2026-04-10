---
source: platform
url: https://platform.claude.com/docs/id/about-claude/pricing
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 4dfcc579ddffc94790d73403508361f1ef214d770f6972a4cce2ef1e7e105e67
---

# Harga

Pelajari tentang struktur harga Anthropic untuk model dan fitur

---

Halaman ini menyediakan informasi harga terperinci untuk model dan fitur Anthropic. Semua harga dalam USD.

Untuk informasi harga terkini, silakan kunjungi [claude.com/pricing](https://claude.com/pricing).

## Harga model

Tabel berikut menunjukkan harga untuk semua model Claude di berbagai tingkat penggunaan:

| Model             | Base Input Tokens | 5m Cache Writes | 1h Cache Writes | Cache Hits & Refreshes | Output Tokens |
|-------------------|-------------------|-----------------|-----------------|----------------------|---------------|
| Claude Opus 4.6     | $5 / MTok         | $6.25 / MTok    | $10 / MTok      | $0.50 / MTok | $25 / MTok    |
| Claude Opus 4.5   | $5 / MTok         | $6.25 / MTok    | $10 / MTok      | $0.50 / MTok | $25 / MTok    |
| Claude Opus 4.1   | $15 / MTok        | $18.75 / MTok   | $30 / MTok      | $1.50 / MTok | $75 / MTok    |
| Claude Opus 4     | $15 / MTok        | $18.75 / MTok   | $30 / MTok      | $1.50 / MTok | $75 / MTok    |
| Claude Sonnet 4.6   | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Sonnet 4.5   | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Sonnet 4   | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)) | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Haiku 4.5  | $1 / MTok         | $1.25 / MTok    | $2 / MTok       | $0.10 / MTok | $5 / MTok     |
| Claude Haiku 3.5  | $0.80 / MTok      | $1 / MTok       | $1.6 / MTok     | $0.08 / MTok | $4 / MTok     |
| Claude Opus 3 ([deprecated](/docs/en/about-claude/model-deprecations))    | $15 / MTok        | $18.75 / MTok   | $30 / MTok      | $1.50 / MTok | $75 / MTok    |
| Claude Haiku 3    | $0.25 / MTok      | $0.30 / MTok    | $0.50 / MTok    | $0.03 / MTok | $1.25 / MTok  |

<Note>
MTok = Juta token. Kolom "Base Input Tokens" menunjukkan harga input standar, "Cache Writes" dan "Cache Hits" khusus untuk [prompt caching](#prompt-caching), dan "Output Tokens" menunjukkan harga output. Lihat [harga prompt caching](#prompt-caching) di bawah untuk penjelasan kolom cache dan pengali harga.
</Note>

## Harga platform pihak ketiga

Model Claude tersedia di [AWS Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Untuk harga resmi, kunjungi:
- [Harga AWS Bedrock](https://aws.amazon.com/bedrock/pricing/)
- [Harga Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [Harga Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/#pricing)

<Note>
**Harga endpoint regional dan multi-region untuk model Claude 4.5 dan seterusnya**

Mulai dengan Claude Sonnet 4.5 dan Haiku 4.5:
- **AWS Bedrock** menawarkan dua jenis endpoint: endpoint global (perutean dinamis untuk ketersediaan maksimum) dan endpoint regional (perutean data yang dijamin melalui wilayah geografis tertentu).
- **Google Vertex AI** menawarkan tiga jenis endpoint: endpoint global, endpoint multi-region (perutean dinamis dalam area geografis), dan endpoint regional.

Endpoint regional dan multi-region mencakup premi 10% di atas endpoint global. Claude API (1P) bersifat global secara default; untuk opsi residensi data 1P dan harga, lihat [Harga residensi data](#data-residency-pricing) di bawah.

**Cakupan:** Struktur harga ini berlaku untuk Claude Sonnet 4.5, Haiku 4.5, dan semua model di masa mendatang. Model sebelumnya (Claude Sonnet 4, Opus 4, dan rilis sebelumnya) mempertahankan harga yang ada.

Untuk detail implementasi dan contoh kode:
- [Endpoint global vs regional AWS Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock#global-vs-regional-endpoints)
- [Endpoint global, multi-region, dan regional Google Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai#global-multi-region-and-regional-endpoints)
</Note>

## Harga khusus fitur

### Prompt caching

Prompt caching mengurangi biaya dan latensi dengan menggunakan kembali bagian prompt yang telah diproses sebelumnya di seluruh panggilan API. Alih-alih memproses ulang system prompt besar, dokumen, atau riwayat percakapan yang sama pada setiap permintaan, API membaca dari cache dengan sebagian kecil dari harga input standar.

Ada dua cara untuk mengaktifkan prompt caching:

- **Caching otomatis:** Tambahkan satu field `cache_control` di tingkat atas permintaan Anda. Sistem secara otomatis mengelola breakpoint cache seiring percakapan berkembang. Ini adalah titik awal yang direkomendasikan untuk sebagian besar kasus penggunaan.
- **Breakpoint cache eksplisit:** Tempatkan `cache_control` langsung pada blok konten individual untuk kontrol terperinci atas apa yang di-cache.

Prompt caching menggunakan pengali harga berikut relatif terhadap tarif token input dasar:

| Operasi cache | Pengali | Durasi |
|:----------------|:-----------|:---------|
| Penulisan cache 5 menit | 1,25x harga input dasar | Cache berlaku selama 5 menit |
| Penulisan cache 1 jam | 2x harga input dasar | Cache berlaku selama 1 jam |
| Pembacaan cache (hit) | 0,1x harga input dasar | Durasi sama dengan penulisan sebelumnya |

Token penulisan cache dikenakan biaya saat konten pertama kali disimpan. Token pembacaan cache dikenakan biaya saat permintaan berikutnya mengambil konten yang di-cache. Cache hit dikenakan biaya 10% dari harga input standar, yang berarti caching terbayar setelah hanya satu pembacaan cache untuk durasi 5 menit (penulisan 1,25x), atau setelah dua pembacaan cache untuk durasi 1 jam (penulisan 2x).

Pengali ini bertumpuk dengan pengubah harga lainnya, termasuk diskon Batch API dan residensi data.

Untuk detail implementasi, model yang didukung, dan contoh kode, lihat [dokumentasi prompt caching](/docs/id/build-with-claude/prompt-caching).

### Harga residensi data

Untuk Claude Opus 4.6 dan model yang lebih baru, menentukan inferensi khusus AS melalui parameter `inference_geo` dikenakan pengali 1,1x pada semua kategori harga token, termasuk token input, token output, penulisan cache, dan pembacaan cache. Perutean global (default) menggunakan harga standar.

Ini hanya berlaku untuk Claude API (1P). Platform pihak ketiga memiliki harga regional mereka sendiri. Lihat [AWS Bedrock](https://aws.amazon.com/bedrock/pricing/) dan [Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/pricing) untuk detailnya. Model sebelumnya mempertahankan harga yang ada terlepas dari pengaturan `inference_geo`.

Untuk informasi lebih lanjut, lihat [dokumentasi residensi data](/docs/id/build-with-claude/data-residency).

### Harga fast mode

[Fast mode](/docs/id/build-with-claude/fast-mode) (beta: pratinjau penelitian) untuk Claude Opus 4.6 memberikan output yang jauh lebih cepat dengan harga premium (6x tarif standar). Harga fast mode berlaku di seluruh jendela konteks penuh, termasuk permintaan di atas 200k token input. Saat ini didukung pada Opus 4.6:

| Input | Output |
|:------|:-------|
| $30 / MTok | $150 / MTok |

Harga fast mode bertumpuk dengan pengubah harga lainnya:
- [Pengali prompt caching](#model-pricing) berlaku di atas harga fast mode
- Pengali [residensi data](/docs/id/build-with-claude/data-residency) berlaku di atas harga fast mode

Fast mode tidak tersedia dengan [Batch API](#batch-processing).

Untuk informasi lebih lanjut, lihat [dokumentasi fast mode](/docs/id/build-with-claude/fast-mode).

### Pemrosesan batch

Batch API memungkinkan pemrosesan asinkron dari volume permintaan yang besar dengan diskon 50% pada token input dan output.

| Model             | Batch input      | Batch output    |
|-------------------|------------------|-----------------|
| Claude Opus 4.6       | $2.50 / MTok     | $12.50 / MTok   |
| Claude Opus 4.5     | $2.50 / MTok     | $12.50 / MTok   |
| Claude Opus 4.1     | $7.50 / MTok     | $37.50 / MTok   |
| Claude Opus 4     | $7.50 / MTok     | $37.50 / MTok   |
| Claude Sonnet 4.6   | $1.50 / MTok     | $7.50 / MTok    |
| Claude Sonnet 4.5   | $1.50 / MTok     | $7.50 / MTok    |
| Claude Sonnet 4   | $1.50 / MTok     | $7.50 / MTok    |
| Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)) | $1.50 / MTok     | $7.50 / MTok    |
| Claude Haiku 4.5  | $0.50 / MTok     | $2.50 / MTok    |
| Claude Haiku 3.5  | $0.40 / MTok     | $2 / MTok       |
| Claude Opus 3 ([deprecated](/docs/en/about-claude/model-deprecations))  | $7.50 / MTok     | $37.50 / MTok   |
| Claude Haiku 3    | $0.125 / MTok    | $0.625 / MTok   |

Untuk informasi lebih lanjut tentang pemrosesan batch, lihat [dokumentasi pemrosesan batch](/docs/id/build-with-claude/batch-processing).

### Harga konteks panjang

[Claude Mythos Preview](https://anthropic.com/glasswing), Opus 4.6 dan Sonnet 4.6 mencakup [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) penuh dengan harga standar. (Permintaan 900k token ditagih dengan tarif per token yang sama seperti permintaan 9k token.) Diskon prompt caching dan pemrosesan batch berlaku dengan tarif standar di seluruh jendela konteks penuh.

### Harga penggunaan alat

Tool use requests are priced based on:
1. The total number of input tokens sent to the model (including in the `tools` parameter)
2. The number of output tokens generated
3. For server-side tools, additional usage-based pricing (e.g., web search charges per search performed)

Client-side tools are priced the same as any other Claude API request, while server-side tools may incur additional charges based on their specific usage.

The additional tokens from tool use come from:

- The `tools` parameter in API requests (tool names, descriptions, and schemas)
- `tool_use` content blocks in API requests and responses
- `tool_result` content blocks in API requests

When you use `tools`, we also automatically include a special system prompt for the model which enables tool use. The number of tool use tokens required for each model are listed below (excluding the additional tokens listed above). Note that the table assumes at least 1 tool is provided. If no `tools` are provided, then a tool choice of `none` uses 0 additional system prompt tokens.

| Model                    | Tool choice                                          | Tool use system prompt token count          |
|--------------------------|------------------------------------------------------|---------------------------------------------|
| Claude Opus 4.6              | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Opus 4.5            | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Opus 4.1            | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Opus 4            | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Sonnet 4.6          | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Sonnet 4.5          | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Sonnet 4          | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations))        | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Haiku 4.5         | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Haiku 3.5         | `auto`, `none`<hr />`any`, `tool`   | 264 tokens<hr />340 tokens |
| Claude Opus 3 ([deprecated](/docs/en/about-claude/model-deprecations))            | `auto`, `none`<hr />`any`, `tool`   | 530 tokens<hr />281 tokens |
| Claude Sonnet 3          | `auto`, `none`<hr />`any`, `tool`   | 159 tokens<hr />235 tokens |
| Claude Haiku 3           | `auto`, `none`<hr />`any`, `tool`   | 264 tokens<hr />340 tokens |

These token counts are added to your normal input and output tokens to calculate the total cost of a request.

Untuk harga per model saat ini, lihat bagian [harga model](#model-pricing).

Untuk informasi lebih lanjut tentang implementasi penggunaan alat dan praktik terbaik, lihat [dokumentasi penggunaan alat](/docs/id/agents-and-tools/tool-use/overview).

### Harga alat tertentu

#### Alat Bash

The bash tool adds **245 input tokens** to your API calls.

Additional tokens are consumed by:
- Command outputs (stdout/stderr)
- Error messages
- Large file contents

Lihat [harga penggunaan alat](#tool-use-pricing) untuk detail harga lengkap.

#### Alat eksekusi kode

**Code execution is free when used with web search or web fetch.** When `web_search_20260209` or `web_fetch_20260209` is included in your API request, there are no additional charges for code execution tool calls beyond the standard input and output token costs.

When used without these tools, code execution is billed by execution time, tracked separately from token usage:

- Execution time has a minimum of 5 minutes
- Each organization receives **1,550 free hours** of usage per month
- Additional usage beyond 1,550 hours is billed at **$0.05 per hour, per container**
- If files are included in the request, execution time is billed even if the tool is not invoked, due to files being preloaded onto the container

Code execution usage is tracked in the response:

```json
"usage": {
  "input_tokens": 105,
  "output_tokens": 239,
  "server_tool_use": {
    "code_execution_requests": 1
  }
}
```

#### Alat editor teks

The text editor tool uses the same pricing structure as other tools used with Claude. It follows the standard input and output token pricing based on the Claude model you're using.

In addition to the base tokens, the following additional input tokens are needed for the text editor tool:

| Tool | Additional input tokens |
| ----------------------------------------- | --------------------------------------- |
| `text_editor_20250429` (Claude 4.x) | 700 tokens |
| `text_editor_20250124` (Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations))) | 700 tokens |

Lihat [harga penggunaan alat](#tool-use-pricing) untuk detail harga lengkap.

#### Alat pencarian web

Web search usage is charged in addition to token usage:

```json
"usage": {
  "input_tokens": 105,
  "output_tokens": 6039,
  "cache_read_input_tokens": 7123,
  "cache_creation_input_tokens": 7345,
  "server_tool_use": {
    "web_search_requests": 1
  }
}
```

Web search is available on the Claude API for **$10 per 1,000 searches**, plus standard token costs for search-generated content. Web search results retrieved throughout a conversation are counted as input tokens, in search iterations executed during a single turn and in subsequent conversation turns.

Each web search counts as one use, regardless of the number of results returned. If an error occurs during web search, the web search will not be billed.

#### Alat pengambilan web

Web fetch usage has **no additional charges** beyond standard token costs:

```json
"usage": {
  "input_tokens": 25039,
  "output_tokens": 931,
  "cache_read_input_tokens": 0,
  "cache_creation_input_tokens": 0,
  "server_tool_use": {
    "web_fetch_requests": 1
  }
}
```

The web fetch tool is available on the Claude API at **no additional cost**. You only pay standard token costs for the fetched content that becomes part of your conversation context.

To protect against inadvertently fetching large content that would consume excessive tokens, use the `max_content_tokens` parameter to set appropriate limits based on your use case and budget considerations.

Example token usage for typical content:
- Average web page (10&nbsp;kB): ~2,500 tokens
- Large documentation page (100&nbsp;kB): ~25,000 tokens
- Research paper PDF (500&nbsp;kB): ~125,000 tokens

#### Alat penggunaan komputer

Computer use follows the standard [tool use pricing](/docs/en/agents-and-tools/tool-use/overview#pricing). When using the computer use tool:

**System prompt overhead**: The computer use beta adds 466-499 tokens to the system prompt

**Computer use tool token usage**:
| Model | Input tokens per tool definition |
| ----- | -------------------------------- |
| Claude 4.x models | 735 tokens |
| Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)) | 735 tokens |

**Additional token consumption**:
- Screenshot images (see [Vision pricing](/docs/en/build-with-claude/vision))
- Tool execution results returned to Claude

<Note>
If you're also using bash or text editor tools alongside computer use, those tools have their own token costs as documented in their respective pages.
</Note>

## Harga Claude Managed Agents

[Claude Managed Agents](/docs/id/managed-agents/overview) ditagih berdasarkan dua dimensi: token dan durasi sesi.

### Token

Semua token yang dikonsumsi oleh sesi Claude Managed Agents ditagih dengan tarif yang ditunjukkan dalam [Harga model](#model-pricing) di atas. Pengali [Prompt caching](#prompt-caching) berlaku secara identik. Pencarian web yang dipicu di dalam sesi dikenakan biaya standar $10 per 1.000 pencarian.

Pengubah Messages API berikut **tidak** berlaku untuk sesi Claude Managed Agents:

| Pengubah | Mengapa tidak berlaku |
| --- | --- |
| [Diskon Batch API](#batch-processing) | Sesi bersifat stateful dan interaktif. Tidak ada mode batch. |
| [Premi fast mode](#fast-mode-pricing) | Kecepatan inferensi dikelola oleh runtime. |
| [Pengali residensi data](#data-residency-pricing) | `inference_geo` adalah field permintaan Messages API. |
| [Premi konteks panjang](#long-context-pricing) | Jendela konteks dikelola oleh runtime. |
| [Harga platform pihak ketiga](#third-party-platform-pricing) | Claude Managed Agents hanya tersedia melalui Claude API secara langsung. |

### Durasi sesi

| SKU | Tarif | Pengukuran |
| --- | --- | --- |
| Durasi sesi | $0,08 per jam sesi | Durasi status `running` |

Durasi diukur hingga milidetik dan hanya terakumulasi saat status sesi adalah `running`. Waktu yang dihabiskan dalam status `idle` (menunggu pesan berikutnya atau konfirmasi alat), `rescheduling`, atau `terminated` tidak dihitung sebagai durasi.

<Note>
Durasi sesi menggantikan model penagihan jam kontainer [Code Execution](#code-execution-tool) saat menggunakan Claude Managed Agents. Anda tidak ditagih secara terpisah untuk jam kontainer di atas durasi sesi.
</Note>

### Contoh perhitungan

Sesi coding satu jam menggunakan Claude Opus 4.6 yang mengonsumsi 50.000 token input dan 15.000 token output:

| Item | Perhitungan | Biaya |
| --- | --- | --- |
| Token input | 50.000 × $5 / 1.000.000 | $0,25 |
| Token output | 15.000 × $25 / 1.000.000 | $0,375 |
| Durasi sesi | 1,0 jam × $0,08 | $0,08 |
| **Total** | | **$0,705** |

Jika prompt caching aktif dan 40.000 dari token input adalah cache read:

| Item | Perhitungan | Biaya |
| --- | --- | --- |
| Token input tidak di-cache | 10.000 × $5 / 1.000.000 | $0,05 |
| Token cache read | 40.000 × $5 × 0,1 / 1.000.000 | $0,02 |
| Token output | 15.000 × $25 / 1.000.000 | $0,375 |
| Durasi sesi | 1,0 jam × $0,08 | $0,08 |
| **Total** | | **$0,525** |

<Note>
  Contoh perhitungan untuk memproses 10.000 tiket dukungan:
  - Rata-rata ~3.700 token per percakapan
  - Menggunakan Claude Opus 4.6 dengan input $5/MTok, output $25/MTok
  - Total biaya: ~$37,00 per 10.000 tiket
</Note>

Untuk panduan terperinci tentang perhitungan ini, lihat [panduan agen dukungan pelanggan](/docs/id/about-claude/use-case-guides/customer-support-chat).

## Pertimbangan harga tambahan

### Strategi optimasi biaya

Saat membangun agen dengan Claude:

1. **Gunakan model yang sesuai:** Pilih Haiku untuk tugas sederhana, Sonnet untuk penalaran kompleks
2. **Terapkan prompt caching:** Kurangi biaya untuk konteks yang berulang
3. **Operasi batch:** Gunakan Batch API untuk tugas yang tidak sensitif terhadap waktu
4. **Pantau pola penggunaan:** Lacak konsumsi token untuk mengidentifikasi peluang optimasi

<Tip>
  Untuk aplikasi agen bervolume tinggi, hubungi [tim penjualan enterprise](https://claude.com/contact-sales) untuk pengaturan harga khusus.
</Tip>

### Batas laju

Batas laju bervariasi berdasarkan tingkat penggunaan dan memengaruhi berapa banyak permintaan yang dapat Anda buat:

- **Tier 1:** Penggunaan tingkat awal dengan batas dasar
- **Tier 2:** Batas yang ditingkatkan untuk aplikasi yang berkembang
- **Tier 3:** Batas lebih tinggi untuk aplikasi yang sudah mapan
- **Tier 4:** Batas standar maksimum
- **Enterprise:** Batas khusus tersedia

Untuk informasi batas laju terperinci, lihat [dokumentasi batas laju](/docs/id/api/rate-limits).

Untuk batas laju yang lebih tinggi atau pengaturan harga khusus, [hubungi tim penjualan](https://claude.com/contact-sales).

### Diskon volume

Diskon volume mungkin tersedia untuk pengguna bervolume tinggi. Ini dinegosiasikan berdasarkan kasus per kasus.

- Tingkat standar menggunakan harga yang ditunjukkan di atas
- Pelanggan enterprise dapat [menghubungi penjualan](mailto:sales@anthropic.com) untuk harga khusus
- Diskon akademik dan penelitian mungkin tersedia

### Harga enterprise

Untuk pelanggan enterprise dengan kebutuhan khusus:

- Batas laju khusus
- Diskon volume
- Dukungan khusus
- Ketentuan khusus

Hubungi tim penjualan di [sales@anthropic.com](mailto:sales@anthropic.com) atau melalui [Claude Console](/settings/limits) untuk mendiskusikan opsi harga enterprise.

## Penagihan dan pembayaran

- Penagihan berdasarkan penggunaan bulanan aktual
- Semua pembayaran dalam USD
- Opsi kartu kredit dan faktur tersedia
- Pelacakan penggunaan tersedia di [Claude Console](/)

## Pertanyaan yang sering diajukan

**Bagaimana penggunaan token dihitung?**

Token adalah potongan teks yang diproses oleh model. Sebagai perkiraan kasar, 1 token kira-kira 4 karakter atau 0,75 kata dalam bahasa Inggris. Jumlah pasti bervariasi berdasarkan bahasa dan jenis konten.

**Apakah ada tingkat gratis atau uji coba?**

Pengguna baru menerima sejumlah kecil kredit gratis untuk menguji API. [Hubungi penjualan](mailto:sales@anthropic.com) untuk informasi tentang uji coba yang diperpanjang untuk evaluasi enterprise.

**Bagaimana diskon bertumpuk?**

Diskon Batch API dan prompt caching dapat digabungkan. Misalnya, menggunakan kedua fitur bersama-sama memberikan penghematan biaya yang signifikan dibandingkan panggilan API standar. Lihat [harga prompt caching](#prompt-caching) untuk cara pengali berinteraksi.

**Metode pembayaran apa yang diterima?**

Kartu kredit utama diterima untuk akun standar. Pelanggan enterprise dapat mengatur faktur dan metode pembayaran lainnya.

Untuk pertanyaan tambahan tentang harga, hubungi [support@anthropic.com](mailto:support@anthropic.com).