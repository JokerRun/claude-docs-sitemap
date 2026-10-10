---
source: platform
url: https://platform.claude.com/docs/id/intro
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: b787925a0d290995f8bf2035a4d6c515a3673a951c3c25273407e54d39062dc3
---

---
title: Pengantar Claude
url: https://platform.claude.com/docs/id/intro
description: Claude adalah platform AI berkinerja tinggi, tepercaya, dan cerdas yang dibangun oleh Anthropic. Claude unggul dalam tugas-tugas yang melibatkan bahasa, penalaran, analisis, pengodean, dan banyak lagi.
---

<Note>
  Ingin mengobrol dengan Claude? Kunjungi [claude.ai](https://claude.ai).
</Note>

Anthropic menawarkan dua cara untuk membangun dengan Claude, masing-masing cocok untuk kasus penggunaan yang berbeda:

|                        | Messages API                                    | Claude Managed Agents                                                                    |
| ---------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Apa itu**            | Akses langsung untuk memberikan prompt ke model | Harness agen siap pakai yang dapat dikonfigurasi dan berjalan di infrastruktur terkelola |
| **Paling cocok untuk** | Loop agen kustom dan kontrol yang terperinci    | Tugas yang berjalan lama dan pekerjaan asinkron                                          |

Untuk mempelajari lebih lanjut tentang masing-masing, lihat [Menggunakan Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) dan [ikhtisar Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview).

## Jelajahi generasi terbaru model Claude

Jika Anda tidak yakin model mana yang akan digunakan, mulailah dengan [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview) untuk sebagian besar beban kerja. Gunakan [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) untuk penalaran yang menuntut dan pekerjaan agentik jangka panjang, atau ketika hasil evaluasi (evals) Anda pada Claude Opus 5.5 dengan tingkat effort yang lebih tinggi masih belum memadai. Semua model saat ini mendukung input teks dan gambar, output teks, kemampuan multibahasa, "vision" (penglihatan), dan "tool use" (penggunaan alat). Halaman setiap model mencantumkan platform tempat model tersebut tersedia.

* [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) (`claude-fable-5-1`) — New — *For demanding reasoning and long-horizon agentic work* — Most capable · Research · Multi-day tasks
* [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview) (`claude-opus-5-5`) — New — *For long-running agentic coding and knowledge work* — Complex projects · Agents · Coding
* [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview) (`claude-sonnet-5-5`) — New — *The best combination of speed and intelligence* — Everyday tasks · Writing · Cost-efficient
* [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview) (`claude-haiku-5-5`) — New — *For high-volume, latency-sensitive tasks such as classification, extraction, and routing* — Fastest · Lowest cost · High volume

[Bandingkan model](https://platform.claude.com/docs/id/models/overview)

***

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
    Temukan apa yang dapat dilakukan Claude: "thinking" (pemikiran), pencarian web, penanganan file, output terstruktur, dan banyak lagi.

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
