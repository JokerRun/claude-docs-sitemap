---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 2c88c727f8f0fc3c2230fbfca54d8c28c7e3517ad6a4d6459ae8cb318713bab6
---

# TypeScript SDK

Instal dan konfigurasikan Anthropic TypeScript SDK untuk Node.js, Deno, Bun, dan lingkungan browser

---

Library ini menyediakan akses yang mudah ke Anthropic REST API dari TypeScript atau JavaScript.

<Info>
  Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK yang spesifik untuk TypeScript.
</Info>

## Instalasi

```bash
npm install @anthropic-ai/sdk
```

## Persyaratan

TypeScript >= 4.9 didukung.

Runtime berikut didukung:

* Node.js 20 LTS atau versi yang lebih baru ([non-EOL](https://endoflife.date/nodejs)).
* Deno v1.28.0 atau lebih tinggi.
* Bun 1.0 atau lebih baru.
* Cloudflare Workers.
* Vercel Edge Runtime.
* Jest 28 atau lebih tinggi dengan lingkungan `"node"` (`"jsdom"` tidak didukung saat ini).
* Nitro v2.6 atau lebih tinggi.
* Browser web: dinonaktifkan secara default untuk menghindari terpaparnya kredensial API rahasia Anda (lihat [praktik terbaik kunci API](https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure)). Aktifkan dukungan browser dengan secara eksplisit mengatur `dangerouslyAllowBrowser` ke `true`.

Perhatikan bahwa React Native tidak didukung saat ini.

Jika Anda tertarik dengan lingkungan runtime lainnya, buka atau beri dukungan (upvote) pada issue di [repositori GitHub](https://github.com/anthropics/anthropic-sdk-typescript).

## Penggunaan

```typescript
const client = new Anthropic({
  apiKey: process.env["ANTHROPIC_API_KEY"] // This is the default and can be omitted
});

const message = await client.messages.create({
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-4-8"
});

for (const block of message.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

Untuk opsi autentikasi termasuk Workload Identity Federation, lihat [Autentikasi](/docs/id/manage-claude/authentication).

## Tipe request dan response

Library ini menyertakan definisi TypeScript untuk semua parameter request dan field response. Anda dapat mengimpor dan menggunakannya seperti ini:

```typescript
const client = new Anthropic({
  apiKey: process.env["ANTHROPIC_API_KEY"] // This is the default and can be omitted
});

const params: Anthropic.MessageCreateParams = {
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-4-8"
};
const message: Anthropic.Message = await client.messages.create(params);
```

Dokumentasi untuk setiap metode, parameter request, dan field response tersedia dalam docstring dan muncul saat hover di sebagian besar editor modern.

## Menghitung token

Anda dapat melihat penggunaan yang tepat untuk request tertentu melalui properti response `usage`, misalnya:

```typescript
const message = await client.messages.create(/* ... */);
console.log(message.usage);
// { input_tokens: 25, output_tokens: 13 }
```

## Streaming respons

SDK menyediakan dukungan untuk streaming respons menggunakan Server Sent Events (SSE).

```typescript
const client = new Anthropic();

const stream = await client.messages.create({
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-4-8",
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
    model: "claude-opus-4-8",
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

Streaming dengan `client.messages.stream(...)` mengekspos berbagai helper untuk kenyamanan Anda termasuk event handler dan akumulasi.

Sebagai alternatif, Anda dapat menggunakan `client.messages.create({ ..., stream: true })` yang hanya mengembalikan async iterable dari event dalam stream dan dengan demikian menggunakan lebih sedikit memori (tidak membangun objek pesan akhir untuk Anda).

## Helper alat

SDK ini menyediakan helper untuk memudahkan pembuatan dan menjalankan alat di Messages API. Anda dapat menggunakan skema Zod atau JSON Schema untuk mendeskripsikan input ke sebuah alat. Anda kemudian dapat menjalankan alat-alat tersebut menggunakan metode `client.beta.messages.toolRunner()`. Metode ini menangani penerusan input yang dihasilkan oleh model yang dipilih ke alat yang tepat dan meneruskan hasilnya kembali ke model.

Untuk detail lebih lanjut tentang penggunaan alat, lihat [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview).

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
  model: "claude-opus-4-8",
  max_tokens: 1000,
  messages: [{ role: "user", content: "What is the weather in San Francisco?" }],
  tools: [weatherTool]
});

console.log(finalMessage.content);
```

### Error alat

Untuk melaporkan error dari sebuah alat kembali ke model, lempar (throw) `ToolError` dari fungsi `run`. Tidak seperti `Error` biasa, `ToolError` menerima blok konten, memungkinkan Anda menyertakan gambar atau konten terstruktur lainnya dalam respons error:

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
      // Sertakan tangkapan layar error agar model dapat melihat apa yang salah
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

Jika `Error` biasa dilempar, pesannya akan dikonversi menjadi blok konten teks.

## Penggunaan alat

SDK ini menyediakan dukungan untuk penggunaan alat (tool use), juga dikenal sebagai function calling. Untuk detail lebih lanjut, lihat [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview).

## Helper MCP

SDK ini menyediakan helper untuk integrasi dengan server [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). Helper ini mengonversi tipe MCP ke tipe Claude API, mengurangi boilerplate saat bekerja dengan alat, prompt, dan resource MCP.

<Tip>
  Claude API juga mendukung [parameter `mcp_servers`](/docs/id/agents-and-tools/mcp-connector) yang memungkinkan Claude terhubung langsung ke server MCP jarak jauh. Gunakan `mcp_servers` ketika Anda memiliki server jarak jauh yang dapat diakses melalui URL dan hanya memerlukan dukungan alat. Gunakan helper MCP ketika Anda memerlukan server MCP lokal, prompt, resource, atau kontrol lebih besar atas koneksi MCP.
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

// Menghubungkan ke server MCP
const transport = new StdioClientTransport({ command: "mcp-server", args: [] });
const mcpClient = new Client({ name: "my-client", version: "1.0.0" });
await mcpClient.connect(transport);

// Menggunakan prompt MCP
const { messages } = await mcpClient.getPrompt({ name: "my-prompt" });
const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: mcpMessages(messages)
});
console.log(response.content);

// Menggunakan alat MCP dengan toolRunner
const { tools } = await mcpClient.listTools();
const finalMessage = await anthropic.beta.messages.toolRunner({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Use the available tools" }],
  tools: mcpTools(tools, mcpClient)
});
console.log(finalMessage.content);

// Menggunakan resource MCP sebagai konten
const resource = await mcpClient.readResource({ uri: "file:///path/to/doc.txt" });
await anthropic.beta.messages.create({
  model: "claude-opus-4-8",
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

// Mengunggah resource MCP sebagai file
const fileResource = await mcpClient.readResource({ uri: "file:///path/to/data.json" });
await anthropic.beta.files.upload({ file: mcpResourceToFile(fileResource) });
```

### Penanganan error MCP

Fungsi konversi melempar `UnsupportedMCPValueError` jika nilai MCP tidak didukung oleh Claude API (misalnya, tipe konten yang tidak didukung, tipe MIME yang tidak didukung, resource link non-http/https).

## Message batches

SDK ini menyediakan dukungan untuk [Message Batches API](/docs/id/build-with-claude/batch-processing) di bawah namespace `client.messages.batches`.

### Membuat batch

Message Batches menerima array request, di mana setiap objek memiliki pengidentifikasi `custom_id`, dan `params` request yang sama persis dengan Messages API standar:

```typescript
const batch = await client.messages.batches.create({
  requests: [
    {
      custom_id: "my-first-request",
      params: {
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hello, world" }]
      }
    },
    {
      custom_id: "my-second-request",
      params: {
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hi again, friend" }]
      }
    }
  ]
});
```

### Mendapatkan hasil dari batch

Setelah Message Batch diproses, yang ditandai dengan `.processing_status === 'ended'`, Anda dapat mengakses hasilnya dengan `.batches.results()`

```typescript
const results = await client.messages.batches.results(batch.id);
for await (const entry of results) {
  if (entry.result.type === "succeeded") {
    console.log(entry.result.message.content);
  }
}
```

## Unggah file

Parameter request yang berkaitan dengan unggahan file dapat diberikan dalam berbagai bentuk:

* `File` (atau objek dengan struktur yang sama)
* `Response` dari `fetch` (atau objek dengan struktur yang sama)
* `fs.ReadStream`
* nilai kembalian dari helper `toFile`

Atur content-type secara eksplisit karena files API tidak akan menyimpulkannya untuk Anda:

```typescript
import fs from "node:fs";
import Anthropic, { toFile } from "@anthropic-ai/sdk";

const client = new Anthropic();

// Jika Anda memiliki akses ke Node `fs`, gunakan `fs.createReadStream()`:
await client.beta.files.upload({
  file: await toFile(fs.createReadStream("/path/to/file"), undefined, {
    type: "application/json"
  })
});

// Atau jika Anda memiliki API `File` web, Anda dapat meneruskan instance `File`:
await client.beta.files.upload({
  file: new File(["my bytes"], "file.txt", { type: "text/plain" })
});
// Anda juga dapat meneruskan `Response` dari `fetch`:
await client.beta.files.upload({
  file: await fetch("https://somesite/file")
});

// Atau `Buffer` / `Uint8Array`
await client.beta.files.upload({
  file: await toFile(Buffer.from("my bytes"), "file", { type: "text/plain" })
});
await client.beta.files.upload({
  file: await toFile(new Uint8Array([0, 1, 2]), "file", { type: "text/plain" })
});
```

## Menangani error

Ketika library tidak dapat terhubung ke API, atau jika API mengembalikan kode status non-sukses (yaitu, respons 4xx atau 5xx), subclass dari `APIError` akan dilempar:

```typescript
const message = await client.messages
  .create({
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-4-8"
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

> Untuk informasi lebih lanjut tentang debugging request, lihat [Request ID](/docs/id/api/errors#request-id).

Semua respons objek dalam SDK menyediakan properti `_request_id` yang ditambahkan dari header respons `request-id` sehingga Anda dapat dengan cepat mencatat request yang gagal dan melaporkannya kembali ke Anthropic.

```typescript
const message = await client.messages.create({
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-opus-4-8"
});
console.log(message._request_id); // req_018EeWyXxfu5pfWkrYcMdjWG
```

## Percobaan ulang

Error tertentu secara otomatis dicoba ulang 2 kali secara default, dengan exponential backoff singkat. Error koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict, 429 Rate Limit, dan error Internal >=500 semuanya dicoba ulang secara default.

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
    model: "claude-opus-4-8"
  },
  { maxRetries: 5 }
);
```

## Timeout

Secara default, request akan timeout setelah 10 menit. Namun jika Anda telah menentukan nilai `max_tokens` yang besar dan *tidak* melakukan streaming, timeout default akan dihitung secara dinamis menggunakan rumus:

```typescript
const minimum = 10 * 60;
const calculated = (60 * 60 * maxTokens) / 128_000;
return calculated < minimum ? minimum * 1000 : calculated * 1000;
```

yang akan menghasilkan timeout hingga 60 menit, diskalakan berdasarkan parameter `max_tokens`, kecuali ditimpa pada level request atau klien.

Anda dapat mengonfigurasi ini dengan opsi `timeout`:

```typescript
// Konfigurasikan default untuk semua permintaan:
const client = new Anthropic({
  timeout: 20 * 1000 // 20 seconds (default is 10 minutes)
});

// Ganti per permintaan:
await client.messages.create(
  {
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-4-8"
  },
  { timeout: 5 * 1000 }
);
```

Saat timeout, `APIConnectionTimeoutError` akan dilempar.

Perhatikan bahwa request yang timeout akan [dicoba ulang dua kali secara default](#retries).

## Request yang panjang

<Warning>
  Pertimbangkan untuk menggunakan [Messages API](#streaming-responses) dengan streaming untuk request yang berjalan lebih lama.
</Warning>

Hindari mengatur nilai `max_tokens` yang besar tanpa menggunakan streaming. Beberapa jaringan mungkin memutuskan koneksi yang idle setelah jangka waktu tertentu, yang dapat menyebabkan request gagal atau [timeout](#timeouts) tanpa menerima respons dari Anthropic.

SDK ini juga melempar error jika request non-streaming diperkirakan akan berlangsung lebih dari sekitar 10 menit. Memberikan `stream: true` atau [menimpa](#timeouts) opsi `timeout` pada level klien atau request akan menonaktifkan error ini.

"Latency" (latensi) request yang diperkirakan lebih lama dari [timeout](#timeouts) untuk request non-streaming akan mengakibatkan klien memutuskan koneksi dan mencoba ulang tanpa menerima respons.

Ketika didukung oleh implementasi `fetch`, SDK mengatur opsi [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/overview.html) untuk mengurangi dampak timeout koneksi idle pada beberapa jaringan. Ini dapat [ditimpa](#configuring-proxies) dengan mengonfigurasi proxy kustom.

## Paginasi otomatis

Metode list di Claude API menggunakan paginasi. Anda dapat menggunakan sintaks `for await ... of` untuk melakukan iterasi melalui item di semua halaman:

```typescript
async function fetchAllMessageBatches() {
  const allMessageBatches = [];
  // Secara otomatis mengambil lebih banyak halaman sesuai kebutuhan.
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

SDK secara otomatis mengirimkan header `anthropic-version` yang diatur ke `2023-06-01`.

Jika perlu, Anda dapat menimpanya dengan mengatur header default per request.

Perlu diketahui bahwa melakukan hal tersebut dapat mengakibatkan tipe yang salah dan perilaku tak terduga atau tidak terdefinisi lainnya dalam SDK.

```typescript
const client = new Anthropic();

const message = await client.messages.create(
  {
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-4-8"
  },
  { headers: { "anthropic-version": "My-Custom-Value" } }
);
```

## Penggunaan lanjutan

### Mengakses data Response mentah (misalnya, header)

`Response` "mentah" yang dikembalikan oleh `fetch()` dapat diakses melalui metode `.asResponse()` pada tipe `APIPromise` yang dikembalikan oleh semua metode. Metode ini mengembalikan segera setelah header untuk respons yang berhasil diterima dan tidak mengonsumsi body respons, sehingga Anda bebas menulis logika parsing atau streaming kustom.

Anda juga dapat menggunakan metode `.withResponse()` untuk mendapatkan `Response` mentah bersama dengan data yang telah di-parse. Tidak seperti `.asResponse()`, metode ini mengonsumsi body, dan mengembalikan setelah selesai di-parse.

```typescript
const client = new Anthropic();

const response = await client.messages
  .create({
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-4-8"
  })
  .asResponse();
console.log(response.headers.get("X-My-Header"));
console.log(response.statusText); // access the underlying Response object

const { data: message, response: raw } = await client.messages
  .create({
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    model: "claude-opus-4-8"
  })
  .withResponse();
console.log(raw.headers.get("X-My-Header"));
console.log(message.content);
```

### Logging

<Warning>
  Semua pesan log hanya dimaksudkan untuk debugging. Format dan isi pesan log dapat berubah antar rilis.
</Warning>

#### Level log

Anda dapat mengonfigurasi level log dengan dua cara:

1. Melalui variabel lingkungan `ANTHROPIC_LOG`
2. Menggunakan opsi klien `logLevel` (menimpa variabel lingkungan jika diatur)

```typescript
const client = new Anthropic({
  logLevel: "debug" // Show all log messages
});
```

Level log yang tersedia, dari yang paling verbose hingga yang paling sedikit:

* `'debug'` - Menampilkan pesan debug, info, peringatan, dan error
* `'info'` - Menampilkan pesan info, peringatan, dan error
* `'warn'` - Menampilkan peringatan dan error (default)
* `'error'` - Hanya menampilkan error
* `'off'` - Menonaktifkan semua logging

Pada level `'debug'`, semua request dan respons HTTP dicatat, termasuk header dan body. Beberapa header terkait autentikasi disamarkan, tetapi data sensitif dalam body request dan respons mungkin masih terlihat.

#### Logger kustom

Secara default, library ini mencatat log ke `globalThis.console`. Anda juga dapat menyediakan logger kustom. Sebagian besar library logging didukung, termasuk [pino](https://www.npmjs.com/package/pino), [winston](https://www.npmjs.com/package/winston), [bunyan](https://www.npmjs.com/package/bunyan), [consola](https://www.npmjs.com/package/consola), [signale](https://www.npmjs.com/package/signale), dan [@std/log](https://jsr.io/@std/log). Jika logger Anda tidak berfungsi, buka sebuah issue.

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

Library ini memiliki tipe untuk akses yang mudah ke API yang terdokumentasi. Jika Anda perlu mengakses endpoint, parameter, atau properti respons yang tidak terdokumentasi, library ini tetap dapat digunakan.

#### Endpoint yang tidak terdokumentasi

Untuk membuat request ke endpoint yang tidak terdokumentasi, Anda dapat menggunakan `client.get`, `client.post`, dan verba HTTP lainnya. Opsi pada klien, seperti percobaan ulang, tetap dihormati saat membuat request ini.

```typescript
await client.post("/some/path", {
  body: { some_prop: "foo" },
  query: { some_query_arg: "bar" }
});
```

#### Parameter request yang tidak terdokumentasi

Untuk membuat request menggunakan parameter yang tidak terdokumentasi, Anda dapat menggunakan `// @ts-expect-error` pada parameter yang tidak terdokumentasi. Library ini tidak memvalidasi saat runtime bahwa request cocok dengan tipenya, jadi nilai tambahan apa pun yang Anda kirim akan dikirim apa adanya.

```typescript
client.messages.create({
  // ...
  // @ts-expect-error baz is not yet public
  baz: "undocumented option"
});
```

Untuk request dengan verba `GET`, parameter tambahan apa pun akan berada di query; semua request lainnya akan mengirimkan parameter tambahan di body.

Jika Anda ingin secara eksplisit mengirim argumen tambahan, Anda dapat melakukannya dengan opsi request `query`, `body`, dan `headers`.

#### Properti respons yang tidak terdokumentasi

Untuk mengakses properti respons yang tidak terdokumentasi, Anda dapat mengakses objek respons dengan `// @ts-expect-error` pada objek respons, atau melakukan cast objek respons ke tipe yang diperlukan. Seperti parameter request, SDK tidak memvalidasi atau menghapus properti tambahan dari respons API.

### Menyesuaikan klien fetch

Secara default, library ini mengharapkan fungsi `fetch` global telah didefinisikan.

Jika Anda ingin menggunakan fungsi `fetch` yang berbeda, Anda dapat melakukan polyfill pada global:

```typescript
import fetch from "my-fetch";

globalThis.fetch = fetch;
```

Atau meneruskannya ke klien:

```typescript
import fetch from "my-fetch";

const client = new Anthropic({ fetch });
```

### Opsi fetch

Jika Anda ingin mengatur opsi `fetch` kustom tanpa menimpa fungsi `fetch`, Anda dapat menyediakan objek `fetchOptions` saat membuat klien atau membuat request. (Opsi spesifik request menimpa opsi klien.)

```typescript
const client = new Anthropic({
  fetchOptions: {
    // Opsi `RequestInit`
  }
});
```

### Mengonfigurasi proxy

Untuk memodifikasi perilaku proxy, Anda dapat menyediakan `fetchOptions` kustom yang menambahkan opsi proxy spesifik runtime ke request:

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

Fitur beta tersedia sebelum rilis umum untuk mendapatkan umpan balik awal dan menguji fungsionalitas baru. Anda dapat memeriksa ketersediaan semua kemampuan dan alat Claude di [ikhtisar membangun dengan Claude](/docs/id/build-with-claude/overview).

Anda dapat mengakses sebagian besar fitur API beta melalui properti beta dari klien. Untuk mengaktifkan fitur beta tertentu, Anda perlu menambahkan [header beta](/docs/id/api/beta-headers) yang sesuai ke field `betas` saat membuat pesan.

Misalnya, untuk menggunakan [Files API](/docs/id/build-with-claude/files):

```typescript
const client = new Anthropic();
const response = await client.beta.messages.create({
  model: "claude-opus-4-8",
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

<Accordion title="Penggunaan di browser">
  Mengaktifkan opsi `dangerouslyAllowBrowser` bisa berbahaya karena mengekspos kredensial API rahasia Anda dalam kode sisi klien. Browser web secara inheren kurang aman dibandingkan lingkungan server, pengguna mana pun yang memiliki akses ke browser berpotensi memeriksa, mengekstrak, dan menyalahgunakan kredensial ini. Hal ini dapat menyebabkan akses tidak sah menggunakan kredensial Anda dan berpotensi membahayakan data atau fungsionalitas sensitif.

  **Kapan hal ini mungkin tidak berbahaya?**

  Dalam skenario tertentu di mana mengaktifkan dukungan browser mungkin tidak menimbulkan risiko signifikan:

  * **Alat internal:** Jika aplikasi digunakan semata-mata dalam lingkungan internal yang terkontrol di mana penggunanya tepercaya, risiko terpaparnya kredensial dapat dimitigasi.
  * **Tujuan pengembangan atau debugging:** Mengaktifkan fitur ini sementara mungkin dapat diterima, asalkan kredensialnya berumur pendek, tidak juga digunakan di lingkungan produksi, atau sering dirotasi.
</Accordion>

## Integrasi platform

<Note>
  Untuk panduan penyiapan platform yang terperinci dengan contoh kode, lihat:

  * [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 dan sebelumnya)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai)
  * [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry)
</Note>

TypeScript SDK mendukung platform berikut:

* **Agent Platform:** `npm install @anthropic-ai/vertex-sdk`: Menyediakan klien `AnthropicVertex`
* **Bedrock:** `npm install @anthropic-ai/bedrock-sdk`: Menyediakan klien `AnthropicBedrockMantle`, dan `AnthropicBedrock` untuk jalur `bedrock-runtime`
* **Claude Platform di AWS:** `npm install @anthropic-ai/aws-sdk`: Menyediakan klien `AnthropicAws`. Berikan `workspaceId` ke konstruktor atau atur variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID`. Tersedia dalam beta.
* **Foundry:** `npm install @anthropic-ai/foundry-sdk`: Menyediakan klien `AnthropicFoundry`

Gunakan `AnthropicBedrockMantle` untuk proyek baru; `AnthropicBedrock` tetap ada untuk aplikasi yang sudah ada yang menggunakan API `InvokeModel` Bedrock.

## Semantic versioning

Paket ini secara umum mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan tertentu yang tidak kompatibel ke belakang dapat dirilis sebagai versi minor:

1. Perubahan yang hanya memengaruhi tipe statis, tanpa merusak perilaku runtime.
2. Perubahan pada internal library yang secara teknis publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal.
3. Perubahan yang tidak diperkirakan akan berdampak pada sebagian besar pengguna dalam praktiknya.

Kompatibilitas ke belakang ditangani dengan serius untuk memastikan Anda dapat mengandalkan pengalaman upgrade yang lancar.

## Pertanyaan yang sering diajukan

Lihat [repositori GitHub](https://github.com/anthropics/anthropic-sdk-typescript) untuk FAQ, issue, dan dukungan komunitas.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-typescript)
* [Referensi API](/docs/id/api/overview)
* [Streaming Messages](/docs/id/build-with-claude/streaming)
* [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview)
