---
source: platform
url: https://platform.claude.com/docs/id/api/openai-sdk
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 864a4181175680ab24f0eb7817285599bbea6eda732297706fd3cd242711edbe
---

# Kompatibilitas OpenAI SDK

Anthropic menyediakan lapisan kompatibilitas yang memungkinkan Anda menggunakan OpenAI SDK untuk menguji Claude API. Dengan beberapa perubahan kode, Anda dapat dengan cepat mengevaluasi kemampuan model Anthropic.

---

<Note>
Lapisan kompatibilitas ini terutama dimaksudkan untuk menguji dan membandingkan kemampuan model, dan tidak dianggap sebagai solusi jangka panjang atau siap produksi untuk sebagian besar kasus penggunaan. Meskipun dimaksudkan untuk tetap berfungsi penuh dan tidak memiliki perubahan yang merusak, prioritasnya adalah keandalan dan efektivitas [Claude API](/docs/id/api/overview).

Untuk informasi lebih lanjut tentang batasan kompatibilitas yang diketahui, lihat [Batasan kompatibilitas OpenAI yang penting](#important-openai-compatibility-limitations).

Jika Anda mengalami masalah dengan fitur kompatibilitas OpenAI SDK, silakan bagikan umpan balik Anda melalui [formulir umpan balik kompatibilitas](https://forms.gle/oQV4McQNiuuNbz9n8) ini.
</Note>

<Tip>
Untuk pengalaman terbaik dan akses ke rangkaian fitur lengkap Claude API ([pemrosesan PDF](/docs/id/build-with-claude/pdf-support), [kutipan](/docs/id/build-with-claude/citations), [pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking), dan [penyimpanan prompt](/docs/id/build-with-claude/prompt-caching)), gunakan [Claude API](/docs/id/api/overview) asli.
</Tip>

## Memulai dengan OpenAI SDK

Untuk menggunakan fitur kompatibilitas OpenAI SDK, Anda perlu:

1. Menggunakan OpenAI SDK resmi
2. Mengubah hal berikut
   * Perbarui URL dasar Anda untuk menunjuk ke Claude API
   * Ganti kunci API Anda dengan [kunci Claude API](/settings/keys)
   * Perbarui nama model Anda untuk menggunakan [model Claude](/docs/id/about-claude/models/overview)
3. Tinjau dokumentasi di bawah ini untuk fitur apa yang didukung

### Contoh mulai cepat

<CodeGroup>
    
    ```python Python nocheck
    import os

    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),  # Your Claude API key
        base_url="https://api.anthropic.com/v1/",  # the Claude API endpoint
    )

    response = client.chat.completions.create(
        model="claude-opus-4-7",  # Claude model name
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who are you?"},
        ],
    )

    print(response.choices[0].message.content)
    ```

    
    ```typescript TypeScript nocheck
    import OpenAI from "openai";

    const openai = new OpenAI({
      apiKey: "ANTHROPIC_API_KEY", // Your Claude API key
      baseURL: "https://api.anthropic.com/v1/" // Claude API endpoint
    });

    const response = await openai.chat.completions.create({
      messages: [{ role: "user", content: "Who are you?" }],
      model: "claude-opus-4-7" // Claude model name
    });

    console.log(response.choices[0].message.content);
    ```

</CodeGroup>

## Batasan kompatibilitas OpenAI yang penting

### Perilaku API

Berikut adalah perbedaan paling substansial dari penggunaan OpenAI:

* Parameter `strict` untuk pemanggilan fungsi diabaikan, yang berarti JSON penggunaan alat tidak dijamin mengikuti skema yang disediakan. Untuk kepatuhan skema yang dijamin, gunakan [Claude API asli dengan Structured Outputs](/docs/id/build-with-claude/structured-outputs).
* Input audio tidak didukung; itu akan diabaikan dan dihapus dari input
* Penyimpanan prompt tidak didukung, tetapi didukung di [Anthropic SDK](/docs/id/api/client-sdks)
* Pesan sistem/pengembang diangkat dan digabungkan ke awal percakapan, karena Anthropic hanya mendukung satu pesan sistem awal.

Sebagian besar bidang yang tidak didukung diabaikan secara diam-diam daripada menghasilkan kesalahan. Semuanya didokumentasikan di bawah ini.

### Pertimbangan kualitas output

Jika Anda telah melakukan banyak penyesuaian pada prompt Anda, kemungkinan besar itu akan disesuaikan dengan baik khusus untuk OpenAI. Pertimbangkan menggunakan [penyempurna prompt di Claude Console](/dashboard) sebagai titik awal yang baik.

### Pengangkatan pesan sistem / pengembang

Sebagian besar input ke OpenAI SDK jelas memetakan langsung ke parameter API Anthropic, tetapi satu perbedaan yang berbeda adalah penanganan prompt sistem / pengembang. Kedua prompt ini dapat ditempatkan di seluruh percakapan obrolan melalui OpenAI. Karena Anthropic hanya mendukung pesan sistem awal, API mengambil semua pesan sistem/pengembang dan menggabungkannya bersama dengan satu baris baru (`\n`) di antara mereka. String lengkap ini kemudian disediakan sebagai pesan sistem tunggal di awal pesan.

### Dukungan pemikiran yang diperluas

Anda dapat mengaktifkan kemampuan [pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking) dengan menambahkan parameter `thinking`. Meskipun ini meningkatkan penalaran Claude untuk tugas-tugas kompleks, OpenAI SDK tidak mengembalikan proses pemikiran terperinci Claude. Untuk fitur pemikiran yang diperluas penuh, termasuk akses ke output penalaran langkah demi langkah Claude, gunakan Claude API asli.

<CodeGroup>
    
    ```python Python nocheck hidelines={1..9}
    import os

    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        base_url="https://api.anthropic.com/v1/",
    )

    response = client.chat.completions.create(
        model="claude-sonnet-4-6",
        messages=[{"role": "user", "content": "Who are you?"}],
        extra_body={"thinking": {"type": "enabled", "budget_tokens": 2000}},
    )
    ```

    
    ```typescript TypeScript nocheck
    const response = await openai.chat.completions.create({
      messages: [{ role: "user", content: "Who are you?" }],
      model: "claude-sonnet-4-6",
      // @ts-expect-error
      thinking: { type: "enabled", budget_tokens: 2000 }
    });
    ```

</CodeGroup>

## Batas laju

Batas laju mengikuti [batas standar](/docs/id/api/rate-limits) Anthropic untuk titik akhir `/v1/messages`.

## Dukungan API yang kompatibel dengan OpenAI secara terperinci
### Bidang permintaan
#### Bidang sederhana
| Bidang | Status dukungan |
|--------|----------------|
| `model` | Gunakan nama model Claude |
| `max_tokens` | Didukung sepenuhnya |
| `max_completion_tokens` | Didukung sepenuhnya |
| `stream` | Didukung sepenuhnya |
| `stream_options` | Didukung sepenuhnya |
| `top_p` | Didukung sepenuhnya |
| `parallel_tool_calls` | Didukung sepenuhnya |
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
| `name`       | Didukung sepenuhnya |
| `description`| Didukung sepenuhnya |
| `parameters` | Didukung sepenuhnya |
| `strict`     | Diabaikan. Gunakan [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dengan Claude API asli untuk validasi skema yang ketat |
</Tab>
<Tab title="Functions">

Bidang `functions[n]`
<Info>
OpenAI telah menghapus bidang `functions` dan menyarankan menggunakan `tools` sebagai gantinya.
</Info>
| Bidang        | Status dukungan         |
|--------------|-----------------|
| `name`       | Didukung sepenuhnya |
| `description`| Didukung sepenuhnya |
| `parameters` | Didukung sepenuhnya |
| `strict`     | Diabaikan. Gunakan [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dengan Claude API asli untuk validasi skema yang ketat |
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
| `content` | Didukung sepenuhnya, tetapi diangkat |
| `name` | Diabaikan |

</Tab>
<Tab title="Peran sistem">
Bidang untuk `messages[n].role == "system"`

<Info>
Pesan sistem diangkat ke awal percakapan sebagai bagian dari pesan sistem awal
</Info>
| Bidang | Status dukungan |
|-------|---------|
| `content` | Didukung sepenuhnya, tetapi diangkat |
| `name` | Diabaikan |

</Tab>
<Tab title="Peran pengguna">
Bidang untuk `messages[n].role == "user"`

| Bidang | Varian | Sub-bidang | Status dukungan |
|-------|---------|-----------|----------------|
| `content` | `string` | | Didukung sepenuhnya |
| | `array`, `type == "text"` | | Didukung sepenuhnya |
| | `array`, `type == "image_url"` | `url` | Didukung sepenuhnya |
| | | `detail` | Diabaikan |
| | `array`, `type == "input_audio"` | | Diabaikan |
| | `array`, `type == "file"` | | Diabaikan |
| `name` | | | Diabaikan |

</Tab>

<Tab title="Peran asisten">
Bidang untuk `messages[n].role == "assistant"`
| Bidang | Varian | Status dukungan |
|-------|---------|----------------|
| `content` | `string` | Didukung sepenuhnya |
| | `array`, `type == "text"` | Didukung sepenuhnya |
| | `array`, `type == "refusal"` | Diabaikan |
| `tool_calls` | | Didukung sepenuhnya |
| `function_call` | | Didukung sepenuhnya |
| `audio` | | Diabaikan |
| `refusal` | | Diabaikan |

</Tab>

<Tab title="Peran alat">
Bidang untuk `messages[n].role == "tool"`
| Bidang | Varian | Status dukungan |
|-------|---------|----------------|
| `content` | `string` | Didukung sepenuhnya |
| | `array`, `type == "text"` | Didukung sepenuhnya |
| `tool_call_id` | | Didukung sepenuhnya |
| `tool_choice` | | Didukung sepenuhnya |
| `name` | | Diabaikan |
</Tab>

<Tab title="Peran fungsi">
Bidang untuk `messages[n].role == "function"`
| Bidang | Varian | Status dukungan |
|-------|---------|----------------|
| `content` | `string` | Didukung sepenuhnya |
| | `array`, `type == "text"` | Didukung sepenuhnya |
| `tool_choice` | | Didukung sepenuhnya |
| `name` | | Diabaikan |
</Tab>
</Tabs>

</section>

### Bidang respons

| Bidang | Status dukungan |
|---------------------------|----------------|
| `id` | Didukung sepenuhnya |
| `choices[]` | Akan selalu memiliki panjang 1 |
| `choices[].finish_reason` | Didukung sepenuhnya |
| `choices[].index` | Didukung sepenuhnya |
| `choices[].message.role` | Didukung sepenuhnya |
| `choices[].message.content` | Didukung sepenuhnya |
| `choices[].message.tool_calls` | Didukung sepenuhnya |
| `object` | Didukung sepenuhnya |
| `created` | Didukung sepenuhnya |
| `model` | Didukung sepenuhnya |
| `finish_reason` | Didukung sepenuhnya |
| `content` | Didukung sepenuhnya |
| `usage.completion_tokens` | Didukung sepenuhnya |
| `usage.prompt_tokens` | Didukung sepenuhnya |
| `usage.total_tokens` | Didukung sepenuhnya |
| `usage.completion_tokens_details` | Selalu kosong |
| `usage.prompt_tokens_details` | Selalu kosong |
| `choices[].message.refusal` | Selalu kosong |
| `choices[].message.audio` | Selalu kosong |
| `logprobs` | Selalu kosong |
| `service_tier` | Selalu kosong |
| `system_fingerprint` | Selalu kosong |

### Kompatibilitas pesan kesalahan

Lapisan kompatibilitas mempertahankan format kesalahan yang konsisten dengan API OpenAI. Namun, pesan kesalahan terperinci tidak akan setara. Hanya gunakan pesan kesalahan untuk pencatatan dan debugging.

### Kompatibilitas header

Meskipun OpenAI SDK secara otomatis mengelola header, berikut adalah daftar lengkap header yang didukung oleh Claude API untuk pengembang yang perlu bekerja dengannya secara langsung.

| Header | Status Dukungan |
|---------|----------------|
| `x-ratelimit-limit-requests` | Didukung sepenuhnya |
| `x-ratelimit-limit-tokens` | Didukung sepenuhnya |
| `x-ratelimit-remaining-requests` | Didukung sepenuhnya |
| `x-ratelimit-remaining-tokens` | Didukung sepenuhnya |
| `x-ratelimit-reset-requests` | Didukung sepenuhnya |
| `x-ratelimit-reset-tokens` | Didukung sepenuhnya |
| `retry-after` | Didukung sepenuhnya |
| `request-id` | Didukung sepenuhnya |
| `openai-version` | Selalu `2020-10-01` |
| `authorization` | Didukung sepenuhnya |
| `openai-processing-ms` | Selalu kosong |