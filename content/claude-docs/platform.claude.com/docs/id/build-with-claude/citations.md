---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/citations
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 145ce899c603b83a2cae0def266636a59387a1933982abac09aa4cc0c32b671d
---

# Sitasi

---

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Claude mampu memberikan sitasi terperinci saat menjawab pertanyaan tentang dokumen, membantu Anda melacak dan memverifikasi sumber informasi dalam respons.

Semua [model aktif](/docs/id/about-claude/models/overview) mendukung sitasi, dengan pengecualian Haiku 3.

<Tip>
  Bagikan masukan dan saran Anda tentang fitur sitasi menggunakan [formulir](https://forms.gle/9n9hSrKnKe3rpowH9) ini.
</Tip>

Berikut adalah contoh cara menggunakan sitasi dengan Messages API:

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

```python Python hidelines={1..2}
import anthropic

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

```java Java hidelines={1..8,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.*;
import java.util.List;

public class DocumentExample {

  public static void main(String[] args) {
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
  }
}
```

</CodeGroup>

<Tip>
**Perbandingan dengan pendekatan berbasis prompt**

Dibandingkan dengan solusi sitasi berbasis prompt, fitur sitasi memiliki keunggulan berikut:
- **Penghematan biaya:** Jika pendekatan berbasis prompt Anda meminta Claude untuk menghasilkan kutipan langsung, Anda mungkin melihat penghematan biaya karena `cited_text` tidak dihitung terhadap token output Anda.
- **Keandalan sitasi yang lebih baik:** Karena sitasi diurai ke dalam format respons masing-masing yang disebutkan di atas dan `cited_text` diekstrak, sitasi dijamin berisi penunjuk yang valid ke dokumen yang disediakan.
- **Kualitas sitasi yang lebih baik:** Dalam evaluasi, fitur sitasi ditemukan secara signifikan lebih mungkin mengutip kutipan yang paling relevan dari dokumen dibandingkan dengan pendekatan yang murni berbasis prompt.
</Tip>

---

## Cara kerja sitasi \{#how-citations-work}

Integrasikan sitasi dengan Claude dalam langkah-langkah berikut:

<Steps>
  <Step title="Sediakan dokumen dan aktifkan sitasi">
    - Sertakan dokumen dalam salah satu format yang didukung: [PDF](#pdf-documents), [teks biasa](#plain-text-documents), atau dokumen [konten kustom](#custom-content-documents)
    - Atur `citations.enabled=true` pada setiap dokumen Anda. Saat ini, sitasi harus diaktifkan pada semua atau tidak sama sekali pada dokumen dalam sebuah permintaan.
    - Perhatikan bahwa hanya sitasi teks yang saat ini didukung dan sitasi gambar belum dimungkinkan.
  </Step>
  <Step title="Dokumen diproses">
    - Konten dokumen "dipecah menjadi chunk" untuk menentukan granularitas minimum dari sitasi yang mungkin. Misalnya, pemecahan berdasarkan kalimat akan memungkinkan Claude mengutip satu kalimat atau merangkai beberapa kalimat berurutan untuk mengutip sebuah paragraf (atau lebih panjang)!
      - **Untuk PDF:** Teks diekstrak seperti yang dijelaskan dalam [Dukungan PDF](/docs/id/build-with-claude/pdf-support) dan konten dipecah menjadi kalimat. Mengutip gambar dari PDF saat ini tidak didukung.
      - **Untuk dokumen teks biasa:** Konten dipecah menjadi kalimat yang dapat dikutip.
      - **Untuk dokumen konten kustom:** Blok konten yang Anda sediakan digunakan apa adanya dan tidak ada pemecahan lebih lanjut yang dilakukan.
  </Step>
  <Step title="Claude memberikan respons dengan sitasi">
    - Respons sekarang dapat menyertakan beberapa blok teks di mana setiap blok teks dapat berisi klaim yang dibuat Claude dan daftar sitasi yang mendukung klaim tersebut.
    - Sitasi merujuk ke lokasi spesifik dalam dokumen sumber. Format sitasi ini bergantung pada jenis dokumen yang dikutip.
      - **Untuk PDF:** Sitasi menyertakan rentang nomor halaman (indeks dimulai dari 1).
      - **Untuk dokumen teks biasa:** Sitasi menyertakan rentang indeks karakter (indeks dimulai dari 0).
      - **Untuk dokumen konten kustom:** Sitasi menyertakan rentang indeks blok konten (indeks dimulai dari 0) yang sesuai dengan daftar konten asli yang disediakan.
    - Indeks dokumen disediakan untuk menunjukkan sumber referensi dan diindeks mulai dari 0 sesuai dengan daftar semua dokumen dalam permintaan asli Anda.
  </Step>
</Steps>

<Tip>
  **Pemecahan otomatis vs konten kustom**

  Secara default, dokumen teks biasa dan PDF secara otomatis dipecah menjadi kalimat. Jika Anda memerlukan kontrol lebih atas granularitas sitasi (misalnya, untuk poin-poin atau transkrip), gunakan dokumen konten kustom sebagai gantinya. Lihat [Jenis Dokumen](#document-types) untuk detail lebih lanjut.

  Misalnya, jika Anda ingin Claude dapat mengutip kalimat spesifik dari chunk RAG Anda, Anda harus menempatkan setiap chunk RAG ke dalam dokumen teks biasa. Sebaliknya, jika Anda tidak ingin pemecahan lebih lanjut dilakukan, atau jika Anda ingin menyesuaikan pemecahan tambahan apa pun, Anda dapat menempatkan chunk RAG ke dalam dokumen konten kustom.
</Tip>

### Konten yang dapat dikutip vs tidak dapat dikutip \{#citable-vs-non-citable-content}

- Teks yang ditemukan dalam konten `source` dokumen dapat dikutip.
- `title` dan `context` adalah field opsional yang akan diteruskan ke model tetapi tidak digunakan sebagai konten yang dikutip.
- `title` memiliki batasan panjang sehingga Anda mungkin menemukan field `context` berguna untuk menyimpan metadata dokumen apa pun sebagai teks atau json yang di-stringify.

### Indeks sitasi \{#citation-indices}
- Indeks dokumen dimulai dari 0 berdasarkan daftar semua blok konten dokumen dalam permintaan (mencakup semua pesan).
- Indeks karakter dimulai dari 0 dengan indeks akhir eksklusif.
- Nomor halaman dimulai dari 1 dengan nomor halaman akhir eksklusif.
- Indeks blok konten dimulai dari 0 dengan indeks akhir eksklusif dari daftar `content` yang disediakan dalam dokumen konten kustom.

### Biaya token \{#token-costs}
- Mengaktifkan sitasi menyebabkan sedikit peningkatan pada token input karena penambahan prompt sistem dan pemecahan dokumen.
- Namun, fitur sitasi sangat efisien dengan token output. Di balik layar, model menghasilkan sitasi dalam format terstandar yang kemudian diurai menjadi teks yang dikutip dan indeks lokasi dokumen. Field `cited_text` disediakan untuk kemudahan dan tidak dihitung terhadap token output.
- Ketika diteruskan kembali dalam giliran percakapan berikutnya, `cited_text` juga tidak dihitung terhadap token input.

### Kompatibilitas fitur \{#feature-compatibility}
Sitasi bekerja bersama dengan fitur API lainnya termasuk [caching prompt](/docs/id/build-with-claude/prompt-caching), [penghitungan token](/docs/id/build-with-claude/token-counting), dan [pemrosesan batch](/docs/id/build-with-claude/batch-processing).

<Warning>
**Sitasi dan Structured Outputs tidak kompatibel**

Sitasi tidak dapat digunakan bersama dengan [Structured Outputs](/docs/id/build-with-claude/structured-outputs). Jika Anda mengaktifkan sitasi pada dokumen apa pun yang disediakan pengguna (blok Document atau RequestSearchResultBlock) dan juga menyertakan parameter `output_config.format` (atau parameter `output_format` yang sudah tidak digunakan lagi), API akan mengembalikan error 400.

Hal ini karena sitasi memerlukan penyisipan blok sitasi di antara output teks, yang tidak kompatibel dengan batasan skema JSON yang ketat dari structured outputs.
</Warning>

#### Menggunakan Caching Prompt dengan Sitasi \{#using-prompt-caching-with-citations}

Sitasi dan caching prompt dapat digunakan bersama secara efektif.

Blok sitasi yang dihasilkan dalam respons tidak dapat di-cache secara langsung, tetapi dokumen sumber yang dirujuknya dapat di-cache. Untuk mengoptimalkan kinerja, terapkan `cache_control` pada blok konten dokumen tingkat atas Anda.

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data '{
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

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Konten dokumen panjang (mis., dokumentasi teknis)
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

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// Konten dokumen panjang (mis., dokumentasi teknis)
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
```
</CodeGroup>

Dalam contoh ini:
- Konten dokumen di-cache menggunakan `cache_control` pada blok dokumen
- Sitasi diaktifkan pada dokumen
- Claude dapat menghasilkan respons dengan sitasi sambil mendapatkan manfaat dari konten dokumen yang di-cache
- Permintaan berikutnya yang menggunakan dokumen yang sama akan mendapatkan manfaat dari konten yang di-cache

## Jenis Dokumen \{#document-types}

### Memilih jenis dokumen \{#choosing-a-document-type}

Tiga jenis dokumen didukung untuk sitasi. Dokumen dapat disediakan langsung dalam pesan (base64, teks, atau URL) atau diunggah melalui [Files API](/docs/id/build-with-claude/files) dan direferensikan dengan `file_id`:

| Jenis | Paling cocok untuk | Pemecahan (chunking) | Format sitasi |
| :--- | :--- | :--- | :--- |
| Teks biasa | Dokumen teks sederhana, prosa | Kalimat | Indeks karakter (dimulai dari 0) |
| PDF | File PDF dengan konten teks | Kalimat | Nomor halaman (dimulai dari 1) |
| Konten kustom | Daftar, transkrip, pemformatan khusus, sitasi yang lebih granular | Tidak ada pemecahan tambahan | Indeks blok (dimulai dari 0) |

<Note>
File .csv, .xlsx, .docx, .md, dan .txt tidak didukung sebagai blok dokumen. Konversikan file-file ini ke teks biasa dan sertakan langsung dalam konten pesan. Lihat [Bekerja dengan format file lainnya](/docs/id/build-with-claude/files#working-with-other-file-formats).
</Note>

### Dokumen teks biasa \{#plain-text-documents}

Dokumen teks biasa secara otomatis dipecah menjadi kalimat. Anda dapat menyediakannya secara inline atau dengan referensi menggunakan `file_id`:

<Tabs>
<Tab title="Teks inline">
```python
{
    "type": "document",
    "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": "Plain text content...",
    },
    "title": "Document Title",  # optional
    "context": "Context about the document that will not be cited from",  # optional
    "citations": {"enabled": True},
}
```
</Tab>
<Tab title="Files API">
```python
{
    "type": "document",
    "source": {"type": "file", "file_id": "file_011CNvxoj286tYUAZFiZMf1U"},
    "title": "Document Title",  # optional
    "context": "Context about the document that will not be cited from",  # optional
    "citations": {"enabled": True},
}
```
</Tab>
</Tabs>

<section title="Contoh sitasi teks biasa">

```python
{
    "type": "char_location",
    "cited_text": "The exact text being cited",  # not counted towards output tokens
    "document_index": 0,
    "document_title": "Document Title",
    "start_char_index": 0,  # 0-indexed
    "end_char_index": 50,  # exclusive
}
```

</section>

### Dokumen PDF \{#pdf-documents}

Dokumen PDF dapat disediakan sebagai data yang dikodekan base64, URL, atau dengan `file_id`. Teks PDF diekstrak dan dipecah menjadi kalimat. Karena sitasi gambar belum didukung, PDF yang merupakan hasil pemindaian dokumen dan tidak berisi teks yang dapat diekstrak tidak akan dapat dikutip.

<Tabs>
<Tab title="Base64">
```python
{
    "type": "document",
    "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": base64_encoded_pdf_data,
    },
    "title": "Document Title",  # optional
    "context": "Context about the document that will not be cited from",  # optional
    "citations": {"enabled": True},
}
```
</Tab>
<Tab title="URL">
```python
{
    "type": "document",
    "source": {"type": "url", "url": "https://example.com/document.pdf"},
    "title": "Document Title",  # optional
    "context": "Context about the document that will not be cited from",  # optional
    "citations": {"enabled": True},
}
```
</Tab>
<Tab title="Files API">
```python
{
    "type": "document",
    "source": {"type": "file", "file_id": "file_011CNvxoj286tYUAZFiZMf1U"},
    "title": "Document Title",  # optional
    "context": "Context about the document that will not be cited from",  # optional
    "citations": {"enabled": True},
}
```
</Tab>
</Tabs>

<section title="Contoh sitasi PDF">

```python
{
    "type": "page_location",
    "cited_text": "The exact text being cited",  # not counted towards output tokens
    "document_index": 0,
    "document_title": "Document Title",
    "start_page_number": 1,  # 1-indexed
    "end_page_number": 2,  # exclusive
}
```

</section>

### Dokumen konten kustom \{#custom-content-documents}

Dokumen konten kustom memberi Anda kontrol atas granularitas sitasi. Tidak ada pemecahan tambahan yang dilakukan dan chunk disediakan ke model sesuai dengan blok konten yang disediakan.

```python
{
    "type": "document",
    "source": {
        "type": "content",
        "content": [
            {"type": "text", "text": "First chunk"},
            {"type": "text", "text": "Second chunk"},
        ],
    },
    "title": "Document Title",  # optional
    "context": "Context about the document that will not be cited from",  # optional
    "citations": {"enabled": True},
}
```

<section title="Contoh sitasi">

```python
{
    "type": "content_block_location",
    "cited_text": "The exact text being cited",  # not counted towards output tokens
    "document_index": 0,
    "document_title": "Document Title",
    "start_block_index": 0,  # 0-indexed
    "end_block_index": 1,  # exclusive
}
```

</section>

---

## Struktur Respons \{#response-structure}

Ketika sitasi diaktifkan, respons menyertakan beberapa blok teks dengan sitasi:

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

### Dukungan Streaming \{#streaming-support}

Untuk respons streaming, tipe `citations_delta` disertakan yang berisi satu sitasi untuk ditambahkan ke daftar `citations` pada blok konten `text` saat ini.

<section title="Contoh event streaming">

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

</section>