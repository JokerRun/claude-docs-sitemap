---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 696e10afad354c6bb80eab6abceabca16cecd5955f2be80cc16b78695e75fdd3
---

---
title: Alat web fetch
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool
description: Ambil dan baca konten dari URL tertentu untuk memperkaya konteks Claude dengan konten web langsung.
featureMetadata:
  status: stable
  zdr:
    eligibility: eligible
    note: Excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements). Konten web yang diambil dikembalikan dalam respons API. Pemfilteran dinamis untuk web fetch tidak memenuhi syarat kelayakan ZDR atau HIPAA. Penerbit situs web mungkin menyimpan data permintaan (seperti URL yang diambil dan metadata permintaan) sesuai kebijakan mereka sendiri.
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: stable
    Claude Platform on AWS: stable
    Claude Models on Google Cloud (Anthropic managed): stable
    Microsoft Foundry:
      availability: stable
      note: "Deployment yang di-host di Azure hanya mendukung `web_fetch_20250910`: tanpa pemfilteran dinamis, penyertaan respons, atau bypass cache."
---

**Dukungan API**: Penggunaan berbeda menurut produk.

* **Messages API**: Tambahkan alat `web_fetch` ke `tools` permintaan.
* **Managed Agents**: Aktif secara default dalam toolset agen, tanpa `max_uses`, `citations`, atau `cache_control`.

Alat web fetch memungkinkan Claude mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan.

Versi terbaru alat web fetch (`web_fetch_20260318`) mendukung **dynamic filtering** (pemfilteran dinamis): Claude dapat menulis dan mengeksekusi kode untuk memfilter konten yang diambil sebelum mencapai “context window” (jendela konteks), sehingga hanya informasi yang relevan yang disimpan dan sisanya dibuang. Ini mengurangi konsumsi token sambil mempertahankan kualitas respons. Pemfilteran dinamis tersedia dengan model Claude 4.6 dan yang lebih baru serta [Claude Mythos Preview](https://anthropic.com/glasswing). `web_fetch_20260318` juga menambahkan kontrol [response inclusion](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#response-inclusion) (penyertaan respons) untuk alur kerja agentic. Versi sebelumnya (`web_fetch_20260309` untuk pemfilteran dinamis dan [cache bypass](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#cache-bypass), `web_fetch_20260209` hanya untuk pemfilteran dinamis, `web_fetch_20250910` untuk fetch dasar) tetap tersedia.

Web fetch (dengan dan tanpa pemfilteran dinamis) tersedia di Claude API, [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, deployment yang [di-host di Azure](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure) hanya mendukung alat web fetch dasar (`web_fetch_20250910`, tanpa pemfilteran dinamis). Deployment yang di-host di Anthropic mendukung semua versi.

<Note>
  Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), web fetch tersedia di Claude API dan Microsoft Foundry.
</Note>

<Note>
  Gunakan [formulir umpan balik](https://forms.gle/NhWcgmkcvPCMmPE86) untuk memberikan umpan balik tentang kualitas respons model, API itu sendiri, atau kualitas dokumentasi.
</Note>

Untuk kelayakan Zero Data Retention dan solusi `allowed_callers`, lihat [Alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools#zdr-and-allowed-callers).

<Warning>
  Mengaktifkan alat web fetch di lingkungan tempat Claude memproses input yang tidak tepercaya bersama data sensitif menimbulkan risiko eksfiltrasi data. Gunakan alat ini hanya di lingkungan tepercaya atau saat menangani data yang tidak sensitif.

  Untuk meminimalkan risiko eksfiltrasi, Claude tidak dapat mengambil URL yang hanya muncul di output-nya sendiri. Claude hanya dapat mengambil URL yang sebelumnya telah muncul dalam percakapan: URL dalam pesan pengguna, URL dalam hasil alat sisi klien, dan URL dari hasil web search atau web fetch sebelumnya (lihat [Validasi URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#url-validation)). Claude juga tidak dapat mengambil URL yang tampaknya berisi kredensial, seperti kunci API atau kata sandi, kecuali kredensial tersebut muncul di prompt sistem atau di teks pesan pengguna.

  Namun, masih ada risiko residual yang harus Anda pertimbangkan dengan cermat saat menggunakan alat ini.

  Jika eksfiltrasi data menjadi perhatian, pertimbangkan:

  * Menonaktifkan alat web fetch sepenuhnya
  * Menggunakan parameter `max_uses` untuk membatasi jumlah permintaan
  * Menggunakan parameter `allowed_domains` untuk membatasi ke domain yang diketahui aman
  * Menggunakan parameter `url_sources` untuk menghentikan hasil alat sisi klien agar tidak dihitung sebagai sumber (lihat [Sumber URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#url-sources))
</Warning>

Untuk dukungan model, lihat [Referensi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference).

## Cara kerja web fetch

Web fetch adalah [alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools): API mengambil konten selama permintaan dan menyisipkan hasilnya ke dalam percakapan. Anda tidak menjalankan apa pun atau mengembalikan `tool_result`. Pengecualiannya adalah ketika Claude memanggil web fetch dan salah satu alat klien Anda dalam grup panggilan alat paralel yang sama: API mengembalikan respons dengan `stop_reason: "tool_use"` sebelum fetch tersebut dijalankan, lalu menjalankan fetch saat Anda mengirim kembali blok `tool_result` klien. Lihat [Mencampur alat server dan alat klien dalam satu giliran](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools#mixing-server-tools-and-client-tools-in-one-turn).

Saat Anda menambahkan alat web fetch ke permintaan API Anda:

1. Claude menentukan kapan harus mengambil konten berdasarkan prompt dan URL yang tersedia.
2. API mengambil konten teks lengkap dari URL yang ditentukan.
3. Untuk PDF, API mengembalikan konten sebagai data yang dienkode base64 dan memprosesnya seperti dokumen PDF yang dilampirkan langsung.
4. Claude menganalisis konten yang diambil dan memberikan respons dengan sitasi opsional.

<Note>
  Alat web fetch saat ini tidak mendukung situs web yang dirender secara dinamis dengan JavaScript. Untuk halaman yang memerlukan browser sungguhan (rendering JavaScript, mengklik, atau mengisi formulir), pertimbangkan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool), alat klien tempat aplikasi Anda mengendalikan browser dan mengembalikan teks halaman atau tangkapan layar ke Claude sebagai hasil alat.
</Note>

### Kapan Claude melakukan fetch

Claude melakukan fetch ketika permintaan mengarah ke halaman atau dokumen tertentu:

* URL diberikan dalam percakapan (atau hasil alat sebelumnya)
* Pengguna menyebutkan sumber daya tertentu (artikel tertentu, README, halaman harga, atau bagian dokumentasi) tanpa URL, dan [alat web search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) juga diaktifkan sehingga Claude dapat menemukannya terlebih dahulu (lihat [Gabungan search dan fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#combined-search-and-fetch))

Claude **tidak** melakukan fetch untuk pertanyaan pengetahuan umum atau pertanyaan terbuka yang tidak merujuk ke halaman tertentu. “Ringkas artikel ini: `<url>`” memicu fetch. “Apa praktik terbaik untuk desain REST API?” dijawab secara langsung.

### Pemfilteran dinamis

Mengambil halaman web dan PDF lengkap dapat dengan cepat menghabiskan token, terutama ketika hanya informasi tertentu yang dibutuhkan dari dokumen besar. Dengan `web_fetch_20260209` atau yang lebih baru, Claude dapat menulis dan menjalankan kode untuk memfilter konten yang diambil sebelum memuatnya ke dalam konteks.

Pemfilteran dinamis ini sangat berguna untuk:

* Mengekstrak bagian tertentu dari dokumen panjang
* Memproses data terstruktur dari halaman web
* Memfilter informasi yang relevan dari PDF
* Mengurangi biaya token saat bekerja dengan dokumen besar

<Note>
  Pemfilteran dinamis berjalan di [alat code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool), yang diaktifkan secara otomatis oleh API untuk permintaan tersebut. Anda tidak perlu menambahkan alat code execution ke array `tools`.
</Note>

Untuk mengaktifkan pemfilteran dinamis, gunakan `web_fetch_20260209` atau versi yang lebih baru. Contoh berikut menggunakan `web_fetch_20260318`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
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
  model: claude-opus-5-5
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
      model="claude-opus-5-5",
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
    model: "claude-opus-5-5",
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
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Messages = [new UserMessageParam { Content = "Fetch the content at https://example.com/research-paper and extract the key findings." }],
      Tools = [new ToolUnion(new WebFetchTool20260318())]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
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
          .model(Model.CLAUDE_OPUS_5_5)
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
      model: 'claude-opus-5-5',
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
    model: "claude-opus-5-5",
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

<Note>
  Admin organisasi dapat menonaktifkan web fetch untuk organisasi Anda di halaman [**Capabilities**](https://platform.claude.com/settings/capabilities) di Claude Console. Dengan web fetch dinonaktifkan, permintaan Messages API yang menyertakan alat tersebut gagal dengan error 400 `invalid_request_error` yang menyatakan bahwa web fetch tidak diaktifkan. Dengan web fetch diaktifkan, admin juga dapat menetapkan domain yang diizinkan atau diblokir untuk web fetch di halaman yang sama. Untuk cara daftar tersebut diterapkan pada permintaan, lihat [Pemfilteran domain](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering).
</Note>

Untuk cara pengaturan web fetch organisasi Anda diterapkan dalam sesi Claude Managed Agents, lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions).

Sediakan alat web fetch dalam permintaan API Anda:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
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
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Please analyze the content at https://example.com/article"}' \
    --tool '{type: web_fetch_20250910, name: web_fetch, max_uses: 5}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
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
    model: "claude-opus-5-5",
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
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new UserMessageParam { Content = "Please analyze the content at https://example.com/article" }],
      Tools = [new ToolUnion(new WebFetchTool20250910() { MaxUses = 5 })]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
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
          .model(Model.CLAUDE_OPUS_5_5)
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
      model: 'claude-opus-5-5',
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
    model: "claude-opus-5-5",
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

  // Optional: Limit the number of fetches for each request
  "max_uses": 10,

  // Optional: Only fetch from these domains
  "allowed_domains": ["example.com", "docs.example.com"],

  // Optional: Never fetch from these domains (cannot be combined with allowed_domains)
  "blocked_domains": ["private.example.com"],

  // Optional: Don't fetch URLs that appear only in client-side tool results
  "url_sources": {
    "client_tool_results": { "type": "none" }
  },

  // Optional: Enable citations for fetched content
  "citations": {
    "enabled": true
  },

  // Optional: Maximum content length in tokens
  "max_content_tokens": 100000
}
```

Versi alat yang lebih baru menambahkan dua parameter opsional lagi: `use_cache` memerlukan `web_fetch_20260309` atau yang lebih baru (lihat [Cache bypass](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#cache-bypass)), dan `response_inclusion` memerlukan `web_fetch_20260318` atau yang lebih baru (lihat [Response inclusion](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#response-inclusion)).

### Max uses

Parameter `max_uses` membatasi jumlah web fetch yang dilakukan. Fetch yang gagal dihitung terhadap batas tersebut. Jika Claude mencoba melakukan fetch lebih banyak dari yang diizinkan, `web_fetch_tool_result` akan berupa error dengan kode error `max_uses_exceeded`. Saat ini tidak ada batas default.

### Pemfilteran domain

Untuk pemfilteran domain dengan `allowed_domains` dan `blocked_domains`, lihat [Alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering).

Di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tetapkan field ini pada entri `web_fetch` dari toolset agen; lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions).

### Batas konten

Parameter `max_content_tokens` membatasi jumlah konten yang disertakan dalam konteks. Jika konten yang diambil melebihi batas ini, alat akan memotongnya. Ini membantu mengontrol penggunaan token saat mengambil dokumen besar. Batas ini bersifat perkiraan: jumlah sebenarnya token input yang digunakan dapat sedikit bervariasi. Batas ini berlaku untuk konten teks, bukan untuk konten biner seperti PDF.

Jika PDF yang diambil akan membuat permintaan melebihi [batas halaman atau ukuran PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support#check-pdf-requirements), `web_fetch_tool_result` akan berupa error dengan kode error `content_too_large`. PDF dan gambar yang sudah ada dalam percakapan dihitung terhadap batas tersebut, sehingga menghapusnya dapat membuat fetch berhasil.

Di Claude Managed Agents, entri `web_fetch` dari toolset agen juga menerima `max_content_tokens`; lihat [pengaturan alat web](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#settings).

### Cache bypass

<Note>
  Memerlukan `web_fetch_20260309` atau yang lebih baru (termasuk `web_fetch_20260318`).
</Note>

Parameter `use_cache` mengontrol apakah konten yang di-cache boleh dikembalikan. Tetapkan `"use_cache": false` untuk melewati cache dan mengambil konten terbaru. Default-nya adalah `true`. Nonaktifkan caching hanya ketika pengguna secara eksplisit meminta konten terbaru atau saat mengambil sumber yang berubah dengan cepat, karena melewati cache meningkatkan “latency” (latensi).

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

### Response inclusion

<Note>
  Memerlukan `web_fetch_20260318` atau yang lebih baru.
</Note>

Parameter `response_inclusion` mengontrol bagaimana blok hasil fetch muncul dalam respons API ketika hasilnya dikonsumsi oleh panggilan [code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) yang telah selesai dalam giliran yang sama. Tetapkan `"response_inclusion": "excluded"` untuk menghapus pasangan blok `server_tool_use` dan blok hasil bersarang tersebut sepenuhnya dari respons, sehingga mengurangi biaya token output untuk alur kerja agentic yang tidak perlu mengembalikan konten halaman mentah ke klien. Default-nya adalah `"full"`. Hasil dari panggilan langsung, atau dari panggilan code execution yang dijeda sebelum selesai, selalu dikembalikan secara lengkap sehingga dapat dikirim kembali pada giliran berikutnya.

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

Berbeda dengan web search, di mana sitasi selalu diaktifkan, sitasi bersifat opsional untuk web fetch dan dinonaktifkan secara default. Tetapkan `"citations": {"enabled": true}` untuk memungkinkan Claude mengutip bagian tertentu dari dokumen yang diambil.

<Note>
  Saat menampilkan output API secara langsung kepada pengguna akhir, sertakan sitasi ke sumber aslinya. Jika Anda melakukan modifikasi pada output API, termasuk dengan memproses ulang atau menggabungkannya dengan materi Anda sendiri sebelum menampilkannya kepada pengguna akhir, tampilkan sitasi sebagaimana mestinya berdasarkan konsultasi dengan tim hukum Anda.
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
  Alat web fetch menyimpan hasil dalam cache untuk meningkatkan kinerja dan mengurangi permintaan yang berulang. Konten yang dikembalikan mungkin tidak selalu mencerminkan versi terbaru yang tersedia di URL tersebut. Perilaku cache dikelola secara otomatis dan dapat berubah seiring waktu untuk mengoptimalkan berbagai jenis konten dan pola penggunaan. Untuk mengambil konten terbaru, tetapkan `"use_cache": false` (lihat [Cache bypass](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#cache-bypass)).
</Note>

Untuk dokumen PDF, konten dikembalikan sebagai data yang dienkode base64:

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

Ketika alat web fetch mengalami error, Claude API mengembalikan respons 200 (sukses) dengan error yang direpresentasikan dalam body respons. Claude menerima hasil error tersebut dan melanjutkan giliran. Contohnya:

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

Berikut adalah kode error yang mungkin:

* `invalid_tool_input`: Input alat tidak valid, seperti URL yang formatnya salah atau skema non-HTTP(S)
* `url_too_long`: URL melebihi panjang maksimum (250 karakter)
* `url_not_allowed`: URL diblokir oleh aturan pemfilteran domain (termasuk pengaturan organisasi Anda) atau oleh pembatasan dari sisi Anthropic, seperti alamat privat, `robots.txt`, dan URL yang tampaknya berisi kredensial yang tidak Anda berikan
* `url_not_in_prior_context`: URL tidak muncul sebelumnya dalam percakapan, atau hanya muncul di sumber yang dikecualikan oleh `url_sources` (lihat [Validasi URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#url-validation))
* `url_not_accessible`: Gagal mengambil konten (error HTTP)
* `too_many_requests`: Batas laju terlampaui
* `unsupported_content_type`: Jenis konten tidak didukung (hanya teks, HTML, dan PDF)
* `content_too_large`: PDF yang diambil akan membuat permintaan melebihi batas halaman atau ukuran PDF (lihat [Batas konten](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#content-limits))
* `max_uses_exceeded`: Penggunaan maksimum alat web fetch terlampaui
* `unavailable`: Terjadi error internal

## Validasi URL

Untuk alasan keamanan, alat web fetch hanya dapat mengambil URL yang sebelumnya telah muncul dalam konteks percakapan. Ini mencakup:

* URL dalam pesan pengguna
* URL dalam hasil alat sisi klien
* URL dari hasil web search atau web fetch sebelumnya

Alat ini tidak dapat mengambil URL yang hanya muncul di output Claude sendiri atau hanya di prompt sistem. Agar URL dari prompt sistem dapat diambil, sertakan juga URL tersebut dalam pesan pengguna. Hasil dari alat sisi server lainnya, seperti [code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool), [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector), atau [tool search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool), juga bukan sumber yang diizinkan. Secara default, hasil alat sisi klien adalah sumber yang diizinkan bahkan ketika hasil tersebut mengulang teks yang dihasilkan Claude (misalnya, perintah yang mencetak inputnya, atau pesan error yang mengutipnya).

Alat ini juga menolak URL yang tampaknya berisi kredensial, seperti kunci API atau kata sandi, kecuali kredensial tersebut muncul di prompt sistem atau di teks pesan pengguna. Kredensial yang hanya muncul dalam hasil alat tidak dihitung. Hasilnya adalah error `url_not_allowed`. Untuk mengambil URL seperti itu, sertakan URL tersebut dalam pesan pengguna.

### Sumber URL

<Note>
  Berfungsi dengan `web_fetch_20250910`, `web_fetch_20260209`, `web_fetch_20260309`, dan `web_fetch_20260318`.
</Note>

Parameter opsional `url_sources` memungkinkan Anda menonaktifkan salah satu dari tiga sumber yang diizinkan, atau membatasi hasil alat ke alat tertentu. Parameter ini memiliki satu key untuk setiap sumber, dan setiap key memiliki default `{"type": "all"}`:

* `user_input`: URL dalam pesan pengguna. `type`-nya adalah `"all"` atau `"none"`.
* `client_tool_results`: URL dalam hasil alat sisi klien. `type`-nya adalah `"all"`, `"none"`, atau filter `"only"` atau `"except"` yang menyebutkan nama alat, seperti dalam contoh berikut.
* `server_tool_results`: URL dari hasil web search atau web fetch sebelumnya. Key ini menerima nilai yang sama, dan filternya menyebutkan `web_search` atau `web_fetch`.

Misalnya, alat yang menjalankan kode yang ditulis Claude mengembalikan apa pun yang dicetak oleh kode tersebut, termasuk URL apa pun yang dimasukkan Claude ke dalamnya. Untuk menghentikan hasil alat tersebut agar tidak dihitung sebagai sumber, sebutkan alat tersebut dalam filter `"except"`:

```json
{
  "tools": [
    {
      "type": "web_fetch_20260318",
      "name": "web_fetch",
      "url_sources": {
        "client_tool_results": {
          "type": "except",
          "tools": [{ "type": "tool_reference", "name": "run_code" }]
        }
      }
    },
    {
      "name": "run_code",
      "description": "Run Python code and return its output",
      "input_schema": {
        "type": "object",
        "properties": { "code": { "type": "string" } },
        "required": ["code"]
      }
    }
  ]
}
```

Filter mencantumkan alat sebagai objek `tool_reference`. Setiap nama harus cocok dengan alat dalam array `tools` pada permintaan: alat klien untuk `client_tool_results`, atau alat server untuk `server_tool_results`. Jika tidak, permintaan gagal dengan error. Di bawah `"except"`, alat yang Anda tambahkan ke `tools` kemudian dihitung sebagai sumber. Di bawah `"only"`, alat tersebut tidak dihitung.

Alat sisi klien selain `run_code` juga dapat mengembalikan teks yang ditulis Claude, misalnya dalam pesan error yang mengutipnya. Untuk mengecualikan semua hasil alat sisi klien, tetapkan `client_tool_results` ke `{"type": "none"}`.

Jika URL hanya muncul di sumber yang dikecualikan oleh `url_sources`, mengambilnya akan mengembalikan error `url_not_in_prior_context`.

## Gabungan search dan fetch

Ketika alat web search dan web fetch sama-sama diaktifkan, dan pengguna menyebutkan halaman atau dokumen tertentu tanpa memberikan URL (misalnya, “baca README dari repositori anthropics/anthropic-sdk-python”), Claude menggunakan web search untuk menemukannya, lalu mengambil hasilnya. Contoh berikut meminta pencarian dan analisis dalam satu permintaan:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
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
  model: claude-opus-5-5
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
      model="claude-opus-5-5",
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
    model: "claude-opus-5-5",
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
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Messages = [new UserMessageParam { Content = "Find recent articles about quantum computing and analyze the most relevant one in detail" }],
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
  	Model:     anthropic.ModelClaudeOpus5_5,
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
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(4096L)
          .addUserMessage("Find recent articles about quantum computing and analyze the most relevant one in detail")
          .addTool(WebSearchTool20250305.builder()
              .maxUses(3L)
              .build())
          .addTool(WebFetchTool20250910.builder()
              .maxUses(5L)
              .citations(CitationsConfigParam.builder()
                  .enabled(true)
                  .build())
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
      model: 'claude-opus-5-5',
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
    model: "claude-opus-5-5",
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

Untuk menyimpan definisi alat dalam cache di seluruh giliran, lihat [Penggunaan alat dengan caching prompt](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

## Streaming

Dengan streaming diaktifkan, event fetch merupakan bagian dari stream dengan jeda selama pengambilan konten:

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

// Pause while fetch runs

// Fetch results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "web_fetch_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"type": "web_fetch_result", "url": "https://example.com/article", "content": {"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "Article content..."}}}}}

// Claude's response continues...
```

## Permintaan batch

Anda dapat menyertakan alat web fetch dalam [Messages Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing). Panggilan alat web fetch melalui Messages Batches API dikenakan harga yang sama dengan panggilan dalam permintaan Messages API biasa.

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
    Jalankan kode Python dan Bash dalam container sandbox untuk menganalisis data, menghasilkan file, dan melakukan iterasi pada solusi.
  </Card>

  <Card href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools" title="Alat server" icon="cloud">
    Bekerja dengan alat yang dijalankan Anthropic: blok `server_tool_use`, kelanjutan `pause_turn`, dan pemfilteran domain.
  </Card>

  <Card href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat" icon="book">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>
</CardGroup>

## Ketersediaan

Alat web fetch tersedia di semua model dan layak untuk retensi data nol.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia
* Penggunaan: Tambahkan alat `web_fetch` ke `tools` permintaan. Pengaturan seperti `max_uses`, daftar domain, `citations`, dan `max_content_tokens` ditempatkan pada alat tersebut.

| Status               | Platform cloud                                                                                                                                                                                                                                                                                                                                                                                               |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tersedia             | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), [Microsoft Foundry (hosted on Anthropic)](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) |
| Tersedia<sup>1</sup> | [Microsoft Foundry (hosted on Azure)](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)                                                                                                                                                                                                                                                                                     |

1. Deployment yang di-host di Azure hanya mendukung `web_fetch_20250910`: tanpa pemfilteran dinamis, penyertaan respons, atau bypass cache.

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tersedia
* Penggunaan: Bagian dari toolset agen, dan aktif secara default setelah toolset ditambahkan. Daftar domain (tanpa path) dan `max_content_tokens` ditempatkan pada entri `web_fetch` di toolset; `max_uses`, `citations`, dan `cache_control` tidak tersedia.

| Status   | Platform cloud                                                                                                     |
| -------- | ------------------------------------------------------------------------------------------------------------------ |
| Tersedia | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                                                                                                                                     | HIPAA       |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------- |
| Status | Layak (tidak termasuk [Model yang dicakup](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements))                                                                                                                     | Tidak layak |
| Detail | Konten web yang diambil dikembalikan dalam respons API. Pemfilteran dinamis untuk web fetch tidak memenuhi syarat kelayakan ZDR atau HIPAA. Penerbit situs web mungkin menyimpan data permintaan (seperti URL yang diambil dan metadata permintaan) sesuai kebijakan mereka sendiri. | —           |

Endpoint yang berlaku:

* `/v1/messages` dengan alat `web_fetch`
