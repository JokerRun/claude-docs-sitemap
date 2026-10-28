---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/authentication
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: 10c4f3e214475459e68a3072f8e7b604c48d2426b7f4b81866aeb3ae41db68b2
---

---
title: Autentikasi
url: https://platform.claude.com/docs/id/manage-claude/authentication
description: Autentikasi ke Claude API dengan kunci API, Workload Identity Federation, atau App Attest.
---

Claude API mendukung tiga cara untuk mengautentikasi permintaan:

| Metode                                                                                                                        | Kredensial                                                                                                                           | Paling cocok untuk                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Kunci API](https://platform.claude.com/docs/id/manage-claude/authentication#api-keys)                                        | Rahasia statis `sk-ant-api...` yang dikirim sebagai bearer token di header `Authorization`                                           | Pengembangan lokal, prototyping, skrip, dan server tempat Anda mengontrol penyimpanan rahasia                                                       |
| [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/authentication#workload-identity-federation) | Bearer token berumur pendek yang ditukar dari identity token penyedia identitas Anda                                                 | Beban kerja produksi pada platform cloud (AWS, Google Cloud, Azure), pipeline CI/CD, dan Kubernetes, tempat Anda ingin menghilangkan rahasia statis |
| [App Attest](https://platform.claude.com/docs/id/manage-claude/authentication#app-attest)                                     | Access token berumur pendek yang diterbitkan untuk instalasi asli dan terverifikasi dari aplikasi iOS atau macOS Anda yang terdaftar | Aplikasi iOS dan macOS yang didistribusikan ke pengguna akhir, tempat aplikasi memanggil Claude API secara langsung tanpa back end atau proxy       |

Kunci API dan Workload Identity Federation memberikan akses yang sama ke endpoint Claude API. Pilih kunci API untuk memulai dengan cepat: kunci pribadi untuk pengembangan Anda sendiri, atau kunci akun layanan untuk apa pun yang dibagikan. Beralih ke Workload Identity Federation ketika beban kerja Anda sudah memiliki identitas yang diterbitkan platform yang dapat Anda federasikan. Gunakan App Attest untuk aplikasi iOS dan macOS yang Anda distribusikan ke pengguna akhir.

## Kunci API

Kunci API adalah rahasia statis yang Anda hasilkan di Claude Console dan kirim pada setiap permintaan sebagai bearer token di header `Authorization`.

### Jenis kunci

Saat Anda membuat kunci, Anda memilih jenisnya, yang menentukan apa yang dapat dilakukan kunci, di mana kunci bekerja, dan kapan kunci berhenti bekerja:

| Jenis kunci                 | Bertindak sebagai                                                                                                         | Bekerja di                                                                                                                                                                                                                  | Berhenti bekerja ketika                                                                                                                                                                                                                                                                                                        |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Kunci pribadi**           | Anda, sang pengguna, dengan peran dan izin Anda                                                                           | Satu workspace saja atau workspace tempat peran Anda mengizinkan penggunaan API, dipilih saat kunci dibuat                                                                                                                  | Anda kehilangan akses ke organisasi. Kunci satu workspace juga berhenti berfungsi ketika Anda kehilangan akses ke workspace tersebut atau workspace tersebut diarsipkan. Kunci pribadi diarsipkan ketika Anda dikeluarkan dari organisasi. Jika Anda diundang kembali, buat kunci baru; kunci yang diarsipkan tidak dipulihkan |
| **Kunci service account**   | Sebuah [service account](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#service-accounts) | Satu workspace saja atau apa pun yang dapat diakses oleh service account, dipilih saat kunci dibuat. Service account memiliki akses ke Default Workspace dan ke workspace tempat service account tersebut telah ditambahkan | Service account diarsipkan. Kunci satu workspace juga berhenti berfungsi ketika service account dihapus dari workspace tersebut atau workspace tersebut diarsipkan                                                                                                                                                             |
| **Kunci workspace** (lawas) | Tidak ada: kunci ini milik workspace tempat kunci dibuat                                                                  | Workspace tersebut                                                                                                                                                                                                          | Kunci kedaluwarsa, dinonaktifkan atau dihapus, atau workspace-nya diarsipkan, terlepas dari apakah pembuatnya meninggalkan organisasi                                                                                                                                                                                          |

Kunci pribadi dan kunci service account didukung identitas: masing-masing dimiliki oleh pengguna atau service account yang sudah dikelola organisasi Anda, dan setiap permintaan bertindak sebagai identitas tersebut. Ketika identitas tersebut dikeluarkan dari organisasi, kunci berhenti berfungsi. Artinya, kunci tidak secara tidak sengaja bertahan lebih lama daripada orang atau workload yang memilikinya. Utamakan jenis kunci ini dibandingkan kunci workspace untuk integrasi baru.

Gunakan kunci pribadi untuk pengembangan dan skrip Anda sendiri. Kunci pribadi yang dibagikan bertindak sebagai satu orang dan rusak ketika orang tersebut pergi. Untuk beban kerja yang dibagikan atau otomatis (CI, layanan produksi), minta admin organisasi membuat akun layanan sehingga beban kerja memiliki identitasnya sendiri.

Kunci API workspace masih berfungsi tetapi harus dianggap lawas; kunci yang didukung identitas atau [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) lebih diutamakan. Untuk bermigrasi, lihat [Mengganti kunci API workspace](https://platform.claude.com/docs/id/manage-claude/authentication#replacing-workspace-api-keys).

### Membuat dan menggunakan kunci

* **Membuat kunci:** Di Claude Console, buka halaman [API keys](https://platform.claude.com/settings/keys) (`platform.claude.com/settings/keys`) dan klik **Create key**. Beri nama kunci dan pilih [masa kedaluwarsa](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration). Atur **Linked account** ke diri Anda sendiri untuk kunci pribadi, atau ke service account untuk kunci yang digunakan bersama oleh banyak pengguna. Anda juga dapat membatasi cakupan kunci ke workspace tertentu, sehingga Anda tidak perlu mengatur ID workspace secara manual pada permintaan berikutnya.
* **Menggunakan kunci:** Kirim sebagai `Authorization: Bearer <key>` pada permintaan HTTP langsung, atau atur variabel lingkungan `ANTHROPIC_API_KEY` dan [client SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) akan mengambilnya secara otomatis.

```http
POST /v1/messages
Authorization: Bearer YOUR_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

Header lawas `x-api-key: YOUR_API_KEY` masih didukung sebagai pengganti `Authorization`.

Simpan kunci API di secrets manager, rotasi secara berkala, dan nonaktifkan atau hapus kunci apa pun yang Anda curigai telah bocor. Di halaman [API keys](https://platform.claude.com/settings/keys) pada Claude Console, **Disable** dapat dibatalkan (Admin API melaporkan `status` kunci sebagai `"inactive"`, dan **Re-enable** mengembalikannya ke `"active"`), sedangkan **Delete** bersifat permanen: kunci diarsipkan dan masih muncul di [List API Keys](https://platform.claude.com/docs/id/api/organization/api_keys/list) dengan `status: "archived"`. Kunci yang sudah kedaluwarsa hanya dapat dihapus. Anda juga dapat mengatur [masa kedaluwarsa](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration) saat membuat kunci untuk membatasi berapa lama kredensial yang bocor tetap dapat digunakan.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```bash CLI
  # Lihat /docs/en/cli-sdks-libraries/cli/authentication#api-key untuk varian zsh, bash, dan Windows
  export ANTHROPIC_API_KEY=sk-ant-api03-...
  ```

  ```python Python
  client = Anthropic(api_key="my-anthropic-api-key")
  # atau, dengan ANTHROPIC_API_KEY yang diatur di environment:
  client = Anthropic()
  ```

  ```typescript TypeScript
  const client = new Anthropic({ apiKey: "my-anthropic-api-key" });
  // atau, dengan ANTHROPIC_API_KEY yang diatur di environment:
  // const client = new Anthropic();
  ```

  ```csharp C#
  using Anthropic;

  AnthropicClient client = new() { ApiKey = "my-anthropic-api-key" };
  // Atau, dengan ANTHROPIC_API_KEY diatur di environment:
  // AnthropicClient client = new();
  ```

  ```go Go
  client := anthropic.NewClient(
  	option.WithAPIKey("sk-ant-api03-..."), // defaults to os.LookupEnv("ANTHROPIC_API_KEY")
  )
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;

  // Eksplisit
  AnthropicClient client = AnthropicOkHttpClient.builder()
      .apiKey("my-anthropic-api-key")
      .build();

  // Dari ANTHROPIC_API_KEY (atau properti sistem anthropic.apiKey)
  AnthropicClient clientFromEnv = AnthropicOkHttpClient.fromEnv();
  ```

  ```php PHP
  // Membaca ANTHROPIC_API_KEY dari environment
  $client = new Client();
  // Atau berikan kunci secara eksplisit:
  $client = new Client(apiKey: 'my-anthropic-api-key');
  ```

  ```ruby Ruby
  anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")
  # atau, dengan ANTHROPIC_API_KEY yang diatur di environment:
  anthropic = Anthropic::Client.new
  ```
</CodeGroup>

### Memilih workspace

Kunci API yang dibuat untuk workspace tertentu hanya berfungsi di workspace tersebut, dan permintaan API yang menggunakan kunci ini dapat menghilangkan ID workspace.

Jika kunci API Anda tidak dibatasi ke workspace, Anda harus menentukan ID workspace di header `anthropic-workspace-id` untuk setiap permintaan. Lihat contoh berikut untuk cara mengatur header ini dalam permintaan atau di SDK.

[Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) menerima kunci pribadi atau kunci akun layanan hanya jika kunci tersebut tidak dibatasi cakupannya ke workspace tertentu.

Anda dapat menemukan ID workspace di kolom **ID** pada halaman [Workspaces](https://platform.claude.com/settings/workspaces) (`platform.claude.com/settings/workspaces`) di Claude Console, atau dengan memanggil endpoint [List Workspaces](https://platform.claude.com/docs/id/api/organization/workspaces/list). List Workspaces menyertakan Default Workspace hanya jika Anda meneruskan `include_default=true`; ID-nya juga ada di [header respons](https://platform.claude.com/docs/id/manage-claude/workspaces#identify-the-workspace-behind-an-api-response) `anthropic-workspace-id` dari setiap permintaan yang berjalan di sana.

<CodeGroup>
  ```bash cURL
  # Wajib di setiap permintaan untuk kunci yang tidak dibatasi ke suatu workspace.
  # Hilangkan header anthropic-workspace-id untuk kunci yang dibatasi ke satu workspace.
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-workspace-id: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```bash CLI
  # Wajib pada setiap perintah untuk kunci yang tidak dibatasi ke suatu workspace.
  # Hilangkan --workspace-id untuk kunci yang dibatasi ke satu workspace.
  ant messages create \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  client = Anthropic()  # reads ANTHROPIC_API_KEY

  # Wajib di setiap permintaan untuk kunci yang tidak dibatasi ke satu workspace.
  # Hilangkan extra_headers untuk kunci yang dibatasi ke satu workspace.
  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      extra_headers={"anthropic-workspace-id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"},
  )
  print(message.content)

  # Atau atur sekali untuk setiap permintaan dari klien ini:
  workspace_client = Anthropic(
      default_headers={"anthropic-workspace-id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"},
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic(); // reads ANTHROPIC_API_KEY

  // Wajib di setiap permintaan untuk kunci yang tidak dibatasi ke satu workspace.
  // Hilangkan argumen kedua untuk kunci yang dibatasi ke satu workspace.
  const message = await client.messages.create(
    {
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    },
    { headers: { "anthropic-workspace-id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ" } }
  );
  console.log(message.content);

  // Atau atur sekali untuk setiap permintaan dari klien ini:
  const workspaceClient = new Anthropic({
    defaultHeaders: { "anthropic-workspace-id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ" }
  });
  ```

  ```csharp C#
  AnthropicClient client = new(); // reads ANTHROPIC_API_KEY

  MessageCreateParams parameters = new()
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new UserMessageParam { Content = "Hello, Claude" }],
  };

  // Wajib pada setiap permintaan untuk kunci yang tidak dibatasi pada satu workspace.
  // Panggil client.Messages.Create(parameters) secara langsung untuk kunci yang dibatasi pada satu workspace.
  var message = await client
      .WithOptions(options =>
          options with
          {
              ExtraHeaders = new Dictionary<string, string>
              {
                  ["anthropic-workspace-id"] = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
              },
          }
      )
      .Messages.Create(parameters);
  Console.WriteLine(message);

  // Atau atur sekali untuk setiap permintaan dari client ini:
  AnthropicClient workspaceClient = new(new ClientOptions
  {
      ExtraHeaders = new Dictionary<string, string>
      {
          ["anthropic-workspace-id"] = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      },
  });
  ```

  ```go Go
  client := anthropic.NewClient() // reads ANTHROPIC_API_KEY

  // Wajib di setiap permintaan untuk kunci yang tidak dicakup ke satu workspace.
  // Hilangkan opsi ini untuk kunci yang dicakup ke satu workspace.
  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  }, option.WithHeader("anthropic-workspace-id", "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"))
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message.Content)

  // Atau atur sekali untuk setiap permintaan dari klien ini:
  workspaceClient := anthropic.NewClient(
  	option.WithHeader("anthropic-workspace-id", "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"),
  )
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv(); // reads ANTHROPIC_API_KEY

  // Wajib pada setiap permintaan untuk kunci yang tidak dibatasi ke suatu workspace.
  // Hilangkan putAdditionalHeader untuk kunci yang dibatasi ke satu workspace.
  Message message = client.messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024)
      .addUserMessage("Hello, Claude")
      .putAdditionalHeader("anthropic-workspace-id", "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
      .build());

  IO.println(message.content());

  // Atau atur sekali untuk setiap permintaan dari klien ini:
  AnthropicClient workspaceClient = AnthropicOkHttpClient.builder()
      .fromEnv()
      .putHeader("anthropic-workspace-id", "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
      .build();
  ```

  ```php PHP
  $client = new Client(); // reads ANTHROPIC_API_KEY

  // Diperlukan pada setiap permintaan untuk kunci multi-workspace.
  // Hilangkan requestOptions untuk kunci single-workspace.
  $message = $client->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      requestOptions: [
          'extraHeaders' => ['anthropic-workspace-id' => 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ'],
      ],
  );

  echo json_encode($message->content), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new # reads ANTHROPIC_API_KEY

  # Wajib pada setiap permintaan untuk kunci yang tidak dibatasi pada satu workspace.
  # Hilangkan request_options untuk kunci yang dibatasi pada satu workspace.
  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    request_options: {extra_headers: {"anthropic-workspace-id" => "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"}}
  )

  puts message.content
  ```
</CodeGroup>

Jika permintaan yang dibuat dengan kunci yang tidak dibatasi cakupannya ke workspace menghilangkan header, API mengembalikan 400 `invalid_request_error`:

```json JSON
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "This API key is not scoped to a workspace, so this request must include the anthropic-workspace-id header with the ID of the workspace to use. Add the header, or use an API key that is scoped to a workspace."
  },
  "request_id": "req_011CSHoEeqs5C35K2UUqR7Fy"
}
```

Nilai header yang bukan ID workspace yang valid mengembalikan 400 `invalid_request_error` dengan pesan `anthropic-workspace-id header must be a valid workspace ID.` Jika workspace tidak ada, atau pengguna atau akun layanan kunci tidak memiliki akses ke sana, API mengembalikan 404 `not_found_error` dengan pesan ``Workspace `<id>` not found.``, respons yang sama seperti untuk workspace yang tidak dikenal.

Workload Identity Federation memilih workspace saat pertukaran token sebagai gantinya; lihat [referensi WIF](https://platform.claude.com/docs/id/manage-claude/wif-reference) untuk detailnya.

### Kedaluwarsa kunci

Saat Anda membuat kunci API dari halaman [API keys](https://platform.claude.com/settings/keys) di Claude Console, Anda memilih masa kedaluwarsa: preset (3 jam, 1 hari, 7 hari, atau 30 hari), durasi kustom, atau **Never** untuk kunci yang Anda simpan di secrets manager dan rotasi sendiri. Jika organisasi Anda memiliki kebijakan masa kedaluwarsa maksimum, Console membatasi preset dan durasi kustom hingga batas maksimum kebijakan, dan **Never** tidak tersedia. Kunci yang sudah ada mempertahankan perilakunya saat ini; masa kedaluwarsa diatur saat pembuatan dan tidak dapat diubah setelahnya. Pilihan masa kedaluwarsa yang sama berlaku saat Anda [membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys) di Claude Console.

Anthropic mengirim email kepada pembuat kunci saat kedaluwarsa mendekat: 7 hari sebelum kedaluwarsa untuk kunci yang dibuat dengan masa pakai minimal 14 hari, dan 1 hari sebelumnya untuk kunci dengan masa pakai minimal 7 hari. Kunci dengan masa pakai lebih pendek kedaluwarsa tanpa email peringatan.

Setelah kunci kedaluwarsa, permintaan yang dibuat dengannya mengembalikan `401 authentication_error`. Buat kunci baru untuk memulihkan akses; kunci yang kedaluwarsa tidak dapat diaktifkan kembali.

Tabel kunci API di Console menampilkan masa kedaluwarsa setiap kunci, dan Admin API melaporkan timestamp `expires_at` setiap kunci pada endpoint [List API Keys](https://platform.claude.com/docs/id/api/organization/api_keys/list) dan [Retrieve API Key](https://platform.claude.com/docs/id/api/organization/api_keys/retrieve), sehingga Anda dapat mengaudit dan merotasi kunci sebelum kedaluwarsa. Field ini bernilai `null` untuk kunci tanpa masa kedaluwarsa.

Kedaluwarsa membatasi masa pakai kredensial yang bocor, tetapi bukan pengganti kebersihan rahasia. Terlepas dari kedaluwarsa, simpan kunci di secrets manager dan nonaktifkan atau hapus kunci apa pun yang Anda curigai telah bocor.

### Mengganti kunci API workspace

Jika Anda memiliki kunci workspace, Anda mungkin ingin menggantinya dengan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/wif-reference) atau kunci pribadi atau akun layanan. Ini memberikan keamanan dan observabilitas yang lebih baik.

Lihat [referensi WIF](https://platform.claude.com/docs/id/manage-claude/wif-reference) untuk detail tentang mengonfigurasi Workload Identity Federation, yang lebih diutamakan dibandingkan kunci berumur panjang.

Untuk mengganti kunci workspace dengan kunci pribadi atau akun layanan:

1. **Tentukan jenis kunci.** Perkakas Anda sendiri harus menggunakan kunci pribadi. Beban kerja yang dibagikan atau tanpa pengawasan harus menggunakan kunci akun layanan.
2. **Buat service account** jika diperlukan. Anda mungkin harus meminta admin organisasi untuk membuatnya di halaman [Service accounts](https://platform.claude.com/settings/service-accounts) (`platform.claude.com/settings/service-accounts`) di Claude Console dan menambahkannya ke workspace yang relevan.
3. **Buat kunci baru.** Buat kunci tersebut khusus untuk workspace integrasi kecuali integrasi memerlukan beberapa workspace.
4. **Terapkan kunci baru.** Ganti kunci lama di mana pun integrasi membacanya, biasanya variabel lingkungan `ANTHROPIC_API_KEY` atau entri secrets manager. Untuk kunci yang tidak dibatasi ke workspace, kirim juga header `anthropic-workspace-id` seperti yang ditunjukkan di [Memilih workspace](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace).
5. **Hapus kunci lama.** Pastikan permintaan berhasil, lalu hapus kunci workspace di [halaman kunci API](https://platform.claude.com/settings/keys) di Claude Console.

## Workload Identity Federation

Workload Identity Federation (WIF) memungkinkan workload melakukan autentikasi dengan identity token berumur pendek yang diterbitkan oleh “identity provider” (penyedia identitas), atau IdP, yang sudah Anda percayai. IdP tersebut meliputi AWS IAM, Google Cloud, dan penerbit OIDC apa pun yang mematuhi standar (seperti GitHub Actions, service account Kubernetes, SPIFFE, Microsoft Entra ID, atau Okta). Workload menukar JWT yang diterbitkan IdP-nya di `POST /v1/oauth/token` dengan access token Claude API berumur pendek, dan SDK memperbarui token tersebut secara otomatis sebelum kedaluwarsa. Tidak ada string `sk-ant-api...` yang perlu dibuat, didistribusikan, atau dirotasi.

Federasi menghilangkan kunci Claude API berumur panjang dari lingkungan Anda, yang membatasi kerusakan yang dapat ditimbulkan oleh kredensial yang bocor dan memungkinkan Anda mengelola akses dengan kontrol IdP yang sama yang sudah Anda gunakan untuk sumber daya cloud. Federasi sendiri tidak menjamin keamanan end-to-end: rantai kepercayaan hanya sekuat konfigurasi penyedia identitas Anda, dan secret berumur panjang satu langkah lebih awal dalam rantai tersebut (misalnya, kredensial cloud statis yang dapat membuat token IdP) masih dapat melemahkannya. Padukan federasi dengan kontrol dari penyedia Anda, seperti allowlist IP, MFA, dan audit logging.

Untuk mengonfigurasi federasi, Anda membuat tiga sumber daya di Claude Console (akun layanan, penerbit federasi, dan aturan federasi) lalu mengarahkan SDK Anda ke aturan tersebut. Lihat [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) untuk panduan pengaturan lengkap.

## App Attest

App Attest mengautentikasi aplikasi iOS dan macOS yang memanggil Claude API langsung dari perangkat. Setiap instalasi membuktikan bahwa instalasi tersebut merupakan build asli dan tidak dimodifikasi dari aplikasi yang Anda daftarkan di Claude Console, menggunakan layanan App Attest dari Apple. Anthropic kemudian menerbitkan access token berumur pendek untuk perangkat tersebut yang menagihkan penggunaan ke workspace Anda. Token dibatasi ke workspace Anda, kedaluwarsa setelah 1 jam, dan hanya mengotorisasi panggilan [Messages API](https://platform.claude.com/docs/id/api/messages/create).

Untuk mendaftarkan aplikasi Anda dan mendapatkan client ID, lihat [App Attest untuk aplikasi iOS dan macOS](https://platform.claude.com/docs/id/manage-claude/app-attest).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Siapkan Workload Identity Federation" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/workload-identity-federation">
    Konfigurasikan penerbit, aturan, dan akun layanan, lalu tukar token
  </Card>

  <Card title="Panduan penyedia identitas" icon="cloud" href="https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#identity-providers">
    Panduan langkah demi langkah untuk AWS, Google Cloud, Azure, GitHub Actions, Kubernetes, SPIFFE, dan Okta
  </Card>

  <Card title="Referensi WIF" icon="book" href="https://platform.claude.com/docs/id/manage-claude/wif-reference">
    Variabel lingkungan, aturan validasi, konfigurasi profil, dan referensi kesalahan
  </Card>

  <Card title="App Attest untuk aplikasi iOS dan macOS" icon="fingerprint" href="https://platform.claude.com/docs/id/manage-claude/app-attest">
    Biarkan instalasi asli aplikasi Anda memanggil Claude API tanpa mengirimkan kunci API
  </Card>

  <Card title="SDK klien" icon="code" href="https://platform.claude.com/docs/id/cli-sdks-libraries/overview">
    Python, TypeScript, C#, Go, Java, PHP, Ruby, dan CLI
  </Card>
</CardGroup>
