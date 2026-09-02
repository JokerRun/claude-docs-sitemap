---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: c94b012afaf65c7b2247633ba4100a25c3e94da409b8782dedde90e616e0a229
---

---
title: Apple Foundation Models
url: https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models
description: Gunakan Claude di platform Apple melalui framework Foundation Models dengan paket Swift Claude for Foundation Models.
---

[Claude for Foundation Models](https://github.com/anthropics/ClaudeForFoundationModels) adalah paket Swift yang membuat Claude tersedia sebagai model bahasa sisi server dalam framework [Foundation Models](https://developer.apple.com/documentation/foundationmodels) milik Apple. Paket ini menyesuaikan Claude dengan protokol `LanguageModel` milik framework tersebut, sehingga Anda mengendalikannya dengan API `LanguageModelSession` yang sama dengan yang Anda gunakan untuk model on-device Apple: `respond(to:)`, streaming, guided generation, dan pemanggilan alat semuanya bekerja dengan cara yang sama.

Permintaan dikirim langsung dari aplikasi Anda ke Claude API; Apple tidak berada di jalur permintaan dan tidak melihat prompt maupun respons. Penggunaan ditagihkan ke akun Anthropic Anda dengan [harga API standar](https://platform.claude.com/docs/id/about-claude/pricing), sehingga organisasi Anda memerlukan saldo kredit yang tersedia atau metode penagihan yang aktif. Aplikasi Anda yang menentukan kapan menggunakan Claude dan kapan menggunakan model on-device Apple: teruskan model mana pun yang Anda inginkan ke setiap sesi.

<Note>
  **Beta.** Paket ini menargetkan API model bahasa sisi server Foundation Models yang diperkenalkan dalam beta OS 27. API dapat berubah selama masa beta.
</Note>

<Info>
  Claude for Foundation Models **bukan** klien Messages API serbaguna. Permukaan publiknya adalah konformansi penyedia Foundation Models ditambah tipe konfigurasi yang menjangkaunya (`ClaudeLanguageModel`, `ClaudeModel`, `AuthMode`, `ClaudeServerTool`). Untuk akses langsung ke Messages API dalam bahasa lain, lihat [Client SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview#client-sdks).
</Info>

## Persyaratan

* iOS 27, macOS 27, visionOS 27, atau watchOS 27 (semuanya dalam beta): rilis OS yang framework Foundation Models-nya mendukung model bahasa sisi server
* Xcode 27 (beta)
* Kunci API Claude dari [Claude Console](https://platform.claude.com/) untuk pengembangan. Lihat [Autentikasi](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models#authentication) untuk opsi produksi.

## Instal paket

Tambahkan paket ke `Package.swift` Anda:

```swift
dependencies: [
  .package(url: "https://github.com/anthropics/ClaudeForFoundationModels.git", from: "0.1.0")
]
```

Atau di Xcode: **File** > **Add Package Dependencies…** lalu masukkan URL repositori.

Kemudian tambahkan `ClaudeForFoundationModels` ke dependensi target Anda dan impor bersama `FoundationModels`:

```swift
import FoundationModels
import ClaudeForFoundationModels
```

## Mulai cepat

`ClaudeLanguageModel` adalah titik masuknya. Teruskan ke `LanguageModelSession` dan gunakan sesi tersebut persis seperti yang Anda lakukan dengan penyedia Foundation Models mana pun:

```swift
import FoundationModels
import ClaudeForFoundationModels

let model = ClaudeLanguageModel(
  name: .sonnet5,
  auth: .apiKey(ProcessInfo.processInfo.environment["ANTHROPIC_API_KEY"] ?? "")
)

let session = LanguageModelSession(model: model)
let response = try await session.respond(to: "Plan a 4-day trip to Buenos Aires.")
print(response.content)
```

Initializer ini juga menerima `baseURL` (default `https://api.anthropic.com`), `timeout`, dan `serverTools` (lihat [Alat sisi server](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models#server-side-tools)).

Untuk program lengkap yang berfungsi, repositori menyertakan [`Examples/ClaudeExample`](https://github.com/anthropics/ClaudeForFoundationModels/tree/main/Examples/ClaudeExample), target command-line yang dapat dijalankan yang melakukan streaming satu giliran chat ke terminal, dengan flag `--search` yang mengaktifkan pencarian web sisi server untuk giliran tersebut. Menjalankannya memerlukan host macOS 27.

## Memilih model

Pengidentifikasi model adalah nilai dari `ClaudeModel`. Gunakan konstanta yang sudah dikompilasi, atau buat satu dengan kapabilitas eksplisit untuk ID yang belum dikompilasi (lihat [Kapabilitas](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models#capabilities)):

```swift
ClaudeLanguageModel(name: .opus5, auth: auth)
```

Konstanta mencerminkan ID model API (`.opus5` adalah `claude-opus-5`) dan membawa kapabilitas masing-masing model. Model baru dirilis sebagai konstanta baru dalam rilis paket; periksa `ClaudeModel` di Xcode untuk daftar terkini, dan [Ikhtisar model](https://platform.claude.com/docs/id/models/overview) untuk membandingkan model.

### Kapabilitas

Setiap `ClaudeModel` mendeklarasikan apa yang diterimanya: parameter sampling, tingkat effort, adaptive thinking, output terstruktur, dan input gambar. Paket menggunakan ini untuk menentukan field permintaan mana yang dikirim, karena mengirim field yang ditolak model merupakan error fatal. Konstanta membawa kapabilitas yang tepat. Untuk ID yang belum dikompilasi, deklarasikan apa yang diterima model (sengaja tidak ada pintasan yang menebak):

```swift
let model = ClaudeModel(
  id: "claude-experimental-x",
  capabilities: .init(samplingParams: false, effortLevels: [.low, .high])
)
ClaudeLanguageModel(name: model, auth: auth)
```

### Effort

Tetapkan [tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort) Claude untuk setiap permintaan dengan `fixedEffort:`. Ini lebih diutamakan daripada petunjuk reasoning per permintaan milik framework. Tingkat reasoning bernama milik framework berhenti di high; untuk meminta effort lebih tinggi untuk satu permintaan saja, teruskan tingkat reasoning kustom yang menyebutkan effort Claude (`.custom("xhigh")` atau `.custom("max")`), yang dipetakan secara langsung. API menggunakan default `high` ketika tidak ada effort yang dikirim:

```swift
ClaudeLanguageModel(name: .opus5, auth: auth, fixedEffort: .xhigh)
```

Tingkat tersebut harus merupakan tingkat yang diterima model. Setiap `ClaudeModel` mendeklarasikan mana dari lima tingkat (`low`, `medium`, `high`, `xhigh`, `max`) yang diterima modelnya, jika ada: beberapa model tidak menerima effort sama sekali.

### Kapan menggunakan Claude versus model on-device

Model on-device Apple cepat, privat, dan tersedia secara offline, tetapi ukurannya dirancang untuk tugas ringan. Eskalasikan ke Claude ketika Anda memerlukan konteks yang lebih besar, reasoning terdepan, atau alat sisi server seperti pencarian web dan eksekusi kode. Karena keduanya menggunakan API `LanguageModelSession` yang sama, Anda dapat beralih dengan menukar argumen `model:`.

## Autentikasi

Atur kredensial dengan parameter `auth:`. Gunakan `.appAttest` untuk merilis tanpa back end, `.proxied` untuk merutekan permintaan melalui back end Anda sendiri, atau `.apiKey` untuk beriterasi selama pengembangan.

### App Attest

Setiap instalasi aplikasi Anda menggunakan layanan [App Attest](https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity) dari Apple untuk membuktikan bahwa aplikasi tersebut adalah build asli yang tidak dimodifikasi dari aplikasi yang Anda daftarkan. Anthropic kemudian menerbitkan "access token" (token akses) berumur pendek untuk perangkat tersebut yang menagihkan penggunaan ke workspace Anda. Aplikasi tidak menyertakan kunci API, dan tidak ada proxy yang perlu Anda operasikan.

Autentikasi App Attest hanya tersedia ketika aplikasi Anda memanggil Claude API secara langsung. Autentikasi ini tidak tersedia melalui Amazon Bedrock, Google Cloud, atau Microsoft Foundry.

Untuk merilis tanpa menjalankan back end, gunakan `.appAttest`:

```swift
ClaudeLanguageModel(
  name: .sonnet5,
  auth: .appAttest(clientID: "clid_...")
)
```

<Note>
  App Attest memerlukan perangkat fisik. Simulator, dan perangkat keras tanpa Secure Enclave, tidak dapat melakukan App Attest. Gunakan `.apiKey` saat beriterasi di Simulator, dan `.appAttest` saat berjalan di perangkat.
</Note>

Untuk menyiapkan App Attest, Anda memerlukan Apple Developer Team ID Anda dan peran admin, owner, atau primary owner di organisasi Anda. Konfigurasikan proyek Xcode Anda dan daftarkan aplikasi Anda di [Claude Console](https://platform.claude.com/):

1. Di Xcode, tambahkan kapabilitas **App Attest** ke target aplikasi Anda di bawah **Signing & Capabilities**.
2. Di pengaturan workspace Anda di Claude Console, buka **App integrations**.
3. Klik **Create app integration** dan masukkan nama, Apple Developer Team ID Anda, dan satu atau lebih bundle ID (hingga 32).
4. Salin client ID (`clid_...`) dari tab **Overview** integrasi tersebut dan teruskan ke konfigurasi Claude aplikasi Anda.

Saat pertama kali aplikasi Anda menggunakan Claude di sebuah perangkat, aplikasi meminta challenge dari Anthropic, melakukan atestasi perangkat dengan `DCAppAttestService` milik Apple, dan menukarkan atestasi yang telah diverifikasi dengan "access token" (token akses). Paket Claude for Foundation Models menjalankan alur ini secara otomatis dan meminta token baru saat token lama kedaluwarsa; tidak ada kode atestasi yang perlu Anda tulis.

Token dibatasi cakupannya pada workspace Anda, kedaluwarsa setelah satu jam, dan hanya mengotorisasi panggilan [Messages API](https://platform.claude.com/docs/id/api/messages/create). Token tidak membawa identitas pengguna akhir: App Attest mengidentifikasi aplikasi Anda, bukan orang yang menggunakannya, jadi tangani logika per pengguna apa pun di dalam aplikasi Anda.

Untuk menghentikan aplikasi yang telah disusupi atau dipensiunkan, cabut integrasinya: di pengaturan workspace Anda di Claude Console, buka **App integrations**, pilih integrasi tersebut, dan klik **Revoke**, lalu konfirmasi. Mencabut integrasi akan mencabut token-tokennya yang masih berlaku, dan perangkat terdaftarnya tidak dapat lagi meminta token baru. Pencabutan bersifat permanen, jadi buat integrasi aplikasi baru untuk memulihkan akses.

### Proxy (produksi)

Untuk produksi, rutekan permintaan melalui back end Anda sendiri dengan `.proxied`. Relay di `baseURL` menambahkan kredensial Claude API di sisi server, sehingga aplikasi tidak menyertakan kunci apa pun. `headers` yang Anda berikan dikirim pada setiap permintaan agar proxy Anda dapat mengotorisasi pemanggil. Teruskan `[:]` jika tidak memerlukan apa pun:

```swift
ClaudeLanguageModel(
  name: .sonnet5,
  auth: .proxied(headers: ["X-App-Token": "..."]),
  baseURL: URL(string: "https://api.yourapp.com/claude")!
)
```

Proxy Anda menerima permintaan [Messages API](https://platform.claude.com/docs/id/api/messages/create) standar, melampirkan header `x-api-key`, dan meneruskannya ke `https://api.anthropic.com`.

### Kunci API (pengembangan)

Teruskan kunci API secara langsung saat mengembangkan:

```swift
ClaudeLanguageModel(name: .sonnet5, auth: .apiKey("YOUR_API_KEY"))
```

<Warning>
  Kunci yang dibundel ke dalam aplikasi dapat diekstrak dari binary yang dirilis, dan siapa pun yang mengekstraknya dapat membuat permintaan yang ditagihkan ke akun Anda. Gunakan `.apiKey` hanya untuk pengembangan, dan beralihlah ke App Attest atau proxy sebelum rilis.
</Warning>

## Streaming

`streamResponse(to:)` mengembalikan respons secara bertahap. Setiap elemen adalah snapshot kumulatif dari respons sejauh ini, bukan delta:

```swift
let stream = session.streamResponse(to: "Summarize today's top science stories.")
for try await partial in stream {
  print(partial.content)
}
```

## Output terstruktur

Anotasi sebuah tipe dengan `@Generable` dan minta dengan `generating:`. Model mengembalikan nilai dari tipe tersebut melalui [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs):

```swift
@Generable
struct Trip {
  @Guide(description: "Destination city") var destination: String
  @Guide(description: "Length in days") var days: Int
}

let response = try await session.respond(to: "Plan a trip to Tokyo.", generating: Trip.self)
print(response.content.destination)
```

Output terstruktur memerlukan model yang kapabilitasnya mencakup fitur ini (semua konstanta yang sudah dikompilasi mencakupnya). Jika model yang dipilih tidak mencakupnya, paket melempar `LanguageModelError.unsupportedGenerationGuide` alih-alih menurunkan kualitas secara diam-diam.

## Penggunaan alat

### Alat sisi klien

Array `tools:` milik framework bekerja tanpa perubahan. Sesuaikan tipe Anda dengan `Tool`, teruskan ke `LanguageModelSession`, dan framework akan memanggilnya di perangkat ketika Claude memanggilnya. Lihat [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview).

```swift
let session = LanguageModelSession(model: model, tools: [FindRestaurantsTool()])
```

### Alat sisi server

[Alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools) (pencarian web, web fetch, dan eksekusi kode) berjalan di infrastruktur Anthropic dalam satu round trip, tanpa ada yang perlu dipanggil framework di perangkat. Konfigurasikan untuk setiap model dengan `serverTools:`:

```swift
let model = ClaudeLanguageModel(
  name: .sonnet5,
  auth: auth,
  serverTools: [
    .webSearch(maxUses: 5),
    .codeExecution,
  ]
)
```

`.webSearch` dan `.webFetch` menerima `allowedDomains`, `blockedDomains`, dan `maxUses` opsional. Aktivitas alat server muncul dalam transkrip sebagai segmen kustom `ClaudeServerToolSegment`.

<Note>
  `serverTools` dikonfigurasi pada `ClaudeLanguageModel` dan bukan pada `LanguageModelSession` karena tipe sesi adalah milik Apple. Untuk menggunakan set alat server yang berbeda untuk setiap percakapan, buat beberapa instance `ClaudeLanguageModel`.
</Note>

## Gambar

Model yang kapabilitasnya mencakup input gambar mendeklarasikan kapabilitas vision milik framework. Teruskan konten gambar melalui API sesi standar framework; paket mengonversinya ke format gambar Claude API. Lihat [Vision](https://platform.claude.com/docs/id/build-with-claude/vision) untuk persyaratan gambar.

## Penanganan error

Paket memetakan error Claude API ke kasus `LanguageModelError` milik Apple jika ada yang sesuai: luapan jendela konteks muncul sebagai `.contextSizeExceeded`, HTTP 429 sebagai `.rateLimited`, permintaan yang melewati timeout yang dikonfigurasi sebagai `.timeout`. Error penyedia yang tidak memiliki padanan di framework muncul sebagai `ClaudeError`. Gunakan pattern matching untuk mengarahkan alur produk:

```swift
do {
  let response = try await session.respond(to: prompt)
  print(response.content)
} catch ClaudeError.missingCredential {
  // Meminta kunci API.
} catch let error as LanguageModelError {
  // Error berbentuk framework (batas laju, guardrail, panjang konteks, decoding).
} catch {
  // Error transport.
}
```

Pola yang umum adalah menangkap `.rateLimited` dan beralih ke `SystemLanguageModel` untuk giliran tersebut, mengantrekan permintaan, atau menampilkan opsi coba lagi.

## Dukungan fitur

Paket menampilkan kapabilitas Messages API yang dapat diekspresikan oleh protokol penyedia Foundation Models. Fitur yang tidak memiliki representasi dalam protokol Apple tidak tersedia melaluinya, termasuk:

* Kontrol caching prompt (paket menerapkan caching prompt secara otomatis; TTL cache dan penempatan breakpoint tidak dapat dikonfigurasi)
* Stop sequence
* Pemrosesan batch
* Files API
* Penghitungan token
* Header beta

## Sumber daya tambahan

| Referensi                                                                                         | Mencakup                                                                                             |
| ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| [Dokumentasi Apple Foundation Models](https://developer.apple.com/documentation/foundationmodels) | `LanguageModelSession`, `@Generable`, `Transcript`, `Tool`, dan bagian lain dari permukaan framework |
| [`ClaudeForFoundationModels` di GitHub](https://github.com/anthropics/ClaudeForFoundationModels)  | Kode sumber, contoh yang dapat dijalankan, dan issue tracker                                         |
| [Referensi Claude API](https://platform.claude.com/docs/id/api/overview)                          | Messages API yang mendasarinya                                                                       |

Paket ini dilisensikan di bawah Apache 2.0. Laporan bug diterima melalui GitHub issues. Pull request eksternal tidak diterima selama periode beta.
