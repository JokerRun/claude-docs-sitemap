---
source: platform
url: https://platform.claude.com/docs/id/models/fable-5-1/overview
fetched_at: 2026-09-03T02:44:34.856042Z
sha256: 23c0ded8e098151e596604f45016f2640996c3baa11897001a20d888e7d07f81
---

---
title: Claude Fable 5.1
url: https://platform.claude.com/docs/id/models/fable-5-1/overview
description: "Sekilas tentang Claude Fable 5.1: kegunaannya, ID model di setiap platform, jendela konteks, batas output, harga, ketersediaan, dan sumber daya untuk membangun dengannya."
---

**Latest.** Released September 1, 2026.

For demanding reasoning and long-horizon agentic work

Model ID: `claude-fable-5-1`

Context window: 1M tokens · Max output: 128K tokens · Input pricing: $10 / MTok · Output pricing: $50 / MTok

[Announcement](https://www.anthropic.com/claude-fable-and-mythos-5-1) · [What’s new](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1) · [Migration guide](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide)

## Ikhtisar

Claude Fable 5.1 memperluas Claude Fable 5 dengan harga input dan output yang sama, dengan pembacaan cache seharga seperempat dari biaya sebelumnya, serta menghadirkan agentic coding jangka panjang yang lebih kuat, riset multilangkah, dan pekerjaan dokumen, spreadsheet, dan slide. Untuk sebagian besar beban kerja, mulailah dengan Claude Opus 5 (lihat [Memilih model](https://platform.claude.com/docs/id/about-claude/models/choosing-a-model)). Gunakan Claude Fable 5.1 untuk penalaran yang berat dan pekerjaan agentic berjangka panjang, atau ketika eval Anda pada Claude Opus 5 dengan effort lebih tinggi masih belum memadai. Claude Mythos 5.1 menawarkan kemampuan yang sama hanya untuk peserta [Project Glasswing](https://anthropic.com/glasswing).

Jika Anda sudah memanggil Claude Fable 5, ada tiga perubahan yang merusak kompatibilitas: [penggunaan alat paksa mengembalikan error](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#forced-tool-use-is-not-supported), [model sebelumnya tidak dapat membaca blok thinking-nya](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#thinking-blocks-are-tied-to-the-model-that-produced-them), dan [mengedit giliran sebelumnya membatalkan blok thinking](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#editing-earlier-turns-invalidates-thinking-blocks). Lima perubahan bersifat tambahan: [effort per pesan](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#change-effort-mid-conversation-beta) (beta), [pesan sistem dengan cakupan giliran](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#turn-scoped-system-messages-beta) (beta), [pembaruan progres yang dapat dibaca di antara pemanggilan alat](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#progress-updates-between-tool-calls-beta) (`display: "updates"`, beta), [harga pembacaan cache yang lebih rendah](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#pricing), dan [provenans konten](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#content-provenance).

[Yang baru di Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1)

## Claude Fable 5.1 dan Claude Mythos 5.1

[Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview) menawarkan kemampuan yang sama hanya melalui undangan, sebagai bagian dari [Project Glasswing](https://anthropic.com/glasswing). Model ini memiliki spesifikasi dan harga yang sama dengan Claude Fable 5.1. Untuk mendapatkan akses, hubungi tim akun Anthropic, AWS, atau Google Cloud Anda.

## Perbandingannya

| Model                                                                             | Context | Max output | Price / MTok | Latency  | Thinking             | Default effort | Knowledge cutoff |
| :-------------------------------------------------------------------------------- | :------ | :--------- | :----------- | :------- | :------------------- | :------------- | :--------------- |
| **Claude Fable 5.1** (this model)                                                 | 1M      | 128K       | $10 / $50    | Slower   | Adaptive (always on) | `high`         | Jun 2026         |
| [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview)       | 1M      | 128K       | $5 / $25     | Moderate | Adaptive             | `high`         | May 2026         |
| [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview)   | 1M      | 128K       | $2 / $10     | Fast     | Adaptive             | `high`         | Jan 2026         |
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

| Platform                                                                                               | Model ID                     |
| :----------------------------------------------------------------------------------------------------- | :--------------------------- |
| Claude API                                                                                             | `claude-fable-5-1`           |
| [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)       | `anthropic.claude-fable-5-1` |
| [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)              | `claude-fable-5-1`           |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | `claude-fable-5-1`           |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) | `claude-fable-5-1`           |

### Pricing

| Feature                                                                                | Value                                                               |
| :------------------------------------------------------------------------------------- | :------------------------------------------------------------------ |
| Input                                                                                  | $10 / MTok                                                          |
| Output                                                                                 | $50 / MTok                                                          |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $12.50 / MTok                                                       |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $20 / MTok                                                          |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $0.25 / MTok                                                        |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)    | 50% discount on input and output                                    |
| Full price list                                                                        | [Pricing](https://platform.claude.com/docs/id/about-claude/pricing) |

### Capabilities

| Feature                                                                                 | Value                  |
| :-------------------------------------------------------------------------------------- | :--------------------- |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows) | 1M tokens              |
| Max output                                                                              | 128K tokens            |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)              | Adaptive (always on)   |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)          | `high`                 |
| Comparative latency                                                                     | Slower                 |
| Input → output                                                                          | Text and images → text |
| Reliable knowledge cutoff                                                               | Jun 2026               |
| Training data cutoff                                                                    | Jun 2026               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                   |
| :---------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (latest)                                                                                                                                                                                                                                                                                                                                                                                                         |
| Released                                                                      | September 1, 2026                                                                                                                                                                                                                                                                                                                                                                                                       |
| Retirement                                                                    | Not sooner than September 1, 2027                                                                                                                                                                                                                                                                                                                                                                                       |
| Platforms                                                                     | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

## Sumber daya

<CardGroup cols={3}>
  <Card title="Prompting Claude Fable 5.1" icon="lightbulb" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1">
    Panduan prompting khusus model untuk pekerjaan jangka panjang dan agentik.
  </Card>

  <Card title="Migrasi ke Claude Fable 5.1" icon="arrow-right" href="https://platform.claude.com/docs/id/models/fable-5-1/migration-guide">
    Apa yang berubah saat Anda beralih dari Claude Fable 5, Claude Opus 5, atau Claude Opus 4.8.
  </Card>

  <Card title="Pemikiran yang dipertahankan" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-thinking">
    Kapan blok pemikiran model ini tetap dapat digunakan: lintas pergantian model dan lintas perubahan pada percakapan.
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

  <Card title="System card" icon="file" href="https://www.anthropic.com/claude-fable-5-1-mythos-5-1-system-card">
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
