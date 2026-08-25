---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 09d3c18adcb6418f0150a4fdb4d316ea8307c0d8fd61f247b5244ebf85585b54
---

---
title: Mengembangkan integrasi Inference hooks
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint
description: Bangun server keamanan AI yang menerima permintaan Inference hooks yang ditandatangani, memverifikasinya, dan mengembalikan verdict allow atau deny.
---

<Note>
  Inference hooks masih dalam versi beta dan tersedia untuk organisasi Claude Enterprise. Nama field, bentuk permintaan, dan header dapat berubah selama masa beta.
</Note>

Integrasi Inference hooks adalah sebuah "AI security server" (server keamanan AI): layanan HTTPS yang dipanggil oleh Anthropic. Untuk setiap permintaan yang diatur, server Anda menerima `POST` bertanda tangan yang membawa transkrip percakapan dan merespons dengan "verdict" (putusan) allow atau deny. Halaman ini mendokumentasikan protokol untuk membangun server tersebut: skema permintaan dan verdict, verifikasi tanda tangan, dan kontrak operasional.

Untuk mengaktifkan Inference hooks dan mengarahkannya ke endpoint Anda, lihat [Mengonfigurasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration). Untuk mengetahui apa itu Inference hooks dan kapan menggunakannya, lihat [ikhtisar Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks).

## Mendapatkan round trip verdict pertama

Integrasi terkecil yang berfungsi adalah server yang membaca setiap permintaan dan mengizinkannya. Jalankan salah satu server berikut, ekspos di URL `https://` publik (misalnya, di belakang reverse proxy yang menangani terminasi TLS pada host yang Anda kendalikan, bukan layanan reverse-tunnel; lihat [Menerima permintaan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#receive-a-request)), lalu minta administrator Anda [menetapkannya sebagai endpoint dan menguji koneksinya](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration): hasil **Test connection** melaporkan verdict allow yang dikembalikan server Anda.

<CodeGroup exclude="shell">
  ```python Python
  # Jalankan dengan: python server.py
  from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


  class VerdictHandler(BaseHTTPRequestHandler):
      protocol_version = "HTTP/1.1"  # keep the connection open between verdicts

      def do_POST(self):
          # Kuras body; transkrip bisa berukuran megabyte.
          self.rfile.read(int(self.headers.get("Content-Length", 0)))
          verdict = b'{"action": "allow"}'
          self.send_response(200)
          self.send_header("Content-Type", "application/json")
          self.send_header("Content-Length", str(len(verdict)))
          self.end_headers()
          self.wfile.write(verdict)


  ThreadingHTTPServer(("", 8000), VerdictHandler).serve_forever()
  ```

  ```typescript TypeScript
  // Jalankan dengan: node server.ts
  import { createServer } from "node:http";

  createServer((request, response) => {
    // Kosongkan body sebelum menjawab; transkrip bisa berukuran megabyte.
    request.resume();
    request.on("end", () => {
      response.writeHead(200, { "Content-Type": "application/json" });
      response.end('{"action": "allow"}');
    });
  }).listen(8000);
  ```

  ```csharp C#
  #:sdk Microsoft.NET.Sdk.Web
  #:property PublishAot=false
  // Jalankan dengan: dotnet run server.cs

  var app = WebApplication.Create();

  app.MapPost("/{**path}", async (HttpRequest request) =>
  {
      // Kuras body; transkrip bisa berukuran megabyte.
      await request.Body.CopyToAsync(Stream.Null);
      return Results.Text("""{"action": "allow"}""", "application/json");
  });

  app.Run("http://0.0.0.0:8000");
  ```

  ```go Go
  // Jalankan dengan: go run server.go
  package main

  import (
  	"io"
  	"log"
  	"net/http"
  )

  func main() {
  	http.HandleFunc("POST /", func(writer http.ResponseWriter, request *http.Request) {
  		// Kuras body agar koneksi dapat digunakan kembali; transkrip bisa berukuran megabyte.
  		io.Copy(io.Discard, request.Body)
  		writer.Header().Set("Content-Type", "application/json")
  		writer.Write([]byte(`{"action": "allow"}`))
  	})
  	log.Fatal(http.ListenAndServe(":8000", nil))
  }
  ```

  ```java Java
  // Jalankan dengan: java VerdictServer.java
  import com.sun.net.httpserver.HttpServer;

  void main() throws IOException {
      HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
      server.createContext("/", exchange -> {
          // Kuras body tanpa melakukan buffering; transkrip bisa berukuran megabyte.
          exchange.getRequestBody().transferTo(OutputStream.nullOutputStream());
          byte[] verdict = "{\"action\": \"allow\"}".getBytes(StandardCharsets.UTF_8);
          exchange.getResponseHeaders().set("Content-Type", "application/json");
          exchange.sendResponseHeaders(200, verdict.length);
          try (OutputStream responseBody = exchange.getResponseBody()) {
              responseBody.write(verdict);
          }
      });
      server.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
      server.start();
  }
  ```

  ```php PHP
  <?php
  // Jalankan dengan: php -S 0.0.0.0:8000 server.php

  // Kuras isi body; transkrip bisa berukuran megabyte.
  file_get_contents('php://input');

  http_response_code(200);
  header('Content-Type: application/json');
  echo '{"action": "allow"}';
  ```

  ```ruby Ruby
  # webrick adalah gem biasa di Ruby 3.4: gem install webrick, atau tambahkan gem "webrick".
  # Jalankan dengan: ruby server.rb
  require "webrick"

  server = WEBrick::HTTPServer.new(Port: 8000)
  server.mount_proc("/") do |request, response|
    request.body # Drain the body; transcripts can be megabytes.
    response.status = 200
    response["Content-Type"] = "application/json"
    response.body = '{"action": "allow"}'
  end
  server.start
  ```
</CodeGroup>

<Note>
  Server-server ini menerima setiap permintaan, termasuk yang tidak ditandatangani. Tambahkan [verifikasi tanda tangan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#verify-the-signature) sebelum Anda melakukan penegakan.
</Note>

## Menerima permintaan

Anthropic mengirim `POST` HTTPS ke URL yang dikonfigurasi administrator Anda. Seluruh URL yang dikonfigurasi adalah endpoint-nya: tidak ada sufiks path tetap, jadi pilih path apa pun yang sesuai dengan server Anda.

Host server keamanan AI Anda di tempat yang dapat dijangkau Anthropic: URL `https://` pada port 443, pada host yang dapat dirutekan secara publik (rentang privat, loopback, dan carrier-grade NAT ditolak saat koneksi), dengan sertifikat yang tervalidasi terhadap trust store CA publik, dan merespons tanpa redirect. URL yang dikonfigurasi harus menjadi tujuan akhir. Host reverse-tunnel (ngrok dan layanan tunnel serupa) tidak didukung: kebijakan jaringan Anthropic memblokirnya. Host server Anda pada domain yang Anda kendalikan. [Mengonfigurasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration) membahas cara administrator Anda menetapkan dan menguji URL tersebut.

Setiap permintaan membawa header tetap berikut, bersama dengan [header permintaan kustom](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration) apa pun yang dikonfigurasi administrator Anda dan, setelah organisasi Anda memiliki signing secret, header tanda tangan `webhook-*` yang dijelaskan di [Memverifikasi tanda tangan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#verify-the-signature):

| Header            | Nilai              |
| ----------------- | ------------------ |
| `Content-Type`    | `application/json` |
| `User-Agent`      | `anthropic-dlp/1`  |
| `Accept-Encoding` | `identity`         |

Saat ini ada satu event hook: prompt frame, yang dikirim sekali per permintaan inferensi yang diatur, sebelum inferensi dimulai. Anthropic menahan permintaan hingga server keamanan AI Anda merespons atau batas waktu verdict habis.

## Prompt frame

Body permintaan adalah objek JSON dengan field-field berikut:

| Field        | Tipe             | Deskripsi                                                                                                                                                                                                                                                                                                              |
| ------------ | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`       | string           | Event hook. Saat ini selalu `"prompt"`; tipe event lain akan diperkenalkan di masa mendatang, jadi tangani nilai yang tidak dikenali dengan baik (lihat [Kompatibilitas ke depan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#forward-compatibility)).                                  |
| `request_id` | string           | Pengidentifikasi opaque per panggilan inferensi untuk korelasi. Sama dengan header `webhook-id`.                                                                                                                                                                                                                       |
| `tenant_id`  | string atau null | Pengidentifikasi opaque untuk organisasi pemilik permintaan.                                                                                                                                                                                                                                                           |
| `actor`      | object           | Principal yang menjadi atribusi permintaan, didiskriminasi berdasarkan `type` (`"user"` adalah satu-satunya nilai yang dikirim saat ini): `id` (pengidentifikasi bertag, stabil di seluruh permintaan untuk akun yang sama) dan `email_address` (jika tersedia). Baik `id` maupun `email_address` dapat bernilai null. |
| `source`     | object           | Aplikasi asal: `application` (lihat [Nilai source](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#source-values)).                                                                                                                                                                         |
| `messages`   | array            | Transkrip percakapan hingga titik inferensi. Lihat [Blok konten](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#content-blocks).                                                                                                                                                           |
| `session_id` | string atau null | Pengidentifikasi percakapan opaque, jika ada. Jangan mem-parse-nya. Untuk Claude Code, ini adalah pengidentifikasi sesi best-effort yang dinyatakan oleh klien.                                                                                                                                                        |
| `model`      | string atau null | Pengidentifikasi model publik untuk permintaan ini, jika tersedia.                                                                                                                                                                                                                                                     |
| `metadata`   | object           | Map ekstensi yang dicadangkan dari kunci string ke nilai string, saat ini dikirim kosong. Jangan mensyaratkan apa pun darinya, dan toleransi ketidakhadirannya, kehadirannya, serta kunci apa pun yang muncul.                                                                                                         |

<Note>
  Permintaan saat ini juga membawa alias lama yang sudah deprecated untuk beberapa field ini. Baca nama field yang didokumentasikan di halaman ini dan abaikan yang lainnya; alias tersebut hanya ada untuk integrasi terdahulu.
</Note>

Contoh body permintaan:

```json
{
  "type": "prompt",
  "request_id": "req_abc123",
  "tenant_id": "11111111-1111-1111-1111-111111111111",
  "actor": {
    "type": "user",
    "id": "user_01AbCdEfGhIjKlMnOpQrStUv",
    "email_address": "alice@example.com"
  },
  "source": {
    "application": "claude-ai"
  },
  "session_id": "22222222-2222-2222-2222-222222222222",
  "model": "claude-sonnet-4-5",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Summarize the attached report."
        },
        {
          "type": "attachment",
          "file_name": "q2-report.pdf",
          "media_type": "application/pdf",
          "size_bytes": 48213,
          "text": "Q2 revenue grew 14% quarter over quarter..."
        }
      ]
    }
  ],
  "metadata": {}
}
```

### Blok konten

Setiap entri dalam `messages` memiliki `role` berupa `user` atau `assistant` (hasil alat muncul di bawah role `user`, sesuai dengan model konten Messages API publik) dan array `content` berisi blok-blok yang didiskriminasi berdasarkan `type`:

| `type` blok   | Field                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text`        | `text`: konten teks.                                                                                                                                                                                                                                                                                                                                                                                                          |
| `tool_use`    | `id`: pengidentifikasi yang dirujuk oleh hasil alat yang cocok. `tool_name`: nama alat. `input`: argumen yang diteruskan model ke alat.                                                                                                                                                                                                                                                                                       |
| `tool_result` | `content`: output alat sebagai teks, dengan bagian-bagian yang digabungkan dengan baris baru; bagian biner seperti gambar diganti dengan penanda placeholder, dan byte mentah tidak pernah dikirim. `is_error`: apakah panggilan alat gagal. `tool_name`: nama alat, sehingga kebijakan dapat mengondisikan pada identitas alat tanpa merujuk silang ke blok sebelumnya. `tool_use_id`: `id` dari blok `tool_use` yang cocok. |
| `attachment`  | `file_name`: nama atau path file asli. `media_type`: tipe media lampiran. `size_bytes`: ukuran file asli. `text`: konten teks lampiran jika tersedia, seperti teks dokumen yang diekstrak, transkrip audio, atau metadata tautan. Byte mentah lampiran tidak pernah dikirim.                                                                                                                                                  |

Blok dengan `type` yang tidak Anda kenali adalah tambahan yang kompatibel ke depan. Satu-satunya field yang dijaminnya adalah `type`; kebijakan Anda boleh memeriksa field lain apa pun yang ada, tetapi tidak boleh menolak permintaan karena tipe yang tidak dikenali.

### Apa yang terkandung dalam transkrip

Transkrip adalah percakapan sebagaimana dilihat pengguna akhir, hingga titik inferensi: teks transkrip, panggilan alat dan hasilnya, teks lampiran yang diekstrak, dan giliran sebelumnya. Transkrip tidak pernah menyertakan prompt sistem, definisi alat, konteks internal Anthropic, penalaran tersembunyi Claude, atau byte file mentah.

Giliran yang setiap bloknya dikecualikan akan dihilangkan seluruhnya, jadi jangan berasumsi adanya pergantian ketat antara user dan assistant.

Transkrip dikirim tanpa pemotongan, sehingga percakapan panjang dengan lampiran besar menghasilkan body permintaan yang besar, hingga batas atas 10 MB. Naikkan batas body server Anda untuk menerima batas tersebut. Beberapa nilai default umum jauh lebih kecil, termasuk `client_max_body_size` nginx sebesar 1 MB dan `express.json()` Express sebesar 100 kB, dan body yang ditolak dihitung sebagai kegagalan webhook, sehingga di bawah penanganan kegagalan **Allow the request**, prompt yang terlalu besar akan mencapai model tanpa diperiksa.

### Nilai source

`source.application` adalah string terbuka, bukan enum tertutup. Nilai yang dikenal adalah `claude-ai` dan `claude-code`; [uji koneksi](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration) menggunakan `config-test`. Nilai baru dapat muncul, dan server Anda tidak boleh menolak permintaan karena nilai yang tidak dikenalinya.

Perlakukan `source.application` sebagai metadata perutean yang bersifat saran, bukan batas kepercayaan: jangan menyandarkan keputusan kebijakan yang kritis terhadap keamanan hanya padanya.

## Mengembalikan verdict

Respons dengan HTTP 200 dan body verdict JSON untuk kedua hasil; field `action` yang membedakan. Untuk mengizinkan permintaan:

```json
{
  "action": "allow"
}
```

Untuk menolaknya:

```json
{
  "action": "deny",
  "deny_reason": "This prompt appears to contain customer payment card data, which your organization's policy does not allow.",
  "reference_id": "scan_01HXPT4R9V"
}
```

| Field          | Batasan                                                                    | Semantik                                                                                                                                                                                                                                                                                                                                                   |
| -------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `action`       | `"allow"` atau `"deny"`; wajib                                             | `allow` membiarkan inferensi berlanjut; `deny` menolaknya.                                                                                                                                                                                                                                                                                                 |
| `deny_reason`  | string atau null; maksimal 500 karakter, nilai yang lebih panjang dipotong | Ditampilkan kepada pengguna akhir ketika `action` adalah `deny`; diabaikan pada `allow`.                                                                                                                                                                                                                                                                   |
| `reference_id` | string atau null; maksimal 50 karakter dari `[A-Za-z0-9._:/-]`             | Pengidentifikasi Anda sendiri untuk evaluasi ini. Ini dicatat pada [aktivitas kepatuhan](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) `inference_hooks_request_denied` milik penolakan tersebut dan tidak pernah ditampilkan kepada pengguna akhir. Jaga agar tetap opaque: tanpa konten permintaan dan tanpa data pribadi. |

Deny tidak pernah dibuang karena masalah format: `deny_reason` yang terlalu besar dipotong, `reference_id` yang salah format dibuang secara diam-diam, dan `action` tetap dihormati.

Kebalikannya tidak berlaku. Apa pun selain HTTP 200 dengan verdict yang dapat di-parse adalah kegagalan webhook, dan [penanganan kegagalan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration) organisasi Anda berlaku sebagai pengganti verdict. Khususnya:

* Jangan menandakan deny dengan status error. Respons non-200 adalah kegagalan, bukan deny.
* Nilai `action` apa pun selain `allow` atau `deny` diperlakukan sebagai kegagalan webhook.

Anthropic membaca maksimal 64 KiB dari body respons, dan body tersebut harus tidak terkompresi. Redirect tidak diikuti, dan cookie diabaikan. Field yang tidak dikenal dalam body verdict diabaikan, sehingga Anda dapat mengembalikan objek yang lebih kaya di samping field yang didokumentasikan di sini.

## Memverifikasi tanda tangan

Permintaan ditandatangani sesuai spesifikasi [Standard Webhooks](https://www.standardwebhooks.com/), menggunakan tiga header. Anthropic mengirim nama header dalam huruf kecil, dan proxy bebas mengubah kapitalisasinya, jadi cari header tersebut tanpa membedakan huruf besar-kecil.

| Header              | Isi                                                                                                                                                                                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `webhook-id`        | Pengidentifikasi unik untuk pengiriman ini. Sama dengan `request_id` pada body. Gunakan sebagai kunci idempotensi dan sebagai komponen pertama dari payload yang ditandatangani.                                                                                |
| `webhook-timestamp` | Waktu Unix dalam detik, sebagai string desimal, saat permintaan ditandatangani. Tolak timestamp yang berselisih lebih dari lima menit dari jam server Anda, ke arah mana pun.                                                                                   |
| `webhook-signature` | Satu atau lebih nilai `v1,<base64>` yang dipisahkan spasi, masing-masing merupakan HMAC-SHA256 atas `{webhook-id}.{webhook-timestamp}.{raw body bytes}`. Terima permintaan jika ada nilai yang cocok dengan milik Anda, menggunakan perbandingan constant-time. |

Dua detail menyebabkan sebagian besar bug verifikasi:

* **Verifikasi byte mentah.** Hitung HMAC atas body persis seperti yang diterima, sebelum parsing JSON atau re-encoding apa pun.
* **Decode secret dengan decoder base64 standar.** Signing secret adalah nilai setelah prefiks `whsec_`, di-encode dengan alfabet base64 standar (`+` dan `/`), begitu pula tanda tangan dalam header. Decoder URL-safe menghasilkan byte kunci yang salah setiap kali secret mengandung `+` atau `/`, yang terjadi hampir selalu.

Setelah organisasi Anda memiliki signing secret, setiap permintaan yang dikirim Anthropic ditandatangani, dan [mengaktifkan Inference hooks mensyaratkannya](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration), jadi tolak permintaan apa pun yang tiba tanpa tanda tangan. Satu pengecualian: uji koneksi yang dikirim sebelum penyimpanan pertama organisasi Anda tiba tanpa tanda tangan, karena signing secret belum ada. Terima permintaan tanpa tanda tangan hingga administrator Anda mengonfirmasi bahwa secret sudah ada, lalu tolak.

[Merotasi secret](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#rotate-your-signing-secret) adalah peralihan seketika, tetapi permintaan yang ditandatangani dengan secret sebelumnya masih dapat tiba selama sekitar satu menit setelahnya, ditambah apa pun yang sudah dalam perjalanan. Buat server keamanan AI Anda menerima tanda tangan dari kedua secret selama masa peralihan agar permintaan yang tertinggal tersebut tidak ditolak.

Contoh-contoh berikut adalah implementasi server, sehingga tidak ada tab shell: server keamanan AI adalah layanan HTTPS yang berjalan lama, bukan permintaan sekali jalan. Setiap contoh hanya menggunakan pustaka standar bahasa tersebut; proyek [Standard Webhooks](https://www.standardwebhooks.com/) juga menerbitkan pustaka verifikasi untuk sebagian besar bahasa.

<CodeGroup exclude="shell">
  ```python Python
  import base64
  import hashlib
  import hmac
  import time

  TOLERANCE_SECONDS = 300


  def verify(secret: str, headers: dict[str, str], body: bytes) -> bool:
      """Return True if the body was signed by Anthropic for this organization.

      Anthropic sends header names in lowercase, but proxies are free to
      re-case them, so normalize the lookup to lowercase.
      """
      lowercased = {name.lower(): value for name, value in headers.items()}
      try:
          message_id = lowercased["webhook-id"]
          timestamp = lowercased["webhook-timestamp"]
          signatures = lowercased["webhook-signature"]
      except KeyError:
          return False  # unsigned request: not from Anthropic

      try:
          signed_at = int(timestamp)
      except ValueError:
          return False
      if abs(time.time() - signed_at) > TOLERANCE_SECONDS:
          return False  # replayed, or the clocks disagree

      try:
          key = base64.b64decode(secret.removeprefix("whsec_"), validate=True)
      except ValueError:
          return False  # misconfigured secret: reject rather than crash

      payload = f"{message_id}.{timestamp}.".encode() + body
      expected = b"v1," + base64.b64encode(
          hmac.new(key, payload, hashlib.sha256).digest()
      )

      # Bandingkan byte: compare_digest pada str memunculkan error untuk input non-ASCII.
      return any(
          hmac.compare_digest(expected, candidate.encode())
          for candidate in signatures.split()
      )
  ```

  ```typescript TypeScript
  import { createHmac, timingSafeEqual } from "node:crypto";
  import type { IncomingHttpHeaders } from "node:http";

  const TOLERANCE_SECONDS = 300;

  /**
   * Returns true if the body was signed by Anthropic for this organization.
   *
   * Node lowercases incoming header names, matching how Anthropic sends
   * them, so look them up in lowercase.
   */
  export function verify(secret: string, headers: IncomingHttpHeaders, body: Buffer): boolean {
    const messageId = headers["webhook-id"];
    const timestamp = headers["webhook-timestamp"];
    const signatures = headers["webhook-signature"];
    if (
      typeof messageId !== "string" ||
      typeof timestamp !== "string" ||
      typeof signatures !== "string"
    ) {
      return false; // unsigned request: not from Anthropic
    }

    const signedAt = Number(timestamp);
    if (
      !Number.isFinite(signedAt) ||
      Math.abs(Date.now() / 1000 - signedAt) > TOLERANCE_SECONDS
    ) {
      return false; // replayed, or the clocks disagree
    }

    const key = Buffer.from(secret.replace(/^whsec_/, ""), "base64");
    const payload = Buffer.concat([Buffer.from(`${messageId}.${timestamp}.`), body]);
    const expected = Buffer.from(
      "v1," + createHmac("sha256", key).update(payload).digest("base64")
    );

    return signatures.split(" ").some((candidate) => {
      const candidateBytes = Buffer.from(candidate);
      return (
        candidateBytes.length === expected.length && timingSafeEqual(candidateBytes, expected)
      );
    });
  }
  ```

  ```csharp C#
  using System.Security.Cryptography;
  using System.Text;

  static class InferenceHooks
  {
      private const int ToleranceSeconds = 300;

      /// <summary>
      /// Mengembalikan true jika body ditandatangani oleh Anthropic untuk organisasi ini.
      /// Anthropic mengirim nama header dalam huruf kecil, tetapi proxy bebas
      /// mengubah kapitalisasinya, jadi cocokkan tanpa membedakan huruf besar/kecil.
      /// </summary>
      public static bool Verify(string secret, IReadOnlyDictionary<string, string> headers, byte[] body)
      {
          // TryAdd mempertahankan nilai pertama jika proxy mengirim nama duplikat
          // yang hanya berbeda kapitalisasi; konstruktor penyalin justru akan melempar exception.
          var lookup = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
          foreach (var (name, value) in headers)
          {
              lookup.TryAdd(name, value);
          }

          if (!lookup.TryGetValue("webhook-id", out var messageId) ||
              !lookup.TryGetValue("webhook-timestamp", out var timestamp) ||
              !lookup.TryGetValue("webhook-signature", out var signatures))
          {
              return false; // unsigned request: not from Anthropic
          }

          if (!long.TryParse(timestamp, out var signedAt) ||
              Math.Abs(DateTimeOffset.UtcNow.ToUnixTimeSeconds() - signedAt) > ToleranceSeconds)
          {
              return false; // replayed, or the clocks disagree
          }

          // Alfabet base64 standar: decoder URL-safe akan menghasilkan byte kunci yang salah.
          var encodedKey = secret.StartsWith("whsec_") ? secret["whsec_".Length..] : secret;
          byte[] key;
          try
          {
              key = Convert.FromBase64String(encodedKey);
          }
          catch (FormatException)
          {
              return false; // misconfigured secret: reject rather than crash
          }

          byte[] payload = [.. Encoding.UTF8.GetBytes($"{messageId}.{timestamp}."), .. body];
          var expected = Encoding.UTF8.GetBytes(
              "v1," + Convert.ToBase64String(HMACSHA256.HashData(key, payload)));

          // FixedTimeEquals berjalan dalam waktu konstan dan mengembalikan false jika panjangnya tidak cocok.
          return signatures.Split(' ', StringSplitOptions.RemoveEmptyEntries).Any(candidate =>
              CryptographicOperations.FixedTimeEquals(Encoding.UTF8.GetBytes(candidate), expected));
      }
  }
  ```

  ```go Go
  package hooks

  import (
  	"crypto/hmac"
  	"crypto/sha256"
  	"encoding/base64"
  	"net/http"
  	"strconv"
  	"strings"
  	"time"
  )

  const toleranceSeconds = 300

  // verify melaporkan apakah body ditandatangani oleh Anthropic untuk organisasi ini.
  // net/http mengkanonisasi nama header saat pencarian, sehingga nama dengan huruf besar/kecil berbeda tetap cocok.
  func verify(secret string, header http.Header, body []byte) bool {
  	messageID := header.Get("webhook-id")
  	timestamp := header.Get("webhook-timestamp")
  	signatures := header.Get("webhook-signature")
  	if messageID == "" || timestamp == "" || signatures == "" {
  		return false // unsigned request: not from Anthropic
  	}

  	signedAt, err := strconv.ParseInt(timestamp, 10, 64)
  	if err != nil {
  		return false
  	}
  	age := time.Now().Unix() - signedAt
  	if age > toleranceSeconds || age < -toleranceSeconds {
  		return false // replayed, or the clocks disagree
  	}

  	// Alfabet base64 standar: decoder URL-safe akan menghasilkan byte kunci yang salah.
  	key, err := base64.StdEncoding.DecodeString(strings.TrimPrefix(secret, "whsec_"))
  	if err != nil {
  		return false
  	}

  	mac := hmac.New(sha256.New, key)
  	mac.Write([]byte(messageID + "." + timestamp + "."))
  	mac.Write(body)
  	expected := "v1," + base64.StdEncoding.EncodeToString(mac.Sum(nil))

  	for _, candidate := range strings.Fields(signatures) {
  		if hmac.Equal([]byte(candidate), []byte(expected)) { // constant-time
  			return true
  		}
  	}
  	return false
  }
  ```

  ```java Java
  import java.nio.charset.StandardCharsets;
  import java.security.GeneralSecurityException;
  import java.security.MessageDigest;
  import java.time.Instant;
  import java.util.Base64;
  import java.util.HashMap;
  import java.util.Locale;
  import java.util.Map;
  import javax.crypto.Mac;
  import javax.crypto.spec.SecretKeySpec;

  public final class InferenceHookVerifier {
      private static final long TOLERANCE_SECONDS = 300;

      /**
       * Returns true if the body was signed by Anthropic for this organization.
       *
       * <p>Anthropic sends header names in lowercase, but proxies are free to
       * re-case them, so normalize the lookup to lowercase.
       */
      public static boolean verify(String secret, Map<String, String> headers, byte[] body) {
          Map<String, String> lowercased = new HashMap<>();
          headers.forEach((name, value) -> lowercased.put(name.toLowerCase(Locale.ROOT), value));

          String messageId = lowercased.get("webhook-id");
          String timestamp = lowercased.get("webhook-timestamp");
          String signatures = lowercased.get("webhook-signature");
          if (messageId == null || timestamp == null || signatures == null) {
              return false; // unsigned request: not from Anthropic
          }

          long signedAt;
          try {
              signedAt = Long.parseLong(timestamp);
          } catch (NumberFormatException _) {
              return false;
          }
          if (Math.abs(Instant.now().getEpochSecond() - signedAt) > TOLERANCE_SECONDS) {
              return false; // replayed, or the clocks disagree
          }

          // Alfabet base64 standar: decoder URL-safe akan menghasilkan byte kunci yang salah.
          byte[] key;
          try {
              key = Base64.getDecoder().decode(
                      secret.startsWith("whsec_") ? secret.substring("whsec_".length()) : secret);
          } catch (IllegalArgumentException _) {
              return false; // misconfigured secret: reject rather than crash
          }

          byte[] expected;
          try {
              Mac mac = Mac.getInstance("HmacSHA256");
              mac.init(new SecretKeySpec(key, "HmacSHA256"));
              mac.update((messageId + "." + timestamp + ".").getBytes(StandardCharsets.UTF_8));
              expected = ("v1," + Base64.getEncoder().encodeToString(mac.doFinal(body)))
                      .getBytes(StandardCharsets.UTF_8);
          } catch (GeneralSecurityException impossible) {
              // Setiap JVM menyertakan HmacSHA256, jadi ini tidak pernah terpicu saat runtime.
              throw new IllegalStateException(impossible);
          }

          for (String candidate : signatures.split(" ")) {
              if (MessageDigest.isEqual(candidate.getBytes(StandardCharsets.UTF_8), expected)) {
                  return true; // MessageDigest.isEqual is constant-time
              }
          }
          return false;
      }
  }
  ```

  ```php PHP
  const TOLERANCE_SECONDS = 300;

  /**
   * Returns true if the body was signed by Anthropic for this organization.
   *
   * Anthropic sends header names in lowercase, but proxies are free to
   * re-case them, so normalize the lookup to lowercase.
   */
  function verify(string $secret, array $headers, string $body): bool
  {
      $lowercased = array_change_key_case($headers, CASE_LOWER);
      $messageId = $lowercased['webhook-id'] ?? null;
      $timestamp = $lowercased['webhook-timestamp'] ?? null;
      $signatures = $lowercased['webhook-signature'] ?? null;
      if ($messageId === null || $timestamp === null || $signatures === null) {
          return false; // unsigned request: not from Anthropic
      }

      $signedAt = filter_var($timestamp, FILTER_VALIDATE_INT);
      if ($signedAt === false || abs(time() - $signedAt) > TOLERANCE_SECONDS) {
          return false; // replayed, or the clocks disagree
      }

      // Alfabet base64 standar: decoder URL-safe akan menghasilkan byte kunci yang salah.
      $encodedKey = str_starts_with($secret, 'whsec_') ? substr($secret, strlen('whsec_')) : $secret;
      $key = base64_decode($encodedKey, strict: true);
      if ($key === false) {
          return false;
      }

      $payload = "{$messageId}.{$timestamp}." . $body;
      $expected = 'v1,' . base64_encode(hash_hmac('sha256', $payload, $key, binary: true));

      foreach (explode(' ', $signatures) as $candidate) {
          if (hash_equals($expected, $candidate)) { // constant-time
              return true;
          }
      }
      return false;
  }
  ```

  ```ruby Ruby
  # base64 adalah bundled gem di Ruby 3.4: aplikasi yang dikelola Bundler perlu menambahkan gem "base64".
  require "base64"
  require "openssl"

  TOLERANCE_SECONDS = 300

  # Mengembalikan true jika body ditandatangani oleh Anthropic untuk organisasi ini.
  #
  # Anthropic mengirim nama header dalam huruf kecil, tetapi proxy bebas
  # mengubah kapitalisasinya, jadi normalisasi pencarian ke huruf kecil.
  def verify(secret, headers, body)
    lowercased = headers.transform_keys(&:downcase)
    message_id = lowercased["webhook-id"]
    timestamp = lowercased["webhook-timestamp"]
    signatures = lowercased["webhook-signature"]
    if message_id.nil? || timestamp.nil? || signatures.nil?
      return false # unsigned request: not from Anthropic
    end

    signed_at = Integer(timestamp, exception: false)
    if signed_at.nil? || (Time.now.to_i - signed_at).abs > TOLERANCE_SECONDS
      return false # replayed, or the clocks disagree
    end

    # Alfabet base64 standar: decoder URL-safe akan menghasilkan byte kunci yang salah.
    begin
      key = Base64.strict_decode64(secret.delete_prefix("whsec_"))
    rescue ArgumentError
      return false # misconfigured secret: reject rather than crash
    end

    # Masukkan body secara terpisah agar encoding-nya tidak perlu sama dengan prefix.
    hmac = OpenSSL::HMAC.new(key, "SHA256")
    hmac.update("#{message_id}.#{timestamp}.")
    hmac.update(body)
    expected = "v1," + Base64.strict_encode64(hmac.digest)

    signatures.split(" ").any? do |candidate|
      # fixed_length_secure_compare melempar error jika panjang tidak cocok, jadi periksa panjang dulu.
      candidate.bytesize == expected.bytesize &&
        OpenSSL.fixed_length_secure_compare(candidate, expected)
    end
  end
  ```
</CodeGroup>

## Semantik operasional

### Batas waktu dan percobaan ulang

Administrator Anda menetapkan batas waktu verdict antara 1 dan 10.000 md (5.000 md secara default). Anggaran ini mencakup seluruh pertukaran: koneksi, handshake TLS, permintaan, dan respons.

Anthropic mencoba ulang tepat satu kali, setelah jeda 100 md, dan hanya ketika upaya koneksi gagal. Percobaan ulang berbagi anggaran batas waktu yang sama dan membawa `webhook-id` yang sama serta tanda tangan yang sama. Setelah server keamanan AI Anda merespons, pertukaran tidak pernah dicoba ulang.

### Kegagalan webhook

Batas waktu habis, status non-200 (termasuk redirect), body respons yang tidak dapat di-parse atau terlalu besar, dan endpoint yang tidak dapat dijangkau semuanya adalah kegagalan webhook. Kegagalan webhook tidak pernah menjadi deny; sebaliknya, pengaturan [penanganan kegagalan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration) organisasi Anda yang menentukan apakah permintaan yang terdampak diblokir atau dilanjutkan tanpa pemeriksaan.

### Circuit breaker

Kegagalan webhook berkelanjutan yang disebabkan oleh server keamanan AI Anda memicu "circuit breaker" (pemutus sirkuit) yang menghentikan penegakan: Anthropic berhenti menghubungi server Anda, dan penanganan kegagalan berlaku untuk setiap permintaan. Pemulihan terjadi di sisi admin: perbaiki server, lalu minta administrator Anda mengaktifkan kembali **Enforce verdicts**. Lihat [Circuit breaker](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#circuit-breaker).

Setiap pemicuan dicatat sebagai aktivitas `inference_hooks_circuit_breaker_tripped` di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed), satu aktivitas per pemicuan. Selama circuit breaker terpicu, tidak ada aktivitas Inference hooks per permintaan yang dicatat, sehingga aktivitas pemicuan adalah satu-satunya catatan feed untuk jendela waktu terpicu tersebut.

### Latensi

Penegakan menambahkan round trip server keamanan AI Anda ke "latency" (latensi) setiap permintaan yang diatur di organisasi Anda. Jaga agar verdict tetap cepat, dan lakukan uji beban pada server Anda sebelum meluncurkannya ke organisasi besar.

### Alamat IP sumber

Permintaan ke server keamanan AI Anda berasal dari `160.79.106.0/24`, bagian dari [rentang IP keluar](https://platform.claude.com/docs/id/api/ip-addresses) Anthropic yang dipublikasikan. Masukkan blok tersebut ke allowlist, bukan rentang masuk pada halaman yang sama, yang tidak mencakupnya. Allowlist mempersempit eksposur server Anda, tetapi bukan pengganti verifikasi tanda tangan: blok tersebut membawa lalu lintas egress Anthropic di luar Inference hooks.

## Kompatibilitas ke depan

Protokol ini berkembang tanpa merusak server yang ditulis dengan benar. Server Anda harus mengabaikan:

* Field tingkat atas yang tidak dikenal pada prompt frame.
* Kunci yang tidak dikenal dalam `metadata`.
* Nilai `source.application` baru.
* Nilai `actor.type` baru. `actor` adalah union yang didiskriminasi berdasarkan `type`, dan `"user"` adalah satu-satunya jenis yang dikirim saat ini; jenis di masa mendatang hanya menjamin bahwa `type` ada.
* Blok konten dengan `type` yang tidak dikenali.

Jangan pernah menolak permintaan karena tipe blok atau field yang tidak dikenali; baca field yang Anda ketahui dan lewati sisanya.

Tipe event hook lain akan diperkenalkan di masa mendatang. Tipe event baru adalah tambahan yang tidak dapat ditangani server Anda dengan melewati sebuah field: permintaan tetap membutuhkan verdict. Ketika `type` tingkat atas adalah nilai yang tidak Anda kenali, kembalikan verdict allow alih-alih status error; respons error adalah [kegagalan webhook](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#webhook-failures), dan kegagalan berkelanjutan memicu [circuit breaker](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#circuit-breaker).

## Merancang integrasi Anda

Server keamanan AI produksi membuat beberapa pilihan desain di luar protokol wire.

**Deduplikasi berdasarkan `webhook-id`.** Header `webhook-id` unik per pengiriman dan sama dengan `request_id` pada body, dan percobaan ulang akibat kegagalan koneksi menggunakannya kembali, sehingga berfungsi sebagai kunci idempotensi. Jika Anda mencatat verdict, gunakan header ini sebagai kunci catatan.

**Catat verdict dan gabungkan penolakan.** Simpan setiap verdict yang Anda kembalikan bersama `reference_id`-nya. Setiap penolakan dicatat sebagai aktivitas kepatuhan `inference_hooks_request_denied` yang membawa `reference_id` yang dikembalikan server Anda, sehingga Anda dapat menggabungkan penolakan di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) dengan catatan yang cocok di sistem Anda sendiri.

**Arsipkan dengan server yang selalu mengizinkan.** Untuk menangkap transkrip secara real time tanpa mengawasinya, kembalikan `{"action": "allow"}` tanpa syarat dan simpan frame setelah merespons. Ini adalah alternatif berbasis push untuk polling [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api), dan menjawab sebelum Anda menyimpan menjaga round trip Anda di luar jalur kritis pengguna.

**Tulis `deny_reason` untuk pengguna akhir.** Teks yang Anda kembalikan adalah apa yang dilihat pengguna ketika permintaan mereka diblokir, dipotong pada 500 karakter. Beri tahu mereka apa yang harus diubah, seperti jenis konten apa yang harus dihapus, alih-alih mengeluarkan kode pemindai yang hanya dapat ditafsirkan oleh tim Anda.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mengonfigurasi Inference hooks" href="https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration">
    Aktifkan Inference hooks, hubungkan dan uji endpoint Anda, serta kendalikan penegakan, penanganan kegagalan, dan peluncuran.
  </Card>

  <Card title="Ikhtisar Inference hooks" href="https://platform.claude.com/docs/id/manage-claude/inference-hooks">
    Apa itu Inference hooks, cara kerja round trip verdict, dan kapan menggunakannya.
  </Card>
</CardGroup>
