---
source: platform
url: https://platform.claude.com/docs/id/models/fable-5/overview
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: a50c1b62560cda0b655d8d2419bf7c219a240051d5227fcc4b661d818a227509
---

---
title: Claude Fable 5
url: https://platform.claude.com/docs/id/models/fable-5/overview
description: "Referensi Claude Fable 5: status siklus hidup, ID model di setiap platform, jendela konteks, batas output, harga, dan sumber daya migrasi. Claude Fable 5 adalah model lawas, dan Claude Fable 5.1 adalah model Fable saat ini."
---

**Legacy.** Released June 9, 2026.

Although Claude Fable 5 is still available, you should consider migrating to Claude Fable 5.1 for improved performance. [See Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) · [Migrate to Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-fable-5-to-claude-fable-5-1)

Model ID: `claude-fable-5`

Context window: 1M tokens · Max output: 128K tokens · Input pricing: $10 / MTok · Output pricing: $50 / MTok

[Announcement](https://www.anthropic.com/news/claude-fable-5-mythos-5) · [What’s new](https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5)

## Fable vs. Mythos

[Claude Mythos 5](https://platform.claude.com/docs/id/models/mythos-5/overview) ditawarkan secara terpisah, hanya dengan undangan, untuk alur kerja keamanan siber defensif sebagai bagian dari [Project Glasswing](https://anthropic.com/glasswing). Model ini berbagi spesifikasi dan harga Claude Fable 5; Claude Fable 5 menyertakan pengklasifikasi keamanan yang dapat menolak permintaan, dan Claude Mythos 5 tidak. Untuk akses, hubungi tim akun Anthropic, AWS, atau Google Cloud Anda.

## Bagaimana perbandingannya dengan lineup saat ini

| Model                                                                             | Context | Max output | Price / MTok | Thinking             | Default effort | Knowledge cutoff |
| :-------------------------------------------------------------------------------- | :------ | :--------- | :----------- | :------------------- | :------------- | :--------------- |
| [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) | 1M      | 128K       | $10 / $50    | Adaptive (always on) | `high`         | Jun 2026         |
| **Claude Fable 5** (this model)                                                   | 1M      | 128K       | $10 / $50    | Adaptive (always on) | `high`         | Jan 2026         |
| [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview)       | 1M      | 128K       | $5 / $25     | Adaptive             | `high`         | May 2026         |
| [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview)   | 1M      | 128K       | $2 / $10     | Adaptive             | `high`         | Jan 2026         |
| [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/haiku-4-5/overview) | 200K    | 64K        | $1 / $5      | Extended             | —              | Feb 2025         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price. See Pricing for the full list.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual budget\_tokens mode on earlier models.
* **Default effort:** The effort parameter’s default on the Claude API. Models without a value don’t support the parameter.
* **Knowledge cutoff:** Reliable knowledge cutoff: the date through which the model’s knowledge is most extensive and reliable.

## Spesifikasi

### Model IDs

| Platform                                                                                               | Model ID                   |
| :----------------------------------------------------------------------------------------------------- | :------------------------- |
| Claude API                                                                                             | `claude-fable-5`           |
| [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)       | `anthropic.claude-fable-5` |
| [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)              | `claude-fable-5`           |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | `claude-fable-5`           |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) | `claude-fable-5`           |

### Pricing

| Feature                                                                                | Value                                                               |
| :------------------------------------------------------------------------------------- | :------------------------------------------------------------------ |
| Input                                                                                  | $10 / MTok                                                          |
| Output                                                                                 | $50 / MTok                                                          |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $12.50 / MTok                                                       |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $20 / MTok                                                          |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $1 / MTok                                                           |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)    | 50% discount on input and output                                    |
| Full price list                                                                        | [Pricing](https://platform.claude.com/docs/id/about-claude/pricing) |

### Capabilities

| Feature                                                                                 | Value                  |
| :-------------------------------------------------------------------------------------- | :--------------------- |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows) | 1M tokens              |
| Max output                                                                              | 128K tokens            |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)              | Adaptive (always on)   |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)          | `high`                 |
| Input → output                                                                          | Text and images → text |
| Reliable knowledge cutoff                                                               | Jan 2026               |
| Training data cutoff                                                                    | Jan 2026               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                   |
| :---------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (legacy)                                                                                                                                                                                                                                                                                                                                                                                                         |
| Released                                                                      | June 9, 2026                                                                                                                                                                                                                                                                                                                                                                                                            |
| Retirement                                                                    | Not sooner than June 9, 2027                                                                                                                                                                                                                                                                                                                                                                                            |
| Platforms                                                                     | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

## Sumber Daya

<CardGroup cols={3}>
  <Card title="Migrasi ke Claude Fable 5.1" icon="arrows-left-right" href="https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-fable-5-to-claude-fable-5-1">
    Apa yang berubah saat berpindah dari Claude Fable 5 ke Claude Fable 5.1.
  </Card>

  <Card title="Claude Fable 5.1" icon="arrow-right" href="https://platform.claude.com/docs/id/models/fable-5-1/overview">
    Model Fable saat ini: ikhtisar, spesifikasi, dan sumber daya.
  </Card>

  <Card title="Memperkenalkan Claude Fable 5 dan Claude Mythos 5" icon="star" href="https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5">
    Kemampuan, perubahan API, dan ketersediaan untuk Claude Fable 5.
  </Card>

  <Card title="Prompting Claude Fable 5" icon="lightbulb" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5">
    Panduan prompting khusus model untuk pekerjaan jangka panjang dan agentik.
  </Card>

  <Card title="Penolakan dan fallback" icon="shield" href="https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback">
    Menangani penolakan pengklasifikasi dan mencoba ulang pada model Claude lain dengan parameter `fallbacks`.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="Prompt sistem" icon="text" href="https://platform.claude.com/docs/id/release-notes/system-prompts#claude-fable-5">
    Prompt sistem yang digunakan Claude Fable 5 di claude.ai dan aplikasi Claude.
  </Card>

  <Card title="System card" icon="file" href="https://www.anthropic.com/claude-fable-5-mythos-5-system-card">
    Evaluasi keamanan dan keputusan penerapan untuk Claude Fable 5 dan Claude Mythos 5.
  </Card>

  <Card title="Harga" icon="coins" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Daftar harga lengkap, termasuk diskon batch dan tarif caching prompt.
  </Card>

  <Card title="ID model dan versioning" icon="fingerprint" href="https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions">
    Cara kerja ID model, alias, dan snapshot yang disematkan.
  </Card>

  <Card title="Penghentian model" icon="clock" href="https://platform.claude.com/docs/id/about-claude/model-deprecations">
    Status siklus hidup dan komitmen penghentian untuk setiap model Claude.
  </Card>
</CardGroup>
