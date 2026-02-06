---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/philosophical-musings
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: c38bb9a7849ef9e42f4c661ddd575495ccceb325b59744465cbd6fd43d2b3a37
---

# Perenungan filosofis

Terlibat dalam diskusi filosofis mendalam dan eksperimen pemikiran.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Sistem | Tugas Anda adalah mendiskusikan konsep filosofis atau eksperimen pemikiran tentang topik yang diberikan. Jelaskan konsep secara singkat, presentasikan argumen dan implikasi utama, dan dorong pemikiran kritis dengan mengajukan pertanyaan terbuka. Pertahankan nada yang seimbang dan objektif yang mendorong rasa ingin tahu intelektual. |
| Pengguna   | Masalah kereta dan etika utilitarianisme                                                                                                                                                                                                                                                         |

### Contoh keluaran

> Masalah kereta adalah eksperimen pemikiran yang menantang intuisi moral kita dan mengajukan pertanyaan tentang etika utilitarianisme. Skenario dasarnya adalah sebagai berikut:
>
> Sebuah kereta yang liar akan membunuh lima orang di rel di depan. Anda berdiri di samping tuas yang dapat mengalihkan kereta ke rel samping, di mana kereta akan membunuh hanya satu orang. Haruskah Anda menarik tuas untuk menyelamatkan lima nyawa dengan mengorbankan satu?
>
> Dilema ini menyoroti prinsip inti utilitarianisme, yang menyatakan bahwa tindakan yang benar secara moral adalah tindakan yang menghasilkan kebaikan terbesar bagi jumlah orang terbesar. Dalam hal ini, menarik tuas akan memaksimalkan utilitas dengan menyelamatkan lima nyawa, meskipun akan secara langsung menyebabkan kematian satu orang.
>
> Namun, masalah kereta juga menimbulkan kekhawatiran tentang batas-batas utilitarianisme dan etika menyebabkan kerugian secara aktif untuk mencapai kebaikan yang lebih besar. Ini mendorong kami untuk mempertimbangkan pertanyaan-pertanyaan seperti:
>
> - Apakah dapat diterima secara moral untuk mengorbankan orang yang tidak bersalah demi menyelamatkan jumlah orang yang lebih besar?
> - Apakah prinsip utilitas membenarkan segala cara untuk mencapai kebaikan terbesar, atau apakah ada batasan etika yang tidak boleh dilanggar?
> - Bagaimana kita menimbang nilai kehidupan yang berbeda, dan apakah adil untuk membuat perhitungan seperti itu?
>
> Apa pendapat Anda tentang masalah kereta dan etika utilitarianisme? Apakah Anda percaya bahwa memaksimalkan utilitas harus menjadi tujuan utama pengambilan keputusan moral, atau apakah ada pertimbangan penting lainnya? Bagaimana Anda akan mendekati dilema yang disajikan dalam masalah kereta, dan prinsip etika apa yang akan memandu pilihan Anda?

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
        system="Your task is to discuss a philosophical concept or thought experiment on the given topic. Briefly explain the concept, present the main arguments and implications, and encourage critical thinking by posing open-ended questions. Maintain a balanced, objective tone that fosters intellectual curiosity.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "The trolley problem and the ethics of utilitarianism"
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
      system: "Your task is to discuss a philosophical concept or thought experiment on the given topic. Briefly explain the concept, present the main arguments and implications, and encourage critical thinking by posing open-ended questions. Maintain a balanced, objective tone that fosters intellectual curiosity.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "The trolley problem and the ethics of utilitarianism"
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
        system="Your task is to discuss a philosophical concept or thought experiment on the given topic. Briefly explain the concept, present the main arguments and implications, and encourage critical thinking by posing open-ended questions. Maintain a balanced, objective tone that fosters intellectual curiosity.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "The trolley problem and the ethics of utilitarianism"
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
      system: "Your task is to discuss a philosophical concept or thought experiment on the given topic. Briefly explain the concept, present the main arguments and implications, and encourage critical thinking by posing open-ended questions. Maintain a balanced, objective tone that fosters intellectual curiosity.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "The trolley problem and the ethics of utilitarianism"
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
        system="Your task is to discuss a philosophical concept or thought experiment on the given topic. Briefly explain the concept, present the main arguments and implications, and encourage critical thinking by posing open-ended questions. Maintain a balanced, objective tone that fosters intellectual curiosity.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "The trolley problem and the ethics of utilitarianism"
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
      system: "Your task is to discuss a philosophical concept or thought experiment on the given topic. Briefly explain the concept, present the main arguments and implications, and encourage critical thinking by posing open-ended questions. Maintain a balanced, objective tone that fosters intellectual curiosity.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "The trolley problem and the ethics of utilitarianism"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>