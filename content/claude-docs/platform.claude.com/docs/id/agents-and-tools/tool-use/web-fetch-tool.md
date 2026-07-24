---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: cd2604e788071905a77b34cf51787e4b3f6e638ffaf96e93561ed71577c38dce
---

# Alat web fetch

Ambil dan baca konten dari URL tertentu untuk memperkaya konteks Claude dengan konten web langsung.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

Alat web fetch memungkinkan Claude mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan.

Versi alat web fetch terbaru (`web_fetch_20260318`) mendukung **dynamic filtering** (pemfilteran dinamis) dengan Claude Fable 5, Claude Opus 4.8, Claude Mythos 5, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6. Claude dapat menulis dan mengeksekusi kode untuk memfilter konten yang diambil sebelum mencapai jendela konteks, hanya menyimpan informasi yang relevan dan membuang sisanya. Ini mengurangi konsumsi token sambil mempertahankan kualitas respons. `web_fetch_20260318` juga menambahkan kontrol [response inclusion](#response-inclusion) untuk alur kerja agentik. Versi sebelumnya (`web_fetch_20260309` untuk pemfilteran dinamis dan [cache bypass](#cache-bypass), `web_fetch_20260209` untuk pemfilteran dinamis saja, `web_fetch_20250910` untuk fetch dasar) tetap tersedia.

Web fetch (dengan dan tanpa pemfilteran dinamis) tersedia di Claude API, [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, web fetch memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure). Saat ini belum tersedia di Amazon Bedrock atau Google Cloud.

<Note>
  Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), web fetch tersedia di Claude API dan Microsoft Foundry. Saat ini belum tersedia untuk Mythos Preview di Amazon Bedrock atau Google Cloud.
</Note>

<Note>
  Gunakan [formulir umpan balik](https://forms.gle/NhWcgmkcvPCMmPE86) untuk memberikan umpan balik tentang kualitas respons model, API itu sendiri, atau kualitas dokumentasi.
</Note>

Untuk kelayakan Zero Data Retention dan solusi `allowed_callers`, lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#zdr-and-allowed-callers).

<Warning>
  Mengaktifkan alat web fetch di lingkungan tempat Claude memproses input yang tidak tepercaya bersama data sensitif menimbulkan risiko eksfiltrasi data. Hanya gunakan alat ini di lingkungan tepercaya atau saat menangani data yang tidak sensitif.

  Untuk meminimalkan risiko eksfiltrasi, Claude tidak diizinkan membangun URL secara dinamis. Claude hanya dapat mengambil URL yang telah diberikan secara eksplisit oleh pengguna atau yang berasal dari hasil web search atau web fetch sebelumnya. Namun, masih ada risiko residual yang harus Anda pertimbangkan dengan cermat saat menggunakan alat ini.

  Jika eksfiltrasi data menjadi perhatian, pertimbangkan:

  * Menonaktifkan alat web fetch sepenuhnya
  * Menggunakan parameter `max_uses` untuk membatasi jumlah permintaan
  * Menggunakan parameter `allowed_domains` untuk membatasi ke domain yang diketahui aman
</Warning>

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Cara kerja web fetch

Web fetch adalah [alat server](/docs/id/agents-and-tools/tool-use/server-tools): API mengambil konten selama permintaan dan menyisipkan hasilnya ke dalam percakapan. Anda tidak menjalankan apa pun atau mengembalikan `tool_result`. Pengecualiannya adalah ketika Claude memanggil web fetch dan salah satu alat klien Anda dalam grup panggilan alat paralel yang sama: API mengembalikan respons dengan `stop_reason: "tool_use"` sebelum fetch tersebut dijalankan, lalu menjalankan fetch ketika Anda mengirim kembali blok `tool_result` klien. Lihat [Mencampur alat server dan alat klien dalam satu giliran](/docs/id/agents-and-tools/tool-use/server-tools#mixing-server-tools-and-client-tools-in-one-turn).

Ketika Anda menambahkan alat web fetch ke permintaan API Anda:

1. Claude menentukan kapan mengambil konten berdasarkan prompt dan URL yang tersedia.
2. API mengambil konten teks lengkap dari URL yang ditentukan.
3. Untuk PDF, API mengembalikan konten sebagai data yang dikodekan base64 dan memprosesnya seperti dokumen PDF yang dilampirkan langsung.
4. Claude menganalisis konten yang diambil dan memberikan respons dengan sitasi opsional.

<Note>
  Alat web fetch saat ini tidak mendukung situs web yang dirender secara dinamis dengan JavaScript.
</Note>

### Kapan Claude melakukan fetch

Claude melakukan fetch ketika permintaan menunjuk ke halaman atau dokumen tertentu:

* URL diberikan dalam percakapan (atau hasil alat sebelumnya)
* Pengguna menyebutkan sumber daya tertentu (artikel tertentu, README, halaman harga, atau bagian dokumentasi) tanpa URL, dan [alat web search](/docs/id/agents-and-tools/tool-use/web-search-tool) juga diaktifkan sehingga Claude dapat menemukannya terlebih dahulu (lihat [Pencarian dan fetch gabungan](#combined-search-and-fetch))

Claude **tidak** melakukan fetch untuk pertanyaan pengetahuan umum atau pertanyaan terbuka yang tidak merujuk ke halaman tertentu. "Ringkas artikel ini: `<url>`" memicu fetch. "Apa praktik terbaik untuk desain REST API?" dijawab secara langsung.

### Pemfilteran dinamis

Mengambil halaman web dan PDF lengkap dapat dengan cepat menghabiskan token, terutama ketika hanya informasi tertentu yang dibutuhkan dari dokumen besar. Dengan `web_fetch_20260209` atau yang lebih baru, Claude dapat menulis dan mengeksekusi kode untuk memfilter konten yang diambil sebelum memuatnya ke dalam konteks.

Pemfilteran dinamis ini sangat berguna untuk:

* Mengekstrak bagian tertentu dari dokumen panjang
* Memproses data terstruktur dari halaman web
* Memfilter informasi yang relevan dari PDF
* Mengurangi biaya token saat bekerja dengan dokumen besar

<Note>
  Pemfilteran dinamis berjalan pada [alat code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool), yang diaktifkan secara otomatis oleh API untuk permintaan tersebut. Anda tidak perlu menambahkan alat code execution ke array `tools`.
</Note>

Untuk mengaktifkan pemfilteran dinamis, gunakan `web_fetch_20260209` atau versi yang lebih baru. Contoh berikut menggunakan `web_fetch_20260318`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [
        {
          "role": "user",
          "content": "Fetch the content at https://example.com/research-paper and extract the key findings."
        }
      ],
      "tools": [{
        "type": "web_fetch_20260318",
        "name": "web_fetch"
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
        Fetch the content at https://example.com/research-paper
        and extract the key findings.
  tools:
    - type: web_fetch_20260318
      name: web_fetch
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
              "content": "Fetch the content at https://example.com/research-paper and extract the key findings.",
          }
      ],
      tools=[{"type": "web_fetch_20260318", "name": "web_fetch"}],
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
          "Fetch the content at https://example.com/research-paper and extract the key findings."
      }
    ],
    tools: [{ type: "web_fetch_20260318", name: "web_fetch" }]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Fetch the content at https://example.com/research-paper and extract the key findings." }],
      Tools = [new ToolUnion(new WebFetchTool20260318())]
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
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Fetch the content at https://example.com/research-paper and extract the key findings.")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfWebFetchTool20260318: &anthropic.WebFetchTool20260318Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.WebFetchTool20260318;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(4096L)
          .addUserMessage("Fetch the content at https://example.com/research-paper and extract the key findings.")
          .addTool(WebFetchTool20260318.builder().build())
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
          ['role' => 'user', 'content' => 'Fetch the content at https://example.com/research-paper and extract the key findings.']
      ],
      model: 'claude-opus-4-8',
      tools: [[
          'type' => 'web_fetch_20260318',
          'name' => 'web_fetch',
      ]],
  );
  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Fetch the content at https://example.com/research-paper and extract the key findings." }
    ],
    tools: [{
      type: "web_fetch_20260318",
      name: "web_fetch"
    }]
  )
  puts message
  ```
</CodeGroup>

## Cara menggunakan web fetch

Sediakan alat web fetch dalam permintaan API Anda:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": "Please analyze the content at https://example.com/article"
        }
      ],
      "tools": [{
        "type": "web_fetch_20250910",
        "name": "web_fetch",
        "max_uses": 5
      }]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Please analyze the content at https://example.com/article"}' \
    --tool '{type: web_fetch_20250910, name: web_fetch, max_uses: 5}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Please analyze the content at https://example.com/article",
          }
      ],
      tools=[{"type": "web_fetch_20250910", "name": "web_fetch", "max_uses": 5}],
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
        content: "Please analyze the content at https://example.com/article"
      }
    ],
    tools: [
      {
        type: "web_fetch_20250910",
        name: "web_fetch",
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
      Messages = [new() { Role = Role.User, Content = "Please analyze the content at https://example.com/article" }],
      Tools = [new ToolUnion(new WebFetchTool20250910() { MaxUses = 5 })]
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
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Please analyze the content at https://example.com/article")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfWebFetchTool20250910: &anthropic.WebFetchTool20250910Param{
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
  import com.anthropic.models.messages.WebFetchTool20250910;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addUserMessage("Please analyze the content at https://example.com/article")
          .addTool(WebFetchTool20250910.builder()
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
          ['role' => 'user', 'content' => 'Please analyze the content at https://example.com/article']
      ],
      model: 'claude-opus-4-8',
      tools: [[
          'type' => 'web_fetch_20250910',
          'name' => 'web_fetch',
          'max_uses' => 5,
      ]],
  );
  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "Please analyze the content at https://example.com/article" }
    ],
    tools: [{
      type: "web_fetch_20250910",
      name: "web_fetch",
      max_uses: 5
    }]
  )
  puts message
  ```
</CodeGroup>

## Definisi alat

Alat web fetch mendukung parameter berikut:

```json JSON
{
  "type": "web_fetch_20250910",
  "name": "web_fetch",

  // Optional: Limit the number of fetches per request
  "max_uses": 10,

  // Optional: Only fetch from these domains
  "allowed_domains": ["example.com", "docs.example.com"],

  // Optional: Never fetch from these domains (cannot be combined with allowed_domains)
  "blocked_domains": ["private.example.com"],

  // Optional: Enable citations for fetched content
  "citations": {
    "enabled": true
  },

  // Optional: Maximum content length in tokens
  "max_content_tokens": 100000
}
```

Versi alat yang lebih baru menambahkan dua parameter opsional lagi: `use_cache` memerlukan `web_fetch_20260309` atau yang lebih baru (lihat [Bypass cache](#cache-bypass)), dan `response_inclusion` memerlukan `web_fetch_20260318` atau yang lebih baru (lihat [Inklusi respons](#response-inclusion)).

### Penggunaan maksimum

Parameter `max_uses` membatasi jumlah web fetch yang dilakukan. Fetch yang gagal tetap dihitung terhadap batas. Jika Claude mencoba melakukan fetch lebih banyak dari yang diizinkan, `web_fetch_tool_result` akan berupa error dengan kode error `max_uses_exceeded`. Saat ini tidak ada batas default.

### Pemfilteran domain

Untuk pemfilteran domain dengan `allowed_domains` dan `blocked_domains`, lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering).

### Batas konten

Parameter `max_content_tokens` membatasi jumlah konten yang disertakan dalam konteks. Jika konten yang diambil melebihi batas ini, alat akan memotongnya. Ini membantu mengontrol penggunaan token saat mengambil dokumen besar. Batas ini berlaku untuk konten teks, bukan untuk konten biner seperti PDF.

<Note>
  Batas parameter `max_content_tokens` bersifat perkiraan. Jumlah input token yang sebenarnya digunakan dapat bervariasi dalam jumlah kecil.
</Note>

### Bypass cache

<Note>
  Memerlukan `web_fetch_20260309` atau yang lebih baru (termasuk `web_fetch_20260318`).
</Note>

Parameter `use_cache` mengontrol apakah konten yang di-cache boleh dikembalikan. Atur `"use_cache": false` untuk melewati cache dan mengambil konten baru. Nilai default-nya adalah `true`. Hanya nonaktifkan caching ketika pengguna secara eksplisit meminta konten baru atau saat mengambil sumber yang berubah dengan cepat, karena melewati cache meningkatkan latensi.

```json
{
  "tools": [
    {
      "type": "web_fetch_20260309",
      "name": "web_fetch",
      "use_cache": false
    }
  ]
}
```

### Inklusi respons

<Note>
  Memerlukan `web_fetch_20260318` atau yang lebih baru.
</Note>

Parameter `response_inclusion` mengontrol bagaimana blok hasil fetch muncul dalam respons API ketika hasilnya dikonsumsi oleh panggilan [code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool) yang selesai dalam giliran yang sama. Atur `"response_inclusion": "excluded"` untuk menghapus pasangan blok `server_tool_use` dan blok hasil yang bersarang tersebut sepenuhnya dari respons, mengurangi biaya output token untuk alur kerja agentik yang tidak perlu menggemakan konten halaman mentah kembali ke klien. Nilai default-nya adalah `"full"`. Hasil dari panggilan langsung, atau dari panggilan code execution yang dijeda sebelum selesai, selalu dikembalikan secara penuh sehingga dapat dikirim kembali pada giliran berikutnya.

```json
{
  "tools": [
    {
      "type": "web_fetch_20260318",
      "name": "web_fetch",
      "response_inclusion": "excluded"
    }
  ]
}
```

### Sitasi

Tidak seperti web search di mana sitasi selalu diaktifkan, sitasi bersifat opsional untuk web fetch dan dinonaktifkan secara default. Atur `"citations": {"enabled": true}` untuk memungkinkan Claude mengutip bagian tertentu dari dokumen yang diambil.

<Note>
  Saat menampilkan output API langsung kepada pengguna akhir, sertakan sitasi ke sumber aslinya. Jika Anda melakukan modifikasi pada output API, termasuk dengan memproses ulang dan/atau menggabungkannya dengan materi Anda sendiri sebelum menampilkannya kepada pengguna akhir, tampilkan sitasi sebagaimana mestinya berdasarkan konsultasi dengan tim hukum Anda.
</Note>

## Respons

Berikut adalah contoh struktur respons:

```json Output
{
  "role": "assistant",
  "content": [
    // 1. Claude's decision to fetch
    {
      "type": "text",
      "text": "I'll fetch the content from the article to analyze it."
    },
    // 2. The fetch request
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01234567890abcdef",
      "name": "web_fetch",
      "input": {
        "url": "https://example.com/article"
      }
    },
    // 3. Fetch results
    {
      "type": "web_fetch_tool_result",
      "tool_use_id": "srvtoolu_01234567890abcdef",
      "content": {
        "type": "web_fetch_result",
        "url": "https://example.com/article",
        "content": {
          "type": "document",
          "source": {
            "type": "text",
            "media_type": "text/plain",
            "data": "Full text content of the article..."
          },
          "title": "Article Title",
          "citations": { "enabled": true }
        },
        "retrieved_at": "2025-08-25T10:30:00Z"
      }
    },
    // 4. Claude's analysis with citations (if enabled)
    {
      "text": "Based on the article, ",
      "type": "text"
    },
    {
      "text": "the main argument presented is that artificial intelligence will transform healthcare",
      "type": "text",
      "citations": [
        {
          "type": "char_location",
          "document_index": 0,
          "document_title": "Article Title",
          "start_char_index": 1234,
          "end_char_index": 1456,
          "cited_text": "Artificial intelligence is poised to revolutionize healthcare delivery..."
        }
      ]
    }
  ],
  "id": "msg_a930390d3a",
  "usage": {
    "input_tokens": 25039,
    "output_tokens": 931,
    "server_tool_use": {
      "web_fetch_requests": 1
    }
  },
  "stop_reason": "end_turn"
}
```

### Hasil fetch

Hasil fetch mencakup:

* `url`: URL yang diambil
* `content`: Blok dokumen yang berisi konten yang diambil
* `retrieved_at`: Timestamp saat konten diambil

<Note>
  Alat web fetch menyimpan hasil dalam cache untuk meningkatkan kinerja dan mengurangi permintaan yang berlebihan. Konten yang dikembalikan mungkin tidak selalu mencerminkan versi terbaru yang tersedia di URL tersebut. Perilaku cache dikelola secara otomatis dan dapat berubah seiring waktu untuk mengoptimalkan berbagai jenis konten dan pola penggunaan. Untuk mengambil konten baru, atur `"use_cache": false` (lihat [Bypass cache](#cache-bypass)).
</Note>

Untuk dokumen PDF, konten dikembalikan sebagai data yang dikodekan base64:

```json Output
{
  "type": "web_fetch_tool_result",
  "tool_use_id": "srvtoolu_02",
  "content": {
    "type": "web_fetch_result",
    "url": "https://example.com/paper.pdf",
    "content": {
      "type": "document",
      "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": "JVBERi0xLjQKJcOkw7zDtsOfCjIgMCBvYmo..."
      },
      "citations": { "enabled": true }
    },
    "retrieved_at": "2025-08-25T10:30:02Z"
  }
}
```

### Error

Ketika alat web fetch mengalami error, Claude API mengembalikan respons 200 (sukses) dengan error yang direpresentasikan dalam body respons. Claude melihat hasil error dan melanjutkan giliran. Sebagai contoh:

```json Output
{
  "type": "web_fetch_tool_result",
  "tool_use_id": "srvtoolu_a93jad",
  "content": {
    "type": "web_fetch_tool_result_error",
    "error_code": "url_not_accessible"
  }
}
```

Berikut adalah kode error yang mungkin terjadi:

* `invalid_tool_input`: Input alat tidak valid, seperti URL yang salah format atau skema non-HTTP(S)
* `url_too_long`: URL melebihi panjang maksimum (250 karakter)
* `url_not_allowed`: URL diblokir oleh aturan pemfilteran domain (termasuk pengaturan organisasi Anda) atau oleh pembatasan di sisi Anthropic, seperti alamat privat dan `robots.txt`
* `url_not_in_prior_context`: URL tidak muncul sebelumnya dalam percakapan (lihat [Validasi URL](#url-validation))
* `url_not_accessible`: Gagal mengambil konten (error HTTP)
* `too_many_requests`: Batas laju terlampaui
* `unsupported_content_type`: Jenis konten tidak didukung (hanya teks, HTML, dan PDF)
* `max_uses_exceeded`: Penggunaan maksimum alat web fetch terlampaui
* `unavailable`: Terjadi error internal

## Validasi URL

Untuk alasan keamanan, alat web fetch hanya dapat mengambil URL yang sebelumnya telah muncul dalam konteks percakapan. Ini mencakup:

* URL dalam pesan pengguna
* URL dalam hasil alat sisi klien
* URL dari hasil web search atau web fetch sebelumnya

Alat ini tidak dapat mengambil URL sembarang yang dihasilkan Claude atau URL dari alat server berbasis container (seperti Code Execution dan Bash).

## Pencarian dan fetch gabungan

Ketika alat web search dan web fetch keduanya diaktifkan, dan pengguna menyebutkan halaman atau dokumen tertentu tanpa memberikan URL (misalnya, "baca README dari repositori anthropics/anthropic-sdk-python"), Claude menggunakan web search untuk menemukannya, lalu mengambil hasilnya. Contoh berikut meminta pencarian dan analisis dalam satu permintaan:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [
        {
          "role": "user",
          "content": "Find recent articles about quantum computing and analyze the most relevant one in detail"
        }
      ],
      "tools": [
        {
          "type": "web_search_20250305",
          "name": "web_search",
          "max_uses": 3
        },
        {
          "type": "web_fetch_20250910",
          "name": "web_fetch",
          "max_uses": 5,
          "citations": {"enabled": true}
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: >-
        Find recent articles about quantum computing
        and analyze the most relevant one in detail
  tools:
    - type: web_search_20250305
      name: web_search
      max_uses: 3
    - type: web_fetch_20250910
      name: web_fetch
      max_uses: 5
      citations:
        enabled: true
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
              "content": "Find recent articles about quantum computing and analyze the most relevant one in detail",
          }
      ],
      tools=[
          {"type": "web_search_20250305", "name": "web_search", "max_uses": 3},
          {
              "type": "web_fetch_20250910",
              "name": "web_fetch",
              "max_uses": 5,
              "citations": {"enabled": True},
          },
      ],
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
          "Find recent articles about quantum computing and analyze the most relevant one in detail"
      }
    ],
    tools: [
      { type: "web_search_20250305", name: "web_search", max_uses: 3 },
      {
        type: "web_fetch_20250910",
        name: "web_fetch",
        max_uses: 5,
        citations: { enabled: true }
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
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Find recent articles about quantum computing and analyze the most relevant one in detail" }],
      Tools = [
          new ToolUnion(new WebSearchTool20250305() { MaxUses = 3 }),
          new ToolUnion(new WebFetchTool20250910() { MaxUses = 5, Citations = new() { Enabled = true } })
      ]
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
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Find recent articles about quantum computing and analyze the most relevant one in detail")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfWebSearchTool20250305: &anthropic.WebSearchTool20250305Param{
  			MaxUses: anthropic.Int(3),
  		}},
  		{OfWebFetchTool20250910: &anthropic.WebFetchTool20250910Param{
  			MaxUses:   anthropic.Int(5),
  			Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  		}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.CitationsConfigParam;
  // ...
  import com.anthropic.models.messages.WebFetchTool20250910;
  import com.anthropic.models.messages.WebSearchTool20250305;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(4096L)
          .addUserMessage("Find recent articles about quantum computing and analyze the most relevant one in detail")
          .addTool(WebSearchTool20250305.builder()
              .maxUses(3L)
              .build())
          .addTool(WebFetchTool20250910.builder()
              .maxUses(5L)
              .citations(CitationsConfigParam.builder().enabled(true).build())
              .build())
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
          ['role' => 'user', 'content' => 'Find recent articles about quantum computing and analyze the most relevant one in detail']
      ],
      model: 'claude-opus-4-8',
      tools: [
          [
              'type' => 'web_search_20250305',
              'name' => 'web_search',
              'max_uses' => 3,
          ],
          [
              'type' => 'web_fetch_20250910',
              'name' => 'web_fetch',
              'max_uses' => 5,
              'citations' => ['enabled' => true],
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
      { role: "user", content: "Find recent articles about quantum computing and analyze the most relevant one in detail" }
    ],
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 3
      },
      {
        type: "web_fetch_20250910",
        name: "web_fetch",
        max_uses: 5,
        citations: { enabled: true }
      }
    ]
  )
  puts message
  ```
</CodeGroup>

Dalam alur kerja ini, Claude:

1. Menggunakan web search untuk menemukan artikel yang relevan.
2. Memilih hasil yang paling menjanjikan.
3. Menggunakan web fetch untuk mengambil konten lengkap.
4. Memberikan analisis terperinci dengan sitasi.

## Caching prompt

Untuk caching definisi alat di seluruh giliran, lihat [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

## Streaming

Dengan streaming diaktifkan, event fetch menjadi bagian dari stream dengan jeda selama pengambilan konten:

```sse Output
event: message_start
data: {"type": "message_start", "message": {"id": "msg_abc123", "type": "message"}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

// Claude's decision to fetch

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "web_fetch"}}

// Fetch URL streamed
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"url\":\"https://example.com/article\"}"}}

// Pause while fetch executes

// Fetch results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "web_fetch_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"type": "web_fetch_result", "url": "https://example.com/article", "content": {"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "Article content..."}}}}}

// Claude's response continues...
```

## Permintaan batch

Anda dapat menyertakan alat web fetch dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Panggilan alat web fetch melalui Messages Batches API dikenakan harga yang sama dengan panggilan dalam permintaan Messages API reguler.

## Penggunaan dan harga

Penggunaan web fetch **tidak dikenakan biaya tambahan** di luar biaya token standar:

```json
{
  "usage": {
    "input_tokens": 25039,
    "output_tokens": 931,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0,
    "server_tool_use": {
      "web_fetch_requests": 1
    }
  }
}
```

Alat web fetch tersedia di Claude API **tanpa biaya tambahan**. Anda hanya membayar biaya token standar untuk konten yang diambil dan menjadi bagian dari konteks percakapan Anda.

Untuk melindungi dari pengambilan konten berukuran besar secara tidak sengaja yang akan menghabiskan token secara berlebihan, gunakan parameter `max_content_tokens` untuk menetapkan batas yang sesuai berdasarkan kasus penggunaan dan pertimbangan anggaran Anda.

Contoh penggunaan token untuk konten umum:

* Halaman web rata-rata (10 kB): \~2.500 token
* Halaman dokumentasi besar (100 kB): \~25.000 token
* PDF makalah penelitian (500 kB): \~125.000 token

## Langkah selanjutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/code-execution-tool" title="Alat code execution" icon="code">
    Jalankan kode Python dan bash dalam container yang di-sandbox untuk menganalisis data, menghasilkan file, dan mengiterasi solusi.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/server-tools" title="Alat server" icon="cloud">
    Bekerja dengan alat yang dieksekusi Anthropic: blok server\_tool\_use, kelanjutan pause\_turn, dan pemfilteran domain.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat" icon="book">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>
</CardGroup>
