---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/streaming-output
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 10ea10861dfb7d5176a983accf480f8dd40fa59db6103cb89dd6eebc5425abf0
---

# Streaming respons secara real-time

Dapatkan respons real-time dari Agent SDK saat teks dan pemanggilan alat mengalir

---

Secara default, Agent SDK menghasilkan objek `AssistantMessage` lengkap setelah Claude selesai menghasilkan setiap respons. Untuk menerima pembaruan inkremental saat teks dan pemanggilan alat dihasilkan, aktifkan streaming pesan parsial dengan menetapkan `include_partial_messages` (Python) atau `includePartialMessages` (TypeScript) ke `true` dalam opsi Anda.

<Tip>
Halaman ini mencakup streaming output (menerima token secara real-time). Untuk mode input (cara Anda mengirim pesan), lihat [Kirim pesan ke agen](/docs/id/agent-sdk/streaming-vs-single-mode). Anda juga dapat [streaming respons menggunakan Agent SDK melalui CLI](https://code.claude.com/docs/en/headless).
</Tip>

## Aktifkan streaming output

Untuk mengaktifkan streaming, atur `include_partial_messages` (Python) atau `includePartialMessages` (TypeScript) ke `true` dalam opsi Anda. Ini menyebabkan SDK menghasilkan pesan `StreamEvent` yang berisi peristiwa API mentah saat tiba, selain `AssistantMessage` dan `ResultMessage` yang biasa.

Kode Anda kemudian perlu:
1. Memeriksa tipe setiap pesan untuk membedakan `StreamEvent` dari tipe pesan lainnya
2. Untuk `StreamEvent`, ekstrak bidang `event` dan periksa `type`-nya
3. Cari peristiwa `content_block_delta` di mana `delta.type` adalah `text_delta`, yang berisi potongan teks sebenarnya

Contoh di bawah ini mengaktifkan streaming dan mencetak potongan teks saat tiba. Perhatikan pemeriksaan tipe bersarang: pertama untuk `StreamEvent`, kemudian untuk `content_block_delta`, kemudian untuk `text_delta`:

<CodeGroup>

```python Python
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import StreamEvent
import asyncio

async def stream_response():
    options = ClaudeAgentOptions(
        include_partial_messages=True,
        allowed_tools=["Bash", "Read"],
    )

    async for message in query(prompt="List the files in my project", options=options):
        if isinstance(message, StreamEvent):
            event = message.event
            if event.get("type") == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "text_delta":
                    print(delta.get("text", ""), end="", flush=True)

asyncio.run(stream_response())
```

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "List the files in my project",
  options: {
    includePartialMessages: true,
    allowedTools: ["Bash", "Read"],
  }
})) {
  if (message.type === "stream_event") {
    const event = message.event;
    if (event.type === "content_block_delta") {
      if (event.delta.type === "text_delta") {
        process.stdout.write(event.delta.text);
      }
    }
  }
}
```

</CodeGroup>

## Referensi StreamEvent

Ketika pesan parsial diaktifkan, Anda menerima peristiwa streaming API Claude mentah yang dibungkus dalam objek. Tipe memiliki nama berbeda di setiap SDK:

- **Python**: `StreamEvent` (impor dari `claude_agent_sdk.types`)
- **TypeScript**: `SDKPartialAssistantMessage` dengan `type: 'stream_event'`

Keduanya berisi peristiwa API Claude mentah, bukan teks terakumulasi. Anda perlu mengekstrak dan mengakumulasi delta teks sendiri. Berikut adalah struktur setiap tipe:

<CodeGroup>

```python Python
@dataclass
class StreamEvent:
    uuid: str                      # Unique identifier for this event
    session_id: str                # Session identifier
    event: dict[str, Any]          # The raw Claude API stream event
    parent_tool_use_id: str | None # Parent tool ID if from a subagent
```

```typescript TypeScript
type SDKPartialAssistantMessage = {
  type: 'stream_event';
  event: RawMessageStreamEvent;    // From Anthropic SDK
  parent_tool_use_id: string | null;
  uuid: UUID;
  session_id: string;
}
```

</CodeGroup>

Bidang `event` berisi peristiwa streaming mentah dari [Claude API](/docs/id/build-with-claude/streaming#event-types). Tipe peristiwa umum meliputi:

| Tipe Peristiwa | Deskripsi |
|:-----------|:------------|
| `message_start` | Awal pesan baru |
| `content_block_start` | Awal blok konten baru (teks atau penggunaan alat) |
| `content_block_delta` | Pembaruan inkremental ke konten |
| `content_block_stop` | Akhir blok konten |
| `message_delta` | Pembaruan tingkat pesan (alasan berhenti, penggunaan) |
| `message_stop` | Akhir pesan |

## Alur pesan

Dengan pesan parsial diaktifkan, Anda menerima pesan dalam urutan ini:

```
StreamEvent (message_start)
StreamEvent (content_block_start) - text block
StreamEvent (content_block_delta) - text chunks...
StreamEvent (content_block_stop)
StreamEvent (content_block_start) - tool_use block
StreamEvent (content_block_delta) - tool input chunks...
StreamEvent (content_block_stop)
StreamEvent (message_delta)
StreamEvent (message_stop)
AssistantMessage - complete message with all content
... tool executes ...
... more streaming events for next turn ...
ResultMessage - final result
```

Tanpa pesan parsial diaktifkan (`include_partial_messages` di Python, `includePartialMessages` di TypeScript), Anda menerima semua tipe pesan kecuali `StreamEvent`. Tipe umum meliputi `SystemMessage` (inisialisasi sesi), `AssistantMessage` (respons lengkap), `ResultMessage` (hasil akhir), dan `CompactBoundaryMessage` (menunjukkan kapan riwayat percakapan dipadatkan).

## Streaming respons teks

Untuk menampilkan teks saat dihasilkan, cari peristiwa `content_block_delta` di mana `delta.type` adalah `text_delta`. Ini berisi potongan teks inkremental. Contoh di bawah ini mencetak setiap potongan saat tiba:

<CodeGroup>

```python Python
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import StreamEvent
import asyncio

async def stream_text():
    options = ClaudeAgentOptions(include_partial_messages=True)

    async for message in query(prompt="Explain how databases work", options=options):
        if isinstance(message, StreamEvent):
            event = message.event
            if event.get("type") == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "text_delta":
                    # Print each text chunk as it arrives
                    print(delta.get("text", ""), end="", flush=True)

    print()  # Final newline

asyncio.run(stream_text())
```

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Explain how databases work",
  options: { includePartialMessages: true }
})) {
  if (message.type === "stream_event") {
    const event = message.event;
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
}

console.log(); // Final newline
```

</CodeGroup>

## Streaming pemanggilan alat

Pemanggilan alat juga streaming secara inkremental. Anda dapat melacak kapan alat dimulai, menerima input mereka saat dihasilkan, dan melihat kapan mereka selesai. Contoh di bawah ini melacak alat saat ini yang dipanggil dan mengakumulasi input JSON saat mengalir. Ini menggunakan tiga tipe peristiwa:

- `content_block_start`: alat dimulai
- `content_block_delta` dengan `input_json_delta`: potongan input tiba
- `content_block_stop`: pemanggilan alat selesai

<CodeGroup>

```python Python
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import StreamEvent
import asyncio

async def stream_tool_calls():
    options = ClaudeAgentOptions(
        include_partial_messages=True,
        allowed_tools=["Read", "Bash"],
    )

    # Track the current tool and accumulate its input JSON
    current_tool = None
    tool_input = ""

    async for message in query(prompt="Read the README.md file", options=options):
        if isinstance(message, StreamEvent):
            event = message.event
            event_type = event.get("type")

            if event_type == "content_block_start":
                # New tool call is starting
                content_block = event.get("content_block", {})
                if content_block.get("type") == "tool_use":
                    current_tool = content_block.get("name")
                    tool_input = ""
                    print(f"Starting tool: {current_tool}")

            elif event_type == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "input_json_delta":
                    # Accumulate JSON input as it streams in
                    chunk = delta.get("partial_json", "")
                    tool_input += chunk
                    print(f"  Input chunk: {chunk}")

            elif event_type == "content_block_stop":
                # Tool call complete - show final input
                if current_tool:
                    print(f"Tool {current_tool} called with: {tool_input}")
                    current_tool = None

asyncio.run(stream_tool_calls())
```

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Track the current tool and accumulate its input JSON
let currentTool: string | null = null;
let toolInput = "";

for await (const message of query({
  prompt: "Read the README.md file",
  options: {
    includePartialMessages: true,
    allowedTools: ["Read", "Bash"],
  }
})) {
  if (message.type === "stream_event") {
    const event = message.event;

    if (event.type === "content_block_start") {
      // New tool call is starting
      if (event.content_block.type === "tool_use") {
        currentTool = event.content_block.name;
        toolInput = "";
        console.log(`Starting tool: ${currentTool}`);
      }
    } else if (event.type === "content_block_delta") {
      if (event.delta.type === "input_json_delta") {
        // Accumulate JSON input as it streams in
        const chunk = event.delta.partial_json;
        toolInput += chunk;
        console.log(`  Input chunk: ${chunk}`);
      }
    } else if (event.type === "content_block_stop") {
      // Tool call complete - show final input
      if (currentTool) {
        console.log(`Tool ${currentTool} called with: ${toolInput}`);
        currentTool = null;
      }
    }
  }
}
```

</CodeGroup>

## Bangun UI streaming

Contoh ini menggabungkan streaming teks dan alat menjadi UI yang kohesif. Ini melacak apakah agen saat ini menjalankan alat (menggunakan bendera `in_tool`) untuk menampilkan indikator status seperti `[Using Read...]` saat alat berjalan. Teks mengalir secara normal ketika tidak dalam alat, dan penyelesaian alat memicu pesan "done". Pola ini berguna untuk antarmuka obrolan yang perlu menunjukkan kemajuan selama tugas agen multi-langkah.

<CodeGroup>

```python Python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
from claude_agent_sdk.types import StreamEvent
import asyncio
import sys

async def streaming_ui():
    options = ClaudeAgentOptions(
        include_partial_messages=True,
        allowed_tools=["Read", "Bash", "Grep"],
    )

    # Track whether we're currently in a tool call
    in_tool = False

    async for message in query(
        prompt="Find all TODO comments in the codebase",
        options=options
    ):
        if isinstance(message, StreamEvent):
            event = message.event
            event_type = event.get("type")

            if event_type == "content_block_start":
                content_block = event.get("content_block", {})
                if content_block.get("type") == "tool_use":
                    # Tool call is starting - show status indicator
                    tool_name = content_block.get("name")
                    print(f"\n[Using {tool_name}...]", end="", flush=True)
                    in_tool = True

            elif event_type == "content_block_delta":
                delta = event.get("delta", {})
                # Only stream text when not executing a tool
                if delta.get("type") == "text_delta" and not in_tool:
                    sys.stdout.write(delta.get("text", ""))
                    sys.stdout.flush()

            elif event_type == "content_block_stop":
                if in_tool:
                    # Tool call finished
                    print(" done", flush=True)
                    in_tool = False

        elif isinstance(message, ResultMessage):
            # Agent finished all work
            print(f"\n\n--- Complete ---")

asyncio.run(streaming_ui())
```

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Track whether we're currently in a tool call
let inTool = false;

for await (const message of query({
  prompt: "Find all TODO comments in the codebase",
  options: {
    includePartialMessages: true,
    allowedTools: ["Read", "Bash", "Grep"],
  }
})) {
  if (message.type === "stream_event") {
    const event = message.event;

    if (event.type === "content_block_start") {
      if (event.content_block.type === "tool_use") {
        // Tool call is starting - show status indicator
        process.stdout.write(`\n[Using ${event.content_block.name}...]`);
        inTool = true;
      }
    } else if (event.type === "content_block_delta") {
      // Only stream text when not executing a tool
      if (event.delta.type === "text_delta" && !inTool) {
        process.stdout.write(event.delta.text);
      }
    } else if (event.type === "content_block_stop") {
      if (inTool) {
        // Tool call finished
        console.log(" done");
        inTool = false;
      }
    }
  } else if (message.type === "result") {
    // Agent finished all work
    console.log("\n\n--- Complete ---");
  }
}
```

</CodeGroup>

## Keterbatasan yang diketahui

Beberapa fitur SDK tidak kompatibel dengan streaming:

- **Extended thinking**: ketika Anda secara eksplisit menetapkan `max_thinking_tokens` (Python) atau `maxThinkingTokens` (TypeScript), pesan `StreamEvent` tidak dipancarkan. Anda hanya akan menerima pesan lengkap setelah setiap giliran. Perhatikan bahwa pemikiran dinonaktifkan secara default di SDK, jadi streaming berfungsi kecuali Anda mengaktifkannya.
- **Structured output**: hasil JSON muncul hanya di `ResultMessage.structured_output` akhir, bukan sebagai delta streaming. Lihat [structured outputs](/docs/id/agent-sdk/structured-outputs) untuk detail.

## Langkah berikutnya

Sekarang yang Anda dapat streaming teks dan pemanggilan alat secara real-time, jelajahi topik terkait ini:

- [Interactive vs one-shot queries](/docs/id/agent-sdk/streaming-vs-single-mode): pilih antara mode input untuk kasus penggunaan Anda
- [Structured outputs](/docs/id/agent-sdk/structured-outputs): dapatkan respons JSON yang diketik dari agen
- [Permissions](/docs/id/agent-sdk/permissions): kontrol alat mana yang dapat digunakan agen