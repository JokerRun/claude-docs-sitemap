---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/trivia-generator
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: a6cf77ce9b8095ce08ed09e9ff24887eacea45ef26f588c929b42ea3dc2a6d6a
---

# Pembuat trivia

Hasilkan pertanyaan trivia pada berbagai topik dan berikan petunjuk saat diperlukan.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

| Peran | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pengguna | Hasilkan pertanyaan trivia pada berbagai topik dan berikan petunjuk untuk membantu pengguna sampai pada jawaban yang benar. Pilih dari beragam kategori dan buat pertanyaan yang menguji pengetahuan atau keterampilan penalaran pengguna. Tawarkan serangkaian petunjuk yang semakin spesifik untuk memandu pengguna menuju solusi. Pastikan bahwa pertanyaan menantang dan petunjuk memberikan informasi yang cukup untuk membantu pengguna tanpa memberikan jawaban terlalu mudah. |

## Contoh Output

Kategori: Geografi

Pertanyaan:  
 Apa satu-satunya negara di dunia yang berbatasan dengan Prancis dan Spanyol?

Petunjuk 1: Negara ini terletak di pegunungan Pyrenees antara Prancis dan Spanyol.  
 Petunjuk 2: Negara ini dikenal karena pemandangan pegunungannya yang menakjubkan, resor ski, dan belanja bebas pajak.  
 Petunjuk 3: Kota ibu kota negara ini menampilkan nama negara itu sendiri.

Jawaban: Andorra

Kategori: Sains

Pertanyaan:  
 Apa proses di mana tumbuhan mengubah sinar matahari, air, dan karbon dioksida menjadi energi dan oksigen?

Petunjuk 1: Proses ini penting bagi kehidupan di Bumi, karena menyediakan makanan dan oksigen.  
 Petunjuk 2: Proses ini terjadi terutama di daun tumbuhan.  
 Petunjuk 3: Proses ini melibatkan klorofil, pigmen hijau yang menyerap sinar matahari.

Jawaban: Fotosintesis

Kategori: Sastra

Pertanyaan:  
 Siapa yang menulis novel klasik "Pride and Prejudice," yang pertama kali diterbitkan pada tahun 1813?

Petunjuk 1: Penulis adalah seorang wanita Inggris yang hidup dari 1775 hingga 1817.  
 Petunjuk 2: Dia dikenal karena penggambaran yang cerdas dan mendalam tentang masyarakat dan tata krama Inggris.  
 Petunjuk 3: Karya terkenal lainnya termasuk "Sense and Sensibility" dan "Emma."

Jawaban: Jane Austen

Kategori: Sejarah

Pertanyaan:  
 Pada tahun berapa Tembok Berlin, yang membagi Jerman Timur dan Barat, mulai dihancurkan?

Petunjuk 1: Peristiwa ini terjadi pada akhir abad ke-20.  
 Petunjuk 2: Ini menandai momen penting dalam berakhirnya Perang Dingin.  
 Petunjuk 3: Tahun ini sering dikaitkan dengan frasa "jatuhnya komunisme" di Eropa.

Jawaban: 1989

---

## Permintaan API

<Tabs>
<Tab title="Python">

```python
import anthropic

client = anthropic.Anthropic(
  # defaults to os.environ.get("ANTHROPIC_API_KEY")
  api_key="my_api_key",
)
message = client.messages.create(
  model="claude-opus-4-6",
  max_tokens=2000,
  temperature=0.5,
  messages=[
    {
    "role": "user",
    "content": [
        {
          "type": "text",
          "text": "Generate trivia questions on various topics and provide hints to help users arrive at the correct answer. Select from a diverse set of categories and create questions that test the user's knowledge or reasoning skills. Offer a series of increasingly specific hints to guide users towards the solution. Ensure that the questions are challenging and that the hints provide enough information to help the user without giving away the answer too easily."
        }
      ]
    }
  ]
)
print(message.content)

```

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
  temperature: 0.5,
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate trivia questions on various topics and provide hints to help users arrive at the correct answer. Select from a diverse set of categories and create questions that test the user's knowledge or reasoning skills. Offer a series of increasingly specific hints to guide users towards the solution. Ensure that the questions are challenging and that the hints provide enough information to help the user without giving away the answer too easily."
        }
      ]
    }
  ]
});
console.log(msg);

```

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
temperature=0.5,
messages=[
{
"role": "user",
"content": [
{
"type": "text",
"text": "Generate trivia questions on various topics and provide hints to help users arrive at the correct answer. Select from a diverse set of categories and create questions that test the user's knowledge or reasoning skills. Offer a series of increasingly specific hints to guide users towards the solution. Ensure that the questions are challenging and that the hints provide enough information to help the user without giving away the answer too easily."
}
]
}
]
)
print(message.content)

```

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
  temperature: 0.5,
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate trivia questions on various topics and provide hints to help users arrive at the correct answer. Select from a diverse set of categories and create questions that test the user's knowledge or reasoning skills. Offer a series of increasingly specific hints to guide users towards the solution. Ensure that the questions are challenging and that the hints provide enough information to help the user without giving away the answer too easily."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
<Tab title="Vertex AI Python">

```python
from anthropic import AnthropicVertex

client = AnthropicVertex()

message = client.messages.create(
    model="claude-sonnet-4@20250514",
    max_tokens=2000,
    temperature=0.5,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate trivia questions on various topics and provide hints to help users arrive at the correct answer. Select from a diverse set of categories and create questions that test the user's knowledge or reasoning skills. Offer a series of increasingly specific hints to guide users towards the solution. Ensure that the questions are challenging and that the hints provide enough information to help the user without giving away the answer too easily."
                }
            ]
        }
    ]
)
print(message.content)

```

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
  temperature: 0.5,
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate trivia questions on various topics and provide hints to help users arrive at the correct answer. Select from a diverse set of categories and create questions that test the user's knowledge or reasoning skills. Offer a series of increasingly specific hints to guide users towards the solution. Ensure that the questions are challenging and that the hints provide enough information to help the user without giving away the answer too easily."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>