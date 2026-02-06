---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/vr-fitness-innovator
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 2cf3df109b0fd59b965ac9b10e8a0dd153b88c86dc8af562e4ae4eee503fb0e5
---

# Inovator kebugaran VR

Brainstorm ide-ide kreatif untuk permainan kebugaran realitas virtual.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

| Peran | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pengguna | Tugas Anda adalah menghasilkan daftar ide-ide inovatif dan menarik untuk permainan kebugaran realitas virtual (VR). Pertimbangkan berbagai genre permainan, mekanik gameplay unik, lingkungan yang imersif, dan cara-cara kreatif untuk menggabungkan latihan fisik dan gerakan. Ide-ide harus menarik bagi berbagai penggemar kebugaran dan gamer, mendorong mereka untuk tetap aktif dan bersenang-senang sambil berolahraga di VR. Untuk setiap ide, berikan deskripsi singkat tentang konsep permainan, fitur utama, dan bagaimana hal itu mempromosikan kebugaran. |

## Contoh Output

1.  Ide: VR Parkour Adventure  
    Deskripsi: Pemain menavigasi melalui lingkungan perkotaan yang dinamis, berlari, melompat, memanjat, dan melakukan akrobat parkour untuk mengatasi rintangan dan mencapai tujuan. Permainan beradaptasi dengan gerakan pemain, memberikan latihan tubuh penuh yang intens sambil menjelajahi kota virtual.  
    Fitur utama: Mekanik parkour yang realistis, lingkungan yang dihasilkan secara prosedural, balapan multipemain, dan tantangan.  
    Aspek kebugaran: Kardio, kelincahan, koordinasi, dan kekuatan tubuh bagian bawah.
2.  Ide: Rhythm Boxing  
    Deskripsi: Permainan tinju berenergi tinggi yang disetel dengan irama lagu musik populer. Pemain harus memukul, menghindari, dan memblokir sesuai dengan ritme untuk mendapatkan poin dan maju melalui level yang semakin menantang. Permainan menawarkan berbagai gaya tinju dan mode pelatihan.  
    Fitur utama: Musik berlisensi, petinju yang dapat disesuaikan, multipemain online, dan berbagai teknik tinju.  
    Aspek kebugaran: Kardio, kekuatan tubuh bagian atas, refleks, dan daya tahan.
3.  Idea: VR Fitness RPG  
    Deskripsi: Permainan bermain peran yang imersif di mana pemain membuat karakter mereka sendiri dan memulai misi untuk menyelamatkan dunia fantasi. Permainan menggabungkan elemen RPG tradisional dengan tantangan kebugaran, memerlukan pemain untuk melakukan latihan fisik untuk melempar mantra, mengalahkan musuh, dan meningkatkan level karakter mereka.  
    Fitur utama: Kustomisasi karakter, pohon keterampilan, pertempuran bos yang epik, dan campuran latihan kekuatan, kardio, dan fleksibilitas.  
    Aspek kebugaran: Latihan tubuh penuh, pelatihan kekuatan, kardio, dan fleksibilitas.

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
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Your task is to generate a list of innovative and engaging ideas for virtual reality (VR) fitness games. Consider various game genres, unique gameplay mechanics, immersive environments, and creative ways to incorporate physical exercises and movements. The ideas should be appealing to a wide range of fitness enthusiasts and gamers, encouraging them to stay active and have fun while exercising in VR. For each idea, provide a brief description of the game concept, key features, and how it promotes fitness."
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
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Your task is to generate a list of innovative and engaging ideas for virtual reality (VR) fitness games. Consider various game genres, unique gameplay mechanics, immersive environments, and creative ways to incorporate physical exercises and movements. The ideas should be appealing to a wide range of fitness enthusiasts and gamers, encouraging them to stay active and have fun while exercising in VR. For each idea, provide a brief description of the game concept, key features, and how it promotes fitness."
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
    temperature=1,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Your task is to generate a list of innovative and engaging ideas for virtual reality (VR) fitness games. Consider various game genres, unique gameplay mechanics, immersive environments, and creative ways to incorporate physical exercises and movements. The ideas should be appealing to a wide range of fitness enthusiasts and gamers, encouraging them to stay active and have fun while exercising in VR. For each idea, provide a brief description of the game concept, key features, and how it promotes fitness."
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
  temperature: 1,
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Your task is to generate a list of innovative and engaging ideas for virtual reality (VR) fitness games. Consider various game genres, unique gameplay mechanics, immersive environments, and creative ways to incorporate physical exercises and movements. The ideas should be appealing to a wide range of fitness enthusiasts and gamers, encouraging them to stay active and have fun while exercising in VR. For each idea, provide a brief description of the game concept, key features, and how it promotes fitness."
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
    temperature=1,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Your task is to generate a list of innovative and engaging ideas for virtual reality (VR) fitness games. Consider various game genres, unique gameplay mechanics, immersive environments, and creative ways to incorporate physical exercises and movements. The ideas should be appealing to a wide range of fitness enthusiasts and gamers, encouraging them to stay active and have fun while exercising in VR. For each idea, provide a brief description of the game concept, key features, and how it promotes fitness."
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
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Your task is to generate a list of innovative and engaging ideas for virtual reality (VR) fitness games. Consider various game genres, unique gameplay mechanics, immersive environments, and creative ways to incorporate physical exercises and movements. The ideas should be appealing to a wide range of fitness enthusiasts and gamers, encouraging them to stay active and have fun while exercising in VR. For each idea, provide a brief description of the game concept, key features, and how it promotes fitness."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>