---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling
fetched_at: 2026-07-03T03:11:00.926352Z
sha256: ba7bf49179240b918fb9a3dd6ef47b5b0297e4c88a247d0d308e41f55977b1b3
---

# Pemanggilan alat secara terprogram

Biarkan Claude memanggil alat Anda dari kode di dalam kontainer eksekusi kode, mengurangi bolak-balik model dan penggunaan token dalam alur kerja multi-alat.

---

Pemanggilan alat secara terprogram memungkinkan Claude menulis kode yang memanggil alat Anda secara terprogram di dalam kontainer [code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool) (eksekusi kode), alih-alih memerlukan bolak-balik melalui model untuk setiap pemanggilan alat. Hal ini mengurangi latensi untuk alur kerja multi-alat dan menurunkan konsumsi token dengan memungkinkan Claude memfilter atau memproses data sebelum data tersebut mencapai jendela konteks model. Pada benchmark pencarian agentik seperti [BrowseComp](https://arxiv.org/abs/2504.12516) dan [DeepSearchQA](https://github.com/google-deepmind/deepsearchqa), yang menguji riset web multi-langkah dan pengambilan informasi kompleks, menambahkan pemanggilan alat secara terprogram di atas alat pencarian dasar meningkatkan performa rata-rata sebesar 11% sambil menggunakan 24% lebih sedikit token input (lihat [Improved web search with dynamic filtering](https://claude.com/blog/improved-web-search-with-dynamic-filtering)).

Pertimbangkan pemeriksaan kepatuhan anggaran untuk 20 karyawan: pendekatan tradisional memerlukan 20 bolak-balik model terpisah, menarik ribuan baris item pengeluaran ke dalam konteks sepanjang prosesnya. Dengan pemanggilan alat secara terprogram, satu skrip menjalankan seluruh 20 pencarian, memfilter hasilnya, dan hanya mengembalikan karyawan yang melebihi batas mereka, menyusutkan apa yang perlu dipikirkan Claude dari ratusan kilobyte menjadi hanya beberapa baris.

<Tip>
  Untuk pembahasan lebih mendalam tentang biaya inferensi dan konteks yang diatasi oleh pemanggilan alat secara terprogram, lihat [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use).
</Tip>

<Note>
  Fitur ini memerlukan alat eksekusi kode untuk diaktifkan.
</Note>

<Note>
  Fitur ini **tidak** memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Data disimpan sesuai dengan kebijakan retensi standar fitur ini.
</Note>

## Kompatibilitas model

Pemanggilan alat secara terprogram memerlukan `code_execution_20260120` atau yang lebih baru, yang didukung pada model-model berikut:

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

Untuk matriks versi alat eksekusi kode lengkap, lihat [tabel kompatibilitas model alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility). Pemanggilan alat secara terprogram tersedia di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, pemanggilan alat secara terprogram memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure). Fitur ini saat ini tidak tersedia di Amazon Bedrock atau Google Cloud.

## Mulai cepat

Berikut adalah contoh di mana Claude secara terprogram melakukan kueri ke database beberapa kali dan mengagregasi hasilnya:

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

Respons berhenti dengan `stop_reason: "tool_use"`, sebuah ID `container`, dan blok `tool_use` untuk `query_database` yang field `caller`-nya mengidentifikasi eksekusi kode yang memanggilnya. Kembalikan hasilnya seperti yang ditunjukkan di [Langkah 3 dari contoh alur kerja](#step-3-provide-tool-result) agar kode dapat selesai.

## Cara kerja pemanggilan alat secara terprogram

Ketika Anda mengonfigurasi sebuah alat agar dapat dipanggil dari eksekusi kode dan Claude memutuskan untuk menggunakan alat tersebut:

1. Claude menulis kode Python yang memanggil alat tersebut sebagai fungsi, yang mungkin mencakup beberapa pemanggilan alat dan logika pra/pasca-pemrosesan
2. Claude menjalankan kode ini di kontainer sandbox melalui eksekusi kode
3. Ketika fungsi alat dipanggil, eksekusi kode dijeda dan API mengembalikan blok `tool_use`
4. Anda memberikan hasil alat, dan eksekusi kode dilanjutkan (hasil antara tidak dimuat ke dalam jendela konteks Claude)
5. Setelah semua eksekusi kode selesai, Claude menerima output akhir dan melanjutkan pengerjaan tugas

Pendekatan ini sangat berguna untuk:

* **Pemrosesan data besar:** Memfilter atau mengagregasi hasil alat sebelum mencapai konteks Claude
* **Alur kerja multi-langkah:** Menghemat token dan latensi dengan memanggil alat secara serial atau dalam loop tanpa melakukan sampling Claude di antara pemanggilan alat
* **Logika kondisional:** Membuat keputusan berdasarkan hasil alat antara

<Note>
  Alat yang mengizinkan pemanggil eksekusi kode diekspos ke kode Claude sebagai fungsi Python async, sehingga Claude dapat menjalankannya secara paralel dengan `asyncio.gather`. Setiap fungsi menerima satu dict argumen dan mengembalikan string: teks dari `tool_result` yang Anda kirim kembali. Kode Claude menunggu fungsi-fungsi ini dengan `await` tingkat atas dan mem-parsing hasil yang dibutuhkannya sebagai data terstruktur, misalnya `rows = json.loads(await query_database({"sql": "<sql>"}))`.
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
* `["code_execution_20260120"]` - Claude diarahkan untuk memanggil alat ini hanya dari dalam eksekusi kode
* `["direct", "code_execution_20260120"]` - Claude dapat memanggil alat ini secara langsung atau dari dalam eksekusi kode

Baik `"code_execution_20260120"` maupun `"code_execution_20260521"` diterima dalam `allowed_callers` dan dapat dipertukarkan: permintaan yang menggunakan salah satu versi alat eksekusi kode memenuhi alat yang mencantumkan salah satu pemanggil tersebut. Blok respons selalu menandai pemanggil sebagai `code_execution_20260120` terlepas dari versi mana yang dideklarasikan oleh permintaan.

<Tip>
  Pilih salah satu antara `["direct"]` atau `["code_execution_20260120"]` untuk setiap alat daripada mengaktifkan keduanya, karena ini memberikan panduan yang lebih jelas kepada Claude tentang cara terbaik menggunakan alat tersebut.
</Tip>

<Note>
  `allowed_callers` mengontrol bagaimana alat disajikan kepada Claude dan divalidasi terhadap `tool_choice`, tetapi ini bukan pemblokiran keras tingkat API terhadap pemanggilan langsung. Claude diarahkan dengan kuat untuk menghormatinya, tetapi klien Anda tetap harus siap menangani `tool_use` langsung untuk alat apa pun yang didefinisikannya. Jangan mengandalkan `allowed_callers` sebagai batas keamanan.
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

`tool_id` adalah `id` dari blok `server_tool_use` eksekusi kode yang melakukan pemanggilan, sehingga Anda dapat mencocokkan setiap `tool_use` terprogram dengan eksekusi kode yang menghasilkannya.

### Siklus hidup kontainer

Pemanggilan alat secara terprogram menggunakan kontainer yang sama dengan eksekusi kode:

* **Pembuatan kontainer:** Kontainer baru dibuat untuk setiap permintaan kecuali Anda menggunakan kembali yang sudah ada
* **ID kontainer:** Dikembalikan dalam respons di field `container`, bersama dengan timestamp `expires_at`
* **Penggunaan kembali:** Kirim kembali ID kontainer pada permintaan berikutnya untuk mempertahankan state. Saat pemanggilan alat terprogram sedang menunggu hasil Anda, ID kontainer wajib ada pada permintaan tersebut, bukan opsional: API menolak permintaan tanpanya.
* **Kedaluwarsa:** `expires_at` memberi tahu Anda berapa lama waktu yang tersisa untuk kontainer. Kontainer yang idle saat ini diklaim kembali setelah sekitar 5 menit, dan tidak ada kontainer yang dapat digunakan kembali lebih dari 30 hari setelah dibuat.

<Warning>
  Saat kode Claude sedang menunggu hasil alat terprogram, pemanggilan yang tertunda akan timeout setelah sekitar 4 menit dan memunculkan `TimeoutError` di dalam kode. Kembalikan setiap hasil alat jauh sebelum timestamp `expires_at` pada respons yang dijeda. Lihat [Kedaluwarsa kontainer selama pemanggilan alat](#container-expiration-during-tool-call).
</Warning>

## Contoh alur kerja

Berikut adalah cara kerja alur pemanggilan alat secara terprogram yang lengkap:

### Langkah 1: Permintaan awal

Kirim permintaan dengan eksekusi kode dan alat yang mengizinkan pemanggilan terprogram. Untuk mengaktifkan pemanggilan terprogram, tambahkan field `allowed_callers` ke definisi alat Anda.

<Note>
  Berikan deskripsi terperinci tentang format output alat Anda dalam deskripsi alat. Jika Anda menentukan bahwa alat mengembalikan JSON, Claude akan mencoba melakukan deserialisasi dan memproses hasilnya dalam kode. Semakin detail yang Anda berikan tentang skema output, semakin baik Claude dapat menangani respons secara terprogram.
</Note>

Bentuk permintaan identik dengan contoh [Mulai cepat](#quick-start): sertakan `code_execution` dalam daftar alat Anda, tambahkan `allowed_callers: ["code_execution_20260120"]` ke alat apa pun yang Anda ingin Claude panggil dari kode, dan kirim pesan pengguna Anda. Langkah-langkah selanjutnya dalam alur kerja ini menggunakan pesan pengguna `"Query customer purchase history from the last quarter and identify our top 5 customers by revenue"`.

### Langkah 2: Respons API dengan pemanggilan alat

Claude menulis kode yang memanggil alat Anda. API dijeda dan mengembalikan:

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

Kirim seluruh riwayat percakapan ditambah hasil alat Anda. Tiga detail penting pada permintaan ini:

* Pesan pengguna yang membawa hasil Anda hanya boleh berisi blok `tool_result`. Lihat [Batasan pemformatan pesan](#message-formatting-restrictions).
* Kirim ID `container` dari respons yang dijeda. API menolak kelanjutan yang memiliki pemanggilan alat terprogram yang tertunda tetapi tanpa ID kontainer.
* Kirim array `tools` yang sama seperti permintaan asli. Alat eksekusi kode harus tetap ada agar kode yang dijeda dapat dilanjutkan, dan alat yang Anda kirim pada permintaan ini adalah definisi yang dapat digunakan Claude dan kode yang sedang berjalan untuk sisa giliran tersebut.

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
  # Array tools yang sama seperti permintaan awal
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
      # Array tools yang sama seperti permintaan awal
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
    // Array tools yang sama seperti permintaan awal
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
      // Array tools yang sama seperti permintaan awal
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
  	// Array tools yang sama seperti permintaan awal
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
          // Array tools yang sama seperti permintaan awal
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
      // Array tools yang sama seperti permintaan awal
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
    # Array tools yang sama seperti permintaan awal
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

Kode melanjutkan dari tempat ia dijeda dan memproses hasil Anda. Setiap respons kelanjutan akan dijeda lagi dengan lebih banyak blok `tool_use` terprogram, atau menyelesaikan eksekusi kode dan membiarkan Claude melanjutkan giliran (Langkah 5). Periksa `stop_reason` dan `caller` dari setiap blok `tool_use` untuk membedakan keduanya: respons yang dijeda untuk Anda memiliki `stop_reason: "tool_use"` dan blok `tool_use` yang `caller`-nya menyebutkan versi eksekusi kode, dan Anda mengulangi Langkah 3 dengan `tool_result` untuk setiap pemanggilan terprogram yang tertunda dalam satu pesan pengguna.

### Langkah 5: Respons akhir

Setelah eksekusi kode selesai, Claude memberikan respons akhir:

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

Claude dapat menulis kode yang memproses banyak item secara efisien:

```python
regions = ["West", "East", "Central", "North", "South"]
results = {}
for region in regions:
    rows = json.loads(await query_database({"sql": f"<sql for {region}>"}))
    results[region] = sum(row["revenue"] for row in rows)

# Proses hasil secara terprogram
top_region = max(results.items(), key=lambda x: x[1])
print(f"Top region: {top_region[0]} with ${top_region[1]:,} in revenue")
```

Pola ini:

* Mengurangi bolak-balik model dari N (satu per wilayah) menjadi 1
* Memproses kumpulan hasil yang besar secara terprogram sebelum dikembalikan ke Claude
* Menghemat token dengan hanya mengembalikan kesimpulan yang telah diagregasi alih-alih data mentah

### Terminasi dini

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

Ketika eksekusi kode memanggil sebuah alat:

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

### Penyelesaian eksekusi kode

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

| Error                                        | Tempat muncul                                                           | Deskripsi                                                                              | Solusi                                                                                                                                |
| -------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `invalid_tool_input`                         | `error_code` pada blok error `code_execution_tool_result` dalam respons | Parameter yang tidak valid diteruskan ke alat eksekusi kode                            | Lihat [error alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#errors)                                       |
| `invalid_request_error` (pada `tool_choice`) | Respons error HTTP 400                                                  | `tool_choice` menyebutkan alat yang `allowed_callers`-nya tidak menyertakan `"direct"` | Tambahkan `"direct"` ke `allowed_callers` alat tersebut, atau hapus alat dari `tool_choice` dan biarkan Claude memanggilnya dari kode |

### Kedaluwarsa kontainer selama pemanggilan alat

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
* Terapkan timeout untuk eksekusi alat Anda
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

### Inkompatibilitas fitur

* **Structured outputs:** Alat dengan `strict: true` tidak didukung dengan pemanggilan terprogram
* **Tool choice:** Anda tidak dapat memaksa pemanggilan terprogram dari alat tertentu melalui `tool_choice`
* **Parallel tool use:** `disable_parallel_tool_use: true` tidak didukung dengan pemanggilan terprogram

### Keterbatasan skema input

Alat kustom yang `input_schema`-nya berisi `$ref` rekursif (siklus referensi, seperti skema yang merujuk ke dirinya sendiri) tidak dapat diaktifkan untuk pemanggilan terprogram. Menyertakan versi alat eksekusi kode dalam `allowed_callers` untuk alat semacam itu menyebabkan permintaan gagal dengan `400 invalid_request_error` yang pesannya berisi `Circular $ref detected`. Skema yang sama diterima untuk pemanggilan alat langsung.

Untuk mengatasi hal ini, lakukan salah satu dari berikut:

* Pertahankan alat sebagai direct-only dengan menghilangkan `allowed_callers` (atau mengaturnya ke `["direct"]`). Alat lain dalam permintaan yang sama tetap dapat menggunakan pemanggilan terprogram.
* Hapus siklus dari skema. Misalnya, buka gulungan rekursi hingga kedalaman tetap dan jelaskan nesting yang lebih dalam di `description` dari level terdalam, atau ganti properti rekursif dengan `{"type": "object"}` biasa yang `description`-nya menjelaskan bentuk yang diharapkan.

### Batasan alat

Alat berikut tidak dapat dipanggil secara terprogram:

* Alat yang disediakan oleh [MCP connector](/docs/id/agents-and-tools/mcp-connector)

### Batasan pemformatan pesan

Saat merespons pemanggilan alat terprogram, ada persyaratan pemformatan yang ketat:

**Respons hanya berisi hasil alat:** Jika ada pemanggilan alat terprogram yang tertunda menunggu hasil, pesan respons Anda harus berisi **hanya** blok `tool_result`. Anda tidak dapat menyertakan konten teks apa pun, bahkan setelah hasil alat.

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

Batasan ini hanya berlaku saat merespons pemanggilan alat terprogram (eksekusi kode). Untuk pemanggilan alat sisi klien biasa, Anda dapat menyertakan konten teks setelah hasil alat.

**Konten hasil alat hanya teks:** `content` dari setiap `tool_result` yang menjawab pemanggilan terprogram harus berupa string atau blok `text`. Tipe blok konten gambar, dokumen, dan lainnya ditolak.

### Batas laju

Pemanggilan alat terprogram tunduk pada batas laju yang sama dengan pemanggilan alat biasa. Setiap pemanggilan alat dari eksekusi kode dihitung sebagai pemanggilan terpisah.

### Validasi hasil alat sebelum digunakan

Saat mengimplementasikan alat yang didefinisikan pengguna yang akan dipanggil secara terprogram:

* **Hasil alat dikembalikan sebagai string:** Hasil tersebut dapat berisi konten apa pun, termasuk cuplikan kode atau perintah yang dapat dieksekusi yang mungkin diproses oleh lingkungan eksekusi.
* **Validasi hasil alat eksternal:** Jika alat Anda mengembalikan data dari sumber eksternal atau menerima input pengguna, waspadai risiko injeksi kode jika output akan diinterpretasikan atau dieksekusi sebagai kode.

## Efisiensi token

Pemanggilan alat secara terprogram mengurangi konsumsi token dalam tiga cara:

* **Hasil alat dari pemanggilan terprogram tidak ditambahkan ke konteks Claude** - hanya output kode akhir yang ditambahkan
* **Pemrosesan antara terjadi dalam kode** - pemfilteran, agregasi, dan transformasi lainnya tidak mengonsumsi token model
* **Beberapa pemanggilan alat dalam satu eksekusi kode** - mengurangi overhead dibandingkan dengan giliran model terpisah

Misalnya, memanggil 10 alat secara langsung menggunakan \~10x token dibandingkan memanggilnya secara terprogram dan mengembalikan ringkasan.

Dalam evaluasi internal Anthropic pada model Claude produksi:

* Pada benchmark agen manajemen proyek dengan 75 alat, mengaktifkan pemanggilan alat secara terprogram mengurangi token input yang ditagih sekitar 38% tanpa perubahan pada akurasi tugas.
* Pada [τ²-bench](https://arxiv.org/abs/2506.07982) (domain maskapai penerbangan, ritel, dan telekomunikasi), di mana setiap giliran membuat satu atau dua pemanggilan alat berurutan, pemanggilan alat secara terprogram tidak mengubah skor dan biayanya sekitar 8% lebih tinggi. Alur kerja pemanggilan tunggal berurutan tidak mendapat manfaat.
* Di seluruh lalu lintas API produksi, permintaan yang array `tools`-nya berisi 10 hingga 49 definisi alat mengalami penghematan token tipikal sebesar 20% hingga 40% dengan pemanggilan alat secara terprogram diaktifkan.

Penghematan aktual bervariasi tergantung bentuk beban kerja. Lihat [Kapan menggunakan pemanggilan terprogram](#when-to-use-programmatic-calling).

## Penggunaan dan harga

Pemanggilan alat secara terprogram menggunakan harga yang sama dengan eksekusi kode. Lihat [harga eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk detailnya.

<Note>
  Penghitungan token untuk pemanggilan alat terprogram: Hasil alat dari pemanggilan terprogram tidak dihitung terhadap penggunaan token input/output Anda. Hanya hasil eksekusi kode akhir dan respons Claude yang dihitung.
</Note>

## Praktik terbaik

### Desain alat

* **Berikan deskripsi output yang terperinci:** Karena Claude melakukan deserialisasi hasil alat dalam kode, dokumentasikan formatnya (struktur JSON dan tipe field)
* **Kembalikan data terstruktur:** JSON atau format lain yang dapat dibaca mesin bekerja paling baik untuk pemrosesan terprogram
* **Jaga respons tetap ringkas:** Kembalikan hanya data yang diperlukan untuk meminimalkan overhead pemrosesan

### Kapan menggunakan pemanggilan terprogram

Pemanggilan alat secara terprogram menukar overhead tetap yang kecil (startup kontainer, pembuatan skrip) dengan penghematan besar pada token hasil alat dan bolak-balik model. Apakah pertukaran itu menguntungkan tergantung pada bentuk beban kerja.

**Sangat cocok:**

* Operasi fan-out atau paralel di banyak item (misalnya, memeriksa 50 endpoint atau mencari 20 record)
* Hasil alat besar yang dapat difilter, diagregasi, atau diringkas sebelum mencapai konteks Claude
* Pencarian dan pengambilan agentik, di mana kueri iteratif dan pemfilteran hasil mendominasi alur kerja

**Kurang cocok:**

* Alur kerja yang sangat berurutan di mana setiap pemanggilan bergantung pada penalaran Claude atas hasil sebelumnya, karena skrip tidak dapat melewati bolak-balik model dalam kasus tersebut
* Sejumlah kecil pemanggilan alat dengan respons kecil, terutama pada giliran pertama percakapan, di mana overhead kontainer dan skrip dapat melebihi penghematan
* Alat yang memerlukan umpan balik pengguna segera di antara pemanggilan

Jika Anda tidak yakin, ukur token input yang ditagih dengan dan tanpa `allowed_callers` pada sampel representatif dari lalu lintas Anda sebelum mengaktifkannya secara luas.

### Optimasi performa

* **Gunakan kembali kontainer** saat membuat beberapa permintaan terkait untuk mempertahankan state
* **Kelompokkan operasi serupa** dalam satu eksekusi kode jika memungkinkan

## Pemecahan masalah

### Masalah umum

**`invalid_request_error` saat mengatur `tool_choice`**

* `tool_choice` tidak dapat menyebutkan alat yang `allowed_callers`-nya tidak menyertakan `"direct"`. Tambahkan `"direct"` ke `allowed_callers` alat tersebut, atau hapus alat dari `tool_choice` dan biarkan Claude memanggilnya dari kode.

**Kedaluwarsa kontainer**

* Respons setiap pemanggilan alat terprogram jauh sebelum timestamp `expires_at` dari respons yang dijeda. Kode Claude berhenti menunggu hasil setelah sekitar 4 menit, dan kontainer yang idle saat ini diklaim kembali setelah sekitar 5 menit.
* Pertimbangkan untuk mengimplementasikan eksekusi alat yang lebih cepat

**Hasil alat tidak di-parse dengan benar**

* Pastikan alat Anda mengembalikan data string yang dapat di-deserialisasi oleh Claude
* Berikan dokumentasi format output yang jelas dalam deskripsi alat Anda

### Tips debugging

1. **Catat semua pemanggilan alat dan hasilnya** untuk melacak alurnya
2. **Periksa field `caller`** untuk mengonfirmasi pemanggilan terprogram
3. **Pantau ID kontainer** untuk memastikan penggunaan kembali yang tepat
4. **Uji alat secara independen** sebelum mengaktifkan pemanggilan terprogram

## Mengapa pemanggilan alat secara terprogram berhasil

Claude dilatih pada sejumlah besar kode, sehingga menyajikan alat sebagai fungsi Python yang dapat dipanggil memungkinkannya menggunakan kekuatan tersebut:

* **Komposisi alat:** Pemanggilan berantai, loop, dan kondisional adalah alur kontrol Python biasa alih-alih serangkaian bolak-balik model
* **Pemrosesan hasil:** Kode Claude memfilter dan mengagregasi output alat yang besar, atau menulisnya ke file, dan hanya output akhir yang masuk ke jendela konteks
* **Latensi:** Model tidak di-sampling ulang di antara pemanggilan alat dalam satu eksekusi kode

## Implementasi alternatif

Pemanggilan alat secara terprogram adalah pola yang dapat digeneralisasi yang juga dapat diimplementasikan pada infrastruktur Anda sendiri. Berikut perbandingan pendekatannya:

### Eksekusi langsung sisi klien

Berikan Claude alat eksekusi kode dan jelaskan fungsi apa yang tersedia di lingkungan tersebut. Ketika Claude memanggil alat dengan kode, aplikasi Anda mengeksekusinya secara lokal di tempat fungsi-fungsi tersebut didefinisikan.

**Keuntungan:**

* Minimal perombakan arsitektur aplikasi Anda
* Kontrol penuh atas lingkungan dan instruksi

**Kerugian:**

* Mengeksekusi kode yang tidak tepercaya di luar sandbox
* Pemanggilan alat dapat menjadi vektor untuk injeksi kode

**Gunakan ketika:** Aplikasi Anda dapat mengeksekusi kode arbitrer dengan aman, Anda menginginkan implementasi terkecil, dan penawaran terkelola Anthropic tidak sesuai dengan kebutuhan Anda.

### Eksekusi sandbox yang dikelola sendiri

Pendekatan yang sama dari perspektif Claude, tetapi kode berjalan di kontainer sandbox dengan batasan keamanan (misalnya, tanpa egress jaringan). Jika alat Anda memerlukan sumber daya eksternal, Anda memerlukan protokol untuk mengeksekusi pemanggilan alat di luar sandbox.

**Keuntungan:**

* Pemanggilan alat terprogram yang aman pada infrastruktur Anda sendiri
* Kontrol penuh atas lingkungan eksekusi

**Kerugian:**

* Kompleks untuk dibangun dan dipelihara
* Memerlukan pengelolaan infrastruktur dan komunikasi antar-proses

**Gunakan ketika:** Keamanan sangat penting dan solusi terkelola Anthropic tidak sesuai dengan kebutuhan Anda.

### Eksekusi yang dikelola Anthropic

Pemanggilan alat secara terprogram dari Anthropic adalah versi terkelola dari eksekusi sandbox dengan lingkungan Python yang opinionated dan disetel untuk Claude. Anthropic menangani manajemen kontainer, eksekusi kode, dan komunikasi pemanggilan alat yang aman.

**Keuntungan:**

* Aman dan terjamin secara default
* Diaktifkan dengan definisi alat, tanpa infrastruktur yang perlu dijalankan
* Lingkungan dan instruksi dioptimalkan untuk Claude

Pertimbangkan untuk menggunakan solusi terkelola Anthropic jika Anda menggunakan Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), atau [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, pemanggilan alat secara terprogram memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure).

## Retensi data

Pemanggilan alat secara terprogram dibangun di atas infrastruktur eksekusi kode dan menggunakan kontainer sandbox yang sama. Data kontainer, termasuk artefak eksekusi dan output, disimpan hingga 30 hari.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Fine-grained tool streaming" icon="bolt" href="/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming">
    Stream input alat tanpa buffering JSON sisi server untuk aplikasi yang sensitif terhadap latensi.
  </Card>

  <Card title="Alat eksekusi kode" icon="code" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Jalankan kode Python dan bash di kontainer sandbox untuk menganalisis data, menghasilkan file, dan melakukan iterasi pada solusi.
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="wrench" href="/docs/id/agents-and-tools/tool-use/overview">
    Hubungkan Claude ke alat dan API eksternal. Lihat di mana alat dieksekusi, kapan Claude memanggilnya, dan alat mana yang sesuai dengan tugas Anda.
  </Card>

  <Card title="Mendefinisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tentukan skema alat, tulis deskripsi yang efektif, dan kontrol kapan Claude memanggil alat Anda.
  </Card>
</CardGroup>
