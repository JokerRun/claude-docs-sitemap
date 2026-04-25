---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner
fetched_at: 2026-04-25T03:09:48.142425Z
sha256: 6ba333a7d7c99e377f1bff09f29091a5acbbb9ba4bc274cb43f81091c4b294c4
---

# Tool Runner (SDK)

Gunakan abstraksi Tool Runner SDK untuk menangani loop agentic, pembungkus error, dan keamanan tipe secara otomatis.

---

Tool Runner menangani loop agentic, pembungkus error, dan keamanan tipe sehingga Anda tidak perlu melakukannya. Gunakan [loop manual](/docs/id/agents-and-tools/tool-use/handle-tool-calls) hanya ketika Anda memerlukan persetujuan manusia-dalam-loop, logging khusus, atau eksekusi bersyarat. Tersedia di Python, TypeScript, dan Ruby SDKs.

Tool runner menyediakan solusi siap pakai untuk menjalankan tools dengan Claude. Alih-alih menangani tool calls, hasil tool, dan manajemen percakapan secara manual, tool runner secara otomatis:

- Menjalankan tools ketika Claude memanggilnya
- Menangani siklus permintaan/respons
- Mengelola status percakapan
- Menyediakan keamanan tipe dan validasi

Gunakan tool runner untuk sebagian besar implementasi tool use.

<Note>
Tool runner saat ini dalam beta dan tersedia di [Python](https://github.com/anthropics/anthropic-sdk-python/blob/main/tools.md), [TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/helpers.md#tool-helpers), dan [Ruby](https://github.com/anthropics/anthropic-sdk-ruby/blob/main/helpers.md#3-auto-looping-tool-runner-beta) SDKs.
</Note>

<Tip>
**Manajemen konteks otomatis dengan pemadatan**

Tool runner mendukung [pemadatan](/docs/id/build-with-claude/context-editing#client-side-compaction-sdk) otomatis, yang menghasilkan ringkasan ketika penggunaan token melebihi ambang batas. Ini memungkinkan tugas agentic jangka panjang untuk melanjutkan melampaui batas jendela konteks.
</Tip>

## Penggunaan dasar

Tentukan tools menggunakan helper SDK, kemudian gunakan tool runner untuk menjalankannya.

<Tabs>
<Tab title="Python">

Gunakan dekorator `@beta_tool` untuk mendefinisikan tools dengan type hints dan docstrings.

<Note>
Jika Anda menggunakan async client, ganti `@beta_tool` dengan `@beta_async_tool` dan tentukan fungsi dengan `async def`.
</Note>

```python
import json
from anthropic import Anthropic, beta_tool

client = Anthropic()


@beta_tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a given location.

    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: Temperature unit, either 'celsius' or 'fahrenheit'
    """
    return json.dumps({"temperature": "20°C", "condition": "Sunny"})


@beta_tool
def calculate_sum(a: int, b: int) -> str:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number
    """
    return str(a + b)


runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
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
    print(message)
```

Dekorator `@beta_tool` memeriksa argumen fungsi dan docstring untuk mengekstrak representasi skema JSON. Misalnya, `calculate_sum` menjadi:

```json
{
  "name": "calculate_sum",
  "description": "Add two numbers together.",
  "input_schema": {
    "additionalProperties": false,
    "properties": {
      "a": {
        "description": "First number",
        "title": "A",
        "type": "integer"
      },
      "b": {
        "description": "Second number",
        "title": "B",
        "type": "integer"
      }
    },
    "required": ["a", "b"],
    "type": "object"
  }
}
```

</Tab>
<Tab title="TypeScript">

Gunakan `betaZodTool()` untuk definisi tool yang aman tipe dengan validasi Zod, atau `betaTool()` untuk definisi berbasis JSON Schema.

TypeScript menawarkan dua pendekatan untuk mendefinisikan tools:

**Menggunakan Zod (direkomendasikan)** - Gunakan `betaZodTool()` untuk definisi tool yang aman tipe dengan validasi Zod (memerlukan Zod 3.25.0 atau lebih tinggi):

```typescript hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const client = new Anthropic();

const getWeatherTool = betaZodTool({
  name: "get_weather",
  description: "Get the current weather in a given location",
  inputSchema: z.object({
    location: z.string().describe("The city and state, e.g. San Francisco, CA"),
    unit: z.enum(["celsius", "fahrenheit"]).default("fahrenheit").describe("Temperature unit")
  }),
  run: async (input) => {
    return JSON.stringify({ temperature: "20°C", condition: "Sunny" });
  }
});

const finalMessage = await client.beta.messages.toolRunner({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [getWeatherTool],
  messages: [{ role: "user", content: "What's the weather like in Paris?" }]
});

for (const block of finalMessage.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

**Menggunakan JSON Schema** - Gunakan `betaTool()` untuk definisi tool yang aman tipe tanpa Zod:

<Note>
Input yang dihasilkan oleh Claude tidak akan divalidasi pada runtime. Lakukan validasi di dalam fungsi `run` jika diperlukan.
</Note>

```typescript hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import { betaTool } from "@anthropic-ai/sdk/helpers/beta/json-schema";

const client = new Anthropic();

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

const finalMessage = await client.beta.messages.toolRunner({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [calculateSumTool],
  messages: [{ role: "user", content: "What's 15 + 27?" }]
});

for (const block of finalMessage.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

</Tab>
<Tab title="Ruby">

Gunakan kelas `Anthropic::BaseTool` untuk mendefinisikan tools dengan skema input yang diketik.

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
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [GetWeather.new, CalculateSum.new],
  messages: [
    {role: "user", content: "What's the weather like in Paris? Also, what's 15 + 27?"}
  ]
)

runner.each_message do |message|
  message.content.each do |block|
    puts block.text if block.type == :text
  end
end
```

Kelas `Anthropic::BaseTool` menggunakan metode `doc` untuk deskripsi tool dan `input_schema` untuk mendefinisikan parameter yang diharapkan. SDK secara otomatis mengonversi ini ke format skema JSON yang sesuai.

</Tab>
</Tabs>

Fungsi tool harus mengembalikan blok konten atau array blok konten, termasuk teks, gambar, atau blok dokumen. Ini memungkinkan tools untuk mengembalikan respons kaya dan multimodal. String yang dikembalikan akan dikonversi ke blok konten teks. Jika Anda ingin mengembalikan objek JSON terstruktur ke Claude, enkode ke string JSON sebelum mengembalikannya. Angka, boolean, atau primitif non-string lainnya juga harus dikonversi ke string.

## Iterasi di atas tool runner

Tool runner adalah iterable yang menghasilkan pesan dari Claude. Ini sering disebut sebagai "tool call loop". Setiap iterasi, runner memeriksa apakah Claude meminta penggunaan tool. Jika ya, ia memanggil tool dan mengirim hasilnya kembali ke Claude secara otomatis, kemudian menghasilkan pesan berikutnya dari Claude untuk melanjutkan loop Anda.

Anda dapat mengakhiri loop di iterasi mana pun dengan pernyataan `break`. Runner akan loop sampai Claude mengembalikan pesan tanpa penggunaan tool.

Jika Anda tidak memerlukan pesan perantara, Anda dapat mendapatkan pesan final secara langsung:

<Tabs>
<Tab title="Python">

Gunakan `runner.until_done()` untuk mendapatkan pesan final.

```python hidelines={1..16}
import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()


@beta_tool
def get_weather(location: str) -> str:
    """Get the current weather in a given location."""
    return "20°C, Sunny"


@beta_tool
def calculate_sum(a: int, b: int) -> str:
    """Add two numbers together."""
    return str(a + b)


runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
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

Cukup `await` runner untuk mendapatkan pesan final.

```typescript hidelines={1..13}
import Anthropic from "@anthropic-ai/sdk";
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const client = new Anthropic();

const getWeatherTool = betaZodTool({
  name: "get_weather",
  description: "Get the current weather in a given location",
  inputSchema: z.object({ location: z.string() }),
  run: async () => JSON.stringify({ temperature: "20°C", condition: "Sunny" })
});

const runner = client.beta.messages.toolRunner({
  model: "claude-opus-4-7",
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

```ruby hidelines={1..25}
class GetWeatherInput < Anthropic::BaseModel
  required :location, String
end

class GetWeather < Anthropic::BaseTool
  doc "Get the current weather in a given location"
  input_schema GetWeatherInput
  def call(input)
    "Weather in #{input.location}: 20°C, Sunny"
  end
end

class CalculateSumInput < Anthropic::BaseModel
  required :a, Integer
  required :b, Integer
end

class CalculateSum < Anthropic::BaseTool
  doc "Add two numbers together"
  input_schema CalculateSumInput
  def call(input)
    (input.a + input.b).to_s
  end
end

runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-7",
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

## Penggunaan lanjutan

Dalam loop, Anda dapat sepenuhnya menyesuaikan permintaan berikutnya tool runner ke Messages API. Runner secara otomatis menambahkan hasil tool ke riwayat pesan, jadi Anda tidak perlu mengelolanya secara manual. Anda dapat secara opsional memeriksa hasil tool untuk logging atau debugging, dan memodifikasi parameter permintaan sebelum panggilan API berikutnya.

<Tabs>
<Tab title="Python">

Gunakan `generate_tool_call_response()` untuk secara opsional memeriksa hasil tool (runner menambahkannya secara otomatis). Gunakan `set_messages_params()` dan `append_messages()` untuk memodifikasi permintaan.

```python nocheck
runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
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

Gunakan `generateToolResponse()` untuk secara opsional memeriksa hasil tool (runner menambahkannya secara otomatis). Gunakan `setMessagesParams()` dan `pushMessages()` untuk memodifikasi permintaan.

```typescript nocheck
const runner = client.beta.messages.toolRunner({
  model: "claude-opus-4-7",
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
  runner.setMessagesParams((params) => ({
    ...params,
    max_tokens: 2048 // Increase tokens for next request
  }));

  // Or add additional messages
  runner.pushMessages({ role: "user", content: "Please be concise in your response." });
}
```

</Tab>
<Tab title="Ruby">

Gunakan `next_message` untuk kontrol langkah demi langkah. Gunakan `feed_messages` untuk menyuntikkan pesan dan `params` untuk mengakses parameter.

```ruby hidelines={1..12}
class GetWeatherInput < Anthropic::BaseModel
  required :location, String
end

class GetWeather < Anthropic::BaseTool
  doc "Get the current weather in a given location"
  input_schema GetWeatherInput
  def call(input)
    "Weather in #{input.location}: 20°C, Sunny"
  end
end

runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-7",
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

### Debugging eksekusi tool

Ketika tool melempar pengecualian, tool runner menangkapnya dan mengembalikan error ke Claude sebagai hasil tool dengan `is_error: true`. Secara default, hanya pesan pengecualian yang disertakan, bukan stack trace lengkap.

Untuk melihat stack trace lengkap dan informasi debug, atur variabel lingkungan `ANTHROPIC_LOG`:

```bash
# View info-level logs including tool errors
export ANTHROPIC_LOG=info

# View debug-level logs for more verbose output
export ANTHROPIC_LOG=debug
```

Ketika diaktifkan, SDK mencatat detail pengecualian lengkap (menggunakan modul `logging` Python, konsol di TypeScript, atau logger Ruby), termasuk stack trace lengkap ketika tool gagal.

### Mengintersepsi error tool

Secara default, error tool diteruskan kembali ke Claude, yang kemudian dapat merespons dengan tepat. Namun, Anda mungkin ingin mendeteksi error dan menanganinya secara berbeda, misalnya, untuk menghentikan eksekusi lebih awal atau menerapkan penanganan error khusus.

Gunakan metode respons tool untuk mengintersepsi hasil tool dan memeriksa error sebelum dikirim ke Claude:

<Tabs>
<Tab title="Python">

```python hidelines={1..11}
import anthropic
import json
from anthropic import beta_tool

client = anthropic.Anthropic()


@beta_tool
def my_tool(query: str) -> str:
    """A sample tool."""
    return f"Result for: {query}"


runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[my_tool],
    messages=[{"role": "user", "content": "Run the tool"}],
)

for message in runner:
    tool_response = runner.generate_tool_call_response()

    if tool_response is not None:
        # tool_response is a dict: {"role": "user", "content": [...]}
        # Check if any tool result has an error
        for block in tool_response["content"]:
            if block.get("is_error"):
                # Option 1: Raise an exception to stop the loop
                raise RuntimeError(f"Tool failed: {json.dumps(block['content'])}")

                # Option 2: Log and continue (let Claude handle it)
                # logger.error(f"Tool error: {json.dumps(block['content'])}")

    # Process the message normally
    print(message.content)
```

</Tab>
<Tab title="TypeScript">

```typescript hidelines={1..13}
import Anthropic from "@anthropic-ai/sdk";
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const client = new Anthropic();

const myTool = betaZodTool({
  name: "my_tool",
  description: "A sample tool",
  inputSchema: z.object({ query: z.string() }),
  run: async (input) => `Result for: ${input.query}`
});

const runner = client.beta.messages.toolRunner({
  model: "claude-opus-4-7",
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

```ruby hidelines={1..12}
class MyToolInput < Anthropic::BaseModel
  required :query, String
end

class MyTool < Anthropic::BaseTool
  doc "A sample tool"
  input_schema MyToolInput
  def call(input)
    "Result for: #{input.query}"
  end
end

runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [MyTool.new],
  messages: [{role: "user", content: "Run the tool"}]
)

runner.each_message do |message|
  # Get the tool response to check for errors
  # Note: The runner automatically handles tool execution and appends results
  # This is just for error checking/logging purposes
  tool_results = runner.params[:messages].last

  if tool_results && tool_results[:role] == :user && tool_results[:content].is_a?(Array)
    tool_results[:content].each do |block|
      if block[:type] == :tool_result && block[:is_error]
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

### Memodifikasi hasil tool

Anda dapat memodifikasi hasil tool sebelum dikirim kembali ke Claude. Ini berguna untuk menambahkan metadata seperti `cache_control` untuk mengaktifkan [prompt caching](/docs/id/build-with-claude/prompt-caching) pada hasil tool, atau untuk mengubah output tool.

Gunakan metode respons tool untuk mendapatkan hasil tool, kemudian modifikasi sebelum runner melanjutkan. Apakah Anda secara eksplisit menambahkan hasil yang dimodifikasi atau memutasinya di tempat tergantung pada SDK; lihat komentar kode di setiap tab.

<Tabs>
<Tab title="Python">

```python hidelines={1..10}
import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()


@beta_tool
def search_documents(query: str) -> str:
    """Search documents for relevant information."""
    return f"Found 3 documents matching: {query}"


runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
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

    if tool_response is not None:
        # tool_response is a dict: {"role": "user", "content": [...]}
        # Modify the tool result to add cache control
        for block in tool_response["content"]:
            if block["type"] == "tool_result":
                # Add cache_control to cache this tool result
                block["cache_control"] = {"type": "ephemeral"}

        # Append the modified response (this prevents auto-append of the original)
        runner.append_messages(message, tool_response)

    print(message.content)
```

</Tab>
<Tab title="TypeScript">

```typescript hidelines={1..13}
import Anthropic from "@anthropic-ai/sdk";
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const client = new Anthropic();

const searchDocuments = betaZodTool({
  name: "search_documents",
  description: "Search documents for relevant information",
  inputSchema: z.object({ query: z.string() }),
  run: async (input) => `Found 3 documents matching: ${input.query}`
});

const runner = client.beta.messages.toolRunner({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [searchDocuments],
  messages: [
    { role: "user", content: "Search for information about the climate of San Francisco" }
  ]
});

for await (const message of runner) {
  const toolResultMessage = await runner.generateToolResponse();

  if (toolResultMessage && typeof toolResultMessage.content !== "string") {
    // Modify the tool result to add cache control
    for (const block of toolResultMessage.content) {
      if (block.type === "tool_result") {
        // Add cache_control to cache this tool result
        block.cache_control = { type: "ephemeral" };
      }
    }
    // No pushMessages call needed: the runner auto-appends both the assistant
    // message and the (now-mutated) cached tool response.
  }

  console.log(message.content);
}
```

</Tab>
<Tab title="Ruby">

```ruby hidelines={1..12}
class SearchDocumentsInput < Anthropic::BaseModel
  required :query, String
end

class SearchDocuments < Anthropic::BaseTool
  doc "Search documents for relevant information"
  input_schema SearchDocumentsInput
  def call(input)
    "Found 3 documents matching: #{input.query}"
  end
end

runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-7",
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

  if tool_results_message && tool_results_message[:role] == :user
    tool_results_message[:content].each do |block|
      if block[:type] == :tool_result
        # Modify the tool result to add cache control
        block[:cache_control] = {type: "ephemeral"}
      end
    end
  end

  puts message.content
  break if message.stop_reason != :tool_use
end
```

</Tab>
</Tabs>

<Tip>
Menambahkan `cache_control` ke hasil tool sangat berguna ketika tools mengembalikan jumlah data besar (seperti hasil pencarian dokumen) yang ingin Anda cache untuk panggilan API berikutnya. Lihat [Prompt caching](/docs/id/build-with-claude/prompt-caching) untuk detail lebih lanjut tentang strategi caching.
</Tip>

## Streaming

Aktifkan streaming untuk menerima event saat tiba. Setiap iterasi menghasilkan objek stream yang dapat Anda iterasi untuk event.

<Tabs>
<Tab title="Python">

Atur `stream=True` dan gunakan `get_final_message()` untuk mendapatkan pesan yang terakumulasi.

```python hidelines={1..10}
import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()


@beta_tool
def calculate_sum(a: int, b: int) -> str:
    """Add two numbers together."""
    return str(a + b)


runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
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

```typescript hidelines={1..13}
import Anthropic from "@anthropic-ai/sdk";
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const client = new Anthropic();

const getWeatherTool = betaZodTool({
  name: "get_weather",
  description: "Get the current weather in a given location",
  inputSchema: z.object({ location: z.string() }),
  run: async () => JSON.stringify({ temperature: "20°C", condition: "Sunny" })
});

const runner = client.beta.messages.toolRunner({
  model: "claude-opus-4-7",
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

Gunakan `each_streaming` untuk iterasi di atas event streaming.

```ruby hidelines={1..13}
class CalculateSumInput < Anthropic::BaseModel
  required :a, Integer
  required :b, Integer
end

class CalculateSum < Anthropic::BaseTool
  doc "Add two numbers together"
  input_schema CalculateSumInput
  def call(input)
    (input.a + input.b).to_s
  end
end

runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [CalculateSum.new],
  messages: [{role: "user", content: "What is 15 + 27?"}]
)

runner.each_streaming do |event|
  case event
  when Anthropic::Streaming::TextEvent
    print event.text
  when Anthropic::Streaming::InputJsonEvent
    puts "\nTool input: #{event.partial_json}"
  end
end
```

</Tab>
</Tabs>

## Langkah berikutnya

- Untuk kontrol manual atas loop tool-call, lihat [Handle tool calls](/docs/id/agents-and-tools/tool-use/handle-tool-calls).
- Untuk menjalankan multiple tools secara bersamaan, lihat [Parallel tool use](/docs/id/agents-and-tools/tool-use/parallel-tool-use).
- Untuk workflow tool-use lengkap, lihat [Define tools](/docs/id/agents-and-tools/tool-use/define-tools).