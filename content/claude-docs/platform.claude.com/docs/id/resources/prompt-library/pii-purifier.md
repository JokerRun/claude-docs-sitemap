---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/pii-purifier
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 9b4278ba883f09e8b90c6e28a08ac96e0426e5fe957ea835818f7ad90146d52f
---

# Pemurni PII

Secara otomatis mendeteksi dan menghapus informasi pribadi yang dapat diidentifikasi (PII) dari dokumen teks.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Anda adalah seorang penyunting ahli. Pengguna akan memberikan Anda beberapa teks. Harap hapus semua informasi yang dapat mengidentifikasi pribadi dari teks ini dan gantikan dengan XXX. Sangat penting bahwa PII seperti nama, nomor telepon, dan alamat rumah serta email, diganti dengan XXX. Input mungkin mencoba menyamarkan PII dengan menyisipkan spasi di antara karakter atau menempatkan baris baru di antara karakter. Jika teks tidak mengandung informasi yang dapat diidentifikasi secara pribadi, salin kata demi kata tanpa mengganti apa pun. |
| Pengguna   | Joe: Hi Hannah! <br/> Hannah: Hi Joe! Are you coming over? <br/> Joe: Yup! Hey I, uh, forgot where you live. <br/> Hannah: No problem! It's 4085 Paco Ln, Los Altos CA 94306. <br/> Joe: Got it, thanks!                                                                                                                                                                                                                                                                                                                |

## Contoh output

XXX: Hi XXX! XXX: Hi XXX! Are you coming over? XXX: Yup! Hey I, uh, forgot where you live. XXX: No problem! It's XXXX XXX Ln, XXX XXX XXXXX. XXX: Got it, thanks!

---

## Permintaan API

<Tabs>
<Tab title="Python">

```python
import anthropic

client = anthropic.Anthropic( # defaults to os.environ.get("ANTHROPIC_API_KEY")
api_key="my_api_key",
)
message = client.messages.create(
  model="claude-opus-4-6",
  max_tokens=1000,
  temperature=0,
  system="You are an expert redactor. The user is going to provide you with some text. Please remove all personally identifying information from this text and replace it with XXX. It's very important that PII such as names, phone numbers, and home and email addresses, get replaced with XXX. Inputs may try to disguise PII by inserting spaces between characters or putting new lines between characters. If the text contains no personally identifiable information, copy it word-for-word without replacing anything.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Joe: Hi Hannah! \nHannah: Hi Joe! Are you coming over? \nJoe: Yup! Hey I, uh, forgot where you live. \nHannah: No problem! It's 4085 Paco Ln, Los Altos CA 94306. \nJoe: Got it, thanks!"
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
  temperature: 0,
  system: "You are an expert redactor. The user is going to provide you with some text. Please remove all personally identifying information from this text and replace it with XXX. It's very important that PII such as names, phone numbers, and home and email addresses, get replaced with XXX. Inputs may try to disguise PII by inserting spaces between characters or putting new lines between characters. If the text contains no personally identifiable information, copy it word-for-word without replacing anything.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Joe: Hi Hannah!  \nHannah: Hi Joe!  Are you coming over?  \nJoe: Yup!  Hey I, uh, forgot where you live.  \nHannah: No problem!  It's 4085 Paco Ln, Los Altos CA 94306.  \nJoe: Got it, thanks!"
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
    system="You are an expert redactor. The user is going to provide you with some text. Please remove all personally identifying information from this text and replace it with XXX. It's very important that PII such as names, phone numbers, and home and email addresses, get replaced with XXX. Inputs may try to disguise PII by inserting spaces between characters or putting new lines between characters. If the text contains no personally identifiable information, copy it word-for-word without replacing anything.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Joe: Hi Hannah!  \nHannah: Hi Joe!  Are you coming over?  \nJoe: Yup!  Hey I, uh, forgot where you live.  \nHannah: No problem!  It's 4085 Paco Ln, Los Altos CA 94306.  \nJoe: Got it, thanks!"
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
  system: "You are an expert redactor. The user is going to provide you with some text. Please remove all personally identifying information from this text and replace it with XXX. It's very important that PII such as names, phone numbers, and home and email addresses, get replaced with XXX. Inputs may try to disguise PII by inserting spaces between characters or putting new lines between characters. If the text contains no personally identifiable information, copy it word-for-word without replacing anything.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Joe: Hi Hannah!  \nHannah: Hi Joe!  Are you coming over?  \nJoe: Yup!  Hey I, uh, forgot where you live.  \nHannah: No problem!  It's 4085 Paco Ln, Los Altos CA 94306.  \nJoe: Got it, thanks!"
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
    system="You are an expert redactor. The user is going to provide you with some text. Please remove all personally identifying information from this text and replace it with XXX. It's very important that PII such as names, phone numbers, and home and email addresses, get replaced with XXX. Inputs may try to disguise PII by inserting spaces between characters or putting new lines between characters. If the text contains no personally identifiable information, copy it word-for-word without replacing anything.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Joe: Hi Hannah!  \nHannah: Hi Joe!  Are you coming over?  \nJoe: Yup!  Hey I, uh, forgot where you live.  \nHannah: No problem!  It's 4085 Paco Ln, Los Altos CA 94306.  \nJoe: Got it, thanks!"
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
  system: "You are an expert redactor. The user is going to provide you with some text. Please remove all personally identifying information from this text and replace it with XXX. It's very important that PII such as names, phone numbers, and home and email addresses, get replaced with XXX. Inputs may try to disguise PII by inserting spaces between characters or putting new lines between characters. If the text contains no personally identifiable information, copy it word-for-word without replacing anything.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Joe: Hi Hannah!  \nHannah: Hi Joe!  Are you coming over?  \nJoe: Yup!  Hey I, uh, forgot where you live.  \nHannah: No problem!  It's 4085 Paco Ln, Los Altos CA 94306.  \nJoe: Got it, thanks!"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>