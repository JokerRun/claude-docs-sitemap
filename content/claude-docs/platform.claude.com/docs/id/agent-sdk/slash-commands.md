---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/slash-commands
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 32fd4f6d11cfe68ec44a8ae2176ec9f118e6e184a2f0ff8b04e47c5e6ca20192
---

# Slash Commands dalam SDK

Pelajari cara menggunakan slash commands untuk mengontrol sesi Claude Code melalui SDK

---

Slash commands menyediakan cara untuk mengontrol sesi Claude Code dengan perintah khusus yang dimulai dengan `/`. Perintah-perintah ini dapat dikirim melalui SDK untuk melakukan tindakan seperti menghapus riwayat percakapan, memadatkan pesan, atau mendapatkan bantuan.

## Menemukan Slash Commands yang Tersedia

Claude Agent SDK menyediakan informasi tentang slash commands yang tersedia dalam pesan inisialisasi sistem. Akses informasi ini ketika sesi Anda dimulai:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Hello Claude",
  options: { maxTurns: 1 }
})) {
  if (message.type === "system" && message.subtype === "init") {
    console.log("Available slash commands:", message.slash_commands);
    // Example output: ["/compact", "/clear", "/help"]
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query

async def main():
    async for message in query(
        prompt="Hello Claude",
        options={"max_turns": 1}
    ):
        if message.type == "system" and message.subtype == "init":
            print("Available slash commands:", message.slash_commands)
            # Example output: ["/compact", "/clear", "/help"]

asyncio.run(main())
```

</CodeGroup>

## Mengirim Slash Commands

Kirim slash commands dengan memasukkannya dalam string prompt, seperti teks biasa:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Send a slash command
for await (const message of query({
  prompt: "/compact",
  options: { maxTurns: 1 }
})) {
  if (message.type === "result") {
    console.log("Command executed:", message.result);
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query

async def main():
    # Send a slash command
    async for message in query(
        prompt="/compact",
        options={"max_turns": 1}
    ):
        if message.type == "result":
            print("Command executed:", message.result)

asyncio.run(main())
```

</CodeGroup>

## Slash Commands Umum

### `/compact` - Padatkan Riwayat Percakapan

Perintah `/compact` mengurangi ukuran riwayat percakapan Anda dengan merangkum pesan yang lebih lama sambil mempertahankan konteks penting:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "/compact",
  options: { maxTurns: 1 }
})) {
  if (message.type === "system" && message.subtype === "compact_boundary") {
    console.log("Compaction completed");
    console.log("Pre-compaction tokens:", message.compact_metadata.pre_tokens);
    console.log("Trigger:", message.compact_metadata.trigger);
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query

async def main():
    async for message in query(
        prompt="/compact",
        options={"max_turns": 1}
    ):
        if (message.type == "system" and 
            message.subtype == "compact_boundary"):
            print("Compaction completed")
            print("Pre-compaction tokens:", 
                  message.compact_metadata.pre_tokens)
            print("Trigger:", message.compact_metadata.trigger)

asyncio.run(main())
```

</CodeGroup>

### `/clear` - Hapus Percakapan

Perintah `/clear` memulai percakapan baru dengan menghapus semua riwayat sebelumnya:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Clear conversation and start fresh
for await (const message of query({
  prompt: "/clear",
  options: { maxTurns: 1 }
})) {
  if (message.type === "system" && message.subtype === "init") {
    console.log("Conversation cleared, new session started");
    console.log("Session ID:", message.session_id);
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query

async def main():
    # Clear conversation and start fresh
    async for message in query(
        prompt="/clear",
        options={"max_turns": 1}
    ):
        if message.type == "system" and message.subtype == "init":
            print("Conversation cleared, new session started")
            print("Session ID:", message.session_id)

asyncio.run(main())
```

</CodeGroup>

## Membuat Slash Commands Kustom

Selain menggunakan slash commands bawaan, Anda dapat membuat perintah kustom Anda sendiri yang tersedia melalui SDK. Perintah kustom didefinisikan sebagai file markdown dalam direktori tertentu, mirip dengan cara subagents dikonfigurasi.

### Lokasi File

Slash commands kustom disimpan dalam direktori yang ditunjuk berdasarkan cakupan mereka:

- **Perintah proyek**: `.claude/commands/` - Hanya tersedia di proyek saat ini
- **Perintah pribadi**: `~/.claude/commands/` - Tersedia di semua proyek Anda

### Format File

Setiap perintah kustom adalah file markdown di mana:
- Nama file (tanpa ekstensi `.md`) menjadi nama perintah
- Konten file mendefinisikan apa yang dilakukan perintah
- Frontmatter YAML opsional menyediakan konfigurasi

#### Contoh Dasar

Buat `.claude/commands/refactor.md`:

```markdown
Refactor the selected code to improve readability and maintainability.
Focus on clean code principles and best practices.
```

Ini membuat perintah `/refactor` yang dapat Anda gunakan melalui SDK.

#### Dengan Frontmatter

Buat `.claude/commands/security-check.md`:

```markdown
---
allowed-tools: Read, Grep, Glob
description: Run security vulnerability scan
model: claude-opus-4-6
---

Analyze the codebase for security vulnerabilities including:
- SQL injection risks
- XSS vulnerabilities
- Exposed credentials
- Insecure configurations
```

### Menggunakan Perintah Kustom dalam SDK

Setelah didefinisikan dalam sistem file, perintah kustom secara otomatis tersedia melalui SDK:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Use a custom command
for await (const message of query({
  prompt: "/refactor src/auth/login.ts",
  options: { maxTurns: 3 }
})) {
  if (message.type === "assistant") {
    console.log("Refactoring suggestions:", message.message);
  }
}

// Custom commands appear in the slash_commands list
for await (const message of query({
  prompt: "Hello",
  options: { maxTurns: 1 }
})) {
  if (message.type === "system" && message.subtype === "init") {
    // Will include both built-in and custom commands
    console.log("Available commands:", message.slash_commands);
    // Example: ["/compact", "/clear", "/help", "/refactor", "/security-check"]
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query

async def main():
    # Use a custom command
    async for message in query(
        prompt="/refactor src/auth/login.py",
        options={"max_turns": 3}
    ):
        if message.type == "assistant":
            print("Refactoring suggestions:", message.message)
    
    # Custom commands appear in the slash_commands list
    async for message in query(
        prompt="Hello",
        options={"max_turns": 1}
    ):
        if message.type == "system" and message.subtype == "init":
            # Will include both built-in and custom commands
            print("Available commands:", message.slash_commands)
            # Example: ["/compact", "/clear", "/help", "/refactor", "/security-check"]

asyncio.run(main())
```

</CodeGroup>

### Fitur Lanjutan

#### Argumen dan Placeholder

Perintah kustom mendukung argumen dinamis menggunakan placeholder:

Buat `.claude/commands/fix-issue.md`:

```markdown
---
argument-hint: [issue-number] [priority]
description: Fix a GitHub issue
---

Fix issue #$1 with priority $2.
Check the issue description and implement the necessary changes.
```

Gunakan dalam SDK:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Pass arguments to custom command
for await (const message of query({
  prompt: "/fix-issue 123 high",
  options: { maxTurns: 5 }
})) {
  // Command will process with $1="123" and $2="high"
  if (message.type === "result") {
    console.log("Issue fixed:", message.result);
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query

async def main():
    # Pass arguments to custom command
    async for message in query(
        prompt="/fix-issue 123 high",
        options={"max_turns": 5}
    ):
        # Command will process with $1="123" and $2="high"
        if message.type == "result":
            print("Issue fixed:", message.result)

asyncio.run(main())
```

</CodeGroup>

#### Eksekusi Perintah Bash

Perintah kustom dapat mengeksekusi perintah bash dan menyertakan output mereka:

Buat `.claude/commands/git-commit.md`:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current status: !`git status`
- Current diff: !`git diff HEAD`

## Task

Create a git commit with appropriate message based on the changes.
```

#### Referensi File

Sertakan konten file menggunakan awalan `@`:

Buat `.claude/commands/review-config.md`:

```markdown
---
description: Review configuration files
---

Review the following configuration files for issues:
- Package config: @package.json
- TypeScript config: @tsconfig.json
- Environment config: @.env

Check for security issues, outdated dependencies, and misconfigurations.
```

### Organisasi dengan Namespacing

Organisir perintah dalam subdirektori untuk struktur yang lebih baik:

```bash
.claude/commands/
├── frontend/
│   ├── component.md      # Creates /component (project:frontend)
│   └── style-check.md     # Creates /style-check (project:frontend)
├── backend/
│   ├── api-test.md        # Creates /api-test (project:backend)
│   └── db-migrate.md      # Creates /db-migrate (project:backend)
└── review.md              # Creates /review (project)
```

Subdirektori muncul dalam deskripsi perintah tetapi tidak mempengaruhi nama perintah itu sendiri.

### Contoh Praktis

#### Perintah Code Review

Buat `.claude/commands/code-review.md`:

```markdown
---
allowed-tools: Read, Grep, Glob, Bash(git diff:*)
description: Comprehensive code review
---

## Changed Files
!`git diff --name-only HEAD~1`

## Detailed Changes
!`git diff HEAD~1`

## Review Checklist

Review the above changes for:
1. Code quality and readability
2. Security vulnerabilities
3. Performance implications
4. Test coverage
5. Documentation completeness

Provide specific, actionable feedback organized by priority.
```

#### Perintah Test Runner

Buat `.claude/commands/test.md`:

```markdown
---
allowed-tools: Bash, Read, Edit
argument-hint: [test-pattern]
description: Run tests with optional pattern
---

Run tests matching pattern: $ARGUMENTS

1. Detect the test framework (Jest, pytest, etc.)
2. Run tests with the provided pattern
3. If tests fail, analyze and fix them
4. Re-run to verify fixes
```

Gunakan perintah-perintah ini melalui SDK:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Run code review
for await (const message of query({
  prompt: "/code-review",
  options: { maxTurns: 3 }
})) {
  // Process review feedback
}

// Run specific tests
for await (const message of query({
  prompt: "/test auth",
  options: { maxTurns: 5 }
})) {
  // Handle test results
}
```

```python Python
import asyncio
from claude_agent_sdk import query

async def main():
    # Run code review
    async for message in query(
        prompt="/code-review",
        options={"max_turns": 3}
    ):
        # Process review feedback
        pass
    
    # Run specific tests
    async for message in query(
        prompt="/test auth",
        options={"max_turns": 5}
    ):
        # Handle test results
        pass

asyncio.run(main())
```

</CodeGroup>

## Lihat Juga

- [Slash Commands](https://code.claude.com/docs/id/slash-commands) - Dokumentasi slash command lengkap
- [Subagents dalam SDK](/docs/id/agent-sdk/subagents) - Konfigurasi berbasis sistem file serupa untuk subagents
- [Referensi SDK TypeScript](/docs/id/agent-sdk/typescript) - Dokumentasi API lengkap
- [Gambaran umum SDK](/docs/id/agent-sdk/overview) - Konsep SDK umum
- [Referensi CLI](https://code.claude.com/docs/id/cli-reference) - Antarmuka baris perintah