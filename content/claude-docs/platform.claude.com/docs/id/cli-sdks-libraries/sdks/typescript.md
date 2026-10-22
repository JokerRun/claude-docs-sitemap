---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript
fetched_at: 2026-10-22T02:21:21.745661Z
sha256: 554cae492d4776865bd7f46ff1fa9305c52a5e66249703022b5c64254f7061fe
---

---
title: TypeScript SDK
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript
description: Instal dan konfigurasikan Anthropic TypeScript SDK untuk lingkungan Node.js, Deno, Bun, dan browser
---

Library ini menyediakan akses yang mudah ke Claude API dari TypeScript atau JavaScript.

<Info>
  Untuk dokumentasi fitur API beserta contoh kode, lihat [referensi API](https://platform.claude.com/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK yang khusus untuk TypeScript.
</Info>

## Instalasi

```bash
npm install @anthropic-ai/sdk
```

## Persyaratan

TypeScript >= 5.0 didukung.

Runtime berikut didukung:

* Node.js 20 LTS atau versi yang lebih baru ([non-EOL](https://endoflife.date/nodejs)).
* Deno v1.28.0 atau lebih tinggi.
* Bun 1.0 atau lebih baru.
* Cloudflare Workers.
* Vercel Edge Runtime.
* Jest 28 atau lebih tinggi dengan lingkungan `"node"` (`"jsdom"` saat ini tidak didukung).
* Nitro v2.6 atau lebih tinggi.
* Browser web: dinonaktifkan secara default untuk menghindari terpaparnya kredensial API rahasia Anda (lihat [praktik terbaik kunci API](https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure)). Aktifkan dukungan browser dengan secara eksplisit mengatur `dangerouslyAllowBrowser` ke `true`.

Perhatikan bahwa React Native saat ini tidak didukung.

Jika Anda tertarik dengan lingkungan runtime lain, buka atau berikan upvote pada issue di [repositori GitHub](https://github.com/anthropics/anthropic-sdk-typescript).

## Penggunaan

```typescript
const client = new Anthropic({
  apiKey: process.env["ANTHROPIC_API_KEY"] // This is the default and can be omitted
});

const message = await client.messages.create({
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-5-5"
});

for (const block of message.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

Untuk opsi autentikasi termasuk Workload Identity Federation, lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication). Jika kunci API Anda adalah [kunci personal atau kunci akun layanan](https://platform.claude.com/docs/id/manage-claude/authentication#key-types) dengan akses ke beberapa workspace, tetapkan ID workspace di header permintaan `anthropic-workspace-id`; [Pilih workspace](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace) menunjukkan opsi per permintaan untuk SDK ini.

## Tipe request dan response

Library ini menyertakan definisi TypeScript untuk semua parameter request dan field response. Anda dapat mengimpor dan menggunakannya seperti ini:

```typescript
const client = new Anthropic({
  apiKey: process.env["ANTHROPIC_API_KEY"] // This is the default and can be omitted
});

const params: Anthropic.MessageCreateParams = {
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-5-5"
};
const message: Anthropic.Message = await client.messages.create(params);
```

Dokumentasi untuk setiap metode, parameter request, dan field response tersedia dalam docstring dan muncul saat hover di sebagian besar editor modern.

## Menghitung token

Anda dapat melihat penggunaan yang tepat untuk request tertentu melalui properti response `usage`, misalnya:

```typescript
const message = await client.messages.create({
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-5-5"
});
console.log(message.usage);
// { input_tokens: 25, output_tokens: 13 }
```

## Streaming response

SDK menyediakan dukungan untuk streaming response menggunakan "Server-Sent Events" (peristiwa yang dikirim server), atau SSE.

```typescript
const client = new Anthropic();

const stream = await client.messages.create({
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-5-5",
  stream: true
});
for await (const messageStreamEvent of stream) {
  console.log(messageStreamEvent.type);
}
```

Jika Anda perlu membatalkan stream, Anda dapat melakukan `break` dari loop atau memanggil `stream.controller.abort()`.

## Helper streaming

Library ini menyediakan beberapa kemudahan untuk streaming pesan, misalnya:

```typescript
const anthropic = new Anthropic();

const stream = anthropic.messages
  .stream({
    model: "claude-opus-5-5",
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
```

Streaming dengan `client.messages.stream(...)` menyediakan berbagai helper untuk kemudahan Anda, termasuk event handler dan akumulasi.

Sebagai alternatif, Anda dapat menggunakan `client.messages.create({ ..., stream: true })` yang hanya mengembalikan async iterable dari event dalam stream sehingga menggunakan lebih sedikit memori (metode ini tidak membangun objek pesan akhir untuk Anda).

## Helper alat

SDK ini menyediakan helper untuk memudahkan pembuatan dan menjalankan alat di Messages API. Anda dapat menggunakan skema Zod atau JSON Schema untuk mendeskripsikan input ke sebuah alat. Anda kemudian dapat menjalankan alat tersebut menggunakan metode `client.beta.messages.toolRunner()`. Metode ini menangani penerusan input yang dihasilkan oleh model yang dipilih ke alat yang tepat dan meneruskan hasilnya kembali ke model.

Untuk detail lebih lanjut tentang penggunaan alat, lihat [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview). Untuk menjalankan alat browser use atau alat computer use dengan SDK ini, lihat [Browser dan computer use dengan toolset SDK](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk).

```typescript
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
  model: "claude-opus-5-5",
  max_tokens: 1000,
  messages: [{ role: "user", content: "What is the weather in San Francisco?" }],
  tools: [weatherTool]
});

console.log(finalMessage.content);
```

### Error alat

Untuk melaporkan error dari sebuah alat kembali ke model, lemparkan `ToolError` dari fungsi `run`. Tidak seperti `Error` biasa, `ToolError` menerima content block, sehingga Anda dapat menyertakan gambar atau konten terstruktur lainnya dalam response error:

```typescript
import { ToolError } from "@anthropic-ai/sdk/lib/tools/BetaRunnableTool";

const screenshotTool = betaZodTool({
  name: "take_screenshot",
  inputSchema: z.object({ url: z.string() }),
  run: async (input) => {
    if (!isValidUrl(input.url)) {
      throw new ToolError(`Invalid URL: ${input.url}`);
    }
    const result = await takeScreenshot(input.url);
    if (result.error) {
      // Sertakan screenshot error agar model dapat melihat apa yang salah
      throw new ToolError([
        { type: "text", text: `Failed to load page: ${result.error}` },
        {
          type: "image",
          source: { type: "base64", data: result.screenshot, media_type: "image/png" }
        }
      ]);
    }
    return {
      type: "image",
      source: { type: "base64", data: result.screenshot, media_type: "image/png" }
    };
  }
});
```

Jika `Error` biasa yang dilemparkan, pesannya akan dikonversi menjadi content block teks.

## Penggunaan alat

SDK ini menyediakan dukungan untuk penggunaan alat, yang juga dikenal sebagai "function calling" (pemanggilan fungsi). Untuk detail lebih lanjut, lihat [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview).

## Helper MCP

SDK ini menyediakan helper untuk integrasi dengan server [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). Helper ini mengonversi tipe MCP ke tipe Claude API, mengurangi boilerplate saat bekerja dengan alat, prompt, dan resource MCP.

<Tip>
  Claude API juga mendukung [parameter `mcp_servers`](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector) yang memungkinkan Claude terhubung langsung ke server MCP jarak jauh. Gunakan `mcp_servers` ketika Anda memiliki server jarak jauh yang dapat diakses melalui URL dan hanya memerlukan dukungan alat. Gunakan helper MCP ketika Anda memerlukan server MCP lokal, prompt, resource, atau kontrol lebih atas koneksi MCP.
</Tip>

```typescript
import {
  mcpTools,
  mcpMessages,
  mcpResourceToContent,
  mcpResourceToFile
} from "@anthropic-ai/sdk/helpers/beta/mcp";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const anthropic = new Anthropic();

// Hubungkan ke server MCP
const transport = new StdioClientTransport({ command: "mcp-server", args: [] });
const mcpClient = new Client({ name: "my-client", version: "1.0.0" });
await mcpClient.connect(transport);

// Gunakan prompt MCP
const { messages } = await mcpClient.getPrompt({ name: "my-prompt" });
const response = await anthropic.beta.messages.create({
  model: "claude-opus-5-5",
  max_tokens: 1024,
  messages: mcpMessages(messages)
});
console.log(response.content);

// Gunakan alat MCP dengan toolRunner
const { tools } = await mcpClient.listTools();
const finalMessage = await anthropic.beta.messages.toolRunner({
  model: "claude-opus-5-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Use the available tools" }],
  tools: mcpTools(tools, mcpClient)
});
console.log(finalMessage.content);

// Gunakan resource MCP sebagai konten
const resource = await mcpClient.readResource({ uri: "file:///path/to/doc.txt" });
await anthropic.beta.messages.create({
  model: "claude-opus-5-5",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        mcpResourceToContent(resource),
        { type: "text", text: "Summarize this document" }
      ]
    }
  ]
});

// Unggah resource MCP sebagai file
const fileResource = await mcpClient.readResource({ uri: "file:///path/to/data.json" });
await anthropic.files.upload({ file: mcpResourceToFile(fileResource) });
```

### Penanganan error MCP

Fungsi konversi melemparkan `UnsupportedMCPValueError` jika nilai MCP tidak didukung oleh Claude API (misalnya, tipe konten yang tidak didukung, tipe MIME yang tidak didukung, tautan resource non-HTTP/HTTPS).

## Message batch

SDK ini menyediakan dukungan untuk [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) di bawah namespace `client.messages.batches`.

### Membuat batch

Message Batches menerima array request, di mana setiap objek memiliki identifier `custom_id`, dan `params` request yang sama persis dengan Messages API standar:

```typescript
const batch = await client.messages.batches.create({
  requests: [
    {
      custom_id: "my-first-request",
      params: {
        model: "claude-opus-5-5",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hello, world" }]
      }
    },
    {
      custom_id: "my-second-request",
      params: {
        model: "claude-opus-5-5",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hi again, friend" }]
      }
    }
  ]
});
```

### Mendapatkan hasil dari batch

Setelah Message Batch selesai diproses, yang ditandai dengan `.processing_status === 'ended'`, Anda dapat mengakses hasilnya dengan `.batches.results()`

```typescript
const results = await client.messages.batches.results(batch.id);
for await (const entry of results) {
  if (entry.result.type === "succeeded") {
    console.log(entry.result.message.content);
  }
}
```

## Unggahan file

Parameter request yang berkaitan dengan unggahan file dapat diteruskan dalam berbagai bentuk:

* `File` (atau objek dengan struktur yang sama)
* `Response` dari `fetch` (atau objek dengan struktur yang sama)
* `fs.ReadStream`
* nilai kembalian dari helper `toFile`

Atur tipe konten secara eksplisit karena Files API tidak akan menyimpulkannya untuk Anda:

```typescript
import fs from "node:fs";
import Anthropic, { toFile } from "@anthropic-ai/sdk";

const client = new Anthropic();

// Jika Anda memiliki akses ke Node `fs`, gunakan `fs.createReadStream()`:
await client.files.upload({
  file: await toFile(fs.createReadStream("/path/to/file"), undefined, {
    type: "application/json"
  })
});

// Atau jika Anda memiliki API web `File`, Anda dapat meneruskan instans `File`:
await client.files.upload({
  file: new File(["my bytes"], "file.txt", { type: "text/plain" })
});
// Anda juga dapat meneruskan `Response` dari `fetch`:
await client.files.upload({
  file: await fetch("https://somesite/file")
});

// Atau `Buffer` / `Uint8Array`
await client.files.upload({
  file: await toFile(Buffer.from("my bytes"), "file", { type: "text/plain" })
});
await client.files.upload({
  file: await toFile(new Uint8Array([0, 1, 2]), "file", { type: "text/plain" })
});
```

## Menangani error

Ketika library tidak dapat terhubung ke API, atau jika API mengembalikan kode status yang tidak sukses (yaitu, response 4xx atau 5xx), subclass dari `APIError` akan dilemparkan:

```typescript
const message = await client.messages
  .create({
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-5-5"
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

Kode error adalah sebagai berikut:

| Kode status | Tipe error                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 409         | `ConflictError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

## Request ID

> Untuk informasi lebih lanjut tentang debugging request, lihat [Request ID](https://platform.claude.com/docs/id/api/errors#request-id).

Semua response objek di SDK menyediakan properti `_request_id` yang ditambahkan dari header response `request-id` sehingga Anda dapat dengan cepat mencatat request yang gagal dan melaporkannya kembali ke Anthropic.

```typescript
const message = await client.messages.create({
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-5-5"
});
console.log(message._request_id); // req_018EeWyXxfu5pfWkrYcMdjWG
```

## Percobaan ulang

Error tertentu secara otomatis dicoba ulang 2 kali secara default, dengan "exponential backoff" (jeda eksponensial) yang singkat. Error koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict, 429 Rate Limit, dan error Internal >=500 semuanya dicoba ulang secara default.

Anda dapat menggunakan opsi `maxRetries` untuk mengonfigurasi atau menonaktifkan ini:

```typescript
// Konfigurasikan default untuk semua permintaan:
const client = new Anthropic({
  maxRetries: 0 // default is 2
});

// Atau, konfigurasikan per permintaan:
await client.messages.create(
  {
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-5-5"
  },
  { maxRetries: 5 }
);
```

## Timeout

Secara default, request akan timeout setelah 10 menit. Namun, jika Anda telah menentukan nilai `max_tokens` yang besar dan *tidak* menggunakan streaming, timeout default akan dihitung secara dinamis menggunakan rumus:

```typescript
const minimum = 10 * 60;
const calculated = (60 * 60 * maxTokens) / 128_000;
return calculated < minimum ? minimum * 1000 : calculated * 1000;
```

yang akan menghasilkan timeout hingga 60 menit, diskalakan berdasarkan parameter `max_tokens`, kecuali di-override pada tingkat request atau client.

Anda dapat mengonfigurasi ini dengan opsi `timeout`:

```typescript
// Konfigurasikan nilai default untuk semua permintaan:
const client = new Anthropic({
  timeout: 20 * 1000 // 20 seconds (default is 10 minutes)
});

// Timpa per permintaan:
await client.messages.create(
  {
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-5-5"
  },
  { timeout: 5 * 1000 }
);
```

Saat timeout, `APIConnectionTimeoutError` akan dilemparkan.

Perhatikan bahwa request yang mengalami timeout akan [dicoba ulang dua kali secara default](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript#retries).

## Request panjang

<Warning>
  Pertimbangkan untuk menggunakan streaming [Messages API](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript#streaming-responses) untuk request yang berjalan lebih lama.
</Warning>

Hindari mengatur nilai `max_tokens` yang besar tanpa menggunakan streaming. Beberapa jaringan mungkin memutus koneksi idle setelah periode waktu tertentu, yang dapat menyebabkan request gagal atau [timeout](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript#timeouts) tanpa menerima response dari Anthropic.

SDK ini juga melemparkan error jika request non-streaming diperkirakan berlangsung lebih dari sekitar 10 menit. Meneruskan `stream: true` atau [meng-override](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript#timeouts) opsi `timeout` pada tingkat client atau request akan menonaktifkan error ini.

Latensi request yang diperkirakan lebih lama dari [timeout](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript#timeouts) untuk request non-streaming akan mengakibatkan client memutus koneksi dan mencoba ulang tanpa menerima response.

Ketika didukung oleh implementasi `fetch`, SDK mengatur opsi [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/overview.html) untuk mengurangi dampak timeout koneksi idle pada beberapa jaringan. Ini dapat [di-override](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript#configuring-proxies) dengan mengonfigurasi proxy kustom.

## Paginasi otomatis

Metode list di Claude API menggunakan paginasi. Anda dapat menggunakan sintaks `for await ... of` untuk melakukan iterasi item di semua halaman:

```typescript
async function fetchAllMessageBatches() {
  const allMessageBatches = [];
  // Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for await (const messageBatch of client.messages.batches.list({ limit: 20 })) {
    allMessageBatches.push(messageBatch);
  }
  return allMessageBatches;
}
```

Sebagai alternatif, Anda dapat meminta satu halaman pada satu waktu:

```typescript
let page = await client.messages.batches.list({ limit: 20 });
for (const messageBatch of page.data) {
  console.log(messageBatch);
}

// Metode praktis disediakan untuk melakukan paginasi secara manual:
while (page.hasNextPage()) {
  page = await page.getNextPage();
  // ...
}
```

## Header default

SDK secara otomatis mengirimkan header `anthropic-version` yang diatur ke versi API untuk versi mayor SDK ini (lihat [Semantic versioning](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript#semantic-versioning)).

Jika perlu, Anda dapat meng-override-nya dengan mengatur header default per request.

Perlu diketahui bahwa melakukan hal tersebut dapat mengakibatkan tipe yang salah dan perilaku tak terduga atau tidak terdefinisi lainnya di SDK.

```typescript
const client = new Anthropic();

const message = await client.messages.create(
  {
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-5-5"
  },
  { headers: { "anthropic-version": "My-Custom-Value" } }
);
```

## Penggunaan lanjutan

### Mengakses data Response mentah (misalnya, header)

`Response` "mentah" yang dikembalikan oleh `fetch()` dapat diakses melalui metode `.asResponse()` pada tipe `APIPromise` yang dikembalikan oleh semua metode. Metode ini langsung kembali segera setelah header untuk response yang sukses diterima dan tidak mengonsumsi body response, sehingga Anda bebas menulis logika parsing atau streaming kustom.

Anda juga dapat menggunakan metode `.withResponse()` untuk mendapatkan `Response` mentah beserta data yang telah di-parse. Tidak seperti `.asResponse()`, metode ini mengonsumsi body, dan kembali setelah body di-parse.

```typescript
const client = new Anthropic();

const response = await client.messages
  .create({
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-5-5"
  })
  .asResponse();
console.log(response.headers.get("X-My-Header"));
console.log(response.statusText); // access the underlying Response object

const { data: message, response: raw } = await client.messages
  .create({
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-5-5"
  })
  .withResponse();
console.log(raw.headers.get("X-My-Header"));
console.log(message.content);
```

### Logging

<Warning>
  Semua pesan log ditujukan hanya untuk debugging. Format dan konten pesan log dapat berubah antar rilis.
</Warning>

#### Level log

Anda dapat mengonfigurasi level log dengan dua cara:

1. Melalui variabel lingkungan `ANTHROPIC_LOG`
2. Menggunakan opsi client `logLevel` (meng-override variabel lingkungan jika diatur)

```typescript
const client = new Anthropic({
  logLevel: "debug" // Show all log messages
});
```

Level log yang tersedia, dari yang paling verbose hingga paling sedikit:

* `'debug'` - Menampilkan pesan debug, info, peringatan, dan error
* `'info'` - Menampilkan pesan info, peringatan, dan error
* `'warn'` - Menampilkan peringatan dan error (default)
* `'error'` - Hanya menampilkan error
* `'off'` - Menonaktifkan semua logging

Pada level `'debug'`, semua request dan response HTTP dicatat, termasuk header dan body. Beberapa header terkait autentikasi disamarkan, tetapi data sensitif dalam body request dan response mungkin masih terlihat.

#### Logger kustom

Secara default, library ini mencatat log ke `globalThis.console`. Anda juga dapat menyediakan logger kustom. Sebagian besar library logging didukung, termasuk [pino](https://www.npmjs.com/package/pino), [winston](https://www.npmjs.com/package/winston), [bunyan](https://www.npmjs.com/package/bunyan), [consola](https://www.npmjs.com/package/consola), [signale](https://www.npmjs.com/package/signale), dan [@std/log](https://jsr.io/@std/log). Jika logger Anda tidak berfungsi, buka issue.

Saat menyediakan logger kustom, opsi `logLevel` tetap mengontrol pesan mana yang dikeluarkan; pesan di bawah level yang dikonfigurasi tidak akan dikirim ke logger Anda.

```typescript
import pino from "pino";

const logger = pino();

const client = new Anthropic({
  logger: logger.child({ name: "Anthropic" }),
  logLevel: "debug" // Send all messages to pino, allowing it to filter
});
```

### Membuat request kustom/tidak terdokumentasi

Library ini diberi tipe untuk akses yang mudah ke API yang terdokumentasi. Jika Anda perlu mengakses endpoint, parameter, atau properti response yang tidak terdokumentasi, library ini tetap dapat digunakan.

#### Endpoint tidak terdokumentasi

Untuk membuat request ke endpoint yang tidak terdokumentasi, Anda dapat menggunakan `client.get`, `client.post`, dan verb HTTP lainnya. Opsi pada client, seperti percobaan ulang, tetap dihormati saat membuat request ini.

```typescript
await client.post("/some/path", {
  body: { some_prop: "foo" },
  query: { some_query_arg: "bar" }
});
```

#### Parameter request tidak terdokumentasi

Untuk membuat request menggunakan parameter yang tidak terdokumentasi, Anda dapat menggunakan `// @ts-expect-error` pada parameter yang tidak terdokumentasi tersebut. Library ini tidak memvalidasi saat runtime bahwa request sesuai dengan tipenya, sehingga nilai tambahan apa pun yang Anda kirim akan dikirim apa adanya.

```typescript
client.messages.create({
  // ...
  // @ts-expect-error baz is not yet public
  baz: "undocumented option"
});
```

Untuk request dengan verb `GET`, parameter tambahan apa pun akan berada di query; semua request lainnya akan mengirimkan parameter tambahan di body.

Jika Anda ingin mengirimkan argumen tambahan secara eksplisit, Anda dapat melakukannya dengan opsi request `query`, `body`, dan `headers`.

#### Properti response tidak terdokumentasi

Untuk mengakses properti response yang tidak terdokumentasi, Anda dapat mengakses objek response dengan `// @ts-expect-error` pada objek response, atau melakukan cast objek response ke tipe yang diperlukan. Seperti halnya parameter request, SDK tidak memvalidasi atau menghapus properti tambahan dari response API.

### Menyesuaikan fetch client

Secara default, library ini mengharapkan fungsi `fetch` global telah didefinisikan.

Jika Anda ingin menggunakan fungsi `fetch` yang berbeda, Anda dapat melakukan polyfill pada global:

```typescript
import fetch from "my-fetch";

globalThis.fetch = fetch;
```

Atau meneruskannya ke client:

```typescript
import fetch from "my-fetch";

const client = new Anthropic({ fetch });
```

### Opsi fetch

Jika Anda ingin mengatur opsi `fetch` kustom tanpa meng-override fungsi `fetch`, Anda dapat menyediakan objek `fetchOptions` saat membuat client atau membuat request. (Opsi khusus request meng-override opsi client.)

```typescript
const client = new Anthropic({
  fetchOptions: {
    // Opsi `RequestInit`
  }
});
```

### Mengonfigurasi proxy

Untuk mengubah perilaku proxy, Anda dapat menyediakan `fetchOptions` kustom yang menambahkan opsi proxy khusus runtime ke request:

<Tabs>
  <Tab title="Node.js">
    ```typescript
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

## Fitur beta

Fitur beta tersedia sebelum rilis umum untuk mendapatkan umpan balik awal dan menguji fungsionalitas baru. Anda dapat memeriksa ketersediaan semua kemampuan dan alat Claude di [Ikhtisar fitur](https://platform.claude.com/docs/id/build-with-claude/overview).

Anda dapat mengakses sebagian besar fitur API beta melalui properti `beta` dari client. Untuk mengaktifkan fitur beta tertentu, Anda perlu menambahkan [header beta](https://platform.claude.com/docs/id/api/beta-headers) yang sesuai ke field `betas` saat membuat pesan.

Misalnya, untuk mengaktifkan [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing):

```typescript
const client = new Anthropic();
const response = await client.beta.messages.create({
  model: "claude-opus-5-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  betas: ["context-management-2025-06-27"]
});
```

## Dukungan runtime

<Accordion title="Penggunaan browser">
  Mengaktifkan opsi `dangerouslyAllowBrowser` dapat berbahaya karena mengekspos kredensial API rahasia Anda dalam kode sisi client. Browser web secara inheren kurang aman dibandingkan lingkungan server. Setiap pengguna yang memiliki akses ke browser berpotensi dapat memeriksa, mengekstrak, dan menyalahgunakan kredensial ini. Hal ini dapat menyebabkan akses tidak sah menggunakan kredensial Anda dan berpotensi membahayakan data atau fungsionalitas sensitif.

  **Kapan hal ini mungkin tidak berbahaya?**

  Dalam skenario tertentu, mengaktifkan dukungan browser mungkin tidak menimbulkan risiko yang signifikan:

  * **Alat internal:** Jika aplikasi hanya digunakan dalam lingkungan internal yang terkontrol di mana penggunanya tepercaya, risiko terpaparnya kredensial dapat dimitigasi.
  * **Tujuan pengembangan atau debugging:** Mengaktifkan fitur ini untuk sementara mungkin dapat diterima, asalkan kredensial berumur pendek, tidak juga digunakan di lingkungan produksi, atau sering dirotasi.
</Accordion>

## Integrasi platform

<Note>
  Untuk panduan penyiapan platform terperinci beserta contoh kode, lihat:

  * [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)
  * [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)
</Note>

TypeScript SDK mendukung platform berikut:

* **Agent Platform:** `npm install @anthropic-ai/vertex-sdk`: Menyediakan client `AnthropicVertex`
* **Bedrock:** `npm install @anthropic-ai/bedrock-sdk`: Menyediakan client `AnthropicBedrockMantle`, dan `AnthropicBedrock` untuk jalur `bedrock-runtime`
* **Claude Platform on AWS:** `npm install @anthropic-ai/aws-sdk`: Menyediakan client `AnthropicAws`. Teruskan `workspaceId` ke constructor atau atur variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID`. Tersedia dalam beta.
* **Foundry:** `npm install @anthropic-ai/foundry-sdk`: Menyediakan client `AnthropicFoundry`

Gunakan `AnthropicBedrockMantle` untuk proyek baru; `AnthropicBedrock` tetap tersedia untuk aplikasi yang sudah ada yang menggunakan Bedrock `InvokeModel` API.

## Semantic versioning

Setiap versi mayor SDK ini mengirimkan satu versi API dalam header `anthropic-version` secara default, dan versi mayor baru hadir bersama setiap versi API baru. Versi mayor pertama yang mengirimkan `2026-10-21` adalah 1.0.0; lihat [Migrasi ke versi API 2026-10-21](https://platform.claude.com/docs/id/api/migration-2026-10-21#upgrade).

Paket ini umumnya mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan tertentu yang tidak kompatibel ke belakang dapat dirilis sebagai versi minor:

1. Perubahan yang hanya memengaruhi tipe statis, tanpa merusak perilaku runtime.
2. Perubahan pada internal library yang secara teknis bersifat publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal.
3. Perubahan yang tidak diperkirakan akan berdampak pada sebagian besar pengguna dalam praktiknya.

Kompatibilitas ke belakang ditangani dengan serius untuk memastikan Anda dapat mengandalkan pengalaman upgrade yang lancar.

## Pertanyaan yang sering diajukan

Lihat [repositori GitHub](https://github.com/anthropics/anthropic-sdk-typescript) untuk FAQ, issue, dan dukungan komunitas.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-typescript)
* [Referensi API](https://platform.claude.com/docs/id/api/overview)
* [Streaming Messages](https://platform.claude.com/docs/id/build-with-claude/streaming)
* [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview)
