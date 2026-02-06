---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/adaptive-thinking
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 50581283bdc52382b7efabcf70bb49a1b1f6d006a1f59545efa21d053a3b271b
---

# Pemikiran adaptif

Biarkan Claude secara dinamis memutuskan kapan dan berapa banyak untuk berpikir dengan mode pemikiran adaptif.

---

Pemikiran adaptif adalah cara yang direkomendasikan untuk menggunakan [extended thinking](/docs/id/build-with-claude/extended-thinking) dengan Claude Opus 4.6. Alih-alih menetapkan anggaran token pemikiran secara manual, pemikiran adaptif memungkinkan Claude secara dinamis memutuskan kapan dan berapa banyak untuk berpikir berdasarkan kompleksitas setiap permintaan.

<Tip>
Pemikiran adaptif secara andal mendorong kinerja yang lebih baik daripada extended thinking dengan `budget_tokens` tetap, dan kami merekomendasikan untuk beralih ke pemikiran adaptif untuk mendapatkan respons paling cerdas dari Opus 4.6. Tidak ada header beta yang diperlukan.
</Tip>

## Model yang didukung

Pemikiran adaptif didukung pada model berikut:

- Claude Opus 4.6 (`claude-opus-4-6`)

<Warning>
`thinking.type: "enabled"` dan `budget_tokens` adalah **deprecated** pada Opus 4.6 dan akan dihapus dalam rilis model di masa depan. Gunakan `thinking.type: "adaptive"` dengan [parameter effort](/docs/id/build-with-claude/effort) sebagai gantinya.

Model yang lebih lama (Sonnet 4.5, Opus 4.5, dll.) tidak mendukung pemikiran adaptif dan memerlukan `thinking.type: "enabled"` dengan `budget_tokens`.
</Warning>

## Cara kerja pemikiran adaptif

Dalam mode adaptif, pemikiran bersifat opsional untuk model. Claude mengevaluasi kompleksitas setiap permintaan dan memutuskan apakah dan berapa banyak untuk berpikir. Pada tingkat effort default (`high`), Claude hampir selalu akan berpikir. Pada tingkat effort yang lebih rendah, Claude dapat melewati pemikiran untuk masalah yang lebih sederhana.

Pemikiran adaptif juga secara otomatis mengaktifkan [interleaved thinking](/docs/id/build-with-claude/extended-thinking#interleaved-thinking). Ini berarti Claude dapat berpikir di antara panggilan alat, menjadikannya sangat efektif untuk alur kerja agentic.

## Cara menggunakan pemikiran adaptif

Atur `thinking.type` ke `"adaptive"` dalam permintaan API Anda:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
    "max_tokens": 16000,
    "thinking": {
        "type": "adaptive"
    },
    "messages": [
        {
            "role": "user",
            "content": "Explain why the sum of two even numbers is always even."
        }
    ]
}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={
        "type": "adaptive"
    },
    messages=[{
        "role": "user",
        "content": "Explain why the sum of two even numbers is always even."
    }]
)

for block in response.content:
    if block.type == "thinking":
        print(f"\nThinking: {block.thinking}")
    elif block.type == "text":
        print(f"\nResponse: {block.text}")
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 16000,
  thinking: {
    type: "adaptive"
  },
  messages: [{
    role: "user",
    content: "Explain why the sum of two even numbers is always even."
  }]
});

for (const block of response.content) {
  if (block.type === "thinking") {
    console.log(`\nThinking: ${block.thinking}`);
  } else if (block.type === "text") {
    console.log(`\nResponse: ${block.text}`);
  }
}
```
</CodeGroup>

## Pemikiran adaptif dengan parameter effort

Anda dapat menggabungkan pemikiran adaptif dengan [parameter effort](/docs/id/build-with-claude/effort) untuk memandu berapa banyak Claude berpikir. Tingkat effort bertindak sebagai panduan lembut untuk alokasi pemikiran Claude:

| Tingkat effort | Perilaku pemikiran |
|:-------------|:------------------|
| `max` | Claude selalu berpikir tanpa batasan pada kedalaman pemikiran. Hanya Opus 4.6 — permintaan menggunakan `max` pada model lain akan mengembalikan kesalahan. |
| `high` (default) | Claude selalu berpikir. Memberikan penalaran mendalam pada tugas kompleks. |
| `medium` | Claude menggunakan pemikiran moderat. Dapat melewati pemikiran untuk kueri yang sangat sederhana. |
| `low` | Claude meminimalkan pemikiran. Melewati pemikiran untuk tugas sederhana di mana kecepatan paling penting. |

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={
        "type": "adaptive"
    },
    output_config={
        "effort": "medium"
    },
    messages=[{
        "role": "user",
        "content": "What is the capital of France?"
    }]
)

print(response.content[0].text)
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 16000,
  thinking: {
    type: "adaptive"
  },
  output_config: {
    effort: "medium"
  },
  messages: [{
    role: "user",
    content: "What is the capital of France?"
  }]
});

console.log(response.content[0].text);
```

```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
    "max_tokens": 16000,
    "thinking": {
        "type": "adaptive"
    },
    "output_config": {
        "effort": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
}'
```
</CodeGroup>

## Streaming dengan pemikiran adaptif

Pemikiran adaptif bekerja dengan mulus dengan [streaming](/docs/id/build-with-claude/streaming). Blok pemikiran di-stream melalui acara `thinking_delta` seperti mode pemikiran manual:

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    messages=[{"role": "user", "content": "What is the greatest common divisor of 1071 and 462?"}],
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            print(f"\nStarting {event.content_block.type} block...")
        elif event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const stream = await client.messages.stream({
  model: "claude-opus-4-6",
  max_tokens: 16000,
  thinking: { type: "adaptive" },
  messages: [{ role: "user", content: "What is the greatest common divisor of 1071 and 462?" }]
});

for await (const event of stream) {
  if (event.type === "content_block_start") {
    console.log(`\nStarting ${event.content_block.type} block...`);
  } else if (event.type === "content_block_delta") {
    if (event.delta.type === "thinking_delta") {
      process.stdout.write(event.delta.thinking);
    } else if (event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
}
```
</CodeGroup>

## Pemikiran adaptif vs manual vs disabled

| Mode | Config | Ketersediaan | Kapan digunakan |
|:-----|:-------|:-------------|:------------|
| **Adaptif** | `thinking: {type: "adaptive"}` | Opus 4.6 | Claude memutuskan kapan dan berapa banyak untuk berpikir. Gunakan `effort` untuk memandu. |
| **Manual** | `thinking: {type: "enabled", budget_tokens: N}` | Semua model. Deprecated pada Opus 4.6 — gunakan mode adaptif sebagai gantinya. | Ketika Anda memerlukan kontrol presisi atas pengeluaran token pemikiran. |
| **Disabled** | Hilangkan parameter `thinking` | Semua model | Ketika Anda tidak memerlukan extended thinking dan menginginkan latensi terendah. |

<Note>
Pemikiran adaptif saat ini tersedia pada Opus 4.6. Model yang lebih lama hanya mendukung `type: "enabled"` dengan `budget_tokens`. Pada Opus 4.6, `type: "enabled"` dengan `budget_tokens` masih diterima tetapi deprecated — kami merekomendasikan menggunakan pemikiran adaptif dengan [parameter effort](/docs/id/build-with-claude/effort) sebagai gantinya.
</Note>

## Pertimbangan penting

### Perubahan validasi

Ketika menggunakan pemikiran adaptif, giliran asisten sebelumnya tidak perlu dimulai dengan blok pemikiran. Ini lebih fleksibel daripada mode manual, di mana API memberlakukan bahwa giliran yang diaktifkan pemikiran dimulai dengan blok pemikiran.

### Prompt caching

Permintaan berturut-turut menggunakan pemikiran `adaptive` mempertahankan titik henti [prompt cache](/docs/id/build-with-claude/prompt-caching). Namun, beralih antara mode pemikiran `adaptive` dan `enabled`/`disabled` memecah titik henti cache untuk pesan. Prompt sistem dan definisi alat tetap di-cache terlepas dari perubahan mode.

### Tuning perilaku pemikiran

Perilaku pemicu pemikiran adaptif dapat dipromptkan. Jika Claude berpikir lebih atau kurang sering daripada yang Anda inginkan, Anda dapat menambahkan panduan ke prompt sistem Anda:

```
Extended thinking adds latency and should only be used when it
will meaningfully improve answer quality — typically for problems
that require multi-step reasoning. When in doubt, respond directly.
```

<Warning>
Mengarahkan Claude untuk berpikir lebih jarang dapat mengurangi kualitas pada tugas yang mendapat manfaat dari penalaran. Ukur dampak pada beban kerja spesifik Anda sebelum menerapkan tuning berbasis prompt ke produksi. Pertimbangkan pengujian dengan [tingkat effort](/docs/id/build-with-claude/effort) yang lebih rendah terlebih dahulu.
</Warning>

### Kontrol biaya

Gunakan `max_tokens` sebagai batas keras pada total output (pemikiran + teks respons). Parameter `effort` memberikan panduan lembut tambahan tentang berapa banyak pemikiran yang Claude alokasikan. Bersama-sama, ini memberi Anda kontrol efektif atas biaya.

Pada tingkat effort `high` dan `max`, Claude dapat berpikir lebih ekstensif dan lebih mungkin untuk menghabiskan anggaran `max_tokens`. Jika Anda mengamati `stop_reason: "max_tokens"` dalam respons, pertimbangkan untuk meningkatkan `max_tokens` untuk memberikan lebih banyak ruang kepada model, atau menurunkan tingkat effort.

## Bekerja dengan blok pemikiran

Konsep berikut berlaku untuk semua model yang mendukung extended thinking, terlepas dari apakah Anda menggunakan mode adaptif atau manual.

### Pemikiran ringkasan

With extended thinking enabled, the Messages API for Claude 4 models returns a summary of Claude's full thinking process. Summarized thinking provides the full intelligence benefits of extended thinking, while preventing misuse.

Here are some important considerations for summarized thinking:

- You're charged for the full thinking tokens generated by the original request, not the summary tokens.
- The billed output token count will **not match** the count of tokens you see in the response.
- The first few lines of thinking output are more verbose, providing detailed reasoning that's particularly helpful for prompt engineering purposes.
- As Anthropic seeks to improve the extended thinking feature, summarization behavior is subject to change.
- Summarization preserves the key ideas of Claude's thinking process with minimal added latency, enabling a streamable user experience and easy migration from Claude Sonnet 3.7 to Claude 4 and later models.
- Summarization is processed by a different model than the one you target in your requests. The thinking model does not see the summarized output.

<Note>
Claude Sonnet 3.7 continues to return full thinking output.

In rare cases where you need access to full thinking output for Claude 4 models, [contact our sales team](mailto:sales@anthropic.com).
</Note>

### Enkripsi pemikiran

Full thinking content is encrypted and returned in the `signature` field. This field is used to verify that thinking blocks were generated by Claude when passed back to the API.

<Note>
It is only strictly necessary to send back thinking blocks when using [tools with extended thinking](/docs/en/build-with-claude/extended-thinking#extended-thinking-with-tool-use). Otherwise you can omit thinking blocks from previous turns, or let the API strip them for you if you pass them back.

If sending back thinking blocks, we recommend passing everything back as you received it for consistency and to avoid potential issues.
</Note>

Here are some important considerations on thinking encryption:
- When [streaming responses](/docs/en/build-with-claude/extended-thinking#streaming-thinking), the signature is added via a `signature_delta` inside a `content_block_delta` event just before the `content_block_stop` event.
- `signature` values are significantly longer in Claude 4 models than in previous models.
- The `signature` field is an opaque field and should not be interpreted or parsed - it exists solely for verification purposes.
- `signature` values are compatible across platforms (Claude APIs, [Amazon Bedrock](/docs/en/build-with-claude/claude-on-amazon-bedrock), and [Vertex AI](/docs/en/build-with-claude/claude-on-vertex-ai)). Values generated on one platform will be compatible with another.

### Redaksi pemikiran

Occasionally Claude's internal reasoning will be flagged by our safety systems. When this occurs, we encrypt some or all of the `thinking` block and return it to you as a `redacted_thinking` block. `redacted_thinking` blocks are decrypted when passed back to the API, allowing Claude to continue its response without losing context.

When building customer-facing applications that use extended thinking:

- Be aware that redacted thinking blocks contain encrypted content that isn't human-readable
- Consider providing a simple explanation like: "Some of Claude's internal reasoning has been automatically encrypted for safety reasons. This doesn't affect the quality of responses."
- If showing thinking blocks to users, you can filter out redacted blocks while preserving normal thinking blocks
- Be transparent that using extended thinking features may occasionally result in some reasoning being encrypted
- Implement appropriate error handling to gracefully manage redacted thinking without breaking your UI

Here's an example showing both normal and redacted thinking blocks:

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me analyze this step by step...",
      "signature": "WaUjzkypQ2mUEVM36O2TxuC06KN8xyfbJwyem2dw3URve/op91XWHOEBLLqIOMfFG/UvLEczmEsUjavL...."
    },
    {
      "type": "redacted_thinking",
      "data": "EmwKAhgBEgy3va3pzix/LafPsn4aDFIT2Xlxh0L5L8rLVyIwxtE3rAFBa8cr3qpPkNRj2YfWXGmKDxH4mPnZ5sQ7vB9URj2pLmN3kF8/dW5hR7xJ0aP1oLs9yTcMnKVf2wRpEGjH9XZaBt4UvDcPrQ..."
    },
    {
      "type": "text",
      "text": "Based on my analysis..."
    }
  ]
}
```

<Note>
Seeing redacted thinking blocks in your output is expected behavior. The model can still use this redacted reasoning to inform its responses while maintaining safety guardrails.

If you need to test redacted thinking handling in your application, you can use this special test string as your prompt: `ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB`
</Note>

When passing `thinking` and `redacted_thinking` blocks back to the API in a multi-turn conversation, you must include the complete unmodified block back to the API for the last assistant turn. This is critical for maintaining the model's reasoning flow. We suggest always passing back all thinking blocks to the API. For more details, see the [Preserving thinking blocks](/docs/en/build-with-claude/extended-thinking#preserving-thinking-blocks) section.

### Harga

For complete pricing information including base rates, cache writes, cache hits, and output tokens, see the [pricing page](/docs/en/about-claude/pricing).

The thinking process incurs charges for:
- Tokens used during thinking (output tokens)
- Thinking blocks from the last assistant turn included in subsequent requests (input tokens)
- Standard text output tokens

<Note>
When extended thinking is enabled, a specialized system prompt is automatically included to support this feature.
</Note>

When using summarized thinking:
- **Input tokens**: Tokens in your original request (excludes thinking tokens from previous turns)
- **Output tokens (billed)**: The original thinking tokens that Claude generated internally
- **Output tokens (visible)**: The summarized thinking tokens you see in the response
- **No charge**: Tokens used to generate the summary

<Warning>
The billed output token count will **not** match the visible token count in the response. You are billed for the full thinking process, not the summary you see.
</Warning>

### Topik tambahan

Halaman extended thinking mencakup beberapa topik secara lebih detail dengan contoh kode khusus mode:

- **[Penggunaan alat dengan pemikiran](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use)**: Aturan yang sama berlaku untuk pemikiran adaptif — pertahankan blok pemikiran di antara panggilan alat dan waspadai keterbatasan `tool_choice` ketika pemikiran aktif.
- **[Prompt caching](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-prompt-caching)**: Dengan pemikiran adaptif, permintaan berturut-turut menggunakan mode pemikiran yang sama mempertahankan titik henti cache. Beralih antara mode `adaptive` dan `enabled`/`disabled` memecah titik henti cache untuk pesan (prompt sistem dan definisi alat tetap di-cache).
- **[Jendela konteks](/docs/id/build-with-claude/extended-thinking#max-tokens-and-context-window-size-with-extended-thinking)**: Bagaimana token pemikiran berinteraksi dengan `max_tokens` dan batas jendela konteks.

## Langkah berikutnya

<CardGroup>
  <Card title="Extended thinking" icon="settings" href="/docs/id/build-with-claude/extended-thinking">
    Pelajari lebih lanjut tentang extended thinking, termasuk mode manual, penggunaan alat, dan prompt caching.
  </Card>
  <Card title="Parameter effort" icon="gauge" href="/docs/id/build-with-claude/effort">
    Kontrol seberapa menyeluruh Claude merespons dengan parameter effort.
  </Card>
</CardGroup>