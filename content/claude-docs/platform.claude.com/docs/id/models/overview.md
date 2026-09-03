---
source: platform
url: https://platform.claude.com/docs/id/models/overview
fetched_at: 2026-09-03T02:44:34.856042Z
sha256: 11a1a8f81d9f5b5f5f557cfca286c76a923e953f239da98df56c212a12f39e3e
---

---
title: Ikhtisar model
url: https://platform.claude.com/docs/id/models/overview
description: Claude adalah keluarga model bahasa besar mutakhir yang dikembangkan oleh Anthropic. Panduan ini memperkenalkan model-model yang tersedia dan membandingkan kinerjanya.
---

# Ikhtisar model

Claude adalah keluarga model bahasa besar mutakhir yang dikembangkan oleh Anthropic. Bandingkan jajaran model terkini, temukan ID model untuk setiap platform, dan buka halaman masing-masing model untuk melihat spesifikasi lengkap dan sumber dayanya.

<HomeQuickChip icon="Signpost" href="https://platform.claude.com/docs/id/about-claude/models/choosing-a-model">
  Memilih model
</HomeQuickChip>

<HomeQuickChip icon="DollarSign" href="https://platform.claude.com/docs/id/about-claude/pricing">
  Harga
</HomeQuickChip>

<HomeQuickChip icon="ArrowUpCircle" href="https://platform.claude.com/docs/id/about-claude/models/migration-guide">
  Panduan migrasi
</HomeQuickChip>

## Bandingkan model

Jika Anda tidak yakin model mana yang harus digunakan, mulailah dengan [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview) untuk sebagian besar beban kerja. Gunakan [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) untuk penalaran yang menuntut dan pekerjaan agentik berjangka panjang, atau ketika evaluasi Anda pada Claude Opus 5 dengan effort yang lebih tinggi masih belum memadai. Semua model terkini mendukung input teks dan gambar, output teks, kemampuan multibahasa, visi, dan "tool use" (penggunaan alat). Halaman setiap model mencantumkan platform tempat model tersebut tersedia.

| Feature                                                                                                   | Claude Fable 5.1                                                                  | Claude Opus 5                                                               | Claude Sonnet 5                                                                 | Claude Haiku 4.5                                                                  |
| :-------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------- | :-------------------------------------------------------------------------- | :------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------- |
| Description                                                                                               | For demanding reasoning and long-horizon agentic work                             | For complex agentic coding and enterprise work                              | The best combination of speed and intelligence                                  | The fastest model with near-frontier intelligence                                 |
| Model page                                                                                                | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) | [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview) | [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview) | [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/haiku-4-5/overview) |
| Comparative latency                                                                                       | Slower                                                                            | Moderate                                                                    | Fast                                                                            | Fastest                                                                           |
| [Pricing](https://platform.claude.com/docs/id/about-claude/pricing)                                       | $10 / input MTok, $50 / output MTok                                               | $5 / input MTok, $25 / output MTok                                          | $2 / input MTok, $10 / output MTok                                              | $1 / input MTok, $5 / output MTok                                                 |
| Claude API ID                                                                                             | `claude-fable-5-1`                                                                | `claude-opus-5`                                                             | `claude-sonnet-5`                                                               | `claude-haiku-4-5-20251001`                                                       |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)                                | Adaptive (always on)                                                              | Adaptive                                                                    | Adaptive                                                                        | Extended                                                                          |
| [Default effort](https://platform.claude.com/docs/id/build-with-claude/effort)                            | `high`                                                                            | `high`                                                                      | `high`                                                                          | Not supported                                                                     |
| [Context window](https://platform.claude.com/docs/id/build-with-claude/context-windows)                   | 1M tokens                                                                         | 1M tokens                                                                   | 1M tokens                                                                       | 200K tokens                                                                       |
| Max output                                                                                                | 128K tokens                                                                       | 128K tokens                                                                 | 128K tokens                                                                     | 64K tokens                                                                        |
| Reliable knowledge cutoff                                                                                 | Jun 2026                                                                          | May 2026                                                                    | Jan 2026                                                                        | Feb 2025                                                                          |
| Training data cutoff                                                                                      | Jun 2026                                                                          | May 2026                                                                    | Jan 2026                                                                        | Jul 2025                                                                          |
| [Retirement](https://platform.claude.com/docs/id/about-claude/model-deprecations)                         | Not sooner than September 1, 2027                                                 | Not sooner than July 24, 2027                                               | Not sooner than June 30, 2027                                                   | Not sooner than October 15, 2026                                                  |
| Claude API alias                                                                                          | `claude-fable-5-1`                                                                | `claude-opus-5`                                                             | `claude-sonnet-5`                                                               | `claude-haiku-4-5`                                                                |
| [Amazon Bedrock ID](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)       | `anthropic.claude-fable-5-1`                                                      | `anthropic.claude-opus-5`                                                   | `anthropic.claude-sonnet-5`                                                     | `anthropic.claude-haiku-4-5`                                                      |
| [Google Cloud ID](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)              | `claude-fable-5-1`                                                                | `claude-opus-5`                                                             | `claude-sonnet-5`                                                               | `claude-haiku-4-5@20251001`                                                       |
| [Microsoft Foundry ID](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | `claude-fable-5-1`                                                                | `claude-opus-5`                                                             | `claude-sonnet-5`                                                               | `claude-haiku-4-5`                                                                |
| [Claude Platform on AWS ID](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) | `claude-fable-5-1`                                                                | —                                                                           | `claude-sonnet-5`                                                               | `claude-haiku-4-5`                                                                |

* **Comparative latency:** Relative to the current lineup. Actual latency depends on prompt length, output length, and thinking effort.
* **Pricing:** Base price per million tokens. Batch API requests are 50% off; prompt cache reads cost 10% of the base input price (2.5% on Claude Fable 5.1 and Claude Mythos 5.1). See Pricing for cache writes, long-context, and per-platform pricing.
* **Claude API ID:** Every Claude model ID is a pinned snapshot, including the dateless IDs used from the 4.6 generation on.
* **Thinking:** Adaptive thinking lets the model decide how much to think, steered by effort. Extended thinking is the manual thinking.type “enabled” + budget\_tokens mode on earlier models; it is deprecated on Claude Opus 4.6 and Claude Sonnet 4.6 and not accepted on later models.
* **Default effort:** The effort parameter’s default on the Claude API. Set effort explicitly to use a different level.
* **Context window:** 1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer (introduced with Claude Opus 4.7); models before it fit about 750k words in 1M tokens. 200k tokens is roughly 150k words.
* **Max output:** Synchronous Messages API limit. On the Message Batches API, Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 support up to 300k output tokens with the output-300k-2026-03-24 beta header.
* **Reliable knowledge cutoff:** The date through which the model’s knowledge is most extensive and reliable. Training data cutoff (under Show all details) is the broader range of data used. See Anthropic’s Transparency Hub for details.
* **Retirement:** Anthropic’s commitment for Anthropic-operated platforms (Claude API, Claude Platform on AWS, Microsoft Foundry). Amazon Bedrock and Google Cloud set their own dates.
* **Claude API alias:** For models before the 4.6 generation, the alias is a convenience pointer that resolves to the dated ID. Dateless IDs are their own pinned snapshot; the alias row repeats them.
* **Amazon Bedrock ID:** The ID on Bedrock’s Messages-API endpoint (Claude Opus 4.7 and later, plus Claude Haiku 4.5); a model offered only through Bedrock’s InvokeModel integration shows that ID instead. Bedrock offers global endpoints (dynamic routing) and regional endpoints (guaranteed data routing) for Claude Sonnet 4.5 and later, and sets its own lifecycle dates.
* **Google Cloud ID:** Google Cloud offers global, multi-region, and regional endpoints, and sets its own lifecycle dates.
* **Microsoft Foundry ID:** Foundry deployments default to the Claude API model ID (the alias, where one exists); the deployment name is what you send. Foundry follows the Claude API lifecycle schedule.
* **Claude Platform on AWS ID:** Claude Platform on AWS uses the Claude API model IDs (the dateless form where the Claude API has an alias), not Bedrock-style IDs, and follows Anthropic’s first-party model lifecycle.

See [Model IDs and versioning](https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions) and [Pricing](https://platform.claude.com/docs/id/about-claude/pricing).

Legacy models (still available): [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview), [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-4-7/overview), [Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-4-6/overview), [Claude Opus 4.5](https://platform.claude.com/docs/id/models/opus-4-5/overview), [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-4-6/overview), [Claude Sonnet 4.5](https://platform.claude.com/docs/id/models/sonnet-4-5/overview).

Setelah Anda memilih model, [pelajari cara melakukan panggilan API pertama Anda](https://platform.claude.com/docs/id/get-started). Untuk memahami cara kerja ID model, alias, dan snapshot, lihat [ID model dan pembuatan versi](https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions); untuk batas pengetahuan andal dan batas data pelatihan di balik setiap model, lihat [Transparency Hub Anthropic](https://www.anthropic.com/transparency).

## Menggunakan Models API

Anda dapat mengkueri kemampuan model dan batas token secara terprogram dengan [Models API](https://platform.claude.com/docs/id/api/models/list). Responsnya mencakup `max_input_tokens`, `max_tokens`, dan objek `capabilities` untuk setiap model yang tersedia.

## Kinerja prompt dan output

Model Claude terkini unggul dalam:

* **Kinerja:** Hasil kelas atas dalam penalaran, pengodean, tugas multibahasa, penanganan konteks panjang, kejujuran, dan pemrosesan gambar. Lihat [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan prompting umum dan khusus model.
* **Respons yang menarik:** Model Claude ideal untuk aplikasi yang memerlukan interaksi yang kaya dan mirip manusia. Jika Anda lebih menyukai respons yang lebih ringkas, sesuaikan prompt Anda untuk mengarahkan model ke panjang output yang diinginkan. Lihat [panduan rekayasa prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering) untuk detailnya.
* **Kualitas output:** Saat bermigrasi dari generasi model sebelumnya, Anda mungkin melihat peningkatan yang lebih besar dalam kinerja secara keseluruhan. Jika Anda menggunakan Claude Opus 4.8 atau yang lebih lama, lihat [Bermigrasi ke Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/migration-guide).

## Mulai menggunakan Claude

Jika Anda siap untuk mulai menjelajahi apa yang dapat dilakukan Claude untuk Anda, mari mulai! Baik Anda seorang pengembang yang ingin mengintegrasikan Claude ke dalam aplikasi Anda maupun pengguna yang ingin merasakan langsung kekuatan AI, sumber daya berikut dapat membantu.

<CardGroup cols={3}>
  <Card title="Pengantar Claude" icon="check" href="https://platform.claude.com/docs/id/intro">
    Jelajahi kemampuan dan alur pengembangan Claude.
  </Card>

  <Card title="Mulai cepat" icon="lightning" href="https://platform.claude.com/docs/id/get-started">
    Pelajari cara melakukan panggilan API pertama Anda dalam hitungan menit.
  </Card>

  <Card title="Memilih model" icon="compass" href="https://platform.claude.com/docs/id/about-claude/models/choosing-a-model">
    Tetapkan kriteria dan pilih model yang tepat untuk kasus penggunaan Anda.
  </Card>

  <Card title="Harga" icon="coins" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Harga lengkap, termasuk diskon batch dan tarif caching prompt.
  </Card>

  <Card title="Penghentian model" icon="clock" href="https://platform.claude.com/docs/id/about-claude/model-deprecations">
    Status siklus hidup dan komitmen pemensiunan untuk setiap model.
  </Card>

  <Card title="Claude Console" icon="code" href="https://platform.claude.com/">
    Buat dan uji prompt langsung di browser Anda.
  </Card>
</CardGroup>

Ingin mengobrol dengan Claude? Kunjungi [claude.ai](https://claude.ai). Jika Anda memiliki pertanyaan, hubungi [tim dukungan](https://support.claude.com/) atau [komunitas Discord](https://www.anthropic.com/discord).
