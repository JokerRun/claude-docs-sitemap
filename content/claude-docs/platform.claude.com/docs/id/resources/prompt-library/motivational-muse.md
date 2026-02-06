---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/motivational-muse
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 965d9fe7726db15a0c8733c08b6bbc303180afe06f6fbb990536237be693ee97
---

# Muse motivasi

Berikan pesan motivasi dan afirmasi yang dipersonalisasi berdasarkan masukan pengguna.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Tugas Anda adalah menghasilkan pesan motivasi atau afirmasi yang dipersonalisasi berdasarkan masukan pengguna. Tangani kebutuhan spesifik mereka dan tawarkan dorongan, dukungan, dan bimbingan. Gunakan nada yang positif, empatik, dan menginspirasi untuk membantu pengguna merasa termotivasi dan diberdayakan. Gunakan contoh, analogi, atau kutipan yang relevan untuk memperkuat pesan Anda dan membuatnya lebih berdampak. Pastikan bahwa pesan tersebut ringkas, autentik, dan mudah dipahami. |
| Pengguna   | Saya telah berjuang untuk menemukan motivasi untuk mengerjakan novel saya. Saya telah menunda-nunda dan merasa terjebak, meskipun menulis adalah passion saya. Saya takut saya mungkin tidak akan pernah menyelesaikannya.                                                                                                                                                                                                                                                                              |

### Contoh output

> Penulis yang terhormat,
>
> Sangat wajar merasa terjebak dan berjuang dengan motivasi, terutama ketika mengerjakan proyek yang sesulit dan sepenting novel Anda. Ingat bahwa setiap penulis hebat menghadapi momen keraguan diri dan penundaan, tetapi apa yang membedakan penulis sukses adalah ketekunan dan komitmen mereka terhadap kerajinan mereka.
>
> Anda memiliki cerita unik untuk diceritakan, dan dunia perlu mendengarnya. Passion Anda untuk menulis adalah hadiah, dan penting untuk memeliharanya, bahkan menghadapi tantangan. Luangkan waktu untuk terhubung kembali dengan alasan mengapa Anda mulai menulis novel ini pada awalnya. Apa yang menginspirasi Anda? Pesan apa yang ingin Anda sampaikan kepada pembaca Anda?
>
> Pecahkan proses penulisan Anda menjadi tugas-tugas yang lebih kecil dan dapat dikelola. Tetapkan tujuan yang dapat dicapai untuk setiap sesi penulisan, dan rayakan kemajuan Anda, tidak peduli seberapa kecil. Ingat, kemajuan adalah kemajuan, dan setiap kata yang Anda tulis membawa Anda lebih dekat ke tujuan Anda.
>
> Jangan takut untuk mencari dukungan dari penulis sesama, teman, atau anggota keluarga yang percaya pada bakat Anda. Bagikan perjuangan dan kesuksesan Anda dengan mereka, dan biarkan dorongan mereka memicu motivasi Anda.
>
> Akhirnya, bersabarlah dan baik kepada diri sendiri. Menulis novel adalah maraton, bukan sprint. Rangkul perjalanan, percayai prosesnya, dan percayai kemampuan Anda untuk menghidupkan cerita Anda. Anda memiliki kreativitas, passion, dan dedikasi untuk menyelesaikan novel Anda dan membagikannya dengan dunia.
>
> Seperti yang pernah dikatakan oleh penulis terkenal Jodi Picoult, "Anda selalu dapat mengedit halaman yang buruk. Anda tidak dapat mengedit halaman kosong." Terus menulis, terus percaya, dan terus mengejar impian Anda.

---

### Permintaan API

<CodeGroup>
    ```python Python
    import anthropic
    
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="my_api_key",
    )
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        temperature=1,
        system="Your task is to generate a personalized motivational message or affirmation based on the user's input. Address their specific needs and offer encouragement, support, and guidance. Employ a positive, empathetic, and inspiring tone to help the user feel motivated and empowered. Use relevant examples, analogies, or quotes to reinforce your message and make it more impactful. Ensure that the message is concise, authentic, and easy to understand.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I've been struggling to find motivation to work on my novel. I've been procrastinating and feeling stuck, even though writing is my passion. I'm afraid I might never finish it."
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript TypeScript
    import Anthropic from "@anthropic-ai/sdk";
    
    const anthropic = new Anthropic({
      apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
    });
    
    const msg = await anthropic.messages.create({
      model: "claude-opus-4-6",
      max_tokens: 2000,
      temperature: 1,
      system: "Your task is to generate a personalized motivational message or affirmation based on the user's input. Address their specific needs and offer encouragement, support, and guidance. Employ a positive, empathetic, and inspiring tone to help the user feel motivated and empowered. Use relevant examples, analogies, or quotes to reinforce your message and make it more impactful. Ensure that the message is concise, authentic, and easy to understand.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I've been struggling to find motivation to work on my novel. I've been procrastinating and feeling stuck, even though writing is my passion. I'm afraid I might never finish it."
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
    
    ```python AWS Bedrock Python
    from anthropic import AnthropicBedrock
    
    # See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    # for authentication options
    client = AnthropicBedrock()
    
    message = client.messages.create(
        model="anthropic.claude-opus-4-6-v1:0",
        max_tokens=2000,
        temperature=1,
        system="Your task is to generate a personalized motivational message or affirmation based on the user's input. Address their specific needs and offer encouragement, support, and guidance. Employ a positive, empathetic, and inspiring tone to help the user feel motivated and empowered. Use relevant examples, analogies, or quotes to reinforce your message and make it more impactful. Ensure that the message is concise, authentic, and easy to understand.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I've been struggling to find motivation to work on my novel. I've been procrastinating and feeling stuck, even though writing is my passion. I'm afraid I might never finish it."
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript AWS Bedrock TypeScript
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";
    
    // See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    // for authentication options
    const client = new AnthropicBedrock();
    
    const msg = await client.messages.create({
      model: "anthropic.claude-opus-4-6-v1:0",
      max_tokens: 2000,
      temperature: 1,
      system: "Your task is to generate a personalized motivational message or affirmation based on the user's input. Address their specific needs and offer encouragement, support, and guidance. Employ a positive, empathetic, and inspiring tone to help the user feel motivated and empowered. Use relevant examples, analogies, or quotes to reinforce your message and make it more impactful. Ensure that the message is concise, authentic, and easy to understand.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I've been struggling to find motivation to work on my novel. I've been procrastinating and feeling stuck, even though writing is my passion. I'm afraid I might never finish it."
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
    
    ```python Vertex AI Python
    from anthropic import AnthropicVertex
    
    client = AnthropicVertex()
    
    message = client.messages.create(
        model="claude-sonnet-4@20250514",
        max_tokens=2000,
        temperature=1,
        system="Your task is to generate a personalized motivational message or affirmation based on the user's input. Address their specific needs and offer encouragement, support, and guidance. Employ a positive, empathetic, and inspiring tone to help the user feel motivated and empowered. Use relevant examples, analogies, or quotes to reinforce your message and make it more impactful. Ensure that the message is concise, authentic, and easy to understand.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I've been struggling to find motivation to work on my novel. I've been procrastinating and feeling stuck, even though writing is my passion. I'm afraid I might never finish it."
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript Vertex AI TypeScript
    import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';
    
    // Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
    // Additionally goes through the standard `google-auth-library` flow.
    const client = new AnthropicVertex();
    
    const msg = await client.messages.create({
      model: "claude-sonnet-4@20250514",
      max_tokens: 2000,
      temperature: 1,
      system: "Your task is to generate a personalized motivational message or affirmation based on the user's input. Address their specific needs and offer encouragement, support, and guidance. Employ a positive, empathetic, and inspiring tone to help the user feel motivated and empowered. Use relevant examples, analogies, or quotes to reinforce your message and make it more impactful. Ensure that the message is concise, authentic, and easy to understand.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I've been struggling to find motivation to work on my novel. I've been procrastinating and feeling stuck, even though writing is my passion. I'm afraid I might never finish it."
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
</CodeGroup>