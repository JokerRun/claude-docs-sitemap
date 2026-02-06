---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/interview-question-crafter
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: b572b4f9d825a8956069f681489c6ad6f38f36c9780071f79b8602081bfd392d
---

# Pembuat pertanyaan wawancara

Hasilkan pertanyaan untuk wawancara.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Tugas Anda adalah menghasilkan serangkaian pertanyaan yang bijaksana dan terbuka untuk wawancara berdasarkan konteks yang diberikan. Pertanyaan harus dirancang untuk mendapatkan respons yang mendalam dan terperinci dari pewawancara, memungkinkan mereka menampilkan pengetahuan, pengalaman, dan keterampilan berpikir kritis mereka. Hindari pertanyaan ya/tidak atau pertanyaan dengan jawaban yang jelas. Sebaliknya, fokus pada pertanyaan yang mendorong refleksi, penilaian diri, dan berbagi contoh atau anekdot spesifik. |
| Pengguna   | Anda sedang mewawancarai kandidat untuk posisi manajer pemasaran di perusahaan e-commerce yang sudah mapan. Kandidat ideal harus memiliki pengalaman mengembangkan dan melaksanakan kampanye pemasaran multi-saluran, keterampilan analitik yang kuat, dan kemampuan untuk berkolaborasi secara efektif dengan tim lintas fungsi. Mereka juga harus bersemangat tentang tetap mengikuti tren dan teknologi pemasaran terbaru.                                                                             |

## Contoh Output

1.  Bisakah Anda membimbing saya melalui kampanye pemasaran multi-saluran yang sukses yang Anda kembangkan dan jalankan di peran sebelumnya? Tantangan apa yang Anda hadapi, dan bagaimana Anda mengatasinya?
2.  Bagaimana Anda mengukur kesuksesan kampanye pemasaran Anda, dan metrik apa yang Anda fokuskan? Bisakah Anda memberikan contoh tentang bagaimana Anda menggunakan data dan analitik untuk mengoptimalkan kinerja kampanye?
3.  Berdasarkan pengalaman Anda, apa elemen kunci dari strategi pemasaran e-commerce yang sukses? Bagaimana Anda memastikan bahwa strategi Anda sejalan dengan tujuan bisnis keseluruhan perusahaan?
4.  Bisakah Anda berbagi contoh waktu ketika Anda harus berkolaborasi dengan tim lintas fungsi (misalnya, produk, penjualan, atau layanan pelanggan) untuk mencapai tujuan pemasaran? Tantangan apa yang Anda hadapi, dan bagaimana Anda mendorong kolaborasi yang efektif?
5.  Bagaimana Anda tetap terinformasi tentang tren dan teknologi pemasaran terbaru, dan bagaimana Anda menerapkan pengetahuan ini untuk meningkatkan strategi atau kampanye pemasaran Anda?
6.  Bisakah Anda menjelaskan waktu ketika kampanye pemasaran yang Anda libatkan tidak berkinerja seperti yang diharapkan? Apa yang Anda pelajari dari pengalaman tersebut, dan bagaimana Anda menerapkan pelajaran tersebut ke kampanye di masa depan?
7.  Perusahaan kami menghargai inovasi dan peningkatan berkelanjutan. Bisakah Anda berbagi contoh waktu ketika Anda memperkenalkan pendekatan, alat, atau teknologi pemasaran baru yang berdampak signifikan pada kinerja atau hasil tim Anda?

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
  max_tokens=1000,
  temperature=0.5,
  system="Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
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
  max_tokens: 1000,
  temperature: 0.5,
  system: "Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
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
    max_tokens=1000,
    temperature=0.5,
    system="Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
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
  max_tokens: 1000,
  temperature: 0.5,
  system: "Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
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
    max_tokens=1000,
    temperature=0.5,
    system="Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
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
  max_tokens: 1000,
  temperature: 0.5,
  system: "Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>