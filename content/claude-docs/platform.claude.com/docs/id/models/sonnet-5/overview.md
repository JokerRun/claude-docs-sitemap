---
source: platform
url: https://platform.claude.com/docs/id/models/sonnet-5/overview
fetched_at: 2026-09-03T02:44:34.856042Z
sha256: 4191b29a2ce302e096ba29aa29b7cdd381e837b839daeb1eb3a1ae26977a516b
---

---
title: Claude Sonnet 5
url: https://platform.claude.com/docs/id/models/sonnet-5/overview
description: "Sekilas tentang Claude Sonnet 5: kegunaannya, ID model di setiap platform, jendela konteks, batas output, harga, ketersediaan, serta panduan dan sumber daya untuk membangun dengannya."
---

**Latest.** Released June 30, 2026.

The best combination of speed and intelligence

Model ID: `claude-sonnet-5`

Context window: 1M tokens · Max output: 128K tokens · Input pricing: $2 / MTok · Output pricing: $10 / MTok

[Announcement](https://www.anthropic.com/news/claude-sonnet-5) · [What’s new](https://platform.claude.com/docs/id/models/sonnet-5/whats-new-sonnet-5) · [Migration guide](https://platform.claude.com/docs/id/models/sonnet-5/migration-guide)

## Ikhtisar

Claude Sonnet 5 adalah generasi berikutnya dari keluarga model Sonnet milik Anthropic. Model ini merupakan peningkatan langsung (drop-in) untuk Claude Sonnet 4.6 dengan tiga perubahan perilaku: [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) aktif secara default, "extended thinking" (pemikiran diperpanjang) manual kini mengembalikan error 400 (fitur ini sudah dideprekasi pada Claude Sonnet 4.6), dan mengatur parameter sampling (`temperature`, `top_p`, `top_k`) ke nilai non-default mengembalikan error 400. Halaman ini merangkum semua yang baru saat peluncuran, termasuk tokenizer baru.

[Apa yang baru di Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/whats-new-sonnet-5)

## Perbandingannya

| Model                                                                             | Context | Max output | Price / MTok | Latency  | Thinking             | Default effort | Knowledge cutoff |
| :-------------------------------------------------------------------------------- | :------ | :--------- | :----------- | :------- | :------------------- | :------------- | :--------------- |
| [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) | 1M      | 128K       | $10 / $50    | Slower   | Adaptive (always on) | `high`         | Jun 2026         |
| [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview)       | 1M      | 128K       | $5 / $25     | Moderate | Adaptive             | `high`         | May 2026         |
| **Claude Sonnet 5** (this model)                                                  | 1M      | 128K       | $2 / $10     | Fast     | Adaptive             | `high`         | Jan 2026         |
| [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/haiku-4-5/overview) | 200K    | 64K        | $1 / $5      | Fastest  | Extended             | —              | Feb 2025         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price (2.5% on Claude Fable 5.1 and Claude Mythos 5.1). See Pricing for the full list.
* **Latency:** Comparative latency, relative to the current lineup, as published in the models overview. Actual latency depends on prompt length, output length, and thinking effort.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual budget\_tokens mode on earlier models.
* **Default effort:** The effort parameter’s default on the Claude API. Models without a value don’t support the parameter.
* **Knowledge cutoff:** Reliable knowledge cutoff: the date through which the model’s knowledge is most extensive and reliable.

## Spesifikasi

### Model IDs

| Platform                                                                                               | Model ID                    |
| :----------------------------------------------------------------------------------------------------- | :-------------------------- |
| Claude API                                                                                             | `claude-sonnet-5`           |
| [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)       | `anthropic.claude-sonnet-5` |
| [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)              | `claude-sonnet-5`           |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | `claude-sonnet-5`           |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) | `claude-sonnet-5`           |

### Pricing

| Feature                                                                                | Value                                                               |
| :------------------------------------------------------------------------------------- | :------------------------------------------------------------------ |
| Input                                                                                  | $2 / MTok                                                           |
| Output                                                                                 | $10 / MTok                                                          |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $2.50 / MTok                                                        |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $4 / MTok                                                           |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $0.20 / MTok                                                        |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)    | 50% discount on input and output                                    |
| Full price list                                                                        | [Pricing](https://platform.claude.com/docs/id/about-claude/pricing) |

### Capabilities

| Feature                                                                                                                     | Value                  |
| :-------------------------------------------------------------------------------------------------------------------------- | :--------------------- |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows)                                     | 1M tokens              |
| Max output                                                                                                                  | 128K tokens            |
| [Max output (Batch API, beta)](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta) | 300K tokens            |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)                                                  | Adaptive               |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)                                              | `high`                 |
| Comparative latency                                                                                                         | Fast                   |
| Input → output                                                                                                              | Text and images → text |
| Reliable knowledge cutoff                                                                                                   | Jan 2026               |
| Training data cutoff                                                                                                        | Jan 2026               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                   |
| :---------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (latest)                                                                                                                                                                                                                                                                                                                                                                                                         |
| Released                                                                      | June 30, 2026                                                                                                                                                                                                                                                                                                                                                                                                           |
| Retirement                                                                    | Not sooner than June 30, 2027                                                                                                                                                                                                                                                                                                                                                                                           |
| Platforms                                                                     | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

## Perlu diketahui

* Pada [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta), Claude Sonnet 5 mendukung hingga 300 ribu token output dengan header beta `output-300k-2026-03-24`.
* Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default akan mengembalikan error 400. Lihat [Yang baru di Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/whats-new-sonnet-5#sampling-parameters-not-accepted).
* Kueri batas dan kemampuan secara terprogram dengan [Models API](https://platform.claude.com/docs/id/api/models/list).

## Sumber daya

<CardGroup cols={3}>
  <Card title="Prompting Claude Sonnet 5" icon="lightbulb" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5">
    Panduan prompting khusus model.
  </Card>

  <Card title="Pemikiran adaptif" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Aktif secara default pada Claude Sonnet 5. Atur kedalamannya dengan `effort`.
  </Card>

  <Card title="Effort" icon="sliders" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Effort secara default bernilai `high` pada Claude API dan Claude Code. Pilih tingkat sesuai beban kerja.
  </Card>

  <Card title="Jendela konteks" icon="stack" href="https://platform.claude.com/docs/id/build-with-claude/context-windows">
    1 juta token secara default. Cara jendela konteks dihitung dan dikelola.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="System card" icon="file" href="https://www.anthropic.com/claude-sonnet-5-system-card">
    Evaluasi keamanan dan keputusan deployment untuk Claude Sonnet 5.
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
