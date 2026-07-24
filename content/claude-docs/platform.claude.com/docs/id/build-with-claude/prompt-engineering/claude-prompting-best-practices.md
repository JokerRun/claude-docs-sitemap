---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 0d34595187006e62c2b9dfd40bdcd06b7a84f483b12f1c8a225678f7ab66291d
---

# Praktik terbaik prompting

Panduan komprehensif tentang teknik rekayasa prompt untuk model-model terbaru Claude, mencakup kejelasan, contoh, penstrukturan XML, pemikiran, dan sistem agentik.

---

Ini adalah referensi untuk rekayasa prompt dengan model-model terbaru Claude, termasuk Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, dan Claude Haiku 4.5. Halaman ini disusun dalam tiga bagian:

* **Panduan spesifik model** terlebih dahulu: di mana [Claude Fable 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5), [Claude Sonnet 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5), dan [Claude Opus 4.8](/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-4-8) berperilaku berbeda dan apa yang perlu diubah.
* **Teknik untuk semua model saat ini** setelah itu: prinsip umum, output dan pemformatan, penggunaan alat, pemikiran, dan sistem agentik.
* **Pertimbangan migrasi** terakhir, untuk prompt yang berpindah dari generasi sebelumnya.

<Tip>
  Untuk gambaran umum kemampuan model, lihat [gambaran umum model](/docs/id/about-claude/models/overview). Untuk kemampuan Claude Fable 5 dan perubahan API, lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5). Untuk detail tentang apa yang baru di Claude Sonnet 5, lihat [Apa yang baru di Claude Sonnet 5](/docs/id/about-claude/models/whats-new-sonnet-5). Untuk detail tentang apa yang baru di Claude Opus 4.8, lihat [Apa yang baru di Claude Opus 4.8](/docs/id/about-claude/models/whats-new-claude-4-8). Untuk panduan migrasi, lihat [Panduan migrasi](/docs/id/about-claude/models/migration-guide).
</Tip>

## Claude Fable 5

Panduan prompting untuk Claude Fable 5 dan Claude Mythos 5 memiliki halamannya sendiri: [Prompting Claude Fable 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5). Halaman tersebut mencakup perbedaan perilaku dari Claude Opus 4.8 serta perubahan prompt dan scaffolding yang layak dilakukan, termasuk tingkat effort, kepatuhan terhadap instruksi, klaim kemajuan jangka panjang, sistem memori, dan kategori penolakan `reasoning_extraction`.

## Claude Sonnet 5

Panduan prompting untuk Claude Sonnet 5 memiliki halamannya sendiri: [Prompting Claude Sonnet 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5). Halaman tersebut mencakup perbedaan perilaku dari Claude Sonnet 4.6 dan perubahan prompt yang layak dilakukan, termasuk panjang respons, kalibrasi effort dan kedalaman pemikiran, pemicu penggunaan alat, kepatuhan instruksi secara literal, serta default desain dan frontend.

## Prompting Claude Opus 4.8

Panduan prompting untuk Claude Opus 4.8 memiliki halamannya sendiri: [Prompting Claude Opus 4.8](/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-4-8). Halaman tersebut mencakup panjang respons, kalibrasi effort dan kedalaman pemikiran, pemicu penggunaan alat, kepatuhan instruksi secara literal, kontrol subagen, serta default desain dan frontend.

## Prinsip umum

Teknik-teknik di bagian ini dan bagian-bagian berikutnya berlaku untuk semua model Claude saat ini, termasuk Claude Fable 5 dan Claude Mythos 5.

### Jelas dan langsung

Claude merespons dengan baik terhadap instruksi yang jelas dan eksplisit. Bersikap spesifik tentang output yang Anda inginkan dapat membantu meningkatkan hasil. Jika Anda menginginkan perilaku "melampaui ekspektasi", minta secara eksplisit alih-alih mengandalkan model untuk menyimpulkannya dari prompt yang samar.

Anggap Claude sebagai karyawan baru yang brilian tetapi tidak memiliki konteks tentang norma dan alur kerja Anda. Semakin tepat Anda menjelaskan apa yang Anda inginkan, semakin baik hasilnya.

**Aturan emas:** Tunjukkan prompt Anda kepada rekan kerja yang memiliki konteks minimal tentang tugas tersebut dan minta mereka mengikutinya. Jika mereka bingung, Claude juga akan bingung.

* Bersikap spesifik tentang format output dan batasan yang diinginkan.
* Berikan instruksi sebagai langkah-langkah berurutan menggunakan daftar bernomor atau poin-poin ketika urutan atau kelengkapan langkah itu penting.

<Accordion title="Contoh: Membuat dasbor analitik">
  **Kurang efektif:**

  ```text wrap
  Create an analytics dashboard
  ```

  **Lebih efektif:**

  ```text wrap
  Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.
  ```
</Accordion>

### Tambahkan konteks untuk meningkatkan kinerja

Memberikan konteks atau motivasi di balik instruksi Anda, seperti menjelaskan kepada Claude mengapa perilaku tersebut penting, dapat membantu Claude lebih memahami tujuan Anda dan memberikan respons yang lebih tepat sasaran.

<Accordion title="Contoh: Preferensi pemformatan">
  **Kurang efektif:**

  ```text wrap
  NEVER use ellipses
  ```

  **Lebih efektif:**

  ```text wrap
  Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them.
  ```
</Accordion>

Claude cukup cerdas untuk menggeneralisasi dari penjelasan tersebut.

### Gunakan contoh secara efektif

Contoh adalah salah satu cara paling andal untuk mengarahkan format output, nada, dan struktur Claude. Beberapa contoh yang dibuat dengan baik (dikenal sebagai few-shot atau multishot prompting) meningkatkan akurasi dan konsistensi.

Saat menambahkan contoh, pastikan contoh tersebut:

* **Relevan:** Mencerminkan kasus penggunaan aktual Anda secara dekat.
* **Beragam:** Mencakup kasus tepi dan cukup bervariasi sehingga Claude tidak menangkap pola yang tidak diinginkan.
* **Terstruktur:** Bungkus contoh dalam tag `<example>` (beberapa contoh dalam tag `<examples>`) agar Claude dapat membedakannya dari instruksi.

<Tip>
  Sertakan 3–5 contoh untuk hasil terbaik. Anda juga dapat meminta Claude untuk mengevaluasi contoh Anda dari segi relevansi dan keragaman, atau untuk menghasilkan contoh tambahan berdasarkan set awal Anda.
</Tip>

### Strukturkan prompt dengan tag XML

Tag XML membantu Claude mengurai prompt yang kompleks tanpa ambiguitas, terutama ketika prompt Anda mencampur instruksi, konteks, contoh, dan input variabel. Membungkus setiap jenis konten dalam tagnya sendiri (misalnya, `<instructions>`, `<context>`, `<input>`) mengurangi salah tafsir.

Praktik terbaik:

* Gunakan nama tag yang konsisten dan deskriptif di seluruh prompt Anda.
* Sarangkan tag ketika konten memiliki hierarki alami (dokumen di dalam `<documents>`, masing-masing di dalam `<document index="n">`).

### Berikan Claude sebuah peran

Menetapkan peran dalam prompt sistem memfokuskan perilaku dan nada Claude untuk kasus penggunaan Anda. Bahkan satu kalimat saja membuat perbedaan:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "system": "You are a helpful coding assistant specializing in Python.",
      "messages": [
        {"role": "user", "content": "How do I sort a list of dictionaries by key?"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --system "You are a helpful coding assistant specializing in Python." \
    --message '{role: user, content: "How do I sort a list of dictionaries by key?"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      system="You are a helpful coding assistant specializing in Python.",
      messages=[
          {"role": "user", "content": "How do I sort a list of dictionaries by key?"}
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    system: "You are a helpful coding assistant specializing in Python.",
    messages: [{ role: "user", content: "How do I sort a list of dictionaries by key?" }]
  });

  console.log(message.content);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      System = "You are a helpful coding assistant specializing in Python.",
      Messages =
      [
          new() { Role = Role.User, Content = "How do I sort a list of dictionaries by key?" }
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	System: []anthropic.TextBlockParam{
  		{Text: "You are a helpful coding assistant specializing in Python."},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("How do I sort a list of dictionaries by key?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024)
      .system("You are a helpful coding assistant specializing in Python.")
      .addUserMessage("How do I sort a list of dictionaries by key?")
      .build();

  Message message = client.messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'How do I sort a list of dictionaries by key?']
      ],
      model: 'claude-opus-4-8',
      system: 'You are a helpful coding assistant specializing in Python.',
  );

  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    system: "You are a helpful coding assistant specializing in Python.",
    messages: [
      { role: "user", content: "How do I sort a list of dictionaries by key?" }
    ]
  )

  puts message.content
  ```
</CodeGroup>

### Prompting konteks panjang

Saat bekerja dengan dokumen besar atau input yang kaya data (20k+ token), strukturkan prompt Anda dengan hati-hati untuk mendapatkan hasil terbaik:

* **Letakkan data panjang di bagian atas:** Tempatkan dokumen dan input panjang Anda di dekat bagian atas prompt, di atas kueri, instruksi, dan contoh Anda. Ini meningkatkan kinerja di semua model.

  <Note>
    Kueri di bagian akhir dapat meningkatkan kualitas respons hingga 30 persen dalam pengujian, terutama dengan input multidokumen yang kompleks.
  </Note>

* **Strukturkan konten dokumen dan metadata dengan tag XML:** Saat menggunakan beberapa dokumen, bungkus setiap dokumen dalam tag `<document>` dengan subtag `<document_content>` dan `<source>` (serta metadata lainnya) untuk kejelasan.

  <Accordion title="Contoh struktur multidokumen">
    ```xml
    <documents>
      <document index="1">
        <source>annual_report_2023.pdf</source>
        <document_content>
          {{ANNUAL_REPORT}}
        </document_content>
      </document>
      <document index="2">
        <source>competitor_analysis_q2.xlsx</source>
        <document_content>
          {{COMPETITOR_ANALYSIS}}
        </document_content>
      </document>
    </documents>

    Analyze the annual report and competitor analysis. Identify strategic advantages and recommend Q3 focus areas.
    ```
  </Accordion>

* **Landaskan respons pada kutipan:** Untuk tugas dokumen panjang, minta Claude mengutip bagian-bagian relevan dari dokumen terlebih dahulu sebelum melaksanakan tugasnya. Ini membantu Claude fokus pada konten yang relevan dan mengabaikan sisa dokumen.

  <Accordion title="Contoh ekstraksi kutipan">
    ```xml
    You are an AI physician's assistant. Your task is to help doctors diagnose possible patient illnesses.

    <documents>
      <document index="1">
        <source>patient_symptoms.txt</source>
        <document_content>
          {{PATIENT_SYMPTOMS}}
        </document_content>
      </document>
      <document index="2">
        <source>patient_records.txt</source>
        <document_content>
          {{PATIENT_RECORDS}}
        </document_content>
      </document>
      <document index="3">
        <source>patient01_appt_history.txt</source>
        <document_content>
          {{PATIENT01_APPOINTMENT_HISTORY}}
        </document_content>
      </document>
    </documents>

    Find quotes from the patient records and appointment history that are relevant to diagnosing the patient's reported symptoms. Place these in <quotes> tags. Then, based on these quotes, list all information that would help the doctor diagnose the patient's symptoms. Place your diagnostic information in <info> tags.
    ```
  </Accordion>

### Pengetahuan diri model

Jika Anda ingin Claude mengidentifikasi dirinya dengan benar dalam aplikasi Anda atau menggunakan string API tertentu:

```text Sample prompt for model identity wrap
The assistant is Claude, created by Anthropic. The current model is Claude Opus 4.8.
```

Untuk aplikasi bertenaga LLM yang perlu menentukan string model:

```text Sample prompt for model string wrap
When an LLM is needed, please default to Claude Opus 4.8 unless the user requests
otherwise. The exact model string for Claude Opus 4.8 is claude-opus-4-8.
```

## Output dan pemformatan

### Gaya komunikasi dan verbositas

Model-model terbaru Claude memiliki gaya komunikasi yang lebih ringkas dan alami dibandingkan model-model sebelumnya:

* **Lebih langsung dan berlandaskan fakta:** Memberikan laporan kemajuan berbasis fakta alih-alih pembaruan yang memuji diri sendiri
* **Lebih percakapan:** Sedikit lebih lancar dan kolokial, tidak terlalu seperti mesin
* **Kurang bertele-tele:** Mungkin melewatkan ringkasan terperinci demi efisiensi kecuali diminta sebaliknya

Ini berarti Claude mungkin melewatkan ringkasan verbal setelah pemanggilan alat, langsung melompat ke tindakan berikutnya. Jika Anda lebih menyukai visibilitas yang lebih besar terhadap penalarannya:

```text Sample prompt wrap
After completing a task that involves tool use, provide a quick summary of the work you've done.
```

### Kontrol format respons

Ada beberapa cara yang sangat efektif untuk mengarahkan pemformatan output:

1. **Beri tahu Claude apa yang harus dilakukan alih-alih apa yang tidak boleh dilakukan**

   * Alih-alih: "Jangan gunakan markdown dalam respons Anda"
   * Coba: "Respons Anda harus terdiri dari paragraf prosa yang mengalir dengan lancar."

2. **Gunakan indikator format XML**

   * Coba: "Tulis bagian prosa dari respons Anda dalam tag \<smoothly\_flowing\_prose\_paragraphs>."

3. **Cocokkan gaya prompt Anda dengan output yang diinginkan**

   Gaya pemformatan yang digunakan dalam prompt Anda dapat memengaruhi gaya respons Claude. Jika Anda masih mengalami masalah keterarahan dengan pemformatan output, coba cocokkan gaya prompt Anda dengan gaya output yang Anda inginkan sedekat mungkin. Misalnya, menghapus markdown dari prompt Anda dapat mengurangi volume markdown dalam output.

4. **Gunakan prompt terperinci untuk preferensi pemformatan tertentu**

   Untuk kontrol lebih besar atas penggunaan markdown dan pemformatan, berikan panduan eksplisit:

````text Sample prompt to minimize markdown wrap
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any long-form
content, write in clear, flowing prose using complete paragraphs and sentences. Use
standard paragraph breaks for organization and reserve markdown primarily for `inline
code`, code blocks (```...```), and simple headings (## and ###). Avoid using **bold**
and *italics*.

DO NOT use ordered lists (1. ...) or unordered lists (*) unless: a) you're presenting
truly discrete items where a list format is the best option, or b) the user explicitly
requests a list or ranking

Instead of listing items with bullets or numbers, incorporate them naturally into
sentences. This guidance applies especially to technical writing. Using prose instead of
excessive formatting will improve user satisfaction. NEVER output a series of overly
short bullet points.

Your goal is readable, flowing text that guides the reader naturally through ideas
rather than fragmenting information into isolated points.
</avoid_excessive_markdown_and_bullet_points>
````

### Output LaTeX

Model-model terbaru Claude secara default menggunakan LaTeX untuk ekspresi matematika, persamaan, dan penjelasan teknis. Jika Anda lebih menyukai teks biasa, tambahkan instruksi berikut ke prompt Anda:

```text Sample prompt wrap
Format your response in plain text only. Do not use LaTeX, MathJax, or any markup
notation such as \( \), $, or \frac{}{}. Write all math expressions using standard text
characters (e.g., "/" for division, "*" for multiplication, and "^" for exponents).
```

### Pembuatan dokumen

Model-model terbaru Claude membuat presentasi, animasi, dan dokumen visual dengan kepatuhan instruksi yang kuat, dan biasanya menghasilkan output yang dapat digunakan pada percobaan pertama.

Untuk hasil terbaik dengan pembuatan dokumen:

```text Sample prompt wrap
Create a professional presentation on [topic]. Include thoughtful design elements,
visual hierarchy, and engaging animations where appropriate.
```

### Bermigrasi dari respons yang diisi sebelumnya (prefilled)

Mulai dari model Claude 4.6 dan [Claude Mythos Preview](https://anthropic.com/glasswing), respons yang diisi sebelumnya atau prefilled (memberikan pesan asisten parsial untuk dilanjutkan oleh Claude) pada giliran asisten terakhir tidak lagi didukung. Permintaan dengan pesan asisten yang diisi sebelumnya ke model-model ini mengembalikan error 400. Kecerdasan model dan kepatuhan instruksi telah berkembang sedemikian rupa sehingga sebagian besar kasus penggunaan prefill tidak lagi memerlukannya. Model-model sebelumnya tetap mendukung prefill, dan menambahkan pesan asisten di tempat lain dalam percakapan tidak terpengaruh.

Berikut adalah skenario prefill yang umum dan cara bermigrasi darinya:

<Accordion title="Mengontrol pemformatan output">
  Prefill telah digunakan untuk memaksa format output tertentu seperti JSON/YAML, klasifikasi, dan pola serupa di mana prefill membatasi Claude pada struktur tertentu.

  **Migrasi:** Fitur [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dirancang khusus untuk membatasi respons Claude agar mengikuti skema yang diberikan. Coba minta model untuk menyesuaikan dengan struktur output Anda terlebih dahulu, karena model-model yang lebih baru dapat mencocokkan skema kompleks dengan andal ketika diminta, terutama jika diimplementasikan dengan percobaan ulang. Untuk tugas klasifikasi, gunakan alat dengan field enum yang berisi label valid Anda atau structured outputs.
</Accordion>

<Accordion title="Menghilangkan pembukaan">
  Prefill seperti `Here is the requested summary:\n` digunakan untuk melewati teks pengantar.

  **Migrasi:** Gunakan instruksi langsung dalam prompt sistem: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc." Sebagai alternatif, arahkan model untuk menghasilkan output di dalam tag XML, gunakan structured outputs, atau gunakan pemanggilan alat. Jika sesekali pembukaan masih lolos, hapus dalam pasca-pemrosesan.
</Accordion>

<Accordion title="Menghindari penolakan yang tidak tepat">
  Prefill digunakan untuk mengarahkan model agar menghindari penolakan yang tidak perlu.

  **Migrasi:** Claude sekarang jauh lebih baik dalam melakukan penolakan yang tepat. Prompting yang jelas dalam pesan `user` tanpa prefill seharusnya sudah cukup.
</Accordion>

<Accordion title="Kelanjutan">
  Prefill digunakan untuk melanjutkan penyelesaian parsial, melanjutkan respons yang terputus, atau melanjutkan dari titik di mana generasi sebelumnya berhenti.

  **Migrasi:** Pindahkan kelanjutan ke pesan pengguna, dan sertakan teks terakhir dari respons yang terputus: "Your previous response was interrupted and ended with \`\[previous\_response]\`. Continue from where you left off." Jika ini adalah bagian dari penanganan error atau penanganan respons tidak lengkap dan tidak ada penalti UX, coba ulangi permintaan.
</Accordion>

<Accordion title="Hidrasi konteks dan konsistensi peran">
  Prefill digunakan untuk secara berkala memastikan konteks yang disegarkan atau disuntikkan.

  **Migrasi:** Untuk percakapan yang sangat panjang, suntikkan apa yang sebelumnya merupakan pengingat asisten yang diisi sebelumnya ke dalam giliran pengguna. Jika hidrasi konteks adalah bagian dari sistem agentik yang lebih kompleks, pertimbangkan untuk melakukan hidrasi melalui alat (ekspos atau dorong penggunaan alat yang berisi konteks berdasarkan heuristik seperti jumlah giliran) atau selama [pemadatan konteks](/docs/id/build-with-claude/compaction).
</Accordion>

## Penggunaan alat

### Penggunaan alat

Model-model terbaru Claude dilatih untuk kepatuhan instruksi yang presisi dan mendapat manfaat dari arahan eksplisit untuk menggunakan alat tertentu. Jika Anda mengatakan "bisakah kamu menyarankan beberapa perubahan," Claude terkadang akan memberikan saran alih-alih mengimplementasikannya, meskipun membuat perubahan mungkin adalah yang Anda maksudkan. Untuk cara mendefinisikan alat dan memecahkan masalah pemicu alat, lihat [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview).

Agar Claude mengambil tindakan, bersikaplah lebih eksplisit:

<Accordion title="Contoh: Instruksi eksplisit">
  **Kurang efektif (Claude hanya akan menyarankan):**

  ```text wrap
  Can you suggest some changes to improve this function?
  ```

  **Lebih efektif (Claude akan membuat perubahan):**

  ```text wrap
  Change this function to improve its performance.
  ```

  Atau:

  ```text wrap
  Make these edits to the authentication flow.
  ```
</Accordion>

Untuk membuat Claude lebih proaktif dalam mengambil tindakan secara default, Anda dapat menambahkan ini ke prompt sistem Anda:

```text Sample prompt for proactive action wrap
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is
unclear, infer the most useful likely action and proceed, using tools to discover any
missing details instead of guessing. Try to infer the user's intent about whether a tool
call (e.g., file edit or read) is intended or not, and act accordingly.
</default_to_action>
```

Di sisi lain, jika Anda ingin model lebih ragu-ragu secara default, tidak terlalu cenderung langsung melompat ke implementasi, dan hanya mengambil tindakan jika diminta, Anda dapat mengarahkan perilaku ini dengan prompt seperti berikut:

```text Sample prompt for conservative action wrap
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed to make
changes. When the user's intent is ambiguous, default to providing information, doing
research, and providing recommendations rather than taking action. Only proceed with
edits, modifications, or implementations when the user explicitly requests them.
</do_not_act_before_instructions>
```

Claude Opus 4.5 dan Claude Opus 4.6 juga lebih responsif terhadap prompt sistem dibandingkan model-model sebelumnya. Jika prompt Anda dirancang untuk mengurangi pemicu yang kurang (undertriggering) pada alat atau skill, model-model ini sekarang mungkin memicu secara berlebihan. Solusinya adalah mengurangi bahasa yang agresif. Di mana Anda mungkin mengatakan "CRITICAL: You MUST use this tool when...", Anda dapat menggunakan prompting yang lebih normal seperti "Use this tool when...".

### Optimalkan pemanggilan alat paralel

Model-model terbaru Claude menjalankan pemanggilan alat independen secara paralel. Model-model ini akan:

* Menjalankan beberapa pencarian spekulatif selama riset
* Membaca beberapa file sekaligus untuk membangun konteks lebih cepat
* Menjalankan perintah bash secara paralel (yang bahkan dapat menjadi hambatan kinerja sistem)

Perilaku ini dapat diarahkan. Meskipun model memiliki tingkat keberhasilan yang tinggi dalam pemanggilan alat paralel tanpa prompting, Anda dapat meningkatkannya hingga \~100% atau menyesuaikan tingkat agresivitasnya:

```text Sample prompt for maximum parallel efficiency wrap
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool
calls, make all of the independent tool calls in parallel. Prioritize calling tools
simultaneously whenever the actions can be done in parallel rather than sequentially.
For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into
context at the same time. Maximize use of parallel tool calls where possible to increase
speed and efficiency. However, if some tool calls depend on previous calls to inform
dependent values like the parameters, do NOT call these tools in parallel and instead
call them sequentially. Never use placeholders or guess missing parameters in tool
calls.
</use_parallel_tool_calls>
```

```text Sample prompt to reduce parallel execution wrap
Execute operations sequentially with brief pauses between each step to ensure stability.
```

## Pemikiran dan penalaran

### Berpikir berlebihan dan ketelitian yang berlebihan

Claude Opus 4.6 melakukan lebih banyak eksplorasi awal dibandingkan model-model sebelumnya, terutama pada pengaturan [`effort`](/docs/id/build-with-claude/effort) yang lebih tinggi. Pekerjaan awal ini sering membantu mengoptimalkan hasil akhir, tetapi model mungkin mengumpulkan konteks yang ekstensif atau mengejar beberapa alur riset tanpa diminta. Jika prompt Anda sebelumnya mendorong model untuk lebih teliti, Anda harus menyesuaikan panduan tersebut untuk Claude Opus 4.6:

* **Ganti default menyeluruh dengan instruksi yang lebih terarah.** Alih-alih "Default to using \[tool]," tambahkan panduan seperti "Use \[tool] when it would enhance your understanding of the problem."
* **Hapus prompting yang berlebihan.** Alat yang kurang terpicu pada model-model sebelumnya kemungkinan akan terpicu dengan tepat sekarang. Instruksi seperti "If in doubt, use \[tool]" akan menyebabkan pemicu yang berlebihan.
* **Gunakan effort sebagai cadangan.** Jika Claude terus bersikap terlalu agresif, gunakan pengaturan yang lebih rendah untuk `effort`.

Dalam beberapa kasus, Claude Opus 4.6 mungkin berpikir secara ekstensif, yang dapat meningkatkan token pemikiran dan memperlambat respons. Jika perilaku ini tidak diinginkan, Anda dapat menambahkan instruksi eksplisit untuk membatasi penalarannya, atau Anda dapat menurunkan pengaturan `effort` untuk mengurangi pemikiran dan penggunaan token secara keseluruhan.

```text Sample prompt wrap
When you're deciding how to approach a problem, choose an approach and commit to it.
Avoid revisiting decisions unless you encounter new information that directly
contradicts your reasoning. If you're weighing two approaches, pick one and see it
through. You can always course-correct later if the chosen approach fails.
```

Jika Anda memerlukan batas atas yang tegas pada biaya pemikiran, pemikiran diperpanjang dengan batas `budget_tokens` masih berfungsi pada Opus 4.6 dan Sonnet 4.6 tetapi sudah usang (deprecated). Pada Claude Opus 4.7 dan model-model setelahnya, serta pada Claude Fable 5 dan Claude Mythos 5, menetapkan `budget_tokens` mengembalikan error 400. Lebih baik menurunkan pengaturan [effort](/docs/id/build-with-claude/effort) atau menggunakan `max_tokens` sebagai batas tegas dengan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking).

### Manfaatkan kemampuan pemikiran & pemikiran tersisip

Model-model terbaru Claude menawarkan kemampuan pemikiran yang dapat sangat membantu untuk tugas-tugas yang melibatkan refleksi setelah penggunaan alat atau penalaran multilangkah yang kompleks. Anda dapat memandu pemikiran awal atau tersisipnya untuk hasil yang lebih baik.

Claude Opus 4.6, Claude Opus 4.7, Claude Opus 4.8, dan Claude Sonnet 4.6 menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana Claude secara dinamis memutuskan kapan dan seberapa banyak berpikir. Pada Claude Fable 5 dan Claude Mythos 5, pemikiran selalu aktif dan pemikiran adaptif adalah satu-satunya mode. Claude mengkalibrasi pemikirannya berdasarkan dua faktor: parameter `effort` dan kompleksitas kueri. Effort yang lebih tinggi memunculkan lebih banyak pemikiran, dan kueri yang lebih kompleks melakukan hal yang sama. Pada kueri yang lebih mudah yang tidak memerlukan pemikiran, model merespons secara langsung. Dalam evaluasi internal, pemikiran adaptif secara andal menghasilkan kinerja yang lebih baik daripada pemikiran diperpanjang. Pertimbangkan untuk beralih ke pemikiran adaptif untuk mendapatkan respons yang paling cerdas.

Gunakan pemikiran adaptif untuk beban kerja yang memerlukan perilaku agentik seperti penggunaan alat multilangkah, tugas pengkodean yang kompleks, dan loop agen jangka panjang. Model-model yang lebih lama menggunakan [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) manual dengan `budget_tokens`; lihat [tabel model yang didukung](/docs/id/build-with-claude/extended-thinking#supported-models) untuk mengetahui mode mana yang diterima setiap model.

Anda dapat memandu perilaku pemikiran Claude:

```text Example prompt wrap
After receiving tool results, carefully reflect on their quality and determine optimal
next steps before proceeding. Use your thinking to plan and iterate based on this new
information, and then take the best next action.
```

Perilaku pemicu untuk pemikiran adaptif dapat diatur melalui prompt. Jika Anda menemukan model berpikir lebih sering dari yang Anda inginkan, yang dapat terjadi dengan prompt sistem yang besar atau kompleks, tambahkan panduan untuk mengarahkannya:

```text Sample prompt wrap
Extended thinking adds latency and should only be used when it will meaningfully improve
answer quality - typically for problems that require multistep reasoning. When in
doubt, respond directly.
```

Jika Anda bermigrasi dari [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) dengan `budget_tokens`, ganti konfigurasi pemikiran Anda dan pindahkan kontrol anggaran ke `effort`. Contoh-contoh berikut menunjukkan permintaan yang sama sebelum dan sesudah migrasi (lihat [effort](/docs/id/build-with-claude/effort) untuk tingkat yang tersedia dan ketersediaan per model):

<CodeGroup>
  ```bash cURL
  # Sebelum: pemikiran diperpanjang dengan budget manual (model lama)
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 16000,
      "thinking": {"type": "enabled", "budget_tokens": 10000},
      "messages": [
        {"role": "user", "content": "..."}
      ]
    }'

  # Sesudah: pemikiran adaptif dengan effort (model saat ini)
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 16000,
      "thinking": {"type": "adaptive"},
      "output_config": {"effort": "high"},
      "messages": [
        {"role": "user", "content": "..."}
      ]
    }'
  ```

  ```bash CLI
  # Sebelum: pemikiran diperpanjang dengan budget manual (model lama)
  ant messages create <<'YAML'
  model: claude-sonnet-4-5-20250929
  max_tokens: 16000
  thinking:
    type: enabled
    budget_tokens: 10000
  messages:
    - role: user
      content: "..."
  YAML

  # Sesudah: pemikiran adaptif dengan effort (model saat ini)
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 16000
  thinking:
    type: adaptive
  output_config:
    effort: high
  messages:
    - role: user
      content: "..."
  YAML
  ```

  ```python Python
  # Sebelum: pemikiran diperpanjang dengan anggaran manual (model lama)
  client.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=16000,
      thinking={"type": "enabled", "budget_tokens": 10000},
      messages=[{"role": "user", "content": "..."}],
  )

  # Sesudah: pemikiran adaptif dengan effort (model saat ini)
  client.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      thinking={"type": "adaptive"},
      output_config={"effort": "high"},
      messages=[{"role": "user", "content": "..."}],
  )
  ```

  ```typescript TypeScript
  // Sebelum: pemikiran diperpanjang dengan budget manual (model lama)
  await client.messages.create({
    model: "claude-sonnet-4-5-20250929",
    max_tokens: 16000,
    thinking: { type: "enabled", budget_tokens: 10000 },
    messages: [{ role: "user", content: "..." }]
  });

  // Sesudah: pemikiran adaptif dengan effort (model saat ini)
  await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    thinking: { type: "adaptive" },
    output_config: { effort: "high" },
    messages: [{ role: "user", content: "..." }]
  });
  ```

  ```csharp C#
  // Sebelum: pemikiran diperpanjang dengan budget manual (model lama)
  await client.Messages.Create(new MessageCreateParams
  {
      Model = "claude-sonnet-4-5-20250929",
      MaxTokens = 16000,
      Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
      Messages = [new() { Role = Role.User, Content = "..." }]
  });

  // Sesudah: pemikiran adaptif dengan effort (model saat ini)
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigAdaptive(),
      OutputConfig = new OutputConfig { Effort = Effort.High },
      Messages = [new() { Role = Role.User, Content = "..." }]
  });
  ```

  ```go Go
  // Sebelum: pemikiran diperpanjang dengan budget manual (model lama)
  client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     "claude-sonnet-4-5-20250929",
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfEnabled: &anthropic.ThinkingConfigEnabledParam{BudgetTokens: 10000},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
  	},
  })

  // Sesudah: pemikiran adaptif dengan effort (model saat ini)
  client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
  	},
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortHigh,
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
  	},
  })
  ```

  ```java Java
  // Sebelum: pemikiran diperpanjang dengan budget manual (model lama)
  client.messages().create(MessageCreateParams.builder()
      .model("claude-sonnet-4-5-20250929")
      .maxTokens(16000L)
      .thinking(ThinkingConfigEnabled.builder().budgetTokens(10000L).build())
      .addUserMessage("...")
      .build());

  // Sesudah: pemikiran adaptif dengan effort (model saat ini)
  client.messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(16000L)
      .thinking(ThinkingConfigAdaptive.builder().build())
      .outputConfig(OutputConfig.builder()
          .effort(OutputConfig.Effort.HIGH)
          .build())
      .addUserMessage("...")
      .build());
  ```

  ```php PHP
  // Sebelum: pemikiran diperpanjang dengan budget manual (model lama)
  $client->messages->create(
      model: 'claude-sonnet-4-5-20250929',
      maxTokens: 16000,
      thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
      messages: [['role' => 'user', 'content' => '...']],
  );

  // Sesudah: pemikiran adaptif dengan effort (model saat ini)
  $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 16000,
      thinking: ['type' => 'adaptive'],
      outputConfig: ['effort' => 'high'],
      messages: [['role' => 'user', 'content' => '...']],
  );
  ```

  ```ruby Ruby
  # Sebelum: pemikiran diperpanjang dengan anggaran manual (model lama)
  client.messages.create(
    model: "claude-sonnet-4-5-20250929",
    max_tokens: 16000,
    thinking: { type: "enabled", budget_tokens: 10000 },
    messages: [{ role: "user", content: "..." }]
  )

  # Sesudah: pemikiran adaptif dengan effort (model saat ini)
  client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16000,
    thinking: { type: "adaptive" },
    output_config: { effort: "high" },
    messages: [{ role: "user", content: "..." }]
  )
  ```
</CodeGroup>

Jika Anda tidak menggunakan pemikiran diperpanjang, tidak ada perubahan yang diperlukan. Pada Claude Opus 4.6 hingga Claude Opus 4.8 dan Claude Sonnet 4.6, pemikiran nonaktif ketika Anda menghilangkan parameter `thinking`. Pada Claude Fable 5 dan Claude Mythos 5, pemikiran selalu aktif, terlepas dari apakah Anda menetapkan parameter `thinking` atau tidak.

* **Utamakan instruksi umum daripada langkah-langkah preskriptif.** Prompt seperti "think thoroughly" sering menghasilkan penalaran yang lebih baik daripada rencana langkah demi langkah yang ditulis tangan. Penalaran Claude sering melampaui apa yang akan ditentukan oleh manusia.
* **Contoh multishot bekerja dengan pemikiran.** Gunakan tag `<thinking>` di dalam contoh few-shot Anda untuk menunjukkan pola penalaran kepada Claude. Claude akan menggeneralisasi gaya tersebut ke blok pemikiran diperpanjangnya sendiri.
* **Prompting chain-of-thought (CoT) manual sebagai cadangan.** Ketika pemikiran nonaktif, Anda masih dapat mendorong penalaran langkah demi langkah dengan meminta Claude memikirkan masalahnya. Gunakan tag terstruktur seperti `<thinking>` dan `<answer>` untuk memisahkan penalaran dari output akhir dengan rapi.
* **Minta Claude memeriksa dirinya sendiri.** Tambahkan sesuatu seperti "Before you finish, verify your answer against \[test criteria]." Ini menangkap kesalahan dengan andal, terutama untuk pengkodean dan matematika.

<Note>
  Ketika pemikiran diperpanjang dinonaktifkan, Claude Opus 4.5 sangat sensitif terhadap kata "think" dan variannya. Pertimbangkan untuk menggunakan alternatif seperti "consider," "evaluate," atau "reason through" dalam kasus-kasus tersebut.
</Note>

<Info>
  Untuk informasi lebih lanjut tentang kemampuan pemikiran, lihat [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) dan [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking).
</Info>

## Sistem agentik

### Penalaran jangka panjang dan pelacakan status

Model-model terbaru Claude menangani tugas penalaran jangka panjang dengan pelacakan status yang kuat. Claude mempertahankan orientasi di sepanjang sesi yang diperpanjang dengan berfokus pada kemajuan bertahap, membuat kemajuan yang stabil pada beberapa hal sekaligus alih-alih mencoba semuanya sekaligus. Kemampuan ini terutama muncul di beberapa jendela konteks atau iterasi tugas, di mana Claude dapat mengerjakan tugas yang kompleks, menyimpan status, dan melanjutkan dengan jendela konteks yang baru.

#### Kesadaran konteks dan alur kerja multijendela

Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, dan Claude Haiku 4.5 memiliki fitur [kesadaran konteks](/docs/id/build-with-claude/context-windows#context-awareness), yang memungkinkan model melacak sisa jendela konteksnya (yaitu, "anggaran token"-nya) sepanjang percakapan. Ini memungkinkan Claude untuk menjalankan tugas dan mengelola konteks dengan lebih efektif dengan memahami berapa banyak ruang yang dimilikinya untuk bekerja.

**Mengelola batas konteks:**

Jika Anda menggunakan Claude dalam harness agen yang memadatkan konteks atau memungkinkan penyimpanan konteks ke file eksternal (seperti di Claude Code), pertimbangkan untuk menambahkan informasi ini ke prompt Anda agar Claude dapat berperilaku sesuai. Jika tidak, Claude terkadang secara alami mencoba menyelesaikan pekerjaan saat mendekati batas konteks. Berikut adalah contoh prompt:

```text Sample prompt wrap
Your context window will be automatically compacted as it approaches its limit, allowing
you to continue working indefinitely from where you left off. Therefore, do not stop
tasks early due to token budget concerns. As you approach your token budget limit, save
your current progress and state to memory before the context window refreshes. Always be
as persistent and autonomous as possible and complete tasks fully, even if the end of
your budget is approaching. Never artificially stop any task early regardless of the
context remaining.
```

[Alat memori](/docs/id/agents-and-tools/tool-use/memory-tool) berpasangan dengan baik dengan kesadaran konteks untuk mengelola transisi konteks.

#### Alur kerja di beberapa jendela konteks

Untuk tugas yang mencakup beberapa jendela konteks:

1. **Gunakan prompt yang berbeda untuk jendela konteks pertama:** Gunakan jendela konteks pertama untuk menyiapkan kerangka kerja (menulis pengujian, membuat skrip penyiapan), lalu gunakan jendela konteks berikutnya untuk mengiterasi daftar tugas.

2. **Minta model menulis pengujian dalam format terstruktur:** Minta Claude membuat pengujian sebelum memulai pekerjaan dan melacaknya dalam format terstruktur (misalnya, `tests.json`). Ini menghasilkan kemampuan jangka panjang yang lebih baik untuk beriterasi. Ingatkan Claude tentang pentingnya pengujian: "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

3. **Siapkan alat kenyamanan:** Dorong Claude untuk membuat skrip penyiapan (misalnya, `init.sh`) untuk memulai server, menjalankan rangkaian pengujian, dan linter dengan lancar. Ini mencegah pekerjaan berulang saat melanjutkan dari jendela konteks yang baru.

4. **Memulai dari awal versus pemadatan:** Ketika jendela konteks dibersihkan, pertimbangkan untuk memulai dengan jendela konteks yang benar-benar baru alih-alih menggunakan pemadatan. Model-model terbaru Claude sangat efektif dalam menemukan status dari sistem file lokal. Dalam beberapa kasus, Anda mungkin ingin memanfaatkan ini daripada pemadatan. Bersikaplah preskriptif tentang bagaimana model harus memulai:

   * "Call pwd; you can only read and write files in this directory."
   * "Review progress.txt, tests.json, and the git logs."
   * "Manually run through a fundamental integration test before moving on to implementing new features."

5. **Sediakan alat verifikasi:** Seiring bertambahnya panjang tugas otonom, Claude perlu memverifikasi kebenaran tanpa umpan balik manusia yang berkelanjutan. Alat seperti server Playwright MCP atau kemampuan penggunaan komputer untuk menguji UI sangat membantu.

6. **Dorong penggunaan konteks secara penuh:** Beri prompt kepada Claude untuk menyelesaikan komponen secara efisien sebelum melanjutkan:

```text Sample prompt wrap
This is a very long task, so it may be beneficial to plan out your work clearly. It's
encouraged to spend your entire output context working on the task - just make sure you
don't run out of context with significant uncommitted work. Continue working
systematically until you have completed this task.
```

#### Praktik terbaik manajemen status

* **Gunakan format terstruktur untuk data status:** Saat melacak informasi terstruktur (seperti hasil pengujian atau status tugas), gunakan JSON atau format terstruktur lainnya untuk membantu Claude memahami persyaratan skema.
* **Gunakan teks tidak terstruktur untuk catatan kemajuan:** Catatan kemajuan bentuk bebas bekerja dengan baik untuk melacak kemajuan umum dan konteks.
* **Gunakan git untuk pelacakan status:** Git menyediakan log tentang apa yang telah dilakukan dan titik pemeriksaan yang dapat dipulihkan. Model-model terbaru Claude berkinerja sangat baik dalam menggunakan git untuk melacak status di beberapa sesi.
* **Tekankan kemajuan bertahap:** Secara eksplisit minta Claude untuk melacak kemajuannya dan fokus pada pekerjaan bertahap.

<Accordion title="Contoh: Pelacakan status">
  ```json
  // Structured state file (tests.json)
  {
    "tests": [
      { "id": 1, "name": "authentication_flow", "status": "passing" },
      { "id": 2, "name": "user_management", "status": "failing" },
      { "id": 3, "name": "api_endpoints", "status": "not_started" }
    ],
    "total": 200,
    "passing": 150,
    "failing": 25,
    "not_started": 25
  }
  ```

  ```text wrap
  // Progress notes (progress.txt)
  Session 3 progress:
  - Fixed authentication token validation
  - Updated user model to handle edge cases
  - Next: investigate user_management test failures (test #2)
  - Note: Do not remove tests as this could lead to missing functionality
  ```
</Accordion>

### Menyeimbangkan otonomi dan keamanan

Tanpa panduan, Claude Opus 4.6 mungkin mengambil tindakan yang sulit dibalikkan atau memengaruhi sistem bersama, seperti menghapus file, melakukan force-push, atau memposting ke layanan eksternal. Jika Anda ingin Claude Opus 4.6 mengonfirmasi sebelum mengambil tindakan yang berpotensi berisiko, tambahkan panduan ke prompt Anda:

```text Sample prompt wrap
Consider the reversibility and potential impact of your actions. You are encouraged to
take local, reversible actions like editing files or running tests, but for actions that
are hard to reverse, affect shared systems, or could be destructive, ask the user before
proceeding.

Examples of actions that warrant confirmation:
- Destructive operations: deleting files or branches, dropping database tables, rm -rf
- Hard to reverse operations: git push --force, git reset --hard, amending published commits
- Operations visible to others: pushing code, commenting on PRs/issues, sending
messages, modifying shared infrastructure

When encountering obstacles, do not use destructive actions as a shortcut. For example,
don't bypass safety checks (e.g. --no-verify) or discard unfamiliar files that may be
in-progress work.
```

### Riset dan pengumpulan informasi

Model-model terbaru Claude dapat menemukan dan mensintesis informasi dari berbagai sumber secara efektif. Untuk hasil riset yang optimal:

1. **Berikan kriteria keberhasilan yang jelas:** Tentukan apa yang merupakan jawaban yang berhasil untuk pertanyaan riset Anda.

2. **Dorong verifikasi sumber:** Minta Claude untuk memverifikasi informasi di berbagai sumber.

3. **Untuk tugas riset yang kompleks, gunakan pendekatan terstruktur:**

```text Sample prompt for complex research wrap
Search for this information in a structured way. As you gather data, develop several
competing hypotheses. Track your confidence levels in your progress notes to improve
calibration. Regularly self-critique your approach and plan. Update a hypothesis tree or
research notes file to persist information and provide transparency. Break down this
complex research task systematically.
```

Pendekatan terstruktur ini membantu Claude bekerja melalui korpus besar secara metodis dan mengkritik temuannya secara iteratif.

### Orkestrasi subagen

Model-model terbaru Claude mengorkestrasi subagen secara native. Model-model ini dapat mengenali kapan tugas akan mendapat manfaat dari mendelegasikan pekerjaan ke subagen khusus dan melakukannya secara proaktif tanpa memerlukan instruksi eksplisit.

Untuk memanfaatkan perilaku ini:

1. **Pastikan alat subagen terdefinisi dengan baik:** Sediakan alat subagen dan deskripsikan dalam definisi alat.
2. **Biarkan Claude mengorkestrasi secara alami:** Claude akan mendelegasikan dengan tepat tanpa instruksi eksplisit.
3. **Waspadai penggunaan berlebihan:** Claude Opus 4.6 memiliki kecenderungan kuat terhadap subagen dan mungkin memunculkannya dalam situasi di mana pendekatan yang lebih sederhana dan langsung sudah cukup. Misalnya, model mungkin memunculkan subagen untuk eksplorasi kode ketika pemanggilan grep langsung lebih cepat dan memadai.

Jika Anda melihat penggunaan subagen yang berlebihan, tambahkan panduan eksplisit tentang kapan subagen diperlukan dan tidak diperlukan:

```text Sample prompt for subagent usage wrap
Use subagents when tasks can run in parallel, require isolated context, or involve
independent workstreams that don't need to share state. For simple tasks, sequential
operations, single-file edits, or tasks where you need to maintain context across steps,
work directly rather than delegating.
```

### Rantai prompt yang kompleks

Dengan pemikiran adaptif dan orkestrasi subagen, Claude menangani sebagian besar penalaran multilangkah secara internal. Perantaian prompt eksplisit (memecah tugas menjadi pemanggilan API berurutan) masih berguna ketika Anda perlu memeriksa output perantara atau menerapkan struktur pipeline tertentu.

Pola perantaian yang paling umum adalah **koreksi diri:** hasilkan draf → minta Claude meninjaunya terhadap kriteria → minta Claude menyempurnakannya berdasarkan tinjauan. Setiap langkah adalah pemanggilan API terpisah sehingga Anda dapat mencatat, mengevaluasi, atau bercabang di titik mana pun.

### Kurangi pembuatan file dalam pengkodean agentik

Model-model terbaru Claude terkadang membuat file baru untuk tujuan pengujian dan iterasi, terutama saat bekerja dengan kode. Pendekatan ini memungkinkan Claude menggunakan file, terutama skrip Python, sebagai 'papan coret sementara' sebelum menyimpan output akhirnya. Menggunakan file sementara dapat meningkatkan hasil terutama untuk kasus penggunaan pengkodean agentik.

Jika Anda lebih suka meminimalkan pembuatan file baru bersih, Anda dapat menginstruksikan Claude untuk membersihkan setelahnya:

```text Sample prompt wrap
If you create any temporary new files, scripts, or helper files for iteration, clean up
these files by removing them at the end of the task.
```

### Terlalu bersemangat

Claude Opus 4.5 dan Claude Opus 4.6 memiliki kecenderungan untuk melakukan rekayasa berlebihan dengan membuat file tambahan, menambahkan abstraksi yang tidak perlu, atau membangun fleksibilitas yang tidak diminta. Jika Anda melihat perilaku yang tidak diinginkan ini, tambahkan panduan spesifik untuk menjaga solusi tetap minimal.

Misalnya:

```text Sample prompt to minimize overengineering wrap
Avoid over-engineering. Only make changes that are directly requested or clearly
necessary. Keep solutions simple and focused:

- Scope: Don't add features, refactor code, or make "improvements" beyond what was
asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need
extra configurability.

- Documentation: Don't add docstrings, comments, or type annotations to code you didn't
change. Only add comments where the logic isn't self-evident.

- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios
that can't happen. Trust internal code and framework guarantees. Only validate at system
boundaries (user input, external APIs).

- Abstractions: Don't create helpers, utilities, or abstractions for one-time
operations. Don't design for hypothetical future requirements. The right amount of
complexity is the minimum needed for the current task.
```

### Hindari fokus pada lulus pengujian dan hardcoding

Claude terkadang dapat terlalu fokus pada membuat pengujian lulus dengan mengorbankan solusi yang lebih umum, atau mungkin menggunakan solusi sementara seperti skrip pembantu untuk refactoring yang kompleks alih-alih menggunakan alat standar secara langsung. Untuk mencegah perilaku ini dan mendapatkan solusi yang dapat digeneralisasi:

```text Sample prompt wrap
Please write a high-quality, general-purpose solution using the standard tools
available. Do not create helper scripts or workarounds to accomplish the task more
efficiently. Implement a solution that works correctly for all valid inputs, not just
the test cases. Do not hard-code values or create solutions that only work for specific
test inputs. Instead, implement the actual logic that solves the problem generally.

Focus on understanding the problem requirements and implementing the correct algorithm.
Tests are there to verify correctness, not to define the solution. Provide a principled
implementation that follows best practices and software design principles.

If the task is unreasonable or infeasible, or if any of the tests are incorrect, please
inform me rather than working around them. The solution should be robust, maintainable,
and extendable.
```

### Meminimalkan halusinasi dalam pengkodean agentik

Model-model terbaru Claude kurang rentan terhadap halusinasi dan memberikan jawaban yang lebih akurat, berlandaskan fakta, dan cerdas berdasarkan kode. Untuk lebih mendorong perilaku ini dan meminimalkan halusinasi:

```text Sample prompt wrap
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file,
you MUST read the file before answering. Make sure to investigate and read relevant
files BEFORE answering questions about the codebase. Never make any claims about code
before investigating unless you are certain of the correct answer - give grounded and
hallucination-free answers.
</investigate_before_answering>
```

## Tips spesifik kemampuan

### Kemampuan visi yang ditingkatkan

Claude Opus 4.5 dan Claude Opus 4.6 memiliki kemampuan visi yang ditingkatkan dibandingkan model-model Claude sebelumnya. Mereka berkinerja lebih baik pada tugas pemrosesan gambar dan ekstraksi data, terutama ketika ada beberapa gambar dalam konteks. Peningkatan ini juga berlaku untuk penggunaan komputer, di mana model dapat menafsirkan tangkapan layar dan elemen UI dengan lebih andal. Anda juga dapat menggunakan model-model ini untuk menganalisis video dengan memecahnya menjadi frame.

Salah satu teknik yang terbukti efektif untuk lebih meningkatkan kinerja adalah memberikan Claude alat pemotong (crop tool) atau [agent skill](/docs/id/agents-and-tools/agent-skills/overview). Pengujian telah menunjukkan peningkatan yang konsisten pada evaluasi gambar ketika Claude dapat "memperbesar" wilayah yang relevan dari sebuah gambar. Anthropic telah membuat [resep untuk alat pemotong](https://platform.claude.com/cookbook/multimodal-crop-tool).

### Desain frontend

Claude Opus 4.5 dan Claude Opus 4.6 membangun aplikasi web dunia nyata yang kompleks dengan desain frontend yang kuat. Namun, tanpa panduan, model dapat secara default menggunakan pola generik yang menciptakan apa yang disebut pengguna sebagai estetika "AI slop". Untuk membuat frontend yang khas dan kreatif yang mengejutkan dan menyenangkan:

<Tip>
  Untuk panduan terperinci tentang meningkatkan desain frontend, lihat postingan blog tentang [meningkatkan desain frontend melalui skill](https://www.claude.com/blog/improving-frontend-design-through-skills).
</Tip>

Untuk pekerjaan desain frontend di luar API, [Claude Design](https://support.claude.com/en/articles/14604416-get-started-with-claude-design) menyediakan kanvas dan alat desain di mana Claude menghasilkan dan mengiterasi desain secara interaktif.

Berikut adalah cuplikan prompt sistem yang dapat Anda gunakan untuk mendorong desain frontend yang lebih baik:

```text Sample prompt for frontend aesthetics wrap
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this
creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive
frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic
fonts like Arial and Inter; opt instead for distinctive choices that elevate the
frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency.
Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw
from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only
solutions for HTML. Use Motion library for React when available. Focus on high-impact
moments: one well-orchestrated page load with staggered reveals (animation-delay)
creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer
CSS gradients, use geometric patterns, or add contextual effects that match the overall
aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the
context. Vary between light and dark themes, different fonts, different aesthetics. You
still tend to converge on common choices (Space Grotesk, for example) across
generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

Anda juga dapat merujuk ke [definisi skill lengkap](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md).

## Pertimbangan migrasi

Saat bermigrasi ke model Claude saat ini dari generasi sebelumnya:

1. **Bersikap spesifik tentang perilaku yang diinginkan:** Pertimbangkan untuk mendeskripsikan dengan tepat apa yang ingin Anda lihat dalam output.

2. **Bingkai instruksi Anda dengan pengubah:** Menambahkan pengubah yang mendorong Claude untuk meningkatkan kualitas dan detail outputnya dapat membantu membentuk kinerja Claude dengan lebih baik. Misalnya, alih-alih "Create an analytics dashboard", gunakan "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation."

3. **Minta fitur spesifik secara eksplisit:** Animasi dan elemen interaktif harus diminta secara eksplisit ketika diinginkan.

4. **Perbarui konfigurasi pemikiran:** Model Claude 4.6 menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) alih-alih pemikiran manual dengan `budget_tokens`. Gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran.

5. **Bermigrasi dari respons yang diisi sebelumnya:** Respons yang diisi sebelumnya pada giliran asisten terakhir tidak lagi didukung mulai dari model Claude 4.6. Lihat [Bermigrasi dari respons yang diisi sebelumnya (prefilled)](#migrating-away-from-prefilled-responses) untuk panduan terperinci tentang alternatifnya.

6. **Sesuaikan prompting anti-kemalasan:** Jika prompt Anda sebelumnya mendorong model untuk lebih teliti atau menggunakan alat secara lebih agresif, kurangi panduan tersebut. Model Claude 4.6 lebih proaktif dan mungkin memicu secara berlebihan pada instruksi yang diperlukan untuk model-model sebelumnya.

Untuk langkah-langkah migrasi terperinci, lihat [Panduan migrasi](/docs/id/about-claude/models/migration-guide).

### Bermigrasi ke Claude Sonnet 5 dari Claude Sonnet 4.5 atau sebelumnya

Lihat [Bermigrasi ke Claude Sonnet 5 dari Claude Sonnet 4.5 atau sebelumnya](/docs/id/about-claude/models/migration-guide#migrating-from-sonnet-45) dalam panduan migrasi, yang mencakup perubahan default effort dan penghapusan pemikiran diperpanjang manual (`budget_tokens`).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Prompting Claude Fable 5" icon="terminal" href="/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5">
    Perbedaan perilaku dan pola prompting untuk Claude Fable 5 dan Claude Mythos 5, mencakup effort, kepatuhan instruksi, eksekusi jangka panjang, memori, dan perubahan scaffolding.
  </Card>

  <Card title="Prompting Claude Sonnet 5" icon="terminal" href="/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5">
    Perbedaan perilaku dan pola prompting untuk Claude Sonnet 5, mencakup effort, default pemikiran adaptif, penggunaan alat, dan migrasi dari Claude Sonnet 4.6.
  </Card>

  <Card title="Gambaran umum rekayasa prompt" icon="edit" href="/docs/id/build-with-claude/prompt-engineering/overview">
    Kapan menggunakan rekayasa prompt dan cara merencanakan pendekatan Anda sebelum menyetel prompt.
  </Card>
</CardGroup>
