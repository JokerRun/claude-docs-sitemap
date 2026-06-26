---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: 28e27d2ff00c6e2c57f126c49bb1ec34e4f37cb3529d362692b7485c0d4efbae
---

# Penggunaan alat dengan Claude

Hubungkan Claude ke alat dan API eksternal. Pelajari di mana alat dieksekusi dan bagaimana loop agentik bekerja.

---

"Tool use" (penggunaan alat) memungkinkan Claude memanggil fungsi yang Anda definisikan atau yang disediakan oleh Anthropic. Claude memutuskan kapan harus memanggil alat berdasarkan permintaan pengguna dan deskripsi alat tersebut, lalu mengembalikan panggilan terstruktur yang dieksekusi oleh aplikasi Anda (alat klien) atau yang dieksekusi oleh Anthropic (alat server).

Berikut adalah contoh paling sederhana menggunakan alat server, di mana Anthropic menangani eksekusinya:

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "tools": [{"type": "web_search_20260209", "name": "web_search"}],
    "messages": [{"role": "user", "content": "What'\''s the latest on the Mars rover?"}]
  }'
```

```bash CLI
ant messages create --transform content --format yaml \
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --tool '{type: web_search_20260209, name: web_search}' \
  --message '{role: user, content: "What is the latest on the Mars rover?"}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[{"type": "web_search_20260209", "name": "web_search"}],
    messages=[{"role": "user", "content": "What's the latest on the Mars rover?"}],
)
print(response.content)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [{ type: "web_search_20260209", name: "web_search" }],
  messages: [{ role: "user", content: "What's the latest on the Mars rover?" }]
});
console.log(response.content);
```

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Tools = [new ToolUnion(new WebSearchTool20260209())],
    Messages = [new() { Role = Role.User, Content = "What's the latest on the Mars rover?" }]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message.Content);
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Tools: []anthropic.ToolUnionParam{
			{OfWebSearchTool20260209: &anthropic.WebSearchTool20260209Param{}},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What's the latest on the Mars rover?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Content)
}
```

```java Java hidelines={1..5}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.WebSearchTool20260209;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024L)
        .addTool(WebSearchTool20260209.builder().build())
        .addUserMessage("What's the latest on the Mars rover?")
        .build();

    Message response = client.messages().create(params);
    IO.println(response.content());
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    model: 'claude-opus-4-8',
    maxTokens: 1024,
    tools: [
        ['type' => 'web_search_20260209', 'name' => 'web_search'],
    ],
    messages: [
        ['role' => 'user', 'content' => "What's the latest on the Mars rover?"],
    ],
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [{ type: "web_search_20260209", name: "web_search" }],
  messages: [{ role: "user", content: "What's the latest on the Mars rover?" }]
)
puts message.content
```
</CodeGroup>

---

## Cara kerja penggunaan alat \{#how-tool-use-works}

Alat dibedakan terutama berdasarkan di mana kodenya dieksekusi. **Alat klien** (termasuk alat yang didefinisikan pengguna dan alat dengan skema Anthropic seperti bash dan text_editor) berjalan di aplikasi Anda: Claude merespons dengan `stop_reason: "tool_use"` dan satu atau lebih blok `tool_use`, kode Anda mengeksekusi operasi tersebut, dan Anda mengirimkan kembali sebuah `tool_result`. **Alat server** (web_search, code_execution, web_fetch, tool_search) berjalan di infrastruktur Anthropic: Anda melihat hasilnya secara langsung tanpa perlu menangani eksekusi.

Untuk model konseptual lengkap termasuk loop agentik dan kapan harus memilih setiap pendekatan, lihat [Cara kerja penggunaan alat](/docs/id/agents-and-tools/tool-use/how-tool-use-works).

Untuk menghubungkan ke server MCP, lihat [konektor MCP](/docs/id/agents-and-tools/mcp-connector). Untuk membangun klien MCP Anda sendiri, lihat [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/develop/build-client).

<Tip>
**Jamin kesesuaian skema dengan penggunaan alat ketat**

Tambahkan `strict: true` ke definisi alat Anda untuk memastikan panggilan alat Claude selalu cocok persis dengan skema Anda. Lihat [Penggunaan alat ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use).
</Tip>

Akses ke alat adalah salah satu kemampuan paling efektif yang dapat Anda berikan kepada agen. Pada benchmark seperti [LAB-Bench FigQA](https://lab-bench.org/) (interpretasi gambar ilmiah) dan [SWE-bench](https://www.swebench.com/) (rekayasa perangkat lunak dunia nyata), menambahkan alat dasar sekalipun menghasilkan peningkatan besar, sering kali melampaui baseline pakar manusia.

---

## Kapan Claude menggunakan alat \{#when-claude-uses-tools}

Dengan `tool_choice` default `{"type": "auto"}`, Claude memutuskan pada setiap giliran apakah akan memanggil alat atau merespons secara langsung. Claude memanggil alat ketika permintaan sesuai dengan kemampuan yang dijelaskan alat tersebut dan jawabannya belum ada dalam konteks. Claude merespons secara langsung untuk pengetahuan yang stabil, tugas kreatif, dan giliran percakapan biasa.

Batasan ini dapat diarahkan melalui prompt sistem Anda. Jika Claude tidak memanggil alat saat Anda mengharapkannya, instruksi ringan seperti `"Use the tools to investigate before responding."` secara terukur meningkatkan penggunaan alat. Bentuk yang lebih kuat seperti `"Always call a tool first before responding."` mendorong lebih jauh lagi. Sebaliknya, `"Use your judgment about whether to call a tool or respond directly."` menjaga perilaku pemicuan tetap konservatif.

Untuk jaminan yang pasti alih-alih sekadar dorongan, gunakan [`tool_choice`](/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use).

Setiap halaman alat server menjelaskan batasan pemicunya sendiri secara lebih rinci. Lihat misalnya [alat pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) atau [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool).

---

## Contoh penggunaan alat \{#tool-use-examples}

Untuk panduan langsung yang lengkap, lihat [tutorial](/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent). Untuk contoh referensi dari konsep individual, lihat [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools) dan [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

<section title="Apa yang terjadi ketika Claude membutuhkan informasi lebih lanjut">

Jika prompt pengguna tidak menyertakan informasi yang cukup untuk mengisi semua parameter yang diperlukan untuk sebuah alat, Claude Opus jauh lebih mungkin mengenali bahwa ada parameter yang hilang dan menanyakannya. Claude Sonnet mungkin bertanya, terutama ketika diminta untuk berpikir sebelum mengeluarkan permintaan alat. Tetapi ia juga mungkin berusaha sebaik mungkin untuk menyimpulkan nilai yang masuk akal.

Misalnya, diberikan alat `get_weather` yang memerlukan parameter `location`, jika Anda bertanya kepada Claude "Bagaimana cuacanya?" tanpa menentukan lokasi, Claude (khususnya Claude Sonnet) mungkin menebak input alat:

```json JSON
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "get_weather",
  "input": { "location": "New York, NY", "unit": "fahrenheit" }
}
```

Perilaku ini tidak dijamin, terutama untuk prompt yang lebih ambigu dan untuk model yang kurang cerdas. Jika Claude Opus tidak memiliki konteks yang cukup untuk mengisi parameter yang diperlukan, ia jauh lebih mungkin merespons dengan pertanyaan klarifikasi alih-alih melakukan panggilan alat.

</section>

---

## Harga \{#pricing}

Permintaan penggunaan alat dikenakan biaya berdasarkan:
1. Jumlah total token input yang dikirim ke model (termasuk dalam parameter `tools`)
2. Jumlah token output yang dihasilkan
3. Untuk alat sisi server, biaya tambahan berbasis penggunaan (misalnya, pencarian web dikenakan biaya per pencarian yang dilakukan)

Alat sisi klien dikenakan biaya sama seperti permintaan API Claude lainnya, sementara alat sisi server dapat dikenakan biaya tambahan berdasarkan penggunaan spesifiknya.

Token tambahan dari penggunaan alat berasal dari:

- Parameter `tools` dalam permintaan API (nama alat, deskripsi, dan skema)
- Blok konten `tool_use` dalam permintaan dan respons API
- Blok konten `tool_result` dalam permintaan API

Ketika Anda menggunakan `tools`, API juga secara otomatis menyertakan prompt sistem khusus untuk model yang mengaktifkan penggunaan alat. Jumlah token penggunaan alat yang diperlukan untuk setiap model tercantum di bawah ini (tidak termasuk token tambahan yang tercantum di atas). Perhatikan bahwa tabel ini mengasumsikan setidaknya 1 alat disediakan. Jika tidak ada `tools` yang disediakan, maka pilihan alat `none` menggunakan 0 token prompt sistem tambahan.

| Model                    | Pilihan alat                                         | Jumlah token prompt sistem penggunaan alat  |
|--------------------------|------------------------------------------------------|---------------------------------------------|
| Claude Opus 4.8                | `auto`, `none`<hr />`any`, `tool`   | 290 token<hr />410 token |
| Claude Opus 4.7                | `auto`, `none`<hr />`any`, `tool`   | 675 token<hr />804 token |
| Claude Opus 4.6              | `auto`, `none`<hr />`any`, `tool`   | 497 token<hr />589 token |
| Claude Opus 4.5            | `auto`, `none`<hr />`any`, `tool`   | 496 token<hr />588 token |
| Claude Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)) | `auto`, `none`<hr />`any`, `tool`   | 313 token<hr />315 token |
| Claude Opus 4 ([dihentikan, kecuali di Vertex AI](/docs/id/about-claude/model-deprecations)) | `auto`, `none`<hr />`any`, `tool`   | 313 token<hr />315 token |
| Claude Sonnet 4.6          | `auto`, `none`<hr />`any`, `tool`   | 497 token<hr />589 token |
| Claude Sonnet 4.5          | `auto`, `none`<hr />`any`, `tool`   | 496 token<hr />588 token |
| Claude Sonnet 4 ([dihentikan, kecuali di Bedrock dan Vertex AI](/docs/id/about-claude/model-deprecations)) | `auto`, `none`<hr />`any`, `tool`   | 313 token<hr />315 token |
| Claude Haiku 4.5         | `auto`, `none`<hr />`any`, `tool`   | 496 token<hr />588 token |
| Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Vertex AI](/docs/id/about-claude/model-deprecations)) | `auto`, `none`<hr />`any`, `tool`   | 264 token<hr />355 token |

Jumlah token ini ditambahkan ke token input dan output normal Anda untuk menghitung total biaya permintaan.

Lihat [tabel ikhtisar model](/docs/id/about-claude/models/overview#latest-models-comparison) untuk harga per model saat ini.

Ketika Anda mengirim prompt penggunaan alat, seperti permintaan API lainnya, respons menyertakan jumlah token input dan output dalam metrik `usage` yang dilaporkan.

---

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={3}>
  <Card href="/docs/id/agents-and-tools/tool-use/how-tool-use-works" title="Cara kerja penggunaan alat" icon="compass">
    Pahami loop penggunaan alat, di mana alat dieksekusi, dan kapan menggunakan alat alih-alih prosa.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent" title="Tutorial: Membangun agen yang menggunakan alat" icon="graduation-cap">
    Panduan terpandu dari satu panggilan alat hingga loop agentik yang siap produksi.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat" icon="book">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>
</CardGroup>