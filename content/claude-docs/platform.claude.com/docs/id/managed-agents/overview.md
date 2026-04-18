---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/overview
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: cb5ad6d9ca9b8cd7008a6999d5a8844f4dc7b0177c18a59778d8d6482825ee6f
---

# Ikhtisar Claude Managed Agents

Harness agen yang telah dibangun sebelumnya dan dapat dikonfigurasi yang berjalan di infrastruktur terkelola. Terbaik untuk tugas jangka panjang dan pekerjaan asinkron.

---

Anthropic offers two ways to build with Claude, each suited to different use cases:

| | Messages API | Claude Managed Agents |
|---|---|---|
| **What it is** | Direct model prompting access | Pre-built, configurable agent harness that runs in managed infrastructure |
| **Best for** | Custom agent loops and fine-grained control | Long-running tasks and asynchronous work |
| **Learn more** | [Messages API docs](/docs/en/build-with-claude/working-with-messages) | [Claude Managed Agents docs](/docs/en/managed-agents/overview) |

Claude Managed Agents menyediakan harness dan infrastruktur untuk menjalankan Claude sebagai agen otonom. Alih-alih membangun loop agen, eksekusi alat, dan runtime Anda sendiri, Anda mendapatkan lingkungan yang sepenuhnya terkelola di mana Claude dapat membaca file, menjalankan perintah, menjelajahi web, dan menjalankan kode dengan aman. Harness mendukung caching prompt bawaan, pemadatan, dan optimasi kinerja lainnya untuk output agen berkualitas tinggi dan efisien.

<CardGroup cols={2}>
  <Card title="Quickstart" icon="play" href="/docs/id/managed-agents/quickstart">
    Buat sesi agen pertama Anda
  </Card>
  <Card title="API Reference" icon="code-brackets" href="/docs/id/managed-agents/sessions">
    Dokumentasi endpoint lengkap
  </Card>
</CardGroup>

## Konsep inti

Claude Managed Agents dibangun di sekitar empat konsep:

| Concept | Description |
|---------|-------------|
| **Agent** | The model, system prompt, tools, MCP servers, and skills |
| **Environment** | A configured container template (packages, network access) |
| **Session** | A running agent instance within an environment, performing a specific task and generating outputs |
| **Events** | Messages exchanged between your application and the agent (user turns, tool results, status updates) |

## Cara kerjanya

<Steps>
  <Step title="Buat agen">
    Tentukan model, system prompt, alat, server MCP, dan keterampilan. Buat agen sekali dan referensikan dengan ID di seluruh sesi.
  </Step>
  <Step title="Buat lingkungan">
    Konfigurasikan kontainer cloud dengan paket pra-instal (Python, Node.js, Go, dll.), aturan akses jaringan, dan file yang dipasang.
  </Step>
  <Step title="Mulai sesi">
    Luncurkan sesi yang mereferensikan konfigurasi agen dan lingkungan Anda.
  </Step>
  <Step title="Kirim acara dan streaming respons">
    Kirim pesan pengguna sebagai acara. Claude secara otonom menjalankan alat dan streaming kembali hasil melalui server-sent events (SSE). Riwayat acara disimpan di sisi server dan dapat diambil sepenuhnya.
  </Step>
  <Step title="Kemudi atau interupsi">
    Kirim acara pengguna tambahan untuk memandu agen selama eksekusi, atau interupsi untuk mengubah arah.
  </Step>
</Steps>

## Kapan menggunakan Claude Managed Agents

Claude Managed Agents terbaik untuk beban kerja yang membutuhkan:

- **Eksekusi jangka panjang** - Tugas yang berjalan selama menit atau jam dengan beberapa panggilan alat
- **Infrastruktur cloud** - Kontainer aman dengan paket pra-instal dan akses jaringan
- **Infrastruktur minimal** - Tidak perlu membangun loop agen, sandbox, atau lapisan eksekusi alat Anda sendiri
- **Sesi stateful** - Sistem file persisten dan riwayat percakapan di seluruh interaksi berganda

## Alat yang didukung

Claude Managed Agents memberikan Claude akses ke serangkaian alat bawaan yang komprehensif:

- **Bash** - Jalankan perintah shell di kontainer
- **Operasi file** - Baca, tulis, edit, glob, dan grep file di kontainer
- **Pencarian web dan pengambilan** - Cari web dan ambil konten dari URL
- **Server MCP** - Terhubung ke penyedia alat eksternal

Lihat [Tools](/docs/id/managed-agents/tools) untuk daftar lengkap dan opsi konfigurasi.

## Akses beta
<Note>
Claude Managed Agents saat ini dalam beta. Semua endpoint Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK secara otomatis menetapkan header beta. Perilaku dapat disempurnakan antar rilis untuk meningkatkan output.
</Note>

Untuk memulai, Anda membutuhkan:

1. [Kunci API Claude](/settings/keys)
2. Header beta di atas pada semua permintaan
3. Akses ke Claude Managed Agents (diaktifkan secara default untuk semua akun API)

Fitur tertentu ([outcomes](/docs/id/managed-agents/define-outcomes), [multiagent](/docs/id/managed-agents/multi-agent), dan [memory](/docs/id/managed-agents/memory)) berada dalam pratinjau penelitian. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.

## Batas laju

Endpoint Managed Agents dibatasi laju per organisasi:

| Operasi | Batas |
| --- | --- |
| Buat endpoint (agen, sesi, lingkungan, dll.) | 60 permintaan per menit |
| Baca endpoint (ambil, daftar, streaming, dll.) | 600 permintaan per menit |

[Batas pengeluaran](/docs/id/api/rate-limits) tingkat organisasi dan batas laju berbasis tingkat juga berlaku.

## Pedoman branding

Untuk mitra yang mengintegrasikan Claude Managed Agents, penggunaan branding Claude bersifat opsional. Saat mereferensikan Claude di produk Anda:

**Diizinkan:**
- "Claude Agent" (lebih disukai untuk menu dropdown)
- "Claude" (ketika sudah dalam menu berlabel "Agents")
- "{YourAgentName} Powered by Claude" (jika Anda memiliki nama agen yang ada)

**Tidak diizinkan:**
- "Claude Code" atau "Claude Code Agent"
- "Claude Cowork" atau "Claude Cowork Agent"
- ASCII art bermerek Claude Code atau elemen visual yang meniru Claude Code

Produk Anda harus mempertahankan branding sendiri dan tidak boleh terlihat seperti Claude Code, Claude Cowork, atau produk Anthropic lainnya. Untuk pertanyaan tentang kepatuhan branding, hubungi [tim penjualan](https://www.anthropic.com/contact-sales) Anthropic.