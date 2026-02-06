---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/overview
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: db6286563fe03a7e0dc49714a3dcdef8b1396038f26ba93e9a20f57dc406e05d
---

# Ringkasan Agent SDK

Bangun agen AI produksi dengan Claude Code sebagai perpustakaan

---

<Note>
Claude Code SDK telah diubah namanya menjadi Claude Agent SDK. Jika Anda bermigrasi dari SDK lama, lihat [Panduan Migrasi](/docs/id/agent-sdk/migration-guide).
</Note>

Bangun agen AI yang secara mandiri membaca file, menjalankan perintah, mencari web, mengedit kode, dan banyak lagi. Agent SDK memberi Anda alat yang sama, loop agen, dan manajemen konteks yang mendukung Claude Code, dapat diprogram dalam Python dan TypeScript.

<CodeGroup>
```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"])
    ):
        print(message)  # Claude reads the file, finds the bug, edits it

asyncio.run(main())
```

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find and fix the bug in auth.py",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  console.log(message);  // Claude reads the file, finds the bug, edits it
}
```
</CodeGroup>

Agent SDK mencakup alat bawaan untuk membaca file, menjalankan perintah, dan mengedit kode, sehingga agen Anda dapat mulai bekerja segera tanpa Anda perlu mengimplementasikan eksekusi alat. Selami panduan cepat atau jelajahi agen nyata yang dibangun dengan SDK:

<CardGroup cols={2}>
  <Card title="Panduan Cepat" icon="play" href="/docs/id/agent-sdk/quickstart">
    Bangun agen perbaikan bug dalam hitungan menit
  </Card>
  <Card title="Agen contoh" icon="star" href="https://github.com/anthropics/claude-agent-sdk-demos">
    Asisten email, agen penelitian, dan banyak lagi
  </Card>
</CardGroup>

## Memulai

<Steps>
  <Step title="Instal SDK">
    <Tabs>
      <Tab title="TypeScript">
        ```bash
        npm install @anthropic-ai/claude-agent-sdk
        ```
      </Tab>
      <Tab title="Python">
        ```bash
        pip install claude-agent-sdk
        ```
      </Tab>
    </Tabs>
  </Step>
  <Step title="Atur kunci API Anda">
    Dapatkan kunci API dari [Konsol](https://platform.claude.com/), kemudian atur sebagai variabel lingkungan:

    ```bash
    export ANTHROPIC_API_KEY=your-api-key
    ```

    SDK juga mendukung autentikasi melalui penyedia API pihak ketiga:

    - **Amazon Bedrock**: atur variabel lingkungan `CLAUDE_CODE_USE_BEDROCK=1` dan konfigurasi kredensial AWS
    - **Google Vertex AI**: atur variabel lingkungan `CLAUDE_CODE_USE_VERTEX=1` dan konfigurasi kredensial Google Cloud
    - **Microsoft Azure**: atur variabel lingkungan `CLAUDE_CODE_USE_FOUNDRY=1` dan konfigurasi kredensial Azure

    Lihat panduan penyiapan untuk [Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), atau [Azure AI Foundry](https://code.claude.com/docs/en/azure-ai-foundry) untuk detail.

    <Note>
    Kecuali sebelumnya disetujui, Anthropic tidak mengizinkan pengembang pihak ketiga untuk menawarkan login claude.ai atau batasan tingkat untuk produk mereka, termasuk agen yang dibangun di Claude Agent SDK. Silakan gunakan metode autentikasi kunci API yang dijelaskan dalam dokumen ini.
    </Note>
  </Step>
  <Step title="Jalankan agen pertama Anda">
    Contoh ini membuat agen yang mencantumkan file di direktori saat ini menggunakan alat bawaan.

    <CodeGroup>
    ```python Python
    import asyncio
    from claude_agent_sdk import query, ClaudeAgentOptions

    async def main():
        async for message in query(
            prompt="What files are in this directory?",
            options=ClaudeAgentOptions(allowed_tools=["Bash", "Glob"])
        ):
            if hasattr(message, "result"):
                print(message.result)

    asyncio.run(main())
    ```

    ```typescript TypeScript
    import { query } from "@anthropic-ai/claude-agent-sdk";

    for await (const message of query({
      prompt: "What files are in this directory?",
      options: { allowedTools: ["Bash", "Glob"] },
    })) {
      if ("result" in message) console.log(message.result);
    }
    ```
    </CodeGroup>
  </Step>
</Steps>

**Siap untuk membangun?** Ikuti [Panduan Cepat](/docs/id/agent-sdk/quickstart) untuk membuat agen yang menemukan dan memperbaiki bug dalam hitungan menit.

## Kemampuan

Semua yang membuat Claude Code kuat tersedia di SDK:

<Tabs>
  <Tab title="Alat bawaan">
    Agen Anda dapat membaca file, menjalankan perintah, dan mencari basis kode langsung dari kotak. Alat kunci meliputi:

    | Alat | Apa yang dilakukannya |
    |------|--------------|
    | **Read** | Baca file apa pun di direktori kerja |
    | **Write** | Buat file baru |
    | **Edit** | Buat pengeditan presisi pada file yang ada |
    | **Bash** | Jalankan perintah terminal, skrip, operasi git |
    | **Glob** | Temukan file berdasarkan pola (`**/*.ts`, `src/**/*.py`) |
    | **Grep** | Cari konten file dengan regex |
    | **WebSearch** | Cari web untuk informasi terkini |
    | **WebFetch** | Ambil dan parse konten halaman web |
    | **[AskUserQuestion](/docs/id/agent-sdk/user-input#handle-clarifying-questions)** | Tanyakan pertanyaan klarifikasi kepada pengguna dengan opsi pilihan ganda |

    Contoh ini membuat agen yang mencari basis kode Anda untuk komentar TODO:

    <CodeGroup>
    ```python Python
    import asyncio
    from claude_agent_sdk import query, ClaudeAgentOptions

    async def main():
        async for message in query(
            prompt="Find all TODO comments and create a summary",
            options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"])
        ):
            if hasattr(message, "result"):
                print(message.result)

    asyncio.run(main())
    ```

    ```typescript TypeScript
    import { query } from "@anthropic-ai/claude-agent-sdk";

    for await (const message of query({
      prompt: "Find all TODO comments and create a summary",
      options: { allowedTools: ["Read", "Glob", "Grep"] }
    })) {
      if ("result" in message) console.log(message.result);
    }
    ```
    </CodeGroup>

  </Tab>
  <Tab title="Hooks">
    Jalankan kode khusus pada titik-titik kunci dalam siklus hidup agen. Hook SDK menggunakan fungsi callback untuk memvalidasi, mencatat, memblokir, atau mengubah perilaku agen.

    **Hook yang tersedia:** `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, dan banyak lagi.

    Contoh ini mencatat semua perubahan file ke file audit:

    <CodeGroup>
    ```python Python
    import asyncio
    from datetime import datetime
    from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

    async def log_file_change(input_data, tool_use_id, context):
        file_path = input_data.get('tool_input', {}).get('file_path', 'unknown')
        with open('./audit.log', 'a') as f:
            f.write(f"{datetime.now()}: modified {file_path}\n")
        return {}

    async def main():
        async for message in query(
            prompt="Refactor utils.py to improve readability",
            options=ClaudeAgentOptions(
                permission_mode="acceptEdits",
                hooks={
                    "PostToolUse": [HookMatcher(matcher="Edit|Write", hooks=[log_file_change])]
                }
            )
        ):
            if hasattr(message, "result"):
                print(message.result)

    asyncio.run(main())
    ```

    ```typescript TypeScript
    import { query, HookCallback } from "@anthropic-ai/claude-agent-sdk";
    import { appendFileSync } from "fs";

    const logFileChange: HookCallback = async (input) => {
      const filePath = (input as any).tool_input?.file_path ?? "unknown";
      appendFileSync("./audit.log", `${new Date().toISOString()}: modified ${filePath}\n`);
      return {};
    };

    for await (const message of query({
      prompt: "Refactor utils.py to improve readability",
      options: {
        permissionMode: "acceptEdits",
        hooks: {
          PostToolUse: [{ matcher: "Edit|Write", hooks: [logFileChange] }]
        }
      }
    })) {
      if ("result" in message) console.log(message.result);
    }
    ```
    </CodeGroup>

    [Pelajari lebih lanjut tentang hooks →](/docs/id/agent-sdk/hooks)
  </Tab>
  <Tab title="Subagents">
    Spawn agen khusus untuk menangani subtask yang terfokus. Agen utama Anda mendelegasikan pekerjaan, dan subagen melaporkan kembali dengan hasil.

    Tentukan agen khusus dengan instruksi khusus. Sertakan `Task` dalam `allowedTools` karena subagen dipanggil melalui alat Task:

    <CodeGroup>
    ```python Python
    import asyncio
    from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

    async def main():
        async for message in query(
            prompt="Use the code-reviewer agent to review this codebase",
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Glob", "Grep", "Task"],
                agents={
                    "code-reviewer": AgentDefinition(
                        description="Expert code reviewer for quality and security reviews.",
                        prompt="Analyze code quality and suggest improvements.",
                        tools=["Read", "Glob", "Grep"]
                    )
                }
            )
        ):
            if hasattr(message, "result"):
                print(message.result)

    asyncio.run(main())
    ```

    ```typescript TypeScript
    import { query } from "@anthropic-ai/claude-agent-sdk";

    for await (const message of query({
      prompt: "Use the code-reviewer agent to review this codebase",
      options: {
        allowedTools: ["Read", "Glob", "Grep", "Task"],
        agents: {
          "code-reviewer": {
            description: "Expert code reviewer for quality and security reviews.",
            prompt: "Analyze code quality and suggest improvements.",
            tools: ["Read", "Glob", "Grep"]
          }
        }
      }
    })) {
      if ("result" in message) console.log(message.result);
    }
    ```
    </CodeGroup>

    Pesan dari dalam konteks subagen mencakup bidang `parent_tool_use_id`, memungkinkan Anda melacak pesan mana yang termasuk dalam eksekusi subagen mana.

    [Pelajari lebih lanjut tentang subagents →](/docs/id/agent-sdk/subagents)
  </Tab>
  <Tab title="MCP">
    Terhubung ke sistem eksternal melalui Model Context Protocol: database, browser, API, dan [ratusan lainnya](https://github.com/modelcontextprotocol/servers).

    Contoh ini menghubungkan [server Playwright MCP](https://github.com/microsoft/playwright-mcp) untuk memberikan agen Anda kemampuan otomasi browser:

    <CodeGroup>
    ```python Python
    import asyncio
    from claude_agent_sdk import query, ClaudeAgentOptions

    async def main():
        async for message in query(
            prompt="Open example.com and describe what you see",
            options=ClaudeAgentOptions(
                mcp_servers={
                    "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
                }
            )
        ):
            if hasattr(message, "result"):
                print(message.result)

    asyncio.run(main())
    ```

    ```typescript TypeScript
    import { query } from "@anthropic-ai/claude-agent-sdk";

    for await (const message of query({
      prompt: "Open example.com and describe what you see",
      options: {
        mcpServers: {
          playwright: { command: "npx", args: ["@playwright/mcp@latest"] }
        }
      }
    })) {
      if ("result" in message) console.log(message.result);
    }
    ```
    </CodeGroup>

    [Pelajari lebih lanjut tentang MCP →](/docs/id/agent-sdk/mcp)
  </Tab>
  <Tab title="Izin">
    Kontrol dengan tepat alat mana yang dapat digunakan agen Anda. Izinkan operasi yang aman, blokir yang berbahaya, atau minta persetujuan untuk tindakan sensitif.

    <Note>
    Untuk prompt persetujuan interaktif dan alat `AskUserQuestion`, lihat [Tangani persetujuan dan input pengguna](/docs/id/agent-sdk/user-input).
    </Note>

    Contoh ini membuat agen hanya-baca yang dapat menganalisis tetapi tidak memodifikasi kode:

    <CodeGroup>
    ```python Python
    import asyncio
    from claude_agent_sdk import query, ClaudeAgentOptions

    async def main():
        async for message in query(
            prompt="Review this code for best practices",
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Glob", "Grep"],
                permission_mode="bypassPermissions"
            )
        ):
            if hasattr(message, "result"):
                print(message.result)

    asyncio.run(main())
    ```

    ```typescript TypeScript
    import { query } from "@anthropic-ai/claude-agent-sdk";

    for await (const message of query({
      prompt: "Review this code for best practices",
      options: {
        allowedTools: ["Read", "Glob", "Grep"],
        permissionMode: "bypassPermissions"
      }
    })) {
      if ("result" in message) console.log(message.result);
    }
    ```
    </CodeGroup>

    [Pelajari lebih lanjut tentang izin →](/docs/id/agent-sdk/permissions)
  </Tab>
  <Tab title="Sesi">
    Pertahankan konteks di seluruh pertukaran ganda. Claude mengingat file yang dibaca, analisis yang dilakukan, dan riwayat percakapan. Lanjutkan sesi nanti, atau fork mereka untuk menjelajahi pendekatan berbeda.

    Contoh ini menangkap ID sesi dari kueri pertama, kemudian melanjutkan untuk terus dengan konteks penuh:

    <CodeGroup>
    ```python Python
    import asyncio
    from claude_agent_sdk import query, ClaudeAgentOptions

    async def main():
        session_id = None

        # First query: capture the session ID
        async for message in query(
            prompt="Read the authentication module",
            options=ClaudeAgentOptions(allowed_tools=["Read", "Glob"])
        ):
            if hasattr(message, 'subtype') and message.subtype == 'init':
                session_id = message.session_id

        # Resume with full context from the first query
        async for message in query(
            prompt="Now find all places that call it",  # "it" = auth module
            options=ClaudeAgentOptions(resume=session_id)
        ):
            if hasattr(message, "result"):
                print(message.result)

    asyncio.run(main())
    ```

    ```typescript TypeScript
    import { query } from "@anthropic-ai/claude-agent-sdk";

    let sessionId: string | undefined;

    // First query: capture the session ID
    for await (const message of query({
      prompt: "Read the authentication module",
      options: { allowedTools: ["Read", "Glob"] }
    })) {
      if (message.type === "system" && message.subtype === "init") {
        sessionId = message.session_id;
      }
    }

    // Resume with full context from the first query
    for await (const message of query({
      prompt: "Now find all places that call it",  // "it" = auth module
      options: { resume: sessionId }
    })) {
      if ("result" in message) console.log(message.result);
    }
    ```
    </CodeGroup>

    [Pelajari lebih lanjut tentang sesi →](/docs/id/agent-sdk/sessions)
  </Tab>
</Tabs>

### Fitur Claude Code

SDK juga mendukung konfigurasi berbasis sistem file Claude Code. Untuk menggunakan fitur ini, atur `setting_sources=["project"]` (Python) atau `settingSources: ['project']` (TypeScript) dalam opsi Anda.

| Fitur | Deskripsi | Lokasi |
|---------|-------------|----------|
| [Skills](/docs/id/agent-sdk/skills) | Kemampuan khusus yang ditentukan dalam Markdown | `.claude/skills/SKILL.md` |
| [Slash commands](/docs/id/agent-sdk/slash-commands) | Perintah khusus untuk tugas umum | `.claude/commands/*.md` |
| [Memory](/docs/id/agent-sdk/modifying-system-prompts) | Konteks proyek dan instruksi | `CLAUDE.md` atau `.claude/CLAUDE.md` |
| [Plugins](/docs/id/agent-sdk/plugins) | Perluas dengan perintah khusus, agen, dan server MCP | Programmatic via `plugins` option |

## Bandingkan Agent SDK dengan alat Claude lainnya

Platform Claude menawarkan berbagai cara untuk membangun dengan Claude. Berikut cara Agent SDK cocok:

<Tabs>
  <Tab title="Agent SDK vs Client SDK">
    [Anthropic Client SDK](/docs/id/api/client-sdks) memberi Anda akses API langsung: Anda mengirim prompt dan mengimplementasikan eksekusi alat sendiri. **Agent SDK** memberi Anda Claude dengan eksekusi alat bawaan.

    Dengan Client SDK, Anda mengimplementasikan loop alat. Dengan Agent SDK, Claude menanganinya:

    <CodeGroup>
    ```python Python
    # Client SDK: You implement the tool loop
    response = client.messages.create(...)
    while response.stop_reason == "tool_use":
        result = your_tool_executor(response.tool_use)
        response = client.messages.create(tool_result=result, ...)

    # Agent SDK: Claude handles tools autonomously
    async for message in query(prompt="Fix the bug in auth.py"):
        print(message)
    ```

    ```typescript TypeScript
    // Client SDK: You implement the tool loop
    let response = await client.messages.create({...});
    while (response.stop_reason === "tool_use") {
      const result = yourToolExecutor(response.tool_use);
      response = await client.messages.create({ tool_result: result, ... });
    }

    // Agent SDK: Claude handles tools autonomously
    for await (const message of query({ prompt: "Fix the bug in auth.py" })) {
      console.log(message);
    }
    ```
    </CodeGroup>
  </Tab>
  <Tab title="Agent SDK vs Claude Code CLI">
    Kemampuan yang sama, antarmuka berbeda:

    | Kasus penggunaan | Pilihan terbaik |
    |----------|-------------|
    | Pengembangan interaktif | CLI |
    | Pipa CI/CD | SDK |
    | Aplikasi khusus | SDK |
    | Tugas sekali jalan | CLI |
    | Otomasi produksi | SDK |

    Banyak tim menggunakan keduanya: CLI untuk pengembangan harian, SDK untuk produksi. Alur kerja diterjemahkan langsung di antara keduanya.
  </Tab>
</Tabs>

## Changelog

Lihat changelog lengkap untuk pembaruan SDK, perbaikan bug, dan fitur baru:

- **TypeScript SDK**: [lihat CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/CHANGELOG.md)
- **Python SDK**: [lihat CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-python/blob/main/CHANGELOG.md)

## Melaporkan bug

Jika Anda menemukan bug atau masalah dengan Agent SDK:

- **TypeScript SDK**: [laporkan masalah di GitHub](https://github.com/anthropics/claude-agent-sdk-typescript/issues)
- **Python SDK**: [laporkan masalah di GitHub](https://github.com/anthropics/claude-agent-sdk-python/issues)

## Pedoman branding

Untuk mitra yang mengintegrasikan Claude Agent SDK, penggunaan branding Claude bersifat opsional. Saat mereferensikan Claude di produk Anda:

**Diizinkan:**
- "Claude Agent" (lebih disukai untuk menu dropdown)
- "Claude" (ketika sudah dalam menu berlabel "Agents")
- "{YourAgentName} Powered by Claude" (jika Anda memiliki nama agen yang ada)

**Tidak diizinkan:**
- "Claude Code" atau "Claude Code Agent"
- Elemen visual atau ASCII art bermerek Claude Code yang meniru Claude Code

Produk Anda harus mempertahankan branding sendiri dan tidak boleh terlihat seperti Claude Code atau produk Anthropic apa pun. Untuk pertanyaan tentang kepatuhan branding, hubungi [tim penjualan](https://www.anthropic.com/contact-sales) kami.

## Lisensi dan persyaratan

Penggunaan Claude Agent SDK diatur oleh [Persyaratan Layanan Komersial Anthropic](https://www.anthropic.com/legal/commercial-terms), termasuk ketika Anda menggunakannya untuk memberdayakan produk dan layanan yang Anda buat tersedia untuk pelanggan dan pengguna akhir Anda sendiri, kecuali sejauh komponen atau dependensi tertentu dicakup oleh lisensi berbeda seperti yang ditunjukkan dalam file LICENSE komponen tersebut.

## Langkah berikutnya

<CardGroup cols={2}>
  <Card title="Panduan Cepat" icon="play" href="/docs/id/agent-sdk/quickstart">
    Bangun agen yang menemukan dan memperbaiki bug dalam hitungan menit
  </Card>
  <Card title="Agen contoh" icon="star" href="https://github.com/anthropics/claude-agent-sdk-demos">
    Asisten email, agen penelitian, dan banyak lagi
  </Card>
  <Card title="TypeScript SDK" icon="code" href="/docs/id/agent-sdk/typescript">
    Referensi API TypeScript lengkap dan contoh
  </Card>
  <Card title="Python SDK" icon="code" href="/docs/id/agent-sdk/python">
    Referensi API Python lengkap dan contoh
  </Card>
</CardGroup>