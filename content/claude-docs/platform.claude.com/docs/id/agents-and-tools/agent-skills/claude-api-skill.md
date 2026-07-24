---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 14ca9f6e9d5fd9555020dcde7de710d499363312e09527da3237a237104db7da
---

# Skill Claude API

Agent Skill open-source yang menyediakan Claude dengan materi referensi API terkini, dokumentasi SDK, dan praktik terbaik untuk membangun aplikasi dengan Claude API dan Claude Managed Agents.

---

Skill `claude-api` adalah [Agent Skill](/docs/id/agents-and-tools/agent-skills/overview) open-source yang menyediakan Claude dengan materi referensi yang terperinci dan terkini untuk membangun aplikasi pada dua permukaan Anthropic:

* **Messages API:** Permukaan utama untuk permintaan tunggal, streaming chat, penggunaan alat, pemrosesan batch, caching prompt, output terstruktur, dan loop agen kustom.
* **Claude Managed Agents (beta):** Permukaan yang di-hosting oleh Anthropic untuk agen stateful yang dikelola server dengan eksekusi alat yang di-hosting Anthropic, konfigurasi agen persisten, dan sandbox per-sesi.

Skill ini mencakup delapan bahasa pemrograman untuk Messages API dan Managed Agents: Python, TypeScript, C#, Go, Java, PHP, Ruby, dan cURL.

Skill ini sudah dibundel dengan [Claude Code](https://code.claude.com/docs/en/overview) dan juga tersedia di [repositori skills Anthropic](https://github.com/anthropics/skills) yang open-source, di mana Anda dapat menginstalnya di lingkungan apa pun yang mendukung Agent Skills.

Skill ini menggunakan [progressive disclosure](/docs/id/agents-and-tools/agent-skills/overview#how-skills-work) (pengungkapan progresif) untuk menjaga efisiensi konteks: Claude hanya memuat dokumentasi yang relevan dengan bahasa proyek Anda, permukaan (Messages API atau Managed Agents), dan tugas spesifik yang sedang dikerjakan (penggunaan alat, streaming, batch, dan sebagainya), alih-alih memuat semuanya sekaligus.

## Apa yang disediakan skill ini

Saat dipicu, skill ini melengkapi Claude dengan:

**Untuk Messages API:**

* **Dokumentasi SDK spesifik bahasa:** Instalasi, mulai cepat, pola umum, dan penanganan error untuk bahasa proyek Anda
* **Panduan penggunaan alat:** Contoh spesifik bahasa dan [fondasi konseptual](/docs/id/agents-and-tools/tool-use/overview) untuk pemanggilan fungsi, termasuk tool runner beta jika tersedia
* **Pola streaming:** Detail implementasi untuk membangun UI chat dan menangani tampilan inkremental
* **Pemrosesan batch:** Pemrosesan batch offline dengan biaya 50%
* **Caching prompt:** Desain prefix-stability, penempatan breakpoint, dan audit silent-invalidator
* **Migrasi model:** Panduan langkah demi langkah untuk bermigrasi ke model Claude yang lebih baru (termasuk breaking changes dan perubahan perilaku pada [Claude Opus 4.8](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47))
* **Informasi model terkini:** ID model, ukuran jendela konteks, dan harga
* **Jebakan umum:** Panduan terperinci untuk menghindari kesalahan yang sering terjadi saat berintegrasi dengan API

**Untuk Managed Agents (beta):**

* **Alur onboarding:** Panduan berbasis wawancara untuk menyiapkan Managed Agent baru dari awal, tersedia melalui subperintah `/claude-api managed-agents-onboard`
* **Dokumentasi Managed Agents spesifik bahasa:** Membuat agen persisten, memulai sesi, streaming event, dan menangani konfirmasi alat untuk Python, TypeScript, C#, Go, Java, PHP, Ruby, dan cURL
* **Pola klien:** Reconnect stream tanpa kehilangan data, gerbang queued/processed `processed_at`, penanganan interupsi, jebakan file-mount, dan penanganan kredensial
* **Batasan deployment:** Managed Agents hanya tersedia di Claude API dan [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws) (tidak di Amazon Bedrock, Google Cloud, atau Microsoft Foundry). Skill ini mengarahkan deployment lainnya ke Messages API dan penggunaan alat sebagai gantinya.

## Kapan skill ini aktif

Skill ini aktif dengan dua cara:

**Aktivasi otomatis** terjadi ketika:

* Kode Anda mengimpor SDK Anthropic (`anthropic` untuk Python, `@anthropic-ai/sdk` untuk TypeScript/JavaScript)
* Anda meminta Claude untuk membantu membangun, men-debug, atau mengoptimalkan sesuatu dengan Claude API, SDK Anthropic, atau Managed Agents
* Anda menambahkan, memodifikasi, atau menyetel fitur Claude dalam sebuah file (caching prompt, adaptive thinking, compaction, penggunaan alat, batch, files, citations, memory) atau referensi model

**Pemanggilan manual** dengan mengetik `/claude-api` (dengan subperintah atau teks opsional) di lingkungan mana pun tempat skill ini terinstal.

Skill ini tidak aktif untuk tugas pemrograman umum, pekerjaan ML/data-science, atau kode yang mengimpor SDK AI lain (seperti OpenAI).

## Bahasa yang didukung

Skill ini mendeteksi bahasa proyek Anda secara otomatis dengan memeriksa file proyek (misalnya, `requirements.txt` untuk Python, `tsconfig.json` untuk TypeScript, `go.mod` untuk Go) dan memuat dokumentasi yang sesuai.

| Bahasa     | SDK Messages API | Tool runner | Managed Agents |
| ---------- | ---------------- | ----------- | -------------- |
| Python     | Ya               | Ya (beta)   | Ya (beta)      |
| TypeScript | Ya               | Ya (beta)   | Ya (beta)      |
| C#         | Ya               | Ya (beta)   | Ya (beta)      |
| Go         | Ya               | Ya (beta)   | Ya (beta)      |
| Java       | Ya               | Ya (beta)   | Ya (beta)      |
| PHP        | Ya               | Ya (beta)   | Ya (beta)      |
| Ruby       | Ya               | Ya (beta)   | Ya (beta)      |
| cURL       | Ya               | N/A         | Ya (beta)      |

Jika proyek Anda menggunakan beberapa bahasa, Claude akan menanyakan bahasa mana yang berlaku. Untuk bahasa yang tidak didukung (Rust, Swift, C++), skill ini menyediakan contoh cURL/raw HTTP.

## Cara menggunakan skill ini

### Di Claude Code (dibundel)

Skill ini disertakan bersama [Claude Code](https://code.claude.com/docs/en/overview) dan tidak memerlukan instalasi. Ketika Anda meminta Claude untuk membantu membangun sesuatu dengan Claude API, atau ketika proyek Anda sudah mengimpor SDK Anthropic, skill ini aktif secara otomatis.

Anda juga dapat memanggilnya secara langsung:

```text wrap
/claude-api
```

Untuk informasi lebih lanjut tentang cara kerja skill yang dibundel di Claude Code, lihat [dokumentasi skills Claude Code](https://code.claude.com/docs/en/skills#bundled-skills).

### Dari repositori skills

Kode sumber skill ini tersedia di [repositori skills Anthropic](https://github.com/anthropics/skills). Anda dapat menginstalnya menggunakan perintah `npx`:

```bash
npx skills add https://github.com/anthropics/skills --skill claude-api
```

Atau instal sebagai [plugin Claude Code](https://code.claude.com/docs/en/plugins):

```text wrap
/plugin marketplace add anthropics/skills
/plugin install claude-api@anthropic-agent-skills
```

## Bermigrasi ke model Claude yang lebih baru

Skill Claude API dapat melakukan migrasi model Claude di seluruh basis kode. Panggil secara langsung dengan `/claude-api migrate`:

```text wrap
/claude-api migrate this project to claude-opus-4-8
```

Anda juga dapat memberikan cakupan spesifik di awal untuk melewati pertanyaan konfirmasi cakupan:

```text wrap
/claude-api migrate everything under src/ to claude-opus-4-8
/claude-api migrate apps/api.py and apps/worker.py to claude-opus-4-8
```

Ketika cakupan ambigu (misalnya, `/claude-api migrate to claude-opus-4-8` tanpa keterangan tambahan), skill ini akan meminta Anda memilih antara seluruh direktori kerja, subdirektori tertentu, atau daftar file eksplisit sebelum mengedit file apa pun. Ini berlaku untuk pemanggil Messages API maupun Managed Agents.

Skill ini menangani:

* **Penggantian ID model**, termasuk konstanta SDK bertipe (`Model.CLAUDE_OPUS_4_7` → `Model.CLAUDE_OPUS_4_8`) di semua bahasa yang didukung, dan mengklasifikasikan setiap file sebagai pemanggil, pendefinisi model, atau referensi string opak sebelum mengedit
* **Deteksi platform cloud**, mempertahankan format ID model spesifik platform (misalnya, prefiks `anthropic.` di Amazon Bedrock) dan melewati perubahan untuk fitur yang tidak tersedia di platform yang dioperasikan mitra
* **Perubahan parameter yang bersifat breaking**, seperti menghapus `temperature`, `top_p`, dan `top_k` untuk Claude Opus 4.8 dan Claude Opus 4.7, serta mengonversi `thinking: {type: "enabled", budget_tokens: N}` menjadi `thinking: {type: "adaptive"}`
* **Penggantian prefill**, mengonversi pola prefill pesan asisten menjadi [output terstruktur](/docs/id/build-with-claude/structured-outputs) jika berlaku
* **Pembersihan header beta**, menghapus header yang sudah GA pada model target (misalnya, `effort-2025-11-24`, `fine-grained-tool-streaming-2025-05-14`, `interleaved-thinking-2025-05-14`) dan beralih kembali dari `client.beta.messages.create` ke `client.messages.create`
* **Kalibrasi effort**, merekomendasikan titik awal `output_config.effort` untuk model target (misalnya, `xhigh` untuk kasus penggunaan coding dan agentik pada Claude Opus 4.8 dan Claude Opus 4.7)
* **Penyetelan perilaku prompt**, menandai prompt kontrol panjang, pemicu alat, subagen, dan pengikutan instruksi yang mungkin berperilaku berbeda pada model target
* **Penanganan default senyap**, mengaktifkan kembali ringkasan pemikiran (`thinking.display: "summarized"`) ketika penalaran ditampilkan kepada pengguna pada Claude Opus 4.8 dan Claude Opus 4.7
* **Konfigurasi fallback penolakan**, menambahkan penanganan `stop_reason: "refusal"` sebelum membaca konten respons dan menyiapkan [jalur retry fallback](/docs/id/build-with-claude/refusals-and-fallback) ketika targetnya adalah Claude Fable 5 (parameter `fallbacks` sisi server, middleware refusal-fallback SDK, atau retry fallback-credit), serta memperbarui kode fallback yang ditulis berdasarkan bentuk preview sebelumnya

Saat mengedit, skill ini menjelaskan setiap perubahan dan motivasinya secara inline. Setelah selesai, skill ini menghasilkan daftar periksa item yang memerlukan verifikasi manual (biasanya pengujian integrasi, penyetelan prompt kontrol panjang, dan penetapan ulang baseline biaya/batas laju).

Untuk daftar lengkap perubahan spesifik model yang diterapkan skill ini, lihat [Bermigrasi ke Claude Opus 4.8 dari Claude Opus 4.7](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47).

## Menyiapkan Managed Agent

Untuk membuat kerangka Managed Agent baru dari awal, panggil subperintah `managed-agents-onboard`:

```text wrap
/claude-api managed-agents-onboard
```

Skill ini menjalankan wawancara yang memandu Anda melalui model mental Managed Agents (konfigurasi Agent versus Sessions), membuat templat konfigurasi agen, mengonfigurasi lingkungan dan alat, menyiapkan loop sesi, dan menghasilkan kode yang dapat dijalankan untuk bahasa Anda. Skill ini juga mencakup alur wajib **Agent (sekali) → Session (setiap eksekusi)**: `model`, `system`, dan `tools` berada pada agen, tidak pernah pada sesi, dan agen harus dibuat sekali lalu direferensikan berdasarkan ID.

Managed Agents memerlukan header beta `managed-agents-2026-04-01`, yang diatur secara otomatis oleh SDK untuk semua panggilan `client.beta.agents.*`, `client.beta.environments.*`, `client.beta.sessions.*`, dan `client.beta.vaults.*`.

## Contoh penggunaan

Berikut adalah contoh tugas yang dibantu skill ini agar dapat ditangani Claude:

**Membangun aplikasi chat:**

```text wrap
Build a streaming chat UI with the Claude API in TypeScript
```

**Memigrasikan proyek yang sudah ada:**

```text wrap
/claude-api migrate this codebase to claude-opus-4-8 and re-tune effort
```

**Onboarding Managed Agent baru:**

```text wrap
/claude-api managed-agents-onboard
```

Dalam setiap kasus, skill ini memuat dokumentasi spesifik bahasa yang relevan dan memandu Claude melalui implementasi menggunakan pola API terkini dan praktik terbaik.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ikhtisar Agent Skills" icon="graduation-cap" href="/docs/id/agents-and-tools/agent-skills/overview">
    Pelajari cara kerja Agent Skills dan model progressive disclosure
  </Card>

  <Card title="SDK Klien" icon="code" href="/docs/id/cli-sdks-libraries/overview">
    Jelajahi SDK resmi Anthropic untuk semua bahasa yang didukung
  </Card>

  <Card title="Repositori skills" icon="github-logo" href="https://github.com/anthropics/skills">
    Jelajahi repositori skills publik Anthropic di GitHub
  </Card>
</CardGroup>
