---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/stop-reasons
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: fbdec175c330e55c48ff4da9f38af6940000dc2b65c45a17b61a9650df9d8d27
---

# Menangani alasan berhenti

Deteksi penolakan dan alasan berhenti lainnya langsung dari pesan hasil dalam Agent SDK

---

Bidang `stop_reason` pada pesan hasil memberi tahu Anda mengapa model berhenti menghasilkan. Ini adalah cara yang direkomendasikan untuk mendeteksi penolakan, batas token maksimal, dan kondisi penghentian lainnya (tidak diperlukan parsing stream).

<Tip>
`stop_reason` tersedia pada setiap `ResultMessage`, terlepas dari apakah streaming diaktifkan. Anda tidak perlu mengatur `include_partial_messages` (Python) atau `includePartialMessages` (TypeScript).
</Tip>

## Membaca stop_reason

Bidang `stop_reason` hadir pada pesan hasil kesuksesan dan kesalahan. Periksanya setelah mengulangi aliran pesan:

<CodeGroup>

```python Python
from claude_agent_sdk import query, ResultMessage
import asyncio

async def check_stop_reason():
    async for message in query(prompt="Write a poem about the ocean"):
        if isinstance(message, ResultMessage):
            print(f"Stop reason: {message.stop_reason}")
            if message.stop_reason == "refusal":
                print("The model declined this request.")

asyncio.run(check_stop_reason())
```

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Write a poem about the ocean",
})) {
  if (message.type === "result") {
    console.log("Stop reason:", message.stop_reason);
    if (message.stop_reason === "refusal") {
      console.log("The model declined this request.");
    }
  }
}
```

</CodeGroup>

## Alasan berhenti yang tersedia

| Alasan berhenti | Arti |
|:------------|:--------|
| `end_turn` | Model selesai menghasilkan responsnya secara normal. |
| `max_tokens` | Respons mencapai batas token keluaran maksimal. |
| `stop_sequence` | Model menghasilkan urutan berhenti yang dikonfigurasi. |
| `refusal` | Model menolak untuk memenuhi permintaan. |
| `tool_use` | Keluaran akhir model adalah panggilan alat. Ini jarang terjadi dalam hasil SDK karena panggilan alat biasanya dieksekusi sebelum hasil dikembalikan. |
| `null` | Tidak ada respons API yang diterima; misalnya, kesalahan terjadi sebelum permintaan pertama, atau hasil diputar ulang dari sesi yang di-cache. |

## Alasan berhenti pada hasil kesalahan

Hasil kesalahan (seperti `error_max_turns` atau `error_during_execution`) juga membawa `stop_reason`. Nilainya mencerminkan pesan asisten terakhir yang diterima sebelum kesalahan terjadi:

| Varian hasil | nilai `stop_reason` |
|:---------------|:-------------------|
| `success` | Alasan berhenti dari pesan asisten akhir. |
| `error_max_turns` | Alasan berhenti dari pesan asisten terakhir sebelum batas giliran tercapai. |
| `error_max_budget_usd` | Alasan berhenti dari pesan asisten terakhir sebelum anggaran terlampaui. |
| `error_max_structured_output_retries` | Alasan berhenti dari pesan asisten terakhir sebelum batas percobaan ulang tercapai. |
| `error_during_execution` | Alasan berhenti terakhir yang terlihat, atau `null` jika kesalahan terjadi sebelum respons API apa pun. |

<CodeGroup>

```python Python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
import asyncio

async def handle_max_turns():
    options = ClaudeAgentOptions(max_turns=3)

    async for message in query(prompt="Refactor this module", options=options):
        if isinstance(message, ResultMessage):
            if message.subtype == "error_max_turns":
                print(f"Hit turn limit. Last stop reason: {message.stop_reason}")
                # stop_reason might be "end_turn" or "tool_use"
                # depending on what the model was doing when the limit hit

asyncio.run(handle_max_turns())
```

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Refactor this module",
  options: { maxTurns: 3 },
})) {
  if (message.type === "result" && message.subtype === "error_max_turns") {
    console.log("Hit turn limit. Last stop reason:", message.stop_reason);
    // stop_reason might be "end_turn" or "tool_use"
    // depending on what the model was doing when the limit hit
  }
}
```

</CodeGroup>

## Mendeteksi penolakan

`stop_reason === "refusal"` adalah cara paling sederhana untuk mendeteksi ketika model menolak permintaan. Sebelumnya, mendeteksi penolakan memerlukan pengaktifan streaming pesan parsial dan pemindaian manual pesan `StreamEvent` untuk acara `message_delta`. Dengan `stop_reason` pada pesan hasil, Anda dapat memeriksa secara langsung:

<CodeGroup>

```python Python
from claude_agent_sdk import query, ResultMessage
import asyncio

async def safe_query(prompt: str):
    async for message in query(prompt=prompt):
        if isinstance(message, ResultMessage):
            if message.stop_reason == "refusal":
                print("Request was declined. Please revise your prompt.")
                return None
            return message.result
    return None

asyncio.run(safe_query("Summarize this article"))
```

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

async function safeQuery(prompt: string): Promise<string | null> {
  for await (const message of query({ prompt })) {
    if (message.type === "result") {
      if (message.stop_reason === "refusal") {
        console.log("Request was declined. Please revise your prompt.");
        return null;
      }
      if (message.subtype === "success") {
        return message.result;
      }
      return null;
    }
  }
  return null;
}
```

</CodeGroup>

## Langkah selanjutnya

- [Streaming respons secara real-time](/docs/id/agent-sdk/streaming-output): akses acara API mentah termasuk `message_delta` saat tiba
- [Keluaran terstruktur](/docs/id/agent-sdk/structured-outputs): dapatkan respons JSON yang diketik dari agen
- [Melacak biaya dan penggunaan](/docs/id/agent-sdk/cost-tracking): pahami penggunaan token dan penagihan dari pesan hasil