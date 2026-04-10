---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/overview
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 3c80b9c92cff534a84b2c658df6587bbea0744034090be915e14d76c07093dbf
---

# Ikhtisar Claude Managed Agents

Harness agen yang sudah dibuat sebelumnya dan dapat dikonfigurasi yang berjalan di infrastruktur terkelola. Terbaik untuk tugas yang berjalan lama dan pekerjaan asinkron.

---

Anthropic offers two ways to build with Claude, each suited to different use cases:

| | Messages API | Claude Managed Agents |
|---|---|---|
| **What it is** | Direct model prompting access | Pre-built, configurable agent harness that runs in managed infrastructure |
| **Best for** | Custom agent loops and fine-grained control | Long-running tasks and asynchronous work |
| **Learn more** | [Messages API docs](/docs/en/build-with-claude/working-with-messages) | [Claude Managed Agents docs](/docs/en/managed-agents/overview) |

Claude Managed Agents menyediakan harness dan infrastruktur untuk menjalankan Claude sebagai agen otonom. Alih-alih membangun loop agen, eksekusi alat, dan runtime Anda sendiri, Anda mendapatkan lingkungan yang sepenuhnya terkelola di mana Claude dapat membaca file, menjalankan perintah, menjelajahi web, dan mengeksekusi kode dengan aman. Harness mendukung prompt caching bawaan, kompaksi, dan optimasi performa lainnya untuk output agen yang berkualitas tinggi dan efisien.

<CardGroup cols={2}>
  <Card title="Quickstart" icon="play" href="/docs/id/managed-agents/quickstart">
    Buat sesi agen pertama Anda
  </Card>
  <Card title="Referensi API" icon="code-brackets" href="/docs/id/api/beta/sessions">
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
    Tentukan model, system prompt, alat, server MCP, dan skill. Buat agen sekali dan referensikan berdasarkan ID di seluruh sesi.
  </Step>
  <Step title="Buat lingkungan">
    Konfigurasikan container cloud dengan paket yang sudah terinstal (Python, Node.js, Go, dll.), aturan akses jaringan, dan file yang dipasang.
  </Step>
  <Step title="Mulai sesi">
    Luncurkan sesi yang mereferensikan konfigurasi agen dan lingkungan Anda.
  </Step>
  <Step title="Kirim event dan streaming respons">
    Kirim pesan pengguna sebagai event. Claude secara otonom mengeksekusi alat dan melakukan streaming hasil kembali melalui server-sent events (SSE). Riwayat event disimpan di sisi server dan dapat diambil secara lengkap.
  </Step>
  <Step title="Arahkan atau hentikan">
    Kirim event pengguna tambahan untuk memandu agen di tengah eksekusi, atau hentikan untuk mengubah arah.
  </Step>
</Steps>

## Kapan menggunakan Claude Managed Agents

Claude Managed Agents paling cocok untuk beban kerja yang membutuhkan:

- **Eksekusi jangka panjang** - Tugas yang berjalan selama menit atau jam dengan beberapa pemanggilan alat
- **Infrastruktur cloud** - Container aman dengan paket yang sudah terinstal dan akses jaringan
- **Infrastruktur minimal** - Tidak perlu membangun loop agen, sandbox, atau lapisan eksekusi alat sendiri
- **Sesi stateful** - Sistem file persisten dan riwayat percakapan di berbagai interaksi

## Alat yang didukung

Claude Managed Agents memberi Claude akses ke serangkaian alat bawaan yang komprehensif:

- **Bash** - Jalankan perintah shell di container
- **Operasi file** - Baca, tulis, edit, glob, dan grep file di container
- **Pencarian dan pengambilan web** - Cari web dan ambil konten dari URL
- **Server MCP** - Hubungkan ke penyedia alat eksternal

Lihat [Alat](/docs/id/managed-agents/tools) untuk daftar lengkap dan opsi konfigurasi.

## Akses beta
<Note>
Claude Managed Agents saat ini dalam versi beta. Semua endpoint Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis. Perilaku dapat disempurnakan antar rilis untuk meningkatkan output.
</Note>

Untuk memulai, Anda memerlukan:

1. [Kunci API Claude](/settings/keys)
2. Header beta di atas pada semua permintaan
3. Akses ke Claude Managed Agents (diaktifkan secara default untuk semua akun API)

Fitur tertentu ([outcomes](/docs/id/managed-agents/define-outcomes), [multiagent](/docs/id/managed-agents/multi-agent), dan [memory](/docs/id/managed-agents/memory)) berada dalam pratinjau penelitian. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.

## Batas laju

Endpoint Managed Agents dibatasi lajunya per organisasi:

| Operasi | Batas |
| --- | --- |
| Endpoint pembuatan (agen, sesi, lingkungan, dll.) | 60 permintaan per menit |
| Endpoint baca (ambil, daftar, streaming, dll.) | 600 permintaan per menit |

[Batas pengeluaran dan batas laju berbasis tingkatan](/docs/id/api/rate-limits) tingkat organisasi juga berlaku.

## Panduan merek

Untuk mitra yang mengintegrasikan Claude Managed Agents, penggunaan merek Claude bersifat opsional. Saat mereferensikan Claude dalam produk Anda:

**Diizinkan:**
- "Claude Agent" (lebih disukai untuk menu dropdown)
- "Claude" (saat berada dalam menu yang sudah berlabel "Agents")
- "{NamaAgenAnda} Powered by Claude" (jika Anda memiliki nama agen yang sudah ada)

**Tidak diizinkan:**
- "Claude Code" atau "Claude Code Agent"
- "Claude Cowork" atau "Claude Cowork Agent"
- Seni ASCII bermerek Claude Code atau elemen visual yang meniru Claude Code

Produk Anda harus mempertahankan mereknya sendiri dan tidak tampak seperti Claude Code, Claude Cowork, atau produk Anthropic lainnya. Untuk pertanyaan tentang kepatuhan merek, hubungi [tim penjualan](https://www.anthropic.com/contact-sales) Anthropic.