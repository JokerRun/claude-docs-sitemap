---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/authentication
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 77dc6ce9c9e665eda17162306af05f72f2f3d1b7de391e90a2214d1ba202f0bb
---

# Autentikasi

Autentikasi ke Claude API dengan kunci API atau Workload Identity Federation.

---

Claude API mendukung dua cara untuk mengautentikasi permintaan:

| Metode                                                        | Kredensial                                                                            | Paling cocok untuk                                                                                                                                 |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Kunci API](#api-keys)                                        | Rahasia statis `sk-ant-api...` di header `x-api-key`                                  | Pengembangan lokal, pembuatan prototipe, skrip, dan server single-tenant di mana Anda mengontrol penyimpanan rahasia                               |
| [Workload Identity Federation](#workload-identity-federation) | Bearer token berumur pendek yang ditukar dari token identitas penyedia identitas Anda | Beban kerja produksi di platform cloud (AWS, Google Cloud, Azure), pipeline CI/CD, dan Kubernetes, di mana Anda ingin menghilangkan rahasia statis |

Kedua metode memberikan akses yang sama ke endpoint Claude API. Pilih kunci API untuk memulai dengan cepat, dan beralih ke Workload Identity Federation ketika beban kerja Anda sudah memiliki identitas yang diterbitkan platform yang dapat Anda federasikan.

## Kunci API

"API key" (kunci API) adalah rahasia statis yang Anda buat di Claude Console dan kirimkan pada setiap permintaan.

* **Buat kunci:** Buka [Settings → API keys](https://platform.claude.com/settings/keys) di Claude Console. Anda memilih [masa berlaku](#key-expiration) sebagai bagian dari pembuatan. Gunakan [workspaces](https://platform.claude.com/settings/workspaces) untuk membatasi cakupan kunci berdasarkan proyek atau lingkungan.
* **Kirim kunci:** Atur header `x-api-key` pada permintaan HTTP langsung, atau atur variabel lingkungan `ANTHROPIC_API_KEY` dan [SDK klien](/docs/id/cli-sdks-libraries/overview) akan mengambilnya secara otomatis.

```http
POST /v1/messages
x-api-key: YOUR_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

Simpan kunci API di secrets manager, rotasi secara berkala, dan cabut kunci apa pun yang Anda curigai telah bocor. Anda juga dapat mengatur [masa berlaku](#key-expiration) saat membuat kunci untuk membatasi berapa lama kredensial yang bocor tetap dapat digunakan.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```python Python
  client = Anthropic(api_key="my-anthropic-api-key")
  # atau, dengan ANTHROPIC_API_KEY yang sudah diatur di environment:
  client = Anthropic()
  ```

  ```typescript TypeScript
  const client = new Anthropic({ apiKey: "my-anthropic-api-key" });
  // atau, dengan ANTHROPIC_API_KEY yang sudah diatur di environment:
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
  // Atau, dengan ANTHROPIC_API_KEY yang sudah diatur di environment:
  // AnthropicClient client = new();
  ```

  ```php PHP
  // Membaca ANTHROPIC_API_KEY dari environment
  $client = new Client();
  // Atau berikan kunci secara eksplisit:
  $client = new Client(apiKey: 'my-anthropic-api-key');
  ```

  ```ruby Ruby
  anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")
  # atau, dengan ANTHROPIC_API_KEY yang sudah diatur di environment:
  anthropic = Anthropic::Client.new
  ```

  ```bash CLI
  # Lihat /docs/en/cli-sdks-libraries/cli/authentication#api-key untuk varian zsh, bash, dan Windows
  export ANTHROPIC_API_KEY=sk-ant-api03-...
  ```
</CodeGroup>

### Masa berlaku kunci

Saat Anda membuat kunci API dari [halaman API keys](https://platform.claude.com/settings/keys) di Claude Console, Anda memilih masa berlaku: preset (3 jam, 1 hari, 7 hari, atau 30 hari), durasi kustom, atau **Never** untuk kunci yang Anda simpan di secrets manager dan rotasi sendiri. Jika organisasi Anda memiliki kebijakan masa berlaku maksimum, Console membatasi preset dan durasi kustom hingga maksimum kebijakan, dan **Never** tidak tersedia. Kunci yang sudah ada mempertahankan perilaku saat ini; masa berlaku ditetapkan pada saat pembuatan dan tidak dapat diubah setelahnya. Pilihan masa berlaku yang sama berlaku saat Anda [membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys) di Claude Console.

Anthropic mengirim email kepada pembuat kunci saat masa berlaku mendekati: 7 hari sebelum kedaluwarsa untuk kunci yang dibuat dengan masa pakai setidaknya 14 hari, dan 1 hari sebelumnya untuk kunci dengan masa pakai setidaknya 7 hari. Kunci dengan masa pakai yang lebih pendek kedaluwarsa tanpa email peringatan.

Setelah kunci kedaluwarsa, permintaan yang dibuat dengannya mengembalikan `401 authentication_error`. Buat kunci baru untuk memulihkan akses; kunci yang kedaluwarsa tidak dapat diaktifkan kembali.

Tabel kunci API di Console menampilkan masa berlaku setiap kunci, dan Admin API melaporkan timestamp `expires_at` setiap kunci pada endpoint [List API Keys](/docs/id/api/admin/api_keys/list) dan [Retrieve API Key](/docs/id/api/admin/api_keys/retrieve), sehingga Anda dapat mengaudit dan merotasi kunci sebelum kedaluwarsa. Field tersebut bernilai `null` untuk kunci tanpa masa berlaku.

Masa berlaku membatasi masa pakai kredensial yang bocor, tetapi bukan pengganti kebersihan rahasia. Terlepas dari masa berlaku, simpan kunci di secrets manager dan cabut kunci apa pun yang Anda curigai telah bocor.

## Workload Identity Federation

"Workload Identity Federation" (federasi identitas beban kerja), atau WIF, memungkinkan beban kerja mengautentikasi dengan token identitas berumur pendek yang diterbitkan oleh "identity provider" (penyedia identitas), atau IdP, yang sudah Anda percayai, seperti AWS IAM, Google Cloud, atau penerbit OIDC apa pun yang sesuai standar (seperti GitHub Actions, service account Kubernetes, SPIFFE, Microsoft Entra ID, atau Okta). Beban kerja menukar JWT yang diterbitkan IdP di `POST /v1/oauth/token` dengan token akses Claude API berumur pendek, dan SDK menyegarkan token tersebut secara otomatis sebelum kedaluwarsa. Tidak ada string `sk-ant-api...` yang perlu dibuat, didistribusikan, atau dirotasi.

Federasi menghilangkan kunci Claude API berumur panjang dari lingkungan Anda, yang memperkecil dampak dari kredensial yang bocor dan memungkinkan Anda mengelola akses dengan kontrol IdP yang sama yang sudah Anda gunakan untuk sumber daya cloud. Ini tidak, dengan sendirinya, menjamin keamanan end-to-end: rantai kepercayaan hanya sekuat konfigurasi penyedia identitas Anda, dan rahasia berumur panjang satu langkah di hulu (misalnya, kredensial cloud statis yang dapat membuat token IdP) masih dapat melemahkannya. Padukan federasi dengan kontrol penyedia Anda, seperti daftar IP yang diizinkan, MFA, dan pencatatan audit.

Untuk mengonfigurasi federasi, Anda membuat tiga sumber daya di Claude Console (service account, federation issuer, dan federation rule) lalu mengarahkan SDK Anda ke rule tersebut. Lihat [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation) untuk panduan penyiapan lengkap.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Siapkan Workload Identity Federation" icon="lock" href="/docs/id/manage-claude/workload-identity-federation">
    Konfigurasikan issuer, rule, dan service account, lalu tukar token
  </Card>

  <Card title="Panduan penyedia identitas" icon="cloud" href="/docs/id/manage-claude/workload-identity-federation#identity-providers">
    Panduan langkah demi langkah untuk AWS, Google Cloud, Azure, GitHub Actions, Kubernetes, SPIFFE, dan Okta
  </Card>

  <Card title="Referensi WIF" icon="book" href="/docs/id/manage-claude/wif-reference">
    Variabel lingkungan, aturan validasi, konfigurasi profil, dan referensi kesalahan
  </Card>

  <Card title="SDK Klien" icon="code" href="/docs/id/cli-sdks-libraries/overview">
    Python, TypeScript, C#, Go, Java, PHP, Ruby, dan CLI
  </Card>
</CardGroup>
