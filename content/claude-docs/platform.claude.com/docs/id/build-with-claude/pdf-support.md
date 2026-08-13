---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/pdf-support
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 5595ee89b03a0c01c86d8e9f093263994c25257348c67d007890f13a90d85a48
---

---
title: Dukungan PDF
url: https://platform.claude.com/docs/id/build-with-claude/pdf-support
description: "Proses PDF dengan Claude: ekstrak teks, analisis grafik, dan pahami konten visual dari dokumen Anda."
---

## Compatibility
- [ZDR](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention): eligible (excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements))
- Platforms: Claude API, Claude Platform on AWS, Amazon Bedrock, Google Cloud, Microsoft Foundry

Anda dapat bertanya kepada Claude tentang teks, gambar, grafik, dan tabel apa pun dalam PDF yang Anda berikan. Beberapa contoh kasus penggunaan:

* Menganalisis laporan keuangan dan memahami grafik/tabel
* Mengekstrak informasi penting dari dokumen hukum
* Membantu penerjemahan dokumen
* Mengonversi informasi dokumen menjadi format terstruktur

## Sebelum Anda mulai

### Periksa persyaratan PDF

Claude bekerja dengan PDF standar apa pun. Pastikan ukuran permintaan Anda memenuhi persyaratan berikut:

| Persyaratan                     | Batas                                                                                                           |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Ukuran permintaan maksimum      | 32 MB ([bervariasi berdasarkan platform](https://platform.claude.com/docs/id/api/overview#request-size-limits)) |
| Halaman maksimum per permintaan | 600 (100 jika jendela konteks permintaan di bawah 1 juta token)                                                 |
| Format                          | PDF standar (tanpa kata sandi/enkripsi)                                                                         |

Kedua batas tersebut berlaku untuk seluruh payload permintaan, termasuk konten lain yang dikirim bersama PDF. Untuk PDF berukuran besar, pertimbangkan untuk mengunggah dengan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) dan mereferensikannya melalui `file_id` agar payload permintaan tetap kecil.

<Tip>
  PDF yang padat (banyak halaman dengan font kecil, tabel kompleks, atau grafik berat) dapat memenuhi jendela konteks sebelum mencapai batas halaman. Permintaan dengan PDF besar juga dapat gagal sebelum mencapai batas halaman, bahkan saat menggunakan Files API. Coba pisahkan dokumen menjadi beberapa bagian; untuk file besar, karena setiap halaman diproses sebagai gambar, menurunkan resolusi gambar yang disematkan juga dapat membantu.
</Tip>

Karena dukungan PDF bergantung pada kemampuan vision Claude, dukungan ini tunduk pada [batasan dan pertimbangan](https://platform.claude.com/docs/id/build-with-claude/vision#limitations) yang sama seperti tugas vision lainnya.

### Platform dan model yang didukung

Semua [model aktif](https://platform.claude.com/docs/id/about-claude/models/overview) mendukung pemrosesan PDF. Untuk dukungan PDF melalui Converse API Amazon Bedrock, lihat [Dukungan PDF Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/pdf-support#amazon-bedrock-pdf-support).

### Dukungan PDF Amazon Bedrock

Saat menggunakan dukungan PDF melalui Converse API, bagian dari [Claude di Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), terdapat dua mode pemrosesan dokumen yang berbeda:

<Note>
  **Penting:** Untuk mengakses kemampuan pemahaman PDF visual penuh dari Claude di Converse API, Anda harus mengaktifkan sitasi. Tanpa sitasi diaktifkan, API akan kembali ke ekstraksi teks dasar saja. Pelajari lebih lanjut tentang [bekerja dengan sitasi](https://platform.claude.com/docs/id/build-with-claude/citations).
</Note>

#### Mode pemrosesan dokumen

1. **Converse Document Chat** (Mode asli - Ekstraksi teks saja)

   * Menyediakan ekstraksi teks dasar dari PDF
   * Tidak dapat menganalisis gambar, grafik, atau tata letak visual dalam PDF
   * Menggunakan sekitar 1.000 token untuk PDF 3 halaman
   * Digunakan secara otomatis ketika sitasi tidak diaktifkan

2. **Claude PDF Chat** (Mode baru - Pemahaman visual penuh)

   * Menyediakan analisis visual lengkap dari PDF
   * Dapat memahami dan menganalisis grafik, diagram, gambar, dan tata letak visual
   * Memproses setiap halaman sebagai teks dan gambar untuk pemahaman yang komprehensif
   * Menggunakan sekitar 7.000 token untuk PDF 3 halaman
   * **Memerlukan sitasi diaktifkan** di Converse API

#### Batasan utama

* **Converse API:** Analisis PDF visual memerlukan sitasi diaktifkan. Saat ini tidak ada opsi untuk menggunakan analisis visual tanpa sitasi (tidak seperti InvokeModel API).
* **InvokeModel API:** Memberikan kontrol penuh atas pemrosesan PDF tanpa sitasi yang dipaksakan.

#### Masalah umum

Jika Claude tidak melihat gambar atau grafik dalam PDF Anda saat menggunakan Converse API, kemungkinan Anda perlu mengaktifkan flag sitasi. Tanpa itu, Converse kembali ke ekstraksi teks dasar saja.

<Note>
  Ini adalah kendala yang diketahui pada Converse API. Untuk aplikasi yang memerlukan analisis PDF visual tanpa sitasi, pertimbangkan untuk menggunakan InvokeModel API sebagai gantinya.
</Note>

<Note>
  File teks biasa seperti .txt, .csv, atau .md dapat digunakan langsung dalam blok dokumen: unggah ke Files API dengan tipe MIME `text/plain` dan referensikan melalui `file_id`. Format biner seperti .xlsx atau .docx tidak didukung dalam blok dokumen dan harus dikonversi ke teks atau PDF terlebih dahulu. Lihat [Bekerja dengan format file lain](https://platform.claude.com/docs/id/build-with-claude/files#working-with-other-file-formats).
</Note>

## Memproses PDF dengan Claude

### Kirim permintaan PDF pertama Anda

Mulailah dengan contoh sederhana menggunakan Messages API. Anda dapat memberikan PDF kepada Claude dengan tiga cara:

1. Sebagai referensi URL ke PDF yang di-host secara online
2. Sebagai PDF yang dienkode base64 dalam blok konten `document`
3. Melalui `file_id` dari [Files API](https://platform.claude.com/docs/id/build-with-claude/files)

<Note>
  Di Amazon Bedrock dan Google Cloud, saat ini hanya sumber yang dienkode base64 yang tersedia. Di Microsoft Foundry, Files API tidak didukung untuk deployment yang di-host di Azure.
</Note>

#### Opsi 1: Dokumen PDF berbasis URL

Pendekatan paling sederhana adalah mereferensikan PDF langsung dari URL:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [{
          "role": "user",
          "content": [{
              "type": "document",
              "source": {
                  "type": "url",
                  "url": "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
              }
          },
          {
              "type": "text",
              "text": "What are the key findings in this document?"
          }]
      }]
  }'
  ```

  ```bash CLI
  ant messages create --transform content --format yaml <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: document
          source:
            type: url
            url: https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
        - type: text
          text: What are the key findings in this document?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()
  message = client.messages.create(
      model="claude-opus-5",
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
                  },
                  {"type": "text", "text": "What are the key findings in this document?"},
              ],
          }
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const response = await anthropic.messages.create({
    model: "claude-opus-5",
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
            }
          },
          {
            type: "text",
            text: "What are the key findings in this document?"
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  // Buat blok dokumen dengan URL
  var documentParam = new DocumentBlockParam
  {
      Source = new UrlPdfSource
      {
          Url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf",
      },
  };

  // Buat pesan dengan blok konten dokumen dan teks
  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new List<ContentBlockParam>
              {
                  documentParam,
                  new TextBlockParam("What are the key findings in this document?"),
              },
          },
      ],
  });

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewDocumentBlock(anthropic.URLPDFSourceParam{
  				URL: "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf",
  			}),
  			anthropic.NewTextBlock("What are the key findings in this document?"),
  		),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Buat blok dokumen dengan URL
  DocumentBlockParam documentParam = DocumentBlockParam.builder()
    .source(
      UrlPdfSource.builder()
        .url(
          "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
        )
        .build()
    )
    .build();

  // Buat pesan dengan blok konten dokumen dan teks
  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_5)
    .maxTokens(1024)
    .addUserMessageOfBlockParams(
      List.of(
        ContentBlockParam.ofDocument(documentParam),
        ContentBlockParam.ofText(
          TextBlockParam.builder()
            .text("What are the key findings in this document?")
            .build()
        )
      )
    )
    .build();

  Message message = client.messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
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
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What are the key findings in this document?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-5',
  );

  echo $message;
  ```

  ```ruby Ruby
  anthropic = Anthropic::Client.new

  message = anthropic.messages.create(
    model: "claude-opus-5",
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
            }
          },
          {type: "text", text: "What are the key findings in this document?"}
        ]
      }
    ]
  )

  puts(message.content)
  ```
</CodeGroup>

Respons mengembalikan analisis Claude sebagai blok teks dalam `content`, dengan konsumsi token dalam `usage`:

```json Output
{
  "id": "msg_01Hfp8YuFjQ55VgWbpdHDehB",
  "type": "message",
  "role": "assistant",
  "model": "claude-opus-5",
  "content": [
    {
      "type": "text",
      "text": "This document is an addendum to the Claude 3 model card, reporting updated evaluation results. The key findings include..."
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 45000,
    "output_tokens": 300
  }
}
```

#### Opsi 2: Dokumen PDF yang dienkode base64

Jika Anda perlu mengirim PDF dari sistem lokal Anda atau ketika URL tidak tersedia:

<CodeGroup>
  ```bash cURL
  # Metode 1: Ambil dan enkode PDF jarak jauh
  curl -sL "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt

  # Metode 2: Enkode file PDF lokal
  # base64 document.pdf | tr -d '\n' > pdf_base64.txt

  # Buat file permintaan JSON menggunakan konten pdf_base64.txt
  jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [{
          "role": "user",
          "content": [{
              "type": "document",
              "source": {
                  "type": "base64",
                  "media_type": "application/pdf",
                  "data": $PDF_BASE64
              }
          },
          {
              "type": "text",
              "text": "What are the key findings in this document?"
          }]
      }]
  }' > request.json

  # Kirim permintaan API menggunakan file JSON tersebut
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d @request.json
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --transform content \
    --format yaml <<'YAML'
  messages:
    - role: user
      content:
        - type: document
          source:
            type: base64
            media_type: application/pdf
            data: "@./document.pdf"
        - type: text
          text: What are the key findings in this document?
  YAML
  ```

  ```python Python
  import base64
  import httpx

  # Pertama, muat dan enkode PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_data = base64.standard_b64encode(
      httpx.get(pdf_url, follow_redirects=True).content
  ).decode("utf-8")

  # Alternatif: Muat dari file lokal
  # with open("document.pdf", "rb") as f:
  #     pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

  # Kirim ke Claude menggunakan enkode base64
  client = anthropic.Anthropic()
  message = client.messages.create(
      model="claude-opus-5",
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
                          "data": pdf_data,
                      },
                  },
                  {"type": "text", "text": "What are the key findings in this document?"},
              ],
          }
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  // Metode 1: Ambil dan enkode PDF jarak jauh
  const pdfURL =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  const pdfResponse = await fetch(pdfURL);
  const arrayBuffer = await pdfResponse.arrayBuffer();
  const pdfBase64 = Buffer.from(arrayBuffer).toString("base64");

  // Metode 2: Muat dari file lokal
  // import { readFile } from "node:fs/promises";
  // const pdfBase64 = (await readFile('document.pdf')).toString('base64');

  // Kirim permintaan API dengan PDF yang dienkode base64
  const anthropic = new Anthropic();
  const response = await anthropic.messages.create({
    model: "claude-opus-5",
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
            }
          },
          {
            type: "text",
            text: "What are the key findings in this document?"
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  // Metode 1: Unduh dan enkode PDF jarak jauh
  var pdfUrl = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  using var httpClient = new HttpClient();
  var pdfBase64 = Convert.ToBase64String(await httpClient.GetByteArrayAsync(pdfUrl));

  // Metode 2: Muat dari file lokal
  // var pdfBase64 = Convert.ToBase64String(await File.ReadAllBytesAsync("document.pdf"));

  // Buat blok dokumen dengan data base64
  var documentParam = new DocumentBlockParam
  {
      Source = new Base64PdfSource { Data = pdfBase64 },
  };

  // Buat pesan dengan blok konten dokumen dan teks
  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new List<ContentBlockParam>
              {
                  documentParam,
                  new TextBlockParam("What are the key findings in this document?"),
              },
          },
      ],
  });

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  // Pertama, muat dan enkode PDF
  pdfURL := "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  resp, err := http.Get(pdfURL)
  if err != nil {
  	panic(err)
  }
  defer resp.Body.Close()
  pdfBytes, err := io.ReadAll(resp.Body)
  if err != nil {
  	panic(err)
  }
  pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

  // Alternatif: Muat dari file lokal (tambahkan "os" ke impor)
  // pdfBytes, err := os.ReadFile("document.pdf")
  // pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

  // Kirim ke Claude menggunakan enkode base64
  client := anthropic.NewClient()
  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewDocumentBlock(anthropic.Base64PDFSourceParam{
  				Data: pdfBase64,
  			}),
  			anthropic.NewTextBlock("What are the key findings in this document?"),
  		),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Metode 1: Unduh dan enkode PDF jarak jauh
  String pdfUrl =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  HttpClient httpClient = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NORMAL).build();
  HttpRequest request = HttpRequest.newBuilder().uri(URI.create(pdfUrl)).GET().build();

  HttpResponse<byte[]> response = httpClient.send(
    request,
    HttpResponse.BodyHandlers.ofByteArray()
  );
  String pdfBase64 = Base64.getEncoder().encodeToString(response.body());

  // Metode 2: Muat dari file lokal
  // byte[] fileBytes = Files.readAllBytes(Path.of("document.pdf"));
  // String pdfBase64 = Base64.getEncoder().encodeToString(fileBytes);

  // Buat blok dokumen dengan data base64
  DocumentBlockParam documentParam = DocumentBlockParam.builder()
    .source(Base64PdfSource.builder().data(pdfBase64).build())
    .build();

  // Buat pesan dengan blok konten dokumen dan teks
  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_5)
    .maxTokens(1024)
    .addUserMessageOfBlockParams(
      List.of(
        ContentBlockParam.ofDocument(documentParam),
        ContentBlockParam.ofText(
          TextBlockParam.builder()
            .text("What are the key findings in this document?")
            .build()
        )
      )
    )
    .build();

  Message message = client.messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  // Pertama, muat dan enkode PDF
  $pdf_url = 'https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf';
  $pdf_data = base64_encode(file_get_contents($pdf_url));

  // Alternatif: Muat dari file lokal
  // $pdf_data = base64_encode(file_get_contents('document.pdf'));

  // Kirim ke Claude menggunakan enkode base64
  $message = $client->messages->create(
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
                          'data' => $pdf_data,
                      ],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What are the key findings in this document?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-5',
  );

  echo $message;
  ```

  ```ruby Ruby
  require "open-uri"

  # Pertama, muat dan enkode PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_bytes = URI.open(pdf_url, "rb") { |f| f.read }
  pdf_data = [pdf_bytes].pack("m0") # Base64-encode without newlines

  # Alternatif: Muat dari file lokal
  # pdf_data = [File.binread("document.pdf")].pack("m0")

  # Kirim ke Claude menggunakan enkode base64
  anthropic = Anthropic::Client.new
  message = anthropic.messages.create(
    model: "claude-opus-5",
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
              data: pdf_data
            }
          },
          {type: "text", text: "What are the key findings in this document?"}
        ]
      }
    ]
  )

  puts(message.content)
  ```
</CodeGroup>

#### Opsi 3: Files API

Untuk PDF yang akan Anda gunakan berulang kali, atau ketika Anda ingin menghindari overhead encoding, gunakan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) (beta):

<CodeGroup>
  ```bash cURL
  # Pertama, unggah PDF Anda ke Files API
  FILE_ID=$(curl -sS -X POST https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -F "file=@document.pdf" | jq -r '.id')

  # Kemudian gunakan file_id yang dikembalikan dalam pesan Anda
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -d @- <<EOF
  {
    "model": "claude-opus-5",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": [{
        "type": "document",
        "source": {
          "type": "file",
          "file_id": "$FILE_ID"
        }
      },
      {
        "type": "text",
        "text": "What are the key findings in this document?"
      }]
    }]
  }
  EOF
  ```

  ```bash CLI
  # Pertama, unggah PDF Anda ke Files API
  FILE_ID=$(ant beta:files upload \
    --file ./document.pdf \
    --transform id \
    --raw-output)

  # Kemudian gunakan file_id yang dikembalikan dalam pesan Anda
  ant beta:messages create \
    --beta files-api-2025-04-14 \
    --transform content \
    --format yaml <<YAML
  model: claude-opus-5
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: document
          source:
            type: file
            file_id: $FILE_ID
        - type: text
          text: What are the key findings in this document?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Unggah file PDF
  with open("/path/to/document.pdf", "rb") as f:
      file_upload = client.beta.files.upload(file=("document.pdf", f, "application/pdf"))

  # Gunakan file yang diunggah dalam pesan
  message = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      betas=["files-api-2025-04-14"],
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "document",
                      "source": {"type": "file", "file_id": file_upload.id},
                  },
                  {"type": "text", "text": "What are the key findings in this document?"},
              ],
          }
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  import Anthropic, { toFile } from "@anthropic-ai/sdk";
  import fs from "node:fs";

  const anthropic = new Anthropic();

  // Unggah file PDF
  const fileUpload = await anthropic.beta.files.upload({
    file: await toFile(fs.createReadStream("/path/to/document.pdf"), undefined, {
      type: "application/pdf"
    })
  });

  // Gunakan file yang diunggah dalam pesan
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    betas: ["files-api-2025-04-14"],
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "file",
              file_id: fileUpload.id
            }
          },
          {
            type: "text",
            text: "What are the key findings in this document?"
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  using Messages = Anthropic.Models.Messages;

  var client = new AnthropicClient();

  // Unggah file PDF
  var fileUpload = await client.Beta.Files.Upload(new FileUploadParams
  {
      File = new BinaryContent
      {
          Stream = File.OpenRead("/path/to/document.pdf"),
          FileName = "document.pdf",
          ContentType = new("application/pdf"),
      },
  });

  // Gunakan file yang diunggah dalam pesan
  var message = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus5,
      MaxTokens = 1024,
      Betas = [AnthropicBeta.FilesApi2025_04_14],
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new List<BetaContentBlockParam>
              {
                  new BetaRequestDocumentBlock
                  {
                      Source = new BetaFileDocumentSource { FileID = fileUpload.ID },
                  },
                  new BetaTextBlockParam("What are the key findings in this document?"),
              },
          },
      ],
  });

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  client := anthropic.NewClient()

  // Unggah file PDF
  pdfFile, err := os.Open("/path/to/document.pdf")
  if err != nil {
  	panic(err)
  }
  defer pdfFile.Close()

  fileUpload, err := client.Beta.Files.Upload(context.TODO(), anthropic.BetaFileUploadParams{
  	File: anthropic.File(pdfFile, "document.pdf", "application/pdf"),
  })
  if err != nil {
  	panic(err)
  }

  // Gunakan file yang diunggah dalam pesan
  message, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(
  			anthropic.NewBetaDocumentBlock(anthropic.BetaFileDocumentSourceParam{
  				FileID: fileUpload.ID,
  			}),
  			anthropic.NewBetaTextBlock("What are the key findings in this document?"),
  		),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Unggah file PDF
  FileMetadata file = client
    .beta()
    .files()
    .upload(FileUploadParams.builder().file(Path.of("/path/to/document.pdf")).build());

  // Gunakan file yang diunggah dalam pesan
  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_5)
    .addBeta("files-api-2025-04-14")
    .maxTokens(1024)
    .addUserMessageOfBetaContentBlockParams(
      List.of(
        BetaContentBlockParam.ofDocument(
          BetaRequestDocumentBlock.builder()
            .source(
              BetaFileDocumentSource.builder()
                .fileId(file.id())
                .build()
            )
            .build()
        ),
        BetaContentBlockParam.ofText(
          BetaTextBlockParam.builder()
            .text("What are the key findings in this document?")
            .build()
        )
      )
    )
    .build();

  BetaMessage message = client.beta().messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  use Anthropic\Core\FileParam;

  $client = new Client();

  // Unggah file PDF
  $file_upload = $client->beta->files->upload(
      file: FileParam::fromResource(fopen('/path/to/document.pdf', 'r'), contentType: 'application/pdf'),
  );

  // Gunakan file yang diunggah dalam pesan
  $message = $client->beta->messages->create(
      maxTokens: 1024,
      betas: ['files-api-2025-04-14'],
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'file',
                          'file_id' => $file_upload->id,
                      ],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What are the key findings in this document?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-5',
  );

  echo $message;
  ```

  ```ruby Ruby
  anthropic = Anthropic::Client.new

  # Unggah file PDF
  file_upload = File.open("/path/to/document.pdf", "rb") do |f|
    anthropic.beta.files.upload(
      file: Anthropic::FilePart.new(f, filename: "document.pdf", content_type: "application/pdf")
    )
  end

  # Gunakan file yang diunggah dalam pesan
  message = anthropic.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    betas: ["files-api-2025-04-14"],
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {type: "file", file_id: file_upload.id}
          },
          {type: "text", text: "What are the key findings in this document?"}
        ]
      }
    ]
  )

  puts(message.content)
  ```
</CodeGroup>

### Cara kerja dukungan PDF

Ketika Anda mengirim PDF ke Claude, langkah-langkah berikut terjadi:

<Steps>
  <Step title="Sistem mengekstrak konten dokumen.">
    * Sistem mengonversi setiap halaman dokumen menjadi gambar.
    * Teks dari setiap halaman diekstrak dan disediakan bersama gambar setiap halaman.
  </Step>

  <Step title="Claude menganalisis teks dan gambar untuk memahami dokumen dengan lebih baik.">
    * Dokumen disediakan sebagai kombinasi teks dan gambar untuk analisis.
    * Ini memungkinkan pengguna untuk meminta wawasan tentang elemen visual PDF, seperti grafik, diagram, dan konten non-tekstual lainnya.
  </Step>

  <Step title="Claude merespons, mereferensikan konten PDF jika relevan.">
    Claude dapat mereferensikan konten tekstual dan visual saat merespons. Anda dapat lebih meningkatkan kinerja dengan mengintegrasikan dukungan PDF dengan:

    * [Gunakan caching prompt](https://platform.claude.com/docs/id/build-with-claude/pdf-support#use-prompt-caching): Untuk meningkatkan kinerja pada analisis berulang.
    * [Proses batch dokumen](https://platform.claude.com/docs/id/build-with-claude/pdf-support#process-document-batches): Untuk pemrosesan dokumen bervolume tinggi.
    * [Penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview): Untuk mengekstrak informasi spesifik dari dokumen untuk digunakan sebagai input alat.
  </Step>
</Steps>

### Perkirakan biaya Anda

Jumlah token dari file PDF bergantung pada total teks yang diekstrak dari dokumen dan jumlah halaman:

* Biaya token teks: Setiap halaman biasanya menggunakan 1.500–3.000 token per halaman tergantung pada kepadatan konten. Harga API standar berlaku tanpa biaya PDF tambahan.
* Biaya token gambar: Karena setiap halaman dikonversi menjadi gambar, [perhitungan biaya berbasis gambar](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size) yang sama diterapkan.

Anda dapat menggunakan [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) untuk memperkirakan biaya untuk PDF spesifik Anda.

## Optimalkan pemrosesan PDF

### Tingkatkan kinerja

Ikuti praktik terbaik berikut untuk hasil optimal:

* Tempatkan PDF sebelum teks dalam permintaan Anda
* Gunakan font standar
* Pastikan teks jelas dan mudah dibaca
* Putar halaman ke orientasi tegak yang benar
* Gunakan nomor halaman logis (dari penampil PDF) dalam prompt
* Pisahkan PDF besar menjadi beberapa bagian jika diperlukan
* Aktifkan caching prompt untuk analisis berulang

### Skalakan implementasi Anda

Untuk pemrosesan bervolume tinggi, pertimbangkan pendekatan berikut:

#### Gunakan caching prompt

Cache PDF dengan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) untuk meningkatkan kinerja pada kueri berulang:

<CodeGroup>
  ```bash cURL
  curl -sL "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt
  # Buat file permintaan JSON menggunakan konten pdf_base64.txt
  jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [{
          "role": "user",
          "content": [{
              "type": "document",
              "source": {
                  "type": "base64",
                  "media_type": "application/pdf",
                  "data": $PDF_BASE64
              },
              "cache_control": {
                  "type": "ephemeral"
              }
          },
          {
              "type": "text",
              "text": "Which model has the highest human preference win rates across each use-case?"
          }]
      }]
  }' > request.json

  # Kemudian lakukan panggilan API menggunakan file JSON tersebut
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d @request.json
  ```

  ```bash CLI
  ant messages create --transform content --format yaml <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: document
          source:
            type: base64
            media_type: application/pdf
            data: "@./document.pdf"
          cache_control:
            type: ephemeral
        - type: text
          text: Which model has the highest human preference win rates across each use-case?
  YAML
  ```

  ```python Python
  import base64
  import httpx

  # Pertama, muat dan enkode PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_data = base64.standard_b64encode(
      httpx.get(pdf_url, follow_redirects=True).content
  ).decode("utf-8")

  # Buat pesan dengan dokumen yang di-cache
  client = anthropic.Anthropic()
  message = client.messages.create(
      model="claude-opus-5",
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
                          "data": pdf_data,
                      },
                      "cache_control": {"type": "ephemeral"},
                  },
                  {
                      "type": "text",
                      "text": "Which model has the highest human preference win rates across each use-case?",
                  },
              ],
          }
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  // Pertama, muat dan enkode PDF
  const pdfURL =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  const pdfResponse = await fetch(pdfURL);
  const arrayBuffer = await pdfResponse.arrayBuffer();
  const pdfBase64 = Buffer.from(arrayBuffer).toString("base64");

  // Buat pesan dengan dokumen yang di-cache
  const anthropic = new Anthropic();
  const response = await anthropic.messages.create({
    model: "claude-opus-5",
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
            cache_control: { type: "ephemeral" }
          },
          {
            type: "text",
            text: "Which model has the highest human preference win rates across each use-case?"
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  // Unduh dan enkode PDF
  var pdfUrl = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  using var httpClient = new HttpClient();
  var pdfBase64 = Convert.ToBase64String(await httpClient.GetByteArrayAsync(pdfUrl));

  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new List<ContentBlockParam>
              {
                  new DocumentBlockParam
                  {
                      Source = new Base64PdfSource { Data = pdfBase64 },
                      CacheControl = new CacheControlEphemeral(),
                  },
                  new TextBlockParam("Which model has the highest human preference win rates across each use-case?"),
              },
          },
      ],
  });

  Console.WriteLine(message);
  ```

  ```go Go
  // Pertama, muat dan enkode PDF
  pdfURL := "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  resp, err := http.Get(pdfURL)
  if err != nil {
  	panic(err)
  }
  defer resp.Body.Close()
  pdfBytes, err := io.ReadAll(resp.Body)
  if err != nil {
  	panic(err)
  }
  pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

  // Buat blok dokumen dengan cache control
  client := anthropic.NewClient()
  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
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
  					CacheControl: anthropic.NewCacheControlEphemeralParam(),
  				},
  			},
  			anthropic.NewTextBlock("Which model has the highest human preference win rates across each use-case?"),
  		),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Unduh dan enkode PDF
  String pdfUrl =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  HttpClient httpClient = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NORMAL).build();
  HttpRequest request = HttpRequest.newBuilder().uri(URI.create(pdfUrl)).GET().build();

  HttpResponse<byte[]> response = httpClient.send(
    request,
    HttpResponse.BodyHandlers.ofByteArray()
  );
  String pdfBase64 = Base64.getEncoder().encodeToString(response.body());

  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_5)
    .maxTokens(1024)
    .addUserMessageOfBlockParams(
      List.of(
        ContentBlockParam.ofDocument(
          DocumentBlockParam.builder()
            .source(Base64PdfSource.builder().data(pdfBase64).build())
            .cacheControl(CacheControlEphemeral.builder().build())
            .build()
        ),
        ContentBlockParam.ofText(
          TextBlockParam.builder()
            .text(
              "Which model has the highest human preference win rates across each use-case?"
            )
            .build()
        )
      )
    )
    .build();

  Message message = client.messages().create(params);
  System.out.println(message);
  ```

  ```php PHP
  $client = new Client();

  // Muat dan enkode PDF
  $pdf_url = 'https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf';
  $pdf_data = base64_encode(file_get_contents($pdf_url));

  $message = $client->messages->create(
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
                          'data' => $pdf_data,
                      ],
                      'cache_control' => ['type' => 'ephemeral'],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'Which model has the highest human preference win rates across each use-case?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-5',
  );

  echo $message;
  ```

  ```ruby Ruby
  require "open-uri"

  # Muat dan enkode PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_bytes = URI.open(pdf_url, "rb") { |f| f.read }
  pdf_data = [pdf_bytes].pack("m0") # Base64-encode without newlines

  anthropic = Anthropic::Client.new

  message = anthropic.messages.create(
    model: "claude-opus-5",
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
              data: pdf_data
            },
            cache_control: {type: "ephemeral"}
          },
          {
            type: "text",
            text: "Which model has the highest human preference win rates across each use-case?"
          }
        ]
      }
    ]
  )

  puts(message.content)
  ```
</CodeGroup>

#### Proses batch dokumen

Gunakan [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing) untuk memproses banyak PDF dalam satu permintaan:

<CodeGroup>
  ```bash cURL
  curl -sL "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt
  # Buat file permintaan JSON menggunakan konten pdf_base64.txt
  jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
      "requests": [
      {
          "custom_id": "my-first-request",
          "params": {
              "model": "claude-opus-5",
              "max_tokens": 1024,
              "messages": [{
                  "role": "user",
                  "content": [{
                      "type": "document",
                      "source": {
                          "type": "base64",
                          "media_type": "application/pdf",
                          "data": $PDF_BASE64
                      }
                  },
                  {
                      "type": "text",
                      "text": "Which model has the highest human preference win rates across each use-case?"
                  }]
              }]
          }
      },
      {
          "custom_id": "my-second-request",
          "params": {
              "model": "claude-opus-5",
              "max_tokens": 1024,
              "messages": [{
                  "role": "user",
                  "content": [{
                      "type": "document",
                      "source": {
                          "type": "base64",
                          "media_type": "application/pdf",
                          "data": $PDF_BASE64
                      }
                  },
                  {
                      "type": "text",
                      "text": "Extract 5 key insights from this document."
                  }]
              }]
          }
      }]
  }' > request.json

  # Kemudian lakukan panggilan API menggunakan file JSON tersebut
  curl https://api.anthropic.com/v1/messages/batches \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d @request.json
  ```

  ```bash CLI
  ant messages:batches create <<'YAML'
  requests:
    - custom_id: my-first-request
      params:
        model: claude-opus-5
        max_tokens: 1024
        messages:
          - role: user
            content:
              - type: document
                source:
                  type: base64
                  media_type: application/pdf
                  data: "@./document.pdf"
              - type: text
                text: >-
                  Which model has the highest human preference win rates
                  across each use-case?
    - custom_id: my-second-request
      params:
        model: claude-opus-5
        max_tokens: 1024
        messages:
          - role: user
            content:
              - type: document
                source:
                  type: base64
                  media_type: application/pdf
                  data: "@./document.pdf"
              - type: text
                text: Extract 5 key insights from this document.
  YAML
  ```

  ```python Python
  import base64
  import httpx

  # Pertama, muat dan enkode PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_data = base64.standard_b64encode(
      httpx.get(pdf_url, follow_redirects=True).content
  ).decode("utf-8")

  # Buat batch permintaan yang menggunakan dokumen tersebut
  client = anthropic.Anthropic()
  message_batch = client.messages.batches.create(
      requests=[
          {
              "custom_id": "my-first-request",
              "params": {
                  "model": "claude-opus-5",
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
                                      "data": pdf_data,
                                  },
                              },
                              {
                                  "type": "text",
                                  "text": "Which model has the highest human preference win rates across each use-case?",
                              },
                          ],
                      }
                  ],
              },
          },
          {
              "custom_id": "my-second-request",
              "params": {
                  "model": "claude-opus-5",
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
                                      "data": pdf_data,
                                  },
                              },
                              {
                                  "type": "text",
                                  "text": "Extract 5 key insights from this document.",
                              },
                          ],
                      }
                  ],
              },
          },
      ]
  )

  print(message_batch)
  ```

  ```typescript TypeScript
  // Pertama, muat dan enkode PDF
  const pdfURL =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  const pdfResponse = await fetch(pdfURL);
  const arrayBuffer = await pdfResponse.arrayBuffer();
  const pdfBase64 = Buffer.from(arrayBuffer).toString("base64");

  // Buat batch permintaan yang menggunakan dokumen tersebut
  const anthropic = new Anthropic();
  const response = await anthropic.messages.batches.create({
    requests: [
      {
        custom_id: "my-first-request",
        params: {
          model: "claude-opus-5",
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
                  }
                },
                {
                  type: "text",
                  text: "Which model has the highest human preference win rates across each use-case?"
                }
              ]
            }
          ]
        }
      },
      {
        custom_id: "my-second-request",
        params: {
          model: "claude-opus-5",
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
                  }
                },
                {
                  type: "text",
                  text: "Extract 5 key insights from this document."
                }
              ]
            }
          ]
        }
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  // Unduh dan enkode PDF
  var pdfUrl = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  using var httpClient = new HttpClient();
  var pdfBase64 = Convert.ToBase64String(await httpClient.GetByteArrayAsync(pdfUrl));

  var batch = await client.Messages.Batches.Create(new BatchCreateParams
  {
      Requests =
      [
          new()
          {
              CustomID = "my-first-request",
              Params = new()
              {
                  Model = Model.ClaudeOpus5,
                  MaxTokens = 1024,
                  Messages =
                  [
                      new()
                      {
                          Role = Role.User,
                          Content = new List<ContentBlockParam>
                          {
                              new DocumentBlockParam
                              {
                                  Source = new Base64PdfSource { Data = pdfBase64 },
                              },
                              new TextBlockParam("Which model has the highest human preference win rates across each use-case?"),
                          },
                      },
                  ],
              },
          },
          new()
          {
              CustomID = "my-second-request",
              Params = new()
              {
                  Model = Model.ClaudeOpus5,
                  MaxTokens = 1024,
                  Messages =
                  [
                      new()
                      {
                          Role = Role.User,
                          Content = new List<ContentBlockParam>
                          {
                              new DocumentBlockParam
                              {
                                  Source = new Base64PdfSource { Data = pdfBase64 },
                              },
                              new TextBlockParam("Extract 5 key insights from this document."),
                          },
                      },
                  ],
              },
          },
      ],
  });

  Console.WriteLine(batch);
  ```

  ```go Go
  // Pertama, muat dan enkode PDF
  pdfURL := "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  resp, err := http.Get(pdfURL)
  if err != nil {
  	panic(err)
  }
  defer resp.Body.Close()
  pdfBytes, err := io.ReadAll(resp.Body)
  if err != nil {
  	panic(err)
  }
  pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

  // Buat batch permintaan yang menggunakan dokumen tersebut
  client := anthropic.NewClient()
  batch, err := client.Messages.Batches.New(context.TODO(), anthropic.MessageBatchNewParams{
  	Requests: []anthropic.MessageBatchNewParamsRequest{
  		{
  			CustomID: "my-first-request",
  			Params: anthropic.MessageBatchNewParamsRequestParams{
  				Model:     anthropic.ModelClaudeOpus5,
  				MaxTokens: 1024,
  				Messages: []anthropic.MessageParam{
  					anthropic.NewUserMessage(
  						anthropic.NewDocumentBlock(anthropic.Base64PDFSourceParam{
  							Data: pdfBase64,
  						}),
  						anthropic.NewTextBlock("Which model has the highest human preference win rates across each use-case?"),
  					),
  				},
  			},
  		},
  		{
  			CustomID: "my-second-request",
  			Params: anthropic.MessageBatchNewParamsRequestParams{
  				Model:     anthropic.ModelClaudeOpus5,
  				MaxTokens: 1024,
  				Messages: []anthropic.MessageParam{
  					anthropic.NewUserMessage(
  						anthropic.NewDocumentBlock(anthropic.Base64PDFSourceParam{
  							Data: pdfBase64,
  						}),
  						anthropic.NewTextBlock("Extract 5 key insights from this document."),
  					),
  				},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", batch)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Unduh dan enkode PDF
  String pdfUrl =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  HttpClient httpClient = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NORMAL).build();
  HttpRequest request = HttpRequest.newBuilder().uri(URI.create(pdfUrl)).GET().build();

  HttpResponse<byte[]> response = httpClient.send(
    request,
    HttpResponse.BodyHandlers.ofByteArray()
  );
  String pdfBase64 = Base64.getEncoder().encodeToString(response.body());

  BatchCreateParams params = BatchCreateParams.builder()
    .addRequest(
      BatchCreateParams.Request.builder()
        .customId("my-first-request")
        .params(
          BatchCreateParams.Request.Params.builder()
            .model(Model.CLAUDE_OPUS_5)
            .maxTokens(1024)
            .addUserMessageOfBlockParams(
              List.of(
                ContentBlockParam.ofDocument(
                  DocumentBlockParam.builder()
                    .source(Base64PdfSource.builder().data(pdfBase64).build())
                    .build()
                ),
                ContentBlockParam.ofText(
                  TextBlockParam.builder()
                    .text(
                      "Which model has the highest human preference win rates across each use-case?"
                    )
                    .build()
                )
              )
            )
            .build()
        )
        .build()
    )
    .addRequest(
      BatchCreateParams.Request.builder()
        .customId("my-second-request")
        .params(
          BatchCreateParams.Request.Params.builder()
            .model(Model.CLAUDE_OPUS_5)
            .maxTokens(1024)
            .addUserMessageOfBlockParams(
              List.of(
                ContentBlockParam.ofDocument(
                  DocumentBlockParam.builder()
                    .source(Base64PdfSource.builder().data(pdfBase64).build())
                    .build()
                ),
                ContentBlockParam.ofText(
                  TextBlockParam.builder()
                    .text("Extract 5 key insights from this document.")
                    .build()
                )
              )
            )
            .build()
        )
        .build()
    )
    .build();

  MessageBatch batch = client.messages().batches().create(params);
  System.out.println(batch);
  ```

  ```php PHP
  $client = new Client();

  // Muat dan enkode PDF
  $pdf_url = 'https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf';
  $pdf_data = base64_encode(file_get_contents($pdf_url));

  $batch = $client->messages->batches->create(
      requests: [
          [
              'custom_id' => 'my-first-request',
              'params' => [
                  'model' => 'claude-opus-5',
                  'max_tokens' => 1024,
                  'messages' => [
                      [
                          'role' => 'user',
                          'content' => [
                              [
                                  'type' => 'document',
                                  'source' => [
                                      'type' => 'base64',
                                      'media_type' => 'application/pdf',
                                      'data' => $pdf_data,
                                  ],
                              ],
                              [
                                  'type' => 'text',
                                  'text' => 'Which model has the highest human preference win rates across each use-case?',
                              ],
                          ],
                      ],
                  ],
              ],
          ],
          [
              'custom_id' => 'my-second-request',
              'params' => [
                  'model' => 'claude-opus-5',
                  'max_tokens' => 1024,
                  'messages' => [
                      [
                          'role' => 'user',
                          'content' => [
                              [
                                  'type' => 'document',
                                  'source' => [
                                      'type' => 'base64',
                                      'media_type' => 'application/pdf',
                                      'data' => $pdf_data,
                                  ],
                              ],
                              [
                                  'type' => 'text',
                                  'text' => 'Extract 5 key insights from this document.',
                              ],
                          ],
                      ],
                  ],
              ],
          ],
      ],
  );

  echo $batch;
  ```

  ```ruby Ruby
  require "open-uri"

  # Muat dan enkode PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_bytes = URI.open(pdf_url, "rb") { |f| f.read }
  pdf_data = [pdf_bytes].pack("m0") # Base64-encode without newlines

  anthropic = Anthropic::Client.new

  message_batch = anthropic.messages.batches.create(
    requests: [
      {
        custom_id: "my-first-request",
        params: {
          model: "claude-opus-5",
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
                    data: pdf_data
                  }
                },
                {
                  type: "text",
                  text: "Which model has the highest human preference win rates across each use-case?"
                }
              ]
            }
          ]
        }
      },
      {
        custom_id: "my-second-request",
        params: {
          model: "claude-opus-5",
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
                    data: pdf_data
                  }
                },
                {
                  type: "text",
                  text: "Extract 5 key insights from this document."
                }
              ]
            }
          ]
        }
      }
    ]
  )

  puts(message_batch)
  ```
</CodeGroup>

Batch diproses secara asinkron. Untuk memeriksa progres dan mengambil hasil setelah pemrosesan selesai, lihat [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Vision" icon="image" href="https://platform.claude.com/docs/id/build-with-claude/vision">
    Kemampuan vision Claude memungkinkannya memahami dan menganalisis gambar, membuka kemungkinan menarik untuk interaksi multimodal.
  </Card>

  <Card title="Coba contoh PDF" icon="file" href="https://platform.claude.com/cookbook/multimodal-getting-started-with-vision">
    Jelajahi contoh praktis pemrosesan PDF dalam resep Claude Cookbook.
  </Card>

  <Card title="Lihat referensi API" icon="code" href="https://platform.claude.com/docs/id/api/messages/create">
    Lihat dokumentasi API lengkap untuk dukungan PDF.
  </Card>
</CardGroup>
