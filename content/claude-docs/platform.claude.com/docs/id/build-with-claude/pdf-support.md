---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/pdf-support
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: cf5d8030a14200e1e94e5735924c66082158ced02c370f7e206ef2e26be34447
---

# Dukungan PDF

Proses PDF dengan Claude. Ekstrak teks, analisis grafik, dan pahami konten visual dari dokumen Anda.

---

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Anda dapat bertanya kepada Claude tentang teks, gambar, grafik, dan tabel apa pun dalam PDF yang Anda berikan. Beberapa contoh kasus penggunaan:
- Menganalisis laporan keuangan dan memahami grafik/tabel
- Mengekstrak informasi penting dari dokumen hukum
- Bantuan penerjemahan untuk dokumen
- Mengonversi informasi dokumen ke dalam format terstruktur

## Sebelum Anda mulai \{#before-you-begin}

### Periksa persyaratan PDF \{#check-pdf-requirements}
Claude dapat bekerja dengan PDF standar apa pun. Pastikan ukuran permintaan Anda memenuhi persyaratan berikut:

| Persyaratan | Batas |
|------------|--------|
| Ukuran permintaan maksimum | 32&nbsp;MB ([bervariasi berdasarkan platform](/docs/id/api/overview#request-size-limits)) |
| Halaman maksimum per permintaan | 600 (100 untuk model dengan jendela konteks 200k token) |
| Format | PDF standar (tanpa kata sandi/enkripsi) |

Kedua batas tersebut berlaku untuk seluruh payload permintaan, termasuk konten lain yang dikirim bersama PDF. Untuk PDF berukuran besar, pertimbangkan untuk mengunggah dengan [Files API](#option-3-files-api) dan mereferensikannya melalui `file_id` agar payload permintaan tetap kecil.

<Tip>
PDF yang padat (banyak halaman dengan font kecil, tabel kompleks, atau grafik yang berat) dapat memenuhi jendela konteks sebelum mencapai batas halaman. Permintaan dengan PDF besar juga dapat gagal sebelum mencapai batas halaman, bahkan saat menggunakan Files API. Cobalah membagi dokumen menjadi beberapa bagian; untuk file besar, karena setiap halaman diproses sebagai gambar, menurunkan resolusi (downsampling) gambar yang disematkan juga dapat membantu.
</Tip>

Karena dukungan PDF bergantung pada kemampuan visi Claude, dukungan ini tunduk pada [batasan dan pertimbangan](/docs/id/build-with-claude/vision#limitations) yang sama seperti tugas visi lainnya.

### Platform dan model yang didukung \{#supported-platforms-and-models}

Dukungan PDF tersedia di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) (lihat [Dukungan PDF Amazon Bedrock](#amazon-bedrock-pdf-support)), [Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Semua [model aktif](/docs/id/about-claude/models/overview) mendukung pemrosesan PDF.

### Dukungan PDF Amazon Bedrock \{#amazon-bedrock-pdf-support}

Saat menggunakan dukungan PDF melalui Converse API dari Bedrock, terdapat dua mode pemrosesan dokumen yang berbeda:

<Note>
**Penting:** Untuk mengakses kemampuan pemahaman PDF visual penuh dari Claude di Converse API, Anda harus mengaktifkan sitasi. Tanpa sitasi diaktifkan, API akan kembali ke ekstraksi teks dasar saja. Pelajari lebih lanjut tentang [bekerja dengan sitasi](/docs/id/build-with-claude/citations).
</Note>

#### Mode pemrosesan dokumen \{#document-processing-modes}

1. **Converse Document Chat** (Mode asli - Hanya ekstraksi teks)
   - Menyediakan ekstraksi teks dasar dari PDF
   - Tidak dapat menganalisis gambar, grafik, atau tata letak visual dalam PDF
   - Menggunakan sekitar 1.000 token untuk PDF 3 halaman
   - Digunakan secara otomatis ketika sitasi tidak diaktifkan

2. **Claude PDF Chat** (Mode baru - Pemahaman visual penuh)
   - Menyediakan analisis visual lengkap terhadap PDF
   - Dapat memahami dan menganalisis grafik, diagram, gambar, dan tata letak visual
   - Memproses setiap halaman sebagai teks dan gambar untuk pemahaman yang komprehensif
   - Menggunakan sekitar 7.000 token untuk PDF 3 halaman
   - **Memerlukan sitasi diaktifkan** di Converse API

#### Batasan utama \{#key-limitations}

- **Converse API**: Analisis PDF visual memerlukan sitasi diaktifkan. Saat ini tidak ada opsi untuk menggunakan analisis visual tanpa sitasi (tidak seperti InvokeModel API).
- **InvokeModel API**: Menyediakan kontrol penuh atas pemrosesan PDF tanpa sitasi yang dipaksakan.

#### Masalah umum \{#common-issues}

Jika Claude tidak melihat gambar atau grafik dalam PDF Anda saat menggunakan Converse API, kemungkinan Anda perlu mengaktifkan flag sitasi. Tanpa itu, Converse akan kembali ke ekstraksi teks dasar saja.

<Note>
Ini adalah kendala yang diketahui pada Converse API. Untuk aplikasi yang memerlukan analisis PDF visual tanpa sitasi, pertimbangkan untuk menggunakan InvokeModel API sebagai gantinya.
</Note>

<Note>
Untuk file non-PDF seperti file .csv, .xlsx, .docx, .md, atau .txt, lihat [Bekerja dengan format file lain](/docs/id/build-with-claude/files#working-with-other-file-formats).
</Note>

***

## Memproses PDF dengan Claude \{#process-pdfs-with-claude}

### Kirim permintaan PDF pertama Anda \{#send-your-first-pdf-request}
Mari kita mulai dengan contoh sederhana menggunakan Messages API. Anda dapat memberikan PDF kepada Claude dengan tiga cara:

1. Sebagai referensi URL ke PDF yang dihosting secara online
2. Sebagai PDF yang dienkode base64 dalam blok konten `document`
3. Melalui `file_id` dari [Files API](/docs/id/build-with-claude/files)

<Note>
Di Amazon Bedrock dan Vertex AI, saat ini hanya sumber yang dienkode base64 yang tersedia.
</Note>

#### Opsi 1: Dokumen PDF berbasis URL \{#option-1-url-based-pdf-document}

Pendekatan paling sederhana adalah mereferensikan PDF langsung dari URL:

<CodeGroup>
   ```bash cURL
    curl https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "claude-opus-4-8",
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
    model: claude-opus-4-8
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

    const response = await anthropic.messages.create({
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
    ```java Java hidelines={1..8,-2..}
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.*;
    import java.util.List;

    public class PdfUrlExample {

      public static void main(String[] args) {
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
          .model(Model.CLAUDE_OPUS_4_8)
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

#### Opsi 2: Dokumen PDF yang dienkode base64 \{#option-2-base64-encoded-pdf-document}

Jika Anda perlu mengirim PDF dari sistem lokal Anda atau ketika URL tidak tersedia:

<CodeGroup>
    ```bash cURL hidelines={1}
    cd "$(mktemp -d)"
    # Metode 1: Ambil dan enkode PDF jarak jauh
    curl -s "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt

    # Metode 2: Enkode file PDF lokal
    # base64 document.pdf | tr -d '\n' > pdf_base64.txt

    # Buat file permintaan JSON menggunakan konten pdf_base64.txt
    jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
        "model": "claude-opus-4-8",
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
    ```bash CLI hidelines={1..2}
    cd "$(mktemp -d)"
    curl -sSo document.pdf https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
    ant messages create \
      --model claude-opus-4-8 \
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

    # Pertama, muat dan enkode PDF
    pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
    pdf_data = base64.standard_b64encode(httpx.get(pdf_url).content).decode("utf-8")

    # Alternatif: Muat dari file lokal
    # with open("document.pdf", "rb") as f:
    #     pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # Kirim ke Claude menggunakan enkode base64
    client = anthropic.Anthropic()
    message = client.messages.create(
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

        // Metode 1: Unduh dan enkode PDF jarak jauh
        String pdfUrl =
          "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
        HttpClient httpClient = HttpClient.newHttpClient();
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
          .model(Model.CLAUDE_OPUS_4_8)
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

#### Opsi 3: Files API \{#option-3-files-api}

Untuk PDF yang akan Anda gunakan berulang kali, atau ketika Anda ingin menghindari overhead encoding, gunakan [Files API](/docs/id/build-with-claude/files):

<CodeGroup>
```bash cURL hidelines={1..2}
cd "$(mktemp -d)"
curl -sSo document.pdf https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
# Pertama, unggah PDF Anda ke Files API
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@document.pdf"

# Kemudian gunakan file_id yang dikembalikan dalam pesan Anda
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -d '{
    "model": "claude-opus-4-8",
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

```bash CLI nocheck hidelines={1..2}
cd "$(mktemp -d)"
curl -sSo document.pdf https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
# Pertama, unggah PDF Anda ke Files API
FILE_ID=$(ant beta:files upload \
  --file ./document.pdf \
  --transform id --raw-output)

# Kemudian gunakan file_id yang dikembalikan dalam pesan Anda
ant beta:messages create \
  --beta files-api-2025-04-14 \
  --transform content --format yaml <<YAML
model: claude-opus-4-8
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

# Unggah file PDF
with open("document.pdf", "rb") as f:
    file_upload = client.beta.files.upload(file=("document.pdf", f, "application/pdf"))

# Gunakan file yang diunggah dalam pesan
message = client.beta.messages.create(
    model="claude-opus-4-8",
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

// Unggah file PDF
const fileUpload = await anthropic.beta.files.upload({
  file: await toFile(fs.createReadStream("document.pdf"), undefined, {
    type: "application/pdf"
  })
});

// Gunakan file yang diunggah dalam pesan
const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-8",
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

    // Unggah file PDF
    FileMetadata file = client
      .beta()
      .files()
      .upload(FileUploadParams.builder().file(Path.of("document.pdf")).build());

    // Gunakan file yang diunggah dalam pesan
    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
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

### Cara kerja dukungan PDF \{#how-pdf-support-works}
Ketika Anda mengirim PDF ke Claude, langkah-langkah berikut terjadi:
<Steps>
  <Step title="Sistem mengekstrak konten dokumen.">
    - Sistem mengonversi setiap halaman dokumen menjadi gambar.
    - Teks dari setiap halaman diekstrak dan disediakan bersama gambar setiap halaman.
  </Step>
  <Step title="Claude menganalisis teks dan gambar untuk lebih memahami dokumen.">
    - Dokumen disediakan sebagai kombinasi teks dan gambar untuk dianalisis.
    - Ini memungkinkan pengguna untuk meminta wawasan tentang elemen visual dari PDF, seperti grafik, diagram, dan konten non-tekstual lainnya.
  </Step>
  <Step title="Claude merespons, mereferensikan konten PDF jika relevan.">
    Claude dapat mereferensikan konten tekstual dan visual saat merespons. Anda dapat lebih meningkatkan kinerja dengan mengintegrasikan dukungan PDF dengan:
    - **Caching prompt**: Untuk meningkatkan kinerja pada analisis berulang.
    - **Pemrosesan batch**: Untuk pemrosesan dokumen bervolume tinggi.
    - **Penggunaan alat**: Untuk mengekstrak informasi spesifik dari dokumen untuk digunakan sebagai input alat.
  </Step>
</Steps>

### Perkirakan biaya Anda \{#estimate-your-costs}
Jumlah token dari file PDF bergantung pada total teks yang diekstrak dari dokumen serta jumlah halaman:
- Biaya token teks: Setiap halaman biasanya menggunakan 1.500-3.000 token per halaman tergantung pada kepadatan konten. Harga API standar berlaku tanpa biaya PDF tambahan.
- Biaya token gambar: Karena setiap halaman dikonversi menjadi gambar, [perhitungan biaya berbasis gambar](/docs/id/build-with-claude/vision#evaluate-image-size) yang sama diterapkan.

Anda dapat menggunakan [penghitungan token](/docs/id/build-with-claude/token-counting) untuk memperkirakan biaya untuk PDF spesifik Anda.

***

## Optimalkan pemrosesan PDF \{#optimize-pdf-processing}

### Tingkatkan kinerja \{#improve-performance}
Ikuti praktik terbaik berikut untuk hasil yang optimal:
- Tempatkan PDF sebelum teks dalam permintaan Anda
- Gunakan font standar
- Pastikan teks jelas dan mudah dibaca
- Putar halaman ke orientasi tegak yang benar
- Gunakan nomor halaman logis (dari penampil PDF) dalam prompt
- Bagi PDF besar menjadi beberapa bagian jika diperlukan
- Aktifkan caching prompt untuk analisis berulang

### Skalakan implementasi Anda \{#scale-your-implementation}
Untuk pemrosesan bervolume tinggi, pertimbangkan pendekatan berikut:

#### Gunakan caching prompt \{#use-prompt-caching}
Cache PDF untuk meningkatkan kinerja pada kueri berulang:
<CodeGroup>
```bash cURL hidelines={1..2}
cd "$(mktemp -d)"
curl -s "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt
# Buat file permintaan JSON menggunakan konten pdf_base64.txt
jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
    "model": "claude-opus-4-8",
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
```bash CLI hidelines={1..2}
cd "$(mktemp -d)"
curl -sSo document.pdf https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
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
  model: "claude-opus-4-8",
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
      .model(Model.CLAUDE_OPUS_4_8)
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

#### Proses batch dokumen \{#process-document-batches}
Gunakan Message Batches API untuk alur kerja bervolume tinggi:
<CodeGroup>
```bash cURL hidelines={1..2}
cd "$(mktemp -d)"
curl -s "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt
# Buat file permintaan JSON menggunakan konten pdf_base64.txt
jq -n --rawfile PDF_BASE64 pdf_base64.txt '
{
  "requests": [
      {
          "custom_id": "my-first-request",
          "params": {
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

# Kemudian lakukan panggilan API menggunakan file JSON tersebut
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
      model: claude-opus-4-8
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
      model: claude-opus-4-8
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
        model: "claude-opus-4-8"
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
        model: "claude-opus-4-8"
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
              .model(Model.CLAUDE_OPUS_4_8)
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
              .model(Model.CLAUDE_OPUS_4_8)
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

## Langkah selanjutnya \{#next-steps}

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