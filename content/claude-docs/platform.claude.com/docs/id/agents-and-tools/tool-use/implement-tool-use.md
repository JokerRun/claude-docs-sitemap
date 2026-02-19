---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/implement-tool-use
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: 27ea6b89b0ee29ac9f888f3162babbfaf03937cc374e73da0722610e64d24287
---

# Cara mengimplementasikan penggunaan alat

Panduan lengkap untuk mengimplementasikan penggunaan alat dengan Claude, termasuk definisi alat, contoh, dan praktik terbaik.

---

## Memilih model

Kami merekomendasikan menggunakan model Claude Opus terbaru (4.6) untuk alat kompleks dan kueri yang ambigu; model ini menangani beberapa alat dengan lebih baik dan mencari klarifikasi saat diperlukan.

Gunakan model Claude Haiku untuk alat yang sederhana, tetapi perhatikan bahwa mereka mungkin menyimpulkan parameter yang hilang.

<Tip>
Jika menggunakan Claude dengan penggunaan alat dan pemikiran yang diperluas, lihat [panduan pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking) untuk informasi lebih lanjut.
</Tip>

## Menentukan alat klien

Alat klien (baik yang ditentukan Anthropic maupun yang ditentukan pengguna) ditentukan dalam parameter tingkat atas `tools` dari permintaan API. Setiap definisi alat mencakup:

| Parameter      | Deskripsi                                                                                         |
| :------------- | :-------------------------------------------------------------------------------------------------- |
| `name`         | Nama alat. Harus cocok dengan regex `^[a-zA-Z0-9_-]{1,64}$`.                                 |
| `description`  | Deskripsi plaintext terperinci tentang apa yang dilakukan alat, kapan harus digunakan, dan bagaimana perilakunya. |
| `input_schema` | Objek [JSON Schema](https://json-schema.org/) yang mendefinisikan parameter yang diharapkan untuk alat.     |
| `input_examples` | (Opsional) Larik objek input contoh untuk membantu Claude memahami cara menggunakan alat. Lihat [Memberikan contoh penggunaan alat](#providing-tool-use-examples). |

<section title="Contoh definisi alat sederhana">

```json JSON
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

Alat ini, bernama `get_weather`, mengharapkan objek input dengan string `location` yang diperlukan dan string `unit` opsional yang harus berupa "celsius" atau "fahrenheit".

</section>

### Prompt sistem penggunaan alat

Ketika Anda memanggil API Claude dengan parameter `tools`, kami membuat prompt sistem khusus dari definisi alat, konfigurasi alat, dan prompt sistem yang ditentukan pengguna. Prompt yang dibangun dirancang untuk menginstruksikan model menggunakan alat yang ditentukan dan memberikan konteks yang diperlukan agar alat beroperasi dengan baik:

```text
In this environment you have access to a set of tools you can use to answer the user's question.
{{ FORMATTING INSTRUCTIONS }}
String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular expressions.
Here are the functions available in JSONSchema format:
{{ TOOL DEFINITIONS IN JSON SCHEMA }}
{{ USER SYSTEM PROMPT }}
{{ TOOL CONFIGURATION }}
```

### Praktik terbaik untuk definisi alat

Untuk mendapatkan kinerja terbaik dari Claude saat menggunakan alat, ikuti panduan ini:

- **Berikan deskripsi yang sangat terperinci.** Ini adalah faktor paling penting dalam kinerja alat. Deskripsi Anda harus menjelaskan setiap detail tentang alat, termasuk:
  - Apa yang dilakukan alat
  - Kapan harus digunakan (dan kapan tidak boleh)
  - Apa arti setiap parameter dan bagaimana pengaruhnya terhadap perilaku alat
  - Peringatan atau batasan penting, seperti informasi apa yang tidak dikembalikan alat jika nama alat tidak jelas. Semakin banyak konteks yang dapat Anda berikan Claude tentang alat Anda, semakin baik dalam memutuskan kapan dan bagaimana menggunakannya. Targetkan setidaknya 3-4 kalimat per deskripsi alat, lebih banyak jika alat kompleks.
- **Prioritaskan deskripsi, tetapi pertimbangkan menggunakan `input_examples` untuk alat kompleks.** Deskripsi yang jelas paling penting, tetapi untuk alat dengan input kompleks, objek bersarang, atau parameter sensitif format, Anda dapat menggunakan bidang `input_examples` untuk memberikan contoh yang divalidasi skema. Lihat [Memberikan contoh penggunaan alat](#providing-tool-use-examples) untuk detail.

<section title="Contoh deskripsi alat yang baik">

```json JSON
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

</section>

<section title="Contoh deskripsi alat yang buruk">

```json JSON
{
  "name": "get_stock_price",
  "description": "Gets the stock price for a ticker.",
  "input_schema": {
    "type": "object",
    "properties": {
      "ticker": {
        "type": "string"
      }
    },
    "required": ["ticker"]
  }
}
```

</section>

Deskripsi yang baik dengan jelas menjelaskan apa yang dilakukan alat, kapan menggunakannya, data apa yang dikembalikan, dan apa arti parameter `ticker`. Deskripsi yang buruk terlalu singkat dan meninggalkan Claude dengan banyak pertanyaan terbuka tentang perilaku dan penggunaan alat.

## Memberikan contoh penggunaan alat

Anda dapat memberikan contoh konkret input alat yang valid untuk membantu Claude memahami cara menggunakan alat Anda dengan lebih efektif. Ini sangat berguna untuk alat kompleks dengan objek bersarang, parameter opsional, atau input sensitif format.

### Penggunaan dasar

Tambahkan bidang `input_examples` opsional ke definisi alat Anda dengan larik objek input contoh. Setiap contoh harus valid sesuai dengan `input_schema` alat:

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature",
                    },
                },
                "required": ["location"],
            },
            "input_examples": [
                {"location": "San Francisco, CA", "unit": "fahrenheit"},
                {"location": "Tokyo, Japan", "unit": "celsius"},
                {
                    "location": "New York, NY"  # 'unit' is optional
                },
            ],
        }
    ],
    messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [
    {
      name: "get_weather",
      description: "Get the current weather in a given location",
      input_schema: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "The city and state, e.g. San Francisco, CA"
          },
          unit: {
            type: "string",
            enum: ["celsius", "fahrenheit"],
            description: "The unit of temperature"
          }
        },
        required: ["location"]
      },
      input_examples: [
        {
          location: "San Francisco, CA",
          unit: "fahrenheit"
        },
        {
          location: "Tokyo, Japan",
          unit: "celsius"
        },
        {
          location: "New York, NY"
          // Demonstrates that 'unit' is optional
        }
      ]
    }
  ],
  messages: [{ role: "user", content: "What's the weather like in San Francisco?" }]
});
```
</CodeGroup>

Contoh disertakan dalam prompt bersama skema alat Anda, menunjukkan Claude pola konkret untuk panggilan alat yang terbentuk dengan baik. Ini membantu Claude memahami kapan harus menyertakan parameter opsional, format apa yang harus digunakan, dan cara menyusun input kompleks.

### Persyaratan dan batasan

- **Validasi skema** - Setiap contoh harus valid sesuai dengan `input_schema` alat. Contoh yang tidak valid mengembalikan kesalahan 400
- **Tidak didukung untuk alat sisi server** - Hanya alat yang ditentukan pengguna yang dapat memiliki contoh input
- **Biaya token** - Contoh menambah token prompt: ~20-50 token untuk contoh sederhana, ~100-200 token untuk objek bersarang kompleks

## Pelari alat (beta)

Pelari alat menyediakan solusi siap pakai untuk menjalankan alat dengan Claude. Alih-alih menangani panggilan alat, hasil alat, dan manajemen percakapan secara manual, pelari alat secara otomatis:

- Menjalankan alat ketika Claude memanggilnya
- Menangani siklus permintaan/respons
- Mengelola status percakapan
- Menyediakan keamanan tipe dan validasi

Kami merekomendasikan agar Anda menggunakan pelari alat untuk sebagian besar implementasi penggunaan alat.

<Note>
Pelari alat saat ini dalam beta dan tersedia di SDK [Python](https://github.com/anthropics/anthropic-sdk-python/blob/main/tools.md), [TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/helpers.md#tool-helpers), dan [Ruby](https://github.com/anthropics/anthropic-sdk-ruby/blob/main/helpers.md#3-auto-looping-tool-runner-beta).
</Note>

<Tip>
**Manajemen konteks otomatis dengan pemadatan**

Pelari alat mendukung [pemadatan](/docs/id/build-with-claude/context-editing#client-side-compaction-sdk) otomatis, yang menghasilkan ringkasan ketika penggunaan token melebihi ambang batas. Ini memungkinkan tugas agentic jangka panjang untuk melanjutkan melampaui batas jendela konteks.
</Tip>

### Penggunaan dasar

Tentukan alat menggunakan pembantu SDK, kemudian gunakan pelari alat untuk menjalankannya.

<Tabs>
<Tab title="Python">

Gunakan dekorator `@beta_tool` untuk mendefinisikan alat dengan petunjuk tipe dan docstring.

<Note>
Jika Anda menggunakan klien async, ganti `@beta_tool` dengan `@beta_async_tool` dan tentukan fungsi dengan `async def`.
</Note>

```python
import anthropic
import json
from anthropic import beta_tool

# Initialize client
client = anthropic.Anthropic()


# Define tools using the decorator
@beta_tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a given location.

    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: Temperature unit, either 'celsius' or 'fahrenheit'
    """
    # In a full implementation, you'd call a weather API here
    return json.dumps({"temperature": "20°C", "condition": "Sunny"})


@beta_tool
def calculate_sum(a: int, b: int) -> str:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number
    """
    return str(a + b)


# Use the tool runner
runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[get_weather, calculate_sum],
    messages=[
        {
            "role": "user",
            "content": "What's the weather like in Paris? Also, what's 15 + 27?",
        }
    ],
)
for message in runner:
    print(message.content[0].text)
```

Dekorator `@beta_tool` memeriksa argumen fungsi dan docstring untuk mengekstrak representasi skema JSON. Misalnya, `calculate_sum` menjadi:

```json
{
  "name": "calculate_sum",
  "description": "Adds two integers together.",
  "input_schema": {
    "additionalProperties": false,
    "properties": {
      "left": {
        "description": "The first integer to add.",
        "title": "Left",
        "type": "integer"
      },
      "right": {
        "description": "The second integer to add.",
        "title": "Right",
        "type": "integer"
      }
    },
    "required": ["left", "right"],
    "type": "object"
  }
}
```

</Tab>
<Tab title="TypeScript">

Gunakan `betaZodTool()` untuk definisi alat yang aman tipe dengan validasi Zod, atau `betaTool()` untuk definisi berbasis JSON Schema.

TypeScript menawarkan dua pendekatan untuk mendefinisikan alat:

**Menggunakan Zod (direkomendasikan)** - Gunakan `betaZodTool()` untuk definisi alat yang aman tipe dengan validasi Zod (memerlukan Zod 3.25.0 atau lebih tinggi):

```typescript
import { Anthropic } from "@anthropic-ai/sdk";
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const anthropic = new Anthropic();

const getWeatherTool = betaZodTool({
  name: "get_weather",
  description: "Get the current weather in a given location",
  inputSchema: z.object({
    location: z.string().describe("The city and state, e.g. San Francisco, CA"),
    unit: z.enum(["celsius", "fahrenheit"]).default("fahrenheit")
      .describe("Temperature unit")
  }),
  run: async (input) => {
    // In a full implementation, you'd call a weather API here
    return JSON.stringify({ temperature: "20°C", condition: "Sunny" });
  }
});

const runner = anthropic.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [getWeatherTool],
  messages: [{ role: "user", content: "What's the weather like in Paris?" }]
});

for await (const message of runner) {
  console.log(message.content[0].text);
}
```

**Menggunakan JSON Schema** - Gunakan `betaTool()` untuk definisi alat yang aman tipe tanpa Zod:

<Note>
Input yang dihasilkan oleh Claude tidak akan divalidasi saat runtime. Lakukan validasi di dalam fungsi `run` jika diperlukan.
</Note>

```typescript
import { Anthropic } from "@anthropic-ai/sdk";
import { betaTool } from "@anthropic-ai/sdk/helpers/beta/json-schema";

const anthropic = new Anthropic();

const calculateSumTool = betaTool({
  name: "calculate_sum",
  description: "Add two numbers together",
  inputSchema: {
    type: "object",
    properties: {
      a: { type: "number", description: "First number" },
      b: { type: "number", description: "Second number" }
    },
    required: ["a", "b"]
  },
  run: async (input) => {
    return String(input.a + input.b);
  }
});

const runner = anthropic.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [calculateSumTool],
  messages: [{ role: "user", content: "What's 15 + 27?" }]
});

for await (const message of runner) {
  console.log(message.content[0].text);
}
```

</Tab>
<Tab title="Ruby">

Gunakan kelas `Anthropic::BaseTool` untuk mendefinisikan alat dengan skema input yang diketik.

```ruby
require "anthropic"

# Initialize client
client = Anthropic::Client.new

# Define input schema
class GetWeatherInput < Anthropic::BaseModel
  required :location, String, doc: "The city and state, e.g. San Francisco, CA"
  optional :unit, Anthropic::InputSchema::EnumOf["celsius", "fahrenheit"],
           doc: "Temperature unit"
end

# Define tool
class GetWeather < Anthropic::BaseTool
  doc "Get the current weather in a given location"
  input_schema GetWeatherInput

  def call(input)
    # In a full implementation, you'd call a weather API here
    JSON.generate({temperature: "20°C", condition: "Sunny"})
  end
end

class CalculateSumInput < Anthropic::BaseModel
  required :a, Integer, doc: "First number"
  required :b, Integer, doc: "Second number"
end

class CalculateSum < Anthropic::BaseTool
  doc "Add two numbers together"
  input_schema CalculateSumInput

  def call(input)
    (input.a + input.b).to_s
  end
end

# Use the tool runner
runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [GetWeather.new, CalculateSum.new],
  messages: [
    {role: "user", content: "What's the weather like in Paris? Also, what's 15 + 27?"}
  ]
)

runner.each_message do |message|
  message.content.each do |block|
    puts block.text if block.respond_to?(:text)
  end
end
```

Kelas `Anthropic::BaseTool` menggunakan metode `doc` untuk deskripsi alat dan `input_schema` untuk mendefinisikan parameter yang diharapkan. SDK secara otomatis mengonversi ini ke format skema JSON yang sesuai.

</Tab>
</Tabs>

Fungsi alat harus mengembalikan blok konten atau larik blok konten, termasuk teks, gambar, atau blok dokumen. Ini memungkinkan alat untuk mengembalikan respons multimodal yang kaya. String yang dikembalikan akan dikonversi ke blok konten teks. Jika Anda ingin mengembalikan objek JSON terstruktur ke Claude, enkode ke string JSON sebelum mengembalikannya. Angka, boolean, atau primitif non-string lainnya juga harus dikonversi ke string.

### Iterasi di atas pelari alat

Pelari alat adalah iterable yang menghasilkan pesan dari Claude. Ini sering disebut sebagai "tool call loop". Setiap iterasi, pelari memeriksa apakah Claude meminta penggunaan alat. Jika ya, ia memanggil alat dan mengirim hasilnya kembali ke Claude secara otomatis, kemudian menghasilkan pesan berikutnya dari Claude untuk melanjutkan loop Anda.

Anda dapat mengakhiri loop pada iterasi apa pun dengan pernyataan `break`. Pelari akan berulang sampai Claude mengembalikan pesan tanpa penggunaan alat.

Jika Anda tidak memerlukan pesan perantara, Anda dapat mendapatkan pesan akhir secara langsung:

<Tabs>
<Tab title="Python">

Gunakan `runner.until_done()` untuk mendapatkan pesan akhir.

```python
runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[get_weather, calculate_sum],
    messages=[
        {
            "role": "user",
            "content": "What's the weather like in Paris? Also, what's 15 + 27?",
        }
    ],
)
final_message = runner.until_done()
print(final_message.content[0].text)
```

</Tab>
<Tab title="TypeScript">

Cukup `await` pelari untuk mendapatkan pesan akhir.

```typescript
const runner = anthropic.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [getWeatherTool],
  messages: [{ role: "user", content: "What's the weather like in Paris?" }]
});

const finalMessage = await runner;
console.log(finalMessage.content[0].text);
```

</Tab>
<Tab title="Ruby">

Gunakan `runner.run_until_finished` untuk mendapatkan semua pesan.

```ruby
runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [GetWeather.new, CalculateSum.new],
  messages: [
    {role: "user", content: "What's the weather like in Paris? Also, what's 15 + 27?"}
  ]
)

all_messages = runner.run_until_finished
all_messages.each { |msg| puts msg.content }
```

</Tab>
</Tabs>

### Penggunaan lanjutan

Dalam loop, Anda dapat sepenuhnya menyesuaikan permintaan berikutnya pelari alat ke API Pesan. Pelari secara otomatis menambahkan hasil alat ke riwayat pesan, jadi Anda tidak perlu mengelolanya secara manual. Anda dapat secara opsional memeriksa hasil alat untuk logging atau debugging, dan memodifikasi parameter permintaan sebelum panggilan API berikutnya.

<Tabs>
<Tab title="Python">

Gunakan `generate_tool_call_response()` untuk secara opsional memeriksa hasil alat (pelari menambahkannya secara otomatis). Gunakan `set_messages_params()` dan `append_messages()` untuk memodifikasi permintaan.

```python
runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[get_weather],
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}],
)
for message in runner:
    # Optional: inspect the tool response (automatically appended by the runner)
    tool_response = runner.generate_tool_call_response()
    if tool_response:
        print(f"Tool result: {tool_response}")

    # Customize the next request
    runner.set_messages_params(
        lambda params: {
            **params,
            "max_tokens": 2048,  # Increase tokens for next request
        }
    )

    # Or add additional messages
    runner.append_messages(
        {"role": "user", "content": "Please be concise in your response."}
    )
```

</Tab>
<Tab title="TypeScript">

Gunakan `generateToolResponse()` untuk secara opsional memeriksa hasil alat (pelari menambahkannya secara otomatis). Gunakan `setMessagesParams()` dan `pushMessages()` untuk memodifikasi permintaan.

```typescript
const runner = anthropic.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [getWeatherTool],
  messages: [{ role: "user", content: "What's the weather in San Francisco?" }]
});

for await (const message of runner) {
  // Optional: inspect the tool result message (automatically appended by the runner)
  const toolResultMessage = await runner.generateToolResponse();
  if (toolResultMessage) {
    console.log("Tool result:", toolResultMessage);
  }

  // Customize the next request
  runner.setMessagesParams(params => ({
    ...params,
    max_tokens: 2048 // Increase tokens for next request
  }));

  // Or add additional messages
  runner.pushMessages(
    { role: "user", content: "Please be concise in your response." }
  );
}
```

</Tab>
<Tab title="Ruby">

Gunakan `next_message` untuk kontrol langkah demi langkah. Gunakan `feed_messages` untuk menyuntikkan pesan dan `params` untuk mengakses parameter.

```ruby
runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [GetWeather.new],
  messages: [{role: "user", content: "What's the weather in San Francisco?"}]
)

# Manual step-by-step control
message = runner.next_message
puts message.content

# Inject follow-up messages
runner.feed_messages([
  {role: "user", content: "Also check Boston"}
])

# Access current parameters
puts runner.params
```

</Tab>
</Tabs>

#### Debugging eksekusi alat

Ketika alat melempar pengecualian, pelari alat menangkapnya dan mengembalikan kesalahan ke Claude sebagai hasil alat dengan `is_error: true`. Secara default, hanya pesan pengecualian yang disertakan, bukan stack trace lengkap.

Untuk melihat stack trace lengkap dan informasi debug, atur variabel lingkungan `ANTHROPIC_LOG`:

```bash
# View info-level logs including tool errors
export ANTHROPIC_LOG=info

# View debug-level logs for more verbose output
export ANTHROPIC_LOG=debug
```

Ketika diaktifkan, SDK mencatat detail pengecualian lengkap (menggunakan modul `logging` Python, konsol di TypeScript, atau logger Ruby), termasuk stack trace lengkap ketika alat gagal.

#### Mengintersepsi kesalahan alat

Secara default, kesalahan alat diteruskan kembali ke Claude, yang kemudian dapat merespons dengan tepat. Namun, Anda mungkin ingin mendeteksi kesalahan dan menanganinya secara berbeda—misalnya, untuk menghentikan eksekusi lebih awal atau menerapkan penanganan kesalahan khusus.

Gunakan metode respons alat untuk mengintersepsi hasil alat dan memeriksa kesalahan sebelum dikirim ke Claude:

<Tabs>
<Tab title="Python">

```python
import json

runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[my_tool],
    messages=[{"role": "user", "content": "Run the tool"}],
)

for message in runner:
    tool_response = runner.generate_tool_call_response()

    if tool_response:
        # Check if any tool result has an error
        for block in tool_response.content:
            if block.is_error:
                # Option 1: Raise an exception to stop the loop
                raise RuntimeError(f"Tool failed: {json.dumps(block.content)}")

                # Option 2: Log and continue (let Claude handle it)
                # logger.error(f"Tool error: {json.dumps(block.content)}")

    # Process the message normally
    print(message.content)
```

</Tab>
<Tab title="TypeScript">

```typescript
const runner = anthropic.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [myTool],
  messages: [{ role: "user", content: "Run the tool" }]
});

for await (const message of runner) {
  const toolResultMessage = await runner.generateToolResponse();

  if (toolResultMessage) {
    // Check if any tool result has an error
    for (const block of toolResultMessage.content) {
      if (block.type === "tool_result" && block.is_error) {
        // Option 1: Throw to stop the loop
        throw new Error(`Tool failed: ${JSON.stringify(block.content)}`);

        // Option 2: Log and continue (let Claude handle it)
        // console.error(`Tool error: ${JSON.stringify(block.content)}`);
      }
    }
  }

  // Process the message normally
  console.log(message.content);
}
```

</Tab>
<Tab title="Ruby">

```ruby
runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [MyTool.new],
  messages: [{role: "user", content: "Run the tool"}]
)

runner.each_message do |message|
  # Get the tool response to check for errors
  # Note: The runner automatically handles tool execution and appends results
  # This is just for error checking/logging purposes
  tool_results = runner.params[:messages].last

  if tool_results && tool_results[:role] == "user"
    tool_results[:content].each do |block|
      if block[:type] == "tool_result" && block[:is_error]
        # Option 1: Raise an exception to stop the loop
        raise "Tool failed: #{block[:content]}"

        # Option 2: Log and continue (let Claude handle it)
        # logger.error("Tool error: #{block[:content]}")
      end
    end
  end

  puts message.content
end
```

</Tab>
</Tabs>

#### Memodifikasi hasil alat

Anda dapat memodifikasi hasil alat sebelum dikirim kembali ke Claude. Ini berguna untuk menambahkan metadata seperti `cache_control` untuk mengaktifkan [prompt caching](/docs/id/build-with-claude/prompt-caching) pada hasil alat, atau untuk mengubah output alat.

Gunakan metode respons alat untuk mendapatkan hasil alat, memodifikasinya, kemudian tambahkan versi yang dimodifikasi ke pesan:

<Tabs>
<Tab title="Python">

```python
runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[search_documents],
    messages=[
        {
            "role": "user",
            "content": "Search for information about the climate of San Francisco",
        }
    ],
)

for message in runner:
    tool_response = runner.generate_tool_call_response()

    if tool_response:
        # Modify the tool result to add cache control
        for block in tool_response.content:
            if block.type == "tool_result":
                # Add cache_control to cache this tool result
                block.cache_control = {"type": "ephemeral"}

        # Append the modified response (this prevents auto-append of original)
        runner.append_messages(message, tool_response)

    print(message.content)
```

</Tab>
<Tab title="TypeScript">

```typescript
const runner = anthropic.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [searchDocuments],
  messages: [{ role: "user", content: "Search for information about the climate of San Francisco" }]
});

for await (const message of runner) {
  const toolResultMessage = await runner.generateToolResponse();

  if (toolResultMessage) {
    // Modify the tool result to add cache control
    for (const block of toolResultMessage.content) {
      if (block.type === "tool_result") {
        // Add cache_control to cache this tool result
        block.cache_control = { type: "ephemeral" };
      }
    }

    // Push the modified message (this prevents auto-append of original)
    runner.pushMessages(message, toolResultMessage);
  }

  console.log(message.content);
}
```

</Tab>
<Tab title="Ruby">

```ruby
runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [SearchDocuments.new],
  messages: [{role: "user", content: "Search for information about the climate of San Francisco"}]
)

loop do
  message = runner.next_message
  break unless message

  # Access the most recent tool results from the messages array
  # The runner automatically adds tool results, but we can modify them
  tool_results_message = runner.params[:messages].last

  if tool_results_message && tool_results_message[:role] == "user"
    tool_results_message[:content].each do |block|
      if block[:type] == "tool_result"
        # Modify the tool result to add cache control
        block[:cache_control] = {type: "ephemeral"}
      end
    end
  end

  puts message.content
  break if message.stop_reason != "tool_use"
end
```

</Tab>
</Tabs>

<Tip>
Menambahkan `cache_control` ke hasil alat sangat berguna ketika alat mengembalikan jumlah data besar (seperti hasil pencarian dokumen) yang ingin Anda cache untuk panggilan API berikutnya. Lihat [Prompt caching](/docs/id/build-with-claude/prompt-caching) untuk detail lebih lanjut tentang strategi caching.
</Tip>

### Streaming

Aktifkan streaming untuk menerima acara saat tiba. Setiap iterasi menghasilkan objek stream yang dapat Anda iterasi untuk acara.

<Tabs>
<Tab title="Python">

Atur `stream=True` dan gunakan `get_final_message()` untuk mendapatkan pesan yang terakumulasi.

```python
runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[calculate_sum],
    messages=[{"role": "user", "content": "What is 15 + 27?"}],
    stream=True,
)

# When streaming, the runner returns BetaMessageStream
for message_stream in runner:
    for event in message_stream:
        print("event:", event)
    print("message:", message_stream.get_final_message())

print(runner.until_done())
```

</Tab>
<Tab title="TypeScript">

Atur `stream: true` dan gunakan `finalMessage()` untuk mendapatkan pesan yang terakumulasi.

```typescript
const runner = anthropic.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 1000,
  messages: [{ role: "user", content: "What is the weather in San Francisco?" }],
  tools: [getWeatherTool],
  stream: true
});

// When streaming, the runner returns BetaMessageStream
for await (const messageStream of runner) {
  for await (const event of messageStream) {
    console.log("event:", event);
  }
  console.log("message:", await messageStream.finalMessage());
}

console.log(await runner);
```

</Tab>
<Tab title="Ruby">

Gunakan `each_streaming` untuk mengulangi acara streaming.

```ruby
runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [CalculateSum.new],
  messages: [{role: "user", content: "What is 15 + 27?"}]
)

runner.each_streaming do |event|
  case event
  when Anthropic::Streaming::TextEvent
    print event.text
  when Anthropic::Streaming::ToolUseEvent
    puts "\nTool called: #{event.tool_name}"
  end
end
```

</Tab>
</Tabs>

<Note>
Pelari alat SDK dalam beta. Sisa dokumen ini mencakup implementasi alat manual.
</Note>

## Mengontrol output Claude

### Memaksa penggunaan alat

Dalam beberapa kasus, Anda mungkin ingin Claude menggunakan alat tertentu untuk menjawab pertanyaan pengguna, bahkan jika Claude berpikir dapat memberikan jawaban tanpa menggunakan alat. Anda dapat melakukan ini dengan menentukan alat dalam bidang `tool_choice` seperti ini:

```text
tool_choice = {"type": "tool", "name": "get_weather"}
```

Saat bekerja dengan parameter tool_choice, kami memiliki empat opsi yang mungkin:

- `auto` memungkinkan Claude memutuskan apakah akan memanggil alat yang disediakan atau tidak. Ini adalah nilai default ketika `tools` disediakan.
- `any` memberitahu Claude bahwa ia harus menggunakan salah satu alat yang disediakan, tetapi tidak memaksa alat tertentu.
- `tool` memungkinkan kami memaksa Claude untuk selalu menggunakan alat tertentu.
- `none` mencegah Claude menggunakan alat apa pun. Ini adalah nilai default ketika tidak ada `tools` yang disediakan.

<Note>
Saat menggunakan [prompt caching](/docs/id/build-with-claude/prompt-caching#what-invalidates-the-cache), perubahan pada parameter `tool_choice` akan membatalkan blok pesan yang di-cache. Definisi alat dan prompt sistem tetap di-cache, tetapi konten pesan harus diproses ulang.
</Note>

Diagram ini mengilustrasikan cara kerja setiap opsi:

<Frame>
  ![Image](/docs/images/tool_choice.png)
</Frame>

Perhatikan bahwa ketika Anda memiliki `tool_choice` sebagai `any` atau `tool`, kami akan mengisi pesan asisten sebelumnya untuk memaksa alat digunakan. Ini berarti model tidak akan mengeluarkan respons bahasa alami atau penjelasan sebelum blok konten `tool_use`, bahkan jika secara eksplisit diminta untuk melakukannya.

<Note>
Saat menggunakan [pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking) dengan penggunaan alat, `tool_choice: {"type": "any"}` dan `tool_choice: {"type": "tool", "name": "..."}` tidak didukung dan akan menghasilkan kesalahan. Hanya `tool_choice: {"type": "auto"}` (default) dan `tool_choice: {"type": "none"}` yang kompatibel dengan pemikiran yang diperluas.
</Note>

Pengujian kami menunjukkan bahwa ini seharusnya tidak mengurangi kinerja. Jika Anda ingin model memberikan konteks bahasa alami atau penjelasan sambil tetap meminta model menggunakan alat tertentu, Anda dapat menggunakan `{"type": "auto"}` untuk `tool_choice` (default) dan menambahkan instruksi eksplisit dalam pesan `user`. Misalnya: `What's the weather like in London? Use the get_weather tool in your response.`

<Tip>
**Panggilan alat yang dijamin dengan alat ketat**

Gabungkan `tool_choice: {"type": "any"}` dengan [penggunaan alat ketat](/docs/id/build-with-claude/structured-outputs) untuk menjamin bahwa salah satu alat Anda akan dipanggil DAN input alat akan mengikuti skema Anda dengan ketat. Atur `strict: true` pada definisi alat Anda untuk mengaktifkan validasi skema.
</Tip>

### Output JSON

Alat tidak perlu menjadi fungsi klien — Anda dapat menggunakan alat kapan saja Anda ingin model mengembalikan output JSON yang mengikuti skema yang disediakan. Misalnya, Anda mungkin menggunakan alat `record_summary` dengan skema tertentu. Lihat [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview) untuk contoh kerja lengkap.

### Respons model dengan alat

Saat menggunakan alat, Claude sering kali akan mengomentari apa yang sedang dilakukan atau merespons secara alami kepada pengguna sebelum memanggil alat.

Misalnya, diberikan prompt "Bagaimana cuaca di San Francisco sekarang, dan jam berapa di sana?", Claude mungkin merespons dengan:

```json JSON
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll help you check the current weather and time in San Francisco."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "get_weather",
      "input": {"location": "San Francisco, CA"}
    }
  ]
}
```

Gaya respons alami ini membantu pengguna memahami apa yang dilakukan Claude dan menciptakan interaksi yang lebih percakapan. Anda dapat memandu gaya dan konten respons ini melalui prompt sistem Anda dan dengan menyediakan `<examples>` dalam prompt Anda.

Penting untuk dicatat bahwa Claude dapat menggunakan berbagai frasa dan pendekatan saat menjelaskan tindakannya. Kode Anda harus memperlakukan respons ini seperti teks yang dihasilkan asisten lainnya, dan tidak mengandalkan konvensi pemformatan tertentu.

### Penggunaan alat paralel

Secara default, Claude dapat menggunakan beberapa alat untuk menjawab pertanyaan pengguna. Anda dapat menonaktifkan perilaku ini dengan:

- Mengatur `disable_parallel_tool_use=true` ketika jenis tool_choice adalah `auto`, yang memastikan bahwa Claude menggunakan **paling banyak satu** alat
- Mengatur `disable_parallel_tool_use=true` ketika jenis tool_choice adalah `any` atau `tool`, yang memastikan bahwa Claude menggunakan **tepat satu** alat

<section title="Contoh penggunaan alat paralel lengkap">

<Note>
**Lebih sederhana dengan Tool runner**: Contoh di bawah ini menunjukkan penanganan alat paralel manual. Untuk sebagian besar kasus penggunaan, [tool runner](#tool-runner-beta) secara otomatis menangani eksekusi alat paralel dengan kode yang jauh lebih sedikit.
</Note>

Berikut adalah contoh lengkap yang menunjukkan cara memformat panggilan alat paralel dengan benar dalam riwayat pesan:

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

# Define tools
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                }
            },
            "required": ["location"],
        },
    },
    {
        "name": "get_time",
        "description": "Get the current time in a given timezone",
        "input_schema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "The timezone, e.g. America/New_York",
                }
            },
            "required": ["timezone"],
        },
    },
]

# Initial request
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[
        {
            "role": "user",
            "content": "What's the weather in SF and NYC, and what time is it there?",
        }
    ],
)

# Claude's response with parallel tool calls
print("Claude wants to use tools:", response.stop_reason == "tool_use")
print(
    "Number of tool calls:", len([c for c in response.content if c.type == "tool_use"])
)

# Build the conversation with tool results
messages = [
    {
        "role": "user",
        "content": "What's the weather in SF and NYC, and what time is it there?",
    },
    {
        "role": "assistant",
        "content": response.content,  # Contains multiple tool_use blocks
    },
    {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": "toolu_01",  # Must match the ID from tool_use
                "content": "San Francisco: 68°F, partly cloudy",
            },
            {
                "type": "tool_result",
                "tool_use_id": "toolu_02",
                "content": "New York: 45°F, clear skies",
            },
            {
                "type": "tool_result",
                "tool_use_id": "toolu_03",
                "content": "San Francisco time: 2:30 PM PST",
            },
            {
                "type": "tool_result",
                "tool_use_id": "toolu_04",
                "content": "New York time: 5:30 PM EST",
            },
        ],
    },
]

# Get final response
final_response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024, tools=tools, messages=messages
)

print(final_response.content[0].text)
```

```typescript TypeScript
import { Anthropic } from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

// Define tools
const tools = [
  {
    name: "get_weather",
    description: "Get the current weather in a given location",
    input_schema: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "The city and state, e.g. San Francisco, CA"
        }
      },
      required: ["location"]
    }
  },
  {
    name: "get_time",
    description: "Get the current time in a given timezone",
    input_schema: {
      type: "object",
      properties: {
        timezone: {
          type: "string",
          description: "The timezone, e.g. America/New_York"
        }
      },
      required: ["timezone"]
    }
  }
];

// Initial request
const response = await anthropic.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: tools,
  messages: [
    {
      role: "user",
      content: "What's the weather in SF and NYC, and what time is it there?"
    }
  ]
});

// Build conversation with tool results
const messages = [
  {
    role: "user",
    content: "What's the weather in SF and NYC, and what time is it there?"
  },
  {
    role: "assistant",
    content: response.content // Contains multiple tool_use blocks
  },
  {
    role: "user",
    content: [
      {
        type: "tool_result",
        tool_use_id: "toolu_01", // Must match the ID from tool_use
        content: "San Francisco: 68°F, partly cloudy"
      },
      {
        type: "tool_result",
        tool_use_id: "toolu_02",
        content: "New York: 45°F, clear skies"
      },
      {
        type: "tool_result",
        tool_use_id: "toolu_03",
        content: "San Francisco time: 2:30 PM PST"
      },
      {
        type: "tool_result",
        tool_use_id: "toolu_04",
        content: "New York time: 5:30 PM EST"
      }
    ]
  }
];

// Get final response
const finalResponse = await anthropic.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: tools,
  messages: messages
});

console.log(finalResponse.content[0].text);
```
</CodeGroup>

Pesan asisten dengan panggilan alat paralel akan terlihat seperti ini:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll check the weather and time for both San Francisco and New York City."
    },
    {
      "type": "tool_use",
      "id": "toolu_01",
      "name": "get_weather",
      "input": {"location": "San Francisco, CA"}
    },
    {
      "type": "tool_use",
      "id": "toolu_02",
      "name": "get_weather",
      "input": {"location": "New York, NY"}
    },
    {
      "type": "tool_use",
      "id": "toolu_03",
      "name": "get_time",
      "input": {"timezone": "America/Los_Angeles"}
    },
    {
      "type": "tool_use",
      "id": "toolu_04",
      "name": "get_time",
      "input": {"timezone": "America/New_York"}
    }
  ]
}
```

</section>
<section title="Skrip uji lengkap untuk alat paralel">

Berikut adalah skrip lengkap yang dapat dijalankan untuk menguji dan memverifikasi bahwa panggilan alat paralel berfungsi dengan benar:

<CodeGroup>
```python Python
#!/usr/bin/env python3
"""Test script to verify parallel tool calls with the Claude API"""

import os
from anthropic import Anthropic

# Initialize client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Define tools
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                }
            },
            "required": ["location"],
        },
    },
    {
        "name": "get_time",
        "description": "Get the current time in a given timezone",
        "input_schema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "The timezone, e.g. America/New_York",
                }
            },
            "required": ["timezone"],
        },
    },
]

# Test conversation with parallel tool calls
messages = [
    {
        "role": "user",
        "content": "What's the weather in SF and NYC, and what time is it there?",
    }
]

# Make initial request
print("Requesting parallel tool calls...")
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024, messages=messages, tools=tools
)

# Check for parallel tool calls
tool_uses = [block for block in response.content if block.type == "tool_use"]
print(f"\n✓ Claude made {len(tool_uses)} tool calls")

if len(tool_uses) > 1:
    print("✓ Parallel tool calls detected!")
    for tool in tool_uses:
        print(f"  - {tool.name}: {tool.input}")
else:
    print("✗ No parallel tool calls detected")

# Simulate tool execution and format results correctly
tool_results = []
for tool_use in tool_uses:
    if tool_use.name == "get_weather":
        if "San Francisco" in str(tool_use.input):
            result = "San Francisco: 68°F, partly cloudy"
        else:
            result = "New York: 45°F, clear skies"
    else:  # get_time
        if "Los_Angeles" in str(tool_use.input):
            result = "2:30 PM PST"
        else:
            result = "5:30 PM EST"

    tool_results.append(
        {"type": "tool_result", "tool_use_id": tool_use.id, "content": result}
    )

# Continue conversation with tool results
messages.extend(
    [
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": tool_results},  # All results in one message!
    ]
)

# Get final response
print("\nGetting final response...")
final_response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024, messages=messages, tools=tools
)

print(f"\nClaude's response:\n{final_response.content[0].text}")

# Verify formatting
print("\n--- Verification ---")
print(f"✓ Tool results sent in single user message: {len(tool_results)} results")
print("✓ No text before tool results in content array")
print("✓ Conversation formatted correctly for future parallel tool use")
```

```typescript TypeScript
#!/usr/bin/env node
// Test script to verify parallel tool calls with the Claude API

import { Anthropic } from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

// Define tools
const tools = [
  {
    name: "get_weather",
    description: "Get the current weather in a given location",
    input_schema: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "The city and state, e.g. San Francisco, CA"
        }
      },
      required: ["location"]
    }
  },
  {
    name: "get_time",
    description: "Get the current time in a given timezone",
    input_schema: {
      type: "object",
      properties: {
        timezone: {
          type: "string",
          description: "The timezone, e.g. America/New_York"
        }
      },
      required: ["timezone"]
    }
  }
];

async function testParallelTools() {
  // Make initial request
  console.log("Requesting parallel tool calls...");
  const response = await anthropic.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 1024,
    messages: [{
      role: "user",
      content: "What's the weather in SF and NYC, and what time is it there?"
    }],
    tools: tools
  });

  // Check for parallel tool calls
  const toolUses = response.content.filter(block => block.type === "tool_use");
  console.log(`\n✓ Claude made ${toolUses.length} tool calls`);

  if (toolUses.length > 1) {
    console.log("✓ Parallel tool calls detected!");
    toolUses.forEach(tool => {
      console.log(`  - ${tool.name}: ${JSON.stringify(tool.input)}`);
    });
  } else {
    console.log("✗ No parallel tool calls detected");
  }

  // Simulate tool execution and format results correctly
  const toolResults = toolUses.map(toolUse => {
    let result;
    if (toolUse.name === "get_weather") {
      result = toolUse.input.location.includes("San Francisco")
        ? "San Francisco: 68°F, partly cloudy"
        : "New York: 45°F, clear skies";
    } else {
      result = toolUse.input.timezone.includes("Los_Angeles")
        ? "2:30 PM PST"
        : "5:30 PM EST";
    }

    return {
      type: "tool_result",
      tool_use_id: toolUse.id,
      content: result
    };
  });

  // Get final response with correct formatting
  console.log("\nGetting final response...");
  const finalResponse = await anthropic.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "What's the weather in SF and NYC, and what time is it there?" },
      { role: "assistant", content: response.content },
      { role: "user", content: toolResults } // All results in one message!
    ],
    tools: tools
  });

  console.log(`\nClaude's response:\n${finalResponse.content[0].text}`);

  // Verify formatting
  console.log("\n--- Verification ---");
  console.log(`✓ Tool results sent in single user message: ${toolResults.length} results`);
  console.log("✓ No text before tool results in content array");
  console.log("✓ Conversation formatted correctly for future parallel tool use");
}

testParallelTools().catch(console.error);
```
</CodeGroup>

Skrip ini mendemonstrasikan:
- Cara memformat panggilan alat paralel dan hasil dengan benar
- Cara memverifikasi bahwa panggilan paralel sedang dilakukan
- Struktur pesan yang benar yang mendorong penggunaan alat paralel di masa depan
- Kesalahan umum yang harus dihindari (seperti teks sebelum hasil alat)

Jalankan skrip ini untuk menguji implementasi Anda dan memastikan Claude membuat panggilan alat paralel secara efektif.

</section>

#### Memaksimalkan penggunaan alat paralel

Meskipun model Claude 4 memiliki kemampuan penggunaan alat paralel yang sangat baik secara default, Anda dapat meningkatkan kemungkinan eksekusi alat paralel di semua model dengan prompting yang ditargetkan:

<section title="Prompt sistem untuk penggunaan alat paralel">

Untuk model Claude 4 (Opus 4, dan Sonnet 4), tambahkan ini ke prompt sistem Anda:
```text
For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
```

Untuk penggunaan alat paralel yang bahkan lebih kuat (direkomendasikan jika default tidak cukup), gunakan:
```text
<use_parallel_tool_calls>
For maximum efficiency, whenever you perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially. Prioritize calling tools in parallel whenever possible. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. When running multiple read-only commands like `ls` or `list_dir`, always run all of the commands in parallel. Err on the side of maximizing parallel tool calls rather than running too many tools sequentially.
</use_parallel_tool_calls>
```

</section>
<section title="Prompting pesan pengguna">

Anda juga dapat mendorong penggunaan alat paralel dalam pesan pengguna tertentu:

```python
# Instead of:
"What's the weather in Paris? Also check London."

# Use:
"Check the weather in Paris and London simultaneously."

# Or be explicit:
"Please use parallel tool calls to get the weather for Paris, London, and Tokyo at the same time."
```

</section>

<Warning>
**Penggunaan alat paralel dengan Claude Sonnet 3.7**

Claude Sonnet 3.7 mungkin kurang mungkin membuat panggilan alat paralel dalam respons, bahkan ketika Anda belum mengatur `disable_parallel_tool_use`. Kami merekomendasikan [upgrade ke model Claude 4](/docs/id/about-claude/models/migration-guide), yang memiliki penggunaan alat yang efisien token dan pemanggilan alat paralel yang ditingkatkan.

Jika Anda masih menggunakan Claude Sonnet 3.7, Anda dapat mengaktifkan [header beta](/docs/id/api/beta-headers) `token-efficient-tools-2025-02-19`, yang membantu mendorong Claude untuk menggunakan alat paralel. Anda juga dapat memperkenalkan "alat batch" yang dapat bertindak sebagai meta-alat untuk membungkus invokasi ke alat lain secara bersamaan.

Lihat [contoh ini](https://platform.claude.com/cookbook/tool-use-parallel-tools) dalam cookbook kami untuk cara menggunakan solusi ini.

</Warning>

## Menangani blok konten penggunaan alat dan hasil alat

<Note>
**Lebih sederhana dengan Tool runner**: Penanganan alat manual yang dijelaskan di bagian ini secara otomatis dikelola oleh [tool runner](#tool-runner-beta). Gunakan bagian ini ketika Anda memerlukan kontrol khusus atas eksekusi alat.
</Note>

Respons Claude berbeda berdasarkan apakah menggunakan alat klien atau alat server.

### Menangani hasil dari alat klien

Respons akan memiliki `stop_reason` dari `tool_use` dan satu atau lebih blok konten `tool_use` yang mencakup:

- `id`: Pengenal unik untuk blok penggunaan alat tertentu ini. Ini akan digunakan untuk mencocokkan hasil alat nanti.
- `name`: Nama alat yang digunakan.
- `input`: Objek yang berisi input yang diteruskan ke alat, sesuai dengan `input_schema` alat.

<section title="Contoh respons API dengan blok konten `tool_use`">

```json JSON
{
  "id": "msg_01Aq9w938a90dw8q",
  "model": "claude-opus-4-6",
  "stop_reason": "tool_use",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll check the current weather in San Francisco for you."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "get_weather",
      "input": {"location": "San Francisco, CA", "unit": "celsius"}
    }
  ]
}
```

</section>

Ketika Anda menerima respons penggunaan alat untuk alat klien, Anda harus:

1. Ekstrak `name`, `id`, dan `input` dari blok `tool_use`.
2. Jalankan alat aktual dalam codebase Anda yang sesuai dengan nama alat tersebut, meneruskan `input` alat.
3. Lanjutkan percakapan dengan mengirim pesan baru dengan `role` dari `user`, dan blok `content` yang berisi jenis `tool_result` dan informasi berikut:
   - `tool_use_id`: `id` dari permintaan penggunaan alat ini adalah hasil untuk.
   - `content`: Hasil alat, sebagai string (misalnya, `"content": "15 degrees"`), daftar blok konten bersarang (misalnya, `"content": [{"type": "text", "text": "15 degrees"}]`), atau daftar blok dokumen (misalnya, `"content": ["type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "15 degrees"}]`). Blok konten ini dapat menggunakan jenis `text`, `image`, atau `document`.
   - `is_error` (opsional): Atur ke `true` jika eksekusi alat menghasilkan kesalahan.

<Note>
**Persyaratan pemformatan penting**:
- Blok hasil alat harus segera mengikuti blok penggunaan alat yang sesuai dalam riwayat pesan. Anda tidak dapat menyertakan pesan apa pun antara pesan penggunaan alat asisten dan pesan hasil alat pengguna.
- Dalam pesan pengguna yang berisi hasil alat, blok tool_result harus datang PERTAMA dalam array konten. Teks apa pun harus datang SETELAH semua hasil alat.

Misalnya, ini akan menyebabkan kesalahan 400:
```json
{"role": "user", "content": [
  {"type": "text", "text": "Here are the results:"},  // ❌ Text before tool_result
  {"type": "tool_result", "tool_use_id": "toolu_01", ...}
]}
```

Ini benar:
```json
{"role": "user", "content": [
  {"type": "tool_result", "tool_use_id": "toolu_01", ...},
  {"type": "text", "text": "What should I do next?"}  // ✅ Text after tool_result
]}
```

Jika Anda menerima kesalahan seperti "tool_use ids were found without tool_result blocks immediately after", periksa bahwa hasil alat Anda diformat dengan benar.
</Note>

<section title="Contoh hasil alat yang berhasil">

```json JSON
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

</section>

<section title="Contoh hasil alat dengan gambar">

```json JSON
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": [
        {"type": "text", "text": "15 degrees"},
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": "/9j/4AAQSkZJRg...",
          }
        }
      ]
    }
  ]
}
```

</section>
<section title="Contoh hasil alat kosong">

```json JSON
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
    }
  ]
}
```

</section>

<section title="Contoh hasil alat dengan dokumen">

```json JSON
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": [
        {"type": "text", "text": "The weather is"},
        {
          "type": "document",
          "source": {
            "type": "text",
            "media_type": "text/plain",
            "data": "15 degrees"
          }
        }
      ]
    }
  ]
}
```

</section>

Setelah menerima hasil alat, Claude akan menggunakan informasi tersebut untuk melanjutkan menghasilkan respons terhadap prompt pengguna asli.

### Menangani hasil dari alat server

Claude mengeksekusi alat secara internal dan menggabungkan hasil langsung ke dalam responsnya tanpa memerlukan interaksi pengguna tambahan.

<Tip>
  **Perbedaan dari API lain**

Tidak seperti API yang memisahkan penggunaan alat atau menggunakan peran khusus seperti `tool` atau `function`, API Claude mengintegrasikan alat langsung ke dalam struktur pesan `user` dan `assistant`.

Pesan berisi array blok `text`, `image`, `tool_use`, dan `tool_result`. Pesan `user` mencakup konten klien dan `tool_result`, sementara pesan `assistant` berisi konten yang dihasilkan AI dan `tool_use`.

</Tip>

### Menangani alasan penghentian `max_tokens`

Jika [respons Claude terpotong karena mencapai batas `max_tokens`](/docs/id/build-with-claude/handling-stop-reasons#max-tokens), dan respons terpotong berisi blok penggunaan alat yang tidak lengkap, Anda perlu mengulangi permintaan dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan penggunaan alat lengkap.

<CodeGroup>
```python Python
# Check if response was truncated during tool use
if response.stop_reason == "max_tokens":
    # Check if the last content block is an incomplete tool_use
    last_block = response.content[-1]
    if last_block.type == "tool_use":
        # Send the request with higher max_tokens
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,  # Increased limit
            messages=messages,
            tools=tools,
        )
```

```typescript TypeScript
// Check if response was truncated during tool use
if (response.stop_reason === "max_tokens") {
  // Check if the last content block is an incomplete tool_use
  const lastBlock = response.content[response.content.length - 1];
  if (lastBlock.type === "tool_use") {
    // Send the request with higher max_tokens
    response = await anthropic.messages.create({
      model: "claude-opus-4-6",
      max_tokens: 4096, // Increased limit
      messages: messages,
      tools: tools
    });
  }
}
```
</CodeGroup>

#### Menangani alasan penghentian `pause_turn`

Saat menggunakan alat server seperti pencarian web, API dapat mengembalikan alasan penghentian `pause_turn`, menunjukkan bahwa API telah menjeda giliran yang berjalan lama.

Berikut cara menangani alasan penghentian `pause_turn`:

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

# Initial request with web search
response = client.messages.create(
    model="claude-3-7-sonnet-latest",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Search for comprehensive information about quantum computing breakthroughs in 2025",
        }
    ],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}],
)

# Check if the response has pause_turn stop reason
if response.stop_reason == "pause_turn":
    # Continue the conversation with the paused content
    messages = [
        {
            "role": "user",
            "content": "Search for comprehensive information about quantum computing breakthroughs in 2025",
        },
        {"role": "assistant", "content": response.content},
    ]

    # Send the continuation request
    continuation = client.messages.create(
        model="claude-3-7-sonnet-latest",
        max_tokens=1024,
        messages=messages,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}],
    )

    print(continuation)
else:
    print(response)
```

```typescript TypeScript
import { Anthropic } from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

// Initial request with web search
const response = await anthropic.messages.create({
  model: "claude-3-7-sonnet-latest",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: "Search for comprehensive information about quantum computing breakthroughs in 2025"
    }
  ],
  tools: [{
    type: "web_search_20250305",
    name: "web_search",
    max_uses: 10
  }]
});

// Check if the response has pause_turn stop reason
if (response.stop_reason === "pause_turn") {
  // Continue the conversation with the paused content
  const messages = [
    { role: "user", content: "Search for comprehensive information about quantum computing breakthroughs in 2025" },
    { role: "assistant", content: response.content }
  ];

  // Send the continuation request
  const continuation = await anthropic.messages.create({
    model: "claude-3-7-sonnet-latest",
    max_tokens: 1024,
    messages: messages,
    tools: [{
      type: "web_search_20250305",
      name: "web_search",
      max_uses: 10
    }]
  });

  console.log(continuation);
} else {
  console.log(response);
}
```
</CodeGroup>

Saat menangani `pause_turn`:
- **Lanjutkan percakapan**: Teruskan respons yang dijeda kembali apa adanya dalam permintaan berikutnya untuk membiarkan Claude melanjutkan gilirannya
- **Ubah jika diperlukan**: Anda dapat secara opsional mengubah konten sebelum melanjutkan jika Anda ingin mengganggu atau mengarahkan kembali percakapan
- **Pertahankan status alat**: Sertakan alat yang sama dalam permintaan lanjutan untuk mempertahankan fungsionalitas

## Pemecahan masalah kesalahan

<Note>
**Penanganan Kesalahan Bawaan**: [Tool runner](#tool-runner-beta) menyediakan penanganan kesalahan otomatis untuk sebagian besar skenario umum. Bagian ini mencakup penanganan kesalahan manual untuk kasus penggunaan lanjutan.
</Note>

Ada beberapa jenis kesalahan berbeda yang dapat terjadi saat menggunakan alat dengan Claude:

<section title="Kesalahan eksekusi alat">

Jika alat itu sendiri melempar kesalahan selama eksekusi (misalnya, kesalahan jaringan saat mengambil data cuaca), Anda dapat mengembalikan pesan kesalahan dalam `content` bersama dengan `"is_error": true`:

```json JSON
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

Claude kemudian akan menggabungkan kesalahan ini ke dalam responsnya kepada pengguna. Misalnya: "Maaf, saya tidak dapat mengambil cuaca saat ini karena API layanan cuaca tidak tersedia. Silakan coba lagi nanti."

</section>
<section title="Nama alat tidak valid">

Jika penggunaan alat yang dicoba oleh Claude tidak valid (misalnya, parameter yang diperlukan hilang), biasanya berarti tidak ada cukup informasi bagi Claude untuk menggunakan alat dengan benar. Taruhan terbaik Anda selama pengembangan adalah mencoba permintaan lagi dengan nilai `description` yang lebih terperinci dalam definisi alat Anda.

Namun, Anda juga dapat melanjutkan percakapan maju dengan `tool_result` yang menunjukkan kesalahan, dan Claude akan mencoba menggunakan alat lagi dengan informasi yang hilang diisi:

```json JSON
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Missing required 'location' parameter",
      "is_error": true
    }
  ]
}
```

Jika permintaan alat tidak valid atau parameter hilang, Claude akan mencoba 2-3 kali dengan koreksi sebelum meminta maaf kepada pengguna.

<Tip>
Untuk menghilangkan panggilan alat yang tidak valid sepenuhnya, gunakan [penggunaan alat ketat](/docs/id/build-with-claude/structured-outputs) dengan `strict: true` pada definisi alat Anda. Ini menjamin bahwa input alat akan selalu sesuai dengan skema Anda dengan tepat, mencegah parameter yang hilang dan ketidakcocokan tipe.
</Tip>

</section>
<section title="Tag \<search_quality_reflection>">

Untuk mencegah Claude dari mencerminkan kualitas hasil pencarian dengan tag \<search_quality_reflection>, tambahkan "Do not reflect on the quality of the returned search results in your response" ke prompt Anda.

</section>
<section title="Kesalahan alat server">

Ketika alat server mengalami kesalahan (misalnya, masalah jaringan dengan Pencarian Web), Claude akan menangani kesalahan ini secara transparan dan mencoba memberikan respons alternatif atau penjelasan kepada pengguna. Tidak seperti alat klien, Anda tidak perlu menangani hasil `is_error` untuk alat server.

Untuk pencarian web khususnya, kode kesalahan yang mungkin termasuk:
- `too_many_requests`: Batas laju terlampaui
- `invalid_input`: Parameter kueri pencarian tidak valid
- `max_uses_exceeded`: Penggunaan alat pencarian web maksimum terlampaui
- `query_too_long`: Kueri melebihi panjang maksimum
- `unavailable`: Kesalahan internal terjadi

</section>
<section title="Penggunaan alat paralel tidak berfungsi">

Jika Claude tidak membuat panggilan alat paralel saat diharapkan, periksa masalah umum ini:

**1. Pemformatan hasil alat yang tidak benar**

Masalah paling umum adalah memformat hasil alat secara tidak benar dalam riwayat percakapan. Ini "mengajarkan" Claude untuk menghindari panggilan paralel.

Khusus untuk penggunaan alat paralel:
- ❌ **Salah**: Mengirim pesan pengguna terpisah untuk setiap hasil alat
- ✅ **Benar**: Semua hasil alat harus dalam satu pesan pengguna

```json
// ❌ This reduces parallel tool use
[
  {"role": "assistant", "content": [tool_use_1, tool_use_2]},
  {"role": "user", "content": [tool_result_1]},
  {"role": "user", "content": [tool_result_2]}  // Separate message
]

// ✅ This maintains parallel tool use
[
  {"role": "assistant", "content": [tool_use_1, tool_use_2]},
  {"role": "user", "content": [tool_result_1, tool_result_2]}  // Single message
]
```

Lihat [persyaratan pemformatan umum di atas](#handling-tool-use-and-tool-result-content-blocks) untuk aturan pemformatan lainnya.

**2. Prompting yang lemah**

Prompting default mungkin tidak cukup. Gunakan bahasa yang lebih kuat:

```text
<use_parallel_tool_calls>
For maximum efficiency, whenever you perform multiple independent operations,
invoke all relevant tools simultaneously rather than sequentially.
Prioritize calling tools in parallel whenever possible.
</use_parallel_tool_calls>
```

**3. Mengukur penggunaan alat paralel**

Untuk memverifikasi panggilan alat paralel berfungsi:

```python
# Calculate average tools per tool-calling message
tool_call_messages = [
    msg for msg in messages if any(block.type == "tool_use" for block in msg.content)
]
total_tool_calls = sum(
    len([b for b in msg.content if b.type == "tool_use"]) for msg in tool_call_messages
)
avg_tools_per_message = total_tool_calls / len(tool_call_messages)
print(f"Average tools per message: {avg_tools_per_message}")
# Should be > 1.0 if parallel calls are working
```

**4. Perilaku khusus model**

- Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5, Opus 4.5, Opus 4.1, dan Sonnet 4: Unggul dalam penggunaan alat paralel dengan prompting minimal
- Claude Sonnet 3.7: Mungkin memerlukan prompting yang lebih kuat atau [header beta](/docs/id/api/beta-headers) `token-efficient-tools-2025-02-19`. Pertimbangkan [upgrade ke Claude 4](/docs/id/about-claude/models/migration-guide).
- Claude Haiku: Kurang mungkin menggunakan alat paralel tanpa prompting eksplisit

</section>