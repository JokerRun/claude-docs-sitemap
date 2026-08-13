---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/overview
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 13f6100e172230b83fbc4e62d1c588d14b2141066d1333c30e71120ad3099da6
---

---
title: Ikhtisar model
url: https://platform.claude.com/docs/id/about-claude/models/overview
description: Claude adalah keluarga model bahasa besar mutakhir yang dikembangkan oleh Anthropic. Panduan ini memperkenalkan model-model yang tersedia dan membandingkan kinerjanya.
---

## Memilih model

Jika Anda tidak yakin model mana yang akan digunakan, mulailah dengan **Claude Opus 5** untuk pengodean agentik yang kompleks dan pekerjaan enterprise. Untuk beban kerja yang membutuhkan kapabilitas tertinggi yang tersedia, gunakan [Claude Fable 5](https://platform.claude.com/docs/id/about-claude/models/overview#claude-fable-5-and-claude-mythos-5).

Semua model Claude saat ini mendukung input teks dan gambar, output teks, kemampuan multibahasa, dan vision. Model tersedia melalui Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry).

Setelah Anda memilih model, [pelajari cara melakukan panggilan API pertama Anda](https://platform.claude.com/docs/id/get-started).

### Claude Fable 5 dan Claude Mythos 5

Claude Fable 5 (`claude-fable-5`) adalah model Anthropic paling mumpuni yang dirilis secara luas. Claude Mythos 5 (`claude-mythos-5`) memiliki spesifikasi dan harga yang sama dengan Claude Fable 5 dan bergabung dengan Claude Mythos Preview (`claude-mythos-preview`) yang hanya tersedia melalui undangan dalam [Project Glasswing](https://anthropic.com/glasswing). Lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) untuk detail peluncuran dan perubahan API.

Claude Fable 5 tersedia secara umum di Claude API, Amazon Bedrock, Claude Platform on AWS, Google Cloud, dan Microsoft Foundry mulai 9 Juni 2026. Claude Mythos 5 tidak tersedia secara umum: model ini ditawarkan dalam ketersediaan terbatas kepada pelanggan yang disetujui dalam [Project Glasswing](https://anthropic.com/glasswing), mulai pada hari yang sama. Untuk mendapatkan akses, hubungi tim akun Anthropic, AWS, atau Google Cloud Anda.

### Perbandingan model terbaru

| Fitur                                                                                                                              | Claude Fable 5                                                                                                                                                                                                                                                                                                                            | Claude Opus 5                                                                                | Claude Sonnet 5                                                                              | Claude Haiku 4.5                                                                               |
| ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Deskripsi**                                                                                                                      | Kecerdasan generasi berikutnya untuk agen yang berjalan lama                                                                                                                                                                                                                                                                              | Untuk pengodean agentik yang kompleks dan pekerjaan enterprise                               | Kombinasi terbaik antara kecepatan dan kecerdasan                                            | Model tercepat dengan kecerdasan mendekati frontier                                            |
| **ID Claude API**                                                                                                                  | claude-fable-5                                                                                                                                                                                                                                                                                                                            | claude-opus-5                                                                                | claude-sonnet-5                                                                              | claude-haiku-4-5-20251001                                                                      |
| **Alias Claude API**                                                                                                               | claude-fable-5                                                                                                                                                                                                                                                                                                                            | claude-opus-5                                                                                | claude-sonnet-5                                                                              | claude-haiku-4-5                                                                               |
| **ID AWS Bedrock**                                                                                                                 | anthropic.claude-fable-53                                                                                                                                                                                                                                                                                                                 | anthropic.claude-opus-53                                                                     | anthropic.claude-sonnet-53                                                                   | anthropic.claude-haiku-4-5-20251001-v1:0                                                       |
| **ID Google Cloud**                                                                                                                | claude-fable-5                                                                                                                                                                                                                                                                                                                            | claude-opus-5                                                                                | claude-sonnet-5                                                                              | claude-haiku-4-5\@20251001                                                                     |
| **Harga**1                                                                                                                         | $10 / input MTok $50 / output MTok                                                                                                                                                                                                                                                                                                        | $5 / input MTok $25 / output MTok                                                            | $2 / input MTok $10 / output MTok                                                            | $1 / input MTok $5 / output MTok                                                               |
| **[Pemikiran diperpanjang (`thinking.type: "enabled"`)](https://platform.claude.com/docs/id/build-with-claude/extended-thinking)** | Tidak                                                                                                                                                                                                                                                                                                                                     | Tidak                                                                                        | Tidak                                                                                        | Ya                                                                                             |
| **[Pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking)**                                            | Ya (selalu aktif)                                                                                                                                                                                                                                                                                                                         | Ya                                                                                           | Ya                                                                                           | Tidak                                                                                          |
| **Latensi komparatif**                                                                                                             | Lebih lambat                                                                                                                                                                                                                                                                                                                              | Sedang                                                                                       | Cepat                                                                                        | Tercepat                                                                                       |
| **Jendela konteks**                                                                                                                | <Tooltip tooltipContent="~555 ribu kata \ ~2,5 juta karakter unicode. Claude Fable 5 menggunakan tokenizer yang diperkenalkan dengan Claude Opus 4.7; dibandingkan dengan model sebelum Claude Opus 4.7, teks yang sama menghasilkan sekitar 30% lebih banyak token. Peningkatan pastinya bergantung pada konten.">1 juta token</Tooltip> | <Tooltip tooltipContent="~555 ribu kata \ ~2,5 juta karakter unicode">1 juta token</Tooltip> | <Tooltip tooltipContent="~555 ribu kata \ ~2,5 juta karakter unicode">1 juta token</Tooltip> | <Tooltip tooltipContent="~150 ribu kata \ ~680 ribu karakter unicode">200 ribu token</Tooltip> |
| **Output maksimum**                                                                                                                | 128 ribu token                                                                                                                                                                                                                                                                                                                            | 128 ribu token                                                                               | 128 ribu token                                                                               | 64 ribu token                                                                                  |
| **Batas pengetahuan andal**                                                                                                        | Jan 20262                                                                                                                                                                                                                                                                                                                                 | Mei 20262                                                                                    | Jan 20262                                                                                    | Feb 2025                                                                                       |
| **Batas data pelatihan**                                                                                                           | Jan 2026                                                                                                                                                                                                                                                                                                                                  | Mei 2026                                                                                     | Jan 2026                                                                                     | Jul 2025                                                                                       |

*1 Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk informasi harga lengkap termasuk diskon Batch API dan tarif caching prompt.*

*2 **Batas pengetahuan andal** menunjukkan tanggal hingga kapan pengetahuan model paling luas dan andal. **Batas data pelatihan** adalah rentang tanggal yang lebih luas dari data pelatihan yang digunakan. Untuk informasi lebih lanjut, lihat [Transparency Hub Anthropic](https://www.anthropic.com/transparency).*

*3 Claude Fable 5, Claude Opus 5, dan Claude Sonnet 5 tersedia di Bedrock melalui [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) (endpoint Bedrock Messages-API).*

<Info>
  Claude Mythos 5 dan Claude Mythos Preview ditawarkan secara terpisah untuk alur kerja keamanan siber defensif sebagai bagian dari [Project Glasswing](https://anthropic.com/glasswing). Akses hanya melalui undangan dan tidak ada pendaftaran mandiri.
</Info>

<Note>
  Setiap ID model Claude adalah snapshot yang dipatok. Model dengan tanggal dalam ID-nya (misalnya, 

  `20250929`

  ) dipatok ke rilis spesifik tersebut. Mulai dari generasi Claude 4.6, ID model menggunakan format tanpa tanggal yang juga merupakan snapshot yang dipatok, bukan pointer yang selalu diperbarui. Untuk model sebelum generasi 4.6, entri di kolom alias Claude API adalah pointer kemudahan yang mengarah ke ID model bertanggal. Untuk detail tentang konvensi penamaan dan cara kerja versioning, lihat 

  [ID Model dan versioning](https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions)

  .
</Note>

<Note>
  Mulai dari 

  **Claude Sonnet 4.5 dan semua model berikutnya**

   (termasuk Claude Sonnet 4.6), Bedrock menawarkan dua jenis endpoint: 

  **endpoint global**

   (routing dinamis untuk ketersediaan maksimum) dan 

  **endpoint regional**

   (routing data yang dijamin melalui wilayah geografis tertentu). Google Cloud menawarkan tiga jenis endpoint: endpoint global, 

  **endpoint multi-region**

   (routing dinamis dalam area geografis), dan endpoint regional. Untuk informasi lebih lanjut, lihat 

  [Harga platform cloud](https://platform.claude.com/docs/id/about-claude/pricing#cloud-platform-pricing)

  .
</Note>

<Note>
  **Claude Platform on AWS**

   menggunakan ID model yang sama dengan Claude API (misalnya, 

  `claude-opus-4-6`

  ), bukan ID bergaya Bedrock. Siklus hidup model di Claude Platform on AWS mengikuti 

  [Deprekasi model](https://platform.claude.com/docs/id/about-claude/model-deprecations)

   pihak pertama Anthropic, bukan milik Bedrock. Lihat 

  [Model yang tersedia](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#available-models)

   untuk daftar model.
</Note>

<Tip>
  Anda dapat melakukan kueri kapabilitas model dan batas token secara terprogram dengan [Models API](https://platform.claude.com/docs/id/api/models/list). Respons mencakup `max_input_tokens`, `max_tokens`, dan objek `capabilities` untuk setiap model yang tersedia.
</Tip>

<Note>
  Pada Claude Opus 4.8, parameter `effort` secara default diatur ke `high` di semua permukaan, termasuk Claude API, Claude Code, dan claude.ai. Pada Claude Opus 5 dan Claude Sonnet 5, parameter ini secara default diatur ke `high` di Claude API dan Claude Code. Atur `effort` secara eksplisit untuk menggunakan level yang berbeda. Lihat [Effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk panduan memilih level.
</Note>

<Note>
  Nilai output maksimum dalam tabel berlaku untuk Messages API sinkron. Pada [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta), Claude Opus 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 5, dan Sonnet 4.6 mendukung hingga 300 ribu token output dengan menggunakan header beta `output-300k-2026-03-24`.
</Note>

<AccordionGroup>
  <Accordion title="Model lama">
    Model-model berikut masih tersedia. Pertimbangkan untuk bermigrasi ke model saat ini untuk kinerja yang lebih baik:

    | Fitur                                                                                                                              | Claude Opus 4.8                                                                              | Claude Opus 4.7                                                                                                                    | Claude Opus 4.6                                                                              | Claude Sonnet 4.6                                                                            | Claude Sonnet 4.5                                                                              | Claude Opus 4.5                                                                                |
    | ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
    | **ID Claude API**                                                                                                                  | claude-opus-4-8                                                                              | claude-opus-4-7                                                                                                                    | claude-opus-4-6                                                                              | claude-sonnet-4-6                                                                            | claude-sonnet-4-5-20250929                                                                     | claude-opus-4-5-20251101                                                                       |
    | **Alias Claude API**                                                                                                               | claude-opus-4-8                                                                              | claude-opus-4-7                                                                                                                    | claude-opus-4-6                                                                              | claude-sonnet-4-6                                                                            | claude-sonnet-4-5                                                                              | claude-opus-4-5                                                                                |
    | **ID AWS Bedrock**                                                                                                                 | anthropic.claude-opus-4-86                                                                   | anthropic.claude-opus-4-76                                                                                                         | anthropic.claude-opus-4-6-v1                                                                 | anthropic.claude-sonnet-4-6                                                                  | anthropic.claude-sonnet-4-5-20250929-v1:0                                                      | anthropic.claude-opus-4-5-20251101-v1:0                                                        |
    | **ID Google Cloud**                                                                                                                | claude-opus-4-8                                                                              | claude-opus-4-7                                                                                                                    | claude-opus-4-6                                                                              | claude-sonnet-4-6                                                                            | claude-sonnet-4-5\@20250929                                                                    | claude-opus-4-5\@20251101                                                                      |
    | **Harga**                                                                                                                          | $5 / input MTok $25 / output MTok                                                            | $5 / input MTok $25 / output MTok                                                                                                  | $5 / input MTok $25 / output MTok                                                            | $3 / input MTok $15 / output MTok                                                            | $3 / input MTok $15 / output MTok                                                              | $5 / input MTok $25 / output MTok                                                              |
    | **[Pemikiran diperpanjang (`thinking.type: "enabled"`)](https://platform.claude.com/docs/id/build-with-claude/extended-thinking)** | Tidak                                                                                        | Tidak                                                                                                                              | Ya (tidak digunakan lagi)                                                                    | Ya (tidak digunakan lagi)                                                                    | Ya                                                                                             | Ya                                                                                             |
    | **[Pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking)**                                            | Ya                                                                                           | Ya                                                                                                                                 | Ya                                                                                           | Ya                                                                                           | Tidak                                                                                          | Tidak                                                                                          |
    | **Latensi komparatif**                                                                                                             | Sedang                                                                                       | Sedang                                                                                                                             | Sedang                                                                                       | Cepat                                                                                        | Cepat                                                                                          | Sedang                                                                                         |
    | **Jendela konteks**                                                                                                                | <Tooltip tooltipContent="~555 ribu kata \ ~2,5 juta karakter unicode">1 juta token</Tooltip> | <Tooltip tooltipContent="~555 ribu kata \ ~2,5 juta karakter unicode (Opus 4.7 menggunakan tokenizer baru)">1 juta token</Tooltip> | <Tooltip tooltipContent="~750 ribu kata \ ~3,4 juta karakter unicode">1 juta token</Tooltip> | <Tooltip tooltipContent="~750 ribu kata \ ~3,4 juta karakter unicode">1 juta token</Tooltip> | <Tooltip tooltipContent="~150 ribu kata \ ~680 ribu karakter unicode">200 ribu token</Tooltip> | <Tooltip tooltipContent="~150 ribu kata \ ~680 ribu karakter unicode">200 ribu token</Tooltip> |
    | **Output maksimum**                                                                                                                | 128 ribu token                                                                               | 128 ribu token                                                                                                                     | 128 ribu token                                                                               | 128 ribu token                                                                               | 64 ribu token                                                                                  | 64 ribu token                                                                                  |
    | **Batas pengetahuan andal**                                                                                                        | Jan 20265                                                                                    | Jan 20265                                                                                                                          | Mei 20255                                                                                    | Agu 20255                                                                                    | Jan 20255                                                                                      | Mei 20255                                                                                      |
    | **Batas data pelatihan**                                                                                                           | Jan 2026                                                                                     | Jan 2026                                                                                                                           | Agu 2025                                                                                     | Jan 2026                                                                                     | Jul 2025                                                                                       | Agu 2025                                                                                       |

    *5 **Batas pengetahuan andal** menunjukkan tanggal hingga kapan pengetahuan model paling luas dan andal. **Batas data pelatihan** adalah rentang tanggal yang lebih luas dari data pelatihan yang digunakan.*

    *6 Claude Opus 4.8 dan Claude Opus 4.7 tersedia di Bedrock melalui [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) (endpoint Bedrock Messages-API).*
  </Accordion>
</AccordionGroup>

## Kinerja prompt dan output

Model Claude saat ini unggul dalam:

* **Kinerja:** Hasil tingkat atas dalam penalaran, pengodean, tugas multibahasa, penanganan konteks panjang, kejujuran, dan pemrosesan gambar. Lihat [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan prompting umum dan spesifik model.

* **Respons yang menarik:** Model Claude ideal untuk aplikasi yang membutuhkan interaksi yang kaya dan mirip manusia.

  * Jika Anda lebih menyukai respons yang lebih ringkas, Anda dapat menyesuaikan prompt Anda untuk mengarahkan model ke panjang output yang diinginkan. Lihat [panduan rekayasa prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering) untuk detailnya.
  * Untuk praktik terbaik prompting, lihat [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

* **Kualitas output:** Saat bermigrasi dari generasi model sebelumnya, Anda mungkin melihat peningkatan yang lebih besar dalam kinerja keseluruhan.

## Bermigrasi ke Claude Opus 5

Jika Anda saat ini menggunakan Claude Opus 4.8 atau model Claude sebelumnya, lihat [Bermigrasi ke Claude Opus 5](https://platform.claude.com/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5).

## Mulai dengan Claude

Jika Anda siap untuk mulai menjelajahi apa yang dapat dilakukan Claude untuk Anda, langsung saja! Baik Anda seorang developer yang ingin mengintegrasikan Claude ke dalam aplikasi Anda atau pengguna yang ingin merasakan kekuatan AI secara langsung, sumber daya berikut dapat membantu.

<Note>
  Ingin mengobrol dengan Claude? Kunjungi 

  [claude.ai](https://claude.ai)

  !
</Note>

<CardGroup cols={3}>
  <Card title="Pengantar Claude" icon="check" href="https://platform.claude.com/docs/id/intro">
    Jelajahi kapabilitas dan alur pengembangan Claude.
  </Card>

  <Card title="Mulai cepat" icon="lightning" href="https://platform.claude.com/docs/id/get-started">
    Pelajari cara melakukan panggilan API pertama Anda dalam hitungan menit.
  </Card>

  <Card title="Claude Console" icon="code" href="https://platform.claude.com/">
    Buat dan uji prompt yang kuat langsung di browser Anda.
  </Card>
</CardGroup>

Jika Anda memiliki pertanyaan atau membutuhkan bantuan, jangan ragu untuk menghubungi [tim dukungan](https://support.claude.com/) atau berkonsultasi dengan [komunitas Discord](https://www.anthropic.com/discord).
