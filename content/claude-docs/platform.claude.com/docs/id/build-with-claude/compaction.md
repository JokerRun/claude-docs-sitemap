---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/compaction
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: cb0f073bc693f08652c636637e8cf08c340735d41b8fe89d1f7ed64fa9a76a53
---

# Compaction

Compaction konteks sisi server untuk mengelola percakapan panjang yang mendekati batas jendela konteks.

---

<Tip>
Compaction sisi server adalah strategi yang direkomendasikan untuk mengelola konteks dalam percakapan jangka panjang dan alur kerja agentic. Ini menangani manajemen konteks secara otomatis dengan usaha integrasi minimal.
</Tip>

Compaction memperpanjang panjang konteks efektif untuk percakapan dan tugas jangka panjang dengan secara otomatis merangkum konteks yang lebih lama saat mendekati batas jendela konteks. Ini ideal untuk:

- Percakapan berbasis obrolan, multi-putaran di mana Anda ingin pengguna menggunakan satu obrolan untuk jangka waktu yang lama
- Prompt berorientasi tugas yang memerlukan banyak pekerjaan lanjutan (sering kali penggunaan alat) yang mungkin melebihi jendela konteks 200K

<Note>
Compaction saat ini dalam beta. Sertakan [beta header](/docs/id/api/beta-headers) `compact-2026-01-12` dalam permintaan API Anda untuk menggunakan fitur ini.
</Note>

## Model yang didukung

Compaction didukung pada model berikut:

- Claude Opus 4.6 (`claude-opus-4-6`)

## Cara kerja compaction

Ketika compaction diaktifkan, Claude secara otomatis merangkum percakapan Anda saat mendekati ambang token yang dikonfigurasi. API:

1. Mendeteksi ketika token input melebihi ambang pemicu yang Anda tentukan.
2. Menghasilkan ringkasan percakapan saat ini.
3. Membuat blok `compaction` yang berisi ringkasan.
4. Melanjutkan respons dengan konteks yang dikompaksi.

Pada permintaan berikutnya, tambahkan respons ke pesan Anda. API secara otomatis menghapus semua blok pesan sebelum blok `compaction`, melanjutkan percakapan dari ringkasan.

![Compaction flow diagram](/docs/images/compaction-flow.svg)

## Penggunaan dasar

Aktifkan compaction dengan menambahkan strategi `compact_20260112` ke `context_management.edits` dalam permintaan Messages API Anda.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: compact-2026-01-12" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
    "max_tokens": 4096,
    "messages": [
        {
            "role": "user",
            "content": "Help me build a website"
        }
    ],
    "context_management": {
        "edits": [
            {
                "type": "compact_20260112"
            }
        ]
    }
}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

messages = [{"role": "user", "content": "Help me build a website"}]

response = client.beta.messages.create(
    betas=["compact-2026-01-12"],
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=messages,
    context_management={
        "edits": [
            {
                "type": "compact_20260112"
            }
        ]
    }
)

# Append the response (including any compaction block) to continue the conversation
messages.append({"role": "assistant", "content": response.content})
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const messages = [{ role: "user", content: "Help me build a website" }];

const response = await client.beta.messages.create({
  betas: ["compact-2026-01-12"],
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages,
  context_management: {
    edits: [
      {
        type: "compact_20260112"
      }
    ]
  }
});

// Append the response (including any compaction block) to continue the conversation
messages.push({ role: "assistant", content: response.content });
```
</CodeGroup>

## Parameter

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `type` | string | Required | Harus `"compact_20260112"` |
| `trigger` | object | 150,000 tokens | Kapan memicu compaction. Harus minimal 50.000 token. |
| `pause_after_compaction` | boolean | `false` | Apakah akan berhenti setelah menghasilkan ringkasan compaction |
| `instructions` | string | `null` | Prompt perangkuman khusus. Sepenuhnya menggantikan prompt default saat disediakan. |

### Konfigurasi trigger

Konfigurasikan kapan compaction dipicu menggunakan parameter `trigger`:

<CodeGroup>
```python Python
response = client.beta.messages.create(
    betas=["compact-2026-01-12"],
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=messages,
    context_management={
        "edits": [
            {
                "type": "compact_20260112",
                "trigger": {
                    "type": "input_tokens",
                    "value": 150000
                }
            }
        ]
    }
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  betas: ["compact-2026-01-12"],
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages,
  context_management: {
    edits: [
      {
        type: "compact_20260112",
        trigger: {
          type: "input_tokens",
          value: 150000
        }
      }
    ]
  }
});
```
</CodeGroup>

### Instruksi perangkuman khusus

Secara default, compaction menggunakan prompt perangkuman berikut:

```text
You have written a partial transcript for the initial task above. Please write a summary of the transcript. The purpose of this summary is to provide continuity so you can continue to make progress towards solving the task in a future context, where the raw history above may not be accessible and will be replaced with this summary. Write down anything that would be helpful, including the state, next steps, learnings etc. You must wrap your summary in a <summary></summary> block.
```

Anda dapat menyediakan instruksi khusus melalui parameter `instructions` untuk sepenuhnya menggantikan prompt ini. Instruksi khusus tidak melengkapi default; mereka sepenuhnya menggantinya:

<CodeGroup>
```python Python
response = client.beta.messages.create(
    betas=["compact-2026-01-12"],
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=messages,
    context_management={
        "edits": [
            {
                "type": "compact_20260112",
                "instructions": "Focus on preserving code snippets, variable names, and technical decisions."
            }
        ]
    }
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  betas: ["compact-2026-01-12"],
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages,
  context_management: {
    edits: [
      {
        type: "compact_20260112",
        instructions: "Focus on preserving code snippets, variable names, and technical decisions."
      }
    ]
  }
});
```
</CodeGroup>

### Berhenti setelah compaction

Gunakan `pause_after_compaction` untuk menghentikan API setelah menghasilkan ringkasan compaction. Ini memungkinkan Anda menambahkan blok konten tambahan (seperti menyimpan pesan terbaru atau pesan berorientasi instruksi tertentu) sebelum API melanjutkan dengan respons.

Ketika diaktifkan, API mengembalikan pesan dengan alasan berhenti `compaction` setelah menghasilkan blok compaction:

<CodeGroup>
```python Python
response = client.beta.messages.create(
    betas=["compact-2026-01-12"],
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=messages,
    context_management={
        "edits": [
            {
                "type": "compact_20260112",
                "pause_after_compaction": True
            }
        ]
    }
)

# Check if compaction triggered a pause
if response.stop_reason == "compaction":
    # Response contains only the compaction block
    messages.append({"role": "assistant", "content": response.content})

    # Continue the request
    response = client.beta.messages.create(
        betas=["compact-2026-01-12"],
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=messages,
        context_management={
            "edits": [{"type": "compact_20260112"}]
        }
    )
```

```typescript TypeScript
let response = await client.beta.messages.create({
  betas: ["compact-2026-01-12"],
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages,
  context_management: {
    edits: [
      {
        type: "compact_20260112",
        pause_after_compaction: true
      }
    ]
  }
});

// Check if compaction triggered a pause
if (response.stop_reason === "compaction") {
  // Response contains only the compaction block
  messages.push({ role: "assistant", content: response.content });

  // Continue the request
  response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-6",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  });
}
```
</CodeGroup>

#### Memberlakukan anggaran token total

Ketika model bekerja pada tugas panjang dengan banyak iterasi penggunaan alat, konsumsi token total dapat tumbuh secara signifikan. Anda dapat menggabungkan `pause_after_compaction` dengan penghitung compaction untuk memperkirakan penggunaan kumulatif dan dengan anggun membungkus tugas setelah anggaran tercapai:

```python Python
TRIGGER_THRESHOLD = 100_000
TOTAL_TOKEN_BUDGET = 3_000_000
n_compactions = 0

response = client.beta.messages.create(
    betas=["compact-2026-01-12"],
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=messages,
    context_management={
        "edits": [
            {
                "type": "compact_20260112",
                "trigger": {"type": "input_tokens", "value": TRIGGER_THRESHOLD},
                "pause_after_compaction": True,
            }
        ]
    },
)

if response.stop_reason == "compaction":
    n_compactions += 1
    messages.append({"role": "assistant", "content": response.content})

    # Estimate total tokens consumed; prompt wrap-up if over budget
    if n_compactions * TRIGGER_THRESHOLD >= TOTAL_TOKEN_BUDGET:
        messages.append({
            "role": "user",
            "content": "Please wrap up your current work and summarize the final state.",
        })
```

## Bekerja dengan blok compaction

Ketika compaction dipicu, API mengembalikan blok `compaction` di awal respons asisten.

Percakapan jangka panjang dapat menghasilkan beberapa compaction. Blok compaction terakhir mencerminkan keadaan akhir prompt, menggantikan konten sebelumnya dengan ringkasan yang dihasilkan.

```json
{
  "content": [
    {
      "type": "compaction",
      "content": "Summary of the conversation: The user requested help building a web scraper..."
    },
    {
      "type": "text",
      "text": "Based on our conversation so far..."
    }
  ]
}
```

### Melewatkan blok compaction kembali

Anda harus melewatkan blok `compaction` kembali ke API pada permintaan berikutnya untuk melanjutkan percakapan dengan prompt yang diperpendek. Pendekatan paling sederhana adalah menambahkan seluruh konten respons ke pesan Anda:

<CodeGroup>
```python Python
# After receiving a response with a compaction block
messages.append({"role": "assistant", "content": response.content})

# Continue the conversation
messages.append({"role": "user", "content": "Now add error handling"})

response = client.beta.messages.create(
    betas=["compact-2026-01-12"],
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=messages,
    context_management={
        "edits": [{"type": "compact_20260112"}]
    }
)
```

```typescript TypeScript
// After receiving a response with a compaction block
messages.push({ role: "assistant", content: response.content });

// Continue the conversation
messages.push({ role: "user", content: "Now add error handling" });

const nextResponse = await client.beta.messages.create({
  betas: ["compact-2026-01-12"],
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages,
  context_management: {
    edits: [{ type: "compact_20260112" }]
  }
});
```
</CodeGroup>

Ketika API menerima blok `compaction`, semua blok konten sebelumnya diabaikan. Anda dapat:

- Menyimpan pesan asli dalam daftar Anda dan membiarkan API menangani penghapusan konten yang dikompaksi
- Secara manual menghapus pesan yang dikompaksi dan hanya menyertakan blok compaction ke depan

### Streaming

Ketika streaming respons dengan compaction diaktifkan, Anda akan menerima acara `content_block_start` ketika compaction dimulai. Blok compaction streaming berbeda dari blok teks. Anda akan menerima acara `content_block_start`, diikuti oleh satu `content_block_delta` dengan konten ringkasan lengkap (tidak ada streaming perantara), dan kemudian acara `content_block_stop`.

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

with client.beta.messages.stream(
    betas=["compact-2026-01-12"],
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=messages,
    context_management={
        "edits": [{"type": "compact_20260112"}]
    }
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "compaction":
                print("Compaction started...")
            elif event.content_block.type == "text":
                print("Text response started...")

        elif event.type == "content_block_delta":
            if event.delta.type == "compaction_delta":
                print(f"Compaction complete: {len(event.delta.content)} chars")
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)

    # Get the final accumulated message
    message = stream.get_final_message()
    messages.append({"role": "assistant", "content": message.content})
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const stream = await client.beta.messages.stream({
  betas: ["compact-2026-01-12"],
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages,
  context_management: {
    edits: [{ type: "compact_20260112" }]
  }
});

for await (const event of stream) {
  if (event.type === "content_block_start") {
    if (event.content_block.type === "compaction") {
      console.log("Compaction started...");
    } else if (event.content_block.type === "text") {
      console.log("Text response started...");
    }
  } else if (event.type === "content_block_delta") {
    if (event.delta.type === "compaction_delta") {
      console.log(`Compaction complete: ${event.delta.content.length} chars`);
    } else if (event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
}

// Get the final accumulated message
const message = await stream.finalMessage();
messages.push({ role: "assistant", content: message.content });
```
</CodeGroup>

### Prompt caching

Anda dapat menambahkan breakpoint `cache_control` pada blok compaction, yang menyimpan prompt sistem lengkap bersama dengan konten yang dirangkum. Konten yang dikompaksi asli diabaikan.

```json
{
    "role": "assistant",
    "content": [
        {
            "type": "compaction",
            "content": "[summary text]",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": "Based on our conversation..."
        }
    ]
}
```

## Memahami penggunaan

Compaction memerlukan langkah sampling tambahan, yang berkontribusi pada batas laju dan penagihan. API mengembalikan informasi penggunaan terperinci dalam respons:

```json
{
  "usage": {
    "input_tokens": 45000,
    "output_tokens": 1234,
    "iterations": [
      {
        "type": "compaction",
        "input_tokens": 180000,
        "output_tokens": 3500
      },
      {
        "type": "message",
        "input_tokens": 23000,
        "output_tokens": 1000
      }
    ]
  }
}
```

Array `iterations` menunjukkan penggunaan untuk setiap iterasi sampling. Ketika compaction terjadi, Anda akan melihat iterasi `compaction` diikuti oleh iterasi `message` utama. Hitungan token iterasi akhir mencerminkan ukuran konteks efektif setelah compaction.

<Note>
`input_tokens` dan `output_tokens` tingkat atas tidak termasuk penggunaan iterasi compaction—mereka mencerminkan jumlah semua iterasi non-compaction. Untuk menghitung total token yang dikonsumsi dan ditagih untuk permintaan, jumlahkan semua entri dalam array `usage.iterations`.

Jika Anda sebelumnya mengandalkan `usage.input_tokens` dan `usage.output_tokens` untuk pelacakan biaya atau audit, Anda perlu memperbarui logika pelacakan Anda untuk mengagregasi di seluruh `usage.iterations` ketika compaction diaktifkan. Array `iterations` hanya diisi ketika compaction baru dipicu selama permintaan. Menerapkan kembali blok `compaction` sebelumnya tidak menimbulkan biaya compaction tambahan, dan bidang penggunaan tingkat atas tetap akurat dalam hal itu.
</Note>

## Menggabungkan dengan fitur lain

### Server tools

Ketika menggunakan server tools (seperti pencarian web), pemicu compaction diperiksa di awal setiap iterasi sampling. Compaction dapat terjadi beberapa kali dalam satu permintaan tergantung pada ambang pemicu Anda dan jumlah output yang dihasilkan.

### Token counting

Endpoint token counting (`/v1/messages/count_tokens`) menerapkan blok `compaction` yang ada dalam prompt Anda tetapi tidak memicu compaction baru. Gunakan untuk memeriksa hitungan token efektif Anda setelah compaction sebelumnya:

<CodeGroup>
```python Python
count_response = client.beta.messages.count_tokens(
    betas=["compact-2026-01-12"],
    model="claude-opus-4-6",
    messages=messages,
    context_management={
        "edits": [{"type": "compact_20260112"}]
    }
)

print(f"Current tokens: {count_response.input_tokens}")
print(f"Original tokens: {count_response.context_management.original_input_tokens}")
```

```typescript TypeScript
const countResponse = await client.beta.messages.countTokens({
  betas: ["compact-2026-01-12"],
  model: "claude-opus-4-6",
  messages,
  context_management: {
    edits: [{ type: "compact_20260112" }]
  }
});

console.log(`Current tokens: ${countResponse.input_tokens}`);
console.log(`Original tokens: ${countResponse.context_management.original_input_tokens}`);
```
</CodeGroup>

## Contoh

Berikut adalah contoh lengkap percakapan jangka panjang dengan compaction:

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

messages: list[dict] = []

def chat(user_message: str) -> str:
    messages.append({"role": "user", "content": user_message})

    response = client.beta.messages.create(
        betas=["compact-2026-01-12"],
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=messages,
        context_management={
            "edits": [
                {
                    "type": "compact_20260112",
                    "trigger": {"type": "input_tokens", "value": 100000}
                }
            ]
        }
    )

    # Append response (compaction blocks are automatically included)
    messages.append({"role": "assistant", "content": response.content})

    # Return the text content
    return next(
        block.text for block in response.content if block.type == "text"
    )

# Run a long conversation
print(chat("Help me build a Python web scraper"))
print(chat("Add support for JavaScript-rendered pages"))
print(chat("Now add rate limiting and error handling"))
# ... continue as long as needed
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const messages: Anthropic.Beta.BetaMessageParam[] = [];

async function chat(userMessage: string): Promise<string> {
  messages.push({ role: "user", content: userMessage });

  const response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-6",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [
        {
          type: "compact_20260112",
          trigger: { type: "input_tokens", value: 100000 }
        }
      ]
    }
  });

  // Append response (compaction blocks are automatically included)
  messages.push({ role: "assistant", content: response.content });

  // Return the text content
  const textBlock = response.content.find(block => block.type === "text");
  return textBlock?.text ?? "";
}

// Run a long conversation
console.log(await chat("Help me build a Python web scraper"));
console.log(await chat("Add support for JavaScript-rendered pages"));
console.log(await chat("Now add rate limiting and error handling"));
// ... continue as long as needed
```
</CodeGroup>

Berikut adalah contoh yang menggunakan `pause_after_compaction` untuk menyimpan dua pesan terakhir (satu putaran pengguna + satu asisten) secara verbatim alih-alih merangkumnya:

<CodeGroup>
```python Python
import anthropic
from typing import Any

client = anthropic.Anthropic()

messages: list[dict[str, Any]] = []

def chat(user_message: str) -> str:
    messages.append({"role": "user", "content": user_message})

    response = client.beta.messages.create(
        betas=["compact-2026-01-12"],
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=messages,
        context_management={
            "edits": [
                {
                    "type": "compact_20260112",
                    "trigger": {"type": "input_tokens", "value": 100000},
                    "pause_after_compaction": True
                }
            ]
        }
    )

    # Check if compaction occurred and paused
    if response.stop_reason == "compaction":
        # Get the compaction block from the response
        compaction_block = response.content[0]

        # Preserve the last 2 messages (1 user + 1 assistant turn)
        # by including them after the compaction block
        preserved_messages = messages[-2:] if len(messages) >= 2 else messages

        # Build new message list: compaction + preserved messages
        new_assistant_content = [compaction_block]
        messages_after_compaction = [
            {"role": "assistant", "content": new_assistant_content}
        ] + preserved_messages

        # Continue the request with the compacted context + preserved messages
        response = client.beta.messages.create(
            betas=["compact-2026-01-12"],
            model="claude-opus-4-6",
            max_tokens=4096,
            messages=messages_after_compaction,
            context_management={
                "edits": [{"type": "compact_20260112"}]
            }
        )

        # Update our message list to reflect the compaction
        messages.clear()
        messages.extend(messages_after_compaction)

    # Append the final response
    messages.append({"role": "assistant", "content": response.content})

    # Return the text content
    return next(
        block.text for block in response.content if block.type == "text"
    )

# Run a long conversation
print(chat("Help me build a Python web scraper"))
print(chat("Add support for JavaScript-rendered pages"))
print(chat("Now add rate limiting and error handling"))
# ... continue as long as needed
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

let messages: Anthropic.Beta.BetaMessageParam[] = [];

async function chat(userMessage: string): Promise<string> {
  messages.push({ role: "user", content: userMessage });

  let response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-6",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [
        {
          type: "compact_20260112",
          trigger: { type: "input_tokens", value: 100000 },
          pause_after_compaction: true
        }
      ]
    }
  });

  // Check if compaction occurred and paused
  if (response.stop_reason === "compaction") {
    // Get the compaction block from the response
    const compactionBlock = response.content[0];

    // Preserve the last 2 messages (1 user + 1 assistant turn)
    // by including them after the compaction block
    const preservedMessages = messages.length >= 2
      ? messages.slice(-2)
      : [...messages];

    // Build new message list: compaction + preserved messages
    const messagesAfterCompaction: Anthropic.Beta.BetaMessageParam[] = [
      { role: "assistant", content: [compactionBlock] },
      ...preservedMessages
    ];

    // Continue the request with the compacted context + preserved messages
    response = await client.beta.messages.create({
      betas: ["compact-2026-01-12"],
      model: "claude-opus-4-6",
      max_tokens: 4096,
      messages: messagesAfterCompaction,
      context_management: {
        edits: [{ type: "compact_20260112" }]
      }
    });

    // Update our message list to reflect the compaction
    messages = messagesAfterCompaction;
  }

  // Append the final response
  messages.push({ role: "assistant", content: response.content });

  // Return the text content
  const textBlock = response.content.find(block => block.type === "text");
  return textBlock?.text ?? "";
}

// Run a long conversation
console.log(await chat("Help me build a Python web scraper"));
console.log(await chat("Add support for JavaScript-rendered pages"));
console.log(await chat("Now add rate limiting and error handling"));
// ... continue as long as needed
```
</CodeGroup>

## Batasan saat ini

- **Model yang sama untuk perangkuman:** Model yang ditentukan dalam permintaan Anda digunakan untuk perangkuman. Tidak ada opsi untuk menggunakan model yang berbeda (misalnya, lebih murah) untuk ringkasan.

## Langkah berikutnya

<CardGroup>
  <Card title="Compaction cookbook" icon="book" href="https://platform.claude.com/cookbook">
    Jelajahi contoh dan implementasi praktis di cookbook.
  </Card>
  <Card title="Context windows" icon="arrows-maximize" href="/docs/id/build-with-claude/context-windows">
    Pelajari tentang ukuran jendela konteks dan strategi manajemen.
  </Card>
  <Card title="Context editing" icon="pen" href="/docs/id/build-with-claude/context-editing">
    Jelajahi strategi lain untuk mengelola konteks percakapan seperti pembersihan hasil alat dan pembersihan blok pemikiran.
  </Card>
</CardGroup>