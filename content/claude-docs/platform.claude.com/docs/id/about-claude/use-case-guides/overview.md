---
source: platform
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/overview
fetched_at: 2026-09-17T02:21:00.513769Z
sha256: 19df698fa037fa2c8760fc4a036a53b4b6b3f9cee9dea3fd0c2cf863af8103bd
---

---
title: Panduan untuk kasus penggunaan umum
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/overview
description: "Jelajahi panduan produksi untuk membangun kasus penggunaan Claude yang umum: perutean tiket, agen dukungan pelanggan, moderasi konten, peringkasan dokumen hukum, dan agen perdagangan."
---

Claude dirancang untuk unggul dalam berbagai tugas. Jelajahi panduan produksi mendalam ini untuk mempelajari cara membangun kasus penggunaan umum dengan Claude.

<CardGroup cols={2}>
  <Card title="Perutean tiket" icon="headset" href="https://platform.claude.com/docs/id/about-claude/use-case-guides/ticket-routing">
    Praktik terbaik untuk menggunakan Claude dalam mengklasifikasikan dan merutekan tiket dukungan pelanggan dalam skala besar.
  </Card>

  <Card title="Agen dukungan pelanggan" icon="robot" href="https://platform.claude.com/docs/id/about-claude/use-case-guides/customer-support-chat">
    Bangun chatbot cerdas yang sadar konteks dengan Claude untuk meningkatkan interaksi dukungan pelanggan.
  </Card>

  <Card title="Moderasi konten" icon="verified" href="https://platform.claude.com/docs/id/about-claude/use-case-guides/content-moderation">
    Teknik dan praktik terbaik untuk menggunakan Claude dalam melakukan pemfilteran konten dan moderasi konten secara umum.
  </Card>

  <Card title="Peringkasan dokumen hukum" icon="book" href="https://platform.claude.com/docs/id/about-claude/use-case-guides/legal-summarization">
    Ringkas dokumen hukum menggunakan Claude untuk mengekstrak informasi penting dan mempercepat riset.
  </Card>

  <Card title="Agen perdagangan" icon="building" href="https://platform.claude.com/docs/id/about-claude/use-case-guides/commerce-agents">
    Bangun agen belanja dan agen pedagang dari cetak biru sumber terbuka yang berjalan di Messages API, Claude Agent SDK, dan Claude Managed Agents.
  </Card>
</CardGroup>

## Memilih jalur pembangunan

Ketiga jalur untuk membangun dengan Claude berbeda dalam seberapa banyak kendali yang Anda pertahankan dan seberapa banyak implementasi yang Anda serahkan kepada Anthropic. [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) memberi Anda kendali paling besar: Anda menulis "agent loop" (perulangan agen) dan menjalankan alat serta infrastruktur Anda sendiri. [Claude Agent SDK](https://code.claude.com/docs/id/agent-sdk/overview) berada di antara keduanya, menyediakan agent loop dan eksekusi alat dalam proses yang Anda operasikan. Dengan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), Anda menyerahkan paling banyak: Anthropic meng-hosting agent loop, eksekusi alat, dan "runtime" (lingkungan eksekusi) untuk Anda.
