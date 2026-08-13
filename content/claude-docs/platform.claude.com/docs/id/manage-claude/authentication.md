---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/authentication
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 1fac1eff658f8906fa69a14610f0ad8b2451703d3fb19a4b9c9c6445acd84d4b
---

---
title: Autentikasi
url: https://platform.claude.com/docs/id/manage-claude/authentication
description: Autentikasi ke Claude API dengan kunci API, Workload Identity Federation, atau App Attest.
---

Claude API mendukung tiga cara untuk mengautentikasi permintaan:

| Metode                                                                                                                        | Kredensial                                                                                                                      | Paling cocok untuk                                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| [Kunci API](https://platform.claude.com/docs/id/manage-claude/authentication#api-keys)                                        | Rahasia statis `sk-ant-api...` di header `x-api-key`                                                                            | Pengembangan lokal, pembuatan prototipe, skrip, dan server single-tenant di mana Anda mengontrol penyimpanan rahasia                            |
| [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/authentication#workload-identity-federation) | Bearer token berumur pendek yang ditukar dari identity token milik identity provider Anda                                       | Workload produksi di platform cloud (AWS, Google Cloud, Azure), pipeline CI/CD, dan Kubernetes, di mana Anda ingin menghilangkan rahasia statis |
| [App Attest](https://platform.claude.com/docs/id/manage-claude/authentication#app-attest)                                     | Access token berumur pendek yang diterbitkan untuk instalasi asli dan terverifikasi dari aplikasi iOS atau macOS terdaftar Anda | Aplikasi iOS dan macOS yang didistribusikan ke pengguna akhir, di mana aplikasi memanggil Claude API secara langsung tanpa back end atau proxy  |

Kunci API dan Workload Identity Federation memberikan akses yang sama ke endpoint Claude API. Pilih kunci API untuk memulai dengan cepat, dan beralih ke Workload Identity Federation ketika workload Anda sudah memiliki identitas yang diterbitkan platform yang dapat Anda federasikan. Gunakan App Attest untuk aplikasi iOS dan macOS yang Anda distribusikan ke pengguna akhir.

## Kunci API

Kunci API adalah rahasia statis yang Anda buat di Claude Console dan kirimkan pada setiap permintaan.

* **Buat kunci:** Buka [Settings → API keys](https://platform.claude.com/settings/keys) di Claude Console. Anda memilih [masa berlaku](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration) sebagai bagian dari pembuatan. Gunakan [workspace](https://platform.claude.com/settings/workspaces) untuk membatasi cakupan kunci berdasarkan proyek atau lingkungan.
* **Kirim kunci:** Atur header `x-api-key` pada permintaan HTTP langsung, atau atur variabel lingkungan `ANTHROPIC_API_KEY` dan [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) akan mengambilnya secara otomatis.

```http
POST /v1/messages
x-api-key: YOUR_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

Simpan kunci API di secrets manager, rotasi secara berkala, dan cabut kunci apa pun yang Anda curigai telah bocor. Anda juga dapat mengatur [masa berlaku](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration) saat membuat kunci untuk membatasi berapa lama kredensial yang bocor tetap dapat digunakan.

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
  # atau, dengan ANTHROPIC_API_KEY yang diatur di environment:
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
  // Atau, dengan ANTHROPIC_API_KEY yang telah diatur di environment:
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
  # atau, dengan ANTHROPIC_API_KEY yang diatur di environment:
  anthropic = Anthropic::Client.new
  ```

  ```bash CLI
  # Lihat /docs/en/cli-sdks-libraries/cli/authentication#api-key untuk varian zsh, bash, dan Windows
  export ANTHROPIC_API_KEY=sk-ant-api03-...
  ```
</CodeGroup>

### Masa berlaku kunci

Saat Anda membuat kunci API dari [halaman API keys](https://platform.claude.com/settings/keys) di Claude Console, Anda memilih masa berlaku: preset (3 jam, 1 hari, 7 hari, atau 30 hari), durasi kustom, atau **Never** untuk kunci yang Anda simpan di secrets manager dan rotasi sendiri. Jika organisasi Anda memiliki kebijakan masa berlaku maksimum, Console membatasi preset dan durasi kustom ke maksimum kebijakan tersebut, dan **Never** tidak tersedia. Kunci yang sudah ada mempertahankan perilakunya saat ini; masa berlaku diatur pada saat pembuatan dan tidak dapat diubah setelahnya. Pilihan masa berlaku yang sama berlaku saat Anda [membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys) di Claude Console.

Anthropic mengirim email kepada pembuat kunci saat masa berlaku mendekat: 7 hari sebelum kedaluwarsa untuk kunci yang dibuat dengan masa hidup minimal 14 hari, dan 1 hari sebelumnya untuk kunci dengan masa hidup minimal 7 hari. Kunci dengan masa hidup lebih pendek akan kedaluwarsa tanpa email peringatan.

Setelah kunci kedaluwarsa, permintaan yang dibuat dengannya mengembalikan `401 authentication_error`. Buat kunci baru untuk memulihkan akses; kunci yang kedaluwarsa tidak dapat diaktifkan kembali.

Tabel API keys di Console menampilkan masa berlaku setiap kunci, dan Admin API melaporkan timestamp `expires_at` setiap kunci pada endpoint [List API Keys](https://platform.claude.com/docs/id/api/admin/api_keys/list) dan [Retrieve API Key](https://platform.claude.com/docs/id/api/admin/api_keys/retrieve), sehingga Anda dapat mengaudit dan merotasi kunci sebelum kedaluwarsa. Field ini bernilai `null` untuk kunci tanpa masa berlaku.

Masa berlaku membatasi masa hidup kredensial yang bocor, tetapi bukan pengganti untuk kebersihan rahasia. Terlepas dari masa berlaku, simpan kunci di secrets manager dan cabut kunci apa pun yang Anda curigai telah bocor.

## Workload Identity Federation

"Workload Identity Federation" (federasi identitas workload), atau WIF, memungkinkan workload mengautentikasi dengan identity token berumur pendek yang diterbitkan oleh "identity provider" (penyedia identitas), atau IdP, yang sudah Anda percaya, seperti AWS IAM, Google Cloud, atau issuer OIDC apa pun yang sesuai standar (seperti GitHub Actions, service account Kubernetes, SPIFFE, Microsoft Entra ID, atau Okta). Workload menukar JWT yang diterbitkan IdP-nya di `POST /v1/oauth/token` dengan access token Claude API berumur pendek, dan SDK menyegarkan token tersebut secara otomatis sebelum kedaluwarsa. Tidak ada string `sk-ant-api...` yang perlu dibuat, didistribusikan, atau dirotasi.

Federasi menghilangkan kunci Claude API berumur panjang dari lingkungan Anda, yang memperkecil dampak dari kredensial yang bocor dan memungkinkan Anda mengelola akses dengan kontrol IdP yang sama yang sudah Anda gunakan untuk sumber daya cloud. Federasi tidak, dengan sendirinya, menjamin keamanan end-to-end: rantai kepercayaan hanya sekuat konfigurasi identity provider Anda, dan rahasia berumur panjang satu hop di hulu (misalnya, kredensial cloud statis yang dapat membuat token IdP) masih dapat merusaknya. Padukan federasi dengan kontrol provider Anda, seperti IP allowlist, MFA, dan audit logging.

Untuk mengonfigurasi federasi, Anda membuat tiga sumber daya di Claude Console (service account, federation issuer, dan federation rule) lalu mengarahkan SDK Anda ke rule tersebut. Lihat [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) untuk panduan penyiapan lengkap.

## App Attest

App Attest mengautentikasi aplikasi iOS dan macOS yang memanggil Claude API langsung dari perangkat. Setiap instalasi membuktikan bahwa ia adalah build asli dan tidak dimodifikasi dari aplikasi yang Anda daftarkan di Claude Console, menggunakan layanan App Attest dari Apple. Anthropic kemudian menerbitkan access token berumur pendek ke perangkat yang menagih penggunaan ke workspace Anda. Token dibatasi cakupannya ke workspace Anda, kedaluwarsa setelah satu jam, dan hanya mengotorisasi panggilan [Messages API](https://platform.claude.com/docs/id/api/messages/create).

Untuk mendaftarkan aplikasi Anda dan mendapatkan client ID, lihat [App Attest untuk aplikasi iOS dan macOS](https://platform.claude.com/docs/id/manage-claude/app-attest).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Siapkan Workload Identity Federation" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/workload-identity-federation">
    Konfigurasikan issuer, rule, dan service account, lalu tukar token
  </Card>

  <Card title="Panduan identity provider" icon="cloud" href="https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#identity-providers">
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
