---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 1a812c708a4e94d814320b19e9f951bcdea66ab939c2fd150c4e9bbb593e8011
---

# Penggunaan alat dengan Claude

Hubungkan Claude ke alat dan API eksternal. Pelajari di mana alat dieksekusi dan bagaimana loop agentik bekerja.

---

Penggunaan alat memungkinkan Claude memanggil fungsi yang Anda definisikan atau yang disediakan oleh Anthropic. Claude memutuskan kapan harus memanggil alat berdasarkan permintaan pengguna dan deskripsi alat tersebut, lalu mengembalikan panggilan terstruktur yang dieksekusi oleh aplikasi Anda (alat klien) atau yang dieksekusi oleh Anthropic (alat server).

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

```python Python
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

```typescript TypeScript
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
</CodeGroup>

---

## Cara kerja penggunaan alat \{#how-tool-use-works}

Alat dibedakan terutama berdasarkan di mana kode dieksekusi. **Alat klien** (termasuk alat yang didefinisikan pengguna dan alat dengan skema Anthropic seperti bash dan text_editor) berjalan di aplikasi Anda: Claude merespons dengan `stop_reason: "tool_use"` dan satu atau lebih blok `tool_use`, kode Anda mengeksekusi operasi tersebut, dan Anda mengirimkan kembali sebuah `tool_result`. **Alat server** (web_search, code_execution, web_fetch, tool_search) berjalan di infrastruktur Anthropic: Anda melihat hasilnya secara langsung tanpa perlu menangani eksekusi.

Untuk model konseptual lengkap termasuk loop agentik dan kapan memilih setiap pendekatan, lihat [Cara kerja penggunaan alat](/docs/id/agents-and-tools/tool-use/how-tool-use-works).

Untuk menghubungkan ke server MCP, lihat [konektor MCP](/docs/id/agents-and-tools/mcp-connector). Untuk membangun klien MCP Anda sendiri, lihat [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/develop/build-client).

<Tip>
**Jamin kesesuaian skema dengan penggunaan alat strict**

Tambahkan `strict: true` ke definisi alat Anda untuk memastikan panggilan alat Claude selalu cocok persis dengan skema Anda. Lihat [Penggunaan alat strict](/docs/id/agents-and-tools/tool-use/strict-tool-use).
</Tip>

Akses ke alat adalah salah satu primitif dengan daya ungkit tertinggi yang dapat Anda berikan kepada agen. Pada benchmark seperti [LAB-Bench FigQA](https://lab-bench.org/) (interpretasi gambar ilmiah) dan [SWE-bench](https://www.swebench.com/) (rekayasa perangkat lunak dunia nyata), menambahkan alat dasar sekalipun menghasilkan peningkatan kemampuan yang sangat besar, sering kali melampaui baseline pakar manusia.

---

## Kapan Claude menggunakan alat \{#when-claude-uses-tools}

Dengan `tool_choice` default `{"type": "auto"}`, Claude memutuskan pada setiap giliran apakah akan memanggil alat atau merespons secara langsung. Claude memanggil alat ketika permintaan sesuai dengan kemampuan yang dijelaskan alat tersebut dan jawabannya belum ada dalam konteks; Claude merespons secara langsung untuk pengetahuan yang stabil, tugas kreatif, dan giliran percakapan biasa.

Batasan ini dapat diarahkan melalui prompt sistem Anda. Jika Claude tidak memanggil alat saat Anda mengharapkannya, instruksi ringan seperti `"Use the tools to investigate before responding."` secara terukur meningkatkan penggunaan alat; bentuk yang lebih kuat seperti `"Always call a tool first before responding."` mendorong lebih jauh lagi. Sebaliknya, `"Use your judgment about whether to call a tool or respond directly."` menjaga perilaku pemicuan tetap konservatif.

Untuk jaminan keras alih-alih sekadar dorongan, gunakan [`tool_choice`](/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use).

Halaman setiap alat server menjelaskan batasan pemicunya sendiri secara lebih rinci. Lihat misalnya [alat pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) atau [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool).

---

## Contoh penggunaan alat \{#tool-use-examples}

Untuk panduan langkah demi langkah yang lengkap, lihat [tutorial](/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent). Untuk contoh referensi dari konsep individual, lihat [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools) dan [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

<section title="Apa yang terjadi ketika Claude membutuhkan informasi lebih lanjut">

Jika prompt pengguna tidak menyertakan informasi yang cukup untuk mengisi semua parameter yang diperlukan untuk sebuah alat, Claude Opus jauh lebih mungkin mengenali bahwa ada parameter yang hilang dan menanyakannya. Claude Sonnet mungkin bertanya, terutama ketika diminta untuk berpikir sebelum mengeluarkan permintaan alat. Tetapi Claude Sonnet juga mungkin berusaha sebaik mungkin untuk menyimpulkan nilai yang masuk akal.

Misalnya, diberikan alat `get_weather` yang memerlukan parameter `location`, jika Anda bertanya kepada Claude "Bagaimana cuacanya?" tanpa menentukan lokasi, Claude (khususnya Claude Sonnet) mungkin menebak input alat:

```json JSON
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "get_weather",
  "input": { "location": "New York, NY", "unit": "fahrenheit" }
}
```

Perilaku ini tidak dijamin, terutama untuk prompt yang lebih ambigu dan untuk model yang kurang cerdas. Jika Claude Opus tidak memiliki konteks yang cukup untuk mengisi parameter yang diperlukan, Claude Opus jauh lebih mungkin merespons dengan pertanyaan klarifikasi alih-alih melakukan panggilan alat.

</section>

---

## Harga \{#pricing}

Permintaan penggunaan alat dikenakan harga berdasarkan:
1. Jumlah total token input yang dikirim ke model (termasuk dalam parameter `tools`)
2. Jumlah token output yang dihasilkan
3. Untuk alat sisi server, harga tambahan berbasis penggunaan (misalnya, pencarian web dikenakan biaya per pencarian yang dilakukan)

Alat sisi klien dikenakan harga yang sama seperti permintaan API Claude lainnya, sedangkan alat sisi server mungkin dikenakan biaya tambahan berdasarkan penggunaan spesifiknya.

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
| Claude Opus 4 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)) | `auto`, `none`<hr />`any`, `tool`   | 313 token<hr />315 token |
| Claude Sonnet 4.6          | `auto`, `none`<hr />`any`, `tool`   | 497 token<hr />589 token |
| Claude Sonnet 4.5          | `auto`, `none`<hr />`any`, `tool`   | 496 token<hr />588 token |
| Claude Sonnet 4 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)) | `auto`, `none`<hr />`any`, `tool`   | 313 token<hr />315 token |
| Claude Haiku 4.5         | `auto`, `none`<hr />`any`, `tool`   | 496 token<hr />588 token |
| Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Vertex AI](/docs/id/about-claude/model-deprecations)) | `auto`, `none`<hr />`any`, `tool`   | 264 token<hr />355 token |

Jumlah token ini ditambahkan ke token input dan output normal Anda untuk menghitung total biaya permintaan.

Lihat [tabel ikhtisar model](/docs/id/about-claude/models/overview#latest-models-comparison) untuk harga terkini per model.

Ketika Anda mengirim prompt penggunaan alat, sama seperti permintaan API lainnya, respons akan menampilkan jumlah token input dan output sebagai bagian dari metrik `usage` yang dilaporkan.

---

## Langkah selanjutnya \{#next-steps}

### Pilih jalur Anda \{#choose-your-path}

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/how-tool-use-works" title="Pahami konsepnya">
    Di mana alat berjalan, bagaimana loop bekerja, dan kapan menggunakan alat.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent" title="Bangun langkah demi langkah">
    Tutorial: dari satu panggilan alat hingga produksi.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Jelajahi semua alat">
    Direktori alat yang disediakan Anthropic beserta propertinya.
  </Card>
</CardGroup>