---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: fa496a803e21ea07d83f7488b1b4fea395b9bf8cdf92032ef4bf761cbf9bbb2d
---

# Pesan sistem di tengah percakapan

Tambahkan atau perbarui instruksi sistem di tengah percakapan tanpa membatalkan prefix yang sudah di-cache sebelumnya.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

Instruksi sistem biasanya berada di field `system` tingkat atas, sebelum setiap pesan dalam percakapan. Posisi itu sangat baik untuk [prompt caching](/docs/id/build-with-claude/prompt-caching) (caching prompt): prompt sistem adalah bagian dari prefix yang stabil, sehingga giliran-giliran berikutnya mendapatkan cache hit. Namun posisi itu buruk untuk instruksi yang baru Anda sadari diperlukan di tengah sesi, karena mengedit field `system` tingkat atas mengubah bagian paling awal dari prompt dan membatalkan cache untuk semua yang mengikutinya.

Pesan sistem di tengah percakapan menutup celah tersebut. Anda menambahkan pesan `{"role": "system"}` pada titik dalam percakapan di mana instruksi baru menjadi relevan, alih-alih mengedit field `system` tingkat atas. Prefix yang di-cache tetap sama, sehingga permintaan berikutnya masih membacanya dari cache, dan instruksi baru tetap diterapkan sebagai instruksi sistem, bukan sebagai teks pengguna biasa.

<Note>
  Pesan sistem di tengah percakapan tersedia di Claude API, [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), dan [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai).

  Fitur ini tersedia di Claude Fable 5, [Claude Mythos 5](https://anthropic.com/glasswing), dan Claude Opus 4.8. Tidak diperlukan header beta. Fitur ini tidak tersedia di Claude Sonnet 5; gunakan field `system` tingkat atas sebagai gantinya.
</Note>

## Kapan menggunakan pesan sistem di tengah percakapan

[Prompt caching](/docs/id/build-with-claude/prompt-caching) melakukan hash terhadap prefix permintaan secara berurutan: `tools`, lalu `system`, lalu `messages`. Cache hit mengharuskan prefix cocok persis dengan permintaan terbaru, byte demi byte, hingga breakpoint cache.

Urutan tersebut berarti field `system` tingkat atas berada di dekat bagian paling awal dari prefix yang di-hash. Perubahan apa pun padanya, bahkan menambahkan satu kalimat, menghasilkan hash yang berbeda, dan permintaan tersebut gagal mendapatkan cache untuk prompt sistem dan setiap pesan yang di-cache setelahnya.

Pesan sistem di tengah percakapan memungkinkan Anda menambahkan instruksi di **akhir** riwayat pesan sebagai gantinya. Semua yang ada sebelum instruksi baru tidak berubah, sehingga entri cache yang ada masih cocok, dan hanya pesan baru yang diproses sebagai input baru.

Beberapa situasi di mana hal ini penting:

* **Perubahan kebijakan atau persona di tengah sesi.** Sesi agentik yang panjang memerlukan batasan baru ("mulai sekarang, tulis semua SQL sebagai parameterized query") setelah puluhan giliran yang sudah di-cache. Menambahkannya ke field `system` tingkat atas akan memproses ulang seluruh riwayat.
* **Konteks per giliran yang harus bersifat otoritatif.** Anda ingin menyisipkan catatan kesegaran data, tenggat waktu sesi, atau perubahan ketersediaan alat dengan bobot tingkat sistem, dan hal itu terlalu sering berubah untuk ditempatkan di prefix yang di-cache.
* **Perubahan status yang diamati aplikasi Anda.** Aplikasi Anda mendeteksi sesuatu yang harus diperlakukan Claude sebagai fakta tingkat operator: file berubah di disk, pengguna mengaktifkan pengaturan auto-approve, alat yang tersedia berubah, atau sisa anggaran token turun di bawah ambang batas.
* **Input pengguna yang tidak boleh menginterupsi loop agentik.** Pengguna mengetik tindak lanjut saat Claude masih mengeksekusi alat untuk permintaan sebelumnya. Meneruskannya sebagai pesan sistem setelah hasil alat berikutnya memungkinkan Claude memasukkan input baru ke dalam pekerjaan yang sedang dilakukannya, alih-alih memperlakukannya sebagai permintaan baru untuk beralih. Lihat [Penempatan setelah hasil alat](#placement-after-tool-results) di bawah.
* **Peralihan mode yang memberikan izin tetap.** Mode tingkat sesi dapat menggunakan pesan sistem di tengah percakapan untuk memberikan persetujuan tetap terhadap kemampuan yang mahal, seperti meluncurkan alur kerja multiagen secara otomatis, dengan pengingat singkat setiap beberapa giliran dan pemberitahuan keluar saat mode dimatikan. Untuk contoh lengkap, lihat [Membangun mode orkestrasi](/docs/id/build-with-claude/mid-conversation-effort-example).

Dalam semua kasus ini Anda bisa saja menempatkan instruksi dalam pesan `user` biasa, dan Claude memang mengikuti instruksi yang datang dalam giliran pengguna. Perbedaannya adalah prioritas: pesan `user` diperlakukan sebagai berasal dari pengguna akhir, sedangkan pesan `system` diperlakukan sebagai berasal dari Anda, operator aplikasi. Ketika keduanya bertentangan, instruksi sistem lebih diutamakan, jadi gunakan role `system` untuk fakta dan batasan tingkat operator yang harus tetap berlaku bahkan jika pengguna akhir meminta sesuatu yang berbeda. Pesan sistem di tengah percakapan mempertahankan prioritas tingkat operator tersebut tanpa membayar biaya cache miss akibat mengedit field `system` tingkat atas.

## Cara kerjanya

Tambahkan pesan dengan `"role": "system"` ke array `messages`. Gunakan string biasa atau blok konten untuk `content`, sama seperti giliran `user` atau `assistant`. Instruksi berlaku mulai dari titik tersebut dalam percakapan dan seterusnya. Ketika instruksi bertentangan, pesan sistem yang lebih baru lebih diutamakan daripada yang lebih lama, dan pesan sistem di tengah percakapan lebih diutamakan daripada field `system` tingkat atas untuk giliran-giliran yang mengikutinya.

Anda tetap dapat mengatur field `system` tingkat atas untuk instruksi yang harus berlaku pada seluruh percakapan. Cadangkan pesan sistem di tengah percakapan untuk instruksi yang baru menjadi relevan belakangan, atau yang ingin Anda tambahkan tanpa membatalkan prefix yang di-cache.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "cache_control": {"type": "ephemeral"},
      "system": "You are a code review assistant. Be concise.",
      "messages": [
        {
          "role": "user",
          "content": "Review process() in utils.py for performance issues."
        },
        {
          "role": "assistant",
          "content": "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list."
        },
        {
          "role": "user",
          "content": "Now review the calling code that invokes process()."
        },
        {
          "role": "system",
          "content": "From now on, every suggestion must include explicit type annotations."
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create --transform 'content.0.text' --raw-output <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  cache_control:
    type: ephemeral
  system: You are a code review assistant. Be concise.
  messages:
    - role: user
      content: Review process() in utils.py for performance issues.
    - role: assistant
      content: >-
        The list comprehension is fine for small inputs. For large inputs,
        consider a generator to avoid materializing the full list.
    - role: user
      content: Now review the calling code that invokes process().
    - role: system
      content: From now on, every suggestion must include explicit type annotations.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      # Caching prompt otomatis: setiap permintaan menyimpan percakapan sejauh ini ke cache,
      # dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
      cache_control={"type": "ephemeral"},
      system="You are a code review assistant. Be concise.",
      messages=[
          {
              "role": "user",
              "content": "Review process() in utils.py for performance issues.",
          },
          {
              "role": "assistant",
              "content": "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.",
          },
          {
              "role": "user",
              "content": "Now review the calling code that invokes process().",
          },
          # Peninjau menyadari di tengah sesi bahwa semua saran harus
          # juga lolos kebijakan typing ketat dari tim. Menambahkan
          # instruksi di sini menjaga giliran-giliran sebelumnya tetap identik byte demi byte, sehingga
          # prefiks yang di-cache oleh permintaan sebelumnya masih dibaca dari cache.
          {
              "role": "system",
              "content": "From now on, every suggestion must include explicit type annotations.",
          },
      ],
  )

  print(response.content[0].text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    // Caching prompt otomatis: setiap permintaan meng-cache percakapan sejauh ini,
    // dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
    cache_control: { type: "ephemeral" },
    system: "You are a code review assistant. Be concise.",
    messages: [
      {
        role: "user",
        content: "Review process() in utils.py for performance issues."
      },
      {
        role: "assistant",
        content:
          "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list."
      },
      {
        role: "user",
        content: "Now review the calling code that invokes process()."
      },
      // Peninjau menyadari di tengah sesi bahwa semua saran juga harus lolos
      // kebijakan typing ketat tim. Menambahkan instruksi di sini menjaga
      // giliran-giliran sebelumnya tetap identik byte demi byte, sehingga prefiks yang di-cache oleh
      // permintaan sebelumnya masih dibaca dari cache.
      {
        role: "system",
        content: "From now on, every suggestion must include explicit type annotations."
      }
    ]
  });

  const textBlock = response.content.find(
    (block): block is Anthropic.TextBlock => block.type === "text"
  );
  console.log(textBlock?.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      // Caching prompt otomatis: setiap permintaan meng-cache percakapan sejauh ini,
      // dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
      CacheControl = new CacheControlEphemeral(),
      System = "You are a code review assistant. Be concise.",
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = "Review process() in utils.py for performance issues."
          },
          new()
          {
              Role = Role.Assistant,
              Content = "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list."
          },
          new()
          {
              Role = Role.User,
              Content = "Now review the calling code that invokes process()."
          },
          // Peninjau menyadari di tengah sesi bahwa semua saran juga harus lolos
          // kebijakan typing ketat tim. Menambahkan instruksi di sini menjaga
          // giliran-giliran sebelumnya tetap identik byte demi byte, sehingga prefiks yang di-cache
          // oleh permintaan sebelumnya masih dibaca dari cache.
          new()
          {
              Role = Role.System,
              Content = "From now on, every suggestion must include explicit type annotations."
          }
      ]
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	// Caching prompt otomatis: setiap permintaan menyimpan percakapan sejauh ini ke cache,
  	// dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
  	CacheControl: anthropic.NewCacheControlEphemeralParam(),
  	System: []anthropic.TextBlockParam{
  		{Text: "You are a code review assistant. Be concise."},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Review process() in utils.py for performance issues.")),
  		anthropic.NewAssistantMessage(anthropic.NewTextBlock("The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.")),
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Now review the calling code that invokes process().")),
  		// Peninjau menyadari di tengah sesi bahwa semua saran juga harus
  		// lolos kebijakan typing ketat tim. Menambahkan instruksi
  		// di sini menjaga giliran sebelumnya tetap identik byte demi byte, sehingga prefiks yang di-cache
  		// oleh permintaan sebelumnya masih dibaca dari cache.
  		{
  			Role: anthropic.MessageParamRoleSystem,
  			Content: []anthropic.ContentBlockParamUnion{
  				anthropic.NewTextBlock("From now on, every suggestion must include explicit type annotations."),
  			},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content[0].Text)
  ```

  ```java Java
  import com.anthropic.models.messages.CacheControlEphemeral;
  // ...
  import com.anthropic.models.messages.MessageParam;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          // Caching prompt otomatis: setiap permintaan menyimpan percakapan sejauh ini ke cache,
          // dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
          .cacheControl(CacheControlEphemeral.builder().build())
          .system("You are a code review assistant. Be concise.")
          .addUserMessage("Review process() in utils.py for performance issues.")
          .addAssistantMessage("The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.")
          .addUserMessage("Now review the calling code that invokes process().")
          // Peninjau menyadari di tengah sesi bahwa semua saran juga harus lolos
          // kebijakan typing ketat tim. Menambahkan instruksi di sini menjaga
          // giliran-giliran sebelumnya tetap identik byte demi byte, sehingga prefiks yang di-cache oleh
          // permintaan sebelumnya masih dibaca dari cache.
          .addMessage(MessageParam.builder()
              .role(MessageParam.Role.SYSTEM)
              .content("From now on, every suggestion must include explicit type annotations.")
              .build())
          .build();

      Message response = client.messages().create(params);
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> System.out.println(textBlock.text()));
  ```

  ```php PHP
  use Anthropic\Messages\CacheControlEphemeral;
  // ...
  $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Review process() in utils.py for performance issues.'],
          ['role' => 'assistant', 'content' => 'The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.'],
          ['role' => 'user', 'content' => 'Now review the calling code that invokes process().'],
          // Peninjau menyadari di tengah sesi bahwa semua saran juga harus
          // memenuhi kebijakan typing ketat tim. Menambahkan instruksi di sini
          // menjaga giliran sebelumnya tetap identik byte demi byte, sehingga prefix
          // yang di-cache oleh permintaan sebelumnya masih dibaca dari cache.
          ['role' => 'system', 'content' => 'From now on, every suggestion must include explicit type annotations.']
      ],
      model: 'claude-opus-4-8',
      // Caching prompt otomatis: setiap permintaan meng-cache percakapan sejauh ini,
      // dan permintaan berikutnya membaca prefix yang tidak berubah dari cache.
      cacheControl: CacheControlEphemeral::with(),
      system: 'You are a code review assistant. Be concise.',
  );

  echo $response->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    # Caching prompt otomatis: setiap permintaan menyimpan percakapan sejauh ini ke cache,
    # dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
    cache_control: { type: "ephemeral" },
    system: "You are a code review assistant. Be concise.",
    messages: [
      { role: "user", content: "Review process() in utils.py for performance issues." },
      { role: "assistant", content: "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list." },
      { role: "user", content: "Now review the calling code that invokes process()." },
      # Peninjau menyadari di tengah sesi bahwa semua saran juga harus lolos
      # kebijakan typing ketat tim. Menambahkan instruksi di sini menjaga
      # giliran-giliran sebelumnya tetap identik byte demi byte, sehingga prefiks yang di-cache oleh
      # permintaan sebelumnya masih dibaca dari cache.
      { role: "system", content: "From now on, every suggestion must include explicit type annotations." }
    ]
  )

  puts response.content.first.text
  ```
</CodeGroup>

Contoh ini mengaktifkan [caching otomatis](/docs/id/build-with-claude/prompt-caching#automatic-caching) dengan field `cache_control` tingkat atas. Caching prompt bersifat opt-in: jika permintaan tidak memiliki field `cache_control` (otomatis atau [breakpoint eksplisit](/docs/id/build-with-claude/prompt-caching#explicit-cache-breakpoints)), tidak ada yang di-cache dan setiap permintaan membayar harga token input reguler untuk seluruh percakapan. Dengan caching diaktifkan, menambahkan pesan sistem membiarkan giliran-giliran yang sudah di-cache tidak berubah, sehingga permintaan yang membawa instruksi baru masih membacanya dari cache alih-alih memprosesnya lagi. Caching juga mengharuskan percakapan memenuhi [panjang prompt minimum yang dapat di-cache](/docs/id/build-with-claude/prompt-caching#cache-limitations); contoh sependek ini berada di bawahnya, sehingga `cache_creation_input_tokens` dan `cache_read_input_tokens` tetap 0 sampai percakapan bertambah panjang.

Pesan sistem di tengah percakapan harus langsung mengikuti giliran `user` (atau giliran `assistant` yang diakhiri dengan hasil alat server), dan harus menjadi entri terakhir dalam `messages` atau langsung diikuti oleh giliran `assistant`. Pesan `user` yang membawa blok `tool_result` juga dihitung: dalam loop agentik Anda dapat menempatkan pesan sistem tepat setelah hasil alat, sebelum giliran Claude berikutnya. Posisi lain mana pun, termasuk di antara blok `tool_use` milik `assistant` dan `tool_result` yang menjawabnya, mengembalikan error 400.

### Penempatan setelah hasil alat

Dalam [loop agentik](/docs/id/agents-and-tools/tool-use/overview), pesan sistem ditempatkan setelah pesan `user` yang menyampaikan hasil alat. Di sinilah juga aplikasi Anda dapat meneruskan input yang diketik pengguna saat Claude sedang bekerja, sehingga konteks baru diserap tanpa memulai ulang giliran:

```json
[
  { "role": "user", "content": "Run the test suite and fix any failures." },
  {
    "role": "assistant",
    "content": [{ "type": "tool_use", "id": "toolu_01", "name": "run_tests", "input": {} }]
  },
  {
    "role": "user",
    "content": [
      { "type": "tool_result", "tool_use_id": "toolu_01", "content": "12 passed, 0 failed" }
    ]
  },
  {
    "role": "system",
    "content": "The user sent the following message while you were working: also update the changelog before you finish."
  }
]
```

Susun konten sistem sebagai konteks, bukan sebagai perintah yang menimpa pengguna. Nyatakan faktanya ("input baru datang dari pengguna: X", "sisa anggaran token sekarang adalah Y") dan biarkan Claude bertindak berdasarkan itu. Claude dilatih untuk menolak instruksi yang tampak bekerja melawan pengguna, dan perlindungan itu tetap berlaku untuk role sistem, sehingga bahasa seperti "abaikan apa yang dikatakan pengguna" kurang efektif dibandingkan menyatakan apa yang berubah.

Pola ini untuk meneruskan input dari pengguna akhir percakapan itu sendiri. Jangan gunakan untuk meneruskan output alat, dokumen yang diambil, atau konten pihak ketiga lainnya; simpan konten tersebut dalam blok `tool_result` (lihat [Keterbatasan](#limitations)).

## Menggabungkan dengan caching prompt

Pesan sistem di tengah percakapan dan [prompt caching](/docs/id/build-with-claude/prompt-caching) (caching prompt) dirancang untuk digunakan bersama:

* **Aktifkan caching secara eksplisit.** Caching hanya terjadi ketika permintaan menyertakan `cache_control`, baik field [caching otomatis](/docs/id/build-with-claude/prompt-caching#automatic-caching) tingkat atas maupun [breakpoint eksplisit](/docs/id/build-with-claude/prompt-caching#explicit-cache-breakpoints) pada blok konten. Pesan sistem di tengah percakapan tidak membuat entri cache dengan sendirinya, dan tanpa caching diaktifkan tidak ada penghematan yang perlu dipertahankan.
* **Cache prefix yang stabil seperti biasa.** Tempatkan `cache_control` pada blok terakhir yang tetap sama di seluruh permintaan, baik itu akhir dari field `system` tingkat atas, akhir dari definisi alat Anda, atau titik yang stabil dalam riwayat pesan.
* **Tambahkan pesan sistem setelah breakpoint.** Karena berada setelah prefix yang di-cache, pesan tersebut tidak mengubah hash prefix dan cache tetap mendapatkan hit.
* **Pesan sistem di tengah percakapan itu sendiri dapat di-cache.** Setelah berada dalam percakapan, pesan tersebut menjadi bagian dari riwayat yang stabil. Pada giliran berikutnya Anda dapat memindahkan breakpoint cache Anda melewatinya (atau mengandalkan [caching otomatis](/docs/id/build-with-claude/prompt-caching#automatic-caching) untuk melakukannya) dan pesan sistem dibaca dari cache seperti giliran lainnya.

Hindari mengedit atau menghapus pesan sistem di tengah percakapan yang sudah dikirim. Seperti perubahan lain pada pesan-pesan sebelumnya, hal itu membatalkan cache mulai dari titik tersebut dan seterusnya. Jika instruksi perlu berkembang, tambahkan pesan sistem baru alih-alih menulis ulang yang lama. Pesan sistem yang berurutan diterima dan diperlakukan sebagai satu bagian sistem, yang mengikuti aturan penempatan yang sama secara keseluruhan.

## Keterbatasan

* **Bukan untuk pesan pertama.** Pesan `system` tidak dapat menjadi entri pertama dalam `messages`. Gunakan field `system` tingkat atas untuk instruksi yang berlaku sejak awal.
* **Penempatan dibatasi.** Pesan `system` harus langsung mengikuti giliran `user` (termasuk giliran `user` yang membawa blok `tool_result`) atau giliran `assistant` yang diakhiri dengan hasil alat server, dan harus mendahului giliran `assistant` atau mengakhiri array. Pesan tersebut tidak dapat berada di antara blok `tool_use` dan `tool_result`-nya. Menempatkannya di tempat lain mengembalikan error 400.
* **Bukan tempat untuk konten yang tidak tepercaya.** Claude memperlakukan konten sistem sebagai instruksi operator dan mengikutinya. Jangan menempatkan teks dari luar percakapan, seperti output alat mentah, dokumen yang diambil, atau konten web, langsung dalam pesan sistem; melakukan hal itu memberikan teks tersebut otoritas tingkat operator. Simpan data tersebut dalam blok `tool_result` dan tetap ikuti [Mitigasi jailbreak dan injeksi prompt](/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks).

## Terkait

<CardGroup cols={2}>
  <Card title="Caching prompt" icon="bolt" href="/docs/id/build-with-claude/prompt-caching">
    Cara kerja caching, di mana menempatkan breakpoint, dan cara membaca field penggunaan cache.
  </Card>

  <Card title="Diagnostik cache" icon="magnifying-glass" href="/docs/id/build-with-claude/cache-diagnostics">
    Temukan dengan tepat di mana dua permintaan berbeda ketika cache hit yang Anda harapkan tidak terjadi.
  </Card>

  <Card title="Menggunakan Messages API" icon="message" href="/docs/id/build-with-claude/working-with-messages">
    Struktur pesan, percakapan multi-giliran, dan field `system`.
  </Card>

  <Card title="Praktik terbaik prompting" icon="text" href="/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    Menulis prompt dan instruksi sistem yang efektif.
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="wrench" href="/docs/id/agents-and-tools/tool-use/overview">
    Bagaimana blok `tool_use` dan `tool_result` disusun dalam array `messages`.
  </Card>
</CardGroup>
