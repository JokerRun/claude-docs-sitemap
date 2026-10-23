---
source: platform
url: https://platform.claude.com/docs/id/models/opus-5-5/migration-guide
fetched_at: 2026-10-23T02:21:28.653315Z
sha256: f5e451462e6c6389d83a7e35a90f313f1cdb8d1354edeea9082c809d4e4c7b41
---

---
title: Panduan migrasi Claude Opus 5.5
url: https://platform.claude.com/docs/id/models/opus-5-5/migration-guide
description: Beralih ke Claude Opus 5.5 dari model Opus sebelumnya atau Claude Sonnet 5 dengan panduan migrasi ini. Panduan untuk mengaktifkan Claude Opus 5.5 mencakup pengaturan permintaan yang mengembalikan error, blok thinking di setiap respons, dan daftar periksa untuk setiap model awal.
---

<Note>
  Panduan ini membahas migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

<Tip>
  **Otomatiskan migrasi Anda dengan [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).** Skill ini sudah disertakan dalam Claude Code dan berfungsi untuk model Claude terkini mana pun sebagai target:

  Biarkan Claude Code memigrasikan kode Anda

  ```text
  /claude-api migrate proyek ini ke claude-opus-5-5
  ```

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, serta kalibrasi effort untuk model target Anda di seluruh basis kode Anda, lalu menghasilkan daftar periksa berisi item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, sebuah subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock dan Claude Platform on AWS serta menyesuaikan format ID model dan perubahan fitur untuk platform tersebut.
</Tip>

Halaman ini mencantumkan perubahan kode untuk beralih ke Claude Opus 5.5 dari [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-5), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-4-8), [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-47), [Claude Opus 4.6 dan model Opus sebelumnya](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-46), atau [Claude Sonnet 5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-sonnet-5). Setiap pembaca memerlukan [Apa yang harus dipenuhi setiap permintaan ke Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#request-requirements) dan [Menangani thinking di setiap respons](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-in-every-response). Kemudian buka bagian untuk model Anda saat ini: kalimat pertamanya menyebutkan bagian lain yang berlaku untuk Anda. [Daftar periksa migrasi](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migration-checklist) mencantumkan setiap perubahan berdasarkan model awal.

Claude Opus 5.5 lebih murah daripada Claude Opus 5 ($4 / $20 USD per juta token input / output, dibandingkan dengan $5 / $25; lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing)). Untuk dukungan fitur, lihat [Apa yang baru di Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#feature-support). Untuk perbedaan perilaku dan pola prompting khusus model, lihat [Prompting Claude Opus 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5).

## Apa yang harus dipenuhi setiap permintaan ke Claude Opus 5.5

Dari model mana pun Anda beralih, permintaan ke `claude-opus-5-5` harus memenuhi hal-hal berikut. Jika suatu item menyatakan bahwa pengaturan ditolak, API mengembalikan error 400.

* **ID model:** Gunakan `claude-opus-5-5`, ID model tetap tanpa akhiran tanggal. Di Amazon Bedrock, Claude Platform on AWS, Claude Models on Google Cloud (Google managed), dan Microsoft Foundry, gunakan ID model platform tersebut; lihat [Ketersediaan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#availability).
* **Thinking:** Jangan kirim field `thinking`, atau kirim `thinking: {"type": "adaptive"}`, yang setara: [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif. `thinking: {"type": "disabled"}` dan anggaran thinking manual (`thinking: {"type": "enabled", "budget_tokens": N}`) ditolak. Lihat [sebelum dan sesudah untuk thinking](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-cant-be-disabled).
* **Effort:** Kendalikan kedalaman thinking dengan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort), satu-satunya parameter permintaan yang mengendalikannya. Kelima level (`low`, `medium`, `high`, `xhigh`, `max`) didukung, dan defaultnya adalah `medium`. Lihat [Level effort yang direkomendasikan untuk Claude Opus 5.5](https://platform.claude.com/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-5-5).
* **Pilihan alat:** Gunakan `tool_choice` `{"type": "auto"}` (default) atau `{"type": "none"}`. Memaksa pemanggilan alat dengan `{"type": "any"}` atau `{"type": "tool", "name": "..."}` ditolak. Lihat [sebelum dan sesudah untuk pilihan alat](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#forced-tool-use).
* **Parameter sampling:** Hilangkan `temperature`, `top_p`, dan `top_k`. Gunakan prompting untuk mengarahkan perilaku model.
* **Prefill:** Jangan akhiri `messages` dengan giliran asisten yang di-prefill: itu ditolak. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) atau instruksi prompt sistem sebagai gantinya.
* **Computer use:** Di Claude API dan Claude Models on Google Cloud (Google managed), deklarasikan computer use sebagai toolset `computer_toolset_20260801`; alat `computer_20251124` yang lebih lama ditolak di sana. Lihat [perubahan yang merusak untuk computer use](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#computer-use-toolset).
* **Jendela konteks:** Tidak diperlukan header beta jendela konteks. [Jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) adalah default, dan header yang dikirim untuk model lama tidak berpengaruh.

Permintaan berikut memenuhi setiap item dalam daftar: effort diatur, dan tidak ada field `thinking`. Tab SDK yang mencetak teks memilihnya berdasarkan tipe blok, karena blok `thinking` muncul lebih dulu.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 4096,
      "messages": [{
        "role": "user",
        "content": "Analyze the trade-offs between microservices and monolithic architectures"
      }],
      "output_config": {
        "effort": "medium"
      }
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5-5 \
    --max-tokens 4096 \
    --output-config '{effort: medium}' \
    --message '{role: user, content: "Analyze the trade-offs between microservices and monolithic architectures"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Analyze the trade-offs between microservices and monolithic architectures",
          }
      ],
      output_config={"effort": "medium"},
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Analyze the trade-offs between microservices and monolithic architectures"
      }
    ],
    output_config: {
      effort: "medium"
    }
  });

  const textBlock = response.content.find((block) => block.type === "text");
  console.log(textBlock?.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Messages = [
          new UserMessageParam {
              Content = "Analyze the trade-offs between microservices and monolithic architectures"
          }
      ],
      OutputConfig = new OutputConfig
      {
          Effort = Effort.Medium
      }
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the trade-offs between microservices and monolithic architectures")),
  	},
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortMedium,
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.messages.OutputConfig;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(4096L)
          .addUserMessage("Analyze the trade-offs between microservices and monolithic architectures")
          .outputConfig(OutputConfig.builder()
              .effort(OutputConfig.Effort.MEDIUM)
              .build())
          .build();

      Message response = client.messages().create(params);
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Analyze the trade-offs between microservices and monolithic architectures']
      ],
      model: 'claude-opus-5-5',
      outputConfig: ['effort' => 'medium'],
  );

  foreach ($message->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Analyze the trade-offs between microservices and monolithic architectures" }
    ],
    output_config: {
      effort: "medium"
    }
  )

  message.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

## Menangani thinking di setiap respons

Thinking berjalan pada setiap permintaan Claude Opus 5.5, sehingga setiap respons dapat diawali dengan blok `thinking`, dan `max_tokens` mencakup thinking ditambah teks. Jika kode Anda sudah berjalan dengan thinking aktif, item 1 hingga 3 kemungkinan sudah terpenuhi: periksa item 4 dan 5. Jika kode Anda berjalan tanpa thinking, pada model sebelumnya mana pun, setiap item merupakan perubahan.

1. **`max_tokens` mencakup thinking ditambah teks:** Pada Claude Opus 4.8 dan model Opus sebelumnya, permintaan tanpa field `thinking` berjalan tanpa thinking. Claude Opus 5 dan Claude Sonnet 5 menerima `thinking: {"type": "disabled"}`. Pada Claude Opus 5.5, setiap permintaan berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking). `max_tokens` tetap menjadi batas keras untuk total output, yaitu thinking ditambah teks respons, jadi tinjau kembali nilainya untuk beban kerja yang berjalan tanpa thinking. Token thinking ditagih sebagai token output bahkan ketika teks thinking tidak dikembalikan kepada Anda, sehingga beban kerja seperti itu dapat menghasilkan lebih banyak token output per permintaan. Lihat [Pengendalian biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control). Untuk menghabiskan lebih sedikit token untuk thinking, turunkan level [effort](https://platform.claude.com/docs/id/build-with-claude/effort). Jika Anda menjalankan pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak; mulailah dari 64k token dan sesuaikan dari sana. Jika prompt Anda disetel untuk berjalan tanpa thinking, lihat [Prompt yang ditulis untuk thinking yang dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#prompts-written-for-thinking-disabled).

2. **Respons diawali dengan blok thinking:** Respons dapat diawali dengan satu atau lebih blok `thinking` sebelum blok `text` pertama. Kode yang membaca balasan berdasarkan posisi, seperti `content[0].text` atau handler stream yang memperlakukan event `content_block_start` pertama sebagai teks, akan rusak pada respons ini. Pilih blok konten berdasarkan field `type`-nya: baca `text` dari blok yang `type`-nya adalah `"text"`, dan lakukan percabangan berdasarkan tipe blok saat menangani event stream.

3. **Kembalikan blok thinking tanpa modifikasi dalam loop penggunaan alat:** Jika Anda menjalankan loop penggunaan alat, kirimkan kembali blok `thinking` dari setiap respons asisten ke API secara lengkap dan tanpa modifikasi saat Anda mengembalikan hasil alat, termasuk blok yang field `thinking`-nya kosong. Kirim ulang pesan asisten sebagaimana diterima alih-alih memfilter blok kontennya berdasarkan tipe atau membangunnya ulang: API menolak blok thinking yang diedit, diurutkan ulang, atau dihapus sebagian dengan error 400. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).

4. **Teks thinking dihilangkan secara default:** `thinking.display` secara default bernilai `"omitted"`, sehingga blok `thinking` tiba dengan field `thinking` kosong bersama `signature`-nya. Perlakukan field `thinking` hanya sebagai teks tampilan. Untuk menerima ringkasan yang dapat dibaca, atur `thinking.display` ke `"summarized"`:

   <CodeGroup exclude="shell">
     ```python Python
     thinking = {
         "type": "adaptive",
         "display": "summarized",
     }
     ```

     ```typescript TypeScript
     const thinking = {
       type: "adaptive",
       display: "summarized"
     };
     ```

     ```csharp C#
     var thinking = new ThinkingConfigAdaptive { Display = Display.Summarized };
     ```

     ```go Go
     thinking := anthropic.ThinkingConfigParamUnion{
     	OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{
     		Display: anthropic.ThinkingConfigAdaptiveDisplaySummarized,
     	},
     }
     ```

     ```java Java
     ThinkingConfigAdaptive thinking = ThinkingConfigAdaptive.builder()
         .display(ThinkingConfigAdaptive.Display.SUMMARIZED)
         .build();
     ```

     ```php PHP
     $thinking = ['type' => 'adaptive', 'display' => 'summarized'];
     ```

     ```ruby Ruby
     thinking = {
       type: "adaptive",
       display: "summarized"
     }
     ```
   </CodeGroup>

   Jika produk Anda melakukan streaming penalaran kepada pengguna, default ini tampak sebagai jeda panjang sebelum output dimulai; atur `display: "summarized"` untuk memulihkan progres yang terlihat selama thinking. Lihat [Mengendalikan tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).

5. **Teks di antara pemanggilan alat tiba dalam blok thinking:** Catatan singkat yang ditulis model di antara pemanggilan alat dikembalikan sebagai blok `thinking`, yang kosong pada tampilan default. Lihat [Teks di antara pemanggilan alat dikembalikan dalam blok thinking](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#text-between-tool-calls).

## Daftar periksa migrasi berdasarkan model awal

Telusuri grup-grup dari atas ke bawah dan berhenti setelah grup yang menyebutkan model Anda saat ini: setiap item hingga titik itu berlaku untuk Anda. Jika Anda menggunakan Claude Opus 5, grup pertama adalah seluruh daftarnya. Jika Anda menggunakan Claude Sonnet 5, terapkan grup pertama dan grup terakhir.

### Setiap model awal

* Perbarui ID model ke `claude-opus-5-5`.
* Hapus `thinking: {"type": "disabled"}` dan `thinking: {"type": "enabled", ...}`; pilih level effort sebagai gantinya.
* Atur `effort` secara eksplisit: defaultnya adalah `medium`, sedangkan default Claude Opus 5 adalah `high`.
* Ganti tipe `tool_choice` `any` dan `tool` dengan `auto` ditambah strict tool use atau structured outputs.
* Jika Anda menggunakan computer use di Claude API atau Claude Models on Google Cloud (Google managed), deklarasikan `computer_toolset_20260801` (tanpa header beta) alih-alih `computer_20251124` dan perbarui loop agen Anda untuk toolset tersebut. Di Amazon Bedrock, tetap gunakan `computer_20251124`; periksa bagian [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#compatibility) pada alat computer use untuk platform lain.
* Jika router atau fallback dapat memindahkan percakapan dari Claude Opus 5.5 ke model lain, perkirakan model tersebut berjalan tanpa blok thinking Claude Opus 5.5 (Claude Fable 5.1 dan Claude Mythos 5.1 di Claude API adalah pengecualian dan mempertahankannya). Claude Opus 5.5 sendiri membaca thinking dari Claude Opus 5, dari model Opus, Sonnet, dan Haiku sebelumnya, dan, di Claude API dan Claude Models on Google Cloud (Google managed), dari Claude Sonnet 5.5 dan Claude Haiku 5.5, tetapi tidak dari model Claude Fable atau Claude Mythos.
* Baca blok konten berdasarkan `type`, dan kirimkan kembali blok `thinking` tanpa modifikasi dalam loop penggunaan alat.
* Jika antarmuka Anda menampilkan teks di antara pemanggilan alat, atur `display: "updates"` (beta) atau `"summarized"` dan tampilkan blok `thinking` yang tidak kosong.
* Jika kode Anda mengedit giliran sebelumnya, prompt `system`, atau `tools` di tengah percakapan, ikuti [Preserved thinking](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking).
* Tangani `stop_reason: "refusal"` dan konfigurasikan fallback.
* Tetapkan ulang baseline biaya dan latensi pada level effort yang Anda pilih.
* Jika kode Anda menonaktifkan thinking, tinjau kembali `max_tokens`, yang mencakup thinking ditambah teks respons; pada effort `xhigh` atau `max`, mulailah dari 64k. Lihat [Menangani thinking di setiap respons](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-in-every-response).

### Claude Opus 4.8 atau sebelumnya

* Tinjau beban kerja yang berjalan tanpa field `thinking`: pada Claude Opus 5.5 beban kerja tersebut berjalan dengan thinking, dan thinking tidak dapat dinonaktifkan. Tinjau kembali `max_tokens`, yang tetap menjadi batas keras untuk total output (thinking ditambah teks respons), dan turunkan `effort` di mana Anda menginginkan lebih sedikit thinking. Token thinking ditagih sebagai token output, sehingga beban kerja ini dapat menghasilkan lebih banyak token output per permintaan.
* Verifikasi bahwa kode apa pun yang mem-parsing field `thinking` memperlakukannya hanya sebagai teks tampilan. Atur `display: "summarized"` untuk menerima ringkasan yang dapat dibaca.
* Tinjau prompt yang mendekati batas minimum caching: prompt sebesar 512 token atau lebih dapat membuat entri cache.
* Jika organisasi Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models), rencanakan kapasitas secara terpisah: Priority Tier tidak didukung pada Claude Opus 5.5.
* Jika Anda menjalankan pada effort `xhigh` atau `max`, naikkan `max_tokens` ke setidaknya 64k sebagai titik awal.
* Untuk beban kerja agentik, pertimbangkan [task budgets](https://platform.claude.com/docs/id/build-with-claude/task-budgets) (beta) dan perubahan alat di tengah percakapan (beta).

### Claude Opus 4.7 atau sebelumnya

* Jalankan sweep [effort](https://platform.claude.com/docs/id/build-with-claude/effort) baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk model sebelumnya.
* Hapus header beta jendela konteks apa pun.
* Jika Anda membangun ulang riwayat percakapan untuk memperbarui instruksi, pertimbangkan untuk beralih ke pesan sistem di tengah percakapan untuk mempertahankan cache hit prompt.
* Verifikasi bahwa penanganan stop reason Anda membaca `stop_details` pada penolakan.
* Jika Anda menginginkan fast mode, yang ditolak oleh Claude Opus 4.7, atur `speed: "fast"` pada permintaan Claude API Anda. Claude Opus 5.5 tidak memerlukan header beta.

### Claude Opus 4.6 atau sebelumnya

* Hapus `temperature`, `top_p`, dan `top_k` dari payload permintaan.
* Ganti `thinking: {"type": "enabled", "budget_tokens": N}` dengan `thinking: {"type": "adaptive"}` ditambah [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort), atau hapus field `thinking` sepenuhnya; adaptive thinking selalu aktif.
* Jika UI Anda menampilkan konten thinking, ikut serta secara eksplisit dalam peringkasan thinking.
* Lakukan benchmark ulang biaya dan latensi end-to-end di bawah tokenisasi yang diperbarui.
* Setel ulang `max_tokens` untuk memperhitungkan tokenisasi yang diperbarui, termasuk pemicu compaction.
* Uji ulang estimasi jumlah token di sisi klien.
* Jika aplikasi Anda mengirim gambar, anggarkan ulang untuk [dukungan gambar resolusi tinggi](https://platform.claude.com/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (hingga sekitar 3x lebih banyak token gambar per gambar resolusi penuh). Lakukan downsample sebelum mengirim jika Anda tidak memerlukan fidelitas tambahan.
* Jika Anda menggunakan koordinat pointing atau bounding-box dari model, hapus konversi faktor skala apa pun; koordinat bernilai 1:1 dengan piksel gambar sebenarnya pada Claude Opus 4.7 dan model yang lebih baru.
* Tinjau [perubahan perilaku](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#behavior-changes) yang dimulai pada Claude Opus 4.7.
* Jika produk Anda melakukan pekerjaan keamanan yang sah, ajukan permohonan ke [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) untuk mendapatkan akses ke pembatasan yang lebih rendah pada konten siber.

### Claude Opus 4.5 atau sebelumnya

* Hapus prefill pesan asisten apa pun; Claude Opus 4.6 sudah menolaknya.
* Verifikasi bahwa parsing JSON pemanggilan alat menggunakan parser JSON standar.
* Pindah dari `client.beta.messages.create()` (csharp: `client.Beta.Messages.Create()`; go: `client.Beta.Messages.New()`; java: `client.beta().messages().create()`; php: `$client->beta->messages->create()`; cli: `ant beta:messages create`) ke `client.messages.create()` (csharp: `client.Messages.Create()`; go: `client.Messages.New()`; java: `client.messages().create()`; php: `$client->messages->create()`; cli: `ant messages create`): adaptive thinking dan effort tidak memerlukan namespace beta.
* Hapus header beta `effort-2025-11-24` (parameter effort tidak memerlukannya).
* Hapus header beta `fine-grained-tool-streaming-2025-05-14`.
* Hapus header beta `interleaved-thinking-2025-05-14` (adaptive thinking mengaktifkan interleaved thinking secara otomatis).
* Migrasikan `output_format` ke `output_config.format` (jika berlaku).

### Claude 4.1 atau sebelumnya

* Perbarui versi alat (`text_editor_20250728`, `code_execution_20260521`).
* Tangani stop reason `refusal`.
* Tangani stop reason `model_context_window_exceeded`.
* Verifikasi penanganan parameter string alat untuk baris baru di akhir.
* Hapus header beta lama (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`).
* Tinjau dan perbarui prompt dengan mengikuti [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

### Hanya Claude Sonnet 5

* Jika Anda membangun ulang riwayat percakapan untuk memperbarui instruksi, pertimbangkan untuk beralih ke pesan sistem di tengah percakapan untuk mempertahankan cache hit prompt.
* Tinjau prompt yang mendekati batas minimum caching: prompt sebesar 512 token atau lebih dapat membuat entri cache.

## Migrasi ke Claude Opus 5.5 dari Claude Opus 5

Pertama, kerjakan [Apa yang harus dipenuhi setiap permintaan ke Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#request-requirements) dan [Menangani thinking di setiap respons](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-in-every-response). Setiap model awal memerlukan perubahan di bagian ini. Perubahan tersebut adalah pengaturan permintaan yang ditolak oleh Claude Opus 5.5 dan perubahan respons yang menyertainya. Daftar periksa untuk bagian ini adalah grup pertama dari [daftar periksa migrasi](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migration-checklist).

### Perbarui nama model Anda

```python
model = "claude-opus-5"  # Before
model = "claude-opus-5-5"  # After
```

`claude-opus-5-5` adalah ID model tetap tanpa akhiran tanggal, skema yang sama dengan `claude-opus-5`. Di Amazon Bedrock, Claude Platform on AWS, Claude Models on Google Cloud (Google managed), dan Microsoft Foundry, gunakan ID model platform tersebut; lihat [Ketersediaan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#availability).

### Perubahan yang merusak

Setiap perubahan dijelaskan di [Apa yang baru di Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#breaking-changes); bagian ini memberikan perubahan kode untuk masing-masing.

#### Thinking tidak dapat dinonaktifkan

`thinking: {"type": "disabled"}` dan `thinking: {"type": "enabled", "budget_tokens": N}` keduanya mengembalikan error 400 (`"thinking.type.disabled" is not supported for this model.` atau `"thinking.type.enabled" is not supported for this model.`). Hapus field `thinking` dan pilih level [effort](https://platform.claude.com/docs/id/build-with-claude/effort); di mana Anda menonaktifkan thinking untuk menghemat token, gunakan level yang lebih rendah. Respons kemudian diawali dengan blok `thinking`, jadi pilih blok konten berdasarkan `type` dan kirimkan kembali blok `thinking` tanpa modifikasi bersama hasil alat. Lihat [Thinking tidak dapat dinonaktifkan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-cant-be-disabled).

Sebelum. Claude Opus 5 menerima permintaan ini, dan Claude Opus 5.5 menolaknya dengan error 400:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 16000,
      "thinking": {"type": "disabled"},
      "messages": [{"role": "user", "content": "..."}]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 16000 \
    --thinking '{type: disabled}' \
    --message '{role: user, content: "..."}'
  ```

  ```python Python
  client.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      thinking={"type": "disabled"},
      messages=[{"role": "user", "content": "..."}],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 16000,
    thinking: { type: "disabled" },
    messages: [{ role: "user", content: "..." }]
  });
  ```

  ```csharp C#
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigDisabled(),
      Messages = [new UserMessageParam { Content = "..." }],
  });
  ```

  ```go Go
  client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfDisabled: &anthropic.ThinkingConfigDisabledParam{},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
  	},
  })
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(16000L)
      .thinking(ThinkingConfigDisabled.builder().build())
      .addUserMessage("...")
      .build();

  client.messages().create(params);
  ```

  ```php PHP
  $client->messages->create(
      model: Model::CLAUDE_OPUS_5,
      maxTokens: 16000,
      thinking: ThinkingConfigDisabled::with(),
      messages: [['role' => 'user', 'content' => '...']],
  );
  ```

  ```ruby Ruby
  client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5,
    max_tokens: 16000,
    thinking: Anthropic::ThinkingConfigDisabled.new,
    messages: [{ role: "user", content: "..." }]
  )
  ```
</CodeGroup>

Sesudah:

<CodeGroup>
  ```bash cURL
  # thinking selalu aktif; effort adalah pengendalinya
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 16000,
      "output_config": {"effort": "low"},
      "messages": [{"role": "user", "content": "..."}]
    }'
  ```

  ```bash CLI
  # thinking selalu aktif; effort adalah pengendalinya
  ant messages create \
    --model claude-opus-5-5 \
    --max-tokens 16000 \
    --output-config '{effort: low}' \
    --message '{role: user, content: "..."}'
  ```

  ```python Python
  client.messages.create(
      model="claude-opus-5-5",
      max_tokens=16000,
      output_config={"effort": "low"},  # thinking is always on; effort is the control
      messages=[{"role": "user", "content": "..."}],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 16000,
    output_config: { effort: "low" }, // thinking is always on; effort is the control
    messages: [{ role: "user", content: "..." }]
  });
  ```

  ```csharp C#
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 16000,
      OutputConfig = new() { Effort = Effort.Low }, // thinking is always on; effort is the control
      Messages = [new UserMessageParam { Content = "..." }],
  });
  ```

  ```go Go
  client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 16000,
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortLow, // thinking is always on; effort is the control
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
  	},
  })
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(16000L)
      // thinking selalu aktif; effort adalah pengendalinya
      .outputConfig(OutputConfig.builder()
          .effort(OutputConfig.Effort.LOW)
          .build())
      .addUserMessage("...")
      .build();

  client.messages().create(params);
  ```

  ```php PHP
  $client->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 16000,
      // thinking selalu aktif; effort adalah pengendalinya
      outputConfig: OutputConfig::with(effort: Effort::LOW),
      messages: [['role' => 'user', 'content' => '...']],
  );
  ```

  ```ruby Ruby
  client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 16000,
    # thinking selalu aktif; effort adalah pengendalinya
    output_config: { effort: Anthropic::OutputConfig::Effort::LOW },
    messages: [{ role: "user", content: "..." }]
  )
  ```
</CodeGroup>

#### Penggunaan alat paksa tidak didukung

Tipe `tool_choice` `any` dan `tool` mengembalikan error 400 (`tool_choice: type "tool" and "any" are not supported for this model.`), termasuk pada endpoint penghitungan token. Gunakan `auto` dengan [strict tool use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) atau [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), dan nyatakan dalam prompt kapan alat tersebut berlaku. Strict tool use menerima subset dari JSON Schema, jadi periksa `input_schema` setiap alat sebelum Anda menambahkan `strict: true`. Setiap objek dalam skema harus mengatur `additionalProperties: false`; lihat [Keterbatasan JSON Schema](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations). Lihat [Penggunaan alat paksa tidak didukung](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#forced-tool-use-is-not-supported).

Sebelum. Claude Opus 5 menerima permintaan ini, dan Claude Opus 5.5 menolaknya dengan error 400:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "tools": [{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"],
          "additionalProperties": false
        }
      }],
      "tool_choice": {"type": "tool", "name": "get_weather"},
      "messages": [{"role": "user", "content": "What'\''s the weather in Paris?"}]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
        required: [location]
        additionalProperties: false
  tool_choice:
    type: tool
    name: get_weather
  messages:
    - role: user
      content: What's the weather in Paris?
  YAML
  ```

  ```python Python
  client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      tools=tools,
      tool_choice={"type": "tool", "name": "get_weather"},
      messages=[{"role": "user", "content": "What's the weather in Paris?"}],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    tools,
    tool_choice: { type: "tool", name: "get_weather" },
    messages: [{ role: "user", content: "What's the weather in Paris?" }]
  });
  ```

  ```csharp C#
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Tools = [.. tools],
      ToolChoice = new ToolChoiceTool { Name = "get_weather" },
      Messages = [new UserMessageParam { Content = "What's the weather in Paris?" }],
  });
  ```

  ```go Go
  client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:      anthropic.ModelClaudeOpus5,
  	MaxTokens:  1024,
  	Tools:      tools,
  	ToolChoice: anthropic.ToolChoiceParamOfTool("get_weather"),
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
  	},
  })
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(1024L)
      .tools(tools)
      .toolChoice(ToolChoiceTool.of("get_weather"))
      .addUserMessage("What's the weather in Paris?")
      .build();

  client.messages().create(params);
  ```

  ```php PHP
  $client->messages->create(
      model: Model::CLAUDE_OPUS_5,
      maxTokens: 1024,
      tools: $tools,
      toolChoice: ToolChoiceTool::with(name: 'get_weather'),
      messages: [['role' => 'user', 'content' => "What's the weather in Paris?"]],
  );
  ```

  ```ruby Ruby
  client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5,
    max_tokens: 1024,
    tools: tools,
    tool_choice: Anthropic::ToolChoiceTool.new(name: "get_weather"),
    messages: [{ role: "user", content: "What's the weather in Paris?" }]
  )
  ```
</CodeGroup>

Sesudah:

<CodeGroup>
  ```bash cURL
  # penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "tools": [{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"],
          "additionalProperties": false
        },
        "strict": true
      }],
      "tool_choice": {"type": "auto"},
      "messages": [{
        "role": "user",
        "content": "What'\''s the weather in Paris? Use the get_weather tool."
      }]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
        required: [location]
        additionalProperties: false
      # penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
      strict: true
  tool_choice:
    type: auto
  messages:
    - role: user
      content: What's the weather in Paris? Use the get_weather tool.
  YAML
  ```

  ```python Python
  client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      # penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
      tools=[{**tool, "strict": True} for tool in tools],
      tool_choice={"type": "auto"},
      messages=[
          {
              "role": "user",
              "content": "What's the weather in Paris? Use the get_weather tool.",
          }
      ],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    // penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
    tools: tools.map((tool) => ({ ...tool, strict: true })),
    tool_choice: { type: "auto" },
    messages: [
      {
        role: "user",
        content: "What's the weather in Paris? Use the get_weather tool."
      }
    ]
  });
  ```

  ```csharp C#
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      // penggunaan alat ketat: setiap panggilan cocok dengan input_schema milik alat
      Tools = [.. tools.Select(tool => tool with { Strict = true })],
      ToolChoice = new ToolChoiceAuto(),
      Messages =
      [
          new UserMessageParam { Content = "What's the weather in Paris? Use the get_weather tool." },
      ],
  });
  ```

  ```go Go
  // penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
  var strictTools []anthropic.ToolUnionParam
  for _, tool := range tools {
  	strictTool := *tool.OfTool
  	strictTool.Strict = anthropic.Bool(true)
  	strictTools = append(strictTools, anthropic.ToolUnionParam{OfTool: &strictTool})
  }
  client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:      anthropic.ModelClaudeOpus5_5,
  	MaxTokens:  1024,
  	Tools:      strictTools,
  	ToolChoice: anthropic.ToolChoiceUnionParam{OfAuto: &anthropic.ToolChoiceAutoParam{}},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewTextBlock("What's the weather in Paris? Use the get_weather tool."),
  		),
  	},
  })
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024L)
      // penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
      .tools(tools.stream()
          .map(tool -> tool.tool()
              .map(customTool -> customTool.toBuilder().strict(true).build())
              .map(ToolUnion::ofTool)
              .orElse(tool))
          .toList())
      .toolChoice(ToolChoiceAuto.builder().build())
      .addUserMessage("What's the weather in Paris? Use the get_weather tool.")
      .build();

  client.messages().create(params);
  ```

  ```php PHP
  $client->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      // penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
      tools: array_map(fn (Tool $tool) => $tool->withStrict(true), $tools),
      toolChoice: ToolChoiceAuto::with(),
      messages: [
          [
              'role' => 'user',
              'content' => "What's the weather in Paris? Use the get_weather tool.",
          ],
      ],
  );
  ```

  ```ruby Ruby
  client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    # penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
    tools: tools.map { |tool| tool.merge(strict: true) },
    tool_choice: Anthropic::ToolChoiceAuto.new,
    messages: [
      { role: "user", content: "What's the weather in Paris? Use the get_weather tool." }
    ]
  )
  ```
</CodeGroup>

#### Blok thinking terikat pada model dan percakapan

Di Claude API, Claude Fable 5.1 dan Claude Mythos 5.1 membaca blok thinking Claude Opus 5.5; tidak ada model lain yang melakukannya. Router atau fallback yang memindahkan percakapan dari Claude Opus 5.5 ke model lain mana pun menjalankan giliran tersebut tanpa blok itu. Ke arah sebaliknya, Claude Opus 5.5 membaca blok thinking dari Claude Opus 5, dari model Opus, Sonnet, dan Haiku sebelumnya, dan, di Claude API dan Claude Models on Google Cloud (Google managed), dari Claude Sonnet 5.5 dan Claude Haiku 5.5, tetapi tidak dari model Claude Fable atau Claude Mythos. Pertahankan percakapan agar hanya ditambahkan (append-only, tanpa pengeditan pada prompt `system`, `tools`, atau pesan sebelumnya di tengah percakapan) sehingga blok tetap valid; Claude Code, claude.ai, Claude Managed Agents, dan Claude Agent SDK sudah melakukannya. Penegakan aturan sama dengan Claude Fable 5.1 di setiap platform: untuk akun yang dibuat pada atau setelah 31 Agustus 2026, 00:00 UTC, memutar ulang blok thinking setelah pengeditan semacam itu mengembalikan error 400 secara default. Tidak ada perubahan kode untuk integrasi append-only. Lihat [Blok thinking terikat pada model dan percakapan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them) dan [Preserved thinking](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking).

#### Alat computer use `computer_20251124` tidak didukung di Claude API dan Claude Models on Google Cloud (Google managed)

Di Claude API dan Claude Models on Google Cloud (Google managed), entri `tools` bertipe `computer_20251124` mengembalikan error 400 (`'claude-opus-5-5' does not support tool types: computer_20251124.`, diikuti oleh tipe alat yang diterima model). Deklarasikan toolset `computer_toolset_20260801` sebagai gantinya: hapus header beta dan kirim entri tanpa `name` atau dimensi tampilan. Dalam loop agen Anda, tangani blok `tool_use` anggota (aksinya adalah `name` blok, bukan `input.action`), beberapa di antaranya per giliran, dan kirim ulang `toolset_name` pada setiap hasil. Perubahan permintaan ditunjukkan di bawah; perubahan loop agen tercantum di [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124). Di Amazon Bedrock, alat `computer_20251124` yang lebih lama tetap berfungsi pada Claude Opus 5.5 seperti pada Claude Opus 5, sehingga tidak diperlukan perubahan di sana; untuk platform lain, lihat bagian [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#compatibility) pada alat computer use. Lihat [Alat computer use `computer_20251124` tidak didukung di Claude API dan Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#computer-20251124-is-not-supported).

Sebelum. Claude Opus 5 menerima permintaan ini, dan di Claude API dan Claude Models on Google Cloud (Google managed), Claude Opus 5.5 menolaknya dengan error 400:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: computer-use-2025-11-24" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "tools": [{
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": 1024,
        "display_height_px": 768
      }],
      "messages": [{"role": "user", "content": "Open the display settings."}]
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-opus-5 \
    --max-tokens 4096 \
    --beta computer-use-2025-11-24 \
    --tool '{
      type: computer_20251124,
      name: computer,
      display_width_px: 1024,
      display_height_px: 768
    }' \
    --message '{role: user, content: "Open the display settings."}'
  ```

  ```python Python
  client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=["computer-use-2025-11-24"],
      tools=[
          {
              "type": "computer_20251124",
              "name": "computer",
              "display_width_px": 1024,
              "display_height_px": 768,
          }
      ],
      messages=[{"role": "user", "content": "Open the display settings."}],
  )
  ```

  ```typescript TypeScript
  await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["computer-use-2025-11-24"],
    tools: [
      {
        type: "computer_20251124",
        name: "computer",
        display_width_px: 1024,
        display_height_px: 768
      }
    ],
    messages: [{ role: "user", content: "Open the display settings." }]
  });
  ```

  ```csharp C#
  await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 4096,
      Betas = [AnthropicBeta.ComputerUse2025_11_24],
      Tools =
      [
          new BetaToolComputerUse20251124
          {
              DisplayWidthPx = 1024,
              DisplayHeightPx = 768,
          },
      ],
      Messages = [new BetaUserMessageParam { Content = "Open the display settings." }],
  });
  ```

  ```go Go
  client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 4096,
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaComputerUse2025_11_24},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfComputerUseTool20251124: &anthropic.BetaToolComputerUse20251124Param{
  			DisplayWidthPx:  1024,
  			DisplayHeightPx: 768,
  		}},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Open the display settings.")),
  	},
  })
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(4096L)
      .addBeta(AnthropicBeta.COMPUTER_USE_2025_11_24)
      .addTool(BetaToolComputerUse20251124.builder()
          .displayWidthPx(1024L)
          .displayHeightPx(768L)
          .build())
      .addUserMessage("Open the display settings.")
      .build();

  client.beta().messages().create(params);
  ```

  ```php PHP
  $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5,
      maxTokens: 4096,
      betas: [AnthropicBeta::COMPUTER_USE_2025_11_24],
      tools: [
          BetaToolComputerUse20251124::with(
              displayWidthPx: 1024,
              displayHeightPx: 768,
          ),
      ],
      messages: [['role' => 'user', 'content' => 'Open the display settings.']],
  );
  ```

  ```ruby Ruby
  client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5,
    max_tokens: 4096,
    betas: [Anthropic::AnthropicBeta::COMPUTER_USE_2025_11_24],
    tools: [
      Anthropic::Beta::BetaToolComputerUse20251124.new(
        name: :computer,
        display_width_px: 1024,
        display_height_px: 768
      )
    ],
    messages: [{ role: "user", content: "Open the display settings." }]
  )
  ```
</CodeGroup>

Sesudah:

<CodeGroup>
  ```bash cURL
  # tanpa header beta; entri toolset tidak menerima nama atau ukuran tampilan
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 4096,
      "tools": [{"type": "computer_toolset_20260801"}],
      "messages": [{"role": "user", "content": "Open the display settings."}]
    }'
  ```

  ```bash CLI
  # tanpa header beta; entri toolset tidak menerima nama atau ukuran tampilan
  ant messages create \
    --model claude-opus-5-5 \
    --max-tokens 4096 \
    --tool '{type: computer_toolset_20260801}' \
    --message '{role: user, content: "Open the display settings."}'
  ```

  ```python Python
  client.messages.create(
      model="claude-opus-5-5",
      max_tokens=4096,
      # tanpa header beta; entri toolset tidak menerima nama atau ukuran tampilan
      tools=[{"type": "computer_toolset_20260801"}],
      messages=[{"role": "user", "content": "Open the display settings."}],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 4096,
    // tanpa header beta; entri toolset tidak menerima nama atau ukuran tampilan
    tools: [{ type: "computer_toolset_20260801" }],
    messages: [{ role: "user", content: "Open the display settings." }]
  });
  ```

  ```csharp C#
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      // tanpa header beta; entri toolset tidak menerima nama atau ukuran tampilan
      Tools = [new ComputerToolset20260801()],
      Messages = [new UserMessageParam { Content = "Open the display settings." }],
  });
  ```

  ```go Go
  client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 4096,
  	// tanpa header beta; entri toolset tidak menerima nama atau ukuran tampilan
  	Tools: []anthropic.ToolUnionParam{
  		{OfComputerToolset20260801: &anthropic.ComputerToolset20260801Param{}},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Open the display settings.")),
  	},
  })
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(4096L)
      // tanpa header beta; entri toolset tidak menerima nama atau ukuran tampilan
      .addTool(ComputerToolset20260801.builder().build())
      .addUserMessage("Open the display settings.")
      .build();

  client.messages().create(params);
  ```

  ```php PHP
  $client->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 4096,
      // tanpa header beta; entri toolset tidak menerima nama atau ukuran tampilan
      tools: [ComputerToolset20260801::with()],
      messages: [['role' => 'user', 'content' => 'Open the display settings.']],
  );
  ```

  ```ruby Ruby
  client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 4096,
    # tanpa header beta; entri toolset tidak menerima nama atau ukuran tampilan
    tools: [Anthropic::ComputerToolset20260801.new],
    messages: [{ role: "user", content: "Open the display settings." }]
  )
  ```
</CodeGroup>

### Teks di antara pemanggilan alat dikembalikan dalam blok thinking

Pada Claude Opus 5, teks yang ditulis model di antara pemanggilan alat dikembalikan sebagai blok `text`. Pada Claude Opus 5.5, seperti pada Claude Fable 5.1, narasi tersebut dikembalikan sebagai [blok `thinking` pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates), paling banyak satu sebelum setiap pemanggilan alat. Pada `thinking.display` default yaitu `"omitted"`, field `thinking`-nya kosong. Tidak ada permintaan yang gagal, tetapi aplikasi yang melakukan streaming teks tersebut kepada penggunanya sebagai pembaruan progres menjadi diam di antara pemanggilan alat. Untuk memulihkan pembaruan, baca dari blok `thinking` dan atur nilai `display` yang mengembalikan teksnya: `"updates"` (beta, header `thinking-display-updates-2026-08-18`) mengembalikan pembaruan progres sementara penalaran tetap tersembunyi, dan `"summarized"` mengembalikan keduanya, tercampur bersama. Kemudian tampilkan setiap blok `thinking` yang tidak kosong sebelum blok `tool_use` yang didahuluinya, dan kirimkan kembali blok tersebut tanpa perubahan bersama sisa giliran asisten. Lihat [Pembaruan progres yang ditampilkan kepada pengguna](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#user-facing-progress-updates).

### Classifier keamanan dan fallback

Claude Opus 5.5 dapat mengembalikan `stop_reason: "refusal"` dengan kategori `stop_details`. Classifier-nya mencakup kumpulan kategori yang lebih luas daripada milik Claude Opus 5, jadi perkirakan nilai `stop_details.category` seperti `"bio"` selain `"cyber"` dan `"reasoning_extraction"`; lihat [tabel kategori penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response). Tangani penolakan dan konfigurasikan [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) atau percobaan ulang Anda sendiri (fallback sisi server tidak mencoba ulang permintaan yang ditolak dengan `"reasoning_extraction"`; penolakan tersebut dikembalikan kepada Anda); lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) dan [Penolakan safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#safeguard-refusals).

### Perubahan yang direkomendasikan

1. **Jalankan ulang sweep effort Anda.** Effort adalah satu-satunya kontrol thinking pada Claude Opus 5.5, dan defaultnya adalah `medium` sedangkan default Claude Opus 5 adalah `high`, sehingga permintaan yang menghilangkan `effort` kini berjalan pada `medium`. Turunkan level di mana kualitas tetap terjaga, dan naikkan untuk pekerjaan yang paling menuntut. Lihat [Effort](https://platform.claude.com/docs/id/build-with-claude/effort).
2. **Evaluasi ulang instruksi prompt khusus model.** Instruksi yang disetel untuk perilaku Claude Opus 5 mungkin tidak lagi diperlukan; lihat [Prompting Claude Opus 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5). Jika Anda menjalankan dengan thinking dinonaktifkan, lihat juga [Prompt yang ditulis untuk thinking yang dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#prompts-written-for-thinking-disabled).
3. **Uji di lingkungan pengembangan** sebelum mengalihkan lalu lintas produksi.

## Migrasi ke Claude Opus 5.5 dari Claude Opus 4.8

Pertama, kerjakan [Apa yang harus dipenuhi setiap permintaan ke Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#request-requirements), [Menangani thinking di setiap respons](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-in-every-response), dan [Migrasi ke Claude Opus 5.5 dari Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-5). Gunakan `claude-opus-4-8` sebagai ID model yang Anda ganti. Bagian terakhir tersebut berlaku untuk kode pada Claude Opus 4.8 sebagaimana tertulis, karena Claude Opus 4.8, seperti Claude Opus 5:

* Menerima `thinking: {"type": "disabled"}`, pilihan alat paksa, dan alat `computer_20251124`.
* Mengembalikan teks di antara pemanggilan alat sebagai blok `text`.
* Menggunakan effort `high` secara default.

Bagian ini menambahkan apa yang berubah antara Claude Opus 4.8 dan Claude Opus 5. Untuk daftar periksa, lihat dua grup pertama dari [daftar periksa migrasi](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migration-checklist).

### Apa yang berubah

1. **Thinking berjalan pada permintaan yang menghilangkannya:** Pada Claude Opus 4.8, thinking nonaktif kecuali Anda memintanya. Pada Claude Opus 5.5, permintaan tanpa field `thinking` berjalan dengan thinking, sehingga setiap item di [Menangani thinking di setiap respons](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-in-every-response) merupakan perubahan untuk kode tersebut. Jika kode Anda tidak pernah mengirim field `thinking`, tidak ada yang perlu dihapus di bawah [sebelum dan sesudah untuk thinking](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-cant-be-disabled).

2. **Batas minimum caching prompt yang lebih rendah:** Panjang prompt minimum yang dapat di-cache pada Claude Opus 5.5 adalah 512 token, turun dari 1.024 token pada Claude Opus 4.8. Prompt yang terlalu pendek untuk di-cache pada Claude Opus 4.8 dapat membuat entri cache, tanpa memerlukan perubahan kode. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk batas minimum per model.

3. **Priority Tier tidak didukung:** [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak didukung pada Claude Opus 5.5, sementara Claude Opus 4.8 tetap mendukungnya. Jika organisasi Anda memiliki komitmen Priority Tier, rencanakan kapasitas secara terpisah.

### Perubahan yang direkomendasikan

Perubahan ini tidak wajib tetapi akan meningkatkan pengalaman Anda:

1. **Pertimbangkan task budgets (beta):** Untuk beban kerja agentik, [task budgets](https://platform.claude.com/docs/id/build-with-claude/task-budgets) memberi tahu model berapa banyak token yang dimilikinya untuk satu loop agentik penuh. Fitur ini memerlukan header beta `task-budgets-2026-03-13`.

2. **Pertimbangkan perubahan alat di tengah percakapan (beta):** Perubahan alat di tengah percakapan memungkinkan Anda menambahkan atau menghapus alat di antara giliran percakapan tanpa membatalkan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya. Mengubah array `tools` itu sendiri membatalkan prefiks yang di-cache. Di Claude API, kirim header beta `inline-tools-2026-09-15`. Header `mid-conversation-tool-changes-2026-07-01` yang lebih lama masih berfungsi untuk perubahan yang menyebut alat berdasarkan referensi, di Claude API, Amazon Bedrock, dan Claude Models on Google Cloud (Google managed).

## Migrasi ke Claude Opus 5.5 dari Claude Opus 4.7

Pertama, kerjakan [Apa yang harus dipenuhi setiap permintaan ke Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#request-requirements), [Menangani thinking di setiap respons](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-in-every-response), [Migrasi ke Claude Opus 5.5 dari Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-5), dan [Migrasi ke Claude Opus 5.5 dari Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-4-8). Gunakan `claude-opus-4-7` sebagai ID model yang Anda ganti. Bagian-bagian tersebut berlaku untuk kode pada Claude Opus 4.7 sebagaimana tertulis. Seperti Claude Opus 4.8, model ini menerima `thinking: {"type": "disabled"}`, pilihan alat paksa, dan alat `computer_20251124`. Model ini menggunakan effort `high` secara default dan berjalan tanpa thinking kecuali Anda memintanya.

Bagian ini menambahkan apa yang berubah setelah Claude Opus 4.7. Jika kode Anda menggunakan Claude Opus 4.6 atau sebelumnya, lanjutkan dengan [Migrasi ke Claude Opus 5.5 dari Claude Opus 4.6 dan model Opus sebelumnya](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-46) setelah bagian ini. Bagian tersebut menambahkan perubahan yang merusak yang mulai berlaku pada Claude Opus 4.7. Untuk daftar periksa, lihat tiga grup pertama dari [daftar periksa migrasi](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migration-checklist).

### Apa yang berubah

Tidak satu pun dari item ini menambahkan perubahan yang merusak pada yang ada di bagian sebelumnya; item-item ini layak diperiksa setelah Anda mengganti ID model.

1. **Level effort dikalibrasi ulang:** Alokasi token di balik setiap level effort berubah pada Claude Opus 5.5 dibandingkan dengan Claude Opus 4.7. Defaultnya adalah `medium`, sedangkan default Claude Opus 4.7 adalah `high`. Jalankan sweep effort baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk Claude Opus 4.7. Lihat [Effort](https://platform.claude.com/docs/id/build-with-claude/effort).

2. **Jendela konteks 1M adalah default:** Claude Opus 5.5 menyediakan [jendela konteks](https://platform.claude.com/docs/id/build-with-claude/context-windows) penuh 1M token secara default tanpa header beta. Jika klien Anda mengirimkan header beta jendela konteks untuk kompatibilitas dengan model lama, hapus header tersebut.

3. **Pesan sistem di tengah percakapan:** Di Claude API, Amazon Bedrock, dan Claude Models on Google Cloud (Google managed), Claude Opus 5.5 menerima pesan `role: "system"` tepat setelah giliran pengguna dalam array `messages` (tunduk pada [aturan penempatan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Gunakan field `system` tingkat atas untuk instruksi yang berlaku sejak awal. Claude Opus 4.7 menolak `role: "system"` dalam `messages` dengan error 400. Jika Anda memelihara jalur kode yang membangun ulang seluruh riwayat pesan untuk memperbarui instruksi, Anda dapat menyederhanakannya dan mempertahankan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya.

4. **Detail stop penolakan:** Ketika model menolak permintaan, Claude Opus 5.5 mengembalikan objek `stop_details` yang menyebutkan kategori penolakan, bersama dengan stop reason `refusal`. Claude Opus 4.7 mengembalikan objek yang sama, jadi hal ini hanya penting jika penanganan stop reason Anda belum membacanya. Tidak diperlukan header beta, dan tidak ada opsi untuk menonaktifkannya. Jika penanganan stop reason Anda belum membacanya, lihat [Menangani stop reason](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons). Claude Opus 5.5 menolak dalam lebih banyak kategori; lihat [Classifier keamanan dan fallback](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#safety-classifiers-and-fallback).

5. **Fast mode:** Claude Opus 5.5 mendukung [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) di Claude API. Fast mode tidak tersedia pada Claude Opus 4.7, di mana permintaan dengan `speed: "fast"` mengembalikan error. Atur `speed: "fast"` pada permintaan Anda. Claude Opus 5.5 tidak memerlukan header beta.

6. **Toolset computer use dan alat browser use:** Di Claude API dan Claude Models on Google Cloud (Google managed), Claude Opus 5.5 mendukung [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) sebagai toolset `computer_toolset_20260801` dan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) untuk tugas di dalam halaman web. Claude Opus 4.7 tidak mendukung keduanya. Di platform tersebut, Claude Opus 5.5 tidak menerima alat `computer_20251124` yang lebih lama; lihat [perubahan yang merusak untuk computer use](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#computer-use-toolset).

## Migrasi ke Claude Opus 5.5 dari Claude Opus 4.6 dan model Opus sebelumnya

Pertama, kerjakan setiap bagian sebelumnya, sesuai urutan halaman. Bagian-bagian tersebut adalah [Yang harus dipenuhi setiap permintaan ke Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#request-requirements), [Menangani thinking di setiap respons](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-in-every-response), serta bagian untuk [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-5), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-4-8), dan [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-47). Bagian-bagian tersebut berlaku untuk kode pada Claude Opus 4.6 sebagaimana tertulis. Seperti Claude Opus 4.7, model ini menerima `thinking: {"type": "disabled"}`, forced tool choice, dan alat `computer_20251124`. Model ini secara default menggunakan effort `high` dan berjalan tanpa thinking kecuali Anda memintanya. Claude Opus 4.5 dan model Opus sebelumnya juga menerima `thinking: {"type": "disabled"}` dan forced tool choice, serta berjalan tanpa thinking kecuali Anda memintanya, sehingga bagian-bagian tersebut juga berlaku untuk model-model itu.

Bagian ini menambahkan apa yang berubah di Claude Opus 4.7, dengan `claude-opus-4-6` sebagai ID model yang Anda ganti. Dua subbagiannya menambahkan apa yang berubah sebelum itu, untuk pembaca yang menggunakan [Claude Opus 4.5 atau sebelumnya](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-45) dan [Claude 4.1 atau sebelumnya](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-4-1-or-earlier). Untuk daftar periksa, lihat [daftar periksa migrasi](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migration-checklist) hingga kelompok yang menyebutkan model Anda.

### Perubahan yang merusak kompatibilitas

1. **Pemikiran diperpanjang dihapus:** `thinking: {"type": "enabled", "budget_tokens": N}` tidak lagi didukung pada Claude Opus 4.7 dan model yang lebih baru serta mengembalikan error 400. Beralihlah ke [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (`thinking: {"type": "adaptive"}`) dan gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking. Pada Claude Opus 5.5, adaptive thinking selalu aktif: `thinking: {"type": "adaptive"}` valid dan setara dengan menghilangkan field `thinking` sepenuhnya.

   Sebelum (Claude Opus 4.6):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-opus-4-6",
         "max_tokens": 16000,
         "thinking": {
           "type": "enabled",
           "budget_tokens": 10000
         },
         "messages": [
           {
             "role": "user",
             "content": "..."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-4-6
     max_tokens: 16000
     thinking:
       type: enabled
       budget_tokens: 10000
     messages:
       - role: user
         content: "..."
     YAML
     ```

     ```python Python
     client.messages.create(
         model="claude-opus-4-6",
         max_tokens=16000,
         thinking={"type": "enabled", "budget_tokens": 10000},
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-opus-4-6",
       max_tokens: 16000,
       thinking: { type: "enabled", budget_tokens: 10000 },
       messages: [{ role: "user", content: "..." }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = Model.ClaudeOpus4_6,
         MaxTokens = 16000,
         Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
         Messages = [new UserMessageParam { Content = "..." }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     anthropic.ModelClaudeOpus4_6,
     	MaxTokens: 16000,
     	Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
     	},
     })
     if err != nil {
     	log.Fatal(err)
     }
     fmt.Println(response)
     ```

     ```java Java
     AnthropicClient client = AnthropicOkHttpClient.fromEnv();

     MessageCreateParams params = MessageCreateParams.builder()
         .model(Model.CLAUDE_OPUS_4_6)
         .maxTokens(16000L)
         .enabledThinking(10000L)
         .addUserMessage("...")
         .build();

     Message response = client.messages().create(params);
     IO.println(response);
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => '...']],
         model: 'claude-opus-4-6',
         thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-opus-4-6",
       max_tokens: 16000,
       thinking: {
         type: "enabled",
         budget_tokens: 10000
       },
       messages: [
         { role: "user", content: "..." }
       ]
     )
     ```
   </CodeGroup>

   Sesudah (Claude Opus 5.5), dengan baris ID model, `thinking`, dan `output_config` yang berbeda:

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-opus-5-5",
         "max_tokens": 16000,
         "thinking": {
           "type": "adaptive"
         },
         "output_config": {
           "effort": "high"
         },
         "messages": [
           {
             "role": "user",
             "content": "..."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-5-5
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
     client.messages.create(
         model="claude-opus-5-5",
         max_tokens=16000,
         thinking={"type": "adaptive"},
         output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-opus-5-5",
       max_tokens: 16000,
       thinking: { type: "adaptive" },
       output_config: { effort: "high" }, // or "max", "xhigh", "medium", "low"
       messages: [{ role: "user", content: "..." }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = Model.ClaudeOpus5_5,
         MaxTokens = 16000,
         Thinking = new ThinkingConfigAdaptive(),
         OutputConfig = new OutputConfig { Effort = Effort.High }, // or Max, Xhigh, Medium, Low
         Messages = [new UserMessageParam { Content = "..." }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     anthropic.ModelClaudeOpus5_5,
     	MaxTokens: 16000,
     	Thinking: anthropic.ThinkingConfigParamUnion{
     		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
     	},
     	OutputConfig: anthropic.OutputConfigParam{
     		Effort: anthropic.OutputConfigEffortHigh, // or Max, Xhigh, Medium, Low
     	},
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
     	},
     })
     if err != nil {
     	log.Fatal(err)
     }
     fmt.Println(response)
     ```

     ```java Java
     AnthropicClient client = AnthropicOkHttpClient.fromEnv();

     MessageCreateParams params = MessageCreateParams.builder()
         .model(Model.CLAUDE_OPUS_5_5)
         .maxTokens(16000L)
         .thinking(ThinkingConfigAdaptive.builder().build())
         .outputConfig(OutputConfig.builder()
             .effort(OutputConfig.Effort.HIGH) // or MAX, XHIGH, MEDIUM, LOW
             .build())
         .addUserMessage("...")
         .build();

     Message response = client.messages().create(params);
     IO.println(response);
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => '...']],
         model: 'claude-opus-5-5',
         thinking: ['type' => 'adaptive'],
         outputConfig: ['effort' => 'high'], // or 'max', 'xhigh', 'medium', 'low'
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-opus-5-5",
       max_tokens: 16000,
       thinking: {
         type: "adaptive"
       },
       output_config: {
         effort: "high" # or "max", "xhigh", "medium", "low"
       },
       messages: [
         { role: "user", content: "..." }
       ]
     )
     ```
   </CodeGroup>

   Adaptive thinking dapat diarahkan melalui prompting dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort), yang menggantikan anggaran thinking sebagai cara untuk mengontrol seberapa banyak model bernalar. Jalankan effort sweep pada eval Anda sendiri alih-alih menerjemahkan nilai `budget_tokens`. [Tabel tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort#effort-levels) menjelaskan kapan menggunakan setiap tingkat, dan [Tingkat effort yang direkomendasikan untuk Claude Opus 5.5](https://platform.claude.com/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-5-5) membahas model ini.

2. **Parameter sampling dihapus:** Hilangkan `temperature`, `top_p`, dan `top_k`. Prompting adalah cara yang direkomendasikan untuk memandu perilaku model pada Claude Opus 5.5. Jika Anda menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa hal itu tidak pernah menjamin output yang identik pada model sebelumnya.

3. **Konten thinking dihilangkan secara default:** Blok thinking masih muncul dalam stream respons pada Claude Opus 4.7 dan model yang lebih baru, tetapi field `thinking`-nya kosong kecuali Anda secara eksplisit memilih untuk mengaktifkannya. Ini adalah perubahan diam-diam dari Claude Opus 4.6, yang secara default mengembalikan teks thinking yang diringkas. Untuk memulihkannya, lihat butir 4 dari [Menangani thinking di setiap respons](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-in-every-response).

4. **Penghitungan token yang diperbarui:** Claude Opus 4.7 memperkenalkan tokenizer baru, yang juga digunakan oleh model Opus yang lebih baru, termasuk Claude Opus 5.5. Tokenizer ini berkontribusi pada peningkatan kinerja di berbagai tugas, dan dapat menggunakan sekitar 1x hingga 1,35x lebih banyak token saat memproses teks dibandingkan model sebelum Claude Opus 4.7 (hingga \~35% lebih banyak, bervariasi menurut konten).

   [`/v1/messages/count_tokens`](https://platform.claude.com/docs/id/build-with-claude/token-counting) mengembalikan jumlah token yang berbeda untuk Claude Opus 5.5 dibandingkan untuk Claude Opus 4.6. Efisiensi token dapat bervariasi menurut bentuk beban kerja.

   Perbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu compaction, dan uji ulang setiap jalur kode yang memperkirakan token di sisi klien atau mengasumsikan rasio token-ke-karakter yang tetap. Gunakan [endpoint Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) untuk memverifikasi. Intervensi prompting, [`task_budget`](https://platform.claude.com/docs/id/build-with-claude/task-budgets), dan [`effort`](https://platform.claude.com/docs/id/build-with-claude/effort) dapat membantu mengontrol biaya; kontrol-kontrol ini mungkin mengorbankan kecerdasan model.

5. **Penghapusan prefill (sudah berlaku pada Claude Opus 4.6):** Prefill pesan asisten mengembalikan error 400 pada Claude Opus 4.6 dan model Opus yang lebih baru, termasuk Claude Opus 5.5, sehingga ini hanya merupakan perubahan jika Anda berasal dari Claude Opus 4.5 atau sebelumnya. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) atau instruksi prompt sistem sebagai gantinya.

### Perubahan perilaku

Claude Opus 4.7 memperkenalkan perbedaan perilaku dari Claude Opus 4.6 yang bukan merupakan perubahan API yang merusak kompatibilitas. Tiga hal berikut memengaruhi kode atau scaffolding:

1. **Pembaruan progres bawaan dalam trace agentik:** Claude Opus 4.7 memberikan pembaruan yang lebih teratur dan berkualitas lebih tinggi kepada pengguna sepanjang trace agentik yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status sementara ("Setelah setiap 3 panggilan alat, ringkas progres"), coba hapus. Pada Claude Opus 5.5, pembaruan ini tiba dalam blok `thinking`, yang kosong pada `thinking.display` default. Untuk menerimanya, lihat [Teks di antara panggilan alat dikembalikan dalam blok thinking](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#text-between-tool-calls). Untuk membentuk panjang dan isinya, lihat [Pembaruan progres yang ditampilkan kepada pengguna](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#user-facing-progress-updates).

2. **Pengamanan keamanan siber real-time:** Baru ditambahkan di Claude Opus 4.7, permintaan yang melibatkan topik terlarang atau berisiko tinggi dapat menyebabkan penolakan. Untuk pekerjaan keamanan yang sah seperti penetration testing, riset kerentanan, atau red-teaming, ajukan permohonan ke [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) untuk meminta pengurangan pembatasan. Jalur pengajuan bergantung pada cara Anda mengakses Claude.

3. **Dukungan gambar resolusi tinggi:** Claude Opus 4.7 adalah model Claude pertama dengan dukungan gambar resolusi tinggi. Resolusi gambar maksimum adalah 2.576 piksel pada sisi panjang, naik dari 1.568 piksel pada model sebelumnya. Ini membuka peningkatan pada beban kerja yang banyak menggunakan visi dan sangat berharga untuk computer use, pemahaman screenshot, dan analisis dokumen.

   Dukungan resolusi tinggi bersifat otomatis dan tidak memerlukan beta header atau opt-in di sisi klien. Dua hal yang perlu direncanakan:

   * Gambar resolusi penuh dapat menggunakan hingga sekitar 3x lebih banyak token gambar dibandingkan pada model sebelumnya (hingga 4.784 token per gambar, dibandingkan batas sebelumnya sekitar 1.600 token per gambar). Anggarkan ulang `max_tokens` dan ekspektasi biaya untuk beban kerja yang banyak menggunakan gambar, atau lakukan downsample sebelum mengirim jika Anda tidak memerlukan fidelitas tambahan.
   * Koordinat pointing dan bounding-box yang dikembalikan oleh model adalah 1:1 dengan piksel gambar sebenarnya pada Claude Opus 4.7, sehingga tidak diperlukan konversi faktor skala.

   Lihat [Dukungan gambar resolusi tinggi pada Claude Opus 4.7](https://platform.claude.com/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) untuk detailnya.

Untuk perbedaan di sisi prompt, lihat [Prompting Claude Opus 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) dan [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

### Migrasi dari Claude Opus 4.5 atau sebelumnya

Jika Anda bermigrasi dari Claude Opus 4.5, Claude Opus 4.1, atau model sebelumnya langsung ke Claude Opus 5.5, baca halaman ini dari atas: pertama, kerjakan setiap bagian sebelumnya, sesuai urutan halaman. Kemudian kerjakan [perubahan yang merusak kompatibilitas untuk migrasi dari Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#opus-46-breaking-changes) di bagian awal bagian ini. Kemudian terapkan perubahan kumulatif berikut, yang berlaku antara Claude Opus 4.5 dan Claude Opus 4.7. Jika Anda menggunakan Claude Opus 4.1 atau sebelumnya, lanjutkan dengan [Migrasi dari Claude 4.1 atau sebelumnya](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-4-1-or-earlier) setelah subbagian ini.

#### Perubahan yang merusak kompatibilitas

1. **Penghapusan prefill** dibahas dalam [perubahan yang merusak kompatibilitas untuk migrasi dari Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#opus-46-breaking-changes).

2. **Quoting parameter alat:** Claude Opus 4.6 dan model yang lebih baru mungkin menghasilkan escaping string JSON yang sedikit berbeda dalam argumen panggilan alat (misalnya, penanganan escape Unicode atau escaping garis miring yang berbeda). Jika Anda mem-parse `input` panggilan alat sebagai string mentah alih-alih menggunakan parser JSON, verifikasi logika parsing Anda. Parser JSON standar (seperti `json.loads()` atau `JSON.parse()`) menangani perbedaan ini secara otomatis.

#### Perubahan yang direkomendasikan

Butir pertama wajib pada Claude Opus 5.5; sisanya direkomendasikan.

1. **Migrasi ke adaptive thinking (wajib):** `thinking: {"type": "enabled", "budget_tokens": N}` mengembalikan error 400 pada Claude Opus 4.7 dan model yang lebih baru. Contoh sebelum dan sesudahnya ada di butir 1 dari [perubahan yang merusak kompatibilitas untuk migrasi dari Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#opus-46-breaking-changes). Migrasi ini juga berpindah dari `client.beta.messages.create()` (csharp: `client.Beta.Messages.Create()`; go: `client.Beta.Messages.New()`; java: `client.beta().messages().create()`; php: `$client->beta->messages->create()`; cli: `ant beta:messages create`) ke `client.messages.create()` (csharp: `client.Messages.Create()`; go: `client.Messages.New()`; java: `client.messages().create()`; php: `$client->messages->create()`; cli: `ant messages create`): adaptive thinking dan effort tidak memerlukan namespace SDK beta atau beta header apa pun.

2. **Hapus beta header effort:** Parameter effort tidak memerlukan beta header. Hapus beta `effort-2025-11-24` dari permintaan Anda.

3. **Hapus beta header fine-grained tool streaming:** Fine-grained tool streaming tidak memerlukan beta header. Hapus beta `fine-grained-tool-streaming-2025-05-14` dari permintaan Anda.

4. **Hapus beta header interleaved thinking:** Dengan adaptive thinking, interleaved thinking bersifat otomatis pada setiap model yang mendukung adaptive thinking. Hapus beta `interleaved-thinking-2025-05-14` dari permintaan Anda.

5. **Migrasi ke output\_config.format:** Jika menggunakan structured outputs, perbarui `output_format={...}` menjadi `output_config={"format": {...}}`. Parameter `output_format` sudah deprecated dan akan dihapus di masa mendatang. Untuk tetap menggunakannya, tambahkan beta header `structured-outputs-2025-11-13`. Tanpanya, API mengembalikan error 400. Python SDK (v1.0 dan yang lebih baru) tidak menerima `output_format={...}` pada `client.beta.messages.create()` atau `count_tokens()`. Argumen `output_format=Model` dari helper `parse()` dan `stream()` tidak berubah.

### Migrasi dari Claude 4.1 atau sebelumnya

Jika Anda bermigrasi dari Claude Opus 4.1 atau model sebelumnya langsung ke Claude Opus 5.5, pertama terapkan semua yang ada di [Migrasi dari Claude Opus 4.5 atau sebelumnya](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-45). Subbagian tersebut dimulai dengan setiap bagian sebelumnya, sehingga pada dasarnya Anda membaca halaman ini dari atas. Kemudian terapkan perubahan tambahan dalam subbagian ini.

#### Perubahan tambahan yang merusak kompatibilitas

1. **Hapus parameter sampling:** Dibahas dalam [Parameter sampling dihapus](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#opus-46-breaking-changes).

2. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat saat ini. Hapus kode apa pun yang menggunakan perintah `undo_edit`.

   <CodeGroup exclude="shell">
     ```python Python
     # Sebelum
     tools = [{"type": "text_editor_20250124", "name": "str_replace_editor"}]

     # Sesudah
     tools = [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
     ```

     ```typescript TypeScript
     // Sebelum
     const legacyTools = [{ type: "text_editor_20250124", name: "str_replace_editor" }];

     // Sesudah
     const tools = [{ type: "text_editor_20250728", name: "str_replace_based_edit_tool" }];
     ```

     ```csharp C#
     var parameters = new MessageCreateParams
     {
         // Sebelum: {"type": "text_editor_20250124", "name": "str_replace_editor"}
         // Sesudah:
         Tools = [new ToolTextEditor20250728()],
         // ...
     };
     ```

     ```go Go
     params := anthropic.MessageNewParams{
     	// Sebelum: {"type": "text_editor_20250124", "name": "str_replace_editor"}
     	// Sesudah:
     	Tools: []anthropic.ToolUnionParam{
     		{OfTextEditor20250728: &anthropic.ToolTextEditor20250728Param{}},
     	},
     	// ...
     }
     ```

     ```java Java
     MessageCreateParams params = MessageCreateParams.builder()
         // Sebelum: {"type": "text_editor_20250124", "name": "str_replace_editor"}
         // Sesudah:
         .addTool(ToolTextEditor20250728.builder().build())
         // ...
         .build();
     ```

     ```php PHP
     $message = $client->messages->create(
         // Sebelum: ['type' => 'text_editor_20250124', 'name' => 'str_replace_editor']
         // Sesudah:
         tools: [new ToolTextEditor20250728()],
         // ...
     );
     ```

     ```ruby Ruby
     # Sebelum
     legacy_tools = [{type: "text_editor_20250124", name: "str_replace_editor"}]

     # Sesudah
     tools = [{type: "text_editor_20250728", name: "str_replace_based_edit_tool"}]
     ```
   </CodeGroup>

   * **Text editor:** Gunakan `text_editor_20250728` dan `str_replace_based_edit_tool`. Lihat dokumentasi [Alat text editor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool) untuk detailnya.
   * **Code execution:** Tingkatkan ke `code_execution_20260521`. Lihat dokumentasi [Alat code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) untuk instruksi migrasi.
   * **Computer use:** Pada Claude API dan Claude Models on Google Cloud (Google managed), Claude Opus 5.5 hanya menerima computer use sebagai toolset `computer_toolset_20260801`: alat `computer_20250124` dan `computer_20251124` yang lebih lama ditolak di sana. Lihat [perubahan computer use yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#computer-use-toolset).

3. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals):

   <CodeGroup exclude="shell">
     ```python Python
     response = client.messages.create(...)

     if response.stop_reason == "refusal":
         # Tangani penolakan dengan tepat
         pass
     ```

     ```typescript TypeScript
     const response = await client.messages.create(/* ... */);

     if (response.stop_reason === "refusal") {
       // Tangani penolakan dengan tepat
     }
     ```

     ```csharp C#
     var response = await client.Messages.Create(...);

     if (response.StopReason?.Value() == StopReason.Refusal)
     {
         // Tangani penolakan dengan tepat
     }
     ```

     ```go Go
     response, _ := client.Messages.New(ctx, params) // your existing request

     if response.StopReason == anthropic.StopReasonRefusal {
     	// Tangani penolakan dengan tepat
     }
     ```

     ```java Java
     Message response = client.messages().create(...);

     StopReason reason = response.stopReason().orElse(StopReason.END_TURN);
     if (reason.equals(StopReason.REFUSAL)) {
         // Tangani penolakan dengan tepat
     }
     ```

     ```php PHP
     $response = $client->messages->create(...);

     if ($response->stopReason === 'refusal') {
         // Tangani penolakan dengan tepat
     }
     ```

     ```ruby Ruby
     response = client.messages.create(...)

     if response.stop_reason == :refusal
       # Tangani penolakan dengan tepat
     end
     ```
   </CodeGroup>

4. **Tangani stop reason `model_context_window_exceeded`**

   Claude 4.5 dan model yang lebih baru mengembalikan stop reason `model_context_window_exceeded` ketika generasi berhenti karena mencapai batas jendela konteks, bukan batas `max_tokens` yang diminta. Perbarui aplikasi Anda untuk menangani stop reason baru ini:

   <CodeGroup exclude="shell">
     ```python Python
     response = client.messages.create(...)

     if response.stop_reason == "model_context_window_exceeded":
         # Tangani batas jendela konteks dengan tepat
         pass
     ```

     ```typescript TypeScript
     const response = await client.messages.create(/* ... */);

     if (response.stop_reason === "model_context_window_exceeded") {
       // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```csharp C#
     var response = await client.Messages.Create(...);

     if (response.StopReason?.Raw() == "model_context_window_exceeded")
     {
         // Tangani batas "context window" (jendela konteks) dengan tepat
     }
     ```

     ```go Go
     response, _ := client.Messages.New(ctx, params) // your existing request

     if response.StopReason == "model_context_window_exceeded" {
     	// Tangani batas jendela konteks dengan tepat
     }
     ```

     ```java Java
     Message response = client.messages().create(...);

     StopReason reason = response.stopReason().orElse(StopReason.END_TURN);
     if (reason.equals(StopReason.of("model_context_window_exceeded"))) {
         // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```php PHP
     $response = $client->messages->create(...);

     if ($response->stopReason === 'model_context_window_exceeded') {
         // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```ruby Ruby
     response = client.messages.create(...)

     if response.stop_reason == :model_context_window_exceeded
       # Tangani batas jendela konteks dengan tepat
     end
     ```
   </CodeGroup>

5. **Verifikasi penanganan parameter alat (trailing newline)**

   Claude 4.5 dan model yang lebih baru mempertahankan trailing newline dalam parameter string panggilan alat yang sebelumnya dihapus. Jika alat Anda bergantung pada pencocokan string yang persis terhadap parameter panggilan alat, verifikasi bahwa logika Anda menangani trailing newline dengan benar.

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Claude 4 dan model yang lebih baru memiliki gaya komunikasi yang lebih ringkas dan langsung serta memerlukan arahan eksplisit. Tinjau [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

#### Perubahan tambahan yang direkomendasikan

* **Hapus beta header lama:** Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19`. Semua model Claude 4 dan yang lebih baru memiliki penggunaan alat yang efisien token bawaan dan header-header ini tidak berpengaruh.

## Migrasi ke Claude Opus 5.5 dari Claude Sonnet 5

Kerjakan [Yang harus dipenuhi setiap permintaan ke Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#request-requirements), [Menangani thinking di setiap respons](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-in-every-response), dan [Migrasi ke Claude Opus 5.5 dari Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-5). Gunakan `claude-sonnet-5` sebagai ID model yang Anda ganti. Bagian terakhir tersebut berlaku untuk kode pada Claude Sonnet 5 sebagaimana tertulis, karena Claude Sonnet 5, seperti Claude Opus 5:

* Berjalan dengan thinking aktif secara default dan menerima `thinking: {"type": "disabled"}`, dalam kasusnya pada tingkat effort apa pun.
* Menerima forced tool choice dan alat `computer_20251124`.
* Mengembalikan teks di antara panggilan alat sebagai blok `text`.
* Secara default menggunakan effort `high`.

Pemikiran diperpanjang manual, parameter sampling , dan prefill asisten mengembalikan error 400 pada kedua model, sehingga tidak ada yang berubah di sana. Tidak ada perubahan wajib dalam bagian untuk Claude Opus 4.8, Claude Opus 4.7, dan Claude Opus 4.6 yang berlaku untuk Anda.

### Apa yang berubah

1. **Pesan sistem di tengah percakapan:** Pada Claude API, Amazon Bedrock, dan Claude Models on Google Cloud (Google managed), Claude Opus 5.5 menerima pesan `role: "system"` tepat setelah giliran pengguna dalam array `messages` (tunduk pada [aturan penempatan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Fitur ini tidak tersedia di Claude Sonnet 5. Jika Anda memelihara jalur kode yang membangun ulang seluruh riwayat pesan untuk memperbarui instruksi, Anda dapat menyederhanakannya dan mempertahankan hit [prompt cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya.

2. **Minimum caching prompt yang lebih rendah:** Panjang prompt minimum yang dapat di-cache pada Claude Opus 5.5 adalah 512 token, turun dari 1.024 token pada Claude Sonnet 5. Prompt yang terlalu pendek untuk di-cache pada Claude Sonnet 5 dapat membuat entri cache, tanpa memerlukan perubahan kode. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.
