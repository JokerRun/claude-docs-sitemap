---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 381c30440a0280db8967aa4e640c51dc0ee51cbdfae58aa81c21bed182725c3e
---

# Pemanggilan alat terprogram

Biarkan Claude memanggil alat Anda dari kode di dalam container eksekusi kode, mengurangi perjalanan bolak-balik model dan penggunaan token dalam alur kerja multi-alat.

---

"Programmatic tool calling" (pemanggilan alat terprogram) memungkinkan Claude menulis kode yang memanggil alat Anda secara terprogram di dalam container [code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool), alih-alih memerlukan perjalanan bolak-balik melalui model untuk setiap pemanggilan alat. Ini mengurangi latensi untuk alur kerja multi-alat dan menurunkan konsumsi token dengan memungkinkan Claude memfilter atau memproses data sebelum mencapai jendela konteks model. Pada benchmark pencarian agentik seperti [BrowseComp](https://arxiv.org/abs/2504.12516) dan [DeepSearchQA](https://github.com/google-deepmind/deepsearchqa), yang menguji riset web multilangkah dan pengambilan informasi kompleks, menambahkan pemanggilan alat terprogram di atas alat pencarian dasar meningkatkan kinerja rata-rata 11% sambil menggunakan 24% lebih sedikit input token (lihat [Improved web search with dynamic filtering](https://claude.com/blog/improved-web-search-with-dynamic-filtering)).

Pertimbangkan pemeriksaan kepatuhan anggaran untuk 20 karyawan: pendekatan tradisional memerlukan 20 perjalanan bolak-balik model yang terpisah, menarik ribuan item baris pengeluaran ke dalam konteks di sepanjang jalan. Dengan pemanggilan alat terprogram, satu skrip menjalankan semua 20 pencarian, memfilter hasilnya, dan hanya mengembalikan karyawan yang melebihi batas mereka, memperkecil apa yang perlu dipertimbangkan Claude dari ratusan kilobyte menjadi hanya beberapa baris.

<Tip>
  Untuk melihat lebih dalam biaya inferensi dan konteks yang diatasi oleh pemanggilan alat terprogram, lihat [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use).
</Tip>

<Note>
  Fitur ini memerlukan alat code execution untuk diaktifkan.
</Note>

<Note>
  Untuk mengetahui bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

## Kompatibilitas model

Pemanggilan alat terprogram memerlukan `code_execution_20260120` atau yang lebih baru, yang didukung pada model-model berikut:

| Model                                          |
| ---------------------------------------------- |
| Claude Fable 5 (claude-fable-5)                |
| Claude Mythos 5 (claude-mythos-5)              |
| Claude Opus 4.8 (claude-opus-4-8)              |
| Claude Opus 4.7 (claude-opus-4-7)              |
| Claude Opus 4.6 (claude-opus-4-6)              |
| Claude Sonnet 5 (claude-sonnet-5)              |
| Claude Sonnet 4.6 (claude-sonnet-4-6)          |
| Claude Opus 4.5 (claude-opus-4-5-20251101)     |
| Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) |

Untuk matriks versi alat code execution lengkap, lihat [tabel kompatibilitas model alat code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility). Pemanggilan alat terprogram tersedia di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, pemanggilan alat terprogram memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure). Saat ini tidak tersedia di Amazon Bedrock atau Google Cloud.

## Mulai cepat

Berikut adalah contoh di mana Claude secara terprogram mengkueri database beberapa kali dan mengagregasi hasilnya:

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
                  "content": "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
              }
          ],
          "tools": [
              {
                  "type": "code_execution_20260120",
                  "name": "code_execution"
              },
              {
                  "name": "query_database",
                  "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "sql": {
                              "type": "string",
                              "description": "SQL query to execute"
                          }
                      },
                      "required": ["sql"]
                  },
                  "allowed_callers": ["code_execution_20260120"]
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
        Query sales data for the West, East, and Central regions, then
        tell me which region had the highest revenue
  tools:
    - type: code_execution_20260120
      name: code_execution
    - name: query_database
      description: >-
        Execute a SQL query against the sales database. Returns a list
        of rows as JSON objects.
      input_schema:
        type: object
        properties:
          sql:
            type: string
            description: SQL query to execute
        required:
          - sql
      allowed_callers:
        - code_execution_20260120
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
              "content": "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue",
          }
      ],
      tools=[
          {"type": "code_execution_20260120", "name": "code_execution"},
          {
              "name": "query_database",
              "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "sql": {"type": "string", "description": "SQL query to execute"}
                  },
                  "required": ["sql"],
              },
              "allowed_callers": ["code_execution_20260120"],
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
          "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
      }
    ],
    tools: [
      {
        type: "code_execution_20260120",
        name: "code_execution"
      },
      {
        name: "query_database",
        description:
          "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
        input_schema: {
          type: "object" as const,
          properties: {
            sql: {
              type: "string",
              description: "SQL query to execute"
            }
          },
          required: ["sql"]
        },
        allowed_callers: ["code_execution_20260120"]
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
      Messages = [
          new() {
              Role = Role.User,
              Content = "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
          }
      ],
      Tools = [
          new CodeExecutionTool20260120(),
          new ToolUnion(new Tool()
          {
              Name = "query_database",
              Description = "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["sql"] = JsonSerializer.SerializeToElement(new { type = "string", description = "SQL query to execute" }),
                  },
                  Required = ["sql"],
              },
              AllowedCallers = ["code_execution_20260120"]
          }),
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
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20260120: &anthropic.CodeExecutionTool20260120Param{}},
  		{OfTool: &anthropic.ToolParam{
  			Name:        "query_database",
  			Description: anthropic.String("Execute a SQL query against the sales database. Returns a list of rows as JSON objects."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"sql": map[string]any{
  						"type":        "string",
  						"description": "SQL query to execute",
  					},
  				},
  				Required: []string{"sql"},
  			},
  			AllowedCallers: []string{"code_execution_20260120"},
  		}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.CodeExecutionTool20260120;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(4096L)
          .addUserMessage("Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue")
          .addTool(CodeExecutionTool20260120.builder().build())
          .addTool(Tool.builder()
              .name("query_database")
              .description("Execute a SQL query against the sales database. Returns a list of rows as JSON objects.")
              .inputSchema(InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                      "sql", Map.of(
                          "type", "string",
                          "description", "SQL query to execute"
                      )
                  )))
                  .putAdditionalProperty("required", JsonValue.from(List.of("sql")))
                  .build())
              .allowedCallers(List.of(Tool.AllowedCaller.of("code_execution_20260120")))
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
          ['role' => 'user', 'content' => 'Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue'],
      ],
      model: 'claude-opus-4-8',
      tools: [
          [
              'type' => 'code_execution_20260120',
              'name' => 'code_execution',
          ],
          [
              'name' => 'query_database',
              'description' => 'Execute a SQL query against the sales database. Returns a list of rows as JSON objects.',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'sql' => [
                          'type' => 'string',
                          'description' => 'SQL query to execute',
                      ],
                  ],
                  'required' => ['sql'],
              ],
              'allowed_callers' => ['code_execution_20260120'],
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
      {
        role: "user",
        content: "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
      }
    ],
    tools: [
      {
        type: "code_execution_20260120",
        name: "code_execution"
      },
      {
        name: "query_database",
        description: "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
        input_schema: {
          type: "object",
          properties: {
            sql: {
              type: "string",
              description: "SQL query to execute"
            }
          },
          required: ["sql"]
        },
        allowed_callers: ["code_execution_20260120"]
      }
    ]
  )

  puts message
  ```
</CodeGroup>

Respons berhenti dengan `stop_reason: "tool_use"`, ID `container`, dan blok `tool_use` untuk `query_database` yang field `caller`-nya mengidentifikasi eksekusi kode yang memanggilnya. Kembalikan hasilnya seperti yang ditunjukkan di [Langkah 3 dari contoh alur kerja](#step-3-provide-tool-result) agar kode dapat selesai.

## Cara kerja pemanggilan alat terprogram

Ketika Anda mengonfigurasi alat agar dapat dipanggil dari code execution dan Claude memutuskan untuk menggunakan alat tersebut:

1. Claude menulis kode Python yang memanggil alat sebagai fungsi, berpotensi mencakup beberapa pemanggilan alat dan logika pra/pasca-pemrosesan
2. Claude menjalankan kode ini dalam container sandbox melalui code execution
3. Ketika fungsi alat dipanggil, code execution berhenti sejenak dan API mengembalikan blok `tool_use`
4. Anda memberikan hasil alat, dan code execution berlanjut (hasil antara tidak dimuat ke dalam jendela konteks Claude)
5. Setelah semua code execution selesai, Claude menerima output akhir dan melanjutkan mengerjakan tugas

Pendekatan ini sangat berguna untuk:

* **Pemrosesan data besar:** Memfilter atau mengagregasi hasil alat sebelum mencapai konteks Claude
* **Alur kerja multilangkah:** Menghemat token dan latensi dengan memanggil alat secara serial atau dalam loop tanpa melakukan sampling Claude di antara pemanggilan alat
* **Logika kondisional:** Membuat keputusan berdasarkan hasil alat antara

<Note>
  Alat yang mengizinkan pemanggil code execution diekspos ke kode Claude sebagai fungsi Python async, sehingga Claude dapat menjalankannya secara paralel dengan `asyncio.gather`. Setiap fungsi menerima satu dict argumen dan mengembalikan string: teks dari `tool_result` yang Anda kirim kembali. Kode Claude menunggu fungsi-fungsi ini dengan `await` tingkat atas dan mem-parsing hasil yang dibutuhkannya sebagai data terstruktur, misalnya `rows = json.loads(await query_database({"sql": "<sql>"}))`.
</Note>

## Konsep inti

### Field `allowed_callers`

Field `allowed_callers` menentukan konteks mana yang dapat memanggil sebuah alat:

```json
{
  "name": "query_database",
  "description": "Execute a SQL query against the database",
  "input_schema": {
    // ...
  },
  "allowed_callers": ["code_execution_20260120"]
}
```

**Nilai yang mungkin:**

* `["direct"]` - Claude diarahkan untuk memanggil alat ini secara langsung (default jika dihilangkan)
* `["code_execution_20260120"]` - Claude diarahkan untuk memanggil alat ini hanya dari dalam code execution
* `["direct", "code_execution_20260120"]` - Claude dapat memanggil alat ini secara langsung atau dari dalam code execution

Baik `"code_execution_20260120"` maupun `"code_execution_20260521"` diterima dalam `allowed_callers` dan dapat dipertukarkan: permintaan yang menggunakan salah satu versi alat code-execution memenuhi alat yang mencantumkan salah satu pemanggil. Blok respons selalu menandai pemanggil sebagai `code_execution_20260120` terlepas dari versi mana yang dideklarasikan permintaan.

<Tip>
  Pilih salah satu antara `["direct"]` atau `["code_execution_20260120"]` untuk setiap alat daripada mengaktifkan keduanya, karena ini memberikan panduan yang lebih jelas kepada Claude tentang cara terbaik menggunakan alat tersebut.
</Tip>

<Note>
  `allowed_callers` mengontrol bagaimana alat disajikan kepada Claude dan divalidasi terhadap `tool_choice`, tetapi ini bukan pemblokiran keras di tingkat API terhadap pemanggilan langsung. Claude sangat diarahkan untuk menghormatinya, tetapi klien Anda tetap harus siap menangani `tool_use` langsung untuk alat apa pun yang didefinisikannya. Jangan mengandalkan `allowed_callers` sebagai batas keamanan.
</Note>

### Field `caller` dalam respons

Setiap blok tool use menyertakan field `caller` yang menunjukkan bagaimana alat tersebut dipanggil:

**Pemanggilan langsung (penggunaan alat tradisional):**

```json
{
  "type": "tool_use",
  "id": "toolu_abc123",
  "name": "query_database",
  "input": { "sql": "<sql>" },
  "caller": { "type": "direct" }
}
```

**Pemanggilan terprogram:**

```json
{
  "type": "tool_use",
  "id": "toolu_xyz789",
  "name": "query_database",
  "input": { "sql": "<sql>" },
  "caller": {
    "type": "code_execution_20260120",
    "tool_id": "srvtoolu_abc123"
  }
}
```

`tool_id` adalah `id` dari blok `server_tool_use` code execution yang melakukan pemanggilan, sehingga Anda dapat mencocokkan setiap `tool_use` terprogram dengan eksekusi kode yang menghasilkannya.

### Siklus hidup container

Pemanggilan alat terprogram menggunakan container yang sama dengan code execution:

* **Pembuatan container:** Container baru dibuat untuk setiap permintaan kecuali Anda menggunakan kembali yang sudah ada
* **ID container:** Dikembalikan dalam respons di field `container`, bersama dengan timestamp `expires_at`
* **Penggunaan kembali:** Kirimkan kembali ID container pada permintaan berikutnya untuk mempertahankan state. Saat pemanggilan alat terprogram sedang menunggu hasil Anda, ID container wajib ada pada permintaan tersebut, bukan opsional: API menolak permintaan tanpanya.
* **Kedaluwarsa:** `expires_at` memberi tahu Anda berapa lama waktu yang tersisa untuk container. Container yang idle saat ini diklaim kembali setelah sekitar 5 menit, dan tidak ada container yang dapat digunakan kembali lebih dari 30 hari setelah dibuat.

<Warning>
  Saat kode Claude menunggu hasil alat terprogram, pemanggilan yang tertunda akan habis waktunya setelah sekitar 4 menit dan memunculkan `TimeoutError` di dalam kode. Kembalikan setiap hasil alat jauh sebelum timestamp `expires_at` pada respons yang dijeda. Lihat [Kedaluwarsa container selama pemanggilan alat](#container-expiration-during-tool-call).
</Warning>

## Contoh alur kerja

Berikut adalah cara kerja alur pemanggilan alat terprogram yang lengkap:

### Langkah 1: Permintaan awal

Kirim permintaan dengan code execution dan alat yang mengizinkan pemanggilan terprogram. Untuk mengaktifkan pemanggilan terprogram, tambahkan field `allowed_callers` ke definisi alat Anda.

<Note>
  Berikan deskripsi terperinci tentang format output alat Anda dalam deskripsi alat. Jika Anda menentukan bahwa alat mengembalikan JSON, Claude akan mencoba melakukan deserialisasi dan memproses hasilnya dalam kode. Semakin banyak detail yang Anda berikan tentang skema output, semakin baik Claude dapat menangani respons secara terprogram.
</Note>

Bentuk permintaannya identik dengan contoh [Mulai cepat](#quick-start): sertakan `code_execution` dalam daftar tools Anda, tambahkan `allowed_callers: ["code_execution_20260120"]` ke alat apa pun yang Anda ingin Claude panggil dari kode, dan kirim pesan pengguna Anda. Langkah-langkah selanjutnya dalam alur kerja ini menggunakan pesan pengguna `"Query customer purchase history from the last quarter and identify our top 5 customers by revenue"`.

### Langkah 2: Respons API dengan pemanggilan alat

Claude menulis kode yang memanggil alat Anda. API berhenti sejenak dan mengembalikan:

```json Output
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll query the purchase history and analyze the results."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_abc123",
      "name": "code_execution",
      "input": {
        "code": "import json\n\nrows = json.loads(await query_database({'sql': '<sql>'}))\ntop_customers = sorted(rows, key=lambda x: x['revenue'], reverse=True)[:5]\nprint(f'Top 5 customers: {top_customers}')"
      }
    },
    {
      "type": "tool_use",
      "id": "toolu_def456",
      "name": "query_database",
      "input": { "sql": "<sql>" },
      "caller": {
        "type": "code_execution_20260120",
        "tool_id": "srvtoolu_abc123"
      }
    }
  ],
  "container": {
    "id": "container_xyz789",
    "expires_at": "2026-01-20T14:30:00Z"
  },
  "stop_reason": "tool_use"
}
```

### Langkah 3: Berikan hasil alat

Kirim riwayat percakapan lengkap ditambah hasil alat Anda. Tiga detail penting pada permintaan ini:

* Pesan pengguna yang membawa hasil Anda hanya boleh berisi blok `tool_result`. Lihat [Pembatasan pemformatan pesan](#message-formatting-restrictions).
* Kirimkan ID `container` dari respons yang dijeda. API menolak kelanjutan yang memiliki pemanggilan alat terprogram yang tertunda tetapi tidak memiliki ID container.
* Kirim array `tools` yang sama dengan permintaan asli. Alat code execution harus tetap ada agar kode yang dijeda dapat dilanjutkan, dan alat yang Anda kirim pada permintaan ini adalah definisi yang dapat digunakan Claude dan kode yang sedang berjalan untuk sisa giliran tersebut.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 4096,
          "container": "container_xyz789",
          "messages": [
              {
                  "role": "user",
                  "content": "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
              },
              {
                  "role": "assistant",
                  "content": [
                      {
                          "type": "text",
                          "text": "I'\''ll query the purchase history and analyze the results."
                      },
                      {
                          "type": "server_tool_use",
                          "id": "srvtoolu_abc123",
                          "name": "code_execution",
                          "input": {"code": "..."}
                      },
                      {
                          "type": "tool_use",
                          "id": "toolu_def456",
                          "name": "query_database",
                          "input": {"sql": "<sql>"},
                          "caller": {
                              "type": "code_execution_20260120",
                              "tool_id": "srvtoolu_abc123"
                          }
                      }
                  ]
              },
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "tool_result",
                          "tool_use_id": "toolu_def456",
                          "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000}, {\"customer_id\": \"C2\", \"revenue\": 38000}]"
                      }
                  ]
              }
          ],
          "tools": [
              {
                  "type": "code_execution_20260120",
                  "name": "code_execution"
              },
              {
                  "name": "query_database",
                  "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "sql": {
                              "type": "string",
                              "description": "SQL query to execute"
                          }
                      },
                      "required": ["sql"]
                  },
                  "allowed_callers": ["code_execution_20260120"]
              }
          ]
      }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  container: container_xyz789
  messages:
    - role: user
      content: >-
        Query customer purchase history from the last quarter and identify our
        top 5 customers by revenue
    - role: assistant
      content:
        - type: text
          text: I'll query the purchase history and analyze the results.
        - type: server_tool_use
          id: srvtoolu_abc123
          name: code_execution
          input:
            code: "..."
        - type: tool_use
          id: toolu_def456
          name: query_database
          input:
            sql: "<sql>"
          caller:
            type: code_execution_20260120
            tool_id: srvtoolu_abc123
    - role: user
      content:
        - type: tool_result
          tool_use_id: toolu_def456
          content: >-
            [{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2",
            "revenue": 38000}, ...]
  # Array tools yang sama dengan permintaan asli
  tools:
    - type: code_execution_20260120
      name: code_execution
    - name: query_database
      description: >-
        Execute a SQL query against the sales database. Returns a list
        of rows as JSON objects.
      input_schema:
        type: object
        properties:
          sql:
            type: string
            description: SQL query to execute
        required:
          - sql
      allowed_callers:
        - code_execution_20260120
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      container="container_xyz789",  # Reuse the container
      messages=[
          {
              "role": "user",
              "content": "Query customer purchase history from the last quarter and identify our top 5 customers by revenue",
          },
          {
              "role": "assistant",
              "content": [
                  {
                      "type": "text",
                      "text": "I'll query the purchase history and analyze the results.",
                  },
                  {
                      "type": "server_tool_use",
                      "id": "srvtoolu_abc123",
                      "name": "code_execution",
                      "input": {"code": "..."},
                  },
                  {
                      "type": "tool_use",
                      "id": "toolu_def456",
                      "name": "query_database",
                      "input": {"sql": "<sql>"},
                      "caller": {
                          "type": "code_execution_20260120",
                          "tool_id": "srvtoolu_abc123",
                      },
                  },
              ],
          },
          {
              "role": "user",
              "content": [
                  {
                      "type": "tool_result",
                      "tool_use_id": "toolu_def456",
                      "content": '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]',
                  }
              ],
          },
      ],
      # Array tools yang sama dengan permintaan asli
      tools=[
          {"type": "code_execution_20260120", "name": "code_execution"},
          {
              "name": "query_database",
              "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "sql": {"type": "string", "description": "SQL query to execute"}
                  },
                  "required": ["sql"],
              },
              "allowed_callers": ["code_execution_20260120"],
          },
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    container: "container_xyz789", // Reuse the container
    messages: [
      {
        role: "user",
        content:
          "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
      },
      {
        role: "assistant",
        content: [
          { type: "text", text: "I'll query the purchase history and analyze the results." },
          {
            type: "server_tool_use",
            id: "srvtoolu_abc123",
            name: "code_execution",
            input: { code: "..." }
          },
          {
            type: "tool_use",
            id: "toolu_def456",
            name: "query_database",
            input: { sql: "<sql>" },
            caller: {
              type: "code_execution_20260120",
              tool_id: "srvtoolu_abc123"
            }
          }
        ]
      },
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: "toolu_def456",
            content:
              '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]'
          }
        ]
      }
    ],
    // Array tools yang sama dengan permintaan asli
    tools: [
      {
        type: "code_execution_20260120",
        name: "code_execution"
      },
      {
        name: "query_database",
        description:
          "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
        input_schema: {
          type: "object" as const,
          properties: {
            sql: {
              type: "string",
              description: "SQL query to execute"
            }
          },
          required: ["sql"]
        },
        allowed_callers: ["code_execution_20260120"]
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
      Container = "container_xyz789",
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
          },
          new()
          {
              Role = Role.Assistant,
              Content = new ContentBlock[]
              {
                  new TextBlock { Text = "I'll query the purchase history and analyze the results." },
                  new ServerToolUseBlock
                  {
                      Id = "srvtoolu_abc123",
                      Name = "code_execution",
                      Input = new { code = "..." }
                  },
                  new ToolUseBlock
                  {
                      Id = "toolu_def456",
                      Name = "query_database",
                      Input = new { sql = "<sql>" },
                      Caller = new ToolCaller
                      {
                          Type = "code_execution_20260120",
                          ToolId = "srvtoolu_abc123"
                      }
                  }
              }
          },
          new()
          {
              Role = Role.User,
              Content = new ContentBlockParam[]
              {
                  new ToolResultBlockParam
                  {
                      ToolUseID = "toolu_def456",
                      Content = "[{\"customer_id\": \"C1\", \"revenue\": 45000}, {\"customer_id\": \"C2\", \"revenue\": 38000}, ...]"
                  }
              }
          }
      ],
      // Array tools yang sama dengan permintaan asli
      Tools = [
          new CodeExecutionTool20260120(),
          new ToolUnion(new Tool()
          {
              Name = "query_database",
              Description = "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["sql"] = JsonSerializer.SerializeToElement(new { type = "string", description = "SQL query to execute" }),
                  },
                  Required = ["sql"],
              },
              AllowedCallers = ["code_execution_20260120"]
          }),
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
  	Container: anthropic.MessageNewParamsContainerUnion{
  		OfString: anthropic.String("container_xyz789"),
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Query customer purchase history from the last quarter and identify our top 5 customers by revenue")),
  		{
  			Role: anthropic.MessageParamRoleAssistant,
  			Content: []anthropic.ContentBlockParamUnion{
  				anthropic.NewTextBlock("I'll query the purchase history and analyze the results."),
  				{OfServerToolUse: &anthropic.ServerToolUseBlockParam{
  					ID:    "srvtoolu_abc123",
  					Name:  anthropic.ServerToolUseBlockParamNameCodeExecution,
  					Input: map[string]any{"code": "..."},
  				}},
  				{OfToolUse: &anthropic.ToolUseBlockParam{
  					ID:    "toolu_def456",
  					Name:  "query_database",
  					Input: map[string]any{"sql": "<sql>"},
  					Caller: anthropic.ServerToolUseBlockParamCallerUnion{
  						OfCodeExecution20260120: &anthropic.ServerToolCaller20260120Param{
  							ToolID: "srvtoolu_abc123",
  						},
  					},
  				}},
  			},
  		},
  		{
  			Role: anthropic.MessageParamRoleUser,
  			Content: []anthropic.ContentBlockParamUnion{
  				{OfToolResult: &anthropic.ToolResultBlockParam{
  					ToolUseID: "toolu_def456",
  					Content: []anthropic.ToolResultBlockParamContentUnion{
  						{OfText: &anthropic.TextBlockParam{
  							Text: `[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]`,
  						}},
  					},
  				}},
  			},
  		},
  	},
  	// Array tools yang sama dengan permintaan asli
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20260120: &anthropic.CodeExecutionTool20260120Param{}},
  		{OfTool: &anthropic.ToolParam{
  			Name:        "query_database",
  			Description: anthropic.String("Execute a SQL query against the sales database. Returns a list of rows as JSON objects."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"sql": map[string]any{
  						"type":        "string",
  						"description": "SQL query to execute",
  					},
  				},
  				Required: []string{"sql"},
  			},
  			AllowedCallers: []string{"code_execution_20260120"},
  		}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.CodeExecutionTool20260120;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(4096L)
          .container("container_xyz789")
          .addUserMessage("Query customer purchase history from the last quarter and identify our top 5 customers by revenue")
          .addAssistantMessageOfBlockParams(List.of(
              ContentBlockParam.ofText(
                  TextBlockParam.builder()
                      .text("I'll query the purchase history and analyze the results.")
                      .build()),
              ContentBlockParam.ofServerToolUse(
                  ServerToolUseBlockParam.builder()
                      .id("srvtoolu_abc123")
                      .name("code_execution")
                      .input(JsonValue.from(Map.of("code", "...")))
                      .build()),
              ContentBlockParam.ofToolUse(
                  ToolUseBlockParam.builder()
                      .id("toolu_def456")
                      .name("query_database")
                      .input(JsonValue.from(Map.of("sql", "<sql>")))
                      .codeExecution20260120Caller("srvtoolu_abc123")
                      .build())
          ))
          .addUserMessageOfBlockParams(List.of(
              ContentBlockParam.ofToolResult(
                  ToolResultBlockParam.builder()
                      .toolUseId("toolu_def456")
                      .content("[{\"customer_id\": \"C1\", \"revenue\": 45000}, {\"customer_id\": \"C2\", \"revenue\": 38000}, ...]")
                      .build())
          ))
          // Array tools yang sama dengan permintaan asli
          .addTool(CodeExecutionTool20260120.builder().build())
          .addTool(Tool.builder()
              .name("query_database")
              .description("Execute a SQL query against the sales database. Returns a list of rows as JSON objects.")
              .inputSchema(InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                      "sql", Map.of(
                          "type", "string",
                          "description", "SQL query to execute"
                      )
                  )))
                  .putAdditionalProperty("required", JsonValue.from(List.of("sql")))
                  .build())
              .allowedCallers(List.of(Tool.AllowedCaller.of("code_execution_20260120")))
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
          [
              'role' => 'user',
              'content' => 'Query customer purchase history from the last quarter and identify our top 5 customers by revenue',
          ],
          [
              'role' => 'assistant',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => "I'll query the purchase history and analyze the results.",
                  ],
                  [
                      'type' => 'server_tool_use',
                      'id' => 'srvtoolu_abc123',
                      'name' => 'code_execution',
                      'input' => ['code' => '...'],
                  ],
                  [
                      'type' => 'tool_use',
                      'id' => 'toolu_def456',
                      'name' => 'query_database',
                      'input' => ['sql' => '<sql>'],
                      'caller' => [
                          'type' => 'code_execution_20260120',
                          'tool_id' => 'srvtoolu_abc123',
                      ],
                  ],
              ],
          ],
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'tool_result',
                      'tool_use_id' => 'toolu_def456',
                      'content' => '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
      container: 'container_xyz789',
      // Array tools yang sama dengan permintaan asli
      tools: [
          [
              'type' => 'code_execution_20260120',
              'name' => 'code_execution',
          ],
          [
              'name' => 'query_database',
              'description' => 'Execute a SQL query against the sales database. Returns a list of rows as JSON objects.',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'sql' => [
                          'type' => 'string',
                          'description' => 'SQL query to execute',
                      ],
                  ],
                  'required' => ['sql'],
              ],
              'allowed_callers' => ['code_execution_20260120'],
          ],
      ],
  );

  echo $message;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    container: "container_xyz789",
    messages: [
      {
        role: "user",
        content: "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
      },
      {
        role: "assistant",
        content: [
          {
            type: "text",
            text: "I'll query the purchase history and analyze the results."
          },
          {
            type: "server_tool_use",
            id: "srvtoolu_abc123",
            name: "code_execution",
            input: { code: "..." }
          },
          {
            type: "tool_use",
            id: "toolu_def456",
            name: "query_database",
            input: { sql: "<sql>" },
            caller: {
              type: "code_execution_20260120",
              tool_id: "srvtoolu_abc123"
            }
          }
        ]
      },
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: "toolu_def456",
            content: '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]'
          }
        ]
      }
    ],
    # Array tools yang sama dengan permintaan asli
    tools: [
      {
        type: "code_execution_20260120",
        name: "code_execution"
      },
      {
        name: "query_database",
        description: "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
        input_schema: {
          type: "object",
          properties: {
            sql: {
              type: "string",
              description: "SQL query to execute"
            }
          },
          required: ["sql"]
        },
        allowed_callers: ["code_execution_20260120"]
      }
    ]
  )

  puts message
  ```
</CodeGroup>

### Langkah 4: Pemanggilan alat berikutnya atau penyelesaian

Kode melanjutkan dari tempat ia dijeda dan memproses hasil Anda. Setiap respons kelanjutan akan berhenti sejenak lagi dengan lebih banyak blok `tool_use` terprogram, atau menyelesaikan code execution dan membiarkan Claude melanjutkan giliran (Langkah 5). Periksa `stop_reason` dan `caller` dari setiap blok `tool_use` untuk membedakan keduanya: respons yang berhenti sejenak untuk Anda memiliki `stop_reason: "tool_use"` dan blok `tool_use` yang `caller`-nya menyebutkan versi code execution, dan Anda mengulangi Langkah 3 dengan `tool_result` untuk setiap pemanggilan terprogram yang tertunda dalam satu pesan pengguna.

### Langkah 5: Respons akhir

Setelah code execution selesai, Claude memberikan respons akhir:

```json Output
{
  "content": [
    {
      "type": "code_execution_tool_result",
      "tool_use_id": "srvtoolu_abc123",
      "content": {
        "type": "code_execution_result",
        "stdout": "Top 5 customers: [{'customer_id': 'C1', 'revenue': 45000}, {'customer_id': 'C2', 'revenue': 38000}, {'customer_id': 'C5', 'revenue': 32000}, {'customer_id': 'C8', 'revenue': 28500}, {'customer_id': 'C3', 'revenue': 24000}]",
        "stderr": "",
        "return_code": 0,
        "content": []
      }
    },
    {
      "type": "text",
      "text": "I've analyzed the purchase history from last quarter. Your top 5 customers generated $167,500 in total revenue, with Customer C1 leading at $45,000."
    }
  ],
  "stop_reason": "end_turn"
}
```

## Pola lanjutan

### Pemrosesan batch dengan loop

Claude dapat menulis kode yang memproses beberapa item secara efisien:

```python
regions = ["West", "East", "Central", "North", "South"]
results = {}
for region in regions:
    rows = json.loads(await query_database({"sql": f"<sql for {region}>"}))
    results[region] = sum(row["revenue"] for row in rows)

# Memproses hasil secara terprogram
top_region = max(results.items(), key=lambda x: x[1])
print(f"Top region: {top_region[0]} with ${top_region[1]:,} in revenue")
```

Pola ini:

* Mengurangi perjalanan bolak-balik model dari N (satu per wilayah) menjadi 1
* Memproses kumpulan hasil besar secara terprogram sebelum kembali ke Claude
* Menghemat token dengan hanya mengembalikan kesimpulan teragregasi alih-alih data mentah

### Penghentian dini

Claude dapat berhenti memproses segera setelah kriteria keberhasilan terpenuhi:

```python
endpoints = ["us-east", "eu-west", "apac"]
for endpoint in endpoints:
    status = await check_health({"endpoint": endpoint})
    if status == "healthy":
        print(f"Found healthy endpoint: {endpoint}")
        break  # Stop early, don't check remaining
```

### Pemilihan alat kondisional

```python
path = "/tmp/example.txt"
file_info = json.loads(await get_file_info({"path": path}))
if file_info["size"] < 10000:
    content = await read_full_file({"path": path})
else:
    content = await read_file_summary({"path": path})
print(content)
```

### Pemfilteran data

```python
server_id = "srv-01"
log_text = await fetch_logs({"server_id": server_id})
errors = [line for line in log_text.splitlines() if "ERROR" in line]
print(f"Found {len(errors)} errors")
for error in errors[-10:]:  # Only return last 10 errors
    print(error)
```

## Format respons

### Pemanggilan alat terprogram

Ketika code execution memanggil sebuah alat:

```json
{
  "type": "tool_use",
  "id": "toolu_abc123",
  "name": "query_database",
  "input": { "sql": "<sql>" },
  "caller": {
    "type": "code_execution_20260120",
    "tool_id": "srvtoolu_xyz789"
  }
}
```

### Penanganan hasil alat

Hasil alat Anda diteruskan kembali ke kode yang sedang berjalan:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_abc123",
      "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000, \"orders\": 23}, {\"customer_id\": \"C2\", \"revenue\": 38000, \"orders\": 18}, ...]"
    }
  ]
}
```

### Penyelesaian code execution

Ketika semua pemanggilan alat terpenuhi dan kode selesai:

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_xyz789",
  "content": {
    "type": "code_execution_result",
    "stdout": "Analysis complete. Top 5 customers identified from 847 total records.",
    "stderr": "",
    "return_code": 0,
    "content": []
  }
}
```

## Penanganan error

### Error umum

| Error                                        | Di mana muncul                                                          | Deskripsi                                                                              | Solusi                                                                                                                                |
| -------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `invalid_tool_input`                         | `error_code` pada blok error `code_execution_tool_result` dalam respons | Parameter yang tidak valid diteruskan ke alat code execution                           | Lihat [error alat code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool#errors)                                      |
| `invalid_request_error` (pada `tool_choice`) | Respons error HTTP 400                                                  | `tool_choice` menyebutkan alat yang `allowed_callers`-nya tidak menyertakan `"direct"` | Tambahkan `"direct"` ke `allowed_callers` alat tersebut, atau hapus alat dari `tool_choice` dan biarkan Claude memanggilnya dari kode |

### Kedaluwarsa container selama pemanggilan alat

Jika hasil alat Anda tidak tiba dalam waktu sekitar 4 menit, pemanggilan yang tertunda memunculkan `TimeoutError` di dalam kode Claude yang sedang berjalan. Claude melihat error tersebut di `stderr` dan biasanya mencoba ulang pemanggilan:

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_abc123",
  "content": {
    "type": "code_execution_result",
    "stdout": "",
    "stderr": "TimeoutError: Calling tool ['query_database'] timed out (no response after 270s).",
    "return_code": 0,
    "content": []
  }
}
```

Untuk mencegah timeout:

* Pantau field `expires_at` dalam respons
* Implementasikan timeout untuk eksekusi alat Anda
* Pertimbangkan untuk memecah operasi panjang menjadi bagian-bagian yang lebih kecil

### Error eksekusi alat

Jika alat Anda mengembalikan error:

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_abc123",
  "content": "Error: Query timeout - table lock exceeded 30 seconds"
}
```

Kode Claude menerima error ini dan dapat menanganinya dengan tepat.

## Batasan dan keterbatasan

### Ketidakcocokan fitur

* **Structured outputs:** Alat dengan `strict: true` tidak didukung dengan pemanggilan terprogram
* **Tool choice:** Anda tidak dapat memaksa pemanggilan terprogram dari alat tertentu melalui `tool_choice`
* **Parallel tool use:** `disable_parallel_tool_use: true` tidak didukung dengan pemanggilan terprogram

### Keterbatasan skema input

Alat kustom yang `input_schema`-nya berisi `$ref` rekursif (siklus referensi, seperti skema yang merujuk pada dirinya sendiri) tidak dapat diaktifkan untuk pemanggilan terprogram. Menyertakan versi alat code execution dalam `allowed_callers` untuk alat semacam itu menyebabkan permintaan gagal dengan `400 invalid_request_error` yang pesannya berisi `Circular $ref detected`. Skema yang sama diterima untuk pemanggilan alat langsung.

Untuk mengatasi hal ini, lakukan salah satu dari berikut:

* Pertahankan alat hanya-langsung dengan menghilangkan `allowed_callers` (atau mengaturnya ke `["direct"]`). Alat lain dalam permintaan yang sama masih dapat menggunakan pemanggilan terprogram.
* Hapus siklus dari skema. Misalnya, uraikan rekursi ke kedalaman tetap dan jelaskan penyarangan yang lebih dalam di `description` pada tingkat terdalam, atau ganti properti rekursif dengan `{"type": "object"}` biasa yang `description`-nya menjelaskan bentuk yang diharapkan.

### Pembatasan alat

Alat-alat berikut tidak dapat dipanggil secara terprogram:

* Alat yang disediakan oleh [MCP connector](/docs/id/agents-and-tools/mcp-connector)

### Pembatasan pemformatan pesan

Saat merespons pemanggilan alat terprogram, ada persyaratan pemformatan yang ketat:

**Respons hanya hasil alat:** Jika ada pemanggilan alat terprogram yang tertunda menunggu hasil, pesan respons Anda harus berisi **hanya** blok `tool_result`. Anda tidak dapat menyertakan konten teks apa pun, bahkan setelah hasil alat.

Tidak valid - Tidak dapat menyertakan teks saat merespons pemanggilan alat terprogram:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01",
      "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000}]"
    },
    { "type": "text", "text": "What should I do next?" }
  ]
}
```

Valid - Hanya hasil alat saat merespons pemanggilan alat terprogram:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01",
      "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000}]"
    }
  ]
}
```

Pembatasan ini hanya berlaku saat merespons pemanggilan alat terprogram (code execution). Untuk pemanggilan alat sisi klien biasa, Anda dapat menyertakan konten teks setelah hasil alat.

**Konten hasil alat hanya teks:** `content` dari setiap `tool_result` yang menjawab pemanggilan terprogram harus berupa string atau blok `text`. Tipe blok konten gambar, dokumen, dan lainnya ditolak.

### Batas laju

Pemanggilan alat terprogram tunduk pada batas laju yang sama dengan pemanggilan alat biasa. Setiap pemanggilan alat dari code execution dihitung sebagai pemanggilan terpisah.

### Validasi hasil alat sebelum digunakan

Saat mengimplementasikan alat yang didefinisikan pengguna yang akan dipanggil secara terprogram:

* **Hasil alat dikembalikan sebagai string:** Hasil tersebut dapat berisi konten apa pun, termasuk cuplikan kode atau perintah yang dapat dieksekusi yang mungkin diproses oleh lingkungan eksekusi.
* **Validasi hasil alat eksternal:** Jika alat Anda mengembalikan data dari sumber eksternal atau menerima input pengguna, waspadai risiko injeksi kode jika output akan diinterpretasikan atau dieksekusi sebagai kode.

## Efisiensi token

Pemanggilan alat terprogram mengurangi konsumsi token dengan tiga cara:

* **Hasil alat dari pemanggilan terprogram tidak ditambahkan ke konteks Claude** - hanya output kode akhir yang ditambahkan
* **Pemrosesan antara terjadi dalam kode** - pemfilteran, agregasi, dan transformasi lainnya tidak mengonsumsi token model
* **Beberapa pemanggilan alat dalam satu code execution** - mengurangi overhead dibandingkan dengan giliran model terpisah

Misalnya, memanggil 10 alat secara langsung menggunakan \~10x token dibandingkan memanggilnya secara terprogram dan mengembalikan ringkasan.

Dalam evaluasi internal Anthropic pada model Claude produksi:

* Pada benchmark agen manajemen proyek dengan 75 alat, mengaktifkan pemanggilan alat terprogram mengurangi input token yang ditagih sekitar 38% tanpa perubahan akurasi tugas.
* Pada [τ²-bench](https://arxiv.org/abs/2506.07982) (domain maskapai, ritel, dan telekomunikasi), di mana setiap giliran melakukan satu atau dua pemanggilan alat berurutan, pemanggilan alat terprogram tidak mengubah skor dan biayanya sekitar 8% lebih mahal. Alur kerja pemanggilan tunggal berurutan tidak mendapat manfaat.
* Di seluruh lalu lintas API produksi, permintaan yang array `tools`-nya berisi 10 hingga 49 definisi alat melihat penghematan token tipikal 20% hingga 40% dengan pemanggilan alat terprogram diaktifkan.

Penghematan aktual bervariasi tergantung bentuk beban kerja. Lihat [Kapan menggunakan pemanggilan terprogram](#when-to-use-programmatic-calling).

## Penggunaan dan harga

Pemanggilan alat terprogram menggunakan harga yang sama dengan code execution. Lihat [harga code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk detailnya.

<Note>
  Penghitungan token untuk pemanggilan alat terprogram: Hasil alat dari pemanggilan terprogram tidak dihitung dalam penggunaan input/output token Anda. Hanya hasil code execution akhir dan respons Claude yang dihitung.
</Note>

## Praktik terbaik

### Desain alat

* **Berikan deskripsi output yang terperinci:** Karena Claude melakukan deserialisasi hasil alat dalam kode, dokumentasikan formatnya (struktur JSON dan tipe field)
* **Kembalikan data terstruktur:** JSON atau format lain yang dapat dibaca mesin paling cocok untuk pemrosesan terprogram
* **Jaga respons tetap ringkas:** Kembalikan hanya data yang diperlukan untuk meminimalkan overhead pemrosesan

### Kapan menggunakan pemanggilan terprogram

Pemanggilan alat terprogram menukar overhead tetap yang kecil (startup container, pembuatan skrip) dengan penghematan besar pada token hasil alat dan perjalanan bolak-balik model. Apakah pertukaran itu menguntungkan tergantung pada bentuk beban kerja.

**Sangat cocok:**

* Operasi fan-out atau paralel di banyak item (misalnya, memeriksa 50 endpoint atau mencari 20 catatan)
* Hasil alat besar yang dapat difilter, diagregasi, atau diringkas sebelum mencapai konteks Claude
* Pencarian dan pengambilan agentik, di mana kueri iteratif dan pemfilteran hasil mendominasi alur kerja

**Kurang cocok:**

* Alur kerja yang sangat berurutan di mana setiap pemanggilan bergantung pada penalaran Claude atas hasil sebelumnya, karena skrip tidak dapat melewati perjalanan bolak-balik model dalam kasus tersebut
* Sejumlah kecil pemanggilan alat dengan respons kecil, terutama pada giliran pertama percakapan, di mana overhead container dan skrip dapat melebihi penghematan
* Alat yang memerlukan umpan balik pengguna langsung di antara pemanggilan

Jika Anda tidak yakin, ukur input token yang ditagih dengan dan tanpa `allowed_callers` pada sampel representatif dari lalu lintas Anda sebelum mengaktifkannya secara luas.

### Optimasi kinerja

* **Gunakan kembali container** saat membuat beberapa permintaan terkait untuk mempertahankan state
* **Kelompokkan operasi serupa** dalam satu code execution jika memungkinkan

## Pemecahan masalah

### Masalah umum

**`invalid_request_error` saat mengatur `tool_choice`**

* `tool_choice` tidak dapat menyebutkan alat yang `allowed_callers`-nya menghilangkan `"direct"`. Tambahkan `"direct"` ke `allowed_callers` alat tersebut, atau hapus alat dari `tool_choice` dan biarkan Claude memanggilnya dari kode.

**Kedaluwarsa container**

* Respons setiap pemanggilan alat terprogram jauh sebelum timestamp `expires_at` dari respons yang dijeda. Kode Claude berhenti menunggu hasil setelah sekitar 4 menit, dan container yang idle saat ini diklaim kembali setelah sekitar 5 menit.
* Pertimbangkan untuk mengimplementasikan eksekusi alat yang lebih cepat

**Hasil alat tidak di-parse dengan benar**

* Pastikan alat Anda mengembalikan data string yang dapat dideserialisasi oleh Claude
* Berikan dokumentasi format output yang jelas dalam deskripsi alat Anda

### Tips debugging

1. **Catat semua pemanggilan alat dan hasilnya** untuk melacak alur
2. **Periksa field `caller`** untuk mengonfirmasi pemanggilan terprogram
3. **Pantau ID container** untuk memastikan penggunaan kembali yang tepat
4. **Uji alat secara independen** sebelum mengaktifkan pemanggilan terprogram

## Mengapa pemanggilan alat terprogram berhasil

Claude dilatih pada sejumlah besar kode, sehingga menyajikan alat sebagai fungsi Python yang dapat dipanggil memungkinkannya menggunakan kekuatan tersebut:

* **Komposisi alat:** Pemanggilan berantai, loop, dan kondisional adalah alur kontrol Python biasa alih-alih serangkaian perjalanan bolak-balik model
* **Pemrosesan hasil:** Kode Claude memfilter dan mengagregasi output alat yang besar, atau menulisnya ke file, dan hanya output akhir yang masuk ke jendela konteks
* **Latensi:** Model tidak di-sampling ulang di antara pemanggilan alat dalam satu code execution

## Implementasi alternatif

Pemanggilan alat terprogram adalah pola yang dapat digeneralisasi yang juga dapat diimplementasikan pada infrastruktur Anda sendiri. Berikut perbandingan pendekatannya:

### Eksekusi langsung sisi klien

Berikan Claude alat code execution dan jelaskan fungsi apa yang tersedia di lingkungan tersebut. Ketika Claude memanggil alat dengan kode, aplikasi Anda mengeksekusinya secara lokal di mana fungsi-fungsi tersebut didefinisikan.

**Keuntungan:**

* Perubahan arsitektur minimal pada aplikasi Anda
* Kontrol penuh atas lingkungan dan instruksi

**Kerugian:**

* Mengeksekusi kode yang tidak tepercaya di luar sandbox
* Pemanggilan alat dapat menjadi vektor untuk injeksi kode

**Gunakan ketika:** Aplikasi Anda dapat mengeksekusi kode arbitrer dengan aman, Anda menginginkan implementasi terkecil, dan penawaran terkelola Anthropic tidak sesuai dengan kebutuhan Anda.

### Eksekusi sandbox yang dikelola sendiri

Pendekatan yang sama dari perspektif Claude, tetapi kode berjalan dalam container sandbox dengan pembatasan keamanan (misalnya, tanpa egress jaringan). Jika alat Anda memerlukan sumber daya eksternal, Anda memerlukan protokol untuk mengeksekusi pemanggilan alat di luar sandbox.

**Keuntungan:**

* Pemanggilan alat terprogram yang aman pada infrastruktur Anda sendiri
* Kontrol penuh atas lingkungan eksekusi

**Kerugian:**

* Kompleks untuk dibangun dan dipelihara
* Memerlukan pengelolaan infrastruktur dan komunikasi antar-proses

**Gunakan ketika:** Keamanan sangat penting dan solusi terkelola Anthropic tidak sesuai dengan persyaratan Anda.

### Eksekusi yang dikelola Anthropic

Pemanggilan alat terprogram Anthropic adalah versi terkelola dari eksekusi sandbox dengan lingkungan Python yang telah disesuaikan untuk Claude. Anthropic menangani pengelolaan container, code execution, dan komunikasi pemanggilan alat yang aman.

**Keuntungan:**

* Aman dan terlindungi secara default
* Diaktifkan dengan definisi alat, tanpa infrastruktur yang perlu dijalankan
* Lingkungan dan instruksi dioptimalkan untuk Claude

Pertimbangkan untuk menggunakan solusi terkelola Anthropic jika Anda menggunakan Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), atau [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, pemanggilan alat terprogram memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure).

## Retensi data

Pemanggilan alat terprogram dibangun di atas infrastruktur code execution dan menggunakan container sandbox yang sama. Data container, termasuk artefak eksekusi dan output, disimpan hingga 30 hari.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Streaming alat berbutir halus" icon="bolt" href="/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming">
    Streaming input alat tanpa buffering JSON sisi server untuk aplikasi yang sensitif terhadap latensi.
  </Card>

  <Card title="Alat code execution" icon="code" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Jalankan kode Python dan bash dalam container sandbox untuk menganalisis data, menghasilkan file, dan mengiterasi solusi.
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="wrench" href="/docs/id/agents-and-tools/tool-use/overview">
    Hubungkan Claude ke alat dan API eksternal. Lihat di mana alat dieksekusi, kapan Claude memanggilnya, dan alat mana yang cocok untuk tugas Anda.
  </Card>

  <Card title="Definisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tentukan skema alat, tulis deskripsi yang efektif, dan kontrol kapan Claude memanggil alat Anda.
  </Card>
</CardGroup>
