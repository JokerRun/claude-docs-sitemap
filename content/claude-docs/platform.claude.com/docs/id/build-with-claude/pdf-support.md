---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/pdf-support
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 4ab2aeef602b088385dcd56d774cf51a4be3bba257a43af1fd5d79696c4d54f0
---

# Dukungan PDF

Proses PDF dengan Claude. Ekstrak teks, analisis bagan, dan pahami konten visual dari dokumen Anda.

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Anda dapat bertanya kepada Claude tentang teks, gambar, bagan, dan tabel apa pun dalam PDF yang Anda berikan. Beberapa contoh kasus penggunaan:
- Menganalisis laporan keuangan dan memahami bagan/tabel
- Mengekstrak informasi kunci dari dokumen hukum
- Bantuan terjemahan untuk dokumen
- Mengonversi informasi dokumen ke format terstruktur

## Sebelum Anda memulai

### Periksa persyaratan PDF
Claude bekerja dengan PDF standar apa pun. Pastikan ukuran permintaan Anda memenuhi persyaratan ini:

| Persyaratan | Batas |
|------------|--------|
| Ukuran permintaan maksimal | 32&nbsp;MB ([bervariasi menurut platform](/docs/id/api/overview#request-size-limits)) |
| Halaman maksimal per permintaan | 600 (100 untuk model dengan jendela konteks 200k-token) |
| Format | PDF Standar (tanpa kata sandi/enkripsi) |

Kedua batas berada pada seluruh muatan permintaan, termasuk konten lain apa pun yang dikirim bersama PDF. Untuk PDF besar, pertimbangkan untuk mengunggah dengan [Files API](#option-3-files-api) dan mereferensikan dengan `file_id` untuk menjaga muatan permintaan tetap kecil.

<Tip>
PDF padat (banyak halaman font kecil, tabel kompleks, atau grafis berat) dapat mengisi jendela konteks sebelum mencapai batas halaman. Permintaan dengan PDF besar juga dapat gagal sebelum mencapai batas halaman, bahkan saat menggunakan Files API. Coba bagi dokumen menjadi bagian-bagian; untuk file besar, karena setiap halaman diproses sebagai gambar, downsampling gambar tertanam juga dapat membantu.
</Tip>

Karena dukungan PDF bergantung pada kemampuan visi Claude, dukungan ini tunduk pada [batasan dan pertimbangan](/docs/id/build-with-claude/vision#limitations) yang sama seperti tugas visi lainnya.

### Platform dan model yang didukung

Dukungan PDF saat ini didukung melalui akses API langsung dan Google Vertex AI. Semua [model aktif](/docs/id/about-claude/models/overview) mendukung pemrosesan PDF.

Dukungan PDF sekarang tersedia di Amazon Bedrock dengan pertimbangan berikut:

### Dukungan PDF Amazon Bedrock

Saat menggunakan dukungan PDF melalui Converse API Amazon Bedrock, ada dua mode pemrosesan dokumen yang berbeda:

<Note>
**Penting:** Untuk mengakses kemampuan pemahaman PDF visual penuh Claude di Converse API, Anda harus mengaktifkan kutipan. Tanpa kutipan yang diaktifkan, API kembali ke ekstraksi teks dasar saja. Pelajari lebih lanjut tentang [bekerja dengan kutipan](/docs/id/build-with-claude/citations).
</Note>

#### Mode Pemrosesan Dokumen

1. **Converse Document Chat** (Mode asli - Ekstraksi teks saja)
   - Menyediakan ekstraksi teks dasar dari PDF
   - Tidak dapat menganalisis gambar, bagan, atau tata letak visual dalam PDF
   - Menggunakan sekitar 1.000 token untuk PDF 3 halaman
   - Digunakan secara otomatis ketika kutipan tidak diaktifkan

2. **Claude PDF Chat** (Mode baru - Pemahaman visual penuh)
   - Menyediakan analisis visual lengkap PDF
   - Dapat memahami dan menganalisis bagan, grafik, gambar, dan tata letak visual
   - Memproses setiap halaman sebagai teks dan gambar untuk pemahaman komprehensif
   - Menggunakan sekitar 7.000 token untuk PDF 3 halaman
   - **Memerlukan kutipan untuk diaktifkan** di Converse API

#### Batasan Utama

- **Converse API**: Analisis PDF visual memerlukan kutipan untuk diaktifkan. Saat ini tidak ada opsi untuk menggunakan analisis visual tanpa kutipan (tidak seperti InvokeModel API).
- **InvokeModel API**: Menyediakan kontrol penuh atas pemrosesan PDF tanpa kutipan paksa.

#### Masalah Umum

Jika pelanggan melaporkan bahwa Claude tidak melihat gambar atau bagan dalam PDF mereka saat menggunakan Converse API, mereka kemungkinan perlu mengaktifkan flag kutipan. Tanpa itu, Converse kembali ke ekstraksi teks dasar saja.

<Note>
Ini adalah batasan yang diketahui dengan Converse API. Untuk aplikasi yang memerlukan analisis PDF visual tanpa kutipan, pertimbangkan menggunakan InvokeModel API sebagai gantinya.
</Note>

<Note>
Untuk file non-PDF seperti .csv, .xlsx, .docx, .md, atau .txt, lihat [Bekerja dengan format file lain](/docs/id/build-with-claude/files#working-with-other-file-formats).
</Note>

***

## Proses PDF dengan Claude

### Kirim permintaan PDF pertama Anda
Mari kita mulai dengan contoh sederhana menggunakan Messages API. Anda dapat memberikan PDF kepada Claude dengan tiga cara:

1. Sebagai referensi URL ke PDF yang dihosting online
2. Sebagai PDF yang dikodekan base64 dalam blok konten `document`
3. Dengan `file_id` dari [Files API](/docs/id/build-with-claude/files)

#### Opsi 1: Dokumen PDF berbasis URL

Pendekatan paling sederhana adalah mereferensikan PDF langsung dari URL:

<CodeGroup>
   ```bash Shell
    curl https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "claude-opus-4-6",
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
    model: claude-opus-4-6
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
    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-6",
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
    ```typescript TypeScript hidelines={1..4}
    import Anthropic from "@anthropic-ai/sdk";

    const anthropic = new Anthropic();

    async function main() {
      const response = await anthropic.messages.create({
        model: "claude-opus-4-6",
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
    }

    main();
    ```
    ```java Java hidelines={1..8,-2..}
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.*;
    import java.util.List;

    public class PdfUrlExample {

      public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Create document block with URL
        DocumentBlockParam documentParam = DocumentBlockParam.builder()
          .source(
            UrlPdfSource.builder()
              .url(
                "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
              )
              .build()
          )
          .build();

        // Create a message with document and text content blocks
        MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_6)
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
      }
    }
    ```
</CodeGroup>

#### Opsi 2: Dokumen PDF yang dikodekan base64

Jika Anda perlu mengirim PDF dari sistem lokal Anda atau ketika URL tidak tersedia:

<CodeGroup>
    ```bash Shell hidelines={1}
    cd "$(mktemp -d)"
    # Method 1: Fetch and encode a remote PDF
    curl -s "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt

    # Method 2: Encode a local PDF file
    # base64 document.pdf | tr -d '\n' > pdf_base64.txt

    # Create a JSON request file using the pdf_base64.txt content
    jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
        "model": "claude-opus-4-6",
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

    # Send the API request using the JSON file
    curl https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d @request.json
    ```
    ```bash CLI hidelines={1..2}
    cd "$(mktemp -d)"
    curl -sSo document.pdf https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
    ant messages create \
      --model claude-opus-4-6 \
      --max-tokens 1024 \
      --transform content --format yaml <<'YAML'
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
    ```python Python hidelines={1}
    import anthropic
    import base64
    import httpx

    # First, load and encode the PDF
    pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
    pdf_data = base64.standard_b64encode(httpx.get(pdf_url).content).decode("utf-8")

    # Alternative: Load from a local file
    # with open("document.pdf", "rb") as f:
    #     pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # Send to Claude using base64 encoding
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-6",
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
    ```typescript TypeScript hidelines={1..3,-3..-1}
    import Anthropic from "@anthropic-ai/sdk";

    async function main() {
      // Method 1: Fetch and encode a remote PDF
      const pdfURL =
        "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
      const pdfResponse = await fetch(pdfURL);
      const arrayBuffer = await pdfResponse.arrayBuffer();
      const pdfBase64 = Buffer.from(arrayBuffer).toString("base64");

      // Method 2: Load from a local file
      // import fs from "fs";
      // const pdfBase64 = (await fs.readFile('document.pdf')).toString('base64');

      // Send the API request with base64-encoded PDF
      const anthropic = new Anthropic();
      const response = await anthropic.messages.create({
        model: "claude-opus-4-6",
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
    }

    main();
    ```

    ```java Java hidelines={1..2,4,6..22,-2..}
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.Base64PdfSource;
    import com.anthropic.models.messages.ContentBlockParam;
    import com.anthropic.models.messages.DocumentBlockParam;
    import com.anthropic.models.messages.Message;
    import com.anthropic.models.messages.MessageCreateParams;
    import com.anthropic.models.messages.Model;
    import com.anthropic.models.messages.TextBlockParam;
    import java.io.IOException;
    import java.net.URI;
    import java.net.http.HttpClient;
    import java.net.http.HttpRequest;
    import java.net.http.HttpResponse;
    import java.util.Base64;
    import java.util.List;

    public class PdfBase64Example {

      public static void main(String[] args) throws IOException, InterruptedException {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Method 1: Download and encode a remote PDF
        String pdfUrl =
          "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
        HttpClient httpClient = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder().uri(URI.create(pdfUrl)).GET().build();

        HttpResponse<byte[]> response = httpClient.send(
          request,
          HttpResponse.BodyHandlers.ofByteArray()
        );
        String pdfBase64 = Base64.getEncoder().encodeToString(response.body());

        // Method 2: Load from a local file
        // byte[] fileBytes = Files.readAllBytes(Path.of("document.pdf"));
        // String pdfBase64 = Base64.getEncoder().encodeToString(fileBytes);

        // Create document block with base64 data
        DocumentBlockParam documentParam = DocumentBlockParam.builder()
          .source(Base64PdfSource.builder().data(pdfBase64).build())
          .build();

        // Create a message with document and text content blocks
        MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_6)
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
      }
    }
    ```

</CodeGroup>

#### Opsi 3: Files API

Untuk PDF yang akan Anda gunakan berulang kali, atau ketika Anda ingin menghindari overhead pengkodean, gunakan [Files API](/docs/id/build-with-claude/files):

<CodeGroup>
```bash Shell hidelines={1..2}
cd "$(mktemp -d)"
curl -sSo document.pdf https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
# First, upload your PDF to the Files API
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@document.pdf"

# Then use the returned file_id in your message
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": [{
        "type": "document",
        "source": {
          "type": "file",
          "file_id": "file_abc123"
        }
      },
      {
        "type": "text",
        "text": "What are the key findings in this document?"
      }]
    }]
  }'
```

```bash CLI hidelines={1..2}
cd "$(mktemp -d)"
curl -sSo document.pdf https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
# First, upload your PDF to the Files API
FILE_ID=$(ant beta:files upload \
  --file ./document.pdf \
  --transform id --format yaml)

# Then use the returned file_id in your message
ant beta:messages create \
  --beta files-api-2025-04-14 \
  --transform content --format yaml <<YAML
model: claude-opus-4-6
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

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Upload the PDF file
with open("document.pdf", "rb") as f:
    file_upload = client.beta.files.upload(file=("document.pdf", f, "application/pdf"))

# Use the uploaded file in a message
message = client.beta.messages.create(
    model="claude-opus-4-6",
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

```typescript TypeScript nocheck
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import fs from "fs";

const anthropic = new Anthropic();

async function main() {
  // Upload the PDF file
  const fileUpload = await anthropic.beta.files.upload({
    file: await toFile(fs.createReadStream("document.pdf"), undefined, {
      type: "application/pdf"
    }),
    betas: ["files-api-2025-04-14"]
  });

  // Use the uploaded file in a message
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-6",
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
}

main();
```

```java Java nocheck hidelines={1..3,6,8,10..19,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Model;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.models.beta.files.FileUploadParams;
import com.anthropic.models.beta.messages.BetaContentBlockParam;
import com.anthropic.models.beta.messages.BetaFileDocumentSource;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaRequestDocumentBlock;
import com.anthropic.models.beta.messages.BetaTextBlockParam;
import com.anthropic.models.beta.messages.MessageCreateParams;
import java.nio.file.Path;
import java.util.List;

public class PdfFilesExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Upload the PDF file
    FileMetadata file = client
      .beta()
      .files()
      .upload(FileUploadParams.builder().file(Path.of("document.pdf")).build());

    // Use the uploaded file in a message
    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
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
  }
}
```
</CodeGroup>

### Cara kerja dukungan PDF
Ketika Anda mengirim PDF ke Claude, langkah-langkah berikut terjadi:
<Steps>
  <Step title="Sistem mengekstrak konten dokumen.">
    - Sistem mengonversi setiap halaman dokumen menjadi gambar.
    - Teks dari setiap halaman diekstrak dan disediakan bersama gambar setiap halaman.
  </Step>
  <Step title="Claude menganalisis teks dan gambar untuk lebih memahami dokumen.">
    - Dokumen disediakan sebagai kombinasi teks dan gambar untuk analisis.
    - Ini memungkinkan pengguna untuk meminta wawasan tentang elemen visual PDF, seperti bagan, diagram, dan konten non-tekstual lainnya.
  </Step>
  <Step title="Claude merespons, mereferensikan konten PDF jika relevan.">
    Claude dapat mereferensikan konten tekstual dan visual saat merespons. Anda dapat lebih meningkatkan kinerja dengan mengintegrasikan dukungan PDF dengan:
    - **Prompt caching**: Untuk meningkatkan kinerja untuk analisis berulang.
    - **Batch processing**: Untuk pemrosesan dokumen volume tinggi.
    - **Tool use**: Untuk mengekstrak informasi spesifik dari dokumen untuk digunakan sebagai input alat.
  </Step>
</Steps>

### Perkirakan biaya Anda
Jumlah token file PDF tergantung pada total teks yang diekstrak dari dokumen serta jumlah halaman:
- Biaya token teks: Setiap halaman biasanya menggunakan 1.500-3.000 token per halaman tergantung pada kepadatan konten. Harga API standar berlaku tanpa biaya PDF tambahan.
- Biaya token gambar: Karena setiap halaman dikonversi menjadi gambar, [perhitungan biaya berbasis gambar](/docs/id/build-with-claude/vision#evaluate-image-size) yang sama diterapkan.

Anda dapat menggunakan [token counting](/docs/id/build-with-claude/token-counting) untuk memperkirakan biaya untuk PDF spesifik Anda.

***

## Optimalkan pemrosesan PDF

### Tingkatkan kinerja
Ikuti praktik terbaik ini untuk hasil optimal:
- Tempatkan PDF sebelum teks dalam permintaan Anda
- Gunakan font standar
- Pastikan teks jelas dan mudah dibaca
- Putar halaman ke orientasi tegak yang benar
- Gunakan nomor halaman logis (dari penampil PDF) dalam prompt
- Bagi PDF besar menjadi potongan saat diperlukan
- Aktifkan prompt caching untuk analisis berulang

### Skalakan implementasi Anda
Untuk pemrosesan volume tinggi, pertimbangkan pendekatan berikut:

#### Gunakan prompt caching
Cache PDF untuk meningkatkan performa pada kueri berulang:
<CodeGroup>
```bash Shell hidelines={1..2}
cd "$(mktemp -d)"
curl -s "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt
# Buat file permintaan JSON menggunakan konten pdf_base64.txt
jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
    "model": "claude-opus-4-6",
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

# Kemudian buat panggilan API menggunakan file JSON
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d @request.json
```
```bash CLI hidelines={1..2}
cd "$(mktemp -d)"
curl -sSo document.pdf https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
ant messages create <<'YAML'
model: claude-opus-4-6
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

```python Python nocheck hidelines={1..5,7..13}
import anthropic
import base64
from pypdf import PdfWriter
import io

client = anthropic.Anthropic()

buf = io.BytesIO()
writer = PdfWriter()
writer.add_blank_page(width=72, height=72)
writer.write(buf)
pdf_data = base64.standard_b64encode(buf.getvalue()).decode("utf-8")

message = client.messages.create(
    model="claude-opus-4-6",
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
                {"type": "text", "text": "Analyze this document."},
            ],
        }
    ],
)
```

```typescript TypeScript nocheck
const response = await anthropic.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    {
      content: [
        {
          type: "document",
          source: {
            media_type: "application/pdf",
            type: "base64",
            data: pdfBase64
          },
          cache_control: { type: "ephemeral" }
        },
        {
          type: "text",
          text: "Which model has the highest human preference win rates across each use-case?"
        }
      ],
      role: "user"
    }
  ]
});
console.log(response);
```

```java Java nocheck hidelines={1..2,5,7..20,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Base64PdfSource;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.DocumentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class MessagesDocumentExample {

  public static void main(String[] args) throws IOException {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Baca file PDF sebagai base64
    byte[] pdfBytes = Files.readAllBytes(Paths.get("pdf_base64.txt"));
    String pdfBase64 = new String(pdfBytes);

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
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
  }
}
```
</CodeGroup>

#### Proses batch dokumen
Gunakan Message Batches API untuk alur kerja volume tinggi:
<CodeGroup>
```bash Shell hidelines={1..2}
cd "$(mktemp -d)"
curl -s "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt
# Buat file permintaan JSON menggunakan konten pdf_base64.txt
jq -n --rawfile PDF_BASE64 pdf_base64.txt '
{
  "requests": [
      {
          "custom_id": "my-first-request",
          "params": {
              "model": "claude-opus-4-6",
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
                                "data": $PDF_BASE64
                            }
                        },
                        {
                            "type": "text",
                            "text": "Which model has the highest human preference win rates across each use-case?"
                        }
                    ]
                }
              ]
          }
      },
      {
          "custom_id": "my-second-request",
          "params": {
              "model": "claude-opus-4-6",
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
                                "data": $PDF_BASE64
                            }
                        },
                        {
                            "type": "text",
                            "text": "Extract 5 key insights from this document."
                        }
                    ]
                }
              ]
          }
      }
  ]
}
' > request.json

# Kemudian buat panggilan API menggunakan file JSON
curl https://api.anthropic.com/v1/messages/batches \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d @request.json
```
```bash CLI hidelines={1..2}
cd "$(mktemp -d)"
curl -sSo document.pdf https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
ant messages:batches create <<'YAML'
requests:
  - custom_id: my-first-request
    params:
      model: claude-opus-4-6
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
      model: claude-opus-4-6
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

```python Python nocheck hidelines={1..5,7..13}
import anthropic
import base64
from pypdf import PdfWriter
import io

client = anthropic.Anthropic()

buf = io.BytesIO()
writer = PdfWriter()
writer.add_blank_page(width=72, height=72)
writer.write(buf)
pdf_data = base64.standard_b64encode(buf.getvalue()).decode("utf-8")

message_batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "doc1",
            "params": {
                "model": "claude-opus-4-6",
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
                            {"type": "text", "text": "Summarize this document."},
                        ],
                    }
                ],
            },
        }
    ]
)
```

```typescript TypeScript nocheck
const response = await anthropic.messages.batches.create({
  requests: [
    {
      custom_id: "my-first-request",
      params: {
        max_tokens: 1024,
        messages: [
          {
            content: [
              {
                type: "document",
                source: {
                  media_type: "application/pdf",
                  type: "base64",
                  data: pdfBase64
                }
              },
              {
                type: "text",
                text: "Which model has the highest human preference win rates across each use-case?"
              }
            ],
            role: "user"
          }
        ],
        model: "claude-opus-4-6"
      }
    },
    {
      custom_id: "my-second-request",
      params: {
        max_tokens: 1024,
        messages: [
          {
            content: [
              {
                type: "document",
                source: {
                  media_type: "application/pdf",
                  type: "base64",
                  data: pdfBase64
                }
              },
              {
                type: "text",
                text: "Extract 5 key insights from this document."
              }
            ],
            role: "user"
          }
        ],
        model: "claude-opus-4-6"
      }
    }
  ]
});
console.log(response);
```

```java Java nocheck hidelines={1..3,5..14,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.*;
import com.anthropic.models.messages.batches.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class MessagesBatchDocumentExample {

  public static void main(String[] args) throws IOException {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Baca file PDF sebagai base64
    byte[] pdfBytes = Files.readAllBytes(Paths.get("pdf_base64.txt"));
    String pdfBase64 = new String(pdfBytes);

    BatchCreateParams params = BatchCreateParams.builder()
      .addRequest(
        BatchCreateParams.Request.builder()
          .customId("my-first-request")
          .params(
            BatchCreateParams.Request.Params.builder()
              .model(Model.CLAUDE_OPUS_4_6)
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
              .model(Model.CLAUDE_OPUS_4_6)
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
  }
}
```
</CodeGroup>

## Langkah berikutnya

<CardGroup cols={2}>
  <Card
    title="Coba contoh PDF"
    icon="file"
    href="https://platform.claude.com/cookbook/multimodal-getting-started-with-vision"
  >
    Jelajahi contoh praktis pemrosesan PDF dalam resep cookbook.
  </Card>

  <Card
    title="Lihat referensi API"
    icon="code"
    href="/docs/id/api/messages/create"
  >
    Lihat dokumentasi API lengkap untuk dukungan PDF.
  </Card>
</CardGroup>