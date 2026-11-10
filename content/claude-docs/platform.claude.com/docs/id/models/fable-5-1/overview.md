---
source: platform
url: https://platform.claude.com/docs/id/models/fable-5-1/overview
fetched_at: 2026-11-10T02:13:26.049428Z
sha256: f0a00677d21c28083ffaaf139709be48a85e92210569a4cc7b94263efcf9dd88
---

---
title: Claude Fable 5.1
url: https://platform.claude.com/docs/id/models/fable-5-1/overview
description: "Referensi Claude Fable 5.1: status siklus hidup, ID model di setiap platform, jendela konteks, batas output, harga, dan sumber daya migrasi. Claude Fable 5.1 adalah model lama, dan Claude Fable 5.2 adalah model Fable saat ini."
---

**Legacy.** Released September 1, 2026.

For demanding reasoning and long-horizon agentic work

Although Claude Fable 5.1 is still available, you should consider migrating to Claude Fable 5.2. [See Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/overview) · [Migrate to Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/migration-guide)

Model ID: `claude-fable-5-1`

Context window: 1M tokens · Max output: 128K tokens · Input pricing: $10 / MTok · Output pricing: $50 / MTok

[Announcement](https://www.anthropic.com/claude-fable-and-mythos-5-1)

## Claude Fable 5.1 dan Claude Mythos 5.1

[Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview) menawarkan kemampuan yang sama hanya kepada organisasi yang telah diverifikasi melalui program verifikasi Anthropic, seperti [Cyber Verification Program](https://support.claude.com/en/articles/14604842). Model ini memiliki spesifikasi dan harga yang sama dengan Claude Fable 5.1. Untuk meminta akses, ajukan permohonan ke program yang mencakup kasus penggunaan Anda, atau hubungi tim akun Anthropic, AWS, atau Google Cloud Anda.

## Perbandingannya dengan jajaran model saat ini

| Model                                                                               | Context | Max output | Price / MTok       | Thinking             | Default effort | Knowledge cutoff |
| :---------------------------------------------------------------------------------- | :------ | :--------- | :----------------- | :------------------- | :------------- | :--------------- |
| [Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/overview)   | 1M      | 128K       | $8 / $40           | Adaptive (always on) | `high`         | Jun 2026         |
| **Claude Fable 5.1** (this model)                                                   | 1M      | 128K       | $10 / $50          | Adaptive (always on) | `high`         | Jun 2026         |
| [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview)     | 1M      | 128K       | $4 / $20           | Adaptive (always on) | `medium`       | Jun 2026         |
| [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview) | 1M      | 128K       | $2 / $10           | Adaptive             | `high`         | Jun 2026         |
| [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview)   | 1M      | 128K       | From $0.10 / $0.50 | Adaptive             | `medium`       | Jun 2026         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Sonnet 5, Claude Haiku 5.5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price (2.5% on Claude Fable 5.2, Claude Mythos 5.2, Claude Fable 5.1, and Claude Mythos 5.1, 5% on Claude Opus 5.5 and Claude Sonnet 5.5). See Pricing for the full list.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual budget\_tokens mode on earlier models.
* **Default effort:** The effort parameter’s default on the Claude API. Models without a value don’t support the parameter.
* **Knowledge cutoff:** Reliable knowledge cutoff: the date through which the model’s knowledge is most extensive and reliable.

## Spesifikasi

### Model IDs

| Platform                                                                                                                                                   | Model ID                     |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------- |
| Claude API                                                                                                                                                 | `claude-fable-5-1`           |
| [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)                                                           | `anthropic.claude-fable-5-1` |
| [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed)       | `claude-fable-5-1`           |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)                                                     | `claude-fable-5-1`           |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)                                                     | `claude-fable-5-1`           |
| [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) | `claude-fable-5-1`           |

### Pricing

| Feature                                                                                | Value                            |
| :------------------------------------------------------------------------------------- | :------------------------------- |
| Input                                                                                  | $10 / MTok                       |
| Output                                                                                 | $50 / MTok                       |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $12.50 / MTok                    |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $20 / MTok                       |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $0.25 / MTok                     |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)    | 50% discount on input and output |

[Full price list](https://platform.claude.com/docs/id/about-claude/pricing)

### Capabilities

| Feature                                                                                 | Value                  |
| :-------------------------------------------------------------------------------------- | :--------------------- |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows) | 1M tokens              |
| Max output                                                                              | 128K tokens            |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)              | Adaptive (always on)   |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)          | `high`                 |
| Input → output                                                                          | Text and images → text |
| Reliable knowledge cutoff                                                               | Jun 2026               |
| Training data cutoff                                                                    | Jun 2026               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| :---------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (legacy)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Released                                                                      | September 1, 2026                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Retirement                                                                    | Not sooner than September 1, 2027                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Platforms                                                                     | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) |

## Sumber daya

<CardGroup cols={3}>
  <Card title="Migrasi ke Claude Fable 5.2" icon="arrows-left-right" href="https://platform.claude.com/docs/id/models/fable-5-2/migration-guide#migrating-from-claude-fable-5-1-to-claude-fable-5-2">
    Apa yang berubah saat beralih dari Claude Fable 5.1 ke Claude Fable 5.2.
  </Card>

  <Card title="Claude Fable 5.2" icon="arrow-right" href="https://platform.claude.com/docs/id/models/fable-5-2/overview">
    Model Fable saat ini: ikhtisar, spesifikasi, dan sumber daya.
  </Card>

  <Card title="Menulis prompt untuk Claude Fable 5.1" icon="lightbulb" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1">
    Panduan prompting khusus model untuk pekerjaan jangka panjang dan agentik.
  </Card>

  <Card title="Pemikiran yang dipertahankan" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-thinking">
    Kapan blok pemikiran model ini tetap dapat digunakan: saat berganti model dan saat terjadi perubahan pada percakapan.
  </Card>

  <Card title="Effort per pesan" icon="sliders" href="https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta">
    Ubah tingkat effort di tengah percakapan tanpa membatalkan cache prompt.
  </Card>

  <Card title="Penolakan dan fallback" icon="shield" href="https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback">
    Tangani penolakan classifier dan coba ulang pada model Claude lain.
  </Card>

  <Card title="Pemikiran adaptif" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Satu-satunya mode pemikiran pada Claude Fable 5.1. Atur kedalamannya dengan `effort`.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="Prompt sistem" icon="text" href="https://platform.claude.com/docs/id/release-notes/system-prompts/claude-fable-5-1">
    Prompt sistem yang digunakan Claude Fable 5.1 di claude.ai dan aplikasi Claude.
  </Card>

  <Card title="Kartu sistem" icon="file" href="https://www.anthropic.com/claude-fable-5-1-mythos-5-1-system-card">
    Evaluasi keamanan dan keputusan deployment untuk Claude Fable 5.1 dan Claude Mythos 5.1.
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
