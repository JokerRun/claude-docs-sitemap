---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: ee2999b2f4d949ee5d6b59111320b05993a52260bd0a462cc18cdb09ce38f88f
---

---
title: Alat computer use
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool
description: Berikan Claude kendali tangkapan layar, mouse, dan keyboard atas lingkungan desktop dengan alat computer use, yaitu toolset klien computer_toolset_20260801.
---

## Compatibility
- [ZDR](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention): eligible (excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements))
- Supported models: `claude-fable-5`, `claude-mythos-5`, `claude-opus-5`, `claude-sonnet-5`, `claude-opus-4-8`
- Platforms: Claude API, Claude Platform on AWS (beta), Amazon Bedrock (beta), Google Cloud (beta), Microsoft Foundry (beta)
- Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Opus 4.5 mendukung computer use hanya melalui versi alat `computer_20251124` yang lebih lama, yang memerlukan header beta; lihat [Versi alat yang lebih lama](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#earlier-tool-versions).
- Platform selain Claude API saat ini hanya menawarkan [versi alat beta yang lebih lama](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#earlier-tool-versions).

Claude dapat berinteraksi dengan lingkungan komputer melalui alat "computer use" (penggunaan komputer), yang menyediakan kemampuan tangkapan layar serta kendali mouse/keyboard untuk interaksi desktop secara otonom.

Alat computer use adalah "client toolset" (toolset klien) yang didefinisikan oleh Anthropic, lihat [toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets): satu entri `{"type": "computer_toolset_20260801"}` dalam `tools` memberi Claude 17 alat anggota seperti `screenshot`, `left_click`, `type`, dan `zoom`, dan aplikasi Anda menjalankan setiap panggilan di lingkungan yang Anda kendalikan. Alat ini saat ini belum tersedia di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/tools). Panggilan Claude berupa blok `tool_use` yang `name`-nya adalah nama anggota dan yang membawa `"toolset_name": "computer"`, sering kali beberapa per giliran (sebuah [aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions)).

Untuk tugas yang tetap berada di dalam halaman web, [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) lebih cocok: alat anggotanya membaca dan bertindak pada halaman itu sendiri, dan tidak memerlukan lingkungan desktop penuh.

<Note>
  Computer use tersedia di Claude API sebagai toolset `computer_toolset_20260801`, tanpa header beta; lihat [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#compatibility) untuk model yang didukung.

  Integrasi `computer_20251124` yang sudah ada tetap berfungsi, dan versi alat yang lebih lama tetap tersedia dalam beta untuk model dan platform yang tidak mendukung toolset ini. Lihat [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124) untuk meningkatkan versi, atau [Versi alat yang lebih lama](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#earlier-tool-versions) untuk header beta.
</Note>

## Pertimbangan keamanan

Computer use memiliki risiko unik yang berbeda dari fitur API standar. Risiko ini meningkat saat berinteraksi dengan internet.

<Warning>
  Untuk meminimalkan risiko, pertimbangkan untuk mengambil tindakan pencegahan seperti:

  1. Menggunakan mesin virtual atau container khusus dengan hak akses minimal untuk mencegah serangan sistem langsung atau kecelakaan.
  2. Menghindari pemberian akses kepada model ke data sensitif, seperti informasi login akun, untuk mencegah pencurian informasi.
  3. Membatasi akses internet ke daftar domain yang diizinkan (allowlist) untuk mengurangi paparan terhadap konten berbahaya.
  4. Meminta manusia untuk mengonfirmasi keputusan yang dapat mengakibatkan konsekuensi nyata yang berarti serta tugas apa pun yang memerlukan persetujuan afirmatif, seperti menerima cookie, menyelesaikan transaksi keuangan, atau menyetujui ketentuan layanan.
</Warning>

Dalam beberapa keadaan, Claude akan mengikuti perintah yang ditemukan dalam konten meskipun bertentangan dengan instruksi Anda. Misalnya, instruksi pada halaman web atau yang terkandung dalam gambar dapat mengesampingkan instruksi Anda atau menyebabkan Claude membuat kesalahan. Ambil tindakan pencegahan untuk mengisolasi Claude dari data dan tindakan sensitif guna menghindari risiko terkait prompt injection.

Anthropic telah melatih model untuk menahan prompt injection ini dan telah menambahkan lapisan pertahanan ekstra. Jika Anda menggunakan alat computer use, classifier akan otomatis berjalan pada prompt Anda untuk menandai potensi kejadian prompt injection. Ketika classifier ini mengidentifikasi potensi prompt injection dalam tangkapan layar, classifier akan otomatis mengarahkan model untuk meminta konfirmasi pengguna sebelum melanjutkan ke tindakan berikutnya. Perlindungan ekstra ini tidak akan ideal untuk setiap kasus penggunaan (misalnya, kasus penggunaan tanpa manusia dalam loop), jadi jika Anda ingin memilih keluar dan menonaktifkannya, [hubungi dukungan](https://support.claude.com/en/).

Tindakan pencegahan ini tetap penting bahkan dengan adanya lapisan pertahanan classifier.

Informasikan kepada pengguna akhir tentang risiko yang relevan dan dapatkan persetujuan mereka sebelum mengaktifkan computer use dalam produk Anda sendiri.

## Mulai cepat

Tambahkan toolset computer use ke array `tools` dari permintaan [Messages API](https://platform.claude.com/docs/id/api/messages/create) sebagai `{"type": "computer_toolset_20260801"}`. Permintaan ini tidak memerlukan header beta. Contoh ini juga mendeklarasikan [alat editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool) dan [alat bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool), yang biasanya digunakan Claude bersama computer use:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "tools": [
        {
          "type": "computer_toolset_20260801"
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
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  tools:
    - type: computer_toolset_20260801
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

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      tools=[
          {"type": "computer_toolset_20260801"},
          {"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"},
          {"type": "bash_20250124", "name": "bash"},
      ],
      messages=[{"role": "user", "content": "Save a picture of a cat to my desktop."}],
  )
  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    tools: [
      {
        type: "computer_toolset_20260801"
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
    messages: [{ role: "user", content: "Save a picture of a cat to my desktop." }]
  });

  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Tools =
      [
          new ComputerToolset20260801(),
          new ToolTextEditor20250728(),
          new ToolBash20250124(),
      ],
      Messages =
      [
          new MessageParam
          {
              Role = Role.User,
              Content = "Save a picture of a cat to my desktop.",
          },
      ],
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Tools: []anthropic.ToolUnionParam{
  		{OfComputerToolset20260801: &anthropic.ComputerToolset20260801Param{}},
  		{OfTextEditor20250728: &anthropic.ToolTextEditor20250728Param{}},
  		{OfBashTool20250124: &anthropic.ToolBash20250124Param{}},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Save a picture of a cat to my desktop.")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())
  ```

  ```java Java
  import com.anthropic.models.messages.ComputerToolset20260801;
  // ...
  import com.anthropic.models.messages.ToolBash20250124;
  import com.anthropic.models.messages.ToolTextEditor20250728;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .addTool(ComputerToolset20260801.builder().build())
          .addTool(ToolTextEditor20250728.builder().build())
          .addTool(ToolBash20250124.builder().build())
          .addUserMessage("Save a picture of a cat to my desktop.")
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Save a picture of a cat to my desktop.'],
      ],
      model: 'claude-opus-5',
      tools: [
          ['type' => 'computer_toolset_20260801'],
          [
              'type' => 'text_editor_20250728',
              'name' => 'str_replace_based_edit_tool',
          ],
          [
              'type' => 'bash_20250124',
              'name' => 'bash',
          ],
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    tools: [
      { type: "computer_toolset_20260801" },
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
    ]
  )

  puts response
  ```
</CodeGroup>

Ketika Claude bertindak pada desktop, respons memiliki `stop_reason` berupa `tool_use` dan berisi satu atau lebih blok `tool_use` anggota, masing-masing menyebutkan nama alat anggota dan membawa `"toolset_name": "computer"`. Di tengah tugas ini, setelah Claude melihat tangkapan layar desktop, respons mungkin terlihat seperti ini:

```json Output
{
  "id": "msg_01UZ3bXcQH8mTqNhVfL9eK2p",
  "type": "message",
  "role": "assistant",
  "model": "claude-opus-5",
  "content": [
    {
      "type": "text",
      "text": "I'll open the web browser to find a picture of a cat."
    },
    {
      "type": "tool_use",
      "id": "toolu_01WkoTUvSHDzTBu2xnGk8Ep8",
      "name": "left_click",
      "toolset_name": "computer",
      "input": { "coordinate": [512, 742] }
    },
    {
      "type": "tool_use",
      "id": "toolu_017nJn3RgSCkTMwuZDb4uUov",
      "name": "screenshot",
      "toolset_name": "computer",
      "input": {}
    }
  ],
  "stop_reason": "tool_use",
  "stop_sequence": null
}
```

Aplikasi Anda menjalankan setiap panggilan secara berurutan di lingkungan Anda sendiri, mengembalikan satu blok `tool_result` per blok `tool_use`, dan memanggil API lagi; [Cara kerja computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#how-computer-use-works) menjelaskan loop tersebut, dan bagian selanjutnya dari halaman ini menunjukkan cara mengimplementasikannya.

***

## Cara kerja computer use

<Steps>
  <Step title="Berikan Claude alat computer use dan prompt pengguna" icon="tool">
    * Tambahkan toolset computer use (dan opsional alat lainnya) ke array `tools` dari permintaan API Anda.
    * Sertakan prompt pengguna yang memerlukan interaksi desktop, misalnya, "Simpan gambar kucing ke desktop saya."
  </Step>

  <Step title="Claude merespons dengan panggilan alat anggota" icon="wrench">
    * Claude menilai apakah bertindak pada desktop dapat membantu menjawab pertanyaan pengguna.
    * Jika ya, Claude merespons dengan satu atau lebih blok `tool_use` anggota, seperti `screenshot`, `left_click`, atau `type`, masing-masing membawa `"toolset_name": "computer"`. Respons dengan beberapa blok ini adalah sebuah [aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions).
    * Respons API memiliki `stop_reason` berupa `tool_use`, yang menandakan permintaan penggunaan alat.
  </Step>

  <Step title="Jalankan panggilan secara berurutan dan kembalikan hasilnya" icon="computer">
    * Iterasi setiap blok `tool_use` dalam respons, secara berurutan. Untuk masing-masing, lakukan dispatch berdasarkan `name` anggota bersama dengan `toolset_name`, dan lakukan tindakan tersebut dengan `input` blok pada container atau mesin virtual Anda.
    * Lanjutkan percakapan dengan pesan `user` baru yang berisi satu blok `tool_result` per blok `tool_use`, dicocokkan berdasarkan `tool_use_id` dan masing-masing menyertakan `"toolset_name": "computer"`. Kembalikan gambar untuk `screenshot` dan `zoom`; teks singkat seperti `OK` sudah cukup untuk tindakan lainnya.
    * Jika suatu tindakan gagal, kembalikan `is_error: true` untuk blok tersebut dan jawab sisa batch seperti yang dijelaskan dalam [Aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions).
  </Step>

  <Step title="Claude melanjutkan hingga tugas selesai" icon="arrows-clockwise">
    * Claude menganalisis hasil alat untuk menentukan apakah diperlukan tindakan lebih lanjut atau tugas telah selesai.
    * Jika Claude menentukan bahwa diperlukan tindakan lebih lanjut, Claude merespons dengan `stop_reason` `tool_use` lainnya dan Anda harus kembali ke langkah 3.
    * Jika tidak, Claude mengembalikan respons teks kepada pengguna.
  </Step>
</Steps>

Pengulangan langkah 3 dan 4 tanpa input pengguna disebut sebagai "agent loop" (loop agen), yaitu Claude merespons dengan permintaan penggunaan alat dan aplikasi Anda merespons Claude dengan hasil evaluasi permintaan tersebut.

### Aksi batch

Claude dapat merencanakan urutan tindakan singkat, seperti klik, ketik, lalu mengambil tangkapan layar, dan mengembalikannya bersama-sama dalam satu respons. Ini disebut "batch action" (aksi batch); aksi ini menggunakan bentuk respons yang sama dengan [penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use) dengan satu perbedaan: Anda menjalankan blok-blok tersebut secara berurutan, bukan secara bersamaan.

Respons dengan batch tiga tindakan terlihat seperti ini:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "tool_use",
      "id": "toolu_01HqCF3nJ4Vzr8sTkPZ2wxYA",
      "name": "left_click",
      "toolset_name": "computer",
      "input": { "coordinate": [640, 60] }
    },
    {
      "type": "tool_use",
      "id": "toolu_01Ppr3sZ3TnE9m6VUu4RyH2K",
      "name": "type",
      "toolset_name": "computer",
      "input": { "text": "pictures of cats" }
    },
    {
      "type": "tool_use",
      "id": "toolu_01Xf5W1sD8Q9aBcJ7kLmN2pQ",
      "name": "screenshot",
      "toolset_name": "computer",
      "input": {}
    }
  ]
}
```

Kembalikan satu blok `tool_result` untuk setiap blok `tool_use`, dicocokkan berdasarkan `tool_use_id`, semuanya dalam pesan `user` berikutnya. Setiap hasil untuk alat anggota harus membawa `"toolset_name": "computer"`; hasil yang menghilangkannya, atau yang menyebutkan toolset berbeda dari blok `tool_use`-nya, akan ditolak. Hanya hasil `screenshot` dan `zoom` yang memerlukan gambar; untuk anggota lainnya, pengakuan teks singkat seperti `OK` sudah cukup (`cursor_position` mengembalikan koordinat sebagai teks):

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01HqCF3nJ4Vzr8sTkPZ2wxYA",
      "toolset_name": "computer",
      "content": [{ "type": "text", "text": "OK" }]
    },
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01Ppr3sZ3TnE9m6VUu4RyH2K",
      "toolset_name": "computer",
      "content": [{ "type": "text", "text": "OK" }]
    },
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01Xf5W1sD8Q9aBcJ7kLmN2pQ",
      "toolset_name": "computer",
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

**Jalankan blok secara berurutan dan berhenti pada kegagalan pertama.** Tindakan selanjutnya dalam batch biasanya bergantung pada tindakan sebelumnya: `type` dalam contoh ini memasukkan teks ke elemen apa pun yang difokuskan oleh klik sebelumnya. Jalankan blok secara berurutan sesuai urutan kemunculannya dalam `content`, dan jika salah satu gagal, jangan jalankan sisanya. Setiap blok `tool_use` tetap memerlukan `tool_result`, jadi jawab batch sebagai berikut:

* Untuk setiap tindakan yang berhasil, kembalikan hasil normalnya.
* Untuk tindakan yang gagal, kembalikan `is_error: true` dengan deskripsi teks tentang apa yang salah.
* Untuk setiap tindakan selanjutnya dalam batch, kembalikan `is_error: true` dengan teks persis berikut (alat browser use menggunakan [teks penghentian](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions) miliknya sendiri):

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01Xf5W1sD8Q9aBcJ7kLmN2pQ",
  "toolset_name": "computer",
  "is_error": true,
  "content": "Not executed: an earlier computer action in this turn failed."
}
```

Claude kemudian melihat tindakan mana yang berhasil, mana yang gagal, dan mana yang dilewati, lalu merencanakan ulang pada giliran berikutnya. Permintaan yang membiarkan blok `tool_use` apa pun dalam batch tidak terjawab akan ditolak dengan `invalid_request_error`, sehingga loop agen yang hanya membaca blok pertama akan gagal pada panggilan berikutnya. Jika aplikasi Anda meminta manusia untuk mengonfirmasi tindakan yang berdampak, lakukan pemeriksaan tersebut sebelum setiap blok dijalankan, karena sebuah batch dapat menyelesaikan tindakan multilangkah dalam satu giliran.

Claude biasanya mengakhiri batch dengan `screenshot` agar dapat mengamati hasilnya sebelum memutuskan apa yang harus dilakukan selanjutnya. Ketika batch tidak diakhiri dengan tangkapan layar, aplikasi Anda dapat melampirkan tangkapan layar sebagai blok `image` tambahan pada hasil terakhir dalam batch sehingga Claude selalu melihat keadaan layar saat ini, yang menghemat satu perjalanan bolak-balik dibandingkan menunggu Claude memintanya. Anda juga dapat memberi prompt kepada Claude untuk mengakhiri setiap batch dengan tangkapan layar (lihat [Optimalkan kinerja model dengan prompting](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#optimize-model-performance-with-prompting)).

### Lingkungan komputasi

Computer use memerlukan lingkungan komputasi sandbox tempat Claude dapat berinteraksi dengan aman dengan aplikasi dan web. Lingkungan ini mencakup:

1. **Tampilan virtual:** Server tampilan X11 virtual (menggunakan Xvfb) yang merender antarmuka desktop yang akan dilihat Claude melalui tangkapan layar dan dikendalikan dengan tindakan mouse/keyboard.

2. **Lingkungan desktop:** UI ringan dengan window manager (Mutter) dan panel (Tint2) yang berjalan di Linux, yang menyediakan antarmuka grafis yang konsisten untuk berinteraksi dengan Claude.

3. **Aplikasi:** Aplikasi Linux yang sudah terinstal seperti Firefox, LibreOffice, editor teks, dan pengelola file yang dapat digunakan Claude untuk menyelesaikan tugas.

4. **Implementasi alat:** Kode integrasi yang menerjemahkan permintaan alat abstrak Claude (seperti "gerakkan mouse" atau "ambil tangkapan layar") menjadi operasi nyata di lingkungan virtual.

5. **Loop agen:** Program yang menangani komunikasi antara Claude dan lingkungan, mengirimkan tindakan Claude ke lingkungan dan mengembalikan hasilnya (tangkapan layar, output perintah) kembali ke Claude.

Saat Anda menggunakan computer use, Claude tidak terhubung langsung ke lingkungan ini. Sebaliknya, aplikasi Anda:

1. Menerima permintaan penggunaan alat dari Claude
2. Menerjemahkannya menjadi tindakan di lingkungan komputasi Anda
3. Menangkap hasilnya (seperti tangkapan layar dan output perintah)
4. Mengembalikan hasil ini ke Claude

Untuk keamanan dan isolasi, implementasi referensi menjalankan semua ini di dalam container Docker dengan pemetaan port yang sesuai untuk melihat dan berinteraksi dengan lingkungan.

***

## Cara mengimplementasikan computer use

Meningkatkan versi integrasi `computer_20251124` yang sudah ada? Mulailah dengan [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124); sisa bagian ini berlaku untuk integrasi baru maupun yang dimigrasikan.

<Tip>
  [Implementasi referensi computer use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) adalah contoh kerja yang lengkap: sebuah [lingkungan dalam container](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/Dockerfile) yang cocok untuk computer use, implementasi [alat computer use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo/computer_use_demo/tools), sebuah [loop agen](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/computer_use_demo/loop.py) yang memanggil Claude API dan menjalankan alat, serta antarmuka web untuk container, loop, dan alat tersebut.
</Tip>

### Memahami loop agen

Inti dari computer use adalah "loop agen": siklus di mana Claude meminta tindakan alat, aplikasi Anda menjalankannya, dan mengembalikan hasilnya ke Claude. Loop ini menggunakan klien yang Anda buat di [Mulai cepat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#quick-start), array `tools` yang hanya mendeklarasikan toolset computer use, dan helper pemrosesan panggilan alat di bawah [Implementasikan alat computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#implement-the-computer-use-tool). Jika Anda juga mendeklarasikan alat lain, seperti alat bash dan editor teks dari Mulai cepat, lakukan dispatch blok `tool_use` mereka dalam proses yang sama; helper hanya menjawab panggilan anggota computer use, dan loop memperlakukan giliran tanpa panggilan yang terjawab sebagai selesai. Berikut contoh yang disederhanakan:

<CodeGroup exclude="shell">
  ```python Python
  def sampling_loop(model: str, messages: list[MessageParam], max_iterations: int = 10):
      """
      Run the computer-use agent loop until Claude stops requesting tools
      or the iteration limit is reached.
      """
      for _ in range(max_iterations):
          response = client.messages.create(
              model=model,
              max_tokens=4096,
              messages=messages,
              tools=TOOLS,
          )

          # Tambahkan respons Claude ke riwayat percakapan
          messages.append({"role": "assistant", "content": response.content})

          # Jalankan aksi yang diminta Claude, secara berurutan, dan kumpulkan hasilnya
          tool_results = process_tool_calls(response)
          if not tool_results:
              return messages  # No more tool use; task complete

          # Kirim semua hasil kembali ke Claude dalam satu pesan user
          messages.append({"role": "user", "content": tool_results})

      return messages
  ```

  ```typescript TypeScript
  async function samplingLoop(
    model: string,
    messages: Anthropic.MessageParam[],
    maxIterations = 10,
  ): Promise<Anthropic.MessageParam[]> {
    // Jalankan loop agen computer-use hingga Claude berhenti meminta alat
    // atau batas iterasi tercapai.
    for (let i = 0; i < maxIterations; i++) {
      const response = await client.messages.create({
        model,
        max_tokens: 4096,
        messages,
        tools,
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
  async Task<List<MessageParam>> SamplingLoop(
      Model model,
      List<MessageParam> messages,
      int maxIterations = 10
  )
  {
      // Jalankan loop agen computer-use hingga Claude berhenti meminta alat
      // atau batas iterasi tercapai.
      for (var i = 0; i < maxIterations; i++)
      {
          var response = await client.Messages.Create(
              new MessageCreateParams
              {
                  Model = model,
                  MaxTokens = 4096,
                  Messages = messages,
                  Tools = tools,
              }
          );

          // Tambahkan respons Claude ke riwayat percakapan
          messages.Add(
              new()
              {
                  Role = Role.Assistant,
                  Content = response
                      .Content.Select(block => new ContentBlockParam(block.Json))
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
  func samplingLoop(ctx context.Context, model anthropic.Model, messages []anthropic.MessageParam, maxIterations int) ([]anthropic.MessageParam, error) {
  	for range maxIterations {
  		response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  			Model:     model,
  			MaxTokens: 4096,
  			Messages:  messages,
  			Tools:     tools,
  		})
  		if err != nil {
  			return nil, err
  		}

  		// Tambahkan respons Claude ke riwayat percakapan
  		messages = append(messages, response.ToParam())

  		// Jalankan aksi yang diminta Claude secara berurutan, dan kumpulkan hasilnya
  		toolResults := processToolCalls(response)
  		if len(toolResults) == 0 {
  			return messages, nil // No more tool use; task complete
  		}

  		// Kirim semua hasil kembali ke Claude dalam satu pesan pengguna
  		messages = append(messages, anthropic.NewUserMessage(toolResults...))
  	}
  	return messages, nil
  }

  ```

  ```java Java
  /**
   * Run the computer-use agent loop until Claude stops requesting tools
   * or the iteration limit is reached.
   */
  List<MessageParam> samplingLoop(Model model, List<MessageParam> messages, int maxIterations) {
      for (int i = 0; i < maxIterations; i++) {
          Message response = client.messages().create(MessageCreateParams.builder()
                  .model(model)
                  .maxTokens(4096)
                  .messages(messages)
                  .addTool(COMPUTER_TOOLSET)
                  .build());

          // Tambahkan respons Claude ke riwayat percakapan
          messages.add(MessageParam.builder()
                  .role(MessageParam.Role.ASSISTANT)
                  .contentOfBlockParams(response.content().stream().map(ContentBlock::toParam).toList())
                  .build());

          // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
          List<ContentBlockParam> toolResults = processToolCalls(response);
          if (toolResults.isEmpty()) {
              return messages; // No more tool use; task complete
          }

          // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
          messages.add(MessageParam.builder()
                  .role(MessageParam.Role.USER)
                  .contentOfBlockParams(toolResults)
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
          $response = $client->messages->create(
              model: $model,
              maxTokens: 4096,
              messages: $messages,
              tools: $tools,
          );

          // Tambahkan respons Claude ke riwayat percakapan
          $messages[] = MessageParam::with(role: Role::ASSISTANT, content: $response->content);

          // Jalankan alat yang diminta Claude dan kumpulkan hasilnya
          $toolResults = processToolCalls($response);
          if ($toolResults === []) {
              return $messages; // No more tool use; task complete
          }

          // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
          $messages[] = MessageParam::with(role: Role::USER, content: $toolResults);
      }

      return $messages;
  }
  ```

  ```ruby Ruby
  # Jalankan loop agen computer-use hingga Claude berhenti meminta alat
  # atau batas iterasi tercapai.
  def sampling_loop(model, messages, max_iterations: 10)
    max_iterations.times do
      response = CLIENT.messages.create(
        model: model,
        max_tokens: 4096,
        messages: messages,
        tools: TOOLS
      )

      # Tambahkan respons Claude ke riwayat percakapan
      messages << { role: "assistant", content: response.content }

      # Jalankan aksi yang diminta Claude, secara berurutan, dan kumpulkan hasilnya
      tool_results = process_tool_calls(response)
      return messages if tool_results.empty? # No more tool use; task complete

      # Kirim semua hasil kembali ke Claude dalam satu pesan pengguna
      messages << { role: "user", content: tool_results }
    end

    messages
  end
  ```
</CodeGroup>

Loop berlanjut hingga Claude merespons tanpa meminta alat apa pun (tugas selesai) atau batas iterasi maksimum tercapai. Pengaman ini mencegah potensi loop tak terbatas yang dapat mengakibatkan biaya API yang tidak terduga.

### Optimalkan kinerja model dengan prompting

1. Tentukan tugas yang sederhana dan terdefinisi dengan baik serta berikan instruksi eksplisit untuk setiap langkah.
2. Claude terkadang mengasumsikan hasil dari tindakannya tanpa secara eksplisit memeriksa hasilnya. Untuk mencegah hal ini, Anda dapat memberi prompt kepada Claude dengan `After each step, take a screenshot and carefully evaluate if you have achieved the right outcome. Explicitly show your thinking: "I have evaluated step X..." If not correct, try again. Only when you confirm a step was executed correctly should you move on to the next one.`
3. Beberapa elemen UI (seperti dropdown dan scrollbar) mungkin sulit dimanipulasi oleh Claude menggunakan gerakan mouse. Jika Anda mengalami hal ini, coba beri prompt kepada model untuk menggunakan pintasan keyboard.
4. Untuk tugas atau interaksi UI yang berulang, sertakan contoh tangkapan layar dan panggilan alat dari hasil yang berhasil dalam prompt Anda.
5. Jika Anda memerlukan model untuk login, berikan nama pengguna dan kata sandi dalam prompt Anda di dalam tag XML seperti `<robot_credentials>`. Menggunakan computer use dalam aplikasi yang memerlukan login meningkatkan risiko hasil buruk akibat prompt injection. Tinjau [Mitigasi jailbreak dan prompt injection](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) sebelum memberikan kredensial login kepada model.
6. Saat menyusun array `content` pada giliran pengguna, tempatkan teks instruksi *sebelum* gambar tangkapan layar. Memberikan deskripsi target sebelum gambar diproses meningkatkan akurasi klik.
7. Claude menggunakan tindakan `zoom` untuk memeriksa suatu wilayah pada resolusi penuh ketika ditanya tentang teks kecil atau elemen UI tertentu yang tidak terbaca pada resolusi default tangkapan layar, seperti nama file di sidebar, judul tab, teks status bar, nomor baris, atau label tombol. Jika Claude tidak melakukan zoom saat Anda mengharapkannya, tanyakan tentang wilayah atau elemen tertentu, bukan layar secara keseluruhan.
8. Jika Anda ingin setiap [aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions) diakhiri dengan tangkapan layar, nyatakan hal itu dalam prompt sistem, misalnya, `End each group of actions with a screenshot so you can verify the result before continuing.`

<Tip>
  Jika Anda berulang kali menemui serangkaian masalah yang jelas atau mengetahui sebelumnya tugas yang perlu diselesaikan Claude, gunakan prompt sistem untuk memberi Claude tips atau instruksi eksplisit tentang cara menyelesaikan tugas dengan sukses.
</Tip>

<Tip>
  Untuk agen yang mencakup beberapa sesi, jalankan verifikasi end-to-end di awal setiap sesi, bukan hanya setelah implementasi. Pemeriksaan berbasis browser menangkap regresi dari sesi sebelumnya yang terlewat oleh tinjauan tingkat kode saja. Lihat [Harness efektif untuk agen yang berjalan lama](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) untuk detailnya.
</Tip>

### Prompt sistem

Saat Anda menyertakan alat computer use dalam permintaan, API menghasilkan prompt sistem khusus computer use. Prompt ini mirip dengan [prompt sistem penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools#tool-use-system-prompt) tetapi dimulai dengan:

> You have access to a set of functions you can use to answer the user's question. This includes access to a sandboxed computing environment. You do NOT currently have the ability to inspect files or interact with external resources, except by invoking the below functions.

Seperti pada penggunaan alat biasa, parameter `system` yang disediakan pengguna tetap dihormati dan digunakan dalam penyusunan prompt sistem gabungan.

### Tindakan yang tersedia

Setiap tindakan adalah alat anggota dari toolset computer use: Claude menyebutkan nama anggota dalam blok `tool_use` yang membawa `"toolset_name": "computer"`, dan `input` blok hanya berisi parameter anggota tersebut, tanpa field `action`. Toolset ini memiliki 17 alat anggota:

| Anggota                                                       | Input                                                                                                                                                                                                                       | Deskripsi                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `screenshot`                                                  | Tidak ada (`{}`)                                                                                                                                                                                                            | Menangkap seluruh tampilan dan mengembalikannya sebagai gambar.                                                                                                                                                                                                                                                             |
| `zoom`                                                        | `region`: `[x0, y0, x1, y1]`, sudut kiri atas dan kanan bawah dari area yang akan diperiksa                                                                                                                                 | Menangkap hanya wilayah tampilan tersebut pada resolusi penuh dan mengembalikannya sebagai gambar, diskalakan agar muat dalam dimensi tangkapan layar biasa Anda dengan rasio aspek dipertahankan. Ini memungkinkan Claude membaca teks kecil atau UI padat yang tidak terbaca dalam tangkapan layar penuh yang diperkecil. |
| `left_click`                                                  | `coordinate` (opsional): `[x, y]`; `text` (opsional): tombol modifier yang ditahan selama klik: `shift`, `ctrl`, `alt`, `super` (tombol Command atau Windows), atau kombinasi yang digabung dengan `+` seperti `ctrl+shift` | Mengklik tombol kiri mouse di `coordinate`, atau di posisi kursor saat ini jika `coordinate` dihilangkan.                                                                                                                                                                                                                   |
| `right_click`, `middle_click`, `double_click`, `triple_click` | Sama seperti `left_click`                                                                                                                                                                                                   | Tombol mouse lainnya dan klik ganda/berulang.                                                                                                                                                                                                                                                                               |
| `left_click_drag`                                             | `start_coordinate`: `[x, y]`; `coordinate`: `[x, y]`; `text` (opsional): tombol modifier                                                                                                                                    | Menekan di `start_coordinate`, menyeret ke `coordinate`, lalu melepas.                                                                                                                                                                                                                                                      |
| `mouse_move`                                                  | `coordinate`: `[x, y]`                                                                                                                                                                                                      | Memindahkan kursor tanpa mengklik, misalnya, untuk hover.                                                                                                                                                                                                                                                                   |
| `left_mouse_down`, `left_mouse_up`                            | Tidak ada (`{}`)                                                                                                                                                                                                            | Menekan atau melepas tombol kiri mouse di posisi kursor saat ini, untuk seretan yang tidak dapat diekspresikan oleh `left_click_drag`. Pindahkan kursor dengan `mouse_move` terlebih dahulu.                                                                                                                                |
| `cursor_position`                                             | Tidak ada (`{}`)                                                                                                                                                                                                            | Melaporkan posisi `[x, y]` kursor saat ini sebagai teks.                                                                                                                                                                                                                                                                    |
| `scroll`                                                      | `scroll_direction`: `"up"`, `"down"`, `"left"`, atau `"right"`; `scroll_amount`: jumlah klik roda gulir; `coordinate` (opsional): `[x, y]`; `text` (opsional): tombol modifier                                              | Menggulir di `coordinate`, atau di posisi kursor saat ini.                                                                                                                                                                                                                                                                  |
| `type`                                                        | `text`: string yang akan diketik                                                                                                                                                                                            | Mengetik teks literal pada fokus keyboard saat ini.                                                                                                                                                                                                                                                                         |
| `key`                                                         | `text`: sebuah tombol atau kombinasi yang digabung dengan `+` seperti `"Return"`, `"ctrl+s"`, atau `"alt+Tab"`; `repeat` (opsional): 1 hingga 100, default 1                                                                | Menekan tombol atau kombinasi tombol, sebanyak `repeat` kali.                                                                                                                                                                                                                                                               |
| `hold_key`                                                    | `text`: sebuah tombol atau kombinasi; `duration`: detik, hingga 300                                                                                                                                                         | Menahan tombol selama durasi yang diberikan.                                                                                                                                                                                                                                                                                |
| `wait`                                                        | `duration`: detik, hingga 300                                                                                                                                                                                               | Berhenti sejenak sebelum tindakan berikutnya, misalnya, saat aplikasi sedang dimuat.                                                                                                                                                                                                                                        |

Perhatikan hal-hal berikut saat mengimplementasikan anggota:

* **Koordinat dalam piksel tangkapan layar.** Setiap nilai `coordinate`, `start_coordinate`, dan `region`, serta posisi yang dilaporkan `cursor_position`, berada dalam ruang piksel tangkapan layar tampilan penuh yang Anda kembalikan, dengan titik asal di kiri atas. Gambar zoom tidak mengubah hal ini: setelah `zoom`, Claude tetap mengekspresikan koordinat dalam ruang tangkapan layar penuh, tidak pernah relatif terhadap gambar yang di-zoom. Jika Anda memperkecil tangkapan layar sebelum mengembalikannya, skalakan kembali koordinat Claude ke atas sebelum menerapkannya ke tampilan sebenarnya (lihat [Sesuaikan ukuran tangkapan layar agar sesuai batas gambar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions)).
* **Semua anggota diaktifkan secara default, termasuk `zoom`.** Jika lingkungan Anda tidak dapat menghasilkan gambar zoom, tahan anggota tersebut dengan `configs` (lihat [Parameter alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#tool-parameters)) daripada membiarkannya aktif dan mengembalikan error. Jika Claude memanggil anggota yang Anda tahan atau tidak Anda implementasikan, kembalikan `tool_result` dengan `is_error: true` untuk blok tersebut.
* **Lakukan dispatch berdasarkan pasangan (`toolset_name`, `name`).** `toolset_name` adalah yang menandai sebuah blok sebagai tindakan komputer: alat kustom dalam permintaan yang sama dapat memiliki nama yang sama dengan anggota, dan versi toolset yang lebih baru dapat menambahkan anggota (lihat [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets)).

<Accordion title="Contoh tindakan">
  Setiap contoh adalah blok `tool_use` lengkap seperti yang muncul dalam respons Claude.

  Shift+klik pada suatu posisi, misalnya, untuk memperluas seleksi. Tidak seperti `hold_key`, `text` menahan modifier hanya selama durasi klik atau gulir tersebut:

  ```json
  {
    "type": "tool_use",
    "id": "toolu_01Qg8m3XqC5aRy7tD2eS4jUg",
    "name": "left_click",
    "toolset_name": "computer",
    "input": { "coordinate": [500, 300], "text": "shift" }
  }
  ```

  Seret dari satu titik ke titik lain:

  ```json
  {
    "type": "tool_use",
    "id": "toolu_01Ed6j9VnA3yPw5rB8cQ2gSe",
    "name": "left_click_drag",
    "toolset_name": "computer",
    "input": {
      "start_coordinate": [200, 300],
      "coordinate": [600, 300]
    }
  }
  ```

  Gulir ke bawah tiga klik roda:

  ```json
  {
    "type": "tool_use",
    "id": "toolu_01Yc5h8UmZ2xNv4qA7bP9fRd",
    "name": "scroll",
    "toolset_name": "computer",
    "input": {
      "coordinate": [500, 400],
      "scroll_direction": "down",
      "scroll_amount": 3
    }
  }
  ```

  Tekan Tab empat kali:

  ```json
  {
    "type": "tool_use",
    "id": "toolu_01Sb4g7TkY9wLu3pX6zM8eQc",
    "name": "key",
    "toolset_name": "computer",
    "input": { "text": "Tab", "repeat": 4 }
  }
  ```

  Zoom untuk memeriksa suatu wilayah pada resolusi penuh:

  ```json
  {
    "type": "tool_use",
    "id": "toolu_01Kf7k2WpB4zQx6sC9dR3hTf",
    "name": "zoom",
    "toolset_name": "computer",
    "input": { "region": [100, 200, 400, 350] }
  }
  ```

  Laporkan posisi kursor. Jawab panggilan ini dengan hasil teks singkat yang memberikan posisi dalam piksel tangkapan layar, misalnya, `X=512, Y=384`:

  ```json
  {
    "type": "tool_use",
    "id": "toolu_01Ekh3vqB6yTs2mNc4Rw8pLd",
    "name": "cursor_position",
    "toolset_name": "computer",
    "input": {}
  }
  ```
</Accordion>

### Parameter alat

Entri toolset dalam array `tools` menerima empat parameter; aturan yang dibagikannya dengan toolset browser use tercantum di bawah [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets).

| Parameter         | Wajib | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`            | Ya    | `computer_toolset_20260801`                                                                                                                                                                                                                                                                                                                                                                                                     |
| `configs`         | Tidak | Pengaturan per anggota dengan kunci nama anggota; setiap anggota menerima `enabled` (default `true` untuk semua 17, termasuk `zoom`) dan `defer_loading` (default `false`, untuk [pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#deferred-tool-loading)), dan anggota yang Anda hilangkan mempertahankan default-nya.                                                           |
| `cache_control`   | Tidak | Breakpoint [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada definisi toolset; hanya pada entri. Breakpoint pada blok `tool_use` atau `tool_result` apa pun dalam batch berlaku di akhir batch tersebut; lihat [Penggunaan alat dengan caching prompt](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching#cache-control-on-tool-definitions). |
| `allowed_callers` | Tidak | Hanya `["direct"]`.                                                                                                                                                                                                                                                                                                                                                                                                             |

Misalnya, entri ini menahan `zoom` untuk lingkungan yang tidak mengimplementasikannya dan menetapkan breakpoint cache pada definisi toolset:

```json
{
  "type": "computer_toolset_20260801",
  "configs": {
    "zoom": { "enabled": false }
  },
  "cache_control": { "type": "ephemeral" }
}
```

Jika loop agen Anda hanya dapat menjalankan satu tindakan per perjalanan bolak-balik, atur `disable_parallel_tool_use` ke `true` dalam `tool_choice`; Claude kemudian mengembalikan paling banyak satu blok `tool_use` anggota per giliran (lihat [Nonaktifkan penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use#disable-parallel-tool-use)).

Entri ini menolak parameter berikut dari versi alat yang lebih lama, dan permintaan yang menyertakan salah satunya mengembalikan `invalid_request_error`:

* `name`: nama anggota ditetapkan oleh versi toolset.
* `display_width_px`, `display_height_px`, dan `display_number`: koordinat selalu berada dalam ruang piksel tangkapan layar yang Anda kembalikan.
* `enable_zoom`: zoom adalah alat anggota yang Anda kendalikan melalui `configs`.

Entri ini juga tidak dapat dideklarasikan dalam permintaan yang sama dengan entri `computer_20251124` atau alat lain bernama `computer`. Untuk `strict`, `input_examples`, penempatan `defer_loading`, `tool_choice`, streaming, dan pembatasan pemanggil, lihat [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets).

### Menggabungkan dengan thinking

Untuk menggabungkan computer use dengan "thinking" (pemikiran), lihat [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking).

<Tip>
  Untuk alat `computer_20251124` yang lebih lama, benchmark internal pada model yang menggunakannya menyarankan pengaturan `effort` berikut:

  * **Claude Opus 4.7:** gunakan `high` sebagai default; gunakan `low` untuk beban kerja throughput tinggi atau yang sensitif terhadap biaya.
  * **Claude Sonnet 4.6 dan Claude Opus 4.6:** gunakan `medium` sebagai default (rasio akurasi terhadap biaya terbaik). Hindari `max`, yang menambah biaya token tanpa meningkatkan akurasi pada tugas UI. Pada model-model ini, `low` menggunakan token output *lebih sedikit* daripada menonaktifkan thinking sepenuhnya (lebih sedikit kesalahan berarti lebih sedikit percobaan ulang), menjadikannya pilihan yang kuat untuk loop yang sensitif terhadap biaya.
</Tip>

### Memperkaya computer use dengan alat lain

Untuk menambahkan alat lain bersama computer use, sertakan alat tersebut dalam array `tools` yang sama. Bagian [Mulai cepat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#quick-start) menunjukkan pola ini dengan [alat bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool) dan [alat editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool). Anda dapat menambahkan [definisi alat kustom](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools) Anda sendiri dengan cara yang sama.

Untuk tugas yang tetap berada di dalam halaman web, Anda juga dapat [mendeklarasikan alat browser use dalam permintaan yang sama](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#combine-with-other-tools): kedua toolset bekerja secara independen, masing-masing dalam kerangka koordinatnya sendiri, dan panggilan ke anggota yang memiliki nama sama, seperti `screenshot` atau `key`, dibedakan berdasarkan `toolset_name`.

### Bangun lingkungan computer use kustom

[Implementasi referensi](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) dimaksudkan untuk membantu Anda memulai dengan computer use. Implementasi ini mencakup semua komponen yang diperlukan agar Claude dapat menggunakan komputer. Namun, Anda dapat membangun lingkungan Anda sendiri untuk computer use sesuai kebutuhan Anda. Anda akan memerlukan:

* Lingkungan tervirtualisasi atau dalam container yang cocok untuk computer use dengan Claude
* Implementasi tindakan-tindakan alat computer use
* Loop agen yang berinteraksi dengan Claude API dan menjalankan hasil `tool_use` menggunakan implementasi alat Anda
* API atau UI yang memungkinkan input pengguna untuk memulai loop agen

### Implementasikan alat computer use

Alat computer use diimplementasikan sebagai alat tanpa skema. Saat menggunakan alat ini, Anda tidak perlu menyediakan skema input seperti pada alat lain; skema sudah tertanam dalam model Claude dan tidak dapat dimodifikasi.

<Steps>
  <Step title="Siapkan lingkungan komputasi Anda">
    Buat tampilan virtual atau hubungkan ke tampilan yang sudah ada yang akan berinteraksi dengan Claude. Ini biasanya melibatkan penyiapan Xvfb (X Virtual Framebuffer) atau teknologi serupa.
  </Step>

  <Step title="Implementasikan handler tindakan">
    Buat fungsi untuk menangani setiap jenis tindakan yang mungkin diminta Claude:

    <CodeGroup exclude="shell">
      ```python Python
      # Data gambar placeholder; executor sungguhan menangkap layar dan mengembalikan byte PNG
      PLACEHOLDER_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="


      def capture_screenshot() -> list[ImageBlockParam]:
          # screenshot menjawab dengan blok gambar, bukan teks: kembalikan daftar konten hasil
          return [
              {
                  "type": "image",
                  "source": {"type": "base64", "media_type": "image/png", "data": PLACEHOLDER_PNG},
              }
          ]


      def click(coordinate=None):
          if coordinate is None:
              return "clicked at current cursor"
          x, y = coordinate
          return f"clicked at ({x}, {y})"


      def type_text(text):
          return f"typed: {text}"


      def handle_computer_action(name, tool_input):
          if name == "screenshot":
              return capture_screenshot()
          elif name == "left_click":
              # coordinate bersifat opsional; tanpanya, klik di posisi kursor saat ini
              return click(tool_input.get("coordinate"))
          elif name == "type":
              return type_text(tool_input["text"])
          # Tangani aksi lain sesuai kebutuhan
          raise ValueError(f"Unknown or unimplemented member: {name}")
      ```

      ```typescript TypeScript
      // Data gambar placeholder; eksekutor nyata menangkap layar sebagai byte PNG
      const PLACEHOLDER_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==";

      function captureScreenshot(): Anthropic.ImageBlockParam[] {
        // screenshot menjawab dengan blok gambar, bukan teks
        return [
          {
            type: "image",
            source: {
              type: "base64",
              media_type: "image/png",
              data: PLACEHOLDER_PNG,
            },
          },
        ];
      }

      function clickAt(x: number, y: number): string {
        return `clicked at (${x}, ${y})`;
      }

      function clickAtCursor(): string {
        return "clicked at the current cursor position";
      }

      function typeText(text: string): string {
        return `typed: ${text}`;
      }

      function handleComputerAction(
        action: string,
        input: unknown,
      ): string | Anthropic.ImageBlockParam[] {
        const params: object =
          typeof input === "object" && input !== null ? input : {};
        if (action === "screenshot") {
          return captureScreenshot();
        } else if (action === "left_click") {
          // coordinate bersifat opsional pada toolset; tanpanya, klik di posisi kursor
          if ("coordinate" in params && Array.isArray(params.coordinate)) {
            const [x, y] = params.coordinate;
            return clickAt(x, y);
          }
          return clickAtCursor();
        } else if (action === "type" && "text" in params) {
          return typeText(String(params.text));
        }
        // Tangani aksi lain sesuai kebutuhan
        throw new Error(`Unknown or unimplemented member: ${action}`);
      }
      ```

      ```csharp C#
      // Data gambar placeholder; eksekutor nyata menangkap layar dan mengembalikan byte PNG
      const string PlaceholderPng = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==";

      // screenshot menjawab dengan blok gambar, bukan teks: kembalikan daftar konten hasil
      List<Block> CaptureScreenshot() =>
          [
              new ImageBlockParam(
                  new Base64ImageSource { Data = PlaceholderPng, MediaType = MediaType.ImagePng }
              ),
          ];

      string ClickAt(int x, int y) => $"clicked at ({x}, {y})";

      string ClickAtCursor() => "clicked at the current cursor position";

      string TypeText(string text) => $"typed: {text}";

      ToolResultBlockParamContent HandleComputerAction(
          string action,
          IReadOnlyDictionary<string, JsonElement> input
      ) =>
          action switch
          {
              "screenshot" => CaptureScreenshot(),
              // coordinate bersifat opsional pada anggota click; tanpanya, klik di posisi kursor saat ini
              "left_click" when input.TryGetValue("coordinate", out var xy) => ClickAt(
                  xy[0].GetInt32(),
                  xy[1].GetInt32()
              ),
              "left_click" => ClickAtCursor(),
              "type" => TypeText(input["text"].GetString()!),
              // Tangani aksi lain sesuai kebutuhan
              _ => throw new NotSupportedException($"Unknown or unimplemented member: {action}"),
          };
      ```

      ```go Go
      // placeholderPNG menggantikan tangkapan layar nyata: executor mengembalikan
      // layar sebagai data PNG yang dienkode base64.
      const placeholderPNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

      // captureScreenshot mengembalikan blok gambar, bukan teks.
      func captureScreenshot() []anthropic.ToolResultBlockParamContentUnion {
      	return []anthropic.ToolResultBlockParamContentUnion{{
      		OfImage: &anthropic.ImageBlockParam{
      			Source: anthropic.ImageBlockParamSourceUnion{
      				OfBase64: &anthropic.Base64ImageSourceParam{
      					MediaType: anthropic.Base64ImageSourceMediaTypeImagePNG,
      					Data:      placeholderPNG,
      				},
      			},
      		},
      	}}
      }

      // textContent membungkus teks sebagai konten tool_result.
      func textContent(text string) []anthropic.ToolResultBlockParamContentUnion {
      	return []anthropic.ToolResultBlockParamContentUnion{
      		{OfText: &anthropic.TextBlockParam{Text: text}},
      	}
      }

      func clickAt(x, y int) string {
      	return fmt.Sprintf("clicked at (%d, %d)", x, y)
      }

      func clickAtCursor() string {
      	return "clicked at the current cursor position"
      }

      func typeText(text string) string {
      	return fmt.Sprintf("typed: %s", text)
      }

      func handleComputerAction(action string, params map[string]any) ([]anthropic.ToolResultBlockParamContentUnion, error) {
      	switch action {
      	case "screenshot":
      		return captureScreenshot(), nil
      	case "left_click":
      		// coordinate bersifat opsional; tanpanya, klik di posisi kursor saat ini
      		coord, ok := params["coordinate"].([]any)
      		if !ok {
      			return textContent(clickAtCursor()), nil
      		}
      		if len(coord) == 2 {
      			x, xok := coord[0].(float64)
      			y, yok := coord[1].(float64)
      			if xok && yok {
      				return textContent(clickAt(int(x), int(y))), nil
      			}
      		}
      	case "type":
      		if text, ok := params["text"].(string); ok {
      			return textContent(typeText(text)), nil
      		}
      	// Tangani aksi lain sesuai kebutuhan
      	default:
      		return nil, fmt.Errorf("unknown or unimplemented member: %s", action)
      	}
      	// Tercapai saat input anggota tidak memiliki field atau field bertipe salah
      	return nil, fmt.Errorf("invalid input for %s", action)
      }

      ```

      ```java Java
      /** Placeholder pixels; a real executor captures the screen and base64-encodes the PNG. */
      static final String PLACEHOLDER_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==";

      ToolResultBlockParam.Content captureScreenshot() {
          ImageBlockParam image = ImageBlockParam.builder()
                  .source(Base64ImageSource.builder()
                          .mediaType(Base64ImageSource.MediaType.IMAGE_PNG)
                          .data(PLACEHOLDER_PNG)
                          .build())
                  .build();
          return ToolResultBlockParam.Content.ofBlocks(
                  List.of(ToolResultBlockParam.Content.Block.ofImage(image)));
      }

      String clickAt(long x, long y) {
          return "clicked at (" + x + ", " + y + ")";
      }

      String clickAtCursor() {
          return "clicked at current cursor";
      }

      String typeText(String text) {
          return "typed: " + text;
      }

      /** Runs one computer toolset member; {@code action} is the tool_use block's name. */
      ToolResultBlockParam.Content handleComputerAction(String action, Map<String, JsonValue> input) {
          if (action.equals("screenshot")) {
              return captureScreenshot(); // the one member here that answers with an image block
          }
          String output = switch (action) {
              case "left_click" -> {
                  JsonValue coordinate = input.get("coordinate"); // optional on the toolset
                  if (coordinate == null) {
                      yield clickAtCursor();
                  }
                  List<JsonValue> point = (List<JsonValue>) coordinate.asArray().get();
                  long x = ((Number) point.get(0).asNumber().get()).longValue();
                  long y = ((Number) point.get(1).asNumber().get()).longValue();
                  yield clickAt(x, y);
              }
              case "type" -> typeText(input.get("text").asStringOrThrow());
              // Tangani aksi lain sesuai kebutuhan
              default -> throw new UnsupportedOperationException("Unknown or unimplemented member: " + action);
          };
          return ToolResultBlockParam.Content.ofString(output);
      }
      ```

      ```php PHP
      // Pengganti untuk byte PNG asli; eksekutor nyata menangkap layar
      const PLACEHOLDER_PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==';

      function captureScreenshot(): array
      {
          // screenshot menjawab dengan blok gambar, bukan teks, jadi kembalikan daftar konten hasil
          $image = [
              'type' => 'image',
              'source' => ['type' => 'base64', 'media_type' => 'image/png', 'data' => PLACEHOLDER_PNG],
          ];

          return [$image];
      }

      function clickAt(?array $coordinate): string
      {
          // left_click boleh tanpa coordinate; jika demikian, klik terjadi di posisi kursor saat ini
          if ($coordinate === null) {
              return 'clicked at current cursor';
          }
          [$x, $y] = $coordinate;

          return "clicked at ({$x}, {$y})";
      }

      function typeText(string $text): string
      {
          return "typed: {$text}";
      }

      function handleComputerAction(string $name, array $input): string|array
      {
          return match ($name) {
              'screenshot' => captureScreenshot(),
              'left_click' => clickAt($input['coordinate'] ?? null),
              'type' => typeText($input['text']),
              // Tangani aksi lain sesuai kebutuhan
              default => throw new RuntimeException("Unknown or unimplemented member: {$name}"),
          };
      }
      ```

      ```ruby Ruby
      # Data gambar pengganti; eksekutor nyata menangkap layar sebagai PNG.
      PLACEHOLDER_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

      # screenshot menjawab dengan blok gambar, bukan teks
      def capture_screenshot
        [
          {
            type: "image",
            source: { type: "base64", media_type: "image/png", data: PLACEHOLDER_PNG }
          }
        ]
      end

      def click(coordinate = nil)
        return "clicked at current cursor" if coordinate.nil?

        x, y = coordinate
        "clicked at (#{x}, #{y})"
      end

      def type_text(text)
        "typed: #{text}"
      end

      def handle_computer_action(name, input)
        case name
        when "screenshot"
          capture_screenshot
        when "left_click"
          # coordinate bersifat opsional; tanpanya, klik di posisi kursor saat ini
          click(input[:coordinate])
        when "type"
          type_text(input[:text])
        # Tangani aksi lain sesuai kebutuhan
        else
          raise ArgumentError, "Unknown or unimplemented member: #{name}"
        end
      end
      ```
    </CodeGroup>
  </Step>

  <Step title="Proses panggilan alat Claude">
    Ekstrak dan jalankan panggilan alat dari respons Claude:

    <CodeGroup exclude="shell">
      ```python Python
      NOT_EXECUTED = "Not executed: an earlier computer action in this turn failed."


      def process_tool_calls(response: Message) -> list[ToolResultBlockParam]:
          """
          Run the computer actions in Claude's response in order and answer each
          one. After the first failure the rest are skipped, because Claude planned
          them assuming the earlier actions succeeded.
          """
          tool_results: list[ToolResultBlockParam] = []
          failed = False
          for block in response.content:
              # Hanya toolset computer yang dideklarasikan; arahkan alat lain ke sini jika Anda menambahkannya
              if block.type != "tool_use" or block.toolset_name != "computer":
                  continue
              result: ToolResultBlockParam = {
                  "type": "tool_result",
                  "tool_use_id": block.id,
                  "toolset_name": "computer",
              }
              if failed:
                  result["content"] = NOT_EXECUTED
                  result["is_error"] = True
              else:
                  try:
                      # Sebuah string, atau daftar blok konten seperti gambar screenshot
                      result["content"] = handle_computer_action(block.name, block.input)
                  except Exception as err:
                      result["content"] = f"Error: {err}"
                      result["is_error"] = True
                      failed = True
              tool_results.append(result)
          return tool_results
      ```

      ```typescript TypeScript
      const HALT_TEXT =
        "Not executed: an earlier computer action in this turn failed.";

      function computerResult(
        toolUseId: string,
        content: string | Anthropic.ImageBlockParam[],
        isError?: boolean,
      ): Anthropic.ToolResultBlockParam {
        return {
          type: "tool_result",
          tool_use_id: toolUseId,
          toolset_name: "computer",
          content,
          is_error: isError,
        };
      }

      function processToolCalls(
        response: Anthropic.Message,
      ): Anthropic.ToolResultBlockParam[] {
        const toolResults: Anthropic.ToolResultBlockParam[] = [];
        let failed = false;
        for (const block of response.content) {
          if (block.type !== "tool_use") {
            continue;
          }
          if (block.toolset_name !== "computer") {
            // Contoh ini hanya mendeklarasikan toolset computer; arahkan alat lain
            // ke sini jika Anda menambahkannya.
            continue;
          }
          if (failed) {
            // Batch berhenti pada kegagalan pertama; jawab aksi berikutnya sebagai tidak dieksekusi
            toolResults.push(computerResult(block.id, HALT_TEXT, true));
            continue;
          }
          try {
            // Sebuah string, atau daftar blok gambar yang dikembalikan screenshot
            const result = handleComputerAction(block.name, block.input);
            toolResults.push(computerResult(block.id, result));
          } catch (error) {
            failed = true;
            const message = error instanceof Error ? error.message : String(error);
            toolResults.push(computerResult(block.id, `Error: ${message}`, true));
          }
        }
        return toolResults;
      }
      ```

      ```csharp C#
      const string HaltText = "Not executed: an earlier computer action in this turn failed.";

      List<ContentBlockParam> ProcessToolCalls(Message response)
      {
          List<ContentBlockParam> toolResults = [];
          var failed = false;
          foreach (var block in response.Content)
          {
              if (!block.TryPickToolUse(out var toolUse))
              {
                  continue;
              }

              if (toolUse.ToolsetName != "computer")
              {
                  // Contoh ini hanya mendeklarasikan toolset computer; arahkan alat lain
                  // ke sini jika Anda menambahkannya.
                  continue;
              }

              if (failed)
              {
                  // Batch berhenti pada kegagalan pertamanya; jawab aksi berikutnya tanpa menjalankannya
                  toolResults.Add(
                      new ToolResultBlockParam(toolUse.ID)
                      {
                          Content = HaltText,
                          IsError = true,
                          ToolsetName = "computer",
                      }
                  );
                  continue;
              }

              try
              {
                  // Sebuah string, atau daftar blok gambar yang dikembalikan screenshot
                  var result = HandleComputerAction(toolUse.Name, toolUse.Input);
                  toolResults.Add(
                      new ToolResultBlockParam(toolUse.ID) { Content = result, ToolsetName = "computer" }
                  );
              }
              catch (Exception e)
              {
                  failed = true;
                  toolResults.Add(
                      new ToolResultBlockParam(toolUse.ID)
                      {
                          Content = $"Error: {e.Message}",
                          IsError = true,
                          ToolsetName = "computer",
                      }
                  );
              }
          }
          return toolResults;
      }
      ```

      ```go Go
      const notExecuted = "Not executed: an earlier computer action in this turn failed."

      // computerToolResult membangun hasil untuk satu aksi komputer. Berbeda dengan
      // hasil alat biasa, ia harus menyertakan kembali nama toolset.
      func computerToolResult(toolUseID string, content []anthropic.ToolResultBlockParamContentUnion, isError bool) anthropic.ContentBlockParamUnion {
      	result := anthropic.ToolResultBlockParam{
      		ToolUseID:   toolUseID,
      		ToolsetName: anthropic.String("computer"),
      		Content:     content,
      	}
      	if isError {
      		result.IsError = anthropic.Bool(true)
      	}
      	return anthropic.ContentBlockParamUnion{OfToolResult: &result}
      }

      // processToolCalls menjalankan aksi komputer dalam respons Claude secara berurutan dan
      // membangun satu tool_result per blok tool_use. Setelah kegagalan pertama, sisanya
      // dilewati: Claude merencanakannya dengan asumsi aksi sebelumnya berhasil.
      func processToolCalls(response *anthropic.Message) []anthropic.ContentBlockParamUnion {
      	var toolResults []anthropic.ContentBlockParamUnion
      	failed := false
      	for _, block := range response.Content {
      		switch variant := block.AsAny().(type) {
      		case anthropic.ToolUseBlock:
      			// Contoh ini hanya mendeklarasikan toolset komputer; arahkan alat lain ke sini jika Anda menambahkannya.
      			if variant.ToolsetName != "computer" {
      				continue
      			}
      			if failed {
      				toolResults = append(toolResults, computerToolResult(variant.ID, textContent(notExecuted), true))
      				continue
      			}
      			var input map[string]any
      			var content []anthropic.ToolResultBlockParamContentUnion
      			err := json.Unmarshal(variant.Input, &input)
      			if err == nil {
      				// Teks, atau blok gambar yang dikembalikan screenshot
      				content, err = handleComputerAction(variant.Name, input)
      			}
      			if err != nil {
      				failed = true
      				content = textContent("Error: " + err.Error())
      			}
      			toolResults = append(toolResults, computerToolResult(variant.ID, content, err != nil))
      		}
      	}
      	return toolResults
      }

      ```

      ```java Java
      /** The exact text the toolset contract prescribes for member calls skipped after a failure. */
      static final String HALT_TEXT = "Not executed: an earlier computer action in this turn failed.";

      /** Every result answering a computer toolset member echoes toolset_name. */
      ToolResultBlockParam.Builder computerResult(ToolUseBlock toolUse) {
          return ToolResultBlockParam.builder()
                  .toolUseId(toolUse.id())
                  .toolsetName("computer");
      }

      /**
       * Run the computer actions in Claude's response in order and build one
       * tool_result per tool_use block. After the first failure, skip the rest:
       * Claude planned them assuming the earlier actions succeeded.
       */
      List<ContentBlockParam> processToolCalls(Message response) {
          List<ContentBlockParam> toolResults = new ArrayList<>();
          boolean failed = false;
          for (ContentBlock block : response.content()) {
              // Contoh ini hanya mendeklarasikan toolset computer; arahkan alat lain ke sini jika Anda menambahkannya.
              if (!block.isToolUse() || !block.asToolUse().toolsetName().equals(Optional.of("computer"))) {
                  continue;
              }
              ToolUseBlock toolUse = block.asToolUse();
              ToolResultBlockParam result;
              if (failed) {
                  result = computerResult(toolUse).content(HALT_TEXT).isError(true).build();
              } else {
                  try {
                      Map<String, JsonValue> input =
                              (Map<String, JsonValue>) toolUse._input().asObject().get();
                      // Sebuah string, atau blok gambar yang dikembalikan oleh screenshot
                      ToolResultBlockParam.Content output = handleComputerAction(toolUse.name(), input);
                      result = computerResult(toolUse).content(output).build();
                  } catch (RuntimeException e) {
                      failed = true;
                      result = computerResult(toolUse).content("Error: " + e.getMessage()).isError(true).build();
                  }
              }
              toolResults.add(ContentBlockParam.ofToolResult(result));
          }
          return toolResults;
      }
      ```

      ```php PHP
      const HALT_TEXT = 'Not executed: an earlier computer action in this turn failed.';

      function processToolCalls(Message $response): array
      {
          $toolResults = [];
          $failed = false;
          foreach ($response->content as $block) {
              // Contoh ini hanya mendeklarasikan toolset computer; arahkan alat lain ke sini jika Anda menambahkannya.
              if (!($block instanceof ToolUseBlock) || $block->toolsetName !== 'computer') {
                  continue;
              }
              $result = ['type' => 'tool_result', 'tool_use_id' => $block->id, 'toolset_name' => 'computer'];
              if ($failed) {
                  // Batch berhenti pada kegagalan pertama; aksi sisanya dijawab tanpa dijalankan
                  $toolResults[] = [...$result, 'content' => HALT_TEXT, 'is_error' => true];
                  continue;
              }
              try {
                  // Sebuah string, atau daftar blok gambar yang dikembalikan screenshot
                  $toolResults[] = [...$result, 'content' => handleComputerAction($block->name, $block->input)];
              } catch (Throwable $e) {
                  $failed = true;
                  $toolResults[] = [...$result, 'content' => 'Error: ' . $e->getMessage(), 'is_error' => true];
              }
          }

          return $toolResults;
      }
      ```

      ```ruby Ruby
      NOT_EXECUTED = "Not executed: an earlier computer action in this turn failed."

      # Jalankan aksi komputer dalam respons Claude secara berurutan dan buat satu
      # tool_result per blok tool_use. Setelah kegagalan pertama, lewati sisanya:
      # Claude merencanakannya dengan asumsi aksi sebelumnya berhasil.
      def process_tool_calls(response)
        tool_results = []
        failed = false
        response.content.each do |block|
          # Contoh ini hanya mendeklarasikan toolset komputer; arahkan alat lain ke sini
          # jika Anda menambahkannya.
          next unless block.type == :tool_use && block.toolset_name == "computer"

          result = { type: "tool_result", tool_use_id: block.id, toolset_name: "computer" }
          if failed
            result.update(content: NOT_EXECUTED, is_error: true)
          else
            begin
              # Sebuah String, atau blok konten gambar yang dikembalikan screenshot
              result[:content] = handle_computer_action(block.name, block.input)
            rescue => e
              result.update(content: "Error: #{e.message}", is_error: true)
              failed = true
            end
          end
          tool_results << result
        end
        tool_results
      end
      ```
    </CodeGroup>
  </Step>

  <Step title="Implementasikan loop agen">
    Bungkus dua langkah sebelumnya dalam sebuah loop yang mengirimkan hasilnya kembali dan berulang hingga Claude tidak mengembalikan panggilan alat anggota; [Memahami loop agen](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#understanding-the-agentic-loop) menunjukkan loop ini dalam setiap bahasa.
  </Step>
</Steps>

### Tangani error

Laporkan tindakan yang gagal kepada Claude sebagai `tool_result` dengan `is_error: true` dan deskripsi singkat, serta sertakan `"toolset_name": "computer"` seperti pada hasil anggota lainnya. Jika tindakan yang gagal merupakan bagian dari [aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions), jawab blok-blok yang tersisa dalam batch dengan teks penghentian yang ditunjukkan di sana alih-alih menjalankannya.

Misalnya, ketika pengambilan tangkapan layar gagal:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "toolset_name": "computer",
      "content": "Error: Failed to capture screenshot. Display may be locked or unavailable.",
      "is_error": true
    }
  ]
}
```

Gunakan bentuk yang sama untuk koordinat di luar batas tampilan dan untuk tindakan yang gagal dijalankan, dengan pesan yang menjelaskan apa yang salah.

### Sesuaikan ukuran tangkapan layar agar sesuai batas gambar

Tangkapan layar dan gambar zoom yang Anda kembalikan ke toolset computer use harus sudah muat dalam [batas ukuran gambar](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size) model Anda: toolset tidak menerima dimensi tampilan dan API tidak memperkecil gambar untuk Anda, sehingga gambar `tool_result` yang terlalu besar ditolak dengan error validasi. Karena Claude mengembalikan koordinat dalam ruang piksel gambar yang dilihatnya, simpan faktor skala yang Anda gunakan agar Anda dapat memetakan koordinat tersebut kembali ke layar Anda.

<Note>
  Batas bervariasi menurut model. Claude Opus 4.7 dan model yang lebih baru, termasuk setiap model yang mendukung `computer_toolset_20260801`, menerima hingga 2576 piksel pada sisi panjang dan total 4784 token visual (`⌈width / 28⌉ × ⌈height / 28⌉`, sekitar 3,75 megapiksel); model yang lebih lama menerima hingga 1568 piksel pada sisi panjang dan total sekitar 1,15 megapiksel (lihat [Resolusi dan biaya token](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size) untuk tingkat setiap model). Contoh berikut menggunakan batas model lama 1568 px / 1,15 MP. Untuk model tingkat resolusi tinggi, sesuaikan ukuran dengan batas token visual, bukan total piksel, misalnya dengan helper pengubah ukuran di [Ubah ukuran gambar Anda sebelum mengunggah](https://platform.claude.com/docs/id/build-with-claude/vision-coordinates#resize-your-image-before-uploading).
</Note>

Jika layar Anda lebih besar dari batas, ubah ukuran setiap tangkapan layar sebelum mengembalikannya dan skalakan koordinat yang dikembalikan Claude kembali ke ruang layar asli. Karena toolset tidak menerima dimensi tampilan, pengubahan ukuran dan penskalaan koordinat dalam kode aplikasi Anda adalah semua yang Anda perlukan:

<CodeGroup exclude="shell">
  ```python Python
  import math

  screen_width, screen_height = 1512, 982


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

  # Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
  screenshot = capture_and_resize(scaled_width, scaled_height)


  # Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
  def execute_click(x, y):
      screen_x = x / scale
      screen_y = y / scale
      perform_click(screen_x, screen_y)
  ```

  ```typescript TypeScript
  const screenWidth = 1512;
  const screenHeight = 982;
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

  // Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
  const screenshot = captureAndResize(scaledWidth, scaledHeight);

  // Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
  function executeClick(x: number, y: number): void {
    const screenX = x / scale;
    const screenY = y / scale;
    performClick(screenX, screenY);
  }
  ```

  ```csharp C#
  int screenWidth = 1512, screenHeight = 982;

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

  // Ubah ukuran gambar ke dimensi yang telah diskalakan sebelum mengirim ke Claude
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
  	screenWidth, screenHeight := 1512, 982

  	// Saat mengambil tangkapan layar
  	scale := getScaleFactor(screenWidth, screenHeight)
  	scaledWidth := int(float64(screenWidth) * scale)
  	scaledHeight := int(float64(screenHeight) * scale)

  	// Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
  	screenshot := captureAndResize(scaledWidth, scaledHeight)

  	// Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
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
      int screenWidth = 1512, screenHeight = 982;

      // Saat mengambil tangkapan layar
      double scale = getScaleFactor(screenWidth, screenHeight);
      int scaledWidth = (int)(screenWidth * scale);
      int scaledHeight = (int)(screenHeight * scale);

      // Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
      var screenshot = captureAndResize(scaledWidth, scaledHeight);

      // Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
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

  $screenWidth = 1512;
  $screenHeight = 982;

  // Saat mengambil tangkapan layar
  $scale = getScaleFactor($screenWidth, $screenHeight);
  $scaledWidth = (int)($screenWidth * $scale);
  $scaledHeight = (int)($screenHeight * $scale);

  // Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
  $screenshot = captureAndResize($scaledWidth, $scaledHeight);

  // Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
  $executeClick = fn(int $x, int $y) => performClick($x / $scale, $y / $scale);
  ```

  ```ruby Ruby
  def get_scale_factor(width, height)
    [1.0, 1568.0 / [width, height].max, Math.sqrt(1_150_000.0 / (width * height))].min
  end

  screen_width, screen_height = 1512, 982

  # Saat mengambil tangkapan layar
  scale = get_scale_factor(screen_width, screen_height)
  scaled_width = (screen_width * scale).to_i
  scaled_height = (screen_height * scale).to_i

  # Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
  screenshot = capture_and_resize(scaled_width, scaled_height)

  # Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
  execute_click = ->(x, y) { perform_click(x / scale, y / scale) }
  ```
</CodeGroup>

<Note>
  **Tampilan Retina macOS** menangkap tangkapan layar dengan rasio piksel perangkat 2, sehingga gambar memiliki resolusi dua kali lipat dari koordinat layar logis. Perkecil tangkapan layar 2x sebelum mengirim, atau bagi dua koordinat yang dikembalikan Claude sebelum melakukan klik.
</Note>

Saat Anda memilih resolusi tampilan dan mengembalikan tangkapan layar:

* Untuk tugas desktop umum, gunakan 1024x768 atau 1280x720; untuk aplikasi web, gunakan 1280x800 atau 1366x768.
* Hindari resolusi di atas 1920x1080 untuk mencegah masalah kinerja.
* Enkode tangkapan layar sebagai PNG atau JPEG base64, dan pertimbangkan untuk mengompresi tangkapan layar besar guna meningkatkan kinerja.
* Sertakan metadata yang relevan seperti timestamp atau keadaan tampilan.
* Jika Anda menggunakan resolusi yang lebih tinggi, pastikan koordinat diskalakan secara akurat.

### Mengelola riwayat tangkapan layar

Loop agen yang panjang mengakumulasi tangkapan layar dengan cepat (kira-kira 1.000–1.800 token input masing-masing). [Batas permintaan](https://platform.claude.com/docs/id/build-with-claude/vision#request-limits) API juga berlaku. Begitu satu permintaan membawa lebih dari 20 gambar, setiap gambar di dalamnya dikenai batas per sisi yang lebih ketat. Loop yang menyimpan riwayat tangkapan layarnya mencapai jumlah tersebut dalam beberapa puluh giliran, jadi ubah ukuran setiap tangkapan layar sehingga tidak ada sisi yang melebihi 2000 px atau pangkas tangkapan layar lama agar tetap 20 atau kurang dalam permintaan.

Agar [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) tetap efektif sambil membatasi konteks:

* Tempatkan satu breakpoint `cache_control` setelah prompt sistem dan definisi alat, dan hingga tiga lagi pada blok `tool_result` terakhir dari masing-masing giliran terbaru, dengan memajukannya setiap giliran. Dalam [aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions), penanda pada beberapa blok bertindak sebagai satu breakpoint tetapi masing-masing tetap dihitung terhadap batas empat, jadi gunakan satu per giliran.
* Pangkas tangkapan layar lama secara *batch*, bukan satu per giliran. Membuang satu tangkapan layar setiap giliran mengubah prefiks setiap giliran dan membatalkan cache. Default yang wajar adalah menyimpan tiga tangkapan layar terakhir dan memangkas setiap 25 giliran, sehingga prefiks tetap identik byte demi byte di antara peristiwa pemangkasan; jika tangkapan layar Anda melebihi 2000 px pada salah satu sisi, pilih interval yang menjaga setiap permintaan pada 20 gambar atau kurang.

### Mendiagnosis masalah klik

Jika klik meleset dari targetnya, penyebabnya biasanya salah satu dari berikut ini:

| Gejala                                                      | Kemungkinan penyebab                                                                                                                                 | Coba                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Klik secara konsisten bergeser ke satu arah                 | Koordinat Claude, yang berada dalam ruang piksel tangkapan layar yang Anda kembalikan, diterapkan ke tampilan dengan ukuran berbeda tanpa penskalaan | Skalakan setiap koordinat dengan rasio ukuran layar Anda terhadap ukuran tangkapan layar Anda sebelum mengklik (lihat [Menyesuaikan ukuran tangkapan layar agar sesuai batas gambar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions)); pada layar Retina macOS, perhitungkan rasio piksel perangkat 2x |
| Klik mendarat di area yang benar tetapi meleset dari target | Target sangat kecil, detail hilang saat menurunkan skala sumber 4K+, atau rasio aspek terdistorsi                                                    | Biarkan anggota `zoom` tetap aktif dan implementasikan agar Claude dapat memeriksa wilayah tersebut pada resolusi penuh; tangkap pada DPI lebih rendah atau potong ke wilayah yang relevan; pertahankan rasio aspek saat mengubah ukuran                                                                                                                                                 |
| Claude mengklik elemen yang sepenuhnya salah                | Instruksi ambigu, atau elemen yang mirip secara visual di dekatnya                                                                                   | Gunakan prompt posisional ("tombol Submit biru di kanan bawah"); pecah interaksi menjadi langkah-langkah yang lebih kecil                                                                                                                                                                                                                                                                |
| Akurasi secara konsisten buruk                              | Resolusi terlalu rendah                                                                                                                              | Coba 1280x720 sebagai baseline                                                                                                                                                                                                                                                                                                                                                           |

<Tip>
  **Pilihan model memengaruhi presisi klik.** Di antara model yang menggunakan alat `computer_20251124` sebelumnya, Claude Sonnet 4.6 lebih presisi secara mekanis dalam mengklik daripada Claude Opus 4.6 dan lebih tangguh ketika tangkapan layar memerlukan penurunan skala yang besar. Claude Opus 4.7 mempersempit kesenjangan itu: presisi kliknya kira-kira sebanding dengan Sonnet 4.6, dan batas resolusinya yang lebih tinggi berarti lebih sedikit penurunan skala yang diperlukan.
</Tip>

### Mengikuti praktik terbaik implementasi

<AccordionGroup>
  <Accordion title="Menambahkan jeda aksi">
    Beberapa aplikasi memerlukan waktu untuk merespons aksi:

    <CodeGroup exclude="shell">
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

  <Accordion title="Memvalidasi aksi sebelum menjalankannya">
    Periksa bahwa aksi yang diminta aman dan valid:

    <CodeGroup exclude="shell">
      ```python Python
      display_width, display_height = 1024, 768


      def validate_action(action_type, params):
          if action_type == "left_click" and "coordinate" in params:
              x, y = params["coordinate"]
              if not (0 <= x < display_width and 0 <= y < display_height):
                  return False, "Coordinates out of bounds"
          return True, None
      ```

      ```typescript TypeScript
      const displayWidth = 1024;
      const displayHeight = 768;

      interface ActionParams {
        coordinate?: [number, number];
      }

      function validateAction(actionType: string, params: ActionParams): [boolean, string | null] {
        if (actionType === "left_click" && params.coordinate) {
          const [x, y] = params.coordinate;
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
          if (actionType == "left_click" && parameters.TryGetValue("coordinate", out JsonElement coordinate))
          {
              int x = coordinate[0].GetInt32();
              int y = coordinate[1].GetInt32();
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
      	raw, hasCoordinate := params["coordinate"]
      	if actionType == "left_click" && hasCoordinate {
      		coord, ok := raw.([]any)
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
          if (actionType.equals("left_click") && params.containsKey("coordinate")) {
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
          if ($actionType === 'left_click' && isset($params['coordinate'])) {
              [$x, $y] = $params['coordinate'];
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
        if action_type == "left_click" && params.key?(:coordinate)
          x, y = params[:coordinate]
          unless (0...DISPLAY_WIDTH).cover?(x) && (0...DISPLAY_HEIGHT).cover?(y)
            return [false, "Coordinates out of bounds"]
          end
        end
        [true, nil]
      end
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Mencatat aksi untuk debugging">
    Simpan log semua aksi untuk pemecahan masalah:

    <CodeGroup exclude="shell">
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

## Migrasi dari `computer_20251124`

Peningkatan dari `computer_20251124` ke toolset bersifat opsional: model yang tercantum untuk `computer_20251124` di bawah [Versi alat sebelumnya](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#earlier-tool-versions) tetap menerimanya dengan header beta-nya, sehingga integrasi yang ada tetap berfungsi sampai Anda mengubahnya. Untuk meningkatkan, lakukan perubahan berikut secara bersamaan:

1. **Hapus header beta.** Buang `anthropic-beta: computer-use-2025-11-24` dari permintaan Anda. Di SDK, hapus parameter `betas` dan panggil Messages API melalui klien standar, bukan namespace beta.
2. **Ubah entri `tools`.** Atur `type` ke `computer_toolset_20260801` dan hapus `name`, `display_width_px`, `display_height_px`, `display_number`, dan `enable_zoom`. Toolset menolak masing-masing field ini.
3. **Pilih apakah zoom tetap diaktifkan.** Zoom diaktifkan secara default pada toolset, sedangkan `enable_zoom` default-nya `false`. Jika lingkungan Anda tidak mengimplementasikan zoom, tambahkan `"configs": {"zoom": {"enabled": false}}` untuk mempertahankan perilaku sebelumnya; jika tidak, implementasikan (lihat [Aksi yang tersedia](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#available-actions)).
4. **Tangani setiap blok dalam satu giliran.** Perbarui loop agen Anda untuk mengiterasi setiap blok `tool_use` dalam respons, bukan hanya membaca yang pertama, dan untuk melakukan dispatch berdasarkan `name` blok bersama dengan `toolset_name`, bukan berdasarkan `input.action`. Input anggota tidak lagi berisi field `action`; field lainnya tidak berubah.
5. **Jalankan blok secara berurutan dan gunakan teks penghentian.** Jalankan blok secara berurutan, berhenti pada kegagalan pertama, dan jawab blok yang tersisa dengan `Not executed: an earlier computer action in this turn failed.` seperti dijelaskan dalam [Aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions). Jika loop Anda belum dapat menjalankan batch, [Parameter alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#tool-parameters) menjelaskan cara membatasi Claude ke satu aksi per giliran.
6. **Gemakan `toolset_name` pada hasil.** Tambahkan `"toolset_name": "computer"` ke setiap `tool_result` yang menjawab panggilan anggota. Hasil hanya boleh berisi konten `text` dan `image`.
7. **Dukung `repeat` pada `key`.** Anggota `key` menerima hitungan `repeat` opsional dari 1 hingga 100. Handler yang mengabaikan field yang tidak dikenali akan menekan tombol sekali, jadi pastikan handler `key` Anda menghormati `repeat`.
8. **Ubah ukuran tangkapan layar sendiri.** Toolset menolak tangkapan layar atau gambar zoom yang melebihi batas gambar model alih-alih menurunkan skalanya. Ubah ukuran sebelum mengembalikan gambar dan tetap skalakan koordinat seperti dijelaskan dalam [Menyesuaikan ukuran tangkapan layar agar sesuai batas gambar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions).
9. **Hapus opsi yang tidak didukung.** Pindahkan `defer_loading` apa pun dari entri ke dalam `configs`, dengan nilai yang sama pada setiap anggota yang diaktifkan. Opsi lain yang tidak didukung pada entri toolset tercantum di bawah [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets).

Ini adalah entri `tools` sebelum perubahan, dikirim dengan header `anthropic-beta: computer-use-2025-11-24`:

```json
{
  "type": "computer_20251124",
  "name": "computer",
  "display_width_px": 1024,
  "display_height_px": 768,
  "display_number": 1
}
```

Ini adalah entri `tools` setelah perubahan, dikirim tanpa header beta. Objek `configs` menjaga zoom tetap nonaktif agar sesuai dengan entri sebelumnya, yang tidak mengatur `enable_zoom`; hilangkan `configs` sepenuhnya untuk menerima default dan membiarkan Claude melakukan zoom:

```json
{
  "type": "computer_toolset_20260801",
  "configs": {
    "zoom": { "enabled": false }
  }
}
```

Pasangan berikut menunjukkan blok `tool_use` sebelum dan sesudah perubahan. Nama aksi berpindah dari `input.action` ke `name`, dan blok mendapatkan `toolset_name`:

```json
{
  "type": "tool_use",
  "id": "toolu_01A9r5kQm2LxWc7vT3nZ4bJs",
  "name": "computer",
  "input": { "action": "left_click", "coordinate": [500, 300] }
}
```

```json
{
  "type": "tool_use",
  "id": "toolu_01A9r5kQm2LxWc7vT3nZ4bJs",
  "name": "left_click",
  "toolset_name": "computer",
  "input": { "coordinate": [500, 300] }
}
```

## Versi alat sebelumnya

Dua versi sebelumnya dari alat computer use tetap tersedia dalam beta untuk integrasi yang ada, untuk model yang tidak mendukung toolset, dan pada platform tempat toolset saat ini belum tersedia. Masing-masing memerlukan [header beta](https://platform.claude.com/docs/id/api/beta-headers)-nya pada setiap permintaan, dan parameternya didokumentasikan dalam [referensi Messages API beta](https://platform.claude.com/docs/id/api/beta/messages/create). Di SDK, teruskan header melalui parameter `betas` dan gunakan namespace beta; hanya alat computer use yang memerlukan header, bukan alat bash atau editor teks dalam permintaan yang sama.

| Versi alat          | Header beta               | Gunakan dengan                                                                                                                                                                                                                                                                                                                                                                                                                                                | Parameter                                                                     |
| ------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `computer_20251124` | `computer-use-2025-11-24` | Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Opus 4.5                                                                                                                                                                                                                                                                                                    | [Referensi API](https://platform.claude.com/docs/id/api/beta/messages/create) |
| `computer_20250124` | `computer-use-2025-01-24` | Claude Sonnet 4.5, Claude Haiku 4.5, Claude Opus 4.1 ([dipensiunkan, kecuali di Bedrock dan Google Cloud](https://platform.claude.com/docs/id/about-claude/model-deprecations)), Claude Sonnet 4 ([dipensiunkan, kecuali di Bedrock dan Google Cloud](https://platform.claude.com/docs/id/about-claude/model-deprecations)), dan Claude Opus 4 ([dipensiunkan, kecuali di Google Cloud](https://platform.claude.com/docs/id/about-claude/model-deprecations)) | [Referensi API](https://platform.claude.com/docs/id/api/beta/messages/create) |

***

## Keterbatasan

1. **Latensi:** "Latency" (latensi) computer use saat ini untuk interaksi manusia-AI mungkin terlalu lambat dibandingkan dengan aksi komputer biasa yang diarahkan manusia. Fokuslah pada kasus penggunaan di mana kecepatan tidak kritis (misalnya, pengumpulan informasi latar belakang, pengujian perangkat lunak otomatis) di lingkungan tepercaya.
2. **Akurasi dan keandalan computer vision:** Claude mungkin membuat kesalahan atau berhalusinasi saat mengeluarkan koordinat tertentu ketika menghasilkan aksi. Output [pemikiran ringkas](https://platform.claude.com/docs/id/build-with-claude/thinking#summarized-thinking) Claude dapat membantu Anda memahami penalaran model dan mengidentifikasi potensi masalah; atur `display: "summarized"` pada konfigurasi thinking, karena model yang mendukung toolset menghilangkan teks thinking secara default.
3. **Akurasi dan keandalan pemilihan alat:** Claude mungkin membuat kesalahan atau berhalusinasi saat memilih alat ketika menghasilkan aksi atau mengambil aksi tak terduga untuk menyelesaikan masalah. Selain itu, keandalan mungkin lebih rendah saat berinteraksi dengan aplikasi khusus atau beberapa aplikasi sekaligus. Berikan prompt kepada model dengan hati-hati saat meminta tugas yang kompleks.
4. **Keandalan scrolling:** Aksi scroll mendukung kontrol arah (atas, bawah, kiri, kanan) dan jumlah yang ditentukan. Pada aplikasi di mana scrolling tidak berpengaruh, alternatif keyboard seperti Page Down dapat membantu.
5. **Interaksi spreadsheet:** Gunakan aksi kontrol mouse yang terperinci (`left_mouse_down`, `left_mouse_up`) dan kombinasi tombol modifier untuk memilih sel individual. Operasi spreadsheet yang kompleks mungkin masih memerlukan beberapa percobaan.
6. **Pembuatan akun dan pembuatan konten di platform sosial dan komunikasi:** Meskipun Claude mengunjungi situs web, kemampuannya untuk membuat akun, menghasilkan dan membagikan konten, atau terlibat dalam peniruan manusia di situs web dan platform media sosial terbatas.
7. **Kerentanan:** Jailbreak dan prompt injection dapat memengaruhi computer use sebagaimana dapat memengaruhi sistem AI frontier mana pun, termasuk melalui instruksi yang disematkan dalam halaman web atau gambar; terapkan tindakan pencegahan dalam [Pertimbangan keamanan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#security-considerations).
8. **Aksi yang tidak pantas atau ilegal:** Berdasarkan Ketentuan Layanan Anthropic, Anda tidak boleh menggunakan computer use untuk melanggar hukum apa pun atau Kebijakan Penggunaan yang Dapat Diterima.

Selalu tinjau dan verifikasi dengan cermat aksi dan log computer use Claude. Jangan gunakan Claude untuk tugas yang memerlukan presisi sempurna atau informasi pengguna yang sensitif tanpa pengawasan manusia.

## Retensi data

Computer use adalah alat sisi klien. Semua tangkapan layar, aksi mouse, input keyboard, dan file apa pun yang terlibat dalam sesi ditangkap dan disimpan di lingkungan Anda, bukan oleh Anthropic. Anthropic memproses gambar tangkapan layar dan permintaan aksi secara real time sebagai bagian dari panggilan API. Retensi untuk permintaan API tersebut diatur oleh [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

Karena aplikasi Anda mengontrol di mana dan bagaimana data computer use disimpan, computer use memenuhi syarat ZDR. Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

## Harga

Computer use mengikuti [harga penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview#pricing) standar. Saat menggunakan alat computer use:

**Overhead definisi toolset:** Mendeklarasikan `computer_toolset_20260801` dengan anggota defaultnya menambahkan sekitar 4.500 token input ke sebuah permintaan (sekitar 4.520 pada Claude Fable 5, Claude Mythos 5, Claude Opus 5, dan Claude Opus 4.8, serta sekitar 4.590 pada Claude Sonnet 5), yang mencakup definisi alat anggota dan prompt sistem penggunaan alat. Menonaktifkan `zoom` dengan `configs` menghapus sekitar 410 dari token tersebut. Jumlah pasti untuk sebuah permintaan dilaporkan dalam `usage` respons, dan Anda dapat memperkirakannya terlebih dahulu dengan [endpoint penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).

**Versi alat sebelumnya:** Angka-angka berikut berlaku untuk versi alat `computer_20251124` dan `computer_20250124`, bukan untuk `computer_toolset_20260801`:

* Overhead prompt sistem: 466–499 token ditambahkan ke prompt sistem
* Definisi alat: sekitar 735 token input per definisi alat (diukur dengan `computer_20250124`)

**Konsumsi token tambahan:**

* Gambar screenshot dan zoom yang dikembalikan dalam hasil alat, ditagih sebagai input gambar (lihat [Harga Vision](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size))
* Hasil eksekusi alat yang dikembalikan ke Claude

<Note>
  Jika Anda juga menggunakan alat bash atau editor teks bersama computer use, alat-alat tersebut memiliki biaya token sendiri seperti yang didokumentasikan di halaman masing-masing.
</Note>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Pemecahan masalah penggunaan alat" icon="wrench" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use">
    Perbaiki kesalahan penggunaan alat yang paling umum dengan tabel diagnostik gejala-ke-perbaikan.
  </Card>

  <Card title="Implementasi referensi" icon="github-logo" href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo">
    Mulai dengan implementasi lengkap berbasis Docker
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="tool" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview">
    Hubungkan Claude ke alat dan API eksternal. Lihat di mana alat dieksekusi, kapan Claude memanggilnya, dan alat mana yang cocok untuk tugas Anda.
  </Card>

  <Card title="Praktik terbaik secara detail" icon="book" href="https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude">
    Rekomendasi berbasis benchmark untuk resolusi, upaya thinking, dan manajemen konteks
  </Card>

  <Card title="Alat browser use" icon="browser" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool">
    Biarkan Claude menavigasi, membaca, dan berinteraksi dengan halaman web di lingkungan browser Anda sendiri, untuk tugas yang tetap berada di dalam browser.
  </Card>
</CardGroup>
