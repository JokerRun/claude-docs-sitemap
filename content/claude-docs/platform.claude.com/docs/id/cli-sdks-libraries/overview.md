---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/overview
fetched_at: 2026-10-22T02:21:21.745661Z
sha256: 0f0794701c536be036b0a932cdc73f38ab755964c1a8e71db45d14923bd75c92
---

---
title: SDK, CLI, dan library
url: https://platform.claude.com/docs/id/cli-sdks-libraries/overview
description: "Alat resmi untuk membangun dengan Claude API: SDK klien dalam tujuh bahasa, CLI ant, dan library khusus framework."
---

Anthropic menyediakan tiga jenis alat resmi untuk membangun dengan Claude API:

* **CLI:** Alat baris perintah `ant` untuk scripting shell dan penggunaan interaktif.
* **SDK klien:** Klien Messages API serbaguna untuk Python, TypeScript, C#, Go, Java, PHP, dan Ruby. Setiap SDK menyediakan antarmuka yang idiomatis, keamanan tipe, serta dukungan bawaan untuk streaming, percobaan ulang, dan penanganan kesalahan.
* **Library dan integrasi:** Paket dan lapisan kompatibilitas yang mengekspos Claude di dalam permukaan API framework lain, alih-alih langsung melalui Messages API.

<Info>
  Untuk spesifikasi API lengkap, lihat [referensi API](https://platform.claude.com/docs/id/api/overview).
</Info>

## CLI

<CardGroup cols={3}>
  <Card title="ant CLI" href="https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart">
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
    Objek nilai, pola builder
  </Card>

  <Card title="Ruby" href="https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/ruby">
    Tipe Sorbet, helper streaming
  </Card>
</CardGroup>

Setiap versi mayor SDK klien mengirimkan satu [versi API](https://platform.claude.com/docs/id/api/versioning) secara default, dan versi mayor baru hadir bersama setiap versi API baru. Untuk beralih ke `2026-10-21`, lihat [Upgrade ke 2026-10-21](https://platform.claude.com/docs/id/api/migration-2026-10-21#upgrade).

## Versi terbaru

| Alat       | Versi terbaru | Paket                                                                                                 |
| ---------- | ------------- | ----------------------------------------------------------------------------------------------------- |
| ant CLI    | `2.1.0`       | [`github.com/anthropics/anthropic-cli`](https://github.com/anthropics/anthropic-cli/releases)         |
| Python     | `2.1.0`       | [`anthropic`](https://pypi.org/project/anthropic/)                                                    |
| TypeScript | `1.1.0`       | [`@anthropic-ai/sdk`](https://www.npmjs.com/package/@anthropic-ai/sdk)                                |
| C#         | `13.1.0`      | [`Anthropic`](https://www.nuget.org/packages/Anthropic)                                               |
| Go         | `2.1.0`       | [`github.com/anthropics/anthropic-sdk-go`](https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go) |
| Java       | `3.1.0`       | [`com.anthropic:anthropic-java`](https://central.sonatype.com/artifact/com.anthropic/anthropic-java)  |
| PHP        | `1.1.0`       | [`anthropic-ai/sdk`](https://packagist.org/packages/anthropic-ai/sdk)                                 |
| Ruby       | `2.1.0`       | [`anthropic`](https://rubygems.org/gems/anthropic)                                                    |

Versi yang sama tersedia dalam format JSON di `https://platform.claude.com/docs/sdk-versions.json`.

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
