---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 4586edd8efb387488e0b947eca000f8b46f1b89cc71eba9f4aa713387c61b791
---

# Kompatibilitas OpenAI SDK

Anthropic menyediakan lapisan kompatibilitas yang memungkinkan Anda menggunakan OpenAI SDK untuk menguji Claude API. Dengan beberapa perubahan kode, Anda dapat dengan cepat mengevaluasi kemampuan model Anthropic.

---

<Note>
  Lapisan kompatibilitas ini terutama ditujukan untuk menguji dan membandingkan kemampuan model, dan tidak dianggap sebagai solusi jangka panjang atau siap produksi untuk sebagian besar kasus penggunaan. Meskipun lapisan ini dimaksudkan untuk tetap berfungsi penuh dan tidak memiliki perubahan yang merusak, prioritasnya adalah keandalan dan efektivitas [Claude API](/docs/id/api/overview).

  Untuk informasi lebih lanjut tentang keterbatasan kompatibilitas yang diketahui, lihat [Keterbatasan penting kompatibilitas OpenAI](#important-openai-compatibility-limitations).

  Jika Anda mengalami masalah dengan fitur kompatibilitas OpenAI SDK, silakan bagikan umpan balik Anda melalui [formulir umpan balik kompatibilitas](https://forms.gle/oQV4McQNiuuNbz9n8) ini.
</Note>

<Tip>
  Untuk pengalaman terbaik dan akses ke rangkaian fitur lengkap Claude API ([pemrosesan PDF](/docs/id/build-with-claude/pdf-support), [sitasi](/docs/id/build-with-claude/citations), [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking), dan [caching prompt](/docs/id/build-with-claude/prompt-caching)), gunakan [Claude API](/docs/id/api/overview) native.
</Tip>

## Memulai dengan OpenAI SDK

Untuk menggunakan fitur kompatibilitas OpenAI SDK, Anda perlu:

1. Menggunakan OpenAI SDK resmi

2. Mengubah hal-hal berikut

   * Perbarui base URL Anda agar mengarah ke Claude API
   * Ganti kunci API Anda dengan [kunci Claude API](/settings/keys)
   * Perbarui nama model Anda untuk menggunakan [model Claude](/docs/id/about-claude/models/overview)

3. Tinjau dokumentasi di bawah ini untuk mengetahui fitur apa saja yang didukung

### Contoh mulai cepat

<CodeGroup>
  ```python Python
  import os

  from openai import OpenAI

  client = OpenAI(
      api_key=os.environ.get("ANTHROPIC_API_KEY"),  # Your Claude API key
      base_url="https://api.anthropic.com/v1/",  # the Claude API endpoint
  )

  response = client.chat.completions.create(
      model="claude-opus-4-8",  # Claude model name
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Who are you?"},
      ],
  )

  print(response.choices[0].message.content)
  ```

  ```typescript TypeScript
  import OpenAI from "openai";

  const openai = new OpenAI({
    apiKey: "ANTHROPIC_API_KEY", // Your Claude API key
    baseURL: "https://api.anthropic.com/v1/" // Claude API endpoint
  });

  const response = await openai.chat.completions.create({
    messages: [{ role: "user", content: "Who are you?" }],
    model: "claude-opus-4-8" // Claude model name
  });

  console.log(response.choices[0].message.content);
  ```
</CodeGroup>

## Keterbatasan penting kompatibilitas OpenAI

### Perilaku API

Berikut adalah perbedaan paling substansial dibandingkan menggunakan OpenAI:

* Parameter `strict` untuk pemanggilan fungsi diabaikan, yang berarti JSON tool\_use tidak dijamin mengikuti skema yang diberikan. Untuk kesesuaian skema yang terjamin, gunakan [Claude API native dengan Structured Outputs](/docs/id/build-with-claude/structured-outputs).
* Input audio tidak didukung; input tersebut akan diabaikan dan dihapus dari input
* Caching prompt tidak didukung, tetapi didukung di [Anthropic SDK](/docs/id/cli-sdks-libraries/overview)
* Pesan system/developer diangkat dan digabungkan ke awal percakapan, karena Anthropic hanya mendukung satu pesan sistem awal.

Sebagian besar field yang tidak didukung diabaikan secara diam-diam alih-alih menghasilkan error. Semuanya didokumentasikan di bawah ini.

### Pertimbangan kualitas output

Jika Anda telah melakukan banyak penyesuaian pada prompt Anda, kemungkinan besar prompt tersebut telah disetel dengan baik khusus untuk OpenAI. Pertimbangkan untuk mengerjakan ulang prompt tersebut untuk Claude menggunakan [panduan praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

### Pengangkatan pesan system / developer

Sebagian besar input ke OpenAI SDK jelas dipetakan langsung ke parameter API Anthropic, tetapi satu perbedaan yang mencolok adalah penanganan prompt system / developer. Kedua prompt ini dapat ditempatkan di sepanjang percakapan chat melalui OpenAI. Karena Anthropic hanya mendukung pesan sistem awal, API mengambil semua pesan system/developer dan menggabungkannya bersama dengan satu baris baru (`\n`) di antaranya. String lengkap ini kemudian diberikan sebagai satu pesan sistem di awal pesan.

### Dukungan pemikiran diperpanjang

Anda dapat mengaktifkan kemampuan [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) dengan menambahkan parameter `thinking`. Meskipun ini meningkatkan penalaran Claude untuk tugas-tugas kompleks, OpenAI SDK tidak mengembalikan proses berpikir Claude secara terperinci. Untuk fitur pemikiran diperpanjang lengkap, termasuk akses ke output penalaran langkah demi langkah Claude, gunakan Claude API native.

<CodeGroup>
  ```python Python
  response = client.chat.completions.create(
      model="claude-sonnet-4-6",
      messages=[{"role": "user", "content": "Who are you?"}],
      extra_body={"thinking": {"type": "enabled", "budget_tokens": 2000}},
  )
  ```

  ```typescript TypeScript
  const response = await openai.chat.completions.create({
    messages: [{ role: "user", content: "Who are you?" }],
    model: "claude-sonnet-4-6",
    // @ts-expect-error
    thinking: { type: "enabled", budget_tokens: 2000 }
  });
  ```
</CodeGroup>

## Batas laju

Batas laju mengikuti [batas standar](/docs/id/api/rate-limits) Anthropic untuk endpoint `/v1/messages`.

## Dukungan API kompatibel OpenAI secara terperinci

### Field permintaan

#### Field sederhana

| Field                   | Status dukungan                                                                                                                    |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `model`                 | Gunakan nama model Claude                                                                                                          |
| `max_tokens`            | Didukung penuh                                                                                                                     |
| `max_completion_tokens` | Didukung penuh                                                                                                                     |
| `stream`                | Didukung penuh                                                                                                                     |
| `stream_options`        | Didukung penuh                                                                                                                     |
| `top_p`                 | Didukung penuh                                                                                                                     |
| `parallel_tool_calls`   | Didukung penuh                                                                                                                     |
| `stop`                  | Semua stop sequence non-spasi berfungsi                                                                                            |
| `temperature`           | Antara 0 dan 1 (inklusif). Nilai yang lebih besar dari 1 dibatasi pada 1.                                                          |
| `n`                     | Harus tepat 1                                                                                                                      |
| `logprobs`              | Diabaikan                                                                                                                          |
| `metadata`              | Diabaikan                                                                                                                          |
| `response_format`       | Diabaikan. Untuk output JSON, gunakan [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dengan Claude API native |
| `prediction`            | Diabaikan                                                                                                                          |
| `presence_penalty`      | Diabaikan                                                                                                                          |
| `frequency_penalty`     | Diabaikan                                                                                                                          |
| `seed`                  | Diabaikan                                                                                                                          |
| `service_tier`          | Diabaikan                                                                                                                          |
| `audio`                 | Diabaikan                                                                                                                          |
| `logit_bias`            | Diabaikan                                                                                                                          |
| `store`                 | Diabaikan                                                                                                                          |
| `user`                  | Diabaikan                                                                                                                          |
| `modalities`            | Diabaikan                                                                                                                          |
| `top_logprobs`          | Diabaikan                                                                                                                          |
| `reasoning_effort`      | Diabaikan                                                                                                                          |

#### Field `tools` / `functions`

<Accordion title="Show fields">
  <Tabs>
    <Tab title="Tools">
      Field `tools[n].function`

      | Field         | Status dukungan                                                                                                                                 |
      | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
      | `name`        | Didukung penuh                                                                                                                                  |
      | `description` | Didukung penuh                                                                                                                                  |
      | `parameters`  | Didukung penuh                                                                                                                                  |
      | `strict`      | Diabaikan. Gunakan [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dengan Claude API native untuk validasi skema yang ketat |
    </Tab>

    <Tab title="Functions">
      Field `functions[n]`

      <Info>
        OpenAI telah menghentikan penggunaan field `functions` dan menyarankan untuk menggunakan `tools` sebagai gantinya.
      </Info>

      | Field         | Status dukungan                                                                                                                                 |
      | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
      | `name`        | Didukung penuh                                                                                                                                  |
      | `description` | Didukung penuh                                                                                                                                  |
      | `parameters`  | Didukung penuh                                                                                                                                  |
      | `strict`      | Diabaikan. Gunakan [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dengan Claude API native untuk validasi skema yang ketat |
    </Tab>
  </Tabs>
</Accordion>

#### Field array `messages`

<Accordion title="Show fields">
  <Tabs>
    <Tab title="Developer role">
      Field untuk `messages[n].role == "developer"`

      <Info>
        Pesan developer diangkat ke awal percakapan sebagai bagian dari pesan sistem awal
      </Info>

      | Field     | Status dukungan                 |
      | --------- | ------------------------------- |
      | `content` | Didukung penuh, tetapi diangkat |
      | `name`    | Diabaikan                       |
    </Tab>

    <Tab title="System role">
      Field untuk `messages[n].role == "system"`

      <Info>
        Pesan sistem diangkat ke awal percakapan sebagai bagian dari pesan sistem awal
      </Info>

      | Field     | Status dukungan                 |
      | --------- | ------------------------------- |
      | `content` | Didukung penuh, tetapi diangkat |
      | `name`    | Diabaikan                       |
    </Tab>

    <Tab title="User role">
      Field untuk `messages[n].role == "user"`

      | Field     | Varian                           | Sub-field | Status dukungan |
      | --------- | -------------------------------- | --------- | --------------- |
      | `content` | `string`                         |           | Didukung penuh  |
      |           | `array`, `type == "text"`        |           | Didukung penuh  |
      |           | `array`, `type == "image_url"`   | `url`     | Didukung penuh  |
      |           |                                  | `detail`  | Diabaikan       |
      |           | `array`, `type == "input_audio"` |           | Diabaikan       |
      |           | `array`, `type == "file"`        |           | Diabaikan       |
      | `name`    |                                  |           | Diabaikan       |
    </Tab>

    <Tab title="Assistant role">
      Field untuk `messages[n].role == "assistant"`

      | Field           | Varian                       | Status dukungan |
      | --------------- | ---------------------------- | --------------- |
      | `content`       | `string`                     | Didukung penuh  |
      |                 | `array`, `type == "text"`    | Didukung penuh  |
      |                 | `array`, `type == "refusal"` | Diabaikan       |
      | `tool_calls`    |                              | Didukung penuh  |
      | `function_call` |                              | Didukung penuh  |
      | `audio`         |                              | Diabaikan       |
      | `refusal`       |                              | Diabaikan       |
    </Tab>

    <Tab title="Tool role">
      Field untuk `messages[n].role == "tool"`

      | Field          | Varian                    | Status dukungan |
      | -------------- | ------------------------- | --------------- |
      | `content`      | `string`                  | Didukung penuh  |
      |                | `array`, `type == "text"` | Didukung penuh  |
      | `tool_call_id` |                           | Didukung penuh  |
      | `tool_choice`  |                           | Didukung penuh  |
      | `name`         |                           | Diabaikan       |
    </Tab>

    <Tab title="Function role">
      Field untuk `messages[n].role == "function"`

      | Field         | Varian                    | Status dukungan |
      | ------------- | ------------------------- | --------------- |
      | `content`     | `string`                  | Didukung penuh  |
      |               | `array`, `type == "text"` | Didukung penuh  |
      | `tool_choice` |                           | Didukung penuh  |
      | `name`        |                           | Diabaikan       |
    </Tab>
  </Tabs>
</Accordion>

### Field respons

| Field                             | Status dukungan                |
| --------------------------------- | ------------------------------ |
| `id`                              | Didukung penuh                 |
| `choices[]`                       | Akan selalu memiliki panjang 1 |
| `choices[].finish_reason`         | Didukung penuh                 |
| `choices[].index`                 | Didukung penuh                 |
| `choices[].message.role`          | Didukung penuh                 |
| `choices[].message.content`       | Didukung penuh                 |
| `choices[].message.tool_calls`    | Didukung penuh                 |
| `object`                          | Didukung penuh                 |
| `created`                         | Didukung penuh                 |
| `model`                           | Didukung penuh                 |
| `finish_reason`                   | Didukung penuh                 |
| `content`                         | Didukung penuh                 |
| `usage.completion_tokens`         | Didukung penuh                 |
| `usage.prompt_tokens`             | Didukung penuh                 |
| `usage.total_tokens`              | Didukung penuh                 |
| `usage.completion_tokens_details` | Selalu kosong                  |
| `usage.prompt_tokens_details`     | Selalu kosong                  |
| `choices[].message.refusal`       | Selalu kosong                  |
| `choices[].message.audio`         | Selalu kosong                  |
| `logprobs`                        | Selalu kosong                  |
| `service_tier`                    | Selalu kosong                  |
| `system_fingerprint`              | Selalu kosong                  |

### Kompatibilitas pesan error

Lapisan kompatibilitas mempertahankan format error yang konsisten dengan OpenAI API. Namun, pesan error yang terperinci tidak akan setara. Gunakan pesan error hanya untuk logging dan debugging.

### Kompatibilitas header

Meskipun OpenAI SDK secara otomatis mengelola header, berikut adalah daftar lengkap header yang didukung oleh Claude API untuk pengembang yang perlu bekerja dengannya secara langsung.

| Header                           | Status Dukungan     |
| -------------------------------- | ------------------- |
| `x-ratelimit-limit-requests`     | Didukung penuh      |
| `x-ratelimit-limit-tokens`       | Didukung penuh      |
| `x-ratelimit-remaining-requests` | Didukung penuh      |
| `x-ratelimit-remaining-tokens`   | Didukung penuh      |
| `x-ratelimit-reset-requests`     | Didukung penuh      |
| `x-ratelimit-reset-tokens`       | Didukung penuh      |
| `retry-after`                    | Didukung penuh      |
| `request-id`                     | Didukung penuh      |
| `openai-version`                 | Selalu `2020-10-01` |
| `authorization`                  | Didukung penuh      |
| `openai-processing-ms`           | Selalu kosong       |
