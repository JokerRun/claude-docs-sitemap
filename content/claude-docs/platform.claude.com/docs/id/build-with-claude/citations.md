---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/citations
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 5656e64c6ff58e7d5241693d740389fef90a730d7b1cc70b27873c50b4cdbb70
---

# Kutipan

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Claude mampu memberikan kutipan terperinci saat menjawab pertanyaan tentang dokumen, membantu Anda melacak dan memverifikasi sumber informasi dalam respons.

Semua [model aktif](/docs/id/about-claude/models/overview) mendukung kutipan, kecuali Haiku 3.

<Tip>
  Bagikan masukan dan saran Anda tentang fitur kutipan menggunakan [formulir](https://forms.gle/9n9hSrKnKe3rpowH9) ini.
</Tip>

Berikut adalah contoh cara menggunakan kutipan dengan Messages API:

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
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
model: claude-opus-4-6
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
    model="claude-opus-4-6",
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
      .model(Model.CLAUDE_OPUS_4_6)
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

Dibandingkan dengan solusi kutipan berbasis prompt, fitur kutipan memiliki keunggulan berikut:
- **Penghematan biaya:** Jika pendekatan berbasis prompt Anda meminta Claude untuk mengeluarkan kutipan langsung, Anda mungkin melihat penghematan biaya karena `cited_text` tidak dihitung sebagai token output.
- **Keandalan kutipan yang lebih baik:** Karena kutipan diurai ke dalam format respons masing-masing yang disebutkan di atas dan `cited_text` diekstrak, kutipan dijamin mengandung penunjuk yang valid ke dokumen yang disediakan.
- **Kualitas kutipan yang lebih baik:** Dalam evaluasi, fitur kutipan ditemukan jauh lebih mungkin untuk mengutip kutipan yang paling relevan dari dokumen dibandingkan dengan pendekatan berbasis prompt murni.
</Tip>

---

## Cara kerja kutipan

Integrasikan kutipan dengan Claude dalam langkah-langkah berikut:

<Steps>
  <Step title="Sediakan dokumen dan aktifkan kutipan">
    - Sertakan dokumen dalam salah satu format yang didukung: dokumen [PDF](#pdf-documents), [teks biasa](#plain-text-documents), atau [konten kustom](#custom-content-documents)
    - Atur `citations.enabled=true` pada setiap dokumen Anda. Saat ini, kutipan harus diaktifkan pada semua atau tidak ada dokumen dalam suatu permintaan.
    - Perhatikan bahwa hanya kutipan teks yang saat ini didukung dan kutipan gambar belum tersedia.
  </Step>
  <Step title="Dokumen diproses">
    - Konten dokumen "dipotong" untuk mendefinisikan granularitas minimum dari kemungkinan kutipan. Misalnya, pemotongan kalimat akan memungkinkan Claude untuk mengutip satu kalimat atau menggabungkan beberapa kalimat berurutan untuk mengutip sebuah paragraf (atau lebih panjang)!
      - **Untuk PDF:** Teks diekstrak seperti yang dijelaskan dalam [Dukungan PDF](/docs/id/build-with-claude/pdf-support) dan konten dipotong menjadi kalimat. Mengutip gambar dari PDF saat ini tidak didukung.
      - **Untuk dokumen teks biasa:** Konten dipotong menjadi kalimat yang dapat dikutip.
      - **Untuk dokumen konten kustom:** Blok konten yang Anda sediakan digunakan apa adanya dan tidak ada pemotongan lebih lanjut yang dilakukan.
  </Step>
  <Step title="Claude memberikan respons yang dikutip">
    - Respons sekarang dapat mencakup beberapa blok teks di mana setiap blok teks dapat berisi klaim yang dibuat Claude dan daftar kutipan yang mendukung klaim tersebut.
    - Kutipan merujuk pada lokasi tertentu dalam dokumen sumber. Format kutipan ini bergantung pada jenis dokumen yang dikutip.
      - **Untuk PDF:** Kutipan mencakup rentang nomor halaman (diindeks dari 1).
      - **Untuk dokumen teks biasa:** Kutipan mencakup rentang indeks karakter (diindeks dari 0).
      - **Untuk dokumen konten kustom:** Kutipan mencakup rentang indeks blok konten (diindeks dari 0) yang sesuai dengan daftar konten asli yang disediakan.
    - Indeks dokumen disediakan untuk menunjukkan sumber referensi dan diindeks dari 0 sesuai dengan daftar semua dokumen dalam permintaan asli Anda.
  </Step>
</Steps>

<Tip>
  **Pemotongan otomatis vs konten kustom**

  Secara default, dokumen teks biasa dan PDF dipotong secara otomatis menjadi kalimat. Jika Anda memerlukan kontrol lebih besar atas granularitas kutipan (misalnya, untuk poin-poin atau transkrip), gunakan dokumen konten kustom sebagai gantinya. Lihat [Jenis Dokumen](#document-types) untuk detail lebih lanjut.

  Misalnya, jika Anda ingin Claude dapat mengutip kalimat tertentu dari potongan RAG Anda, Anda harus menempatkan setiap potongan RAG ke dalam dokumen teks biasa. Jika tidak, jika Anda tidak ingin pemotongan lebih lanjut dilakukan, atau jika Anda ingin menyesuaikan pemotongan tambahan, Anda dapat menempatkan potongan RAG ke dalam dokumen konten kustom.
</Tip>

### Konten yang dapat dikutip vs tidak dapat dikutip

- Teks yang ditemukan dalam konten `source` dokumen dapat dikutip.
- `title` dan `context` adalah bidang opsional yang akan diteruskan ke model tetapi tidak digunakan untuk konten yang dikutip.
- `title` dibatasi panjangnya sehingga Anda mungkin menemukan bidang `context` berguna untuk menyimpan metadata dokumen apa pun sebagai teks atau json yang diubah menjadi string.

### Indeks kutipan
- Indeks dokumen diindeks dari 0 dari daftar semua blok konten dokumen dalam permintaan (mencakup semua pesan).
- Indeks karakter diindeks dari 0 dengan indeks akhir eksklusif.
- Nomor halaman diindeks dari 1 dengan nomor halaman akhir eksklusif.
- Indeks blok konten diindeks dari 0 dengan indeks akhir eksklusif dari daftar `content` yang disediakan dalam dokumen konten kustom.

### Biaya token
- Mengaktifkan kutipan menyebabkan sedikit peningkatan token input karena penambahan system prompt dan pemotongan dokumen.
- Namun, fitur kutipan sangat efisien dengan token output. Di balik layar, model mengeluarkan kutipan dalam format standar yang kemudian diurai menjadi teks yang dikutip dan indeks lokasi dokumen. Bidang `cited_text` disediakan untuk kenyamanan dan tidak dihitung sebagai token output.
- Ketika diteruskan kembali dalam giliran percakapan berikutnya, `cited_text` juga tidak dihitung sebagai token input.

### Kompatibilitas fitur
Kutipan bekerja bersama dengan fitur API lainnya termasuk [prompt caching](/docs/id/build-with-claude/prompt-caching), [penghitungan token](/docs/id/build-with-claude/token-counting) dan [pemrosesan batch](/docs/id/build-with-claude/batch-processing).

<Warning>
**Kutipan dan Structured Outputs tidak kompatibel**

Kutipan tidak dapat digunakan bersama dengan [Structured Outputs](/docs/id/build-with-claude/structured-outputs). Jika Anda mengaktifkan kutipan pada dokumen yang disediakan pengguna (blok Dokumen atau RequestSearchResultBlock) dan juga menyertakan parameter `output_config.format` (atau parameter `output_format` yang sudah usang), API akan mengembalikan kesalahan 400.

Ini karena kutipan memerlukan penyisipan blok kutipan dengan output teks, yang tidak kompatibel dengan batasan skema JSON ketat dari structured outputs.
</Warning>

#### Menggunakan Prompt Caching dengan Kutipan

Kutipan dan prompt caching dapat digunakan bersama secara efektif.

Blok kutipan yang dihasilkan dalam respons tidak dapat di-cache secara langsung, tetapi dokumen sumber yang dirujuknya dapat di-cache. Untuk mengoptimalkan kinerja, terapkan `cache_control` ke blok konten dokumen tingkat atas Anda.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data '{
    "model": "claude-opus-4-6",
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
  --model claude-opus-4-6 \
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

# Konten dokumen panjang (misalnya, dokumentasi teknis)
long_document = (
    "This is a very long document with thousands of words..." + " ... " * 1000
)  # Panjang minimum yang dapat di-cache

response = client.messages.create(
    model="claude-opus-4-6",
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
                    },  # Cache konten dokumen
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

// Konten dokumen panjang (misalnya, dokumentasi teknis)
const longDocument =
  "This is a very long document with thousands of words..." + " ... ".repeat(1000); // Panjang minimum yang dapat di-cache

const response = await client.messages.create({
  model: "claude-opus-4-6",
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
          cache_control: { type: "ephemeral" } // Cache konten dokumen
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
- Kutipan diaktifkan pada dokumen
- Claude dapat menghasilkan respons dengan kutipan sambil mendapat manfaat dari konten dokumen yang di-cache
- Permintaan berikutnya yang menggunakan dokumen yang sama akan mendapat manfaat dari konten yang di-cache

## Jenis Dokumen

### Memilih jenis dokumen

Tiga jenis dokumen didukung untuk kutipan. Dokumen dapat disediakan langsung dalam pesan (base64, teks, atau URL) atau diunggah melalui [Files API](/docs/id/build-with-claude/files) dan dirujuk dengan `file_id`:

| Jenis | Terbaik untuk | Pemotongan | Format kutipan |
| :--- | :--- | :--- | :--- |
| Teks biasa | Dokumen teks sederhana, prosa | Kalimat | Indeks karakter (diindeks dari 0) |
| PDF | File PDF dengan konten teks | Kalimat | Nomor halaman (diindeks dari 1) |
| Konten kustom | Daftar, transkrip, pemformatan khusus, kutipan yang lebih granular | Tidak ada pemotongan tambahan | Indeks blok (diindeks dari 0) |

<Note>
File .csv, .xlsx, .docx, .md, dan .txt tidak didukung sebagai blok dokumen. Konversi file-file ini ke teks biasa dan sertakan langsung dalam konten pesan. Lihat [Bekerja dengan format file lain](/docs/id/build-with-claude/files#working-with-other-file-formats).
</Note>

### Dokumen teks biasa

Dokumen teks biasa dipotong secara otomatis menjadi kalimat. Anda dapat menyediakannya secara inline atau dengan referensi menggunakan `file_id`:

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
    "title": "Document Title",  # opsional
    "context": "Context about the document that will not be cited from",  # opsional
    "citations": {"enabled": True},
}
```
</Tab>
<Tab title="Files API">
```python
{
    "type": "document",
    "source": {"type": "file", "file_id": "file_011CNvxoj286tYUAZFiZMf1U"},
    "title": "Document Title",  # opsional
    "context": "Context about the document that will not be cited from",  # opsional
    "citations": {"enabled": True},
}
```
</Tab>
</Tabs>

<section title="Contoh kutipan teks biasa">

```python
{
    "type": "char_location",
    "cited_text": "The exact text being cited",  # tidak dihitung sebagai token output
    "document_index": 0,
    "document_title": "Document Title",
    "start_char_index": 0,  # diindeks dari 0
    "end_char_index": 50,  # eksklusif
}
```

</section>

### Dokumen PDF

Dokumen PDF dapat disediakan sebagai data yang dikodekan base64 atau dengan `file_id`. Teks PDF diekstrak dan dipotong menjadi kalimat. Karena kutipan gambar belum didukung, PDF yang merupakan hasil pemindaian dokumen dan tidak mengandung teks yang dapat diekstrak tidak akan dapat dikutip.

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
    "title": "Document Title",  # opsional
    "context": "Context about the document that will not be cited from",  # opsional
    "citations": {"enabled": True},
}
```
</Tab>
<Tab title="Files API">
```python
{
    "type": "document",
    "source": {"type": "file", "file_id": "file_011CNvxoj286tYUAZFiZMf1U"},
    "title": "Document Title",  # opsional
    "context": "Context about the document that will not be cited from",  # opsional
    "citations": {"enabled": True},
}
```
</Tab>
</Tabs>

<section title="Contoh kutipan PDF">

```python
{
    "type": "page_location",
    "cited_text": "The exact text being cited",  # tidak dihitung sebagai token output
    "document_index": 0,
    "document_title": "Document Title",
    "start_page_number": 1,  # diindeks dari 1
    "end_page_number": 2,  # eksklusif
}
```

</section>

### Dokumen konten kustom

Dokumen konten kustom memberi Anda kontrol atas granularitas kutipan. Tidak ada pemotongan tambahan yang dilakukan dan potongan disediakan ke model sesuai dengan blok konten yang disediakan.

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
    "title": "Document Title",  # opsional
    "context": "Context about the document that will not be cited from",  # opsional
    "citations": {"enabled": True},
}
```

<section title="Contoh kutipan">

```python
{
    "type": "content_block_location",
    "cited_text": "The exact text being cited",  # tidak dihitung sebagai token output
    "document_index": 0,
    "document_title": "Document Title",
    "start_block_index": 0,  # diindeks dari 0
    "end_block_index": 1,  # eksklusif
}
```

</section>

---

## Struktur Respons

Ketika kutipan diaktifkan, respons mencakup beberapa blok teks dengan kutipan:

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

### Dukungan Streaming

Untuk respons streaming, tipe `citations_delta` disertakan yang berisi satu kutipan yang akan ditambahkan ke daftar `citations` pada blok konten `text` saat ini.

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