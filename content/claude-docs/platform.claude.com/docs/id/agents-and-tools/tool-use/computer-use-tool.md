---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: f41ac169f74fa53a01016d9a3ed82a7ec75544bcbb867ac8b66bc0e8f7e7dedc
---

# Alat computer use

Berikan Claude kontrol tangkapan layar, mouse, dan keyboard atas lingkungan desktop dengan alat computer use.

---

Claude dapat berinteraksi dengan lingkungan komputer melalui alat computer use, yang menyediakan kemampuan tangkapan layar dan kontrol mouse/keyboard untuk interaksi desktop secara otonom.

<Note>
  Computer use berada dalam tahap beta dan memerlukan [header beta](/docs/id/api/beta-headers):

  * `"computer-use-2025-11-24"` untuk Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Opus 4.5
  * `"computer-use-2025-01-24"` untuk Claude Sonnet 4.5, Claude Haiku 4.5, Claude Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)), Claude Sonnet 4 ([dihentikan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations)), dan Claude Opus 4 ([dihentikan, kecuali di Google Cloud](/docs/id/about-claude/model-deprecations))

  Hubungi kami melalui [formulir umpan balik](https://forms.gle/H6UFuXaaLywri9hz6) untuk membagikan umpan balik Anda tentang fitur ini.
</Note>

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

## Ikhtisar

Computer use adalah fitur beta yang memungkinkan Claude berinteraksi dengan lingkungan desktop. Alat ini menyediakan:

* **Pengambilan tangkapan layar:** Melihat apa yang saat ini ditampilkan di layar
* **Kontrol mouse:** Klik, seret, dan gerakkan kursor
* **Input keyboard:** Mengetik teks dan menggunakan pintasan keyboard
* **Otomatisasi desktop:** Berinteraksi dengan aplikasi atau antarmuka apa pun

Meskipun computer use dapat ditambah dengan alat lain seperti bash dan text editor untuk alur kerja otomatisasi yang lebih komprehensif, computer use secara khusus mengacu pada kemampuan alat computer use untuk melihat dan mengontrol lingkungan desktop.

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Pertimbangan keamanan

Computer use adalah fitur beta dengan risiko unik yang berbeda dari fitur API standar. Risiko ini meningkat saat berinteraksi dengan internet.

<Warning>
  Untuk meminimalkan risiko, pertimbangkan untuk mengambil tindakan pencegahan seperti:

  1. Menggunakan mesin virtual atau container khusus dengan hak istimewa minimal untuk mencegah serangan sistem langsung atau kecelakaan.
  2. Menghindari memberikan model akses ke data sensitif, seperti informasi login akun, untuk mencegah pencurian informasi.
  3. Membatasi akses internet ke daftar domain yang diizinkan untuk mengurangi paparan terhadap konten berbahaya.
  4. Meminta manusia untuk mengonfirmasi keputusan yang mungkin mengakibatkan konsekuensi nyata yang berarti dan tugas apa pun yang memerlukan persetujuan afirmatif, seperti menerima cookie, menyelesaikan transaksi keuangan, atau menyetujui ketentuan layanan.
</Warning>

Dalam beberapa keadaan, Claude akan mengikuti perintah yang ditemukan dalam konten bahkan ketika bertentangan dengan instruksi Anda. Misalnya, instruksi di halaman web atau yang terkandung dalam gambar mungkin menimpa instruksi Anda atau menyebabkan Claude membuat kesalahan. Ambil tindakan pencegahan untuk mengisolasi Claude dari data dan tindakan sensitif untuk menghindari risiko terkait prompt injection.

Anthropic telah melatih model untuk menahan prompt injection ini dan telah menambahkan lapisan pertahanan ekstra. Jika Anda menggunakan alat computer use, classifier akan secara otomatis berjalan pada prompt Anda untuk menandai kemungkinan kasus prompt injection. Ketika classifier ini mengidentifikasi potensi prompt injection dalam tangkapan layar, mereka akan secara otomatis mengarahkan model untuk meminta konfirmasi pengguna sebelum melanjutkan dengan tindakan berikutnya. Perlindungan ekstra ini tidak akan ideal untuk setiap kasus penggunaan (misalnya, kasus penggunaan tanpa manusia dalam prosesnya), jadi jika Anda ingin memilih keluar dan menonaktifkannya, [hubungi dukungan](https://support.claude.com/en/).

Tindakan pencegahan ini tetap penting bahkan dengan lapisan pertahanan classifier yang sudah ada.

Informasikan pengguna akhir tentang risiko yang relevan dan dapatkan persetujuan mereka sebelum mengaktifkan computer use di produk Anda sendiri.

<Card title="Implementasi referensi computer use" icon="computer" href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo">
  Mulai dengan implementasi referensi computer use yang mencakup antarmuka web, container Docker, contoh implementasi alat, dan agent loop.
</Card>

## Mulai cepat

Berikut cara memulai dengan computer use:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: computer-use-2025-11-24" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "tools": [
        {
          "type": "computer_20251124",
          "name": "computer",
          "display_width_px": 1024,
          "display_height_px": 768,
          "display_number": 1
        },
        {
          "type": "text_editor_20250728",
          "name": "str_replace_based_edit_tool"
        },
        {
          "type": "bash_20250124",
          "name": "bash"
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Save a picture of a cat to my desktop."
        }
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta computer-use-2025-11-24 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  tools:
    - type: computer_20251124
      name: computer
      display_width_px: 1024
      display_height_px: 768
      display_number: 1
    - type: text_editor_20250728
      name: str_replace_based_edit_tool
    - type: bash_20250124
      name: bash
  messages:
    - role: user
      content: Save a picture of a cat to my desktop.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-4-8",  # or another compatible model
      max_tokens=1024,
      tools=[
          {
              "type": "computer_20251124",
              "name": "computer",
              "display_width_px": 1024,
              "display_height_px": 768,
              "display_number": 1,
          },
          {"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"},
          {"type": "bash_20250124", "name": "bash"},
      ],
      messages=[{"role": "user", "content": "Save a picture of a cat to my desktop."}],
      betas=["computer-use-2025-11-24"],
  )
  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [
      {
        type: "computer_20251124",
        name: "computer",
        display_width_px: 1024,
        display_height_px: 768,
        display_number: 1
      },
      {
        type: "text_editor_20250728",
        name: "str_replace_based_edit_tool"
      },
      {
        type: "bash_20250124",
        name: "bash"
      }
    ],
    messages: [{ role: "user", content: "Save a picture of a cat to my desktop." }],
    betas: ["computer-use-2025-11-24"]
  });

  console.log(response);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  var client = new AnthropicClient();

  var parameters = new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = new BetaToolUnion[]
      {
          new BetaToolComputerUse20251124
          {
              DisplayWidthPx = 1024,
              DisplayHeightPx = 768,
              DisplayNumber = 1
          },
          new BetaToolTextEditor20250728(),
          new BetaToolBash20250124()
      },
      Messages =
      [
          new BetaMessageParam
          {
              Role = Role.User,
              Content = "Save a picture of a cat to my desktop."
          }
      ],
      Betas = ["computer-use-2025-11-24"]
  };

  var response = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfComputerUseTool20251124: &anthropic.BetaToolComputerUse20251124Param{
  			DisplayWidthPx:  1024,
  			DisplayHeightPx: 768,
  			DisplayNumber:   anthropic.Int(1),
  		}},
  		{OfTextEditor20250728: &anthropic.BetaToolTextEditor20250728Param{}},
  		{OfBashTool20250124: &anthropic.BetaToolBash20250124Param{}},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Save a picture of a cat to my desktop.")),
  	},
  	Betas: []anthropic.AnthropicBeta{
  		"computer-use-2025-11-24", // no SDK exposes a named constant for this beta yet
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaToolBash20250124;
  import com.anthropic.models.beta.messages.BetaToolComputerUse20251124;
  import com.anthropic.models.beta.messages.BetaToolTextEditor20250728;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(BetaToolComputerUse20251124.builder()
              .displayWidthPx(1024L)
              .displayHeightPx(768L)
              .displayNumber(1L)
              .build())
          .addTool(BetaToolTextEditor20250728.builder().build())
          .addTool(BetaToolBash20250124.builder().build())
          .addUserMessage("Save a picture of a cat to my desktop.")
          .addBeta("computer-use-2025-11-24")
          .build();

      BetaMessage response = client.beta().messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Save a picture of a cat to my desktop.'],
      ],
      model: 'claude-opus-4-8',
      tools: [
          [
              'type' => 'computer_20251124',
              'name' => 'computer',
              'display_width_px' => 1024,
              'display_height_px' => 768,
              'display_number' => 1,
          ],
          [
              'type' => 'text_editor_20250728',
              'name' => 'str_replace_based_edit_tool',
          ],
          [
              'type' => 'bash_20250124',
              'name' => 'bash',
          ],
      ],
      betas: ['computer-use-2025-11-24'],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [
      {
        type: "computer_20251124",
        name: "computer",
        display_width_px: 1024,
        display_height_px: 768,
        display_number: 1
      },
      {
        type: "text_editor_20250728",
        name: "str_replace_based_edit_tool"
      },
      {
        type: "bash_20250124",
        name: "bash"
      }
    ],
    messages: [
      { role: "user", content: "Save a picture of a cat to my desktop." }
    ],
    betas: ["computer-use-2025-11-24"]
  )

  puts response
  ```
</CodeGroup>

<Note>
  Header beta hanya diperlukan untuk alat computer use.

  Contoh sebelumnya menunjukkan ketiga alat digunakan bersama, yang memerlukan header beta karena menyertakan alat computer use.
</Note>

***

## Cara kerja computer use

<Steps>
  <Step title="Berikan Claude alat computer use dan prompt pengguna" icon="tool">
    * Tambahkan alat computer use (dan opsional alat lainnya) ke permintaan API Anda.
    * Sertakan prompt pengguna yang memerlukan interaksi desktop, misalnya, "Simpan gambar kucing ke desktop saya."
  </Step>

  <Step title="Claude memilih alat computer use" icon="wrench">
    * Claude menilai apakah alat computer use dapat membantu dengan kueri pengguna.
    * Jika ya, Claude membangun permintaan penggunaan alat yang diformat dengan benar.
    * Respons API memiliki `stop_reason` berupa `tool_use`, yang menandakan permintaan penggunaan alat.
  </Step>

  <Step title="Ekstrak input alat, evaluasi alat di komputer, dan kembalikan hasilnya" icon="computer">
    * Di sisi Anda, ekstrak nama alat dan input dari permintaan Claude.
    * Gunakan alat tersebut di container atau mesin virtual.
    * Lanjutkan percakapan dengan pesan `user` baru yang berisi blok konten `tool_result`.
  </Step>

  <Step title="Claude terus memanggil alat computer use hingga tugas selesai" icon="arrows-clockwise">
    * Claude menganalisis hasil alat untuk menentukan apakah penggunaan alat lebih lanjut diperlukan atau tugas telah selesai.
    * Jika Claude menentukan bahwa alat lain diperlukan, ia merespons dengan `stop_reason` `tool_use` lainnya dan Anda harus kembali ke langkah 3.
    * Jika tidak, ia menyusun respons teks untuk pengguna.
  </Step>
</Steps>

Pengulangan langkah 3 dan 4 tanpa input pengguna disebut sebagai "agent loop" (yaitu, Claude merespons dengan permintaan penggunaan alat dan aplikasi Anda merespons Claude dengan hasil evaluasi permintaan tersebut).

### Lingkungan komputasi

Computer use memerlukan lingkungan komputasi yang di-sandbox di mana Claude dapat berinteraksi dengan aplikasi dan web secara aman. Lingkungan ini mencakup:

1. **Tampilan virtual:** Server tampilan X11 virtual (menggunakan Xvfb) yang merender antarmuka desktop yang akan dilihat Claude melalui tangkapan layar dan dikontrol dengan tindakan mouse/keyboard.

2. **Lingkungan desktop:** UI ringan dengan window manager (Mutter) dan panel (Tint2) yang berjalan di Linux, yang menyediakan antarmuka grafis yang konsisten untuk berinteraksi dengan Claude.

3. **Aplikasi:** Aplikasi Linux yang sudah terpasang seperti Firefox, LibreOffice, text editor, dan file manager yang dapat digunakan Claude untuk menyelesaikan tugas.

4. **Implementasi alat:** Kode integrasi yang menerjemahkan permintaan alat abstrak Claude (seperti "gerakkan mouse" atau "ambil tangkapan layar") menjadi operasi aktual di lingkungan virtual.

5. **Agent loop:** Program yang menangani komunikasi antara Claude dan lingkungan, mengirimkan tindakan Claude ke lingkungan dan mengembalikan hasilnya (tangkapan layar, output perintah) kembali ke Claude.

Saat Anda menggunakan computer use, Claude tidak terhubung langsung ke lingkungan ini. Sebaliknya, aplikasi Anda:

1. Menerima permintaan penggunaan alat dari Claude
2. Menerjemahkannya menjadi tindakan di lingkungan komputasi Anda
3. Menangkap hasilnya (seperti tangkapan layar dan output perintah)
4. Mengembalikan hasil ini ke Claude

Untuk keamanan dan isolasi, implementasi referensi menjalankan semua ini di dalam container Docker dengan pemetaan port yang sesuai untuk melihat dan berinteraksi dengan lingkungan.

***

## Cara mengimplementasikan computer use

### Mulai dengan implementasi referensi

[Implementasi referensi](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) tersedia yang mencakup semua yang Anda butuhkan untuk memulai dengan computer use:

* [Lingkungan terkontainerisasi](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/Dockerfile) yang cocok untuk computer use dengan Claude
* Implementasi dari [alat computer use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo/computer_use_demo/tools)
* [Agent loop](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/computer_use_demo/loop.py) yang berinteraksi dengan Claude API dan menjalankan alat computer use
* Antarmuka web untuk berinteraksi dengan container, agent loop, dan alat.

### Pahami agent loop

Inti dari computer use adalah "agent loop": siklus di mana Claude meminta tindakan alat, aplikasi Anda menjalankannya, dan mengembalikan hasilnya ke Claude. Loop ini menggunakan klien yang Anda buat di [Mulai cepat](#quick-start), daftar alat yang berbentuk seperti array `tools` di Mulai cepat, dan helper pemrosesan panggilan alat yang didefinisikan di [Proses panggilan alat Claude](#implement-the-computer-use-tool). Berikut contoh yang disederhanakan:

<CodeGroup>
  ```bash cURL
  # Loop agen adalah pola stateful multi-giliran yang tidak dapat diubah menjadi
  # perintah shell sekali jalan. Lihat tab SDK untuk implementasinya.
  ```

  ```bash CLI
  # Loop agen adalah pola stateful multi-giliran yang tidak dapat diubah menjadi
  # perintah shell sekali jalan. Lihat tab SDK untuk implementasinya.
  ```

  ```python Python
  def sampling_loop(model, messages, max_iterations=10):
      """
      Run the computer-use agent loop until Claude stops requesting tools
      or the iteration limit is reached.
      """
      for _ in range(max_iterations):
          response = client.beta.messages.create(
              model=model,
              max_tokens=4096,
              messages=messages,
              tools=TOOLS,
              betas=["computer-use-2025-11-24"],
          )

          # Tambahkan respons Claude ke riwayat percakapan
          messages.append({"role": "assistant", "content": response.content})

          # Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
          tool_results = process_tool_calls(response)
          if not tool_results:
              return messages  # No more tool use; task complete

          # Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
          messages.append({"role": "user", "content": tool_results})

      return messages
  ```

  ```typescript TypeScript
  async function samplingLoop(
    model: string,
    messages: Anthropic.Beta.BetaMessageParam[],
    maxIterations = 10,
  ): Promise<Anthropic.Beta.BetaMessageParam[]> {
    // Jalankan loop agen computer-use hingga Claude berhenti meminta alat
    // atau batas iterasi tercapai.
    for (let i = 0; i < maxIterations; i++) {
      const response = await client.beta.messages.create({
        model,
        max_tokens: 4096,
        messages,
        tools,
        betas: ["computer-use-2025-11-24"],
      });

      // Tambahkan respons Claude ke riwayat percakapan
      messages.push({ role: "assistant", content: response.content });

      // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
      const toolResults = processToolCalls(response);
      if (toolResults.length === 0) {
        return messages; // No more tool use; task complete
      }

      // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
      messages.push({ role: "user", content: toolResults });
    }

    return messages;
  }
  ```

  ```csharp C#
  async Task<List<BetaMessageParam>> SamplingLoop(
      Model model,
      List<BetaMessageParam> messages,
      int maxIterations = 10
  )
  {
      // Jalankan loop agen computer-use hingga Claude berhenti meminta alat
      // atau batas iterasi tercapai.
      for (var i = 0; i < maxIterations; i++)
      {
          var response = await client.Beta.Messages.Create(
              new MessageCreateParams
              {
                  Model = model,
                  MaxTokens = 4096,
                  Messages = messages,
                  Tools = tools,
                  Betas = ["computer-use-2025-11-24"],
              }
          );

          // Tambahkan respons Claude ke riwayat percakapan
          messages.Add(
              new()
              {
                  Role = Role.Assistant,
                  Content = response
                      .Content.Select(block => new BetaContentBlockParam(block.Json))
                      .ToList(),
              }
          );

          // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
          var toolResults = ProcessToolCalls(response);
          if (toolResults.Count == 0)
          {
              return messages; // No more tool use; task complete
          }

          // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
          messages.Add(new() { Role = Role.User, Content = toolResults });
      }

      return messages;
  }
  ```

  ```go Go
  // samplingLoop menjalankan loop agen computer-use hingga Claude berhenti
  // meminta alat atau batas iterasi tercapai.
  func samplingLoop(ctx context.Context, model anthropic.Model, messages []anthropic.BetaMessageParam, maxIterations int) ([]anthropic.BetaMessageParam, error) {
  	for range maxIterations {
  		response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  			Model:     model,
  			MaxTokens: 4096,
  			Messages:  messages,
  			Tools:     tools,
  			Betas:     []anthropic.AnthropicBeta{"computer-use-2025-11-24"},
  		})
  		if err != nil {
  			return nil, err
  		}

  		// Tambahkan respons Claude ke riwayat percakapan
  		messages = append(messages, response.ToParam())

  		// Jalankan alat yang diminta Claude dan kumpulkan hasilnya
  		toolResults := processToolCalls(response)
  		if len(toolResults) == 0 {
  			return messages, nil // No more tool use; task complete
  		}

  		// Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
  		messages = append(messages, anthropic.BetaMessageParam{
  			Role:    anthropic.BetaMessageParamRoleUser,
  			Content: toolResults,
  		})
  	}
  	return messages, nil
  }

  ```

  ```java Java
  /**
   * Run the computer-use agent loop until Claude stops requesting tools
   * or the iteration limit is reached.
   */
  List<BetaMessageParam> samplingLoop(Model model, List<BetaMessageParam> messages, int maxIterations) {
      for (int i = 0; i < maxIterations; i++) {
          BetaMessage response = client.beta().messages().create(MessageCreateParams.builder()
                  .model(model)
                  .maxTokens(4096)
                  .messages(messages)
                  .addTool(COMPUTER_TOOL)
                  .addBeta("computer-use-2025-11-24")
                  .build());

          // Tambahkan respons Claude ke riwayat percakapan
          messages.add(BetaMessageParam.builder()
                  .role(BetaMessageParam.Role.ASSISTANT)
                  .contentOfBetaContentBlockParams(
                          response.content().stream().map(BetaContentBlock::toParam).toList())
                  .build());

          // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
          List<BetaContentBlockParam> toolResults = processToolCalls(response);
          if (toolResults.isEmpty()) {
              return messages; // No more tool use; task complete
          }

          // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
          messages.add(BetaMessageParam.builder()
                  .role(BetaMessageParam.Role.USER)
                  .contentOfBetaContentBlockParams(toolResults)
                  .build());
      }
      return messages;
  }
  ```

  ```php PHP
  /**
   * Run the computer-use agent loop until Claude stops requesting tools
   * or the iteration limit is reached.
   */
  function samplingLoop(string $model, array $messages, int $maxIterations = 10): array
  {
      global $client, $tools;

      for ($i = 0; $i < $maxIterations; $i++) {
          $response = $client->beta->messages->create(
              model: $model,
              maxTokens: 4096,
              messages: $messages,
              tools: $tools,
              betas: ['computer-use-2025-11-24'],
          );

          // Tambahkan respons Claude ke riwayat percakapan
          $messages[] = BetaMessageParam::with(role: Role::ASSISTANT, content: $response->content);

          // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
          $toolResults = processToolCalls($response);
          if ($toolResults === []) {
              return $messages; // No more tool use; task complete
          }

          // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
          $messages[] = BetaMessageParam::with(role: Role::USER, content: $toolResults);
      }

      return $messages;
  }
  ```

  ```ruby Ruby
  # Jalankan loop agen computer-use hingga Claude berhenti meminta alat
  # atau batas iterasi tercapai.
  def sampling_loop(model, messages, max_iterations: 10)
    max_iterations.times do
      response = CLIENT.beta.messages.create(
        model: model,
        max_tokens: 4096,
        messages: messages,
        tools: TOOLS,
        betas: ["computer-use-2025-11-24"]
      )

      # Tambahkan respons Claude ke riwayat percakapan
      messages << {role: "assistant", content: response.content}

      # Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
      tool_results = process_tool_calls(response)
      return messages if tool_results.empty? # No more tool use; task complete

      # Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
      messages << {role: "user", content: tool_results}
    end

    messages
  end
  ```
</CodeGroup>

Loop berlanjut hingga Claude merespons tanpa meminta alat apa pun (penyelesaian tugas) atau batas iterasi maksimum tercapai. Pengaman ini mencegah potensi loop tak terbatas yang dapat mengakibatkan biaya API yang tidak terduga.

Cobalah implementasi referensi sebelum membaca sisa dokumentasi ini.

### Optimalkan kinerja model dengan prompting

Berikut beberapa tips tentang cara mendapatkan output dengan kualitas terbaik:

1. Tentukan tugas yang sederhana dan terdefinisi dengan baik serta berikan instruksi eksplisit untuk setiap langkah.
2. Claude terkadang mengasumsikan hasil dari tindakannya tanpa secara eksplisit memeriksa hasilnya. Untuk mencegah hal ini, Anda dapat memberi prompt kepada Claude dengan `After each step, take a screenshot and carefully evaluate if you have achieved the right outcome. Explicitly show your thinking: "I have evaluated step X..." If not correct, try again. Only when you confirm a step was executed correctly should you move on to the next one.`
3. Beberapa elemen UI (seperti dropdown dan scrollbar) mungkin sulit dimanipulasi oleh Claude menggunakan gerakan mouse. Jika Anda mengalami hal ini, coba beri prompt kepada model untuk menggunakan pintasan keyboard.
4. Untuk tugas berulang atau interaksi UI, sertakan contoh tangkapan layar dan panggilan alat dari hasil yang berhasil dalam prompt Anda.
5. Jika Anda memerlukan model untuk login, berikan nama pengguna dan kata sandi dalam prompt Anda di dalam tag XML seperti `<robot_credentials>`. Menggunakan computer use dalam aplikasi yang memerlukan login meningkatkan risiko hasil buruk sebagai akibat dari prompt injection. Tinjau [Mitigasi jailbreak dan prompt injection](/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) sebelum memberikan kredensial login kepada model.
6. Saat membangun array `content` dari giliran pengguna, tempatkan teks instruksi *sebelum* gambar tangkapan layar. Memberikan deskripsi target sebelum gambar diproses meningkatkan akurasi klik.
7. Saat menggunakan `computer_20251124` dengan `enable_zoom: true` diatur, Claude memperbesar suatu wilayah ketika ditanya tentang teks kecil atau elemen UI tertentu yang tidak terbaca pada resolusi default tangkapan layar, seperti nama file di sidebar, judul tab, teks status-bar, nomor baris, atau label tombol. Jika Claude tidak memperbesar saat Anda mengharapkannya, tanyakan tentang wilayah atau elemen tertentu daripada layar secara keseluruhan.

<Tip>
  Jika Anda berulang kali menemukan serangkaian masalah yang jelas atau mengetahui sebelumnya tugas yang perlu diselesaikan Claude, gunakan prompt sistem untuk memberikan Claude tips atau instruksi eksplisit tentang cara melakukan tugas dengan sukses.
</Tip>

<Tip>
  Untuk agen yang mencakup beberapa sesi, jalankan verifikasi end-to-end di awal setiap sesi, bukan hanya setelah implementasi. Pemeriksaan berbasis browser menangkap regresi dari sesi sebelumnya yang terlewat oleh tinjauan tingkat kode saja. Lihat [Harness yang efektif untuk agen yang berjalan lama](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) untuk detailnya.
</Tip>

### Prompt sistem

Ketika salah satu alat skema Anthropic diminta melalui Claude API, prompt sistem khusus computer use akan dihasilkan. Ini mirip dengan [prompt sistem penggunaan alat](/docs/id/agents-and-tools/tool-use/define-tools#tool-use-system-prompt) tetapi dimulai dengan:

> You have access to a set of functions you can use to answer the user's question. This includes access to a sandboxed computing environment. You do NOT currently have the ability to inspect files or interact with external resources, except by invoking the below functions.

Seperti penggunaan alat biasa, parameter `system` yang disediakan pengguna tetap dihormati dan digunakan dalam pembangunan prompt sistem gabungan.

### Tindakan yang tersedia

Alat computer use mendukung tindakan-tindakan berikut:

**Tindakan dasar (semua versi)**

* **screenshot:** Menangkap tampilan saat ini
* **left\_click:** Klik pada koordinat `[x, y]`
* **type:** Mengetik string teks
* **key:** Menekan tombol atau kombinasi tombol (misalnya, "ctrl+s")
* **mouse\_move:** Memindahkan kursor ke koordinat

**Tindakan yang ditingkatkan (`computer_20250124` dan yang lebih baru)** Tersedia di `computer_20250124` dan `computer_20251124`:

* **scroll:** Menggulir ke segala arah dengan kontrol jumlah
* **left\_click\_drag:** Klik dan seret antar koordinat
* **right\_click**, **middle\_click:** Tombol mouse tambahan
* **double\_click**, **triple\_click:** Klik berganda
* **left\_mouse\_down**, **left\_mouse\_up:** Kontrol klik yang lebih terperinci
* **hold\_key:** Menahan tombol selama durasi tertentu (dalam detik)
* **wait:** Jeda antar tindakan

**Tindakan yang ditingkatkan (`computer_20251124`)** Tersedia di Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Opus 4.5:

* Semua tindakan dari `computer_20250124`
* **zoom:** Melihat wilayah tertentu dari layar pada resolusi penuh. Memerlukan `enable_zoom: true` dalam definisi alat. Mengambil parameter `region` dengan koordinat `[x1, y1, x2, y2]` yang mendefinisikan sudut kiri-atas dan kanan-bawah dari area yang akan diperiksa.

<Accordion title="Contoh tindakan">
  Ambil tangkapan layar:

  ```json
  {
    "action": "screenshot"
  }
  ```

  Klik pada posisi:

  ```json
  {
    "action": "left_click",
    "coordinate": [500, 300]
  }
  ```

  Ketik teks:

  ```json
  {
    "action": "type",
    "text": "Hello, world!"
  }
  ```

  Gulir ke bawah:

  ```json
  {
    "action": "scroll",
    "coordinate": [500, 400],
    "scroll_direction": "down",
    "scroll_amount": 3
  }
  ```

  Zoom untuk melihat wilayah secara detail (Claude Sonnet 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6, dan Opus 4.5):

  ```json
  {
    "action": "zoom",
    "region": [100, 200, 400, 350]
  }
  ```
</Accordion>

<Accordion title="Tombol modifier dengan tindakan klik dan gulir">
  Untuk menahan tombol modifier (seperti Shift, Ctrl, atau Alt) saat melakukan tindakan klik atau gulir, gunakan parameter `text` pada tindakan tersebut. Ini berbeda dari `hold_key`, yang menahan tombol selama durasi tertentu tanpa melakukan tindakan lain.

  Shift+klik (misalnya, untuk memilih rentang item):

  ```json
  {
    "action": "left_click",
    "coordinate": [500, 300],
    "text": "shift"
  }
  ```

  Ctrl+klik (misalnya, untuk multi-pilih di Windows/Linux):

  ```json
  {
    "action": "left_click",
    "coordinate": [500, 300],
    "text": "ctrl"
  }
  ```

  Cmd+klik (misalnya, untuk multi-pilih di macOS):

  ```json
  {
    "action": "left_click",
    "coordinate": [500, 300],
    "text": "super"
  }
  ```

  Shift+gulir (misalnya, untuk menggulir secara horizontal):

  ```json
  {
    "action": "scroll",
    "coordinate": [500, 400],
    "scroll_direction": "down",
    "scroll_amount": 3,
    "text": "shift"
  }
  ```

  Parameter `text` dalam tindakan klik/gulir menerima tombol modifier seperti `shift`, `ctrl`, `alt`, dan `super` (untuk tombol Command/Windows).
</Accordion>

### Parameter alat

| Parameter           | Wajib | Deskripsi                                                                                                                                             |
| ------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`              | Ya    | Versi alat (`computer_20251124` atau `computer_20250124`)                                                                                             |
| `name`              | Ya    | Harus "computer"                                                                                                                                      |
| `display_width_px`  | Ya    | Lebar tampilan dalam piksel                                                                                                                           |
| `display_height_px` | Ya    | Tinggi tampilan dalam piksel                                                                                                                          |
| `display_number`    | Tidak | Nomor tampilan untuk lingkungan X11                                                                                                                   |
| `enable_zoom`       | Tidak | Mengaktifkan tindakan zoom (hanya `computer_20251124`). Atur ke `true` untuk memungkinkan Claude memperbesar wilayah layar tertentu. Default: `false` |

<Note>
  **Penting:** Aplikasi Anda harus secara eksplisit menjalankan alat computer use; Claude tidak dapat menjalankannya secara langsung. Anda bertanggung jawab untuk mengimplementasikan pengambilan tangkapan layar, gerakan mouse, input keyboard, dan tindakan lainnya berdasarkan permintaan Claude.
</Note>

### Menggabungkan dengan pemikiran diperpanjang

Untuk menggabungkan computer use dengan pemikiran diperpanjang, lihat [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking).

<Tip>
  Khusus untuk computer use, benchmark internal menyarankan pengaturan `effort` berikut:

  * **Claude Opus 4.7:** gunakan `high` sebagai default; gunakan `low` untuk beban kerja throughput tinggi atau yang sensitif terhadap biaya.
  * **Claude Sonnet 4.6 dan Claude Opus 4.6:** gunakan `medium` sebagai default (rasio akurasi-terhadap-biaya terbaik). Hindari `max`, yang menambah biaya token tanpa meningkatkan akurasi pada tugas UI. Pada model-model ini, `low` menggunakan *lebih sedikit* token output dibandingkan menonaktifkan pemikiran sepenuhnya (lebih sedikit kesalahan berarti lebih sedikit percobaan ulang), menjadikannya opsi yang kuat untuk loop yang sensitif terhadap biaya.
</Tip>

### Menambah computer use dengan alat lain

Untuk menambahkan alat lain bersama computer use, sertakan mereka dalam array `tools` yang sama. Bagian [Mulai cepat](#quick-start) menunjukkan pola ini dengan [alat bash](/docs/id/agents-and-tools/tool-use/bash-tool) dan [alat text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool). Anda dapat menambahkan [definisi alat kustom](/docs/id/agents-and-tools/tool-use/define-tools) Anda sendiri dengan cara yang sama.

### Bangun lingkungan computer use kustom

[Implementasi referensi](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) dimaksudkan untuk membantu Anda memulai dengan computer use. Ini mencakup semua komponen yang diperlukan agar Claude dapat menggunakan komputer. Namun, Anda dapat membangun lingkungan Anda sendiri untuk computer use sesuai kebutuhan Anda. Anda akan memerlukan:

* Lingkungan tervirtualisasi atau terkontainerisasi yang cocok untuk computer use dengan Claude
* Implementasi dari setidaknya satu alat computer use skema Anthropic
* Agent loop yang berinteraksi dengan Claude API dan menjalankan hasil `tool_use` menggunakan implementasi alat Anda
* API atau UI yang memungkinkan input pengguna untuk memulai agent loop

#### Implementasikan alat computer use

Alat computer use diimplementasikan sebagai alat tanpa skema. Saat menggunakan alat ini, Anda tidak perlu menyediakan skema input seperti alat lainnya; skema sudah terpasang di model Claude dan tidak dapat dimodifikasi.

<Steps>
  <Step title="Siapkan lingkungan komputasi Anda">
    Buat tampilan virtual atau hubungkan ke tampilan yang sudah ada yang akan diinteraksikan oleh Claude. Ini biasanya melibatkan pengaturan Xvfb (X Virtual Framebuffer) atau teknologi serupa.
  </Step>

  <Step title="Implementasikan handler tindakan">
    Buat fungsi untuk menangani setiap jenis tindakan yang mungkin diminta Claude:

    <CodeGroup>
      ```bash cURL
      # Ini adalah kode pembantu di sisi aplikasi tanpa permintaan API. Lihat tab SDK
      # untuk polanya.
      ```

      ```bash CLI
      # Ini adalah kode helper di sisi aplikasi tanpa permintaan API. Lihat tab SDK
      # untuk polanya.
      ```

      ```python Python
      def capture_screenshot():
          return "<screenshot data>"


      def click_at(x, y):
          return f"clicked at ({x}, {y})"


      def type_text(text):
          return f"typed: {text}"


      def handle_computer_action(action_type, params):
          if action_type == "screenshot":
              return capture_screenshot()
          elif action_type == "left_click":
              x, y = params["coordinate"]
              return click_at(x, y)
          elif action_type == "type":
              return type_text(params["text"])
          # Tangani tindakan lain sesuai kebutuhan
          return f"unhandled action: {action_type}"
      ```

      ```typescript TypeScript
      function captureScreenshot(): string {
        return "<screenshot data>";
      }

      function clickAt(x: number, y: number): string {
        return `clicked at (${x}, ${y})`;
      }

      function typeText(text: string): string {
        return `typed: ${text}`;
      }

      function handleComputerAction(
        actionType: string,
        params: Record<string, unknown>,
      ): string {
        if (actionType === "screenshot") {
          return captureScreenshot();
        } else if (actionType === "left_click") {
          const [x, y] = params.coordinate as [number, number];
          return clickAt(x, y);
        } else if (actionType === "type") {
          return typeText(params.text as string);
        }
        // Tangani aksi lainnya sesuai kebutuhan
        return `unhandled action: ${actionType}`;
      }
      ```

      ```csharp C#
      string CaptureScreenshot() => "<screenshot data>";

      string ClickAt(int x, int y) => $"clicked at ({x}, {y})";

      string TypeText(string text) => $"typed: {text}";

      string HandleComputerAction(string actionType, IReadOnlyDictionary<string, JsonElement> input) =>
          actionType switch
          {
              "screenshot" => CaptureScreenshot(),
              "left_click" => ClickAt(
                  input["coordinate"][0].GetInt32(),
                  input["coordinate"][1].GetInt32()
              ),
              "type" => TypeText(input["text"].GetString()!),
              // Tangani aksi lainnya sesuai kebutuhan
              _ => $"unhandled action: {actionType}",
          };
      ```

      ```go Go
      func captureScreenshot() string {
      	return "<screenshot data>"
      }

      func clickAt(x, y int) string {
      	return fmt.Sprintf("clicked at (%d, %d)", x, y)
      }

      func typeText(text string) string {
      	return fmt.Sprintf("typed: %s", text)
      }

      func handleComputerAction(actionType string, params map[string]any) string {
      	switch actionType {
      	case "screenshot":
      		return captureScreenshot()
      	case "left_click":
      		coord := params["coordinate"].([]any)
      		return clickAt(int(coord[0].(float64)), int(coord[1].(float64)))
      	case "type":
      		return typeText(params["text"].(string))
      	// Tangani aksi lainnya sesuai kebutuhan
      	default:
      		return fmt.Sprintf("unhandled action: %s", actionType)
      	}
      }

      ```

      ```java Java
      String captureScreenshot() {
          return "<screenshot data>";
      }

      String clickAt(long x, long y) {
          return "clicked at (" + x + ", " + y + ")";
      }

      String typeText(String text) {
          return "typed: " + text;
      }

      String handleComputerAction(String actionType, Map<String, JsonValue> params) {
          return switch (actionType) {
              case "screenshot" -> captureScreenshot();
              case "left_click" -> {
                  List<JsonValue> coordinate = (List<JsonValue>) params.get("coordinate").asArray().get();
                  long x = ((Number) coordinate.get(0).asNumber().get()).longValue();
                  long y = ((Number) coordinate.get(1).asNumber().get()).longValue();
                  yield clickAt(x, y);
              }
              case "type" -> typeText(params.get("text").asStringOrThrow());
              // Tangani aksi lain sesuai kebutuhan
              default -> "unhandled action: " + actionType;
          };
      }
      ```

      ```php PHP
      function captureScreenshot(): string
      {
          return '<screenshot data>';
      }

      function clickAt(int $x, int $y): string
      {
          return "clicked at ({$x}, {$y})";
      }

      function typeText(string $text): string
      {
          return "typed: {$text}";
      }

      function handleComputerAction(string $actionType, array $params): string
      {
          return match ($actionType) {
              'screenshot' => captureScreenshot(),
              'left_click' => clickAt(...$params['coordinate']),
              'type' => typeText($params['text']),
              // Tangani tindakan lain sesuai kebutuhan
              default => "unhandled action: {$actionType}",
          };
      }
      ```

      ```ruby Ruby
      def capture_screenshot
        "<screenshot data>"
      end

      def click_at(x, y)
        "clicked at (#{x}, #{y})"
      end

      def type_text(text)
        "typed: #{text}"
      end

      def handle_computer_action(action_type, params)
        case action_type
        when "screenshot"
          capture_screenshot
        when "left_click"
          x, y = params[:coordinate]
          click_at(x, y)
        when "type"
          type_text(params[:text])
        # Tangani aksi lainnya sesuai kebutuhan
        else
          "unhandled action: #{action_type}"
        end
      end
      ```
    </CodeGroup>
  </Step>

  <Step title="Proses panggilan alat Claude">
    Ekstrak dan jalankan panggilan alat dari respons Claude:

    <CodeGroup>
      ```bash cURL
      # Ini adalah kode helper di sisi aplikasi tanpa permintaan API. Lihat tab SDK
      # untuk polanya.
      ```

      ```bash CLI
      # Ini adalah kode helper di sisi aplikasi tanpa permintaan API. Lihat tab SDK
      # untuk polanya.
      ```

      ```python Python
      def process_tool_calls(response):
          tool_results = []
          for block in response.content:
              if block.type == "tool_use":
                  action = block.input["action"]
                  result = handle_computer_action(action, block.input)
                  tool_results.append(
                      {
                          "type": "tool_result",
                          "tool_use_id": block.id,
                          "content": result,
                      }
                  )
          return tool_results
      ```

      ```typescript TypeScript
      function processToolCalls(
        response: Anthropic.Beta.BetaMessage,
      ): Anthropic.Beta.BetaToolResultBlockParam[] {
        const toolResults: Anthropic.Beta.BetaToolResultBlockParam[] = [];
        for (const block of response.content) {
          if (block.type === "tool_use") {
            const input = block.input as Record<string, unknown>;
            const action = input.action as string;
            const result = handleComputerAction(action, input);
            toolResults.push({
              type: "tool_result",
              tool_use_id: block.id,
              content: result,
            });
          }
        }
        return toolResults;
      }
      ```

      ```csharp C#
      List<BetaContentBlockParam> ProcessToolCalls(BetaMessage response)
      {
          List<BetaContentBlockParam> toolResults = [];
          foreach (var block in response.Content)
          {
              if (block.TryPickToolUse(out var toolUse))
              {
                  var action = toolUse.Input["action"].GetString()!;
                  var result = HandleComputerAction(action, toolUse.Input);
                  toolResults.Add(new BetaToolResultBlockParam(toolUse.ID) { Content = result });
              }
          }
          return toolResults;
      }
      ```

      ```go Go
      func processToolCalls(response *anthropic.BetaMessage) []anthropic.BetaContentBlockParamUnion {
      	var toolResults []anthropic.BetaContentBlockParamUnion
      	for _, block := range response.Content {
      		switch variant := block.AsAny().(type) {
      		case anthropic.BetaToolUseBlock:
      			input := variant.Input.(map[string]any)
      			action := input["action"].(string)
      			result := handleComputerAction(action, input)
      			toolResults = append(toolResults, anthropic.NewBetaToolResultBlock(variant.ID, result, false))
      		}
      	}
      	return toolResults
      }

      ```

      ```java Java
      List<BetaContentBlockParam> processToolCalls(BetaMessage response) {
          List<BetaContentBlockParam> toolResults = new ArrayList<>();
          for (BetaContentBlock block : response.content()) {
              if (block.isToolUse()) {
                  BetaToolUseBlock toolUse = block.asToolUse();
                  Map<String, JsonValue> input =
                          (Map<String, JsonValue>) toolUse._input().asObject().get();
                  String action = input.get("action").asStringOrThrow();
                  String result = handleComputerAction(action, input);
                  toolResults.add(BetaContentBlockParam.ofToolResult(
                          BetaToolResultBlockParam.builder()
                                  .toolUseId(toolUse.id())
                                  .content(result)
                                  .build()));
              }
          }
          return toolResults;
      }
      ```

      ```php PHP
      function processToolCalls(BetaMessage $response): array
      {
          $toolResults = [];
          foreach ($response->content as $block) {
              if ($block instanceof BetaToolUseBlock) {
                  $action = $block->input['action'];
                  $result = handleComputerAction($action, $block->input);
                  $toolResults[] = BetaToolResultBlockParam::with(
                      toolUseID: $block->id,
                      content: $result,
                  );
              }
          }
          return $toolResults;
      }
      ```

      ```ruby Ruby
      def process_tool_calls(response)
        tool_results = []
        response.content.each do |block|
          next unless block.type == :tool_use

          action = block.input[:action]
          result = handle_computer_action(action, block.input)
          tool_results << {
            type: "tool_result",
            tool_use_id: block.id,
            content: result
          }
        end
        tool_results
      end
      ```
    </CodeGroup>
  </Step>

  <Step title="Implementasikan agent loop">
    Buat loop yang berlanjut hingga Claude menyelesaikan tugas:

    <CodeGroup>
      ```bash cURL
      # Loop agen adalah pola stateful multi-giliran yang tidak dapat diubah menjadi
      # perintah shell sekali jalan. Lihat tab SDK untuk implementasinya.
      ```

      ```bash CLI
      # Loop agen adalah pola stateful multi-giliran yang tidak dapat diubah menjadi
      # perintah shell sekali jalan. Lihat tab SDK untuk implementasinya.
      ```

      ```python Python
      def sampling_loop(model, messages, max_iterations=10):
          """
          Run the computer-use agent loop until Claude stops requesting tools
          or the iteration limit is reached.
          """
          for _ in range(max_iterations):
              response = client.beta.messages.create(
                  model=model,
                  max_tokens=4096,
                  messages=messages,
                  tools=TOOLS,
                  betas=["computer-use-2025-11-24"],
              )

              # Tambahkan respons Claude ke riwayat percakapan
              messages.append({"role": "assistant", "content": response.content})

              # Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
              tool_results = process_tool_calls(response)
              if not tool_results:
                  return messages  # No more tool use; task complete

              # Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
              messages.append({"role": "user", "content": tool_results})

          return messages
      ```

      ```typescript TypeScript
      async function samplingLoop(
        model: string,
        messages: Anthropic.Beta.BetaMessageParam[],
        maxIterations = 10,
      ): Promise<Anthropic.Beta.BetaMessageParam[]> {
        // Jalankan loop agen computer-use hingga Claude berhenti meminta alat
        // atau batas iterasi tercapai.
        for (let i = 0; i < maxIterations; i++) {
          const response = await client.beta.messages.create({
            model,
            max_tokens: 4096,
            messages,
            tools,
            betas: ["computer-use-2025-11-24"],
          });

          // Tambahkan respons Claude ke riwayat percakapan
          messages.push({ role: "assistant", content: response.content });

          // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
          const toolResults = processToolCalls(response);
          if (toolResults.length === 0) {
            return messages; // No more tool use; task complete
          }

          // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
          messages.push({ role: "user", content: toolResults });
        }

        return messages;
      }
      ```

      ```csharp C#
      async Task<List<BetaMessageParam>> SamplingLoop(
          Model model,
          List<BetaMessageParam> messages,
          int maxIterations = 10
      )
      {
          // Jalankan loop agen computer-use hingga Claude berhenti meminta alat
          // atau batas iterasi tercapai.
          for (var i = 0; i < maxIterations; i++)
          {
              var response = await client.Beta.Messages.Create(
                  new MessageCreateParams
                  {
                      Model = model,
                      MaxTokens = 4096,
                      Messages = messages,
                      Tools = tools,
                      Betas = ["computer-use-2025-11-24"],
                  }
              );

              // Tambahkan respons Claude ke riwayat percakapan
              messages.Add(
                  new()
                  {
                      Role = Role.Assistant,
                      Content = response
                          .Content.Select(block => new BetaContentBlockParam(block.Json))
                          .ToList(),
                  }
              );

              // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
              var toolResults = ProcessToolCalls(response);
              if (toolResults.Count == 0)
              {
                  return messages; // No more tool use; task complete
              }

              // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
              messages.Add(new() { Role = Role.User, Content = toolResults });
          }

          return messages;
      }
      ```

      ```go Go
      // samplingLoop menjalankan loop agen computer-use hingga Claude berhenti
      // meminta alat atau batas iterasi tercapai.
      func samplingLoop(ctx context.Context, model anthropic.Model, messages []anthropic.BetaMessageParam, maxIterations int) ([]anthropic.BetaMessageParam, error) {
      	for range maxIterations {
      		response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
      			Model:     model,
      			MaxTokens: 4096,
      			Messages:  messages,
      			Tools:     tools,
      			Betas:     []anthropic.AnthropicBeta{"computer-use-2025-11-24"},
      		})
      		if err != nil {
      			return nil, err
      		}

      		// Tambahkan respons Claude ke riwayat percakapan
      		messages = append(messages, response.ToParam())

      		// Jalankan alat yang diminta Claude dan kumpulkan hasilnya
      		toolResults := processToolCalls(response)
      		if len(toolResults) == 0 {
      			return messages, nil // No more tool use; task complete
      		}

      		// Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
      		messages = append(messages, anthropic.BetaMessageParam{
      			Role:    anthropic.BetaMessageParamRoleUser,
      			Content: toolResults,
      		})
      	}
      	return messages, nil
      }

      ```

      ```java Java
      /**
       * Run the computer-use agent loop until Claude stops requesting tools
       * or the iteration limit is reached.
       */
      List<BetaMessageParam> samplingLoop(Model model, List<BetaMessageParam> messages, int maxIterations) {
          for (int i = 0; i < maxIterations; i++) {
              BetaMessage response = client.beta().messages().create(MessageCreateParams.builder()
                      .model(model)
                      .maxTokens(4096)
                      .messages(messages)
                      .addTool(COMPUTER_TOOL)
                      .addBeta("computer-use-2025-11-24")
                      .build());

              // Tambahkan respons Claude ke riwayat percakapan
              messages.add(BetaMessageParam.builder()
                      .role(BetaMessageParam.Role.ASSISTANT)
                      .contentOfBetaContentBlockParams(
                              response.content().stream().map(BetaContentBlock::toParam).toList())
                      .build());

              // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
              List<BetaContentBlockParam> toolResults = processToolCalls(response);
              if (toolResults.isEmpty()) {
                  return messages; // No more tool use; task complete
              }

              // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
              messages.add(BetaMessageParam.builder()
                      .role(BetaMessageParam.Role.USER)
                      .contentOfBetaContentBlockParams(toolResults)
                      .build());
          }
          return messages;
      }
      ```

      ```php PHP
      /**
       * Run the computer-use agent loop until Claude stops requesting tools
       * or the iteration limit is reached.
       */
      function samplingLoop(string $model, array $messages, int $maxIterations = 10): array
      {
          global $client, $tools;

          for ($i = 0; $i < $maxIterations; $i++) {
              $response = $client->beta->messages->create(
                  model: $model,
                  maxTokens: 4096,
                  messages: $messages,
                  tools: $tools,
                  betas: ['computer-use-2025-11-24'],
              );

              // Tambahkan respons Claude ke riwayat percakapan
              $messages[] = BetaMessageParam::with(role: Role::ASSISTANT, content: $response->content);

              // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
              $toolResults = processToolCalls($response);
              if ($toolResults === []) {
                  return $messages; // No more tool use; task complete
              }

              // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
              $messages[] = BetaMessageParam::with(role: Role::USER, content: $toolResults);
          }

          return $messages;
      }
      ```

      ```ruby Ruby
      # Jalankan loop agen computer-use hingga Claude berhenti meminta alat
      # atau batas iterasi tercapai.
      def sampling_loop(model, messages, max_iterations: 10)
        max_iterations.times do
          response = CLIENT.beta.messages.create(
            model: model,
            max_tokens: 4096,
            messages: messages,
            tools: TOOLS,
            betas: ["computer-use-2025-11-24"]
          )

          # Tambahkan respons Claude ke riwayat percakapan
          messages << {role: "assistant", content: response.content}

          # Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
          tool_results = process_tool_calls(response)
          return messages if tool_results.empty? # No more tool use; task complete

          # Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
          messages << {role: "user", content: tool_results}
        end

        messages
      end
      ```
    </CodeGroup>
  </Step>
</Steps>

#### Tangani kesalahan

Saat mengimplementasikan alat computer use, berbagai kesalahan mungkin terjadi. Berikut cara menanganinya:

<AccordionGroup>
  <Accordion title="Kegagalan pengambilan tangkapan layar">
    Jika pengambilan tangkapan layar gagal, kembalikan pesan kesalahan yang sesuai:

    ```json
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
          "content": "Error: Failed to capture screenshot. Display may be locked or unavailable.",
          "is_error": true
        }
      ]
    }
    ```
  </Accordion>

  <Accordion title="Koordinat tidak valid">
    Jika Claude memberikan koordinat di luar batas tampilan:

    ```json
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
          "content": "Error: Coordinates (1200, 900) are outside display bounds (1024x768).",
          "is_error": true
        }
      ]
    }
    ```
  </Accordion>

  <Accordion title="Kegagalan eksekusi tindakan">
    Jika suatu tindakan gagal dijalankan:

    ```json
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
          "content": "Error: Failed to perform click action. The application may be unresponsive.",
          "is_error": true
        }
      ]
    }
    ```
  </Accordion>
</AccordionGroup>

#### Sesuaikan ukuran tangkapan layar agar sesuai dengan batas gambar

Tangkapan layar yang dikirim ke alat computer harus sesuai dengan batas ukuran gambar Claude (lihat [batas ukuran gambar](/docs/id/build-with-claude/vision#evaluate-image-size)). API memperkecil gambar yang terlalu besar sebelum Claude melihatnya, dan Claude mengembalikan koordinat untuk gambar yang dilihatnya, sehingga mengandalkan pengecilan di sisi server membuat Anda tidak memiliki faktor skala yang Anda perlukan untuk memetakan koordinat tersebut kembali ke layar Anda. Hanya gambar yang melebihi [batas permintaan](/docs/id/build-with-claude/vision#request-limits) API yang terpisah (misalnya, lebih dari 8.000 px pada satu sisi) yang ditolak dengan kesalahan validasi alih-alih diperkecil.

<Note>
  Batas bervariasi menurut model. Claude Sonnet 5, Claude Opus 4.8, dan Claude Opus 4.7 menerima hingga 2576 piksel pada sisi terpanjang; model sebelumnya menerima hingga 1568 piksel pada sisi terpanjang dan sekitar 1,15 megapiksel total. Contoh berikut menggunakan batas model sebelumnya 1568 px / 1,15 MP; gantikan dengan batas model Anda.
</Note>

Jika layar Anda lebih besar dari batas, ubah ukuran tangkapan layar sebelum mengirimkannya, atur `display_width_px`/`display_height_px` ke dimensi yang telah diubah ukurannya, dan skalakan koordinat yang dikembalikan Claude kembali ke ruang layar asli:

<CodeGroup>
  ```bash cURL
  # Penskalaan koordinat dan pengubahan ukuran screenshot terjadi di kode aplikasi Anda, bukan
  # di permintaan API. Lihat tab SDK untuk pola helper.
  ```

  ```bash CLI
  # Penskalaan koordinat dan pengubahan ukuran screenshot terjadi di kode aplikasi Anda,
  # bukan di permintaan API. Lihat tab SDK untuk pola helper-nya.
  ```

  ```python Python
  import math


  def get_scale_factor(width, height):
      """Calculate scale factor to meet API constraints."""
      long_edge = max(width, height)
      total_pixels = width * height

      long_edge_scale = 1568 / long_edge
      total_pixels_scale = math.sqrt(1_150_000 / total_pixels)

      return min(1.0, long_edge_scale, total_pixels_scale)


  # Saat mengambil tangkapan layar
  scale = get_scale_factor(screen_width, screen_height)
  scaled_width = int(screen_width * scale)
  scaled_height = int(screen_height * scale)

  # Ubah ukuran gambar ke dimensi yang diskalakan sebelum dikirim ke Claude
  screenshot = capture_and_resize(scaled_width, scaled_height)


  # Saat menangani koordinat dari Claude, skalakan kembali ke ukuran semula
  def execute_click(x, y):
      screen_x = x / scale
      screen_y = y / scale
      perform_click(screen_x, screen_y)
  ```

  ```typescript TypeScript
  const MAX_LONG_EDGE = 1568;
  const MAX_PIXELS = 1_150_000;

  function getScaleFactor(width: number, height: number): number {
    const longEdge = Math.max(width, height);
    const totalPixels = width * height;

    const longEdgeScale = MAX_LONG_EDGE / longEdge;
    const totalPixelsScale = Math.sqrt(MAX_PIXELS / totalPixels);

    return Math.min(1.0, longEdgeScale, totalPixelsScale);
  }

  // Saat mengambil tangkapan layar
  const scale = getScaleFactor(screenWidth, screenHeight);
  const scaledWidth = Math.floor(screenWidth * scale);
  const scaledHeight = Math.floor(screenHeight * scale);

  // Ubah ukuran gambar ke dimensi yang diskalakan sebelum dikirim ke Claude
  const screenshot = captureAndResize(scaledWidth, scaledHeight);

  // Saat menangani koordinat dari Claude, skalakan kembali ke ukuran semula
  function executeClick(x: number, y: number): void {
    const screenX = x / scale;
    const screenY = y / scale;
    performClick(screenX, screenY);
  }
  ```

  ```csharp C#
  double GetScaleFactor(int width, int height)
  {
      // Hitung faktor skala untuk memenuhi batasan API.
      int longEdge = Math.Max(width, height);
      int totalPixels = width * height;

      double longEdgeScale = 1568.0 / longEdge;
      double totalPixelsScale = Math.Sqrt(1_150_000.0 / totalPixels);

      return Math.Min(1.0, Math.Min(longEdgeScale, totalPixelsScale));
  }

  // Saat mengambil tangkapan layar
  double scale = GetScaleFactor(screenWidth, screenHeight);
  int scaledWidth = (int)(screenWidth * scale);
  int scaledHeight = (int)(screenHeight * scale);

  // Ubah ukuran gambar ke dimensi yang telah diskalakan sebelum dikirim ke Claude
  var screenshot = CaptureAndResize(scaledWidth, scaledHeight);

  // Saat menangani koordinat dari Claude, skalakan kembali ke ukuran semula
  void ExecuteClick(int x, int y)
  {
      double screenX = x / scale;
      double screenY = y / scale;
      PerformClick(screenX, screenY);
  }
  ```

  ```go Go
  func getScaleFactor(width, height int) float64 {
  	longest := float64(max(width, height))
  	area := float64(width * height)
  	return min(1.0, 1568/longest, math.Sqrt(1_150_000/area))
  }

  // ...
  	// Saat mengambil tangkapan layar
  	scale := getScaleFactor(screenWidth, screenHeight)
  	scaledWidth := int(float64(screenWidth) * scale)
  	scaledHeight := int(float64(screenHeight) * scale)

  	// Ubah ukuran gambar ke dimensi yang diskalakan sebelum dikirim ke Claude
  	screenshot := captureAndResize(scaledWidth, scaledHeight)

  	// Saat menangani koordinat dari Claude, skalakan kembali ke ukuran semula
  	executeClick := func(x, y int) {
  		performClick(float64(x)/scale, float64(y)/scale)
  	}
  ```

  ```java Java
  static double getScaleFactor(int width, int height) {
      return Math.min(
          1.0,
          Math.min(
              1568.0 / Math.max(width, height),
              Math.sqrt(1_150_000.0 / (width * height))
          )
      );
  }

  void main() {
  // ...
      // Saat mengambil tangkapan layar
      double scale = getScaleFactor(screenWidth, screenHeight);
      int scaledWidth = (int)(screenWidth * scale);
      int scaledHeight = (int)(screenHeight * scale);

      // Ubah ukuran gambar ke dimensi yang diskalakan sebelum dikirim ke Claude
      var screenshot = captureAndResize(scaledWidth, scaledHeight);

      // Saat menangani koordinat dari Claude, skalakan kembali ke ukuran semula
      BiConsumer<Integer, Integer> executeClick =
          (x, y) -> performClick(x / scale, y / scale);
  // ...
  }
  ```

  ```php PHP
  function getScaleFactor(int $width, int $height): float
  {
      return min(
          1.0,
          1568 / max($width, $height),
          sqrt(1_150_000 / ($width * $height)),
      );
  }
  // ...
  // Saat mengambil tangkapan layar
  $scale = getScaleFactor($screenWidth, $screenHeight);
  $scaledWidth = (int)($screenWidth * $scale);
  $scaledHeight = (int)($screenHeight * $scale);

  // Ubah ukuran gambar ke dimensi yang diskalakan sebelum dikirim ke Claude
  $screenshot = captureAndResize($scaledWidth, $scaledHeight);

  // Saat menangani koordinat dari Claude, skalakan kembali ke ukuran semula
  $executeClick = fn(int $x, int $y) => performClick($x / $scale, $y / $scale);
  ```

  ```ruby Ruby
  def get_scale_factor(width, height)
    [1.0, 1568.0 / [width, height].max, Math.sqrt(1_150_000.0 / (width * height))].min
  end
  # ...
  # Saat mengambil tangkapan layar
  scale = get_scale_factor(screen_width, screen_height)
  scaled_width = (screen_width * scale).to_i
  scaled_height = (screen_height * scale).to_i

  # Ubah ukuran gambar ke dimensi yang diskalakan sebelum dikirim ke Claude
  screenshot = capture_and_resize(scaled_width, scaled_height)

  # Saat menangani koordinat dari Claude, skalakan kembali ke ukuran semula
  execute_click = ->(x, y) { perform_click(x / scale, y / scale) }
  ```
</CodeGroup>

<Note>
  **Layar Retina macOS** menangkap tangkapan layar pada rasio piksel perangkat 2, sehingga gambar memiliki resolusi dua kali lipat dari koordinat layar logis. Perkecil tangkapan layar sebesar 2x sebelum mengirim, atau bagi dua koordinat yang dikembalikan Claude sebelum melakukan klik.
</Note>

#### Diagnosis masalah klik

Jika klik meleset dari targetnya, penyebabnya biasanya salah satu dari berikut:

| Gejala                                                      | Kemungkinan penyebab                                                                             | Coba                                                                                                                                           |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Klik secara konsisten bergeser ke satu arah                 | `display_width_px`/`display_height_px` tidak cocok dengan dimensi gambar yang sebenarnya dikirim | Pastikan dimensi tampilan sama persis dengan tangkapan layar yang Anda kirim                                                                   |
| Klik mendarat di area yang benar tetapi meleset dari target | Target sangat kecil, detail hilang saat memperkecil sumber 4K+, atau rasio aspek terdistorsi     | Atur `enable_zoom: true`; tangkap pada DPI yang lebih rendah atau potong ke wilayah yang relevan; pertahankan rasio aspek saat mengubah ukuran |
| Claude mengklik elemen yang sepenuhnya salah                | Instruksi ambigu, atau elemen yang mirip secara visual di dekatnya                               | Gunakan prompt posisional ("tombol Submit biru di kanan bawah"); pecah interaksi menjadi langkah-langkah yang lebih kecil                      |
| Akurasi secara konsisten buruk                              | Resolusi terlalu rendah                                                                          | Coba 1280x720 sebagai dasar                                                                                                                    |

<Tip>
  **Pilihan model memengaruhi presisi klik.** Claude Sonnet 4.6 lebih presisi secara mekanis dalam mengklik dibandingkan Claude Opus 4.6 dan lebih tangguh ketika tangkapan layar memerlukan pengecilan yang berat. Claude Opus 4.7 mempersempit kesenjangan itu: presisi kliknya kira-kira sebanding dengan Sonnet 4.6, dan batas resolusinya yang lebih tinggi berarti lebih sedikit pengecilan yang diperlukan.
</Tip>

#### Ikuti praktik terbaik implementasi

<AccordionGroup>
  <Accordion title="Gunakan resolusi tampilan yang sesuai">
    Atur dimensi tampilan yang sesuai dengan kasus penggunaan Anda sambil tetap dalam batas yang direkomendasikan:

    * Untuk tugas desktop umum: 1024x768 atau 1280x720
    * Untuk aplikasi web: 1280x800 atau 1366x768
    * Hindari resolusi di atas 1920x1080 untuk mencegah masalah kinerja
  </Accordion>

  <Accordion title="Implementasikan penanganan tangkapan layar yang tepat">
    Saat mengembalikan tangkapan layar ke Claude:

    * Enkode tangkapan layar sebagai base64 PNG atau JPEG
    * Pertimbangkan untuk mengompresi tangkapan layar besar untuk meningkatkan kinerja
    * Sertakan metadata yang relevan seperti timestamp atau status tampilan
    * Jika menggunakan resolusi yang lebih tinggi, pastikan koordinat diskalakan secara akurat

    Tangkapan layar dikembalikan sebagai blok konten gambar di dalam array konten `tool_result` (lihat [Tangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls)):

    ```json
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
          "content": [
            {
              "type": "image",
              "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": "iVBORw0KGgo..."
              }
            }
          ]
        }
      ]
    }
    ```
  </Accordion>

  <Accordion title="Kelola riwayat tangkapan layar untuk caching prompt">
    Agent loop yang panjang mengakumulasi tangkapan layar dengan cepat (kira-kira 1.000–1.800 token input masing-masing). Untuk menjaga [Caching prompt](/docs/id/build-with-claude/prompt-caching) tetap efektif sambil membatasi konteks:

    * Tempatkan satu breakpoint `cache_control` setelah prompt sistem dan definisi alat, dan hingga tiga lagi pada blok `tool_result` terbaru, memajukannya setiap giliran.
    * Pangkas tangkapan layar lama dalam *batch*, bukan satu setiap giliran. Menghapus satu tangkapan layar setiap giliran mengubah prefix setiap giliran dan membatalkan cache. Default yang wajar adalah menyimpan tiga tangkapan layar terakhir dan memangkas setiap 25 giliran, sehingga prefix tetap identik byte-per-byte di antara peristiwa pemangkasan.
  </Accordion>

  <Accordion title="Tambahkan jeda tindakan">
    Beberapa aplikasi memerlukan waktu untuk merespons tindakan:

    <CodeGroup>
      ```bash cURL
      # Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk
      # polanya.
      ```

      ```bash CLI
      # Ini adalah kode helper di sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk
      # polanya.
      ```

      ```python Python
      def click_and_wait(x, y, wait_time=0.5):
          click_at(x, y)
          time.sleep(wait_time)  # Allow UI to update
      ```

      ```typescript TypeScript
      async function clickAndWait(x: number, y: number, waitMs = 500): Promise<void> {
        clickAt(x, y);
        await setTimeout(waitMs); // Allow UI to update
      }
      ```

      ```csharp C#
      static void ClickAndWait(int x, int y, double waitSeconds = 0.5)
      {
          ClickAt(x, y);
          Thread.Sleep(TimeSpan.FromSeconds(waitSeconds));  // Allow UI to update
      }
      ```

      ```go Go
      func clickAndWaitFor(x, y int, wait time.Duration) {
      	clickAt(x, y)
      	time.Sleep(wait) // Allow UI to update
      }

      func clickAndWait(x, y int) {
      	clickAndWaitFor(x, y, 500*time.Millisecond)
      }
      ```

      ```java Java
      void clickAndWait(int x, int y) throws InterruptedException {
          clickAndWait(x, y, 500);
      }

      void clickAndWait(int x, int y, long waitTimeMillis) throws InterruptedException {
          clickAt(x, y);
          Thread.sleep(waitTimeMillis);  // Allow UI to update
      }
      ```

      ```php PHP
      function clickAndWait(int $x, int $y, float $waitSeconds = 0.5): void
      {
          clickAt($x, $y);
          usleep((int) ($waitSeconds * 1_000_000));  // Allow UI to update
      }
      ```

      ```ruby Ruby
      def click_and_wait(x, y, wait_time: 0.5)
        click_at(x, y)
        sleep(wait_time) # Allow UI to update
      end
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Validasi tindakan sebelum menjalankannya">
    Periksa bahwa tindakan yang diminta aman dan valid:

    <CodeGroup>
      ```bash cURL
      # Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk
      # polanya.
      ```

      ```bash CLI
      # Ini adalah kode helper di sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk
      # polanya.
      ```

      ```python Python
      def validate_action(action_type, params):
          if action_type == "left_click":
              x, y = params.get("coordinate", (0, 0))
              if not (0 <= x < display_width and 0 <= y < display_height):
                  return False, "Coordinates out of bounds"
          return True, None
      ```

      ```typescript TypeScript
      interface ActionParams {
        coordinate?: [number, number];
      }

      function validateAction(actionType: string, params: ActionParams): [boolean, string | null] {
        if (actionType === "left_click") {
          const [x, y] = params.coordinate ?? [0, 0];
          if (!(x >= 0 && x < displayWidth && y >= 0 && y < displayHeight)) {
            return [false, "Coordinates out of bounds"];
          }
        }
        return [true, null];
      }
      ```

      ```csharp C#
      const int DisplayWidth = 1024;
      const int DisplayHeight = 768;
      // ...
      static (bool IsValid, string? Error) ValidateAction(string actionType, IReadOnlyDictionary<string, JsonElement> parameters)
      {
          if (actionType == "left_click")
          {
              int x = parameters["coordinate"][0].GetInt32();
              int y = parameters["coordinate"][1].GetInt32();
              if (x is < 0 or >= DisplayWidth || y is < 0 or >= DisplayHeight)
              {
                  return (false, "Coordinates out of bounds");
              }
          }
          return (true, null);
      }
      ```

      ```go Go
      const (
      	displayWidth  = 1024
      	displayHeight = 768
      )

      func validateAction(actionType string, params map[string]any) (bool, string) {
      	if actionType == "left_click" {
      		coord, ok := params["coordinate"].([]any)
      		if !ok || len(coord) != 2 {
      			return false, "Invalid coordinate"
      		}
      		x, y := int(coord[0].(float64)), int(coord[1].(float64))
      		if !(0 <= x && x < displayWidth && 0 <= y && y < displayHeight) {
      			return false, "Coordinates out of bounds"
      		}
      	}
      	return true, ""
      }
      ```

      ```java Java
      static final int DISPLAY_WIDTH = 1024;
      static final int DISPLAY_HEIGHT = 768;

      record Validation(boolean valid, String error) {}

      Validation validateAction(String actionType, Map<String, JsonValue> params) {
          if (actionType.equals("left_click")) {
              List<JsonValue> coord = (List<JsonValue>) params.get("coordinate").asArray().get();
              long x = ((Number) coord.get(0).asNumber().get()).longValue();
              long y = ((Number) coord.get(1).asNumber().get()).longValue();
              if (!(0 <= x && x < DISPLAY_WIDTH && 0 <= y && y < DISPLAY_HEIGHT)) {
                  return new Validation(false, "Coordinates out of bounds");
              }
          }
          return new Validation(true, null);
      }
      ```

      ```php PHP
      const DISPLAY_WIDTH = 1024;
      const DISPLAY_HEIGHT = 768;

      /** @return array{bool, ?string} */
      function validateAction(string $actionType, array $params): array
      {
          if ($actionType === 'left_click') {
              [$x, $y] = $params['coordinate'] ?? [0, 0];
              if (!(0 <= $x && $x < DISPLAY_WIDTH && 0 <= $y && $y < DISPLAY_HEIGHT)) {
                  return [false, 'Coordinates out of bounds'];
              }
          }
          return [true, null];
      }
      ```

      ```ruby Ruby
      DISPLAY_WIDTH = 1024
      DISPLAY_HEIGHT = 768

      def validate_action(action_type, params)
        if action_type == "left_click"
          x, y = params.fetch(:coordinate, [0, 0])
          unless (0...DISPLAY_WIDTH).cover?(x) && (0...DISPLAY_HEIGHT).cover?(y)
            return [false, "Coordinates out of bounds"]
          end
        end
        [true, nil]
      end
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Catat tindakan untuk debugging">
    Simpan log semua tindakan untuk pemecahan masalah:

    <CodeGroup>
      ```bash cURL
      # Ini adalah kode helper di sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk
      # polanya.
      ```

      ```bash CLI
      # Ini adalah kode helper di sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk
      # polanya.
      ```

      ```python Python
      import logging


      def log_action(action_type, params, result):
          logging.info(f"Action: {action_type}, Params: {params}, Result: {result}")
      ```

      ```typescript TypeScript
      function logAction(actionType: string, params: unknown, result: unknown): void {
        console.error(
          `Action: ${actionType}, Params: ${JSON.stringify(params)}, Result: ${JSON.stringify(
            result
          )}`
        );
      }
      ```

      ```csharp C#
      static void LogAction(string actionType, object? parameters, object? result)
      {
          Console.Error.WriteLine($"Action: {actionType}, Params: {parameters}, Result: {result}");
      }
      ```

      ```go Go
      func logAction(actionType string, params map[string]any, result any) {
      	log.Printf("Action: %s, Params: %v, Result: %v", actionType, params, result)
      }
      ```

      ```java Java
      import static java.lang.System.Logger.Level.INFO;

      static final System.Logger LOGGER = System.getLogger("computer-use");

      void logAction(String actionType, Object params, Object result) {
          LOGGER.log(INFO, "Action: {0}, Params: {1}, Result: {2}", actionType, params, result);
      }
      ```

      ```php PHP
      function logAction(string $actionType, array $params, mixed $result): void
      {
          error_log(sprintf(
              'Action: %s, Params: %s, Result: %s',
              $actionType,
              json_encode($params),
              json_encode($result),
          ));
      }
      ```

      ```ruby Ruby
      require "logger"

      LOGGER = Logger.new($stderr)

      def log_action(action_type, params, result)
        LOGGER.info("Action: #{action_type}, Params: #{params}, Result: #{result}")
      end
      ```
    </CodeGroup>
  </Accordion>
</AccordionGroup>

***

## Pahami keterbatasan computer use

Computer use berada dalam tahap beta. Ingat keterbatasan berikut:

1. **Latency:** "Latency" (latensi) computer use saat ini untuk interaksi manusia-AI mungkin terlalu lambat dibandingkan dengan tindakan komputer yang diarahkan manusia secara biasa. Fokus pada kasus penggunaan di mana kecepatan tidak kritis (misalnya, pengumpulan informasi latar belakang, pengujian perangkat lunak otomatis) di lingkungan tepercaya.

2. **Akurasi dan keandalan computer vision:** Claude mungkin membuat kesalahan atau berhalusinasi saat mengeluarkan koordinat tertentu saat menghasilkan tindakan. Pemikiran diperpanjang dapat membantu Anda memahami penalaran model dan mengidentifikasi potensi masalah.

3. **Akurasi dan keandalan pemilihan alat:** Claude mungkin membuat kesalahan atau berhalusinasi saat memilih alat saat menghasilkan tindakan atau mengambil tindakan yang tidak terduga untuk menyelesaikan masalah. Selain itu, keandalan mungkin lebih rendah saat berinteraksi dengan aplikasi khusus atau beberapa aplikasi sekaligus. Beri prompt kepada model dengan hati-hati saat meminta tugas yang kompleks.

4. **Keandalan pengguliran:** Tindakan scroll mendukung kontrol arah (atas, bawah, kiri, kanan) dan jumlah yang ditentukan. Dalam aplikasi di mana pengguliran tidak berfungsi, alternatif keyboard seperti Page Down dapat membantu.

5. **Interaksi spreadsheet:** Gunakan tindakan kontrol mouse yang terperinci (`left_mouse_down`, `left_mouse_up`) dan kombinasi tombol modifier untuk memilih sel individual. Operasi spreadsheet yang kompleks mungkin masih memerlukan beberapa percobaan.

6. **Pembuatan akun dan pembuatan konten di platform sosial dan komunikasi:** Meskipun Claude akan mengunjungi situs web, kemampuan Claude untuk membuat akun atau menghasilkan dan membagikan konten atau terlibat dalam peniruan manusia di situs web dan platform media sosial terbatas. Kemampuan ini mungkin diperbarui di masa mendatang.

7. **Kerentanan:** Kerentanan seperti jailbreaking atau prompt injection mungkin tetap ada di seluruh sistem AI terdepan, termasuk API computer use beta. Dalam beberapa keadaan, Claude akan mengikuti perintah yang ditemukan dalam konten, terkadang bahkan ketika bertentangan dengan instruksi Anda. Misalnya, instruksi di halaman web atau yang terkandung dalam gambar mungkin menimpa instruksi Anda atau menyebabkan Claude membuat kesalahan. Pertimbangkan hal berikut:

   * Membatasi computer use ke lingkungan tepercaya seperti mesin virtual atau container dengan hak istimewa minimal
   * Menghindari memberikan computer use akses ke akun atau data sensitif tanpa pengawasan ketat
   * Menginformasikan pengguna akhir tentang risiko yang relevan dan mendapatkan persetujuan mereka sebelum mengaktifkan atau meminta izin yang diperlukan untuk fitur computer use di aplikasi Anda

8. **Tindakan yang tidak pantas atau ilegal:** Berdasarkan Ketentuan Layanan Anthropic, Anda tidak boleh menggunakan computer use untuk melanggar hukum apa pun atau Kebijakan Penggunaan yang Dapat Diterima.

Selalu tinjau dan verifikasi tindakan dan log computer use Claude dengan cermat. Jangan gunakan Claude untuk tugas yang memerlukan presisi sempurna atau informasi pengguna yang sensitif tanpa pengawasan manusia.

## Retensi data

Computer use adalah alat sisi klien. Semua tangkapan layar, tindakan mouse, input keyboard, dan file apa pun yang terlibat dalam sesi ditangkap dan disimpan di lingkungan Anda, bukan oleh Anthropic. Anthropic memproses gambar tangkapan layar dan permintaan tindakan secara real time sebagai bagian dari panggilan API. Retensi untuk permintaan API tersebut diatur oleh [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

Karena aplikasi Anda mengontrol di mana dan bagaimana data computer use disimpan, computer use memenuhi syarat ZDR. Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Harga

Computer use mengikuti [harga penggunaan alat](/docs/id/agents-and-tools/tool-use/overview#pricing) standar. Saat menggunakan alat computer use:

**Overhead prompt sistem:** Beta computer use menambahkan 466–499 token ke prompt sistem

**Penggunaan token alat computer use:**

| Model            | Token input per definisi alat |
| ---------------- | ----------------------------- |
| Model Claude 4.x | 735 token                     |

**Konsumsi token tambahan:**

* Gambar tangkapan layar (lihat [harga Vision](/docs/id/build-with-claude/vision))
* Hasil eksekusi alat yang dikembalikan ke Claude

<Note>
  Jika Anda juga menggunakan alat bash atau text editor bersama computer use, alat-alat tersebut memiliki biaya token sendiri sebagaimana didokumentasikan di halaman masing-masing.
</Note>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Pemecahan masalah penggunaan alat" icon="wrench" href="/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use">
    Perbaiki kesalahan penggunaan alat yang paling umum dengan tabel diagnostik gejala-ke-perbaikan.
  </Card>

  <Card title="Implementasi referensi" icon="github-logo" href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo">
    Mulai dengan implementasi lengkap berbasis Docker
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="tool" href="/docs/id/agents-and-tools/tool-use/overview">
    Hubungkan Claude ke alat dan API eksternal. Lihat di mana alat dieksekusi, kapan Claude memanggilnya, dan alat mana yang cocok untuk tugas Anda.
  </Card>

  <Card title="Praktik terbaik secara detail" icon="book" href="https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude">
    Rekomendasi yang telah di-benchmark untuk resolusi, upaya pemikiran, dan manajemen konteks
  </Card>
</CardGroup>
