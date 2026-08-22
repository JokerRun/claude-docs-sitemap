---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/overview
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: d7b7c7f913c572400c7f11eb28da07eefc02d4e27c3bc13a2fcdf108326ee32f
---

---
title: CLI, SDK, dan pustaka
url: https://platform.claude.com/docs/id/cli-sdks-libraries/overview
description: "Alat resmi untuk membangun dengan Claude API: CLI ant, SDK klien dalam tujuh bahasa, dan pustaka khusus framework."
---

Anthropic menyediakan tiga jenis perkakas resmi untuk membangun dengan Claude API:

* **CLI:** Alat baris perintah `ant` untuk shell scripting dan penggunaan interaktif.
* **SDK Klien:** Klien Messages API serbaguna untuk Python, TypeScript, C#, Go, Java, PHP, dan Ruby. Setiap SDK menyediakan antarmuka yang idiomatik, keamanan tipe, dan dukungan bawaan untuk streaming, percobaan ulang, dan penanganan kesalahan.
* **Pustaka dan integrasi:** Paket dan lapisan kompatibilitas yang mengekspos Claude di dalam permukaan API framework lain alih-alih Messages API secara langsung.

<Info>
  Untuk spesifikasi API lengkap, lihat [referensi API](https://platform.claude.com/docs/id/api/overview).
</Info>

## CLI

<CardGroup cols={3}>
  <Card title="ant CLI" href="https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart">
    Shell scripting, flag bertipe, transformasi respons
  </Card>
</CardGroup>

## SDK Klien

<CardGroup cols={3}>
  <Card title="Python" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python">
    Klien sync dan async, model Pydantic
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
    Pola builder, async CompletableFuture
  </Card>

  <Card title="PHP" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php">
    Value object, pola builder
  </Card>

  <Card title="Ruby" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/ruby">
    Tipe Sorbet, helper streaming
  </Card>
</CardGroup>

## Pustaka dan integrasi

Pustaka dan integrasi mengekspos Claude melalui permukaan API framework lain. Keduanya bukan klien Messages API serbaguna.

<CardGroup cols={3}>
  <Card title="Apple Foundation Models" href="https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models">
    Paket Swift untuk API `LanguageModelSession` dari Apple
  </Card>

  <Card title="Kompatibilitas OpenAI SDK" href="https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk">
    Gunakan Claude melalui permukaan OpenAI SDK
  </Card>
</CardGroup>

## Membangun agen atau menggunakan Claude Code?

CLI, SDK klien, dan pustaka ditujukan untuk memanggil Claude API sendiri: Anda mengirim setiap permintaan dan menangani setiap respons. Claude Code, Claude Agent SDK, dan Claude Managed Agents bekerja pada tingkat yang lebih tinggi, menyediakan loop agen, eksekusi alat, dan runtime.

<CardGroup cols={3}>
  <Card title="Claude Code" href="https://code.claude.com/docs/en/overview">
    Alat coding agentik untuk mendelegasikan tugas coding kepada Claude
  </Card>

  <Card title="Claude Agent SDK" href="https://code.claude.com/docs/en/agent-sdk/overview">
    Bangun agen yang berjalan dalam proses yang Anda operasikan
  </Card>

  <Card title="Claude Managed Agents" href="https://platform.claude.com/docs/id/managed-agents/overview">
    Jalankan agen di infrastruktur terkelola Anthropic
  </Card>
</CardGroup>
