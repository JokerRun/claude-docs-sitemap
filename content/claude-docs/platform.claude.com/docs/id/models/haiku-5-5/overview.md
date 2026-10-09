---
source: platform
url: https://platform.claude.com/docs/id/models/haiku-5-5/overview
fetched_at: 2026-10-09T02:29:51.005508Z
sha256: 126e849d662f5fc5b70a6adf1c5bc4a37c777e13758e5ef6f1aeaae9ff4218fd
---

---
title: Claude Haiku 5.5
url: https://platform.claude.com/docs/id/models/haiku-5-5/overview
description: "Sekilas tentang Claude Haiku 5.5: kegunaannya, ID model di setiap platform, jendela konteks, batas output, harga, ketersediaan, serta panduan dan sumber daya untuk membangun dengannya."
---

**Latest.** Released October 7, 2026.

For high-volume, latency-sensitive tasks such as classification, extraction, and routing

Model ID: `claude-haiku-5-5`

Context window: 1M tokens · Max output: 128K tokens · Input pricing: From $0.10 / MTok · Output pricing: From $0.50 / MTok

[Announcement](https://www.anthropic.com/claude-haiku-5-5) · [What’s new](https://platform.claude.com/docs/id/models/haiku-5-5/whats-new-haiku-5-5) · [Migration guide](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide)

## Ikhtisar

Claude Haiku 5.5 dibuat untuk pekerjaan bervolume tinggi yang sensitif terhadap "latency" (latensi) seperti klasifikasi, perutean, ekstraksi, dan tugas subagen. Model ini mendukung "adaptive thinking" (pemikiran adaptif) dengan parameter effort, "context window" (jendela konteks) 1M token, dan hingga 128k token output. Model ini menggunakan tokenizer baru yang sama dengan Claude 4.7 dan model-model setelahnya, sehingga teks yang sama dihitung sebagai sekitar 30% lebih banyak token dibandingkan pada Claude Haiku 4.5. Blok pemikirannya hanya berfungsi di akun yang menghasilkannya, atau di akun yang terhubung dengannya.

Untuk perubahan kode, lihat [panduan migrasi](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide). Untuk ID model, harga, dan batasan, lihat [ikhtisar Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview). Untuk panduan prompting, lihat [Prompting Claude Haiku 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5).

[Yang baru di Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/whats-new-haiku-5-5)

## Perbandingannya

| Model                                                                               | Context | Max output | Price / MTok       | Latency  | Thinking             | Default effort | Knowledge cutoff |
| :---------------------------------------------------------------------------------- | :------ | :--------- | :----------------- | :------- | :------------------- | :------------- | :--------------- |
| [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview)   | 1M      | 128K       | $10 / $50          | Slower   | Adaptive (always on) | `high`         | Jun 2026         |
| [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview)     | 1M      | 128K       | $4 / $20           | Moderate | Adaptive (always on) | `medium`       | Jun 2026         |
| [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview) | 1M      | 128K       | $2 / $10           | Fast     | Adaptive             | `high`         | Jun 2026         |
| **Claude Haiku 5.5** (this model)                                                   | 1M      | 128K       | From $0.10 / $0.50 | Fastest  | Adaptive             | `medium`       | Jun 2026         |

* **Context:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Sonnet 5, Claude Haiku 5.5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Price / MTok:** Input / output, base price per million tokens. Batch API requests are 50% off; prompt caching reads cost 10% of the base input price (2.5% on Claude Fable 5.1 and Claude Mythos 5.1, 5% on Claude Opus 5.5 and Claude Sonnet 5.5). See Pricing for the full list.
* **Latency:** Comparative latency, relative to the current lineup, as published in the models overview. Actual latency depends on prompt length, output length, and thinking effort.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual budget\_tokens mode on earlier models.
* **Default effort:** The effort parameter’s default on the Claude API. Models without a value don’t support the parameter.
* **Knowledge cutoff:** Reliable knowledge cutoff: the date through which the model’s knowledge is most extensive and reliable.

## Spesifikasi

### Model IDs

| Platform                                                                                               | Model ID                     |
| :----------------------------------------------------------------------------------------------------- | :--------------------------- |
| Claude API                                                                                             | `claude-haiku-5-5`           |
| [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)       | `anthropic.claude-haiku-5-5` |
| [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)              | `claude-haiku-5-5`           |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | `claude-haiku-5-5`           |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) | `claude-haiku-5-5`           |

### Pricing

| Feature                                                                                | Value                                                                                         |
| :------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| Input                                                                                  | $0.10 / MTok for prompts up to 100,000 tokens; $0.50 / MTok for prompts over 100,000 tokens   |
| Output                                                                                 | $0.50 / MTok for prompts up to 100,000 tokens; $2.50 / MTok for prompts over 100,000 tokens   |
| [5m cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $0.125 / MTok for prompts up to 100,000 tokens; $0.625 / MTok for prompts over 100,000 tokens |
| [1h cache write](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) | $0.20 / MTok for prompts up to 100,000 tokens; $1 / MTok for prompts over 100,000 tokens      |
| [Cache read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)     | $0.01 / MTok for prompts up to 100,000 tokens; $0.05 / MTok for prompts over 100,000 tokens   |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)    | 50% discount on input and output                                                              |

[Full price list](https://platform.claude.com/docs/id/about-claude/pricing)

### Capabilities

| Feature                                                                                                                     | Value                  |
| :-------------------------------------------------------------------------------------------------------------------------- | :--------------------- |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows)                                     | 1M tokens              |
| Max output                                                                                                                  | 128K tokens            |
| [Max output (Batch API, beta)](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta) | 300K tokens            |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)                                                  | Adaptive               |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)                                              | `medium`               |
| Comparative latency                                                                                                         | Fastest                |
| Input → output                                                                                                              | Text and images → text |
| Reliable knowledge cutoff                                                                                                   | Jun 2026               |
| Training data cutoff                                                                                                        | Jun 2026               |

### Availability

| Feature                                                                       | Value                                                                                                                                                                                                                                                                                                                                                                                                                   |
| :---------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Status](https://platform.claude.com/docs/id/about-claude/model-deprecations) | Active (latest)                                                                                                                                                                                                                                                                                                                                                                                                         |
| Released                                                                      | October 7, 2026                                                                                                                                                                                                                                                                                                                                                                                                         |
| Retirement                                                                    | Not sooner than October 7, 2027                                                                                                                                                                                                                                                                                                                                                                                         |
| Platforms                                                                     | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

## Hal yang perlu diketahui

* "Adaptive thinking" (pemikiran adaptif) aktif secara default. Kendalikan kedalaman pemikiran dengan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort).
* Hilangkan `temperature`, `top_p`, dan `top_k`, karena nilai non-default untuk salah satunya akan mengembalikan error 400.
* Pada [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta), Claude Haiku 5.5 mendukung hingga 300k token output dengan beta header `output-300k-2026-03-24`.
* Kueri batas dan kemampuan secara terprogram dengan [Models API](https://platform.claude.com/docs/id/api/models/list).

## Sumber daya

<CardGroup cols={3}>
  <Card title="Prompting Claude Haiku 5.5" icon="lightbulb" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5">
    Perbedaan perilaku dan pola prompting yang khusus untuk Claude Haiku 5.5.
  </Card>

  <Card title="Mengurangi latensi" icon="lightning" href="https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/reduce-latency">
    Pilih model dan tingkat effort, bentuk prompt, dan lakukan streaming output untuk respons yang lebih cepat.
  </Card>

  <Card title="Pemikiran adaptif" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Claude Haiku 5.5 menentukan kapan dan seberapa banyak berpikir. Arahkan kedalamannya dengan `effort`.
  </Card>

  <Card title="Jendela konteks" icon="stack" href="https://platform.claude.com/docs/id/build-with-claude/context-windows">
    1M token. Cara jendela dihitung dan dikelola.
  </Card>
</CardGroup>

## Referensi

<CardGroup cols={3}>
  <Card title="Prompt sistem" icon="text" href="https://platform.claude.com/docs/id/release-notes/system-prompts/claude-haiku-5-5">
    Prompt sistem yang digunakan Claude Haiku 5.5 di claude.ai dan aplikasi Claude.
  </Card>

  <Card title="System card" icon="file" href="https://www.anthropic.com/document/claude-haiku-5-5-system-card">
    Evaluasi keamanan dan keputusan deployment untuk Claude Haiku 5.5.
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
