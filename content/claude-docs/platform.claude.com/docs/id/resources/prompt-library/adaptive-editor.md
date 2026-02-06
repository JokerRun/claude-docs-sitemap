---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/adaptive-editor
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 7e9a97ac047030e290b424d64ccc2efd6133fb8770a58582935ffb19869c64d4
---

# Editor adaptif

Tulis ulang teks mengikuti instruksi yang diberikan pengguna, seperti dengan nada, audiens, atau gaya yang berbeda.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|      | Konten                                                                                                                                                                                                                                                                                                                                                                              |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Pengguna | Tulis ulang paragraf berikut menggunakan instruksi berikut: dalam gaya seorang bajak laut. Paragraf: Pada tahun 1758, ahli botani dan zoolog Swedia Carl Linnaeus menerbitkan dalam Systema Naturae-nya, penamaan dua kata spesies (nomenklatur binomial). Canis adalah kata Latin yang berarti "anjing", dan di bawah genus ini, dia mendaftarkan anjing domestik, serigala, dan jackal emas. |

### Contoh keluaran

> Ahoy mateys! Kembali pada tahun 1758, ahli botani yang jahat itu dan pecinta hewan Carl Linnaeus mengeluarkan bukunya Systema Naturae, yang memiliki nama-nama dua kata yang mewah untuk semua jenis makhluk (nomenklatur binomial yang dia sebut). Canis adalah kata bajak laut untuk ""anjing"", dan di bawah judul itu dia mendaftarkan anjing biasa, serigala, dan jackal emas juga. Arrr! Semua anjing itu sama bagi Kapten Linnaeus tua. Dia mungkin memiliki kaki kayu dan burung beo di bahunya ketika dia menulis buku itu! Haha! Sekarang bersihkan geladak kalian, para bajak laut, sebelum saya membuat kalian berjalan di papan!

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
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Tulis ulang paragraf berikut menggunakan instruksi berikut: dalam gaya seorang bajak laut.  \n  \nParagraf:  \nPada tahun 1758, ahli botani dan zoolog Swedia Carl Linnaeus menerbitkan dalam Systema Naturae-nya, penamaan dua kata spesies (nomenklatur binomial). Canis adalah kata Latin yang berarti \"anjing\", dan di bawah genus ini, dia mendaftarkan anjing domestik, serigala, dan jackal emas."
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
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Tulis ulang paragraf berikut menggunakan instruksi berikut: dalam gaya seorang bajak laut.  \n  \nParagraf:  \nPada tahun 1758, ahli botani dan zoolog Swedia Carl Linnaeus menerbitkan dalam Systema Naturae-nya, penamaan dua kata spesies (nomenklatur binomial). Canis adalah kata Latin yang berarti \"anjing\", dan di bawah genus ini, dia mendaftarkan anjing domestik, serigala, dan jackal emas."
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
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Tulis ulang paragraf berikut menggunakan instruksi berikut: dalam gaya seorang bajak laut.  \n  \nParagraf:  \nPada tahun 1758, ahli botani dan zoolog Swedia Carl Linnaeus menerbitkan dalam Systema Naturae-nya, penamaan dua kata spesies (nomenklatur binomial). Canis adalah kata Latin yang berarti \"anjing\", dan di bawah genus ini, dia mendaftarkan anjing domestik, serigala, dan jackal emas."
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
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Tulis ulang paragraf berikut menggunakan instruksi berikut: dalam gaya seorang bajak laut.  \n  \nParagraf:  \nPada tahun 1758, ahli botani dan zoolog Swedia Carl Linnaeus menerbitkan dalam Systema Naturae-nya, penamaan dua kata spesies (nomenklatur binomial). Canis adalah kata Latin yang berarti \"anjing\", dan di bawah genus ini, dia mendaftarkan anjing domestik, serigala, dan jackal emas."
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
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Tulis ulang paragraf berikut menggunakan instruksi berikut: dalam gaya seorang bajak laut.  \n  \nParagraf:  \nPada tahun 1758, ahli botani dan zoolog Swedia Carl Linnaeus menerbitkan dalam Systema Naturae-nya, penamaan dua kata spesies (nomenklatur binomial). Canis adalah kata Latin yang berarti \"anjing\", dan di bawah genus ini, dia mendaftarkan anjing domestik, serigala, dan jackal emas."
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
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Tulis ulang paragraf berikut menggunakan instruksi berikut: dalam gaya seorang bajak laut.  \n  \nParagraf:  \nPada tahun 1758, ahli botani dan zoolog Swedia Carl Linnaeus menerbitkan dalam Systema Naturae-nya, penamaan dua kata spesies (nomenklatur binomial). Canis adalah kata Latin yang berarti \"anjing\", dan di bawah genus ini, dia mendaftarkan anjing domestik, serigala, dan jackal emas."
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>