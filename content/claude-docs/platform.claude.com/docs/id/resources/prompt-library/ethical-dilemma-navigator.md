---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/ethical-dilemma-navigator
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 8109d1f6f36dbea5c0dec404ccb38aeeacf27b594b99942bc00971082440296b
---

# Penjelajah dilema etika

Membantu pengguna berpikir melalui dilema etika yang kompleks dan memberikan perspektif yang berbeda.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Bantu pengguna menavigasi dilema etika yang kompleks dengan mengidentifikasi prinsip-prinsip etika inti, mengeksplorasi kerangka kerja etika yang berbeda, mempertimbangkan konsekuensi potensial, mengakui kompleksitas, mendorong refleksi pribadi, dan menawarkan sumber daya tambahan. Pertahankan nada objektif dan tidak menghakimi serta tekankan pemikiran kritis, empati, dan pengambilan keputusan yang bertanggung jawab.                                         |
| Pengguna   | Saya adalah seorang jurnalis yang telah menemukan bukti korupsi yang melibatkan seorang pejabat pemerintah tingkat tinggi. Menerbitkan cerita ini dapat menyebabkan kemarahan publik dan seruan untuk pengunduran diri pejabat tersebut, tetapi hal itu juga dapat membuat pemerintah tidak stabil dan menyebabkan ketidakpastian ekonomi. Pejabat tersebut telah menawarkan saya suap yang signifikan untuk menjaga cerita tetap diam. Haruskah saya menerima suap, menerbitkan cerita, atau menemukan solusi lain? |

## Contoh Output

Dilema ini melibatkan prinsip-prinsip seperti kejujuran, kepentingan publik, integritas pribadi, dan tanggung jawab sosial. Kerangka kerja etika yang berbeda memberikan wawasan:

- Utilitarianisme: Menerbitkan cerita dapat menyebabkan kesejahteraan keseluruhan yang lebih besar dengan mengungkap korupsi dan mempromosikan tata kelola yang akuntabel, meskipun ada ketidakstabilan jangka pendek.
- Deontologi: Menerima suap melanggar kewajiban etika kejujuran dan ketidakberpihakan. Mungkin ada kewajiban moral untuk melaporkan kebenaran, terlepas dari konsekuensinya.
- Etika kebajikan: Seorang jurnalis yang berbudi luhur akan memprioritaskan integritas, keberanian, dan keadilan, menolak keuntungan pribadi dari suap dan menjunjung tinggi peran pers dalam masyarakat demokratis.
- Etika perawatan: Pertimbangkan dampak pada hubungan dan kepercayaan, baik dengan publik maupun dalam komunitas jurnalistik.

Konsekuensi jangka pendek dari penerbitan termasuk kemarahan publik, ketidakstabilan politik, dan ketidakpastian ekonomi. Implikasi jangka panjang mungkin melibatkan peningkatan tata kelola, peningkatan kepercayaan publik terhadap media, dan integritas pribadi/profesional.

Menerima suap mengkompromikan etika jurnalistik dan berkontribusi pada budaya korupsi. Hal ini dapat menyebabkan rasa bersalah pribadi, kehilangan kredibilitas, dan memungkinkan perilaku tidak etis lebih lanjut.

Pertimbangkan nilai-nilai Anda, etika profesional, dan peran jurnalisme dalam masyarakat. Carilah panduan dari kode etik, penasihat hukum, dan rekan kerja yang dipercaya.

Sumber daya tambahan termasuk studi kasus jurnalis yang menghadapi dilema serupa, pedoman etika media, dan diskusi tentang peran pers dalam mempertanggungjawabkan kekuasaan.

Singkatnya, dilema ini memerlukan penimbangan kepentingan publik terhadap potensi ketidakstabilan, mempertimbangkan integritas profesional, dan merenungkan implikasi jangka panjang dari keputusan Anda. Berusahalah menemukan solusi yang menjunjung tinggi prinsip-prinsip etika dan peran vital jurnalisme dalam masyarakat demokratis.

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
  temperature=1,
  system="Help the user navigate a complex ethical dilemma by identifying core ethical principles, exploring different ethical frameworks, considering potential consequences, acknowledging complexity, encouraging personal reflection, and offering additional resources. Maintain an objective, non-judgmental tone and emphasize critical thinking, empathy, and responsible decision-making.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I am a journalist who has uncovered evidence of corruption involving a high-ranking government official. Publishing the story could lead to public outrage and calls for the official's resignation, but it may also destabilize the government and cause economic uncertainty. The official has offered me a significant bribe to keep the story quiet. Should I accept the bribe, publish the story, or find another solution?"
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
  temperature: 1,
  system: "Help the user navigate a complex ethical dilemma by identifying core ethical principles, exploring different ethical frameworks, considering potential consequences, acknowledging complexity, encouraging personal reflection, and offering additional resources. Maintain an objective, non-judgmental tone and emphasize critical thinking, empathy, and responsible decision-making.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I am a journalist who has uncovered evidence of corruption involving a high-ranking government official. Publishing the story could lead to public outrage and calls for the official's resignation, but it may also destabilize the government and cause economic uncertainty. The official has offered me a significant bribe to keep the story quiet. Should I accept the bribe, publish the story, or find another solution?"
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
    max_tokens=2000,
    temperature=1,
    system="Help the user navigate a complex ethical dilemma by identifying core ethical principles, exploring different ethical frameworks, considering potential consequences, acknowledging complexity, encouraging personal reflection, and offering additional resources. Maintain an objective, non-judgmental tone and emphasize critical thinking, empathy, and responsible decision-making.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "I am a journalist who has uncovered evidence of corruption involving a high-ranking government official. Publishing the story could lead to public outrage and calls for the official's resignation, but it may also destabilize the government and cause economic uncertainty. The official has offered me a significant bribe to keep the story quiet. Should I accept the bribe, publish the story, or find another solution?"
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
  temperature: 1,
  system: "Help the user navigate a complex ethical dilemma by identifying core ethical principles, exploring different ethical frameworks, considering potential consequences, acknowledging complexity, encouraging personal reflection, and offering additional resources. Maintain an objective, non-judgmental tone and emphasize critical thinking, empathy, and responsible decision-making.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I am a journalist who has uncovered evidence of corruption involving a high-ranking government official. Publishing the story could lead to public outrage and calls for the official's resignation, but it may also destabilize the government and cause economic uncertainty. The official has offered me a significant bribe to keep the story quiet. Should I accept the bribe, publish the story, or find another solution?"
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
    temperature=1,
    system="Help the user navigate a complex ethical dilemma by identifying core ethical principles, exploring different ethical frameworks, considering potential consequences, acknowledging complexity, encouraging personal reflection, and offering additional resources. Maintain an objective, non-judgmental tone and emphasize critical thinking, empathy, and responsible decision-making.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "I am a journalist who has uncovered evidence of corruption involving a high-ranking government official. Publishing the story could lead to public outrage and calls for the official's resignation, but it may also destabilize the government and cause economic uncertainty. The official has offered me a significant bribe to keep the story quiet. Should I accept the bribe, publish the story, or find another solution?"
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
temperature: 1,
system: "Help the user navigate a complex ethical dilemma by identifying core ethical principles, exploring different ethical frameworks, considering potential consequences, acknowledging complexity, encouraging personal reflection, and offering additional resources. Maintain an objective, non-judgmental tone and emphasize critical thinking, empathy, and responsible decision-making.",
messages: [
{
"role": "user",
"content": [
{
"type": "text",
"text": "I am a journalist who has uncovered evidence of corruption involving a high-ranking government official. Publishing the story could lead to public outrage and calls for the official's resignation, but it may also destabilize the government and cause economic uncertainty. The official has offered me a significant bribe to keep the story quiet. Should I accept the bribe, publish the story, or find another solution?"
}
]
}
]
});
console.log(msg);
```

</Tab>
</Tabs>