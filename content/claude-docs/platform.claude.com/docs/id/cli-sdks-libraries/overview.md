---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/overview
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 794110e224117759487bb5258d4d8d3813634805a332ca0337b1961b2dae980e
---

---
title: CLI, SDK, dan library
url: https://platform.claude.com/docs/id/cli-sdks-libraries/overview
description: "Alat resmi untuk membangun dengan Claude API: CLI ant, SDK klien dalam tujuh bahasa, dan library khusus framework."
---

Anthropic menyediakan tiga jenis alat resmi untuk membangun dengan Claude API:

* **CLI:** Alat baris perintah `ant` untuk scripting shell dan penggunaan interaktif.
* **SDK klien:** Klien Messages API serbaguna untuk Python, TypeScript, C#, Go, Java, PHP, dan Ruby. Setiap SDK menyediakan antarmuka idiomatis, keamanan tipe, dan dukungan bawaan untuk streaming, percobaan ulang, dan penanganan error.
* **Library dan integrasi:** Paket dan lapisan kompatibilitas yang mengekspos Claude di dalam permukaan API framework lain, bukan Messages API secara langsung.

<Info>
  Untuk spesifikasi API lengkap, lihat [referensi API](https://platform.claude.com/docs/id/api/overview).
</Info>

## CLI

<CardGroup cols={3}>
  <Card title="CLI ant" href="https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart">
    Scripting shell, flag bertipe, transformasi respons
  </Card>
</CardGroup>

## SDK klien

<CardGroup cols={3}>
  <Card title="Python" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python">
    Klien sinkron dan asinkron, model Pydantic
  </Card>

  <Card title="TypeScript" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript">
    Dukungan Node.js, Deno, Bun, dan browser
  </Card>

  <Card title="C#" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/csharp">
    .NET Standard 2.0+, integrasi IChatClient
  </Card>

  <Card title="Go" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go">
    Pembatalan berbasis context, opsi fungsional
  </Card>

  <Card title="Java" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java">
    Pola builder, asinkron dengan CompletableFuture
  </Card>

  <Card title="PHP" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php">
    Value object, pola builder
  </Card>

  <Card title="Ruby" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/ruby">
    Tipe Sorbet, helper streaming
  </Card>
</CardGroup>

## Library dan integrasi

Library dan integrasi mengekspos Claude melalui permukaan API framework lain. Keduanya bukan klien Messages API serbaguna.

<CardGroup cols={3}>
  <Card title="Apple Foundation Models" href="https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models">
    Paket Swift untuk API `LanguageModelSession` milik Apple
  </Card>

  <Card title="Kompatibilitas OpenAI SDK" href="https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk">
    Gunakan Claude melalui permukaan OpenAI SDK
  </Card>
</CardGroup>

## Membangun agen atau menggunakan Claude Code?

CLI, SDK klien, dan library ditujukan untuk memanggil Claude API sendiri: Anda mengirim setiap permintaan dan menangani setiap respons. Claude Code, Claude Agent SDK, dan Claude Managed Agents bekerja pada tingkat yang lebih tinggi, menyediakan loop agen, eksekusi alat, dan runtime.

<CardGroup cols={3}>
  <Card title="Claude Code" href="https://code.claude.com/docs/id/overview">
    Alat coding agentik untuk mendelegasikan tugas coding kepada Claude
  </Card>

  <Card title="Claude Agent SDK" href="https://code.claude.com/docs/id/agent-sdk/overview">
    Bangun agen yang berjalan dalam proses yang Anda operasikan
  </Card>

  <Card title="Claude Managed Agents" href="https://platform.claude.com/docs/id/managed-agents/overview">
    Jalankan agen di infrastruktur terkelola Anthropic
  </Card>
</CardGroup>
