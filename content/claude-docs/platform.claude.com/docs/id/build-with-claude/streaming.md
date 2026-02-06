---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/streaming
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: c7e90d27cfa693e30bc09cacb71e911300c62d05179cbd9b439345dc717ddc13
---

# Streaming Pesan

Pelajari cara melakukan streaming respons pesan secara inkremental menggunakan server-sent events (SSE).

---

Saat membuat Pesan, Anda dapat mengatur `"stream": true` untuk melakukan streaming respons secara inkremental menggunakan [server-sent events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents) (SSE).

## Streaming dengan SDK

SDK [Python](https://github.com/anthropics/anthropic-sdk-python) dan [TypeScript](https://github.com/anthropics/anthropic-sdk-typescript) kami menawarkan berbagai cara untuk melakukan streaming. SDK Python memungkinkan streaming sinkron dan asinkron. Lihat dokumentasi di setiap SDK untuk detail lebih lanjut.

<CodeGroup>
    ```python Python
    import anthropic

    client = anthropic.Anthropic()

    with client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
        model="claude-opus-4-6",
    ) as stream:
      for text in stream.text_stream:
          print(text, end="", flush=True)
    ```

    ```typescript TypeScript
    import Anthropic from '@anthropic-ai/sdk';

    const client = new Anthropic();

    await client.messages.stream({
        messages: [{role: 'user', content: "Hello"}],
        model: 'claude-opus-4-6',
        max_tokens: 1024,
    }).on('text', (text) => {
        console.log(text);
    });
    ```
</CodeGroup>

## Dapatkan pesan final tanpa menangani acara

Jika Anda tidak perlu memproses teks saat tiba, SDK menyediakan cara untuk menggunakan streaming di balik layar sambil mengembalikan objek `Message` lengkap — identik dengan apa yang dikembalikan oleh `.create()`. Ini sangat berguna untuk permintaan dengan nilai `max_tokens` besar, di mana SDK memerlukan streaming untuk menghindari timeout HTTP.

<CodeGroup>
    ```python Python
    import anthropic

    client = anthropic.Anthropic()

    with client.messages.stream(
        max_tokens=128000,
        messages=[{"role": "user", "content": "Write a detailed analysis..."}],
        model="claude-opus-4-6",
    ) as stream:
        message = stream.get_final_message()

    print(message.content[0].text)
    ```

    ```typescript TypeScript
    import Anthropic from '@anthropic-ai/sdk';

    const client = new Anthropic();

    const stream = client.messages.stream({
        max_tokens: 128000,
        messages: [{role: 'user', content: 'Write a detailed analysis...'}],
        model: 'claude-opus-4-6',
    });

    const message = await stream.finalMessage();
    console.log(message.content[0].text);
    ```
</CodeGroup>

Panggilan `.stream()` menjaga koneksi HTTP tetap aktif dengan server-sent events, kemudian `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) mengumpulkan semua acara dan mengembalikan objek `Message` lengkap. Tidak ada kode penanganan acara yang diperlukan.

## Jenis acara

Setiap server-sent event mencakup jenis acara bernama dan data JSON terkait. Setiap acara akan menggunakan nama acara SSE (misalnya `event: message_stop`), dan menyertakan `type` acara yang cocok dalam datanya.

Setiap aliran menggunakan alur acara berikut:

1. `message_start`: berisi objek `Message` dengan `content` kosong.
2. Serangkaian blok konten, masing-masing memiliki acara `content_block_start`, satu atau lebih acara `content_block_delta`, dan acara `content_block_stop`. Setiap blok konten akan memiliki `index` yang sesuai dengan indeksnya dalam array `content` Pesan final.
3. Satu atau lebih acara `message_delta`, menunjukkan perubahan tingkat atas pada objek `Message` final.
4. Acara `message_stop` final.

  <Warning>
  Hitungan token yang ditampilkan di bidang `usage` acara `message_delta` adalah *kumulatif*.
  </Warning>

### Acara ping

Aliran acara juga dapat mencakup sejumlah acara `ping`.

### Acara kesalahan

Kami mungkin sesekali mengirim [kesalahan](/docs/id/api/errors) dalam aliran acara. Misalnya, selama periode penggunaan tinggi, Anda mungkin menerima `overloaded_error`, yang biasanya sesuai dengan HTTP 529 dalam konteks non-streaming:

```json Contoh kesalahan
event: error
data: {"type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}}
```

### Acara lainnya

Sesuai dengan [kebijakan versioning](/docs/id/api/versioning) kami, kami dapat menambahkan jenis acara baru, dan kode Anda harus menangani jenis acara yang tidak dikenal dengan baik.

## Jenis delta blok konten

Setiap acara `content_block_delta` berisi `delta` dari jenis yang memperbarui blok `content` pada `index` tertentu.

### Delta teks

Delta blok konten `text` terlihat seperti:
```json Delta teks
event: content_block_delta
data: {"type": "content_block_delta","index": 0,"delta": {"type": "text_delta", "text": "ello frien"}}
```

### Delta JSON input

Delta untuk blok konten `tool_use` sesuai dengan pembaruan untuk bidang `input` blok. Untuk mendukung granularitas maksimal, delta adalah *string JSON parsial*, sedangkan `tool_use.input` final selalu merupakan *objek*.

Anda dapat mengumpulkan delta string dan mengurai JSON setelah menerima acara `content_block_stop`, dengan menggunakan perpustakaan seperti [Pydantic](https://docs.pydantic.dev/latest/concepts/json/#partial-json-parsing) untuk melakukan parsing JSON parsial, atau dengan menggunakan [SDK](/docs/id/api/client-sdks) kami, yang menyediakan pembantu untuk mengakses nilai inkremental yang diurai.

Delta blok konten `tool_use` terlihat seperti:
```json Delta JSON input
event: content_block_delta
data: {"type": "content_block_delta","index": 1,"delta": {"type": "input_json_delta","partial_json": "{\"location\": \"San Fra"}}
```
Catatan: Model kami saat ini hanya mendukung pemancaraan satu properti kunci dan nilai lengkap dari `input` pada satu waktu. Dengan demikian, saat menggunakan alat, mungkin ada penundaan antara acara streaming saat model sedang bekerja. Setelah kunci dan nilai `input` terakumulasi, kami memancarkannya sebagai beberapa acara `content_block_delta` dengan json parsial yang dipotong sehingga format dapat secara otomatis mendukung granularitas lebih halus di model masa depan.

### Delta pemikiran

Saat menggunakan [extended thinking](/docs/id/build-with-claude/extended-thinking#streaming-thinking) dengan streaming diaktifkan, Anda akan menerima konten pemikiran melalui acara `thinking_delta`. Delta ini sesuai dengan bidang `thinking` dari blok konten `thinking`.

Untuk konten pemikiran, acara `signature_delta` khusus dikirim tepat sebelum acara `content_block_stop`. Tanda tangan ini digunakan untuk memverifikasi integritas blok pemikiran.

Delta pemikiran tipikal terlihat seperti:
```json Delta pemikiran
event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}
```

Delta tanda tangan terlihat seperti:
```json Delta tanda tangan
event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3hGgxBdjrkzLoky3dl1pkiMOYds..."}}
```

## Respons aliran HTTP lengkap

Kami sangat merekomendasikan agar Anda menggunakan [SDK klien](/docs/id/api/client-sdks) kami saat menggunakan mode streaming. Namun, jika Anda membangun integrasi API langsung, Anda perlu menangani acara ini sendiri.

Respons aliran terdiri dari:
1. Acara `message_start`
2. Berpotensi beberapa blok konten, masing-masing berisi:
    - Acara `content_block_start`
    - Berpotensi beberapa acara `content_block_delta`
    - Acara `content_block_stop`
3. Acara `message_delta`
4. Acara `message_stop`

Mungkin ada acara `ping` yang tersebar di seluruh respons juga. Lihat [Jenis acara](#event-types) untuk detail lebih lanjut tentang formatnya.

### Permintaan streaming dasar

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --data \
'{
  "model": "claude-opus-4-6",
  "messages": [{"role": "user", "content": "Hello"}],
  "max_tokens": 256,
  "stream": true
}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=256,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
</CodeGroup>

```json Respons
event: message_start
data: {"type": "message_start", "message": {"id": "msg_1nZdL29xx5MUA1yADyHTEsnR8uuvGzszyY", "type": "message", "role": "assistant", "content": [], "model": "claude-opus-4-6", "stop_reason": null, "stop_sequence": null, "usage": {"input_tokens": 25, "output_tokens": 1}}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hello"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "!"}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence":null}, "usage": {"output_tokens": 15}}

event: message_stop
data: {"type": "message_stop"}

```

### Permintaan streaming dengan penggunaan alat

<Tip>
Penggunaan alat mendukung [streaming berbutir halus](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) untuk nilai parameter. Aktifkan per alat dengan `eager_input_streaming`.
</Tip>

Dalam permintaan ini, kami meminta Claude untuk menggunakan alat untuk memberi tahu kami cuaca.

<CodeGroup>
```bash Shell
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-6",
      "max_tokens": 1024,
      "tools": [
        {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              }
            },
            "required": ["location"]
          }
        }
      ],
      "tool_choice": {"type": "any"},
      "messages": [
        {
          "role": "user",
          "content": "What is the weather like in San Francisco?"
        }
      ],
      "stream": true
    }'
```

```python Python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }
]

with client.messages.stream(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "any"},
    messages=[
        {
            "role": "user",
            "content": "What is the weather like in San Francisco?"
        }
    ],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
</CodeGroup>

```json Respons
event: message_start
data: {"type":"message_start","message":{"id":"msg_014p7gG3wDgGV9EUtLvnow3U","type":"message","role":"assistant","model":"claude-opus-4-6","stop_sequence":null,"usage":{"input_tokens":472,"output_tokens":2},"content":[],"stop_reason":null}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Okay"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":","}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" let"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"'s"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" check"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" the"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" weather"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" for"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" San"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" Francisco"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":","}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" CA"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":":"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"tool_use","id":"toolu_01T1x1fJ34qAmk2tNTrN7Up6","name":"get_weather","input":{}}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"{\"location\":"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" \"San"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" Francisc"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"o,"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" CA\""}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":","}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" \"unit\": \"fah"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"renheit\"}"}}

event: content_block_stop
data: {"type":"content_block_stop","index":1}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"tool_use","stop_sequence":null},"usage":{"output_tokens":89}}

event: message_stop
data: {"type":"message_stop"}
```

### Permintaan streaming dengan extended thinking

Dalam permintaan ini, kami mengaktifkan extended thinking dengan streaming untuk melihat penalaran langkah demi langkah Claude.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
    "max_tokens": 20000,
    "stream": true,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 16000
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
    model="claude-opus-4-6",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 16000
    },
    messages=[
        {
            "role": "user",
            "content": "What is the greatest common divisor of 1071 and 462?"
        }
    ],
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
```
</CodeGroup>

```json Respons
event: message_start
data: {"type": "message_start", "message": {"id": "msg_01...", "type": "message", "role": "assistant", "content": [], "model": "claude-opus-4-6", "stop_reason": null, "stop_sequence": null}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n462 = 3 × 147 + 21"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n147 = 7 × 21 + 0"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\nThe remainder is 0, so GCD(1071, 462) = 21."}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3hGgxBdjrkzLoky3dl1pkiMOYds..."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "text", "text": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "text_delta", "text": "The greatest common divisor of 1071 and 462 is **21**."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 1}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}}

event: message_stop
data: {"type": "message_stop"}
```

### Permintaan streaming dengan penggunaan alat pencarian web

Dalam permintaan ini, kami meminta Claude untuk mencari web untuk informasi cuaca terkini.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "stream": true,
    "tools": [
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "What is the weather like in New York City today?"
        }
    ]
}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "What is the weather like in New York City today?"
        }
    ],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
</CodeGroup>

```json Respons
event: message_start
data: {"type":"message_start","message":{"id":"msg_01G...","type":"message","role":"assistant","model":"claude-opus-4-6","content":[],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":2679,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":3}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"I'll check"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" the current weather in New York City for you"}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"."}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"server_tool_use","id":"srvtoolu_014hJH82Qum7Td6UV8gDXThB","name":"web_search","input":{}}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"{\"query"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"\":"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" \"weather"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" NY"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"C to"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"day\"}"}}

event: content_block_stop
data: {"type":"content_block_stop","index":1 }

event: content_block_start
data: {"type":"content_block_start","index":2,"content_block":{"type":"web_search_tool_result","tool_use_id":"srvtoolu_014hJH82Qum7Td6UV8gDXThB","content":[{"type":"web_search_result","title":"Weather in New York City in May 2025 (New York) - detailed Weather Forecast for a month","url":"https://world-weather.info/forecast/usa/new_york/may-2025/","encrypted_content":"Ev0DCioIAxgCIiQ3NmU4ZmI4OC1k...","page_age":null},...]}}

event: content_block_stop
data: {"type":"content_block_stop","index":2}

event: content_block_start
data: {"type":"content_block_start","index":3,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":"Here's the current weather information for New York"}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":" City:\n\n# Weather"}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":" in New York City"}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":"\n\n"}}

...

event: content_block_stop
data: {"type":"content_block_stop","index":17}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},"usage":{"input_tokens":10682,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":510,"server_tool_use":{"web_search_requests":1}}}

event: message_stop
data: {"type":"message_stop"}
```

## Pemulihan kesalahan

Ketika permintaan streaming terputus karena masalah jaringan, timeout, atau kesalahan lainnya, Anda dapat memulihkan dengan melanjutkan dari tempat aliran terputus. Pendekatan ini menghemat Anda dari memproses ulang seluruh respons.

Strategi pemulihan dasar melibatkan:

1. **Tangkap respons parsial**: Simpan semua konten yang berhasil diterima sebelum kesalahan terjadi
2. **Buat permintaan kelanjutan**: Buat permintaan API baru yang mencakup respons asisten parsial sebagai awal dari pesan asisten baru
3. **Lanjutkan streaming**: Terus menerima sisa respons dari tempat terputus

### Praktik terbaik pemulihan kesalahan

1. **Gunakan fitur SDK**: Manfaatkan kemampuan akumulasi pesan dan penanganan kesalahan bawaan SDK
2. **Tangani jenis konten**: Ketahui bahwa pesan dapat berisi beberapa blok konten (`text`, `tool_use`, `thinking`). Blok penggunaan alat dan extended thinking tidak dapat dipulihkan sebagian. Anda dapat melanjutkan streaming dari blok teks paling terbaru.