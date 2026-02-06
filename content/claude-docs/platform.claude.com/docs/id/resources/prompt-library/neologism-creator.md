---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/neologism-creator
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 3bae36de5dfa5af8f143aa259bf4829aa3c689ff0c84c1f4aa75238734c33550
---

# Pencipta neologisme

Ciptakan kata-kata baru dan berikan definisi mereka berdasarkan konsep atau ide yang disediakan pengguna.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|      | Konten                                                                                                                               |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Pengguna | Bisakah Anda membantu saya membuat kata baru untuk tindakan berpura-pura memahami sesuatu untuk menghindari terlihat bodoh atau tidak terinformasi? |

## Contoh keluaran

Bagaimana dengan neologisme "fauxprehension" untuk menggambarkan konsep ini?

Fauxprehension (fəʊprɪˈhɛnʃ(ə)n) - kata benda  
 Definisi: Tindakan menyamar memahami atau menangkap topik, konsep, atau situasi untuk menghindari terlihat bodoh, tidak terinformasi, atau ketinggalan informasi. Ini adalah penyamaran pengetahuan atau pemahaman tentang suatu materi, sering digunakan dalam pengaturan sosial atau profesional untuk mempertahankan citra atau status seseorang.

Etimologi: Kata "fauxprehension" adalah perpaduan dari "faux," yang berasal dari kata Prancis yang berarti palsu atau tiruan, dan "comprehension," yang berarti tindakan atau kemampuan memahami sesuatu.

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
          "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
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
          "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
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
                    "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
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
          "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
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
                    "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
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
          "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>