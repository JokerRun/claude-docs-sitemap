---
source: platform
url: https://platform.claude.com/docs/id/claude_api_primer
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: ad9a7a2651529b98a4152437f538ec6eb1dc02f37cdfed578cf2c5774576602a
---

---
title: Panduan dasar penggunaan API untuk Claude
url: https://platform.claude.com/docs/id/claude_api_primer
description: Panduan ini dirancang untuk memberikan Claude dasar-dasar penggunaan Claude API. Panduan ini memberikan penjelasan dan contoh ID model/Messages API dasar, penggunaan alat, streaming, thinking, dan tidak ada yang lain.
---

# Pengantar penggunaan API untuk Claude

> Panduan ini dirancang untuk memberikan Claude dasar-dasar penggunaan Claude API. Panduan ini memberikan penjelasan dan contoh ID model/Messages API dasar, penggunaan alat, streaming, thinking, dan tidak ada yang lain.

## Model

```text wrap
For complex agentic coding and enterprise work: Claude Opus 5: claude-opus-5
Previous Opus model: Claude Opus 4.8: claude-opus-4-8
Smart model: Claude Sonnet 5: claude-sonnet-5
For fast, cost-effective tasks: Claude Haiku 4.5: claude-haiku-4-5-20251001
```

## Memanggil API

### Permintaan dan respons dasar

<CodeGroup exclude="shell:cURL, typescript, csharp, go, java, php, ruby">
  ```bash CLI
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --message '{"role": "user", "content": "Hello, Claude"}'
  ```

  ```python Python
  import anthropic

  message = anthropic.Anthropic().messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(message)
  ```
</CodeGroup>

```json Output
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello!"
    }
  ],
  "model": "claude-opus-5",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "output_tokens": 6
  }
}
```

### Beberapa giliran percakapan

Messages API bersifat stateless, yang berarti Anda selalu mengirimkan riwayat percakapan lengkap ke API. Anda dapat menggunakan pola ini untuk membangun percakapan dari waktu ke waktu. Giliran percakapan sebelumnya tidak harus benar-benar berasal dari Claude. Anda dapat menggunakan pesan `assistant` sintetis.

<CodeGroup exclude="shell:cURL, typescript, csharp, go, java, php, ruby">
  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  messages:
    - role: user
      content: Hello, Claude
    - role: assistant
      content: Hello!
    - role: user
      content: Can you describe LLMs to me?
  YAML
  ```

  ```python Python
  import anthropic

  message = anthropic.Anthropic().messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          {"role": "user", "content": "Hello, Claude"},
          {"role": "assistant", "content": "Hello!"},
          {"role": "user", "content": "Can you describe LLMs to me?"},
      ],
  )
  print(message)
  ```
</CodeGroup>

### Mengisi awal respons Claude

Anda dapat mengisi awal (prefill) sebagian respons Claude pada posisi terakhir dari daftar pesan input. Gunakan teknik ini untuk membentuk respons Claude. Contoh berikut menggunakan `"max_tokens": 1` untuk mendapatkan satu jawaban pilihan ganda dari Claude.

<Note>
  Model Claude 4.6 dan yang lebih baru serta Claude Mythos Preview tidak mendukung prefill pesan assistant; permintaan ke model-model tersebut harus diakhiri dengan pesan user. Contoh di bawah ini menggunakan model yang mendukung prefill.
</Note>

<CodeGroup exclude="shell:cURL, typescript, csharp, go, java, php, ruby">
  ```bash CLI
  ant messages create <<'YAML'
  model: claude-sonnet-4-5
  max_tokens: 1
  messages:
    - role: user
      content: "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae"
    - role: assistant
      content: "The answer is ("
  YAML
  ```

  ```python Python
  import anthropic

  message = anthropic.Anthropic().messages.create(
      model="claude-sonnet-4-5",
      max_tokens=1,
      messages=[
          {
              "role": "user",
              "content": "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae",
          },
          {"role": "assistant", "content": "The answer is ("},
      ],
  )
  print(message.content[0].text)
  ```
</CodeGroup>

### Vision

Claude dapat membaca teks maupun gambar dalam permintaan. Tipe sumber `base64` dan `url` keduanya didukung untuk gambar, beserta tipe media `image/jpeg`, `image/png`, `image/gif`, dan `image/webp`.

<CodeGroup exclude="shell:cURL, typescript, csharp, go, java, php, ruby">
  ```bash CLI
  IMAGE_URL="https://platform.claude.com/docs/images/vision-example.jpg"

  # Opsi 1: Gambar berenkode base64 (prefiks @ otomatis mengenkode file biner sebagai base64)
  curl -sSo vision-example.jpg "$IMAGE_URL"

  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: image
          source:
            type: base64
            media_type: image/jpeg
            data: "@./vision-example.jpg"
        - type: text
          text: What is in the above image?
  YAML

  # Opsi 2: Gambar yang direferensikan melalui URL
  ant messages create <<YAML
  model: claude-opus-5
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: image
          source:
            type: url
            url: $IMAGE_URL
        - type: text
          text: What is in the above image?
  YAML
  ```

  ```python Python
  import anthropic
  import base64
  import httpx2

  # Opsi 1: Gambar yang dienkode Base64
  image_url = "https://platform.claude.com/docs/images/vision-example.jpg"
  image_media_type = "image/jpeg"
  image_data = base64.standard_b64encode(httpx2.get(image_url).content).decode("utf-8")

  message = anthropic.Anthropic().messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "image",
                      "source": {
                          "type": "base64",
                          "media_type": image_media_type,
                          "data": image_data,
                      },
                  },
                  {"type": "text", "text": "What is in the above image?"},
              ],
          }
      ],
  )
  print(next(block.text for block in message.content if block.type == "text"))

  # Opsi 2: Gambar yang dirujuk melalui URL
  message_from_url = anthropic.Anthropic().messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "image",
                      "source": {
                          "type": "url",
                          "url": "https://platform.claude.com/docs/images/vision-example.jpg",
                      },
                  },
                  {"type": "text", "text": "What is in the above image?"},
              ],
          }
      ],
  )
  print(next(block.text for block in message_from_url.content if block.type == "text"))
  ```
</CodeGroup>

## Thinking

Thinking terkadang dapat membantu Claude dalam tugas yang sangat sulit. Mekanisme saat ini adalah [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) (`thinking: {"type": "adaptive"}`): Claude memutuskan kapan dan seberapa banyak berpikir, dan Anda mengarahkan kedalaman pemikiran dengan parameter [`effort`](https://platform.claude.com/docs/id/build-with-claude/effort) alih-alih anggaran token. Adaptive thinking didukung pada model Claude 4.6 dan yang lebih baru serta Claude Mythos Preview. Pada model Claude 5 dan Claude Mythos Preview, thinking aktif secara default ketika parameter `thinking` dihilangkan.

Temperature harus diatur ke 1 (atau dibiarkan tidak diatur) setiap kali thinking diaktifkan, pada semua model. Pada model Claude 4.7 dan yang lebih baru serta Claude Mythos Preview, `temperature` sudah deprecated dan hanya nilai default-nya yang diterima, bahkan ketika thinking nonaktif.

Thinking didukung pada model-model berikut:

* Claude Opus 5 (claude-opus-5, hanya adaptive thinking, aktif secara default)
* Claude Sonnet 5 (`claude-sonnet-5`, hanya adaptive thinking, aktif secara default)
* Claude Opus 4.8 (claude-opus-4-8, hanya adaptive thinking)
* Claude Opus 4.7 (`claude-opus-4-7`, hanya adaptive thinking)
* Claude Opus 4.6 (`claude-opus-4-6`, adaptive thinking atau manual thinking lama)
* Claude Sonnet 4.6 (`claude-sonnet-4-6`, adaptive thinking atau manual thinking lama)
* Claude Opus 4.5 (`claude-opus-4-5-20251101`, hanya manual thinking lama)
* Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`, hanya manual thinking lama)
* Claude Haiku 4.5 (`claude-haiku-4-5-20251001`, hanya manual thinking lama)

<Note>
  Pada model Claude 4.7 dan yang lebih baru, pemikiran diperpanjang manual (`type: enabled` dengan nilai `budget_tokens`) tidak didukung dan mengembalikan error 400. Gunakan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (`type: adaptive`) sebagai gantinya.
</Note>

### Cara kerja thinking

Ketika thinking aktif, Claude membuat blok konten `thinking` tempat ia mengeluarkan penalaran internalnya. Respons API menyertakan blok konten `thinking`, diikuti oleh blok konten `text`.

<CodeGroup exclude="shell:cURL, typescript, csharp, go, java, php, ruby">
  ```bash CLI
  ant messages create --transform content --format yaml <<'YAML'
  model: claude-opus-5
  max_tokens: 16000
  thinking:
    type: adaptive
    display: summarized
  messages:
    - role: user
      content: Are there an infinite number of prime numbers such that n mod 4 == 3?
  YAML
  ```

  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      thinking={"type": "adaptive", "display": "summarized"},
      messages=[
          {
              "role": "user",
              "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?",
          }
      ],
  )

  # Respons berisi blok pemikiran yang diringkas dan blok teks
  for block in response.content:
      if block.type == "thinking":
          print(f"\nThinking summary: {block.thinking}")
      elif block.type == "text":
          print(f"\nResponse: {block.text}")
  ```
</CodeGroup>

"Manual extended thinking" (pemikiran diperpanjang manual) (`thinking: {"type": "enabled", "budget_tokens": N}`) adalah mekanisme lama. Mekanisme ini hanya berfungsi pada model Claude 4 hingga 4.6 yang mendukung thinking; model Claude 4.7 dan yang lebih baru menolak `type: enabled` dengan error 400 dan menggunakan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) sebagai gantinya. Dengan pemikiran diperpanjang manual, `budget_tokens` menetapkan jumlah maksimum token yang boleh digunakan Claude untuk proses penalaran internalnya; batas ini berlaku untuk token thinking penuh, bukan untuk output yang diringkas. Kecuali Anda menggunakan [interleaved thinking](https://platform.claude.com/docs/id/claude_api_primer#interleaved-thinking), `budget_tokens` harus lebih kecil dari `max_tokens` agar Claude memiliki ruang untuk menulis responsnya setelah thinking selesai.

## Thinking dengan penggunaan alat

Thinking dapat digunakan bersama "tool use" (penggunaan alat), memungkinkan Claude bernalar dalam pemilihan alat dan pemrosesan hasil.

Batasan penting:

1. **Batasan pilihan alat:** Hanya mendukung `tool_choice: {"type": "auto"}` (default) atau `tool_choice: {"type": "none"}`.
2. **Mempertahankan blok thinking:** Selama penggunaan alat, Anda harus mengirimkan kembali blok `thinking` ke API untuk pesan assistant terakhir.

### Mempertahankan blok thinking

<CodeGroup exclude="shell:cURL, typescript, csharp, go, java, php, ruby">
  ```bash CLI
  # Permintaan pertama: tangkap array konten asisten (blok thinking + tool_use,
  # tanda tangan utuh) sebagai JSON ringkas.
  ASSISTANT_CONTENT=$(ant messages create \
    --transform content --format jsonl <<'YAML'
  model: claude-opus-5
  max_tokens: 16000
  thinking:
    type: adaptive
    display: summarized
  tools:
    - name: get_weather
      description: Get the current weather for a location.
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city name.
        required: [location]
  messages:
    - role: user
      content: "What's the weather in Paris?"
  YAML
  )

  TOOL_USE_ID=$(printf '%s' "$ASSISTANT_CONTENT" \
    | jq -r '.[] | select(.type == "tool_use") | .id')

  # Permintaan kedua: kirim kembali blok yang ditangkap tanpa perubahan sebagai pesan
  # asisten. Blok thinking harus menyertai blok tool_use.
  ant messages create <<YAML
  model: claude-opus-5
  max_tokens: 16000
  thinking:
    type: adaptive
    display: summarized
  tools:
    - name: get_weather
      description: Get the current weather for a location.
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city name.
        required: [location]
  messages:
    - role: user
      content: "What's the weather in Paris?"
    - role: assistant
      content: $ASSISTANT_CONTENT
    - role: user
      content:
        - type: tool_result
          tool_use_id: $TOOL_USE_ID
          content: "Current temperature: 72°F"
  YAML
  ```

  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  weather_tool = {
      "name": "get_weather",
      "description": "Get the current weather for a location.",
      "input_schema": {
          "type": "object",
          "properties": {"location": {"type": "string", "description": "The city name."}},
          "required": ["location"],
      },
  }

  weather_data = {"temperature": 72}

  # Permintaan pertama - Claude merespons dengan pemikiran dan permintaan alat
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      thinking={"type": "adaptive", "display": "summarized"},
      tools=[weather_tool],
      messages=[{"role": "user", "content": "What's the weather in Paris?"}],
  )

  # Ekstrak blok thinking dan blok tool use
  thinking_block = next(
      (block for block in response.content if block.type == "thinking"), None
  )
  tool_use_block = next(
      (block for block in response.content if block.type == "tool_use"), None
  )

  # Permintaan kedua - Sertakan blok thinking dan hasil alat
  continuation = client.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      thinking={"type": "adaptive", "display": "summarized"},
      tools=[weather_tool],
      messages=[
          {"role": "user", "content": "What's the weather in Paris?"},
          # Perhatikan bahwa thinking_block juga diteruskan bersama tool_use_block
          {"role": "assistant", "content": [thinking_block, tool_use_block]},
          {
              "role": "user",
              "content": [
                  {
                      "type": "tool_result",
                      "tool_use_id": tool_use_block.id,
                      "content": f"Current temperature: {weather_data['temperature']}°F",
                  }
              ],
          },
      ],
  )

  for block in continuation.content:
      if block.type == "text":
          print(block.text)
  ```
</CodeGroup>

### Interleaved thinking

"Interleaved thinking" (pemikiran berselang-seling) memungkinkan Claude berpikir di antara pemanggilan alat, bernalar tentang hasil alat sebelum memutuskan langkah berikutnya.

<Info>
  Pada model dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (`thinking: {type: "adaptive"}`), interleaved thinking diaktifkan secara otomatis. Tidak diperlukan header beta. Sonnet 4.6 mendukung header beta `interleaved-thinking-2025-05-14` dengan pemikiran diperpanjang manual maupun adaptive thinking.
</Info>

Pada model lama yang menggunakan pemikiran diperpanjang manual (model Claude 4, 4.5, dan Sonnet 4.6), aktifkan interleaved thinking dengan menambahkan header beta `interleaved-thinking-2025-05-14` ke permintaan API Anda:

<CodeGroup exclude="shell:cURL, typescript, csharp, go, java, php, ruby">
  ```bash CLI
  ant beta:messages create --beta interleaved-thinking-2025-05-14 <<'YAML'
  model: claude-sonnet-4-6
  max_tokens: 16000
  thinking:
    type: enabled
    budget_tokens: 10000
  tools:
    - name: calculator
      description: Perform arithmetic calculations.
      input_schema:
        type: object
        properties:
          expression:
            type: string
            description: The math expression to evaluate.
        required:
          - expression
    - name: database_query
      description: Query the product database.
      input_schema:
        type: object
        properties:
          query:
            type: string
            description: The database query.
        required:
          - query
  messages:
    - role: user
      content: "What's the total revenue if we sold 150 units of product A at $50 each?"
  YAML
  ```

  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  calculator_tool = {
      "name": "calculator",
      "description": "Perform arithmetic calculations.",
      "input_schema": {
          "type": "object",
          "properties": {
              "expression": {
                  "type": "string",
                  "description": "The math expression to evaluate.",
              }
          },
          "required": ["expression"],
      },
  }

  database_tool = {
      "name": "database_query",
      "description": "Query the product database.",
      "input_schema": {
          "type": "object",
          "properties": {
              "query": {"type": "string", "description": "The database query."}
          },
          "required": ["query"],
      },
  }

  response = client.beta.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=16000,
      thinking={"type": "enabled", "budget_tokens": 10000},
      tools=[calculator_tool, database_tool],
      messages=[
          {
              "role": "user",
              "content": "What's the total revenue if we sold 150 units of product A at $50 each?",
          }
      ],
      betas=["interleaved-thinking-2025-05-14"],
  )

  for block in response.content:
      if block.type == "thinking":
          print(f"Thinking: {block.thinking}")
      elif block.type == "tool_use":
          print(f"Tool call: {block.name}({block.input})")
      elif block.type == "text":
          print(f"Response: {block.text}")
  ```
</CodeGroup>

Dengan interleaved thinking dan HANYA dengan interleaved thinking (bukan pemikiran diperpanjang manual biasa), `budget_tokens` dapat melebihi parameter `max_tokens`, karena `budget_tokens` dalam kasus ini mewakili total anggaran di seluruh blok thinking dalam satu giliran assistant.

## Penggunaan alat

### Menentukan alat klien

Alat klien ditentukan dalam parameter tingkat atas `tools` pada permintaan API. Setiap definisi alat mencakup:

| Parameter      | Deskripsi                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `name`         | Nama alat. Harus cocok dengan regex `^[a-zA-Z0-9_-]{1,64}$`.                                                            |
| `description`  | Deskripsi teks biasa yang terperinci tentang apa yang dilakukan alat, kapan harus digunakan, dan bagaimana perilakunya. |
| `input_schema` | Objek [JSON Schema](https://json-schema.org/) yang mendefinisikan parameter yang diharapkan untuk alat.                 |

```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
      }
    },
    "required": ["location"]
  }
}
```

### Praktik terbaik untuk definisi alat

**Berikan deskripsi yang sangat terperinci.** Ini adalah faktor yang paling penting dalam kinerja alat. Deskripsi Anda harus menjelaskan setiap detail tentang alat, termasuk:

* Apa yang dilakukan alat
* Kapan harus digunakan (dan kapan tidak)
* Apa arti setiap parameter dan bagaimana pengaruhnya terhadap perilaku alat
* Peringatan atau batasan penting apa pun

**Pertimbangkan penggunaan `input_examples` untuk alat yang kompleks.** Untuk alat dengan objek bersarang, parameter opsional, atau input yang sensitif terhadap format, Anda dapat memberikan contoh konkret menggunakan field `input_examples` (beta). Ini membantu Claude memahami pola input yang diharapkan. Lihat [Memberikan contoh penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples) untuk detailnya.

Contoh deskripsi alat yang baik:

```json
{
  "name": "get_stock_price",
  "description": "Retrieves the current stock price for a given ticker symbol. The ticker symbol must be a valid symbol for a publicly traded company on a major US stock exchange like NYSE or NASDAQ. The tool will return the latest trade price in USD. It should be used when the user asks about the current or most recent price of a specific stock. It will not provide any other information about the stock or company.",
  "input_schema": {
    "type": "object",
    "properties": {
      "ticker": {
        "type": "string",
        "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
      }
    },
    "required": ["ticker"]
  }
}
```

## Mengontrol output Claude

### Memaksa penggunaan alat

Anda dapat memaksa Claude menggunakan alat tertentu dengan menentukan alat tersebut di field `tool_choice`:

```python
tool_choice = {"type": "tool", "name": "get_weather"}
```

Saat bekerja dengan parameter `tool_choice`, ada empat opsi yang mungkin:

* `auto` memungkinkan Claude menentukan apakah akan memanggil alat yang disediakan atau tidak (default).
* `any` memberi tahu Claude bahwa ia harus menggunakan salah satu alat yang disediakan.
* `tool` memaksa Claude untuk selalu menggunakan alat tertentu.
* `none` mencegah Claude menggunakan alat apa pun.

### Output JSON

Alat tidak harus berupa fungsi klien. Anda dapat menggunakan alat kapan pun Anda ingin model mengembalikan output JSON yang mengikuti skema yang disediakan.

### Chain of thought

Saat menggunakan alat, Claude sering menunjukkan "chain of thought" (rantai pemikiran)-nya, yaitu penalaran langkah demi langkah yang digunakannya untuk memecah masalah dan menentukan alat mana yang akan digunakan.

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "<thinking>To answer this question, I will: 1. Use the get_weather tool to get the current weather in San Francisco. 2. Use the get_time tool to get the current time in the America/Los_Angeles timezone, which covers San Francisco, CA.</thinking>"
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "get_weather",
      "input": { "location": "San Francisco, CA" }
    }
  ]
}
```

### Penggunaan alat paralel

Secara default, Claude dapat menggunakan beberapa alat untuk menjawab kueri pengguna. Anda dapat menonaktifkan perilaku ini dengan mengatur `disable_parallel_tool_use=true`.

## Menangani blok konten tool use dan tool result

### Menangani hasil dari alat klien

Respons memiliki `stop_reason` berupa `tool_use` dan satu atau lebih blok konten `tool_use` yang mencakup:

* `id`: Pengenal unik untuk blok penggunaan alat tertentu ini.
* `name`: Nama alat yang digunakan.
* `input`: Objek yang berisi input yang diteruskan ke alat.

Ketika Anda menerima respons penggunaan alat, Anda harus:

1. Mengekstrak `name`, `id`, dan `input` dari blok `tool_use`.
2. Menjalankan alat sebenarnya di basis kode Anda yang sesuai dengan nama alat tersebut.
3. Melanjutkan percakapan dengan mengirim pesan baru berisi `tool_result`:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "15 degrees"
    }
  ]
}
```

### Menangani stop reason `max_tokens`

Jika respons Claude terpotong karena mencapai batas `max_tokens` selama penggunaan alat, coba ulang permintaan dengan nilai `max_tokens` yang lebih tinggi.

### Menangani stop reason `pause_turn`

Saat menggunakan alat server seperti web search, API dapat mengembalikan stop reason `pause_turn`. Lanjutkan percakapan dengan mengirimkan kembali respons yang dijeda apa adanya dalam permintaan berikutnya.

## Memecahkan masalah error

### Error eksekusi alat

Jika alat itu sendiri melempar error selama eksekusi, kembalikan pesan error dengan `"is_error": true`:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "ConnectionError: the weather service API is not available (HTTP 500)",
      "is_error": true
    }
  ]
}
```

### Nama alat tidak valid

Jika upaya Claude menggunakan alat tidak valid (misalnya, parameter wajib tidak ada), coba permintaan lagi dengan nilai `description` yang lebih terperinci dalam definisi alat Anda.

## Streaming pesan

Saat membuat Message, Anda dapat mengatur `"stream": true` untuk melakukan streaming respons secara bertahap menggunakan "server-sent events" (event yang dikirim server), atau SSE.

### Streaming dengan SDK

<CodeGroup exclude="shell:cURL, typescript, csharp, go, java, php, ruby">
  ```bash CLI
  ant messages create --stream --format jsonl \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello"}' \
    | jq -rj 'select(.delta.type? == "text_delta") | .delta.text'
  ```

  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  with client.messages.stream(
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello"}],
      model="claude-opus-5",
  ) as stream:
      for text in stream.text_stream:
          print(text, end="", flush=True)
  ```
</CodeGroup>

### Tipe event

Setiap server-sent event menyertakan tipe event bernama dan data JSON terkait. Setiap stream menggunakan alur event berikut:

1. `message_start`: berisi objek `Message` dengan `content` kosong.
2. Serangkaian blok konten, masing-masing dengan `content_block_start`, satu atau lebih event `content_block_delta`, dan `content_block_stop`.
3. Satu atau lebih event `message_delta`, yang menunjukkan perubahan tingkat atas pada objek `Message` akhir.
4. Event `message_stop` terakhir.

**Peringatan:** Jumlah token yang ditampilkan di field `usage` pada event `message_delta` bersifat *kumulatif*.

### Tipe delta blok konten

#### Text delta

```json
{
  "type": "content_block_delta",
  "index": 0,
  "delta": { "type": "text_delta", "text": "Hello frien" }
}
```

#### Input JSON delta

Untuk blok konten `tool_use`, delta berupa *string JSON parsial*:

```json
{"type": "content_block_delta","index": 1,"delta": {"type": "input_json_delta","partial_json": "{\"location\": \"San Fra"}}}
```

#### Thinking delta

Saat menggunakan thinking dengan streaming:

```json
{
  "type": "content_block_delta",
  "index": 0,
  "delta": {
    "type": "thinking_delta",
    "thinking": "Let me solve this step by step..."
  }
}
```

### Contoh permintaan streaming dasar

```sse
event: message_start
data: {"type": "message_start", "message": {"id": "msg_1nZdL29xx5MUA1yADyHTEsnR8uuvGzszyY", "type": "message", "role": "assistant", "content": [], "model": "claude-opus-5", "stop_reason": null, "stop_sequence": null, "usage": {"input_tokens": 25, "output_tokens": 1}}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

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
