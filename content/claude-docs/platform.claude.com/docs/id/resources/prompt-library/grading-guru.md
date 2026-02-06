---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/grading-guru
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 03818998d71684b298c95e98eebfa754f2c1885abe00640ac03b1388c164f756
---

# Guru penilaian

Bandingkan dan evaluasi kualitas teks tertulis berdasarkan kriteria dan standar yang ditentukan pengguna.

---

> Salin prompt ini ke [Konsol](/dashboard) pengembang kami untuk mencobanya sendiri!

| Peran | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pengguna | Evaluasi kedua teks berikut berdasarkan kriteria yang diberikan: <br/> <br/> Teks 1: <br/> Matahari terbenam di balik gunung-gunung, memancarkan cahaya emas yang hangat di seluruh lembah. Burung-burung berkicau lagu malam mereka saat angin lembut berdesir melalui daun-daun. Ini adalah momen yang damai dan tenang, satu yang memenuhi hati dengan kegembiraan dan kepuasan. <br/><br/> Teks 2: <br/> Matahari terbenam itu cantik. Burung-burung bernyanyi dan angin bertiup. Itu membuat saya bahagia. <br/><br/> Kriteria: <br/> 1. Bahasa deskriptif dan citra <br/> 2. Struktur kalimat dan variasi <br/> 3. Dampak emosional dan keterlibatan <br/> 4. Tata bahasa dan tanda baca |

## Contoh Output

Berdasarkan kriteria yang disediakan, berikut adalah evaluasi saya terhadap kedua teks:

Teks 1:

1.  Bahasa deskriptif dan citra: Teks menggunakan bahasa yang hidup dan evokasi untuk melukis gambaran pengaturan. Frasa seperti "cahaya emas yang hangat," "burung-burung berkicau lagu malam mereka," dan "angin lembut berdesir melalui daun-daun" menciptakan citra visual dan auditori yang kuat, membenamkan pembaca dalam adegan.
2.  Struktur kalimat dan variasi: Teks menunjukkan campuran yang baik dari struktur kalimat, dengan kalimat sederhana dan majemuk. Variasi ini membantu mempertahankan aliran yang mulus dan membuat pembaca tetap terlibat.
3.  Dampak emosional dan keterlibatan: Teks secara efektif menyampaikan rasa kedamaian, kegembiraan, dan kepuasan, mengundang pembaca untuk berbagi dalam pengalaman emosional momen tersebut. Deskripsi pengaturan dan penggunaan bahasa positif menciptakan koneksi emosional yang kuat.
4.  Tata bahasa dan tanda baca: Teks tampaknya secara tata bahasa benar dan tanda baca dengan baik, tanpa kesalahan atau masalah yang jelas.

Teks 2:

1.  Bahasa deskriptif dan citra: Teks kekurangan bahasa deskriptif terperinci dan citra. Meskipun menyebutkan matahari terbenam, burung, dan angin, teks tidak memberikan detail yang hidup atau evokasi untuk membantu pembaca memvisualisasikan adegan.
2.  Struktur kalimat dan variasi: Teks terdiri dari kalimat pendek dan sederhana dengan sedikit variasi dalam struktur. Kurangnya variasi ini dapat membuat tulisan terasa monoton dan kurang menarik.
3.  Dampak emosional dan keterlibatan: Teks menyampaikan emosi positif dengan menyatakan "Itu membuat saya bahagia," tetapi tidak memberikan koneksi emosional yang kuat atau keterlibatan karena kurangnya bahasa deskriptif dan citra.
4.  Tata bahasa dan tanda baca: Teks tampaknya secara tata bahasa benar dan tanda baca dengan baik, tanpa kesalahan atau masalah yang jelas.

Analisis Perbandingan:  
 Berdasarkan evaluasi, Teks 1 berkinerja secara signifikan lebih baik daripada Teks 2 dalam hal bahasa deskriptif, citra, struktur kalimat, variasi, dan dampak emosional. Teks 1 menciptakan pengalaman yang hidup dan mendalam bagi pembaca dan menunjukkan kualitas tulisan yang lebih tinggi berdasarkan kriteria yang diberikan, dengan bahasa deskriptif yang kuat, struktur kalimat yang bervariasi, dan keterlibatan emosional yang efektif. Teks 2, meskipun secara tata bahasa benar, kekurangan kekayaan deskriptif dan dampak emosional yang ada di Teks 1.

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
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Evaluate the following two texts based on the given criteria: \n \nText 1: \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment. \n \nText 2: \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy. \n \nCriteria: \n1. Descriptive language and imagery \n2. Sentence structure and variety \n3. Emotional impact and engagement \n4. Grammar and punctuation",
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
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Evaluate the following two texts based on the given criteria:  \n  \nText 1:  \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment.  \n  \nText 2:  \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy.  \n  \nCriteria:  \n1. Descriptive language and imagery  \n2. Sentence structure and variety  \n3. Emotional impact and engagement  \n4. Grammar and punctuation"
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
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Evaluate the following two texts based on the given criteria:  \n  \nText 1:  \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment.  \n  \nText 2:  \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy.  \n  \nCriteria:  \n1. Descriptive language and imagery  \n2. Sentence structure and variety  \n3. Emotional impact and engagement  \n4. Grammar and punctuation"
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
  temperature: 0,
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Evaluate the following two texts based on the given criteria:  \n  \nText 1:  \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment.  \n  \nText 2:  \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy.  \n  \nCriteria:  \n1. Descriptive language and imagery  \n2. Sentence structure and variety  \n3. Emotional impact and engagement  \n4. Grammar and punctuation"
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
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Evaluate the following two texts based on the given criteria:  \n  \nText 1:  \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment.  \n  \nText 2:  \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy.  \n  \nCriteria:  \n1. Descriptive language and imagery  \n2. Sentence structure and variety  \n3. Emotional impact and engagement  \n4. Grammar and punctuation"
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
  temperature: 0,
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Evaluate the following two texts based on the given criteria:  \n  \nText 1:  \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment.  \n  \nText 2:  \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy.  \n  \nCriteria:  \n1. Descriptive language and imagery  \n2. Sentence structure and variety  \n3. Emotional impact and engagement  \n4. Grammar and punctuation"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>