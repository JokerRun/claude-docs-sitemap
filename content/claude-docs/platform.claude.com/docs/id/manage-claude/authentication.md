---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/authentication
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: c1e9644fda74684afc13c3686eb7ccd16b7eac063fb8d3b86b3ec4a7488cbec1
---

---
title: Autentikasi
url: https://platform.claude.com/docs/id/manage-claude/authentication
description: Lakukan autentikasi ke Claude API dengan kunci API, Workload Identity Federation, atau App Attest.
---

Claude API mendukung tiga cara untuk mengautentikasi permintaan:

| Metode                                                                                                                        | Kredensial                                                                                                                        | Paling cocok untuk                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Kunci API](https://platform.claude.com/docs/id/manage-claude/authentication#api-keys)                                        | Rahasia statis `sk-ant-api...` di header `x-api-key`                                                                              | Pengembangan lokal, pembuatan prototipe, skrip, dan server tempat Anda mengontrol penyimpanan rahasia                                             |
| [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/authentication#workload-identity-federation) | Bearer token berumur pendek yang ditukar dari token identitas penyedia identitas Anda                                             | Beban kerja produksi di platform cloud (AWS, Google Cloud, Azure), pipeline CI/CD, dan Kubernetes, tempat Anda ingin menghilangkan rahasia statis |
| [App Attest](https://platform.claude.com/docs/id/manage-claude/authentication#app-attest)                                     | Token akses berumur pendek yang diterbitkan untuk instalasi asli dan teratestasi dari aplikasi iOS atau macOS Anda yang terdaftar | Aplikasi iOS dan macOS yang didistribusikan ke pengguna akhir, tempat aplikasi memanggil Claude API secara langsung tanpa back end atau proxy     |

Kunci API dan Workload Identity Federation memberikan akses yang sama ke endpoint Claude API. Pilih kunci API untuk memulai dengan cepat: kunci pribadi untuk pengembangan Anda sendiri, atau kunci akun layanan untuk apa pun yang dibagikan. Beralihlah ke Workload Identity Federation ketika beban kerja Anda sudah memiliki identitas yang diterbitkan platform yang dapat Anda federasikan. Gunakan App Attest untuk aplikasi iOS dan macOS yang Anda distribusikan ke pengguna akhir.

## Kunci API

"API key" (kunci API) adalah rahasia statis yang Anda buat di Claude Console dan kirimkan pada setiap permintaan di header `x-api-key`.

### Jenis kunci

Saat Anda membuat kunci, Anda memilih jenisnya, yang menentukan apa yang dapat dilakukan kunci tersebut, di mana kunci tersebut berfungsi, dan kapan kunci tersebut berhenti berfungsi:

| Jenis kunci                  | Bertindak sebagai                                                                                                      | Berfungsi di                                                                                                                                                                                               | Berhenti berfungsi ketika                                                                                                                                                                                                                         |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Kunci pribadi**            | Anda, sang pengguna, dengan peran dan izin Anda                                                                        | Satu workspace saja atau workspace tempat peran Anda mengizinkan penggunaan API, dipilih saat kunci dibuat                                                                                                 | Anda kehilangan akses ke organisasi atau, untuk kunci workspace tunggal, ke workspace tersebut. Kunci pribadi diarsipkan ketika Anda dihapus dari organisasi. Jika Anda diundang kembali, buat kunci baru; kunci yang diarsipkan tidak dipulihkan |
| **Kunci akun layanan**       | Sebuah [akun layanan](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#service-accounts) | Satu workspace saja atau apa pun yang dapat diakses oleh akun layanan, dipilih saat kunci dibuat. Akun layanan memiliki akses ke Default Workspace dan ke workspace tempat akun tersebut telah ditambahkan | Akun layanan diarsipkan atau, untuk kunci workspace tunggal, dihapus dari workspace tersebut                                                                                                                                                      |
| **Kunci workspace** (legacy) | Tidak seorang pun: kunci ini milik workspace tempat kunci tersebut dibuat                                              | Workspace tersebut                                                                                                                                                                                         | Kunci kedaluwarsa, dinonaktifkan atau dihapus, atau workspace-nya diarsipkan, terlepas dari apakah pembuatnya meninggalkan organisasi                                                                                                             |

Kunci pribadi dan kunci akun layanan didukung oleh identitas: masing-masing milik pengguna atau akun layanan yang sudah dikelola organisasi Anda, dan setiap permintaan bertindak sebagai identitas tersebut. Ketika identitas tersebut dihapus dari organisasi, kunci berhenti berfungsi. Ini berarti kunci tidak akan secara tidak sengaja bertahan lebih lama daripada orang atau beban kerja yang memilikinya. Utamakan kunci ini daripada kunci workspace untuk integrasi baru.

Gunakan kunci pribadi untuk pengembangan dan skrip Anda sendiri. Kunci pribadi yang dibagikan bertindak sebagai satu orang dan rusak ketika orang tersebut pergi. Untuk beban kerja bersama atau otomatis (CI, layanan produksi), mintalah admin organisasi membuat akun layanan agar beban kerja memiliki identitasnya sendiri.

Kunci API workspace masih berfungsi tetapi sebaiknya dianggap legacy; kunci yang didukung identitas atau [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) lebih diutamakan. Untuk bermigrasi, lihat [Mengganti kunci API workspace](https://platform.claude.com/docs/id/manage-claude/authentication#replacing-workspace-api-keys).

### Membuat dan menggunakan kunci

* **Buat kunci:** Buka [Settings → API keys](https://platform.claude.com/settings/keys) di Claude Console dan klik **Create key**. Beri nama kunci dan pilih [kedaluwarsa](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration). Atur **Linked account** ke diri Anda sendiri untuk kunci pribadi, atau ke akun layanan untuk kunci yang dibagikan ke beberapa pengguna. Anda juga dapat membatasi cakupan kunci ke workspace tertentu, yang memungkinkan Anda melewati pengaturan ID workspace secara manual pada permintaan berikutnya.
* **Gunakan kunci:** Atur header `x-api-key` pada permintaan HTTP langsung, atau atur variabel lingkungan `ANTHROPIC_API_KEY` dan [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) akan mengambilnya secara otomatis.

```http
POST /v1/messages
x-api-key: YOUR_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

Simpan kunci API di pengelola rahasia, rotasi secara berkala, dan nonaktifkan atau hapus kunci apa pun yang Anda curigai telah bocor. Di [halaman API keys](https://platform.claude.com/settings/keys), **Disable** dapat dibatalkan (Admin API melaporkan `status` kunci sebagai `"inactive"`, dan **Re-enable** mengembalikannya ke `"active"`), sedangkan **Delete** bersifat permanen: kunci diarsipkan dan masih muncul di [List API Keys](https://platform.claude.com/docs/id/api/admin/api_keys/list) dengan `status: "archived"`. Kunci yang kedaluwarsa hanya dapat dihapus. Anda juga dapat mengatur [kedaluwarsa](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration) saat membuat kunci untuk membatasi berapa lama kredensial yang bocor tetap dapat digunakan.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```python Python
  client = Anthropic(api_key="my-anthropic-api-key")
  # atau, dengan ANTHROPIC_API_KEY diatur di environment:
  client = Anthropic()
  ```

  ```typescript TypeScript
  const client = new Anthropic({ apiKey: "my-anthropic-api-key" });
  // atau, dengan ANTHROPIC_API_KEY diatur di environment:
  // const client = new Anthropic();
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

  ```csharp C#
  using Anthropic;

  AnthropicClient client = new() { ApiKey = "my-anthropic-api-key" };
  // Atau, dengan ANTHROPIC_API_KEY yang diatur di environment:
  // AnthropicClient client = new();
  ```

  ```php PHP
  // Membaca ANTHROPIC_API_KEY dari environment
  $client = new Client();
  // Atau teruskan kunci secara eksplisit:
  $client = new Client(apiKey: 'my-anthropic-api-key');
  ```

  ```ruby Ruby
  anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")
  # atau, dengan ANTHROPIC_API_KEY diatur di environment:
  anthropic = Anthropic::Client.new
  ```

  ```bash CLI
  # Lihat /docs/en/cli-sdks-libraries/cli/authentication#api-key untuk varian zsh, bash, dan Windows
  export ANTHROPIC_API_KEY=sk-ant-api03-...
  ```
</CodeGroup>

### Memilih workspace

Kunci API yang dibuat untuk workspace tertentu hanya berfungsi di workspace tersebut, dan permintaan API yang menggunakan kunci ini dapat menghilangkan ID workspace.

Jika kunci API Anda tidak dibatasi cakupannya ke suatu workspace, Anda harus menentukan ID workspace di header `anthropic-workspace-id` untuk setiap permintaan. Lihat contoh berikut untuk cara mengatur header ini dalam permintaan atau di SDK.

[Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) menerima kunci pribadi atau kunci akun layanan hanya jika kunci tersebut tidak dibatasi cakupannya ke workspace tertentu.

Anda dapat menemukan ID workspace di kolom **ID** pada [Settings → Workspaces](https://platform.claude.com/settings/workspaces) di Claude Console, atau dengan memanggil endpoint [List Workspaces](https://platform.claude.com/docs/id/api/admin/workspaces/list). Keduanya tidak mencantumkan ID Default Workspace: baca ID tersebut dari [header respons](https://platform.claude.com/docs/id/manage-claude/workspaces#identify-the-workspace-behind-an-api-response) `anthropic-workspace-id` dari permintaan apa pun yang berjalan di sana (misalnya, permintaan yang dibuat dengan kunci workspace dari Default Workspace), atau dari `scope.workspace_id` pada kunci semacam itu di [List API Keys](https://platform.claude.com/docs/id/api/admin/api_keys/list).

<CodeGroup>
  ```bash cURL
  # Wajib pada setiap permintaan untuk kunci multi-workspace.
  # Hilangkan header anthropic-workspace-id untuk kunci single-workspace.
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-workspace-id: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```bash CLI
  # Wajib pada setiap perintah untuk kunci multi-workspace.
  # Hilangkan --workspace-id untuk kunci workspace tunggal.
  ant messages create \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  client = Anthropic()  # reads ANTHROPIC_API_KEY

  # Wajib pada setiap permintaan untuk kunci multi-workspace.
  # Hilangkan extra_headers untuk kunci single-workspace.
  message = client.messages.create(
      model="claude-opus-5",
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

  // Wajib pada setiap permintaan untuk kunci multi-workspace.
  // Hilangkan argumen kedua untuk kunci single-workspace.
  const message = await client.messages.create(
    {
      model: "claude-opus-5",
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
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
  };

  // Wajib pada setiap permintaan untuk kunci multi-workspace.
  // Panggil client.Messages.Create(parameters) secara langsung untuk kunci single-workspace.
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

  // Wajib pada setiap permintaan untuk kunci multi-workspace.
  // Hilangkan opsi ini untuk kunci single-workspace.
  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
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

  // Wajib pada setiap permintaan untuk kunci multi-workspace.
  // Hilangkan putAdditionalHeader untuk kunci single-workspace.
  Message message = client.messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
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

  // Wajib pada setiap permintaan untuk kunci multi-workspace.
  // Hilangkan requestOptions untuk kunci single-workspace.
  $message = $client->messages->create(
      model: Model::CLAUDE_OPUS_5,
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

  # Wajib pada setiap permintaan untuk kunci multi-workspace.
  # Hilangkan request_options untuk kunci single-workspace.
  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5,
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    request_options: {extra_headers: {"anthropic-workspace-id" => "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"}}
  )

  puts message.content
  ```
</CodeGroup>

Jika permintaan yang dibuat dengan kunci yang tidak dibatasi cakupannya ke suatu workspace menghilangkan header tersebut, API mengembalikan 400 `invalid_request_error`:

```json JSON
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "anthropic-workspace-id is required when authenticating with an identity-linked API key; send the id of the workspace this request acts in."
  },
  "request_id": "req_011CSHoEeqs5C35K2UUqR7Fy"
}
```

Nilai header yang bukan ID workspace yang valid mengembalikan 400 `invalid_request_error` dengan pesan `anthropic-workspace-id header must be a valid workspace ID.` Jika workspace tidak ada, atau pengguna atau akun layanan pemilik kunci tidak memiliki akses ke workspace tersebut, API mengembalikan 404 `not_found_error` dengan pesan ``Workspace `<id>` not found.``, respons yang sama seperti untuk workspace yang tidak dikenal.

Workload Identity Federation memilih workspace pada saat pertukaran token; lihat [referensi WIF](https://platform.claude.com/docs/id/manage-claude/wif-reference) untuk detailnya.

### Kedaluwarsa kunci

Saat Anda membuat kunci API dari [halaman API keys](https://platform.claude.com/settings/keys) di Claude Console, Anda memilih kedaluwarsa: preset (3 jam, 1 hari, 7 hari, atau 30 hari), durasi kustom, atau **Never** untuk kunci yang Anda simpan di pengelola rahasia dan rotasi sendiri. Jika organisasi Anda memiliki kebijakan kedaluwarsa maksimum, Console membatasi preset dan durasi kustom hingga maksimum kebijakan, dan **Never** tidak tersedia. Kunci yang sudah ada mempertahankan perilakunya saat ini; kedaluwarsa diatur pada saat pembuatan dan tidak dapat diubah setelahnya. Pilihan kedaluwarsa yang sama berlaku saat Anda [membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys) di Claude Console.

Anthropic mengirim email kepada pembuat kunci saat kedaluwarsa mendekat: 7 hari sebelum kedaluwarsa untuk kunci yang dibuat dengan masa berlaku setidaknya 14 hari, dan 1 hari sebelumnya untuk kunci dengan masa berlaku setidaknya 7 hari. Kunci dengan masa berlaku lebih pendek kedaluwarsa tanpa email peringatan.

Setelah kunci kedaluwarsa, permintaan yang dibuat dengannya mengembalikan `401 authentication_error`. Buat kunci baru untuk memulihkan akses; kunci yang kedaluwarsa tidak dapat diaktifkan kembali.

Tabel API keys di Console menampilkan kedaluwarsa setiap kunci, dan Admin API melaporkan timestamp `expires_at` setiap kunci pada endpoint [List API Keys](https://platform.claude.com/docs/id/api/admin/api_keys/list) dan [Retrieve API Key](https://platform.claude.com/docs/id/api/admin/api_keys/retrieve), sehingga Anda dapat mengaudit dan merotasi kunci sebelum kedaluwarsa. Field ini bernilai `null` untuk kunci tanpa kedaluwarsa.

Kedaluwarsa membatasi masa berlaku kredensial yang bocor, tetapi bukan pengganti kebersihan rahasia. Terlepas dari kedaluwarsa, simpan kunci di pengelola rahasia dan nonaktifkan atau hapus kunci apa pun yang Anda curigai telah bocor.

### Mengganti kunci API workspace

Jika Anda memiliki kunci workspace, Anda mungkin ingin menggantinya dengan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/wif-reference) atau kunci pribadi atau kunci akun layanan. Ini memberikan keamanan dan observabilitas yang lebih baik.

Lihat [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/wif-reference) untuk detail tentang mengonfigurasi Workload Identity Federation, yang lebih diutamakan daripada kunci berumur panjang.

Untuk mengganti kunci workspace dengan kunci pribadi atau kunci akun layanan:

1. **Tentukan jenis kunci.** Tooling Anda sendiri sebaiknya menggunakan kunci pribadi. Beban kerja bersama atau tanpa pengawasan sebaiknya menggunakan kunci akun layanan.
2. **Buat akun layanan** jika diperlukan. Anda mungkin harus meminta admin organisasi untuk membuatnya di [Settings → Service accounts](https://platform.claude.com/settings/service-accounts) dan menambahkannya ke workspace yang relevan.
3. **Buat kunci baru.** Buat kunci tersebut khusus untuk workspace integrasi kecuali jika diperlukan beberapa workspace.
4. **Deploy kunci baru.** Ganti kunci lama di mana pun integrasi membacanya, biasanya variabel lingkungan `ANTHROPIC_API_KEY` atau entri pengelola rahasia. Untuk kunci multi-workspace, kirim juga header `anthropic-workspace-id` seperti yang ditunjukkan di [Memilih workspace](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace).
5. **Hapus kunci lama.** Pastikan permintaan berhasil, lalu hapus kunci workspace di [halaman API keys](https://platform.claude.com/settings/keys).

## Workload Identity Federation

"Workload Identity Federation" (federasi identitas beban kerja), atau WIF, memungkinkan beban kerja melakukan autentikasi dengan token identitas berumur pendek yang diterbitkan oleh "identity provider" (penyedia identitas), atau IdP, yang sudah Anda percayai, seperti AWS IAM, Google Cloud, atau penerbit OIDC apa pun yang sesuai standar (seperti GitHub Actions, akun layanan Kubernetes, SPIFFE, Microsoft Entra ID, atau Okta). Beban kerja menukar JWT yang diterbitkan IdP-nya di `POST /v1/oauth/token` dengan token akses Claude API berumur pendek, dan SDK memperbarui token tersebut secara otomatis sebelum kedaluwarsa. Tidak ada string `sk-ant-api...` yang perlu dibuat, didistribusikan, atau dirotasi.

Federasi menghilangkan kunci Claude API berumur panjang dari lingkungan Anda, yang memperkecil radius dampak kredensial yang bocor dan memungkinkan Anda mengelola akses dengan kontrol IdP yang sama yang sudah Anda gunakan untuk sumber daya cloud. Federasi tidak, dengan sendirinya, menjamin keamanan end-to-end: rantai kepercayaan hanya sekuat konfigurasi penyedia identitas Anda, dan rahasia berumur panjang satu langkah di hulu (misalnya, kredensial cloud statis yang dapat membuat token IdP) masih dapat melemahkannya. Padukan federasi dengan kontrol penyedia Anda, seperti allowlist IP, MFA, dan pencatatan audit.

Untuk mengonfigurasi federasi, Anda membuat tiga sumber daya di Claude Console (akun layanan, penerbit federasi, dan aturan federasi) lalu mengarahkan SDK Anda ke aturan tersebut. Lihat [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) untuk panduan penyiapan lengkap.

## App Attest

App Attest mengautentikasi aplikasi iOS dan macOS yang memanggil Claude API langsung dari perangkat. Setiap instalasi membuktikan bahwa dirinya adalah build asli dan tidak dimodifikasi dari aplikasi yang Anda daftarkan di Claude Console, menggunakan layanan App Attest dari Apple. Anthropic kemudian menerbitkan token akses berumur pendek untuk perangkat tersebut yang menagihkan penggunaan ke workspace Anda. Token dibatasi cakupannya ke workspace Anda, kedaluwarsa setelah satu jam, dan hanya mengotorisasi panggilan [Messages API](https://platform.claude.com/docs/id/api/messages/create).

Untuk mendaftarkan aplikasi Anda dan mendapatkan client ID, lihat [App Attest untuk aplikasi iOS dan macOS](https://platform.claude.com/docs/id/manage-claude/app-attest).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Siapkan Workload Identity Federation" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/workload-identity-federation">
    Konfigurasikan penerbit, aturan, dan akun layanan, lalu tukarkan token
  </Card>

  <Card title="Panduan penyedia identitas" icon="cloud" href="https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#identity-providers">
    Panduan langkah demi langkah untuk AWS, Google Cloud, Azure, GitHub Actions, Kubernetes, SPIFFE, dan Okta
  </Card>

  <Card title="Referensi WIF" icon="book" href="https://platform.claude.com/docs/id/manage-claude/wif-reference">
    Variabel lingkungan, aturan validasi, konfigurasi profil, dan referensi error
  </Card>

  <Card title="App Attest untuk aplikasi iOS dan macOS" icon="fingerprint" href="https://platform.claude.com/docs/id/manage-claude/app-attest">
    Izinkan instalasi asli aplikasi Anda memanggil Claude API tanpa menyertakan kunci API
  </Card>

  <Card title="SDK Klien" icon="code" href="https://platform.claude.com/docs/id/cli-sdks-libraries/overview">
    Python, TypeScript, C#, Go, Java, PHP, Ruby, dan CLI
  </Card>
</CardGroup>
