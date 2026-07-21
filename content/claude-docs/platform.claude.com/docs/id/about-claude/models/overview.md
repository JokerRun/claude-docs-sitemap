---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/overview
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 3d2760376448bf4572ea834a79493afa1fd34cae2c36615278f85235d40538b9
---

# Ikhtisar model

Claude adalah keluarga model bahasa besar mutakhir yang dikembangkan oleh Anthropic. Panduan ini memperkenalkan model-model yang tersedia dan membandingkan kinerjanya.

---

## Memilih model

Jika Anda tidak yakin model mana yang akan digunakan, mulailah dengan **Claude Opus 4.8** untuk pengkodean agentik yang kompleks dan pekerjaan enterprise. Untuk beban kerja yang membutuhkan kemampuan tertinggi yang tersedia, gunakan [Claude Fable 5](#claude-fable-5-and-claude-mythos-5).

Semua model Claude saat ini mendukung input teks dan gambar, output teks, kemampuan multibahasa, dan visi. Model tersedia melalui Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

Setelah Anda memilih model, [pelajari cara melakukan panggilan API pertama Anda](/docs/id/get-started).

### Claude Fable 5 dan Claude Mythos 5

Claude Fable 5 (`claude-fable-5`) adalah model Anthropic yang paling mumpuni yang dirilis secara luas. Claude Mythos 5 (`claude-mythos-5`) memiliki spesifikasi dan harga yang sama dengan Claude Fable 5 dan bergabung dengan Claude Mythos Preview (`claude-mythos-preview`) yang hanya tersedia melalui undangan dalam [Project Glasswing](https://anthropic.com/glasswing). Lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) untuk detail peluncuran dan perubahan API.

Claude Fable 5 tersedia secara umum di Claude API, Claude Platform on AWS, Amazon Bedrock, Google Cloud, dan Microsoft Foundry mulai 9 Juni 2026. Claude Mythos 5 tidak tersedia secara umum: model ini ditawarkan dengan ketersediaan terbatas kepada pelanggan yang disetujui dalam [Project Glasswing](https://anthropic.com/glasswing), mulai hari yang sama. Untuk akses, hubungi tim akun Anthropic, AWS, atau Google Cloud Anda.

### Perbandingan model terbaru

| Fitur                                                                      | Claude Fable 5                                                                                                                                                                                                                                                                                                                           | Claude Opus 4.8                                                                          | Claude Sonnet 5                                                                          | Claude Haiku 4.5                                                                   |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Deskripsi**                                                              | Kecerdasan generasi berikutnya untuk agen yang berjalan lama                                                                                                                                                                                                                                                                             | Untuk pengkodean agentik yang kompleks dan pekerjaan enterprise                          | Kombinasi terbaik antara kecepatan dan kecerdasan                                        | Model tercepat dengan kecerdasan mendekati frontier                                |
| **ID Claude API**                                                          | claude-fable-5                                                                                                                                                                                                                                                                                                                           | claude-opus-4-8                                                                          | claude-sonnet-5                                                                          | claude-haiku-4-5-20251001                                                          |
| **Alias Claude API**                                                       | claude-fable-5                                                                                                                                                                                                                                                                                                                           | claude-opus-4-8                                                                          | claude-sonnet-5                                                                          | claude-haiku-4-5                                                                   |
| **ID AWS Bedrock**                                                         | anthropic.claude-fable-53                                                                                                                                                                                                                                                                                                                | anthropic.claude-opus-4-83                                                               | anthropic.claude-sonnet-53                                                               | anthropic.claude-haiku-4-5-20251001-v1:0                                           |
| **ID Google Cloud**                                                        | claude-fable-5                                                                                                                                                                                                                                                                                                                           | claude-opus-4-8                                                                          | claude-sonnet-5                                                                          | claude-haiku-4-5\@20251001                                                         |
| **Harga**1                                                                 | $10 / MTok input $50 / MTok output                                                                                                                                                                                                                                                                                                       | $5 / MTok input $25 / MTok output                                                        | $3 / MTok input $15 / MTok output4                                                       | $1 / MTok input $5 / MTok output                                                   |
| **[Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking)** | Tidak                                                                                                                                                                                                                                                                                                                                    | Tidak                                                                                    | Tidak                                                                                    | Ya                                                                                 |
| **[Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking)**      | Ya (selalu aktif)                                                                                                                                                                                                                                                                                                                        | Ya                                                                                       | Ya                                                                                       | Tidak                                                                              |
| **Latensi komparatif**                                                     | Lebih lambat                                                                                                                                                                                                                                                                                                                             | Sedang                                                                                   | Cepat                                                                                    | Tercepat                                                                           |
| **Jendela konteks**                                                        | <Tooltip tooltipContent="~555k kata \ ~2,5 juta karakter unicode. Claude Fable 5 menggunakan tokenizer yang diperkenalkan dengan Claude Opus 4.7; dibandingkan dengan model sebelum Claude Opus 4.7, teks yang sama menghasilkan sekitar 30% lebih banyak token. Peningkatan pastinya bergantung pada kontennya.">1 juta token</Tooltip> | <Tooltip tooltipContent="~555k kata \ ~2,5 juta karakter unicode">1 juta token</Tooltip> | <Tooltip tooltipContent="~555k kata \ ~2,5 juta karakter unicode">1 juta token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> |
| **Output maksimum**                                                        | 128k token                                                                                                                                                                                                                                                                                                                               | 128k token                                                                               | 128k token                                                                               | 64k token                                                                          |
| **Batas pengetahuan andal**                                                | Jan 20262                                                                                                                                                                                                                                                                                                                                | Jan 20262                                                                                | Jan 20262                                                                                | Feb 2025                                                                           |
| **Batas data pelatihan**                                                   | Jan 2026                                                                                                                                                                                                                                                                                                                                 | Jan 2026                                                                                 | Jan 2026                                                                                 | Jul 2025                                                                           |

*1 - Lihat [Harga](/docs/id/about-claude/pricing) untuk informasi harga lengkap termasuk diskon Batch API dan tarif caching prompt.*

*2 - **Batas pengetahuan andal** menunjukkan tanggal hingga kapan pengetahuan model paling luas dan andal. **Batas data pelatihan** adalah rentang tanggal yang lebih luas dari data pelatihan yang digunakan. Untuk informasi lebih lanjut, lihat [Transparency Hub Anthropic](https://www.anthropic.com/transparency).*

*3 - Claude Fable 5, Claude Opus 4.8, dan Claude Sonnet 5 tersedia di Bedrock melalui [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) (endpoint Bedrock Messages-API).*

*4 - Harga perkenalan sebesar $2 / $10 per MTok berlaku untuk Claude Sonnet 5 hingga 31 Agustus 2026. Lihat [Harga](/docs/id/about-claude/pricing#claude-sonnet-5-introductory-pricing).*

<Info>
  Claude Mythos 5 dan Claude Mythos Preview ditawarkan secara terpisah untuk alur kerja keamanan siber defensif sebagai bagian dari [Project Glasswing](https://anthropic.com/glasswing). Akses hanya melalui undangan dan tidak ada pendaftaran mandiri.
</Info>

<Note>
  Setiap ID model Claude adalah snapshot yang dipatok (pinned). Model dengan tanggal di dalam ID (misalnya, 

  `20250929`

  ) terikat pada rilis spesifik tersebut. Mulai dari generasi Claude 4.6, ID model menggunakan format tanpa tanggal yang juga merupakan snapshot yang dipatok, bukan pointer evergreen. Untuk model sebelum generasi 4.6, entri di kolom alias Claude API adalah pointer kemudahan yang mengarah ke ID model bertanggal. Untuk detail tentang konvensi penamaan dan cara kerja pembuatan versi, lihat 

  [ID model dan pembuatan versi](/docs/id/about-claude/models/model-ids-and-versions)

  .
</Note>

<Note>
  Mulai dari 

  **Claude Sonnet 4.5 dan semua model berikutnya**

   (termasuk Claude Sonnet 4.6), Bedrock menawarkan dua jenis endpoint: 

  **endpoint global**

   (perutean dinamis untuk ketersediaan maksimum) dan 

  **endpoint regional**

   (perutean data terjamin melalui wilayah geografis tertentu). Google Cloud menawarkan tiga jenis endpoint: endpoint global, 

  **endpoint multi-wilayah**

   (perutean dinamis dalam suatu area geografis), dan endpoint regional. Untuk informasi lebih lanjut, lihat 

  [Harga platform cloud](/docs/id/about-claude/pricing#cloud-platform-pricing)

  .
</Note>

<Note>
  **Claude Platform on AWS**

   menggunakan ID model yang sama dengan Claude API (misalnya, 

  `claude-opus-4-6`

  ), bukan ID bergaya Bedrock. Siklus hidup model di Claude Platform on AWS mengikuti 

  [Penghentian model](/docs/id/about-claude/model-deprecations)

   pihak pertama Anthropic, bukan milik Bedrock. Lihat 

  [Model yang tersedia](/docs/id/build-with-claude/claude-platform-on-aws#available-models)

   untuk daftar model.
</Note>

<Tip>
  Anda dapat mengkueri kemampuan model dan batas token secara terprogram dengan [Models API](/docs/id/api/models/list). Responsnya mencakup `max_input_tokens`, `max_tokens`, dan objek `capabilities` untuk setiap model yang tersedia.
</Tip>

<Note>
  Pada Claude Opus 4.8, parameter `effort` secara default bernilai `high` di semua permukaan, termasuk Claude API, Claude Code, dan claude.ai. Pada Claude Sonnet 5, nilai defaultnya adalah `high` di Claude API dan Claude Code. Atur `effort` secara eksplisit untuk menggunakan level yang berbeda. Lihat [Effort](/docs/id/build-with-claude/effort) untuk panduan memilih level.
</Note>

<Note>
  Nilai Output maksimum di atas berlaku untuk Messages API sinkron. Pada [Message Batches API](/docs/id/build-with-claude/batch-processing#extended-output-beta), Claude Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 5, dan Sonnet 4.6 mendukung hingga 300k token output dengan menggunakan header beta `output-300k-2026-03-24`.
</Note>

<AccordionGroup>
  <Accordion title="Model lama">
    Model-model berikut masih tersedia. Pertimbangkan untuk bermigrasi ke model saat ini untuk kinerja yang lebih baik:

    | Fitur                                                                      | Claude Opus 4.7                                                                                                                | Claude Opus 4.6                                                                          | Claude Sonnet 4.6                                                                        | Claude Sonnet 4.5                                                                  | Claude Opus 4.5                                                                    | Claude Opus 4.1 (usang)                                                            |
    | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
    | **ID Claude API**                                                          | claude-opus-4-7                                                                                                                | claude-opus-4-6                                                                          | claude-sonnet-4-6                                                                        | claude-sonnet-4-5-20250929                                                         | claude-opus-4-5-20251101                                                           | claude-opus-4-1-20250805                                                           |
    | **Alias Claude API**                                                       | claude-opus-4-7                                                                                                                | claude-opus-4-6                                                                          | claude-sonnet-4-6                                                                        | claude-sonnet-4-5                                                                  | claude-opus-4-5                                                                    | claude-opus-4-1                                                                    |
    | **ID AWS Bedrock**                                                         | anthropic.claude-opus-4-76                                                                                                     | anthropic.claude-opus-4-6-v1                                                             | anthropic.claude-sonnet-4-6                                                              | anthropic.claude-sonnet-4-5-20250929-v1:0                                          | anthropic.claude-opus-4-5-20251101-v1:0                                            | anthropic.claude-opus-4-1-20250805-v1:0                                            |
    | **ID Google Cloud**                                                        | claude-opus-4-7                                                                                                                | claude-opus-4-6                                                                          | claude-sonnet-4-6                                                                        | claude-sonnet-4-5\@20250929                                                        | claude-opus-4-5\@20251101                                                          | claude-opus-4-1\@20250805                                                          |
    | **Harga**                                                                  | $5 / MTok input $25 / MTok output                                                                                              | $5 / MTok input $25 / MTok output                                                        | $3 / MTok input $15 / MTok output                                                        | $3 / MTok input $15 / MTok output                                                  | $5 / MTok input $25 / MTok output                                                  | $15 / MTok input $75 / MTok output                                                 |
    | **[Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking)** | Tidak                                                                                                                          | Ya                                                                                       | Ya                                                                                       | Ya                                                                                 | Ya                                                                                 | Ya                                                                                 |
    | **[Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking)**      | Ya                                                                                                                             | Ya                                                                                       | Ya                                                                                       | Tidak                                                                              | Tidak                                                                              | Tidak                                                                              |
    | **Latensi komparatif**                                                     | Sedang                                                                                                                         | Sedang                                                                                   | Cepat                                                                                    | Cepat                                                                              | Sedang                                                                             | Sedang                                                                             |
    | **Jendela konteks**                                                        | <Tooltip tooltipContent="~555k kata \ ~2,5 juta karakter unicode (Opus 4.7 menggunakan tokenizer baru)">1 juta token</Tooltip> | <Tooltip tooltipContent="~750k kata \ ~3,4 juta karakter unicode">1 juta token</Tooltip> | <Tooltip tooltipContent="~750k kata \ ~3,4 juta karakter unicode">1 juta token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> | <Tooltip tooltipContent="~150k kata \ ~680k karakter unicode">200k token</Tooltip> |
    | **Output maksimum**                                                        | 128k token                                                                                                                     | 128k token                                                                               | 128k token                                                                               | 64k token                                                                          | 64k token                                                                          | 32k token                                                                          |
    | **Batas pengetahuan andal**                                                | Jan 20265                                                                                                                      | Mei 20255                                                                                | Agu 20255                                                                                | Jan 20255                                                                          | Mei 20255                                                                          | Jan 20255                                                                          |
    | **Batas data pelatihan**                                                   | Jan 2026                                                                                                                       | Agu 2025                                                                                 | Jan 2026                                                                                 | Jul 2025                                                                           | Agu 2025                                                                           | Mar 2025                                                                           |

    <Warning>
      Claude Opus 4.1 (`claude-opus-4-1-20250805`) telah usang dan akan dihentikan pada 5 Agustus 2026. Bermigrasilah ke [Claude Opus 4.8](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47) sebelum tanggal penghentian.

      Lihat [penghentian model](/docs/id/about-claude/model-deprecations) untuk detailnya.
    </Warning>

    *5 - **Batas pengetahuan andal** menunjukkan tanggal hingga kapan pengetahuan model paling luas dan andal. **Batas data pelatihan** adalah rentang tanggal yang lebih luas dari data pelatihan yang digunakan.*

    *6 - Claude Opus 4.7 tersedia di Bedrock melalui [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) (endpoint Bedrock Messages-API).*
  </Accordion>
</AccordionGroup>

## Kinerja prompt dan output

Model Claude 4 unggul dalam:

* **Kinerja:** Hasil kelas atas dalam penalaran, pengkodean, tugas multibahasa, penanganan konteks panjang, kejujuran, dan pemrosesan gambar. Lihat [postingan blog Claude 4](https://www.anthropic.com/news/claude-4) untuk informasi lebih lanjut.

* **Respons yang menarik:** Model Claude ideal untuk aplikasi yang membutuhkan interaksi yang kaya dan mirip manusia.

  * Jika Anda lebih menyukai respons yang lebih ringkas, Anda dapat menyesuaikan prompt Anda untuk mengarahkan model ke panjang output yang diinginkan. Lihat [panduan rekayasa prompt](/docs/id/build-with-claude/prompt-engineering) untuk detailnya.
  * Untuk praktik terbaik dalam membuat prompt, lihat [Praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

* **Kualitas output:** Saat bermigrasi dari generasi model sebelumnya ke Claude 4, Anda mungkin melihat peningkatan yang lebih besar dalam kinerja keseluruhan.

## Bermigrasi ke Claude Opus 4.8

Jika Anda saat ini menggunakan Claude Opus 4.7 atau model Claude yang lebih lama, lihat [Bermigrasi ke Claude Opus 4.8](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47).

## Bermigrasi ke Claude Opus 4.7

Jika Anda saat ini menggunakan Claude Opus 4.6 atau model Claude yang lebih lama, lihat [Bermigrasi ke Claude Opus 4.7](/docs/id/about-claude/models/migration-guide#migrating-to-claude-opus-4-7).

## Mulai dengan Claude

Jika Anda siap untuk mulai menjelajahi apa yang dapat Claude lakukan untuk Anda, langsung saja! Baik Anda seorang pengembang yang ingin mengintegrasikan Claude ke dalam aplikasi Anda atau pengguna yang ingin merasakan kekuatan AI secara langsung, sumber daya berikut dapat membantu.

<Note>
  Ingin mengobrol dengan Claude? Kunjungi 

  [claude.ai](https://claude.ai)

  !
</Note>

<CardGroup cols={3}>
  <Card title="Pengantar Claude" icon="check" href="/docs/id/intro">
    Jelajahi kemampuan Claude dan alur pengembangannya.
  </Card>

  <Card title="Mulai cepat" icon="lightning" href="/docs/id/get-started">
    Pelajari cara melakukan panggilan API pertama Anda dalam hitungan menit.
  </Card>

  <Card title="Claude Console" icon="code" href="/">
    Buat dan uji prompt yang andal langsung di browser Anda.
  </Card>
</CardGroup>

Jika Anda memiliki pertanyaan atau membutuhkan bantuan, jangan ragu untuk menghubungi [tim dukungan](https://support.claude.com/) atau berkonsultasi dengan [komunitas Discord](https://www.anthropic.com/discord).
