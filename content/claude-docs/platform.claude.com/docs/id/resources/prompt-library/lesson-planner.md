---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/lesson-planner
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: f10b8481f4f7280603be956e5b0fe55c6223e5cef311a7e3af13318324af8134
---

# Perencana pelajaran

Buat rencana pelajaran mendalam tentang subjek apa pun.

---

> Salin prompt ini ke [Konsol](/docs/id/login?selectAccount=true&returnTo=%2Fdashboard%3F) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Tugas Anda adalah membuat rencana pelajaran yang komprehensif, menarik, dan terstruktur dengan baik tentang subjek yang diberikan. Rencana pelajaran harus dirancang untuk sesi kelas selama 60 menit dan harus disesuaikan dengan tingkat kelas atau kelompok usia tertentu. Mulai dengan menyatakan tujuan pelajaran, yang harus jelas, terukur, dan selaras dengan standar pendidikan yang relevan. Selanjutnya, berikan garis besar pelajaran yang terperinci, membaginya menjadi pengenalan, kegiatan utama, dan kesimpulan. Untuk setiap bagian, jelaskan metode pengajaran, kegiatan pembelajaran, dan sumber daya yang akan Anda gunakan untuk menyampaikan konten secara efektif dan melibatkan siswa. Terakhir, jelaskan metode penilaian yang akan Anda gunakan untuk mengevaluasi pemahaman dan penguasaan siswa terhadap tujuan pelajaran. Rencana pelajaran harus terorganisir dengan baik, mudah diikuti, dan mempromosikan pembelajaran aktif dan pemikiran kritis. |
| Pengguna   | Subjek: Pengenalan Fotosintesis Tingkat Kelas: Kelas 7 (Usia 12-13)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

## Contoh keluaran

> Rencana Pelajaran: Pengenalan Fotosintesis
> Tingkat Kelas: Kelas 7 (Usia 12-13)
> Durasi: 60 menit
>
> Tujuan Pelajaran:
> Pada akhir pelajaran, siswa akan dapat:
>
> 1. Mendefinisikan fotosintesis dan menjelaskan pentingnya dalam ekosistem.
> 2. Mengidentifikasi komponen kunci yang diperlukan untuk fotosintesis terjadi.
> 3. Menjelaskan proses fotosintesis, termasuk peran energi cahaya, karbon dioksida, dan air.
> 4. Mengenali produk fotosintesis dan signifikansinya bagi organisme hidup.
>    Garis Besar Pelajaran:
>
> 5. Pengenalan (10 menit)
>    i. Libatkan siswa dengan menampilkan klip video pendek atau gambar tanaman dan mendiskusikan peran mereka di lingkungan.
>    ii. Perkenalkan konsep fotosintesis dan pentingnya dalam mempertahankan kehidupan di Bumi.
>    iii. Nyatakan tujuan pelajaran dan berikan gambaran umum tentang struktur pelajaran.
> 6. Kegiatan Utama (40 menit)
>    i. Instruksi Terpandu (15 menit)
>    a. Jelaskan komponen kunci yang diperlukan untuk fotosintesis: sinar matahari, karbon dioksida, air, dan klorofil.
>    b. Jelaskan proses fotosintesis, menekankan peran energi cahaya, karbon dioksida, dan air.
>    c. Diskusikan produk fotosintesis (glukosa dan oksigen) dan signifikansinya bagi organisme hidup.
>    ii. Kegiatan Kelompok Kecil (15 menit)
>    a. Bagi kelas menjadi kelompok-kelompok kecil dan berikan setiap kelompok lembar kerja atau pengorganisir grafis.
>    b. Minta siswa untuk bekerja sama membuat representasi visual dari proses fotosintesis, memberi label pada komponen dan produk kunci.
>    c. Dorong siswa untuk mendiskusikan dan menjelaskan pemahaman mereka tentang fotosintesis dalam kelompok mereka.
>    iii. Diskusi Kelas (10 menit)
>    a. Undang setiap kelompok untuk berbagi representasi visual mereka dengan kelas.
>    b. Fasilitasi diskusi kelas, mendorong siswa untuk mengajukan pertanyaan, memberikan umpan balik, dan mengklarifikasi kesalahpahaman apa pun.
> 7. Kesimpulan (10 menit)
>    i. Ringkas poin-poin kunci pelajaran, memperkuat definisi, komponen, proses, dan produk fotosintesis.
>    ii. Berikan kuis singkat atau tiket keluar untuk menilai pemahaman siswa tentang tujuan pelajaran.
>    iii. Berikan siswa tugas pekerjaan rumah untuk lebih mengeksplorasi pentingnya fotosintesis dalam ekosistem yang berbeda.
>    Metode Penilaian:
>
> 8. Penilaian formatif: Amati partisipasi dan pemahaman siswa selama instruksi terpandu dan kegiatan kelompok kecil.
> 9. Penilaian sumatif: Evaluasi representasi visual siswa dan kinerja mereka pada kuis singkat atau tiket keluar.
> 10. Tugas pekerjaan rumah: Tinjau pengajuan pekerjaan rumah siswa untuk mengukur kemampuan mereka menerapkan konsep yang dipelajari dalam pelajaran.
>     Sumber Daya:
>
> 11. Klip video atau gambar tanaman dan peran mereka di lingkungan
> 12. Lembar kerja atau pengorganisir grafis untuk kegiatan kelompok kecil
> 13. Kuis singkat atau tiket keluar untuk penilaian
> 14. Instruksi tugas pekerjaan rumah

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
        max_tokens=4000,
        temperature=0.5,
        system="Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
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
      max_tokens: 4000,
      temperature: 0.5,
      system: "Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
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
        max_tokens=4000,
        temperature=0.5,
        system="Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
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
      max_tokens: 4000,
      temperature: 0.5,
      system: "Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
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
        max_tokens=4000,
        temperature=0.5,
        system="Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
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
      max_tokens: 4000,
      temperature: 0.5,
      system: "Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>