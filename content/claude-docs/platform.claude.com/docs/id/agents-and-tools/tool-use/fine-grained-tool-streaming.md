---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: f2a6c2519af388f249922f759ae9c6a203de1a22cc566126b677d5722938fed0
---

# Streaming alat butir halus

Streaming input alat karakter demi karakter untuk aplikasi yang sensitif terhadap latensi.

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Streaming alat butir halus tersedia secara umum di semua model dan semua platform. Ini memungkinkan [streaming](/docs/id/build-with-claude/streaming) nilai parameter penggunaan alat tanpa buffering atau validasi JSON, mengurangi latensi untuk mulai menerima parameter besar.

<Warning>
Saat menggunakan streaming alat butir halus, Anda mungkin menerima input JSON yang tidak valid atau sebagian. Pastikan untuk mempertimbangkan kasus tepi ini dalam kode Anda.
</Warning>

## Cara menggunakan streaming alat butir halus
Streaming alat butir halus tersedia di semua model dan semua platform (Claude API, Amazon Bedrock, Google Vertex AI, dan Microsoft Foundry). Untuk menggunakannya, atur `eager_input_streaming` ke `true` pada alat yang ditentukan pengguna mana pun di mana Anda ingin streaming butir halus diaktifkan, dan aktifkan streaming pada permintaan Anda.

Berikut adalah contoh cara menggunakan streaming alat butir halus dengan API:

<CodeGroup>

  ```bash Shell
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-7",
      "max_tokens": 65536,
      "tools": [
        {
          "name": "make_file",
          "description": "Write text to a file",
          "eager_input_streaming": true,
          "input_schema": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "description": "The filename to write text to"
              },
              "lines_of_text": {
                "type": "array",
                "description": "An array of lines of text to write to the file"
              }
            },
            "required": ["filename", "lines_of_text"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Can you write a long poem and make a file called poem.txt?"
        }
      ],
      "stream": true
    }'
  ```

  ```bash CLI
  ant messages create --stream \
    --transform usage <<'YAML'
  model: claude-opus-4-7
  max_tokens: 65536
  tools:
    - name: make_file
      description: Write text to a file
      eager_input_streaming: true
      input_schema:
        type: object
        properties:
          filename:
            type: string
            description: The filename to write text to
          lines_of_text:
            type: array
            description: An array of lines of text to write to the file
        required:
          - filename
          - lines_of_text
  messages:
    - role: user
      content: Can you write a long poem and make a file called poem.txt?
  YAML
  ```

  ```python Python hidelines={1..2}
  import anthropic

  client = anthropic.Anthropic()

  with client.messages.stream(
      max_tokens=65536,
      model="claude-opus-4-7",
      tools=[
          {
              "name": "make_file",
              "description": "Write text to a file",
              "eager_input_streaming": True,
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "filename": {
                          "type": "string",
                          "description": "The filename to write text to",
                      },
                      "lines_of_text": {
                          "type": "array",
                          "description": "An array of lines of text to write to the file",
                      },
                  },
                  "required": ["filename", "lines_of_text"],
              },
          }
      ],
      messages=[
          {
              "role": "user",
              "content": "Can you write a long poem and make a file called poem.txt?",
          }
      ],
  ) as stream:
      for event in stream:
          pass
      final_message = stream.get_final_message()

  print(final_message.usage)
  ```

  ```typescript TypeScript hidelines={1..2}
  import Anthropic from "@anthropic-ai/sdk";

  const anthropic = new Anthropic();

  const stream = anthropic.messages.stream({
    model: "claude-opus-4-7",
    max_tokens: 65536,
    tools: [
      {
        name: "make_file",
        description: "Write text to a file",
        eager_input_streaming: true,
        input_schema: {
          type: "object",
          properties: {
            filename: {
              type: "string",
              description: "The filename to write text to"
            },
            lines_of_text: {
              type: "array",
              description: "An array of lines of text to write to the file"
            }
          },
          required: ["filename", "lines_of_text"]
        }
      }
    ],
    messages: [
      {
        role: "user",
        content: "Can you write a long poem and make a file called poem.txt?"
      }
    ]
  });

  const message = await stream.finalMessage();
  console.log(message.usage);
  ```
</CodeGroup>

Dalam contoh ini, streaming alat butir halus memungkinkan Claude untuk streaming baris puisi panjang ke dalam panggilan alat `make_file` tanpa buffering untuk memvalidasi apakah parameter `lines_of_text` adalah JSON yang valid. Ini berarti Anda dapat melihat parameter stream saat tiba, tanpa harus menunggu seluruh parameter untuk buffer dan validasi.

<Note>
Dengan streaming alat butir halus, chunk penggunaan alat mulai streaming lebih cepat, dan sering kali lebih panjang dan berisi lebih sedikit jeda kata. Ini disebabkan oleh perbedaan dalam perilaku chunking.

Contoh:

Tanpa streaming butir halus (penundaan 15 detik):
```text
Chunk 1: '{"'
Chunk 2: 'query": "Ty'
Chunk 3: 'peScri'
Chunk 4: 'pt 5.0 5.1 '
Chunk 5: '5.2 5'
Chunk 6: '.3'
Chunk 8: ' new f'
Chunk 9: 'eatur'
...
```

Dengan streaming butir halus (penundaan 3 detik):
```text
Chunk 1: '{"query": "TypeScript 5.0 5.1 5.2 5.3'
Chunk 2: ' new features comparison'
```
</Note>

<Warning>
Karena streaming butir halus mengirim parameter tanpa buffering atau validasi JSON, tidak ada jaminan bahwa stream yang dihasilkan akan selesai dalam string JSON yang valid.
Khususnya, jika [alasan berhenti](/docs/id/build-with-claude/handling-stop-reasons) `max_tokens` tercapai, stream mungkin berakhir di tengah parameter dan mungkin tidak lengkap. Anda umumnya harus menulis dukungan khusus untuk menangani saat `max_tokens` tercapai.
</Warning>

## Mengakumulasi delta input alat

Ketika blok konten `tool_use` streaming, event `content_block_start` awal berisi `input: {}` (objek kosong). Ini adalah placeholder. Input aktual tiba sebagai serangkaian event `input_json_delta`, masing-masing membawa fragmen string `partial_json`. Kode Anda harus menggabungkan fragmen ini dan mengurai hasilnya setelah blok ditutup.

Kontrak akumulasi:

1. Pada `content_block_start` dengan `type: "tool_use"`, inisialisasi string kosong: `input_json = ""`
2. Untuk setiap `content_block_delta` dengan `type: "input_json_delta"`, tambahkan: `input_json += event.delta.partial_json`
3. Pada `content_block_stop`, parsing string yang terakumulasi: `json.loads(input_json)`

Ketidakcocokan tipe antara `input: {}` awal (objek) dan `partial_json` (string) adalah dengan desain. Objek kosong menandai slot dalam array konten; string delta membangun nilai nyata.

<CodeGroup>

```python Python
import json
import anthropic

client = anthropic.Anthropic()

tool_inputs = {}  # index -> accumulated JSON string

with client.messages.stream(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "eager_input_streaming": True,
            "input_schema": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        }
    ],
    messages=[{"role": "user", "content": "Weather in Paris?"}],
) as stream:
    for event in stream:
        if (
            event.type == "content_block_start"
            and event.content_block.type == "tool_use"
        ):
            tool_inputs[event.index] = ""
        elif (
            event.type == "content_block_delta"
            and event.delta.type == "input_json_delta"
        ):
            tool_inputs[event.index] += event.delta.partial_json
        elif event.type == "content_block_stop" and event.index in tool_inputs:
            parsed = json.loads(tool_inputs[event.index])
            print(f"Tool input: {parsed}")
```

```typescript TypeScript hidelines={1..4}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const toolInputs: Record<number, string> = {};

const stream = anthropic.messages.stream({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [
    {
      name: "get_weather",
      description: "Get current weather for a city",
      eager_input_streaming: true,
      input_schema: {
        type: "object",
        properties: { city: { type: "string" } },
        required: ["city"]
      }
    }
  ],
  messages: [{ role: "user", content: "Weather in Paris?" }]
});

for await (const event of stream) {
  if (event.type === "content_block_start" && event.content_block.type === "tool_use") {
    toolInputs[event.index] = "";
  } else if (event.type === "content_block_delta" && event.delta.type === "input_json_delta") {
    toolInputs[event.index] += event.delta.partial_json;
  } else if (event.type === "content_block_stop" && event.index in toolInputs) {
    const parsed = JSON.parse(toolInputs[event.index]);
    console.log("Tool input:", parsed);
  }
}
```

</CodeGroup>

<Tip>
SDK Python dan TypeScript menyediakan helper stream tingkat lebih tinggi (`stream.get_final_message()`, `stream.finalMessage()`) yang melakukan akumulasi ini untuk Anda. Gunakan pola manual di atas hanya ketika Anda perlu bereaksi terhadap input sebagian sebelum blok ditutup, seperti merender indikator kemajuan atau memulai permintaan hilir lebih awal.
</Tip>

## Menangani JSON tidak valid dalam respons alat

Saat menggunakan streaming alat butir halus, Anda mungkin menerima JSON yang tidak valid atau tidak lengkap dari model. Jika Anda perlu melewatkan JSON yang tidak valid ini kembali ke model dalam blok respons kesalahan, Anda dapat membungkusnya dalam objek JSON untuk memastikan penanganan yang tepat (dengan kunci yang masuk akal). Sebagai contoh:

```json
{
  "INVALID_JSON": "<your invalid json string>"
}
```

Pendekatan ini membantu model memahami bahwa konten adalah JSON yang tidak valid sambil menyimpan data yang salah bentuk asli untuk tujuan debugging.

<Note>
Saat membungkus JSON yang tidak valid, pastikan untuk meloloskan dengan benar tanda kutip atau karakter khusus dalam string JSON yang tidak valid untuk mempertahankan struktur JSON yang valid dalam objek pembungkus.
</Note>

## Langkah berikutnya

<CardGroup cols={3}>
  <Card title="Streaming messages" href="/docs/id/build-with-claude/streaming">
    Referensi lengkap untuk event yang dikirim server dan tipe event stream.
  </Card>
  <Card title="Handle tool calls" href="/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Jalankan alat dan kembalikan hasil dalam format pesan yang diperlukan.
  </Card>
  <Card title="Tool reference" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori lengkap alat skema Anthropic dan string versi mereka.
  </Card>
</CardGroup>