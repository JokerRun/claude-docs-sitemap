---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/alliteration-alchemist
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 7fea109576b250f8a38e7e0208a9fc47aa594214e54888a3e02a9fcdcda2b078
---

# Alliteration alchemist

Hasilkan frasa dan kalimat aliteratif untuk subjek apa pun.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                           |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | Tugas Anda adalah membuat frasa dan kalimat aliteratif untuk subjek yang diberikan. Pastikan bahwa aliterasi tidak hanya terdengar menyenangkan tetapi juga menyampaikan informasi yang relevan atau membangkitkan emosi yang sesuai terkait dengan subjek. |
| User   | Laut                                                                                                                                                                                                                             |

### Contoh output

> 1.  Ombak yang berbisik membasahi pantai.
> 2.  Semprotan laut yang asin memercik di pasir.
> 3.  Arus yang menghantam mengukir tebing pesisir.
> 4.  Kedalaman yang dalam dan gelap menyembunyikan bahaya tersembunyi.
> 5.  Aliran yang bergemuruh membawa kehidupan ke pantai.
> 6.  Mamalia yang megah dan agung bermigrasi melalui perairan.
> 7.  Pasang surut yang menggelegar melempar kapal ke sana kemari.
> 8.  Terumbu yang berkilau melindungi makhluk laut yang tersembunyi.
> 9.  Riak yang bergelombang mengungkapkan dunia di bawah permukaan.
> 10. Laut yang berputar dan membengkak membentuk garis pantai.
> 11. Gumpalan es yang berbusa dan berbuih mengalir dengan bebas.
> 12. Burung camar yang anggun meluncur di atas laut yang berkilau.
> 13. Lumba-lumba yang ceria menyelam melalui perairan yang murni.
> 14. Angin laut yang asin berhembus melintasi biru yang tak terbatas.
> 15. Riak yang berirama bergulir menuju pantai yang berbatu.
> 16. Gua karang menyembunyikan komunitas akuatik yang penuh warna.
> 17. Langit yang badai dan laut yang membengkak menandakan kekuatan alam.
> 18. Pasang surut yang berguling mengubah teluk yang tenang.
> 19. Angin yang berputar dan bersiul menyapu gelombang.
> 20. Perairan safir yang tenang membentang hingga ke cakrawala.

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
        max_tokens=1000,
        temperature=1,
        system="Your task is to create alliterative phrases and sentences for the given subject. Ensure that the alliterations not only sound pleasing but also convey relevant information or evoke appropriate emotions related to the subject.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Ocean"
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
      system: "Your task is to create alliterative phrases and sentences for the given subject. Ensure that the alliterations not only sound pleasing but also convey relevant information or evoke appropriate emotions related to the subject.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Ocean"
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
        system="Your task is to create alliterative phrases and sentences for the given subject. Ensure that the alliterations not only sound pleasing but also convey relevant information or evoke appropriate emotions related to the subject.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Ocean"
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
      system: "Your task is to create alliterative phrases and sentences for the given subject. Ensure that the alliterations not only sound pleasing but also convey relevant information or evoke appropriate emotions related to the subject.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Ocean"
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
        system="Your task is to create alliterative phrases and sentences for the given subject. Ensure that the alliterations not only sound pleasing but also convey relevant information or evoke appropriate emotions related to the subject.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Ocean"
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
      system: "Your task is to create alliterative phrases and sentences for the given subject. Ensure that the alliterations not only sound pleasing but also convey relevant information or evoke appropriate emotions related to the subject.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Ocean"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>