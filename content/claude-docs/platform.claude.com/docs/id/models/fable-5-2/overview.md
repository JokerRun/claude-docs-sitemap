---
source: platform
url: https://platform.claude.com/docs/id/models/fable-5-2/overview
fetched_at: 2026-11-12T02:13:38.637181Z
sha256: 0e0ce123e15f6007950fb4d75b6b9dd51352de056d8ea6fa22079a60503a6d3c
---

---
title: Claude Fable 5.2
url: https://platform.claude.com/docs/id/models/fable-5-2/overview
description: "Ikhtisar Claude Fable 5.2: kegunaannya, ID model di setiap platform, jendela konteks, batas output, harga, ketersediaan, dan sumber daya untuk membangun dengannya."
---

**Latest.** Released November 9, 2026.

For demanding reasoning and long-horizon agentic work

Model ID: `claude-fable-5-2`

Context window: 1M tokens · Max output: 128K tokens · Input pricing: $8 / MTok · Output pricing: $40 / MTok

[Announcement](https://www.anthropic.com/claude-fable-and-mythos-5-2) · [What’s new](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2) · [Migration guide](https://platform.claude.com/docs/id/models/fable-5-2/migration-guide)

## Ikhtisar

Claude Fable 5.2 dirancang untuk penalaran yang menuntut dan pekerjaan agentik jangka panjang. Penggunaan umumnya mencakup sesi agen yang berjalan selama berjam-jam, riset mendalam multilangkah, dan analisis yang dikerjakan hingga menjadi dokumen, spreadsheet, atau deck yang selesai.

## Claude Fable 5.2 dan Claude Mythos 5.2

[Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview) menawarkan kemampuan yang sama hanya kepada organisasi yang telah diverifikasi melalui program verifikasi Anthropic, seperti [Cyber Verification Program](https://support.claude.com/en/articles/14604842). Model ini memiliki spesifikasi dan harga yang sama dengan Claude Fable 5.2. Untuk meminta akses, ajukan permohonan ke program yang mencakup kasus penggunaan Anda, atau hubungi tim akun Anda.

## Perbandingannya

| Model                                                                               | Context | Max output | Price / MTok       | Latency  | Thinking             | Default effort | Knowledge cutoff |
| :---------------------------------------------------------------------------------- | :------ | :--------- | :----------------- | :------- | :------------------- | :------------- | :--------------- |
| **Claude Fable 5.2** (this model)                                                   | 1M      | 128K       | $8 / $40           | Moderate | Adaptive (always on) | `high`         | Jun 2026         |
| [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview)     | 1M      | 128K       | $4 / $20           | Moderate | Adaptive (always on) | `medium`       | Jun 2026         |
| [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview) | 1M      | 128K       | $2 / $10           | Fast     | Adaptive             | `high`         | Jun 2026         |
| [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview)   | 1M      | 128K       | From $0.10 / $0.50 | Fastest  | Adaptive             | `medium`       | Jun 2026         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Sonnet 5, Claude Haiku 5.5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price (2.5% on Claude Fable 5.2, Claude Mythos 5.2, Claude Fable 5.1, and Claude Mythos 5.1, 5% on Claude Opus 5.5 and Claude Sonnet 5.5). See Pricing for the full list.
* **Latency:** Comparative latency, relative to the current lineup, as published in the models overview. Actual latency depends on prompt length, output length, and thinking effort.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual budget\_tokens mode on earlier models.
* **Default effort:** The effort parameter’s default on the Claude API. Models without a value don’t support the parameter.
* **Knowledge cutoff:** Reliable knowledge cutoff: the date through which the model’s knowledge is most extensive and reliable.

## Spesifikasi

### Model IDs

| Platform                                                                                                                                                   | Model ID                            |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------- |
| Claude API                                                                                                                                                 | `claude-fable-5-2`                  |
| [Amazon Bedrock (bedrock-runtime)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)                                  | `global.anthropic.claude-fable-5-2` |
| [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed)       | `claude-fable-5-2`                  |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)                                                     | `claude-fable-5-2`                  |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)                                                     | `claude-fable-5-2`                  |
| [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) | `claude-fable-5-2`                  |

### Pricing

| Feature                                                                                | Value                            |
| :------------------------------------------------------------------------------------- | :------------------------------- |
| Input                                                                                  | $8 / MTok                        |
| Output                                                                                 | $40 / MTok                       |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $10 / MTok                       |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $16 / MTok                       |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $0.20 / MTok                     |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)    | 50% discount on input and output |

[Full price list](https://platform.claude.com/docs/id/about-claude/pricing)

### Capabilities

| Feature                                                                                 | Value                  |
| :-------------------------------------------------------------------------------------- | :--------------------- |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows) | 1M tokens              |
| Max output                                                                              | 128K tokens            |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)              | Adaptive (always on)   |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)          | `high`                 |
| Comparative latency                                                                     | Moderate               |
| Input → output                                                                          | Text and images → text |
| Reliable knowledge cutoff                                                               | Jun 2026               |
| Training data cutoff                                                                    | Jun 2026               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| :---------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (latest)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Released                                                                      | November 9, 2026                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Retirement                                                                    | Not sooner than November 9, 2027                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Platforms                                                                     | Claude API, [Amazon Bedrock (bedrock-runtime)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) |

## Hal yang perlu diketahui

* “Adaptive thinking” (pemikiran adaptif) selalu aktif dan tidak dapat dinonaktifkan. Kendalikan kedalaman pemikiran dengan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort).
* “Forced tool use” (penggunaan alat yang dipaksakan) (`tool_choice` dengan tipe `any` dan `tool`) mengembalikan error 400. Lihat [Thinking dan pilihan alat](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#thinking-and-tool-choice).
* Hilangkan `temperature`, `top_p`, dan `top_k`. Lihat [Parameter sampling](https://platform.claude.com/docs/id/build-with-claude/thinking#sampling-parameters) untuk nilai-nilai yang mengembalikan error 400.
* Claude Fable 5.2 memerlukan retensi data 30 hari dan tidak tersedia dengan “zero data retention” (retensi data nol) kecuali diizinkan secara tegas oleh Anthropic. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Kueri batas dan kemampuan secara terprogram dengan [Models API](https://platform.claude.com/docs/id/api/models/list).

## Sumber daya

<CardGroup cols={3}>
  <Card title="Prompting Claude Fable 5.2" icon="lightbulb" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2">
    Perbedaan perilaku dan pola prompting yang khusus untuk Claude Fable 5.2.
  </Card>

  <Card title="Panduan migrasi Claude Fable 5.2" icon="arrow-right" href="https://platform.claude.com/docs/id/models/fable-5-2/migration-guide">
    Apa yang berubah saat Anda beralih dari Claude Fable 5.1 atau dari model Claude Opus.
  </Card>

  <Card title="Pemikiran yang dipertahankan" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking">
    Mengedit giliran sebelumnya membatalkan blok pemikiran, untuk setiap akun.
  </Card>

  <Card title="Pemikiran adaptif" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Cara kerja pemikiran adaptif. Ini adalah satu-satunya mode pemikiran pada Claude Fable 5.2.
  </Card>

  <Card title="Effort" icon="sliders" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kontrol untuk kedalaman pemikiran, latensi, dan biaya. Pilih level untuk setiap beban kerja.
  </Card>

  <Card title="Penolakan dan fallback" icon="shield" href="https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback">
    Tangani penolakan classifier dan coba lagi pada model Claude lain.
  </Card>

  <Card title="Mode cepat" icon="lightning" href="https://platform.claude.com/docs/id/build-with-claude/fast-mode">
    Output yang lebih cepat dari Claude Fable 5.2 dalam permintaan Messages API, dengan harga premium.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="Prompt sistem" icon="text" href="https://platform.claude.com/docs/id/release-notes/system-prompts/claude-fable-5-2">
    Prompt sistem yang digunakan Claude Fable 5.2 di claude.ai dan aplikasi Claude.
  </Card>

  <Card title="System card" icon="file" href="https://www.anthropic.com/document/claude-fable-5-2-mythos-5-2-system-card">
    Evaluasi keamanan dan keputusan deployment untuk Claude Fable 5.2 dan Claude Mythos 5.2.
  </Card>

  <Card title="Harga" icon="coins" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Daftar harga lengkap, termasuk diskon batch dan tarif caching prompt.
  </Card>

  <Card title="ID model dan pembuatan versi" icon="fingerprint" href="https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions">
    Cara kerja ID model, alias, dan snapshot yang dipatok.
  </Card>

  <Card title="Penghentian model" icon="clock" href="https://platform.claude.com/docs/id/about-claude/model-deprecations">
    Status siklus hidup dan komitmen penghentian untuk setiap model Claude.
  </Card>
</CardGroup>
