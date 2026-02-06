---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/brand-builder
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 9d1abda697ec4c32b37a9abbc8d31b8e4c2536f82e6410b2b60844fbe37d1baf
---

# Pembuat merek

Buat ringkasan desain untuk identitas merek yang holistik.

---

> Salin prompt ini ke [Konsol](/docs/id/login?selectAccount=true&returnTo=%2Fdashboard%3F) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Sistem | Tugas Anda adalah membuat ringkasan desain yang komprehensif untuk identitas merek yang holistik berdasarkan spesifikasi yang diberikan. Identitas merek harus mencakup berbagai elemen seperti saran untuk nama merek, logo, palet warna, tipografi, gaya visual, nada suara, dan kepribadian merek secara keseluruhan. Pastikan bahwa semua elemen bekerja bersama secara harmonis untuk menciptakan pengalaman merek yang kohesif dan berkesan yang secara efektif mengkomunikasikan nilai-nilai merek, misi, dan proposisi penjualan unik kepada audiens target. Berikan detail yang lengkap dan komprehensif serta sediakan cukup detail spesifik agar seseorang dapat membuat identitas merek yang benar-benar unik.                                                                                              |
| Pengguna   | Spesifikasi merek: Ini adalah merek yang fokus pada pembuatan pakaian dan aksesori berkualitas tinggi dan bergaya menggunakan bahan ramah lingkungan dan metode produksi yang etis. Merek ini menargetkan konsumen yang sadar lingkungan berusia 25-40 tahun yang menghargai fashion, keberlanjutan, dan tanggung jawab sosial. Identitas merek harus mencapai tujuan berikut: 1. Mencerminkan komitmen merek terhadap keberlanjutan, praktik etis, dan penatalayanan lingkungan. 2. Menarik audiens target dengan menyampaikan rasa gaya, kualitas, dan tren. 3. Membedakan merek dari pesaing di pasar fashion berkelanjutan. 4. Menciptakan koneksi emosional yang kuat dengan konsumen dan menginspirasi mereka untuk membuat pilihan yang lebih ramah lingkungan. |

### Contoh keluaran

> Ringkasan Desain: Identitas Merek untuk Merek Fashion Ramah Lingkungan
> Saran Nama Merek: "Sēnsus" (Latin untuk "indera" atau "persepsi," membangkitkan rasa kesadaran dan koneksi dengan lingkungan)
>
> Logo:
>
> - Logo minimalis dan modern yang menggabungkan motif daun atau tanaman bergaya dengan tipografi sans-serif yang elegan.
> - Elemen daun atau tanaman melambangkan komitmen merek terhadap keberlanjutan dan penatalayanan lingkungan, sementara tipografi bersih menyampaikan rasa kecanggihan dan gaya.
> - Logo harus serbaguna dan bekerja dengan baik di berbagai aplikasi, termasuk label pakaian, kemasan, dan platform digital.
>   Palet Warna:
>
> - Palet warna netral dan alami yang mencerminkan etika ramah lingkungan merek, seperti nuansa hijau, beige, dan abu-abu hangat.
> - Warna aksen seperti teal dalam atau kuning mustard dapat digunakan dengan hemat untuk menambah vibrasi dan kedalaman.
> - Palet warna harus membangkitkan rasa harmoni alami dan keseimbangan, sambil tetap fashion-forward dan menarik bagi audiens target.
>   Tipografi:
>
> - Kombinasi tipografi sans-serif modern yang bersih untuk judul dan tipografi serif yang melengkapi untuk isi teks.
> - Tipografi harus mudah dibaca dan menarik secara visual, menyampaikan rasa kualitas dan kecanggihan.
> - Penggunaan konsisten dari hierarki tipografi dan spasi akan menciptakan identitas merek yang kohesif dan terorganisir.
>   Gaya Visual:
>
> - Gaya visual minimalis dan tidak berantakan yang menekankan fotografi produk berkualitas tinggi dan tata letak modern yang bersih.
> - Gabungkan elemen alami, seperti motif tanaman atau tekstur, untuk memperkuat nilai-nilai ramah lingkungan merek dan koneksi dengan alam.
> - Gunakan ruang negatif secara efektif untuk menciptakan rasa keterbukaan dan pernapasan, mencerminkan komitmen merek terhadap keberlanjutan.
>   Nada Suara:
>
> - Nada suara merek harus dapat didekati, berpengetahuan, dan autentik.
> - Gunakan bahasa yang mendidik dan menginspirasi konsumen tentang manfaat fashion berkelanjutan dan metode produksi etis.
> - Gabungkan sentuhan kecanggihan dan gaya untuk menarik sensibilitas yang sadar fashion dari audiens target.
>   Kepribadian Merek:
>
> - Sadar lingkungan dan menyadari lingkungan, namun bergaya dan fashion-forward.
> - Percaya diri dan bersemangat tentang mempromosikan praktik berkelanjutan dan pilihan etis.
> - Inklusif dan ramah, mengundang konsumen untuk bergabung dengan komunitas yang berpikiran sama yang berkomitmen untuk membuat perubahan positif.
>   Secara keseluruhan, identitas merek untuk "Sēnsus" harus mencapai keseimbangan antara nilai-nilai ramah lingkungan dan estetika fashion-forward, menarik konsumen yang ingin terlihat bergaya sambil membuat pilihan yang bertanggung jawab secara lingkungan. Elemen visual dan verbal yang kohesif harus menciptakan koneksi emosional yang kuat dengan audiens target dan menginspirasi mereka untuk merangkul gaya hidup yang lebih berkelanjutan.

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
        system="Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
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
      system: "Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
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
        model="anthropic.claude-opus-4-6-v1",
        max_tokens=2000,
        temperature=1,
        system="Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
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
      model: "anthropic.claude-opus-4-6-v1",
      max_tokens: 2000,
      temperature: 1,
      system: "Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
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
        system="Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
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
      system: "Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>