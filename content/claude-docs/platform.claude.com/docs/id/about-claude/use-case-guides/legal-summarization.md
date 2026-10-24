---
source: platform
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/legal-summarization
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: 757756e796a889957e274369640c5ab24e753b7f6c753db8097b2e4b241fa39f
---

---
title: Peringkasan hukum
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/legal-summarization
description: Panduan ini menjelaskan cara menggunakan kemampuan pemrosesan bahasa alami Claude yang canggih untuk meringkas dokumen hukum secara efisien, mengekstrak informasi penting, dan mempercepat riset hukum. Dengan Claude, Anda dapat menyederhanakan peninjauan kontrak, persiapan litigasi, dan pekerjaan regulasi, sehingga menghemat waktu dan memastikan akurasi dalam proses hukum Anda.
---

> Kunjungi [resep peringkasan](https://platform.claude.com/cookbook/capabilities-summarization-guide) di Claude Cookbook untuk melihat contoh implementasi peringkasan dokumen hukum menggunakan Claude.

## Sebelum membangun dengan Claude

### Tentukan apakah akan menggunakan Claude untuk peringkasan hukum

Berikut adalah beberapa indikator utama bahwa Anda sebaiknya menggunakan "large language model" (model bahasa besar), atau LLM, seperti Claude untuk meringkas dokumen hukum:

<AccordionGroup>
  <Accordion title="Anda ingin meninjau dokumen dalam jumlah besar secara efisien dan terjangkau">
    Peninjauan dokumen berskala besar dapat memakan waktu dan biaya jika dilakukan secara manual. Claude dapat memproses dan meringkas dokumen hukum dalam jumlah sangat besar dengan cepat, sehingga secara signifikan mengurangi waktu dan biaya yang terkait dengan peninjauan dokumen. Kemampuan ini sangat berharga untuk tugas-tugas seperti uji tuntas (due diligence), analisis kontrak, atau penemuan bukti litigasi, di mana efisiensi sangat penting.
  </Accordion>

  <Accordion title="Anda memerlukan ekstraksi metadata penting secara otomatis">
    Claude dapat secara efisien mengekstrak dan mengategorikan metadata penting dari dokumen hukum, seperti pihak-pihak yang terlibat, tanggal, ketentuan kontrak, atau klausul tertentu. Ekstraksi otomatis ini dapat membantu mengatur informasi, sehingga lebih mudah untuk mencari, menganalisis, dan mengelola kumpulan dokumen yang besar. Hal ini sangat berguna untuk manajemen kontrak, pemeriksaan kepatuhan, atau pembuatan basis data informasi hukum yang dapat dicari. 
  </Accordion>

  <Accordion title="Anda ingin menghasilkan ringkasan yang jelas, ringkas, dan terstandarisasi">
    Claude dapat menghasilkan ringkasan terstruktur yang mengikuti format yang telah ditentukan sebelumnya, sehingga memudahkan profesional hukum untuk dengan cepat memahami poin-poin penting dari berbagai dokumen. Ringkasan terstandarisasi ini dapat meningkatkan keterbacaan, memudahkan perbandingan antar dokumen, dan meningkatkan pemahaman secara keseluruhan, terutama ketika berhadapan dengan bahasa hukum yang kompleks atau jargon teknis.
  </Accordion>

  <Accordion title="Anda memerlukan sitasi yang tepat untuk ringkasan Anda">
    Saat membuat ringkasan hukum, atribusi dan sitasi yang tepat sangat penting untuk memastikan kredibilitas dan kepatuhan terhadap standar hukum. Claude dapat diberi prompt untuk menyertakan sitasi yang akurat untuk semua poin hukum yang dirujuk, sehingga memudahkan profesional hukum untuk meninjau dan memverifikasi informasi yang diringkas.
  </Accordion>

  <Accordion title="Anda ingin menyederhanakan dan mempercepat proses riset hukum Anda">
    Claude dapat membantu riset hukum dengan cepat menganalisis sejumlah besar yurisprudensi, undang-undang, dan komentar hukum. Claude dapat mengidentifikasi preseden yang relevan, mengekstrak prinsip-prinsip hukum utama, dan meringkas argumen hukum yang kompleks. Kemampuan ini dapat secara signifikan mempercepat proses riset, sehingga para profesional hukum dapat berfokus pada analisis tingkat tinggi dan pengembangan strategi.
  </Accordion>
</AccordionGroup>

### Tentukan detail yang ingin Anda ekstrak dari peringkasan

Tidak ada satu ringkasan yang benar untuk dokumen apa pun. Tanpa arahan yang jelas, Claude mungkin kesulitan menentukan detail mana yang harus disertakan. Untuk mencapai hasil yang optimal, identifikasi informasi spesifik yang ingin Anda sertakan dalam ringkasan.

Misalnya, saat meringkas perjanjian sewa-ulang (sublease agreement), Anda mungkin ingin mengekstrak poin-poin penting berikut:

<CodeGroup exclude="shell">
  ```python Python
  details_to_extract = [
      "Parties involved (sublessor, sublessee, and original lessor)",
      "Property details (address, description, and permitted use)",
      "Term and rent (start date, end date, monthly rent, and security deposit)",
      "Responsibilities (utilities, maintenance, and repairs)",
      "Consent and notices (landlord's consent, and notice requirements)",
      "Special provisions (furniture, parking, and subletting restrictions)",
  ]
  ```

  ```typescript TypeScript
  const detailsToExtract = [
    "Parties involved (sublessor, sublessee, and original lessor)",
    "Property details (address, description, and permitted use)",
    "Term and rent (start date, end date, monthly rent, and security deposit)",
    "Responsibilities (utilities, maintenance, and repairs)",
    "Consent and notices (landlord's consent, and notice requirements)",
    "Special provisions (furniture, parking, and subletting restrictions)"
  ];
  ```

  ```csharp C#
  List<string> detailsToExtract =
  [
      "Parties involved (sublessor, sublessee, and original lessor)",
      "Property details (address, description, and permitted use)",
      "Term and rent (start date, end date, monthly rent, and security deposit)",
      "Responsibilities (utilities, maintenance, and repairs)",
      "Consent and notices (landlord's consent, and notice requirements)",
      "Special provisions (furniture, parking, and subletting restrictions)",
  ];
  ```

  ```go Go
  var detailsToExtract = []string{
  	"Parties involved (sublessor, sublessee, and original lessor)",
  	"Property details (address, description, and permitted use)",
  	"Term and rent (start date, end date, monthly rent, and security deposit)",
  	"Responsibilities (utilities, maintenance, and repairs)",
  	"Consent and notices (landlord's consent, and notice requirements)",
  	"Special provisions (furniture, parking, and subletting restrictions)",
  }
  ```

  ```java Java
  List<String> detailsToExtract = List.of(
      "Parties involved (sublessor, sublessee, and original lessor)",
      "Property details (address, description, and permitted use)",
      "Term and rent (start date, end date, monthly rent, and security deposit)",
      "Responsibilities (utilities, maintenance, and repairs)",
      "Consent and notices (landlord's consent, and notice requirements)",
      "Special provisions (furniture, parking, and subletting restrictions)");
  ```

  ```php PHP
  $detailsToExtract = [
      'Parties involved (sublessor, sublessee, and original lessor)',
      'Property details (address, description, and permitted use)',
      'Term and rent (start date, end date, monthly rent, and security deposit)',
      'Responsibilities (utilities, maintenance, and repairs)',
      "Consent and notices (landlord's consent, and notice requirements)",
      'Special provisions (furniture, parking, and subletting restrictions)',
  ];
  ```

  ```ruby Ruby
  details_to_extract = [
    "Parties involved (sublessor, sublessee, and original lessor)",
    "Property details (address, description, and permitted use)",
    "Term and rent (start date, end date, monthly rent, and security deposit)",
    "Responsibilities (utilities, maintenance, and repairs)",
    "Consent and notices (landlord's consent, and notice requirements)",
    "Special provisions (furniture, parking, and subletting restrictions)"
  ]
  ```
</CodeGroup>

### Tetapkan kriteria keberhasilan

Mengevaluasi kualitas ringkasan adalah tugas yang terkenal sulit. Tidak seperti banyak tugas pemrosesan bahasa alami lainnya, evaluasi ringkasan sering kali tidak memiliki metrik yang jelas dan objektif. Prosesnya bisa sangat subjektif, dengan pembaca yang berbeda menghargai aspek ringkasan yang berbeda pula. Berikut adalah kriteria yang mungkin ingin Anda pertimbangkan saat menilai seberapa baik Claude melakukan peringkasan dokumen hukum.

<AccordionGroup>
  <Accordion title="Kebenaran faktual">
    Ringkasan harus secara akurat merepresentasikan fakta, konsep hukum, dan poin-poin penting dalam dokumen.
  </Accordion>

  <Accordion title="Ketepatan hukum">
    Terminologi dan rujukan ke undang-undang, yurisprudensi, atau peraturan harus benar dan selaras dengan standar hukum.
  </Accordion>

  <Accordion title="Keringkasan">
     Ringkasan harus memadatkan dokumen hukum menjadi poin-poin esensialnya tanpa kehilangan detail penting.
  </Accordion>

  <Accordion title="Konsistensi">
    Jika meringkas beberapa dokumen, LLM harus mempertahankan struktur dan pendekatan yang konsisten untuk setiap ringkasan.
  </Accordion>

  <Accordion title="Keterbacaan">
    Teks harus jelas dan mudah dipahami. Jika audiensnya bukan ahli hukum, ringkasan tidak boleh menyertakan jargon hukum yang dapat membingungkan audiens.
  </Accordion>

  <Accordion title="Bias dan keadilan">
    Ringkasan harus menyajikan gambaran yang tidak bias dan adil atas argumen dan posisi hukum.
  </Accordion>
</AccordionGroup>

Lihat panduan tentang [menetapkan kriteria keberhasilan](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests) untuk informasi lebih lanjut.

***

## Cara meringkas dokumen hukum menggunakan Claude

### Pilih model Claude yang tepat

Akurasi model sangat penting saat meringkas dokumen hukum. Claude Opus 5.5 adalah pilihan yang sangat baik untuk kasus penggunaan seperti ini yang memerlukan akurasi tinggi. Jika ukuran dan jumlah dokumen Anda besar sehingga biaya mulai menjadi perhatian, Anda juga dapat mencoba menggunakan model yang lebih kecil seperti Claude Haiku 5.5.

Untuk membantu memperkirakan biaya ini, berikut adalah perbandingan biaya untuk meringkas 1.000 perjanjian sewa-ulang menggunakan model Opus dan Haiku:

* **Ukuran konten**

  * Jumlah perjanjian: 1.000
  * Karakter per perjanjian: 300.000
  * Total karakter: 300 juta

* **Perkiraan token**

  * Token input: 108 juta, sekitar 108.000 per perjanjian (sekitar 1 token per 2,8 karakter, rasio yang ditunjukkan kedua model pada contoh perjanjian dalam panduan ini)
  * Token output per ringkasan, termasuk token pemikiran apa pun, yang ditagih sebagai output: sekitar 6.200 pada Claude Opus 5.5 dan 3.100 pada Claude Haiku 5.5
  * Total token output: 6,2 juta pada Claude Opus 5.5 dan 3,1 juta pada Claude Haiku 5.5

* **Perkiraan biaya Claude Opus 5.5**

  * Biaya token input: 108 MTok \* $4,00/MTok = $432,00 USD
  * Biaya token output: 6,2 MTok \* $20,00/MTok = $124,00 USD
  * Total biaya: $432,00 + $124,00 = $556,00 USD

* **Perkiraan biaya Claude Haiku 5.5**, dengan harganya untuk prompt di atas 100.000 token

  * Biaya token input: 108 MTok \* $0,50/MTok = $54,00 USD
  * Biaya token output: 3,1 MTok \* $2,50/MTok = $7,75 USD
  * Total biaya: $54,00 + $7,75 = $61,75 USD

<Tip>
  Biaya sebenarnya mungkin berbeda dari perkiraan ini. Jumlah token berasal dari menjalankan contoh di bagian 

  [Bangun prompt yang kuat](https://platform.claude.com/docs/id/about-claude/use-case-guides/legal-summarization#build-a-strong-prompt)

   pada contoh perjanjian dalam panduan ini, sekitar 105.000 token input, dan panjang output bervariasi tergantung dokumen dan dari satu eksekusi ke eksekusi lainnya. Setiap perjanjian di sini adalah satu prompt berukuran sekitar 108.000 token, melebihi ambang 100.000 token untuk 

  [harga prompt panjang](https://platform.claude.com/docs/id/about-claude/pricing#long-context-pricing)

   Claude Haiku 5.5. Dokumen yang prompt-nya tetap pada atau di bawah 100.000 token dikenakan biaya $0,10 / $0,50 USD per juta token input / output sebagai gantinya. Untuk melihat harga mana yang berlaku, hitung dokumen Anda dengan 

  [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting)

   dan 

  `model`

   diatur ke 

  `claude-haiku-5-5`

  .
</Tip>

### Ubah dokumen ke dalam format yang dapat diproses Claude

Sebelum Anda mulai meringkas dokumen, Anda perlu menyiapkan data Anda. Ini melibatkan ekstraksi teks dari PDF, pembersihan teks, dan memastikan teks siap diproses oleh Claude.

Berikut adalah demonstrasi proses ini pada sebuah PDF contoh:

<CodeGroup exclude="shell">
  <CodeGroupItem language="cURL">
    Ekstrak teks dari PDF di dalam kode.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Ekstrak teks dari PDF di dalam kode.
  </CodeGroupItem>

  ```python Python
  from io import BytesIO
  import re

  import pypdf
  import requests


  def get_llm_text(pdf_file):
      reader = pypdf.PdfReader(pdf_file)
      text = "\n".join([page.extract_text() for page in reader.pages])

      # Hapus nomor halaman
      text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

      # Hapus spasi berlebih
      text = re.sub(r"\s+", " ", text)

      return text


  # Buat URL lengkap dari repositori GitHub
  url = "https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/capabilities/summarization/data/Sample Sublease Agreement.pdf"
  url = url.replace(" ", "%20")

  # Unduh file PDF ke dalam memori
  response = requests.get(url)

  # Muat PDF dari memori
  pdf_file = BytesIO(response.content)

  document_text = get_llm_text(pdf_file)
  print(document_text[:50000])
  ```

  ```typescript TypeScript
  import { PDFParse } from "pdf-parse";

  async function getLlmText(pdfData: Uint8Array): Promise<string> {
    const parser = new PDFParse({ data: pdfData });
    const result = await parser.getText();
    await parser.destroy();
    let text = result.pages.map((page) => page.text).join("\n");

    // Hapus nomor halaman
    text = text.replace(/\n\s*\d+\s*\n/g, "\n");

    // Hapus spasi berlebih
    text = text.replace(/\s+/g, " ");

    return text;
  }

  // Unduh contoh perjanjian sewa ulang dari resep ringkasan di Claude Cookbook
  const response = await fetch(
    "https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/capabilities/summarization/data/Sample%20Sublease%20Agreement.pdf"
  );
  const pdfData = new Uint8Array(await response.arrayBuffer());

  const documentText = await getLlmText(pdfData);
  console.log(documentText.slice(0, 50000));
  ```

  ```csharp C#
  using System.Text.RegularExpressions;
  using UglyToad.PdfPig;
  using UglyToad.PdfPig.DocumentLayoutAnalysis.TextExtractor;

  string GetLlmText(byte[] pdfData)
  {
      using var document = PdfDocument.Open(pdfData);
      var text = string.Join("\n", document.GetPages().Select(page => ContentOrderTextExtractor.GetText(page)));

      // Hapus nomor halaman
      text = Regex.Replace(text, @"\n\s*\d+\s*\n", "\n");

      // Hapus spasi berlebih
      text = Regex.Replace(text, @"\s+", " ");

      return text;
  }

  // Unduh contoh perjanjian sewa ulang dari resep ringkasan di Claude Cookbook
  using var httpClient = new HttpClient();
  var pdfData = await httpClient.GetByteArrayAsync(
      "https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/capabilities/summarization/data/Sample%20Sublease%20Agreement.pdf"
  );

  var documentText = GetLlmText(pdfData);
  Console.WriteLine(documentText[..Math.Min(50000, documentText.Length)]);
  ```

  ```go Go
  import (
  	"bytes"
  	"io"
  	"net/http"
  	"regexp"

  	"github.com/ledongthuc/pdf"
  )

  // Teks contoh perjanjian sewa ulang (sublease)
  var documentText string

  func getLLMText(pdfData []byte) (string, error) {
  	reader, err := pdf.NewReader(bytes.NewReader(pdfData), int64(len(pdfData)))
  	if err != nil {
  		return "", err
  	}

  	var pages []string
  	for pageIndex := 1; pageIndex <= reader.NumPage(); pageIndex++ {
  		pageText, err := reader.Page(pageIndex).GetPlainText(nil)
  		if err != nil {
  			return "", err
  		}
  		pages = append(pages, pageText)
  	}
  	text := strings.Join(pages, "\n")

  	// Hapus nomor halaman
  	text = regexp.MustCompile(`\n\s*\d+\s*\n`).ReplaceAllString(text, "\n")

  	// Hapus spasi berlebih
  	text = regexp.MustCompile(`\s+`).ReplaceAllString(text, " ")

  	return text, nil
  }

  // extractDocumentText mengunduh contoh perjanjian sewa ulang dan mengekstrak teksnya.
  func extractDocumentText() {
  	// Unduh contoh perjanjian sewa ulang dari resep ringkasan di Claude Cookbook
  	response, err := http.Get("https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/capabilities/summarization/data/Sample%20Sublease%20Agreement.pdf")
  	if err != nil {
  		log.Fatal(err)
  	}
  	defer response.Body.Close()

  	pdfData, err := io.ReadAll(response.Body)
  	if err != nil {
  		log.Fatal(err)
  	}

  	documentText, err = getLLMText(pdfData)
  	if err != nil {
  		log.Fatal(err)
  	}
  	fmt.Println(documentText[:min(50000, len(documentText))])
  }
  ```

  ```java Java
  import java.io.IOException;
  import java.net.URI;
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;
  import org.apache.pdfbox.Loader;
  import org.apache.pdfbox.pdmodel.PDDocument;
  import org.apache.pdfbox.text.PDFTextStripper;

  // Teks contoh perjanjian sewa ulang (sublease)
  String documentText;

  String getLlmText(byte[] pdfData) throws IOException {
      try (PDDocument document = Loader.loadPDF(pdfData)) {
          String text = new PDFTextStripper().getText(document);

          // Hapus nomor halaman
          text = text.replaceAll("\\n\\s*\\d+\\s*\\n", "\n");

          // Hapus spasi berlebih
          return text.replaceAll("\\s+", " ");
      }
  }

  void extractDocumentText() throws IOException, InterruptedException {
      // Unduh contoh perjanjian sewa ulang dari resep ringkasan di Claude Cookbook
      HttpRequest request = HttpRequest.newBuilder(URI.create(
              "https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/capabilities/summarization/data/Sample%20Sublease%20Agreement.pdf"))
          .build();
      byte[] pdfData;
      try (HttpClient httpClient = HttpClient.newHttpClient()) {
          pdfData = httpClient.send(request, HttpResponse.BodyHandlers.ofByteArray()).body();
      }

      documentText = getLlmText(pdfData);
      IO.println(documentText.substring(0, Math.min(50000, documentText.length())));
  }
  ```

  ```php PHP
  use Smalot\PdfParser\Parser;

  $getLlmText = function (string $pdfData): string {
      $document = (new Parser())->parseContent($pdfData);
      $text = implode("\n", array_map(fn ($page) => $page->getText(), $document->getPages()));

      // Hapus nomor halaman
      $text = preg_replace('/\n\s*\d+\s*\n/', "\n", $text);

      // Hapus spasi berlebih
      return preg_replace('/\s+/', ' ', $text);
  };

  // Unduh contoh perjanjian sewa ulang dari resep ringkasan di Claude Cookbook
  $pdfData = file_get_contents(
      'https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/capabilities/summarization/data/Sample%20Sublease%20Agreement.pdf'
  );

  $documentText = $getLlmText($pdfData);
  echo substr($documentText, 0, 50000) . "\n";
  ```

  ```ruby Ruby
  require "net/http"
  require "pdf-reader"
  require "stringio"

  def get_llm_text(pdf_data)
    reader = PDF::Reader.new(StringIO.new(pdf_data))
    text = reader.pages.map(&:text).join("\n")

    # Hapus nomor halaman
    text = text.gsub(/\n\s*\d+\s*\n/, "\n")

    # Hapus spasi berlebih
    text.gsub(/\s+/, " ")
  end

  # Unduh contoh perjanjian sewa ulang dari resep ringkasan di Claude Cookbook
  pdf_data = Net::HTTP.get(
    URI("https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/capabilities/summarization/data/Sample%20Sublease%20Agreement.pdf")
  )

  document_text = get_llm_text(pdf_data)
  puts document_text[0, 50_000]
  ```
</CodeGroup>

Dalam contoh ini, Anda terlebih dahulu mengunduh PDF contoh perjanjian sewa ulang yang digunakan dalam [resep peringkasan](https://platform.claude.com/cookbook/capabilities-summarization-guide) di Claude Cookbook. Perjanjian ini bersumber dari perjanjian sewa ulang yang tersedia untuk publik dari [situs web sec.gov](https://www.sec.gov/Archives/edgar/data/1045425/000119312507044370/dex1032.htm).

Contoh ini menggunakan pustaka `pypdf` (typescript: `pdf-parse`; csharp: `PdfPig`; go: `github.com/ledongthuc/pdf`; java: `org.apache.pdfbox:pdfbox`; php: `smalot/pdfparser`; ruby: `pdf-reader`) untuk mengekstrak isi PDF dan mengubahnya menjadi teks. Data teks kemudian dibersihkan dengan menghapus nomor halaman dan spasi berlebih.

### Buat prompt yang kuat

Claude dapat beradaptasi dengan berbagai gaya peringkasan. Anda dapat mengubah detail prompt untuk mengarahkan Claude agar lebih atau kurang panjang lebar, menyertakan lebih banyak atau lebih sedikit terminologi teknis, atau memberikan ringkasan konteks yang lebih umum atau lebih terperinci.

Berikut adalah contoh cara membuat prompt yang memastikan ringkasan yang dihasilkan mengikuti struktur yang konsisten saat menganalisis perjanjian sewa-ulang:

<CodeGroup exclude="shell">
  <CodeGroupItem language="cURL">
    Alur kerja ini memerlukan logika lebih dari sekadar satu perintah shell. Gunakan Claude SDK untuk menjalankannya.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Alur kerja ini memerlukan logika lebih dari sekadar satu perintah shell. Gunakan Claude SDK untuk menjalankannya.
  </CodeGroupItem>

  ```python Python
  # Inisialisasi klien Anthropic
  client = anthropic.Anthropic()


  def summarize_document(
      text, details_to_extract, model="claude-opus-5-5", max_tokens=16000
  ):
      # Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
      details_to_extract_str = "\n".join(details_to_extract)

      # Minta model meringkas perjanjian sewa ulang (sublease)
      prompt = f"""Summarize the following sublease agreement. Focus on these key aspects:

      {details_to_extract_str}

      Provide the summary in bullet points nested within the XML header for each section. For example:

      <parties involved>
      - Sublessor: [Name]
      // Add more details as needed
      </parties involved>

      If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.

      Sublease agreement text:
      {text}
      """

      response = client.messages.create(
          model=model,
          max_tokens=max_tokens,
          system="You are a legal analyst specializing in real estate law, known for highly accurate and detailed summaries of sublease agreements.",
          messages=[
              {"role": "user", "content": prompt},
          ],
      )

      return next(block.text for block in response.content if block.type == "text")


  sublease_summary = summarize_document(document_text, details_to_extract)
  print(sublease_summary)
  ```

  ```typescript TypeScript
  // Inisialisasi klien Anthropic
  const client = new Anthropic();

  async function summarizeDocument(
    text: string,
    detailsToExtract: string[],
    model: Anthropic.Model = "claude-opus-5-5",
    maxTokens = 16000
  ): Promise<string> {
    // Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
    const detailsToExtractStr = detailsToExtract.join("\n");

    // Minta model meringkas perjanjian sewa ulang
    const prompt = `Summarize the following sublease agreement. Focus on these key aspects:

      ${detailsToExtractStr}

      Provide the summary in bullet points nested within the XML header for each section. For example:

      <parties involved>
      - Sublessor: [Name]
      // Add more details as needed
      </parties involved>

      If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.

      Sublease agreement text:
      ${text}
      `;

    const response = await client.messages.create({
      model,
      max_tokens: maxTokens,
      system:
        "You are a legal analyst specializing in real estate law, known for highly accurate and detailed summaries of sublease agreements.",
      messages: [{ role: "user", content: prompt }]
    });

    const textBlock = response.content.find((block) => block.type === "text");
    if (!textBlock) {
      throw new Error("Expected a text block in the response");
    }
    return textBlock.text;
  }

  const subleaseSummary = await summarizeDocument(documentText, detailsToExtract);
  console.log(subleaseSummary);
  ```

  ```csharp C#
  // Inisialisasi klien Anthropic
  var client = new AnthropicClient();

  async Task<string> SummarizeDocument(
      string text,
      IReadOnlyList<string> detailsToExtract,
      Model model = Model.ClaudeOpus5_5,
      long maxTokens = 16000
  )
  {
      // Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
      var detailsToExtractStr = string.Join("\n", detailsToExtract);

      // Minta model meringkas perjanjian sewa ulang
      var prompt = $"""
          Summarize the following sublease agreement. Focus on these key aspects:

              {detailsToExtractStr}

              Provide the summary in bullet points nested within the XML header for each section. For example:

              <parties involved>
              - Sublessor: [Name]
              // Add more details as needed
              </parties involved>

              If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.

              Sublease agreement text:
              {text}
          """;

      var response = await client.Messages.Create(
          new()
          {
              Model = model,
              MaxTokens = maxTokens,
              System = "You are a legal analyst specializing in real estate law, known for highly accurate and detailed summaries of sublease agreements.",
              Messages = [new UserMessageParam { Content = prompt }],
          }
      );

      foreach (var block in response.Content)
      {
          if (block.TryPickText(out var textBlock))
          {
              return textBlock.Text;
          }
      }
      throw new InvalidOperationException("Expected a text block in the response.");
  }

  var subleaseSummary = await SummarizeDocument(documentText, detailsToExtract);
  Console.WriteLine(subleaseSummary);
  ```

  ```go Go
  // Inisialisasi klien Anthropic
  var client = anthropic.NewClient()

  func summarizeDocument(text string, detailsToExtract []string, model anthropic.Model, maxTokens int64) string {
  	// Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
  	detailsToExtractStr := strings.Join(detailsToExtract, "\n")

  	// Minta model meringkas perjanjian sewa ulang
  	prompt := fmt.Sprintf(`Summarize the following sublease agreement. Focus on these key aspects:

      %s

      Provide the summary in bullet points nested within the XML header for each section. For example:

      <parties involved>
      - Sublessor: [Name]
      // Add more details as needed
      </parties involved>

      If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.

      Sublease agreement text:
      %s
      `, detailsToExtractStr, text)

  	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     model,
  		MaxTokens: maxTokens,
  		System: []anthropic.TextBlockParam{
  			{Text: "You are a legal analyst specializing in real estate law, known for highly accurate and detailed summaries of sublease agreements."},
  		},
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(prompt)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	for _, block := range response.Content {
  		if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  			return textBlock.Text
  		}
  	}
  	panic("expected a text block in the response")
  }

  // printSubleaseSummary meringkas perjanjian sewa ulang dan mencetak ringkasannya.
  func printSubleaseSummary() {
  	subleaseSummary := summarizeDocument(documentText, detailsToExtract, anthropic.ModelClaudeOpus5_5, 16000)
  	fmt.Println(subleaseSummary)
  }
  ```

  ```java Java
  // Inisialisasi klien Anthropic
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  String summarizeDocument(String text, List<String> detailsToExtract, Model model, long maxTokens) {
      // Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
      String detailsToExtractStr = String.join("\n", detailsToExtract);

      // Minta model meringkas perjanjian sewa ulang
      String prompt = """
          Summarize the following sublease agreement. Focus on these key aspects:

              %s

              Provide the summary in bullet points nested within the XML header for each section. For example:

              <parties involved>
              - Sublessor: [Name]
              // Add more details as needed
              </parties involved>

              If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.

              Sublease agreement text:
              %s
          """
          .formatted(detailsToExtractStr, text);

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(model)
          .maxTokens(maxTokens)
          .system("You are a legal analyst specializing in real estate law, known for highly accurate and detailed summaries of sublease agreements.")
          .addUserMessage(prompt)
          .build());

      return response.content().stream()
          .flatMap(block -> block.text().stream())
          .findFirst()
          .orElseThrow()
          .text();
  }

  void printSubleaseSummary() {
      String subleaseSummary = summarizeDocument(
          documentText, detailsToExtract, Model.CLAUDE_OPUS_5_5, 16000);
      IO.println(subleaseSummary);
  }
  ```

  ```php PHP
  // Inisialisasi klien Anthropic
  $client = new Client();

  $summarizeDocument = function (
      string $text,
      array $detailsToExtract,
      Model $model = Model::CLAUDE_OPUS_5_5,
      int $maxTokens = 16000,
  ) use ($client): string {
      // Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
      $detailsToExtractStr = implode("\n", $detailsToExtract);

      // Minta model meringkas perjanjian sewa ulang
      $prompt = <<<PROMPT
          Summarize the following sublease agreement. Focus on these key aspects:

              {$detailsToExtractStr}

              Provide the summary in bullet points nested within the XML header for each section. For example:

              <parties involved>
              - Sublessor: [Name]
              // Add more details as needed
              </parties involved>

              If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.

              Sublease agreement text:
              {$text}
          PROMPT;

      $response = $client->messages->create(
          model: $model,
          maxTokens: $maxTokens,
          system: 'You are a legal analyst specializing in real estate law, known for highly accurate and detailed summaries of sublease agreements.',
          messages: [['role' => 'user', 'content' => $prompt]],
      );

      $textBlock = array_find($response->content, fn ($block) => $block instanceof \Anthropic\Messages\TextBlock)
          ?? throw new \RuntimeException('Expected a text block in the response.');

      return $textBlock->text;
  };

  $subleaseSummary = $summarizeDocument($documentText, $detailsToExtract);
  echo $subleaseSummary . "\n";
  ```

  ```ruby Ruby
  # Inisialisasi klien Anthropic
  CLIENT = Anthropic::Client.new

  def summarize_document(text, details_to_extract, model: Anthropic::Model::CLAUDE_OPUS_5_5, max_tokens: 16_000)
    # Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
    details_to_extract_str = details_to_extract.join("\n")

    # Minta model meringkas perjanjian sewa ulang
    prompt = <<~PROMPT
      Summarize the following sublease agreement. Focus on these key aspects:

          #{details_to_extract_str}

          Provide the summary in bullet points nested within the XML header for each section. For example:

          <parties involved>
          - Sublessor: [Name]
          // Add more details as needed
          </parties involved>

          If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.

          Sublease agreement text:
          #{text}
    PROMPT

    response = CLIENT.messages.create(
      model:,
      max_tokens:,
      system_: "You are a legal analyst specializing in real estate law, known for highly accurate and detailed summaries of sublease agreements.",
      messages: [{role: :user, content: prompt}]
    )

    response.content.find { |block| block.is_a?(Anthropic::Models::TextBlock) }.text
  end

  sublease_summary = summarize_document(document_text, details_to_extract)
  puts sublease_summary
  ```
</CodeGroup>

Kode ini mengimplementasikan fungsi `summarize_document()` (typescript, go, java: `summarizeDocument()`; php: `$summarizeDocument()`; csharp: `SummarizeDocument()`) yang menggunakan Claude untuk meringkas isi perjanjian sewa-ulang. Fungsi ini menerima string teks dan daftar detail yang akan diekstrak sebagai input. Dalam contoh ini, kode memanggil fungsi tersebut dengan variabel `document_text` (typescript, go, java, csharp: `documentText`; php: `$documentText`) dan `details_to_extract` (typescript, go, java, csharp: `detailsToExtract`; php: `$detailsToExtract`) yang telah didefinisikan dalam cuplikan kode sebelumnya.

Di dalam fungsi, sebuah prompt dibuat untuk Claude, yang mencakup dokumen yang akan diringkas, detail yang akan diekstrak, dan instruksi spesifik untuk meringkas dokumen. Prompt tersebut menginstruksikan Claude untuk merespons dengan ringkasan setiap detail yang akan diekstrak, yang disarangkan di dalam header XML.

Karena kode menghasilkan setiap bagian ringkasan di dalam tag, setiap bagian dapat diurai sebagai langkah pascapemrosesan. Pendekatan ini memungkinkan pembuatan ringkasan terstruktur yang dapat disesuaikan untuk kasus penggunaan Anda, sehingga setiap ringkasan mengikuti pola yang sama.

### Evaluasi prompt Anda

Prompting sering kali memerlukan pengujian dan optimasi agar siap untuk produksi. Untuk menentukan kesiapan solusi Anda, evaluasi kualitas ringkasan Anda menggunakan proses sistematis yang menggabungkan metode kuantitatif dan kualitatif. Membuat [evaluasi empiris yang kuat](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests#build-evaluations) berdasarkan kriteria keberhasilan yang telah Anda tetapkan memungkinkan Anda mengoptimalkan prompt Anda. Berikut adalah beberapa metrik yang mungkin ingin Anda sertakan dalam evaluasi empiris Anda:

<AccordionGroup>
  <Accordion title="Skor ROUGE">
    Metrik ini mengukur tumpang tindih antara ringkasan yang dihasilkan dan ringkasan referensi yang dibuat oleh ahli. Metrik ini terutama berfokus pada recall dan berguna untuk mengevaluasi cakupan konten.
  </Accordion>

  <Accordion title="Skor BLEU">
    Meskipun awalnya dikembangkan untuk penerjemahan mesin, metrik ini dapat diadaptasi untuk tugas peringkasan. Skor BLEU mengukur presisi kecocokan n-gram antara ringkasan yang dihasilkan dan ringkasan referensi. Skor yang lebih tinggi menunjukkan bahwa ringkasan yang dihasilkan mengandung frasa dan terminologi yang serupa dengan ringkasan referensi. 
  </Accordion>

  <Accordion title="Kemiripan embedding kontekstual">
    Metrik ini melibatkan pembuatan representasi vektor (embedding) dari ringkasan yang dihasilkan maupun ringkasan referensi. Kemiripan antara embedding ini kemudian dihitung, sering kali menggunakan cosine similarity. Skor kemiripan yang lebih tinggi menunjukkan bahwa ringkasan yang dihasilkan menangkap makna semantik dan konteks dari ringkasan referensi, meskipun susunan katanya berbeda.
  </Accordion>

  <Accordion title="Penilaian berbasis LLM">
    Metode ini melibatkan penggunaan LLM seperti Claude untuk mengevaluasi kualitas ringkasan yang dihasilkan berdasarkan rubrik penilaian. Rubrik tersebut dapat disesuaikan dengan kebutuhan spesifik Anda, menilai faktor-faktor utama seperti akurasi, kelengkapan, dan koherensi. Untuk panduan implementasi, lihat 

    [Tips untuk penilaian berbasis LLM](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests#tips-for-llm-based-grading)

    .
  </Accordion>

  <Accordion title="Evaluasi manusia">
    Selain membuat ringkasan referensi, ahli hukum juga dapat mengevaluasi kualitas ringkasan yang dihasilkan. Meskipun ini mahal dan memakan waktu dalam skala besar, hal ini sering dilakukan pada beberapa ringkasan sebagai pemeriksaan validasi sebelum diterapkan ke produksi.
  </Accordion>
</AccordionGroup>

### Terapkan prompt Anda

Berikut adalah beberapa pertimbangan tambahan yang perlu diingat saat Anda menerapkan solusi Anda ke produksi.

1. **Pastikan tidak ada tanggung gugat:** Pahami implikasi hukum dari kesalahan dalam ringkasan, yang dapat menimbulkan tanggung gugat hukum bagi organisasi atau klien Anda. Sediakan penafian atau pemberitahuan hukum yang menjelaskan bahwa ringkasan dihasilkan oleh AI dan harus ditinjau oleh profesional hukum.

2. **Tangani beragam jenis dokumen:** Panduan ini membahas cara mengekstrak teks dari PDF. Di dunia nyata, dokumen mungkin hadir dalam berbagai format (seperti PDF, dokumen Word, dan file teks). Pastikan pipeline ekstraksi data Anda dapat mengonversi semua format file yang Anda harapkan akan diterima.

3. **Paralelkan panggilan API ke Claude:** Dokumen panjang dengan jumlah token yang besar mungkin memerlukan waktu hingga satu menit bagi Claude untuk menghasilkan ringkasan. Untuk koleksi dokumen yang besar, Anda mungkin ingin mengirim panggilan API ke Claude secara paralel agar ringkasan dapat diselesaikan dalam jangka waktu yang wajar. Lihat ["rate limits"](https://platform.claude.com/docs/id/api/rate-limits#rate-limits) (batas laju) Anthropic untuk menentukan jumlah maksimum panggilan API yang dapat dilakukan secara paralel.

***

## Tingkatkan performa

Dalam skenario yang kompleks, mungkin berguna untuk mempertimbangkan strategi tambahan guna meningkatkan performa di luar [teknik prompt engineering](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/overview) standar. Berikut adalah beberapa strategi lanjutan:

### Lakukan meta-peringkasan untuk meringkas dokumen panjang

Peringkasan hukum sering kali melibatkan penanganan dokumen panjang atau banyak dokumen terkait sekaligus, sehingga Anda melampaui "context window" (jendela konteks) Claude. Anda dapat menggunakan metode chunking yang dikenal sebagai meta-peringkasan (meta-summarization) untuk menangani kasus penggunaan ini. Teknik ini melibatkan pemecahan dokumen menjadi potongan-potongan (chunk) yang lebih kecil dan mudah dikelola, lalu memproses setiap potongan secara terpisah. Anda kemudian dapat menggabungkan ringkasan setiap potongan untuk membuat meta-ringkasan dari keseluruhan dokumen.

Berikut adalah contoh cara melakukan meta-peringkasan:

<CodeGroup exclude="shell">
  <CodeGroupItem language="cURL">
    Alur kerja ini memerlukan logika lebih dari sekadar satu perintah shell. Gunakan Claude SDK untuk menjalankannya.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Alur kerja ini memerlukan logika lebih dari sekadar satu perintah shell. Gunakan Claude SDK untuk menjalankannya.
  </CodeGroupItem>

  ```python Python
  def chunk_text(text, chunk_size=20000):
      return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


  def summarize_long_document(
      text, details_to_extract, model="claude-opus-5-5", max_tokens=16000
  ):
      # Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
      details_to_extract_str = "\n".join(details_to_extract)

      # Iterasi setiap chunk dan ringkas masing-masing
      chunk_summaries = [
          summarize_document(
              chunk, details_to_extract, model=model, max_tokens=max_tokens
          )
          for chunk in chunk_text(text)
      ]

      final_summary_prompt = f"""

      You are looking at the chunked summaries of multiple documents that are all related.
      Combine the following summaries of the document from different truthful sources into a coherent overall summary:

      <chunked_summaries>
      {"".join(chunk_summaries)}
      </chunked_summaries>

      Focus on these key aspects:
      {details_to_extract_str}

      Provide the summary in bullet points nested within the XML header for each section. For example:

      <parties involved>
      - Sublessor: [Name]
      // Add more details as needed
      </parties involved>

      If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.
      """

      response = client.messages.create(
          model=model,
          max_tokens=max_tokens,
          system="You are a legal expert that summarizes notes on one document.",
          messages=[
              {"role": "user", "content": final_summary_prompt},
          ],
      )

      return next(block.text for block in response.content if block.type == "text")


  long_summary = summarize_long_document(document_text, details_to_extract)
  print(long_summary)
  ```

  ```typescript TypeScript
  function chunkText(text: string, chunkSize = 20000): string[] {
    return Array.from({ length: Math.ceil(text.length / chunkSize) }, (_, index) =>
      text.slice(index * chunkSize, (index + 1) * chunkSize)
    );
  }

  async function summarizeLongDocument(
    text: string,
    detailsToExtract: string[],
    model: Anthropic.Model = "claude-opus-5-5",
    maxTokens = 16000
  ): Promise<string> {
    // Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
    const detailsToExtractStr = detailsToExtract.join("\n");

    // Iterasi setiap chunk dan ringkas masing-masing
    const chunkSummaries: string[] = [];
    for (const chunk of chunkText(text)) {
      chunkSummaries.push(await summarizeDocument(chunk, detailsToExtract, model, maxTokens));
    }

    const finalSummaryPrompt = `

      You are looking at the chunked summaries of multiple documents that are all related.
      Combine the following summaries of the document from different truthful sources into a coherent overall summary:

      <chunked_summaries>
      ${chunkSummaries.join("")}
      </chunked_summaries>

      Focus on these key aspects:
      ${detailsToExtractStr}

      Provide the summary in bullet points nested within the XML header for each section. For example:

      <parties involved>
      - Sublessor: [Name]
      // Add more details as needed
      </parties involved>

      If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.
      `;

    const response = await client.messages.create({
      model,
      max_tokens: maxTokens,
      system: "You are a legal expert that summarizes notes on one document.",
      messages: [{ role: "user", content: finalSummaryPrompt }]
    });

    const textBlock = response.content.find((block) => block.type === "text");
    if (!textBlock) {
      throw new Error("Expected a text block in the response");
    }
    return textBlock.text;
  }

  const longSummary = await summarizeLongDocument(documentText, detailsToExtract);
  console.log(longSummary);
  ```

  ```csharp C#
  IEnumerable<string> ChunkText(string text, int chunkSize = 20000) =>
      text.Chunk(chunkSize).Select(chars => new string(chars));

  async Task<string> SummarizeLongDocument(
      string text,
      IReadOnlyList<string> detailsToExtract,
      Model model = Model.ClaudeOpus5_5,
      long maxTokens = 16000
  )
  {
      // Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
      var detailsToExtractStr = string.Join("\n", detailsToExtract);

      // Iterasi setiap chunk dan ringkas masing-masing
      List<string> chunkSummaries = [];
      foreach (var chunk in ChunkText(text))
      {
          chunkSummaries.Add(await SummarizeDocument(chunk, detailsToExtract, model, maxTokens));
      }

      var finalSummaryPrompt = $"""

              You are looking at the chunked summaries of multiple documents that are all related.
              Combine the following summaries of the document from different truthful sources into a coherent overall summary:

              <chunked_summaries>
              {string.Concat(chunkSummaries)}
              </chunked_summaries>

              Focus on these key aspects:
              {detailsToExtractStr}

              Provide the summary in bullet points nested within the XML header for each section. For example:

              <parties involved>
              - Sublessor: [Name]
              // Add more details as needed
              </parties involved>

              If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.
          """;

      var response = await client.Messages.Create(
          new()
          {
              Model = model,
              MaxTokens = maxTokens,
              System = "You are a legal expert that summarizes notes on one document.",
              Messages = [new UserMessageParam { Content = finalSummaryPrompt }],
          }
      );

      foreach (var block in response.Content)
      {
          if (block.TryPickText(out var textBlock))
          {
              return textBlock.Text;
          }
      }
      throw new InvalidOperationException("Expected a text block in the response.");
  }

  var longSummary = await SummarizeLongDocument(documentText, detailsToExtract);
  Console.WriteLine(longSummary);
  ```

  ```go Go
  func chunkText(text string, chunkSize int) []string {
  	var chunks []string
  	for chunk := range slices.Chunk([]rune(text), chunkSize) {
  		chunks = append(chunks, string(chunk))
  	}
  	return chunks
  }

  func summarizeLongDocument(text string, detailsToExtract []string, model anthropic.Model, maxTokens int64) string {
  	// Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
  	detailsToExtractStr := strings.Join(detailsToExtract, "\n")

  	// Iterasi setiap chunk dan ringkas masing-masing
  	var chunkSummaries []string
  	for _, chunk := range chunkText(text, 20000) {
  		chunkSummaries = append(chunkSummaries, summarizeDocument(chunk, detailsToExtract, model, maxTokens))
  	}

  	finalSummaryPrompt := fmt.Sprintf(`

      You are looking at the chunked summaries of multiple documents that are all related.
      Combine the following summaries of the document from different truthful sources into a coherent overall summary:

      <chunked_summaries>
      %s
      </chunked_summaries>

      Focus on these key aspects:
      %s

      Provide the summary in bullet points nested within the XML header for each section. For example:

      <parties involved>
      - Sublessor: [Name]
      // Add more details as needed
      </parties involved>

      If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.
      `, strings.Join(chunkSummaries, ""), detailsToExtractStr)

  	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     model,
  		MaxTokens: maxTokens,
  		System: []anthropic.TextBlockParam{
  			{Text: "You are a legal expert that summarizes notes on one document."},
  		},
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(finalSummaryPrompt)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	for _, block := range response.Content {
  		if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  			return textBlock.Text
  		}
  	}
  	panic("expected a text block in the response")
  }

  // printLongSummary meringkas perjanjian sewa ulang per chunk dan mencetak ringkasan gabungannya.
  func printLongSummary() {
  	longSummary := summarizeLongDocument(documentText, detailsToExtract, anthropic.ModelClaudeOpus5_5, 16000)
  	fmt.Println(longSummary)
  }
  ```

  ```java Java
  List<String> chunkText(String text, int chunkSize) {
      return IntStream.iterate(0, start -> start < text.length(), start -> start + chunkSize)
          .mapToObj(start -> text.substring(start, Math.min(start + chunkSize, text.length())))
          .toList();
  }

  String summarizeLongDocument(String text, List<String> detailsToExtract, Model model, long maxTokens) {
      // Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
      String detailsToExtractStr = String.join("\n", detailsToExtract);

      // Iterasi setiap chunk dan ringkas masing-masing
      String chunkSummaries = chunkText(text, 20000).stream()
          .map(chunk -> summarizeDocument(chunk, detailsToExtract, model, maxTokens))
          .collect(Collectors.joining());

      String finalSummaryPrompt = """

              You are looking at the chunked summaries of multiple documents that are all related.
              Combine the following summaries of the document from different truthful sources into a coherent overall summary:

              <chunked_summaries>
              %s
              </chunked_summaries>

              Focus on these key aspects:
              %s

              Provide the summary in bullet points nested within the XML header for each section. For example:

              <parties involved>
              - Sublessor: [Name]
              // Add more details as needed
              </parties involved>

              If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.
          """
          .formatted(chunkSummaries, detailsToExtractStr);

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(model)
          .maxTokens(maxTokens)
          .system("You are a legal expert that summarizes notes on one document.")
          .addUserMessage(finalSummaryPrompt)
          .build());

      return response.content().stream()
          .flatMap(block -> block.text().stream())
          .findFirst()
          .orElseThrow()
          .text();
  }

  void printLongSummary() {
      String longSummary = summarizeLongDocument(
          documentText, detailsToExtract, Model.CLAUDE_OPUS_5_5, 16000);
      IO.println(longSummary);
  }
  ```

  ```php PHP
  $chunkText = fn (string $text, int $chunkSize = 20000): array => mb_str_split($text, $chunkSize);

  $summarizeLongDocument = function (
      string $text,
      array $detailsToExtract,
      Model $model = Model::CLAUDE_OPUS_5_5,
      int $maxTokens = 16000,
  ) use ($client, $chunkText, $summarizeDocument): string {
      // Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
      $detailsToExtractStr = implode("\n", $detailsToExtract);

      // Iterasi setiap chunk dan ringkas masing-masing
      $chunkSummaries = array_map(
          fn (string $chunk) => $summarizeDocument($chunk, $detailsToExtract, $model, $maxTokens),
          $chunkText($text),
      );
      $chunkSummariesStr = implode('', $chunkSummaries);

      $finalSummaryPrompt = <<<PROMPT

              You are looking at the chunked summaries of multiple documents that are all related.
              Combine the following summaries of the document from different truthful sources into a coherent overall summary:

              <chunked_summaries>
              {$chunkSummariesStr}
              </chunked_summaries>

              Focus on these key aspects:
              {$detailsToExtractStr}

              Provide the summary in bullet points nested within the XML header for each section. For example:

              <parties involved>
              - Sublessor: [Name]
              // Add more details as needed
              </parties involved>

              If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.
          PROMPT;

      $response = $client->messages->create(
          model: $model,
          maxTokens: $maxTokens,
          system: 'You are a legal expert that summarizes notes on one document.',
          messages: [['role' => 'user', 'content' => $finalSummaryPrompt]],
      );

      $textBlock = array_find($response->content, fn ($block) => $block instanceof \Anthropic\Messages\TextBlock)
          ?? throw new \RuntimeException('Expected a text block in the response.');

      return $textBlock->text;
  };

  $longSummary = $summarizeLongDocument($documentText, $detailsToExtract);
  echo $longSummary . "\n";
  ```

  ```ruby Ruby
  def chunk_text(text, chunk_size: 20_000)
    text.chars.each_slice(chunk_size).map(&:join)
  end

  def summarize_long_document(text, details_to_extract, model: Anthropic::Model::CLAUDE_OPUS_5_5, max_tokens: 16_000)
    # Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
    details_to_extract_str = details_to_extract.join("\n")

    # Iterasi setiap chunk dan ringkas masing-masing
    chunk_summaries = chunk_text(text).map do |chunk|
      summarize_document(chunk, details_to_extract, model:, max_tokens:)
    end

    final_summary_prompt = <<~PROMPT

          You are looking at the chunked summaries of multiple documents that are all related.
          Combine the following summaries of the document from different truthful sources into a coherent overall summary:

          <chunked_summaries>
          #{chunk_summaries.join}
          </chunked_summaries>

          Focus on these key aspects:
          #{details_to_extract_str}

          Provide the summary in bullet points nested within the XML header for each section. For example:

          <parties involved>
          - Sublessor: [Name]
          // Add more details as needed
          </parties involved>

          If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.
    PROMPT

    response = CLIENT.messages.create(
      model:,
      max_tokens:,
      system_: "You are a legal expert that summarizes notes on one document.",
      messages: [{role: :user, content: final_summary_prompt}]
    )

    response.content.find { |block| block.is_a?(Anthropic::Models::TextBlock) }.text
  end

  long_summary = summarize_long_document(document_text, details_to_extract)
  puts long_summary
  ```
</CodeGroup>

Fungsi `summarize_long_document()` (typescript, go, java: `summarizeLongDocument()`; php: `$summarizeLongDocument()`; csharp: `SummarizeLongDocument()`) dibangun di atas fungsi `summarize_document()` (typescript, go, java: `summarizeDocument()`; php: `$summarizeDocument()`; csharp: `SummarizeDocument()`) sebelumnya dengan membagi dokumen menjadi potongan-potongan yang lebih kecil dan meringkas setiap potongan secara individual.

Kode mencapai hal ini dengan menerapkan fungsi `summarize_document()` (typescript, go, java: `summarizeDocument()`; php: `$summarizeDocument()`; csharp: `SummarizeDocument()`) ke setiap potongan berukuran 20.000 karakter dalam dokumen asli. Ringkasan-ringkasan individual tersebut kemudian digabungkan, dan ringkasan akhir dibuat dari ringkasan-ringkasan potongan ini.

Perhatikan bahwa fungsi `summarize_long_document()` (typescript, go, java: `summarizeLongDocument()`; php: `$summarizeLongDocument()`; csharp: `SummarizeLongDocument()`) sebenarnya tidak mutlak diperlukan untuk contoh PDF ini, karena seluruh dokumen muat dalam jendela konteks Claude. Namun, fungsi ini menjadi penting untuk dokumen yang melebihi jendela konteks Claude atau saat meringkas beberapa dokumen terkait secara bersamaan. Terlepas dari itu, teknik meta-peringkasan ini sering kali menangkap detail penting tambahan dalam ringkasan akhir yang terlewatkan dalam pendekatan ringkasan tunggal sebelumnya.

### Gunakan dokumen berindeks ringkasan untuk menjelajahi koleksi dokumen yang besar

Mencari koleksi dokumen dengan LLM biasanya melibatkan "retrieval-augmented generation" (generasi yang diperkaya dengan pengambilan), atau RAG. Namun, dalam skenario yang melibatkan dokumen besar atau ketika pengambilan informasi yang presisi sangat penting, pendekatan RAG dasar mungkin tidak memadai. Dokumen yang diindeks dengan ringkasan (summary indexed documents) adalah pendekatan RAG lanjutan yang menyediakan cara yang lebih efisien untuk memeringkat dokumen untuk pengambilan, dengan menggunakan konteks yang lebih sedikit daripada metode RAG tradisional. Dalam pendekatan ini, Anda terlebih dahulu menggunakan Claude untuk menghasilkan ringkasan singkat untuk setiap dokumen dalam korpus Anda, lalu menggunakan Claude untuk memeringkat relevansi setiap ringkasan terhadap kueri yang diajukan. Untuk detail lebih lanjut tentang pendekatan ini, termasuk contoh berbasis kode, lihat bagian summary indexed documents dalam [resep peringkasan](https://platform.claude.com/cookbook/capabilities-summarization-guide).

### Lakukan fine-tuning pada Claude agar belajar dari dataset Anda

Teknik tingkat lanjut lainnya untuk meningkatkan kemampuan Claude dalam menghasilkan ringkasan adalah "fine-tuning" (penyetelan halus). Fine-tuning melibatkan pelatihan Claude pada dataset kustom yang secara khusus selaras dengan kebutuhan peringkasan hukum Anda, sehingga memastikan Claude beradaptasi dengan kasus penggunaan Anda. Berikut adalah gambaran umum cara melakukan fine-tuning:

1. **Identifikasi kesalahan:** Mulailah dengan mengumpulkan contoh-contoh di mana ringkasan Claude tidak memadai. Ini dapat mencakup detail hukum penting yang terlewat, kesalahpahaman konteks, atau penggunaan terminologi hukum yang tidak tepat.

2. **Kurasi dataset:** Setelah Anda mengidentifikasi masalah-masalah ini, susun dataset dari contoh-contoh bermasalah tersebut. Dataset ini harus menyertakan dokumen hukum asli beserta ringkasan yang telah Anda koreksi, sehingga memastikan Claude mempelajari perilaku yang Anda inginkan.

3. **Lakukan fine-tuning:** Fine-tuning melibatkan pelatihan ulang model pada dataset yang telah Anda kurasi untuk menyesuaikan bobot dan parameternya. Pelatihan ulang ini membantu Claude beradaptasi lebih baik dengan persyaratan spesifik domain hukum Anda, sehingga meningkatkan kemampuannya untuk meringkas dokumen sesuai standar Anda.

4. **Tingkatkan secara iteratif:** Fine-tuning bukanlah proses satu kali. Seiring Claude terus menghasilkan ringkasan, Anda dapat secara iteratif menambahkan contoh-contoh baru di mana performanya kurang baik, sehingga semakin menyempurnakan kemampuannya. Seiring waktu, siklus umpan balik yang berkelanjutan ini akan menghasilkan model yang sangat terspesialisasi untuk tugas peringkasan dokumen hukum Anda.

<Tip>
  Fine-tuning saat ini hanya tersedia melalui Amazon Bedrock. Detail tambahan tersedia di 

  [blog peluncuran AWS](https://aws.amazon.com/blogs/machine-learning/fine-tune-anthropics-claude-3-haiku-in-amazon-bedrock-to-boost-model-accuracy-and-quality/)

  .
</Tip>

<CardGroup cols={2}>
  <Card title="Resep peringkasan" icon="link" href="https://platform.claude.com/cookbook/capabilities-summarization-guide">
    Lihat contoh berbasis kode yang diimplementasikan sepenuhnya tentang cara menggunakan Claude untuk meringkas kontrak.
  </Card>

  <Card title="Resep kutipan" icon="link" href="https://platform.claude.com/cookbook/misc-using-citations">
    Jelajahi resep Citations untuk panduan tentang cara memastikan akurasi dan keterjelasan informasi.
  </Card>
</CardGroup>
