---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/product-naming-pro
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: fd38c7dac854875d31c7a1cd7eb4037b1701d63f9699bd8bf4b0c55e0dedaeea
---

# Penamaan produk pro

Buat nama produk yang menarik dari deskripsi dan kata kunci.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                          |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Sistem | Tugas Anda adalah menghasilkan nama produk yang kreatif, berkesan, dan dapat dipasarkan berdasarkan deskripsi dan kata kunci yang diberikan. Nama produk harus ringkas (2-4 kata), evocative, dan mudah dipahami oleh audiens target. Hindari nama yang generik atau terlalu literal. Sebaliknya, bertujuan untuk membuat nama yang menonjol, menangkap esensi produk, dan meninggalkan kesan yang bertahan lama. |
| Pengguna   | Deskripsi: Headphone nirkabel peredam bising over-ear dengan daya tahan baterai 20 jam dan kontrol sentuh. Dirancang untuk audiophile dan frequent traveler. Kata kunci: immersive, comfortable, high-fidelity, long-lasting, convenient                                                                                                                                                          |

## Contoh output

> 1. SoundOasis Elite
>    2. AudioZen Nomad
>    3. Serenity Pro
>    4. Tranquility Touch
>    5. Harmonix Journey
>    6. SonicSolace Roam
>    7. Auditory Bliss
>    8. Quietude Quest
>    9. Euphony Excursion
>    10. Acoustica Wanderlust

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
        max_tokens=1000,
        temperature=1,
        system="Your task is to generate creative, memorable, and marketable product names based on the provided description and keywords. The product names should be concise (2-4 words), evocative, and easily understood by the target audience. Avoid generic or overly literal names. Instead, aim to create a name that stands out, captures the essence of the product, and leaves a lasting impression.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Description: A noise-canceling, wireless, over-ear headphone with a 20-hour battery life and touch controls. Designed for audiophiles and frequent travelers.  \n  \nKeywords: immersive, comfortable, high-fidelity, long-lasting, convenient"
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
      max_tokens: 1000,
      temperature: 1,
      system: "Your task is to generate creative, memorable, and marketable product names based on the provided description and keywords. The product names should be concise (2-4 words), evocative, and easily understood by the target audience. Avoid generic or overly literal names. Instead, aim to create a name that stands out, captures the essence of the product, and leaves a lasting impression.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Description: A noise-canceling, wireless, over-ear headphone with a 20-hour battery life and touch controls. Designed for audiophiles and frequent travelers.  \n  \nKeywords: immersive, comfortable, high-fidelity, long-lasting, convenient"
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
        max_tokens=1000,
        temperature=1,
        system="Your task is to generate creative, memorable, and marketable product names based on the provided description and keywords. The product names should be concise (2-4 words), evocative, and easily understood by the target audience. Avoid generic or overly literal names. Instead, aim to create a name that stands out, captures the essence of the product, and leaves a lasting impression.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Description: A noise-canceling, wireless, over-ear headphone with a 20-hour battery life and touch controls. Designed for audiophiles and frequent travelers.  \n  \nKeywords: immersive, comfortable, high-fidelity, long-lasting, convenient"
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
      max_tokens: 1000,
      temperature: 1,
      system: "Your task is to generate creative, memorable, and marketable product names based on the provided description and keywords. The product names should be concise (2-4 words), evocative, and easily understood by the target audience. Avoid generic or overly literal names. Instead, aim to create a name that stands out, captures the essence of the product, and leaves a lasting impression.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Description: A noise-canceling, wireless, over-ear headphone with a 20-hour battery life and touch controls. Designed for audiophiles and frequent travelers.  \n  \nKeywords: immersive, comfortable, high-fidelity, long-lasting, convenient"
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
        max_tokens=1000,
        temperature=1,
        system="Your task is to generate creative, memorable, and marketable product names based on the provided description and keywords. The product names should be concise (2-4 words), evocative, and easily understood by the target audience. Avoid generic or overly literal names. Instead, aim to create a name that stands out, captures the essence of the product, and leaves a lasting impression.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Description: A noise-canceling, wireless, over-ear headphone with a 20-hour battery life and touch controls. Designed for audiophiles and frequent travelers.\n\nKeywords: immersive, comfortable, high-fidelity, long-lasting, convenient"
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
      max_tokens: 1000,
      temperature: 1,
      system: "Your task is to generate creative, memorable, and marketable product names based on the provided description and keywords. The product names should be concise (2-4 words), evocative, and easily understood by the target audience. Avoid generic or overly literal names. Instead, aim to create a name that stands out, captures the essence of the product, and leaves a lasting impression.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Description: A noise-canceling, wireless, over-ear headphone with a 20-hour battery life and touch controls. Designed for audiophiles and frequent travelers.\n\nKeywords: immersive, comfortable, high-fidelity, long-lasting, convenient"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>