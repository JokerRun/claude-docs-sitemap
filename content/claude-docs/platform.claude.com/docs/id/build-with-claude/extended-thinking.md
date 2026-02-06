---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/extended-thinking
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 7dfdf0a59499cb9cfaec556ff8243cad945a4a8b3aa9805a03a1b53aac00a267
---

# Membangun dengan pemikiran yang diperluas

Extended thinking memberikan Claude kemampuan penalaran yang ditingkatkan untuk tugas-tugas kompleks, dengan transparansi yang bervariasi ke dalam proses pemikiran langkah demi langkah sebelum memberikan jawaban akhirnya.

---

Extended thinking memberikan Claude kemampuan penalaran yang ditingkatkan untuk tugas-tugas kompleks, dengan transparansi yang bervariasi ke dalam proses pemikiran langkah demi langkah sebelum memberikan jawaban akhirnya.

<Note>
Untuk Claude Opus 4.6, kami merekomendasikan menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) dengan [parameter effort](/docs/id/build-with-claude/effort) alih-alih mode pemikiran manual yang dijelaskan di halaman ini. Konfigurasi `thinking: {type: "enabled", budget_tokens: N}` manual sudah usang di Opus 4.6 dan akan dihapus dalam rilis model di masa depan.
</Note>

## Model yang didukung

Extended thinking didukung dalam model berikut:

- Claude Opus 4.6 (`claude-opus-4-6`) — [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) direkomendasikan; mode manual (`type: "enabled"`) sudah usang
- Claude Opus 4.5 (`claude-opus-4-5-20251101`)
- Claude Opus 4.1 (`claude-opus-4-1-20250805`)
- Claude Opus 4 (`claude-opus-4-20250514`)
- Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`) ([usang](/docs/id/about-claude/model-deprecations))
- Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)

<Note>
Perilaku API berbeda di seluruh model Claude Sonnet 3.7 dan Claude 4, tetapi bentuk API tetap sama persis.

Untuk informasi lebih lanjut, lihat [Perbedaan dalam pemikiran di seluruh versi model](#differences-in-thinking-across-model-versions).
</Note>

## Cara kerja extended thinking

Ketika extended thinking diaktifkan, Claude membuat blok konten `thinking` di mana ia mengeluarkan penalaran internalnya. Claude menggabungkan wawasan dari penalaran ini sebelum membuat respons akhir.

Respons API akan mencakup blok konten `thinking`, diikuti oleh blok konten `text`.

Berikut adalah contoh format respons default:

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Mari saya analisis ini langkah demi langkah...",
      "signature": "WaUjzkypQ2mUEVM36O2TxuC06KN8xyfbJwyem2dw3URve/op91XWHOEBLLqIOMfFG/UvLEczmEsUjavL...."
    },
    {
      "type": "text",
      "text": "Berdasarkan analisis saya..."
    }
  ]
}
```

Untuk informasi lebih lanjut tentang format respons extended thinking, lihat [Referensi API Pesan](/docs/id/api/messages).

## Cara menggunakan extended thinking

Berikut adalah contoh menggunakan extended thinking dalam Messages API:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-5",
    "max_tokens": 16000,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 10000
    },
    "messages": [
        {
            "role": "user",
            "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
        }
    ]
}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{
        "role": "user",
        "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
    }]
)

# The response will contain summarized thinking blocks and text blocks
for block in response.content:
    if block.type == "thinking":
        print(f"\nThinking summary: {block.thinking}")
    elif block.type == "text":
        print(f"\nResponse: {block.text}")
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  messages: [{
    role: "user",
    content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
  }]
});

// The response will contain summarized thinking blocks and text blocks
for (const block of response.content) {
  if (block.type === "thinking") {
    console.log(`\nThinking summary: ${block.thinking}`);
  } else if (block.type === "text") {
    console.log(`\nResponse: ${block.text}`);
  }
}
```

</CodeGroup>

Untuk mengaktifkan extended thinking, tambahkan objek `thinking`, dengan parameter `type` diatur ke `enabled` dan `budget_tokens` ke anggaran token yang ditentukan untuk extended thinking. Untuk Claude Opus 4.6, kami merekomendasikan menggunakan `type: "adaptive"` sebagai gantinya — lihat [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) untuk detail. Meskipun `type: "enabled"` dengan `budget_tokens` masih didukung di Opus 4.6, ini sudah usang dan akan dihapus dalam rilis di masa depan.

Parameter `budget_tokens` menentukan jumlah maksimum token yang diizinkan Claude gunakan untuk proses penalaran internalnya. Di model Claude 4 dan model yang lebih baru, batas ini berlaku untuk token pemikiran penuh, bukan untuk [output yang diringkas](#summarized-thinking). Anggaran yang lebih besar dapat meningkatkan kualitas respons dengan memungkinkan analisis yang lebih menyeluruh untuk masalah kompleks, meskipun Claude mungkin tidak menggunakan seluruh anggaran yang dialokasikan, terutama pada rentang di atas 32k.

<Warning>
`budget_tokens` sudah usang di Claude Opus 4.6 dan akan dihapus dalam rilis model di masa depan. Kami merekomendasikan menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran sebagai gantinya.
</Warning>

<Note>
Claude Opus 4.6 mendukung hingga 128K token output. Model sebelumnya mendukung hingga 64K token output.
</Note>

`budget_tokens` harus diatur ke nilai kurang dari `max_tokens`. Namun, ketika menggunakan [interleaved thinking dengan tools](#interleaved-thinking), Anda dapat melampaui batas ini karena batas token menjadi seluruh jendela konteks Anda (200k token).

### Summarized thinking

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

### Streaming thinking

Anda dapat melakukan streaming respons extended thinking menggunakan [server-sent events (SSE)](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents).

Ketika streaming diaktifkan untuk extended thinking, Anda menerima konten pemikiran melalui acara `thinking_delta`.

Untuk dokumentasi lebih lanjut tentang streaming melalui Messages API, lihat [Streaming Messages](/docs/id/build-with-claude/streaming).

Berikut adalah cara menangani streaming dengan pemikiran:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-5",
    "max_tokens": 16000,
    "stream": true,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 10000
    },
    "messages": [
        {
            "role": "user",
            "content": "What is the greatest common divisor of 1071 and 462?"
        }
    ]
}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "What is the greatest common divisor of 1071 and 462?"}],
) as stream:
    thinking_started = False
    response_started = False

    for event in stream:
        if event.type == "content_block_start":
            print(f"\nStarting {event.content_block.type} block...")
            # Reset flags for each new block
            thinking_started = False
            response_started = False
        elif event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                if not thinking_started:
                    print("Thinking: ", end="", flush=True)
                    thinking_started = True
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                if not response_started:
                    print("Response: ", end="", flush=True)
                    response_started = True
                print(event.delta.text, end="", flush=True)
        elif event.type == "content_block_stop":
            print("\nBlock complete.")
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const stream = await client.messages.stream({
  model: "claude-sonnet-4-5",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  messages: [{
    role: "user",
    content: "What is the greatest common divisor of 1071 and 462?"
  }]
});

let thinkingStarted = false;
let responseStarted = false;

for await (const event of stream) {
  if (event.type === 'content_block_start') {
    console.log(`\nStarting ${event.content_block.type} block...`);
    // Reset flags for each new block
    thinkingStarted = false;
    responseStarted = false;
  } else if (event.type === 'content_block_delta') {
    if (event.delta.type === 'thinking_delta') {
      if (!thinkingStarted) {
        process.stdout.write('Thinking: ');
        thinkingStarted = true;
      }
      process.stdout.write(event.delta.thinking);
    } else if (event.delta.type === 'text_delta') {
      if (!responseStarted) {
        process.stdout.write('Response: ');
        responseStarted = true;
      }
      process.stdout.write(event.delta.text);
    }
  } else if (event.type === 'content_block_stop') {
    console.log('\nBlock complete.');
  }
}
```

</CodeGroup>

<TryInConsoleButton userPrompt="What is the greatest common divisor of 1071 and 462?" thinkingBudgetTokens={16000}>
  Try in Console
</TryInConsoleButton>

Contoh output streaming:
```json
event: message_start
data: {"type": "message_start", "message": {"id": "msg_01...", "type": "message", "role": "assistant", "content": [], "model": "claude-sonnet-4-5", "stop_reason": null, "stop_sequence": null}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n462 = 3 × 147 + 21\n147 = 7 × 21 + 0\n\nSo GCD(1071, 462) = 21"}}

// Additional thinking deltas...

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3hGgxBdjrkzLoky3dl1pkiMOYds..."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "text", "text": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "text_delta", "text": "The greatest common divisor of 1071 and 462 is **21**."}}

// Additional text deltas...

event: content_block_stop
data: {"type": "content_block_stop", "index": 1}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}}

event: message_stop
data: {"type": "message_stop"}
```

<Note>
Ketika menggunakan streaming dengan pemikiran diaktifkan, Anda mungkin memperhatikan bahwa teks kadang-kadang tiba dalam potongan yang lebih besar bergantian dengan pengiriman token demi token yang lebih kecil. Ini adalah perilaku yang diharapkan, terutama untuk konten pemikiran.

Sistem streaming perlu memproses konten dalam batch untuk kinerja optimal, yang dapat menghasilkan pola pengiriman "chunky" ini, dengan kemungkinan penundaan antara acara streaming. Kami terus bekerja untuk meningkatkan pengalaman ini, dengan pembaruan di masa depan berfokus pada membuat konten pemikiran melakukan streaming dengan lebih lancar.
</Note>

## Extended thinking dengan penggunaan tool

Extended thinking dapat digunakan bersama dengan [tool use](/docs/id/agents-and-tools/tool-use/overview), memungkinkan Claude untuk bernalar melalui pemilihan tool dan pemrosesan hasil.

Ketika menggunakan extended thinking dengan tool use, perhatikan batasan berikut:

1. **Batasan pilihan tool**: Tool use dengan pemikiran hanya mendukung `tool_choice: {"type": "auto"}` (default) atau `tool_choice: {"type": "none"}`. Menggunakan `tool_choice: {"type": "any"}` atau `tool_choice: {"type": "tool", "name": "..."}` akan menghasilkan kesalahan karena opsi ini memaksa penggunaan tool, yang tidak kompatibel dengan extended thinking.

2. **Menjaga blok pemikiran**: Selama penggunaan tool, Anda harus melewatkan blok `thinking` kembali ke API untuk pesan asisten terakhir. Sertakan blok yang lengkap dan tidak dimodifikasi kembali ke API untuk mempertahankan kontinuitas penalaran.

### Mengalihkan mode pemikiran dalam percakapan

Anda tidak dapat mengalihkan pemikiran di tengah giliran asisten, termasuk selama loop penggunaan tool. Seluruh giliran asisten harus beroperasi dalam mode pemikiran tunggal:

- **Jika pemikiran diaktifkan**, giliran asisten akhir harus dimulai dengan blok pemikiran.
- **Jika pemikiran dinonaktifkan**, giliran asisten akhir tidak boleh berisi blok pemikiran apa pun

Dari perspektif model, **loop penggunaan tool adalah bagian dari giliran asisten**. Giliran asisten tidak selesai sampai Claude menyelesaikan respons penuhnya, yang mungkin mencakup beberapa panggilan tool dan hasil.

Misalnya, urutan ini semua bagian dari **giliran asisten tunggal**:
```
User: "What's the weather in Paris?"
Assistant: [thinking] + [tool_use: get_weather]
User: [tool_result: "20°C, sunny"]
Assistant: [text: "The weather in Paris is 20°C and sunny"]
```

Meskipun ada beberapa pesan API, loop penggunaan tool secara konseptual merupakan bagian dari satu respons asisten yang berkelanjutan.

#### Degradasi pemikiran yang elegan

Ketika konflik pemikiran mid-turn terjadi (seperti mengalihkan pemikiran on atau off selama loop penggunaan tool), API secara otomatis menonaktifkan pemikiran untuk permintaan itu. Untuk mempertahankan kualitas model dan tetap on-distribution, API dapat:

- Menghapus blok pemikiran dari percakapan ketika mereka akan membuat struktur giliran yang tidak valid
- Menonaktifkan pemikiran untuk permintaan saat ini ketika riwayat percakapan tidak kompatibel dengan pemikiran yang diaktifkan

Ini berarti bahwa mencoba mengalihkan pemikiran mid-turn tidak akan menyebabkan kesalahan, tetapi pemikiran akan diam-diam dinonaktifkan untuk permintaan itu. Untuk mengkonfirmasi apakah pemikiran aktif, periksa kehadiran blok `thinking` dalam respons.

#### Panduan praktis

**Praktik terbaik**: Rencanakan strategi pemikiran Anda di awal setiap giliran daripada mencoba mengalihkan mid-turn.

**Contoh: Mengalihkan pemikiran setelah menyelesaikan giliran**
```
User: "What's the weather?"
Assistant: [tool_use] (thinking disabled)
User: [tool_result]
Assistant: [text: "It's sunny"]
User: "What about tomorrow?"
Assistant: [thinking] + [text: "..."] (thinking enabled - new turn)
```

Dengan menyelesaikan giliran asisten sebelum mengalihkan pemikiran, Anda memastikan bahwa pemikiran benar-benar diaktifkan untuk permintaan baru.

<Note>
Mengalihkan mode pemikiran juga membatalkan prompt caching untuk riwayat pesan. Untuk detail lebih lanjut, lihat bagian [Extended thinking dengan prompt caching](#extended-thinking-with-prompt-caching).
</Note>

<section title="Contoh: Melewatkan blok pemikiran dengan hasil tool">

Berikut adalah contoh praktis yang menunjukkan cara mempertahankan blok pemikiran saat memberikan hasil tool:

<CodeGroup>
```python Python
weather_tool = {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    }
}

# First request - Claude responds with thinking and tool request
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    tools=[weather_tool],
    messages=[
        {"role": "user", "content": "What's the weather in Paris?"}
    ]
)
```

```typescript TypeScript
const weatherTool = {
  name: "get_weather",
  description: "Get current weather for a location",
  input_schema: {
    type: "object",
    properties: {
      location: { type: "string" }
    },
    required: ["location"]
  }
};

// First request - Claude responds with thinking and tool request
const response = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  tools: [weatherTool],
  messages: [
    { role: "user", content: "What's the weather in Paris?" }
  ]
});
```

</CodeGroup>

Respons API akan mencakup blok pemikiran, teks, dan tool_use:

```json
{
    "content": [
        {
            "type": "thinking",
            "thinking": "The user wants to know the current weather in Paris. I have access to a function `get_weather`...",
            "signature": "BDaL4VrbR2Oj0hO4XpJxT28J5TILnCrrUXoKiiNBZW9P+nr8XSj1zuZzAl4egiCCpQNvfyUuFFJP5CncdYZEQPPmLxYsNrcs...."
        },
        {
            "type": "text",
            "text": "I can help you get the current weather information for Paris. Let me check that for you"
        },
        {
            "type": "tool_use",
            "id": "toolu_01CswdEQBMshySk6Y9DFKrfq",
            "name": "get_weather",
            "input": {
                "location": "Paris"
            }
        }
    ]
}
```

Sekarang mari kita lanjutkan percakapan dan gunakan tool

<CodeGroup>
```python Python
# Extract thinking block and tool use block
thinking_block = next((block for block in response.content
                      if block.type == 'thinking'), None)
tool_use_block = next((block for block in response.content
                      if block.type == 'tool_use'), None)

# Call your actual weather API, here is where your actual API call would go
# let's pretend this is what we get back
weather_data = {"temperature": 88}

# Second request - Include thinking block and tool result
# No new thinking blocks will be generated in the response
continuation = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    tools=[weather_tool],
    messages=[
        {"role": "user", "content": "What's the weather in Paris?"},
        # notice that the thinking_block is passed in as well as the tool_use_block
        # if this is not passed in, an error is raised
        {"role": "assistant", "content": [thinking_block, tool_use_block]},
        {"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use_block.id,
            "content": f"Current temperature: {weather_data['temperature']}°F"
        }]}
    ]
)
```

```typescript TypeScript
// Extract thinking block and tool use block
const thinkingBlock = response.content.find(block =>
  block.type === 'thinking');
const toolUseBlock = response.content.find(block =>
  block.type === 'tool_use');

// Call your actual weather API, here is where your actual API call would go
// let's pretend this is what we get back
const weatherData = { temperature: 88 };

// Second request - Include thinking block and tool result
// No new thinking blocks will be generated in the response
const continuation = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  tools: [weatherTool],
  messages: [
    { role: "user", content: "What's the weather in Paris?" },
    // notice that the thinkingBlock is passed in as well as the toolUseBlock
    // if this is not passed in, an error is raised
    { role: "assistant", content: [thinkingBlock, toolUseBlock] },
    { role: "user", content: [{
      type: "tool_result",
      tool_use_id: toolUseBlock.id,
      content: `Current temperature: ${weatherData.temperature}°F`
    }]}
  ]
});
```

</CodeGroup>

Respons API sekarang **hanya** akan mencakup teks

```json
{
    "content": [
        {
            "type": "text",
            "text": "Currently in Paris, the temperature is 88°F (31°C)"
        }
    ]
}
```

</section>

### Menjaga blok pemikiran

Selama penggunaan tool, Anda harus melewatkan blok `thinking` kembali ke API, dan Anda harus menyertakan blok lengkap yang tidak dimodifikasi kembali ke API. Ini sangat penting untuk mempertahankan aliran penalaran model dan integritas percakapan.

<Tip>
Meskipun Anda dapat menghilangkan blok `thinking` dari giliran `assistant` sebelumnya, kami menyarankan selalu melewatkan semua blok pemikiran ke API untuk percakapan multi-turn apa pun. API akan:
- Secara otomatis memfilter blok pemikiran yang disediakan
- Menggunakan blok pemikiran yang relevan yang diperlukan untuk mempertahankan penalaran model
- Hanya menagih token input untuk blok yang ditampilkan ke Claude
</Tip>

<Note>
Ketika mengalihkan mode pemikiran selama percakapan, ingat bahwa seluruh giliran asisten (termasuk loop penggunaan tool) harus beroperasi dalam mode pemikiran tunggal. Untuk detail lebih lanjut, lihat [Mengalihkan mode pemikiran dalam percakapan](#toggling-thinking-modes-in-conversations).
</Note>

Ketika Claude memanggil tool, ia menjeda konstruksi respons untuk menunggu informasi eksternal. Ketika hasil tool dikembalikan, Claude akan melanjutkan membangun respons yang ada. Ini memerlukan pemeliharaan blok pemikiran selama penggunaan tool, untuk beberapa alasan:

1. **Kontinuitas penalaran**: Blok pemikiran menangkap penalaran langkah demi langkah Claude yang menyebabkan permintaan tool. Ketika Anda memposting hasil tool, menyertakan pemikiran asli memastikan Claude dapat melanjutkan penalarannya dari tempat ia berhenti.

2. **Pemeliharaan konteks**: Meskipun hasil tool muncul sebagai pesan pengguna dalam struktur API, mereka adalah bagian dari aliran penalaran yang berkelanjutan. Mempertahankan blok pemikiran mempertahankan aliran konseptual ini di seluruh panggilan API yang berbeda. Untuk informasi lebih lanjut tentang manajemen konteks, lihat [panduan kami tentang jendela konteks](/docs/id/build-with-claude/context-windows).

**Penting**: Ketika memberikan blok `thinking`, seluruh urutan blok `thinking` yang berurutan harus cocok dengan output yang dihasilkan oleh model selama permintaan asli; Anda tidak dapat mengatur ulang atau memodifikasi urutan blok ini.

### Interleaved thinking

Extended thinking dengan tool use di model Claude 4 mendukung interleaved thinking, yang memungkinkan Claude untuk berpikir di antara panggilan tool dan membuat penalaran yang lebih canggih setelah menerima hasil tool.

Dengan interleaved thinking, Claude dapat:
- Bernalar tentang hasil panggilan tool sebelum memutuskan apa yang harus dilakukan selanjutnya
- Menghubungkan beberapa panggilan tool dengan langkah penalaran di antara
- Membuat keputusan yang lebih bernuansa berdasarkan hasil perantara

Untuk Claude Opus 4.6, interleaved thinking secara otomatis diaktifkan ketika menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) — tidak ada header beta yang diperlukan.

Untuk model Claude 4, tambahkan [header beta](/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14` ke permintaan API Anda untuk mengaktifkan interleaved thinking.

Berikut adalah beberapa pertimbangan penting untuk interleaved thinking:
- Dengan interleaved thinking, `budget_tokens` dapat melebihi parameter `max_tokens`, karena mewakili total anggaran di semua blok pemikiran dalam satu giliran asisten.
- Interleaved thinking hanya didukung untuk [tools yang digunakan melalui Messages API](/docs/id/agents-and-tools/tool-use/overview).
- Untuk model Claude 4, interleaved thinking memerlukan header beta `interleaved-thinking-2025-05-14`.
- Panggilan langsung ke Claude API memungkinkan Anda melewatkan `interleaved-thinking-2025-05-14` dalam permintaan ke model apa pun, tanpa efek.
- Di platform pihak ketiga (misalnya, [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock) dan [Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)), jika Anda melewatkan `interleaved-thinking-2025-05-14` ke model apa pun selain Claude Opus 4.6, Claude Opus 4.5, Claude Opus 4.1, Opus 4, atau Sonnet 4, permintaan Anda akan gagal.

<section title="Tool use tanpa interleaved thinking">

Tanpa interleaved thinking, Claude berpikir sekali di awal giliran asisten. Respons berikutnya setelah hasil tool berlanjut tanpa blok pemikiran baru.

```
User: "What's the total revenue if we sold 150 units at $50 each,
       and how does this compare to our average monthly revenue?"

Turn 1: [thinking] "I need to calculate 150 * $50, then check the database..."
        [tool_use: calculator] { "expression": "150 * 50" }
  ↓ tool result: "7500"

Turn 2: [tool_use: database_query] { "query": "SELECT AVG(revenue)..." }
        ↑ no thinking block
  ↓ tool result: "5200"

Turn 3: [text] "The total revenue is $7,500, which is 44% above your
        average monthly revenue of $5,200."
        ↑ no thinking block
```

</section>

<section title="Tool use dengan interleaved thinking">

Dengan interleaved thinking diaktifkan, Claude dapat berpikir setelah menerima setiap hasil tool, memungkinkannya untuk bernalar tentang hasil perantara sebelum melanjutkan.

```
User: "What's the total revenue if we sold 150 units at $50 each,
       and how does this compare to our average monthly revenue?"

Turn 1: [thinking] "I need to calculate 150 * $50 first..."
        [tool_use: calculator] { "expression": "150 * 50" }
  ↓ tool result: "7500"

Turn 2: [thinking] "Got $7,500. Now I should query the database to compare..."
        [tool_use: database_query] { "query": "SELECT AVG(revenue)..." }
        ↑ thinking after receiving calculator result
  ↓ tool result: "5200"

Turn 3: [thinking] "$7,500 vs $5,200 average - that's a 44% increase..."
        [text] "The total revenue is $7,500, which is 44% above your
        average monthly revenue of $5,200."
        ↑ thinking before final answer
```

</section>

## Extended thinking dengan prompt caching

[Prompt caching](/docs/id/build-with-claude/prompt-caching) dengan pemikiran memiliki beberapa pertimbangan penting:

<Tip>
Tugas extended thinking sering kali memakan waktu lebih dari 5 menit untuk diselesaikan. Pertimbangkan menggunakan [durasi cache 1 jam](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) untuk mempertahankan cache hits di seluruh sesi pemikiran yang lebih lama dan alur kerja multi-langkah.
</Tip>

**Penghapusan konteks blok pemikiran**
- Blok pemikiran dari giliran sebelumnya dihapus dari konteks, yang dapat mempengaruhi breakpoint cache
- Ketika melanjutkan percakapan dengan penggunaan tool, blok pemikiran di-cache dan dihitung sebagai token input ketika dibaca dari cache
- Ini menciptakan trade-off: meskipun blok pemikiran tidak mengonsumsi ruang jendela konteks secara visual, mereka masih dihitung terhadap penggunaan token input Anda ketika di-cache
- Jika pemikiran menjadi dinonaktifkan dan Anda melewatkan konten pemikiran dalam giliran penggunaan tool saat ini, konten pemikiran akan dihapus dan pemikiran akan tetap dinonaktifkan untuk permintaan itu

**Pola invalidasi cache**
- Perubahan pada parameter pemikiran (diaktifkan/dinonaktifkan atau alokasi anggaran) membatalkan breakpoint cache pesan
- [Interleaved thinking](#interleaved-thinking) memperkuat invalidasi cache, karena blok pemikiran dapat terjadi di antara beberapa [panggilan tool](#extended-thinking-with-tool-use)
- Prompt sistem dan tools tetap di-cache meskipun ada perubahan parameter pemikiran atau penghapusan blok

<Note>
Meskipun blok pemikiran dihapus untuk caching dan perhitungan konteks, mereka harus dipertahankan ketika melanjutkan percakapan dengan [tool use](#extended-thinking-with-tool-use), terutama dengan [interleaved thinking](#interleaved-thinking).
</Note>

### Memahami perilaku caching blok pemikiran

Saat menggunakan pemikiran yang diperluas dengan penggunaan alat, blok pemikiran menunjukkan perilaku caching tertentu yang mempengaruhi penghitungan token:

**Cara kerjanya:**

1. Caching hanya terjadi ketika Anda membuat permintaan berikutnya yang mencakup hasil alat
2. Ketika permintaan berikutnya dibuat, riwayat percakapan sebelumnya (termasuk blok pemikiran) dapat di-cache
3. Blok pemikiran yang di-cache ini dihitung sebagai token input dalam metrik penggunaan Anda ketika dibaca dari cache
4. Ketika blok pengguna non-hasil-alat disertakan, semua blok pemikiran sebelumnya diabaikan dan dihapus dari konteks

**Alur contoh terperinci:**

**Permintaan 1:**
```
User: "What's the weather in Paris?"
```
**Respons 1:**
```
[thinking_block_1] + [tool_use block 1]
```

**Permintaan 2:**
```
User: ["What's the weather in Paris?"], 
Assistant: [thinking_block_1] + [tool_use block 1], 
User: [tool_result_1, cache=True]
```
**Respons 2:**
```
[thinking_block_2] + [text block 2]
```
Permintaan 2 menulis cache dari konten permintaan (bukan respons). Cache mencakup pesan pengguna asli, blok pemikiran pertama, blok penggunaan alat, dan hasil alat.

**Permintaan 3:**
```
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response, cache=True]
```
Untuk Claude Opus 4.5 dan yang lebih baru (termasuk Claude Opus 4.6), semua blok pemikiran sebelumnya disimpan secara default. Untuk model yang lebih lama, karena blok pengguna non-hasil-alat disertakan, semua blok pemikiran sebelumnya diabaikan. Permintaan ini akan diproses sama dengan:
```
User: ["What's the weather in Paris?"],
Assistant: [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [text block 2],
User: [Text response, cache=True]
```

**Poin kunci:**
- Perilaku caching ini terjadi secara otomatis, bahkan tanpa penanda `cache_control` eksplisit
- Perilaku ini konsisten apakah menggunakan pemikiran reguler atau pemikiran yang disisipi

<section title="Caching prompt sistem (dipertahankan ketika pemikiran berubah)">

<CodeGroup>
```python Python
from anthropic import Anthropic
import requests
from bs4 import BeautifulSoup

client = Anthropic()

def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text
    text = soup.get_text()

    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text

# Fetch the content of the article
book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
book_content = fetch_article_content(book_url)
# Use just enough text for caching (first few chapters)
LARGE_TEXT = book_content[:5000]

SYSTEM_PROMPT=[
    {
        "type": "text",
        "text": "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully.",
    },
    {
        "type": "text",
        "text": LARGE_TEXT,
        "cache_control": {"type": "ephemeral"}
    }
]

MESSAGES = [
    {
        "role": "user",
        "content": "Analyze the tone of this passage."
    }
]

# First request - establish cache
print("First request - establishing cache")
response1 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 4000
    },
    system=SYSTEM_PROMPT,
    messages=MESSAGES
)

print(f"First response usage: {response1.usage}")

MESSAGES.append({
    "role": "assistant",
    "content": response1.content
})
MESSAGES.append({
    "role": "user",
    "content": "Analyze the characters in this passage."
})
# Second request - same thinking parameters (cache hit expected)
print("\nSecond request - same thinking parameters (cache hit expected)")
response2 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 4000
    },
    system=SYSTEM_PROMPT,
    messages=MESSAGES
)

print(f"Second response usage: {response2.usage}")

# Third request - different thinking parameters (cache miss for messages)
print("\nThird request - different thinking parameters (cache miss for messages)")
response3 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 8000  # Changed thinking budget
    },
    system=SYSTEM_PROMPT,  # System prompt remains cached
    messages=MESSAGES  # Messages cache is invalidated
)

print(f"Third response usage: {response3.usage}")
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';
import axios from 'axios';
import * as cheerio from 'cheerio';

const client = new Anthropic();

async function fetchArticleContent(url: string): Promise<string> {
  const response = await axios.get(url);
  const $ = cheerio.load(response.data);
  
  // Remove script and style elements
  $('script, style').remove();
  
  // Get text
  let text = $.text();
  
  // Break into lines and remove leading and trailing space on each
  const lines = text.split('\n').map(line => line.trim());
  // Drop blank lines
  text = lines.filter(line => line.length > 0).join('\n');
  
  return text;
}

// Fetch the content of the article
const bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
const bookContent = await fetchArticleContent(bookUrl);
// Use just enough text for caching (first few chapters)
const LARGE_TEXT = bookContent.slice(0, 5000);

const SYSTEM_PROMPT = [
  {
    type: "text",
    text: "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully.",
  },
  {
    type: "text",
    text: LARGE_TEXT,
    cache_control: { type: "ephemeral" }
  }
];

const MESSAGES = [
  {
    role: "user",
    content: "Analyze the tone of this passage."
  }
];

// First request - establish cache
console.log("First request - establishing cache");
const response1 = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 20000,
  thinking: {
    type: "enabled",
    budget_tokens: 4000
  },
  system: SYSTEM_PROMPT,
  messages: MESSAGES
});

console.log(`First response usage: ${response1.usage}`);

MESSAGES.push({
  role: "assistant",
  content: response1.content
});
MESSAGES.push({
  role: "user",
  content: "Analyze the characters in this passage."
});

// Second request - same thinking parameters (cache hit expected)
console.log("\nSecond request - same thinking parameters (cache hit expected)");
const response2 = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 20000,
  thinking: {
    type: "enabled",
    budget_tokens: 4000
  },
  system: SYSTEM_PROMPT,
  messages: MESSAGES
});

console.log(`Second response usage: ${response2.usage}`);

// Third request - different thinking parameters (cache miss for messages)
console.log("\nThird request - different thinking parameters (cache miss for messages)");
const response3 = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 20000,
  thinking: {
    type: "enabled",
    budget_tokens: 8000  // Changed thinking budget
  },
  system: SYSTEM_PROMPT,  // System prompt remains cached
  messages: MESSAGES  // Messages cache is invalidated
});

console.log(`Third response usage: ${response3.usage}`);
```
</CodeGroup>

</section>
<section title="Caching pesan (dibatalkan ketika pemikiran berubah)">

<CodeGroup>
```python Python
from anthropic import Anthropic
import requests
from bs4 import BeautifulSoup

client = Anthropic()

def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text
    text = soup.get_text()

    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text

# Fetch the content of the article
book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
book_content = fetch_article_content(book_url)
# Use just enough text for caching (first few chapters)
LARGE_TEXT = book_content[:5000]

# No system prompt - caching in messages instead
MESSAGES = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": LARGE_TEXT,
                "cache_control": {"type": "ephemeral"},
            },
            {
                "type": "text",
                "text": "Analyze the tone of this passage."
            }
        ]
    }
]

# First request - establish cache
print("First request - establishing cache")
response1 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 4000
    },
    messages=MESSAGES
)

print(f"First response usage: {response1.usage}")

MESSAGES.append({
    "role": "assistant",
    "content": response1.content
})
MESSAGES.append({
    "role": "user",
    "content": "Analyze the characters in this passage."
})
# Second request - same thinking parameters (cache hit expected)
print("\nSecond request - same thinking parameters (cache hit expected)")
response2 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 4000  # Same thinking budget
    },
    messages=MESSAGES
)

print(f"Second response usage: {response2.usage}")

MESSAGES.append({
    "role": "assistant",
    "content": response2.content
})
MESSAGES.append({
    "role": "user",
    "content": "Analyze the setting in this passage."
})

# Third request - different thinking budget (cache miss expected)
print("\nThird request - different thinking budget (cache miss expected)")
response3 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 8000  # Different thinking budget breaks cache
    },
    messages=MESSAGES
)

print(f"Third response usage: {response3.usage}")
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';
import axios from 'axios';
import * as cheerio from 'cheerio';

const client = new Anthropic();

async function fetchArticleContent(url: string): Promise<string> {
  const response = await axios.get(url);
  const $ = cheerio.load(response.data);

  // Remove script and style elements
  $('script, style').remove();

  // Get text
  let text = $.text();

  // Clean up text (break into lines, remove whitespace)
  const lines = text.split('\n').map(line => line.trim());
  const chunks = lines.flatMap(line => line.split('  ').map(phrase => phrase.trim()));
  text = chunks.filter(chunk => chunk).join('\n');

  return text;
}

async function main() {
  // Fetch the content of the article
  const bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
  const bookContent = await fetchArticleContent(bookUrl);
  // Use just enough text for caching (first few chapters)
  const LARGE_TEXT = bookContent.substring(0, 5000);

  // No system prompt - caching in messages instead
  let MESSAGES = [
    {
      role: "user",
      content: [
        {
          type: "text",
          text: LARGE_TEXT,
          cache_control: {type: "ephemeral"},
        },
        {
          type: "text",
          text: "Analyze the tone of this passage."
        }
      ]
    }
  ];

  // First request - establish cache
  console.log("First request - establishing cache");
  const response1 = await client.messages.create({
    model: "claude-sonnet-4-5",
    max_tokens: 20000,
    thinking: {
      type: "enabled",
      budget_tokens: 4000
    },
    messages: MESSAGES
  });

  console.log(`First response usage: `, response1.usage);

  MESSAGES = [
    ...MESSAGES,
    {
      role: "assistant",
      content: response1.content
    },
    {
      role: "user",
      content: "Analyze the characters in this passage."
    }
  ];

  // Second request - same thinking parameters (cache hit expected)
  console.log("\nSecond request - same thinking parameters (cache hit expected)");
  const response2 = await client.messages.create({
    model: "claude-sonnet-4-5",
    max_tokens: 20000,
    thinking: {
      type: "enabled",
      budget_tokens: 4000  // Same thinking budget
    },
    messages: MESSAGES
  });

  console.log(`Second response usage: `, response2.usage);

  MESSAGES = [
    ...MESSAGES,
    {
      role: "assistant",
      content: response2.content
    },
    {
      role: "user",
      content: "Analyze the setting in this passage."
    }
  ];

  // Third request - different thinking budget (cache miss expected)
  console.log("\nThird request - different thinking budget (cache miss expected)");
  const response3 = await client.messages.create({
    model: "claude-sonnet-4-5",
    max_tokens: 20000,
    thinking: {
      type: "enabled",
      budget_tokens: 8000  // Different thinking budget breaks cache
    },
    messages: MESSAGES
  });

  console.log(`Third response usage: `, response3.usage);
}

main().catch(console.error);
```

</CodeGroup>

Berikut adalah output dari skrip (Anda mungkin melihat angka yang sedikit berbeda)

```
First request - establishing cache
First response usage: { cache_creation_input_tokens: 1370, cache_read_input_tokens: 0, input_tokens: 17, output_tokens: 700 }

Second request - same thinking parameters (cache hit expected)

Second response usage: { cache_creation_input_tokens: 0, cache_read_input_tokens: 1370, input_tokens: 303, output_tokens: 874 }

Third request - different thinking budget (cache miss expected)
Third response usage: { cache_creation_input_tokens: 1370, cache_read_input_tokens: 0, input_tokens: 747, output_tokens: 619 }
```

Contoh ini menunjukkan bahwa ketika caching diatur dalam array pesan, mengubah parameter pemikiran (budget_tokens meningkat dari 4000 menjadi 8000) **membatalkan cache**. Permintaan ketiga menunjukkan tidak ada cache hit dengan `cache_creation_input_tokens=1370` dan `cache_read_input_tokens=0`, membuktikan bahwa caching berbasis pesan dibatalkan ketika parameter pemikiran berubah.

</section>

## Token maksimal dan ukuran jendela konteks dengan pemikiran yang diperluas

Dalam model Claude yang lebih lama (sebelum Claude Sonnet 3.7), jika jumlah token prompt dan `max_tokens` melebihi jendela konteks model, sistem akan secara otomatis menyesuaikan `max_tokens` agar sesuai dengan batas konteks. Ini berarti Anda dapat mengatur nilai `max_tokens` yang besar dan sistem akan secara diam-diam menguranginya sesuai kebutuhan.

Dengan model Claude 3.7 dan 4, `max_tokens` (yang mencakup anggaran pemikiran Anda ketika pemikiran diaktifkan) diberlakukan sebagai batas ketat. Sistem sekarang akan mengembalikan kesalahan validasi jika token prompt + `max_tokens` melebihi ukuran jendela konteks.

<Note>
Anda dapat membaca [panduan kami tentang jendela konteks](/docs/id/build-with-claude/context-windows) untuk penyelaman yang lebih mendalam.
</Note>

### Jendela konteks dengan pemikiran yang diperluas

Saat menghitung penggunaan jendela konteks dengan pemikiran diaktifkan, ada beberapa pertimbangan yang perlu diperhatikan:

- Blok pemikiran dari putaran sebelumnya dihapus dan tidak dihitung terhadap jendela konteks Anda
- Pemikiran putaran saat ini dihitung terhadap batas `max_tokens` untuk putaran itu

Diagram di bawah menunjukkan manajemen token khusus ketika pemikiran yang diperluas diaktifkan:

![Diagram jendela konteks dengan pemikiran yang diperluas](/docs/images/context-window-thinking.svg)

Jendela konteks yang efektif dihitung sebagai:

```
context window =
  (current input tokens - previous thinking tokens) +
  (thinking tokens + encrypted thinking tokens + text output tokens)
```

Kami merekomendasikan menggunakan [API penghitungan token](/docs/id/build-with-claude/token-counting) untuk mendapatkan penghitungan token yang akurat untuk kasus penggunaan spesifik Anda, terutama saat bekerja dengan percakapan multi-putaran yang mencakup pemikiran.

### Jendela konteks dengan pemikiran yang diperluas dan penggunaan alat

Saat menggunakan pemikiran yang diperluas dengan penggunaan alat, blok pemikiran harus secara eksplisit dipertahankan dan dikembalikan dengan hasil alat.

Perhitungan jendela konteks yang efektif untuk pemikiran yang diperluas dengan penggunaan alat menjadi:

```
context window =
  (current input tokens + previous thinking tokens + tool use tokens) +
  (thinking tokens + encrypted thinking tokens + text output tokens)
```

Diagram di bawah mengilustrasikan manajemen token untuk pemikiran yang diperluas dengan penggunaan alat:

![Diagram jendela konteks dengan pemikiran yang diperluas dan penggunaan alat](/docs/images/context-window-thinking-tools.svg)

### Mengelola token dengan pemikiran yang diperluas

Mengingat perilaku jendela konteks dan `max_tokens` dengan pemikiran yang diperluas pada model Claude 3.7 dan 4, Anda mungkin perlu:

- Memantau dan mengelola penggunaan token Anda dengan lebih aktif
- Menyesuaikan nilai `max_tokens` saat panjang prompt Anda berubah
- Berpotensi menggunakan [endpoint penghitungan token](/docs/id/build-with-claude/token-counting) lebih sering
- Menyadari bahwa blok pemikiran sebelumnya tidak terakumulasi dalam jendela konteks Anda

Perubahan ini telah dilakukan untuk memberikan perilaku yang lebih dapat diprediksi dan transparan, terutama karena batas token maksimal telah meningkat secara signifikan.

## Enkripsi pemikiran

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

<section title="Contoh: Bekerja dengan blok pemikiran yang diredaksi">

Contoh ini menunjukkan cara menangani blok `redacted_thinking` yang mungkin muncul dalam respons ketika penalaran internal Claude berisi konten yang ditandai oleh sistem keamanan:

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

# Using a special prompt that triggers redacted thinking (for demonstration purposes only)
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{
        "role": "user",
        "content": "ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB"
    }]
)

# Identify redacted thinking blocks
has_redacted_thinking = any(
    block.type == "redacted_thinking" for block in response.content
)

if has_redacted_thinking:
    print("Response contains redacted thinking blocks")
    # These blocks are still usable in subsequent requests

    # Extract all blocks (both redacted and non-redacted)
    all_thinking_blocks = [
        block for block in response.content
        if block.type in ["thinking", "redacted_thinking"]
    ]

    # When passing to subsequent requests, include all blocks without modification
    # This preserves the integrity of Claude's reasoning

    print(f"Found {len(all_thinking_blocks)} thinking blocks total")
    print(f"These blocks are still billable as output tokens")
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

// Using a special prompt that triggers redacted thinking (for demonstration purposes only)
const response = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  messages: [{
    role: "user",
    content: "ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB"
  }]
});

// Identify redacted thinking blocks
const hasRedactedThinking = response.content.some(
  block => block.type === "redacted_thinking"
);

if (hasRedactedThinking) {
  console.log("Response contains redacted thinking blocks");
  // These blocks are still usable in subsequent requests

  // Extract all blocks (both redacted and non-redacted)
  const allThinkingBlocks = response.content.filter(
    block => block.type === "thinking" || block.type === "redacted_thinking"
  );

  // When passing to subsequent requests, include all blocks without modification
  // This preserves the integrity of Claude's reasoning

  console.log(`Found ${allThinkingBlocks.length} thinking blocks total`);
  console.log(`These blocks are still billable as output tokens`);
}
```

</CodeGroup>

<TryInConsoleButton
  userPrompt="ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB"
  thinkingBudgetTokens={16000}
>
  Coba di Konsol
</TryInConsoleButton>

</section>

## Perbedaan pemikiran di seluruh versi model

Messages API menangani pemikiran secara berbeda di seluruh model Claude Sonnet 3.7 dan Claude 4, terutama dalam perilaku redaksi dan ringkasan.

Lihat tabel di bawah untuk perbandingan yang dipadatkan:

| Fitur | Claude Sonnet 3.7 | Model Claude 4 (pra-Opus 4.5) | Claude Opus 4.5 | Claude Opus 4.6 ([pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking)) |
|---------|------------------|-------------------------------|--------------------------|--------------------------|
| **Output Pemikiran** | Mengembalikan output pemikiran lengkap | Mengembalikan pemikiran yang diringkas | Mengembalikan pemikiran yang diringkas | Mengembalikan pemikiran yang diringkas |
| **Pemikiran yang Disisipi** | Tidak didukung | Didukung dengan header beta `interleaved-thinking-2025-05-14` | Didukung dengan header beta `interleaved-thinking-2025-05-14` | Otomatis dengan pemikiran adaptif (tidak perlu header beta) |
| **Pelestarian Blok Pemikiran** | Tidak dipertahankan di seluruh putaran | Tidak dipertahankan di seluruh putaran | **Dipertahankan secara default** | **Dipertahankan secara default** |

### Pelestarian blok pemikiran di Claude Opus 4.5 dan yang lebih baru

Mulai dari Claude Opus 4.5 (dan berlanjut di Claude Opus 4.6), **blok pemikiran dari putaran asisten sebelumnya dipertahankan dalam konteks model secara default**. Ini berbeda dari model sebelumnya, yang menghapus blok pemikiran dari putaran sebelumnya.

**Manfaat pelestarian blok pemikiran:**

- **Optimasi cache**: Saat menggunakan penggunaan alat, blok pemikiran yang dipertahankan memungkinkan cache hit karena mereka dilewatkan kembali dengan hasil alat dan di-cache secara bertahap di seluruh putaran asisten, menghasilkan penghematan token dalam alur kerja multi-langkah
- **Tidak ada dampak kecerdasan**: Mempertahankan blok pemikiran tidak memiliki efek negatif pada kinerja model

**Pertimbangan penting:**

- **Penggunaan konteks**: Percakapan panjang akan mengonsumsi lebih banyak ruang konteks karena blok pemikiran dipertahankan dalam konteks
- **Perilaku otomatis**: Ini adalah perilaku default untuk model Claude Opus 4.5 dan yang lebih baru (termasuk Opus 4.6)—tidak ada perubahan kode atau header beta yang diperlukan
- **Kompatibilitas mundur**: Untuk memanfaatkan fitur ini, terus lewatkan blok pemikiran lengkap yang tidak dimodifikasi kembali ke API seperti yang Anda lakukan untuk penggunaan alat

<Note>
Untuk model sebelumnya (Claude Sonnet 4.5, Opus 4.1, dll.), blok pemikiran dari putaran sebelumnya terus dihapus dari konteks. Perilaku yang ada yang dijelaskan dalam bagian [Pemikiran yang diperluas dengan caching prompt](#extended-thinking-with-prompt-caching) berlaku untuk model tersebut.
</Note>

## Harga

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

## Praktik terbaik dan pertimbangan untuk pemikiran yang diperluas

### Bekerja dengan anggaran pemikiran

- **Optimasi anggaran:** Anggaran minimum adalah 1.024 token. Kami menyarankan untuk memulai dengan minimum dan meningkatkan anggaran pemikiran secara bertahap untuk menemukan rentang optimal untuk kasus penggunaan Anda. Jumlah token yang lebih tinggi memungkinkan penalaran yang lebih komprehensif tetapi dengan hasil yang semakin berkurang tergantung pada tugas. Meningkatkan anggaran dapat meningkatkan kualitas respons dengan mengorbankan peningkatan latensi. Untuk tugas-tugas penting, uji pengaturan yang berbeda untuk menemukan keseimbangan optimal. Perhatikan bahwa anggaran pemikiran adalah target daripada batas ketat—penggunaan token aktual dapat bervariasi berdasarkan tugas.
- **Titik awal:** Mulai dengan anggaran pemikiran yang lebih besar (16k+ token) untuk tugas-tugas kompleks dan sesuaikan berdasarkan kebutuhan Anda.
- **Anggaran besar:** Untuk anggaran pemikiran di atas 32k, kami merekomendasikan menggunakan [pemrosesan batch](/docs/id/build-with-claude/batch-processing) untuk menghindari masalah jaringan. Permintaan yang mendorong model untuk berpikir di atas 32k token menyebabkan permintaan yang berjalan lama yang mungkin mengalami batas waktu sistem dan batas koneksi terbuka.
- **Pelacakan penggunaan token:** Pantau penggunaan token pemikiran untuk mengoptimalkan biaya dan kinerja.

### Pertimbangan kinerja

- **Waktu respons:** Bersiaplah untuk waktu respons yang berpotensi lebih lama karena pemrosesan tambahan yang diperlukan untuk proses penalaran. Faktor dalam bahwa menghasilkan blok pemikiran dapat meningkatkan waktu respons keseluruhan.
- **Persyaratan streaming:** SDK memerlukan streaming ketika `max_tokens` lebih besar dari 21.333 untuk menghindari batas waktu HTTP pada permintaan yang berjalan lama. Ini adalah validasi sisi klien, bukan pembatasan API. Jika Anda tidak perlu memproses acara secara bertahap, gunakan `.stream()` dengan `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) untuk mendapatkan objek `Message` lengkap tanpa menangani acara individual — lihat [Streaming Messages](/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detail. Saat streaming, bersiaplah untuk menangani blok konten pemikiran dan teks saat mereka tiba.

### Kompatibilitas fitur

- Pemikiran tidak kompatibel dengan modifikasi `temperature` atau `top_k` serta [penggunaan alat yang dipaksa](/docs/id/agents-and-tools/tool-use/implement-tool-use#forcing-tool-use).
- Ketika pemikiran diaktifkan, Anda dapat mengatur `top_p` ke nilai antara 1 dan 0,95.
- Anda tidak dapat mengisi respons sebelumnya ketika pemikiran diaktifkan.
- Perubahan pada anggaran pemikiran membatalkan awalan prompt yang di-cache yang mencakup pesan. Namun, prompt sistem yang di-cache dan definisi alat akan terus berfungsi ketika parameter pemikiran berubah.

### Panduan penggunaan

- **Pemilihan tugas:** Gunakan pemikiran yang diperluas untuk tugas-tugas yang sangat kompleks yang mendapat manfaat dari penalaran langkah demi langkah seperti matematika, pengkodean, dan analisis.
- **Penanganan konteks:** Anda tidak perlu menghapus blok pemikiran sebelumnya sendiri. API Claude secara otomatis mengabaikan blok pemikiran dari putaran sebelumnya dan mereka tidak disertakan saat menghitung penggunaan konteks.
- **Rekayasa prompt:** Tinjau [tips prompt pemikiran yang diperluas](/docs/id/build-with-claude/prompt-engineering/extended-thinking-tips) kami jika Anda ingin memaksimalkan kemampuan pemikiran Claude.

## Langkah berikutnya

<CardGroup>
  <Card title="Coba buku masak pemikiran yang diperluas" icon="book" href="https://platform.claude.com/cookbook/extended-thinking-extended-thinking">
    Jelajahi contoh praktis pemikiran dalam buku masak kami.
  </Card>
  <Card title="Tips prompt pemikiran yang diperluas" icon="code" href="/docs/id/build-with-claude/prompt-engineering/extended-thinking-tips">
    Pelajari praktik terbaik rekayasa prompt untuk pemikiran yang diperluas.
  </Card>
</CardGroup>