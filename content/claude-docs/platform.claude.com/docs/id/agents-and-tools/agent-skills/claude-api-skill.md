---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 8977883cac38f4b3652da36ce0ef2d4c069f7f255dee14b863c591d1fa8b3b35
---

# Keterampilan Claude API

Sebuah Agent Skill sumber terbuka yang menyediakan Claude dengan materi referensi API terkini, dokumentasi SDK, dan praktik terbaik untuk membangun aplikasi dengan Claude API dan Claude Managed Agents.

---

Keterampilan `claude-api` adalah sebuah [Agent Skill](/docs/id/agents-and-tools/agent-skills/overview) sumber terbuka yang menyediakan Claude dengan materi referensi terperinci dan terkini untuk membangun aplikasi di dua permukaan Anthropic:

- **Messages API** — permukaan utama untuk permintaan tunggal, streaming chat, penggunaan alat, pemrosesan batch, caching prompt, output terstruktur, dan loop agen kustom.
- **Claude Managed Agents (beta)** — permukaan pihak pertama untuk agen stateful yang dikelola server dengan eksekusi alat yang dihosting Anthropic, konfigurasi agen persisten, dan kontainer per-sesi.

Ini mencakup 8 bahasa pemrograman untuk Messages API (Python, TypeScript, Java, Go, Ruby, C#, PHP, dan cURL) dan 7 bahasa untuk Managed Agents (Python, TypeScript, Java, Go, Ruby, PHP, dan cURL — C# saat ini tidak didukung).

Keterampilan ini dilengkapi dengan [Claude Code](https://code.claude.com/docs/en/overview) dan juga tersedia di repositori keterampilan sumber terbuka [Anthropic](https://github.com/anthropics/skills/tree/main/skills/claude-api), di mana Anda dapat menginstalnya di lingkungan apa pun yang mendukung Agent Skills.

Keterampilan ini menggunakan [progressive disclosure](/docs/id/agents-and-tools/agent-skills/overview#three-types-of-skill-content-three-levels-of-loading) untuk menjaga konteks tetap efisien: Claude hanya memuat dokumentasi yang relevan dengan bahasa proyek Anda, permukaan (Messages API atau Managed Agents), dan tugas spesifik yang sedang dikerjakan (penggunaan alat, streaming, batch, dan sebagainya), daripada memuat semuanya sekaligus.

## Apa yang disediakan keterampilan ini

Ketika dipicu, keterampilan ini melengkapi Claude dengan:

**Untuk Messages API:**

- **Dokumentasi SDK khusus bahasa:** Instalasi, quick start, pola umum, dan penanganan kesalahan untuk bahasa proyek Anda
- **Panduan penggunaan alat:** Contoh khusus bahasa dan [fondasi konseptual](/docs/id/agents-and-tools/tool-use/overview) untuk function calling, termasuk beta tool runner jika tersedia
- **Pola streaming:** Detail implementasi untuk membangun UI chat dan menangani tampilan inkremental
- **Pemrosesan batch:** Pemrosesan batch offline dengan biaya 50%
- **Caching prompt:** Desain prefix-stability, penempatan breakpoint, dan audit silent-invalidator
- **Migrasi model:** Panduan langkah demi langkah untuk bermigrasi ke model Claude yang lebih baru (termasuk breaking changes dan perubahan perilaku pada [Claude Opus 4.7](/docs/id/about-claude/models/migration-guide#migrating-to-claude-opus-4-7))
- **Informasi model saat ini:** ID model, ukuran jendela konteks, dan harga
- **Jebakan umum:** Panduan terperinci tentang cara menghindari kesalahan yang sering terjadi saat mengintegrasikan dengan API

**Untuk Managed Agents (beta):**

- **Alur onboarding:** Panduan berbasis wawancara untuk menyiapkan Managed Agent baru dari awal, tersedia melalui subperintah `/claude-api managed-agents-onboard`
- **Dokumentasi Managed Agents khusus bahasa:** Membuat agen persisten, memulai sesi, streaming event, dan menangani konfirmasi alat untuk Python, TypeScript, Java, Go, Ruby, PHP, dan cURL
- **Pola klien:** Lossless stream reconnect, `processed_at` queued/processed gate, interrupt handling, file-mount gotchas, dan credential handling
- **Batasan deployment:** Managed Agents hanya pihak pertama (tidak tersedia di Amazon Bedrock, Google Vertex AI, atau Microsoft Foundry) — keterampilan ini mengarahkan deployment pihak ketiga ke Messages API + tool use sebagai gantinya

## Kapan keterampilan ini diaktifkan

Keterampilan ini diaktifkan dengan dua cara:

**Aktivasi otomatis** terjadi ketika:

- Kode Anda mengimpor SDK Anthropic (`anthropic` untuk Python, `@anthropic-ai/sdk` untuk TypeScript/JavaScript)
- Anda meminta Claude untuk membantu membangun, debug, atau mengoptimalkan sesuatu dengan Claude API, SDK Anthropic, atau Managed Agents
- Anda menambah, memodifikasi, atau menyetel fitur Claude dalam file (prompt caching, adaptive thinking, compaction, tool use, batch, files, citations, memory) atau referensi model

**Invokasi manual** dengan mengetik `/claude-api` (dengan subperintah opsional atau prosa) di lingkungan apa pun tempat keterampilan ini diinstal.

Keterampilan ini tidak diaktifkan untuk tugas pemrograman umum, pekerjaan ML/data-science, atau kode yang mengimpor SDK AI lain (seperti OpenAI).

## Bahasa yang didukung

Keterampilan ini mendeteksi bahasa proyek Anda secara otomatis dengan memeriksa file proyek (misalnya, `requirements.txt` untuk Python, `tsconfig.json` untuk TypeScript, `go.mod` untuk Go) dan memuat dokumentasi yang sesuai.

| Bahasa     | Messages API SDK | Tool runner | Managed Agents |
|------------|------------------|-------------|----------------|
| Python     | Ya               | Ya (beta)   | Ya (beta)      |
| TypeScript | Ya               | Ya (beta)   | Ya (beta)      |
| Java       | Ya               | Tidak       | Ya (beta)      |
| Go         | Ya               | Tidak       | Ya (beta)      |
| Ruby       | Ya               | Ya (beta)   | Ya (beta)      |
| C#         | Ya               | Tidak       | Tidak          |
| PHP        | Ya               | Tidak       | Ya (beta)      |
| cURL       | Ya               | T/A         | Ya (beta)      |

Jika proyek Anda menggunakan beberapa bahasa, Claude akan menanyakan bahasa mana yang berlaku. Untuk bahasa yang tidak didukung (Rust, Swift, C++), keterampilan ini menyediakan contoh cURL/raw HTTP.

## Cara menggunakan keterampilan ini

### Di Claude Code (dilengkapi)

Keterampilan ini dilengkapi dengan [Claude Code](https://code.claude.com/docs/en/overview) dan tidak memerlukan instalasi. Ketika Anda meminta Claude untuk membantu membangun sesuatu dengan Claude API, atau ketika proyek Anda sudah mengimpor SDK Anthropic, keterampilan ini diaktifkan secara otomatis.

Anda juga dapat menginvokasinya secara langsung:

```text
/claude-api
```

Untuk informasi lebih lanjut tentang cara keterampilan bundel bekerja di Claude Code, lihat [dokumentasi keterampilan Claude Code](https://code.claude.com/docs/en/skills#bundled-skills).

### Dari repositori keterampilan

Sumber keterampilan tersedia di [repositori keterampilan Anthropic](https://github.com/anthropics/skills). Anda dapat menginstalnya menggunakan perintah `npx`:

```bash
npx skills add https://github.com/anthropics/skills --skill claude-api
```

Atau instal sebagai [plugin](https://code.claude.com/docs/en/plugins) Claude Code:

```bash
/plugin marketplace add anthropics/skills
/plugin install claude-api@anthropic-agent-skills
```

## Bermigrasi ke model Claude yang lebih baru

Keterampilan Claude API dapat melakukan migrasi model Claude di seluruh codebase. Invokasinya secara langsung dengan `/claude-api migrate`:

```text
/claude-api migrate this project to claude-opus-4-7
```

Anda juga dapat melewatkan scope tertentu di awal untuk melewati pertanyaan konfirmasi scope:

```text
/claude-api migrate everything under src/ to claude-opus-4-7
/claude-api migrate apps/api.py and apps/worker.py to claude-opus-4-7
```

Ketika scope tidak jelas (misalnya, `/claude-api migrate to claude-opus-4-7` yang kosong), keterampilan ini meminta Anda untuk memilih antara seluruh direktori kerja, subdirektori tertentu, atau daftar file eksplisit sebelum mengedit file apa pun. Ini berlaku untuk pemanggil Messages API dan Managed Agents.

Keterampilan ini menangani:

- **Penukaran ID model**, termasuk konstanta SDK yang diketik (`Model.CLAUDE_OPUS_4_6` → `Model.CLAUDE_OPUS_4_7`) di semua bahasa yang didukung, dan mengklasifikasikan setiap file sebagai pemanggil, pendefinisi model, atau referensi string buram sebelum mengedit
- **Perubahan parameter yang merusak**, seperti menghapus `temperature`, `top_p`, dan `top_k` untuk Claude Opus 4.7, dan mengonversi `thinking: {type: "enabled", budget_tokens: N}` ke `thinking: {type: "adaptive"}`
- **Penggantian prefill**, mengonversi pola prefill pesan asisten ke [structured outputs](/docs/id/build-with-claude/structured-outputs) jika berlaku
- **Pembersihan header beta**, menghapus header yang GA pada model target (misalnya, `effort-2025-11-24`, `fine-grained-tool-streaming-2025-05-14`, `interleaved-thinking-2025-05-14`) dan beralih kembali dari `client.beta.messages.create` ke `client.messages.create`
- **Kalibrasi effort**, merekomendasikan titik awal `output_config.effort` untuk model target (misalnya, `xhigh` untuk coding dan use case agentic pada Claude Opus 4.7)
- **Penyesuaian perilaku prompt**, menandai prompt kontrol panjang, pemicu alat, subagen, dan pengikutan instruksi yang mungkin berperilaku berbeda pada model target
- **Penanganan default senyap**, memilih kembali ke ringkasan thinking (`thinking.display: "summarized"`) ketika reasoning ditampilkan kepada pengguna pada Claude Opus 4.7

Saat mengedit, keterampilan ini menjelaskan setiap perubahan dan motivasinya secara inline. Setelah selesai, keterampilan ini menghasilkan daftar periksa item yang memerlukan verifikasi manual (biasanya tes integrasi, penyesuaian prompt kontrol panjang, dan re-baselining biaya/rate-limit).

Untuk daftar lengkap perubahan spesifik model yang diterapkan keterampilan ini, lihat [Bermigrasi ke Claude Opus 4.7](/docs/id/about-claude/models/migration-guide#migrating-to-claude-opus-4-7).

## Menyiapkan Managed Agent

Untuk membuat Managed Agent baru dari awal, invokasinya dengan subperintah `managed-agents-onboard`:

```text
/claude-api managed-agents-onboard
```

Keterampilan ini menjalankan wawancara yang memandu Anda melalui model mental Managed Agents (Konfigurasi Agent versus Sesi), membuat template konfigurasi agen, mengonfigurasi lingkungan dan alat, menyiapkan loop sesi, dan mengeluarkan kode yang dapat dijalankan untuk bahasa Anda. Keterampilan ini juga mencakup alur **Agent (sekali) → Session (setiap kali berjalan)** yang wajib — `model`, `system`, dan `tools` hidup di agen, tidak pernah di sesi, dan agen harus dibuat sekali dan direferensikan berdasarkan ID.

Managed Agents memerlukan header beta `managed-agents-2026-04-01`, yang SDK atur secara otomatis untuk semua panggilan `client.beta.agents.*`, `client.beta.environments.*`, `client.beta.sessions.*`, dan `client.beta.vaults.*`.

## Contoh penggunaan

Berikut adalah contoh tugas yang membantu keterampilan ini Claude tangani:

**Membangun aplikasi chat:**
```text
Build a streaming chat UI with the Claude API in TypeScript
```

**Bermigrasi proyek yang ada:**
```text
/claude-api migrate this codebase to claude-opus-4-7 and re-tune effort
```

**Onboarding Managed Agent baru:**
```text
/claude-api managed-agents-onboard
```

Dalam setiap kasus, keterampilan ini memuat dokumentasi spesifik bahasa yang relevan dan memandu Claude melalui implementasi menggunakan pola API saat ini dan praktik terbaik.

## Langkah berikutnya

<CardGroup cols={2}>
  <Card
    title="Ikhtisar Agent Skills"
    icon="graduation-cap"
    href="/docs/id/agents-and-tools/agent-skills/overview"
  >
    Pelajari tentang cara kerja Agent Skills dan model progressive disclosure
  </Card>
  <Card
    title="Client SDKs"
    icon="code"
    href="/docs/id/api/client-sdks"
  >
    Jelajahi SDK Anthropic resmi untuk semua bahasa yang didukung
  </Card>
  <Card
    title="Repositori keterampilan"
    icon="github-logo"
    href="https://github.com/anthropics/skills"
  >
    Jelajahi repositori keterampilan Anthropic publik di GitHub
  </Card>
</CardGroup>