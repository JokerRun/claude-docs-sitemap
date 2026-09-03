---
source: platform
url: https://platform.claude.com/docs/id/models/mythos-5/overview
fetched_at: 2026-09-03T02:44:34.856042Z
sha256: eea972e0933061eaf00a62c665f92bf5b7ac95ea745b46ba805be2187e878388
---

---
title: Claude Mythos 5
url: https://platform.claude.com/docs/id/models/mythos-5/overview
description: "Referensi Claude Mythos 5: model yang sama dengan Claude Fable 5, ditawarkan hanya melalui undangan lewat Project Glasswing untuk pekerjaan keamanan siber defensif. ID model, spesifikasi, harga, dan sumber daya migrasi. Claude Mythos 5.1 adalah model Mythos saat ini."
---

**Invite only.** Released June 9, 2026.

Most capable model for cybersecurity and biology research

Model ID: `claude-mythos-5`

Context window: 1M tokens · Max output: 128K tokens · Input pricing: $10 / MTok · Output pricing: $50 / MTok

[Announcement](https://www.anthropic.com/news/claude-fable-5-mythos-5) · [What’s new](https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5) · [Migration guide](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-mythos-5-to-claude-mythos-5-1)

Claude Mythos 5 is offered separately, by invitation only, as part of Project Glasswing. It shares Claude Fable 5’s specifications and pricing. For access, contact your Anthropic, AWS, or Google Cloud account team. [See Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview) · [Project Glasswing](https://anthropic.com/glasswing)

## Perbandingannya

| Model                                                                             | Context | Max output | Price / MTok | Thinking             | Default effort | Knowledge cutoff |
| :-------------------------------------------------------------------------------- | :------ | :--------- | :----------- | :------------------- | :------------- | :--------------- |
| [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) | 1M      | 128K       | $10 / $50    | Adaptive (always on) | `high`         | Jun 2026         |
| **Claude Mythos 5** (this model)                                                  | 1M      | 128K       | $10 / $50    | Adaptive (always on) | `high`         | Jan 2026         |
| [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview)       | 1M      | 128K       | $5 / $25     | Adaptive             | `high`         | May 2026         |
| [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview)   | 1M      | 128K       | $2 / $10     | Adaptive             | `high`         | Jan 2026         |
| [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/haiku-4-5/overview) | 200K    | 64K        | $1 / $5      | Extended             | —              | Feb 2025         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price (2.5% on Claude Fable 5.1 and Claude Mythos 5.1). See Pricing for the full list.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual budget\_tokens mode on earlier models.
* **Default effort:** The effort parameter’s default on the Claude API. Models without a value don’t support the parameter.
* **Knowledge cutoff:** Reliable knowledge cutoff: the date through which the model’s knowledge is most extensive and reliable.

## Spesifikasi

### Model IDs

| Platform                                                                                               | Model ID                    |
| :----------------------------------------------------------------------------------------------------- | :-------------------------- |
| Claude API                                                                                             | `claude-mythos-5`           |
| [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)       | `anthropic.claude-mythos-5` |
| [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)              | `claude-mythos-5`           |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | `claude-mythos-5`           |

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

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                           |
| :---------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (invite only)                                                                                                                                                                                                                                                                                            |
| Released                                                                      | June 9, 2026                                                                                                                                                                                                                                                                                                    |
| Retirement                                                                    | Not sooner than June 9, 2027                                                                                                                                                                                                                                                                                    |
| Platforms                                                                     | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) |

## Sumber daya

<CardGroup cols={3}>
  <Card title="Migrasi ke Claude Mythos 5.1" icon="arrows-left-right" href="https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-mythos-5-to-claude-mythos-5-1">
    Apa yang berubah saat berpindah dari Claude Mythos 5 ke Claude Mythos 5.1.
  </Card>

  <Card title="Claude Mythos 5.1" icon="arrow-right" href="https://platform.claude.com/docs/id/models/mythos-5-1/overview">
    Model Mythos saat ini: ikhtisar, spesifikasi, dan sumber daya.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="System card" icon="file" href="https://www.anthropic.com/claude-fable-5-mythos-5-system-card">
    Evaluasi keamanan dan keputusan deployment untuk Claude Fable 5 dan Claude Mythos 5.
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
