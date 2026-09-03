---
source: platform
url: https://platform.claude.com/docs/id/models/haiku-4-5/overview
fetched_at: 2026-09-03T02:44:34.856042Z
sha256: 676cf340a970cb08e381574b8fccc5b208803f556f9845197763704b7573b9e0
---

---
title: Claude Haiku 4.5
url: https://platform.claude.com/docs/id/models/haiku-4-5/overview
description: "Sekilas tentang Claude Haiku 4.5: kegunaannya, ID model di setiap platform, jendela konteks, batas output, harga, ketersediaan, serta panduan dan sumber daya untuk membangun dengannya."
---

**Latest.** Released October 15, 2025.

The fastest model with near-frontier intelligence

Model ID: `claude-haiku-4-5-20251001`

Context window: 200K tokens · Max output: 64K tokens · Input pricing: $1 / MTok · Output pricing: $5 / MTok

[Announcement](https://www.anthropic.com/news/claude-haiku-4-5) · [Migration guide](https://platform.claude.com/docs/id/models/haiku-4-5/migration-guide)

## Perbandingannya

| Model                                                                             | Context | Max output | Price / MTok | Latency  | Thinking             | Default effort | Knowledge cutoff |
| :-------------------------------------------------------------------------------- | :------ | :--------- | :----------- | :------- | :------------------- | :------------- | :--------------- |
| [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) | 1M      | 128K       | $10 / $50    | Slower   | Adaptive (always on) | `high`         | Jun 2026         |
| [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview)       | 1M      | 128K       | $5 / $25     | Moderate | Adaptive             | `high`         | May 2026         |
| [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview)   | 1M      | 128K       | $2 / $10     | Fast     | Adaptive             | `high`         | Jan 2026         |
| **Claude Haiku 4.5** (this model)                                                 | 200K    | 64K        | $1 / $5      | Fastest  | Extended             | —              | Feb 2025         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price (2.5% on Claude Fable 5.1 and Claude Mythos 5.1). See Pricing for the full list.
* **Latency:** Comparative latency, relative to the current lineup, as published in the models overview. Actual latency depends on prompt length, output length, and thinking effort.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual budget\_tokens mode on earlier models.
* **Default effort:** The effort parameter’s default on the Claude API. Models without a value don’t support the parameter.
* **Knowledge cutoff:** Reliable knowledge cutoff: the date through which the model’s knowledge is most extensive and reliable.

## Spesifikasi

### Model IDs

| Platform                                                                                                              | Model ID                                   |
| :-------------------------------------------------------------------------------------------------------------------- | :----------------------------------------- |
| Claude API                                                                                                            | `claude-haiku-4-5-20251001`                |
| Claude API alias                                                                                                      | `claude-haiku-4-5`                         |
| [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)                      | `anthropic.claude-haiku-4-5`               |
| [Amazon Bedrock (InvokeModel)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) | `anthropic.claude-haiku-4-5-20251001-v1:0` |
| [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)                             | `claude-haiku-4-5@20251001`                |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)                | `claude-haiku-4-5`                         |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)                | `claude-haiku-4-5`                         |

### Pricing

| Feature                                                                                | Value                                                               |
| :------------------------------------------------------------------------------------- | :------------------------------------------------------------------ |
| Input                                                                                  | $1 / MTok                                                           |
| Output                                                                                 | $5 / MTok                                                           |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $1.25 / MTok                                                        |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $2 / MTok                                                           |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $0.10 / MTok                                                        |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)    | 50% discount on input and output                                    |
| Full price list                                                                        | [Pricing](https://platform.claude.com/docs/id/about-claude/pricing) |

### Capabilities

| Feature                                                                                 | Value                  |
| :-------------------------------------------------------------------------------------- | :--------------------- |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows) | 200K tokens            |
| Max output                                                                              | 64K tokens             |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)              | Extended               |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)          | Not supported          |
| Comparative latency                                                                     | Fastest                |
| Input → output                                                                          | Text and images → text |
| Reliable knowledge cutoff                                                               | Feb 2025               |
| Training data cutoff                                                                    | Jul 2025               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| :---------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (latest)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Released                                                                      | October 15, 2025                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Retirement                                                                    | Not sooner than October 15, 2026                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Platforms                                                                     | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Amazon Bedrock (InvokeModel)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

## Perlu diketahui

* `claude-haiku-4-5` adalah alias praktis yang mengarah ke snapshot tetap `claude-haiku-4-5-20251001`. Lihat [ID model dan pembuatan versi](https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions).
* Claude Haiku 4.5 menggunakan "extended thinking" (pemikiran diperpanjang) manual (`thinking.type: "enabled"`), bukan pemikiran adaptif.
* Kueri batas dan kemampuan secara terprogram dengan [Models API](https://platform.claude.com/docs/id/api/models/list).

## Sumber daya

<CardGroup cols={3}>
  <Card title="Pemikiran diperpanjang" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/extended-thinking">
    Claude Haiku 4.5 mendukung pemikiran diperpanjang manual dengan `budget_tokens`.
  </Card>

  <Card title="Memilih model" icon="scales" href="https://platform.claude.com/docs/id/about-claude/models/choosing-a-model">
    Kapan memulai dengan mengutamakan efisiensi menggunakan Haiku dan kapan beralih ke model yang lebih besar.
  </Card>

  <Card title="Mengurangi latensi" icon="gauge" href="https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/reduce-latency">
    Teknik yang cocok dipadukan dengan model tercepat dalam jajaran ini.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="Prompt sistem" icon="text" href="https://platform.claude.com/docs/id/release-notes/system-prompts#claude-haiku-4-5">
    Prompt sistem yang digunakan Claude Haiku 4.5 di claude.ai dan aplikasi Claude.
  </Card>

  <Card title="System card" icon="file" href="https://www.anthropic.com/claude-haiku-4-5-system-card">
    Evaluasi keamanan dan keputusan deployment untuk Claude Haiku 4.5.
  </Card>

  <Card title="Harga" icon="coins" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Daftar harga lengkap, termasuk diskon batch dan tarif caching prompt.
  </Card>

  <Card title="ID model dan pembuatan versi" icon="fingerprint" href="https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions">
    Cara kerja ID model, alias, dan snapshot tetap.
  </Card>

  <Card title="Penghentian model" icon="clock" href="https://platform.claude.com/docs/id/about-claude/model-deprecations">
    Status siklus hidup dan komitmen penghentian untuk setiap model Claude.
  </Card>

  <Card title="Amazon Bedrock (Opus 4.6 dan sebelumnya)" icon="cloud" href="https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy">
    Claude Haiku 4.5 juga tersedia melalui integrasi InvokeModel Bedrock dan ID model bergaya Bedrock.
  </Card>
</CardGroup>
