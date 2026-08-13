---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 4eebb907d5156e6ff15c9b21bc9cc8de89da4af9b331e7e80f82f0eec79bb9f2
---

---
title: Kompatibilitas OpenAI SDK
url: https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk
description: Anthropic menyediakan lapisan kompatibilitas yang memungkinkan Anda menggunakan OpenAI SDK untuk menguji Claude API. Dengan beberapa perubahan kode, Anda dapat dengan cepat mengevaluasi kemampuan model Anthropic.
---

<Note>
  Lapisan kompatibilitas ini terutama ditujukan untuk menguji dan membandingkan kemampuan model, dan tidak dianggap sebagai solusi jangka panjang atau siap produksi untuk sebagian besar kasus penggunaan. Meskipun lapisan ini dimaksudkan untuk tetap berfungsi penuh dan tidak memiliki perubahan yang merusak (breaking changes), prioritasnya adalah keandalan dan efektivitas [Claude API](https://platform.claude.com/docs/id/api/overview).

  Untuk informasi lebih lanjut tentang batasan kompatibilitas yang diketahui, lihat [Batasan penting kompatibilitas OpenAI](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk#important-openai-compatibility-limitations).

  Jika Anda mengalami masalah dengan fitur kompatibilitas OpenAI SDK, silakan bagikan masukan Anda melalui [formulir masukan kompatibilitas](https://forms.gle/oQV4McQNiuuNbz9n8) ini.
</Note>

<Tip>
  Untuk pengalaman terbaik dan akses ke set fitur lengkap Claude API ([pemrosesan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support), [sitasi](https://platform.claude.com/docs/id/build-with-claude/citations), [pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking), dan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)), gunakan [Claude API](https://platform.claude.com/docs/id/api/overview) native.
</Tip>

## Memulai dengan OpenAI SDK

Untuk menggunakan fitur kompatibilitas OpenAI SDK, Anda perlu:

1. Menggunakan OpenAI SDK resmi

2. Mengubah hal-hal berikut

   * Perbarui base URL Anda agar mengarah ke Claude API
   * Ganti kunci API Anda dengan [kunci API Claude](https://platform.claude.com/settings/keys)
   * Perbarui nama model Anda untuk menggunakan [model Claude](https://platform.claude.com/docs/id/about-claude/models/overview)

3. Tinjau bagian-bagian berikut untuk mengetahui fitur apa saja yang didukung

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
      model="claude-opus-5",  # Claude model name
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
    model: "claude-opus-5" // Claude model name
  });

  console.log(response.choices[0].message.content);
  ```
</CodeGroup>

## Batasan penting kompatibilitas OpenAI

### Perilaku API

Berikut adalah perbedaan paling substansial dibandingkan dengan menggunakan OpenAI:

* Parameter `strict` untuk pemanggilan fungsi (function calling) diabaikan, yang berarti JSON penggunaan alat tidak dijamin mengikuti skema yang disediakan. Untuk kesesuaian skema yang terjamin, gunakan [Claude API native dengan Structured Outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs).
* Input audio tidak didukung; input tersebut akan diabaikan dan dihapus dari input
* Caching prompt tidak didukung, tetapi didukung di [Anthropic SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview)
* Pesan system/developer diangkat (hoisted) dan digabungkan ke awal percakapan, karena Anthropic hanya mendukung satu pesan sistem awal.

Sebagian besar field yang tidak didukung diabaikan secara diam-diam alih-alih menghasilkan error. Semua ini didokumentasikan di bagian-bagian berikut.

### Pertimbangan kualitas output

Jika Anda telah banyak menyesuaikan prompt Anda, kemungkinan besar prompt tersebut sudah disetel dengan baik khusus untuk OpenAI. Pertimbangkan untuk mengerjakannya ulang untuk Claude menggunakan [panduan praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

### Pengangkatan (hoisting) pesan system / developer

Sebagian besar input ke OpenAI SDK jelas dipetakan langsung ke parameter API Anthropic, tetapi satu perbedaan yang mencolok adalah penanganan prompt system / developer. Kedua prompt ini dapat ditempatkan di sepanjang percakapan chat melalui OpenAI. Karena Anthropic hanya mendukung satu pesan sistem awal, API mengambil semua pesan system/developer dan menggabungkannya dengan satu baris baru (`\n`) di antaranya. String lengkap ini kemudian disediakan sebagai satu pesan sistem di awal pesan-pesan.

### Dukungan pemikiran (thinking)

Anda dapat mengaktifkan [pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking) dengan menambahkan parameter `thinking`. Pada model saat ini, pemikiran bersifat adaptif, dengan Claude yang memutuskan kapan dan seberapa dalam untuk berpikir, dan pada model Claude 5 fitur ini aktif secara default; pemikiran diperpanjang yang dikonfigurasi secara manual adalah mode lama (legacy). Meskipun pemikiran meningkatkan penalaran Claude untuk tugas-tugas kompleks, OpenAI SDK tidak mengembalikan proses pemikiran terperinci Claude. Untuk fitur pemikiran lengkap, termasuk akses ke output penalaran langkah demi langkah Claude, gunakan Claude API native.

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

Batas laju mengikuti [batas standar](https://platform.claude.com/docs/id/api/rate-limits) Anthropic untuk endpoint `/v1/messages`.

## Dukungan API kompatibel OpenAI secara terperinci

### Field permintaan

#### Field sederhana

| Field                   | Status dukungan                                                                                                                                               |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`                 | Gunakan nama model Claude                                                                                                                                     |
| `max_tokens`            | Didukung penuh                                                                                                                                                |
| `max_completion_tokens` | Didukung penuh                                                                                                                                                |
| `stream`                | Didukung penuh                                                                                                                                                |
| `stream_options`        | Didukung penuh                                                                                                                                                |
| `top_p`                 | Didukung penuh                                                                                                                                                |
| `parallel_tool_calls`   | Didukung penuh                                                                                                                                                |
| `stop`                  | Semua stop sequence non-whitespace berfungsi                                                                                                                  |
| `temperature`           | Antara 0 dan 1 (inklusif). Nilai yang lebih besar dari 1 dibatasi pada 1.                                                                                     |
| `n`                     | Harus tepat 1                                                                                                                                                 |
| `logprobs`              | Diabaikan                                                                                                                                                     |
| `metadata`              | Diabaikan                                                                                                                                                     |
| `response_format`       | Diabaikan. Untuk output JSON, gunakan [Structured Outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) dengan Claude API native |
| `prediction`            | Diabaikan                                                                                                                                                     |
| `presence_penalty`      | Diabaikan                                                                                                                                                     |
| `frequency_penalty`     | Diabaikan                                                                                                                                                     |
| `seed`                  | Diabaikan                                                                                                                                                     |
| `service_tier`          | Diabaikan                                                                                                                                                     |
| `audio`                 | Diabaikan                                                                                                                                                     |
| `logit_bias`            | Diabaikan                                                                                                                                                     |
| `store`                 | Diabaikan                                                                                                                                                     |
| `user`                  | Diabaikan                                                                                                                                                     |
| `modalities`            | Diabaikan                                                                                                                                                     |
| `top_logprobs`          | Diabaikan                                                                                                                                                     |
| `reasoning_effort`      | Diabaikan                                                                                                                                                     |

#### Field `tools` / `functions`

<Accordion title="Tampilkan field">
  <Tabs>
    <Tab title="Tools">
      Field `tools[n].function`

      | Field         | Status dukungan                                                                                                                                                            |
      | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
      | `name`        | Didukung penuh                                                                                                                                                             |
      | `description` | Didukung penuh                                                                                                                                                             |
      | `parameters`  | Didukung penuh                                                                                                                                                             |
      | `strict`      | Diabaikan. Gunakan [Structured Outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) dengan Claude API native untuk validasi skema yang ketat |
    </Tab>

    <Tab title="Functions">
      Field `functions[n]`

      <Info>
        OpenAI telah menghentikan (deprecated) field `functions` dan menyarankan untuk menggunakan `tools` sebagai gantinya.
      </Info>

      | Field         | Status dukungan                                                                                                                                                            |
      | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
      | `name`        | Didukung penuh                                                                                                                                                             |
      | `description` | Didukung penuh                                                                                                                                                             |
      | `parameters`  | Didukung penuh                                                                                                                                                             |
      | `strict`      | Diabaikan. Gunakan [Structured Outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) dengan Claude API native untuk validasi skema yang ketat |
    </Tab>
  </Tabs>
</Accordion>

#### Field array `messages`

<Accordion title="Tampilkan field">
  <Tabs>
    <Tab title="Developer role">
      Field untuk `messages[n].role == "developer"`

      <Info>
        Pesan developer diangkat (hoisted) ke awal percakapan sebagai bagian dari pesan sistem awal
      </Info>

      | Field     | Status dukungan                           |
      | --------- | ----------------------------------------- |
      | `content` | Didukung penuh, tetapi diangkat (hoisted) |
      | `name`    | Diabaikan                                 |
    </Tab>

    <Tab title="System role">
      Field untuk `messages[n].role == "system"`

      <Info>
        Pesan system diangkat (hoisted) ke awal percakapan sebagai bagian dari pesan sistem awal
      </Info>

      | Field     | Status dukungan                           |
      | --------- | ----------------------------------------- |
      | `content` | Didukung penuh, tetapi diangkat (hoisted) |
      | `name`    | Diabaikan                                 |
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

Lapisan kompatibilitas mempertahankan format error yang konsisten dengan OpenAI API. Namun, pesan error terperinci tidak akan setara. Hanya gunakan pesan error untuk logging dan debugging.

### Kompatibilitas header

Meskipun OpenAI SDK secara otomatis mengelola header, berikut adalah daftar lengkap header yang didukung oleh Claude API untuk developer yang perlu bekerja dengannya secara langsung.

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
