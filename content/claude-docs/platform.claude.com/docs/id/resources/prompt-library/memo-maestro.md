---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/memo-maestro
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 49c39dac5ea29d5d429d0f8a88e1e596bfe7ca73363d35dbdc319cff964517e0
---

# Memo maestro

Susun memo perusahaan yang komprehensif berdasarkan poin-poin kunci.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Tugas Anda adalah menyusun memo perusahaan yang komprehensif berdasarkan poin-poin kunci yang diberikan. Memo harus ditulis dengan nada profesional, mengatasi semua informasi yang relevan dengan cara yang jelas dan ringkas. Gunakan pemformatan yang sesuai, seperti judul, subjudul, dan poin-poin, untuk mengorganisir konten secara efektif. Pastikan bahwa memo terstruktur dengan baik, koheren, dan mudah dipahami oleh audiens yang dituju.                                                                                                                                                                                                                                        |
| Pengguna   | - Pengumuman program kesejahteraan karyawan baru: "Fit4Success" <br/> - Tujuan program: mempromosikan kesejahteraan fisik dan mental, mengurangi stres, dan meningkatkan produktivitas <br/> - Komponen: kelas kebugaran di tempat, opsi makanan sehat, sumber daya kesehatan mental, dan workshop kesejahteraan <br/> - Kemitraan dengan gym lokal dan pusat kesejahteraan untuk keanggotaan diskon <br/> - Insentif untuk partisipasi: pelacak kebugaran, poin kesejahteraan, dan undian hadiah <br/> - Tanggal peluncuran program: 1 Juni 2023 <br/> - Proses pendaftaran: pendaftaran online melalui intranet perusahaan <br/> - Koordinator program: tim Sumber Daya Manusia dan Keterlibatan Karyawan |

## Contoh Output

Subjek: Memperkenalkan Fit4Success - Program Kesejahteraan Karyawan Baru Kami

Hai semua,

Saya dengan senang hati mengumumkan peluncuran program kesejahteraan karyawan baru kami, Fit4Success, yang dirancang untuk mempromosikan kesejahteraan fisik dan mental, mengurangi stres, dan meningkatkan produktivitas di antara anggota tim kami. Program akan secara resmi dimulai pada 1 Juni 2023.

Tujuan Program:

- Mendorong aktivitas fisik reguler dan pilihan gaya hidup sehat
- Menyediakan sumber daya dan dukungan untuk kesehatan mental dan manajemen stres
- Memupuk lingkungan kerja yang positif dan menarik yang memprioritaskan kesejahteraan karyawan
- Meningkatkan produktivitas dan kepuasan kerja secara keseluruhan

Komponen Program:

- Kelas kebugaran di tempat: sesi yoga, Pilates, dan pelatihan interval intensitas tinggi (HIIT)
- Opsi makanan sehat: camilan dan makanan bergizi yang tersedia di kafeteria perusahaan
- Sumber daya kesehatan mental: akses ke layanan konseling, aplikasi meditasi, dan workshop manajemen stres
- Workshop kesejahteraan: seminar tentang topik seperti nutrisi, kebersihan tidur, dan keseimbangan kehidupan kerja

Kemitraan dan Diskon:  
 Untuk lebih mendukung perjalanan kesejahteraan Anda, kami telah bermitra dengan gym lokal dan pusat kesejahteraan untuk menawarkan keanggotaan diskon secara eksklusif untuk karyawan kami. Manfaatkan tarif khusus ini untuk mengakses berbagai fasilitas dan kelas kebugaran.

Insentif untuk Partisipasi:  
 Untuk mendorong partisipasi aktif dalam program Fit4Success, kami akan menawarkan insentif berikut:

- Pelacak kebugaran untuk semua peserta untuk memantau kemajuan mereka dan menetapkan tujuan pribadi
- Poin kesejahteraan yang diperoleh melalui partisipasi program, dapat ditukar dengan hadiah tambahan
- Undian hadiah bulanan untuk peserta yang mencapai tonggak kesejahteraan tertentu

Proses Pendaftaran:  
 Untuk mendaftar dalam program Fit4Success, silakan kunjungi intranet perusahaan kami dan lengkapi formulir pendaftaran online. Batas waktu pendaftaran adalah 25 Mei 2023. Jika Anda memiliki pertanyaan atau kekhawatiran tentang proses pendaftaran, silakan hubungi tim Sumber Daya Manusia kami.

Koordinasi Program:  
 Program Fit4Success akan dikoordinasikan bersama oleh tim Sumber Daya Manusia dan Keterlibatan Karyawan kami. Mereka akan tersedia untuk memberikan panduan, dukungan, dan sumber daya sepanjang perjalanan kesejahteraan Anda.

Kami sangat percaya bahwa berinvestasi dalam kesejahteraan karyawan kami sangat penting untuk kesuksesan dan pertumbuhan organisasi kami. Kami mendorong Anda untuk memanfaatkan peluang menarik ini dan bergabung dengan kami dalam menciptakan tempat kerja yang lebih sehat, lebih bahagia, dan lebih produktif.

Mari kita rangkul program Fit4Success dan bekerja bersama menuju masa depan yang lebih sehat!

Salam hormat,  
 \[Nama Anda\]  
 \[Gelar Anda\]

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
    temperature=1,
    system="Your task is to compose a comprehensive company memo based on the provided key points. The memo should be written in a professional tone, addressing all the relevant information in a clear and concise manner. Use appropriate formatting, such as headings, subheadings, and bullet points, to organize the content effectively. Ensure that the memo is well-structured, coherent, and easy to understand for the intended audience.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "- Announcement of a new employee wellness program: \"Fit4Success\"  \n- Program objectives: promote physical and mental well-being, reduce stress, and increase productivity  \n- Components: on-site fitness classes, healthy meal options, mental health resources, and wellness workshops  \n- Partnership with local gyms and wellness centers for discounted memberships  \n- Incentives for participation: fitness trackers, wellness points, and prize drawings  \n- Program launch date: June 1, 2023  \n- Enrollment process: online registration through company intranet  \n- Program coordinators: Human Resources and Employee Engagement teams"
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
  temperature: 1,
  system: "Your task is to compose a comprehensive company memo based on the provided key points. The memo should be written in a professional tone, addressing all the relevant information in a clear and concise manner. Use appropriate formatting, such as headings, subheadings, and bullet points, to organize the content effectively. Ensure that the memo is well-structured, coherent, and easy to understand for the intended audience.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "- Announcement of a new employee wellness program: \"Fit4Success\"  \n- Program objectives: promote physical and mental well-being, reduce stress, and increase productivity  \n- Components: on-site fitness classes, healthy meal options, mental health resources, and wellness workshops  \n- Partnership with local gyms and wellness centers for discounted memberships  \n- Incentives for participation: fitness trackers, wellness points, and prize drawings  \n- Program launch date: June 1, 2023  \n- Enrollment process: online registration through company intranet  \n- Program coordinators: Human Resources and Employee Engagement teams"
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
model="anthropic.claude-opus-4-6-v1",
max_tokens=1000,
temperature=1,
system="Your task is to compose a comprehensive company memo based on the provided key points. The memo should be written in a professional tone, addressing all the relevant information in a clear and concise manner. Use appropriate formatting, such as headings, subheadings, and bullet points, to organize the content effectively. Ensure that the memo is well-structured, coherent, and easy to understand for the intended audience.",
messages=[
{
"role": "user",
"content": [
{
"type": "text",
"text": "- Announcement of a new employee wellness program: \"Fit4Success\" \n- Program objectives: promote physical and mental well-being, reduce stress, and increase productivity \n- Components: on-site fitness classes, healthy meal options, mental health resources, and wellness workshops \n- Partnership with local gyms and wellness centers for discounted memberships \n- Incentives for participation: fitness trackers, wellness points, and prize drawings \n- Program launch date: June 1, 2023 \n- Enrollment process: online registration through company intranet \n- Program coordinators: Human Resources and Employee Engagement teams"
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
  model: "anthropic.claude-opus-4-6-v1",
  max_tokens: 1000,
  temperature: 1,
  system: "Your task is to compose a comprehensive company memo based on the provided key points. The memo should be written in a professional tone, addressing all the relevant information in a clear and concise manner. Use appropriate formatting, such as headings, subheadings, and bullet points, to organize the content effectively. Ensure that the memo is well-structured, coherent, and easy to understand for the intended audience.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "- Announcement of a new employee wellness program: \"Fit4Success\"  \n- Program objectives: promote physical and mental well-being, reduce stress, and increase productivity  \n- Components: on-site fitness classes, healthy meal options, mental health resources, and wellness workshops  \n- Partnership with local gyms and wellness centers for discounted memberships  \n- Incentives for participation: fitness trackers, wellness points, and prize drawings  \n- Program launch date: June 1, 2023  \n- Enrollment process: online registration through company intranet  \n- Program coordinators: Human Resources and Employee Engagement teams"
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
    max_tokens=1000,
    temperature=1,
    system="Your task is to compose a comprehensive company memo based on the provided key points. The memo should be written in a professional tone, addressing all the relevant information in a clear and concise manner. Use appropriate formatting, such as headings, subheadings, and bullet points, to organize the content effectively. Ensure that the memo is well-structured, coherent, and easy to understand for the intended audience.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "- Announcement of a new employee wellness program: \"Fit4Success\"  \n- Program objectives: promote physical and mental well-being, reduce stress, and increase productivity  \n- Components: on-site fitness classes, healthy meal options, mental health resources, and wellness workshops  \n- Partnership with local gyms and wellness centers for discounted memberships  \n- Incentives for participation: fitness trackers, wellness points, and prize drawings  \n- Program launch date: June 1, 2023  \n- Enrollment process: online registration through company intranet  \n- Program coordinators: Human Resources and Employee Engagement teams"
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
  temperature: 1,
  system: "Your task is to compose a comprehensive company memo based on the provided key points. The memo should be written in a professional tone, addressing all the relevant information in a clear and concise manner. Use appropriate formatting, such as headings, subheadings, and bullet points, to organize the content effectively. Ensure that the memo is well-structured, coherent, and easy to understand for the intended audience.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "- Announcement of a new employee wellness program: \"Fit4Success\"  \n- Program objectives: promote physical and mental well-being, reduce stress, and increase productivity  \n- Components: on-site fitness classes, healthy meal options, mental health resources, and wellness workshops  \n- Partnership with local gyms and wellness centers for discounted memberships  \n- Incentives for participation: fitness trackers, wellness points, and prize drawings  \n- Program launch date: June 1, 2023  \n- Enrollment process: online registration through company intranet  \n- Program coordinators: Human Resources and Employee Engagement teams"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>