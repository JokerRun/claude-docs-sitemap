---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/structured-outputs
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 918296521ca9bcf84bf22b0005f01d4515bbad0e527dd8dc4a9de4435fc98204
---

---
title: Output terstruktur
url: https://platform.claude.com/docs/id/build-with-claude/structured-outputs
description: Dapatkan hasil JSON yang tervalidasi dari alur kerja agen
featureMetadata:
  status: stable
  zdr:
    eligibility: qualified
    note: "Excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements). Prompt Anda dan output Claude tidak disimpan. Hanya JSON schema yang di-cache, hingga 24 jam sejak terakhir digunakan. Ini juga mencakup penggunaan alat ketat (`strict: true` pada alat), yang menggunakan pipeline grammar yang sama."
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
    Amazon Bedrock: stable
    Amazon Bedrock (InvokeModel): stable
    Claude Models on Google Cloud (Google managed): stable
    Microsoft Foundry: stable
---

“Structured outputs” (output terstruktur) membatasi respons Claude agar mengikuti skema tertentu, sehingga memastikan output yang valid dan dapat di-parse untuk pemrosesan hilir. Output terstruktur menyediakan dua fitur yang saling melengkapi:

* **Output JSON** (`output_config.format`): Dapatkan respons Claude dalam format JSON tertentu, misalnya untuk mengekstrak data dari gambar atau teks, menghasilkan laporan terstruktur, atau memformat respons API. Halaman ini membahas output JSON.
* **Penggunaan alat ketat** (`strict: true`): Menjamin validasi skema pada nama dan input alat. Lihat [Penggunaan alat ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use).

Anda dapat menggunakan fitur-fitur ini secara terpisah atau [bersama-sama dalam permintaan yang sama](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#using-both-features-together).

## Mengapa menggunakan output terstruktur

Tanpa output terstruktur, Claude dapat menghasilkan respons JSON yang salah format atau input alat yang tidak valid yang merusak aplikasi Anda. Bahkan dengan prompting yang cermat, Anda mungkin menemui:

* Kesalahan parsing akibat sintaks JSON yang tidak valid
* Bidang wajib yang hilang
* Tipe data yang tidak konsisten
* Pelanggaran skema yang memerlukan penanganan kesalahan dan percobaan ulang

Output terstruktur menjamin respons yang sesuai skema melalui “constrained decoding” (dekode terbatas):

* **Selalu valid:** Tidak ada lagi kesalahan `JSON.parse()`
* **Aman tipe:** Tipe bidang dan bidang wajib terjamin
* **Andal:** Tidak perlu percobaan ulang karena pelanggaran skema

## Cara kerjanya

<Steps>
  <Step title="Definisikan skema Anda">
    Jelaskan struktur yang Anda inginkan sebagai JSON schema atau sebagai tipe dalam bahasa pemrograman Anda. Skema mengikuti JSON Schema, dengan beberapa [batasan](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations).
  </Step>

  <Step title="Kirim dalam output_config.format">
    Permintaan membawa skema dalam `output_config.format` dengan `type: "json_schema"`. Helper SDK mengaturnya untuk Anda.
  </Step>

  <Step title="Baca respons">
    Claude mengembalikan JSON valid yang cocok dengan skema Anda di blok konten teks respons. Helper SDK mem-parse-nya ke dalam tipe Anda.
  </Step>
</Steps>

## Penggunaan

<Tabs>
  <Tab title="cURL">
    ```bash
    curl https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "claude-opus-5-5",
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

    Claude mengembalikan JSON seperti ini di blok konten teks respons:

    ```json Output
    {
      "name": "John Smith",
      "email": "john@example.com",
      "plan_interest": "Enterprise",
      "demo_requested": true
    }
    ```
  </Tab>

  <Tab title="CLI">
    ```bash
    ant messages create <<'YAML'
    model: claude-opus-5-5
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

    Claude mengembalikan JSON seperti ini di blok konten teks respons:

    ```json Output
    {
      "name": "John Smith",
      "email": "john@example.com",
      "plan_interest": "Enterprise",
      "demo_requested": true
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python
    from pydantic import BaseModel
    # ...


    class ContactInfo(BaseModel):
        name: str
        email: str
        plan_interest: str
        demo_requested: bool


    client = Anthropic()

    response = client.messages.parse(
        model="claude-opus-5-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Extract the key information from this email: "
                    "John Smith (john@example.com) is interested in our Enterprise plan "
                    "and wants to schedule a demo for next Tuesday at 2pm."
                ),
            }
        ],
        output_format=ContactInfo,
    )

    print(response.parsed_output)
    ```

    Berikan model [Pydantic](https://docs.pydantic.dev/) ke `client.messages.parse()`, metode yang direkomendasikan, sebagai `output_format`. SDK mentransformasi skema model, mengirimkannya sebagai `output_config.format`, memvalidasi respons, dan mengembalikan model yang telah di-parse dalam `parsed_output`.

    Contoh sebelumnya menghasilkan output:

    ```text Output wrap
    name='John Smith' email='john@example.com' plan_interest='Enterprise' demo_requested=True
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
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
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content:
            "Extract the key information from this email: " +
            "John Smith (john@example.com) is interested in our Enterprise plan " +
            "and wants to schedule a demo for next Tuesday at 2pm."
        }
      ],
      output_config: { format: zodOutputFormat(ContactInfoSchema) }
    });

    // Diurai dan divalidasi secara otomatis
    console.log(response.parsed_output);
    ```

    Bungkus skema [Zod](https://zod.dev/) dalam `zodOutputFormat()` dan berikan ke `client.messages.parse()` sebagai `output_config.format`. `zodOutputFormat()` mentransformasi skema, dan `parse()` memvalidasi respons serta mengembalikan hasil yang telah di-parse dalam `parsed_output`, dengan tipe yang sesuai dengan skema.

    Contoh sebelumnya menghasilkan output:

    ```javascript Output
    {
      name: 'John Smith',
      email: 'john@example.com',
      plan_interest: 'Enterprise',
      demo_requested: true
    }
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using Anthropic;
    using Anthropic.Models.Messages;
    using Anthropic.Services;

    var client = new AnthropicClient();

    var response = await client.Messages.Create<ContactInfo>(new MessageCreateParams
    {
        Model = Model.ClaudeOpus5_5,
        MaxTokens = 1024,
        Messages = [
            new UserMessageParam
            {
                Content = "Extract the key information from this email: "
                    + "John Smith (john@example.com) is interested in our Enterprise plan "
                    + "and wants to schedule a demo for next Tuesday at 2pm."
            }
        ],
    });

    if (response.Content.Select(block => block.Parsed()).OfType<ContactInfo>().FirstOrDefault() is { } contact)
    {
        Console.WriteLine(contact);
    }

    public record ContactInfo
    {
        public string Name { get; set; } = "";
        public string Email { get; set; } = "";
        public string PlanInterest { get; set; } = "";
        public bool DemoRequested { get; set; }
    }
    ```

    Berikan class atau record C# biasa ke overload generik `Create<T>()`. SDK menurunkan JSON schema dari tipe tersebut, mentransformasinya, dan mem-parse setiap blok teks kembali ke dalamnya.

    Contoh sebelumnya menghasilkan output:

    ```text Output wrap
    ContactInfo { Name = John Smith, Email = john@example.com, PlanInterest = Enterprise, DemoRequested = True }
    ```
  </Tab>

  <Tab title="Go">
    ```go
    type ContactInfo struct {
    	Name          string `json:"name"`
    	Email         string `json:"email"`
    	PlanInterest  string `json:"plan_interest"`
    	DemoRequested bool   `json:"demo_requested"`
    }

    func main() {
    	client := anthropic.NewClient()

    	var contact ContactInfo
    	_, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
    		Model:     anthropic.ModelClaudeOpus5_5,
    		MaxTokens: 1024,
    		Messages: []anthropic.BetaMessageParam{
    			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(
    				"Extract the key information from this email: " +
    					"John Smith (john@example.com) is interested in our Enterprise plan " +
    					"and wants to schedule a demo for next Tuesday at 2pm.",
    			)),
    		},
    		OutputConfig: anthropic.BetaOutputConfigParam{
    			Format: anthropic.BetaJSONOutputFormatParam{Schema: &contact},
    		},
    	})
    	if err != nil {
    		panic(err)
    	}

    	fmt.Printf("%#v\n", contact)
    }
    ```

    <Note>
      Memberikan struct sebagai skema masih dalam beta di Go, sehingga contoh ini menggunakan `client.Beta.Messages.New`. Untuk menggunakan `client.Messages.New` yang stabil, berikan JSON schema seperti yang ditunjukkan dalam [Menggunakan JSON schema mentah](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#using-a-raw-json-schema).
    </Note>

    SDK menghasilkan dan mentransformasi JSON schema dari struct dan melakukan unmarshal respons ke dalamnya.

    Contoh sebelumnya menghasilkan output:

    ```text Output wrap
    main.ContactInfo{Name:"John Smith", Email:"john@example.com", PlanInterest:"Enterprise", DemoRequested:true}
    ```
  </Tab>

  <Tab title="Java">
    ```java
    static class ContactInfo {
        public String name;
        public String email;
        public String plan_interest;
        public boolean demo_requested;
    }

    void main() throws Exception {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        StructuredMessageCreateParams<ContactInfo> params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_5_5)
            .maxTokens(1024)
            .addUserMessage("Extract the key information from this email: "
                + "John Smith (john@example.com) is interested in our Enterprise plan "
                + "and wants to schedule a demo for next Tuesday at 2pm.")
            .outputConfig(ContactInfo.class)
            .build();

        StructuredMessage<ContactInfo> response = client.messages().create(params);
        ContactInfo contact = response.content().stream()
            .flatMap(block -> block.text().stream())
            .findFirst().orElseThrow().text();
        IO.println(new ObjectMapper().writeValueAsString(contact));
    }
    ```

    Saat Anda memberikan class Java ke `outputConfig()`, SDK menurunkan JSON schema darinya dan memvalidasi skema tersebut. Builder kemudian menghasilkan `StructuredMessageCreateParams<T>`. Alih-alih mentransformasi skema, validasi lokal SDK menolak [batasan yang tidak didukung oleh API](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations). Baca hasil yang telah di-parse dengan `response.content().stream().flatMap(block -> block.text().stream()).findFirst().orElseThrow().text()`.

    Contoh sebelumnya menghasilkan output:

    ```json Output
    {"name":"John Smith","email":"john@example.com","plan_interest":"Enterprise","demo_requested":true}
    ```

    <Note>
      Deklarasikan class skema Anda sebagai class tingkat atas atau class bersarang `static`. Persyaratan ini berasal dari library Jackson Databind (`com.fasterxml.jackson.databind`), yang digunakan SDK untuk melakukan deserialisasi respons JSON ke dalam instance class Anda dan tidak dapat membuat instance dari inner class non-static.
    </Note>

    <Accordion title="Penghapusan tipe generik">
      Java menyimpan informasi tipe generik untuk bidang dalam metadata class, tetapi “generic type erasure” (penghapusan tipe generik) berlaku dalam cakupan lain. Meskipun JSON schema dapat diturunkan dari bidang `BookList.books` dengan tipe `List<Book>`, JSON schema yang valid tidak dapat diturunkan dari variabel lokal dengan tipe yang sama.

      Jika terjadi kesalahan saat mengonversi respons JSON ke instance class Java, pesan kesalahan menyertakan respons JSON untuk membantu diagnosis. Jika respons JSON Anda mungkin berisi informasi sensitif, hindari mencatatnya secara langsung, atau pastikan Anda menyamarkan detail sensitif apa pun dari pesan kesalahan.
    </Accordion>

    <Accordion title="Validasi skema lokal">
      Output terstruktur mendukung [subset dari bahasa JSON Schema](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations). SDK menghasilkan skema secara otomatis dari class agar selaras dengan subset ini. Metode `outputConfig(Class<T>)` melakukan pemeriksaan validasi pada skema yang diturunkan dari class yang ditentukan.

      Poin-poin utama:

      * **Validasi lokal** terjadi tanpa mengirim permintaan ke model AI jarak jauh.
      * **Validasi jarak jauh** juga dilakukan oleh model AI saat menerima JSON schema.
      * **Kompatibilitas versi:** Jika versi SDK sudah usang, validasi lokal mungkin menolak skema yang diterima oleh validasi jarak jauh.
      * **Menonaktifkan validasi lokal:** Berikan `JsonSchemaLocalValidation.NO` jika Anda mengalami masalah kompatibilitas:

      ```java
      import com.anthropic.core.JsonSchemaLocalValidation;
      // ...

      static class BookList {
          public List<String> books;
      }

      void main() {
          StructuredMessageCreateParams<BookList> createParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(2048)
              .outputConfig(BookList.class, JsonSchemaLocalValidation.NO)
              .addUserMessage("List some famous late twentieth century novels.")
              .build();
      }
      ```
    </Accordion>

    <Accordion title="Streaming">
      Output terstruktur juga berfungsi dengan streaming. Karena respons tiba dalam event stream, Anda perlu mengakumulasi respons lengkap sebelum melakukan deserialisasi JSON.

      Gunakan `MessageAccumulator` untuk mengumpulkan string JSON dari stream. Setelah terakumulasi, panggil `MessageAccumulator.message(Class<T>)` untuk mengonversi `Message` yang terakumulasi menjadi `StructuredMessage`, yang secara otomatis melakukan deserialisasi JSON ke dalam class Java Anda.
    </Accordion>

    <Accordion title="Properti JSON schema">
      Saat SDK menurunkan JSON schema dari class Java Anda, secara default SDK menyertakan semua properti yang direpresentasikan oleh bidang `public` atau metode getter `public` dan mengecualikan bidang dan metode getter non-`public`.

      Anda dapat mengontrol visibilitas dengan anotasi:

      * `@JsonIgnore` mengecualikan bidang atau metode getter `public`.
      * `@JsonProperty` menyertakan bidang atau metode getter non-`public`.

      Jika Anda mendefinisikan bidang `private` dengan metode getter `public`, SDK menurunkan nama properti dari getter (misalnya, bidang `private` `myValue` dengan metode `public` `getMyValue()` menghasilkan properti `"myValue"`). Untuk menggunakan nama getter yang tidak konvensional, beri anotasi `@JsonProperty` pada metode tersebut.

      Setiap class harus mendefinisikan setidaknya satu properti untuk JSON schema. Kesalahan validasi terjadi jika tidak ada bidang atau metode getter yang dapat menghasilkan properti skema, seperti ketika:

      * Tidak ada bidang atau metode getter dalam class
      * Semua anggota `public` diberi anotasi `@JsonIgnore`
      * Semua anggota non-`public` tidak memiliki anotasi `@JsonProperty`
      * Sebuah bidang menggunakan tipe `Map`, yang menghasilkan bidang `"properties"` kosong
    </Accordion>

    <Accordion title="Komposisi dan pewarisan">
      Class Java Anda dapat menggunakan komposisi dan pewarisan untuk berbagi struktur saat mendefinisikan JSON schema. Setiap pola memengaruhi struktur output secara berbeda.

      **Komposisi** menghasilkan output JSON bersarang. Menurunkan skema dari class `Composed` yang mengomposisikan `A` dan `B`:

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

      ```json Output
      {
        "composedA": { "a": "hello" },
        "composedB": { "b": "world" }
      }
      ```

      **Pewarisan** menghasilkan output JSON datar. Menurunkan skema dari class `Derived` yang memperluas `Base`:

      ```java
      static class Base {
          public String a;
      }

      static class Derived extends Base {
          public String b;
      }
      ```

      Output JSON memiliki struktur datar ini:

      ```json Output
      {
        "a": "hello",
        "b": "world"
      }
      ```
    </Accordion>

    <Accordion title="Anotasi (Jackson dan Swagger)">
      Anda dapat menggunakan anotasi Jackson Databind untuk memperkaya JSON schema yang diturunkan dari class Java Anda:

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

      * `@JsonClassDescription`: Menambahkan deskripsi ke class
      * `@JsonPropertyDescription`: Menambahkan deskripsi ke bidang atau metode getter
      * `@JsonIgnore`: Mengecualikan bidang atau getter `public` dari skema
      * `@JsonProperty`: Menyertakan bidang atau getter non-`public` dalam skema

      Jika Anda menggunakan `@JsonProperty(required = false)`, SDK mengabaikan nilai `false`. Skema yang diturunkan dari class selalu menandai semua properti sebagai wajib.

      Anda juga dapat menggunakan anotasi `@Schema` dan `@ArraySchema` dari Swagger Core (OpenAPI 3) untuk batasan khusus tipe:

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

      Validasi lokal memeriksa bahwa Anda tidak menggunakan kata kunci batasan yang tidak didukung, tetapi nilai batasan tidak divalidasi secara lokal. Misalnya, nilai `"format"` yang tidak didukung mungkin lolos validasi lokal tetapi menyebabkan kesalahan jarak jauh.

      Jika Anda menggunakan anotasi Jackson dan Swagger untuk mengatur bidang skema yang sama, anotasi Jackson yang diutamakan.
    </Accordion>
  </Tab>

  <Tab title="PHP">
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
        public bool $demo_requested;
    }

    $message = $client->messages->create(
        maxTokens: 1024,
        messages: [
            [
                'role' => 'user',
                'content' => 'Extract the key information from this email: '
                    . 'John Smith (john@example.com) is interested in our Enterprise plan '
                    . 'and wants to schedule a demo for next Tuesday at 2pm.',
            ],
        ],
        model: 'claude-opus-5-5',
        outputConfig: ['format' => ContactInfo::class],
    );

    $contact = $message->parsedOutput();
    if ($contact instanceof ContactInfo) {
        var_dump($contact);
    }
    ```

    Definisikan class yang mengimplementasikan `StructuredOutputModel` dan menggunakan `StructuredOutputModelTrait`, lalu berikan namanya dalam `outputConfig: ['format' => MyClass::class]`. SDK menurunkan JSON schema dari tipe properti PHP 8 class tersebut, mentransformasinya, dan mengembalikan instance bertipe dari `$message->parsedOutput()`.

    `parsedOutput()` mengembalikan instance model Anda jika berhasil, atau `null` (atau array kesalahan) jika parsing gagal. Gunakan `instanceof` untuk mempersempit tipe sebelum mengakses bidang.

    Contoh sebelumnya menghasilkan output:

    ```text Output wrap
    object(ContactInfo)#42 (4) {
      ["name"]=>
      string(10) "John Smith"
      ["email"]=>
      string(16) "john@example.com"
      ["plan_interest"]=>
      string(10) "Enterprise"
      ["demo_requested"]=>
      bool(true)
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
      | `?type` (nullable)                                     | Bidang opsional                   |
      | Class yang mengimplementasikan `StructuredOutputModel` | Objek bersarang                   |

      Untuk properti `array`, SDK menambahkan skema `items` hanya ketika tipe elemennya adalah `StructuredOutputModel` bersarang, yang dideklarasikan dengan `#[Constrained(itemClass: MyModel::class)]` atau docblock `/** @var MyModel[] */`. Array skalar (`string[]`, `int[]`) menghasilkan `{"type":"array"}` tanpa batasan.

      Semua properti non-nullable menjadi bidang wajib.
    </Accordion>

    <Accordion title="Batasan dengan atribut #[Constrained]">
      Tambahkan batasan dengan atribut `#[Constrained]`:

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

      **Batasan yang ditegakkan API** (dikirim dalam skema): `description`, `format`, `const`, `itemClass`, `minItems` (hanya 0 atau 1).

      **Batasan yang divalidasi SDK** (dihapus dari skema yang dikirim, ditambahkan ke deskripsi, dan divalidasi terhadap respons): `minimum`, `maximum`, `multipleOf`, `minLength`, `maxLength`.
    </Accordion>
  </Tab>

  <Tab title="Ruby">
    ```ruby
    client = Anthropic::Client.new

    class ContactInfo < Anthropic::BaseModel
      required :name, String
      required :email, String
      required :plan_interest, String
      required :demo_requested, Anthropic::Boolean
    end

    message = client.messages.create(
      model: Anthropic::Model::CLAUDE_OPUS_5_5,
      max_tokens: 1024,
      messages: [{
        role: "user",
        content: "Extract the key information from this email: " \
          "John Smith (john@example.com) is interested in our Enterprise plan " \
          "and wants to schedule a demo for next Tuesday at 2pm."
      }],
      output_config: {format: ContactInfo}
    )

    contact = message.parsed_output
    puts contact
    ```

    Definisikan class yang memperluas `Anthropic::BaseModel` dan berikan ke `messages.create()` sebagai `output_config: {format: Model}`. SDK menurunkan JSON schema dari class tersebut, mentransformasinya, dan menetapkan hasil yang telah di-parse ke atribut `parsed_output` respons sebagai objek Ruby bertipe.

    Contoh sebelumnya menghasilkan output:

    ```text Output wrap
    {name: "John Smith", email: "john@example.com", plan_interest: "Enterprise", demo_requested: true}
    ```

    <Accordion title="Fitur model lanjutan">
      Ruby SDK mendukung fitur definisi model tambahan untuk skema yang lebih kaya:

      * **Kata kunci `doc:`:** Menambahkan deskripsi ke bidang untuk output skema yang lebih informatif
      * **`Anthropic::ArrayOf[T]`:** Array bertipe. Berikan batasan tingkat array (`min_items:`, `max_items:`) sebagai kata kunci pada `required`/`optional`, bukan pada `ArrayOf` itu sendiri
      * **`Anthropic::EnumOf[:a, :b]`:** Bidang enum dengan nilai terbatas
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
        model: Anthropic::Model::CLAUDE_OPUS_5_5,
        max_tokens: 1024,
        messages: [{role: "user", content: "give me some famous numbers"}],
        output_config: {format: Output}
      )

      message.parsed_output
      # => #<Output numbers=[#<FamousNumber value=3.14159... reason="Pi is...">...]>
      ```
    </Accordion>
  </Tab>
</Tabs>

## Cara kerja transformasi SDK

Sebagian besar helper SDK mentransformasi skema yang menggunakan fitur yang tidak didukung. Langkah-langkah transformasinya:

1. **Menghapus batasan yang tidak didukung** (misalnya, `minimum`, `maximum`, `minLength`, `maxLength`)
2. **Memperbarui deskripsi** dengan menambahkan setiap batasan yang tidak didukung ke deskripsi bidang (misalnya, `{minimum: 100}`)
3. **Menambahkan `additionalProperties: false`** ke semua objek
4. **Memfilter format string** hanya ke daftar yang didukung
5. **Memvalidasi respons** terhadap skema asli Anda dan semua batasannya, jika helper memvalidasi respons

Claude menerima skema yang disederhanakan, tetapi helper yang memvalidasi respons tetap menegakkan setiap batasan dalam kode Anda.

**Contoh:** Bidang dengan `minimum: 100` menjadi integer biasa dalam skema yang dikirim, dan SDK menambahkan `{minimum: 100}` ke deskripsi bidang. Helper yang memvalidasi respons tetap memeriksa respons terhadap `minimum: 100`.

## Menggunakan JSON schema mentah

Untuk menggunakan JSON schema dari file, spesifikasi OpenAPI, atau kode yang membangunnya saat runtime, berikan skema tersebut dalam `output_config.format`.

<Tabs>
  <Tab title="cURL">
    ```bash
    curl https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "claude-opus-5-5",
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

    Claude mengembalikan JSON seperti ini di blok konten teks respons:

    ```json Output
    {
      "name": "John Smith",
      "email": "john@example.com",
      "plan_interest": "Enterprise",
      "demo_requested": true
    }
    ```
  </Tab>

  <Tab title="CLI">
    ```bash
    ant messages create <<'YAML'
    model: claude-opus-5-5
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

    Claude mengembalikan JSON seperti ini di blok konten teks respons:

    ```json Output
    {
      "name": "John Smith",
      "email": "john@example.com",
      "plan_interest": "Enterprise",
      "demo_requested": true
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Extract the key information from this email: "
                    "John Smith (john@example.com) is interested in our Enterprise plan "
                    "and wants to schedule a demo for next Tuesday at 2pm."
                ),
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
    text = next(block.text for block in response.content if block.type == "text")
    contact = json.loads(text)
    print(contact)
    ```

    Contoh sebelumnya menghasilkan output:

    ```text Output wrap
    {'name': 'John Smith', 'email': 'john@example.com', 'plan_interest': 'Enterprise', 'demo_requested': True}
    ```

    Untuk memindahkan [batasan yang tidak didukung oleh API](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations) ke dalam deskripsi bidang, lewatkan skema melalui `transform_schema()` dari paket `anthropic` sebelum mengirimkannya, dan edit hasilnya jika perlu. `transform_schema()` juga menerima model Pydantic. Berbeda dengan `client.messages.parse()`, fungsi ini mengembalikan skema yang telah ditransformasi alih-alih mengirimkannya.
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    import { jsonSchemaOutputFormat } from "@anthropic-ai/sdk/helpers/json-schema";

    const client = new Anthropic();

    const response = await client.messages.parse({
      model: "claude-opus-5-5",
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
    console.log(response.parsed_output);
    ```

    Gunakan `jsonSchemaOutputFormat()` untuk memberikan JSON schema biasa ke `parse()`, tanpa menginstal Zod. API mengembalikan respons yang sesuai dengan skema, dan jika Anda mendeklarasikan skema dengan `as const`, TypeScript secara otomatis menyimpulkan tipe untuk `parsed_output` sesuai skema Anda. Untuk skema yang diimpor atau dihasilkan, `parsed_output` bertipe `unknown`.

    Secara default, helper ini [mentransformasi skema](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#how-sdk-transformation-works) dengan cara yang sama seperti `zodOutputFormat()`. Berikan `{ transform: false }` sebagai argumen kedua untuk mengirimkannya tanpa perubahan. Berbeda dengan `zodOutputFormat()`, helper ini tidak memvalidasi respons, sehingga tidak menangkap pelanggaran [batasan yang tidak didukung oleh API](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations), seperti `minimum`.

    Contoh sebelumnya menghasilkan output:

    ```javascript Output
    { name: 'John Smith', email: 'john@example.com', planInterest: 'Pro' }
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using System.Text.Json;
    using Anthropic;
    using Anthropic.Models.Messages;

    var client = new AnthropicClient();

    var response = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus5_5,
        MaxTokens = 1024,
        Messages = [
            new UserMessageParam
            {
                Content = "Extract the key information from this email: "
                    + "John Smith (john@example.com) is interested in our Enterprise plan "
                    + "and wants to schedule a demo for next Tuesday at 2pm."
            }
        ],
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

    if (response.Content.Select(block => block.Value).OfType<TextBlock>().FirstOrDefault() is { } textBlock)
    {
        // JSON dijamin sesuai dengan skema
        var contact = JsonSerializer.Deserialize<JsonElement>(textBlock.Text);
        Console.WriteLine(contact);
    }
    ```

    Contoh sebelumnya menghasilkan output:

    ```json Output
    {"name":"John Smith","email":"john@example.com","plan_interest":"Enterprise","demo_requested":true}
    ```
  </Tab>

  <Tab title="Go">
    ```go
    type ContactInfo struct {
    	Name          string `json:"name"`
    	Email         string `json:"email"`
    	PlanInterest  string `json:"plan_interest"`
    	DemoRequested bool   `json:"demo_requested"`
    }

    func main() {
    	client := anthropic.NewClient()

    	message, _ := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     anthropic.ModelClaudeOpus5_5,
    		MaxTokens: 1024,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock(
    				"Extract the key information from this email: " +
    					"John Smith (john@example.com) is interested in our Enterprise plan " +
    					"and wants to schedule a demo for next Tuesday at 2pm.",
    			)),
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

    	for _, block := range message.Content {
    		switch variant := block.AsAny().(type) {
    		case anthropic.TextBlock:
    			var contact ContactInfo
    			json.Unmarshal([]byte(variant.Text), &contact)
    			fmt.Printf("%#v\n", contact)
    		}
    	}
    }
    ```

    Contoh sebelumnya menghasilkan output:

    ```text Output wrap
    main.ContactInfo{Name:"John Smith", Email:"john@example.com", PlanInterest:"Enterprise", DemoRequested:true}
    ```

    Agar SDK mentransformasi skema map, lewatkan skema tersebut melalui `BetaJSONSchemaOutputFormat()` pada API beta.
  </Tab>

  <Tab title="Java">
    ```java
    import com.anthropic.core.JsonValue;
    import com.anthropic.models.messages.JsonOutputFormat;
    // ...
    import com.anthropic.models.messages.OutputConfig;
    import com.fasterxml.jackson.databind.JsonNode;
    import com.fasterxml.jackson.databind.ObjectMapper;

    void main() throws Exception {
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
            .format(JsonOutputFormat.builder()
                .schema(schema)
                .build())
            .build();

        MessageCreateParams createParams = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_5_5)
            .maxTokens(1024)
            .outputConfig(outputConfig)
            .addUserMessage(
                "John Smith (john@example.com) is interested in our Enterprise plan.")
            .build();

        String json = client.messages().create(createParams).content().stream()
            .flatMap(contentBlock -> contentBlock.text().stream())
            .findFirst()
            .orElseThrow()
            .text();

        JsonNode contact = new ObjectMapper().readTree(json);
        IO.println(contact);
    }
    ```

    Contoh sebelumnya menghasilkan output:

    ```json Output
    {"name":"John Smith","email":"john@example.com","plan_interest":"Enterprise"}
    ```

    Untuk contoh yang lebih lengkap yang membangun skema bersarang dengan array dan deskripsi, lihat [`StructuredOutputsRawExample.java`](https://github.com/anthropics/anthropic-sdk-java/blob/main/anthropic-java-example/src/main/java/com/anthropic/example/StructuredOutputsRawExample.java) di repositori SDK.
  </Tab>

  <Tab title="PHP">
    ```php
    use Anthropic\Messages\OutputConfig;
    use Anthropic\Messages\JSONOutputFormat;

    $client = new Client();

    $message = $client->messages->create(
        maxTokens: 1024,
        messages: [
            [
                'role' => 'user',
                'content' => 'Extract the key information from this email: '
                    . 'John Smith (john@example.com) is interested in our Enterprise plan.',
            ],
        ],
        model: 'claude-opus-5-5',
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

    $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
    $contact = json_decode($textBlock->text, associative: true);
    var_dump($contact);
    ```

    Berikan skema sebagai array asosiatif ke `OutputConfig::with()`, dan dekode respons dengan `json_decode()`.

    Contoh sebelumnya menghasilkan output:

    ```text Output wrap
    array(3) {
      ["name"]=>
      string(10) "John Smith"
      ["email"]=>
      string(16) "john@example.com"
      ["plan_interest"]=>
      string(10) "Enterprise"
    }
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    client = Anthropic::Client.new

    response = client.messages.create(
      model: Anthropic::Model::CLAUDE_OPUS_5_5,
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "Extract the key information from this email: " \
            "John Smith (john@example.com) is interested in our Enterprise plan " \
            "and wants to schedule a demo for next Tuesday at 2pm."
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

    text = response.content.find { it.type == :text }.text
    contact = JSON.parse(text)
    p contact
    ```

    Contoh sebelumnya menghasilkan output:

    ```text Output wrap
    {"name" => "John Smith", "email" => "john@example.com", "plan_interest" => "Enterprise", "demo_requested" => true}
    ```
  </Tab>
</Tabs>

## Kasus penggunaan umum

<AccordionGroup>
  <Accordion title="Ekstraksi data">
    Ekstrak data terstruktur dari teks tidak terstruktur:

    <CodeGroup>
      ```bash cURL
      curl https://api.anthropic.com/v1/messages \
        -H "content-type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
          "model": "claude-opus-5-5",
          "max_tokens": 4096,
          "messages": [
            {
              "role": "user",
              "content": "Extract invoice data from: Invoice #12345, Date: 2024-01-15, Total: $500.00"
            }
          ],
          "output_config": {
            "format": {
              "type": "json_schema",
              "schema": {
                "type": "object",
                "properties": {
                  "invoice_number": {"type": "string"},
                  "date": {"type": "string"},
                  "total_amount": {"type": "number"},
                  "line_items": {
                    "type": "array",
                    "items": {"type": "object", "additionalProperties": false}
                  },
                  "customer_name": {"type": "string"}
                },
                "required": ["invoice_number", "date", "total_amount", "line_items", "customer_name"],
                "additionalProperties": false
              }
            }
          }
        }'
      ```

      ```bash CLI
      ant messages create <<'YAML'
      model: claude-opus-5-5
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
          model="claude-opus-5-5",
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
        model: "claude-opus-5-5",
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
          Model = Model.ClaudeOpus5_5,
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
          Messages = [new UserMessageParam { Content = $"Extract invoice data from: {invoiceText}" }]
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
      	Model:     anthropic.ModelClaudeOpus5_5,
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
              .model(Model.CLAUDE_OPUS_5_5)
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
          model: 'claude-opus-5-5',
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
        model: Anthropic::Model::CLAUDE_OPUS_5_5,
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
      ```bash cURL
      curl https://api.anthropic.com/v1/messages \
        -H "content-type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
          "model": "claude-opus-5-5",
          "max_tokens": 1024,
          "messages": [
            {
              "role": "user",
              "content": "Classify this feedback: Great product, fast shipping!"
            }
          ],
          "output_config": {
            "format": {
              "type": "json_schema",
              "schema": {
                "type": "object",
                "properties": {
                  "category": {"type": "string"},
                  "confidence": {"type": "number"},
                  "tags": {"type": "array", "items": {"type": "string"}},
                  "sentiment": {"type": "string"}
                },
                "required": ["category", "confidence", "tags", "sentiment"],
                "additionalProperties": false
              }
            }
          }
        }'
      ```

      ```bash CLI
      ant messages create <<'YAML'
      model: claude-opus-5-5
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
          model="claude-opus-5-5",
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
        model: "claude-opus-5-5",
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
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new UserMessageParam { Content = $"Classify this feedback: {feedbackText}" }],
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
      	Model:     anthropic.ModelClaudeOpus5_5,
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
              .model(Model.CLAUDE_OPUS_5_5)
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

      $feedbackText = 'Great product, fast shipping!';

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => "Classify this feedback: {$feedbackText}"]
          ],
          model: 'claude-opus-5-5',
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
        model: Anthropic::Model::CLAUDE_OPUS_5_5,
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
    Hasilkan respons yang siap untuk API:

    <CodeGroup>
      ```bash cURL
      curl https://api.anthropic.com/v1/messages \
        -H "content-type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
          "model": "claude-opus-5-5",
          "max_tokens": 1024,
          "messages": [
            {
              "role": "user",
              "content": "Process this request: ..."
            }
          ],
          "output_config": {
            "format": {
              "type": "json_schema",
              "schema": {
                "type": "object",
                "properties": {
                  "status": {"type": "string"},
                  "data": {"type": "object", "additionalProperties": false},
                  "errors": {
                    "type": "array",
                    "items": {"type": "object", "additionalProperties": false}
                  },
                  "metadata": {"type": "object", "additionalProperties": false}
                },
                "required": ["status", "data", "metadata"],
                "additionalProperties": false
              }
            }
          }
        }'
      ```

      ```bash CLI
      ant messages create <<'YAML'
      model: claude-opus-5-5
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
          model="claude-opus-5-5",
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
        model: "claude-opus-5-5",
        max_tokens: 1024,
        output_config: { format: zodOutputFormat(APIResponseSchema) },
        messages: [{ role: "user", content: "Process this request..." }]
      });

      console.log(response.parsed_output);
      ```

      ```csharp C#
      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new UserMessageParam { Content = "Process this request: ..." }],
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
      	Model:     anthropic.ModelClaudeOpus5_5,
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
              .model(Model.CLAUDE_OPUS_5_5)
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
          model: 'claude-opus-5-5',
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
        model: Anthropic::Model::CLAUDE_OPUS_5_5,
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

Untuk menegakkan kepatuhan JSON Schema pada input alat dengan “grammar-constrained sampling” (sampling yang dibatasi tata bahasa), lihat [Penggunaan alat ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use).

### Menggunakan kedua fitur bersama-sama

Output JSON dan penggunaan alat ketat menyelesaikan masalah yang berbeda dan dapat bekerja bersama:

* **Output JSON** mengontrol format respons Claude (apa yang dikatakan Claude).
* **Penggunaan alat ketat** memvalidasi parameter alat (bagaimana Claude memanggil fungsi Anda).

Jika digabungkan, Claude dapat memanggil alat dengan parameter yang dijamin valid DAN mengembalikan respons JSON terstruktur. Ini berguna untuk alur kerja agentik di mana Anda memerlukan panggilan alat yang andal sekaligus output akhir yang terstruktur.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": "Help me plan a trip to Paris departing May 15, 2026"
        }
      ],
      "output_config": {
        "format": {
          "type": "json_schema",
          "schema": {
            "type": "object",
            "properties": {
              "summary": {"type": "string"},
              "next_steps": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["summary", "next_steps"],
            "additionalProperties": false
          }
        }
      },
      "tools": [
        {
          "name": "search_flights",
          "strict": true,
          "input_schema": {
            "type": "object",
            "properties": {
              "destination": {"type": "string"},
              "date": {"type": "string", "format": "date"}
            },
            "required": ["destination", "date"],
            "additionalProperties": false
          }
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
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
  # Penggunaan alat ketat: parameter alat terjamin
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
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
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
      # Penggunaan alat ketat: parameter alat yang dijamin
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
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5-5",
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

  // Claude mungkin memanggil alat terlebih dahulu (tool_use) atau merespons dengan JSON (teks)
  console.log("Stop reason:", response.stop_reason);
  for (const block of response.content) {
    switch (block.type) {
      case "tool_use":
        console.log(`Tool call: ${block.name}(${JSON.stringify(block.input)})`);
        break;
      case "text":
        console.log("Response:", block.text);
        break;
    }
  }
  ```

  ```csharp C#
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new UserMessageParam { Content = "Help me plan a trip to Paris departing May 15, 2026" }],
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
  	Model:     anthropic.ModelClaudeOpus5_5,
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
  	// Penggunaan alat ketat: parameter alat yang terjamin
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

  // Penggunaan alat ketat: parameter alat yang dijamin
  InputSchema toolSchema = InputSchema.builder()
      .properties(JsonValue.from(Map.of(
          "destination", Map.of("type", "string"),
          "date", Map.of("type", "string", "format", "date")
      )))
      .putAdditionalProperty("required", JsonValue.from(List.of("destination", "date")))
      .putAdditionalProperty("additionalProperties", JsonValue.from(false))
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024L)
      .addUserMessage("Help me plan a trip to Paris departing May 15, 2026")
      .outputConfig(OutputConfig.builder()
          .format(JsonOutputFormat.builder()
              .schema(outputSchema)
              .build())
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
      model: 'claude-opus-5-5',
      // Output JSON: format respons terstruktur
      outputConfig: ['format' => TripPlan::class],
      // Penggunaan alat ketat: parameter alat yang terjamin
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

  // Claude mungkin memanggil alat terlebih dahulu (tool_use) atau merespons dengan JSON (teks)
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
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
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

### Kompilasi tata bahasa dan caching

Output terstruktur menggunakan sampling terbatas dengan artefak tata bahasa yang dikompilasi. Hal ini menimbulkan beberapa karakteristik kinerja yang perlu diperhatikan:

* **Latensi permintaan pertama:** Pertama kali Anda menggunakan skema tertentu, ada “latency” (latensi) tambahan saat tata bahasa dikompilasi.
* **Caching otomatis:** Tata bahasa yang dikompilasi di-cache selama 24 jam sejak penggunaan terakhir, sehingga permintaan berikutnya jauh lebih cepat.
* **Invalidasi cache:** Cache diinvalidasi jika Anda mengubah struktur JSON schema atau, saat menggunakan output terstruktur dan penggunaan alat sekaligus, kumpulan alat dalam permintaan Anda. Mengubah hanya bidang `name` atau `description` tidak menginvalidasi cache.

### Modifikasi prompt dan biaya token

Saat menggunakan output terstruktur, Claude secara otomatis menerima “system prompt” (prompt sistem) tambahan yang menjelaskan format output yang diharapkan. Ini berarti:

* Jumlah token input Anda sedikit lebih tinggi.
* Prompt yang disisipkan membebankan token kepada Anda seperti prompt sistem lainnya.
* Mengubah parameter `output_config.format` akan menginvalidasi [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) apa pun untuk utas percakapan tersebut.

### Batasan JSON Schema

Output terstruktur mendukung JSON Schema standar dengan beberapa batasan. Output JSON dan penggunaan alat ketat sama-sama memiliki batasan ini.

<Accordion title="Fitur yang didukung">
  * Semua tipe dasar: object, array, string, integer, number, boolean, null
  * `enum` (hanya string, angka, boolean, atau null, tanpa tipe kompleks). Untuk catatan tentang kapitalisasi, lihat [Output tidak valid](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#invalid-outputs).
  * `const`
  * `anyOf` dan `allOf` (dengan batasan: `allOf` dengan `$ref` tidak didukung)
  * `$ref`, `$def`, dan `definitions` (`$ref` eksternal tidak didukung)
  * Properti `default` untuk semua tipe yang didukung
  * `required` dan `additionalProperties` (harus diatur ke `false` untuk objek)
  * Format string: `date-time`, `time`, `date`, `duration`, `email`, `hostname`, `uri`, `ipv4`, `ipv6`, `uuid`
  * `minItems` array (hanya nilai 0 dan 1 yang didukung)
</Accordion>

<Accordion title="Tidak didukung">
  * Skema rekursif
  * Tipe kompleks dalam enum
  * `$ref` eksternal (misalnya, `'$ref': 'http://...'`)
  * Batasan numerik (seperti `minimum`, `maximum`, `multipleOf`)
  * Batasan string (`minLength`, `maxLength`)
  * Batasan array selain `minItems` bernilai 0 atau 1
  * `additionalProperties` yang diatur ke nilai apa pun selain `false`

  Jika Anda menggunakan fitur yang tidak didukung, Anda akan menerima kesalahan 400 beserta detailnya.
</Accordion>

<Accordion title="Dukungan pola (regex)">
  **Fitur regex yang didukung:**

  * Pencocokan penuh (`^...$`) dan pencocokan parsial
  * Kuantifier: `*`, `+`, `?`, kasus `{n,m}` sederhana
  * Kelas karakter: `[]`, `.`, `\d`, `\w`, `\s`
  * Grup: `(...)`

  **TIDAK didukung:**

  * Referensi balik ke grup (misalnya, `\1`, `\2`)
  * Asersi lookahead/lookbehind (misalnya, `(?=...)`, `(?!...)`)
  * Batas kata: `\b`, `\B`
  * Kuantifier `{n,m}` kompleks dengan rentang besar

  Pola regex sederhana berfungsi dengan baik. Pola kompleks mungkin menghasilkan kesalahan 400.
</Accordion>

<Tip>
  Helper SDK dapat mentransformasi skema dengan [batasan yang tidak didukung oleh API](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations). Lihat [Cara kerja transformasi SDK](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#how-sdk-transformation-works).
</Tip>

### Urutan properti

Saat menggunakan output terstruktur, properti dalam objek mempertahankan urutan yang didefinisikan dari skema Anda, dengan satu catatan penting: **properti wajib muncul terlebih dahulu, diikuti oleh properti opsional**.

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

Jika urutan properti dalam output penting bagi aplikasi Anda, tandai semua properti sebagai wajib, atau perhitungkan pengurutan ulang ini dalam logika parsing Anda.

### Output tidak valid

Meskipun output terstruktur menjamin kepatuhan skema dalam sebagian besar kasus, ada skenario di mana output mungkin tidak cocok dengan skema Anda:

**Penolakan** (`stop_reason: "refusal"`)

Claude mempertahankan sifat keamanan dan kebermanfaatannya bahkan saat menggunakan output terstruktur. Jika Claude menolak permintaan karena alasan keamanan:

* Respons memiliki `stop_reason: "refusal"`.
* Anda akan menerima kode status 200.
* Anda akan ditagih untuk token yang dihasilkan.
* Output mungkin tidak cocok dengan skema Anda karena pesan penolakan lebih diutamakan daripada batasan skema.

Properti yang meminta pemikiran model atau penalaran langkah demi langkah dapat menyebabkan penolakan `reasoning_extraction`. Mintalah penjelasan singkat sebagai gantinya. Lihat [Simpan penalaran di blok pemikiran](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks).

**Batas token tercapai** (`stop_reason: "max_tokens"`)

Jika respons terpotong karena mencapai batas `max_tokens`:

* Respons memiliki `stop_reason: "max_tokens"`.
* Output mungkin tidak lengkap dan tidak cocok dengan skema Anda.
* Coba lagi dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan output terstruktur yang lengkap.

**Kapitalisasi nilai enum**

Output terstruktur tidak menjamin kapitalisasi nilai string `enum` dan `const`: Claude mungkin mengembalikan nilai yang berbeda dari skema Anda hanya dalam kapitalisasi, biasanya pada huruf pertama kata yang mengikuti spasi. Misalnya, dengan skema ini:

```json
{
  "type": "string",
  "enum": ["Conversation Topic 1", "Conversation Topic 2", "Conversation topic 3"]
}
```

Output mungkin berisi `"Conversation Topic 3"` (huruf kapital “T”) meskipun nilai persis tersebut tidak ada dalam enum. Respons selesai secara normal, tanpa kesalahan dan tanpa `stop_reason` khusus. Ini berlaku untuk output JSON dan penggunaan alat ketat. Bandingkan nilai enum tanpa membedakan huruf besar/kecil, dan hindari nilai enum yang hanya berbeda dalam kapitalisasi.

### Batas kompleksitas skema

Output terstruktur bekerja dengan mengompilasi JSON schema Anda menjadi tata bahasa yang membatasi output Claude. Skema yang lebih kompleks menghasilkan tata bahasa yang lebih besar yang membutuhkan waktu lebih lama untuk dikompilasi. Untuk melindungi dari waktu kompilasi yang berlebihan, API menerapkan beberapa batas kompleksitas.

#### Batas eksplisit

Batas berikut berlaku untuk semua permintaan dengan `output_config.format` atau `strict: true`:

| Batas                       | Nilai | Deskripsi                                                                                                                                                                                           |
| --------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Alat ketat per permintaan   | 20    | Jumlah maksimum alat dengan `strict: true`. Alat non-ketat tidak dihitung dalam batas ini.                                                                                                          |
| Parameter opsional          | 24    | Total parameter opsional di semua skema alat ketat dan skema output JSON. Setiap parameter yang tidak tercantum dalam `required` dihitung dalam batas ini.                                          |
| Parameter dengan tipe union | 16    | Total parameter yang menggunakan `anyOf` atau array tipe (misalnya, `"type": ["string", "null"]`) di semua skema ketat. Parameter ini sangat mahal karena menciptakan biaya kompilasi eksponensial. |

<Note>
  Batas ini berlaku untuk total gabungan di semua skema ketat dalam satu permintaan. Misalnya, jika Anda memiliki 4 alat ketat dengan masing-masing 6 parameter opsional, Anda akan mencapai batas 24 parameter meskipun tidak ada satu alat pun yang tampak kompleks.
</Note>

#### Batas internal tambahan

Selain batas eksplisit dalam tabel sebelumnya, terdapat batas internal tambahan pada ukuran tata bahasa yang dikompilasi. Batas ini ada karena kompleksitas skema tidak dapat direduksi menjadi satu dimensi: fitur seperti parameter opsional, tipe union, objek bersarang, dan jumlah alat saling berinteraksi dengan cara yang dapat membuat tata bahasa yang dikompilasi menjadi sangat besar secara tidak proporsional.

Ketika batas ini terlampaui, Anda akan menerima kesalahan 400 dengan pesan “Schema is too complex for compilation.” Kesalahan ini berarti kompleksitas gabungan skema Anda melebihi apa yang dapat dikompilasi secara efisien, bahkan jika setiap batas individual dalam tabel sebelumnya terpenuhi. Sebagai pengaman terakhir, API juga menerapkan **batas waktu kompilasi 180 detik**. Skema yang lolos semua pemeriksaan eksplisit tetapi menghasilkan tata bahasa terkompilasi yang sangat besar mungkin mencapai batas waktu ini.

#### Tips untuk mengurangi kompleksitas skema

Jika Anda mencapai batas kompleksitas, coba strategi berikut secara berurutan:

1. **Tandai hanya alat penting sebagai ketat.** Jika Anda memiliki banyak alat, gunakan penggunaan alat ketat hanya untuk alat di mana pelanggaran skema menyebabkan masalah nyata, dan andalkan kepatuhan alami Claude untuk alat yang lebih sederhana.

2. **Kurangi parameter opsional.** Jadikan parameter `required` jika memungkinkan. Setiap parameter opsional kira-kira menggandakan sebagian ruang status tata bahasa. Jika sebuah parameter selalu memiliki nilai default yang wajar, pertimbangkan untuk menjadikannya wajib dan minta Claude memberikan nilai default tersebut secara eksplisit.

3. **Sederhanakan struktur bersarang.** Objek yang bersarang dalam dengan bidang opsional memperparah kompleksitas. Ratakan struktur jika memungkinkan.

4. **Pisahkan menjadi beberapa permintaan.** Jika Anda memiliki banyak alat ketat, pertimbangkan untuk membaginya ke beberapa permintaan terpisah atau subagen.

Untuk masalah yang terus berlanjut dengan skema yang valid, [hubungi dukungan](https://support.claude.com/en/articles/9015913-how-to-get-support) dengan menyertakan definisi skema Anda.

## Migrasi dari beta

Parameter `output_format` telah dipindahkan ke `output_config.format`, dan header beta tidak lagi diperlukan. Parameter `output_format` sudah usang. Untuk tetap menggunakannya, tambahkan header beta `structured-outputs-2025-11-13`. Tanpa header tersebut, API mengembalikan kesalahan 400.

Python SDK (v1.0 dan yang lebih baru) tidak menerima `output_format={...}` pada `client.beta.messages.create()` atau `count_tokens()` dan memunculkan `TypeError`. Gunakan `output_config` sebagai gantinya. Lihat [Menggunakan JSON schema mentah](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#using-a-raw-json-schema) untuk bentuk API yang diperbarui.

## Kompatibilitas fitur

**Berfungsi dengan:**

* **[Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing):** Proses output terstruktur dalam skala besar dengan diskon 50 persen
* **[Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting):** Hitung token tanpa kompilasi
* **[Streaming](https://platform.claude.com/docs/id/build-with-claude/streaming):** Streaming output terstruktur seperti respons normal
* **[Penggunaan gabungan](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#using-both-features-together):** Gunakan output JSON (`output_config.format`) dan penggunaan alat ketat (`strict: true`) bersama-sama dalam permintaan yang sama

**Tidak kompatibel dengan:**

* **[Kutipan](https://platform.claude.com/docs/id/build-with-claude/citations):** Kutipan memerlukan penyisipan blok kutipan di antara teks, yang bertentangan dengan batasan JSON schema yang ketat. API mengembalikan kesalahan 400 jika kutipan diaktifkan bersama `output_config.format`. Untuk mengekstrak data terstruktur dengan kutipan untuk setiap nilai, lihat [Mendapatkan data terstruktur dengan kutipan](https://platform.claude.com/docs/id/build-with-claude/citations#get-structured-data-with-citations).
* **Prefilling pesan:** Prefilling tidak kompatibel dengan output JSON.

<Tip>
  **Cakupan tata bahasa:** Tata bahasa hanya berlaku untuk output langsung Claude, bukan untuk panggilan penggunaan alat, hasil alat, atau tag pemikiran (saat menggunakan [pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking)). Status tata bahasa diatur ulang di antara bagian-bagian, memungkinkan Claude berpikir secara bebas sambil tetap menghasilkan output terstruktur dalam respons akhir.
</Tip>

## Ketersediaan

Output terstruktur tersedia di semua model dan layak untuk kesiapan HIPAA.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia

| Status   | Platform cloud               | Model                                                              |
| -------- | ---------------------------- | ------------------------------------------------------------------ |
| Tersedia | Semua platform yang didukung | [Semua model](https://platform.claude.com/docs/id/models/overview) |

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tidak tersedia

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                                                                                                                                                                                                         | HIPAA                                                                                                                                                                                                          |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Status | Layak (bersyarat; tidak termasuk [Model yang dicakup](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements))                                                                                                                                                                              | Layak                                                                                                                                                                                                          |
| Detail | Prompt Anda dan output Claude tidak disimpan. Hanya JSON schema yang di-cache, hingga 24 jam sejak terakhir digunakan. Ini juga mencakup penggunaan alat ketat (`strict: true` pada alat), yang menggunakan pipeline grammar yang sama. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#data-retention) | PHI tidak boleh disertakan dalam definisi JSON schema; lihat panduan penanganan PHI. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#phi-handling-guidelines) |

Endpoint yang berlaku:

* `/v1/messages`

Prompt dan respons diproses dengan ZDR saat menggunakan output terstruktur. Namun, JSON schema itu sendiri di-cache sementara hingga 24 jam sejak penggunaan terakhir untuk tujuan optimasi. Tidak ada data prompt atau respons yang disimpan di luar respons API.

Output terstruktur memenuhi syarat HIPAA, tetapi **PHI tidak boleh disertakan dalam definisi JSON schema**. API mengompilasi JSON schema menjadi tata bahasa yang di-cache secara terpisah dari konten pesan, dan skema yang di-cache ini tidak menerima perlindungan PHI yang sama seperti prompt dan respons. Jangan sertakan PHI dalam nama properti skema, nilai `enum`, nilai `const`, atau regular expression `pattern`. PHI hanya boleh muncul dalam konten pesan (prompt dan respons), di mana PHI dilindungi berdasarkan perlindungan HIPAA.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Kutipan" icon="book-bookmark" href="https://platform.claude.com/docs/id/build-with-claude/citations">
    Minta Claude mengutip sumbernya saat menjawab pertanyaan tentang dokumen yang diberikan.
  </Card>

  <Card title="Penggunaan alat ketat" icon="check" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use">
    Tegakkan kepatuhan JSON Schema pada input alat Claude dengan sampling yang dibatasi tata bahasa.
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="wrench" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview">
    Hubungkan Claude ke alat dan API eksternal. Pelajari di mana alat dijalankan dan bagaimana loop agentik bekerja.
  </Card>

  <Card title="Harga" icon="calculator" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Pelajari struktur harga Anthropic untuk model dan fitur.
  </Card>
</CardGroup>
