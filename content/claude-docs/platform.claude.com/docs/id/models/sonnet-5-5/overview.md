---
source: platform
url: https://platform.claude.com/docs/id/models/sonnet-5-5/overview
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 3efefdac08f7a9897af7d58d70207a5b445c20a32e26c345b1b655e3c642babe
---

---
title: Claude Sonnet 5.5
url: https://platform.claude.com/docs/id/models/sonnet-5-5/overview
description: "Sekilas tentang Claude Sonnet 5.5: kegunaannya, ID model di setiap platform, jendela konteks, batas output, harga, ketersediaan, serta panduan dan sumber daya untuk membangun dengannya."
---

**Latest.** Released September 28, 2026.

The best combination of speed and intelligence

Model ID: `claude-sonnet-5-5`

Context window: 1M tokens · Max output: 128K tokens · Input pricing: $2 / MTok · Output pricing: $10 / MTok

[Announcement](https://www.anthropic.com/claude-sonnet-5-5) · [What’s new](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5) · [Migration guide](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide)

## Ikhtisar

Claude Sonnet 5.5 menawarkan kombinasi terbaik antara kecepatan dan kecerdasan. Lima "breaking change" (perubahan yang merusak kompatibilitas) memengaruhi kode yang sudah berjalan di Claude Sonnet 5:

* [Matikan pemikiran di awal dengan `between_tools`](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#turn-off-up-front-thinking).
* [Penggunaan alat paksa mengembalikan error](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#forced-tool-use-is-not-supported).
* [Blok pemikiran terikat pada model dan percakapan](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them).
* [Di Claude API dan Google Cloud, alat computer use `computer_20251124` yang lebih lama tidak diterima](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#computer-20251124-is-not-supported).
* [Alat advisor menolak Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5 sebagai advisor](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#advisor-tool-pairings).

Satu perubahan lagi mengubah bentuk respons tanpa menggagalkan permintaan apa pun: [teks di antara pemanggilan alat dikembalikan dalam blok `thinking`](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#text-between-tool-calls). Aplikasi yang melakukan streaming teks tersebut kepada penggunanya akan menjadi senyap di antara pemanggilan alat hingga aplikasi tersebut menetapkan nilai `display` yang mengembalikan teks, atau mematikan pemikiran di awal dengan `between_tools`.

[Yang baru di Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5)

## Perbandingan

| Model                                                                             | Context | Max output | Price / MTok       | Latency  | Thinking             | Default effort | Knowledge cutoff |
| :-------------------------------------------------------------------------------- | :------ | :--------- | :----------------- | :------- | :------------------- | :------------- | :--------------- |
| [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) | 1M      | 128K       | $10 / $50          | Slower   | Adaptive (always on) | `high`         | Jun 2026         |
| [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview)   | 1M      | 128K       | $4 / $20           | Moderate | Adaptive (always on) | `medium`       | Jun 2026         |
| **Claude Sonnet 5.5** (this model)                                                | 1M      | 128K       | $2 / $10           | Fast     | Adaptive             | `high`         | Jun 2026         |
| [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview) | 1M      | 128K       | From $0.10 / $0.50 | Fastest  | Adaptive             | `medium`       | Jun 2026         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Sonnet 5, Claude Haiku 5.5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price (2.5% on Claude Fable 5.1 and Claude Mythos 5.1, 5% on Claude Opus 5.5 and Claude Sonnet 5.5). See Pricing for the full list.
* **Latency:** Comparative latency, relative to the current lineup, as published in the models overview. Actual latency depends on prompt length, output length, and thinking effort.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual budget\_tokens mode on earlier models.
* **Default effort:** The effort parameter’s default on the Claude API. Models without a value don’t support the parameter.
* **Knowledge cutoff:** Reliable knowledge cutoff: the date through which the model’s knowledge is most extensive and reliable.

## Spesifikasi

### Model IDs

| Platform                                                                                               | Model ID                      |
| :----------------------------------------------------------------------------------------------------- | :---------------------------- |
| Claude API                                                                                             | `claude-sonnet-5-5`           |
| [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)       | `anthropic.claude-sonnet-5-5` |
| [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)              | `claude-sonnet-5-5`           |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | `claude-sonnet-5-5`           |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) | `claude-sonnet-5-5`           |

### Pricing

| Feature                                                                                | Value                            |
| :------------------------------------------------------------------------------------- | :------------------------------- |
| Input                                                                                  | $2 / MTok                        |
| Output                                                                                 | $10 / MTok                       |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $2.50 / MTok                     |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $4 / MTok                        |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $0.10 / MTok                     |
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
| Comparative latency                                                                                                         | Fast                   |
| Input → output                                                                                                              | Text and images → text |
| Reliable knowledge cutoff                                                                                                   | Jun 2026               |
| Training data cutoff                                                                                                        | Jun 2026               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                   |
| :---------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (latest)                                                                                                                                                                                                                                                                                                                                                                                                         |
| Released                                                                      | September 28, 2026                                                                                                                                                                                                                                                                                                                                                                                                      |
| Retirement                                                                    | Not sooner than September 28, 2027                                                                                                                                                                                                                                                                                                                                                                                      |
| Platforms                                                                     | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

## Hal yang perlu diketahui

* "Adaptive thinking" (pemikiran adaptif) aktif secara default. Pengaturan thinking terendah adalah `between_tools`, yang menonaktifkan thinking di awal. Pengaturan ini berfungsi pada effort `high` atau lebih rendah. Lihat [Yang baru di Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#turn-off-up-front-thinking).
* Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default akan menghasilkan error 400.
* Panjang prompt minimum yang dapat di-cache adalah 512 token. Lihat ["Prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations).
* Pada [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta), Claude Sonnet 5.5 mendukung hingga 300k token output dengan header beta `output-300k-2026-03-24`.
* Kueri batas dan kemampuan secara terprogram dengan [Models API](https://platform.claude.com/docs/id/api/models/list).

## Sumber daya

<CardGroup cols={3}>
  <Card title="Prompting Claude Sonnet 5.5" icon="lightbulb" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5">
    Perbedaan perilaku dan pola prompting yang khusus untuk Claude Sonnet 5.5.
  </Card>

  <Card title="Effort" icon="sliders" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kontrol untuk kedalaman thinking, "latency" (latensi), dan biaya. Pilih level untuk setiap beban kerja.
  </Card>

  <Card title="Pemikiran adaptif" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Cara kerja pemikiran adaptif, pengaturan thinking yang diterima setiap model, dan cara blok thinking dipertahankan.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="Prompt sistem" icon="text" href="https://platform.claude.com/docs/id/release-notes/system-prompts/claude-sonnet-5-5">
    Prompt sistem yang digunakan Claude Sonnet 5.5 di claude.ai dan aplikasi Claude.
  </Card>

  <Card title="System card" icon="file" href="https://www.anthropic.com/document/claude-sonnet-5-5-system-card">
    Evaluasi keamanan dan keputusan deployment untuk Claude Sonnet 5.5.
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
