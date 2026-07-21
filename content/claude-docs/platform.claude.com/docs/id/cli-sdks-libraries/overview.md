---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/overview
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: c335511c40910c0d2132ac946863e08f7d9d3681612f9881d949076afc4bce5d
---

# CLI, SDK, dan pustaka

Alat resmi untuk membangun dengan Claude API: CLI ant, SDK klien dalam tujuh bahasa, dan pustaka khusus framework.

---

Anthropic menyediakan tiga jenis perkakas resmi untuk membangun dengan Claude API:

* **CLI:** Alat baris perintah `ant` untuk shell scripting dan penggunaan interaktif.
* **SDK Klien:** Klien Messages API serbaguna untuk Python, TypeScript, C#, Go, Java, PHP, dan Ruby. Setiap SDK menyediakan antarmuka yang idiomatik, keamanan tipe, dan dukungan bawaan untuk streaming, percobaan ulang, dan penanganan kesalahan.
* **Pustaka dan integrasi:** Paket dan lapisan kompatibilitas yang mengekspos Claude di dalam permukaan API framework lain alih-alih Messages API secara langsung.

<Info>
  Untuk spesifikasi API lengkap, lihat [referensi API](/docs/id/api/overview).
</Info>

## CLI

<CardGroup cols={3}>
  <Card title="ant CLI" href="/docs/id/cli-sdks-libraries/cli/quickstart">
    Shell scripting, flag bertipe, transformasi respons
  </Card>
</CardGroup>

## SDK Klien

<CardGroup cols={3}>
  <Card title="Python" href="/docs/id/cli-sdks-libraries/sdks/python">
    Klien sync dan async, model Pydantic
  </Card>

  <Card title="TypeScript" href="/docs/id/cli-sdks-libraries/sdks/typescript">
    Dukungan Node.js, Deno, Bun, dan browser
  </Card>

  <Card title="C#" href="/docs/id/cli-sdks-libraries/sdks/csharp">
    .NET Standard 2.0+, integrasi IChatClient
  </Card>

  <Card title="Go" href="/docs/id/cli-sdks-libraries/sdks/go">
    Pembatalan berbasis context, opsi fungsional
  </Card>

  <Card title="Java" href="/docs/id/cli-sdks-libraries/sdks/java">
    Pola builder, async CompletableFuture
  </Card>

  <Card title="PHP" href="/docs/id/cli-sdks-libraries/sdks/php">
    Value object, pola builder
  </Card>

  <Card title="Ruby" href="/docs/id/cli-sdks-libraries/sdks/ruby">
    Tipe Sorbet, helper streaming
  </Card>
</CardGroup>

## Pustaka dan integrasi

Pustaka dan integrasi mengekspos Claude melalui permukaan API framework lain. Keduanya bukan klien Messages API serbaguna.

<CardGroup cols={3}>
  <Card title="Apple Foundation Models" href="/docs/id/cli-sdks-libraries/libraries/apple-foundation-models">
    Paket Swift untuk API `LanguageModelSession` dari Apple
  </Card>

  <Card title="Kompatibilitas OpenAI SDK" href="/docs/id/cli-sdks-libraries/libraries/openai-sdk">
    Gunakan Claude melalui permukaan OpenAI SDK
  </Card>
</CardGroup>

## Membangun agen atau menggunakan Claude Code?

CLI, SDK klien, dan pustaka ditujukan untuk memanggil Claude API sendiri: Anda mengirim setiap permintaan dan menangani setiap respons. Claude Code, Claude Agent SDK, dan Claude Managed Agents bekerja pada tingkat yang lebih tinggi, menyediakan loop agen, eksekusi alat, dan runtime.

<CardGroup cols={3}>
  <Card title="Claude Code" href="https://code.claude.com/docs/id/overview">
    Alat coding agentik untuk mendelegasikan tugas coding kepada Claude
  </Card>

  <Card title="Claude Agent SDK" href="https://code.claude.com/docs/id/agent-sdk/overview">
    Bangun agen yang berjalan dalam proses yang Anda operasikan
  </Card>

  <Card title="Claude Managed Agents" href="/docs/id/managed-agents/overview">
    Jalankan agen di infrastruktur terkelola Anthropic
  </Card>
</CardGroup>
