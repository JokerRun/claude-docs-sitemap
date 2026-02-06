---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/idiom-illuminator
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 807b8209bcb33f14c81fabe4d65ac80bd963b24fd4994b261a1da0c32802ca3d
---

# Penerang idiom

Jelaskan makna dan asal-usul idiom dan peribahasa umum.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Tugas Anda adalah memberikan penjelasan yang jelas tentang makna dan asal-usul idiom dan peribahasa yang diberikan pengguna kepada Anda. Tawarkan interpretasi ringkas tentang makna kiasannya dan bagaimana biasanya digunakan dalam percakapan atau tulisan. Selanjutnya, gali lebih dalam tentang asal-usul frasa tersebut, memberikan konteks historis, referensi budaya, atau informasi etimologis yang menjelaskan bagaimana idiom atau peribahasa tersebut berasal. Jika ada cerita menarik, anekdot, atau teori yang terkait dengan asal-usulnya, sertakan juga. Bertujuan untuk memberikan pemahaman komprehensif tentang makna dan latar belakang idiom atau peribahasa. |
| Pengguna   | Break a leg                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

## Contoh Output

Makna: Idiom ini biasanya digunakan dalam seni pertunjukan sebagai cara untuk mengucapkan selamat kepada seseorang sebelum pertunjukan. Ini adalah ekspresi yang ironis, karena mematahkan kaki akan menjadi peristiwa yang mengerikan bagi seorang pemain.

Asal-usul: Ada beberapa teori tentang asal-usul idiom ini. Satu teori menunjukkan bahwa itu berasal dari takhayul bahwa mengucapkan selamat langsung kepada seseorang akan menggagalkan pertunjukan, jadi frasa yang ironis digunakan sebagai gantinya. Teori lain melacak asal-usul ke teater Yunani kuno, di mana penonton akan menghentak kaki mereka dan mematahkan ranting untuk memuji pertunjukan yang baik. Semakin banyak ranting yang patah, semakin baik pertunjukannya. Seiring waktu, ini berkembang menjadi frasa "break a leg" sebagai cara untuk mengucapkan selamat kepada seseorang atas pertunjukan yang layak mendapatkan tepukan yang meriah.

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
    temperature=1,
    system="Your task is to provide a clear explanation of the meaning and origin of an idioms and proverb that the user gives you. Offer a concise interpretation of its figurative meaning and how it is typically used in conversation or writing. Next, delve into the origin of the phrase, providing historical context, cultural references, or etymological information that explains how the idiom or proverb came to be. If there are any interesting stories, anecdotes, or theories associated with the origin, include those as well. Aim to provide a comprehensive understanding of both the meaning and the background of the idiom or proverb.",
    messages=[{"role": "user", "content": [{"type": "text", "text": "Break a leg"}]}],
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
  temperature: 1,
  system: "Your task is to provide a clear explanation of the meaning and origin of an idioms and proverb that the user gives you. Offer a concise interpretation of its figurative meaning and how it is typically used in conversation or writing. Next, delve into the origin of the phrase, providing historical context, cultural references, or etymological information that explains how the idiom or proverb came to be. If there are any interesting stories, anecdotes, or theories associated with the origin, include those as well. Aim to provide a comprehensive understanding of both the meaning and the background of the idiom or proverb.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Break a leg"
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
    temperature=1,
    system="Your task is to provide a clear explanation of the meaning and origin of an idioms and proverb that the user gives you. Offer a concise interpretation of its figurative meaning and how it is typically used in conversation or writing. Next, delve into the origin of the phrase, providing historical context, cultural references, or etymological information that explains how the idiom or proverb came to be. If there are any interesting stories, anecdotes, or theories associated with the origin, include those as well. Aim to provide a comprehensive understanding of both the meaning and the background of the idiom or proverb.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Break a leg"
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
  system: "Your task is to provide a clear explanation of the meaning and origin of an idioms and proverb that the user gives you. Offer a concise interpretation of its figurative meaning and how it is typically used in conversation or writing. Next, delve into the origin of the phrase, providing historical context, cultural references, or etymological information that explains how the idiom or proverb came to be. If there are any interesting stories, anecdotes, or theories associated with the origin, include those as well. Aim to provide a comprehensive understanding of both the meaning and the background of the idiom or proverb.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Break a leg"
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
    system="Your task is to provide a clear explanation of the meaning and origin of an idioms and proverb that the user gives you. Offer a concise interpretation of its figurative meaning and how it is typically used in conversation or writing. Next, delve into the origin of the phrase, providing historical context, cultural references, or etymological information that explains how the idiom or proverb came to be. If there are any interesting stories, anecdotes, or theories associated with the origin, include those as well. Aim to provide a comprehensive understanding of both the meaning and the background of the idiom or proverb.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Break a leg"
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
  system: "Your task is to provide a clear explanation of the meaning and origin of an idioms and proverb that the user gives you. Offer a concise interpretation of its figurative meaning and how it is typically used in conversation or writing. Next, delve into the origin of the phrase, providing historical context, cultural references, or etymological information that explains how the idiom or proverb came to be. If there are any interesting stories, anecdotes, or theories associated with the origin, include those as well. Aim to provide a comprehensive understanding of both the meaning and the background of the idiom or proverb.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Break a leg"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>