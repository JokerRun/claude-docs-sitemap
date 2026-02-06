---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/subagents
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 00d5d6d394d839088d995a17abc3f9953840e22ec8c657d74c9ea254af56cb09
---

# Subagents dalam SDK

Tentukan dan panggil subagents untuk mengisolasi konteks, menjalankan tugas secara paralel, dan menerapkan instruksi khusus dalam aplikasi Claude Agent SDK Anda.

---

Subagents adalah instans agen terpisah yang dapat dihasilkan oleh agen utama Anda untuk menangani subtask yang terfokus.
Gunakan subagents untuk mengisolasi konteks bagi subtask yang terfokus, menjalankan beberapa analisis secara paralel, dan menerapkan instruksi khusus tanpa membuat prompt agen utama menjadi terlalu besar.

Panduan ini menjelaskan cara mendefinisikan dan menggunakan subagents dalam SDK menggunakan parameter `agents`.

## Ikhtisar

Anda dapat membuat subagents dengan tiga cara:

- **Secara programatis**: gunakan parameter `agents` dalam opsi `query()` Anda ([TypeScript](/docs/id/agent-sdk/typescript#agentdefinition), [Python](/docs/id/agent-sdk/python#agentdefinition))
- **Berbasis sistem file**: tentukan agen sebagai file markdown dalam direktori `.claude/agents/` (lihat [mendefinisikan subagents sebagai file](https://code.claude.com/docs/en/sub-agents))
- **Tujuan umum bawaan**: Claude dapat memanggil subagent `general-purpose` bawaan kapan saja melalui alat Task tanpa Anda mendefinisikan apa pun

Panduan ini berfokus pada pendekatan programatis, yang direkomendasikan untuk aplikasi SDK.

Ketika Anda mendefinisikan subagents, Claude memutuskan apakah akan memanggilnya berdasarkan bidang `description` setiap subagent. Tulis deskripsi yang jelas yang menjelaskan kapan subagent harus digunakan, dan Claude akan secara otomatis mendelegasikan tugas yang sesuai. Anda juga dapat secara eksplisit meminta subagent berdasarkan nama dalam prompt Anda (misalnya, "Gunakan agen code-reviewer untuk...").

## Manfaat menggunakan subagents

### Manajemen konteks
Subagents mempertahankan konteks terpisah dari agen utama, mencegah kelebihan informasi dan menjaga interaksi tetap terfokus. Isolasi ini memastikan bahwa tugas khusus tidak mencemari konteks percakapan utama dengan detail yang tidak relevan.

**Contoh**: subagent `research-assistant` dapat menjelajahi puluhan file dan halaman dokumentasi tanpa mengacaukan percakapan utama dengan semua hasil pencarian perantara, hanya mengembalikan temuan yang relevan.

### Paralelisasi
Beberapa subagents dapat berjalan secara bersamaan, secara dramatis mempercepat alur kerja yang kompleks.

**Contoh**: selama tinjauan kode, Anda dapat menjalankan subagents `style-checker`, `security-scanner`, dan `test-coverage` secara bersamaan, mengurangi waktu tinjauan dari menit menjadi detik.

### Instruksi dan pengetahuan khusus
Setiap subagent dapat memiliki prompt sistem yang disesuaikan dengan keahlian, praktik terbaik, dan batasan tertentu.

**Contoh**: subagent `database-migration` dapat memiliki pengetahuan terperinci tentang praktik terbaik SQL, strategi rollback, dan pemeriksaan integritas data yang akan menjadi kebisingan yang tidak perlu dalam instruksi agen utama.

### Pembatasan alat
Subagents dapat dibatasi pada alat tertentu, mengurangi risiko tindakan yang tidak diinginkan.

**Contoh**: subagent `doc-reviewer` mungkin hanya memiliki akses ke alat Read dan Grep, memastikan dapat menganalisis tetapi tidak pernah secara tidak sengaja memodifikasi file dokumentasi Anda.

## Membuat subagents

### Definisi programatis (direkomendasikan)

Tentukan subagents langsung dalam kode Anda menggunakan parameter `agents`. Contoh ini membuat dua subagents: peninjau kode dengan akses baca saja dan pelari tes yang dapat menjalankan perintah. Alat `Task` harus disertakan dalam `allowedTools` karena Claude memanggil subagents melalui alat Task.

<CodeGroup>
```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="Review the authentication module for security issues",
        options=ClaudeAgentOptions(
            # Task tool is required for subagent invocation
            allowed_tools=["Read", "Grep", "Glob", "Task"],
            agents={
                "code-reviewer": AgentDefinition(
                    # description tells Claude when to use this subagent
                    description="Expert code review specialist. Use for quality, security, and maintainability reviews.",
                    # prompt defines the subagent's behavior and expertise
                    prompt="""You are a code review specialist with expertise in security, performance, and best practices.

When reviewing code:
- Identify security vulnerabilities
- Check for performance issues
- Verify adherence to coding standards
- Suggest specific improvements

Be thorough but concise in your feedback.""",
                    # tools restricts what the subagent can do (read-only here)
                    tools=["Read", "Grep", "Glob"],
                    # model overrides the default model for this subagent
                    model="sonnet"
                ),
                "test-runner": AgentDefinition(
                    description="Runs and analyzes test suites. Use for test execution and coverage analysis.",
                    prompt="""You are a test execution specialist. Run tests and provide clear analysis of results.

Focus on:
- Running test commands
- Analyzing test output
- Identifying failing tests
- Suggesting fixes for failures""",
                    # Bash access lets this subagent run test commands
                    tools=["Bash", "Read", "Grep"]
                )
            }
        )
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

```typescript TypeScript
import { query } from '@anthropic-ai/claude-agent-sdk';

for await (const message of query({
  prompt: "Review the authentication module for security issues",
  options: {
    // Task tool is required for subagent invocation
    allowedTools: ['Read', 'Grep', 'Glob', 'Task'],
    agents: {
      'code-reviewer': {
        // description tells Claude when to use this subagent
        description: 'Expert code review specialist. Use for quality, security, and maintainability reviews.',
        // prompt defines the subagent's behavior and expertise
        prompt: `You are a code review specialist with expertise in security, performance, and best practices.

When reviewing code:
- Identify security vulnerabilities
- Check for performance issues
- Verify adherence to coding standards
- Suggest specific improvements

Be thorough but concise in your feedback.`,
        // tools restricts what the subagent can do (read-only here)
        tools: ['Read', 'Grep', 'Glob'],
        // model overrides the default model for this subagent
        model: 'sonnet'
      },
      'test-runner': {
        description: 'Runs and analyzes test suites. Use for test execution and coverage analysis.',
        prompt: `You are a test execution specialist. Run tests and provide clear analysis of results.

Focus on:
- Running test commands
- Analyzing test output
- Identifying failing tests
- Suggesting fixes for failures`,
        // Bash access lets this subagent run test commands
        tools: ['Bash', 'Read', 'Grep'],
      }
    }
  }
})) {
  if ('result' in message) console.log(message.result);
}
```
</CodeGroup>

### Konfigurasi AgentDefinition

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `description` | `string` | Yes | Deskripsi bahasa alami tentang kapan menggunakan agen ini |
| `prompt` | `string` | Yes | Prompt sistem agen yang mendefinisikan peran dan perilakunya |
| `tools` | `string[]` | No | Array nama alat yang diizinkan. Jika dihilangkan, mewarisi semua alat |
| `model` | `'sonnet' \| 'opus' \| 'haiku' \| 'inherit'` | No | Penggantian model untuk agen ini. Default ke model utama jika dihilangkan |

<Note>
Subagents tidak dapat menjalankan subagents mereka sendiri. Jangan sertakan `Task` dalam array `tools` subagent.
</Note>

### Definisi berbasis sistem file (alternatif)

Anda juga dapat mendefinisikan subagents sebagai file markdown dalam direktori `.claude/agents/`. Lihat [dokumentasi subagents Claude Code](https://code.claude.com/docs/en/sub-agents) untuk detail tentang pendekatan ini. Agen yang didefinisikan secara programatis memiliki prioritas lebih tinggi daripada agen berbasis sistem file dengan nama yang sama.

<Note>
Bahkan tanpa mendefinisikan subagents khusus, Claude dapat menjalankan subagent `general-purpose` bawaan ketika `Task` ada dalam `allowedTools` Anda. Ini berguna untuk mendelegasikan tugas penelitian atau eksplorasi tanpa membuat agen khusus.
</Note>

## Memanggil subagents

### Pemanggilan otomatis

Claude secara otomatis memutuskan kapan akan memanggil subagents berdasarkan tugas dan bidang `description` setiap subagent. Misalnya, jika Anda mendefinisikan subagent `performance-optimizer` dengan deskripsi "Performance optimization specialist for query tuning", Claude akan memanggilnya ketika prompt Anda menyebutkan optimasi kueri.

Tulis deskripsi yang jelas dan spesifik sehingga Claude dapat mencocokkan tugas dengan subagent yang tepat.

### Pemanggilan eksplisit

Untuk menjamin Claude menggunakan subagent tertentu, sebutkan berdasarkan nama dalam prompt Anda:

```
"Use the code-reviewer agent to check the authentication module"
```

Ini melewati pencocokan otomatis dan secara langsung memanggil subagent bernama.

### Konfigurasi agen dinamis

Anda dapat membuat definisi agen secara dinamis berdasarkan kondisi runtime. Contoh ini membuat peninjau keamanan dengan tingkat ketat yang berbeda, menggunakan model yang lebih kuat untuk tinjauan ketat.

<CodeGroup>
```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

# Factory function that returns an AgentDefinition
# This pattern lets you customize agents based on runtime conditions
def create_security_agent(security_level: str) -> AgentDefinition:
    is_strict = security_level == "strict"
    return AgentDefinition(
        description="Security code reviewer",
        # Customize the prompt based on strictness level
        prompt=f"You are a {'strict' if is_strict else 'balanced'} security reviewer...",
        tools=["Read", "Grep", "Glob"],
        # Key insight: use a more capable model for high-stakes reviews
        model="opus" if is_strict else "sonnet"
    )

async def main():
    # The agent is created at query time, so each request can use different settings
    async for message in query(
        prompt="Review this PR for security issues",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Grep", "Glob", "Task"],
            agents={
                # Call the factory with your desired configuration
                "security-reviewer": create_security_agent("strict")
            }
        )
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

```typescript TypeScript
import { query, type AgentDefinition } from '@anthropic-ai/claude-agent-sdk';

// Factory function that returns an AgentDefinition
// This pattern lets you customize agents based on runtime conditions
function createSecurityAgent(securityLevel: 'basic' | 'strict'): AgentDefinition {
  const isStrict = securityLevel === 'strict';
  return {
    description: 'Security code reviewer',
    // Customize the prompt based on strictness level
    prompt: `You are a ${isStrict ? 'strict' : 'balanced'} security reviewer...`,
    tools: ['Read', 'Grep', 'Glob'],
    // Key insight: use a more capable model for high-stakes reviews
    model: isStrict ? 'opus' : 'sonnet'
  };
}

// The agent is created at query time, so each request can use different settings
for await (const message of query({
  prompt: "Review this PR for security issues",
  options: {
    allowedTools: ['Read', 'Grep', 'Glob', 'Task'],
    agents: {
      // Call the factory with your desired configuration
      'security-reviewer': createSecurityAgent('strict')
    }
  }
})) {
  if ('result' in message) console.log(message.result);
}
```
</CodeGroup>

## Mendeteksi pemanggilan subagent

Subagents dipanggil melalui alat Task. Untuk mendeteksi kapan subagent dipanggil, periksa blok `tool_use` dengan `name: "Task"`. Pesan dari dalam konteks subagent menyertakan bidang `parent_tool_use_id`.

Contoh ini mengulangi pesan yang dialirkan, mencatat ketika subagent dipanggil dan ketika pesan berikutnya berasal dari dalam konteks eksekusi subagent tersebut.

<Note>
Struktur pesan berbeda antara SDK. Di Python, blok konten diakses langsung melalui `message.content`. Di TypeScript, `SDKAssistantMessage` membungkus pesan Claude API, jadi konten diakses melalui `message.message.content`.
</Note>

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
                    description="Expert code reviewer.",
                    prompt="Analyze code quality and suggest improvements.",
                    tools=["Read", "Glob", "Grep"]
                )
            }
        )
    ):
        # Check for subagent invocation in message content
        if hasattr(message, 'content') and message.content:
            for block in message.content:
                if getattr(block, 'type', None) == 'tool_use' and block.name == 'Task':
                    print(f"Subagent invoked: {block.input.get('subagent_type')}")

        # Check if this message is from within a subagent's context
        if hasattr(message, 'parent_tool_use_id') and message.parent_tool_use_id:
            print("  (running inside subagent)")

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
        description: "Expert code reviewer.",
        prompt: "Analyze code quality and suggest improvements.",
        tools: ["Read", "Glob", "Grep"]
      }
    }
  }
})) {
  const msg = message as any;

  // Check for subagent invocation in message content
  for (const block of msg.message?.content ?? []) {
    if (block.type === "tool_use" && block.name === "Task") {
      console.log(`Subagent invoked: ${block.input.subagent_type}`);
    }
  }

  // Check if this message is from within a subagent's context
  if (msg.parent_tool_use_id) {
    console.log("  (running inside subagent)");
  }

  if ("result" in message) {
    console.log(message.result);
  }
}
```
</CodeGroup>

## Melanjutkan subagents

Subagents dapat dilanjutkan untuk melanjutkan dari tempat mereka berhenti. Subagents yang dilanjutkan mempertahankan riwayat percakapan lengkap mereka, termasuk semua panggilan alat sebelumnya, hasil, dan penalaran. Subagent melanjutkan tepat dari tempat berhenti daripada memulai dari awal.

Ketika subagent selesai, Claude menerima ID agennya dalam hasil alat Task. Untuk melanjutkan subagent secara programatis:

1. **Tangkap ID sesi**: Ekstrak `session_id` dari pesan selama kueri pertama
2. **Ekstrak ID agen**: Analisis `agentId` dari konten pesan
3. **Lanjutkan sesi**: Lewatkan `resume: sessionId` dalam opsi kueri kedua, dan sertakan ID agen dalam prompt Anda

<Note>
Anda harus melanjutkan sesi yang sama untuk mengakses transkrip subagent. Setiap panggilan `query()` memulai sesi baru secara default, jadi lewatkan `resume: sessionId` untuk melanjutkan dalam sesi yang sama.

Jika Anda menggunakan agen khusus (bukan agen bawaan), Anda juga perlu meneruskan definisi agen yang sama dalam parameter `agents` untuk kedua kueri.
</Note>

Contoh di bawah menunjukkan alur ini: kueri pertama menjalankan subagent dan menangkap ID sesi dan ID agen, kemudian kueri kedua melanjutkan sesi untuk mengajukan pertanyaan lanjutan yang memerlukan konteks dari analisis pertama.

<CodeGroup>
```typescript TypeScript
import { query, type SDKMessage } from '@anthropic-ai/claude-agent-sdk';

// Helper to extract agentId from message content
// Stringify to avoid traversing different block types (TextBlock, ToolResultBlock, etc.)
function extractAgentId(message: SDKMessage): string | undefined {
  if (!('message' in message)) return undefined;
  // Stringify the content so we can search it without traversing nested blocks
  const content = JSON.stringify(message.message.content);
  const match = content.match(/agentId:\s*([a-f0-9-]+)/);
  return match?.[1];
}

let agentId: string | undefined;
let sessionId: string | undefined;

// First invocation - use the Explore agent to find API endpoints
for await (const message of query({
  prompt: "Use the Explore agent to find all API endpoints in this codebase",
  options: { allowedTools: ['Read', 'Grep', 'Glob', 'Task'] }
})) {
  // Capture session_id from ResultMessage (needed to resume this session)
  if ('session_id' in message) sessionId = message.session_id;
  // Search message content for the agentId (appears in Task tool results)
  const extractedId = extractAgentId(message);
  if (extractedId) agentId = extractedId;
  // Print the final result
  if ('result' in message) console.log(message.result);
}

// Second invocation - resume and ask follow-up
if (agentId && sessionId) {
  for await (const message of query({
    prompt: `Resume agent ${agentId} and list the top 3 most complex endpoints`,
    options: { allowedTools: ['Read', 'Grep', 'Glob', 'Task'], resume: sessionId }
  })) {
    if ('result' in message) console.log(message.result);
  }
}
```

```python Python
import asyncio
import json
import re
from claude_agent_sdk import query, ClaudeAgentOptions

def extract_agent_id(text: str) -> str | None:
    """Extract agentId from Task tool result text."""
    match = re.search(r"agentId:\s*([a-f0-9-]+)", text)
    return match.group(1) if match else None

async def main():
    agent_id = None
    session_id = None

    # First invocation - use the Explore agent to find API endpoints
    async for message in query(
        prompt="Use the Explore agent to find all API endpoints in this codebase",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Grep", "Glob", "Task"])
    ):
        # Capture session_id from ResultMessage (needed to resume this session)
        if hasattr(message, "session_id"):
            session_id = message.session_id
        # Search message content for the agentId (appears in Task tool results)
        if hasattr(message, "content"):
            # Stringify the content so we can search it without traversing nested blocks
            content_str = json.dumps(message.content, default=str)
            extracted = extract_agent_id(content_str)
            if extracted:
                agent_id = extracted
        # Print the final result
        if hasattr(message, "result"):
            print(message.result)

    # Second invocation - resume and ask follow-up
    if agent_id and session_id:
        async for message in query(
            prompt=f"Resume agent {agent_id} and list the top 3 most complex endpoints",
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Grep", "Glob", "Task"],
                resume=session_id
            )
        ):
            if hasattr(message, "result"):
                print(message.result)

asyncio.run(main())
```
</CodeGroup>

Transkrip subagent bertahan secara independen dari percakapan utama:

- **Pemadatan percakapan utama**: Ketika percakapan utama dipadatkan, transkrip subagent tidak terpengaruh. Mereka disimpan dalam file terpisah.
- **Persistensi sesi**: Transkrip subagent bertahan dalam sesi mereka. Anda dapat melanjutkan subagent setelah memulai ulang Claude Code dengan melanjutkan sesi yang sama.
- **Pembersihan otomatis**: Transkrip dibersihkan berdasarkan pengaturan `cleanupPeriodDays` (default: 30 hari).

## Pembatasan alat

Subagents dapat memiliki akses alat terbatas melalui bidang `tools`:

- **Hilangkan bidang**: agen mewarisi semua alat yang tersedia (default)
- **Tentukan alat**: agen hanya dapat menggunakan alat yang terdaftar

Contoh ini membuat agen analisis baca saja yang dapat memeriksa kode tetapi tidak dapat memodifikasi file atau menjalankan perintah.

<CodeGroup>
```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="Analyze the architecture of this codebase",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Grep", "Glob", "Task"],
            agents={
                "code-analyzer": AgentDefinition(
                    description="Static code analysis and architecture review",
                    prompt="""You are a code architecture analyst. Analyze code structure,
identify patterns, and suggest improvements without making changes.""",
                    # Read-only tools: no Edit, Write, or Bash access
                    tools=["Read", "Grep", "Glob"]
                )
            }
        )
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

```typescript TypeScript
import { query } from '@anthropic-ai/claude-agent-sdk';

for await (const message of query({
  prompt: "Analyze the architecture of this codebase",
  options: {
    allowedTools: ['Read', 'Grep', 'Glob', 'Task'],
    agents: {
      'code-analyzer': {
        description: 'Static code analysis and architecture review',
        prompt: `You are a code architecture analyst. Analyze code structure,
identify patterns, and suggest improvements without making changes.`,
        // Read-only tools: no Edit, Write, or Bash access
        tools: ['Read', 'Grep', 'Glob']
      }
    }
  }
})) {
  if ('result' in message) console.log(message.result);
}
```
</CodeGroup>

### Kombinasi alat umum

| Use case | Tools | Description |
|:---------|:------|:------------|
| Analisis baca saja | `Read`, `Grep`, `Glob` | Dapat memeriksa kode tetapi tidak memodifikasi atau menjalankan |
| Eksekusi tes | `Bash`, `Read`, `Grep` | Dapat menjalankan perintah dan menganalisis output |
| Modifikasi kode | `Read`, `Edit`, `Write`, `Grep`, `Glob` | Akses baca/tulis penuh tanpa eksekusi perintah |
| Akses penuh | Semua alat | Mewarisi semua alat dari induk (hilangkan bidang `tools`) |

## Pemecahan masalah

### Claude tidak mendelegasikan ke subagents

Jika Claude menyelesaikan tugas secara langsung daripada mendelegasikan ke subagent Anda:

1. **Sertakan alat Task**: subagents dipanggil melalui alat Task, jadi harus ada dalam `allowedTools`
2. **Gunakan prompt eksplisit**: sebutkan subagent berdasarkan nama dalam prompt Anda (misalnya, "Gunakan agen code-reviewer untuk...")
3. **Tulis deskripsi yang jelas**: jelaskan dengan tepat kapan subagent harus digunakan sehingga Claude dapat mencocokkan tugas dengan tepat

### Agen berbasis sistem file tidak dimuat

Agen yang didefinisikan dalam `.claude/agents/` dimuat saat startup saja. Jika Anda membuat file agen baru saat Claude Code sedang berjalan, mulai ulang sesi untuk memuatnya.

### Windows: kegagalan prompt panjang

Di Windows, subagents dengan prompt yang sangat panjang mungkin gagal karena batasan panjang baris perintah (8191 karakter). Jaga prompt tetap ringkas atau gunakan agen berbasis sistem file untuk instruksi kompleks.

## Dokumentasi terkait

- [Subagents Claude Code](https://code.claude.com/docs/en/sub-agents): dokumentasi subagent komprehensif termasuk definisi berbasis sistem file
- [Ikhtisar SDK](/docs/id/agent-sdk/overview): memulai dengan Claude Agent SDK