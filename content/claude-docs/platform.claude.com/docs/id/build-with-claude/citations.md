---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/citations
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: 87dc995faf688f5309f3bccb7e856f768440ac57dbaa1226f2205dadc355c7f1
---

# Citations

Landasi respons Claude pada dokumen sumber Anda. Citations mengembalikan bagian teks persis yang mendukung setiap klaim, sehingga Anda dapat memverifikasi jawaban dan menampilkan sumber kepada pengguna Anda.

---

<Note>
  Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Claude dapat memberikan sitasi (citations) yang terperinci saat menjawab pertanyaan tentang dokumen, membantu Anda melacak dan memverifikasi sumber di balik setiap respons.

Semua [model aktif](/docs/id/about-claude/models/overview) mendukung citations, dengan pengecualian Claude Haiku 3.

<Tip>
  Bagikan umpan balik dan saran Anda tentang fitur citations menggunakan [formulir umpan balik citations](https://forms.gle/9n9hSrKnKe3rpowH9).
</Tip>

Contoh berikut menunjukkan cara mengaktifkan citations pada dokumen teks biasa dengan Messages API:

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
          "content": [
            {
              "type": "document",
              "source": {
                "type": "text",
                "media_type": "text/plain",
                "data": "The grass is green. The sky is blue."
              },
              "title": "My Document",
              "context": "This is a trustworthy document.",
              "citations": {"enabled": true}
            },
            {
              "type": "text",
              "text": "What color is the grass and sky?"
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: document
          source:
            type: text
            media_type: text/plain
            data: The grass is green. The sky is blue.
          title: My Document
          context: This is a trustworthy document.
          citations:
            enabled: true
        - type: text
          text: What color is the grass and sky?
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
              "content": [
                  {
                      "type": "document",
                      "source": {
                          "type": "text",
                          "media_type": "text/plain",
                          "data": "The grass is green. The sky is blue.",
                      },
                      "title": "My Document",
                      "context": "This is a trustworthy document.",
                      "citations": {"enabled": True},
                  },
                  {"type": "text", "text": "What color is the grass and sky?"},
              ],
          }
      ],
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
        content: [
          {
            type: "document",
            source: {
              type: "text",
              media_type: "text/plain",
              data: "The grass is green. The sky is blue."
            },
            title: "My Document",
            context: "This is a trustworthy document.",
            citations: { enabled: true }
          },
          {
            type: "text",
            text: "What color is the grass and sky?"
          }
        ]
      }
    ]
  });
  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var response = await client.Messages.Create(
      new()
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = new MessageParamContent(new List<ContentBlockParam>
                  {
                      new ContentBlockParam(new DocumentBlockParam(
                          new DocumentBlockParamSource(new PlainTextSource()
                          {
                              Data = "The grass is green. The sky is blue.",
                          })
                      )
                      {
                          Title = "My Document",
                          Context = "This is a trustworthy document.",
                          Citations = new CitationsConfigParam { Enabled = true },
                      }),
                      new ContentBlockParam(new TextBlockParam("What color is the grass and sky?")),
                  }),
              },
          ],
      }
  );

  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.ContentBlockParamUnion{
  				OfDocument: &anthropic.DocumentBlockParam{
  					Source: anthropic.DocumentBlockParamSourceUnion{
  						OfText: &anthropic.PlainTextSourceParam{
  							Data: "The grass is green. The sky is blue.",
  						},
  					},
  					Title:     anthropic.String("My Document"),
  					Context:   anthropic.String("This is a trustworthy document."),
  					Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  				},
  			},
  			anthropic.NewTextBlock("What color is the grass and sky?"),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  PlainTextSource source = PlainTextSource.builder()
    .data("The grass is green. The sky is blue.")
    .build();

  DocumentBlockParam documentParam = DocumentBlockParam.builder()
    .source(source)
    .title("My Document")
    .context("This is a trustworthy document.")
    .citations(CitationsConfigParam.builder().enabled(true).build())
    .build();

  TextBlockParam textBlockParam = TextBlockParam.builder()
    .text("What color is the grass and sky?")
    .build();

  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_8)
    .maxTokens(1024)
    .addUserMessageOfBlockParams(
      List.of(
        ContentBlockParam.ofDocument(documentParam),
        ContentBlockParam.ofText(textBlockParam)
      )
    )
    .build();

  Message message = client.messages().create(params);
  System.out.println(message);
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'text',
                          'media_type' => 'text/plain',
                          'data' => 'The grass is green. The sky is blue.',
                      ],
                      'title' => 'My Document',
                      'context' => 'This is a trustworthy document.',
                      'citations' => ['enabled' => true],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What color is the grass and sky?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
  );

  echo json_encode($response, JSON_PRETTY_PRINT);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "text",
              media_type: "text/plain",
              data: "The grass is green. The sky is blue."
            },
            title: "My Document",
            context: "This is a trustworthy document.",
            citations: { enabled: true }
          },
          {
            type: "text",
            text: "What color is the grass and sky?"
          }
        ]
      }
    ]
  )

  puts response
  ```
</CodeGroup>

<Tip>
  **Perbandingan dengan pendekatan berbasis prompt**

  Dibandingkan dengan meminta Claude mengutip sumber melalui prompt, fitur citations menawarkan keunggulan berikut:

  * **Penghematan biaya:** Jika pendekatan berbasis prompt Anda meminta Claude untuk menghasilkan kutipan langsung, Anda mungkin melihat penghematan biaya karena `cited_text` tidak dihitung dalam token output Anda.
  * **Keandalan sitasi yang lebih baik:** Karena API mengurai citations ke dalam format respons yang dijelaskan di bagian berikut dan mengekstrak `cited_text` secara langsung, citations dijamin berisi penunjuk yang valid ke dokumen yang disediakan.
  * **Kualitas sitasi yang lebih baik:** Dalam evaluasi Anthropic, fitur citations secara signifikan lebih mungkin mengutip kutipan yang paling relevan dari dokumen dibandingkan pendekatan yang murni berbasis prompt.
</Tip>

***

## Cara kerja citations

Integrasikan citations dengan Claude melalui langkah-langkah berikut:

<Steps>
  <Step title="Sediakan dokumen dan aktifkan citations">
    * Sertakan dokumen dalam salah satu format yang didukung: [PDF](#pdf-documents), [teks biasa](#plain-text-documents), atau dokumen [konten kustom](#custom-content-documents).
    * Atur `citations.enabled=true` pada setiap dokumen Anda. Saat ini, citations harus diaktifkan pada semua atau tidak sama sekali dari dokumen dalam sebuah permintaan.
    * Hanya sitasi teks yang saat ini didukung. Sitasi gambar belum dimungkinkan.
  </Step>

  <Step title="Dokumen diproses">
    * Konten dokumen "dipecah" (chunked) untuk menentukan granularitas minimum dari citations yang mungkin. Misalnya, pemecahan per kalimat memungkinkan Claude mengutip satu kalimat atau merangkai beberapa kalimat berurutan untuk mengutip paragraf atau bagian yang lebih panjang.

      * **Untuk PDF:** Teks diekstrak seperti yang dijelaskan dalam [dukungan PDF](/docs/id/build-with-claude/pdf-support) dan konten dipecah menjadi kalimat. Mengutip gambar dari PDF saat ini tidak didukung.
      * **Untuk dokumen teks biasa:** Konten dipecah menjadi kalimat-kalimat yang dapat dikutip.
      * **Untuk dokumen konten kustom:** Blok konten yang Anda sediakan digunakan apa adanya dan tidak ada pemecahan lebih lanjut yang dilakukan.
  </Step>

  <Step title="Claude memberikan respons dengan sitasi">
    * Respons sekarang dapat mencakup beberapa blok teks di mana setiap blok teks dapat berisi klaim yang dibuat Claude dan daftar citations yang mendukung klaim tersebut.

    * Citations merujuk pada lokasi spesifik dalam dokumen sumber. Format citations ini bergantung pada jenis dokumen yang dikutip.

      * **Untuk PDF:** Citations mencakup rentang nomor halaman (berindeks 1).
      * **Untuk dokumen teks biasa:** Citations mencakup rentang indeks karakter (berindeks 0).
      * **Untuk dokumen konten kustom:** Citations mencakup rentang indeks blok konten (berindeks 0) yang sesuai dengan daftar konten asli yang disediakan.

    * Indeks dokumen disediakan untuk menunjukkan sumber referensi dan berindeks 0 sesuai dengan daftar semua dokumen dalam permintaan asli Anda.
  </Step>
</Steps>

<Tip>
  **Pemecahan otomatis vs konten kustom**

  Secara default, dokumen teks biasa dan PDF secara otomatis dipecah menjadi kalimat. Jika Anda memerlukan kontrol lebih atas granularitas sitasi (misalnya, untuk poin-poin atau transkrip), gunakan dokumen konten kustom sebagai gantinya. Lihat [Jenis dokumen](#document-types) untuk detail lebih lanjut.

  Misalnya, jika Anda ingin Claude dapat mengutip kalimat tertentu dari chunk RAG Anda, Anda harus memasukkan setiap chunk RAG ke dalam dokumen teks biasa. Sebaliknya, jika Anda tidak ingin ada pemecahan lebih lanjut, atau jika Anda ingin menyesuaikan pemecahan tambahan, Anda dapat memasukkan chunk RAG ke dalam dokumen konten kustom.
</Tip>

### Konten yang dapat dikutip vs tidak dapat dikutip

* Teks yang ditemukan dalam konten `source` dokumen dapat dikutip.
* `title` dan `context` adalah bidang opsional yang diteruskan ke model tetapi tidak digunakan untuk konten yang dikutip.
* `title` dibatasi panjangnya, sehingga bidang `context` berguna untuk menyimpan metadata dokumen sebagai teks atau JSON yang di-string-kan.

### Indeks sitasi

* Indeks dokumen berindeks 0 dari daftar semua blok konten dokumen dalam permintaan (mencakup semua pesan).
* Indeks karakter berindeks 0 dengan indeks akhir eksklusif.
* Nomor halaman berindeks 1 dengan nomor halaman akhir eksklusif.
* Indeks blok konten berindeks 0 dengan indeks akhir eksklusif dari daftar `content` yang disediakan dalam dokumen konten kustom.

### Biaya token

* Mengaktifkan citations menyebabkan sedikit peningkatan token input karena penambahan prompt sistem dan pemecahan dokumen.
* Namun, fitur citations sangat efisien dalam hal token output. Di balik layar, model menghasilkan citations dalam format terstandarisasi yang kemudian diurai menjadi teks yang dikutip dan indeks lokasi dokumen. Bidang `cited_text` disediakan untuk kenyamanan dan tidak dihitung dalam token output.
* Ketika diteruskan kembali dalam giliran percakapan berikutnya, `cited_text` juga tidak dihitung dalam token input.

### Kompatibilitas fitur

Citations bekerja bersama dengan fitur API lainnya termasuk [caching prompt](/docs/id/build-with-claude/prompt-caching), [penghitungan token](/docs/id/build-with-claude/token-counting), dan [pemrosesan batch](/docs/id/build-with-claude/batch-processing).

<Warning>
  **Citations dan structured outputs tidak kompatibel**

  Citations tidak dapat digunakan bersama dengan [structured outputs](/docs/id/build-with-claude/structured-outputs). Jika Anda mengaktifkan citations pada dokumen apa pun yang disediakan pengguna (blok `document` atau blok `search_result`) dan juga menyertakan parameter `output_config.format` (atau parameter `output_format` yang sudah usang), API mengembalikan error 400.

  Hal ini karena citations memerlukan penyisipan blok sitasi di antara output teks, yang tidak kompatibel dengan batasan skema JSON yang ketat dari structured outputs.
</Warning>

#### Menggunakan caching prompt dengan citations

Citations dan "prompt caching" (caching prompt) dapat digunakan bersama secara efektif.

Blok sitasi yang dihasilkan dalam respons tidak dapat di-cache secara langsung, tetapi dokumen sumber yang dirujuknya dapat di-cache. Untuk mengoptimalkan kinerja, terapkan `cache_control` pada blok konten dokumen tingkat atas Anda.

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
          "content": [
            {
              "type": "document",
              "source": {
                "type": "text",
                "media_type": "text/plain",
                "data": "This is a very long document with thousands of words..."
              },
              "citations": {"enabled": true},
              "cache_control": {"type": "ephemeral"}
            },
            {
              "type": "text",
              "text": "What does this document say about API features?"
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 <<'YAML'
  messages:
    - role: user
      content:
        - type: document
          source:
            type: text
            media_type: text/plain
            data: This is a very long document with thousands of words...
          citations:
            enabled: true
          cache_control:
            type: ephemeral
        - type: text
          text: What does this document say about API features?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Konten dokumen panjang (misalnya, dokumentasi teknis)
  long_document = (
      "This is a very long document with thousands of words..." + " ... " * 1000
  )  # Minimum cacheable length

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "document",
                      "source": {
                          "type": "text",
                          "media_type": "text/plain",
                          "data": long_document,
                      },
                      "citations": {"enabled": True},
                      "cache_control": {
                          "type": "ephemeral"
                      },  # Cache the document content
                  },
                  {
                      "type": "text",
                      "text": "What does this document say about API features?",
                  },
              ],
          }
      ],
  )
  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Konten dokumen panjang (misalnya, dokumentasi teknis)
  const longDocument =
    "This is a very long document with thousands of words..." + " ... ".repeat(1000); // Minimum cacheable length

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "text",
              media_type: "text/plain",
              data: longDocument
            },
            citations: { enabled: true },
            cache_control: { type: "ephemeral" } // Cache the document content
          },
          {
            type: "text",
            text: "What does this document say about API features?"
          }
        ]
      }
    ]
  });
  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  // Konten dokumen panjang (misalnya, dokumentasi teknis)
  var longDocument =
      "This is a very long document with thousands of words..."
      + string.Concat(Enumerable.Repeat(" ... ", 1000)); // Minimum cacheable length

  var response = await client.Messages.Create(
      new()
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = new MessageParamContent(new List<ContentBlockParam>
                  {
                      new ContentBlockParam(new DocumentBlockParam(
                          new DocumentBlockParamSource(new PlainTextSource() { Data = longDocument })
                      )
                      {
                          Citations = new CitationsConfigParam { Enabled = true },
                          CacheControl = new CacheControlEphemeral(), // Cache the document content
                      }),
                      new ContentBlockParam(new TextBlockParam("What does this document say about API features?")),
                  }),
              },
          ],
      }
  );

  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Konten dokumen panjang (misalnya, dokumentasi teknis)
  longDocument := "This is a very long document with thousands of words..." +
  	strings.Repeat(" ... ", 1000) // Minimum cacheable length

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.ContentBlockParamUnion{
  				OfDocument: &anthropic.DocumentBlockParam{
  					Source: anthropic.DocumentBlockParamSourceUnion{
  						OfText: &anthropic.PlainTextSourceParam{Data: longDocument},
  					},
  					Citations:    anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  					CacheControl: anthropic.NewCacheControlEphemeralParam(), // Cache the document content
  				},
  			},
  			anthropic.NewTextBlock("What does this document say about API features?"),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Konten dokumen panjang (misalnya, dokumentasi teknis)
  String longDocument =
    "This is a very long document with thousands of words..."
      + " ... ".repeat(1000); // Minimum cacheable length

  DocumentBlockParam documentParam = DocumentBlockParam.builder()
    .source(PlainTextSource.builder().data(longDocument).build())
    .citations(CitationsConfigParam.builder().enabled(true).build())
    .cacheControl(CacheControlEphemeral.builder().build()) // Cache the document content
    .build();

  TextBlockParam textBlockParam = TextBlockParam.builder()
    .text("What does this document say about API features?")
    .build();

  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_8)
    .maxTokens(1024)
    .addUserMessageOfBlockParams(
      List.of(
        ContentBlockParam.ofDocument(documentParam),
        ContentBlockParam.ofText(textBlockParam)
      )
    )
    .build();

  Message message = client.messages().create(params);
  System.out.println(message);
  ```

  ```php PHP
  $client = new Client();

  // Konten dokumen panjang (misalnya, dokumentasi teknis)
  $longDocument =
      'This is a very long document with thousands of words...'
      . str_repeat(' ... ', 1000); // Minimum cacheable length

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'text',
                          'media_type' => 'text/plain',
                          'data' => $longDocument,
                      ],
                      'citations' => ['enabled' => true],
                      'cache_control' => ['type' => 'ephemeral'], // Cache the document content
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What does this document say about API features?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
  );

  echo json_encode($response, JSON_PRETTY_PRINT);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Konten dokumen panjang (misalnya, dokumentasi teknis)
  long_document =
    "This is a very long document with thousands of words..." +
    " ... " * 1000 # Minimum cacheable length

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "text",
              media_type: "text/plain",
              data: long_document
            },
            citations: { enabled: true },
            cache_control: { type: "ephemeral" } # Cache the document content
          },
          {
            type: "text",
            text: "What does this document say about API features?"
          }
        ]
      }
    ]
  )

  puts response
  ```
</CodeGroup>

Dalam contoh ini:

* Konten dokumen di-cache menggunakan `cache_control` pada blok dokumen.
* Citations diaktifkan pada dokumen.
* Claude dapat menghasilkan respons dengan citations sambil mendapatkan manfaat dari konten dokumen yang di-cache.
* Permintaan berikutnya yang menggunakan dokumen yang sama mendapatkan manfaat dari konten yang di-cache.

## Jenis dokumen

### Memilih jenis dokumen

Tiga jenis dokumen didukung untuk citations. Dokumen dapat disediakan langsung dalam pesan (base64, teks, atau URL) atau diunggah melalui [Files API](/docs/id/build-with-claude/files) dan dirujuk dengan `file_id`:

| Jenis         | Terbaik untuk                                                     | Pemecahan                | Format sitasi                 |
| ------------- | ----------------------------------------------------------------- | ------------------------ | ----------------------------- |
| Teks biasa    | Dokumen teks sederhana, prosa                                     | Kalimat                  | Indeks karakter (berindeks 0) |
| PDF           | File PDF dengan konten teks                                       | Kalimat                  | Nomor halaman (berindeks 1)   |
| Konten kustom | Daftar, transkrip, pemformatan khusus, sitasi yang lebih granular | Tanpa pemecahan tambahan | Indeks blok (berindeks 0)     |

<Note>
  Untuk jenis file yang tidak didukung oleh blok `document` (misalnya, .docx dan .xlsx), konversikan file tersebut ke teks biasa dan sertakan kontennya langsung dalam konten pesan. File yang sudah berupa teks biasa, seperti file .csv dan .md, juga dapat diunggah dengan tipe konten `text/plain` secara eksplisit. Lihat [Bekerja dengan format file lain](/docs/id/build-with-claude/files#working-with-other-file-formats).
</Note>

### Dokumen teks biasa

Dokumen teks biasa secara otomatis dipecah menjadi kalimat. Anda dapat menyediakannya secara inline atau dengan referensi menggunakan `file_id`-nya:

<Tabs>
  <Tab title="Teks inline">
    Contoh pengantar di bagian atas halaman ini menunjukkan permintaan teks biasa lengkap di setiap SDK. Blok dokumen menggunakan sumber `text`:

    ```json
    {
      "type": "document",
      "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": "Plain text content..."
      },
      "title": "Document Title",
      "context": "Context about the document that will not be cited from",
      "citations": { "enabled": true }
    }
    ```
  </Tab>

  <Tab title="Files API">
    <Note>
      Sumber dokumen Files API masih dalam tahap beta. Contoh-contoh ini menggunakan jalur klien beta; lihat [Files API](/docs/id/build-with-claude/files) untuk detail pengunggahan.
    </Note>

    <CodeGroup>
      ```bash cURL
      curl -X POST https://api.anthropic.com/v1/messages \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: files-api-2025-04-14" \
        -H "content-type: application/json" \
        -d @- <<EOF
      {
        "model": "claude-opus-4-8",
        "max_tokens": 1024,
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "document",
                "source": {"type": "file", "file_id": "$FILE_ID"},
                "title": "Document Title",
                "context": "Context about the document that will not be cited from",
                "citations": {"enabled": true}
              },
              {
                "type": "text",
                "text": "Summarize this document."
              }
            ]
          }
        ]
      }
      EOF
      ```

      ```bash CLI
      ant beta:messages create --beta files-api-2025-04-14 <<YAML
      model: claude-opus-4-8
      max_tokens: 1024
      messages:
        - role: user
          content:
            - type: document
              source:
                type: file
                file_id: $FILE_ID
              title: Document Title
              context: Context about the document that will not be cited from
              citations:
                enabled: true
            - type: text
              text: Summarize this document.
      YAML
      ```

      ```python Python
      cited_response = client.beta.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          messages=[
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "document",
                          "source": {"type": "file", "file_id": file_id},
                          "title": "Document Title",
                          "context": "Context about the document that will not be cited from",
                          "citations": {"enabled": True},
                      },
                      {"type": "text", "text": "Summarize this document."},
                  ],
              }
          ],
          betas=["files-api-2025-04-14"],
      )
      print(cited_response)
      ```

      ```typescript TypeScript
      const citedResponse = await client.beta.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [
          {
            role: "user",
            content: [
              {
                type: "document",
                source: { type: "file", file_id: uploaded.id },
                title: "Document Title",
                context: "Context about the document that will not be cited from",
                citations: { enabled: true },
              },
              {
                type: "text",
                text: "Summarize this document.",
              },
            ],
          },
        ],
        betas: ["files-api-2025-04-14"],
      });
      console.log(citedResponse);
      ```

      ```csharp C#
      var citedResponse = await client.Beta.Messages.Create(
          new MessageCreateParams
          {
              Model = Messages::Model.ClaudeOpus4_8,
              MaxTokens = 1024,
              Betas = [AnthropicBeta.FilesApi2025_04_14],
              Messages =
              [
                  new BetaMessageParam
                  {
                      Role = Role.User,
                      Content = new List<BetaContentBlockParam>
                      {
                          new BetaRequestDocumentBlock
                          {
                              Source = new BetaFileDocumentSource { FileID = fileId },
                              Title = "Document Title",
                              Context = "Context about the document that will not be cited from",
                              Citations = new BetaCitationsConfigParam { Enabled = true },
                          },
                          new BetaTextBlockParam { Text = "Summarize this document." },
                      }
                  }
              ]
          });

      Console.WriteLine(citedResponse);
      ```

      ```go Go
      citedMsg, err := client.Beta.Messages.New(context.Background(),
      	anthropic.BetaMessageNewParams{
      		Model:     anthropic.ModelClaudeOpus4_8,
      		MaxTokens: 1024,
      		Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
      		Messages: []anthropic.BetaMessageParam{
      			anthropic.NewBetaUserMessage(
      				anthropic.BetaContentBlockParamUnion{
      					OfDocument: &anthropic.BetaRequestDocumentBlockParam{
      						Source: anthropic.BetaRequestDocumentBlockSourceUnionParam{
      							OfFile: &anthropic.BetaFileDocumentSourceParam{FileID: fileID},
      						},
      						Title:     anthropic.String("Document Title"),
      						Context:   anthropic.String("Context about the document that will not be cited from"),
      						Citations: anthropic.BetaCitationsConfigParam{Enabled: anthropic.Bool(true)},
      					},
      				},
      				anthropic.NewBetaTextBlock("Summarize this document."),
      			),
      		},
      	})
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Println(citedMsg)
      ```

      ```java Java
      MessageCreateParams citedParams = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .addBeta("files-api-2025-04-14")
          .maxTokens(1024)
          .addUserMessageOfBetaContentBlockParams(List.of(
              BetaContentBlockParam.ofDocument(BetaRequestDocumentBlock.builder()
                  .source(BetaFileDocumentSource.builder().fileId(fileId).build())
                  .title("Document Title")
                  .context("Context about the document that will not be cited from")
                  .citations(BetaCitationsConfigParam.builder().enabled(true).build())
                  .build()),
              BetaContentBlockParam.ofText(BetaTextBlockParam.builder()
                  .text("Summarize this document.")
                  .build())
          ))
          .build();

      BetaMessage citedMessage = client.beta().messages().create(citedParams);
      System.out.println(citedMessage);
      ```

      ```php PHP
      $citedResponse = $client->beta->messages->create(
          maxTokens: 1024,
          messages: [
              [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'document',
                          'source' => ['type' => 'file', 'file_id' => $fileId],
                          'title' => 'Document Title',
                          'context' => 'Context about the document that will not be cited from',
                          'citations' => ['enabled' => true],
                      ],
                      ['type' => 'text', 'text' => 'Summarize this document.'],
                  ],
              ],
          ],
          model: 'claude-opus-4-8',
          betas: ['files-api-2025-04-14'],
      );

      print_r($citedResponse);
      ```

      ```ruby Ruby
      cited_response = client.beta.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        betas: ["files-api-2025-04-14"],
        messages: [
          {
            role: "user",
            content: [
              {
                type: "document",
                source: { type: "file", file_id: file_id },
                title: "Document Title",
                context: "Context about the document that will not be cited from",
                citations: { enabled: true }
              },
              {
                type: "text",
                text: "Summarize this document."
              }
            ]
          }
        ]
      )

      puts cited_response
      ```
    </CodeGroup>
  </Tab>
</Tabs>

<Accordion title="Contoh sitasi teks biasa">
  ```python
  {
      "type": "char_location",
      "cited_text": "The exact text being cited",  # not counted toward output tokens
      "document_index": 0,
      "document_title": "Document Title",
      "start_char_index": 0,  # 0-indexed
      "end_char_index": 50,  # exclusive
  }
  ```
</Accordion>

### Dokumen PDF

Dokumen PDF dapat disediakan sebagai data yang dikodekan base64, URL, atau dengan `file_id`. Teks PDF diekstrak dan dipecah menjadi kalimat. Karena sitasi gambar belum didukung, PDF yang merupakan hasil pemindaian dokumen dan tidak berisi teks yang dapat diekstrak tidak akan dapat dikutip.

<Tabs>
  <Tab title="Base64">
    <CodeGroup>
      ```bash cURL
      PDF_BASE64=$(base64 /path/to/document.pdf | tr -d '\n')

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
              "content": [
                {
                  "type": "document",
                  "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": "'"$PDF_BASE64"'"
                  },
                  "title": "Document Title",
                  "context": "Context about the document that will not be cited from",
                  "citations": {"enabled": true}
                },
                {
                  "type": "text",
                  "text": "Summarize this document."
                }
              ]
            }
          ]
        }'
      ```

      ```bash CLI
      ant messages create <<'YAML'
      model: claude-opus-4-8
      max_tokens: 1024
      messages:
        - role: user
          content:
            - type: document
              source:
                type: base64
                media_type: application/pdf
                data: "@/path/to/document.pdf"
              title: Document Title
              context: Context about the document that will not be cited from
              citations:
                enabled: true
            - type: text
              text: Summarize this document.
      YAML
      ```

      ```python Python
      client = anthropic.Anthropic()

      pdf_base64 = base64.standard_b64encode(
          pathlib.Path("/path/to/document.pdf").read_bytes()
      ).decode()

      response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          messages=[
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "document",
                          "source": {
                              "type": "base64",
                              "media_type": "application/pdf",
                              "data": pdf_base64,
                          },
                          "title": "Document Title",
                          "context": "Context about the document that will not be cited from",
                          "citations": {"enabled": True},
                      },
                      {"type": "text", "text": "Summarize this document."},
                  ],
              }
          ],
      )
      print(response)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const pdfBase64 = Buffer.from(await readFile("/path/to/document.pdf")).toString("base64");

      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [
          {
            role: "user",
            content: [
              {
                type: "document",
                source: {
                  type: "base64",
                  media_type: "application/pdf",
                  data: pdfBase64
                },
                title: "Document Title",
                context: "Context about the document that will not be cited from",
                citations: { enabled: true }
              },
              {
                type: "text",
                text: "Summarize this document."
              }
            ]
          }
        ]
      });
      console.log(response);
      ```

      ```csharp C#
      var client = new AnthropicClient();

      var pdfBase64 = Convert.ToBase64String(await File.ReadAllBytesAsync("/path/to/document.pdf"));

      var response = await client.Messages.Create(
          new()
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 1024,
              Messages =
              [
                  new()
                  {
                      Role = Role.User,
                      Content = new MessageParamContent(new List<ContentBlockParam>
                      {
                          new ContentBlockParam(new DocumentBlockParam(
                              new DocumentBlockParamSource(new Base64PdfSource() { Data = pdfBase64 })
                          )
                          {
                              Title = "Document Title",
                              Context = "Context about the document that will not be cited from",
                              Citations = new CitationsConfigParam { Enabled = true },
                          }),
                          new ContentBlockParam(new TextBlockParam("Summarize this document.")),
                      }),
                  },
              ],
          }
      );

      Console.WriteLine(response);
      ```

      ```go Go
      client := anthropic.NewClient()

      pdfBytes, err := os.ReadFile("/path/to/document.pdf")
      if err != nil {
      	log.Fatal(err)
      }
      pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 1024,
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(
      			anthropic.ContentBlockParamUnion{
      				OfDocument: &anthropic.DocumentBlockParam{
      					Source: anthropic.DocumentBlockParamSourceUnion{
      						OfBase64: &anthropic.Base64PDFSourceParam{
      							Data: pdfBase64,
      						},
      					},
      					Title:     anthropic.String("Document Title"),
      					Context:   anthropic.String("Context about the document that will not be cited from"),
      					Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
      				},
      			},
      			anthropic.NewTextBlock("Summarize this document."),
      		),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Println(response)
      ```

      ```java Java
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      byte[] pdfBytes = Files.readAllBytes(Path.of("/path/to/document.pdf"));
      String pdfBase64 = Base64.getEncoder().encodeToString(pdfBytes);

      DocumentBlockParam documentParam = DocumentBlockParam.builder()
        .source(Base64PdfSource.builder().data(pdfBase64).build())
        .title("Document Title")
        .context("Context about the document that will not be cited from")
        .citations(CitationsConfigParam.builder().enabled(true).build())
        .build();

      MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024)
        .addUserMessageOfBlockParams(
          List.of(
            ContentBlockParam.ofDocument(documentParam),
            ContentBlockParam.ofText(TextBlockParam.builder().text("Summarize this document.").build())
          )
        )
        .build();

      Message message = client.messages().create(params);
      System.out.println(message);
      ```

      ```php PHP
      $client = new Client();

      $pdfBase64 = base64_encode(file_get_contents('/path/to/document.pdf'));

      $response = $client->messages->create(
          maxTokens: 1024,
          messages: [
              [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'document',
                          'source' => [
                              'type' => 'base64',
                              'media_type' => 'application/pdf',
                              'data' => $pdfBase64,
                          ],
                          'title' => 'Document Title',
                          'context' => 'Context about the document that will not be cited from',
                          'citations' => ['enabled' => true],
                      ],
                      [
                          'type' => 'text',
                          'text' => 'Summarize this document.',
                      ],
                  ],
              ],
          ],
          model: 'claude-opus-4-8',
      );

      echo json_encode($response, JSON_PRETTY_PRINT);
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      pdf_base64 = Base64.strict_encode64(File.binread("/path/to/document.pdf"))

      response = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [
          {
            role: "user",
            content: [
              {
                type: "document",
                source: {
                  type: "base64",
                  media_type: "application/pdf",
                  data: pdf_base64
                },
                title: "Document Title",
                context: "Context about the document that will not be cited from",
                citations: { enabled: true }
              },
              {
                type: "text",
                text: "Summarize this document."
              }
            ]
          }
        ]
      )

      puts response
      ```
    </CodeGroup>
  </Tab>

  <Tab title="URL">
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
              "content": [
                {
                  "type": "document",
                  "source": {
                    "type": "url",
                    "url": "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
                  },
                  "title": "Document Title",
                  "context": "Context about the document that will not be cited from",
                  "citations": {"enabled": true}
                },
                {
                  "type": "text",
                  "text": "Summarize this document."
                }
              ]
            }
          ]
        }'
      ```

      ```bash CLI
      ant messages create <<'YAML'
      model: claude-opus-4-8
      max_tokens: 1024
      messages:
        - role: user
          content:
            - type: document
              source:
                type: url
                url: https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
              title: Document Title
              context: Context about the document that will not be cited from
              citations:
                enabled: true
            - type: text
              text: Summarize this document.
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
                  "content": [
                      {
                          "type": "document",
                          "source": {
                              "type": "url",
                              "url": "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf",
                          },
                          "title": "Document Title",
                          "context": "Context about the document that will not be cited from",
                          "citations": {"enabled": True},
                      },
                      {"type": "text", "text": "Summarize this document."},
                  ],
              }
          ],
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
            content: [
              {
                type: "document",
                source: {
                  type: "url",
                  url: "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
                },
                title: "Document Title",
                context: "Context about the document that will not be cited from",
                citations: { enabled: true }
              },
              {
                type: "text",
                text: "Summarize this document."
              }
            ]
          }
        ]
      });
      console.log(response);
      ```

      ```csharp C#
      var client = new AnthropicClient();

      var response = await client.Messages.Create(
          new()
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 1024,
              Messages =
              [
                  new()
                  {
                      Role = Role.User,
                      Content = new MessageParamContent(new List<ContentBlockParam>
                      {
                          new ContentBlockParam(new DocumentBlockParam(
                              new DocumentBlockParamSource(new UrlPdfSource()
                              {
                                  Url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf",
                              })
                          )
                          {
                              Title = "Document Title",
                              Context = "Context about the document that will not be cited from",
                              Citations = new CitationsConfigParam { Enabled = true },
                          }),
                          new ContentBlockParam(new TextBlockParam("Summarize this document.")),
                      }),
                  },
              ],
          }
      );

      Console.WriteLine(response);
      ```

      ```go Go
      client := anthropic.NewClient()

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 1024,
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(
      			anthropic.ContentBlockParamUnion{
      				OfDocument: &anthropic.DocumentBlockParam{
      					Source: anthropic.DocumentBlockParamSourceUnion{
      						OfURL: &anthropic.URLPDFSourceParam{
      							URL: "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf",
      						},
      					},
      					Title:     anthropic.String("Document Title"),
      					Context:   anthropic.String("Context about the document that will not be cited from"),
      					Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
      				},
      			},
      			anthropic.NewTextBlock("Summarize this document."),
      		),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Println(response)
      ```

      ```java Java
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      DocumentBlockParam documentParam = DocumentBlockParam.builder()
        .source(UrlPdfSource.builder()
          .url("https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf")
          .build())
        .title("Document Title")
        .context("Context about the document that will not be cited from")
        .citations(CitationsConfigParam.builder().enabled(true).build())
        .build();

      MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024)
        .addUserMessageOfBlockParams(
          List.of(
            ContentBlockParam.ofDocument(documentParam),
            ContentBlockParam.ofText(TextBlockParam.builder().text("Summarize this document.").build())
          )
        )
        .build();

      Message message = client.messages().create(params);
      System.out.println(message);
      ```

      ```php PHP
      $client = new Client();

      $response = $client->messages->create(
          maxTokens: 1024,
          messages: [
              [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'document',
                          'source' => [
                              'type' => 'url',
                              'url' => 'https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf',
                          ],
                          'title' => 'Document Title',
                          'context' => 'Context about the document that will not be cited from',
                          'citations' => ['enabled' => true],
                      ],
                      [
                          'type' => 'text',
                          'text' => 'Summarize this document.',
                      ],
                  ],
              ],
          ],
          model: 'claude-opus-4-8',
      );

      echo json_encode($response, JSON_PRETTY_PRINT);
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      response = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [
          {
            role: "user",
            content: [
              {
                type: "document",
                source: {
                  type: "url",
                  url: "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
                },
                title: "Document Title",
                context: "Context about the document that will not be cited from",
                citations: { enabled: true }
              },
              {
                type: "text",
                text: "Summarize this document."
              }
            ]
          }
        ]
      )

      puts response
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Files API">
    <Note>
      Sumber dokumen Files API masih dalam tahap beta. Contoh-contoh ini menggunakan jalur klien beta; lihat [Files API](/docs/id/build-with-claude/files) untuk detail pengunggahan.
    </Note>

    <CodeGroup>
      ```bash cURL
      curl -X POST https://api.anthropic.com/v1/messages \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: files-api-2025-04-14" \
        -H "content-type: application/json" \
        -d @- <<EOF
      {
        "model": "claude-opus-4-8",
        "max_tokens": 1024,
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "document",
                "source": {"type": "file", "file_id": "$FILE_ID"},
                "title": "Document Title",
                "context": "Context about the document that will not be cited from",
                "citations": {"enabled": true}
              },
              {
                "type": "text",
                "text": "Summarize this document."
              }
            ]
          }
        ]
      }
      EOF
      ```

      ```bash CLI
      ant beta:messages create --beta files-api-2025-04-14 <<YAML
      model: claude-opus-4-8
      max_tokens: 1024
      messages:
        - role: user
          content:
            - type: document
              source:
                type: file
                file_id: $FILE_ID
              title: Document Title
              context: Context about the document that will not be cited from
              citations:
                enabled: true
            - type: text
              text: Summarize this document.
      YAML
      ```

      ```python Python
      cited_response = client.beta.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          messages=[
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "document",
                          "source": {"type": "file", "file_id": file_id},
                          "title": "Document Title",
                          "context": "Context about the document that will not be cited from",
                          "citations": {"enabled": True},
                      },
                      {"type": "text", "text": "Summarize this document."},
                  ],
              }
          ],
          betas=["files-api-2025-04-14"],
      )
      print(cited_response)
      ```

      ```typescript TypeScript
      const citedResponse = await client.beta.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [
          {
            role: "user",
            content: [
              {
                type: "document",
                source: { type: "file", file_id: uploaded.id },
                title: "Document Title",
                context: "Context about the document that will not be cited from",
                citations: { enabled: true },
              },
              {
                type: "text",
                text: "Summarize this document.",
              },
            ],
          },
        ],
        betas: ["files-api-2025-04-14"],
      });
      console.log(citedResponse);
      ```

      ```csharp C#
      var citedResponse = await client.Beta.Messages.Create(
          new MessageCreateParams
          {
              Model = Messages::Model.ClaudeOpus4_8,
              MaxTokens = 1024,
              Betas = [AnthropicBeta.FilesApi2025_04_14],
              Messages =
              [
                  new BetaMessageParam
                  {
                      Role = Role.User,
                      Content = new List<BetaContentBlockParam>
                      {
                          new BetaRequestDocumentBlock
                          {
                              Source = new BetaFileDocumentSource { FileID = fileId },
                              Title = "Document Title",
                              Context = "Context about the document that will not be cited from",
                              Citations = new BetaCitationsConfigParam { Enabled = true },
                          },
                          new BetaTextBlockParam { Text = "Summarize this document." },
                      }
                  }
              ]
          });

      Console.WriteLine(citedResponse);
      ```

      ```go Go
      citedMsg, err := client.Beta.Messages.New(context.Background(),
      	anthropic.BetaMessageNewParams{
      		Model:     anthropic.ModelClaudeOpus4_8,
      		MaxTokens: 1024,
      		Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
      		Messages: []anthropic.BetaMessageParam{
      			anthropic.NewBetaUserMessage(
      				anthropic.BetaContentBlockParamUnion{
      					OfDocument: &anthropic.BetaRequestDocumentBlockParam{
      						Source: anthropic.BetaRequestDocumentBlockSourceUnionParam{
      							OfFile: &anthropic.BetaFileDocumentSourceParam{FileID: fileID},
      						},
      						Title:     anthropic.String("Document Title"),
      						Context:   anthropic.String("Context about the document that will not be cited from"),
      						Citations: anthropic.BetaCitationsConfigParam{Enabled: anthropic.Bool(true)},
      					},
      				},
      				anthropic.NewBetaTextBlock("Summarize this document."),
      			),
      		},
      	})
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Println(citedMsg)
      ```

      ```java Java
      MessageCreateParams citedParams = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .addBeta("files-api-2025-04-14")
          .maxTokens(1024)
          .addUserMessageOfBetaContentBlockParams(List.of(
              BetaContentBlockParam.ofDocument(BetaRequestDocumentBlock.builder()
                  .source(BetaFileDocumentSource.builder().fileId(fileId).build())
                  .title("Document Title")
                  .context("Context about the document that will not be cited from")
                  .citations(BetaCitationsConfigParam.builder().enabled(true).build())
                  .build()),
              BetaContentBlockParam.ofText(BetaTextBlockParam.builder()
                  .text("Summarize this document.")
                  .build())
          ))
          .build();

      BetaMessage citedMessage = client.beta().messages().create(citedParams);
      System.out.println(citedMessage);
      ```

      ```php PHP
      $citedResponse = $client->beta->messages->create(
          maxTokens: 1024,
          messages: [
              [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'document',
                          'source' => ['type' => 'file', 'file_id' => $fileId],
                          'title' => 'Document Title',
                          'context' => 'Context about the document that will not be cited from',
                          'citations' => ['enabled' => true],
                      ],
                      ['type' => 'text', 'text' => 'Summarize this document.'],
                  ],
              ],
          ],
          model: 'claude-opus-4-8',
          betas: ['files-api-2025-04-14'],
      );

      print_r($citedResponse);
      ```

      ```ruby Ruby
      cited_response = client.beta.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        betas: ["files-api-2025-04-14"],
        messages: [
          {
            role: "user",
            content: [
              {
                type: "document",
                source: { type: "file", file_id: file_id },
                title: "Document Title",
                context: "Context about the document that will not be cited from",
                citations: { enabled: true }
              },
              {
                type: "text",
                text: "Summarize this document."
              }
            ]
          }
        ]
      )

      puts cited_response
      ```
    </CodeGroup>
  </Tab>
</Tabs>

<Accordion title="Contoh sitasi PDF">
  ```python
  {
      "type": "page_location",
      "cited_text": "The exact text being cited",  # not counted toward output tokens
      "document_index": 0,
      "document_title": "Document Title",
      "start_page_number": 1,  # 1-indexed
      "end_page_number": 2,  # exclusive
  }
  ```
</Accordion>

### Dokumen konten kustom

Dokumen konten kustom memberi Anda kontrol atas granularitas sitasi. Tidak ada pemecahan tambahan yang dilakukan dan chunk disediakan ke model sesuai dengan blok konten yang diberikan.

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
          "content": [
            {
              "type": "document",
              "source": {
                "type": "content",
                "content": [
                  {"type": "text", "text": "First chunk"},
                  {"type": "text", "text": "Second chunk"}
                ]
              },
              "title": "Document Title",
              "context": "Context about the document that will not be cited from",
              "citations": {"enabled": true}
            },
            {
              "type": "text",
              "text": "Summarize this document."
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: document
          source:
            type: content
            content:
              - type: text
                text: First chunk
              - type: text
                text: Second chunk
          title: Document Title
          context: Context about the document that will not be cited from
          citations:
            enabled: true
        - type: text
          text: Summarize this document.
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
              "content": [
                  {
                      "type": "document",
                      "source": {
                          "type": "content",
                          "content": [
                              {"type": "text", "text": "First chunk"},
                              {"type": "text", "text": "Second chunk"},
                          ],
                      },
                      "title": "Document Title",
                      "context": "Context about the document that will not be cited from",
                      "citations": {"enabled": True},
                  },
                  {"type": "text", "text": "Summarize this document."},
              ],
          }
      ],
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
        content: [
          {
            type: "document",
            source: {
              type: "content",
              content: [
                { type: "text", text: "First chunk" },
                { type: "text", text: "Second chunk" }
              ]
            },
            title: "Document Title",
            context: "Context about the document that will not be cited from",
            citations: { enabled: true }
          },
          {
            type: "text",
            text: "Summarize this document."
          }
        ]
      }
    ]
  });
  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var response = await client.Messages.Create(
      new()
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = new MessageParamContent(new List<ContentBlockParam>
                  {
                      new ContentBlockParam(new DocumentBlockParam(
                          new DocumentBlockParamSource(new ContentBlockSource()
                          {
                              Content = new ContentBlockSourceContent(new List<MessageContentBlockSourceContent>
                              {
                                  new TextBlockParam("First chunk"),
                                  new TextBlockParam("Second chunk"),
                              }),
                          })
                      )
                      {
                          Title = "Document Title",
                          Context = "Context about the document that will not be cited from",
                          Citations = new CitationsConfigParam { Enabled = true },
                      }),
                      new ContentBlockParam(new TextBlockParam("Summarize this document.")),
                  }),
              },
          ],
      }
  );

  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.ContentBlockParamUnion{
  				OfDocument: &anthropic.DocumentBlockParam{
  					Source: anthropic.DocumentBlockParamSourceUnion{
  						OfContent: &anthropic.ContentBlockSourceParam{
  							Content: anthropic.ContentBlockSourceContentUnionParam{
  								OfContentBlockSourceContent: []anthropic.ContentBlockSourceContentItemUnionParam{
  									{OfText: &anthropic.TextBlockParam{Text: "First chunk"}},
  									{OfText: &anthropic.TextBlockParam{Text: "Second chunk"}},
  								},
  							},
  						},
  					},
  					Title:     anthropic.String("Document Title"),
  					Context:   anthropic.String("Context about the document that will not be cited from"),
  					Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  				},
  			},
  			anthropic.NewTextBlock("Summarize this document."),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  DocumentBlockParam documentParam = DocumentBlockParam.builder()
    .source(ContentBlockSource.builder()
      .contentOfBlockSource(
        List.of(
          ContentBlockSourceContent.ofText(TextBlockParam.builder().text("First chunk").build()),
          ContentBlockSourceContent.ofText(TextBlockParam.builder().text("Second chunk").build())
        )
      )
      .build())
    .title("Document Title")
    .context("Context about the document that will not be cited from")
    .citations(CitationsConfigParam.builder().enabled(true).build())
    .build();

  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_8)
    .maxTokens(1024)
    .addUserMessageOfBlockParams(
      List.of(
        ContentBlockParam.ofDocument(documentParam),
        ContentBlockParam.ofText(TextBlockParam.builder().text("Summarize this document.").build())
      )
    )
    .build();

  Message message = client.messages().create(params);
  System.out.println(message);
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'content',
                          'content' => [
                              ['type' => 'text', 'text' => 'First chunk'],
                              ['type' => 'text', 'text' => 'Second chunk'],
                          ],
                      ],
                      'title' => 'Document Title',
                      'context' => 'Context about the document that will not be cited from',
                      'citations' => ['enabled' => true],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'Summarize this document.',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
  );

  echo json_encode($response, JSON_PRETTY_PRINT);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "content",
              content: [
                { type: "text", text: "First chunk" },
                { type: "text", text: "Second chunk" }
              ]
            },
            title: "Document Title",
            context: "Context about the document that will not be cited from",
            citations: { enabled: true }
          },
          {
            type: "text",
            text: "Summarize this document."
          }
        ]
      }
    ]
  )

  puts response
  ```
</CodeGroup>

<Accordion title="Contoh sitasi">
  ```python
  {
      "type": "content_block_location",
      "cited_text": "The exact text being cited",  # not counted toward output tokens
      "document_index": 0,
      "document_title": "Document Title",
      "start_block_index": 0,  # 0-indexed
      "end_block_index": 1,  # exclusive
  }
  ```
</Accordion>

***

## Struktur respons

Ketika citations diaktifkan, respons mencakup beberapa blok teks dengan citations:

```python
{
    "content": [
        {"type": "text", "text": "According to the document, "},
        {
            "type": "text",
            "text": "the grass is green",
            "citations": [
                {
                    "type": "char_location",
                    "cited_text": "The grass is green.",
                    "document_index": 0,
                    "document_title": "Example Document",
                    "start_char_index": 0,
                    "end_char_index": 20,
                }
            ],
        },
        {"type": "text", "text": " and "},
        {
            "type": "text",
            "text": "the sky is blue",
            "citations": [
                {
                    "type": "char_location",
                    "cited_text": "The sky is blue.",
                    "document_index": 0,
                    "document_title": "Example Document",
                    "start_char_index": 20,
                    "end_char_index": 36,
                }
            ],
        },
        {
            "type": "text",
            "text": ". Information from page 5 states that ",
        },
        {
            "type": "text",
            "text": "water is essential",
            "citations": [
                {
                    "type": "page_location",
                    "cited_text": "Water is essential for life.",
                    "document_index": 1,
                    "document_title": "PDF Document",
                    "start_page_number": 5,
                    "end_page_number": 6,
                }
            ],
        },
        {
            "type": "text",
            "text": ". The custom document mentions ",
        },
        {
            "type": "text",
            "text": "important findings",
            "citations": [
                {
                    "type": "content_block_location",
                    "cited_text": "These are important findings.",
                    "document_index": 2,
                    "document_title": "Custom Content Document",
                    "start_block_index": 0,
                    "end_block_index": 1,
                }
            ],
        },
    ]
}
```

### Dukungan streaming

Untuk respons streaming, citations tiba sebagai tipe delta `citations_delta` di dalam event `content_block_delta`. Setiap delta berisi satu sitasi untuk ditambahkan ke daftar `citations` pada blok konten `text` saat ini.

<AccordionGroup>
  <Accordion title="Contoh event streaming">
    ```sse
    event: message_start
    data: {"type": "message_start", ...}

    event: content_block_start
    data: {"type": "content_block_start", "index": 0, ...}

    event: content_block_delta
    data: {"type": "content_block_delta", "index": 0,
           "delta": {"type": "text_delta", "text": "According to..."}}

    event: content_block_delta
    data: {"type": "content_block_delta", "index": 0,
           "delta": {"type": "citations_delta",
                     "citation": {
                         "type": "char_location",
                         "cited_text": "...",
                         "document_index": 0,
                         ...
                     }}}

    event: content_block_stop
    data: {"type": "content_block_stop", "index": 0}

    event: message_stop
    data: {"type": "message_stop"}
    ```
  </Accordion>
</AccordionGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Streaming pesan" icon="wifi-high" href="/docs/id/build-with-claude/streaming">
    Tangani tipe delta `citations_delta` bersama dengan delta teks untuk merender respons yang dikutip saat di-streaming.
  </Card>

  <Card title="Hasil pencarian" icon="book-bookmark" href="/docs/id/build-with-claude/search-results">
    Teruskan hasil pencarian dari pipeline RAG Anda sebagai blok konten kelas satu dengan dukungan sitasi bawaan.
  </Card>

  <Card title="Dukungan PDF" icon="file" href="/docs/id/build-with-claude/pdf-support">
    Pelajari bagaimana Claude mengekstrak teks dari PDF dan bagaimana sitasi berbasis halaman dipetakan kembali ke file sumber Anda.
  </Card>

  <Card title="Files API" icon="hard-drives" href="/docs/id/build-with-claude/files">
    Unggah dokumen sekali dan rujuk dengan `file_id` di beberapa permintaan sitasi.
  </Card>
</CardGroup>
