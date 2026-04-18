---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/overview
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 6129335c960dcf393d870c784a7affd7016e35b7f0a378eb62ed51c396d6b977
---

# Ikhtisar model

Claude adalah keluarga model bahasa besar canggih yang dikembangkan oleh Anthropic. Panduan ini memperkenalkan model yang tersedia dan membandingkan kinerja mereka.

---

## Memilih model

Jika Anda tidak yakin model mana yang akan digunakan, pertimbangkan untuk memulai dengan **Claude Opus 4.7** untuk tugas-tugas paling kompleks. Ini adalah model yang paling mampu dan tersedia secara umum, dengan peningkatan lompatan dalam pengkodean agentic dibandingkan Claude Opus 4.6.

Semua model Claude saat ini mendukung input teks dan gambar, output teks, kemampuan multibahasa, dan visi. Model tersedia melalui Claude API, Amazon Bedrock, Vertex AI, dan Microsoft Foundry.

Setelah Anda memilih model, [pelajari cara membuat panggilan API pertama Anda](/docs/id/get-started).

### Perbandingan model terbaru

| Fitur | Claude Opus 4.7 | Claude Sonnet 4.6 | Claude Haiku 4.5 |
|:--------|:--------------|:------------------|:-----------------|
| **Deskripsi** | Model yang paling mampu tersedia secara umum untuk penalaran kompleks dan pengkodean agentic | Kombinasi terbaik dari kecepatan dan intelijen | Model tercepat dengan intelijen mendekati frontier |
| **Claude API ID** | claude-opus-4-7 | claude-sonnet-4-6 | claude-haiku-4-5-20251001 |
| **Claude API alias** | claude-opus-4-7 | claude-sonnet-4-6 | claude-haiku-4-5 |
| **AWS Bedrock ID** | anthropic.claude-opus-4-7<sup>3</sup> | anthropic.claude-sonnet-4-6 | anthropic.claude-haiku-4-5-20251001-v1:0 |
| **GCP Vertex AI ID** | claude-opus-4-7 | claude-sonnet-4-6 | claude-haiku-4-5@20251001 |
| **Harga**<sup>1</sup> | \$5 / input MTok<br/>\$25 / output MTok | \$3 / input MTok<br/>\$15 / output MTok | \$1 / input MTok<br/>\$5 / output MTok |
| **[Extended thinking](/docs/id/build-with-claude/extended-thinking)** | Tidak | Ya | Ya |
| **[Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking)** | Ya | Ya | Tidak |
| **[Priority Tier](/docs/id/api/service-tiers)** | Ya | Ya | Ya |
| **Latensi komparatif** | Sedang | Cepat | Tercepat |
| **Jendela konteks** | <Tooltip tooltipContent="~555k kata \ ~2.5M karakter unicode (Opus 4.7 menggunakan tokenizer baru)">1M token</Tooltip> | <Tooltip tooltipContent="~750k kata \ ~3.4M karakter unicode">1M token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> |
| **Output maksimal** | 128k token | 64k token | 64k token |
| **Cutoff pengetahuan yang andal** | Jan 2026<sup>2</sup> | Aug 2025<sup>2</sup> | Feb 2025 |
| **Cutoff data pelatihan** | Jan 2026 | Jan 2026 | Jul 2025 |

_<sup>1 - Lihat [halaman harga](/docs/id/about-claude/pricing) untuk informasi harga lengkap termasuk diskon Batch API, tingkat prompt caching, biaya extended thinking, dan biaya pemrosesan visi.</sup>_

_<sup>2 - **Cutoff pengetahuan yang andal** menunjukkan tanggal hingga mana pengetahuan model paling luas dan andal. **Cutoff data pelatihan** adalah rentang tanggal yang lebih luas dari data pelatihan yang digunakan. Untuk informasi lebih lanjut, lihat [Transparency Hub Anthropic](https://www.anthropic.com/transparency).</sup>_

_<sup>3 - Claude Opus 4.7 di AWS tersedia melalui [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock-research-preview), saat ini dalam pratinjau penelitian.</sup>_

<Info>
[Claude Mythos Preview](https://anthropic.com/glasswing) ditawarkan secara terpisah sebagai model pratinjau penelitian untuk alur kerja keamanan siber defensif sebagai bagian dari [Project Glasswing](https://anthropic.com/glasswing). Akses hanya dengan undangan dan tidak ada pendaftaran mandiri.
</Info>

<Note>Model dengan tanggal snapshot yang sama (misalnya, 20240620) identik di semua platform dan tidak berubah. Tanggal snapshot dalam nama model memastikan konsistensi dan memungkinkan pengembang mengandalkan kinerja stabil di berbagai lingkungan.</Note>

<Note>Dimulai dengan **Claude Sonnet 4.5 dan semua model berikutnya** (termasuk Claude Sonnet 4.6), AWS Bedrock menawarkan dua jenis endpoint: **endpoint global** (perutean dinamis untuk ketersediaan maksimal) dan **endpoint regional** (perutean data terjamin melalui wilayah geografis tertentu). Google Vertex AI menawarkan tiga jenis endpoint: endpoint global, **endpoint multi-region** (perutean dinamis dalam area geografis), dan endpoint regional. Untuk informasi lebih lanjut, lihat [bagian harga platform pihak ketiga](/docs/id/about-claude/pricing#third-party-platform-pricing).</Note>

<Tip>
Anda dapat menanyakan kemampuan model dan batas token secara terprogram dengan [Models API](/docs/id/api/models/list). Respons mencakup `max_input_tokens`, `max_tokens`, dan objek `capabilities` untuk setiap model yang tersedia.
</Tip>

<Note>
Nilai Max output di atas berlaku untuk Messages API sinkron. Pada [Message Batches API](/docs/id/build-with-claude/batch-processing#extended-output-beta), Opus 4.7, Opus 4.6, dan Sonnet 4.6 mendukung hingga 300k token output dengan menggunakan header beta `output-300k-2026-03-24`.
</Note>

<section title="Model warisan">

Model berikut masih tersedia. Pertimbangkan untuk bermigrasi ke model saat ini untuk kinerja yang ditingkatkan:

| Fitur | Claude Opus 4.6 | Claude Sonnet 4.5 | Claude Opus 4.5 | Claude Opus 4.1 | Claude Sonnet 4 (deprecated) | Claude Opus 4 (deprecated) | Claude Haiku 3 (deprecated) |
|:--------|:----------------|:------------------|:----------------|:----------------|:----------------|:--------------|:----------------------------|
| **Claude API ID** | claude-opus-4-6 | claude-sonnet-4-5-20250929 | claude-opus-4-5-20251101 | claude-opus-4-1-20250805 | claude-sonnet-4-20250514 | claude-opus-4-20250514 | claude-3-haiku-20240307 |
| **Claude API alias** | claude-opus-4-6 | claude-sonnet-4-5 | claude-opus-4-5 | claude-opus-4-1 | claude-sonnet-4-0 | claude-opus-4-0 | N/A |
| **AWS Bedrock ID** | anthropic.claude-opus-4-6-v1 | anthropic.claude-sonnet-4-5-20250929-v1:0 | anthropic.claude-opus-4-5-20251101-v1:0 | anthropic.claude-opus-4-1-20250805-v1:0 | anthropic.claude-sonnet-4-20250514-v1:0 | anthropic.claude-opus-4-20250514-v1:0 | anthropic.claude-3-haiku-20240307-v1:0 |
| **GCP Vertex AI ID** | claude-opus-4-6 | claude-sonnet-4-5@20250929 | claude-opus-4-5@20251101 | claude-opus-4-1@20250805 | claude-sonnet-4@20250514 | claude-opus-4@20250514 | claude-3-haiku@20240307 |
| **Harga** | \$5 / input MTok<br/>\$25 / output MTok | \$3 / input MTok<br/>\$15 / output MTok | \$5 / input MTok<br/>\$25 / output MTok | \$15 / input MTok<br/>\$75 / output MTok | \$3 / input MTok<br/>\$15 / output MTok | \$15 / input MTok<br/>\$75 / output MTok | \$0.25 / input MTok<br/>\$1.25 / output MTok |
| **[Extended thinking](/docs/id/build-with-claude/extended-thinking)** | Ya | Ya | Ya | Ya | Ya | Ya | Tidak |
| **[Priority Tier](/docs/id/api/service-tiers)** | Ya | Ya | Ya | Ya | Ya | Ya | Tidak |
| **Latensi komparatif** | Sedang | Cepat | Sedang | Sedang | Cepat | Sedang | Cepat |
| **Jendela konteks** | <Tooltip tooltipContent="~750k kata \ ~3.4M karakter unicode">1M token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> |
| **Output maksimal** | 128k token | 64k token | 64k token | 32k token | 64k token | 32k token | 4k token |
| **Cutoff pengetahuan yang andal** | May 2025<sup>1</sup> | Jan 2025<sup>1</sup> | May 2025<sup>1</sup> | Jan 2025<sup>1</sup> | Jan 2025<sup>1</sup> | Jan 2025<sup>1</sup> | <sup>2</sup> |
| **Cutoff data pelatihan** | Aug 2025 | Jul 2025 | Aug 2025 | Mar 2025 | Mar 2025 | Mar 2025 | Aug 2023 |

<Warning>
Claude Sonnet 4 (`claude-sonnet-4-20250514`) dan Claude Opus 4 (`claude-opus-4-20250514`) sudah usang dan akan dihentikan pada 15 Juni 2026. Bermigrasi ke [Claude Sonnet 4.6](/docs/id/about-claude/models/overview#latest-models-comparison) dan [Claude Opus 4.7](/docs/id/about-claude/models/overview#latest-models-comparison) masing-masing sebelum tanggal penghentian.

Claude Haiku 3 (`claude-3-haiku-20240307`) sudah usang dan akan dihentikan pada 19 April 2026. Bermigrasi ke [Claude Haiku 4.5](/docs/id/about-claude/models/overview#latest-models-comparison) sebelum tanggal penghentian.

Lihat [penghentian model](/docs/id/about-claude/model-deprecations) untuk detail.
</Warning>

_<sup>1 - **Cutoff pengetahuan yang andal** menunjukkan tanggal hingga mana pengetahuan model paling luas dan andal. **Cutoff data pelatihan** adalah rentang tanggal yang lebih luas dari data pelatihan yang digunakan.</sup>_

_<sup>2 - Beberapa model Haiku memiliki tanggal cutoff data pelatihan tunggal.</sup>_

</section>

## Kinerja prompt dan output

Model Claude 4 unggul dalam:
- **Kinerja**: Hasil tingkat atas dalam penalaran, pengkodean, tugas multibahasa, penanganan konteks panjang, kejujuran, dan pemrosesan gambar. Lihat [postingan blog Claude 4](http://www.anthropic.com/news/claude-4) untuk informasi lebih lanjut.
- **Respons yang menarik**: Model Claude ideal untuk aplikasi yang memerlukan interaksi yang kaya dan mirip manusia.

    - Jika Anda lebih suka respons yang lebih ringkas, Anda dapat menyesuaikan prompt Anda untuk memandu model menuju panjang output yang diinginkan. Lihat [panduan rekayasa prompt](/docs/id/build-with-claude/prompt-engineering) untuk detail.
    - Untuk praktik terbaik prompting, lihat [panduan praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).
- **Kualitas output**: Saat bermigrasi dari generasi model sebelumnya ke Claude 4, Anda mungkin akan melihat peningkatan yang lebih besar dalam kinerja keseluruhan.

## Bermigrasi ke Claude Opus 4.7

Jika Anda saat ini menggunakan Claude Opus 4.6 atau model Claude yang lebih lama, pertimbangkan untuk bermigrasi ke Claude Opus 4.7 untuk memanfaatkan intelijen yang ditingkatkan dan lompatan perubahan dalam pengkodean agentic. Untuk instruksi migrasi terperinci, lihat [Bermigrasi ke Claude Opus 4.7](/docs/id/about-claude/models/migration-guide).

## Mulai dengan Claude

Jika Anda siap untuk mulai menjelajahi apa yang dapat dilakukan Claude untuk Anda, selami! Baik Anda seorang pengembang yang ingin mengintegrasikan Claude ke dalam aplikasi Anda atau pengguna yang ingin mengalami kekuatan AI secara langsung, sumber daya berikut dapat membantu.

<Note>Ingin mengobrol dengan Claude? Kunjungi [claude.ai](http://www.claude.ai)!</Note>

<CardGroup cols={3}>
  <Card title="Intro to Claude" icon="check" href="/docs/id/intro">
    Jelajahi kemampuan Claude dan alur pengembangan.
  </Card>
  <Card title="Quickstart" icon="lightning" href="/docs/id/get-started">
    Pelajari cara membuat panggilan API pertama Anda dalam hitungan menit.
  </Card>
  <Card title="Claude Console" icon="code" href="/">
    Buat dan uji prompt yang kuat langsung di browser Anda.
  </Card>
</CardGroup>

Jika Anda memiliki pertanyaan atau memerlukan bantuan, jangan ragu untuk menghubungi [tim dukungan](https://support.claude.com/) atau konsultasikan [komunitas Discord](https://www.anthropic.com/discord).