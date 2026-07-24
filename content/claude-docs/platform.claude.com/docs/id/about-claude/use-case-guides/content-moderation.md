---
source: platform
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/content-moderation
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 5505ae7b829ac6852175db9d296a34cc00f8d33318490a0617d6059cb633493b
---

# Moderasi konten

Moderasi konten adalah aspek penting dalam menjaga lingkungan yang aman, saling menghormati, dan produktif dalam aplikasi digital. Panduan ini membahas bagaimana Claude dapat digunakan untuk memoderasi konten dalam aplikasi digital Anda.

---

> Kunjungi [cookbook moderasi konten](https://platform.claude.com/cookbook/misc-building-moderation-filter) untuk melihat contoh implementasi moderasi konten menggunakan Claude.

<Tip>
  Panduan ini berfokus pada moderasi konten buatan pengguna dalam aplikasi Anda. Jika Anda mencari panduan tentang memoderasi interaksi dengan Claude, lihat 

  [panduan guardrails](/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

  .
</Tip>

## Sebelum membangun dengan Claude

### Tentukan apakah akan menggunakan Claude untuk moderasi konten

Berikut adalah beberapa indikator utama bahwa Anda sebaiknya menggunakan LLM seperti Claude alih-alih pendekatan ML tradisional atau berbasis aturan untuk moderasi konten:

<AccordionGroup>
  <Accordion title="Anda menginginkan implementasi yang hemat biaya dan cepat">
    Metode ML tradisional memerlukan sumber daya rekayasa yang signifikan, keahlian ML, dan biaya infrastruktur. Sistem moderasi manusia menimbulkan biaya yang bahkan lebih tinggi. Dengan Claude, Anda dapat memiliki sistem moderasi yang canggih dan beroperasi dalam waktu yang jauh lebih singkat dan dengan biaya yang jauh lebih rendah.
  </Accordion>

  <Accordion title="Anda menginginkan pemahaman semantik sekaligus keputusan yang cepat">
    Pendekatan ML tradisional, seperti model bag-of-words atau pencocokan pola sederhana, sering kali kesulitan memahami nada, maksud, dan konteks konten. Meskipun sistem moderasi manusia unggul dalam memahami makna semantik, mereka memerlukan waktu untuk meninjau konten. Claude memenuhi kedua kebutuhan tersebut dengan menggabungkan pemahaman semantik dengan kemampuan untuk memberikan keputusan moderasi dengan cepat.
  </Accordion>

  <Accordion title="Anda membutuhkan keputusan kebijakan yang konsisten">
    Dengan memanfaatkan kemampuan penalaran tingkat lanjutnya, Claude dapat menafsirkan dan menerapkan pedoman moderasi yang kompleks secara seragam. Konsistensi ini membantu memastikan perlakuan yang adil terhadap semua konten, mengurangi risiko keputusan moderasi yang tidak konsisten atau bias yang dapat merusak kepercayaan pengguna.
  </Accordion>

  <Accordion title="Kebijakan moderasi Anda kemungkinan akan berubah atau berkembang seiring waktu">
    Setelah pendekatan ML tradisional dibangun, mengubahnya adalah pekerjaan yang melelahkan dan membutuhkan banyak data. Di sisi lain, seiring berkembangnya produk atau kebutuhan pelanggan Anda, Claude dapat dengan mudah beradaptasi dengan perubahan atau penambahan kebijakan moderasi tanpa pelabelan ulang data pelatihan secara ekstensif.
  </Accordion>

  <Accordion title="Anda memerlukan penalaran yang dapat ditafsirkan untuk keputusan moderasi Anda">
    Jika Anda ingin memberikan penjelasan yang jelas kepada pengguna atau regulator di balik keputusan moderasi, Claude dapat menghasilkan justifikasi yang terperinci dan koheren. Transparansi ini penting untuk membangun kepercayaan dan memastikan akuntabilitas dalam praktik moderasi konten.
  </Accordion>

  <Accordion title="Anda membutuhkan dukungan multibahasa tanpa memelihara model terpisah">
    Pendekatan ML tradisional biasanya memerlukan model terpisah atau proses penerjemahan yang ekstensif untuk setiap bahasa yang didukung. Moderasi manusia memerlukan perekrutan tenaga kerja yang fasih dalam setiap bahasa yang didukung. Kemampuan multibahasa Claude memungkinkannya mengklasifikasikan tiket dalam berbagai bahasa tanpa memerlukan model terpisah atau proses penerjemahan yang ekstensif, menyederhanakan moderasi untuk basis pelanggan global.
  </Accordion>

  <Accordion title="Anda memerlukan dukungan multimodal">
    Kemampuan multimodal Claude memungkinkannya menganalisis dan menafsirkan konten baik dalam bentuk teks maupun gambar. Ini menjadikannya alat yang serbaguna untuk moderasi konten yang komprehensif di lingkungan di mana berbagai jenis media perlu dievaluasi bersama-sama.
  </Accordion>
</AccordionGroup>

<Note>
  Anthropic telah melatih semua model Claude untuk menjadi jujur, membantu, dan tidak berbahaya. Hal ini dapat mengakibatkan Claude memoderasi konten yang dianggap sangat berbahaya (sesuai dengan 

  [Acceptable Use Policy](https://www.anthropic.com/legal/aup)

  ), terlepas dari prompt yang digunakan. Misalnya, situs web dewasa yang ingin mengizinkan pengguna memposting konten seksual eksplisit mungkin mendapati bahwa Claude tetap menandai konten eksplisit sebagai memerlukan moderasi, bahkan jika mereka menentukan dalam prompt mereka untuk tidak memoderasi konten seksual eksplisit. Pertimbangkan untuk meninjau AUP sebelum membangun solusi moderasi.
</Note>

### Buat contoh konten yang akan dimoderasi

Sebelum mengembangkan solusi moderasi konten, pertama-tama buat contoh konten yang harus ditandai dan konten yang tidak boleh ditandai. Pastikan Anda menyertakan kasus tepi (edge case) dan skenario menantang yang mungkin sulit ditangani secara efektif oleh sistem moderasi konten. Setelah itu, tinjau contoh-contoh Anda untuk membuat daftar kategori moderasi yang terdefinisi dengan baik. Sebagai contoh, contoh yang dihasilkan oleh platform media sosial mungkin mencakup hal berikut:

<CodeGroup exclude="shell">
  ```python Python
  client = anthropic.Anthropic()

  allowed_user_comments = [
      "This movie was great, I really enjoyed it. The main actor really killed it!",
      "I hate Mondays.",
      "It is a great time to invest in gold!",
  ]

  disallowed_user_comments = [
      "Delete this post now or you better hide. I am coming after you and your family.",
      "Stay away from the 5G cellphones!! They are using 5G to control you.",
      "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!",
  ]

  # Contoh komentar pengguna untuk menguji moderasi konten
  user_comments = allowed_user_comments + disallowed_user_comments

  # Kategori yang dianggap tidak aman untuk moderasi konten
  unsafe_categories = [
      "Child Exploitation",
      "Conspiracy Theories",
      "Hate",
      "Indiscriminate Weapons",
      "Intellectual Property",
      "Non-Violent Crimes",
      "Privacy",
      "Self-Harm",
      "Sex Crimes",
      "Sexual Content",
      "Specialized Advice",
      "Violent Crimes",
  ]
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const allowedUserComments = [
    "This movie was great, I really enjoyed it. The main actor really killed it!",
    "I hate Mondays.",
    "It is a great time to invest in gold!"
  ];

  const disallowedUserComments = [
    "Delete this post now or you better hide. I am coming after you and your family.",
    "Stay away from the 5G cellphones!! They are using 5G to control you.",
    "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!"
  ];

  // Contoh komentar pengguna untuk menguji moderasi konten
  const userComments = [...allowedUserComments, ...disallowedUserComments];

  // Kategori yang dianggap tidak aman untuk moderasi konten
  const unsafeCategories = [
    "Child Exploitation",
    "Conspiracy Theories",
    "Hate",
    "Indiscriminate Weapons",
    "Intellectual Property",
    "Non-Violent Crimes",
    "Privacy",
    "Self-Harm",
    "Sex Crimes",
    "Sexual Content",
    "Specialized Advice",
    "Violent Crimes"
  ];
  ```

  ```csharp C#
  var client = new AnthropicClient();

  string[] allowedUserComments =
  [
      "This movie was great, I really enjoyed it. The main actor really killed it!",
      "I hate Mondays.",
      "It is a great time to invest in gold!",
  ];

  string[] disallowedUserComments =
  [
      "Delete this post now or you better hide. I am coming after you and your family.",
      "Stay away from the 5G cellphones!! They are using 5G to control you.",
      "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!",
  ];

  // Contoh komentar pengguna untuk menguji moderasi konten
  string[] userComments = [.. allowedUserComments, .. disallowedUserComments];

  // Kategori yang dianggap tidak aman untuk moderasi konten
  string[] unsafeCategories =
  [
      "Child Exploitation",
      "Conspiracy Theories",
      "Hate",
      "Indiscriminate Weapons",
      "Intellectual Property",
      "Non-Violent Crimes",
      "Privacy",
      "Self-Harm",
      "Sex Crimes",
      "Sexual Content",
      "Specialized Advice",
      "Violent Crimes",
  ];
  ```

  ```go Go
  var client = anthropic.NewClient()

  var allowedUserComments = []string{
  	"This movie was great, I really enjoyed it. The main actor really killed it!",
  	"I hate Mondays.",
  	"It is a great time to invest in gold!",
  }

  var disallowedUserComments = []string{
  	"Delete this post now or you better hide. I am coming after you and your family.",
  	"Stay away from the 5G cellphones!! They are using 5G to control you.",
  	"Congratulations! You have won a $1,000 gift card. Click here to claim your prize!",
  }

  // Contoh komentar pengguna untuk menguji moderasi konten
  var userComments = slices.Concat(allowedUserComments, disallowedUserComments)

  // Kategori yang dianggap tidak aman untuk moderasi konten
  var unsafeCategories = []string{
  	"Child Exploitation",
  	"Conspiracy Theories",
  	"Hate",
  	"Indiscriminate Weapons",
  	"Intellectual Property",
  	"Non-Violent Crimes",
  	"Privacy",
  	"Self-Harm",
  	"Sex Crimes",
  	"Sexual Content",
  	"Specialized Advice",
  	"Violent Crimes",
  }

  ```

  ```java Java
  final AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  final List<String> allowedUserComments = List.of(
          "This movie was great, I really enjoyed it. The main actor really killed it!",
          "I hate Mondays.",
          "It is a great time to invest in gold!");

  final List<String> disallowedUserComments = List.of(
          "Delete this post now or you better hide. I am coming after you and your family.",
          "Stay away from the 5G cellphones!! They are using 5G to control you.",
          "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!");

  // Contoh komentar pengguna untuk menguji moderasi konten
  final List<String> userComments =
          Stream.concat(allowedUserComments.stream(), disallowedUserComments.stream()).toList();

  // Kategori yang dianggap tidak aman untuk moderasi konten
  final List<String> unsafeCategories = List.of(
          "Child Exploitation",
          "Conspiracy Theories",
          "Hate",
          "Indiscriminate Weapons",
          "Intellectual Property",
          "Non-Violent Crimes",
          "Privacy",
          "Self-Harm",
          "Sex Crimes",
          "Sexual Content",
          "Specialized Advice",
          "Violent Crimes");
  ```

  ```php PHP
  $client = new Client();

  $allowedUserComments = [
      'This movie was great, I really enjoyed it. The main actor really killed it!',
      'I hate Mondays.',
      'It is a great time to invest in gold!',
  ];

  $disallowedUserComments = [
      'Delete this post now or you better hide. I am coming after you and your family.',
      'Stay away from the 5G cellphones!! They are using 5G to control you.',
      'Congratulations! You have won a $1,000 gift card. Click here to claim your prize!',
  ];

  // Contoh komentar pengguna untuk menguji moderasi konten
  $userComments = [...$allowedUserComments, ...$disallowedUserComments];

  // Kategori yang dianggap tidak aman untuk moderasi konten
  $unsafeCategories = [
      'Child Exploitation',
      'Conspiracy Theories',
      'Hate',
      'Indiscriminate Weapons',
      'Intellectual Property',
      'Non-Violent Crimes',
      'Privacy',
      'Self-Harm',
      'Sex Crimes',
      'Sexual Content',
      'Specialized Advice',
      'Violent Crimes',
  ];
  ```

  ```ruby Ruby
  CLIENT = Anthropic::Client.new

  ALLOWED_USER_COMMENTS = [
    "This movie was great, I really enjoyed it. The main actor really killed it!",
    "I hate Mondays.",
    "It is a great time to invest in gold!"
  ]

  DISALLOWED_USER_COMMENTS = [
    "Delete this post now or you better hide. I am coming after you and your family.",
    "Stay away from the 5G cellphones!! They are using 5G to control you.",
    "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!"
  ]

  # Contoh komentar pengguna untuk menguji moderasi konten
  USER_COMMENTS = ALLOWED_USER_COMMENTS + DISALLOWED_USER_COMMENTS

  # Kategori yang dianggap tidak aman untuk moderasi konten
  UNSAFE_CATEGORIES = [
    "Child Exploitation",
    "Conspiracy Theories",
    "Hate",
    "Indiscriminate Weapons",
    "Intellectual Property",
    "Non-Violent Crimes",
    "Privacy",
    "Self-Harm",
    "Sex Crimes",
    "Sexual Content",
    "Specialized Advice",
    "Violent Crimes"
  ]
  ```
</CodeGroup>

Memoderasi contoh-contoh ini secara efektif memerlukan pemahaman bahasa yang bernuansa. Dalam komentar, `This movie was great, I really enjoyed it. The main actor really killed it!`, sistem moderasi konten perlu mengenali bahwa "killed it" adalah metafora, bukan indikasi kekerasan yang sebenarnya. Sebaliknya, meskipun tidak ada penyebutan kekerasan secara eksplisit, komentar `Delete this post now or you better hide. I am coming after you and your family.` harus ditandai oleh sistem moderasi konten.

Kategori tidak aman dapat disesuaikan agar sesuai dengan kebutuhan spesifik Anda. Misalnya, jika Anda ingin mencegah anak di bawah umur membuat konten di situs web Anda, Anda dapat menambahkan "Underage Posting" ke dalam kategori.

***

## Cara memoderasi konten menggunakan Claude

### Pilih model Claude yang tepat

Saat memilih model, penting untuk mempertimbangkan ukuran data Anda. Jika biaya menjadi perhatian, model yang lebih kecil seperti Claude Haiku 4.5 adalah pilihan yang sangat baik karena efektivitas biayanya. Berikut adalah perkiraan biaya untuk memoderasi teks untuk platform media sosial yang menerima satu miliar postingan per bulan:

* **Ukuran konten**

  * Postingan per bulan: 1 miliar
  * Karakter per postingan: 100
  * Total karakter: 100 miliar

* **Perkiraan token**

  * Token input: 28,6 miliar (dengan asumsi 1 token per 3,5 karakter)
  * Persentase pesan yang ditandai: 3%
  * Token output per pesan yang ditandai: 50
  * Total token output: 1,5 miliar

* **Perkiraan biaya Claude Haiku 4.5**

  * Biaya token input: 28.600 MTok \* $1,00/MTok = $28.600 USD
  * Biaya token output: 1.500 MTok \* $5,00/MTok = $7.500 USD
  * Biaya bulanan: $28.600 + $7.500 = $36.100 USD

* **Perkiraan biaya Claude Opus 4.8**

  * Biaya token input: 28.600 MTok \* $5,00/MTok = $143.000 USD
  * Biaya token output: 1.500 MTok \* $25,00/MTok = $37.500 USD
  * Biaya bulanan: $143.000 + $37.500 = $180.500 USD

<Tip>
  Biaya aktual mungkin berbeda dari perkiraan ini. Perkiraan ini didasarkan pada prompt yang disorot di bagian 

  [pemrosesan batch](#consider-batch-processing)

  . Token output dapat dikurangi lebih jauh lagi dengan menghapus bidang 

  `explanation`

   dari respons.
</Tip>

### Bangun prompt yang kuat

Untuk menggunakan Claude dalam moderasi konten, Claude harus memahami persyaratan moderasi aplikasi Anda. Mulailah dengan menulis prompt yang memungkinkan Anda mendefinisikan kebutuhan moderasi Anda:

<CodeGroup exclude="shell">
  ```python Python
  def moderate_message(message, unsafe_categories):
      # Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      unsafe_category_str = "\n".join(unsafe_categories)

      # Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
      assessment_prompt = f"""
      Determine whether the following message warrants moderation,
      based on the unsafe categories outlined below.

      Message:
      <message>{message}</message>

      Unsafe Categories:
      <categories>
      {unsafe_category_str}
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {{
      "violation": <Boolean field denoting whether the message should be moderated>,
      "categories": [Comma-separated list of violated categories],
      "explanation": [Optional. Only include if there is a violation.]
      }}
  Do not include markdown formatting or code fences in your response."""

      # Kirim permintaan ke Claude untuk moderasi konten
      response = client.messages.create(
          model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
          max_tokens=200,
          messages=[{"role": "user", "content": assessment_prompt}],
      )

      # Parse respons JSON dari Claude
      text_block = next(block for block in response.content if block.type == "text")
      assessment = json.loads(text_block.text)

      # Ekstrak status pelanggaran dari hasil penilaian
      contains_violation = assessment["violation"]

      # Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
      violated_categories = assessment.get("categories", []) if contains_violation else []
      explanation = assessment.get("explanation") if contains_violation else None

      return contains_violation, violated_categories, explanation


  # Proses setiap komentar dan cetak hasilnya
  for comment in user_comments:
      print(f"\nComment: {comment}")
      violation, violated_categories, explanation = moderate_message(
          comment, unsafe_categories
      )

      if violation:
          print(f"Violated Categories: {', '.join(violated_categories)}")
          print(f"Explanation: {explanation}")
      else:
          print("No issues detected.")
  ```

  ```typescript TypeScript
  // Bentuk penilaian JSON yang dikembalikan Claude
  interface ModerationAssessment {
    violation: boolean;
    categories?: string[];
    explanation?: string;
  }

  async function moderateMessage(
    message: string,
    unsafeCategories: string[]
  ): Promise<{ violation: boolean; violatedCategories: string[]; explanation?: string }> {
    // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
    const unsafeCategoryStr = unsafeCategories.join("\n");

    // Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
    const assessmentPrompt = `
      Determine whether the following message warrants moderation,
      based on the unsafe categories outlined below.

      Message:
      <message>${message}</message>

      Unsafe Categories:
      <categories>
      ${unsafeCategoryStr}
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {
      "violation": <Boolean field denoting whether the message should be moderated>,
      "categories": [Comma-separated list of violated categories],
      "explanation": [Optional. Only include if there is a violation.]
      }
  Do not include markdown formatting or code fences in your response.`;

    // Kirim permintaan ke Claude untuk moderasi konten
    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001", // Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{ role: "user", content: assessmentPrompt }]
    });

    // Parse respons JSON dari Claude
    const textBlock = response.content.find((block) => block.type === "text");
    if (!textBlock) {
      throw new Error("Expected a text block in the response");
    }
    const assessment: ModerationAssessment = JSON.parse(textBlock.text);

    // Ekstrak status pelanggaran dari penilaian
    const containsViolation = assessment.violation;

    // Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
    const violatedCategories = containsViolation ? assessment.categories ?? [] : [];
    const explanation = containsViolation ? assessment.explanation : undefined;

    return { violation: containsViolation, violatedCategories, explanation };
  }

  // Proses setiap komentar dan cetak hasilnya
  for (const comment of userComments) {
    console.log(`\nComment: ${comment}`);
    const { violation, violatedCategories, explanation } = await moderateMessage(
      comment,
      unsafeCategories
    );

    if (violation) {
      console.log(`Violated Categories: ${violatedCategories.join(", ")}`);
      console.log(`Explanation: ${explanation}`);
    } else {
      console.log("No issues detected.");
    }
  }
  ```

  ```csharp C#
  async Task<(bool ContainsViolation, List<string> ViolatedCategories, string? Explanation)> ModerateMessage(
      string message,
      IReadOnlyList<string> categories
  )
  {
      // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      var unsafeCategoryText = string.Join("\n", categories);

      // Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
      var assessmentPrompt = $$"""

      Determine whether the following message warrants moderation,
      based on the unsafe categories outlined below.

      Message:
      <message>{{message}}</message>

      Unsafe Categories:
      <categories>
      {{unsafeCategoryText}}
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {
      "violation": <Boolean field denoting whether the message should be moderated>,
      "categories": [Comma-separated list of violated categories],
      "explanation": [Optional. Only include if there is a violation.]
      }
  Do not include markdown formatting or code fences in your response.
  """;

      // Kirim permintaan ke Claude untuk moderasi konten
      var response = await client.Messages.Create(
          new()
          {
              Model = Model.ClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
              MaxTokens = 200,
              Messages = [new() { Role = Role.User, Content = assessmentPrompt }],
          }
      );

      // Persempit blok konten pertama menjadi blok teks, lalu parse respons JSON dari Claude
      if (!response.Content[0].TryPickText(out var textBlock))
      {
          throw new InvalidOperationException("Expected a text response from Claude.");
      }
      var assessment = JsonNode.Parse(textBlock.Text)!;

      // Ekstrak status pelanggaran dari hasil penilaian
      var containsViolation = assessment["violation"]!.GetValue<bool>();

      // Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
      List<string> violatedCategories = containsViolation
          ? assessment["categories"]?.AsArray().Select(category => category!.GetValue<string>()).ToList() ?? []
          : [];
      var explanation = containsViolation ? assessment["explanation"]?.GetValue<string>() : null;

      return (containsViolation, violatedCategories, explanation);
  }

  // Proses setiap komentar dan cetak hasilnya
  foreach (var comment in userComments)
  {
      Console.WriteLine($"\nComment: {comment}");
      var (violation, violatedCategories, explanation) = await ModerateMessage(comment, unsafeCategories);

      if (violation)
      {
          Console.WriteLine($"Violated Categories: {string.Join(", ", violatedCategories)}");
          Console.WriteLine($"Explanation: {explanation}");
      }
      else
      {
          Console.WriteLine("No issues detected.");
      }
  }
  ```

  ```go Go
  func moderateMessage(message string, unsafeCategories []string) (bool, []string, string) {
  	// Mengonversi kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
  	unsafeCategoryStr := strings.Join(unsafeCategories, "\n")

  	// Menyusun prompt untuk Claude, termasuk pesan dan kategori tidak aman
  	assessmentPrompt := fmt.Sprintf(`
      Determine whether the following message warrants moderation,
      based on the unsafe categories outlined below.

      Message:
      <message>%s</message>

      Unsafe Categories:
      <categories>
      %s
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {
      "violation": <Boolean field denoting whether the message should be moderated>,
      "categories": [Comma-separated list of violated categories],
      "explanation": [Optional. Only include if there is a violation.]
      }
  Do not include markdown formatting or code fences in your response.`, message, unsafeCategoryStr)

  	// Mengirim permintaan ke Claude untuk moderasi konten
  	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
  		MaxTokens: 200,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(assessmentPrompt)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Mempersempit blok konten pertama menjadi blok teks sebelum membaca teksnya
  	textBlock, ok := response.Content[0].AsAny().(anthropic.TextBlock)
  	if !ok {
  		log.Fatalf("expected a text block, got %q", response.Content[0].Type)
  	}

  	// Mem-parsing respons JSON dari Claude
  	var assessment struct {
  		Violation   bool     `json:"violation"`
  		Categories  []string `json:"categories"`
  		Explanation string   `json:"explanation"`
  	}
  	if err := json.Unmarshal([]byte(textBlock.Text), &assessment); err != nil {
  		log.Fatal(err)
  	}

  	// Jika ada pelanggaran, kembalikan kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
  	if !assessment.Violation {
  		return false, nil, ""
  	}
  	return true, assessment.Categories, assessment.Explanation
  }

  // moderateAllComments memproses setiap komentar dan mencetak hasilnya.
  func moderateAllComments() {
  	for _, comment := range userComments {
  		fmt.Printf("\nComment: %s\n", comment)
  		violation, violatedCategories, explanation := moderateMessage(comment, unsafeCategories)

  		if violation {
  			fmt.Printf("Violated Categories: %s\n", strings.Join(violatedCategories, ", "))
  			fmt.Printf("Explanation: %s\n", explanation)
  		} else {
  			fmt.Println("No issues detected.")
  		}
  	}
  }

  ```

  ```java Java
  record ModerationResult(boolean violation, List<String> violatedCategories, String explanation) {}

  ModerationResult moderateMessage(String message, List<String> unsafeCategories)
          throws JsonProcessingException {
      // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      String unsafeCategoryStr = String.join("\n", unsafeCategories);

      // Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
      String assessmentPrompt = """

              Determine whether the following message warrants moderation,
              based on the unsafe categories outlined below.

              Message:
              <message>%s</message>

              Unsafe Categories:
              <categories>
              %s
              </categories>

              Respond with ONLY a JSON object, using the format below:
              {
              "violation": <Boolean field denoting whether the message should be moderated>,
              "categories": [Comma-separated list of violated categories],
              "explanation": [Optional. Only include if there is a violation.]
              }
          Do not include markdown formatting or code fences in your response."""
              .formatted(message, unsafeCategoryStr);

      // Kirim permintaan ke Claude untuk moderasi konten
      Message response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_HAIKU_4_5_20251001) // Using the Haiku model for lower costs
              .maxTokens(200)
              .addUserMessage(assessmentPrompt)
              .build());

      // Parse respons JSON dari Claude
      String assessmentJson = response.content().stream()
              .flatMap(contentBlock -> contentBlock.text().stream())
              .findFirst()
              .orElseThrow()
              .text();
      ObjectMapper mapper = new ObjectMapper();
      JsonNode assessment = mapper.readTree(assessmentJson);

      // Ekstrak status pelanggaran dari hasil penilaian
      boolean containsViolation = assessment.required("violation").asBoolean();

      // Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
      List<String> violatedCategories = containsViolation && assessment.has("categories")
              ? mapper.convertValue(assessment.get("categories"), new TypeReference<List<String>>() {})
              : List.of();
      String explanation = containsViolation && assessment.hasNonNull("explanation")
              ? assessment.get("explanation").asText()
              : null;

      return new ModerationResult(containsViolation, violatedCategories, explanation);
  }

  // Proses setiap komentar dan cetak hasilnya
  void printModerationResults() throws JsonProcessingException {
      for (String comment : userComments) {
          IO.println("\nComment: " + comment);
          ModerationResult result = moderateMessage(comment, unsafeCategories);

          if (result.violation()) {
              IO.println("Violated Categories: " + String.join(", ", result.violatedCategories()));
              IO.println("Explanation: " + result.explanation());
          } else {
              IO.println("No issues detected.");
          }
      }
  }
  ```

  ```php PHP
  $moderateMessage = function (string $message, array $unsafeCategories) use ($client): array {
      // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      $unsafeCategoryStr = implode("\n", $unsafeCategories);

      // Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
      $assessmentPrompt = <<<PROMPT

          Determine whether the following message warrants moderation,
          based on the unsafe categories outlined below.

          Message:
          <message>{$message}</message>

          Unsafe Categories:
          <categories>
          {$unsafeCategoryStr}
          </categories>

          Respond with ONLY a JSON object, using the format below:
          {
          "violation": <Boolean field denoting whether the message should be moderated>,
          "categories": [Comma-separated list of violated categories],
          "explanation": [Optional. Only include if there is a violation.]
          }
      Do not include markdown formatting or code fences in your response.
      PROMPT;

      // Kirim permintaan ke Claude untuk moderasi konten
      $response = $client->messages->create(
          model: 'claude-haiku-4-5-20251001', // Using the Haiku model for lower costs
          maxTokens: 200,
          messages: [['role' => 'user', 'content' => $assessmentPrompt]],
      );

      // Parse respons JSON dari Claude. SDK mendekode setiap blok konten
      // ke kelas konkretnya, jadi cari TextBlock sebelum membaca teksnya.
      $textBlock = array_find($response->content, fn ($block) => $block instanceof TextBlock)
          ?? throw new RuntimeException('Expected a text block in the response.');
      $assessment = json_decode($textBlock->text, associative: true, flags: JSON_THROW_ON_ERROR);

      // Ekstrak status pelanggaran dari hasil penilaian
      $containsViolation = $assessment['violation'];

      // Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
      $violatedCategories = $containsViolation ? ($assessment['categories'] ?? []) : [];
      $explanation = $containsViolation ? ($assessment['explanation'] ?? null) : null;

      return [$containsViolation, $violatedCategories, $explanation];
  };

  // Proses setiap komentar dan cetak hasilnya
  foreach ($userComments as $comment) {
      echo "\nComment: {$comment}\n";
      [$violation, $violatedCategories, $explanation] = $moderateMessage($comment, $unsafeCategories);

      if ($violation) {
          echo 'Violated Categories: ' . implode(', ', $violatedCategories) . "\n";
          echo "Explanation: {$explanation}\n";
      } else {
          echo "No issues detected.\n";
      }
  }
  ```

  ```ruby Ruby
  def moderate_message(message, unsafe_categories)
    # Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
    unsafe_category_str = unsafe_categories.join("\n")

    # Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
    assessment_prompt = <<~PROMPT.chomp

          Determine whether the following message warrants moderation,
          based on the unsafe categories outlined below.

          Message:
          <message>#{message}</message>

          Unsafe Categories:
          <categories>
          #{unsafe_category_str}
          </categories>

          Respond with ONLY a JSON object, using the format below:
          {
          "violation": <Boolean field denoting whether the message should be moderated>,
          "categories": [Comma-separated list of violated categories],
          "explanation": [Optional. Only include if there is a violation.]
          }
      Do not include markdown formatting or code fences in your response.
    PROMPT

    # Kirim permintaan ke Claude untuk moderasi konten
    response = CLIENT.messages.create(
      model: "claude-haiku-4-5-20251001", # Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{role: :user, content: assessment_prompt}]
    )

    # Parse respons JSON dari Claude
    text_block = response.content.find { it.type == :text }
    assessment = JSON.parse(text_block.text)

    # Ekstrak status pelanggaran dari hasil penilaian
    contains_violation = assessment["violation"]

    # Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
    violated_categories = contains_violation ? assessment.fetch("categories", []) : []
    explanation = contains_violation ? assessment["explanation"] : nil

    [contains_violation, violated_categories, explanation]
  end


  # Proses setiap komentar dan cetak hasilnya
  USER_COMMENTS.each do |comment|
    puts "\nComment: #{comment}"
    violation, violated_categories, explanation = moderate_message(comment, UNSAFE_CATEGORIES)

    if violation
      puts "Violated Categories: #{violated_categories.join(", ")}"
      puts "Explanation: #{explanation}"
    else
      puts "No issues detected."
    end
  end
  ```
</CodeGroup>

Dalam contoh ini, fungsi `moderate_message` berisi prompt penilaian yang mencakup kategori konten tidak aman dan pesan yang akan dievaluasi. Prompt tersebut meminta Claude untuk menilai apakah pesan harus dimoderasi, berdasarkan kategori tidak aman yang Anda definisikan sebelumnya.

Penilaian model kemudian diurai untuk menentukan apakah ada pelanggaran. Jika ada pelanggaran, Claude juga mengembalikan daftar kategori yang dilanggar dan penjelasan mengapa pesan tersebut tidak aman.

### Evaluasi prompt Anda

Moderasi konten adalah masalah klasifikasi. Dengan demikian, Anda dapat menggunakan teknik yang sama yang diuraikan dalam [cookbook klasifikasi](https://platform.claude.com/cookbook/capabilities-classification-guide) untuk menentukan akurasi sistem moderasi konten Anda.

Satu pertimbangan tambahan adalah alih-alih memperlakukan moderasi konten sebagai masalah klasifikasi biner, Anda dapat membuat beberapa kategori untuk merepresentasikan berbagai tingkat risiko. Membuat beberapa tingkat risiko memungkinkan Anda menyesuaikan tingkat agresivitas moderasi Anda. Misalnya, Anda mungkin ingin secara otomatis memblokir kueri pengguna yang dianggap berisiko tinggi, sementara pengguna dengan banyak kueri berisiko sedang ditandai untuk ditinjau oleh manusia.

<CodeGroup exclude="shell">
  ```python Python
  def assess_risk_level(message, unsafe_categories):
      # Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      unsafe_category_str = "\n".join(unsafe_categories)

      # Susun prompt untuk Claude, termasuk pesan, kategori tidak aman, dan definisi tingkat risiko
      assessment_prompt = f"""
      Assess the risk level of the following message,
      based on the unsafe categories listed below.

  Message:
  <message>{message}</message>

  Unsafe Categories:
  <categories>
  {unsafe_category_str}
  </categories>

  Assign a risk level based on your confidence that the user's message should be moderated
  based on the defined unsafe categories:

  0 - No risk
  1 - Low risk
  2 - Medium risk
  3 - High risk

  Respond with ONLY a JSON object, using the format below:
  {{
    "risk_level": <Numerical field denoting the risk level>,
    "categories": [Comma-separated list of violated categories],
    "explanation": <Optional. Only include if risk level is greater than 0>
  }}
  Do not include markdown formatting or code fences in your response."""

      # Kirim permintaan ke Claude untuk penilaian risiko
      response = client.messages.create(
          model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
          max_tokens=200,
          messages=[{"role": "user", "content": assessment_prompt}],
      )

      # Parse respons JSON dari Claude
      text_block = next(block for block in response.content if block.type == "text")
      assessment = json.loads(text_block.text)

      # Ekstrak tingkat risiko, kategori yang dilanggar, dan penjelasan dari hasil penilaian
      risk_level = assessment["risk_level"]
      violated_categories = assessment["categories"]
      explanation = assessment.get("explanation")

      return risk_level, violated_categories, explanation


  # Proses setiap komentar dan cetak hasilnya
  for comment in user_comments:
      print(f"\nComment: {comment}")
      risk_level, violated_categories, explanation = assess_risk_level(
          comment, unsafe_categories
      )

      print(f"Risk Level: {risk_level}")
      if violated_categories:
          print(f"Violated Categories: {', '.join(violated_categories)}")
      if explanation:
          print(f"Explanation: {explanation}")
  ```

  ```typescript TypeScript
  // Bentuk penilaian risiko JSON yang dikembalikan Claude
  interface RiskAssessment {
    risk_level: number;
    categories: string[];
    explanation?: string;
  }

  async function assessRiskLevel(
    message: string,
    unsafeCategories: string[]
  ): Promise<{ riskLevel: number; violatedCategories: string[]; explanation?: string }> {
    // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
    const unsafeCategoryStr = unsafeCategories.join("\n");

    // Susun prompt untuk Claude, termasuk pesan, kategori tidak aman, dan definisi tingkat risiko
    const assessmentPrompt = `
      Assess the risk level of the following message,
      based on the unsafe categories listed below.

  Message:
  <message>${message}</message>

  Unsafe Categories:
  <categories>
  ${unsafeCategoryStr}
  </categories>

  Assign a risk level based on your confidence that the user's message should be moderated
  based on the defined unsafe categories:

  0 - No risk
  1 - Low risk
  2 - Medium risk
  3 - High risk

  Respond with ONLY a JSON object, using the format below:
  {
    "risk_level": <Numerical field denoting the risk level>,
    "categories": [Comma-separated list of violated categories],
    "explanation": <Optional. Only include if risk level is greater than 0>
  }
  Do not include markdown formatting or code fences in your response.`;

    // Kirim permintaan ke Claude untuk penilaian risiko
    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001", // Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{ role: "user", content: assessmentPrompt }]
    });

    // Parse respons JSON dari Claude
    const textBlock = response.content.find((block) => block.type === "text");
    if (!textBlock) {
      throw new Error("Expected a text block in the response");
    }
    const assessment: RiskAssessment = JSON.parse(textBlock.text);

    // Ekstrak tingkat risiko, kategori yang dilanggar, dan penjelasan dari penilaian
    const { risk_level: riskLevel, categories: violatedCategories, explanation } = assessment;

    return { riskLevel, violatedCategories, explanation };
  }

  // Proses setiap komentar dan cetak hasilnya
  for (const comment of userComments) {
    console.log(`\nComment: ${comment}`);
    const { riskLevel, violatedCategories, explanation } = await assessRiskLevel(
      comment,
      unsafeCategories
    );

    console.log(`Risk Level: ${riskLevel}`);
    if (violatedCategories.length > 0) {
      console.log(`Violated Categories: ${violatedCategories.join(", ")}`);
    }
    if (explanation) {
      console.log(`Explanation: ${explanation}`);
    }
  }
  ```

  ```csharp C#
  async Task<(int RiskLevel, List<string> ViolatedCategories, string? Explanation)> AssessRiskLevel(
      string message,
      IReadOnlyList<string> categories
  )
  {
      // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      var unsafeCategoryText = string.Join("\n", categories);

      // Susun prompt untuk Claude, termasuk pesan, kategori tidak aman, dan definisi tingkat risiko
      var assessmentPrompt = $$"""

      Assess the risk level of the following message,
      based on the unsafe categories listed below.

  Message:
  <message>{{message}}</message>

  Unsafe Categories:
  <categories>
  {{unsafeCategoryText}}
  </categories>

  Assign a risk level based on your confidence that the user's message should be moderated
  based on the defined unsafe categories:

  0 - No risk
  1 - Low risk
  2 - Medium risk
  3 - High risk

  Respond with ONLY a JSON object, using the format below:
  {
    "risk_level": <Numerical field denoting the risk level>,
    "categories": [Comma-separated list of violated categories],
    "explanation": <Optional. Only include if risk level is greater than 0>
  }
  Do not include markdown formatting or code fences in your response.
  """;

      // Kirim permintaan ke Claude untuk penilaian risiko
      var response = await client.Messages.Create(
          new()
          {
              Model = Model.ClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
              MaxTokens = 200,
              Messages = [new() { Role = Role.User, Content = assessmentPrompt }],
          }
      );

      // Persempit blok konten pertama menjadi blok teks, lalu parse respons JSON dari Claude
      if (!response.Content[0].TryPickText(out var textBlock))
      {
          throw new InvalidOperationException("Expected a text response from Claude.");
      }
      var assessment = JsonNode.Parse(textBlock.Text)!;

      // Ekstrak tingkat risiko, kategori yang dilanggar, dan penjelasan dari hasil penilaian
      var riskLevel = assessment["risk_level"]!.GetValue<int>();
      var violatedCategories = assessment["categories"]!
          .AsArray()
          .Select(category => category!.GetValue<string>())
          .ToList();
      var explanation = assessment["explanation"]?.GetValue<string>();

      return (riskLevel, violatedCategories, explanation);
  }

  // Proses setiap komentar dan cetak hasilnya
  foreach (var comment in userComments)
  {
      Console.WriteLine($"\nComment: {comment}");
      var (riskLevel, violatedCategories, explanation) = await AssessRiskLevel(comment, unsafeCategories);

      Console.WriteLine($"Risk Level: {riskLevel}");
      if (violatedCategories.Count > 0)
      {
          Console.WriteLine($"Violated Categories: {string.Join(", ", violatedCategories)}");
      }
      if (!string.IsNullOrEmpty(explanation))
      {
          Console.WriteLine($"Explanation: {explanation}");
      }
  }
  ```

  ```go Go
  func assessRiskLevel(message string, unsafeCategories []string) (int, []string, string) {
  	// Mengonversi kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
  	unsafeCategoryStr := strings.Join(unsafeCategories, "\n")

  	// Menyusun prompt untuk Claude, termasuk pesan, kategori tidak aman, dan definisi tingkat risiko
  	assessmentPrompt := fmt.Sprintf(`
      Assess the risk level of the following message,
      based on the unsafe categories listed below.

  Message:
  <message>%s</message>

  Unsafe Categories:
  <categories>
  %s
  </categories>

  Assign a risk level based on your confidence that the user's message should be moderated
  based on the defined unsafe categories:

  0 - No risk
  1 - Low risk
  2 - Medium risk
  3 - High risk

  Respond with ONLY a JSON object, using the format below:
  {
    "risk_level": <Numerical field denoting the risk level>,
    "categories": [Comma-separated list of violated categories],
    "explanation": <Optional. Only include if risk level is greater than 0>
  }
  Do not include markdown formatting or code fences in your response.`, message, unsafeCategoryStr)

  	// Mengirim permintaan ke Claude untuk penilaian risiko
  	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
  		MaxTokens: 200,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(assessmentPrompt)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Mempersempit blok konten pertama menjadi blok teks sebelum membaca teksnya
  	textBlock, ok := response.Content[0].AsAny().(anthropic.TextBlock)
  	if !ok {
  		log.Fatalf("expected a text block, got %q", response.Content[0].Type)
  	}

  	// Mem-parsing respons JSON dari Claude
  	var assessment struct {
  		RiskLevel   int      `json:"risk_level"`
  		Categories  []string `json:"categories"`
  		Explanation string   `json:"explanation"`
  	}
  	if err := json.Unmarshal([]byte(textBlock.Text), &assessment); err != nil {
  		log.Fatal(err)
  	}

  	// Mengembalikan tingkat risiko, kategori yang dilanggar, dan penjelasan dari penilaian
  	return assessment.RiskLevel, assessment.Categories, assessment.Explanation
  }

  // assessAllRiskLevels memproses setiap komentar dan mencetak hasilnya.
  func assessAllRiskLevels() {
  	for _, comment := range userComments {
  		fmt.Printf("\nComment: %s\n", comment)
  		riskLevel, violatedCategories, explanation := assessRiskLevel(comment, unsafeCategories)

  		fmt.Printf("Risk Level: %d\n", riskLevel)
  		if len(violatedCategories) > 0 {
  			fmt.Printf("Violated Categories: %s\n", strings.Join(violatedCategories, ", "))
  		}
  		if explanation != "" {
  			fmt.Printf("Explanation: %s\n", explanation)
  		}
  	}
  }

  ```

  ```java Java
  record RiskAssessment(int riskLevel, List<String> violatedCategories, String explanation) {}

  RiskAssessment assessRiskLevel(String message, List<String> unsafeCategories)
          throws JsonProcessingException {
      // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      String unsafeCategoryStr = String.join("\n", unsafeCategories);

      // Susun prompt untuk Claude, termasuk pesan, kategori tidak aman, dan definisi tingkat risiko
      String assessmentPrompt = """

              Assess the risk level of the following message,
              based on the unsafe categories listed below.

          Message:
          <message>%s</message>

          Unsafe Categories:
          <categories>
          %s
          </categories>

          Assign a risk level based on your confidence that the user's message should be moderated
          based on the defined unsafe categories:

          0 - No risk
          1 - Low risk
          2 - Medium risk
          3 - High risk

          Respond with ONLY a JSON object, using the format below:
          {
            "risk_level": <Numerical field denoting the risk level>,
            "categories": [Comma-separated list of violated categories],
            "explanation": <Optional. Only include if risk level is greater than 0>
          }
          Do not include markdown formatting or code fences in your response."""
              .formatted(message, unsafeCategoryStr);

      // Kirim permintaan ke Claude untuk penilaian risiko
      Message response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_HAIKU_4_5_20251001) // Using the Haiku model for lower costs
              .maxTokens(200)
              .addUserMessage(assessmentPrompt)
              .build());

      // Parse respons JSON dari Claude
      String assessmentJson = response.content().stream()
              .flatMap(contentBlock -> contentBlock.text().stream())
              .findFirst()
              .orElseThrow()
              .text();
      ObjectMapper mapper = new ObjectMapper();
      JsonNode assessment = mapper.readTree(assessmentJson);

      // Ekstrak tingkat risiko, kategori yang dilanggar, dan penjelasan dari hasil penilaian
      int riskLevel = assessment.required("risk_level").asInt();
      JsonNode categoriesNode = assessment.required("categories");
      List<String> violatedCategories = categoriesNode.isNull()
              ? List.of()
              : mapper.convertValue(categoriesNode, new TypeReference<List<String>>() {});
      String explanation = assessment.hasNonNull("explanation")
              ? assessment.get("explanation").asText()
              : null;

      return new RiskAssessment(riskLevel, violatedCategories, explanation);
  }

  // Proses setiap komentar dan cetak hasilnya
  void printRiskLevels() throws JsonProcessingException {
      for (String comment : userComments) {
          IO.println("\nComment: " + comment);
          RiskAssessment assessment = assessRiskLevel(comment, unsafeCategories);

          IO.println("Risk Level: " + assessment.riskLevel());
          if (!assessment.violatedCategories().isEmpty()) {
              IO.println("Violated Categories: " + String.join(", ", assessment.violatedCategories()));
          }
          if (assessment.explanation() != null && !assessment.explanation().isEmpty()) {
              IO.println("Explanation: " + assessment.explanation());
          }
      }
  }
  ```

  ```php PHP
  $assessRiskLevel = function (string $message, array $unsafeCategories) use ($client): array {
      // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      $unsafeCategoryStr = implode("\n", $unsafeCategories);

      // Susun prompt untuk Claude, termasuk pesan, kategori tidak aman, dan definisi tingkat risiko
      $assessmentPrompt = <<<PROMPT

          Assess the risk level of the following message,
          based on the unsafe categories listed below.

      Message:
      <message>{$message}</message>

      Unsafe Categories:
      <categories>
      {$unsafeCategoryStr}
      </categories>

      Assign a risk level based on your confidence that the user's message should be moderated
      based on the defined unsafe categories:

      0 - No risk
      1 - Low risk
      2 - Medium risk
      3 - High risk

      Respond with ONLY a JSON object, using the format below:
      {
        "risk_level": <Numerical field denoting the risk level>,
        "categories": [Comma-separated list of violated categories],
        "explanation": <Optional. Only include if risk level is greater than 0>
      }
      Do not include markdown formatting or code fences in your response.
      PROMPT;

      // Kirim permintaan ke Claude untuk penilaian risiko
      $response = $client->messages->create(
          model: 'claude-haiku-4-5-20251001', // Using the Haiku model for lower costs
          maxTokens: 200,
          messages: [['role' => 'user', 'content' => $assessmentPrompt]],
      );

      // Parse respons JSON dari Claude. SDK mendekode setiap blok konten
      // ke kelas konkretnya, jadi cari TextBlock sebelum membaca teksnya.
      $textBlock = array_find($response->content, fn ($block) => $block instanceof TextBlock)
          ?? throw new RuntimeException('Expected a text block in the response.');
      $assessment = json_decode($textBlock->text, associative: true, flags: JSON_THROW_ON_ERROR);

      // Ekstrak tingkat risiko, kategori yang dilanggar, dan penjelasan dari hasil penilaian
      $riskLevel = $assessment['risk_level'];
      $violatedCategories = $assessment['categories'];
      $explanation = $assessment['explanation'] ?? null;

      return [$riskLevel, $violatedCategories, $explanation];
  };

  // Proses setiap komentar dan cetak hasilnya
  foreach ($userComments as $comment) {
      echo "\nComment: {$comment}\n";
      [$riskLevel, $violatedCategories, $explanation] = $assessRiskLevel($comment, $unsafeCategories);

      echo "Risk Level: {$riskLevel}\n";
      if ($violatedCategories) {
          echo 'Violated Categories: ' . implode(', ', $violatedCategories) . "\n";
      }
      if ($explanation) {
          echo "Explanation: {$explanation}\n";
      }
  }
  ```

  ```ruby Ruby
  def assess_risk_level(message, unsafe_categories)
    # Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
    unsafe_category_str = unsafe_categories.join("\n")

    # Susun prompt untuk Claude, termasuk pesan, kategori tidak aman, dan definisi tingkat risiko
    assessment_prompt = <<~PROMPT.chomp

          Assess the risk level of the following message,
          based on the unsafe categories listed below.

      Message:
      <message>#{message}</message>

      Unsafe Categories:
      <categories>
      #{unsafe_category_str}
      </categories>

      Assign a risk level based on your confidence that the user's message should be moderated
      based on the defined unsafe categories:

      0 - No risk
      1 - Low risk
      2 - Medium risk
      3 - High risk

      Respond with ONLY a JSON object, using the format below:
      {
        "risk_level": <Numerical field denoting the risk level>,
        "categories": [Comma-separated list of violated categories],
        "explanation": <Optional. Only include if risk level is greater than 0>
      }
      Do not include markdown formatting or code fences in your response.
    PROMPT

    # Kirim permintaan ke Claude untuk penilaian risiko
    response = CLIENT.messages.create(
      model: "claude-haiku-4-5-20251001", # Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{role: :user, content: assessment_prompt}]
    )

    # Parse respons JSON dari Claude
    text_block = response.content.find { it.type == :text }
    assessment = JSON.parse(text_block.text)

    # Ekstrak tingkat risiko, kategori yang dilanggar, dan penjelasan dari hasil penilaian
    risk_level = assessment["risk_level"]
    violated_categories = assessment["categories"]
    explanation = assessment["explanation"]

    [risk_level, violated_categories, explanation]
  end


  # Proses setiap komentar dan cetak hasilnya
  USER_COMMENTS.each do |comment|
    puts "\nComment: #{comment}"
    risk_level, violated_categories, explanation = assess_risk_level(comment, UNSAFE_CATEGORIES)

    puts "Risk Level: #{risk_level}"
    puts "Violated Categories: #{violated_categories.join(", ")}" if violated_categories&.any?
    puts "Explanation: #{explanation}" if explanation
  end
  ```
</CodeGroup>

Kode ini mengimplementasikan fungsi `assess_risk_level` yang menggunakan Claude untuk mengevaluasi tingkat risiko sebuah pesan. Fungsi ini menerima pesan dan kategori tidak aman sebagai input.

Di dalam fungsi tersebut, sebuah prompt dibuat untuk Claude, yang mencakup pesan yang akan dinilai, kategori tidak aman, dan instruksi spesifik untuk mengevaluasi tingkat risiko. Prompt tersebut menginstruksikan Claude untuk merespons dengan objek JSON yang mencakup tingkat risiko, kategori yang dilanggar, dan penjelasan opsional.

Pendekatan ini memungkinkan moderasi konten yang fleksibel dengan menetapkan tingkat risiko. Pendekatan ini dapat diintegrasikan dengan mulus ke dalam sistem yang lebih besar untuk mengotomatiskan penyaringan konten atau menandai komentar untuk ditinjau oleh manusia berdasarkan tingkat risiko yang dinilai. Misalnya, saat menjalankan kode ini, komentar `Delete this post now or you better hide. I am coming after you and your family.` diidentifikasi sebagai berisiko tinggi karena ancamannya yang berbahaya. Sebaliknya, komentar `Stay away from the 5G cellphones!! They are using 5G to control you.` dikategorikan sebagai berisiko sedang.

### Terapkan prompt Anda

Setelah Anda yakin dengan kualitas solusi Anda, saatnya menerapkannya ke produksi. Berikut adalah beberapa praktik terbaik yang harus diikuti saat menggunakan moderasi konten di produksi:

1. **Berikan umpan balik yang jelas kepada pengguna:** Ketika input pengguna diblokir atau respons ditandai karena moderasi konten, berikan umpan balik yang informatif dan konstruktif untuk membantu pengguna memahami mengapa pesan mereka ditandai dan bagaimana mereka dapat menyusun ulang kalimatnya dengan tepat. Dalam contoh kode sebelumnya, hal ini dilakukan melalui bidang `explanation` dalam respons Claude.

2. **Analisis konten yang dimoderasi:** Pantau jenis konten yang ditandai oleh sistem moderasi Anda untuk mengidentifikasi tren dan area potensial untuk perbaikan.

3. **Evaluasi dan tingkatkan secara berkelanjutan:** Nilai kinerja sistem moderasi konten Anda secara berkala menggunakan metrik seperti pelacakan presisi dan recall. Gunakan data ini untuk menyempurnakan prompt moderasi, kata kunci, dan kriteria penilaian Anda secara iteratif.

***

## Tingkatkan kinerja

Dalam skenario yang kompleks, mungkin berguna untuk mempertimbangkan strategi tambahan guna meningkatkan kinerja di luar [teknik rekayasa prompt](/docs/id/build-with-claude/prompt-engineering/overview) standar. Berikut adalah beberapa strategi lanjutan:

### Definisikan topik dan berikan contoh

Selain mencantumkan kategori tidak aman dalam prompt, peningkatan lebih lanjut dapat dilakukan dengan memberikan definisi dan frasa yang terkait dengan setiap kategori.

<CodeGroup exclude="shell">
  ```python Python
  # Kategori yang dianggap tidak aman untuk moderasi konten, beserta definisinya
  unsafe_category_definitions = {
      "Child Exploitation": "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.",
      "Conspiracy Theories": """Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
          which can incite harm or undermine public trust in institutions or facts.""",
      "Hate": """Content that is hateful toward people on the basis of their protected characteristics
          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
          or content that perpetuates negative stereotypes.""",
      "Indiscriminate Weapons": "Content that enables the creation of weapons of mass destruction.",
      "Intellectual Property": "Content that violates the intellectual property rights of third parties.",
      "Non-Violent Crimes": "Content that enables, encourages, or excuses the commission of non-violent crimes.",
      "Privacy": "Content that contains sensitive, personal information about private individuals.",
      "Self-Harm": "Content that enables, encourages, or excuses acts of intentional self-harm.",
      "Sex Crimes": "Content that enables, encourages, or excuses the commission of sex crimes.",
      "Sexual Content": "Content that contains erotic descriptions or explicit depictions of sex acts.",
      "Specialized Advice": """Content that contains financial, medical, or legal advice.
          Financial advice includes guidance on investments, stocks, bonds, or any financial planning.""",
      "Violent Crimes": "Content that enables, encourages, or excuses the commission of violent crimes.",
  }


  def moderate_message_with_definitions(message, unsafe_category_definitions):
      # Format string kategori tidak aman, dengan setiap kategori dan definisinya pada baris baru
      unsafe_category_str = "\n".join(
          f"{category}: {definition}"
          for category, definition in unsafe_category_definitions.items()
      )

      # Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
      assessment_prompt = f"""Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

  Message:
  <message>{message}</message>

  Unsafe Categories and Their Definitions:
  <categories>
  {unsafe_category_str}
  </categories>

  It's important that you remember all unsafe categories and their definitions.

  Respond with ONLY a JSON object, using the format below:
  {{
    "violation": <Boolean field denoting whether the message should be moderated>,
    "categories": [Comma-separated list of violated categories],
    "explanation": [Optional. Only include if there is a violation.]
  }}
  Do not include markdown formatting or code fences in your response."""

      # Kirim permintaan ke Claude untuk moderasi konten
      response = client.messages.create(
          model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
          max_tokens=200,
          messages=[{"role": "user", "content": assessment_prompt}],
      )

      # Parse respons JSON dari Claude
      text_block = next(block for block in response.content if block.type == "text")
      assessment = json.loads(text_block.text)

      # Ekstrak status pelanggaran dari hasil penilaian
      contains_violation = assessment["violation"]

      # Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
      violated_categories = assessment.get("categories", []) if contains_violation else []
      explanation = assessment.get("explanation") if contains_violation else None

      return contains_violation, violated_categories, explanation


  # Proses setiap komentar dan cetak hasilnya
  for comment in user_comments:
      print(f"\nComment: {comment}")
      violation, violated_categories, explanation = moderate_message_with_definitions(
          comment, unsafe_category_definitions
      )

      if violation:
          print(f"Violated Categories: {', '.join(violated_categories)}")
          print(f"Explanation: {explanation}")
      else:
          print("No issues detected.")
  ```

  ```typescript TypeScript
  // Bentuk penilaian JSON yang dikembalikan Claude
  interface DefinitionBasedAssessment {
    violation: boolean;
    categories?: string[];
    explanation?: string;
  }

  // Kategori yang dianggap tidak aman untuk moderasi konten, beserta definisinya
  // (kunci objek mempertahankan urutan penyisipan, sehingga kategori ditampilkan dalam urutan ini)
  const unsafeCategoryDefinitions: Record<string, string> = {
    "Child Exploitation":
      "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.",
    "Conspiracy Theories": `Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
          which can incite harm or undermine public trust in institutions or facts.`,
    "Hate": `Content that is hateful toward people on the basis of their protected characteristics
          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
          or content that perpetuates negative stereotypes.`,
    "Indiscriminate Weapons":
      "Content that enables the creation of weapons of mass destruction.",
    "Intellectual Property":
      "Content that violates the intellectual property rights of third parties.",
    "Non-Violent Crimes":
      "Content that enables, encourages, or excuses the commission of non-violent crimes.",
    "Privacy":
      "Content that contains sensitive, personal information about private individuals.",
    "Self-Harm": "Content that enables, encourages, or excuses acts of intentional self-harm.",
    "Sex Crimes": "Content that enables, encourages, or excuses the commission of sex crimes.",
    "Sexual Content":
      "Content that contains erotic descriptions or explicit depictions of sex acts.",
    "Specialized Advice": `Content that contains financial, medical, or legal advice.
          Financial advice includes guidance on investments, stocks, bonds, or any financial planning.`,
    "Violent Crimes":
      "Content that enables, encourages, or excuses the commission of violent crimes."
  };

  async function moderateMessageWithDefinitions(
    message: string,
    unsafeCategoryDefinitions: Record<string, string>
  ): Promise<{ violation: boolean; violatedCategories: string[]; explanation?: string }> {
    // Format string kategori tidak aman, dengan setiap kategori dan definisinya pada baris baru
    const unsafeCategoryStr = Object.entries(unsafeCategoryDefinitions)
      .map(([category, definition]) => `${category}: ${definition}`)
      .join("\n");

    // Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
    const assessmentPrompt = `Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

  Message:
  <message>${message}</message>

  Unsafe Categories and Their Definitions:
  <categories>
  ${unsafeCategoryStr}
  </categories>

  It's important that you remember all unsafe categories and their definitions.

  Respond with ONLY a JSON object, using the format below:
  {
    "violation": <Boolean field denoting whether the message should be moderated>,
    "categories": [Comma-separated list of violated categories],
    "explanation": [Optional. Only include if there is a violation.]
  }
  Do not include markdown formatting or code fences in your response.`;

    // Kirim permintaan ke Claude untuk moderasi konten
    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001", // Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{ role: "user", content: assessmentPrompt }]
    });

    // Parse respons JSON dari Claude
    const textBlock = response.content.find((block) => block.type === "text");
    if (!textBlock) {
      throw new Error("Expected a text block in the response");
    }
    const assessment: DefinitionBasedAssessment = JSON.parse(textBlock.text);

    // Ekstrak status pelanggaran dari penilaian
    const containsViolation = assessment.violation;

    // Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
    const violatedCategories = containsViolation ? assessment.categories ?? [] : [];
    const explanation = containsViolation ? assessment.explanation : undefined;

    return { violation: containsViolation, violatedCategories, explanation };
  }

  // Proses setiap komentar dan cetak hasilnya
  for (const comment of userComments) {
    console.log(`\nComment: ${comment}`);
    const { violation, violatedCategories, explanation } = await moderateMessageWithDefinitions(
      comment,
      unsafeCategoryDefinitions
    );

    if (violation) {
      console.log(`Violated Categories: ${violatedCategories.join(", ")}`);
      console.log(`Explanation: ${explanation}`);
    } else {
      console.log("No issues detected.");
    }
  }
  ```

  ```csharp C#
  // Kategori yang dianggap tidak aman untuk moderasi konten, beserta definisinya.
  // Entri tetap dalam urutan penyisipan, sehingga prompt yang dihasilkan mencantumkan kategori
  // persis dalam urutan ini.
  (string Category, string Definition)[] unsafeCategoryDefinitions =
  [
      (
          "Child Exploitation",
          "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children."
      ),
      (
          "Conspiracy Theories",
          """
          Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
                  which can incite harm or undermine public trust in institutions or facts.
          """
      ),
      (
          "Hate",
          """
          Content that is hateful toward people on the basis of their protected characteristics
                  (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
                  or content that perpetuates negative stereotypes.
          """
      ),
      ("Indiscriminate Weapons", "Content that enables the creation of weapons of mass destruction."),
      ("Intellectual Property", "Content that violates the intellectual property rights of third parties."),
      ("Non-Violent Crimes", "Content that enables, encourages, or excuses the commission of non-violent crimes."),
      ("Privacy", "Content that contains sensitive, personal information about private individuals."),
      ("Self-Harm", "Content that enables, encourages, or excuses acts of intentional self-harm."),
      ("Sex Crimes", "Content that enables, encourages, or excuses the commission of sex crimes."),
      ("Sexual Content", "Content that contains erotic descriptions or explicit depictions of sex acts."),
      (
          "Specialized Advice",
          """
          Content that contains financial, medical, or legal advice.
                  Financial advice includes guidance on investments, stocks, bonds, or any financial planning.
          """
      ),
      ("Violent Crimes", "Content that enables, encourages, or excuses the commission of violent crimes."),
  ];


  async Task<(bool ContainsViolation, List<string> ViolatedCategories, string? Explanation)> ModerateMessageWithDefinitions(
      string message,
      IReadOnlyList<(string Category, string Definition)> categoryDefinitions
  )
  {
      // Format string kategori tidak aman, dengan setiap kategori dan definisinya pada baris baru
      var unsafeCategoryText = string.Join(
          "\n",
          categoryDefinitions.Select(entry => $"{entry.Category}: {entry.Definition}")
      );

      // Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
      var assessmentPrompt = $$"""
  Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

  Message:
  <message>{{message}}</message>

  Unsafe Categories and Their Definitions:
  <categories>
  {{unsafeCategoryText}}
  </categories>

  It's important that you remember all unsafe categories and their definitions.

  Respond with ONLY a JSON object, using the format below:
  {
    "violation": <Boolean field denoting whether the message should be moderated>,
    "categories": [Comma-separated list of violated categories],
    "explanation": [Optional. Only include if there is a violation.]
  }
  Do not include markdown formatting or code fences in your response.
  """;

      // Kirim permintaan ke Claude untuk moderasi konten
      var response = await client.Messages.Create(
          new()
          {
              Model = Model.ClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
              MaxTokens = 200,
              Messages = [new() { Role = Role.User, Content = assessmentPrompt }],
          }
      );

      // Persempit blok konten pertama menjadi blok teks, lalu parse respons JSON dari Claude
      if (!response.Content[0].TryPickText(out var textBlock))
      {
          throw new InvalidOperationException("Expected a text response from Claude.");
      }
      var assessment = JsonNode.Parse(textBlock.Text)!;

      // Ekstrak status pelanggaran dari hasil penilaian
      var containsViolation = assessment["violation"]!.GetValue<bool>();

      // Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
      List<string> violatedCategories = containsViolation
          ? assessment["categories"]?.AsArray().Select(category => category!.GetValue<string>()).ToList() ?? []
          : [];
      var explanation = containsViolation ? assessment["explanation"]?.GetValue<string>() : null;

      return (containsViolation, violatedCategories, explanation);
  }

  // Proses setiap komentar dan cetak hasilnya
  foreach (var comment in userComments)
  {
      Console.WriteLine($"\nComment: {comment}");
      var (violation, violatedCategories, explanation) = await ModerateMessageWithDefinitions(
          comment,
          unsafeCategoryDefinitions
      );

      if (violation)
      {
          Console.WriteLine($"Violated Categories: {string.Join(", ", violatedCategories)}");
          Console.WriteLine($"Explanation: {explanation}");
      }
      else
      {
          Console.WriteLine("No issues detected.");
      }
  }
  ```

  ```go Go
  // Kategori yang dianggap tidak aman untuk moderasi konten, beserta definisinya.
  // Slice berisi pasangan kategori/definisi (bukan map) menjaga urutan render
  // tetap stabil; map di Go melakukan iterasi dalam urutan acak.
  type categoryDefinition struct {
  	category   string
  	definition string
  }

  var unsafeCategoryDefinitions = []categoryDefinition{
  	{"Child Exploitation", "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children."},
  	{"Conspiracy Theories", `Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
          which can incite harm or undermine public trust in institutions or facts.`},
  	{"Hate", `Content that is hateful toward people on the basis of their protected characteristics
          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
          or content that perpetuates negative stereotypes.`},
  	{"Indiscriminate Weapons", "Content that enables the creation of weapons of mass destruction."},
  	{"Intellectual Property", "Content that violates the intellectual property rights of third parties."},
  	{"Non-Violent Crimes", "Content that enables, encourages, or excuses the commission of non-violent crimes."},
  	{"Privacy", "Content that contains sensitive, personal information about private individuals."},
  	{"Self-Harm", "Content that enables, encourages, or excuses acts of intentional self-harm."},
  	{"Sex Crimes", "Content that enables, encourages, or excuses the commission of sex crimes."},
  	{"Sexual Content", "Content that contains erotic descriptions or explicit depictions of sex acts."},
  	{"Specialized Advice", `Content that contains financial, medical, or legal advice.
          Financial advice includes guidance on investments, stocks, bonds, or any financial planning.`},
  	{"Violent Crimes", "Content that enables, encourages, or excuses the commission of violent crimes."},
  }

  func moderateMessageWithDefinitions(message string, unsafeCategoryDefinitions []categoryDefinition) (bool, []string, string) {
  	// Memformat string kategori tidak aman, dengan setiap kategori dan definisinya pada baris baru
  	categoryLines := make([]string, len(unsafeCategoryDefinitions))
  	for i, entry := range unsafeCategoryDefinitions {
  		categoryLines[i] = fmt.Sprintf("%s: %s", entry.category, entry.definition)
  	}
  	unsafeCategoryStr := strings.Join(categoryLines, "\n")

  	// Menyusun prompt untuk Claude, termasuk pesan dan kategori tidak aman
  	assessmentPrompt := fmt.Sprintf(`Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

  Message:
  <message>%s</message>

  Unsafe Categories and Their Definitions:
  <categories>
  %s
  </categories>

  It's important that you remember all unsafe categories and their definitions.

  Respond with ONLY a JSON object, using the format below:
  {
    "violation": <Boolean field denoting whether the message should be moderated>,
    "categories": [Comma-separated list of violated categories],
    "explanation": [Optional. Only include if there is a violation.]
  }
  Do not include markdown formatting or code fences in your response.`, message, unsafeCategoryStr)

  	// Mengirim permintaan ke Claude untuk moderasi konten
  	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
  		MaxTokens: 200,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(assessmentPrompt)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Mempersempit blok konten pertama menjadi blok teks sebelum membaca teksnya
  	textBlock, ok := response.Content[0].AsAny().(anthropic.TextBlock)
  	if !ok {
  		log.Fatalf("expected a text block, got %q", response.Content[0].Type)
  	}

  	// Mem-parsing respons JSON dari Claude
  	var assessment struct {
  		Violation   bool     `json:"violation"`
  		Categories  []string `json:"categories"`
  		Explanation string   `json:"explanation"`
  	}
  	if err := json.Unmarshal([]byte(textBlock.Text), &assessment); err != nil {
  		log.Fatal(err)
  	}

  	// Jika ada pelanggaran, kembalikan kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
  	if !assessment.Violation {
  		return false, nil, ""
  	}
  	return true, assessment.Categories, assessment.Explanation
  }

  // moderateAllCommentsWithDefinitions memproses setiap komentar dan mencetak hasilnya.
  func moderateAllCommentsWithDefinitions() {
  	for _, comment := range userComments {
  		fmt.Printf("\nComment: %s\n", comment)
  		violation, violatedCategories, explanation := moderateMessageWithDefinitions(comment, unsafeCategoryDefinitions)

  		if violation {
  			fmt.Printf("Violated Categories: %s\n", strings.Join(violatedCategories, ", "))
  			fmt.Printf("Explanation: %s\n", explanation)
  		} else {
  			fmt.Println("No issues detected.")
  		}
  	}
  }

  ```

  ```java Java
  // Kategori yang dianggap tidak aman untuk moderasi konten, beserta definisinya
  record CategoryDefinition(String category, String definition) {}

  final List<CategoryDefinition> unsafeCategoryDefinitions = List.of(
          new CategoryDefinition(
                  "Child Exploitation",
                  "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children."),
          new CategoryDefinition(
                  "Conspiracy Theories",
                  """
                  Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
                          which can incite harm or undermine public trust in institutions or facts."""),
          new CategoryDefinition(
                  "Hate",
                  """
                  Content that is hateful toward people on the basis of their protected characteristics
                          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
                          or content that perpetuates negative stereotypes."""),
          new CategoryDefinition(
                  "Indiscriminate Weapons",
                  "Content that enables the creation of weapons of mass destruction."),
          new CategoryDefinition(
                  "Intellectual Property",
                  "Content that violates the intellectual property rights of third parties."),
          new CategoryDefinition(
                  "Non-Violent Crimes",
                  "Content that enables, encourages, or excuses the commission of non-violent crimes."),
          new CategoryDefinition(
                  "Privacy",
                  "Content that contains sensitive, personal information about private individuals."),
          new CategoryDefinition(
                  "Self-Harm",
                  "Content that enables, encourages, or excuses acts of intentional self-harm."),
          new CategoryDefinition(
                  "Sex Crimes",
                  "Content that enables, encourages, or excuses the commission of sex crimes."),
          new CategoryDefinition(
                  "Sexual Content",
                  "Content that contains erotic descriptions or explicit depictions of sex acts."),
          new CategoryDefinition(
                  "Specialized Advice",
                  """
                  Content that contains financial, medical, or legal advice.
                          Financial advice includes guidance on investments, stocks, bonds, or any financial planning."""),
          new CategoryDefinition(
                  "Violent Crimes",
                  "Content that enables, encourages, or excuses the commission of violent crimes."));

  record ModerationDecision(boolean violation, List<String> violatedCategories, String explanation) {}

  ModerationDecision moderateMessageWithDefinitions(
          String message, List<CategoryDefinition> unsafeCategoryDefinitions)
          throws JsonProcessingException {
      // Format string kategori tidak aman, dengan setiap kategori dan definisinya pada baris baru
      String unsafeCategoryStr = unsafeCategoryDefinitions.stream()
              .map(categoryDefinition ->
                      categoryDefinition.category() + ": " + categoryDefinition.definition())
              .collect(Collectors.joining("\n"));

      // Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
      String assessmentPrompt = """
          Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

          Message:
          <message>%s</message>

          Unsafe Categories and Their Definitions:
          <categories>
          %s
          </categories>

          It's important that you remember all unsafe categories and their definitions.

          Respond with ONLY a JSON object, using the format below:
          {
            "violation": <Boolean field denoting whether the message should be moderated>,
            "categories": [Comma-separated list of violated categories],
            "explanation": [Optional. Only include if there is a violation.]
          }
          Do not include markdown formatting or code fences in your response."""
              .formatted(message, unsafeCategoryStr);

      // Kirim permintaan ke Claude untuk moderasi konten
      Message response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_HAIKU_4_5_20251001) // Using the Haiku model for lower costs
              .maxTokens(200)
              .addUserMessage(assessmentPrompt)
              .build());

      // Parse respons JSON dari Claude
      String assessmentJson = response.content().stream()
              .flatMap(contentBlock -> contentBlock.text().stream())
              .findFirst()
              .orElseThrow()
              .text();
      ObjectMapper mapper = new ObjectMapper();
      JsonNode assessment = mapper.readTree(assessmentJson);

      // Ekstrak status pelanggaran dari hasil penilaian
      boolean containsViolation = assessment.required("violation").asBoolean();

      // Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
      List<String> violatedCategories = containsViolation && assessment.has("categories")
              ? mapper.convertValue(assessment.get("categories"), new TypeReference<List<String>>() {})
              : List.of();
      String explanation = containsViolation && assessment.hasNonNull("explanation")
              ? assessment.get("explanation").asText()
              : null;

      return new ModerationDecision(containsViolation, violatedCategories, explanation);
  }

  // Proses setiap komentar dan cetak hasilnya
  void printModerationResultsWithDefinitions() throws JsonProcessingException {
      for (String comment : userComments) {
          IO.println("\nComment: " + comment);
          ModerationDecision result = moderateMessageWithDefinitions(comment, unsafeCategoryDefinitions);

          if (result.violation()) {
              IO.println("Violated Categories: " + String.join(", ", result.violatedCategories()));
              IO.println("Explanation: " + result.explanation());
          } else {
              IO.println("No issues detected.");
          }
      }
  }
  ```

  ```php PHP
  // Kategori yang dianggap tidak aman untuk moderasi konten, beserta definisinya
  $unsafeCategoryDefinitions = [
      'Child Exploitation' => 'Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.',
      'Conspiracy Theories' => 'Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
          which can incite harm or undermine public trust in institutions or facts.',
      'Hate' => 'Content that is hateful toward people on the basis of their protected characteristics
          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
          or content that perpetuates negative stereotypes.',
      'Indiscriminate Weapons' => 'Content that enables the creation of weapons of mass destruction.',
      'Intellectual Property' => 'Content that violates the intellectual property rights of third parties.',
      'Non-Violent Crimes' => 'Content that enables, encourages, or excuses the commission of non-violent crimes.',
      'Privacy' => 'Content that contains sensitive, personal information about private individuals.',
      'Self-Harm' => 'Content that enables, encourages, or excuses acts of intentional self-harm.',
      'Sex Crimes' => 'Content that enables, encourages, or excuses the commission of sex crimes.',
      'Sexual Content' => 'Content that contains erotic descriptions or explicit depictions of sex acts.',
      'Specialized Advice' => 'Content that contains financial, medical, or legal advice.
          Financial advice includes guidance on investments, stocks, bonds, or any financial planning.',
      'Violent Crimes' => 'Content that enables, encourages, or excuses the commission of violent crimes.',
  ];

  $moderateMessageWithDefinitions = function (string $message, array $unsafeCategoryDefinitions) use ($client): array {
      // Format string kategori tidak aman, dengan setiap kategori dan definisinya pada baris baru
      $categoryLines = [];
      foreach ($unsafeCategoryDefinitions as $category => $definition) {
          $categoryLines[] = "{$category}: {$definition}";
      }
      $unsafeCategoryStr = implode("\n", $categoryLines);

      // Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
      $assessmentPrompt = <<<PROMPT
      Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

      Message:
      <message>{$message}</message>

      Unsafe Categories and Their Definitions:
      <categories>
      {$unsafeCategoryStr}
      </categories>

      It's important that you remember all unsafe categories and their definitions.

      Respond with ONLY a JSON object, using the format below:
      {
        "violation": <Boolean field denoting whether the message should be moderated>,
        "categories": [Comma-separated list of violated categories],
        "explanation": [Optional. Only include if there is a violation.]
      }
      Do not include markdown formatting or code fences in your response.
      PROMPT;

      // Kirim permintaan ke Claude untuk moderasi konten
      $response = $client->messages->create(
          model: 'claude-haiku-4-5-20251001', // Using the Haiku model for lower costs
          maxTokens: 200,
          messages: [['role' => 'user', 'content' => $assessmentPrompt]],
      );

      // Parse respons JSON dari Claude. SDK mendekode setiap blok konten
      // ke kelas konkretnya, jadi cari TextBlock sebelum membaca teksnya.
      $textBlock = array_find($response->content, fn ($block) => $block instanceof TextBlock)
          ?? throw new RuntimeException('Expected a text block in the response.');
      $assessment = json_decode($textBlock->text, associative: true, flags: JSON_THROW_ON_ERROR);

      // Ekstrak status pelanggaran dari hasil penilaian
      $containsViolation = $assessment['violation'];

      // Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
      $violatedCategories = $containsViolation ? ($assessment['categories'] ?? []) : [];
      $explanation = $containsViolation ? ($assessment['explanation'] ?? null) : null;

      return [$containsViolation, $violatedCategories, $explanation];
  };

  // Proses setiap komentar dan cetak hasilnya
  foreach ($userComments as $comment) {
      echo "\nComment: {$comment}\n";
      [$violation, $violatedCategories, $explanation] = $moderateMessageWithDefinitions($comment, $unsafeCategoryDefinitions);

      if ($violation) {
          echo 'Violated Categories: ' . implode(', ', $violatedCategories) . "\n";
          echo "Explanation: {$explanation}\n";
      } else {
          echo "No issues detected.\n";
      }
  }
  ```

  ```ruby Ruby
  # Kategori yang dianggap tidak aman untuk moderasi konten, beserta definisinya
  UNSAFE_CATEGORY_DEFINITIONS = {
    "Child Exploitation" => "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.",
    "Conspiracy Theories" => "Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
          which can incite harm or undermine public trust in institutions or facts.",
    "Hate" => "Content that is hateful toward people on the basis of their protected characteristics
          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
          or content that perpetuates negative stereotypes.",
    "Indiscriminate Weapons" => "Content that enables the creation of weapons of mass destruction.",
    "Intellectual Property" => "Content that violates the intellectual property rights of third parties.",
    "Non-Violent Crimes" => "Content that enables, encourages, or excuses the commission of non-violent crimes.",
    "Privacy" => "Content that contains sensitive, personal information about private individuals.",
    "Self-Harm" => "Content that enables, encourages, or excuses acts of intentional self-harm.",
    "Sex Crimes" => "Content that enables, encourages, or excuses the commission of sex crimes.",
    "Sexual Content" => "Content that contains erotic descriptions or explicit depictions of sex acts.",
    "Specialized Advice" => "Content that contains financial, medical, or legal advice.
          Financial advice includes guidance on investments, stocks, bonds, or any financial planning.",
    "Violent Crimes" => "Content that enables, encourages, or excuses the commission of violent crimes."
  }


  def moderate_message_with_definitions(message, unsafe_category_definitions)
    # Format string kategori tidak aman, dengan setiap kategori dan definisinya pada baris baru
    unsafe_category_str = unsafe_category_definitions
      .map { |category, definition| "#{category}: #{definition}" }
      .join("\n")

    # Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
    assessment_prompt = <<~PROMPT.chomp
      Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

      Message:
      <message>#{message}</message>

      Unsafe Categories and Their Definitions:
      <categories>
      #{unsafe_category_str}
      </categories>

      It's important that you remember all unsafe categories and their definitions.

      Respond with ONLY a JSON object, using the format below:
      {
        "violation": <Boolean field denoting whether the message should be moderated>,
        "categories": [Comma-separated list of violated categories],
        "explanation": [Optional. Only include if there is a violation.]
      }
      Do not include markdown formatting or code fences in your response.
    PROMPT

    # Kirim permintaan ke Claude untuk moderasi konten
    response = CLIENT.messages.create(
      model: "claude-haiku-4-5-20251001", # Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{role: :user, content: assessment_prompt}]
    )

    # Parse respons JSON dari Claude
    text_block = response.content.find { it.type == :text }
    assessment = JSON.parse(text_block.text)

    # Ekstrak status pelanggaran dari hasil penilaian
    contains_violation = assessment["violation"]

    # Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
    violated_categories = contains_violation ? assessment.fetch("categories", []) : []
    explanation = contains_violation ? assessment["explanation"] : nil

    [contains_violation, violated_categories, explanation]
  end


  # Proses setiap komentar dan cetak hasilnya
  USER_COMMENTS.each do |comment|
    puts "\nComment: #{comment}"
    violation, violated_categories, explanation = moderate_message_with_definitions(comment, UNSAFE_CATEGORY_DEFINITIONS)

    if violation
      puts "Violated Categories: #{violated_categories.join(", ")}"
      puts "Explanation: #{explanation}"
    else
      puts "No issues detected."
    end
  end
  ```
</CodeGroup>

Fungsi `moderate_message_with_definitions` memperluas fungsi `moderate_message` sebelumnya dengan memungkinkan setiap kategori tidak aman dipasangkan dengan definisi yang terperinci. Hal ini terjadi dalam kode dengan mengganti koleksi `unsafe_categories` dari fungsi asli dengan pemetaan `unsafe_category_definitions`. Pemetaan ini memasangkan setiap kategori tidak aman dengan definisi yang sesuai. Baik nama kategori maupun definisinya disertakan dalam prompt.

Perlu dicatat, definisi untuk kategori `Specialized Advice` sekarang menentukan jenis nasihat keuangan yang harus dilarang. Akibatnya, komentar `It is a great time to invest in gold!`, yang sebelumnya lolos penilaian `moderate_message`, sekarang memicu pelanggaran.

### Pertimbangkan pemrosesan batch

Untuk mengurangi biaya dalam situasi di mana moderasi real-time tidak diperlukan, pertimbangkan untuk memoderasi pesan secara batch. Sertakan beberapa pesan dalam konteks prompt, dan minta Claude untuk menilai pesan mana yang harus dimoderasi.

<CodeGroup exclude="shell">
  ```python Python
  def batch_moderate_messages(messages, unsafe_categories):
      # Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      unsafe_category_str = "\n".join(unsafe_categories)

      # Format string pesan, dengan setiap pesan dibungkus tag mirip XML dan diberi ID
      messages_str = "\n".join(
          [f"<message id={idx}>{msg}</message>" for idx, msg in enumerate(messages)]
      )

      # Susun prompt untuk Claude, termasuk pesan-pesan dan kategori tidak aman
      assessment_prompt = f"""Determine the messages to moderate, based on the unsafe categories outlined below.

  Messages:
  <messages>
  {messages_str}
  </messages>

  Unsafe Categories:
  <categories>
  {unsafe_category_str}
  </categories>

  Respond with ONLY a JSON object, using the format below:
  {{
    "violations": [
      {{
        "id": <message id>,
        "categories": [list of violated categories],
        "explanation": <Explanation of why there's a violation>
      }}
    ]
  }}

  Important Notes:
  - Remember to analyze every message for a violation.
  - Select any number of violations that reasonably apply.
  - Do not include markdown formatting or code fences in your response."""

      # Kirim permintaan ke Claude untuk moderasi konten
      response = client.messages.create(
          model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
          max_tokens=2048,  # Increased max token count to handle batches
          messages=[{"role": "user", "content": assessment_prompt}],
      )

      # Parse respons JSON dari Claude
      text_block = next(block for block in response.content if block.type == "text")
      assessment = json.loads(text_block.text)
      return assessment


  # Proses batch komentar dan dapatkan responsnya
  response_obj = batch_moderate_messages(user_comments, unsafe_categories)

  # Cetak hasil untuk setiap pelanggaran yang terdeteksi
  for violation in response_obj["violations"]:
      print(f"""Comment: {user_comments[violation["id"]]}
  Violated Categories: {", ".join(violation["categories"])}
  Explanation: {violation["explanation"]}
  """)
  ```

  ```typescript TypeScript
  // Bentuk penilaian batch JSON yang dikembalikan Claude
  interface BatchAssessment {
    violations: {
      id: number;
      categories: string[];
      explanation: string;
    }[];
  }

  async function batchModerateMessages(
    messages: string[],
    unsafeCategories: string[]
  ): Promise<BatchAssessment> {
    // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
    const unsafeCategoryStr = unsafeCategories.join("\n");

    // Format string pesan, dengan setiap pesan dibungkus tag mirip XML dan diberi ID
    const messagesStr = messages
      .map((msg, idx) => `<message id=${idx}>${msg}</message>`)
      .join("\n");

    // Susun prompt untuk Claude, termasuk pesan-pesan dan kategori tidak aman
    const assessmentPrompt = `Determine the messages to moderate, based on the unsafe categories outlined below.

  Messages:
  <messages>
  ${messagesStr}
  </messages>

  Unsafe Categories:
  <categories>
  ${unsafeCategoryStr}
  </categories>

  Respond with ONLY a JSON object, using the format below:
  {
    "violations": [
      {
        "id": <message id>,
        "categories": [list of violated categories],
        "explanation": <Explanation of why there's a violation>
      }
    ]
  }

  Important Notes:
  - Remember to analyze every message for a violation.
  - Select any number of violations that reasonably apply.
  - Do not include markdown formatting or code fences in your response.`;

    // Kirim permintaan ke Claude untuk moderasi konten
    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001", // Using the Haiku model for lower costs
      max_tokens: 2048, // Increased max token count to handle batches
      messages: [{ role: "user", content: assessmentPrompt }]
    });

    // Parse respons JSON dari Claude
    const textBlock = response.content.find((block) => block.type === "text");
    if (!textBlock) {
      throw new Error("Expected a text block in the response");
    }
    const assessment: BatchAssessment = JSON.parse(textBlock.text);
    return assessment;
  }

  // Proses batch komentar dan dapatkan responsnya
  const batchAssessment = await batchModerateMessages(userComments, unsafeCategories);

  // Cetak hasil untuk setiap pelanggaran yang terdeteksi
  for (const violation of batchAssessment.violations) {
    console.log(`Comment: ${userComments[violation.id]}
  Violated Categories: ${violation.categories.join(", ")}
  Explanation: ${violation.explanation}
  `);
  }
  ```

  ```csharp C#
  async Task<JsonNode> BatchModerateMessages(IReadOnlyList<string> messages, IReadOnlyList<string> categories)
  {
      // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      var unsafeCategoryText = string.Join("\n", categories);

      // Format string pesan, dengan setiap pesan dibungkus tag mirip XML dan diberi ID
      var messagesText = string.Join(
          "\n",
          messages.Select((message, index) => $"<message id={index}>{message}</message>")
      );

      // Susun prompt untuk Claude, termasuk pesan-pesan dan kategori tidak aman
      var assessmentPrompt = $$"""
  Determine the messages to moderate, based on the unsafe categories outlined below.

  Messages:
  <messages>
  {{messagesText}}
  </messages>

  Unsafe Categories:
  <categories>
  {{unsafeCategoryText}}
  </categories>

  Respond with ONLY a JSON object, using the format below:
  {
    "violations": [
      {
        "id": <message id>,
        "categories": [list of violated categories],
        "explanation": <Explanation of why there's a violation>
      }
    ]
  }

  Important Notes:
  - Remember to analyze every message for a violation.
  - Select any number of violations that reasonably apply.
  - Do not include markdown formatting or code fences in your response.
  """;

      // Kirim permintaan ke Claude untuk moderasi konten
      var response = await client.Messages.Create(
          new()
          {
              Model = Model.ClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
              MaxTokens = 2048, // Increased max token count to handle batches
              Messages = [new() { Role = Role.User, Content = assessmentPrompt }],
          }
      );

      // Persempit blok konten pertama menjadi blok teks, lalu parse respons JSON dari Claude
      if (!response.Content[0].TryPickText(out var textBlock))
      {
          throw new InvalidOperationException("Expected a text response from Claude.");
      }
      return JsonNode.Parse(textBlock.Text)!;
  }

  // Proses batch komentar dan dapatkan responsnya
  var moderationResults = await BatchModerateMessages(userComments, unsafeCategories);

  // Cetak hasil untuk setiap pelanggaran yang terdeteksi
  foreach (var violation in moderationResults["violations"]!.AsArray())
  {
      var flaggedComment = userComments[violation!["id"]!.GetValue<int>()];
      var violatedCategories = string.Join(
          ", ",
          violation["categories"]!.AsArray().Select(category => category!.GetValue<string>())
      );
      var explanation = violation["explanation"]!.GetValue<string>();

      Console.WriteLine($"""
          Comment: {flaggedComment}
          Violated Categories: {violatedCategories}
          Explanation: {explanation}

          """);
  }
  ```

  ```go Go
  // batchViolation adalah satu entri dalam array "violations" dari Claude: indeks
  // pesan yang melanggar beserta kategori yang dilanggar dan alasannya.
  type batchViolation struct {
  	ID          int      `json:"id"`
  	Categories  []string `json:"categories"`
  	Explanation string   `json:"explanation"`
  }

  func batchModerateMessages(messages []string, unsafeCategories []string) []batchViolation {
  	// Mengonversi kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
  	unsafeCategoryStr := strings.Join(unsafeCategories, "\n")

  	// Memformat string pesan, dengan setiap pesan dibungkus tag mirip XML dan diberi ID
  	messageLines := make([]string, len(messages))
  	for i, message := range messages {
  		messageLines[i] = fmt.Sprintf("<message id=%d>%s</message>", i, message)
  	}
  	messagesStr := strings.Join(messageLines, "\n")

  	// Menyusun prompt untuk Claude, termasuk pesan-pesan dan kategori tidak aman
  	assessmentPrompt := fmt.Sprintf(`Determine the messages to moderate, based on the unsafe categories outlined below.

  Messages:
  <messages>
  %s
  </messages>

  Unsafe Categories:
  <categories>
  %s
  </categories>

  Respond with ONLY a JSON object, using the format below:
  {
    "violations": [
      {
        "id": <message id>,
        "categories": [list of violated categories],
        "explanation": <Explanation of why there's a violation>
      }
    ]
  }

  Important Notes:
  - Remember to analyze every message for a violation.
  - Select any number of violations that reasonably apply.
  - Do not include markdown formatting or code fences in your response.`, messagesStr, unsafeCategoryStr)

  	// Mengirim permintaan ke Claude untuk moderasi konten
  	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
  		MaxTokens: 2048,                                   // Increased max token count to handle batches
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(assessmentPrompt)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Mempersempit blok konten pertama menjadi blok teks sebelum membaca teksnya
  	textBlock, ok := response.Content[0].AsAny().(anthropic.TextBlock)
  	if !ok {
  		log.Fatalf("expected a text block, got %q", response.Content[0].Type)
  	}

  	// Mem-parsing respons JSON dari Claude
  	var assessment struct {
  		Violations []batchViolation `json:"violations"`
  	}
  	if err := json.Unmarshal([]byte(textBlock.Text), &assessment); err != nil {
  		log.Fatal(err)
  	}
  	return assessment.Violations
  }

  // moderateAllCommentsAsBatch memoderasi seluruh batch komentar dalam satu
  // permintaan dan mencetak hasil untuk setiap pelanggaran yang terdeteksi.
  func moderateAllCommentsAsBatch() {
  	// Memproses batch komentar dan mendapatkan respons
  	violations := batchModerateMessages(userComments, unsafeCategories)

  	// Mencetak hasil untuk setiap pelanggaran yang terdeteksi
  	for _, violation := range violations {
  		fmt.Printf(`Comment: %s
  Violated Categories: %s
  Explanation: %s

  `, userComments[violation.ID], strings.Join(violation.Categories, ", "), violation.Explanation)
  	}
  }

  ```

  ```java Java
  JsonNode batchModerateMessages(List<String> messages, List<String> unsafeCategories)
          throws JsonProcessingException {
      // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      String unsafeCategoryStr = String.join("\n", unsafeCategories);

      // Format string pesan, dengan setiap pesan dibungkus tag mirip XML dan diberi ID
      String messagesStr = IntStream.range(0, messages.size())
              .mapToObj(idx -> "<message id=%d>%s</message>".formatted(idx, messages.get(idx)))
              .collect(Collectors.joining("\n"));

      // Susun prompt untuk Claude, termasuk pesan-pesan dan kategori tidak aman
      String assessmentPrompt = """
          Determine the messages to moderate, based on the unsafe categories outlined below.

          Messages:
          <messages>
          %s
          </messages>

          Unsafe Categories:
          <categories>
          %s
          </categories>

          Respond with ONLY a JSON object, using the format below:
          {
            "violations": [
              {
                "id": <message id>,
                "categories": [list of violated categories],
                "explanation": <Explanation of why there's a violation>
              }
            ]
          }

          Important Notes:
          - Remember to analyze every message for a violation.
          - Select any number of violations that reasonably apply.
          - Do not include markdown formatting or code fences in your response."""
              .formatted(messagesStr, unsafeCategoryStr);

      // Kirim permintaan ke Claude untuk moderasi konten
      Message response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_HAIKU_4_5_20251001) // Using the Haiku model for lower costs
              .maxTokens(2048) // Increased max token count to handle batches
              .addUserMessage(assessmentPrompt)
              .build());

      // Parse respons JSON dari Claude
      String assessmentJson = response.content().stream()
              .flatMap(contentBlock -> contentBlock.text().stream())
              .findFirst()
              .orElseThrow()
              .text();
      return new ObjectMapper().readTree(assessmentJson);
  }

  // Proses batch komentar dan cetak hasil untuk setiap pelanggaran yang terdeteksi
  void printBatchViolations() throws JsonProcessingException {
      JsonNode response = batchModerateMessages(userComments, unsafeCategories);

      ObjectMapper mapper = new ObjectMapper();
      for (JsonNode violation : response.required("violations")) {
          List<String> violatedCategories =
                  mapper.convertValue(violation.required("categories"), new TypeReference<List<String>>() {});
          IO.println("""
                  Comment: %s
                  Violated Categories: %s
                  Explanation: %s
                  """.formatted(
                          userComments.get(violation.required("id").asInt()),
                          String.join(", ", violatedCategories),
                          violation.required("explanation").asText()));
      }
  }
  ```

  ```php PHP
  $batchModerateMessages = function (array $messages, array $unsafeCategories) use ($client): array {
      // Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
      $unsafeCategoryStr = implode("\n", $unsafeCategories);

      // Format string pesan, dengan setiap pesan dibungkus tag mirip XML dan diberi ID
      $messageLines = [];
      foreach ($messages as $idx => $msg) {
          $messageLines[] = "<message id={$idx}>{$msg}</message>";
      }
      $messagesStr = implode("\n", $messageLines);

      // Susun prompt untuk Claude, termasuk pesan-pesan dan kategori tidak aman
      $assessmentPrompt = <<<PROMPT
      Determine the messages to moderate, based on the unsafe categories outlined below.

      Messages:
      <messages>
      {$messagesStr}
      </messages>

      Unsafe Categories:
      <categories>
      {$unsafeCategoryStr}
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {
        "violations": [
          {
            "id": <message id>,
            "categories": [list of violated categories],
            "explanation": <Explanation of why there's a violation>
          }
        ]
      }

      Important Notes:
      - Remember to analyze every message for a violation.
      - Select any number of violations that reasonably apply.
      - Do not include markdown formatting or code fences in your response.
      PROMPT;

      // Kirim permintaan ke Claude untuk moderasi konten
      $response = $client->messages->create(
          model: 'claude-haiku-4-5-20251001', // Using the Haiku model for lower costs
          maxTokens: 2048, // Increased max token count to handle batches
          messages: [['role' => 'user', 'content' => $assessmentPrompt]],
      );

      // Parse respons JSON dari Claude. SDK mendekode setiap blok konten
      // ke kelas konkretnya, jadi cari TextBlock sebelum membaca teksnya.
      $textBlock = array_find($response->content, fn ($block) => $block instanceof TextBlock)
          ?? throw new RuntimeException('Expected a text block in the response.');

      return json_decode($textBlock->text, associative: true, flags: JSON_THROW_ON_ERROR);
  };

  // Proses batch komentar dan dapatkan responsnya
  $responseObj = $batchModerateMessages($userComments, $unsafeCategories);

  // Cetak hasil untuk setiap pelanggaran yang terdeteksi
  foreach ($responseObj['violations'] as $violation) {
      echo "Comment: {$userComments[$violation['id']]}\n";
      echo 'Violated Categories: ' . implode(', ', $violation['categories']) . "\n";
      echo "Explanation: {$violation['explanation']}\n\n";
  }
  ```

  ```ruby Ruby
  def batch_moderate_messages(messages, unsafe_categories)
    # Ubah kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
    unsafe_category_str = unsafe_categories.join("\n")

    # Format string pesan, dengan setiap pesan dibungkus tag mirip XML dan diberi ID
    messages_str = messages
      .map.with_index { |message, index| "<message id=#{index}>#{message}</message>" }
      .join("\n")

    # Susun prompt untuk Claude, termasuk pesan-pesan dan kategori tidak aman
    assessment_prompt = <<~PROMPT.chomp
      Determine the messages to moderate, based on the unsafe categories outlined below.

      Messages:
      <messages>
      #{messages_str}
      </messages>

      Unsafe Categories:
      <categories>
      #{unsafe_category_str}
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {
        "violations": [
          {
            "id": <message id>,
            "categories": [list of violated categories],
            "explanation": <Explanation of why there's a violation>
          }
        ]
      }

      Important Notes:
      - Remember to analyze every message for a violation.
      - Select any number of violations that reasonably apply.
      - Do not include markdown formatting or code fences in your response.
    PROMPT

    # Kirim permintaan ke Claude untuk moderasi konten
    response = CLIENT.messages.create(
      model: "claude-haiku-4-5-20251001", # Using the Haiku model for lower costs
      max_tokens: 2048, # Increased max token count to handle batches
      messages: [{role: :user, content: assessment_prompt}]
    )

    # Parse respons JSON dari Claude
    text_block = response.content.find { it.type == :text }
    JSON.parse(text_block.text)
  end


  # Proses batch komentar dan dapatkan responsnya
  response_obj = batch_moderate_messages(USER_COMMENTS, UNSAFE_CATEGORIES)

  # Cetak hasil untuk setiap pelanggaran yang terdeteksi
  response_obj["violations"].each do |violation|
    puts <<~RESULT
      Comment: #{USER_COMMENTS[violation["id"]]}
      Violated Categories: #{violation["categories"].join(", ")}
      Explanation: #{violation["explanation"]}

    RESULT
  end
  ```
</CodeGroup>

Dalam contoh ini, fungsi `batch_moderate_messages` menangani moderasi seluruh batch pesan dengan satu panggilan API Claude. Di dalam fungsi tersebut, sebuah prompt dibuat yang mencakup daftar pesan yang akan dievaluasi dan kategori konten tidak aman. Prompt tersebut mengarahkan Claude untuk mengembalikan objek JSON yang mencantumkan semua pesan yang mengandung pelanggaran. Setiap pesan dalam respons diidentifikasi berdasarkan `id`-nya, yang sesuai dengan posisi pesan dalam batch. Perlu diingat bahwa menemukan ukuran batch yang optimal untuk kebutuhan spesifik Anda mungkin memerlukan beberapa eksperimen. Meskipun ukuran batch yang lebih besar dapat menurunkan biaya, hal itu juga dapat menyebabkan sedikit penurunan kualitas. Selain itu, Anda mungkin perlu meningkatkan parameter `max_tokens` dalam panggilan API Claude untuk mengakomodasi respons yang lebih panjang. Untuk detail tentang jumlah maksimum token yang dapat dihasilkan oleh model pilihan Anda, lihat [tabel perbandingan model](/docs/id/about-claude/models/overview#latest-models-comparison).

<CardGroup cols={2}>
  <Card title="Cookbook moderasi konten" icon="link" href="https://platform.claude.com/cookbook/misc-building-moderation-filter">
    Lihat contoh berbasis kode yang diimplementasikan sepenuhnya tentang cara menggunakan Claude untuk moderasi konten.
  </Card>

  <Card title="Panduan guardrails" icon="link" href="/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations">
    Jelajahi panduan guardrails untuk teknik memoderasi interaksi dengan Claude.
  </Card>
</CardGroup>
