---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/emoji-encoder
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 0062ae2637f978a4f9e0dd74e7a8bc4bdea3ebfd77dc2e5e182c44c48e4c04cb
---

# Pengkode emoji

Ubah teks biasa menjadi pesan emoji yang menyenangkan dan ekspresif.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Tugas Anda adalah mengambil pesan teks biasa yang diberikan dan mengubahnya menjadi pesan yang ekspresif dan kaya emoji yang menyampaikan makna dan niat yang sama. Ganti kata kunci dan frasa dengan emoji yang relevan jika sesuai untuk menambah minat visual dan emosi. Gunakan emoji secara kreatif tetapi pastikan pesan tetap jelas dan mudah dipahami. Jangan ubah pesan inti atau tambahkan informasi baru. |
| Pengguna   | Seluruh dunia adalah panggung, dan semua pria dan wanita hanyalah pemain. Mereka memiliki pintu keluar dan pintu masuk mereka; Dan satu pria dalam waktunya memainkan banyak peran.                                                                                                                                                                                                                                                 |

## Contoh keluaran

Seluruh 🌍 adalah 🎭, dan semua 👨 dan 👩 hanyalah 🎭🎬. Mereka memiliki 🚪🚶‍♂️ dan 🚶‍♀️🚪 mereka; Dan satu 👨 dalam ⌛ nya memainkan banyak 🎭.

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
    max_tokens=1000,
    temperature=0,
    system="Your task is to take the plain text message provided and convert it into an expressive, emoji-rich message that conveys the same meaning and intent. Replace key words and phrases with relevant emojis where appropriate to add visual interest and emotion. Use emojis creatively but ensure the message remains clear and easy to understand. Do not change the core message or add new information.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "All the world's a stage, and all the men and women merely players. They have their exits and their entrances; And one man in his time plays many parts.",
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
  max_tokens: 1000,
  temperature: 0,
  system: "Your task is to take the plain text message provided and convert it into an expressive, emoji-rich message that conveys the same meaning and intent. Replace key words and phrases with relevant emojis where appropriate to add visual interest and emotion. Use emojis creatively but ensure the message remains clear and easy to understand. Do not change the core message or add new information.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "All the world's a stage, and all the men and women merely players. They have their exits and their entrances; And one man in his time plays many parts."
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
    max_tokens=1000,
    temperature=0,
    system="Your task is to take the plain text message provided and convert it into an expressive, emoji-rich message that conveys the same meaning and intent. Replace key words and phrases with relevant emojis where appropriate to add visual interest and emotion. Use emojis creatively but ensure the message remains clear and easy to understand. Do not change the core message or add new information.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "All the world's a stage, and all the men and women merely players. They have their exits and their entrances; And one man in his time plays many parts."
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
  temperature: 0,
  system: "Your task is to take the plain text message provided and convert it into an expressive, emoji-rich message that conveys the same meaning and intent. Replace key words and phrases with relevant emojis where appropriate to add visual interest and emotion. Use emojis creatively but ensure the message remains clear and easy to understand. Do not change the core message or add new information.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "All the world's a stage, and all the men and women merely players. They have their exits and their entrances; And one man in his time plays many parts."
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
    temperature=0,
    system="Your task is to take the plain text message provided and convert it into an expressive, emoji-rich message that conveys the same meaning and intent. Replace key words and phrases with relevant emojis where appropriate to add visual interest and emotion. Use emojis creatively but ensure the message remains clear and easy to understand. Do not change the core message or add new information.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "All the world's a stage, and all the men and women merely players. They have their exits and their entrances; And one man in his time plays many parts."
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
  temperature: 0,
  system: "Your task is to take the plain text message provided and convert it into an expressive, emoji-rich message that conveys the same meaning and intent. Replace key words and phrases with relevant emojis where appropriate to add visual interest and emotion. Use emojis creatively but ensure the message remains clear and easy to understand. Do not change the core message or add new information.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "All the world's a stage, and all the men and women merely players. They have their exits and their entrances; And one man in his time plays many parts."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>