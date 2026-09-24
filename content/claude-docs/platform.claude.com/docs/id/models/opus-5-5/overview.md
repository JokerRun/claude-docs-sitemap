---
source: platform
url: https://platform.claude.com/docs/id/models/opus-5-5/overview
fetched_at: 2026-09-24T02:21:35.920672Z
sha256: 7390d833ec7476a0864f1d1a7601488dbb67d43349c540667f82c2246685b8ee
---

---
title: Claude Opus 5.5
url: https://platform.claude.com/docs/id/models/opus-5-5/overview
description: "Sekilas tentang Claude Opus 5.5: kegunaannya, ID model di setiap platform, jendela konteks, batas output, harga, ketersediaan, serta panduan dan sumber daya untuk membangun dengannya."
---

**Latest.** Released September 22, 2026.

For long-running agentic coding and knowledge work

Model ID: `claude-opus-5-5`

Context window: 1M tokens · Max output: 128K tokens · Input pricing: $4 / MTok · Output pricing: $20 / MTok

[Announcement](https://www.anthropic.com/claude-opus-5-5) · [What’s new](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5) · [Migration guide](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide)

## Ikhtisar

Claude Opus 5.5 dibangun untuk agentic coding dan pekerjaan pengetahuan yang berjalan lama, dengan harga $4 / $20 USD per juta token input / output. Empat "breaking changes" (perubahan yang merusak kompatibilitas) memengaruhi kode yang sudah berjalan di Claude Opus 5: [thinking tidak dapat dinonaktifkan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-cant-be-disabled), [penggunaan alat paksa mengembalikan error](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#forced-tool-use-is-not-supported), [blok thinking terikat pada model dan percakapan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them), dan, di Claude API dan Google Cloud, [alat computer use `computer_20251124` yang lebih lama tidak diterima](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#computer-20251124-is-not-supported). Tiga yang pertama juga berlaku di Claude Fable 5.1. Satu perubahan lain mengubah bentuk respons tanpa menggagalkan permintaan apa pun: [teks di antara panggilan alat dikembalikan dalam blok `thinking`](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#text-between-tool-calls) yang teksnya kosong pada pengaturan `display` default. Aplikasi yang melakukan streaming teks tersebut ke penggunanya sebagai pembaruan progres akan menjadi senyap di antara panggilan alat hingga aplikasi tersebut menetapkan nilai `display` yang mengembalikan teks.

[Yang baru di Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5)

## Perbandingannya

| Model                                                                             | Context | Max output | Price / MTok | Latency  | Thinking             | Default effort | Knowledge cutoff |
| :-------------------------------------------------------------------------------- | :------ | :--------- | :----------- | :------- | :------------------- | :------------- | :--------------- |
| [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) | 1M      | 128K       | $10 / $50    | Slower   | Adaptive (always on) | `high`         | Jun 2026         |
| **Claude Opus 5.5** (this model)                                                  | 1M      | 128K       | $4 / $20     | Moderate | Adaptive (always on) | `medium`       | Jun 2026         |
| [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview)   | 1M      | 128K       | $2 / $10     | Fast     | Adaptive             | `high`         | Jan 2026         |
| [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/haiku-4-5/overview) | 200K    | 64K        | $1 / $5      | Fastest  | Extended             | —              | Feb 2025         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price (2.5% on Claude Fable 5.1 and Claude Mythos 5.1, 5% on Claude Opus 5.5). See Pricing for the full list.
* **Latency:** Comparative latency, relative to the current lineup, as published in the models overview. Actual latency depends on prompt length, output length, and thinking effort.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual budget\_tokens mode on earlier models.
* **Default effort:** The effort parameter’s default on the Claude API. Models without a value don’t support the parameter.
* **Knowledge cutoff:** Reliable knowledge cutoff: the date through which the model’s knowledge is most extensive and reliable.

## Spesifikasi

### Model IDs

| Platform                                                                                               | Model ID                    |
| :----------------------------------------------------------------------------------------------------- | :-------------------------- |
| Claude API                                                                                             | `claude-opus-5-5`           |
| [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)       | `anthropic.claude-opus-5-5` |
| [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)              | `claude-opus-5-5`           |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | `claude-opus-5-5`           |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) | `claude-opus-5-5`           |

### Pricing

| Feature                                                                                | Value                            |
| :------------------------------------------------------------------------------------- | :------------------------------- |
| Input                                                                                  | $4 / MTok                        |
| Output                                                                                 | $20 / MTok                       |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $5 / MTok                        |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $8 / MTok                        |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $0.20 / MTok                     |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)    | 50% discount on input and output |

[Full price list](https://platform.claude.com/docs/id/about-claude/pricing)

### Capabilities

| Feature                                                                                                                     | Value                  |
| :-------------------------------------------------------------------------------------------------------------------------- | :--------------------- |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows)                                     | 1M tokens              |
| Max output                                                                                                                  | 128K tokens            |
| [Max output (Batch API, beta)](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta) | 300K tokens            |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)                                                  | Adaptive (always on)   |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)                                              | `medium`               |
| Comparative latency                                                                                                         | Moderate               |
| Input → output                                                                                                              | Text and images → text |
| Reliable knowledge cutoff                                                                                                   | Jun 2026               |
| Training data cutoff                                                                                                        | Jun 2026               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                   |
| :---------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (latest)                                                                                                                                                                                                                                                                                                                                                                                                         |
| Released                                                                      | September 22, 2026                                                                                                                                                                                                                                                                                                                                                                                                      |
| Retirement                                                                    | Not sooner than September 22, 2027                                                                                                                                                                                                                                                                                                                                                                                      |
| Platforms                                                                     | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

## Perlu diketahui

* "Adaptive thinking" (pemikiran adaptif) selalu aktif dan tidak dapat dinonaktifkan. Kendalikan kedalaman pemikiran dengan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort).
* Pada [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta), Claude Opus 5.5 mendukung hingga 300 ribu token output dengan header beta `output-300k-2026-03-24`.
* Panjang prompt minimum yang dapat di-cache adalah 512 token. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations).
* Kueri batas dan kemampuan secara terprogram dengan [Models API](https://platform.claude.com/docs/id/api/models/list).

## Sumber daya

<CardGroup cols={3}>
  <Card title="Prompting Claude Opus 5.5" icon="lightbulb" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5">
    Perbedaan perilaku dan pola prompting yang khusus untuk Claude Opus 5.5.
  </Card>

  <Card title="Effort" icon="sliders" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kontrol untuk kedalaman pemikiran, "latency" (latensi), dan biaya. Pilih level untuk setiap beban kerja.
  </Card>

  <Card title="Pemikiran adaptif" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Cara kerja pemikiran adaptif dan cara blok pemikiran dipertahankan.
  </Card>

  <Card title="Mode cepat" icon="lightning" href="https://platform.claude.com/docs/id/build-with-claude/fast-mode">
    Claude Opus 5.5 dengan latensi lebih rendah di Claude API (pratinjau riset), dengan harga terpisah.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="Prompt sistem" icon="text" href="https://platform.claude.com/docs/id/release-notes/system-prompts/claude-opus-5-5">
    Prompt sistem yang digunakan Claude Opus 5.5 di claude.ai dan aplikasi Claude.
  </Card>

  <Card title="System card" icon="file" href="https://www.anthropic.com/claude-opus-5-5-system-card">
    Evaluasi keamanan dan keputusan deployment untuk Claude Opus 5.5.
  </Card>

  <Card title="Harga" icon="coins" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Daftar harga lengkap, termasuk diskon batch dan tarif caching prompt.
  </Card>

  <Card title="ID model dan pembuatan versi" icon="fingerprint" href="https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions">
    Cara kerja ID model, alias, dan snapshot yang disematkan.
  </Card>

  <Card title="Penghentian model" icon="clock" href="https://platform.claude.com/docs/id/about-claude/model-deprecations">
    Status siklus hidup dan komitmen penghentian untuk setiap model Claude.
  </Card>
</CardGroup>
