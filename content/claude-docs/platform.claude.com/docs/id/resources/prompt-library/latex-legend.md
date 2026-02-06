---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/latex-legend
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 2d4c313aa0a3f5e1ff65ac6e84ff6074ab281ddd9566eac7934a87bf2ad99a9b
---

# Legenda LaTeX

Tulis dokumen LaTeX, menghasilkan kode untuk persamaan matematika, tabel, dan lainnya.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                              |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Anda adalah asisten AI dengan keahlian dalam LaTeX, sistem persiapan dokumen yang banyak digunakan untuk penulisan akademik dan teknis. Tugas Anda adalah membantu pengguna menulis dokumen LaTeX dengan menyediakan kode yang sesuai untuk berbagai elemen seperti persamaan matematika, tabel, dan lainnya. Tawarkan penjelasan dan contoh yang jelas untuk memastikan pengguna memahami cara menggunakan kode LaTeX secara efektif. |
| Pengguna   | Saya perlu membuat tabel sederhana dengan tiga kolom dan dua baris. Baris header harus berisi judul "Nama," "Usia," dan "Kota." Baris data harus memiliki nilai "John," "25," dan "New York."                                                                                                                                                                                               |

## Contoh Output

Berikut adalah kode LaTeX untuk membuat tabel sederhana dengan tiga kolom dan dua baris, termasuk baris header dengan judul "Nama," "Usia," dan "Kota," serta baris data dengan nilai "John," "25," dan "New York":

```latex
\begin{table}[h]
\centering
\begin{tabular}{|c|c|c|}
\hline
Name & Age & City \\
\hline
John & 25 & New York \\
\hline
\end{tabular}
\caption{Sample Table}
\label{tab:sample}
\end{table}

```

Penjelasan:

- Lingkungan `table` digunakan untuk membuat tabel mengambang yang dapat diposisikan secara otomatis oleh LaTeX.
- Parameter opsional `[h]` menyarankan kepada LaTeX untuk menempatkan tabel "di sini" dalam aliran dokumen, jika memungkinkan.
- Perintah `\centering` memusatkan tabel secara horizontal di halaman.
- Lingkungan `tabular` digunakan untuk membuat struktur tabel yang sebenarnya.
- Argumen `{|c|c|c|}` menentukan tiga kolom berpusat (`c`) yang dipisahkan oleh garis vertikal (`|`).
- Perintah `\hline` menambahkan garis horizontal untuk memisahkan baris header dari baris data dan untuk membingkai tabel.
- Karakter `&` memisahkan sel dalam baris, dan `\\` menandai akhir baris.
- Perintah `\caption` menambahkan keterangan ke tabel, yang akan diberi label "Sample Table" dalam contoh ini.
- Perintah `\label` menetapkan label ke tabel, yang dapat digunakan untuk referensi silang dalam dokumen Anda.

Ketika Anda mengompilasi dokumen LaTeX Anda, kode ini akan menghasilkan tabel yang terlihat seperti ini:

```
+------+-----+----------+
| Name | Age |   City   |
+------+-----+----------+
| John |  25 | New York |
+------+-----+----------+

```

---

## Permintaan API

<Tabs>
<Tab title="Python">
```python
import anthropic

client = anthropic.Anthropic(  # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2000,
    temperature=0,
    system="You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": 'I need to create a simple table with three columns and two rows. The header row should contain the titles "Name," "Age," and "City." The data row should have the values "John," "25," and "New York."',
                }
            ],
        }
    ],
)
print(message.content)


````
</Tab>
<Tab title="TypeScript">
```typescript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
});

const msg = await anthropic.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 2000,
  temperature: 0,
  system: "You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I need to create a simple table with three columns and two rows. The header row should contain the titles \"Name,\" \"Age,\" and \"City.\" The data row should have the values \"John,\" \"25,\" and \"New York.\""
        }
      ]
    }
  ]
});
console.log(msg);

````

</Tab>
<Tab title="AWS Bedrock Python">
```python
from anthropic import AnthropicBedrock

# See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock

# for authentication options

client = AnthropicBedrock()

message = client.messages.create(
model="anthropic.claude-opus-4-6-v1:0",
max_tokens=2000,
temperature=0,
system="You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
messages=[
{
"role": "user",
"content": [
{
"type": "text",
"text": "I need to create a simple table with three columns and two rows. The header row should contain the titles \"Name,\" \"Age,\" and \"City.\" The data row should have the values \"John,\" \"25,\" and \"New York.\""
}
]
}
]
)
print(message.content)

````
</Tab>
<Tab title="AWS Bedrock TypeScript">
```typescript
import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

// See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
// for authentication options
const client = new AnthropicBedrock();

const msg = await client.messages.create({
  model: "anthropic.claude-opus-4-6-v1:0",
  max_tokens: 2000,
  temperature: 0,
  system: "You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I need to create a simple table with three columns and two rows. The header row should contain the titles \"Name,\" \"Age,\" and \"City.\" The data row should have the values \"John,\" \"25,\" and \"New York.\""
        }
      ]
    }
  ]
});
console.log(msg);

````

</Tab>
<Tab title="Vertex AI Python">
```python
from anthropic import AnthropicVertex

client = AnthropicVertex()

message = client.messages.create(
model="claude-sonnet-4@20250514",
max_tokens=2000,
temperature=0,
system="You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
messages=[
{
"role": "user",
"content": [
{
"type": "text",
"text": "I need to create a simple table with three columns and two rows. The header row should contain the titles \"Name,\" \"Age,\" and \"City.\" The data row should have the values \"John,\" \"25,\" and \"New York.\""
}
]
}
]
)
print(message.content)

````
</Tab>
<Tab title="Vertex AI TypeScript">

```typescript
import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';

// Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
// Additionally goes through the standard `google-auth-library` flow.
const client = new AnthropicVertex();

const msg = await client.messages.create({
  model: "claude-sonnet-4@20250514",
  max_tokens: 2000,
  temperature: 0,
  system: "You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I need to create a simple table with three columns and two rows. The header row should contain the titles \"Name,\" \"Age,\" and \"City.\" The data row should have the values \"John,\" \"25,\" and \"New York.\""
        }
      ]
    }
  ]
});
console.log(msg);

````

</Tab>
</Tabs>