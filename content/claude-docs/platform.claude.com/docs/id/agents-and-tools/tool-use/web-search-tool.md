---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: f71e5bc6242205784198a763fb5ff9263287367cf8d0b71bae7852d27d7b2a3c
---

# Alat pencarian web

---

Alat pencarian web memberi Claude akses langsung ke konten web secara real-time, memungkinkannya menjawab pertanyaan dengan informasi terkini yang melampaui batas pengetahuannya. Respons menyertakan sitasi untuk sumber yang diambil dari hasil pencarian.

Versi alat pencarian web terbaru (`web_search_20260318`) mendukung **dynamic filtering** (pemfilteran dinamis) dengan Claude Fable 5, Claude Opus 4.8, Claude Mythos 5, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6. Claude dapat menulis dan mengeksekusi kode untuk memfilter hasil pencarian sebelum masuk ke jendela konteks, hanya menyimpan informasi yang relevan dan membuang sisanya. Hal ini menghasilkan respons yang lebih akurat sekaligus mengurangi konsumsi token. `web_search_20260318` juga menambahkan kontrol [penyertaan respons](#response-inclusion) untuk alur kerja agentik. Versi sebelumnya (`web_search_20260209` untuk pemfilteran dinamis saja, `web_search_20250305` untuk pencarian dasar) tetap tersedia.

<Note>
  Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), pencarian web didukung pada Claude API, Google Cloud, dan Microsoft Foundry. Pencarian web tidak tersedia untuk Mythos Preview pada Amazon Bedrock atau [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws).
</Note>

Untuk kelayakan Zero Data Retention dan solusi `allowed_callers`, lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#zdr-and-allowed-callers).

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Cara kerja pencarian web

Saat Anda menambahkan alat pencarian web ke permintaan API Anda:

1. Claude memutuskan kapan harus mencari berdasarkan prompt.
2. API mengeksekusi pencarian dan memberikan hasilnya kepada Claude. Proses ini dapat berulang beberapa kali dalam satu permintaan.
3. Di akhir gilirannya, Claude memberikan respons akhir dengan sumber yang disitasi.

### Kapan Claude melakukan pencarian

Claude melakukan pencarian ketika permintaan bergantung pada informasi yang terkini, berubah, atau berada di luar data pelatihannya:

* Peristiwa, berita, atau pengumuman terbaru
* Harga, kurs, skor, atau statistik terkini
* Informasi tentang organisasi, orang, atau produk tertentu yang mungkin telah berubah
* Permintaan eksplisit untuk mencari atau menelusuri sesuatu

Claude menjawab langsung tanpa mencari ketika permintaan mengandalkan pengetahuan yang stabil:

* Fakta yang sudah mapan, matematika, dasar-dasar sains, atau konsep pemrograman
* Penulisan kreatif atau brainstorming
* Analisis konten yang sudah disediakan dalam percakapan
* Giliran percakapan biasa dan sapaan

Pemicuan dapat diarahkan melalui prompt sistem Anda: Anda dapat mendorong Claude untuk lebih sering mencari atau lebih memilih menjawab langsung. Untuk batasan keras, gunakan `max_uses` untuk membatasi jumlah pencarian pada setiap permintaan.

### Pemfilteran dinamis

Pencarian web adalah tugas yang intensif token. Dengan pencarian web dasar, Claude perlu menarik hasil pencarian ke dalam konteks, mengambil HTML lengkap dari beberapa situs web, dan bernalar atas semuanya sebelum sampai pada jawaban. Sering kali, sebagian besar konten ini tidak relevan, yang dapat menurunkan kualitas respons.

Dengan `web_search_20260209` atau yang lebih baru, Claude dapat menulis dan mengeksekusi kode untuk memproses hasil kueri setelahnya. Alih-alih bernalar atas file HTML lengkap, Claude secara dinamis memfilter hasil pencarian sebelum memuatnya ke dalam konteks, hanya menyimpan yang relevan dan membuang sisanya.

Pemfilteran dinamis sangat efektif untuk:

* Menelusuri dokumentasi teknis
* Tinjauan literatur dan verifikasi sitasi
* Riset teknis
* Pembumian dan verifikasi respons

<Note>
  Pemfilteran dinamis memerlukan [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk diaktifkan. Alat pencarian web (dengan dan tanpa pemfilteran dinamis) tersedia pada Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Pada Microsoft Foundry, pencarian web memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure). Pada Google Cloud, hanya alat pencarian web dasar (tanpa pemfilteran dinamis) yang tersedia. Pencarian web tidak tersedia pada Amazon Bedrock.
</Note>

Untuk mengaktifkan pemfilteran dinamis, gunakan `web_search_20260209` atau versi yang lebih baru. Contoh berikut menggunakan `web_search_20260209`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 4096,
          "messages": [
              {
                  "role": "user",
                  "content": "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio."
              }
          ],
          "tools": [{
              "type": "web_search_20260209",
              "name": "web_search"
          }]
      }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: >-
        Search for the current prices of AAPL and GOOGL, then calculate
        which has a better P/E ratio.
  tools:
    - type: web_search_20260209
      name: web_search
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio.",
          }
      ],
      tools=[{"type": "web_search_20260209", "name": "web_search"}],
  )
  print(response)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const response = await anthropic.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content:
          "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio."
      }
    ],
    tools: [{ type: "web_search_20260209", name: "web_search" }]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio." }],
      Tools = [new ToolUnion(new WebSearchTool20260209())]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio.")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfWebSearchTool20260209: &anthropic.WebSearchTool20260209Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.WebSearchTool20260209;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(4096L)
          .addUserMessage("Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio.")
          .addTool(WebSearchTool20260209.builder().build())
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio.'],
      ],
      model: 'claude-opus-4-8',
      tools: [
          [
              'type' => 'web_search_20260209',
              'name' => 'web_search',
          ],
      ],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio." }
    ],
    tools: [{
      type: "web_search_20260209",
      name: "web_search"
    }]
  )
  puts message
  ```
</CodeGroup>

## Cara menggunakan pencarian web

<Note>
  Administrator organisasi Anda harus mengaktifkan pencarian web di [Claude Console](/settings/privacy).
</Note>

Sediakan alat pencarian web dalam permintaan API Anda:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 1024,
          "messages": [
              {
                  "role": "user",
                  "content": "What is the weather in NYC?"
              }
          ],
          "tools": [{
              "type": "web_search_20250305",
              "name": "web_search",
              "max_uses": 5
          }]
      }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: What is the weather in NYC?}' \
    --tool '{type: web_search_20250305, name: web_search, max_uses: 5}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "What's the weather in NYC?"}],
      tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
  )
  print(response)
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "What's the weather in NYC?"
      }
    ],
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 5
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "What's the weather in NYC?" }],
      Tools = [new ToolUnion(new WebSearchTool20250305() { MaxUses = 5 })]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in NYC?")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfWebSearchTool20250305: &anthropic.WebSearchTool20250305Param{
  			MaxUses: anthropic.Int(5),
  		}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.WebSearchTool20250305;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addUserMessage("What's the weather in NYC?")
          .addTool(WebSearchTool20250305.builder()
              .maxUses(5L)
              .build())
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => "What's the weather in NYC?"],
      ],
      model: 'claude-opus-4-8',
      tools: [
          [
              'type' => 'web_search_20250305',
              'name' => 'web_search',
              'max_uses' => 5,
          ],
      ],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "What's the weather in NYC?" }
    ],
    tools: [{
      type: "web_search_20250305",
      name: "web_search",
      max_uses: 5
    }]
  )
  puts message
  ```
</CodeGroup>

## Definisi alat

Alat pencarian web mendukung parameter berikut:

```json JSON
{
  "type": "web_search_20250305",
  "name": "web_search",

  // Optional: Limit the number of searches per request
  "max_uses": 5,

  // Optional: Only include results from these domains
  "allowed_domains": ["example.com", "trusteddomain.org"],

  // Optional: Never include results from these domains
  "blocked_domains": ["untrustedsource.com"],

  // Optional: Localize search results
  "user_location": {
    "type": "approximate",
    "city": "San Francisco",
    "region": "California",
    "country": "US",
    "timezone": "America/Los_Angeles"
  }
}
```

### Max uses

Parameter `max_uses` membatasi jumlah pencarian yang dilakukan. Jika Claude mencoba melakukan lebih banyak pencarian dari yang diizinkan, `web_search_tool_result` akan berupa error dengan kode error `max_uses_exceeded`.

Kueri faktual sederhana biasanya menggunakan 1–3 pencarian; riset komparatif atau multi-entitas dapat menggunakan 10 atau lebih. Untuk pencarian yang sensitif terhadap latensi, `max_uses: 3` membatasi biaya sambil jarang memotong hasil. Untuk agen riset, atur `max_uses` ke 15–20 atau hilangkan sepenuhnya.

### Pemfilteran domain

Untuk pemfilteran domain dengan `allowed_domains` dan `blocked_domains`, lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering).

### Lokalisasi

Parameter `user_location` memungkinkan Anda melokalkan hasil pencarian berdasarkan lokasi pengguna.

* `type`: Jenis lokasi (harus `approximate`)
* `city`: Nama kota
* `region`: Wilayah atau negara bagian
* `country`: Negara
* `timezone`: [ID zona waktu IANA](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

### Penyertaan respons

<Note>
  Memerlukan `web_search_20260318` atau yang lebih baru.
</Note>

Parameter `response_inclusion` mengontrol bagaimana blok hasil pencarian muncul dalam respons API ketika hasil tersebut dikonsumsi oleh panggilan [eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) yang telah selesai dalam giliran yang sama. Atur `"response_inclusion": "excluded"` untuk menghilangkan pasangan blok `server_tool_use` dan hasil bersarang tersebut sepenuhnya dari respons, sehingga mengurangi biaya token output untuk alur kerja agentik yang tidak perlu mengirim kembali konten pencarian mentah ke klien. Nilai default-nya adalah `"full"`. Hasil dari panggilan langsung, atau dari panggilan eksekusi kode yang dijeda sebelum selesai, selalu dikembalikan secara penuh agar dapat dikirim kembali pada giliran berikutnya.

```json
{
  "tools": [
    {
      "type": "web_search_20260318",
      "name": "web_search",
      "response_inclusion": "excluded"
    }
  ]
}
```

## Respons

Berikut adalah contoh struktur respons:

```json Output
{
  "role": "assistant",
  "content": [
    // 1. Claude's decision to search
    {
      "type": "text",
      "text": "I'll search for when Claude Shannon was born."
    },
    // 2. The search query used
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01WYG3ziw53XMcoyKL4XcZmE",
      "name": "web_search",
      "input": {
        "query": "claude shannon birth date"
      }
    },
    // 3. Search results
    {
      "type": "web_search_tool_result",
      "tool_use_id": "srvtoolu_01WYG3ziw53XMcoyKL4XcZmE",
      "content": [
        {
          "type": "web_search_result",
          "url": "https://en.wikipedia.org/wiki/Claude_Shannon",
          "title": "Claude Shannon - Wikipedia",
          "encrypted_content": "EqgfCioIARgBIiQ3YTAwMjY1Mi1mZjM5LTQ1NGUtODgxNC1kNjNjNTk1ZWI3Y...",
          "page_age": "April 30, 2025"
        }
      ]
    },
    {
      "text": "Based on the search results, ",
      "type": "text"
    },
    // 4. Claude's response with citations
    {
      "text": "Claude Shannon was born on April 30, 1916, in Petoskey, Michigan",
      "type": "text",
      "citations": [
        {
          "type": "web_search_result_location",
          "url": "https://en.wikipedia.org/wiki/Claude_Shannon",
          "title": "Claude Shannon - Wikipedia",
          "encrypted_index": "Eo8BCioIAhgBIiQyYjQ0OWJmZi1lNm..",
          "cited_text": "Claude Elwood Shannon (April 30, 1916 – February 24, 2001) was an American mathematician, electrical engineer, computer scientist, cryptographer and i..."
        }
      ]
    }
  ],
  "id": "msg_a930390d3a",
  "usage": {
    "input_tokens": 6039,
    "output_tokens": 931,
    "server_tool_use": {
      "web_search_requests": 1
    }
  },
  "stop_reason": "end_turn"
}
```

### Hasil pencarian

Hasil pencarian mencakup:

* `url`: URL halaman sumber
* `title`: Judul halaman sumber
* `page_age`: Kapan situs terakhir diperbarui
* `encrypted_content`: Konten terenkripsi yang harus dikirim kembali dalam percakapan multi-giliran untuk sitasi

### Sitasi

Sitasi selalu diaktifkan untuk pencarian web, dan setiap `web_search_result_location` mencakup:

* `url`: URL sumber yang disitasi
* `title`: Judul sumber yang disitasi
* `encrypted_index`: Referensi yang harus dikirim kembali untuk percakapan multi-giliran.
* `cited_text`: Hingga 150 karakter dari konten yang disitasi

Field sitasi pencarian web `cited_text`, `title`, dan `url` tidak dihitung terhadap penggunaan token input atau output.

<Note>
  Saat menampilkan output API secara langsung kepada pengguna akhir, sitasi harus disertakan ke sumber aslinya. Jika Anda melakukan modifikasi pada output API, termasuk dengan memproses ulang dan/atau menggabungkannya dengan materi Anda sendiri sebelum menampilkannya kepada pengguna akhir, tampilkan sitasi sebagaimana mestinya berdasarkan konsultasi dengan tim hukum Anda.
</Note>

### Error

Ketika alat pencarian web mengalami error (seperti mencapai batas laju), Claude API tetap mengembalikan respons 200 (sukses). Error tersebut direpresentasikan dalam body respons menggunakan struktur berikut:

```json Output
{
  "type": "web_search_tool_result",
  "tool_use_id": "srvtoolu_a93jad",
  "content": {
    "type": "web_search_tool_result_error",
    "error_code": "max_uses_exceeded"
  }
}
```

Berikut adalah kode error yang mungkin muncul:

* `too_many_requests`: Batas laju terlampaui
* `invalid_input`: Parameter kueri pencarian tidak valid
* `max_uses_exceeded`: Penggunaan maksimum alat pencarian web terlampaui
* `query_too_long`: Kueri melebihi panjang maksimum
* `unavailable`: Terjadi error internal

### Stop reason `pause_turn`

Untuk melanjutkan setelah stop reason `pause_turn`, lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#the-server-side-loop-and-pause-turn).

## Caching prompt

Untuk melakukan caching definisi alat di seluruh giliran, lihat [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

## Streaming

Dengan streaming diaktifkan, Anda akan menerima event pencarian sebagai bagian dari stream. Akan ada jeda saat pencarian dieksekusi:

```sse Output
event: message_start
data: {"type": "message_start", "message": {"id": "msg_abc123", "type": "message"}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

// Claude's decision to search

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "web_search"}}

// Search query streamed
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"query\":\"latest quantum computing breakthroughs 2025\"}"}}

// Pause while search executes

// Search results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "web_search_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": [{"type": "web_search_result", "title": "Quantum Computing Breakthroughs in 2025", "url": "https://example.com"}]}}

// Claude's response with citations (omitted in this example)
```

## Permintaan batch

Anda dapat menyertakan alat pencarian web dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Panggilan alat pencarian web melalui Messages Batches API dikenakan harga yang sama dengan permintaan Messages API reguler.

Untuk melindungi kapasitas bersama, Batches API membatasi permintaan pencarian web per organisasi, sehingga batch besar dengan banyak pencarian mungkin memerlukan waktu lebih lama untuk diselesaikan. Anda dapat melihat batas laju pencarian web organisasi Anda di halaman [Limits](/settings/limits) di Claude Console; hubungi tim penjualan dari halaman tersebut untuk meminta batas yang lebih tinggi. Beban kerja pencarian web batch yang umum mencakup memperkaya record dengan data web terkini, meneliti daftar entitas yang besar, dan membumikan atau memeriksa korpus konten terhadap sumber langsung.

## Penggunaan dan harga

Penggunaan pencarian web dikenakan biaya sebagai tambahan dari penggunaan token:

```json
{
  "usage": {
    "input_tokens": 105,
    "output_tokens": 6039,
    "cache_read_input_tokens": 7123,
    "cache_creation_input_tokens": 7345,
    "server_tool_use": {
      "web_search_requests": 1
    }
  }
}
```

Pencarian web tersedia di API Claude dengan harga **$10 per 1.000 pencarian**, ditambah biaya token standar untuk konten yang dihasilkan dari pencarian. Hasil pencarian web yang diambil sepanjang percakapan dihitung sebagai token input, baik dalam iterasi pencarian yang dijalankan selama satu giliran maupun dalam giliran percakapan berikutnya.

Setiap pencarian web dihitung sebagai satu penggunaan, terlepas dari jumlah hasil yang dikembalikan. Jika terjadi kesalahan selama pencarian web, pencarian web tersebut tidak akan ditagih.

## Langkah selanjutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/server-tools" title="Alat server">
    Mekanisme bersama untuk alat yang dieksekusi Anthropic.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat">
    Direktori semua alat yang disediakan Anthropic.
  </Card>
</CardGroup>
