---
source: platform
url: https://platform.claude.com/docs/id/models/sonnet-4-5/overview
fetched_at: 2026-09-03T02:44:34.856042Z
sha256: 7b8e1e79612a62ef830ee4f36755fde23c2d1266acba5fda69edb4a5533d7049
---

---
title: Claude Sonnet 4.5
url: https://platform.claude.com/docs/id/models/sonnet-4-5/overview
description: "Referensi Claude Sonnet 4.5: status siklus hidup, ID model di setiap platform, jendela konteks, batas output, harga, dan sumber daya migrasi. Claude Sonnet 4.5 adalah model legacy; Claude Sonnet 5 adalah model Sonnet saat ini."
---

**Legacy.** Released September 29, 2025.

Although Claude Sonnet 4.5 is still available, you should consider migrating to Claude Sonnet 5 for improved performance. [See Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview) · [Migrate to Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/migration-guide#migrating-from-sonnet-45)

Model ID: `claude-sonnet-4-5-20250929`

Context window: 200K tokens · Max output: 64K tokens · Input pricing: $3 / MTok · Output pricing: $15 / MTok

[Announcement](https://www.anthropic.com/news/claude-sonnet-4-5)

## Bagaimana perbandingannya dengan lineup saat ini

| Model                                                                             | Context | Max output | Price / MTok | Thinking             | Default effort | Knowledge cutoff |
| :-------------------------------------------------------------------------------- | :------ | :--------- | :----------- | :------------------- | :------------- | :--------------- |
| [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) | 1M      | 128K       | $10 / $50    | Adaptive (always on) | `high`         | Jun 2026         |
| [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview)       | 1M      | 128K       | $5 / $25     | Adaptive             | `high`         | May 2026         |
| [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview)   | 1M      | 128K       | $2 / $10     | Adaptive             | `high`         | Jan 2026         |
| **Claude Sonnet 4.5** (this model)                                                | 200K    | 64K        | $3 / $15     | Extended             | —              | Jan 2025         |
| [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/haiku-4-5/overview) | 200K    | 64K        | $1 / $5      | Extended             | —              | Feb 2025         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price (2.5% on Claude Fable 5.1 and Claude Mythos 5.1). See Pricing for the full list.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual budget\_tokens mode on earlier models.
* **Default effort:** The effort parameter’s default on the Claude API. Models without a value don’t support the parameter.
* **Knowledge cutoff:** Reliable knowledge cutoff: the date through which the model’s knowledge is most extensive and reliable.

## Spesifikasi

### Model IDs

| Platform                                                                                                              | Model ID                                    |
| :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------------ |
| Claude API                                                                                                            | `claude-sonnet-4-5-20250929`                |
| Claude API alias                                                                                                      | `claude-sonnet-4-5`                         |
| [Amazon Bedrock (InvokeModel)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) | `anthropic.claude-sonnet-4-5-20250929-v1:0` |
| [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)                             | `claude-sonnet-4-5@20250929`                |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)                | `claude-sonnet-4-5`                         |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)                | `claude-sonnet-4-5`                         |

### Pricing

| Feature                                                                                | Value                                                               |
| :------------------------------------------------------------------------------------- | :------------------------------------------------------------------ |
| Input                                                                                  | $3 / MTok                                                           |
| Output                                                                                 | $15 / MTok                                                          |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $3.75 / MTok                                                        |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $6 / MTok                                                           |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $0.30 / MTok                                                        |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)    | 50% discount on input and output                                    |
| Full price list                                                                        | [Pricing](https://platform.claude.com/docs/id/about-claude/pricing) |

### Capabilities

| Feature                                                                                 | Value                  |
| :-------------------------------------------------------------------------------------- | :--------------------- |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows) | 200K tokens            |
| Max output                                                                              | 64K tokens             |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)              | Extended               |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)          | Not supported          |
| Input → output                                                                          | Text and images → text |
| Reliable knowledge cutoff                                                               | Jan 2025               |
| Training data cutoff                                                                    | Jul 2025               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| :---------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (legacy)                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Released                                                                      | September 29, 2025                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Retirement                                                                    | Not sooner than September 29, 2026                                                                                                                                                                                                                                                                                                                                                                                                           |
| Platforms                                                                     | Claude API, [Amazon Bedrock (InvokeModel)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

## Sumber Daya

<CardGroup cols={3}>
  <Card title="Migrasi ke Claude Sonnet 5" icon="arrows-left-right" href="https://platform.claude.com/docs/id/models/sonnet-5/migration-guide#migrating-from-sonnet-45">
    Apa yang berubah saat berpindah dari Claude Sonnet 4.5 dan model Sonnet sebelumnya ke Claude Sonnet 5.
  </Card>

  <Card title="Claude Sonnet 5" icon="arrow-right" href="https://platform.claude.com/docs/id/models/sonnet-5/overview">
    Model Sonnet saat ini: ikhtisar, spesifikasi, dan sumber daya.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="Prompt sistem" icon="text" href="https://platform.claude.com/docs/id/release-notes/system-prompts#claude-sonnet-4-5">
    Prompt sistem yang digunakan Claude Sonnet 4.5 di claude.ai dan aplikasi Claude.
  </Card>

  <Card title="System card" icon="file" href="https://www.anthropic.com/claude-sonnet-4-5-system-card">
    Evaluasi keamanan dan keputusan penerapan untuk Claude Sonnet 4.5.
  </Card>

  <Card title="Harga" icon="coins" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Daftar harga lengkap, termasuk diskon batch dan tarif caching prompt.
  </Card>

  <Card title="ID model dan versioning" icon="fingerprint" href="https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions">
    Cara kerja ID model, alias, dan snapshot yang disematkan.
  </Card>

  <Card title="Penghentian model" icon="clock" href="https://platform.claude.com/docs/id/about-claude/model-deprecations">
    Status siklus hidup dan komitmen pensiun untuk setiap model Claude.
  </Card>

  <Card title="Amazon Bedrock (Opus 4.6 dan sebelumnya)" icon="cloud" href="https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy">
    Claude Sonnet 4.5 menggunakan integrasi InvokeModel Bedrock dan ID model bergaya Bedrock.
  </Card>
</CardGroup>
