---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 77fc4a08bdb7a9d8bf175efad886ae6c787b736c084bc5cc857b0ae3e7ef3820
---

# Apple Foundation Models

Gunakan Claude di platform Apple melalui framework Foundation Models dengan paket Swift Claude for Foundation Models.

---

[Claude for Foundation Models](https://github.com/anthropics/ClaudeForFoundationModels) adalah paket Swift yang menyediakan Claude sebagai model bahasa sisi server dalam framework [Foundation Models](https://developer.apple.com/documentation/foundationmodels) milik Apple. Paket ini membuat Claude sesuai dengan protokol `LanguageModel` dari framework tersebut, sehingga Anda menjalankannya dengan API `LanguageModelSession` yang sama seperti yang Anda gunakan untuk model on-device Apple: `respond(to:)`, streaming, guided generation, dan pemanggilan alat semuanya bekerja dengan cara yang sama.

Permintaan dikirim langsung dari aplikasi Anda ke API Claude; Apple tidak berada di jalur permintaan dan tidak melihat prompt maupun respons. Penggunaan ditagihkan ke akun Anthropic Anda dengan [harga API standar](/docs/id/about-claude/pricing). Aplikasi Anda yang memutuskan kapan menggunakan Claude dan kapan menggunakan model on-device Apple: berikan model mana pun yang Anda inginkan ke setiap sesi.

<Note>
  **Beta.** Paket ini menargetkan API model bahasa sisi server Foundation Models yang diperkenalkan dalam beta OS 27. API dapat berubah sebelum ketersediaan umum.
</Note>

<Info>
  Claude for Foundation Models **bukan** klien Messages API serbaguna. Permukaan publiknya adalah konformitas penyedia Foundation Models ditambah tipe konfigurasi yang menjangkaunya (`ClaudeLanguageModel`, `ClaudeModel`, `AuthMode`, `ClaudeServerTool`). Untuk akses langsung ke Messages API dalam bahasa lain, lihat [Client SDK](/docs/id/cli-sdks-libraries/overview#client-sdks).
</Info>

## Persyaratan

* iOS 27, macOS 27, visionOS 27, atau watchOS 27 (semuanya dalam beta): rilis OS yang framework Foundation Models-nya mendukung model bahasa sisi server
* Xcode 27 (beta)
* Kunci API Claude dari [Claude Console](https://platform.claude.com/) untuk pengembangan. Lihat [Autentikasi](#authentication) untuk opsi produksi.

## Menginstal paket

Tambahkan paket ke `Package.swift` Anda:

```swift
dependencies: [
  .package(url: "https://github.com/anthropics/ClaudeForFoundationModels.git", from: "0.1.0")
]
```

Atau di Xcode: **File** > **Add Package Dependencies…** dan masukkan URL repositori.

Kemudian tambahkan `ClaudeForFoundationModels` ke dependensi target Anda dan impor bersama dengan `FoundationModels`:

```swift
import FoundationModels
import ClaudeForFoundationModels
```

## Mulai cepat

`ClaudeLanguageModel` adalah titik masuknya. Berikan ke `LanguageModelSession` dan gunakan sesi tersebut persis seperti yang Anda lakukan dengan penyedia Foundation Models mana pun:

```swift
import FoundationModels
import ClaudeForFoundationModels

let model = ClaudeLanguageModel(
  name: .sonnet4_6,
  auth: .apiKey(ProcessInfo.processInfo.environment["ANTHROPIC_API_KEY"] ?? "")
)

let session = LanguageModelSession(model: model)
let response = try await session.respond(to: "Plan a 4-day trip to Buenos Aires.")
print(response.content)
```

Initializer juga menerima `baseURL` (default `https://api.anthropic.com`), `timeout`, dan `serverTools` (lihat [Alat sisi server](#server-side-tools)).

Untuk program lengkap yang berfungsi, repositori menyertakan [`Examples/ClaudeExample`](https://github.com/anthropics/ClaudeForFoundationModels/tree/main/Examples/ClaudeExample), target command-line yang dapat dijalankan yang melakukan streaming satu giliran chat ke terminal, dengan flag `--search` yang mengaktifkan pencarian web sisi server untuk giliran tersebut. Menjalankannya memerlukan host macOS 27.

## Memilih model

Pengidentifikasi model adalah nilai dari `ClaudeModel`. Gunakan konstanta yang sudah dikompilasi, atau buat satu dengan kapabilitas eksplisit untuk ID yang belum dikompilasi (lihat [Kapabilitas](#capabilities)):

```swift
ClaudeLanguageModel(name: .opus4_8, auth: auth)
```

Konstanta mencerminkan ID model API (`.opus4_8` adalah `claude-opus-4-8`) dan membawa kapabilitas masing-masing model. Model baru dirilis sebagai konstanta baru dalam rilis paket; periksa `ClaudeModel` di Xcode untuk daftar terkini, dan [Ikhtisar model](/docs/id/about-claude/models/overview) untuk membandingkan model.

### Kapabilitas

Setiap `ClaudeModel` mendeklarasikan apa yang diterimanya: parameter sampling, tingkat effort, adaptive thinking, output terstruktur, dan input gambar. Paket menggunakan ini untuk memutuskan field permintaan mana yang akan dikirim, karena mengirim field yang ditolak model adalah hard error. Konstanta membawa kapabilitas yang tepat. Untuk ID yang belum dikompilasi, deklarasikan apa yang diterima model (sengaja tidak ada shorthand yang menebak-nebak):

```swift
let model = ClaudeModel(
  id: "claude-experimental-x",
  capabilities: .init(samplingParams: false, effortLevels: [.low, .high])
)
ClaudeLanguageModel(name: model, auth: auth)
```

### Effort

Tetapkan [tingkat effort](/docs/id/build-with-claude/effort) Claude untuk setiap permintaan dengan `fixedEffort:`. Ini lebih diutamakan daripada petunjuk reasoning per-permintaan dari framework, dan ini satu-satunya cara untuk meminta `.xhigh` atau `.max`, karena tingkat reasoning framework berhenti di high. API menggunakan default `high` ketika tidak ada effort yang dikirim:

```swift
ClaudeLanguageModel(name: .opus4_8, auth: auth, fixedEffort: .xhigh)
```

Tingkat tersebut harus merupakan tingkat yang diterima model. Setiap `ClaudeModel` mendeklarasikan mana dari lima tingkat (`low`, `medium`, `high`, `xhigh`, `max`) yang diterima modelnya, jika ada: beberapa model tidak menerima effort sama sekali.

### Kapan menggunakan Claude versus model on-device

Model on-device Apple cepat, privat, dan bekerja secara offline, tetapi ukurannya dirancang untuk tugas ringan. Eskalasikan ke Claude ketika Anda membutuhkan konteks yang lebih besar, penalaran tingkat frontier, atau alat sisi server seperti pencarian web dan eksekusi kode. Karena keduanya menggunakan API `LanguageModelSession` yang sama, Anda dapat beralih dengan menukar argumen `model:`.

## Autentikasi

Atur kredensial dengan parameter `auth:`.

### Kunci API (pengembangan)

Berikan kunci API secara langsung saat mengembangkan:

```swift
ClaudeLanguageModel(name: .sonnet4_6, auth: .apiKey("YOUR_API_KEY"))
```

<Warning>
  Kunci yang dibundel ke dalam aplikasi dapat diekstrak dari binary yang dirilis, dan siapa pun yang mengekstraknya dapat membuat permintaan yang ditagihkan ke akun Anda. Gunakan `.apiKey` hanya untuk pengembangan, dan beralih ke proxy sebelum rilis.
</Warning>

### Proxy (produksi)

Untuk produksi, rutekan permintaan melalui back end Anda sendiri dengan `.proxied`. Relay di `baseURL` menambahkan kredensial API Claude di sisi server, sehingga aplikasi tidak menyertakan kunci apa pun. `headers` yang Anda berikan dikirim pada setiap permintaan sehingga proxy Anda dapat mengotorisasi pemanggil. Berikan `[:]` jika tidak memerlukan apa pun:

```swift
ClaudeLanguageModel(
  name: .sonnet4_6,
  auth: .proxied(headers: ["X-App-Token": "..."]),
  baseURL: URL(string: "https://api.yourapp.com/claude")!
)
```

Proxy Anda menerima permintaan [Messages API](/docs/id/api/messages/create) standar, melampirkan header `x-api-key`, dan meneruskannya ke `https://api.anthropic.com`.

## Streaming

`streamResponse(to:)` mengembalikan respons secara bertahap. Setiap elemen adalah snapshot kumulatif dari respons sejauh ini, bukan delta:

```swift
let stream = session.streamResponse(to: "Summarize today's top science stories.")
for try await partial in stream {
  print(partial.content)
}
```

## Output terstruktur

Anotasi tipe dengan `@Generable` dan minta dengan `generating:`. Model mengembalikan nilai dari tipe tersebut melalui [output terstruktur](/docs/id/build-with-claude/structured-outputs):

```swift
@Generable
struct Trip {
  @Guide(description: "Destination city") var destination: String
  @Guide(description: "Length in days") var days: Int
}

let response = try await session.respond(to: "Plan a trip to Tokyo.", generating: Trip.self)
print(response.content.destination)
```

Output terstruktur memerlukan model yang kapabilitasnya mencakup hal tersebut (semua konstanta yang dikompilasi mendukungnya). Jika model yang dipilih tidak mendukungnya, paket akan melempar `LanguageModelError.unsupportedGenerationGuide` alih-alih menurunkan kualitas secara diam-diam.

## Penggunaan alat

### Alat sisi klien

Array `tools:` dari framework bekerja tanpa perubahan. Sesuaikan tipe Anda dengan `Tool`, berikan ke `LanguageModelSession`, dan framework akan memanggilnya di perangkat ketika Claude memanggilnya. Lihat [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview).

```swift
let session = LanguageModelSession(model: model, tools: [FindRestaurantsTool()])
```

### Alat sisi server

[Alat server](/docs/id/agents-and-tools/tool-use/server-tools) (pencarian web, pengambilan web, dan eksekusi kode) berjalan di infrastruktur Anthropic dalam satu round trip, tanpa ada yang perlu dipanggil framework di perangkat. Konfigurasikan per model dengan `serverTools:`:

```swift
let model = ClaudeLanguageModel(
  name: .sonnet4_6,
  auth: auth,
  serverTools: [
    .webSearch(maxUses: 5),
    .codeExecution,
  ]
)
```

`.webSearch` dan `.webFetch` menerima `allowedDomains`, `blockedDomains`, dan `maxUses` opsional. Aktivitas alat server muncul di transkrip sebagai segmen kustom `ClaudeServerToolSegment`.

<Note>
  `serverTools` dikonfigurasi pada `ClaudeLanguageModel` dan bukan pada `LanguageModelSession` karena tipe sesi adalah milik Apple. Untuk menggunakan set alat server yang berbeda per percakapan, buat beberapa instance `ClaudeLanguageModel`.
</Note>

## Gambar

Model yang kapabilitasnya mencakup input gambar mendeklarasikan kapabilitas vision dari framework. Berikan konten gambar melalui API sesi standar framework; paket mengonversinya ke format gambar API Claude. Lihat [Vision](/docs/id/build-with-claude/vision) untuk persyaratan gambar.

## Penanganan error

Paket memetakan error API Claude ke case `LanguageModelError` milik Apple jika ada yang cocok: overflow jendela konteks muncul sebagai `.contextSizeExceeded`, HTTP 429 sebagai `.rateLimited`, permintaan yang melewati timeout yang dikonfigurasi sebagai `.timeout`. Error penyedia yang tidak memiliki padanan framework muncul sebagai `ClaudeError`. Gunakan pattern-match untuk mengarahkan alur produk:

```swift
do {
  let response = try await session.respond(to: prompt)
  print(response.content)
} catch ClaudeError.missingCredential {
  // Minta kunci API.
} catch let error as LanguageModelError {
  // Error yang dibentuk oleh framework (batas laju, guardrail, panjang konteks, decoding).
} catch {
  // Error transport.
}
```

Pola yang umum adalah menangkap `.rateLimited` dan beralih ke `SystemLanguageModel` untuk giliran tersebut, mengantrekan permintaan, atau menampilkan opsi coba lagi.

## Dukungan fitur

Paket ini menampilkan kapabilitas Messages API yang dapat diekspresikan oleh protokol penyedia Foundation Models. Fitur yang tidak memiliki representasi dalam protokol Apple tidak tersedia melaluinya, termasuk:

* Kontrol caching prompt (paket menerapkan caching prompt secara otomatis; TTL cache dan penempatan breakpoint tidak dapat dikonfigurasi)
* Stop sequence
* Pemrosesan batch
* Files API
* Penghitungan token
* Header beta

## Sumber daya tambahan

| Referensi                                                                                         | Mencakup                                                                                            |
| ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [Dokumentasi Apple Foundation Models](https://developer.apple.com/documentation/foundationmodels) | `LanguageModelSession`, `@Generable`, `Transcript`, `Tool`, dan seluruh permukaan framework lainnya |
| [`ClaudeForFoundationModels` di GitHub](https://github.com/anthropics/ClaudeForFoundationModels)  | Kode sumber, contoh yang dapat dijalankan, dan pelacak isu                                          |
| [Referensi API Claude](/docs/id/api/overview)                                                     | Messages API yang mendasarinya                                                                      |

Paket ini dilisensikan di bawah Apache 2.0. Laporan bug diterima melalui isu GitHub. Pull request eksternal tidak diterima selama periode beta.
