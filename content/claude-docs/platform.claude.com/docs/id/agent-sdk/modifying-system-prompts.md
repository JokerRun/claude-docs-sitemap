---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/modifying-system-prompts
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: efdabd6f7fe40e11e334532d3927cbd326e8d7742382552036dd766f5d5df405
---

# Memodifikasi system prompts

Pelajari cara menyesuaikan perilaku Claude dengan memodifikasi system prompts menggunakan tiga pendekatan - output styles, systemPrompt dengan append, dan custom system prompts.

---

System prompts mendefinisikan perilaku Claude, kemampuan, dan gaya respons. Claude Agent SDK menyediakan tiga cara untuk menyesuaikan system prompts: menggunakan output styles (konfigurasi berbasis file yang persisten), menambahkan ke prompt Claude Code, atau menggunakan prompt kustom sepenuhnya.

## Memahami system prompts

Sebuah system prompt adalah set instruksi awal yang membentuk bagaimana Claude berperilaku sepanjang percakapan.

<Note>
**Perilaku default:** Agent SDK menggunakan **minimal system prompt** secara default. Ini hanya berisi instruksi tool yang penting tetapi menghilangkan pedoman coding Claude Code, gaya respons, dan konteks proyek. Untuk menyertakan system prompt Claude Code lengkap, tentukan `systemPrompt: { preset: "claude_code" }` di TypeScript atau `system_prompt={"type": "preset", "preset": "claude_code"}` di Python.
</Note>

System prompt Claude Code mencakup:

- Instruksi penggunaan tool dan tool yang tersedia
- Pedoman gaya kode dan pemformatan
- Pengaturan nada respons dan verbositas
- Instruksi keamanan dan keselamatan
- Konteks tentang direktori kerja saat ini dan lingkungan

## Metode modifikasi

### Method 1: File CLAUDE.md (instruksi tingkat proyek)

File CLAUDE.md menyediakan konteks dan instruksi spesifik proyek yang secara otomatis dibaca oleh Agent SDK ketika berjalan di direktori. Mereka berfungsi sebagai "memori" persisten untuk proyek Anda.

#### Bagaimana CLAUDE.md bekerja dengan SDK

**Lokasi dan penemuan:**

- **Tingkat proyek:** `CLAUDE.md` atau `.claude/CLAUDE.md` di direktori kerja Anda
- **Tingkat pengguna:** `~/.claude/CLAUDE.md` untuk instruksi global di semua proyek

**PENTING:** SDK hanya membaca file CLAUDE.md ketika Anda secara eksplisit mengonfigurasi `settingSources` (TypeScript) atau `setting_sources` (Python):

- Sertakan `'project'` untuk memuat CLAUDE.md tingkat proyek
- Sertakan `'user'` untuk memuat CLAUDE.md tingkat pengguna (`~/.claude/CLAUDE.md`)

Preset system prompt `claude_code` TIDAK secara otomatis memuat CLAUDE.md - Anda juga harus menentukan sumber pengaturan.

**Format konten:**
File CLAUDE.md menggunakan markdown biasa dan dapat berisi:

- Pedoman coding dan standar
- Konteks spesifik proyek
- Perintah atau alur kerja umum
- Konvensi API
- Persyaratan pengujian

#### Contoh CLAUDE.md

```markdown
# Project Guidelines

## Code Style

- Use TypeScript strict mode
- Prefer functional components in React
- Always include JSDoc comments for public APIs

## Testing

- Run `npm test` before committing
- Maintain >80% code coverage
- Use jest for unit tests, playwright for E2E

## Commands

- Build: `npm run build`
- Dev server: `npm run dev`
- Type check: `npm run typecheck`
```

#### Menggunakan CLAUDE.md dengan SDK

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// IMPORTANT: You must specify settingSources to load CLAUDE.md
// The claude_code preset alone does NOT load CLAUDE.md files
const messages = [];

for await (const message of query({
  prompt: "Add a new React component for user profiles",
  options: {
    systemPrompt: {
      type: "preset",
      preset: "claude_code", // Use Claude Code's system prompt
    },
    settingSources: ["project"], // Required to load CLAUDE.md from project
  },
})) {
  messages.push(message);
}

// Now Claude has access to your project guidelines from CLAUDE.md
```

```python Python
from claude_agent_sdk import query, ClaudeAgentOptions

# IMPORTANT: You must specify setting_sources to load CLAUDE.md
# The claude_code preset alone does NOT load CLAUDE.md files
messages = []

async for message in query(
    prompt="Add a new React component for user profiles",
    options=ClaudeAgentOptions(
        system_prompt={
            "type": "preset",
            "preset": "claude_code"  # Use Claude Code's system prompt
        },
        setting_sources=["project"]  # Required to load CLAUDE.md from project
    )
):
    messages.append(message)

# Now Claude has access to your project guidelines from CLAUDE.md
```

</CodeGroup>

#### Kapan menggunakan CLAUDE.md

**Terbaik untuk:**

- **Konteks bersama tim** - Pedoman yang harus diikuti semua orang
- **Konvensi proyek** - Standar coding, struktur file, pola penamaan
- **Perintah umum** - Perintah build, test, deploy spesifik untuk proyek Anda
- **Memori jangka panjang** - Konteks yang harus persisten di semua sesi
- **Instruksi terkontrol versi** - Commit ke git sehingga tim tetap sinkron

**Karakteristik kunci:**

- ✅ Persisten di semua sesi dalam proyek
- ✅ Dibagikan dengan tim melalui git
- ✅ Penemuan otomatis (tidak perlu perubahan kode)
- ⚠️ Memerlukan pemuatan pengaturan melalui `settingSources`

### Method 2: Output styles (konfigurasi persisten)

Output styles adalah konfigurasi yang disimpan yang memodifikasi system prompt Claude. Mereka disimpan sebagai file markdown dan dapat digunakan kembali di seluruh sesi dan proyek.

#### Membuat output style

<CodeGroup>

```typescript TypeScript
import { writeFile, mkdir } from "fs/promises";
import { join } from "path";
import { homedir } from "os";

async function createOutputStyle(
  name: string,
  description: string,
  prompt: string
) {
  // User-level: ~/.claude/output-styles
  // Project-level: .claude/output-styles
  const outputStylesDir = join(homedir(), ".claude", "output-styles");

  await mkdir(outputStylesDir, { recursive: true });

  const content = `---
name: ${name}
description: ${description}
---

${prompt}`;

  const filePath = join(
    outputStylesDir,
    `${name.toLowerCase().replace(/\s+/g, "-")}.md`
  );
  await writeFile(filePath, content, "utf-8");
}

// Example: Create a code review specialist
await createOutputStyle(
  "Code Reviewer",
  "Thorough code review assistant",
  `You are an expert code reviewer.

For every code submission:
1. Check for bugs and security issues
2. Evaluate performance
3. Suggest improvements
4. Rate code quality (1-10)`
);
```

```python Python
from pathlib import Path

async def create_output_style(name: str, description: str, prompt: str):
    # User-level: ~/.claude/output-styles
    # Project-level: .claude/output-styles
    output_styles_dir = Path.home() / '.claude' / 'output-styles'

    output_styles_dir.mkdir(parents=True, exist_ok=True)

    content = f"""---
name: {name}
description: {description}
---

{prompt}"""

    file_name = name.lower().replace(' ', '-') + '.md'
    file_path = output_styles_dir / file_name
    file_path.write_text(content, encoding='utf-8')

# Example: Create a code review specialist
await create_output_style(
    'Code Reviewer',
    'Thorough code review assistant',
    """You are an expert code reviewer.

For every code submission:
1. Check for bugs and security issues
2. Evaluate performance
3. Suggest improvements
4. Rate code quality (1-10)"""
)
```

</CodeGroup>

#### Menggunakan output styles

Setelah dibuat, aktifkan output styles melalui:

- **CLI**: `/output-style [style-name]`
- **Settings**: `.claude/settings.local.json`
- **Buat baru**: `/output-style:new [description]`

**Catatan untuk pengguna SDK:** Output styles dimuat ketika Anda menyertakan `settingSources: ['user']` atau `settingSources: ['project']` (TypeScript) / `setting_sources=["user"]` atau `setting_sources=["project"]` (Python) dalam opsi Anda.

### Method 3: Menggunakan `systemPrompt` dengan append

Anda dapat menggunakan preset Claude Code dengan properti `append` untuk menambahkan instruksi kustom Anda sambil mempertahankan semua fungsionalitas bawaan.

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

const messages = [];

for await (const message of query({
  prompt: "Help me write a Python function to calculate fibonacci numbers",
  options: {
    systemPrompt: {
      type: "preset",
      preset: "claude_code",
      append:
        "Always include detailed docstrings and type hints in Python code.",
    },
  },
})) {
  messages.push(message);
  if (message.type === "assistant") {
    console.log(message.message.content);
  }
}
```

```python Python
from claude_agent_sdk import query, ClaudeAgentOptions

messages = []

async for message in query(
    prompt="Help me write a Python function to calculate fibonacci numbers",
    options=ClaudeAgentOptions(
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": "Always include detailed docstrings and type hints in Python code."
        }
    )
):
    messages.append(message)
    if message.type == 'assistant':
        print(message.message.content)
```

</CodeGroup>

### Method 4: Custom system prompts

Anda dapat menyediakan string kustom sebagai `systemPrompt` untuk mengganti default sepenuhnya dengan instruksi Anda sendiri.

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

const customPrompt = `You are a Python coding specialist.
Follow these guidelines:
- Write clean, well-documented code
- Use type hints for all functions
- Include comprehensive docstrings
- Prefer functional programming patterns when appropriate
- Always explain your code choices`;

const messages = [];

for await (const message of query({
  prompt: "Create a data processing pipeline",
  options: {
    systemPrompt: customPrompt,
  },
})) {
  messages.push(message);
  if (message.type === "assistant") {
    console.log(message.message.content);
  }
}
```

```python Python
from claude_agent_sdk import query, ClaudeAgentOptions

custom_prompt = """You are a Python coding specialist.
Follow these guidelines:
- Write clean, well-documented code
- Use type hints for all functions
- Include comprehensive docstrings
- Prefer functional programming patterns when appropriate
- Always explain your code choices"""

messages = []

async for message in query(
    prompt="Create a data processing pipeline",
    options=ClaudeAgentOptions(
        system_prompt=custom_prompt
    )
):
    messages.append(message)
    if message.type == 'assistant':
        print(message.message.content)
```

</CodeGroup>

## Perbandingan keempat pendekatan

| Fitur                   | CLAUDE.md           | Output Styles      | `systemPrompt` dengan append | Custom `systemPrompt`     |
| ----------------------- | ------------------- | ------------------ | -------------------------- | ------------------------- |
| **Persistensi**         | File per-proyek | Disimpan sebagai file  | Hanya sesi            | Hanya sesi           |
| **Dapat digunakan kembali**         | Per-proyek      | Di seluruh proyek | Duplikasi kode        | Duplikasi kode       |
| **Manajemen**          | Di sistem file    | CLI + file     | Dalam kode                 | Dalam kode                |
| **Tool default**       | Dipertahankan        | Dipertahankan       | Dipertahankan               | Hilang (kecuali disertakan) |
| **Keamanan bawaan**     | Dipertahankan       | Dipertahankan      | Dipertahankan              | Harus ditambahkan          |
| **Konteks lingkungan** | Otomatis        | Otomatis       | Otomatis               | Harus disediakan       |
| **Tingkat kustomisasi** | Hanya penambahan   | Ganti default | Hanya penambahan          | Kontrol penuh       |
| **Kontrol versi**     | Dengan proyek     | Ya             | Dengan kode               | Dengan kode              |
| **Cakupan**               | Spesifik proyek | Pengguna atau proyek | Sesi kode            | Sesi kode           |

**Catatan:** "Dengan append" berarti menggunakan `systemPrompt: { type: "preset", preset: "claude_code", append: "..." }` di TypeScript atau `system_prompt={"type": "preset", "preset": "claude_code", "append": "..."}` di Python.

## Use cases dan best practices

### Kapan menggunakan CLAUDE.md

**Terbaik untuk:**

- Standar coding dan konvensi spesifik proyek
- Mendokumentasikan struktur dan arsitektur proyek
- Mencantumkan perintah umum (build, test, deploy)
- Konteks bersama tim yang harus dikontrol versi
- Instruksi yang berlaku untuk semua penggunaan SDK dalam proyek

**Contoh:**

- "Semua endpoint API harus menggunakan pola async/await"
- "Jalankan `npm run lint:fix` sebelum commit"
- "Migrasi database ada di direktori `migrations/`"

**Penting:** Untuk memuat file CLAUDE.md, Anda harus secara eksplisit menetapkan `settingSources: ['project']` (TypeScript) atau `setting_sources=["project"]` (Python). Preset system prompt `claude_code` TIDAK secara otomatis memuat CLAUDE.md tanpa pengaturan ini.

### Kapan menggunakan output styles

**Terbaik untuk:**

- Perubahan perilaku persisten di seluruh sesi
- Konfigurasi bersama tim
- Asisten khusus (code reviewer, data scientist, DevOps)
- Modifikasi prompt kompleks yang memerlukan versioning

**Contoh:**

- Membuat asisten optimasi SQL khusus
- Membangun code reviewer yang berfokus pada keamanan
- Mengembangkan asisten pengajaran dengan pedagogi spesifik

### Kapan menggunakan `systemPrompt` dengan append

**Terbaik untuk:**

- Menambahkan standar coding atau preferensi spesifik
- Menyesuaikan pemformatan output
- Menambahkan pengetahuan domain spesifik
- Memodifikasi verbositas respons
- Meningkatkan perilaku default Claude Code tanpa kehilangan instruksi tool

### Kapan menggunakan custom `systemPrompt`

**Terbaik untuk:**

- Kontrol penuh atas perilaku Claude
- Tugas sesi tunggal khusus
- Menguji strategi prompt baru
- Situasi di mana tool default tidak diperlukan
- Membangun agen khusus dengan perilaku unik

## Menggabungkan pendekatan

Anda dapat menggabungkan metode ini untuk fleksibilitas maksimal:

### Contoh: Output style dengan penambahan spesifik sesi

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Assuming "Code Reviewer" output style is active (via /output-style)
// Add session-specific focus areas
const messages = [];

for await (const message of query({
  prompt: "Review this authentication module",
  options: {
    systemPrompt: {
      type: "preset",
      preset: "claude_code",
      append: `
        For this review, prioritize:
        - OAuth 2.0 compliance
        - Token storage security
        - Session management
      `,
    },
  },
})) {
  messages.push(message);
}
```

```python Python
from claude_agent_sdk import query, ClaudeAgentOptions

# Assuming "Code Reviewer" output style is active (via /output-style)
# Add session-specific focus areas
messages = []

async for message in query(
    prompt="Review this authentication module",
    options=ClaudeAgentOptions(
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": """
            For this review, prioritize:
            - OAuth 2.0 compliance
            - Token storage security
            - Session management
            """
        }
    )
):
    messages.append(message)
```

</CodeGroup>

## Lihat juga

- [Output styles](https://code.claude.com/docs/id/output-styles) - Dokumentasi output styles lengkap
- [Panduan TypeScript SDK](/docs/id/agent-sdk/typescript) - Panduan penggunaan SDK lengkap
- [Panduan konfigurasi](https://code.claude.com/docs/id/settings) - Opsi konfigurasi umum