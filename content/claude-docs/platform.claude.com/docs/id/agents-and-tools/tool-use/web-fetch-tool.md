---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool
fetched_at: 2026-09-17T02:21:00.513769Z
sha256: 277d871fea1931c456765e0b434ad9bf6c8dc277ba5af23d8830fb353db22b47
---

---
title: Alat web fetch
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool
description: Ambil dan baca konten dari URL tertentu untuk memperkaya konteks Claude dengan konten web terkini.
---

<Note>
  Untuk mempelajari bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku untuk fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

Alat web fetch memungkinkan Claude mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan.

Versi alat web fetch terbaru (`web_fetch_20260318`) mendukung **dynamic filtering** (pemfilteran dinamis). Dengan fitur ini, Claude dapat menulis dan mengeksekusi kode untuk memfilter konten yang diambil sebelum konten tersebut masuk ke "context window" (jendela konteks). Hanya informasi yang relevan yang disimpan, sedangkan sisanya dibuang. Cara ini mengurangi konsumsi token tanpa menurunkan kualitas respons. Pemfilteran dinamis tersedia untuk Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6. `web_fetch_20260318` juga menambahkan kontrol [response inclusion (penyertaan respons)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#response-inclusion) untuk alur kerja agentik. Versi-versi sebelumnya tetap tersedia: `web_fetch_20260309` untuk pemfilteran dinamis dan [cache bypass (pelewatan cache)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#cache-bypass), `web_fetch_20260209` khusus untuk pemfilteran dinamis, dan `web_fetch_20250910` untuk fetch dasar.

Web fetch (dengan maupun tanpa pemfilteran dinamis) tersedia di Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, deployment yang [di-hosting di Azure](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure) hanya mendukung alat web fetch dasar (`web_fetch_20250910`, tanpa pemfilteran dinamis). Deployment yang di-hosting di Anthropic mendukung semua versi. Web fetch saat ini belum tersedia di Amazon Bedrock maupun Google Cloud.

<Note>
  Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), web fetch tersedia di Claude API dan Microsoft Foundry. Fitur ini saat ini belum tersedia untuk Mythos Preview di Amazon Bedrock maupun Google Cloud.
</Note>

<Note>
  Gunakan [formulir umpan balik](https://forms.gle/NhWcgmkcvPCMmPE86) untuk memberikan masukan tentang kualitas respons model, API itu sendiri, atau kualitas dokumentasi.
</Note>

Untuk kelayakan Zero Data Retention dan solusi alternatif `allowed_callers`, lihat [Alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools#zdr-and-allowed-callers).

<Warning>
  Mengaktifkan alat web fetch di lingkungan tempat Claude memproses input yang tidak tepercaya bersama data sensitif menimbulkan risiko "data exfiltration" (eksfiltrasi data). Gunakan alat ini hanya di lingkungan tepercaya atau saat menangani data yang tidak sensitif.

  Untuk meminimalkan risiko eksfiltrasi, Claude tidak dapat mengambil URL yang hanya muncul dalam output-nya sendiri. Claude hanya dapat mengambil URL yang sebelumnya sudah muncul dalam percakapan, yaitu:

  * URL dalam pesan pengguna
  * URL dalam hasil alat sisi klien (termasuk ketika hasil tersebut mengulang teks yang dihasilkan Claude)
  * URL dari hasil web search atau web fetch sebelumnya (lihat [Validasi URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#url-validation))

  Meski demikian, masih ada risiko tersisa yang perlu Anda pertimbangkan dengan cermat saat menggunakan alat ini.

  Jika eksfiltrasi data menjadi perhatian, pertimbangkan untuk:

  * Menonaktifkan alat web fetch sepenuhnya
  * Menggunakan parameter `max_uses` untuk membatasi jumlah permintaan
  * Menggunakan parameter `allowed_domains` untuk membatasi akses hanya ke domain yang diketahui aman
</Warning>

Untuk dukungan model, lihat [Referensi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference).

## Cara kerja web fetch

Web fetch adalah sebuah ["server tool" (alat server)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools): API mengambil konten selama permintaan berlangsung dan menyisipkan hasilnya ke dalam percakapan. Anda tidak perlu menjalankan apa pun atau mengembalikan `tool_result`.

Ada satu pengecualian, yaitu ketika Claude memanggil web fetch bersamaan dengan salah satu alat klien Anda dalam kelompok panggilan alat paralel yang sama. Dalam kasus ini, API mengembalikan respons dengan `stop_reason: "tool_use"` sebelum fetch tersebut dijalankan. Fetch baru dijalankan setelah Anda mengirimkan kembali blok `tool_result` klien. Lihat [Menggabungkan alat server dan alat klien dalam satu giliran](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools#mixing-server-tools-and-client-tools-in-one-turn).

Saat Anda menambahkan alat web fetch ke permintaan API Anda:

1. Claude menentukan kapan harus mengambil konten berdasarkan prompt dan URL yang tersedia.
2. API mengambil konten teks lengkap dari URL yang ditentukan.
3. Untuk PDF, API mengembalikan konten sebagai data berenkode base64 dan memprosesnya seperti dokumen PDF yang dilampirkan secara langsung.
4. Claude menganalisis konten yang diambil dan memberikan respons, dengan sitasi opsional.

<Note>
  Alat web fetch saat ini tidak mendukung situs web yang dirender secara dinamis dengan JavaScript. Untuk halaman yang memerlukan browser sungguhan (rendering JavaScript, mengklik, atau mengisi formulir), pertimbangkan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool). Alat ini adalah alat klien: aplikasi Anda mengendalikan browser, lalu mengembalikan teks halaman atau tangkapan layar kepada Claude sebagai hasil alat.
</Note>

### Kapan Claude melakukan fetch

Claude melakukan fetch ketika permintaan merujuk ke halaman atau dokumen tertentu:

* Sebuah URL diberikan dalam percakapan (atau dalam hasil alat sebelumnya).
* Pengguna menyebutkan sumber daya tertentu tanpa URL (misalnya artikel, README, halaman harga, atau bagian dokumentasi tertentu), dan [alat web search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) juga diaktifkan sehingga Claude dapat menemukannya terlebih dahulu (lihat [Gabungan pencarian dan fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#combined-search-and-fetch)).

Claude **tidak** melakukan fetch untuk pertanyaan pengetahuan umum atau pertanyaan terbuka yang tidak merujuk ke halaman tertentu. Contohnya, "Ringkas artikel ini: `<url>`" akan memicu fetch, sedangkan "Apa praktik terbaik untuk desain REST API?" akan dijawab secara langsung.

### Pemfilteran dinamis

Mengambil halaman web dan PDF secara utuh dapat menghabiskan token dengan cepat, terutama jika Anda hanya membutuhkan informasi tertentu dari dokumen berukuran besar. Dengan `web_fetch_20260209` atau versi yang lebih baru, Claude dapat menulis dan mengeksekusi kode untuk memfilter konten yang diambil sebelum memuatnya ke dalam konteks.

Pemfilteran dinamis ini sangat berguna untuk:

* Mengekstrak bagian tertentu dari dokumen yang panjang
* Memproses data terstruktur dari halaman web
* Memfilter informasi yang relevan dari PDF
* Mengurangi biaya token saat bekerja dengan dokumen berukuran besar

<Note>
  Pemfilteran dinamis berjalan di atas [alat code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool), yang diaktifkan secara otomatis oleh API untuk permintaan tersebut. Anda tidak perlu menambahkan alat code execution ke array `tools`.
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
  fmt.Println(response.RawJSON())
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

Sertakan alat web fetch dalam permintaan API Anda:

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
  fmt.Println(response.RawJSON())
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

Versi alat yang lebih baru menambahkan dua parameter opsional lagi:

* `use_cache` memerlukan `web_fetch_20260309` atau versi yang lebih baru (lihat [Pelewatan cache](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#cache-bypass)).
* `response_inclusion` memerlukan `web_fetch_20260318` atau versi yang lebih baru (lihat [Penyertaan respons](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#response-inclusion)).

### Penggunaan maksimum

Parameter `max_uses` membatasi jumlah web fetch yang dilakukan. Fetch yang gagal tetap dihitung terhadap batas ini. Jika Claude mencoba melakukan fetch melebihi jumlah yang diizinkan, `web_fetch_tool_result` akan berupa error dengan kode error `max_uses_exceeded`. Saat ini tidak ada batas default.

### Pemfilteran domain

Untuk pemfilteran domain dengan `allowed_domains` dan `blocked_domains`, lihat [Alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering).

Di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), atur kolom-kolom ini pada entri `web_fetch` di toolset agen. Setiap domain yang dicantumkan harus berupa hostname biasa tanpa path. Lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools#restrict-web-search-and-web-fetch-domains).

### Batas konten

Parameter `max_content_tokens` membatasi jumlah konten yang disertakan dalam konteks. Jika konten yang diambil melebihi batas ini, alat akan memotongnya. Parameter ini membantu mengendalikan penggunaan token saat mengambil dokumen berukuran besar. Batas ini berlaku untuk konten teks, bukan untuk konten biner seperti PDF.

<Note>
  Batas parameter `max_content_tokens` bersifat perkiraan. Jumlah token input yang sebenarnya digunakan dapat sedikit berbeda.
</Note>

Di Claude Managed Agents, entri `web_fetch` di toolset agen juga menerima `max_content_tokens`. Lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools#restrict-web-search-and-web-fetch-domains).

### Pelewatan cache

<Note>
  Memerlukan `web_fetch_20260309` atau versi yang lebih baru (termasuk `web_fetch_20260318`).
</Note>

Parameter `use_cache` mengontrol apakah konten yang di-cache boleh dikembalikan. Atur `"use_cache": false` untuk melewati cache dan mengambil konten terbaru. Nilai default-nya adalah `true`.

Karena melewati cache meningkatkan "latency" (latensi), nonaktifkan caching hanya jika:

* pengguna secara eksplisit meminta konten terbaru, atau
* Anda mengambil konten dari sumber yang berubah dengan cepat.

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

### Penyertaan respons

<Note>
  Memerlukan `web_fetch_20260318` atau versi yang lebih baru.
</Note>

Parameter `response_inclusion` mengontrol cara blok hasil fetch ditampilkan dalam respons API, khusus untuk hasil yang telah digunakan oleh panggilan [code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) yang sudah selesai dalam giliran yang sama. Nilai default-nya adalah `"full"`.

Atur `"response_inclusion": "excluded"` untuk menghapus sepenuhnya pasangan blok `server_tool_use` dan blok hasil yang bersarang tersebut dari respons. Pengaturan ini mengurangi biaya token output untuk alur kerja agentik yang tidak perlu mengirimkan kembali konten halaman mentah ke klien.

Hasil dari panggilan langsung, atau dari panggilan code execution yang dijeda sebelum selesai, selalu dikembalikan secara lengkap agar dapat dikirim kembali pada giliran berikutnya.

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

Berbeda dengan web search yang sitasinya selalu aktif, sitasi pada web fetch bersifat opsional dan dinonaktifkan secara default. Atur `"citations": {"enabled": true}` agar Claude dapat mengutip bagian tertentu dari dokumen yang diambil.

<Note>
  Saat menampilkan output API secara langsung kepada pengguna akhir, sertakan sitasi ke sumber aslinya. Jika Anda memodifikasi output API sebelum menampilkannya kepada pengguna akhir, termasuk dengan memproses ulang atau menggabungkannya dengan materi Anda sendiri, tampilkan sitasi sebagaimana mestinya berdasarkan konsultasi dengan tim hukum Anda.
</Note>

## Respons

Berikut contoh struktur respons:

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
* `retrieved_at`: Stempel waktu saat konten diambil

<Note>
  Alat web fetch menyimpan hasil dalam cache untuk meningkatkan performa dan mengurangi permintaan yang berulang. Akibatnya, konten yang dikembalikan mungkin tidak selalu mencerminkan versi terbaru yang tersedia di URL tersebut. Perilaku cache dikelola secara otomatis dan dapat berubah seiring waktu untuk mengoptimalkan berbagai jenis konten dan pola penggunaan. Untuk mengambil konten terbaru, atur `"use_cache": false` (lihat [Pelewatan cache](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#cache-bypass)).
</Note>

Untuk dokumen PDF, konten dikembalikan sebagai data berenkode base64:

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

Ketika alat web fetch mengalami error, Claude API tetap mengembalikan respons 200 (sukses), dengan error dicantumkan di dalam body respons. Claude melihat hasil error tersebut dan melanjutkan gilirannya. Contohnya:

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

Berikut kode error yang mungkin muncul:

* `invalid_tool_input`: Input alat tidak valid, misalnya URL yang formatnya salah atau skema selain HTTP(S)
* `url_too_long`: URL melebihi panjang maksimum (250 karakter)
* `url_not_allowed`: URL diblokir oleh aturan pemfilteran domain (termasuk pengaturan organisasi Anda) atau oleh pembatasan dari sisi Anthropic, seperti alamat privat dan `robots.txt`
* `url_not_in_prior_context`: URL belum pernah muncul sebelumnya dalam percakapan (lihat [Validasi URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#url-validation))
* `url_not_accessible`: Gagal mengambil konten (error HTTP)
* `too_many_requests`: "Rate limit" (batas laju) terlampaui
* `unsupported_content_type`: Jenis konten tidak didukung (hanya teks, HTML, dan PDF yang didukung)
* `max_uses_exceeded`: Jumlah penggunaan maksimum alat web fetch terlampaui
* `unavailable`: Terjadi error internal

## Validasi URL

Demi keamanan, alat web fetch hanya dapat mengambil URL yang sebelumnya sudah muncul dalam konteks percakapan. Ini mencakup:

* URL dalam pesan pengguna
* URL dalam hasil alat sisi klien
* URL dari hasil web search atau web fetch sebelumnya

Alat ini tidak dapat mengambil URL yang hanya muncul dalam output Claude sendiri atau hanya dalam "system prompt" (prompt sistem). Agar URL dari prompt sistem dapat diambil, sertakan juga URL tersebut dalam pesan pengguna.

Hasil dari alat sisi server lainnya juga bukan sumber yang diizinkan. Contohnya adalah [code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool), [konektor "Model Context Protocol", atau MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector), dan [tool search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool).

Sebaliknya, hasil alat sisi klien tetap merupakan sumber yang diizinkan, bahkan ketika hasil tersebut mengulang teks yang dihasilkan Claude. Contohnya adalah perintah yang mencetak input-nya, atau pesan error yang mengutip input tersebut.

## Gabungan pencarian dan fetch

Ketika alat web search dan web fetch sama-sama diaktifkan, dan pengguna menyebutkan halaman atau dokumen tertentu tanpa memberikan URL, Claude menggunakan web search untuk menemukannya, lalu mengambil hasilnya. Contoh permintaan seperti ini adalah "baca README dari repositori anthropics/anthropic-sdk-python". Contoh berikut meminta pencarian dan analisis dalam satu permintaan:

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
  fmt.Println(response.RawJSON())
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
4. Memberikan analisis mendetail beserta sitasi.

## Caching prompt

Untuk menyimpan definisi alat dalam cache di seluruh giliran, lihat ["Tool use" (penggunaan alat) dengan "prompt caching" (caching prompt)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

## Streaming

Saat streaming diaktifkan, event fetch menjadi bagian dari stream, dengan jeda selama proses pengambilan konten:

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

Anda dapat menyertakan alat web fetch dalam [Messages Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing). Harga panggilan alat web fetch melalui Messages Batches API sama dengan harga panggilan dalam permintaan Messages API biasa.

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

Alat web fetch tersedia di Claude API **tanpa biaya tambahan**. Anda hanya membayar biaya token standar untuk konten yang diambil yang menjadi bagian dari konteks percakapan Anda.

Untuk melindungi dari pengambilan konten besar secara tidak sengaja yang akan menghabiskan token secara berlebihan, gunakan parameter `max_content_tokens` untuk menetapkan batas yang sesuai berdasarkan kasus penggunaan dan pertimbangan anggaran Anda.

Contoh penggunaan token untuk konten umum:

* Halaman web rata-rata (10 kB): \~2.500 token
* Halaman dokumentasi besar (100 kB): \~25.000 token
* PDF makalah penelitian (500 kB): \~125.000 token

## Langkah selanjutnya

<CardGroup>
  <Card href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool" title="Alat code execution" icon="code">
    Jalankan kode Python dan bash dalam container sandbox untuk menganalisis data, menghasilkan file, dan menyempurnakan solusi secara iteratif.
  </Card>

  <Card href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools" title="Alat server" icon="cloud">
    Bekerja dengan alat yang dieksekusi oleh Anthropic: blok server\_tool\_use, kelanjutan pause\_turn, dan pemfilteran domain.
  </Card>

  <Card href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat" icon="book">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti opsional definisi alat.
  </Card>
</CardGroup>
