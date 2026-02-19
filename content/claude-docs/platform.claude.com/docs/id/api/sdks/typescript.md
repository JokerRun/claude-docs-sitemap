---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/typescript
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: 077e0fe60ad5105b275f3da222e6a63f6aef2bb022ecaa1d51ce230fb4fe2284
---

# TypeScript SDK

Instal dan konfigurasi Anthropic TypeScript SDK untuk Node.js, Deno, Bun, dan lingkungan browser

---

Perpustakaan ini menyediakan akses yang mudah ke Anthropic REST API dari TypeScript atau JavaScript sisi server.

<Info>
Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini mencakup fitur SDK khusus TypeScript dan konfigurasi.
</Info>

## Instalasi

```bash
npm install @anthropic-ai/sdk
```

## Persyaratan

TypeScript >= 4.9 didukung.

Runtime berikut didukung:

- Node.js 20 LTS atau versi yang lebih baru ([non-EOL](https://endoflife.date/nodejs)).
- Deno v1.28.0 atau lebih tinggi.
- Bun 1.0 atau lebih baru.
- Cloudflare Workers.
- Vercel Edge Runtime.
- Jest 28 atau lebih besar dengan lingkungan `"node"` (`"jsdom"` tidak didukung saat ini).
- Nitro v2.6 atau lebih besar.
- Browser web: dinonaktifkan secara default untuk menghindari paparan kredensial API rahasia Anda (lihat [praktik terbaik kunci API](https://support.anthropic.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure)). Aktifkan dukungan browser dengan secara eksplisit mengatur `dangerouslyAllowBrowser` ke `true`.

Perhatikan bahwa React Native tidak didukung saat ini.

Jika Anda tertarik dengan lingkungan runtime lain, silakan buka atau dukung masalah di [GitHub](https://github.com/anthropics/anthropic-sdk-typescript).

## Penggunaan

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env["ANTHROPIC_API_KEY"] // Ini adalah default dan dapat dihilangkan
});

const message = await client.messages.create({
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-4-6"
});

console.log(message.content);
```

## Tipe Permintaan & Respons

Perpustakaan ini mencakup definisi TypeScript untuk semua parameter permintaan dan bidang respons. Anda dapat mengimpor dan menggunakannya seperti ini:

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env["ANTHROPIC_API_KEY"] // Ini adalah default dan dapat dihilangkan
});

const params: Anthropic.MessageCreateParams = {
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-4-6"
};
const message: Anthropic.Message = await client.messages.create(params);
```

Dokumentasi untuk setiap metode, parameter permintaan, dan bidang respons tersedia dalam docstring dan akan muncul saat mengarahkan kursor di sebagian besar editor modern.

## Menghitung Token

Anda dapat melihat penggunaan yang tepat untuk permintaan tertentu melalui properti respons `usage`, misalnya

```typescript
const message = await client.messages.create(/* ... */);
console.log(message.usage);
// { input_tokens: 25, output_tokens: 13 }
```

## Respons streaming

Kami menyediakan dukungan untuk respons streaming menggunakan Server Sent Events (SSE).

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const stream = await client.messages.create({
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-4-6",
  stream: true
});
for await (const messageStreamEvent of stream) {
  console.log(messageStreamEvent.type);
}
```

Atau `break` di dalam loop iterasi untuk membatalkan.

## Pembantu Streaming

Perpustakaan ini menyediakan beberapa kemudahan untuk pesan streaming, misalnya:

```typescript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

async function main() {
  const stream = anthropic.messages
    .stream({
      model: "claude-opus-4-6",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "Say hello there!"
        }
      ]
    })
    .on("text", (text) => {
      console.log(text);
    });

  const message = await stream.finalMessage();
  console.log(message);
}

main();
```

Streaming dengan `client.messages.stream(...)` mengekspos berbagai pembantu untuk kenyamanan Anda termasuk penanganan acara dan akumulasi.

Alternatifnya, Anda dapat menggunakan `client.messages.create({ ..., stream: true })` yang hanya mengembalikan iterable asinkron dari acara dalam aliran dan dengan demikian menggunakan lebih sedikit memori (tidak membangun objek pesan akhir untuk Anda).

## Pembantu Alat

SDK ini menyediakan pembantu untuk memudahkan pembuatan dan menjalankan alat di Messages API. Anda dapat menggunakan skema Zod atau JSON Schemas untuk mendeskripsikan input ke alat. Anda kemudian dapat menjalankan alat tersebut menggunakan metode `client.messages.toolRunner()`. Metode ini akan menangani melewatkan input yang dihasilkan oleh model yang dipilih ke alat yang tepat dan melewatkan hasilnya kembali ke model.

Untuk detail lebih lanjut tentang penggunaan alat, lihat [ikhtisar penggunaan alat](/docs/id/agents-and-tools/tool-use/overview).

```typescript
import Anthropic from "@anthropic-ai/sdk";

import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const anthropic = new Anthropic();

const weatherTool = betaZodTool({
  name: "get_weather",
  inputSchema: z.object({
    location: z.string()
  }),
  description: "Get the current weather in a given location",
  run: (input) => {
    return `The weather in ${input.location} is foggy and 60°F`;
  }
});

const finalMessage = await anthropic.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 1000,
  messages: [{ role: "user", content: "What is the weather in San Francisco?" }],
  tools: [weatherTool]
});
```

## Penggunaan alat

SDK ini menyediakan dukungan untuk penggunaan alat, alias pemanggilan fungsi. Detail lebih lanjut dapat ditemukan di [ikhtisar penggunaan alat](/docs/id/agents-and-tools/tool-use/overview).

## Batch Pesan

SDK ini menyediakan dukungan untuk [Message Batches API](/docs/id/build-with-claude/batch-processing) di bawah namespace `client.messages.batches`.

### Membuat batch

Message Batches mengambil array permintaan, di mana setiap objek memiliki pengidentifikasi `custom_id`, dan `params` permintaan yang sama persis dengan Messages API standar:

```typescript
await anthropic.messages.batches.create({
  requests: [
    {
      custom_id: "my-first-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hello, world" }]
      }
    },
    {
      custom_id: "my-second-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hi again, friend" }]
      }
    }
  ]
});
```

### Mendapatkan hasil dari batch

Setelah Message Batch diproses, ditunjukkan oleh `.processing_status === 'ended'`, Anda dapat mengakses hasil dengan `.batches.results()`

```typescript
const results = await anthropic.messages.batches.results(batch_id);
for await (const entry of results) {
  if (entry.result.type === "succeeded") {
    console.log(entry.result.message.content);
  }
}
```

## Unggahan file

Parameter permintaan yang sesuai dengan unggahan file dapat diteruskan dalam berbagai bentuk:

- `File` (atau objek dengan struktur yang sama)
- `fetch` `Response` (atau objek dengan struktur yang sama)
- `fs.ReadStream`
- nilai pengembalian dari pembantu `toFile` kami

Perhatikan bahwa kami merekomendasikan Anda mengatur tipe konten secara eksplisit karena API file tidak akan menyimpulkannya untuk Anda:

```typescript
import fs from "fs";
import Anthropic, { toFile } from "@anthropic-ai/sdk";

const client = new Anthropic();

// Jika Anda memiliki akses ke Node `fs` kami merekomendasikan menggunakan `fs.createReadStream()`:
await client.beta.files.upload({
  file: await toFile(fs.createReadStream("/path/to/file"), undefined, { type: "application/json" }),
  betas: ["files-api-2025-04-14"]
});

// Atau jika Anda memiliki web `File` API Anda dapat melewatkan instance `File`:
await client.beta.files.upload({
  file: new File(["my bytes"], "file.txt", { type: "text/plain" }),
  betas: ["files-api-2025-04-14"]
});
// Anda juga dapat melewatkan `fetch` `Response`:
await client.beta.files.upload({
  file: await fetch("https://somesite/file"),
  betas: ["files-api-2025-04-14"]
});

// Atau `Buffer` / `Uint8Array`
await client.beta.files.upload({
  file: await toFile(Buffer.from("my bytes"), "file", { type: "text/plain" }),
  betas: ["files-api-2025-04-14"]
});
await client.beta.files.upload({
  file: await toFile(new Uint8Array([0, 1, 2]), "file", { type: "text/plain" }),
  betas: ["files-api-2025-04-14"]
});
```

## Menangani kesalahan

Ketika perpustakaan tidak dapat terhubung ke API,
atau jika API mengembalikan kode status non-sukses (yaitu, respons 4xx atau 5xx),
subkelas `APIError` akan dilempar:

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const message = await client.messages
  .create({
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-4-6"
  })
  .catch(async (err) => {
    if (err instanceof Anthropic.APIError) {
      console.log(err.status); // 400
      console.log(err.name); // BadRequestError
      console.log(err.headers); // {server: 'nginx', ...}
    } else {
      throw err;
    }
  });
```

Kode kesalahan adalah sebagai berikut:

| Kode Status | Tipe Kesalahan              |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

## ID Permintaan

> Untuk informasi lebih lanjut tentang debugging permintaan, lihat [dokumen ini](/docs/id/api/errors#request-id)

Semua respons objek dalam SDK menyediakan properti `_request_id` yang ditambahkan dari header respons `request-id` sehingga Anda dapat dengan cepat mencatat permintaan yang gagal dan melaporkannya kembali ke Anthropic.

```typescript
const message = await client.messages.create({
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-4-6"
});
console.log(message._request_id); // req_018EeWyXxfu5pfWkrYcMdjWG
```

## Percobaan Ulang

Kesalahan tertentu akan secara otomatis dicoba ulang 2 kali secara default, dengan backoff eksponensial pendek.
Kesalahan koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict,
429 Rate Limit, dan >=500 kesalahan Internal semuanya akan dicoba ulang secara default.

Anda dapat menggunakan opsi `maxRetries` untuk mengonfigurasi atau menonaktifkan ini:

```typescript
// Konfigurasi default untuk semua permintaan:
const client = new Anthropic({
  maxRetries: 0 // default adalah 2
});

// Atau, konfigurasi per-permintaan:
await client.messages.create({ max_tokens: 1024, messages: [{ role: "user", content: "Hello, Claude" }], model: "claude-opus-4-6" }, {
  maxRetries: 5
});
```

## Batas Waktu

Secara default permintaan habis waktu setelah 10 menit. Namun jika Anda telah menentukan nilai `max_tokens` besar dan _tidak_ streaming, batas waktu default akan dihitung secara dinamis menggunakan rumus:

```typescript
const minimum = 10 * 60;
const calculated = (60 * 60 * maxTokens) / 128_000;
return calculated < minimum ? minimum * 1000 : calculated * 1000;
```

yang akan menghasilkan batas waktu hingga 60 menit, diskalakan oleh parameter `max_tokens`, kecuali ditimpa di tingkat permintaan atau klien.

Anda dapat mengonfigurasi ini dengan opsi `timeout`:

```typescript
// Konfigurasi default untuk semua permintaan:
const client = new Anthropic({
  timeout: 20 * 1000 // 20 detik (default adalah 10 menit)
});

// Timpa per-permintaan:
await client.messages.create({ max_tokens: 1024, messages: [{ role: "user", content: "Hello, Claude" }], model: "claude-opus-4-6" }, {
  timeout: 5 * 1000
});
```

Saat batas waktu, `APIConnectionTimeoutError` dilempar.

Perhatikan bahwa permintaan yang habis waktu akan [dicoba ulang dua kali secara default](#retries).

## Permintaan Panjang

<Warning>
Kami sangat mendorong Anda menggunakan [Messages API](#streaming-responses) streaming untuk permintaan yang berjalan lebih lama.
</Warning>

Kami tidak merekomendasikan pengaturan nilai `max_tokens` besar tanpa menggunakan streaming.
Beberapa jaringan dapat menghapus koneksi idle setelah periode waktu tertentu, yang
dapat menyebabkan permintaan gagal atau [habis waktu](#timeouts) tanpa menerima respons dari Anthropic.

SDK ini juga akan melempar kesalahan jika permintaan non-streaming diharapkan lebih lama dari kira-kira 10 menit.
Melewatkan `stream: true` atau [menimpa](#timeouts) opsi `timeout` di tingkat klien atau permintaan menonaktifkan kesalahan ini.

Latensi permintaan yang diharapkan lebih lama dari [batas waktu](#timeouts) untuk permintaan non-streaming
akan menghasilkan klien mengakhiri koneksi dan mencoba ulang tanpa menerima respons.

Ketika didukung oleh implementasi `fetch`, kami mengatur opsi [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/overview.html) untuk mengurangi dampak batas waktu koneksi idle pada beberapa jaringan.
Ini dapat [ditimpa](#configuring-proxies) dengan mengonfigurasi proxy khusus.

## Paginasi Otomatis

Metode daftar di Claude API dipaginasi.
Anda dapat menggunakan sintaks `for await ... of` untuk mengulangi item di semua halaman:

```typescript
async function fetchAllMessageBatches(params) {
  const allMessageBatches = [];
  // Secara otomatis mengambil lebih banyak halaman sesuai kebutuhan.
  for await (const messageBatch of client.messages.batches.list({ limit: 20 })) {
    allMessageBatches.push(messageBatch);
  }
  return allMessageBatches;
}
```

Alternatifnya, Anda dapat meminta satu halaman sekaligus:

```typescript
let page = await client.messages.batches.list({ limit: 20 });
for (const messageBatch of page.data) {
  console.log(messageBatch);
}

// Metode kenyamanan disediakan untuk paginasi manual:
while (page.hasNextPage()) {
  page = await page.getNextPage();
  // ...
}
```

## Header Default

Kami secara otomatis mengirim header `anthropic-version` yang ditetapkan ke `2023-06-01`.

Jika perlu, Anda dapat menimpanya dengan mengatur header default berdasarkan per-permintaan.

Perhatikan bahwa melakukan hal ini dapat menghasilkan tipe yang tidak benar dan perilaku yang tidak terduga atau tidak ditentukan lainnya dalam SDK.

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const message = await client.messages.create(
  {
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-4-6"
  },
  { headers: { "anthropic-version": "My-Custom-Value" } }
);
```

## Penggunaan Lanjutan

### Mengakses data Response mentah (misalnya, header)

`Response` "mentah" yang dikembalikan oleh `fetch()` dapat diakses melalui metode `.asResponse()` pada tipe `APIPromise` yang semua metode kembalikan.
Metode ini mengembalikan segera setelah header untuk respons yang berhasil diterima dan tidak mengonsumsi badan respons, jadi Anda bebas menulis logika parsing atau streaming khusus.

Anda juga dapat menggunakan metode `.withResponse()` untuk mendapatkan `Response` mentah bersama dengan data yang diurai.
Tidak seperti `.asResponse()` metode ini mengonsumsi badan, mengembalikan setelah diurai.

```typescript
const client = new Anthropic();

const response = await client.messages
  .create({
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-4-6"
  })
  .asResponse();
console.log(response.headers.get("X-My-Header"));
console.log(response.statusText); // akses objek Response yang mendasar

const { data: message, response: raw } = await client.messages
  .create({
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-4-6"
  })
  .withResponse();
console.log(raw.headers.get("X-My-Header"));
console.log(message.content);
```

### Pencatatan

<Warning>
Semua pesan log dimaksudkan hanya untuk debugging. Format dan konten pesan log
dapat berubah antar rilis.
</Warning>

#### Tingkat log

Tingkat log dapat dikonfigurasi dengan dua cara:

1. Melalui variabel lingkungan `ANTHROPIC_LOG`
2. Menggunakan opsi klien `logLevel` (menimpa variabel lingkungan jika diatur)

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  logLevel: "debug" // Tampilkan semua pesan log
});
```

Tingkat log yang tersedia, dari paling ke paling tidak verbose:

- `'debug'` - Tampilkan pesan debug, info, peringatan, dan kesalahan
- `'info'` - Tampilkan pesan info, peringatan, dan kesalahan
- `'warn'` - Tampilkan peringatan dan kesalahan (default)
- `'error'` - Tampilkan hanya kesalahan
- `'off'` - Nonaktifkan semua pencatatan

Pada tingkat `'debug'`, semua permintaan dan respons HTTP dicatat, termasuk header dan badan.
Beberapa header terkait autentikasi diredaksi, tetapi data sensitif dalam permintaan dan badan respons
mungkin masih terlihat.

#### Logger khusus

Secara default, perpustakaan ini mencatat ke `globalThis.console`. Anda juga dapat menyediakan logger khusus.
Sebagian besar perpustakaan logging didukung, termasuk [pino](https://www.npmjs.com/package/pino), [winston](https://www.npmjs.com/package/winston), [bunyan](https://www.npmjs.com/package/bunyan), [consola](https://www.npmjs.com/package/consola), [signale](https://www.npmjs.com/package/signale), dan [@std/log](https://jsr.io/@std/log). Jika logger Anda tidak berfungsi, silakan buka masalah.

Saat menyediakan logger khusus, opsi `logLevel` masih mengontrol pesan mana yang dipancarkan, pesan
di bawah tingkat yang dikonfigurasi tidak akan dikirim ke logger Anda.

```typescript
import Anthropic from "@anthropic-ai/sdk";
import pino from "pino";

const logger = pino();

const client = new Anthropic({
  logger: logger.child({ name: "Anthropic" }),
  logLevel: "debug" // Kirim semua pesan ke pino, memungkinkannya untuk memfilter
});
```

### Membuat permintaan khusus/tidak terdokumentasi

Perpustakaan ini diketik untuk akses yang mudah ke API yang terdokumentasi. Jika Anda perlu mengakses titik akhir,
parameter, atau properti respons yang tidak terdokumentasi, perpustakaan masih dapat digunakan.

#### Titik akhir yang tidak terdokumentasi

Untuk membuat permintaan ke titik akhir yang tidak terdokumentasi, Anda dapat menggunakan `client.get`, `client.post`, dan kata kerja HTTP lainnya.
Opsi pada klien, seperti percobaan ulang, akan dihormati saat membuat permintaan ini.

```typescript
await client.post("/some/path", {
  body: { some_prop: "foo" },
  query: { some_query_arg: "bar" }
});
```

#### Parameter permintaan yang tidak terdokumentasi

Untuk membuat permintaan menggunakan parameter yang tidak terdokumentasi, Anda dapat menggunakan `// @ts-expect-error` pada parameter yang tidak terdokumentasi. Perpustakaan ini tidak memvalidasi pada waktu runtime bahwa permintaan cocok dengan tipe, jadi nilai tambahan apa pun yang Anda kirim akan dikirim apa adanya.

```typescript
client.messages.create({
  // ...
  // @ts-expect-error baz belum publik
  baz: "undocumented option"
});
```

Untuk permintaan dengan kata kerja `GET`, parameter tambahan apa pun akan berada dalam kueri, semua permintaan lain akan mengirim parameter tambahan dalam badan.

Jika Anda ingin secara eksplisit mengirim argumen tambahan, Anda dapat melakukannya dengan opsi permintaan `query`, `body`, dan `headers`.

#### Properti respons yang tidak terdokumentasi

Untuk mengakses properti respons yang tidak terdokumentasi, Anda dapat mengakses objek respons dengan `// @ts-expect-error` pada objek respons, atau mentransmisikan objek respons ke tipe yang diperlukan. Seperti parameter permintaan, kami tidak memvalidasi atau menghapus properti tambahan dari respons dari API.

### Menyesuaikan klien fetch

Secara default, perpustakaan ini mengharapkan fungsi `fetch` global didefinisikan.

Jika Anda ingin menggunakan fungsi `fetch` yang berbeda, Anda dapat mempolyfill global:

```typescript
import fetch from "my-fetch";

globalThis.fetch = fetch;
```

Atau teruskan ke klien:

```typescript
import Anthropic from "@anthropic-ai/sdk";
import fetch from "my-fetch";

const client = new Anthropic({ fetch });
```

### Opsi Fetch

Jika Anda ingin mengatur opsi `fetch` khusus tanpa menimpa fungsi `fetch`, Anda dapat menyediakan objek `fetchOptions` saat membuat instance klien atau membuat permintaan. (Opsi khusus permintaan menimpa opsi klien.)

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  fetchOptions: {
    // opsi `RequestInit`
  }
});
```

### Mengonfigurasi proxy

Untuk memodifikasi perilaku proxy, Anda dapat menyediakan `fetchOptions` khusus yang menambahkan opsi proxy khusus runtime ke permintaan:

<Tabs>
<Tab title="Node.js">
```typescript
import Anthropic from "@anthropic-ai/sdk";
import * as undici from "undici";

const proxyAgent = new undici.ProxyAgent("http://localhost:8888");
const client = new Anthropic({
  fetchOptions: {
    dispatcher: proxyAgent
  }
});
```
</Tab>
<Tab title="Bun">
```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  fetchOptions: {
    proxy: "http://localhost:8888"
  }
});
```
</Tab>
<Tab title="Deno">
```typescript
import Anthropic from "npm:@anthropic-ai/sdk";

const httpClient = Deno.createHttpClient({ proxy: { url: "http://localhost:8888" } });
const client = new Anthropic({
  fetchOptions: {
    client: httpClient
  }
});
```
</Tab>
</Tabs>

## Fitur Beta

Kami memperkenalkan fitur beta sebelum tersedia secara umum untuk mendapatkan umpan balik awal dan menguji fungsionalitas baru. Anda dapat memeriksa ketersediaan semua kemampuan dan alat Claude di [ikhtisar build with Claude](/docs/id/build-with-claude/overview).

Anda dapat mengakses sebagian besar fitur API beta melalui properti beta klien. Untuk mengaktifkan fitur beta tertentu, Anda perlu menambahkan [header beta](/docs/id/api/beta-headers) yang sesuai ke bidang `betas` saat membuat pesan.

Misalnya, untuk menggunakan [Files API](/docs/id/build-with-claude/files):

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const response = await client.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        { type: "text", text: "Please summarize this document for me." },
        {
          type: "document",
          source: {
            type: "file",
            file_id: "file_abc123"
          }
        }
      ]
    }
  ],
  betas: ["files-api-2025-04-14"]
});
```

## Dukungan runtime

<section title="Penggunaan browser">

Mengaktifkan opsi `dangerouslyAllowBrowser` dapat berbahaya karena mengekspos kredensial API rahasia Anda dalam kode sisi klien. Browser web secara inheren kurang aman daripada lingkungan server, pengguna mana pun dengan akses ke browser dapat berpotensi memeriksa, mengekstrak, dan menyalahgunakan kredensial ini. Ini dapat menyebabkan akses tidak sah menggunakan kredensial Anda dan berpotensi membahayakan data atau fungsionalitas sensitif.

**Kapan ini mungkin tidak berbahaya?**

Dalam skenario tertentu di mana mengaktifkan dukungan browser mungkin tidak menimbulkan risiko signifikan:

- **Alat Internal:** Jika aplikasi digunakan hanya dalam lingkungan internal yang terkontrol di mana pengguna dipercaya, risiko paparan kredensial dapat dimitigasi.
- **Tujuan pengembangan atau debugging:** Mengaktifkan fitur ini secara sementara mungkin dapat diterima, asalkan kredensial berumur pendek, tidak juga digunakan di lingkungan produksi, atau sering dirotasi.

</section>

## Integrasi platform

<Note>
Untuk panduan penyiapan platform terperinci, lihat:
- [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock)
- [Google Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)
- [Microsoft Azure / Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry)
</Note>

### Amazon Bedrock

Kami menyediakan dukungan untuk [Anthropic Bedrock API](https://aws.amazon.com/bedrock/claude/) melalui paket terpisah.

```bash
npm install @anthropic-ai/bedrock-sdk
```

```typescript
import { AnthropicBedrock } from "@anthropic-ai/bedrock-sdk";

const client = new AnthropicBedrock();

const message = await client.messages.create({
  model: "anthropic.claude-opus-4-6-v1",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }]
});
```

### Google Vertex AI

Kami menyediakan dukungan untuk [Anthropic Vertex AI API](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) melalui paket terpisah.

```bash
npm install @anthropic-ai/vertex-sdk
```

```typescript
import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

const client = new AnthropicVertex();

const message = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }]
});
```

### Microsoft Azure / Foundry

Untuk informasi tentang menggunakan Claude melalui Microsoft Azure dan Azure AI Foundry, lihat [Claude in Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

## Pertanyaan yang Sering Diajukan

Lihat [repositori GitHub](https://github.com/anthropics/anthropic-sdk-typescript) untuk FAQ, masalah, dan dukungan komunitas.

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-typescript)
- [Referensi API](/docs/id/api/overview)
- [Panduan streaming](/docs/id/build-with-claude/streaming)
- [Panduan penggunaan alat](/docs/id/agents-and-tools/tool-use/overview)