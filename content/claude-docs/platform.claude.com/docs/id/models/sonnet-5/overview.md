---
source: platform
url: https://platform.claude.com/docs/id/models/sonnet-5/overview
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 1c859d64425bafe9916820ece4b2639e4f5e02399ae16d3372f9d8fe75c93d97
---

---
title: Claude Sonnet 5
url: https://platform.claude.com/docs/id/models/sonnet-5/overview
description: "Referensi Claude Sonnet 5: status siklus hidup, ID model di setiap platform, jendela konteks, batas output, harga, dan sumber daya migrasi. Claude Sonnet 5 adalah model lama; Claude Sonnet 5.5 adalah model Sonnet saat ini."
---

**Legacy.** Released June 30, 2026.

Although Claude Sonnet 5 is still available, you should consider migrating to Claude Sonnet 5.5 for improved performance. [See Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview) · [Migrate to Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#migrating-from-claude-sonnet-5)

Model ID: `claude-sonnet-5`

Context window: 1M tokens · Max output: 128K tokens · Input pricing: $2 / MTok · Output pricing: $10 / MTok

[Announcement](https://www.anthropic.com/news/claude-sonnet-5)

## Perbandingannya dengan jajaran model saat ini

| Model                                                                               | Context | Max output | Price / MTok       | Thinking             | Default effort | Knowledge cutoff |
| :---------------------------------------------------------------------------------- | :------ | :--------- | :----------------- | :------------------- | :------------- | :--------------- |
| [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview)   | 1M      | 128K       | $10 / $50          | Adaptive (always on) | `high`         | Jun 2026         |
| [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview)     | 1M      | 128K       | $4 / $20           | Adaptive (always on) | `medium`       | Jun 2026         |
| [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview) | 1M      | 128K       | $2 / $10           | Adaptive             | `high`         | Jun 2026         |
| **Claude Sonnet 5** (this model)                                                    | 1M      | 128K       | $2 / $10           | Adaptive             | `high`         | Jan 2026         |
| [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview)   | 1M      | 128K       | From $0.10 / $0.50 | Adaptive             | `medium`       | Jun 2026         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Sonnet 5, Claude Haiku 5.5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price (2.5% on Claude Fable 5.1 and Claude Mythos 5.1, 5% on Claude Opus 5.5 and Claude Sonnet 5.5). See Pricing for the full list.
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

| Feature                                                                                | Value                            |
| :------------------------------------------------------------------------------------- | :------------------------------- |
| Input                                                                                  | $2 / MTok                        |
| Output                                                                                 | $10 / MTok                       |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $2.50 / MTok                     |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $4 / MTok                        |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $0.20 / MTok                     |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)    | 50% discount on input and output |

[Full price list](https://platform.claude.com/docs/id/about-claude/pricing)

### Capabilities

| Feature                                                                                                                     | Value                  |
| :-------------------------------------------------------------------------------------------------------------------------- | :--------------------- |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows)                                     | 1M tokens              |
| Max output                                                                                                                  | 128K tokens            |
| [Max output (Batch API, beta)](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta) | 300K tokens            |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)                                                  | Adaptive               |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)                                              | `high`                 |
| Input → output                                                                                                              | Text and images → text |
| Reliable knowledge cutoff                                                                                                   | Jan 2026               |
| Training data cutoff                                                                                                        | Jan 2026               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                   |
| :---------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (legacy)                                                                                                                                                                                                                                                                                                                                                                                                         |
| Released                                                                      | June 30, 2026                                                                                                                                                                                                                                                                                                                                                                                                           |
| Retirement                                                                    | Not sooner than June 30, 2027                                                                                                                                                                                                                                                                                                                                                                                           |
| Platforms                                                                     | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

## Perlu diketahui

* Pada [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta), Claude Sonnet 5 mendukung hingga 300 ribu token output dengan header beta `output-300k-2026-03-24`.
* Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default akan mengembalikan error 400.
* Kueri batas dan kemampuan secara terprogram dengan [Models API](https://platform.claude.com/docs/id/api/models/list).

## Sumber daya

<CardGroup cols={3}>
  <Card title="Migrasi ke Claude Sonnet 5.5" icon="arrows-left-right" href="https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#migrating-from-claude-sonnet-5">
    Apa yang berubah saat beralih dari Claude Sonnet 5 ke Claude Sonnet 5.5.
  </Card>

  <Card title="Claude Sonnet 5.5" icon="arrow-right" href="https://platform.claude.com/docs/id/models/sonnet-5-5/overview">
    Model Sonnet saat ini: ikhtisar, spesifikasi, dan sumber daya.
  </Card>

  <Card title="Prompting Claude Sonnet 5" icon="lightbulb" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5">
    Panduan prompting khusus model.
  </Card>

  <Card title="Pemikiran adaptif" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Aktif secara default di Claude Sonnet 5. Atur kedalamannya dengan `effort`.
  </Card>

  <Card title="Effort" icon="sliders" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Effort secara default bernilai `high` di Claude API dan Claude Code. Pilih level untuk setiap beban kerja.
  </Card>

  <Card title="Jendela konteks" icon="stack" href="https://platform.claude.com/docs/id/build-with-claude/context-windows">
    1M token secara default. Cara jendela dihitung dan dikelola.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="Prompt sistem" icon="text" href="https://platform.claude.com/docs/id/release-notes/system-prompts/claude-sonnet-5">
    Prompt sistem yang digunakan Claude Sonnet 5 di claude.ai dan aplikasi Claude.
  </Card>

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
