---
source: platform
url: https://platform.claude.com/docs/id/api/openai-sdk
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 92e2885ab4731bf9f7bdeca7b408a83b8cd2797f78a80c78fcdfe41a73bdd675
---

# Kompatibilitas OpenAI SDK

Anthropic menyediakan lapisan kompatibilitas yang memungkinkan Anda menggunakan OpenAI SDK untuk menguji Claude API. Dengan beberapa perubahan kode, Anda dapat dengan cepat mengevaluasi kemampuan model Claude.

---

<Note>
Lapisan kompatibilitas ini terutama dimaksudkan untuk menguji dan membandingkan kemampuan model, dan tidak dianggap sebagai solusi jangka panjang atau siap produksi untuk sebagian besar kasus penggunaan. Meskipun kami bermaksud untuk menjaganya tetap berfungsi penuh dan tidak membuat perubahan yang merusak, prioritas kami adalah keandalan dan efektivitas [Claude API](/docs/id/api/overview).

Untuk informasi lebih lanjut tentang batasan kompatibilitas yang diketahui, lihat [Batasan kompatibilitas OpenAI yang penting](#important-openai-compatibility-limitations).

Jika Anda mengalami masalah dengan fitur kompatibilitas OpenAI SDK, silakan beri tahu kami [di sini](https://forms.gle/oQV4McQNiuuNbz9n8).
</Note>

<Tip>
Untuk pengalaman terbaik dan akses ke rangkaian fitur lengkap Claude API ([pemrosesan PDF](/docs/id/build-with-claude/pdf-support), [kutipan](/docs/id/build-with-claude/citations), [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking), dan [penyimpanan prompt](/docs/id/build-with-claude/prompt-caching)), kami merekomendasikan menggunakan [Claude API](/docs/id/api/overview) asli.
</Tip>

## Memulai dengan OpenAI SDK

Untuk menggunakan fitur kompatibilitas OpenAI SDK, Anda perlu:

1. Menggunakan OpenAI SDK resmi
2. Mengubah hal berikut
   * Perbarui URL dasar Anda untuk menunjuk ke Claude API
   * Ganti kunci API Anda dengan [kunci Claude API](/settings/keys)
   * Perbarui nama model Anda untuk menggunakan [model Claude](/docs/id/about-claude/models/overview)
3. Tinjau dokumentasi di bawah untuk fitur apa yang didukung

### Contoh mulai cepat

<CodeGroup>
    ```python Python
    from openai import OpenAI

    client = OpenAI(
        api_key="ANTHROPIC_API_KEY",  # Your Claude API key
        base_url="https://api.anthropic.com/v1/"  # the Claude API endpoint
    )

    response = client.chat.completions.create(
        model="claude-opus-4-6", # Anthropic model name
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who are you?"}
        ],
    )

    print(response.choices[0].message.content)
    ```
    
    ```typescript TypeScript
    import OpenAI from 'openai';

    const openai = new OpenAI({
        apiKey: "ANTHROPIC_API_KEY",   // Your Claude API key
        baseURL: "https://api.anthropic.com/v1/",  // Claude API endpoint
    });

    const response = await openai.chat.completions.create({
        messages: [
            { role: "user", content: "Who are you?" }
        ],
        model: "claude-opus-4-6", // Claude model name
    });

    console.log(response.choices[0].message.content);
    ```
</CodeGroup>

## Batasan kompatibilitas OpenAI yang penting

#### Perilaku API

Berikut adalah perbedaan paling substansial dari penggunaan OpenAI:

* Parameter `strict` untuk pemanggilan fungsi diabaikan, yang berarti JSON penggunaan alat tidak dijamin mengikuti skema yang disediakan. Untuk kepatuhan skema yang dijamin, gunakan [Claude API asli dengan Structured Outputs](/docs/id/build-with-claude/structured-outputs).
* Input audio tidak didukung; itu akan diabaikan dan dihapus dari input
* Penyimpanan prompt tidak didukung, tetapi didukung dalam [Anthropic SDK](/docs/id/api/client-sdks)
* Pesan sistem/pengembang diangkat dan digabungkan ke awal percakapan, karena Anthropic hanya mendukung satu pesan sistem awal.

Sebagian besar bidang yang tidak didukung diabaikan secara diam-diam daripada menghasilkan kesalahan. Semuanya didokumentasikan di bawah.

#### Pertimbangan kualitas output

Jika Anda telah melakukan banyak penyesuaian pada prompt Anda, kemungkinan besar itu akan disesuaikan dengan baik khusus untuk OpenAI. Pertimbangkan menggunakan [penyempurna prompt kami di Claude Console](/dashboard) sebagai titik awal yang baik.

#### Pengangkatan pesan sistem / pengembang

Sebagian besar input ke OpenAI SDK jelas memetakan langsung ke parameter API Anthropic, tetapi satu perbedaan yang jelas adalah penanganan prompt sistem / pengembang. Kedua prompt ini dapat ditempatkan di seluruh percakapan obrolan melalui OpenAI. Karena Anthropic hanya mendukung pesan sistem awal, kami mengambil semua pesan sistem/pengembang dan menggabungkannya bersama dengan satu baris baru (`\n`) di antara mereka. String lengkap ini kemudian disediakan sebagai pesan sistem tunggal di awal pesan.

#### Dukungan pemikiran diperpanjang

Anda dapat mengaktifkan kemampuan [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) dengan menambahkan parameter `thinking`. Meskipun ini akan meningkatkan penalaran Claude untuk tugas-tugas kompleks, OpenAI SDK tidak akan mengembalikan proses pemikiran terperinci Claude. Untuk fitur pemikiran diperpanjang lengkap, termasuk akses ke output penalaran langkah demi langkah Claude, gunakan Claude API asli.

<CodeGroup>
    ```python Python
    response = client.chat.completions.create(
        model="claude-sonnet-4-5",
        messages=...,
        extra_body={
            "thinking": { "type": "enabled", "budget_tokens": 2000 }
        }
    )
    ```
    
    ```typescript TypeScript
    const response = await openai.chat.completions.create({
        messages: [
            { role: "user", content: "Who are you?" }
        ],
        model: "claude-sonnet-4-5",
        // @ts-expect-error
        thinking: { type: "enabled", budget_tokens: 2000 }
    });

    ```
</CodeGroup>

## Batas laju

Batas laju mengikuti [batas standar](/docs/id/api/rate-limits) Anthropic untuk endpoint `/v1/messages`.

## Dukungan API Kompatibel OpenAI Terperinci
### Bidang permintaan
#### Bidang sederhana
| Bidang | Status dukungan |
|--------|----------------|
| `model` | Gunakan nama model Claude |
| `max_tokens` | Sepenuhnya didukung |
| `max_completion_tokens` | Sepenuhnya didukung |
| `stream` | Sepenuhnya didukung |
| `stream_options` | Sepenuhnya didukung |
| `top_p` | Sepenuhnya didukung |
| `parallel_tool_calls` | Sepenuhnya didukung |
| `stop` | Semua urutan penghenti non-spasi putih berfungsi |
| `temperature` | Antara 0 dan 1 (inklusif). Nilai lebih besar dari 1 dibatasi pada 1. |
| `n` | Harus tepat 1 |
| `logprobs` | Diabaikan |
| `metadata` | Diabaikan |
| `response_format` | Diabaikan. Untuk output JSON, gunakan [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dengan Claude API asli |
| `prediction` | Diabaikan |
| `presence_penalty` | Diabaikan |
| `frequency_penalty` | Diabaikan |
| `seed` | Diabaikan |
| `service_tier` | Diabaikan |
| `audio` | Diabaikan |
| `logit_bias` | Diabaikan |
| `store` | Diabaikan |
| `user` | Diabaikan |
| `modalities` | Diabaikan |
| `top_logprobs` | Diabaikan |
| `reasoning_effort` | Diabaikan |

#### Bidang `tools` / `functions`
<section title="Tampilkan bidang">

<Tabs>
<Tab title="Tools">
Bidang `tools[n].function`
| Bidang        | Status dukungan         |
|--------------|-----------------|
| `name`       | Sepenuhnya didukung |
| `description`| Sepenuhnya didukung |
| `parameters` | Sepenuhnya didukung |
| `strict`     | Diabaikan. Gunakan [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dengan Claude API asli untuk validasi skema ketat |
</Tab>
<Tab title="Functions">

Bidang `functions[n]`
<Info>
OpenAI telah menghapuskan bidang `functions` dan menyarankan menggunakan `tools` sebagai gantinya.
</Info>
| Bidang        | Status dukungan         |
|--------------|-----------------|
| `name`       | Sepenuhnya didukung |
| `description`| Sepenuhnya didukung |
| `parameters` | Sepenuhnya didukung |
| `strict`     | Diabaikan. Gunakan [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dengan Claude API asli untuk validasi skema ketat |
</Tab>
</Tabs>

</section>

#### Bidang array `messages`
<section title="Tampilkan bidang">

<Tabs>
<Tab title="Peran pengembang">
Bidang untuk `messages[n].role == "developer"`
<Info>
Pesan pengembang diangkat ke awal percakapan sebagai bagian dari pesan sistem awal
</Info>
| Bidang | Status dukungan |
|-------|---------|
| `content` | Sepenuhnya didukung, tetapi diangkat |
| `name` | Diabaikan |

</Tab>
<Tab title="Peran sistem">
Bidang untuk `messages[n].role == "system"`

<Info>
Pesan sistem diangkat ke awal percakapan sebagai bagian dari pesan sistem awal
</Info>
| Bidang | Status dukungan |
|-------|---------|
| `content` | Sepenuhnya didukung, tetapi diangkat |
| `name` | Diabaikan |

</Tab>
<Tab title="Peran pengguna">
Bidang untuk `messages[n].role == "user"`

| Bidang | Varian | Sub-bidang | Status dukungan |
|-------|---------|-----------|----------------|
| `content` | `string` | | Sepenuhnya didukung |
| | `array`, `type == "text"` | | Sepenuhnya didukung |
| | `array`, `type == "image_url"` | `url` | Sepenuhnya didukung |
| | | `detail` | Diabaikan |
| | `array`, `type == "input_audio"` | | Diabaikan |
| | `array`, `type == "file"` | | Diabaikan |
| `name` | | | Diabaikan |

</Tab>

<Tab title="Peran asisten">
Bidang untuk `messages[n].role == "assistant"`
| Bidang | Varian | Status dukungan |
|-------|---------|----------------|
| `content` | `string` | Sepenuhnya didukung |
| | `array`, `type == "text"` | Sepenuhnya didukung |
| | `array`, `type == "refusal"` | Diabaikan |
| `tool_calls` | | Sepenuhnya didukung |
| `function_call` | | Sepenuhnya didukung |
| `audio` | | Diabaikan |
| `refusal` | | Diabaikan |

</Tab>

<Tab title="Peran alat">
Bidang untuk `messages[n].role == "tool"`
| Bidang | Varian | Status dukungan |
|-------|---------|----------------|
| `content` | `string` | Sepenuhnya didukung |
| | `array`, `type == "text"` | Sepenuhnya didukung |
| `tool_call_id` | | Sepenuhnya didukung |
| `tool_choice` | | Sepenuhnya didukung |
| `name` | | Diabaikan |
</Tab>

<Tab title="Peran fungsi">
Bidang untuk `messages[n].role == "function"`
| Bidang | Varian | Status dukungan |
|-------|---------|----------------|
| `content` | `string` | Sepenuhnya didukung |
| | `array`, `type == "text"` | Sepenuhnya didukung |
| `tool_choice` | | Sepenuhnya didukung |
| `name` | | Diabaikan |
</Tab>
</Tabs>

</section>

### Bidang respons

| Bidang | Status dukungan |
|---------------------------|----------------|
| `id` | Sepenuhnya didukung |
| `choices[]` | Akan selalu memiliki panjang 1 |
| `choices[].finish_reason` | Sepenuhnya didukung |
| `choices[].index` | Sepenuhnya didukung |
| `choices[].message.role` | Sepenuhnya didukung |
| `choices[].message.content` | Sepenuhnya didukung |
| `choices[].message.tool_calls` | Sepenuhnya didukung |
| `object` | Sepenuhnya didukung |
| `created` | Sepenuhnya didukung |
| `model` | Sepenuhnya didukung |
| `finish_reason` | Sepenuhnya didukung |
| `content` | Sepenuhnya didukung |
| `usage.completion_tokens` | Sepenuhnya didukung |
| `usage.prompt_tokens` | Sepenuhnya didukung |
| `usage.total_tokens` | Sepenuhnya didukung |
| `usage.completion_tokens_details` | Selalu kosong |
| `usage.prompt_tokens_details` | Selalu kosong |
| `choices[].message.refusal` | Selalu kosong |
| `choices[].message.audio` | Selalu kosong |
| `logprobs` | Selalu kosong |
| `service_tier` | Selalu kosong |
| `system_fingerprint` | Selalu kosong |

### Kompatibilitas pesan kesalahan

Lapisan kompatibilitas mempertahankan format kesalahan yang konsisten dengan API OpenAI. Namun, pesan kesalahan terperinci tidak akan setara. Kami merekomendasikan hanya menggunakan pesan kesalahan untuk logging dan debugging.

### Kompatibilitas header

Meskipun OpenAI SDK secara otomatis mengelola header, berikut adalah daftar lengkap header yang didukung oleh Claude API untuk pengembang yang perlu bekerja dengannya secara langsung.

| Header | Status Dukungan |
|---------|----------------|
| `x-ratelimit-limit-requests` | Sepenuhnya didukung |
| `x-ratelimit-limit-tokens` | Sepenuhnya didukung |
| `x-ratelimit-remaining-requests` | Sepenuhnya didukung |
| `x-ratelimit-remaining-tokens` | Sepenuhnya didukung |
| `x-ratelimit-reset-requests` | Sepenuhnya didukung |
| `x-ratelimit-reset-tokens` | Sepenuhnya didukung |
| `retry-after` | Sepenuhnya didukung |
| `request-id` | Sepenuhnya didukung |
| `openai-version` | Selalu `2020-10-01` |
| `authorization` | Sepenuhnya didukung |
| `openai-processing-ms` | Selalu kosong |