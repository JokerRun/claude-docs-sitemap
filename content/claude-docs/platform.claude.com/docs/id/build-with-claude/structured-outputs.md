---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/structured-outputs
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: cee00dfb8b177a634a684736b39abac7f02b3b397d3269865ce3f092c3ff7f0e
---

# Output terstruktur

Dapatkan hasil JSON yang tervalidasi dari alur kerja agen

---

Output terstruktur membatasi respons Claude agar mengikuti skema tertentu, memastikan output yang valid dan dapat diurai untuk pemrosesan lanjutan. Output terstruktur menyediakan dua fitur yang saling melengkapi:

* **Output JSON** (`output_config.format`): Dapatkan respons Claude dalam format JSON tertentu
* **Penggunaan alat ketat** (`strict: true`): Menjamin validasi skema pada nama dan input alat

Anda dapat menggunakan fitur-fitur ini secara independen atau bersamaan dalam permintaan yang sama.

<Note>
  Output terstruktur tersedia secara umum di Claude API untuk Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5. Di Amazon Bedrock, output terstruktur tersedia secara umum untuk Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5; Claude Sonnet 5, Claude Opus 4.7, dan Claude Mythos Preview tersedia melalui [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) (endpoint Bedrock Messages-API). Output terstruktur tersedia di [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws). Di [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai), output terstruktur tersedia secara umum untuk Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5. Output terstruktur tersedia secara umum di [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry) dan memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure).
</Note>

<Note>
  Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention) dengan retensi teknis terbatas. Lihat bagian [Retensi data](#data-retention) untuk detail tentang apa yang disimpan dan alasannya.
</Note>

<Tip>
  **Bermigrasi dari beta?** Parameter `output_format` telah dipindahkan ke `output_config.format`, dan header beta tidak lagi diperlukan. Header beta lama (`structured-outputs-2025-11-13`) dan parameter `output_format` akan tetap berfungsi selama periode transisi. Lihat contoh kode berikut untuk bentuk API yang diperbarui.
</Tip>

## Mengapa menggunakan output terstruktur

Tanpa output terstruktur, Claude dapat menghasilkan respons JSON yang salah format atau input alat yang tidak valid yang merusak aplikasi Anda. Bahkan dengan prompting yang cermat, Anda mungkin menemui:

* Kesalahan parsing dari sintaks JSON yang tidak valid
* Field wajib yang hilang
* Tipe data yang tidak konsisten
* Pelanggaran skema yang memerlukan penanganan kesalahan dan percobaan ulang

Output terstruktur menjamin respons yang sesuai skema melalui "constrained decoding" (dekode terbatas):

* **Selalu valid:** Tidak ada lagi kesalahan `JSON.parse()`
* **Aman secara tipe:** Tipe field dan field wajib yang terjamin
* **Andal:** Tidak perlu percobaan ulang untuk pelanggaran skema

## Output JSON

Output JSON mengontrol format respons Claude, memastikan Claude mengembalikan JSON valid yang cocok dengan skema Anda. Gunakan output JSON ketika Anda perlu:

* Mengontrol format respons Claude
* Mengekstrak data dari gambar atau teks
* Menghasilkan laporan terstruktur
* Memformat respons API

### Mulai cepat

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
        }
      ],
      "output_config": {
        "format": {
          "type": "json_schema",
          "schema": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "email": {"type": "string"},
              "plan_interest": {"type": "string"},
              "demo_requested": {"type": "boolean"}
            },
            "required": ["name", "email", "plan_interest", "demo_requested"],
            "additionalProperties": false
          }
        }
      }
    }'
  ```

  ```bash CLI
  ant messages create \
    --transform 'content.0.text|@fromstr' \
    --format jsonl <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: >-
        Extract the key information from this email: John Smith
        (john@example.com) is interested in our Enterprise plan and wants
        to schedule a demo for next Tuesday at 2pm.
  output_config:
    format:
      type: json_schema
      schema:
        type: object
        properties:
          name: {type: string}
          email: {type: string}
          plan_interest: {type: string}
          demo_requested: {type: boolean}
        required: [name, email, plan_interest, demo_requested]
        additionalProperties: false
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.",
          }
      ],
      output_config={
          "format": {
              "type": "json_schema",
              "schema": {
                  "type": "object",
                  "properties": {
                      "name": {"type": "string"},
                      "email": {"type": "string"},
                      "plan_interest": {"type": "string"},
                      "demo_requested": {"type": "boolean"},
                  },
                  "required": ["name", "email", "plan_interest", "demo_requested"],
                  "additionalProperties": False,
              },
          }
      },
  )
  print(response.content[0].text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content:
          "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
      }
    ],
    output_config: {
      format: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            name: { type: "string" },
            email: { type: "string" },
            plan_interest: { type: "string" },
            demo_requested: { type: "boolean" }
          },
          required: ["name", "email", "plan_interest", "demo_requested"],
          additionalProperties: false
        }
      }
    }
  });

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan." }],
      OutputConfig = new OutputConfig
      {
          Format = new JsonOutputFormat
          {
              Schema = new Dictionary<string, JsonElement>
              {
                  ["type"] = JsonSerializer.SerializeToElement("object"),
                  ["properties"] = JsonSerializer.SerializeToElement(new
                  {
                      name = new { type = "string" },
                      email = new { type = "string" },
                      plan_interest = new { type = "string" },
                      demo_requested = new { type = "boolean" },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(new[] { "name", "email", "plan_interest", "demo_requested" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              },
          },
      },
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, _ := client.Messages.New(context.Background(),
  	anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(
  				anthropic.NewTextBlock("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."),
  			),
  		},
  		OutputConfig: anthropic.OutputConfigParam{
  			Format: anthropic.JSONOutputFormatParam{
  				Schema: map[string]any{
  					"type": "object",
  					"properties": map[string]any{
  						"name":           map[string]string{"type": "string"},
  						"email":          map[string]string{"type": "string"},
  						"plan_interest":  map[string]string{"type": "string"},
  						"demo_requested": map[string]string{"type": "boolean"},
  					},
  					"required":             []string{"name", "email", "plan_interest", "demo_requested"},
  					"additionalProperties": false,
  				},
  			},
  		},
  	})

  fmt.Println(response.Content[0].Text)
  ```

  ```java Java
  static class ContactInfo {
      public String name;
      public String email;
      public String plan_interest;
      public boolean demo_requested;
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      StructuredMessageCreateParams<ContactInfo> params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .addUserMessage("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.")
          .outputConfig(ContactInfo.class)
          .build();

      StructuredMessage<ContactInfo> response = client.messages().create(params);
      ContactInfo contact = response.content().stream()
          .flatMap(block -> block.text().stream())
          .findFirst().orElseThrow().text();
      IO.println(contact.name + " (" + contact.email + ")");
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'
          ]
      ],
      model: 'claude-opus-4-8',
      outputConfig: [
          'format' => [
              'type' => 'json_schema',
              'schema' => [
                  'type' => 'object',
                  'properties' => [
                      'name' => ['type' => 'string'],
                      'email' => ['type' => 'string'],
                      'plan_interest' => ['type' => 'string'],
                      'demo_requested' => ['type' => 'boolean']
                  ],
                  'required' => ['name', 'email', 'plan_interest', 'demo_requested'],
                  'additionalProperties' => false
              ]
          ]
      ],
  );

  echo $response->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."
      }
    ],
    output_config: {
      format: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            name: { type: "string" },
            email: { type: "string" },
            plan_interest: { type: "string" },
            demo_requested: { type: "boolean" }
          },
          required: ["name", "email", "plan_interest", "demo_requested"],
          additionalProperties: false
        }
      }
    }
  )

  puts response.content[0].text
  ```
</CodeGroup>

**Format respons:** JSON valid yang cocok dengan skema Anda di `response.content[0].text`

```json Output
{
  "name": "John Smith",
  "email": "john@example.com",
  "plan_interest": "Enterprise",
  "demo_requested": true
}
```

### Cara kerjanya

<Steps>
  <Step title="Definisikan skema JSON Anda">
    Buat skema JSON yang mendeskripsikan struktur yang Anda inginkan untuk diikuti Claude. Skema ini menggunakan format JSON Schema standar dengan beberapa batasan (lihat [Batasan JSON Schema](#json-schema-limitations)).
  </Step>

  <Step title="Tambahkan parameter output_config.format">
    Sertakan parameter `output_config.format` dalam permintaan API Anda dengan `type: "json_schema"` dan definisi skema Anda.
  </Step>

  <Step title="Urai respons">
    Respons Claude adalah JSON valid yang cocok dengan skema Anda, dikembalikan di `response.content[0].text`.
  </Step>
</Steps>

### Bekerja dengan output JSON di SDK

SDK menyediakan helper yang memudahkan bekerja dengan output JSON, termasuk transformasi skema, validasi otomatis, dan integrasi dengan pustaka skema populer.

<Note>
  `client.messages.parse()` pada SDK Python masih menerima `output_format` sebagai parameter kemudahan dan menerjemahkannya ke `output_config.format` secara internal. SDK lain memerlukan `output_config` secara langsung. Contoh berikut menunjukkan sintaks helper SDK.
</Note>

#### Menggunakan definisi skema native

Alih-alih menulis skema JSON mentah, Anda dapat menggunakan alat definisi skema yang familier dalam bahasa Anda:

* **Python:** Model [Pydantic](https://docs.pydantic.dev/) dengan `client.messages.parse()`
* **TypeScript:** Skema [Zod](https://zod.dev/) dengan `zodOutputFormat()` atau literal JSON Schema bertipe dengan `jsonSchemaOutputFormat()`
* **Java:** Kelas Java biasa dengan derivasi skema otomatis melalui `outputConfig(Class<T>)`
* **Ruby:** Kelas `Anthropic::BaseModel` dengan `output_config: {format: Model}`
* **PHP:** Kelas yang mengimplementasikan `StructuredOutputModel` dengan `outputConfig: ['format' => MyClass::class]`
* **C#:** Kelas C# biasa dengan overload generik `Create<T>()`, yang menurunkan skema secara otomatis
* **Go:** Struct Go yang direfleksikan menjadi skema JSON secara otomatis pada API beta, atau skema JSON mentah melalui `output_config`
* **CLI:** Skema JSON mentah yang diteruskan melalui `output_config`

<CodeGroup>
  ```bash CLI
  { read -r _ NAME; read -r _ EMAIL; } < <(
    ant messages create \
      --transform 'content.0.text|@fromstr|{name,email}' \
      --format yaml <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: >-
        Extract the key information from this email: John Smith
        (john@example.com) is interested in our Enterprise plan and wants
        to schedule a demo for next Tuesday at 2pm.
  output_config:
    format:
      type: json_schema
      schema:
        type: object
        properties:
          name: {type: string}
          email: {type: string}
          plan_interest: {type: string}
          demo_requested: {type: boolean}
        required: [name, email, plan_interest, demo_requested]
        additionalProperties: false
  YAML
  )
  printf '%s (%s)\n' "$NAME" "$EMAIL"
  ```

  ```python Python
  from pydantic import BaseModel
  from anthropic import Anthropic


  class ContactInfo(BaseModel):
      name: str
      email: str
      plan_interest: str
      demo_requested: bool


  client = Anthropic()

  response = client.messages.parse(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.",
          }
      ],
      output_format=ContactInfo,
  )

  print(response.parsed_output)
  ```

  ```typescript TypeScript
  import { z } from "zod";
  import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

  const ContactInfoSchema = z.object({
    name: z.string(),
    email: z.string(),
    plan_interest: z.string(),
    demo_requested: z.boolean()
  });

  const client = new Anthropic();

  const response = await client.messages.parse({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content:
          "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
      }
    ],
    output_config: { format: zodOutputFormat(ContactInfoSchema) }
  });

  // Diurai dan divalidasi secara otomatis
  console.log(response.parsed_output);
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic;
  using Anthropic.Models.Messages;

  var client = new AnthropicClient();

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() {
          Role = Role.User,
          Content = "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
      }],
      OutputConfig = new OutputConfig
      {
          Format = new JsonOutputFormat
          {
              Schema = new Dictionary<string, JsonElement>
              {
                  ["type"] = JsonSerializer.SerializeToElement("object"),
                  ["properties"] = JsonSerializer.SerializeToElement(new
                  {
                      name = new { type = "string" },
                      email = new { type = "string" },
                      plan_interest = new { type = "string" },
                      demo_requested = new { type = "boolean" },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(
                      new[] { "name", "email", "plan_interest", "demo_requested" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              },
          },
      },
  });

  if (response.Content[0].TryPickText(out var textBlock))
  {
      // JSON dijamin sesuai dengan skema
      var contact = JsonSerializer.Deserialize<Dictionary<string, object>>(textBlock.Text)!;
      Console.WriteLine($"{contact["name"]} ({contact["email"]})");
  }
  ```

  ```go Go
  import (
  // ...
  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/invopop/jsonschema"
  )

  type ContactInfo struct {
  	Name          string `json:"name" jsonschema:"description=Full name"`
  	Email         string `json:"email" jsonschema:"description=Email address"`
  	PlanInterest  string `json:"plan_interest" jsonschema:"description=Plan type"`
  	DemoRequested bool   `json:"demo_requested" jsonschema:"description=Whether a demo was requested"`
  }

  func generateSchema(v any) map[string]any {
  	r := jsonschema.Reflector{AllowAdditionalProperties: false, DoNotReference: true}
  	s := r.Reflect(v)
  	b, _ := json.Marshal(s)
  	var m map[string]any
  	json.Unmarshal(b, &m)
  	return m
  }
  // ...
  	schema := generateSchema(&ContactInfo{})

  	message, _ := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(
  				"Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.",
  			)),
  		},
  		OutputConfig: anthropic.OutputConfigParam{
  			Format: anthropic.JSONOutputFormatParam{
  				Schema: schema,
  			},
  		},
  	})

  	for _, block := range message.Content {
  		switch variant := block.AsAny().(type) {
  		case anthropic.TextBlock:
  			var contact ContactInfo
  			json.Unmarshal([]byte(variant.Text), &contact)
  			fmt.Printf("%s (%s)\n", contact.Name, contact.Email)
  		}
  	}
  ```

  ```java Java
  static class ContactInfo {
      public String name;
      public String email;
      public String planInterest;
      public boolean demoRequested;
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .outputConfig(ContactInfo.class)
          .addUserMessage("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.")
          .build();

      StructuredMessage<ContactInfo> response = client.messages().create(createParams);
      ContactInfo contact = response.content().stream()
          .flatMap(block -> block.text().stream())
          .findFirst().orElseThrow().text();
      IO.println(contact.name + " (" + contact.email + ")");
  }
  ```

  ```php PHP
  use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
  use Anthropic\Lib\Contracts\StructuredOutputModel;

  $client = new Client();

  class ContactInfo implements StructuredOutputModel
  {
      use StructuredOutputModelTrait;

      public string $name;
      public string $email;
      public string $plan_interest;
      public bool $demo_requested;
  }

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.'],
      ],
      model: 'claude-opus-4-8',
      outputConfig: ['format' => ContactInfo::class],
  );

  $contact = $message->parsedOutput();
  if ($contact instanceof ContactInfo) {
      echo "{$contact->name} ({$contact->email})\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  class ContactInfo < Anthropic::BaseModel
    required :name, String
    required :email, String
    required :plan_interest, String
    required :demo_requested, Anthropic::Boolean
  end

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{
      role: "user",
      content: "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
    }],
    output_config: {format: ContactInfo}
  )

  contact = message.parsed_output
  puts "#{contact.name} (#{contact.email})"
  ```
</CodeGroup>

#### Metode khusus SDK

Setiap SDK menyediakan helper yang memudahkan bekerja dengan output terstruktur. Lihat halaman SDK masing-masing untuk detail lengkap.

<Tabs>
  <Tab title="CLI">
    **Skema JSON mentah melalui body heredoc**

    CLI meneruskan skema JSON mentah sebagai body heredoc YAML. Gunakan modifier GJSON `@fromstr` dengan `--transform` untuk mengurai string JSON yang dikembalikan di `content[0].text` dan memproyeksikan field tertentu.

    ```bash
    ant messages create \
      --transform 'content.0.text|@fromstr|{name,email}' \
      --format yaml <<'YAML'
    model: claude-opus-4-8
    max_tokens: 1024
    messages:
      - role: user
        content: >-
          Extract contact info: John Smith, john@example.com,
          interested in the Pro plan
    output_config:
      format:
        type: json_schema
        schema:
          type: object
          properties:
            name: {type: string}
            email: {type: string}
            plan_interest: {type: string}
          required: [name, email, plan_interest]
          additionalProperties: false
    YAML
    ```

    ```yaml Output
    name: John Smith
    email: john@example.com
    ```
  </Tab>

  <Tab title="Python">
    **`client.messages.parse()` (Direkomendasikan)**

    Metode `parse()` secara otomatis mentransformasi model Pydantic Anda, memvalidasi respons, dan mengembalikan atribut `parsed_output`.

    ```python
    from pydantic import BaseModel
    # ...
    class ContactInfo(BaseModel):
        name: str
        email: str
        plan_interest: str
    # ...
    response = client.messages.parse(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Extract contact info: John Smith, john@example.com, interested in the Pro plan",
            }
        ],
        output_format=ContactInfo,
    )

    # Akses output yang telah di-parse secara langsung
    contact = response.parsed_output
    print(contact.name, contact.email)
    ```

    **Helper `transform_schema()`**

    Untuk saat Anda perlu mentransformasi skema secara manual sebelum mengirim, atau ketika Anda ingin memodifikasi skema yang dihasilkan Pydantic. Tidak seperti `client.messages.parse()`, yang mentransformasi skema yang disediakan secara otomatis, ini memberi Anda skema yang telah ditransformasi sehingga Anda dapat menyesuaikannya lebih lanjut.

    ```python
    from anthropic import transform_schema
    from pydantic import TypeAdapter
    # ...

    # Pertama konversi model Pydantic ke skema JSON, lalu transformasikan
    schema = TypeAdapter(ContactInfo).json_schema()
    schema = transform_schema(schema)
    # Modifikasi skema jika diperlukan
    schema["properties"]["custom_field"] = {"type": "string"}

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[{"role": "user", "content": "..."}],
        output_config={
            "format": {"type": "json_schema", "schema": schema},
        },
    )
    ```
  </Tab>

  <Tab title="TypeScript">
    **`client.messages.parse()` dengan `zodOutputFormat()`**

    Metode `parse()` menerima skema Zod, memvalidasi respons, dan mengembalikan atribut `parsed_output` dengan tipe TypeScript yang disimpulkan yang cocok dengan skema.

    ```typescript
    import { z } from "zod";
    import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

    const ContactInfo = z.object({
      name: z.string(),
      email: z.string(),
      planInterest: z.string()
    });

    const client = new Anthropic();

    const response = await client.messages.parse({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "Extract contact info: John Smith, john@example.com, interested in the Pro plan"
        }
      ],
      output_config: { format: zodOutputFormat(ContactInfo) }
    });

    // Dijamin type-safe
    console.log(response.parsed_output!.email);
    ```

    **`client.messages.parse()` dengan `jsonSchemaOutputFormat()`**

    Helper `jsonSchemaOutputFormat()` menerima objek JSON Schema dan mengintegrasikannya dengan `parse()` tanpa memerlukan Zod. Zod adalah peer dependency opsional yang Anda instal secara terpisah; `jsonSchemaOutputFormat()` berfungsi langsung karena SDK membundel `json-schema-to-ts` secara langsung.

    Untuk **literal skema inline** (dideklarasikan dengan `as const` di sumber Anda), Anda juga mendapatkan inferensi tipe pada waktu kompilasi: `parsed_output` diberi tipe agar cocok dengan struktur skema. Untuk **skema yang diimpor atau dihasilkan** (dari file JSON atau codegen OpenAPI), helper tetap mengirim skema dan mengurai respons, tetapi tipe yang disimpulkan adalah `unknown` karena `as const` hanya dapat diterapkan pada ekspresi literal.

    ```typescript
    import { jsonSchemaOutputFormat } from "@anthropic-ai/sdk/helpers/json-schema";

    const client = new Anthropic();

    const response = await client.messages.parse({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "Extract contact info: John Smith, john@example.com, interested in the Pro plan"
        }
      ],
      output_config: {
        format: jsonSchemaOutputFormat({
          type: "object",
          properties: {
            name: { type: "string" },
            email: { type: "string" },
            planInterest: { type: "string" }
          },
          required: ["name", "email", "planInterest"],
          additionalProperties: false
        } as const)
      }
    });

    // response.parsed_output bertipe { name: string; email: string; planInterest: string } | null
    console.log(response.parsed_output!.email);
    ```

    **Inferensi tipe memerlukan `as const`.** Gunakan ekspresi objek literal dengan assertion `const` sehingga TypeScript dapat mempersempit tipe properti. Tanpa `as const`, tipe yang disimpulkan runtuh menjadi `unknown`.

    **Transformasi skema.** Secara default, helper mentransformasi skema dengan cara yang sama seperti `zodOutputFormat()`: menghapus constraint yang tidak didukung, menambahkan `additionalProperties: false` ke objek, dan memfilter format string. Teruskan `jsonSchemaOutputFormat(schema, { transform: false })` untuk mengirim skema Anda ke API tanpa perubahan. Lihat [Cara kerja transformasi SDK](#how-sdk-transformation-works).
  </Tab>

  <Tab title="C#">
    **Skema JSON melalui `OutputConfig`**

    SDK C# menerima skema JSON mentah yang dibangun secara programatik dengan `JsonSerializer.SerializeToElement`, seperti yang ditunjukkan di sini, atau menurunkan skema dari kelas C# biasa dengan overload generik `Create<T>()`. Deserialisasi JSON respons dengan `JsonSerializer.Deserialize`.

    ```csharp
    using System.Text.Json;
    using Anthropic;
    using Anthropic.Models.Messages;

    var client = new AnthropicClient();

    var response = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Messages = [new() {
            Role = Role.User,
            Content = "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."
        }],
        OutputConfig = new OutputConfig
        {
            Format = new JsonOutputFormat
            {
                Schema = new Dictionary<string, JsonElement>
                {
                    ["type"] = JsonSerializer.SerializeToElement("object"),
                    ["properties"] = JsonSerializer.SerializeToElement(new
                    {
                        name = new { type = "string" },
                        email = new { type = "string" },
                        plan_interest = new { type = "string" },
                    }),
                    ["required"] = JsonSerializer.SerializeToElement(
                        new[] { "name", "email", "plan_interest" }),
                    ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                },
            },
        },
    });

    if (response.Content[0].TryPickText(out var textBlock))
    {
        // JSON dijamin sesuai dengan skema
        var contact = JsonSerializer.Deserialize<Dictionary<string, object>>(textBlock.Text)!;
        Console.WriteLine($"{contact["name"]} ({contact["email"]})");
    }
    ```
  </Tab>

  <Tab title="Go">
    **Skema JSON mentah melalui `OutputConfigParam`**

    SDK Go bekerja dengan skema JSON mentah. Definisikan struct Go dengan tag json, hasilkan skema JSON (misalnya, menggunakan `invopop/jsonschema`), dan unmarshal teks respons ke dalam struct Anda. Pada API beta, meneruskan struct sebagai skema format output akan merefleksikannya menjadi skema JSON secara otomatis.

    ```go
    import (
    // ...
    	"github.com/anthropics/anthropic-sdk-go"
    	"github.com/invopop/jsonschema"
    )

    type ContactInfo struct {
    	Name         string `json:"name" jsonschema:"description=Full name"`
    	Email        string `json:"email" jsonschema:"description=Email address"`
    	PlanInterest string `json:"plan_interest" jsonschema:"description=Plan type"`
    }

    func generateSchema(v any) map[string]any {
    	r := jsonschema.Reflector{AllowAdditionalProperties: false, DoNotReference: true}
    	s := r.Reflect(v)
    	b, _ := json.Marshal(s)
    	var m map[string]any
    	json.Unmarshal(b, &m)
    	return m
    }
    // ...
    	schema := generateSchema(&ContactInfo{})

    	message, _ := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     anthropic.ModelClaudeOpus4_8,
    		MaxTokens: 1024,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock(
    				"Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.",
    			)),
    		},
    		OutputConfig: anthropic.OutputConfigParam{
    			Format: anthropic.JSONOutputFormatParam{
    				Schema: schema,
    			},
    		},
    	})

    	for _, block := range message.Content {
    		switch variant := block.AsAny().(type) {
    		case anthropic.TextBlock:
    			var contact ContactInfo
    			json.Unmarshal([]byte(variant.Text), &contact)
    			fmt.Printf("%s (%s)\n", contact.Name, contact.Email)
    		}
    	}
    ```
  </Tab>

  <Tab title="Java">
    Contoh Java di halaman ini menggunakan sintaks [compact source file JDK 25](https://openjdk.org/jeps/512); lihat [persyaratan SDK Java](/docs/id/cli-sdks-libraries/sdks/java#requirements) untuk substitusi pada JDK yang lebih lama.

    **Metode `outputConfig(Class<T>)`**

    Teruskan kelas Java ke `outputConfig()` dan SDK secara otomatis menurunkan skema JSON, memvalidasinya, dan mengembalikan `StructuredMessageCreateParams<T>`. Akses hasil yang diurai melalui `response.content().stream().flatMap(block -> block.text().stream()).findFirst().orElseThrow().text()`.

    <Note>
      Deklarasikan kelas skema Anda sebagai kelas tingkat atas atau kelas bersarang `static`. Persyaratan ini berasal dari pustaka Jackson Databind (`com.fasterxml.jackson.databind`), yang digunakan SDK untuk mendeserialisasi respons JSON menjadi instance kelas Anda dan tidak dapat menginstansiasi inner class non-static.
    </Note>

    ```java
    static class ContactInfo {
        public String name;
        public String email;
        public String planInterest;
    }

    void main() {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024)
            .outputConfig(ContactInfo.class)
            .addUserMessage("Extract contact info: John Smith, john@example.com, interested in the Pro plan")
            .build();

        StructuredMessage<ContactInfo> response = client.messages().create(createParams);
        ContactInfo contact = response.content().stream()
            .flatMap(block -> block.text().stream())
            .findFirst().orElseThrow().text();
        IO.println(contact.name + " (" + contact.email + ")");
    }
    ```

    <Accordion title="Penghapusan tipe generik">
      Java mempertahankan informasi tipe generik untuk field dalam metadata kelas, tetapi penghapusan tipe generik berlaku di cakupan lain. Meskipun skema JSON dapat diturunkan dari field `BookList.books` dengan tipe `List<Book>`, skema JSON yang valid tidak dapat diturunkan dari variabel lokal dengan tipe yang sama.

      Jika terjadi kesalahan saat mengonversi respons JSON ke instance kelas Java, pesan kesalahan menyertakan respons JSON untuk membantu diagnosis. Jika respons JSON Anda mungkin berisi informasi sensitif, hindari mencatatnya secara langsung, atau pastikan Anda menyunting detail sensitif apa pun dari pesan kesalahan.
    </Accordion>

    <Accordion title="Validasi skema lokal">
      Output terstruktur mendukung [subset dari bahasa JSON Schema](/docs/id/build-with-claude/structured-outputs#json-schema-limitations). SDK menghasilkan skema secara otomatis dari kelas agar selaras dengan subset ini. Metode `outputConfig(Class<T>)` melakukan pemeriksaan validasi pada skema yang diturunkan dari kelas yang ditentukan.

      Poin-poin penting:

      * **Validasi lokal** terjadi tanpa mengirim permintaan ke model AI jarak jauh.
      * **Validasi jarak jauh** juga dilakukan oleh model AI setelah menerima skema JSON.
      * **Kompatibilitas versi:** Validasi lokal mungkin gagal sementara validasi jarak jauh berhasil jika versi SDK sudah usang.
      * **Menonaktifkan validasi lokal:** Teruskan `JsonSchemaLocalValidation.NO` jika Anda mengalami masalah kompatibilitas:

      ```java
      import com.anthropic.core.JsonSchemaLocalValidation;
      // ...

      static class BookList {
          public List<String> books;
      }

      void main() {
          StructuredMessageCreateParams<BookList> createParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(2048)
              .outputConfig(BookList.class, JsonSchemaLocalValidation.NO)
              .addUserMessage("List some famous late twentieth century novels.")
              .build();
      }
      ```
    </Accordion>

    <Accordion title="Streaming">
      Output terstruktur juga berfungsi dengan streaming. Saat respons tiba dalam event stream, Anda perlu mengakumulasi respons lengkap sebelum mendeserialisasi JSON.

      Gunakan `MessageAccumulator` untuk mengumpulkan string JSON dari stream. Setelah terakumulasi, panggil `MessageAccumulator.message(Class<T>)` untuk mengonversi `Message` yang terakumulasi menjadi `StructuredMessage`, yang secara otomatis mendeserialisasi JSON ke dalam kelas Java Anda.
    </Accordion>

    <Accordion title="Properti skema JSON">
      Ketika SDK menurunkan skema JSON dari kelas Java Anda, SDK menyertakan semua properti yang direpresentasikan oleh field `public` atau metode getter `public` secara default dan mengecualikan field dan metode getter non-`public`.

      Anda dapat mengontrol visibilitas dengan anotasi:

      * `@JsonIgnore` mengecualikan field atau metode getter `public`
      * `@JsonProperty` menyertakan field atau metode getter non-`public`

      Jika Anda mendefinisikan field `private` dengan metode getter `public`, SDK menurunkan nama properti dari getter (misalnya, field `private` `myValue` dengan metode `public` `getMyValue()` menghasilkan properti `"myValue"`). Untuk menggunakan nama getter non-konvensional, anotasi metode dengan `@JsonProperty`.

      Setiap kelas harus mendefinisikan setidaknya satu properti untuk skema JSON. Kesalahan validasi terjadi jika tidak ada field atau metode getter yang dapat menghasilkan properti skema, seperti ketika:

      * Tidak ada field atau metode getter di kelas
      * Semua anggota `public` dianotasi dengan `@JsonIgnore`
      * Semua anggota non-`public` tidak memiliki anotasi `@JsonProperty`
      * Sebuah field menggunakan tipe `Map`, yang menghasilkan field `"properties"` kosong
    </Accordion>

    <Accordion title="Komposisi dan pewarisan">
      Kelas Java Anda dapat menggunakan komposisi dan pewarisan untuk berbagi struktur saat mendefinisikan skema JSON. Setiap pola memengaruhi struktur output secara berbeda.

      **Komposisi** menghasilkan output JSON bersarang. Menurunkan skema dari kelas `Composed` yang mengomposisi `A` dan `B`:

      ```java
      static class A {
          public String a;
      }

      static class B {
          public String b;
      }

      static class Composed {
          public A composedA;
          public B composedB;
      }
      ```

      Output JSON memiliki struktur bersarang ini:

      ```json
      {
        "composedA": { "a": "hello" },
        "composedB": { "b": "world" }
      }
      ```

      **Pewarisan** menghasilkan output JSON datar. Menurunkan skema dari kelas `Derived` yang meng-extend `Base`:

      ```java
      static class Base {
          public String a;
      }

      static class Derived extends Base {
          public String b;
      }
      ```

      Output JSON memiliki struktur datar ini:

      ```json
      {
        "a": "hello",
        "b": "world"
      }
      ```
    </Accordion>

    <Accordion title="Anotasi (Jackson dan Swagger)">
      Anda dapat menggunakan anotasi Jackson Databind untuk memperkaya skema JSON yang diturunkan dari kelas Java Anda:

      ```java
      import com.fasterxml.jackson.annotation.JsonClassDescription;
      import com.fasterxml.jackson.annotation.JsonIgnore;
      import com.fasterxml.jackson.annotation.JsonPropertyDescription;

      static class Person {

        @JsonPropertyDescription("The first name and surname of the person")
        public String name;

        public int birthYear;

        @JsonPropertyDescription("The year the person died, or 'present' if the person is living.")
        public String deathYear;
      }

      @JsonClassDescription("The details of one published book")
      static class Book {

        public String title;
        public Person author;

        @JsonPropertyDescription("The year in which the book was first published.")
        public int publicationYear;

        @JsonIgnore
        public String genre;
      }

      static class BookList {
        public List<Book> books;
      }
      ```

      Ringkasan anotasi:

      * `@JsonClassDescription`: Menambahkan deskripsi ke kelas
      * `@JsonPropertyDescription`: Menambahkan deskripsi ke field atau metode getter
      * `@JsonIgnore`: Mengecualikan field atau getter `public` dari skema
      * `@JsonProperty`: Menyertakan field atau getter non-`public` dalam skema

      Jika Anda menggunakan `@JsonProperty(required = false)`, SDK mengabaikan nilai `false`. Skema yang diturunkan dari kelas selalu menandai semua properti sebagai wajib.

      Anda juga dapat menggunakan anotasi Swagger Core (OpenAPI 3) `@Schema` dan `@ArraySchema` untuk constraint khusus tipe:

      ```java
      import io.swagger.v3.oas.annotations.media.ArraySchema;
      import io.swagger.v3.oas.annotations.media.Schema;

      static class Article {

        @ArraySchema(minItems = 1)
        public List<String> authors;

        public String title;

        @Schema(format = "date")
        public String publicationDate;

        public int pageCount;
      }
      ```

      Validasi lokal memeriksa bahwa Anda tidak menggunakan kata kunci constraint yang tidak didukung, tetapi nilai constraint tidak divalidasi secara lokal. Misalnya, nilai `"format"` yang tidak didukung mungkin lolos validasi lokal tetapi menyebabkan kesalahan jarak jauh.

      Jika Anda menggunakan anotasi Jackson dan Swagger untuk mengatur field skema yang sama, anotasi Jackson yang diutamakan.
    </Accordion>

    <Accordion title="Mendefinisikan skema tanpa kelas Java">
      Derivasi skema berbasis kelas adalah jalur yang paling nyaman, tetapi untuk kontrol langsung atas struktur skema, Anda dapat membangun `JsonOutputFormat.Schema` secara manual dan membungkusnya dalam `OutputConfig`.

      ```java
      import com.anthropic.core.JsonValue;
      import com.anthropic.models.messages.JsonOutputFormat;
      // ...
      import com.anthropic.models.messages.OutputConfig;

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          JsonOutputFormat.Schema schema = JsonOutputFormat.Schema.builder()
              .putAdditionalProperty("type", JsonValue.from("object"))
              .putAdditionalProperty("properties", JsonValue.from(Map.of(
                  "name", Map.of("type", "string"),
                  "email", Map.of("type", "string"),
                  "plan_interest", Map.of("type", "string"))))
              .putAdditionalProperty("required", JsonValue.from(
                  List.of("name", "email", "plan_interest")))
              .putAdditionalProperty("additionalProperties", JsonValue.from(false))
              .build();

          OutputConfig outputConfig = OutputConfig.builder()
              .format(JsonOutputFormat.builder().schema(schema).build())
              .build();

          MessageCreateParams createParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024)
              .outputConfig(outputConfig)
              .addUserMessage(
                  "John Smith (john@example.com) is interested in our Enterprise plan.")
              .build();

          client.messages().create(createParams).content().stream()
              .flatMap(contentBlock -> contentBlock.text().stream())
              .forEach(textBlock -> IO.println(textBlock.text()));
      }
      ```

      Untuk contoh yang lebih ekstensif yang membangun skema bersarang dengan array dan deskripsi, lihat [`StructuredOutputsRawExample.java`](https://github.com/anthropics/anthropic-sdk-java/blob/main/anthropic-java-example/src/main/java/com/anthropic/example/StructuredOutputsRawExample.java) di repositori SDK.
    </Accordion>
  </Tab>

  <Tab title="PHP">
    **Kelas melalui interface `StructuredOutputModel`**

    Definisikan kelas PHP yang mengimplementasikan `StructuredOutputModel` (menggunakan `StructuredOutputModelTrait`) dan teruskan nama kelas ke `outputConfig: ['format' => MyClass::class]`. SDK menurunkan skema JSON dari tipe properti PHP 8 native Anda dan mengembalikan instance bertipe melalui `$message->parsedOutput()`.

    `parsedOutput()` mengembalikan instance model Anda jika berhasil, atau `null` (atau array kesalahan) jika parsing gagal. Gunakan `instanceof` untuk mempersempit tipe sebelum mengakses field.

    ```php
    use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
    use Anthropic\Lib\Contracts\StructuredOutputModel;

    $client = new Client();

    class ContactInfo implements StructuredOutputModel
    {
        use StructuredOutputModelTrait;

        public string $name;
        public string $email;
        public string $plan_interest;
    }

    $message = $client->messages->create(
        maxTokens: 1024,
        messages: [
            ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'],
        ],
        model: 'claude-opus-4-8',
        outputConfig: ['format' => ContactInfo::class],
    );

    $contact = $message->parsedOutput();
    if ($contact instanceof ContactInfo) {
        echo "{$contact->name} ({$contact->email})\n";
    }
    ```

    <Accordion title="Inferensi tipe">
      SDK memetakan tipe properti PHP 8 native ke JSON Schema:

      | Tipe PHP                                               | JSON Schema                       |
      | ------------------------------------------------------ | --------------------------------- |
      | `string`                                               | `"string"`                        |
      | `int`                                                  | `"integer"`                       |
      | `float`                                                | `"number"`                        |
      | `bool`                                                 | `"boolean"`                       |
      | `array`                                                | `"array"` (lihat catatan berikut) |
      | `?type` (nullable)                                     | Field opsional                    |
      | Kelas yang mengimplementasikan `StructuredOutputModel` | Objek bersarang                   |

      Untuk properti `array`, SDK menambahkan skema `items` hanya ketika tipe elemen adalah `StructuredOutputModel` bersarang, dideklarasikan dengan `#[Constrained(itemClass: MyModel::class)]` atau docblock `/** @var MyModel[] */`. Array skalar (`string[]`, `int[]`) menghasilkan `{"type":"array"}` tanpa constraint.

      Semua properti non-nullable menjadi field wajib.
    </Accordion>

    <Accordion title="Constraint dengan atribut #[Constrained]">
      Tambahkan constraint dengan atribut `#[Constrained]`:

      ```php
      use Anthropic\Lib\Attributes\Constrained;
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      class Address implements StructuredOutputModel { use StructuredOutputModelTrait; public string $street; }

      class Profile implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          #[Constrained(description: 'Age in years', minimum: 0, maximum: 150)]
          public int $age;

          #[Constrained(format: 'email')]
          public string $email;

          #[Constrained(itemClass: Address::class, minItems: 1)]
          public array $addresses;
      }
      ```

      **Constraint yang ditegakkan API** (dikirim dalam skema): `description`, `format`, `const`, `itemClass`, `minItems` (hanya 0 atau 1).

      **Constraint yang divalidasi SDK** (dihapus dari skema yang dikirim, ditambahkan ke deskripsi, dan divalidasi terhadap respons): `minimum`, `maximum`, `multipleOf`, `minLength`, `maxLength`.
    </Accordion>

    <Accordion title="Fallback skema JSON mentah">
      Untuk skema yang tidak dapat diekspresikan oleh type hint PHP, teruskan array asosiatif mentah melalui `OutputConfig::with()`. Jalur ini melewati helper `parsedOutput()`; dekode respons dengan `json_decode()`:

      ```php
      use Anthropic\Messages\OutputConfig;
      use Anthropic\Messages\JSONOutputFormat;

      $client = new Client();

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'],
          ],
          model: 'claude-opus-4-8',
          outputConfig: OutputConfig::with(format: JSONOutputFormat::with(schema: [
              'type' => 'object',
              'properties' => [
                  'name' => ['type' => 'string'],
                  'email' => ['type' => 'string'],
                  'plan_interest' => ['type' => 'string'],
              ],
              'required' => ['name', 'email', 'plan_interest'],
              'additionalProperties' => false,
          ])),
      );

      $contact = json_decode($message->content[0]->text, associative: true);
      echo "{$contact['name']} ({$contact['email']})\n";
      ```
    </Accordion>
  </Tab>

  <Tab title="Ruby">
    **`output_config: {format: Model}` dengan `parsed_output`**

    Definisikan kelas model yang meng-extend `Anthropic::BaseModel` dan teruskan sebagai format ke `messages.create()`. Respons menyertakan atribut `parsed_output` dengan objek Ruby bertipe.

    ```ruby
    class ContactInfo < Anthropic::BaseModel
      required :name, String
      required :email, String
      required :plan_interest, String
    end

    client = Anthropic::Client.new

    message = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "Extract contact info: John Smith, john@example.com, interested in the Pro plan"
        }
      ],
      output_config: {format: ContactInfo}
    )

    contact = message.parsed_output
    puts "#{contact.name} (#{contact.email})"
    ```

    <Accordion title="Fitur model lanjutan">
      SDK Ruby mendukung fitur definisi model tambahan untuk skema yang lebih kaya:

      * **Kata kunci `doc:`:** Tambahkan deskripsi ke field untuk output skema yang lebih informatif
      * **`Anthropic::ArrayOf[T]`:** Array bertipe. Teruskan constraint tingkat array (`min_items:`, `max_items:`) sebagai kata kunci pada `required`/`optional`, bukan pada `ArrayOf` itu sendiri
      * **`Anthropic::EnumOf[:a, :b]`:** Field enum dengan nilai terbatas
      * **`Anthropic::UnionOf[T1, T2]`:** Tipe union yang dipetakan ke `anyOf`

      ```ruby
      class FamousNumber < Anthropic::BaseModel
        required :value, Float
        optional :reason, String, doc: "why is this number mathematically significant?"
      end

      class Output < Anthropic::BaseModel
        required :numbers, Anthropic::ArrayOf[FamousNumber], min_items: 3, max_items: 5
      end

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [{role: "user", content: "give me some famous numbers"}],
        output_config: {format: Output}
      )

      message.parsed_output
      # => #<Output numbers=[#<FamousNumber value=3.14159... reason="Pi adalah...">...]>
      ```
    </Accordion>
  </Tab>
</Tabs>

#### Cara kerja transformasi SDK

SDK Python, TypeScript, Ruby, dan PHP secara otomatis mentransformasi skema dengan fitur yang tidak didukung. SDK C# dan Go menerapkan transformasi yang sama ketika skema diturunkan dari tipe native (`Create<T>()` di C#; refleksi struct atau `BetaJSONSchemaOutputFormat()` pada API beta Go). Langkah-langkah transformasi:

1. **Menghapus constraint yang tidak didukung** (misalnya, `minimum`, `maximum`, `minLength`, `maxLength`)
2. **Memperbarui deskripsi** dengan info constraint (misalnya, "Must be at least 100"), ketika constraint tidak didukung secara langsung dengan output terstruktur
3. **Menambahkan `additionalProperties: false`** ke semua objek
4. **Memfilter format string** ke daftar yang didukung saja
5. **Memvalidasi respons** terhadap skema asli Anda (dengan semua constraint)

Ini berarti Claude menerima skema yang disederhanakan, tetapi kode Anda tetap menegakkan semua constraint melalui validasi.

**Contoh:** Field Pydantic dengan `minimum: 100` menjadi integer biasa dalam skema yang dikirim, tetapi SDK memperbarui deskripsi menjadi "Must be at least 100" dan memvalidasi respons terhadap constraint asli.

### Kasus penggunaan umum

<AccordionGroup>
  <Accordion title="Ekstraksi data">
    Ekstrak data terstruktur dari teks tidak terstruktur:

    <CodeGroup>
      ```bash CLI
      ant messages create \
        --transform 'content.0.text|@fromstr' \
        --format jsonl <<'YAML'
      model: claude-opus-4-8
      max_tokens: 4096
      messages:
        - role: user
          content: "Extract invoice data from: Invoice #12345, Date: 2024-01-15, Total: $500.00"
      output_config:
        format:
          type: json_schema
          schema:
            type: object
            properties:
              invoice_number: {type: string}
              date: {type: string}
              total_amount: {type: number}
              line_items:
                type: array
                items: {type: object, additionalProperties: false}
              customer_name: {type: string}
            required: [invoice_number, date, total_amount, line_items, customer_name]
            additionalProperties: false
      YAML
      ```

      ```python Python
      from pydantic import BaseModel


      class Invoice(BaseModel):
          invoice_number: str
          date: str
          total_amount: float
          line_items: list[dict]
          customer_name: str


      client = anthropic.Anthropic()
      invoice_text = "Invoice #12345, Date: 2024-01-15, Total: $500.00"

      response = client.messages.parse(
          model="claude-opus-4-8",
          max_tokens=4096,
          output_format=Invoice,
          messages=[
              {"role": "user", "content": f"Extract invoice data from: {invoice_text}"}
          ],
      )

      print(response.parsed_output)
      ```

      ```typescript TypeScript
      import { z } from "zod";
      import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

      const client = new Anthropic();

      const InvoiceSchema = z.object({
        invoice_number: z.string(),
        date: z.string(),
        total_amount: z.number(),
        line_items: z.array(z.record(z.string(), z.any())),
        customer_name: z.string()
      });

      const invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";
      const response = await client.messages.parse({
        model: "claude-opus-4-8",
        max_tokens: 4096,
        output_config: { format: zodOutputFormat(InvoiceSchema) },
        messages: [{ role: "user", content: `Extract invoice data from: ${invoiceText}` }]
      });
      console.log(response.parsed_output);
      ```

      ```csharp C#
      AnthropicClient client = new();

      string invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 4096,
          OutputConfig = new OutputConfig
          {
              Format = new JsonOutputFormat
              {
                  Schema = new Dictionary<string, JsonElement>
                  {
                      ["type"] = JsonSerializer.SerializeToElement("object"),
                      ["properties"] = JsonSerializer.SerializeToElement(new
                      {
                          invoice_number = new { type = "string" },
                          date = new { type = "string" },
                          total_amount = new { type = "number" },
                          line_items = new
                          {
                              type = "array",
                              items = new
                              {
                                  type = "object",
                                  additionalProperties = false,
                              },
                          },
                          customer_name = new { type = "string" },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "invoice_number", "date", "total_amount", "line_items", "customer_name" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  },
              },
          },
          Messages = [new() { Role = Role.User, Content = $"Extract invoice data from: {invoiceText}" }]
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      client := anthropic.NewClient()

      invoiceText := "Invoice #12345, Date: 2024-01-15, Total: $500.00"

      schema := map[string]any{
      	"type":                 "object",
      	"additionalProperties": false,
      	"properties": map[string]any{
      		"invoice_number": map[string]any{"type": "string"},
      		"date":           map[string]any{"type": "string"},
      		"total_amount":   map[string]any{"type": "number"},
      		"line_items": map[string]any{
      			"type": "array",
      			"items": map[string]any{
      				"type":                 "object",
      				"additionalProperties": false,
      				"properties": map[string]any{
      					"description": map[string]any{"type": "string"},
      					"quantity":    map[string]any{"type": "number"},
      					"unit_price":  map[string]any{"type": "number"},
      				},
      				"required": []string{"description", "quantity", "unit_price"},
      			},
      		},
      		"customer_name": map[string]any{"type": "string"},
      	},
      	"required": []string{"invoice_number", "date", "total_amount", "line_items", "customer_name"},
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 4096,
      	OutputConfig: anthropic.OutputConfigParam{
      		Format: anthropic.JSONOutputFormatParam{
      			Schema: schema,
      		},
      	},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock(fmt.Sprintf("Extract invoice data from: %s", invoiceText))),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      for _, block := range response.Content {
      	switch variant := block.AsAny().(type) {
      	case anthropic.TextBlock:
      		fmt.Println(variant.Text)
      	}
      }
      ```

      ```java Java
      import com.fasterxml.jackson.annotation.JsonProperty;

      static class LineItem {
          @JsonProperty("description")
          public String description;

          @JsonProperty("quantity")
          public int quantity;

          @JsonProperty("unit_price")
          public double unitPrice;
      }

      static class Invoice {
          @JsonProperty("invoice_number")
          public String invoiceNumber;

          @JsonProperty("date")
          public String date;

          @JsonProperty("total_amount")
          public double totalAmount;

          @JsonProperty("line_items")
          public List<LineItem> lineItems;

          @JsonProperty("customer_name")
          public String customerName;
      }

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          String invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

          StructuredMessageCreateParams<Invoice> params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(4096L)
              .outputConfig(Invoice.class)
              .addUserMessage("Extract invoice data from: " + invoiceText)
              .build();

          StructuredMessage<Invoice> response = client.messages().create(params);
          Invoice invoice = response.content().stream()
              .flatMap(block -> block.text().stream())
              .findFirst().orElseThrow().text();
          IO.println(invoice.invoiceNumber + ": $" + invoice.totalAmount);
      }
      ```

      ```php PHP
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      $client = new Client();

      class Invoice implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          public string $invoice_number;
          public string $date;
          public float $total_amount;
          public array $line_items;
          public string $customer_name;
      }

      $invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

      $message = $client->messages->create(
          maxTokens: 4096,
          messages: [
              ['role' => 'user', 'content' => "Extract invoice data from: $invoiceText"]
          ],
          model: 'claude-opus-4-8',
          outputConfig: ['format' => Invoice::class],
      );

      $invoice = $message->parsedOutput();
      if ($invoice instanceof Invoice) {
          echo "Invoice {$invoice->invoice_number}: \${$invoice->total_amount}\n";
      }
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      class LineItem < Anthropic::BaseModel
        required :description, String
        required :amount, Float
      end

      class Invoice < Anthropic::BaseModel
        required :invoice_number, String
        required :date, String
        required :total_amount, Float
        required :line_items, Anthropic::ArrayOf[LineItem]
        required :customer_name, String
      end

      invoice_text = "Invoice #12345, Date: 2024-01-15, Total: $500.00"

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 4096,
        output_config: {format: Invoice},
        messages: [
          {role: "user", content: "Extract invoice data from: #{invoice_text}"}
        ]
      )

      invoice = message.parsed_output
      puts "Invoice #{invoice.invoice_number}: $#{invoice.total_amount}"
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Klasifikasi">
    Klasifikasikan konten dengan kategori terstruktur:

    <CodeGroup>
      ```bash CLI
      ant messages create \
        --transform 'content.0.text|@fromstr' \
        --format jsonl <<'YAML'
      model: claude-opus-4-8
      max_tokens: 1024
      messages:
        - role: user
          content: "Classify this feedback: Great product, fast shipping!"
      output_config:
        format:
          type: json_schema
          schema:
            type: object
            properties:
              category:
                type: string
              confidence:
                type: number
              tags:
                type: array
                items:
                  type: string
              sentiment:
                type: string
            required:
              - category
              - confidence
              - tags
              - sentiment
            additionalProperties: false
      YAML
      ```

      ```python Python
      from pydantic import BaseModel

      client = Anthropic()


      class Classification(BaseModel):
          category: str
          confidence: float
          tags: list[str]
          sentiment: str


      feedback_text = "Great product, but the delivery was slow."
      response = client.messages.parse(
          model="claude-opus-4-8",
          max_tokens=1024,
          output_format=Classification,
          messages=[{"role": "user", "content": f"Classify this feedback: {feedback_text}"}],
      )

      print(response.parsed_output)
      ```

      ```typescript TypeScript
      import { z } from "zod";
      import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

      const client = new Anthropic();

      const ClassificationSchema = z.object({
        category: z.string(),
        confidence: z.number(),
        tags: z.array(z.string()),
        sentiment: z.string()
      });

      const feedbackText = "Great product, but the delivery was slow.";
      const response = await client.messages.parse({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        output_config: { format: zodOutputFormat(ClassificationSchema) },
        messages: [{ role: "user", content: `Classify this feedback: ${feedbackText}` }]
      });

      console.log(response.parsed_output);
      ```

      ```csharp C#
      string feedbackText = "Great product, fast shipping!";

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = $"Classify this feedback: {feedbackText}" }],
          OutputConfig = new OutputConfig
          {
              Format = new JsonOutputFormat
              {
                  Schema = new Dictionary<string, JsonElement>
                  {
                      ["type"] = JsonSerializer.SerializeToElement("object"),
                      ["properties"] = JsonSerializer.SerializeToElement(new
                      {
                          category = new { type = "string" },
                          confidence = new { type = "number" },
                          tags = new { type = "array", items = new { type = "string" } },
                          sentiment = new { type = "string" },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "category", "confidence", "tags", "sentiment" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  },
              },
          },
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      feedbackText := "Great product, fast shipping!"

      schema := map[string]any{
      	"type": "object",
      	"properties": map[string]any{
      		"category":   map[string]any{"type": "string"},
      		"confidence": map[string]any{"type": "number"},
      		"tags":       map[string]any{"type": "array", "items": map[string]any{"type": "string"}},
      		"sentiment":  map[string]any{"type": "string"},
      	},
      	"required":             []string{"category", "confidence", "tags", "sentiment"},
      	"additionalProperties": false,
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 1024,
      	OutputConfig: anthropic.OutputConfigParam{
      		Format: anthropic.JSONOutputFormatParam{
      			Schema: schema,
      		},
      	},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock(fmt.Sprintf("Classify this feedback: %s", feedbackText))),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      for _, block := range response.Content {
      	switch variant := block.AsAny().(type) {
      	case anthropic.TextBlock:
      		var result map[string]any
      		json.Unmarshal([]byte(variant.Text), &result)
      		fmt.Println(result)
      	}
      }
      ```

      ```java Java
      import com.fasterxml.jackson.annotation.JsonProperty;

      static class Classification {
          @JsonProperty("category")
          public String category;

          @JsonProperty("confidence")
          public double confidence;

          @JsonProperty("tags")
          public List<String> tags;

          @JsonProperty("sentiment")
          public String sentiment;
      }

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          String feedbackText = "Great product, fast shipping!";

          StructuredMessageCreateParams<Classification> params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .outputConfig(Classification.class)
              .addUserMessage("Classify this feedback: " + feedbackText)
              .build();

          StructuredMessage<Classification> response = client.messages().create(params);
          Classification result = response.content().stream()
              .flatMap(block -> block.text().stream())
              .findFirst().orElseThrow().text();
          IO.println(result.category + " (" + result.confidence + ")");
      }
      ```

      ```php PHP
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      $client = new Client();

      class Classification implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          public string $category;
          public float $confidence;
          public array $tags;
          public string $sentiment;
      }

      $feedbackText = "Great product, fast shipping!";

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => "Classify this feedback: {$feedbackText}"]
          ],
          model: 'claude-opus-4-8',
          outputConfig: ['format' => Classification::class],
      );

      $result = $message->parsedOutput();
      if ($result instanceof Classification) {
          echo "{$result->category} ({$result->confidence}): {$result->sentiment}\n";
      }
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      class Classification < Anthropic::BaseModel
        required :category, String
        required :confidence, Float
        required :tags, Anthropic::ArrayOf[String]
        required :sentiment, String
      end

      feedback_text = "Great product, fast shipping!"

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        output_config: {format: Classification},
        messages: [
          {role: "user", content: "Classify this feedback: #{feedback_text}"}
        ]
      )
      puts message.parsed_output
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Pemformatan respons API">
    Hasilkan respons siap-API:

    <CodeGroup>
      ```bash CLI
      ant messages create \
        --transform 'content.0.text' \
        --raw-output <<'YAML'
      model: claude-opus-4-8
      max_tokens: 1024
      output_config:
        format:
          type: json_schema
          schema:
            type: object
            properties:
              status:
                type: string
              data:
                type: object
                additionalProperties: false
              errors:
                type: array
                items:
                  type: object
                  additionalProperties: false
              metadata:
                type: object
                additionalProperties: false
            required:
              - status
              - data
              - metadata
            additionalProperties: false
      messages:
        - role: user
          content: "Process this request: ..."
      YAML
      ```

      ```python Python
      from pydantic import BaseModel

      client = Anthropic()


      class APIResponse(BaseModel):
          status: str
          data: dict
          errors: list[dict] | None
          metadata: dict


      response = client.messages.parse(
          model="claude-opus-4-8",
          max_tokens=1024,
          output_format=APIResponse,
          messages=[{"role": "user", "content": "Process this request: ..."}],
      )

      print(response.parsed_output)
      ```

      ```typescript TypeScript
      import { z } from "zod";
      import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

      const client = new Anthropic();

      const APIResponseSchema = z.object({
        status: z.string(),
        data: z.record(z.string(), z.any()),
        errors: z.array(z.record(z.string(), z.any())).optional(),
        metadata: z.record(z.string(), z.any())
      });

      const response = await client.messages.parse({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        output_config: { format: zodOutputFormat(APIResponseSchema) },
        messages: [{ role: "user", content: "Process this request..." }]
      });

      console.log(response.parsed_output);
      ```

      ```csharp C#
      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Process this request: ..." }],
          OutputConfig = new OutputConfig
          {
              Format = new JsonOutputFormat
              {
                  Schema = new Dictionary<string, JsonElement>
                  {
                      ["type"] = JsonSerializer.SerializeToElement("object"),
                      ["properties"] = JsonSerializer.SerializeToElement(new
                      {
                          status = new { type = "string" },
                          data = new { type = "object", additionalProperties = false },
                          errors = new
                          {
                              type = "array",
                              items = new { type = "object", additionalProperties = false },
                          },
                          metadata = new { type = "object", additionalProperties = false },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "status", "data", "metadata" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  },
              },
          },
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      client := anthropic.NewClient()

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 1024,
      	OutputConfig: anthropic.OutputConfigParam{
      		Format: anthropic.JSONOutputFormatParam{
      			Schema: map[string]any{
      				"type":                 "object",
      				"additionalProperties": false,
      				"properties": map[string]any{
      					"status": map[string]any{
      						"type": "string",
      					},
      					"data": map[string]any{
      						"type":                 "object",
      						"additionalProperties": false,
      					},
      					"errors": map[string]any{
      						"type": "array",
      						"items": map[string]any{
      							"type":                 "object",
      							"additionalProperties": false,
      						},
      					},
      					"metadata": map[string]any{
      						"type":                 "object",
      						"additionalProperties": false,
      					},
      				},
      				"required": []string{"status", "data", "metadata"},
      			},
      		},
      	},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("Process this request: ...")),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      for _, block := range response.Content {
      	switch variant := block.AsAny().(type) {
      	case anthropic.TextBlock:
      		fmt.Println(variant.Text)
      	}
      }
      ```

      ```java Java
      import com.fasterxml.jackson.annotation.JsonProperty;

      static class APIData {
          @JsonProperty("message")
          public String message;

          @JsonProperty("resource_id")
          public String resourceId;
      }

      static class APIError {
          @JsonProperty("code")
          public String code;

          @JsonProperty("message")
          public String message;
      }

      static class APIMetadata {
          @JsonProperty("request_id")
          public String requestId;

          @JsonProperty("timestamp")
          public String timestamp;
      }

      static class APIResponse {
          @JsonProperty("status")
          public String status;

          @JsonProperty("data")
          public APIData data;

          @JsonProperty("errors")
          public List<APIError> errors;

          @JsonProperty("metadata")
          public APIMetadata metadata;
      }

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          StructuredMessageCreateParams<APIResponse> params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .outputConfig(APIResponse.class)
              .addUserMessage("Process this request: ...")
              .build();

          StructuredMessage<APIResponse> response = client.messages().create(params);
          APIResponse result = response.content().stream()
              .flatMap(block -> block.text().stream())
              .findFirst().orElseThrow().text();
          IO.println(result.status);
      }
      ```

      ```php PHP
      use Anthropic\Lib\Attributes\Constrained;
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      $client = new Client();

      class Payload implements StructuredOutputModel { use StructuredOutputModelTrait; public string $message; }

      class APIError implements StructuredOutputModel { use StructuredOutputModelTrait; public string $code; public string $detail; }

      class Metadata implements StructuredOutputModel { use StructuredOutputModelTrait; public string $request_id; }

      class APIResponse implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          public string $status;
          public Payload $data;
          #[Constrained(itemClass: APIError::class)]
          public ?array $errors;
          public Metadata $metadata;
      }

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Process this request: ...']
          ],
          model: 'claude-opus-4-8',
          outputConfig: ['format' => APIResponse::class],
      );

      $result = $message->parsedOutput();
      if ($result instanceof APIResponse) {
          echo "{$result->status}: {$result->data->message}\n";
      }
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      class Payload < Anthropic::BaseModel
        required :message, String
      end

      class APIError < Anthropic::BaseModel
        required :code, String
        required :detail, String
      end

      class Metadata < Anthropic::BaseModel
        required :request_id, String
      end

      class APIResponse < Anthropic::BaseModel
        required :status, String
        required :data, Payload
        optional :errors, Anthropic::ArrayOf[APIError]
        required :metadata, Metadata
      end

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        output_config: {format: APIResponse},
        messages: [
          {role: "user", content: "Process this request: ..."}
        ]
      )
      puts message.parsed_output
      ```
    </CodeGroup>
  </Accordion>
</AccordionGroup>

## Penggunaan alat ketat

Untuk menegakkan kepatuhan JSON Schema pada input alat dengan sampling yang dibatasi grammar, lihat [Penggunaan alat ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use).

## Menggunakan kedua fitur bersamaan

Output JSON dan penggunaan alat ketat menyelesaikan masalah yang berbeda dan bekerja bersama:

* **Output JSON** mengontrol format respons Claude (apa yang dikatakan Claude)
* **Penggunaan alat ketat** memvalidasi parameter alat (bagaimana Claude memanggil fungsi Anda)

Ketika digabungkan, Claude dapat memanggil alat dengan parameter yang dijamin valid DAN mengembalikan respons JSON terstruktur. Ini berguna untuk alur kerja agentik di mana Anda memerlukan pemanggilan alat yang andal dan output akhir yang terstruktur.

<CodeGroup>
  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: Help me plan a trip to Paris departing May 15, 2026
  # Output JSON: format respons terstruktur
  output_config:
    format:
      type: json_schema
      schema:
        type: object
        properties:
          summary:
            type: string
          next_steps:
            type: array
            items:
              type: string
        required: [summary, next_steps]
        additionalProperties: false
  # Penggunaan alat yang ketat: parameter alat terjamin
  tools:
    - name: search_flights
      strict: true
      input_schema:
        type: object
        properties:
          destination:
            type: string
          date:
            type: string
            format: date
        required: [destination, date]
        additionalProperties: false
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Help me plan a trip to Paris departing May 15, 2026",
          }
      ],
      # Output JSON: format respons terstruktur
      output_config={
          "format": {
              "type": "json_schema",
              "schema": {
                  "type": "object",
                  "properties": {
                      "summary": {"type": "string"},
                      "next_steps": {"type": "array", "items": {"type": "string"}},
                  },
                  "required": ["summary", "next_steps"],
                  "additionalProperties": False,
              },
          }
      },
      # Penggunaan alat ketat: parameter alat terjamin
      tools=[
          {
              "name": "search_flights",
              "strict": True,
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "destination": {"type": "string"},
                      "date": {"type": "string", "format": "date"},
                  },
                  "required": ["destination", "date"],
                  "additionalProperties": False,
              },
          }
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Help me plan a trip to Paris departing May 15, 2026" }],
    // Output JSON: format respons terstruktur
    output_config: {
      format: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            summary: { type: "string" },
            next_steps: { type: "array", items: { type: "string" } }
          },
          required: ["summary", "next_steps"],
          additionalProperties: false
        }
      }
    },
    // Penggunaan alat ketat: parameter alat yang terjamin
    tools: [
      {
        name: "search_flights",
        description: "Search for available flights to a destination on a specific date",
        strict: true,
        input_schema: {
          type: "object",
          properties: {
            destination: { type: "string" },
            date: { type: "string", format: "date" }
          },
          required: ["destination", "date"],
          additionalProperties: false
        }
      }
    ]
  });

  // Claude mungkin memanggil alat terlebih dahulu (tool_use) atau merespons dengan JSON (text)
  console.log("Stop reason:", response.stop_reason);
  for (const block of response.content) {
    if (block.type === "tool_use") {
      console.log(`Tool call: ${block.name}(${JSON.stringify(block.input)})`);
    } else if (block.type === "text") {
      console.log("Response:", block.text);
    }
  }
  ```

  ```csharp C#
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Help me plan a trip to Paris departing May 15, 2026" }],
      // Output JSON: format respons terstruktur
      OutputConfig = new OutputConfig
      {
          Format = new JsonOutputFormat
          {
              Schema = new Dictionary<string, JsonElement>
              {
                  ["type"] = JsonSerializer.SerializeToElement("object"),
                  ["properties"] = JsonSerializer.SerializeToElement(new
                  {
                      summary = new { type = "string" },
                      next_steps = new { type = "array", items = new { type = "string" } },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(new[] { "summary", "next_steps" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              },
          },
      },
      // Penggunaan alat ketat: parameter alat yang terjamin
      Tools =
      [
          new Tool
          {
              Name = "search_flights",
              Strict = true,
              InputSchema = new InputSchema(new Dictionary<string, JsonElement>
              {
                  ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                  {
                      ["destination"] = new { type = "string" },
                      ["date"] = new { type = "string", format = "date" },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(new[] { "destination", "date" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              }),
          }
      ],
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
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Help me plan a trip to Paris departing May 15, 2026")),
  	},
  	// Output JSON: format respons terstruktur
  	OutputConfig: anthropic.OutputConfigParam{
  		Format: anthropic.JSONOutputFormatParam{
  			Schema: map[string]any{
  				"type":                 "object",
  				"additionalProperties": false,
  				"properties": map[string]any{
  					"summary":    map[string]any{"type": "string"},
  					"next_steps": map[string]any{"type": "array", "items": map[string]any{"type": "string"}},
  				},
  				"required": []string{"summary", "next_steps"},
  			},
  		},
  	},
  	// Penggunaan alat ketat: parameter alat terjamin
  	Tools: []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:   "search_flights",
  			Strict: anthropic.Bool(true),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"destination": map[string]any{"type": "string"},
  					"date":        map[string]any{"type": "string", "format": "date"},
  				},
  				Required: []string{"destination", "date"},
  				ExtraFields: map[string]any{
  					"additionalProperties": false,
  				},
  			}}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Output JSON: format respons terstruktur
  JsonOutputFormat.Schema outputSchema = JsonOutputFormat.Schema.builder()
      .putAdditionalProperty("type", JsonValue.from("object"))
      .putAdditionalProperty("properties", JsonValue.from(Map.of(
          "summary", Map.of("type", "string"),
          "next_steps", Map.of("type", "array", "items", Map.of("type", "string"))
      )))
      .putAdditionalProperty("required", JsonValue.from(List.of("summary", "next_steps")))
      .putAdditionalProperty("additionalProperties", JsonValue.from(false))
      .build();

  // Penggunaan alat ketat: parameter alat yang terjamin
  InputSchema toolSchema = InputSchema.builder()
      .properties(JsonValue.from(Map.of(
          "destination", Map.of("type", "string"),
          "date", Map.of("type", "string", "format", "date")
      )))
      .putAdditionalProperty("required", JsonValue.from(List.of("destination", "date")))
      .putAdditionalProperty("additionalProperties", JsonValue.from(false))
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addUserMessage("Help me plan a trip to Paris departing May 15, 2026")
      .outputConfig(OutputConfig.builder()
          .format(JsonOutputFormat.builder().schema(outputSchema).build())
          .build())
      .addTool(Tool.builder()
          .name("search_flights")
          .description("Search for available flights to a destination on a specific date")
          .strict(true)
          .inputSchema(toolSchema)
          .build())
      .build();

  Message response = client.messages().create(params);
  IO.println(response);
  ```

  ```php PHP
  use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
  use Anthropic\Lib\Contracts\StructuredOutputModel;
  use Anthropic\Messages\ToolUseBlock;

  $client = new Client();

  class TripPlan implements StructuredOutputModel
  {
      use StructuredOutputModelTrait;

      public string $summary;
      public array $next_steps;
  }

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Help me plan a trip to Paris departing May 15, 2026']
      ],
      model: 'claude-opus-4-8',
      // Output JSON: format respons terstruktur
      outputConfig: ['format' => TripPlan::class],
      // Penggunaan alat ketat: parameter alat terjamin
      tools: [
          [
              'name' => 'search_flights',
              'strict' => true,
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'destination' => ['type' => 'string'],
                      'date' => ['type' => 'string', 'format' => 'date']
                  ],
                  'required' => ['destination', 'date'],
                  'additionalProperties' => false
              ]
          ]
      ],
  );

  // Claude mungkin memanggil alat terlebih dahulu (tool_use) atau merespons dengan JSON (text)
  $plan = $message->parsedOutput();
  if ($plan instanceof TripPlan) {
      echo $plan->summary, "\n";
  } elseif ($toolUse = array_find($message->content, fn($block) => $block instanceof ToolUseBlock)) {
      echo "Tool call: {$toolUse->name}(", json_encode($toolUse->input), ")\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {role: "user", content: "Help me plan a trip to Paris departing May 15, 2026"}
    ],
    # Output JSON: format respons terstruktur
    output_config: {
      format: {
        type: :json_schema,
        schema: {
          type: "object",
          properties: {
            summary: {type: "string"},
            next_steps: {type: "array", items: {type: "string"}}
          },
          required: ["summary", "next_steps"],
          additionalProperties: false
        }
      }
    },
    # Penggunaan alat ketat: parameter alat yang terjamin
    tools: [
      {
        name: "search_flights",
        strict: true,
        input_schema: {
          type: "object",
          properties: {
            destination: {type: "string"},
            date: {type: "string", format: "date"}
          },
          required: ["destination", "date"],
          additionalProperties: false
        }
      }
    ]
  )
  puts message
  ```
</CodeGroup>

## Pertimbangan penting

### Kompilasi grammar dan caching

Output terstruktur menggunakan sampling terbatas dengan artefak grammar yang dikompilasi. Ini memperkenalkan beberapa karakteristik performa yang perlu diperhatikan:

* **Latensi permintaan pertama:** Pertama kali Anda menggunakan skema tertentu, ada latensi tambahan saat grammar dikompilasi

* **Caching otomatis:** Grammar yang dikompilasi di-cache selama 24 jam sejak penggunaan terakhir, membuat permintaan berikutnya jauh lebih cepat

* **Invalidasi cache:** Cache diinvalidasi jika Anda mengubah:

  * Struktur skema JSON
  * Kumpulan alat dalam permintaan Anda (saat menggunakan output terstruktur dan penggunaan alat bersamaan)
  * Mengubah hanya field `name` atau `description` tidak menginvalidasi cache

### Modifikasi prompt dan biaya token

Saat menggunakan output terstruktur, Claude secara otomatis menerima prompt sistem tambahan yang menjelaskan format output yang diharapkan. Ini berarti:

* Jumlah token input Anda sedikit lebih tinggi
* Prompt yang disuntikkan dikenakan biaya token seperti prompt sistem lainnya
* Mengubah parameter `output_config.format` akan menginvalidasi [cache prompt](/docs/id/build-with-claude/prompt-caching) apa pun untuk thread percakapan tersebut

### Batasan JSON Schema

Output terstruktur mendukung JSON Schema standar dengan beberapa batasan. Baik output JSON maupun penggunaan alat ketat berbagi batasan ini.

<Accordion title="Fitur yang didukung">
  * Semua tipe dasar: object, array, string, integer, number, boolean, null
  * `enum` (hanya string, number, bool, atau null - tidak ada tipe kompleks)
  * `const`
  * `anyOf` dan `allOf` (dengan batasan - `allOf` dengan `$ref` tidak didukung)
  * `$ref`, `$def`, dan `definitions` (`$ref` eksternal tidak didukung)
  * Properti `default` untuk semua tipe yang didukung
  * `required` dan `additionalProperties` (harus diatur ke `false` untuk objek)
  * Format string: `date-time`, `time`, `date`, `duration`, `email`, `hostname`, `uri`, `ipv4`, `ipv6`, `uuid`
  * Array `minItems` (hanya nilai 0 dan 1 yang didukung)
</Accordion>

<Accordion title="Tidak didukung">
  * Skema rekursif
  * Tipe kompleks dalam enum
  * `$ref` eksternal (misalnya, `'$ref': 'http://...'`)
  * Constraint numerik (seperti `minimum`, `maximum`, `multipleOf`)
  * Constraint string (`minLength`, `maxLength`)
  * Constraint array selain `minItems` 0 atau 1
  * `additionalProperties` diatur ke apa pun selain `false`

  Jika Anda menggunakan fitur yang tidak didukung, Anda akan menerima kesalahan 400 dengan detail.
</Accordion>

<Accordion title="Dukungan pattern (regex)">
  **Fitur regex yang didukung:**

  * Pencocokan penuh (`^...$`) dan pencocokan parsial
  * Quantifier: `*`, `+`, `?`, kasus `{n,m}` sederhana
  * Kelas karakter: `[]`, `.`, `\d`, `\w`, `\s`
  * Grup: `(...)`

  **TIDAK didukung:**

  * Backreference ke grup (misalnya, `\1`, `\2`)
  * Assertion lookahead/lookbehind (misalnya, `(?=...)`, `(?!...)`)
  * Batas kata: `\b`, `\B`
  * Quantifier `{n,m}` kompleks dengan rentang besar

  Pola regex sederhana berfungsi dengan baik. Pola kompleks dapat menghasilkan kesalahan 400.
</Accordion>

<Tip>
  SDK Python, TypeScript, Ruby, dan PHP dapat secara otomatis mentransformasi skema dengan fitur yang tidak didukung dengan menghapusnya dan menambahkan constraint ke deskripsi field. SDK C# dan Go melakukan hal yang sama ketika skema diturunkan dari tipe native. Lihat [Metode khusus SDK](#sdk-specific-methods) untuk detail.
</Tip>

### Pengurutan properti

Saat menggunakan output terstruktur, properti dalam objek mempertahankan urutan yang didefinisikan dari skema Anda, dengan satu peringatan penting: **properti wajib muncul terlebih dahulu, diikuti oleh properti opsional**.

Misalnya, dengan skema ini:

```json
{
  "type": "object",
  "properties": {
    "notes": { "type": "string" },
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "email"],
  "additionalProperties": false
}
```

Output akan mengurutkan properti sebagai:

1. `name` (wajib, sesuai urutan skema)
2. `email` (wajib, sesuai urutan skema)
3. `notes` (opsional, sesuai urutan skema)
4. `age` (opsional, sesuai urutan skema)

Ini berarti output mungkin terlihat seperti:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "notes": "Interested in enterprise plan",
  "age": 35
}
```

Jika urutan properti dalam output penting untuk aplikasi Anda, tandai semua properti sebagai wajib, atau perhitungkan pengurutan ulang ini dalam logika parsing Anda.

### Output tidak valid

Meskipun output terstruktur menjamin kepatuhan skema dalam sebagian besar kasus, ada skenario di mana output mungkin tidak cocok dengan skema Anda:

**Penolakan** (`stop_reason: "refusal"`)

Claude mempertahankan properti keamanan dan kebermanfaatannya bahkan saat menggunakan output terstruktur. Jika Claude menolak permintaan karena alasan keamanan:

* Respons memiliki `stop_reason: "refusal"`
* Anda akan menerima kode status 200
* Anda akan ditagih untuk token yang dihasilkan
* Output mungkin tidak cocok dengan skema Anda karena pesan penolakan lebih diutamakan daripada constraint skema

**Batas token tercapai** (`stop_reason: "max_tokens"`)

Jika respons terpotong karena mencapai batas `max_tokens`:

* Respons memiliki `stop_reason: "max_tokens"`
* Output mungkin tidak lengkap dan tidak cocok dengan skema Anda
* Coba lagi dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan output terstruktur yang lengkap

### Batas kompleksitas skema

Output terstruktur bekerja dengan mengompilasi skema JSON Anda menjadi grammar yang membatasi output Claude. Skema yang lebih kompleks menghasilkan grammar yang lebih besar yang membutuhkan waktu lebih lama untuk dikompilasi. Untuk melindungi dari waktu kompilasi yang berlebihan, API menegakkan beberapa batas kompleksitas.

#### Batas eksplisit

Batas berikut berlaku untuk semua permintaan dengan `output_config.format` atau `strict: true`:

| Batas                       | Nilai | Deskripsi                                                                                                                                                                                 |
| --------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Alat ketat per permintaan   | 20    | Jumlah maksimum alat dengan `strict: true`. Alat non-ketat tidak dihitung terhadap batas ini.                                                                                             |
| Parameter opsional          | 24    | Total parameter opsional di semua skema alat ketat dan skema output JSON. Setiap parameter yang tidak tercantum dalam `required` dihitung terhadap batas ini.                             |
| Parameter dengan tipe union | 16    | Total parameter yang menggunakan `anyOf` atau array tipe (misalnya, `"type": ["string", "null"]`) di semua skema ketat. Ini sangat mahal karena menciptakan biaya kompilasi eksponensial. |

<Note>
  Batas ini berlaku untuk total gabungan di semua skema ketat dalam satu permintaan. Misalnya, jika Anda memiliki 4 alat ketat dengan masing-masing 6 parameter opsional, Anda akan mencapai batas 24 parameter meskipun tidak ada satu alat pun yang tampak kompleks.
</Note>

#### Batas internal tambahan

Di luar batas eksplisit dalam tabel sebelumnya, ada batas internal tambahan pada ukuran grammar yang dikompilasi. Batas ini ada karena kompleksitas skema tidak dapat direduksi menjadi satu dimensi: fitur seperti parameter opsional, tipe union, objek bersarang, dan jumlah alat berinteraksi satu sama lain dengan cara yang dapat membuat grammar yang dikompilasi menjadi sangat besar secara tidak proporsional.

Ketika batas ini terlampaui, Anda akan menerima kesalahan 400 dengan pesan "Schema is too complex for compilation." Kesalahan ini berarti kompleksitas gabungan skema Anda melebihi apa yang dapat dikompilasi secara efisien, bahkan jika setiap batas individual dalam tabel sebelumnya terpenuhi. Sebagai pengaman terakhir, API juga menegakkan **batas waktu kompilasi 180 detik**. Skema yang lolos semua pemeriksaan eksplisit tetapi menghasilkan grammar terkompilasi yang sangat besar mungkin mencapai batas waktu ini.

#### Tips untuk mengurangi kompleksitas skema

Jika Anda mencapai batas kompleksitas, coba strategi ini secara berurutan:

1. **Tandai hanya alat kritis sebagai ketat.** Jika Anda memiliki banyak alat, simpan untuk alat di mana pelanggaran skema menyebabkan masalah nyata, dan andalkan kepatuhan alami Claude untuk alat yang lebih sederhana.

2. **Kurangi parameter opsional.** Buat parameter `required` jika memungkinkan. Setiap parameter opsional kira-kira menggandakan sebagian dari ruang state grammar. Jika parameter selalu memiliki default yang masuk akal, pertimbangkan untuk membuatnya wajib dan meminta Claude memberikan default tersebut secara eksplisit.

3. **Sederhanakan struktur bersarang.** Objek bersarang dalam dengan field opsional memperparah kompleksitas. Ratakan struktur jika memungkinkan.

4. **Pisahkan menjadi beberapa permintaan.** Jika Anda memiliki banyak alat ketat, pertimbangkan untuk memisahkannya ke permintaan atau sub-agen terpisah.

Untuk masalah yang terus berlanjut dengan skema yang valid, [hubungi dukungan](https://support.claude.com/en/articles/9015913-how-to-get-support) dengan definisi skema Anda.

## Retensi data

Prompt dan respons diproses dengan ZDR saat menggunakan output terstruktur. Namun, skema JSON itu sendiri di-cache sementara hingga 24 jam sejak penggunaan terakhir untuk tujuan optimasi. Tidak ada data prompt atau respons yang disimpan di luar respons API.

Output terstruktur memenuhi syarat HIPAA, tetapi **PHI tidak boleh disertakan dalam definisi skema JSON**. API mengompilasi skema JSON menjadi grammar yang di-cache secara terpisah dari konten pesan, dan skema yang di-cache ini tidak menerima perlindungan PHI yang sama seperti prompt dan respons. Jangan sertakan PHI dalam nama properti skema, nilai `enum`, nilai `const`, atau ekspresi reguler `pattern`. PHI hanya boleh muncul dalam konten pesan (prompt dan respons), di mana PHI dilindungi di bawah pengamanan HIPAA.

Untuk kelayakan ZDR dan HIPAA di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Kompatibilitas fitur

**Berfungsi dengan:**

* **[Pemrosesan batch](/docs/id/build-with-claude/batch-processing):** Proses output terstruktur dalam skala besar dengan diskon 50%
* **[Penghitungan token](/docs/id/build-with-claude/token-counting):** Hitung token tanpa kompilasi
* **[Streaming](/docs/id/build-with-claude/streaming):** Stream output terstruktur seperti respons normal
* **Penggunaan gabungan:** Gunakan output JSON (`output_config.format`) dan penggunaan alat ketat (`strict: true`) bersamaan dalam permintaan yang sama

**Tidak kompatibel dengan:**

* **[Sitasi](/docs/id/build-with-claude/citations):** Sitasi memerlukan penyisipan blok sitasi dengan teks, yang bertentangan dengan constraint skema JSON yang ketat. Mengembalikan kesalahan 400 jika sitasi diaktifkan dengan `output_config.format`.
* **Prefilling Pesan:** Tidak kompatibel dengan output JSON

<Tip>
  **Cakupan grammar:** Grammar hanya berlaku untuk output langsung Claude, bukan untuk pemanggilan penggunaan alat, hasil alat, atau tag thinking (saat menggunakan [Pemikiran Diperpanjang](/docs/id/build-with-claude/extended-thinking)). State grammar direset di antara bagian, memungkinkan Claude berpikir dengan bebas sambil tetap menghasilkan output terstruktur dalam respons akhir.
</Tip>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Sitasi" icon="book-bookmark" href="/docs/id/build-with-claude/citations">
    Minta Claude mengutip sumbernya saat menjawab pertanyaan tentang dokumen yang disediakan.
  </Card>

  <Card title="Penggunaan alat ketat" icon="check" href="/docs/id/agents-and-tools/tool-use/strict-tool-use">
    Tegakkan kepatuhan JSON Schema pada input alat Claude dengan sampling yang dibatasi grammar.
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="wrench" href="/docs/id/agents-and-tools/tool-use/overview">
    Hubungkan Claude ke alat dan API eksternal. Pelajari di mana alat dieksekusi dan bagaimana loop agentik bekerja.
  </Card>

  <Card title="Harga" icon="calculator" href="/docs/id/about-claude/pricing">
    Pelajari tentang struktur harga Anthropic untuk model dan fitur.
  </Card>
</CardGroup>
