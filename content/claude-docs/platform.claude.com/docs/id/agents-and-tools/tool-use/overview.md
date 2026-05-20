---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview
fetched_at: 2026-05-20T03:15:44.945478Z
sha256: 587c8efbedf54a25dc54331a686ebe8230ecf0f7c9db5d1e4ca2e9533363d691
---

# Penggunaan alat dengan Claude

Hubungkan Claude ke alat dan API eksternal. Pelajari di mana alat dijalankan dan bagaimana loop agentic bekerja.

---

Penggunaan alat memungkinkan Claude memanggil fungsi yang Anda tentukan atau yang disediakan Anthropic. Claude memutuskan kapan memanggil alat berdasarkan permintaan pengguna dan deskripsi alat, kemudian mengembalikan panggilan terstruktur yang dijalankan aplikasi Anda (alat klien) atau yang dijalankan Anthropic (alat server).

Berikut adalah contoh paling sederhana menggunakan alat server, di mana Anthropic menangani eksekusi:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-7",
    "max_tokens": 1024,
    "tools": [{"type": "web_search_20260209", "name": "web_search"}],
    "messages": [{"role": "user", "content": "What'\''s the latest on the Mars rover?"}]
  }'
```

```bash CLI
ant messages create --transform content --format yaml \
  --model claude-opus-4-7 \
  --max-tokens 1024 \
  --tool '{type: web_search_20260209, name: web_search}' \
  --message '{role: user, content: "What is the latest on the Mars rover?"}'
```

```python Python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[{"type": "web_search_20260209", "name": "web_search"}],
    messages=[{"role": "user", "content": "What's the latest on the Mars rover?"}],
)
print(response.content)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const response = await client.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [{ type: "web_search_20260209", name: "web_search" }],
  messages: [{ role: "user", content: "What's the latest on the Mars rover?" }]
});
console.log(response.content);
```
</CodeGroup>

---

## Cara kerja penggunaan alat

Alat berbeda terutama berdasarkan tempat kode dijalankan. **Alat klien** (termasuk alat yang ditentukan pengguna dan alat skema Anthropic seperti bash dan text_editor) berjalan di aplikasi Anda: Claude merespons dengan `stop_reason: "tool_use"` dan satu atau lebih blok `tool_use`, kode Anda menjalankan operasi, dan Anda mengirim kembali `tool_result`. **Alat server** (web_search, code_execution, web_fetch, tool_search) berjalan di infrastruktur Anthropic: Anda melihat hasilnya secara langsung tanpa menangani eksekusi.

Untuk model konseptual lengkap termasuk loop agentic dan kapan memilih setiap pendekatan, lihat [Cara kerja penggunaan alat](/docs/id/agents-and-tools/tool-use/how-tool-use-works).

Untuk menghubungkan ke server MCP, lihat [konektor MCP](/docs/id/agents-and-tools/mcp-connector). Untuk membangun klien MCP Anda sendiri, lihat [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/develop/build-client).

<Tip>
**Jamin kesesuaian skema dengan penggunaan alat ketat**

Tambahkan `strict: true` ke definisi alat Anda untuk memastikan panggilan alat Claude selalu cocok dengan skema Anda dengan tepat. Lihat [Penggunaan alat ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use).
</Tip>

Akses alat adalah salah satu primitif dengan leverage tertinggi yang dapat Anda berikan kepada agen. Pada benchmark seperti [LAB-Bench FigQA](https://lab-bench.org/) (interpretasi gambar ilmiah) dan [SWE-bench](https://www.swebench.com/) (rekayasa perangkat lunak dunia nyata), menambahkan bahkan alat dasar menghasilkan keuntungan kemampuan yang luar biasa, sering kali melampaui baseline ahli manusia.

---

## Contoh penggunaan alat

Untuk panduan langsung lengkap, lihat [tutorial](/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent). Untuk contoh referensi konsep individual, lihat [Tentukan alat](/docs/id/agents-and-tools/tool-use/define-tools) dan [Tangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

<section title="Apa yang terjadi ketika Claude membutuhkan informasi lebih lanjut">

Jika prompt pengguna tidak menyertakan informasi yang cukup untuk mengisi semua parameter yang diperlukan untuk alat, Claude Opus jauh lebih mungkin mengenali bahwa parameter hilang dan memintanya. Claude Sonnet mungkin bertanya, terutama ketika diminta untuk berpikir sebelum mengeluarkan permintaan alat. Tetapi mungkin juga melakukan yang terbaik untuk menyimpulkan nilai yang masuk akal.

Misalnya, diberikan alat `get_weather` yang memerlukan parameter `location`, jika Anda bertanya kepada Claude "Bagaimana cuacanya?" tanpa menentukan lokasi, Claude (terutama Claude Sonnet) mungkin membuat tebakan tentang input alat:

```json JSON
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "get_weather",
  "input": { "location": "New York, NY", "unit": "fahrenheit" }
}
```

Perilaku ini tidak dijamin, terutama untuk prompt yang lebih ambigu dan untuk model yang kurang cerdas. Jika Claude Opus tidak memiliki konteks yang cukup untuk mengisi parameter yang diperlukan, jauh lebih mungkin untuk merespons dengan pertanyaan klarifikasi daripada membuat panggilan alat.

</section>

---

## Harga

Tool use requests are priced based on:
1. The total number of input tokens sent to the model (including in the `tools` parameter)
2. The number of output tokens generated
3. For server-side tools, additional usage-based pricing (e.g., web search charges per search performed)

Client-side tools are priced the same as any other Claude API request, while server-side tools may incur additional charges based on their specific usage.

The additional tokens from tool use come from:

- The `tools` parameter in API requests (tool names, descriptions, and schemas)
- `tool_use` content blocks in API requests and responses
- `tool_result` content blocks in API requests

When you use `tools`, the API also automatically includes a special system prompt for the model which enables tool use. The number of tool use tokens required for each model are listed below (excluding the additional tokens listed above). Note that the table assumes at least 1 tool is provided. If no `tools` are provided, then a tool choice of `none` uses 0 additional system prompt tokens.

| Model                    | Tool choice                                          | Tool use system prompt token count          |
|--------------------------|------------------------------------------------------|---------------------------------------------|
| Claude Opus 4.7                | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Opus 4.6              | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Opus 4.5            | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Opus 4.1            | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Opus 4 ([deprecated](/docs/en/about-claude/model-deprecations)) | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Sonnet 4.6          | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Sonnet 4.5          | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Sonnet 4 ([deprecated](/docs/en/about-claude/model-deprecations)) | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Haiku 4.5         | `auto`, `none`<hr />`any`, `tool`   | 346 tokens<hr />313 tokens |
| Claude Haiku 3.5 ([retired, except on Bedrock and Vertex AI](/docs/en/about-claude/model-deprecations)) | `auto`, `none`<hr />`any`, `tool`   | 264 tokens<hr />340 tokens |

These token counts are added to your normal input and output tokens to calculate the total cost of a request.

Lihat [tabel ringkasan model](/docs/id/about-claude/models/overview#latest-models-comparison) untuk harga per model saat ini.

Ketika Anda mengirim prompt penggunaan alat, seperti permintaan API lainnya, respons akan menampilkan jumlah token input dan output sebagai bagian dari metrik `usage` yang dilaporkan.

---

## Langkah berikutnya

### Pilih jalur Anda

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/how-tool-use-works" title="Pahami konsepnya">
    Di mana alat berjalan, bagaimana loop bekerja, dan kapan menggunakan alat.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent" title="Bangun langkah demi langkah">
    Tutorial: dari panggilan alat tunggal hingga produksi.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Jelajahi semua alat">
    Direktori alat yang disediakan Anthropic dan properti.
  </Card>
</CardGroup>