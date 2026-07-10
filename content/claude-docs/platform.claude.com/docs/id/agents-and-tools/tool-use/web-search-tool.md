---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: 1fa23c6870f4799b5513d10b1dffb3571bd21f38909bd8565684262c455f34e3
---

# Alat pencarian web

Berikan Claude akses ke konten web terkini dengan sumber yang dikutip, pemfilteran dinamis opsional, dan kontrol domain.

---

Alat pencarian web memberi Claude akses langsung ke konten web real-time, memungkinkannya menjawab pertanyaan dengan informasi terkini di luar batas pengetahuannya. Respons menyertakan sitasi untuk sumber yang diambil dari hasil pencarian.

Dengan `web_search_20260209` dan versi yang lebih baru, Claude dapat menulis dan menjalankan kode yang memfilter hasil pencarian sebelum mencapai "context window" (jendela konteks) (**dynamic filtering** atau pemfilteran dinamis), sehingga hanya informasi yang relevan yang dipertahankan. Pemfilteran dinamis tersedia dengan Claude Fable 5, Claude Opus 4.8, Claude Mythos 5, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6.

Tiga versi alat pencarian web tersedia:

* `web_search_20250305`: pencarian web dasar
* `web_search_20260209`: menambahkan [pemfilteran dinamis](#dynamic-filtering)
* `web_search_20260318`: menambahkan kontrol [penyertaan respons](#response-inclusion) untuk alur kerja agentik

Contoh-contoh di halaman ini menggunakan `web_search_20250305` untuk pencarian dasar dan `web_search_20260318` untuk pemfilteran dinamis.

<Note>
  Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), pencarian web didukung di Claude API, Google Cloud, dan Microsoft Foundry. Pencarian web tidak tersedia untuk Mythos Preview di Amazon Bedrock atau [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws).
</Note>

Untuk kelayakan Zero Data Retention pencarian web dan konfigurasi `allowed_callers` terkait, lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#zdr-and-allowed-callers).

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Cara kerja pencarian web

Saat Anda menambahkan alat pencarian web ke permintaan API Anda:

1. Claude menentukan kapan harus mencari berdasarkan prompt.
2. API menjalankan pencarian dan memberikan hasilnya kepada Claude. Proses ini dapat berulang beberapa kali dalam satu permintaan.
3. Di akhir gilirannya, Claude memberikan respons akhir dengan sumber yang dikutip.

### Kapan Claude mencari

Claude mencari ketika permintaan bergantung pada informasi yang terkini, berubah, atau di luar data pelatihannya:

* Peristiwa, berita, atau pengumuman terbaru
* Harga, tarif, skor, atau statistik terkini
* Informasi tentang organisasi, orang, atau produk tertentu yang mungkin telah berubah
* Permintaan eksplisit untuk mencari atau menelusuri sesuatu

Claude menjawab langsung tanpa mencari ketika permintaan mengandalkan pengetahuan yang stabil:

* Fakta yang sudah mapan, matematika, dasar-dasar sains, atau konsep pemrograman
* Penulisan kreatif atau brainstorming
* Analisis konten yang sudah disediakan dalam percakapan
* Giliran percakapan dan sapaan

Pemicuan dapat diarahkan melalui prompt sistem Anda: Anda dapat mendorong Claude untuk lebih sering mencari atau lebih memilih menjawab langsung. Untuk batasan yang tegas, gunakan `max_uses` untuk membatasi jumlah pencarian untuk setiap permintaan.

### Pemfilteran dinamis

Dengan pencarian web dasar, setiap hasil pencarian dimuat ke dalam jendela konteks Claude, dan sebagian besar konten tersebut bisa jadi tidak relevan dengan permintaan. Dengan `web_search_20260209` atau yang lebih baru, Claude sebagai gantinya menulis dan menjalankan kode yang memfilter hasil terlebih dahulu, sehingga hanya konten yang relevan yang mencapai jendela konteks. Ini mengurangi penggunaan token pada permintaan yang banyak melakukan pencarian.

Pemfilteran dinamis menjalankan pencarian web dari dalam [eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool): pada `web_search_20260209` dan yang lebih baru, field `allowed_callers` alat ini secara default bernilai `["code_execution_20260120"]`, dan ketika pemfilteran dinamis berjalan, API secara otomatis menyediakan eksekusi kode yang dibutuhkan untuk permintaan tersebut. Anda tidak perlu menambahkan alat eksekusi kode ke `tools` sendiri. Tidak ada biaya tambahan untuk panggilan eksekusi kode yang dilakukan dengan cara ini di luar biaya token standar.

Untuk memanggil pencarian web secara langsung, tanpa pemfilteran dinamis, atur `allowed_callers: ["direct"]`. Model yang tidak mendukung pemanggilan alat terprogram memerlukan pengaturan ini. Tanpanya, API mengembalikan error 400 yang memberi tahu Anda untuk mengaturnya.

<Note>
  Alat pencarian web (dengan dan tanpa pemfilteran dinamis) tersedia di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, pencarian web memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure). Di Google Cloud, hanya alat pencarian web dasar (tanpa pemfilteran dinamis) yang tersedia. Pencarian web tidak tersedia di Amazon Bedrock.
</Note>

Contoh-contoh berikut menggunakan `web_search_20260318`:

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
              "type": "web_search_20260318",
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
    - type: web_search_20260318
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
      tools=[{"type": "web_search_20260318", "name": "web_search"}],
  )
  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content:
          "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio."
      }
    ],
    tools: [{ type: "web_search_20260318", name: "web_search" }]
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
      Tools = [new ToolUnion(new WebSearchTool20260318())]
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
  		{OfWebSearchTool20260318: &anthropic.WebSearchTool20260318Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.WebSearchTool20260318;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(4096L)
          .addUserMessage("Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio.")
          .addTool(WebSearchTool20260318.builder().build())
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
              'type' => 'web_search_20260318',
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
      type: "web_search_20260318",
      name: "web_search"
    }]
  )
  puts message
  ```
</CodeGroup>

## Cara menggunakan pencarian web

<Note>
  Pencarian web diaktifkan untuk organisasi Anda kecuali administrator telah menonaktifkannya di [Claude Console](/settings/privacy), di mana mereka juga dapat membatasi domain mana yang dicari. Jika dinonaktifkan, permintaan yang menyertakan alat ini gagal dengan `invalid_request_error` 400 yang menyatakan bahwa pencarian web tidak diaktifkan, bukan [kode error](#errors) di dalam hasil pencarian.
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
  const client = new Anthropic();

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

  // Optional: Only include results from these domains.
  // Use allowed_domains or blocked_domains, not both.
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

Semua versi alat pencarian web menerima `allowed_callers`, yang mengontrol apakah Claude memanggil pencarian web secara langsung atau dari [eksekusi kode](#dynamic-filtering). Pada `web_search_20260209` dan yang lebih baru, nilai defaultnya adalah `["code_execution_20260120"]` alih-alih `["direct"]`. Lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#zdr-and-allowed-callers) untuk cara mengonfigurasinya. `web_search_20260318` dan yang lebih baru juga menerima [`response_inclusion`](#response-inclusion).

### Penggunaan maksimum

Parameter `max_uses` membatasi jumlah pencarian yang dilakukan. Jika Claude mencoba melakukan lebih banyak pencarian daripada yang diizinkan, `web_search_tool_result` akan berupa error dengan kode error `max_uses_exceeded`.

Kueri faktual sederhana biasanya menggunakan 1–3 pencarian; riset komparatif atau multi-entitas dapat menggunakan 10 atau lebih. Untuk pencarian yang sensitif terhadap latensi, `max_uses: 3` membatasi biaya sambil jarang memotong hasil. Untuk agen riset, atur `max_uses` ke 15–20 atau hilangkan sepenuhnya.

### Pemfilteran domain

Sediakan `allowed_domains` atau `blocked_domains`, bukan keduanya. Jika permintaan menyertakan keduanya, API mengembalikan error 400. Entri berupa domain polos dengan path opsional, misalnya `example.com` atau `example.com/blog`, tanpa skema.

Untuk aturan pemfilteran domain lengkap, lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering).

### Lokalisasi

Parameter `user_location` memungkinkan Anda melokalkan hasil pencarian berdasarkan lokasi pengguna. Sediakan setidaknya satu dari `city`, `region`, `country`, atau `timezone`.

* `type`: Jenis lokasi (harus `approximate`)
* `city`: Nama kota
* `region`: Wilayah atau negara bagian
* `country`: Kode negara dua huruf [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). API menolak kode negara yang tidak didukung dengan error 400.
* `timezone`: [ID zona waktu IANA](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

### Penyertaan respons

<Note>
  Memerlukan `web_search_20260318` atau yang lebih baru.
</Note>

Parameter `response_inclusion` mengontrol bagaimana blok hasil pencarian muncul dalam respons API ketika hasil tersebut dikonsumsi oleh panggilan [eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) yang selesai dalam giliran yang sama. Atur `"response_inclusion": "excluded"` untuk menghapus pasangan blok `server_tool_use` dan blok hasil bersarang tersebut sepenuhnya dari respons, mengurangi biaya token output untuk alur kerja agentik yang tidak perlu mengembalikan konten pencarian mentah ke klien. Nilai defaultnya adalah `"full"`. Hasil dari panggilan langsung, atau dari panggilan eksekusi kode yang dijeda sebelum selesai, selalu dikembalikan secara penuh sehingga dapat dikirim kembali pada giliran berikutnya.

```json JSON
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

Contoh ini menunjukkan pencarian langsung. Ketika pencarian berjalan melalui [pemfilteran dinamis](#dynamic-filtering), respons juga berisi blok hasil [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool), dan setiap pasangan `server_tool_use` dan `web_search_tool_result` bersarang membawa field `caller` yang mengidentifikasi panggilan eksekusi kode yang membuatnya.

### Hasil pencarian

Hasil pencarian mencakup:

* `url`: URL halaman sumber
* `title`: Judul halaman sumber
* `page_age`: Kapan situs terakhir diperbarui
* `encrypted_content`: Konten terenkripsi yang harus Anda kirimkan kembali dalam percakapan multi-giliran

Untuk melanjutkan percakapan yang berisi hasil pencarian, kirim kembali blok konten asisten persis seperti yang Anda terima, termasuk `encrypted_content` dari setiap hasil. API mendekripsi konten tersebut pada giliran berikutnya untuk memulihkan hasil pencarian dalam konteks Claude. Jika `encrypted_content` hilang atau dimodifikasi, permintaan gagal dengan error validasi 400.

### Sitasi

Sitasi selalu diaktifkan untuk pencarian web, dan setiap `web_search_result_location` mencakup:

* `url`: URL sumber yang dikutip
* `title`: Judul sumber yang dikutip
* `encrypted_index`: Referensi yang harus dikirimkan kembali untuk percakapan multi-giliran.
* `cited_text`: Hingga 150 karakter dari konten yang dikutip

Field sitasi pencarian web `cited_text`, `title`, dan `url` tidak dihitung dalam penggunaan token input atau output.

<Note>
  Saat menampilkan output API langsung kepada pengguna akhir, sitasi harus disertakan ke sumber aslinya. Jika Anda melakukan modifikasi pada output API, termasuk dengan memproses ulang dan/atau menggabungkannya dengan materi Anda sendiri sebelum menampilkannya kepada pengguna akhir, tampilkan sitasi sebagaimana mestinya berdasarkan konsultasi dengan tim hukum Anda.
</Note>

### Error

Ketika alat pencarian web mengalami error (seperti mencapai batas laju), Claude API tetap mengembalikan respons 200 (sukses). Error direpresentasikan di dalam body respons menggunakan struktur berikut:

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

Pada error, `content` adalah satu objek error, bukan daftar blok hasil. Pencarian yang berhasil tetapi tidak menemukan hasil mengembalikan daftar `content` kosong, bukan error.

Berikut adalah kode error yang mungkin terjadi:

* `too_many_requests`: Batas laju terlampaui
* `invalid_tool_input`: Parameter kueri pencarian tidak valid
* `max_uses_exceeded`: Penggunaan maksimum alat pencarian web terlampaui
* `query_too_long`: Kueri melebihi panjang maksimum
* `request_too_large`: Permintaan pencarian terlalu besar, biasanya karena daftar filter domain yang panjang
* `unavailable`: Terjadi error internal

### Alasan berhenti `pause_turn`

API dapat menjeda giliran pencarian yang berjalan lama dan mengembalikan `stop_reason: "pause_turn"`. Untuk melanjutkan, kirim kembali pesan asisten yang dijeda tanpa perubahan dalam permintaan baru.

Jika Claude memanggil pencarian web dan salah satu alat klien Anda dalam kelompok panggilan alat paralel yang sama, API mengembalikan `stop_reason: "tool_use"` sebagai gantinya dan belum menjalankan pencarian. Untuk melanjutkan, kembalikan hasil alat klien, dan API menjalankan pencarian pada permintaan berikutnya. Lihat [Menggabungkan alat server dan alat klien dalam satu giliran](/docs/id/agents-and-tools/tool-use/server-tools#mixing-server-tools-and-client-tools-in-one-turn).

Untuk loop sisi server dan penanganan `pause_turn`, lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#the-server-side-loop-and-pause-turn).

## Caching prompt

Untuk caching definisi alat antar giliran, lihat [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

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

Anda dapat menyertakan alat pencarian web dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Panggilan alat pencarian web melalui Messages Batches API dikenakan harga yang sama dengan panggilan dalam permintaan Messages API biasa.

Untuk melindungi kapasitas bersama, Batches API membatasi permintaan pencarian web per organisasi, sehingga batch besar dengan banyak pencarian mungkin membutuhkan waktu lebih lama untuk selesai. Anda dapat melihat batas laju pencarian web organisasi Anda di halaman [Limits](/settings/limits) di Claude Console. Untuk meminta batas yang lebih tinggi, hubungi tim penjualan dari halaman tersebut.

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

<CardGroup cols={3}>
  <Card title="Alat pengambilan web" icon="link" href="/docs/id/agents-and-tools/tool-use/web-fetch-tool">
    Ambil dan baca konten dari URL tertentu untuk memperkaya konteks Claude dengan konten web langsung.
  </Card>

  <Card title="Alat server" icon="tool" href="/docs/id/agents-and-tools/tool-use/server-tools">
    Bekerja dengan alat yang dieksekusi Anthropic: blok server\_tool\_use, kelanjutan pause\_turn, dan pemfilteran domain.
  </Card>

  <Card title="Referensi alat" icon="book" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>
</CardGroup>
