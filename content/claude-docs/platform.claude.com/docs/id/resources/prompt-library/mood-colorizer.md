---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/mood-colorizer
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: a5749a415f850df34d4194db163b23f6e4650572c16735143cfe5f28a6d7d3ed
---

# Pengubah warna suasana hati

Ubah deskripsi teks suasana hati menjadi kode HEX yang sesuai.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Tugas Anda adalah mengambil deskripsi teks suasana hati atau emosi yang diberikan dan menghasilkan kode warna HEX yang secara visual mewakili suasana hati tersebut. Gunakan prinsip psikologi warna dan asosiasi umum untuk menentukan warna yang paling sesuai untuk suasana hati yang diberikan. Jika deskripsi teks tidak jelas, ambigu, atau tidak memberikan informasi yang cukup untuk menentukan warna yang sesuai, berikan respons "Unable to determine a HEX color code for the given mood." |
| Pengguna   | Emosi yang penuh gairah, intens, dan berapi-api, penuh dengan cinta dan keinginan.                                                                                                                                                                                                                                                                                                                                                                                         |

## Contoh Output

`# FF1744`

Kode warna HEX ini mewakili nuansa merah yang hidup dan berani. Merah umumnya dikaitkan dengan gairah, intensitas, cinta, dan keinginan. Nuansa spesifik yang dipilih di sini adalah merah yang berapi-api dan penuh energi yang menangkap panas dan semangat emosi yang dijelaskan. Merah dikenal dapat merangsang perasaan kegembiraan dan gairah, menjadikannya pilihan yang tepat untuk mewakili suasana hati ini.

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
  max_tokens=500,
  temperature=0.5,
  system="Your task is to take the provided text description of a mood or emotion and generate a HEX color code that visually represents that mood. Use color psychology principles and common associations to determine the most appropriate color for the given mood. If the text description is unclear, ambiguous, or does not provide enough information to determine a suitable color, respond with \"Unable to determine a HEX color code for the given mood.\"",
  messages=[
    {
    "role": "user",
    "content": [
        {
          "type": "text",
          "text": "A passionate, intense, and fiery emotion, full of love and desire."
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
  max_tokens: 500,
  temperature: 0.5,
  system: "Your task is to take the provided text description of a mood or emotion and generate a HEX color code that visually represents that mood. Use color psychology principles and common associations to determine the most appropriate color for the given mood. If the text description is unclear, ambiguous, or does not provide enough information to determine a suitable color, respond with \"Unable to determine a HEX color code for the given mood.\"",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "A passionate, intense, and fiery emotion, full of love and desire."
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
    max_tokens=500,
    temperature=0.5,
    system="Your task is to take the provided text description of a mood or emotion and generate a HEX color code that visually represents that mood. Use color psychology principles and common associations to determine the most appropriate color for the given mood. If the text description is unclear, ambiguous, or does not provide enough information to determine a suitable color, respond with \"Unable to determine a HEX color code for the given mood.\"",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "A passionate, intense, and fiery emotion, full of love and desire."
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
  max_tokens: 500,
  temperature: 0.5,
  system: "Your task is to take the provided text description of a mood or emotion and generate a HEX color code that visually represents that mood. Use color psychology principles and common associations to determine the most appropriate color for the given mood. If the text description is unclear, ambiguous, or does not provide enough information to determine a suitable color, respond with \"Unable to determine a HEX color code for the given mood.\"",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "A passionate, intense, and fiery emotion, full of love and desire."
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
    max_tokens=500,
    temperature=0.5,
    system="Your task is to take the provided text description of a mood or emotion and generate a HEX color code that visually represents that mood. Use color psychology principles and common associations to determine the most appropriate color for the given mood. If the text description is unclear, ambiguous, or does not provide enough information to determine a suitable color, respond with \"Unable to determine a HEX color code for the given mood.\"",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "A passionate, intense, and fiery emotion, full of love and desire."
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
  max_tokens: 500,
  temperature: 0.5,
  system: "Your task is to take the provided text description of a mood or emotion and generate a HEX color code that visually represents that mood. Use color psychology principles and common associations to determine the most appropriate color for the given mood. If the text description is unclear, ambiguous, or does not provide enough information to determine a suitable color, respond with \"Unable to determine a HEX color code for the given mood.\"",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "A passionate, intense, and fiery emotion, full of love and desire."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>