---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/culinary-creator
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 418aa09d2bda02cdfd0d265ebb281cf3dea3847d2c0582e15e0190cab598c91b
---

# Pencipta kuliner

Sarankan ide resep berdasarkan bahan-bahan yang tersedia dan preferensi diet pengguna.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Tugas Anda adalah menghasilkan ide resep yang dipersonalisasi berdasarkan input pengguna tentang bahan-bahan yang tersedia dan preferensi diet. Gunakan informasi ini untuk menyarankan berbagai resep kreatif dan lezat yang dapat dibuat menggunakan bahan-bahan yang diberikan sambil memenuhi kebutuhan diet pengguna, jika ada yang disebutkan. Untuk setiap resep, berikan deskripsi singkat, daftar bahan-bahan yang diperlukan, dan serangkaian instruksi sederhana. Pastikan resep mudah diikuti, bergizi, dan dapat disiapkan dengan bahan-bahan atau peralatan tambahan minimal. |
| Pengguna   | Bahan-bahan yang tersedia: dada ayam, brokoli, wortel, bawang, bawang putih, minyak zaitun, nasi, kecap asin bebas gluten, madu <br/> Preferensi diet: bebas gluten                                                                                                                                                                                                                                                                                                                                                                                                             |

## Contoh Output

Resep yang disarankan:

Stir-Fry Ayam Madu Bawang Putih

Deskripsi: Stir-fry yang cepat dan lezat menampilkan dada ayam yang empuk, sayuran renyah, dan saus madu bawang putih yang manis dan gurih.  
 Bahan-bahan:

- 2 dada ayam, dipotong menjadi potongan kecil
- 2 cangkir kuntum brokoli
- 1 cangkir wortel iris
- 1 bawang, dicincang
- 3 siung bawang putih, dihaluskan
- 2 sdm minyak zaitun
- 1/4 cangkir kecap asin (bebas gluten)
- 2 sdm madu

Instruksi:

1.  Dalam wajan besar atau wok, panaskan minyak zaitun dengan api sedang-tinggi.
2.  Tambahkan bawang cincang dan bawang putih yang dihaluskan, dan tumis hingga harum, sekitar 2 menit.
3.  Tambahkan potongan ayam dan masak hingga tidak lagi berwarna merah muda, sekitar 5-7 menit.
4.  Tambahkan brokoli dan wortel, dan stir-fry hingga sayuran empuk-renyah, sekitar 5 menit.
5.  Dalam mangkuk kecil, kocok bersama kecap asin dan madu.
6.  Tuangkan saus di atas ayam dan sayuran, dan aduk hingga merata.
7.  Masak selama 2-3 menit tambahan, atau hingga saus mengental sedikit.
8.  Sajikan panas dengan nasi kukus.

Mangkuk Nasi Ayam dan Sayuran

Deskripsi: Mangkuk nasi yang gurih dan bergizi dengan topping ayam berbumbu, sayuran panggang, dan percikan kecap asin.

Bahan-bahan:

- 2 dada ayam, dipotong menjadi potongan kecil
- 2 cangkir kuntum brokoli
- 1 cangkir wortel iris
- 1 bawang, dicincang
- 2 siung bawang putih, dihaluskan
- 2 sdm minyak zaitun
- 1/4 cangkir kecap asin (bebas gluten)
- 2 cangkir nasi matang

Instruksi:

1.  Panaskan oven hingga 400°F (200°C).
2.  Dalam mangkuk besar, gabungkan potongan ayam, brokoli, wortel, bawang, dan bawang putih.
3.  Siramkan dengan minyak zaitun dan setengah dari kecap asin, dan aduk hingga merata.
4.  Sebarkan ayam dan sayuran di atas loyang dan panggang dalam oven yang sudah dipanaskan selama 20-25 menit, atau hingga ayam matang dan sayuran empuk.
5.  Bagi nasi matang di antara mangkuk penyajian.
6.  Topping setiap mangkuk dengan ayam dan sayuran panggang.
7.  Siramkan sisa kecap asin di atas setiap mangkuk.
8.  Sajikan panas dan nikmati!

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
  system="Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
  messages=[
    {
    "role": "user",
    "content": [
        {
          "type": "text",
          "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey \nDietary preferences: gluten free"
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
  system: "Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey  \nDietary preferences: gluten free"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
<Tab title="AWS Bedrock Python">

```
from anthropic import AnthropicBedrock

# See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
# for authentication options
client = AnthropicBedrock()

message = client.messages.create(
    model="anthropic.claude-opus-4-6-v1:0",
    max_tokens=2000,
    temperature=0.5,
    system="Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey  \nDietary preferences: gluten free"
                }
            ]
        }
    ]
)
print(message.content)

```

</Tab>
<Tab title="AWS Bedrock TypeScript">

```
import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

// See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
// for authentication options
const client = new AnthropicBedrock();

const msg = await client.messages.create({
  model: "anthropic.claude-opus-4-6-v1:0",
  max_tokens: 2000,
  temperature: 0.5,
  system: "Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey  \nDietary preferences: gluten free"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
<Tab title="Vertex AI Python">

```
from anthropic import AnthropicVertex

client = AnthropicVertex()

message = client.messages.create(
    model="claude-sonnet-4@20250514",
    max_tokens=2000,
    temperature=0.5,
    system="Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey  \nDietary preferences: gluten free"
                }
            ]
        }
    ]
)
print(message.content)

```

</Tab>
<Tab title="Vertex AI TypeScript">

```
import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';

// Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
// Additionally goes through the standard `google-auth-library` flow.
const client = new AnthropicVertex();

const msg = await client.messages.create({
  model: "claude-sonnet-4@20250514",
  max_tokens: 2000,
  temperature: 0.5,
  system: "Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey  \nDietary preferences: gluten free"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>