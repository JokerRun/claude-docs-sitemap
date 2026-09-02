---
source: platform
url: https://platform.claude.com/docs/id/intro
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: f91784ac4f98fc70efabfa4c5869664f24ae08b136fc2b3030e92f921fcbf8a9
---

---
title: Pengantar Claude
url: https://platform.claude.com/docs/id/intro
description: Claude adalah platform AI berkinerja tinggi, tepercaya, dan cerdas yang dibangun oleh Anthropic. Claude unggul dalam tugas-tugas yang melibatkan bahasa, penalaran, analisis, pengodean, dan banyak lagi.
---

<Tip>
  Generasi terbaru model Claude:

  **Claude Fable 5.1** - Untuk penalaran yang menuntut dan pekerjaan agentik berjangka panjang. Baca [pengumuman Claude Fable 5.1](https://www.anthropic.com/claude/fable/5-1).

  **Claude Mythos 5.1** - Menawarkan kemampuan Claude Fable 5.1 melalui undangan lewat [Project Glasswing](https://anthropic.com/glasswing).

  **Claude Opus 5** - Untuk pengodean agentik yang kompleks dan pekerjaan enterprise. Baca [pengumuman Claude Opus 5](https://www.anthropic.com/news/claude-opus-5).

  **Claude Sonnet 5** - Kecerdasan terdepan dalam skala besar, dibangun untuk pengodean, agen, dan alur kerja enterprise. Baca [pengumuman Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5).

  **Claude Haiku 4.5** - Model tercepat dengan kecerdasan mendekati terdepan. Baca [pengumuman Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5).
</Tip>

<Note>
  Ingin mengobrol dengan Claude? Kunjungi [claude.ai](https://claude.ai).
</Note>

Anthropic menawarkan dua cara untuk membangun dengan Claude, masing-masing cocok untuk kasus penggunaan yang berbeda:

|                        | Messages API                                    | Claude Managed Agents                                                                    |
| ---------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Apa itu**            | Akses langsung untuk memberikan prompt ke model | Harness agen siap pakai yang dapat dikonfigurasi dan berjalan di infrastruktur terkelola |
| **Paling cocok untuk** | Loop agen kustom dan kontrol yang terperinci    | Tugas yang berjalan lama dan pekerjaan asinkron                                          |

Untuk mempelajari lebih lanjut tentang masing-masing, lihat [Menggunakan Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) dan [ikhtisar Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview).

## Jalur yang direkomendasikan untuk developer baru

Ikuti langkah-langkah berikut untuk beranjak dari nol hingga memiliki integrasi Claude yang berfungsi.

<Steps>
  <Step title="Lakukan panggilan API pertama Anda">
    Siapkan lingkungan Anda, instal SDK, dan kirim pesan pertama Anda ke Claude.

    [Buka quickstart](https://platform.claude.com/docs/id/get-started)
  </Step>

  <Step title="Amankan kredensial Anda">
    Tetapkan masa kedaluwarsa saat Anda membuat kunci API. Jauhkan kunci tersebut dari source control, kode sisi klien, dan prompt. Periksa apakah beban kerja Anda dapat menggunakan Workload Identity Federation sebagai pengganti kunci statis.

    [Baca panduan autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication)
  </Step>

  <Step title="Pahami Messages API">
    Pelajari struktur inti permintaan dan respons, termasuk percakapan multi-giliran, "system prompt" (prompt sistem), dan stop reason.

    [Baca panduan Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)
  </Step>

  <Step title="Pilih model yang tepat">
    Bandingkan model-model Claude berdasarkan kemampuan dan biaya untuk memilih yang paling sesuai dengan kasus penggunaan Anda.

    [Lihat ikhtisar model](https://platform.claude.com/docs/id/models/overview)
  </Step>

  <Step title="Jelajahi fitur dan alat">
    Temukan apa yang dapat dilakukan Claude: "extended thinking" (pemikiran diperpanjang), pencarian web, penanganan file, output terstruktur, dan banyak lagi.

    [Telusuri ikhtisar fitur](https://platform.claude.com/docs/id/build-with-claude/overview)
  </Step>
</Steps>

***

## Mengembangkan dengan Claude

Anthropic menyediakan alat developer untuk membantu Anda membangun dan menskalakan aplikasi dengan Claude.

<CardGroup cols={3}>
  <Card title="Developer Console" icon="computer" href="https://platform.claude.com/">
    Jelajahi dan pahami API di browser Anda dengan playground.
  </Card>

  <Card title="Referensi API" icon="code" href="https://platform.claude.com/docs/id/api/overview">
    Jelajahi dokumentasi lengkap Claude API dan SDK klien.
  </Card>

  <Card title="Claude Cookbook" icon="chef-hat" href="https://platform.claude.com/cookbook">
    Belajar dengan notebook Jupyter interaktif yang mencakup PDF, embedding, dan banyak lagi.
  </Card>
</CardGroup>

***

## Kemampuan utama

Claude dapat membantu berbagai tugas yang melibatkan teks, kode, dan gambar.

<CardGroup cols={2}>
  <Card title="Pembuatan teks dan kode" icon="text-aa" href="https://platform.claude.com/docs/id/build-with-claude/overview">
    Merangkum teks, menjawab pertanyaan, mengekstrak data, menerjemahkan teks, serta menjelaskan dan menghasilkan kode.
  </Card>

  <Card title="Vision" icon="image" href="https://platform.claude.com/docs/id/build-with-claude/vision">
    Memproses dan menganalisis input visual serta menghasilkan teks dan kode dari gambar.
  </Card>
</CardGroup>

***

## Dukungan

<CardGroup cols={2}>
  <Card title="Pusat Bantuan" icon="help" href="https://support.claude.com/en/">
    Temukan jawaban atas pertanyaan yang sering diajukan tentang akun dan penagihan.
  </Card>

  <Card title="Status Layanan" icon="chart" href="https://status.claude.com">
    Periksa status layanan Anthropic.
  </Card>
</CardGroup>
