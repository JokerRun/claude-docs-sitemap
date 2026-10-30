---
source: platform
url: https://platform.claude.com/docs/id/api/opentelemetry/spans
fetched_at: 2026-10-30T02:15:26.914079Z
sha256: 4d23fb4b722786a4c08fc7b6e871ed7a0b92113f08da4edc2af94cde1d96f59c
---

---
title: Referensi span OpenTelemetry
url: https://platform.claude.com/docs/id/api/opentelemetry/spans
description: Span OpenTelemetry dan atribut span yang dipancarkan oleh Claude API dan Claude SDK.
featureMetadata:
  topic:
    title: OpenTelemetry
    url: https://platform.claude.com/docs/en/manage-claude/opentelemetry
  status: beta
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: beta
    Claude Platform on AWS: beta
    Claude Models on Google Cloud (Anthropic managed): beta
    Amazon Bedrock: beta
    Amazon Bedrock (InvokeModel): beta
    Claude Models on Google Cloud (Google managed): beta
    Microsoft Foundry: beta
---

<Note>
  Ekspor OpenTelemetry sedang dalam tahap beta. Fitur ini disediakan berdasarkan perjanjian Anda dengan Anthropic, termasuk bagian Layanan Beta dari [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Nama span dan atribut dapat berubah selama masa beta.
</Note>

Untuk mendapatkan span, lihat [Menyiapkan OpenTelemetry dengan Claude SDK](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk) dan [Menyiapkan OpenTelemetry dengan Claude API](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api).

## Nama dan jenis span

| Properti              | Span SDK                                                                                                                              | Span API                                                             |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `service.name`        | `service.name` dari aplikasi                                                                                                          | `claude-platform`                                                    |
| Cakupan instrumentasi | `com.anthropic.sdk.<language>` atau `com.anthropic.sdk.cli`, ditambah `.<platform>` pada klien platform cloud, beserta versi paketnya | `com.anthropic.claude-platform`                                      |
| Jenis span            | `CLIENT` pada span untuk sebuah permintaan, `INTERNAL` untuk lainnya                                                                  | `SERVER` pada span untuk sebuah permintaan, `INTERNAL` untuk lainnya |

* **Span untuk permintaan** memiliki nama metode API dari permintaan tersebut: `anthropic.` diikuti oleh path metode dalam referensi API, dengan titik sebagai pengganti garis miring dan tanpa `beta`. Misalnya, `client.beta.sessions.events.send()` (csharp, go: `client.Beta.Sessions.Events.Send()`; java: `client.beta().sessions().events().send()`; php: `$client->beta->sessions->events->send()`; ruby: `client.beta.sessions.events.send_()`) mengirim permintaan untuk [mengirim event sesi](https://platform.claude.com/docs/id/api/beta/sessions/events/send), dan span-nya memiliki nama [`anthropic.sessions.events.send`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-sessions-events-send).
* **Span alat** memiliki nama tetap, sebuah spasi, dan nama alat, misalnya [`anthropic.tool_use bash`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use).

## Status span

* **`OK`:** Langkah selesai.
* **`ERROR`:** Langkah gagal.
* **Tidak diatur (unset):** Aplikasi membatalkan langkah tersebut, misalnya ketika aplikasi mengirim event [`user.interrupt`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_user_interrupt_event).

Span dari sebuah stream berakhir ketika stream berakhir. Jika aplikasi menutup stream lebih awal, span SDK memiliki status tidak diatur, sehingga span SDK dari stream yang tidak pernah selesai, seperti [`anthropic.sessions.events.stream`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-sessions-method), memiliki status tidak diatur atau `ERROR`.

## Atribut

Atribut menggunakan [konvensi semantik OpenTelemetry untuk AI generatif](https://github.com/open-telemetry/semantic-conventions-genai) (`gen_ai.*`) jika tersedia. Atribut Anthropic diawali dengan `anthropic.`. Span mengikuti konvensi pada commit [`e57c543b`](https://github.com/open-telemetry/semantic-conventions-genai/tree/e57c543b4889619eb2a05702471937db5119165d) tanggal 24 September 2026. Konvensi tersebut masih dalam pengembangan.

### Atribut umum

Setiap span untuk sebuah permintaan memiliki atribut berikut, kecuali jika deskripsinya menyatakan lain. Span lain hanya dapat memiliki tiga atribut pertama:

| Atribut                     | Tipe     | Deskripsi                                                                                                                                                                    |
| --------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gen_ai.provider.name`      | `string` | `anthropic`. Ada di setiap span.<br />**SDK:** `aws.bedrock` pada klien Amazon Bedrock (termasuk Mantle) dan `gcp.vertex_ai` pada klien untuk Google Cloud’s Agent Platform. |
| `anthropic.organization.id` | `string` | ID organisasi.                                                                                                                                                               |
| `anthropic.workspace.id`    | `string` | ID workspace tempat pekerjaan dijalankan.                                                                                                                                    |
| `anthropic.request.id`      | `string` | Nilai header respons `request-id`.                                                                                                                                           |
| `http.request.method`       | `string` | Metode HTTP dari permintaan, misalnya `POST`.                                                                                                                                |
| `http.route`                | `string` | Path dari endpoint, dengan placeholder untuk parameter path-nya, misalnya `/v1/sessions/{session_id}`.                                                                       |
| `http.response.status_code` | `int`    | Kode status HTTP dari respons akhir. Untuk stream, kode status yang dikirim bersama header. Tidak ada jika tidak ada respons.                                                |
| `server.address`            | `string` | Host tujuan pengiriman permintaan, misalnya `api.anthropic.com`.                                                                                                             |
| `server.port`               | `int`    | Port dari URL permintaan, atau port default dari skemanya ketika URL tidak memilikinya.                                                                                      |
| `url.scheme`                | `string` | Skema dari URL, misalnya `https`.                                                                                                                                            |
| `url.path`                  | `string` | Path dari URL, misalnya `/v1/messages`.                                                                                                                                      |
| `url.query`                 | `string` | Query string dari URL, hanya berisi parameter query yang didefinisikan oleh endpoint. Tidak disertakan ketika tidak ada parameter tersebut.                                  |
| `url.full`                  | `string` | URL permintaan.                                                                                                                                                              |

Span API untuk permintaan yang dikirim melalui platform cloud, seperti Claude Platform on AWS, tidak memiliki `server.address`, `server.port`, atau `url.full`.

### Atribut sesi

Dalam sesi Managed Agents, span memiliki atribut berikut. Span dari sebuah sesi dapat berada di lebih dari satu trace, jadi untuk menyusun tampilan sesi, seperti transkrip, [kelompokkan span-nya berdasarkan ID ini](https://platform.claude.com/docs/id/manage-claude/opentelemetry#a-managed-agents-session).

| Atribut                  | Tipe     | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `anthropic.session.id`   | `string` | ID sesi. Tidak ada pada span dari metode yang tidak bekerja pada satu sesi, seperti [`anthropic.sessions.list`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-sessions-method).                                                                                                                                                                                                                                                                                |
| `gen_ai.conversation.id` | `string` | ID thread sesi tempat span berada. [Opsi `conversation_id` (typescript, java, php: `conversationId`; csharp: `ConversationId`; go: `option.WithOpenTelemetryConversationID()`)](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#configure-the-sdk) SDK menggantinya dengan ID percakapan Anda sendiri. Tidak ada pada span SDK tanpa thread kecuali Anda mengatur opsi tersebut, dan pada span API untuk permintaan Sessions API selain permintaan ke satu thread. |

### Atribut konten

Atribut yang ditandai dengan <Badge>Content</Badge> hanya ada pada span dalam mode konten, baik dari SDK maupun API. Lihat [perbedaan mode konten dalam panduan](https://platform.claude.com/docs/id/manage-claude/opentelemetry#choose-a-content-mode). Ketika konten ini terlalu besar, SDK dan API memperpendeknya agar sesuai dengan [batas konten](https://platform.claude.com/docs/id/manage-claude/opentelemetry#content-limits) dan mengatur `anthropic.content.truncated` ke `true`. Jika pengamanan Anthropic menahan konten dari respons, span API juga tidak menyertakannya.

Atribut pesan adalah string JSON dalam format pesan dari konvensi GenAI OpenTelemetry. Setiap blok konten Anthropic menjadi satu bagian pesan konvensi GenAI, pada Messages API dan dalam event pesan Managed Agents seperti `agent.message`:

| Blok konten Anthropic                                                                          | Bagian pesan konvensi GenAI                                                                                                                               |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text`                                                                                         | `text`                                                                                                                                                    |
| `tool_use`, `server_tool_use`                                                                  | `tool_call`, dengan `anthropic_toolset_name` untuk blok `tool_use` yang memiliki `toolset_name`, seperti `computer`                                       |
| `mcp_tool_use`                                                                                 | `tool_call` dengan `anthropic_mcp_server_name`                                                                                                            |
| `tool_result`, `mcp_tool_result`, blok hasil dari alat server seperti `web_search_tool_result` | `tool_call_response`                                                                                                                                      |
| `thinking`                                                                                     | `reasoning`, tanpa signature dari blok `thinking`. Tidak ada dalam span Managed Agents, karena event `agent.thinking` tidak menyertakan konten pemikiran. |
| Blok lainnya, seperti `image`                                                                  | `type` dari blok tersebut dengan awalan `anthropic_`, seperti `anthropic_image`. Bagian tersebut tidak memiliki field lain.                               |

Setiap event penggunaan alat atau hasil alat Managed Agents juga menjadi satu bagian pesan konvensi GenAI:

| Event Managed Agents                                                                        | Bagian pesan konvensi GenAI                    |
| ------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| `agent.tool_use`, `agent.custom_tool_use`                                                   | `tool_call`                                    |
| `agent.mcp_tool_use`                                                                        | `tool_call` dengan `anthropic_mcp_server_name` |
| `user.tool_result`, `user.custom_tool_result`, `agent.tool_result`, `agent.mcp_tool_result` | `tool_call_response`                           |

### Penggunaan token

Span berikut memiliki atribut penggunaan token: [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create), [`anthropic.model_request`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-model-request), [`anthropic.compaction`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-compaction), dan [`anthropic.session.outcome_evaluation`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-outcome-evaluation). Nilainya adalah untuk langkah dari span tersebut, misalnya permintaan, permintaan model, atau compaction. Pada span API untuk permintaan Messages API, jumlah token adalah token yang ditagihkan kepada organisasi Anda, bahkan ketika permintaan gagal atau aplikasi membatalkannya. Span `anthropic.messages.create` dari SDK justru memiliki jumlah yang dilaporkan oleh respons, sehingga untuk permintaan yang gagal atau dibatalkan, jumlahnya bisa lebih rendah daripada pada span API, atau tidak ada. Untuk menghitung setiap token satu kali, lihat [cara menghitung token dalam panduan](https://platform.claude.com/docs/id/manage-claude/opentelemetry#count-tokens).

| Atribut                                                    | Tipe  | Deskripsi                                                                                                                                                                                            |
| ---------------------------------------------------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gen_ai.usage.input_tokens`                                | `int` | Token input, termasuk pembacaan dan penulisan cache.                                                                                                                                                 |
| `gen_ai.usage.output_tokens`                               | `int` | Token output.                                                                                                                                                                                        |
| `gen_ai.usage.cache_write.input_tokens`                    | `int` | Token yang ditulis ke cache prompt. Tidak ada pada span [`anthropic.session.outcome_evaluation`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-outcome-evaluation).  |
| `anthropic.usage.cache_creation.ephemeral_5m_input_tokens` | `int` | Token yang ditulis ke cache 5 menit. Hanya pada span untuk permintaan Messages API. Pada span SDK dari respons streaming, hanya token yang ditulis sebelum token output pertama.                     |
| `anthropic.usage.cache_creation.ephemeral_1h_input_tokens` | `int` | Token yang ditulis ke cache 1 jam. Hanya pada span untuk permintaan Messages API. Pada span SDK dari respons streaming, hanya token yang ditulis sebelum token output pertama.                       |
| `gen_ai.usage.cache_read.input_tokens`                     | `int` | Token yang dibaca dari cache prompt. Tidak ada pada span [`anthropic.session.outcome_evaluation`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-outcome-evaluation). |

## Span

Sebuah span dapat berasal dari SDK di aplikasi atau dari API, sehingga setiap span dalam referensi ini mencantumkan sumbernya. Deskripsi yang diawali dengan **Messages API:** atau **Managed Agents:** berlaku untuk span dari produk tersebut. Deskripsi atribut yang diawali dengan sumber, seperti **SDK:** atau **API:**, berlaku untuk span dari sumber tersebut.

### `anthropic.messages.create`

* **Sumber:** SDK dan API.
* **Jenis:** `CLIENT` dari SDK, `SERVER` dari API.
* **Induk dari span SDK:** Span yang sedang aktif di aplikasi ketika aplikasi memanggil metode tersebut. Jika tidak ada span yang aktif, tidak ada induk.
* **Induk dari span API:** Span dalam header `traceparent` dari permintaan, yang merupakan span SDK ketika permintaan berasal dari SDK. Tanpa header tersebut, span API tidak memiliki induk. Lihat [cara mengirim header `traceparent`](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#connect-api-spans-to-your-own-traces).
* **Anak dari span SDK:** Span API untuk permintaan tersebut.
* **Anak dari span API:** Span [`anthropic.model_request`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-model-request) untuk setiap permintaan model, [span alat](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use) untuk setiap penggunaan alat server atau alat MCP connector yang dijalankan API dalam permintaan tersebut, dan span [`anthropic.compaction`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-compaction) untuk setiap compaction.

SDK memancarkan span ini untuk setiap permintaan Messages, baik di-stream maupun tidak.

API memancarkan span ini untuk setiap permintaan [`POST /v1/messages`](https://platform.claude.com/docs/id/api/messages/create) yang diautentikasinya. API tidak memancarkan span untuk permintaan ke [endpoint yang kompatibel dengan OpenAI](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk), `POST /v1/chat/completions`.

API memancarkan satu span untuk sebuah permintaan, bahkan ketika [model fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) melayaninya.

Span ini memiliki [atribut penggunaan token](https://platform.claude.com/docs/id/api/opentelemetry/spans#token-usage). Span SDK juga memiliki atribut dari setiap [span SDK untuk permintaan](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-resources-method).

| Atribut                                    | Tipe       | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gen_ai.operation.name`                    | `string`   | `chat`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `gen_ai.request.model`                     | `string`   | [`model`](https://platform.claude.com/docs/id/api/messages/create#create.model) dari permintaan.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `gen_ai.response.id`                       | `string`   | [`id`](https://platform.claude.com/docs/id/api/messages/create#message) dari respons.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `gen_ai.response.model`                    | `string`   | Model yang melayani permintaan. Berbeda dari model yang diminta ketika permintaan menggunakan alias model, atau ketika [model fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) melayani permintaan.                                                                                                                                                                                                                                                                                                                                         |
| `anthropic.message.stop_reason`            | `string`   | [`stop_reason`](https://platform.claude.com/docs/id/api/messages#stop_reason) dari respons, misalnya `end_turn`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `anthropic.response.service_tier`          | `string`   | Tingkat layanan yang melayani permintaan: [`usage.service_tier`](https://platform.claude.com/docs/id/api/messages#usage) dari respons. Lihat [bagaimana permintaan ditetapkan ke tingkat layanan](https://platform.claude.com/docs/id/api/service-tiers#how-requests-get-assigned-tiers).                                                                                                                                                                                                                                                                                         |
| `error.type`                               | `string`   | [Tipe error](https://platform.claude.com/docs/id/api/errors#http-errors) dari permintaan yang gagal, misalnya `rate_limit_error`.<br />**SDK:** Juga nilai-nilai lain dalam [span SDK untuk permintaan](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-resources-method).<br />**API:** `api_error` ketika API mengakhiri permintaan tanpa respons error.                                                                                                                                                                                                  |
| `gen_ai.response.time_to_first_chunk`      | `double`   | Hanya pada span dari respons streaming. Jumlah detik hingga event `content_block_delta` pertama dari stream, jika ada.                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `gen_ai.usage.reasoning.output_tokens`     | `int`      | Token thinking, yang merupakan bagian dari token output. Tidak ada jika token thinking tidak dihitung terpisah dari token output lainnya, misalnya pada model yang responsnya tidak memiliki rincian untuk token output.                                                                                                                                                                                                                                                                                                                                                          |
| `anthropic.usage.compaction.input_tokens`  | `int`      | Token input dari [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) permintaan, termasuk pembacaan dan penulisan cache. Bukan bagian dari `gen_ai.usage.input_tokens`. Tidak ada jika permintaan tidak memiliki compaction.                                                                                                                                                                                                                                                                                                                           |
| `anthropic.usage.compaction.output_tokens` | `int`      | Token output dari compaction permintaan. Bukan bagian dari `gen_ai.usage.output_tokens`. Tidak ada jika permintaan tidak memiliki compaction.                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `gen_ai.request.max_tokens`                | `int`      | [`max_tokens`](https://platform.claude.com/docs/id/api/messages/create#create.max_tokens) dari permintaan.                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `gen_ai.request.temperature`               | `double`   | [`temperature`](https://platform.claude.com/docs/id/api/messages/create?version=2023-06-01#create.temperature) dari permintaan. Tidak ada jika permintaan tidak mengaturnya.                                                                                                                                                                                                                                                                                                                                                                                                      |
| `gen_ai.request.top_p`                     | `double`   | [`top_p`](https://platform.claude.com/docs/id/api/messages/create?version=2023-06-01#create.top_p) dari permintaan. Tidak ada jika permintaan tidak mengaturnya.                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `gen_ai.request.top_k`                     | `int`      | [`top_k`](https://platform.claude.com/docs/id/api/messages/create?version=2023-06-01#create.top_k) dari permintaan. Tidak ada jika permintaan tidak mengaturnya.                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `gen_ai.request.stream`                    | `boolean`  | `true` ketika permintaan mengatur [`stream: true`](https://platform.claude.com/docs/id/api/messages/create#create.stream). Tidak ada jika sebaliknya.                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `gen_ai.request.reasoning.level`           | `string`   | [`effort`](https://platform.claude.com/docs/id/api/messages/create#create.output_config.effort) dalam [`output_config`](https://platform.claude.com/docs/id/api/messages/create#create.output_config) dari permintaan. Tidak ada jika permintaan tidak mengaturnya.                                                                                                                                                                                                                                                                                                               |
| `gen_ai.output.type`                       | `string`   | `json` ketika permintaan mengatur format output ke JSON. Tidak ada jika sebaliknya.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `anthropic.request.service_tier`           | `string`   | [`service_tier`](https://platform.claude.com/docs/id/api/messages/create#create.service_tier) dari permintaan. Tidak ada jika permintaan tidak mengaturnya.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `anthropic.thinking.type`                  | `string`   | [`thinking.type`](https://platform.claude.com/docs/id/api/messages/create#create.thinking) dari permintaan. Tidak ada jika permintaan tidak mengaturnya.                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `anthropic.thinking.budget_tokens`         | `int`      | [`budget_tokens`](https://platform.claude.com/docs/id/api/messages#thinking_config_enabled.budget_tokens) dalam objek [`thinking`](https://platform.claude.com/docs/id/api/messages/create#create.thinking) dari permintaan. Tidak ada jika permintaan tidak mengaturnya.                                                                                                                                                                                                                                                                                                         |
| `anthropic.beta`                           | `string[]` | Nama-nama beta dalam header [`anthropic-beta`](https://platform.claude.com/docs/id/api/beta/messages/create#create.betas) dari permintaan.                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `gen_ai.system_instructions`               | `string`   | <Badge>Content</Badge> String JSON yang mengikuti skema OpenTelemetry [`SystemInstructions`](https://github.com/open-telemetry/semantic-conventions-genai/blob/e57c543b4889619eb2a05702471937db5119165d/model/gen-ai/gen-ai-system-instructions.json). Prompt [`system`](https://platform.claude.com/docs/id/api/messages/create#create.system) dari permintaan.                                                                                                                                                                                                                  |
| `gen_ai.input.messages`                    | `string`   | <Badge>Content</Badge> String JSON yang mengikuti skema OpenTelemetry [`InputMessages`](https://github.com/open-telemetry/semantic-conventions-genai/blob/e57c543b4889619eb2a05702471937db5119165d/model/gen-ai/gen-ai-input-messages.json). [`messages`](https://platform.claude.com/docs/id/api/messages/create#create.messages) dari permintaan.                                                                                                                                                                                                                               |
| `gen_ai.output.messages`                   | `string`   | <Badge>Content</Badge> String JSON yang mengikuti skema OpenTelemetry [`OutputMessages`](https://github.com/open-telemetry/semantic-conventions-genai/blob/e57c543b4889619eb2a05702471937db5119165d/model/gen-ai/gen-ai-output-messages.json). [`content`](https://platform.claude.com/docs/id/api/messages/create#message) dari respons, sebagai satu pesan `assistant`.<br />**SDK:** Pada stream, hanya ketika aplikasi membaca stream seperti yang dijelaskan dalam [Penelusuran stream](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#trace-a-stream). |
| `gen_ai.request.stop_sequences`            | `string[]` | <Badge>Content</Badge> [`stop_sequences`](https://platform.claude.com/docs/id/api/messages/create#create.stop_sequences) dari permintaan.                                                                                                                                                                                                                                                                                                                                                                                                                                         |

Span untuk sebuah permintaan tidak memiliki jumlah penggunaan alat server dari respons, seperti `web_search_requests`. Sebagai gantinya, API memancarkan [span alat](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use) untuk setiap penggunaan alat server.

### `anthropic.messages.count_tokens`

* **Sumber:** SDK. API tidak memancarkan span untuk [`POST /v1/messages/count_tokens`](https://platform.claude.com/docs/id/api/messages/count_tokens).
* **Jenis:** `CLIENT`.
* **Induk:** Span yang sedang aktif di aplikasi ketika aplikasi memanggil metode tersebut, atau tidak ada jika tidak ada span yang aktif.
* **Anak:** Tidak ada.

| Atribut                                       | Tipe     | Deskripsi                                                                                                         |
| --------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| `gen_ai.request.model`                        | `string` | Model dari permintaan.                                                                                            |
| `anthropic.message.count_tokens.input_tokens` | `int`    | Jumlah token dalam respons. Jumlah ini bukan penggunaan. Jangan sertakan saat Anda menjumlahkan penggunaan token. |

### `anthropic.sessions.create`

Sama seperti [`anthropic.sessions.<method>`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-sessions-method), kecuali untuk anak dan atribut berikut:

* **Anak dari span SDK:** Span API untuk permintaan tersebut.
* **Anak dari span API:** Span [`anthropic.session.turn`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-turn) dari giliran pertama, ketika permintaan memiliki [`initial_events`](https://platform.claude.com/docs/id/api/beta/sessions/create#create.initial_events) yang tidak kosong.

| Atribut                            | Tipe     | Deskripsi                                                                                               |
| ---------------------------------- | -------- | ------------------------------------------------------------------------------------------------------- |
| `gen_ai.agent.id`                  | `string` | ID agen yang menjadi dasar pembuatan sesi.                                                              |
| `gen_ai.agent.name`                | `string` | Nama agen tersebut.<br />**SDK:** Tidak ada jika permintaan gagal.                                      |
| `gen_ai.request.model`             | `string` | Model dari agen tersebut, yang menjalankan thread utama.<br />**SDK:** Tidak ada jika permintaan gagal. |
| `anthropic.session.environment.id` | `string` | ID environment dari sesi.                                                                               |

### `anthropic.sessions.events.send`

Sama seperti [`anthropic.sessions.<method>`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-sessions-method), kecuali untuk anak dari span API.

* **Anak dari span SDK:** Span API untuk permintaan tersebut.
* **Anak dari span API:** Span [`anthropic.session.turn`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-turn) dari setiap giliran yang dimulai karena event dari permintaan tersebut.

### `anthropic.sessions.update`

Sama seperti [`anthropic.sessions.<method>`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-sessions-method), kecuali untuk anak dari span API.

* **Anak dari span SDK:** Span API untuk permintaan tersebut.
* **Anak dari span API:** Span [`anthropic.session.turn`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-turn) dari setiap giliran yang dilanjutkan karena permintaan menaikkan atau menghapus [anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets#resume-a-session-at-its-budget).

### `anthropic.session.turn`

* **Sumber:** API, untuk sesi Managed Agents.

* **Jenis:** `INTERNAL`.

* **Induk:** Bergantung pada alasan giliran dimulai:

  * Span [`anthropic.sessions.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-sessions-create), untuk giliran pertama dari sesi yang dibuat dengan [`initial_events`](https://platform.claude.com/docs/id/api/beta/sessions/create#create.initial_events) yang tidak kosong.
  * Span [`anthropic.sessions.events.send`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-sessions-events-send) untuk permintaan tempat event dikirim, untuk giliran yang dimulai karena sebuah event, misalnya event [`user.message`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_user_message_event).
  * Span [`anthropic.sessions.update`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-sessions-update), untuk giliran yang dilanjutkan karena permintaan tersebut menaikkan atau menghapus anggaran sesi.
  * Span `anthropic.session.turn` dari giliran [agen yang dijalankan oleh sesi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) yang selama giliran tersebut agen itu memulai giliran ini, untuk giliran pada thread lain.
  * Span `anthropic.session.turn` dari giliran yang menghasilkan balasan tersebut, untuk giliran yang dimulai karena agen pada thread lain membalas, seperti agen yang dipanggil oleh agen utama.
  * Tidak ada, untuk giliran lain mana pun, seperti giliran yang dimulai karena [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs) berakhir.

* **Anak:**

  * Span [`anthropic.model_request`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-model-request) untuk setiap permintaan model dalam giliran.
  * Span alat setiap kali API menjalankan alat dalam giliran, kecuali dalam [kasus yang tercantum di bagian span alat](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use).
  * Span `anthropic.session.turn` untuk setiap giliran pada thread lain yang dimulai selama giliran ini oleh agen yang dijalankan oleh sesi, atau oleh balasan dari giliran ini.
  * Span [`anthropic.session.outcome_evaluation`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-outcome-evaluation) untuk setiap iterasi evaluasi hasil yang dimulai oleh giliran ini.

Sebuah giliran dimulai ketika thread-nya memasuki status `running` dan berakhir ketika thread meninggalkan status tersebut.

| Atribut                              | Tipe     | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gen_ai.operation.name`              | `string` | `invoke_agent`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `gen_ai.agent.id`                    | `string` | ID agen yang menjalankan thread dari giliran tersebut. Tidak ada pada thread [advisor](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#advisor-threads).                                                                                                                                                                                                                                                                                                                              |
| `gen_ai.agent.name`                  | `string` | Nama agen tersebut. `anthropic.advisor` pada thread advisor.                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `gen_ai.request.model`               | `string` | Model dari agen tersebut. Pada thread advisor, model dari advisor.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `anthropic.session.turn.stop_reason` | `string` | Alasan giliran berakhir: [`stop_reason.type`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_session_thread_status_idle_event) dari event [`session.thread_status_idle`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_session_thread_status_idle_event), misalnya `requires_action`. Tidak ada jika thread tidak menjadi idle.                                                                                                              |
| `error.type`                         | `string` | [`error.type`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_session_error_event) dari event [`session.error`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_session_error_event) yang mengakhiri giliran, jika giliran gagal.                                                                                                                                                                                                              |
| `gen_ai.agent.description`           | `string` | Deskripsi agen tersebut. Tidak ada pada thread advisor atau ketika agen tidak memilikinya.                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `gen_ai.system_instructions`         | `string` | <Badge>Content</Badge> String JSON yang mengikuti skema OpenTelemetry [`SystemInstructions`](https://github.com/open-telemetry/semantic-conventions-genai/blob/e57c543b4889619eb2a05702471937db5119165d/model/gen-ai/gen-ai-system-instructions.json). Prompt sistem yang berlaku untuk giliran tersebut. Hanya ada pada giliran pertama sebuah thread. Tidak ada pada thread advisor.                                                                                                                            |
| `gen_ai.input.messages`              | `string` | <Badge>Content</Badge> String JSON yang mengikuti skema OpenTelemetry [`InputMessages`](https://github.com/open-telemetry/semantic-conventions-genai/blob/e57c543b4889619eb2a05702471937db5119165d/model/gen-ai/gen-ai-input-messages.json). Event input dari giliran tersebut: pesan pengguna dan hasil alat, event [`system.message`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_system_message_event_params), dan pesan dari thread lain. Tidak ada pada thread advisor. |
| `gen_ai.output.messages`             | `string` | <Badge>Content</Badge> String JSON yang mengikuti skema OpenTelemetry [`OutputMessages`](https://github.com/open-telemetry/semantic-conventions-genai/blob/e57c543b4889619eb2a05702471937db5119165d/model/gen-ai/gen-ai-output-messages.json). Event output dari giliran tersebut: pesan, penggunaan alat, dan hasil alat dari agen.                                                                                                                                                                              |

### `anthropic.model_request`

* **Sumber:** API, untuk permintaan Messages API dan sesi Managed Agents.

* **Jenis:** `INTERNAL`.

* **Induk:**

  * **Messages API:** Span [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create) untuk permintaan.
  * **Managed Agents:** Span [`anthropic.session.turn`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-turn) dari giliran yang membuat permintaan.

* **Anak:** Tidak ada.

Pada Messages API, setiap span adalah satu permintaan model dalam permintaan API.

Span ini memiliki [atribut penggunaan token](https://platform.claude.com/docs/id/api/opentelemetry/spans#token-usage).

| Atribut                 | Tipe     | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ----------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gen_ai.operation.name` | `string` | Hanya pada span dari sesi Managed Agents, dengan nilai `chat`. Pada Messages API, span [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create) untuk permintaan adalah operasi `chat`.                                                                                                                                                                                       |
| `gen_ai.request.model`  | `string` | Model dari permintaan.                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `gen_ai.response.model` | `string` | Hanya pada span untuk permintaan Messages API. Model yang menjalankan permintaan model.                                                                                                                                                                                                                                                                                                                                                   |
| `error.type`            | `string` | **Messages API:** `error.type` dari span [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create), jika permintaan gagal selama permintaan model ini.<br />**Managed Agents:** Jika permintaan model gagal, [tipe error](https://platform.claude.com/docs/id/api/errors#http-errors)-nya, misalnya `rate_limit_error`. `api_error` jika permintaan model gagal tanpa respons. |

### `anthropic.tool_use`, `anthropic.mcp_tool_use`, dan `anthropic.custom_tool_use`

* **Sumber:** SDK dan API.

* **Nama:** `anthropic.tool_use <tool>`, `anthropic.mcp_tool_use <tool>`, atau `anthropic.custom_tool_use <tool>`, dengan `<tool>` adalah nama alat.

* **Jenis:** `INTERNAL`.

* **Induk dari span SDK:** Span yang sedang aktif di aplikasi ketika alat dimulai, yang dalam Messages tool runner adalah span [`anthropic.messages.tool_runner`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-tool-runner). Jika tidak ada span yang aktif, tidak ada induk.

* **Induk dari span API:**

  * **Messages API:** Span [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create) untuk permintaan tempat API menjalankan alat tersebut.
  * **Managed Agents:** Span [`anthropic.session.turn`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-turn) dari giliran tempat alat dijalankan. Untuk penggunaan alat yang menunggu event [`user.tool_confirmation`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_user_tool_confirmation_event), itu adalah giliran yang dimulai karena konfirmasi tersebut.
  * Untuk penggunaan alat dari kode yang dijalankan oleh alat lain, span alat dari alat tersebut. Pada Messages API, alat tersebut adalah [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool).

* **Anak dari span SDK:** Span yang dimulai oleh kode alat tersebut.

* **Anak dari span API:** Span alat untuk setiap penggunaan alat dari kode yang dijalankan oleh alat ini. Misalnya, kode yang dijalankan oleh alat eksekusi kode mungkin menggunakan `web_search`.

Awalan nama span bergantung pada jenis alat:

* `anthropic.tool_use <tool>` adalah span dari setiap penggunaan [alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools) pada Messages API atau alat dari toolset agen Managed Agents. API menjalankan alat-alat toolset agen, kecuali dalam [sandbox yang di-host sendiri](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#trace-a-self-hosted-sandbox), tempat environment worker menjalankannya.
* `anthropic.mcp_tool_use <tool>` adalah span dari setiap penggunaan alat MCP, di SDK, pada Messages API, dan pada Managed Agents. Di SDK, ini adalah alat dari helper MCP yang dijalankan oleh [Messages tool runner](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner) atau [session tool runner](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#session-tool-runner). Pada Messages API, alat berasal dari [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector). Pada Managed Agents, jika [koneksi ke server MCP gagal](https://platform.claude.com/docs/id/managed-agents/mcp-connector#handle-connection-and-authentication-failures), nama span tidak menyertakan nama alat.
* `anthropic.custom_tool_use <tool>` adalah span dari setiap penggunaan alat yang didefinisikan oleh aplikasi dan dijalankan oleh tool runner. Hanya SDK yang memancarkan span ini.

API tidak memancarkan span alat dalam kasus berikut:

* Model meminta untuk menggunakan alat yang dijalankan oleh aplikasi, seperti [alat kustom](https://platform.claude.com/docs/id/managed-agents/tools). Jika tool runner di SDK menjalankan alat tersebut, tool runner yang memancarkan span-nya.
* **Managed Agents:** Agen menggunakan alat yang berjalan di sandbox yang di-host sendiri. Worker di SDK, yang menjalankan alat tersebut, memancarkan span-nya. Lihat [cara melacak sandbox yang di-host sendiri](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#trace-a-self-hosted-sandbox).
* **Managed Agents:** Agen menggunakan alat [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) atau [alat advisor](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor).
* **Managed Agents:** Agen meminta untuk menggunakan alat, tetapi server menolak penggunaan tersebut berdasarkan [kebijakan izin `auto`](https://platform.claude.com/docs/id/managed-agents/permission-policies#let-the-server-evaluate-each-call-with-auto), atau aplikasi menolaknya dalam event [`user.tool_confirmation`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_user_tool_confirmation_event).

| Atribut                               | Tipe     | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gen_ai.operation.name`               | `string` | `execute_tool`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `gen_ai.tool.name`                    | `string` | Nama alat, misalnya `bash`. Pada span API, nama alat MCP tidak menyertakan nama server. Pada Managed Agents, jika koneksi ke server MCP gagal, nilainya adalah nama yang dihasilkan model dan hanya ada pada span dalam mode konten.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `gen_ai.tool.call.id`                 | `string` | **Messages API:** `id` dari blok tempat model meminta untuk menggunakan alat: blok [`tool_use`](https://platform.claude.com/docs/id/api/messages#tool_use_block), [`server_tool_use`](https://platform.claude.com/docs/id/api/messages#server_tool_use_block), atau [`mcp_tool_use`](https://platform.claude.com/docs/id/api/beta/messages#beta_mcp_tool_use_block).<br />**Managed Agents:** ID event tempat agen meminta untuk menggunakan alat: event [`agent.tool_use`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_agent_tool_use_event), [`agent.mcp_tool_use`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_agent_mcp_tool_use_event), atau [`agent.custom_tool_use`](https://platform.claude.com/docs/id/api/beta/sessions/events#beta_managed_agents_agent_custom_tool_use_event). |
| `anthropic.mcp.server.name`           | `string` | Hanya pada span API dari alat MCP. Nama server MCP dari alat tersebut. Pada Messages API, [`server_name`](https://platform.claude.com/docs/id/api/beta/messages#beta_mcp_tool_use_block.server_name) dari blok [`mcp_tool_use`](https://platform.claude.com/docs/id/api/beta/messages#beta_mcp_tool_use_block).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `gen_ai.conversation.id`              | `string` | ID thread sesi, seperti yang dijelaskan dalam [Atribut sesi](https://platform.claude.com/docs/id/api/opentelemetry/spans#session-attributes). Dalam Messages tool runner, ID percakapan yang diteruskan dengan [opsi `conversation_id` (typescript, java, php: `conversationId`; csharp: `ConversationId`; go: `option.WithOpenTelemetryConversationID()`)](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#configure-the-sdk), dan tidak ada jika tidak diteruskan. Tidak ada pada span API untuk permintaan Messages API.                                                                                                                                                                                                                                                                                                                      |
| `anthropic.session.id`                | `string` | ID sesi. Tidak ada untuk penggunaan alat di luar sesi Managed Agents, seperti pada Messages API atau dalam Messages tool runner.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `anthropic.session.thread.id`         | `string` | Hanya pada span SDK dari session tool runner. ID thread sesi. Tidak ada untuk penggunaan alat pada thread utama.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `anthropic.tool.evaluated_permission` | `string` | Hanya pada span yang dipancarkan API dalam sesi Managed Agents. Hasil evaluasi [kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) untuk penggunaan alat: `allow` atau `ask`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `error.type`                          | `string` | Tipe error, jika penggunaan alat gagal: `tool_error` ketika kode alat memunculkan error atau ketika alat mengembalikan hasil error.<br />**API:** Pada Messages API, hasil error dari alat server sebagai gantinya memiliki [`error_code`](https://platform.claude.com/docs/id/api/messages#web_search_tool_result_error.error_code)-nya, misalnya `max_uses_exceeded`. Pada Managed Agents, jika koneksi ke server MCP gagal, `mcp_authentication_failed_error` ketika autentikasi gagal, selain itu `mcp_connection_failed_error`. Jika permintaan gagal selama penggunaan alat, [tipe error](https://platform.claude.com/docs/id/api/errors#http-errors) dari permintaan tersebut.                                                                                                                                                                                |
| `gen_ai.tool.description`             | `string` | Hanya pada span SDK. Deskripsi dalam definisi alat. Tidak ada jika deskripsi kosong.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `gen_ai.tool.type`                    | `string` | Hanya pada span SDK. `function`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `gen_ai.tool.call.arguments`          | `string` | <Badge>Content</Badge> String JSON yang mengikuti skema OpenTelemetry [`ToolCallArguments`](https://github.com/open-telemetry/semantic-conventions-genai/blob/e57c543b4889619eb2a05702471937db5119165d/model/gen-ai/gen-ai-tool-call-arguments.json). [`input`](https://platform.claude.com/docs/id/api/messages#tool_use_block) dari penggunaan alat.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `anthropic.tool_result.content`       | `string` | <Badge>Content</Badge> String JSON dengan array blok konten. `content` dari hasil alat yang dikembalikan ke model. Juga untuk hasil error, kecuali pada Managed Agents ketika koneksi ke server MCP gagal. `content` berupa string menjadi array dengan satu blok [`text`](https://platform.claude.com/docs/id/api/messages#text_block).<br />**API:** Pada Messages API, `content` hasil alat server yang berupa satu objek, seperti `code_execution_result`, menjadi array dengan objek tersebut.                                                                                                                                                                                                                                                                                                                                                                  |

### `anthropic.compaction`

* **Sumber:** API, untuk permintaan Messages API.
* **Jenis:** `INTERNAL`.
* **Induk:** Span [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create) untuk permintaan tersebut.
* **Anak:** Tidak ada.

Span ini memiliki [atribut penggunaan token](https://platform.claude.com/docs/id/api/opentelemetry/spans#token-usage) dari compaction. Pada [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create), penggunaan dari sebuah compaction berada di atribut `anthropic.usage.compaction.*`, bukan di total `gen_ai.usage.*`.

| Atribut                 | Tipe     | Deskripsi                                                                                                                                                                                                                                        |
| ----------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `gen_ai.request.model`  | `string` | Model yang diminta untuk compaction, yaitu [`model`](https://platform.claude.com/docs/id/api/messages/create#create.model) dari permintaan.                                                                                                      |
| `gen_ai.response.model` | `string` | Model yang menjalankan compaction. Berbeda dari `gen_ai.request.model` ketika permintaan menggunakan alias model, atau ketika [model fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) melayani permintaan. |
| `error.type`            | `string` | [Jenis error](https://platform.claude.com/docs/id/api/errors#http-errors) dari permintaan, jika permintaan gagal selama compaction.                                                                                                              |

### `anthropic.session.outcome_evaluation`

* **Sumber:** API, untuk sesi Managed Agents.
* **Jenis:** `INTERNAL`.
* **Induk:** Span [`anthropic.session.turn`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-turn) dari giliran yang memulai iterasi, bahkan jika giliran tersebut berakhir sebelum iterasi.
* **Anak:** Tidak ada.

Status tidak diatur ketika hasilnya `interrupted` dan `OK` untuk hasil lainnya.

Span ini memiliki dua dari [atribut penggunaan token](https://platform.claude.com/docs/id/api/opentelemetry/spans#token-usage): `gen_ai.usage.input_tokens` dan `gen_ai.usage.output_tokens`.

| Atribut                                            | Tipe     | Deskripsi                                                                                                  |
| -------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------- |
| `anthropic.session.outcome.id`                     | `string` | ID dari outcome yang dievaluasi oleh iterasi.                                                              |
| `anthropic.session.outcome_evaluation.result`      | `string` | Hasil dari iterasi: `satisfied`, `needs_revision`, `max_iterations_reached`, `failed`, atau `interrupted`. |
| `anthropic.session.outcome_evaluation.iteration`   | `int`    | Nomor iterasi.                                                                                             |
| `anthropic.session.outcome_evaluation.explanation` | `string` | <Badge>Content</Badge> Penjelasan hasil dari grader, sebagai teks biasa.                                   |

### `anthropic.messages.tool_runner`

* **Sumber:** SDK.
* **Jenis:** `INTERNAL`.
* **Induk:** Span yang sedang aktif di aplikasi ketika loop dimulai, atau tidak ada jika tidak ada span yang aktif.
* **Anak:** Span [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create) untuk setiap permintaan dalam loop dan [span alat](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use) dari setiap penggunaan alat yang dijalankan oleh runner.

Span berakhir bersama loop. Jika aplikasi menghentikan runner, status tidak diatur. Jika kode sebuah alat memunculkan error, span alatnya memiliki status `ERROR` dan loop berlanjut. Span ini tidak memiliki atribut penggunaan, jadi bacalah penggunaan dari anak-anak [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create)-nya.

| Atribut                  | Tipe     | Deskripsi                                                                                                                                                                                                                                                                                                               |
| ------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gen_ai.operation.name`  | `string` | `invoke_agent`                                                                                                                                                                                                                                                                                                          |
| `gen_ai.request.model`   | `string` | Model dari permintaan pertama dalam loop.                                                                                                                                                                                                                                                                               |
| `gen_ai.conversation.id` | `string` | ID percakapan yang diteruskan dengan [opsi `conversation_id` (typescript, java, php: `conversationId`; csharp: `ConversationId`; go: `option.WithOpenTelemetryConversationID()`)](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#configure-the-sdk). Tidak ada jika opsi tersebut tidak diberikan. |
| `error.type`             | `string` | [Jenis error](https://platform.claude.com/docs/id/api/errors#http-errors) dari permintaan yang mengakhiri loop, jika loop gagal. `client_error` ketika runner itu sendiri gagal.                                                                                                                                        |
| `gen_ai.output.type`     | `string` | `json` ketika permintaan mengatur format output ke JSON. Tidak ada jika sebaliknya.                                                                                                                                                                                                                                     |

### `anthropic.messages.batches.<method>`

* **Sumber:** SDK, untuk setiap metode Message Batches.
* **Jenis:** `CLIENT`.
* **Induk:** Span yang sedang aktif di aplikasi ketika aplikasi memanggil metode, atau tidak ada jika tidak ada span yang aktif.
* **Anak:** Tidak ada.

Span ini juga memiliki atribut dari setiap [span SDK untuk sebuah permintaan](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-resources-method).

| Atribut                                 | Tipe     | Deskripsi                                                                                                                                   |
| --------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `anthropic.message.batch.id`            | `string` | ID dari batch yang ditangani oleh metode, atau untuk `create`, ID dari batch baru. Tidak ada pada `list` dan pada `create` yang gagal.      |
| `anthropic.message.batch.request_count` | `int`    | Hanya pada `create`. Jumlah item dalam array [`requests`](https://platform.claude.com/docs/id/api/messages/batches/create#create.requests). |

### `anthropic.sessions.<method>`

* **Sumber:** SDK dan API.
* **Jenis:** `CLIENT` dari SDK, `SERVER` dari API.
* **Induk dari span SDK:** Span yang sedang aktif di aplikasi ketika aplikasi memanggil metode, atau tidak ada jika tidak ada span yang aktif.
* **Induk dari span API:** Span dalam [header `traceparent`](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#connect-api-spans-to-your-own-traces) permintaan, yaitu span SDK ketika permintaan berasal dari SDK, atau tidak ada tanpa header tersebut.
* **Anak dari span SDK:** Span API untuk permintaan tersebut.
* **Anak dari span API:** Tidak ada.

API memancarkan span `anthropic.sessions.<method>` untuk setiap permintaan terautentikasi ke endpoint [Sessions API](https://platform.claude.com/docs/id/managed-agents/sessions). Permintaan yang dikirim platform atas nama pengguna, seperti pesan yang dikirim di Claude Console atau sesi yang dimulai oleh [scheduled deployment](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments), juga memiliki span, masing-masing dalam trace baru.

<Accordion title="Nama span dan endpoint">
  | Span                                       | Endpoint                                                                                                                                  |
  | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
  | `anthropic.sessions.create`                | [`POST /v1/sessions`](https://platform.claude.com/docs/id/api/beta/sessions/create)                                                       |
  | `anthropic.sessions.list`                  | [`GET /v1/sessions`](https://platform.claude.com/docs/id/api/beta/sessions/list)                                                          |
  | `anthropic.sessions.retrieve`              | [`GET /v1/sessions/{session_id}`](https://platform.claude.com/docs/id/api/beta/sessions/retrieve)                                         |
  | `anthropic.sessions.update`                | [`POST /v1/sessions/{session_id}`](https://platform.claude.com/docs/id/api/beta/sessions/update)                                          |
  | `anthropic.sessions.delete`                | [`DELETE /v1/sessions/{session_id}`](https://platform.claude.com/docs/id/api/beta/sessions/delete)                                        |
  | `anthropic.sessions.archive`               | [`POST /v1/sessions/{session_id}/archive`](https://platform.claude.com/docs/id/api/beta/sessions/archive)                                 |
  | `anthropic.sessions.events.send`           | [`POST /v1/sessions/{session_id}/events`](https://platform.claude.com/docs/id/api/beta/sessions/events/send)                              |
  | `anthropic.sessions.events.list`           | [`GET /v1/sessions/{session_id}/events`](https://platform.claude.com/docs/id/api/beta/sessions/events/list)                               |
  | `anthropic.sessions.events.stream`         | [`GET /v1/sessions/{session_id}/events/stream`](https://platform.claude.com/docs/id/api/beta/sessions/events/stream)                      |
  | `anthropic.sessions.resources.add`         | [`POST /v1/sessions/{session_id}/resources`](https://platform.claude.com/docs/id/api/beta/sessions/resources/add)                         |
  | `anthropic.sessions.resources.list`        | [`GET /v1/sessions/{session_id}/resources`](https://platform.claude.com/docs/id/api/beta/sessions/resources/list)                         |
  | `anthropic.sessions.resources.retrieve`    | [`GET /v1/sessions/{session_id}/resources/{resource_id}`](https://platform.claude.com/docs/id/api/beta/sessions/resources/retrieve)       |
  | `anthropic.sessions.resources.update`      | [`POST /v1/sessions/{session_id}/resources/{resource_id}`](https://platform.claude.com/docs/id/api/beta/sessions/resources/update)        |
  | `anthropic.sessions.resources.delete`      | [`DELETE /v1/sessions/{session_id}/resources/{resource_id}`](https://platform.claude.com/docs/id/api/beta/sessions/resources/delete)      |
  | `anthropic.sessions.threads.list`          | [`GET /v1/sessions/{session_id}/threads`](https://platform.claude.com/docs/id/api/beta/sessions/threads/list)                             |
  | `anthropic.sessions.threads.retrieve`      | [`GET /v1/sessions/{session_id}/threads/{thread_id}`](https://platform.claude.com/docs/id/api/beta/sessions/threads/retrieve)             |
  | `anthropic.sessions.threads.archive`       | [`POST /v1/sessions/{session_id}/threads/{thread_id}/archive`](https://platform.claude.com/docs/id/api/beta/sessions/threads/archive)     |
  | `anthropic.sessions.threads.events.list`   | [`GET /v1/sessions/{session_id}/threads/{thread_id}/events`](https://platform.claude.com/docs/id/api/beta/sessions/threads/events/list)   |
  | `anthropic.sessions.threads.events.stream` | [`GET /v1/sessions/{session_id}/threads/{thread_id}/stream`](https://platform.claude.com/docs/id/api/beta/sessions/threads/events/stream) |
</Accordion>

Span ini memiliki [atribut sesi](https://platform.claude.com/docs/id/api/opentelemetry/spans#session-attributes). Span SDK juga memiliki atribut dari setiap [span SDK untuk sebuah permintaan](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-resources-method).

| Atribut      | Tipe     | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `error.type` | `string` | [Jenis error](https://platform.claude.com/docs/id/api/errors#http-errors) dari permintaan yang gagal, misalnya `rate_limit_error`.<br />**SDK:** Juga nilai-nilai lain dalam [span SDK untuk permintaan](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-resources-method).<br />**API:** `api_error` ketika API menutup koneksi tanpa respons error, atau ketika stream berakhir karena kegagalan di API. |

### `anthropic.environment.work`

* **Sumber:** CLI dan SDK dalam Python, TypeScript, dan Go.
* **Jenis:** `INTERNAL`.
* **Induk:** Span yang sedang aktif di aplikasi ketika environment worker atau work poller mendapatkan work item, atau tidak ada jika tidak ada span yang aktif. Dalam `ant beta:worker poll`, span ini adalah root span.
* **Anak:** Span untuk permintaan yang dikirim environment worker saat menangani work item dan [span alat](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use) dari setiap alat yang dijalankannya untuk work item.

Environment worker dan work poller adalah [helper SDK](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#sdk-helpers) yang mengklaim work item dalam sandbox yang di-host sendiri. Keduanya memancarkan satu span `anthropic.environment.work` untuk setiap work item, sejak poll mengembalikan work item hingga penanganannya berakhir.

| Atribut                         | Tipe     | Deskripsi                                                                                                                                 |
| ------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `anthropic.environment.id`      | `string` | ID dari environment.                                                                                                                      |
| `anthropic.environment.work.id` | `string` | ID dari work item.                                                                                                                        |
| `anthropic.session.id`          | `string` | ID dari sesi tempat work item berada.                                                                                                     |
| `error.type`                    | `string` | `error.type` dari span untuk permintaan yang gagal, jika sebuah permintaan mengakhiri penanganan. `client_error` untuk kegagalan lainnya. |

### `anthropic.<resources>.<method>`

* **Sumber:** SDK.
* **Jenis:** `CLIENT`.
* **Induk:** Span yang sedang aktif di aplikasi ketika aplikasi memanggil metode, atau tidak ada jika tidak ada span yang aktif.
* **Anak:** Tidak ada.

Setiap metode SDK yang mengirim permintaan dan tidak memiliki bagian di halaman ini memancarkan span `anthropic.<resources>.<method>`, misalnya `anthropic.models.list` atau `anthropic.files.upload`. Permintaan untuk setiap halaman berikutnya dari sebuah list memiliki span tersendiri.

Sebuah span mencakup seluruh permintaannya, termasuk percobaan ulang, dan memiliki setiap atribut dari span API dengan nama yang sama ketika SDK memiliki nilainya. SDK mengatur `http.request.method` dan `http.route` ketika memulai span, sehingga sampler dapat menggunakannya.

Setiap span SDK untuk sebuah permintaan, termasuk [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create), [`anthropic.messages.count_tokens`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-count-tokens), dan [`anthropic.messages.batches.<method>`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-batches-method), memiliki atribut berikut:

| Atribut                     | Tipe     | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| --------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gen_ai.conversation.id`    | `string` | ID percakapan yang diteruskan dengan [opsi `conversation_id` (typescript, java, php: `conversationId`; csharp: `ConversationId`; go: `option.WithOpenTelemetryConversationID()`)](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#configure-the-sdk). Tanpa opsi tersebut, ID thread sesi tempat span berada, seperti di [Atribut sesi](https://platform.claude.com/docs/id/api/opentelemetry/spans#session-attributes), dan tidak ada pada span tanpa thread. |
| `anthropic.<resource>.id`   | `string` | Satu atribut untuk setiap ID dalam path permintaan dan satu untuk ID objek yang dibuat oleh metode. Namanya berasal dari path, dalam bentuk tunggal, misalnya `anthropic.session.id` atau `anthropic.session.thread.id`.                                                                                                                                                                                                                                                           |
| `gen_ai.agent.id`           | `string` | ID dari agent, pada metode agent.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `gen_ai.memory.store.id`    | `string` | ID dari memory store, pada metode memory store.                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `gen_ai.memory.record.id`   | `string` | ID dari memori, pada metode memori.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `http.request.resend_count` | `int`    | Berapa kali SDK mengirim ulang permintaan, karena alasan apa pun, seperti percobaan ulang. Tidak ada ketika SDK tidak mengirimnya ulang.                                                                                                                                                                                                                                                                                                                                           |
| `error.type`                | `string` | [Jenis error](https://platform.claude.com/docs/id/api/errors#http-errors) dari panggilan yang gagal, misalnya `rate_limit_error`. Kode status HTTP, misalnya `502`, ketika respons error tidak memiliki jenis error. `connection_error`, `client_timeout_error`, atau `client_error` ketika panggilan gagal di SDK. `api_error` ketika server mengakhiri stream lebih awal.                                                                                                        |
| `server.address`            | `string` | Host dari base URL klien, `api.anthropic.com` secara default. Pada klien platform cloud, host dari platform tersebut.                                                                                                                                                                                                                                                                                                                                                              |
| `url.query`                 | `string` | Query string dari URL, hanya dengan parameter query yang didefinisikan oleh endpoint. Tidak ada ketika tidak ada parameter tersebut. Dalam mode metadata-only, tidak ada ketika query memiliki parameter sensitif, seperti `email`.                                                                                                                                                                                                                                                |
| `url.full`                  | `string` | URL, yang tersusun dari `url.scheme`, `server.address`, port ketika base URL memilikinya, `url.path`, dan `url.query`. Dalam mode metadata-only, tidak ada setiap kali mode tersebut menghilangkan `url.query`.                                                                                                                                                                                                                                                                    |
