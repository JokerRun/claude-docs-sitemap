---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint
fetched_at: 2026-09-17T02:21:00.513769Z
sha256: 36d35e87d7420221f832b2d4b3e0a61200ff496fa756fd95f7f4f0e51a8fd4f5
---

---
title: Mengembangkan integrasi Inference hooks
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint
description: Bangun server keamanan AI yang menerima permintaan Inference hooks bertanda tangan, memverifikasinya, dan mengembalikan putusan allow atau deny.
---

<Note>
  Inference hooks sedang dalam tahap beta dan tersedia untuk organisasi Claude Enterprise. Nama field, bentuk permintaan, dan header dapat berubah selama masa beta.
</Note>

Integrasi Inference hooks adalah server keamanan AI, yaitu layanan HTTPS yang dipanggil oleh Anthropic. Untuk setiap permintaan yang diatur, server Anda menerima `POST` bertanda tangan yang berisi transkrip percakapan, lalu merespons dengan "verdict" (putusan) allow atau deny. Halaman ini mendokumentasikan protokol untuk membangun server tersebut: skema permintaan dan putusan, verifikasi tanda tangan, serta kontrak operasional.

Untuk mengaktifkan Inference hooks dan mengarahkannya ke endpoint Anda, lihat [Mengonfigurasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration). Untuk mempelajari apa itu Inference hooks dan kapan menggunakannya, lihat [ikhtisar Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks).

## Mendapatkan putusan pertama secara bolak-balik

Integrasi paling sederhana yang berfungsi adalah server yang membaca setiap permintaan dan mengizinkannya. Jalankan salah satu server berikut dan ekspos server tersebut di URL `https://` publik. Misalnya, tempatkan server di belakang "reverse proxy" (proksi balik) yang menangani terminasi TLS pada host yang Anda kendalikan, bukan layanan reverse-tunnel; lihat [Menerima permintaan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#receive-a-request). Setelah itu, minta administrator Anda untuk [menetapkannya sebagai endpoint dan menguji koneksi](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration). Hasil **Test connection** akan melaporkan putusan allow yang dikembalikan server Anda.

<CodeGroup exclude="shell">
  ```python Python
  # Jalankan dengan: python server.py
  from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


  class VerdictHandler(BaseHTTPRequestHandler):
      protocol_version = "HTTP/1.1"  # keep the connection open between verdicts

      def do_POST(self):
          # Kuras isi body; transkrip bisa berukuran megabyte.
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
    // Kuras body sebelum menjawab; transkrip bisa berukuran megabyte.
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
      // Kuras isi body; transkrip bisa berukuran megabyte.
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
  		// Kuras body agar koneksi dapat digunakan ulang; transkrip bisa berukuran megabyte.
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
          // Kuras body tanpa mem-buffer-nya; transkrip bisa berukuran megabyte.
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
  Server-server ini menerima setiap permintaan, termasuk yang tidak bertanda tangan. Tambahkan [verifikasi tanda tangan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#verify-the-signature) sebelum Anda menerapkan penegakan.
</Note>

## Menerima permintaan

Anthropic mengirimkan `POST` HTTPS ke URL yang dikonfigurasi oleh administrator Anda. Seluruh URL yang dikonfigurasi merupakan endpoint. Tidak ada sufiks path yang tetap, jadi Anda bebas memilih path yang sesuai dengan server Anda.

Host server keamanan AI Anda di lokasi yang dapat dijangkau Anthropic, dengan ketentuan berikut:

* Menggunakan URL `https://` pada port 443.
* Berada di host yang dapat dirutekan secara publik. Rentang privat, loopback, dan carrier-grade NAT ditolak saat koneksi dibuat.
* Memiliki sertifikat yang tervalidasi terhadap penyimpanan kepercayaan CA publik.
* Merespons tanpa pengalihan (redirect).

URL yang dikonfigurasi harus merupakan tujuan akhir. Host reverse-tunnel (ngrok dan layanan tunnel serupa) tidak didukung karena diblokir oleh kebijakan jaringan Anthropic. Host server Anda di domain yang Anda kendalikan. [Mengonfigurasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration) menjelaskan cara administrator Anda menetapkan dan menguji URL tersebut.

Setiap permintaan membawa header tetap berikut. Selain itu, permintaan juga membawa [header permintaan kustom](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration) yang dikonfigurasi administrator Anda. Setelah organisasi Anda memiliki rahasia penandatanganan, permintaan juga membawa header tanda tangan `webhook-*` yang dijelaskan di [Memverifikasi tanda tangan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#verify-the-signature).

| Header            | Nilai              |
| ----------------- | ------------------ |
| `Content-Type`    | `application/json` |
| `User-Agent`      | `anthropic-dlp/1`  |
| `Accept-Encoding` | `identity`         |

Saat ini hanya ada satu event hook, yaitu prompt frame. Event ini dikirim satu kali untuk setiap permintaan inferensi yang diatur, sebelum inferensi dimulai. Anthropic menahan permintaan hingga server keamanan AI Anda merespons atau batas waktu putusan habis.

## Prompt frame

Body permintaan adalah objek JSON dengan field berikut:

| Field        | Tipe             | Deskripsi                                                                                                                                                                                                                                                                                                       |
| ------------ | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`       | string           | Event hook. Saat ini selalu `"prompt"`. Jenis event lain akan diperkenalkan di masa mendatang, jadi tangani nilai yang tidak dikenali dengan baik (lihat [Kompatibilitas ke depan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#forward-compatibility)).                          |
| `request_id` | string           | Pengidentifikasi opak per panggilan inferensi untuk korelasi. Nilainya sama dengan header `webhook-id`.                                                                                                                                                                                                         |
| `tenant_id`  | string atau null | Pengidentifikasi opak untuk organisasi pemilik permintaan.                                                                                                                                                                                                                                                      |
| `actor`      | object           | Prinsipal yang menjadi atribusi permintaan, dibedakan berdasarkan `type` (saat ini hanya nilai `"user"` yang dikirim). Berisi `id` (pengidentifikasi bertag yang stabil di seluruh permintaan untuk akun yang sama) dan `email_address` (jika tersedia). `id` dan `email_address` keduanya dapat bernilai null. |
| `source`     | object           | Aplikasi asal: `application` (lihat [Nilai source](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#source-values)).                                                                                                                                                                  |
| `messages`   | array            | Transkrip percakapan hingga titik inferensi. Lihat [Blok konten](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#content-blocks).                                                                                                                                                    |
| `session_id` | string atau null | Pengidentifikasi percakapan opak, jika ada. Jangan mem-parse nilai ini. Untuk Claude Code, nilai ini adalah pengidentifikasi sesi yang dinyatakan oleh klien secara best-effort.                                                                                                                                |
| `model`      | string atau null | Pengidentifikasi model publik untuk permintaan ini, jika tersedia.                                                                                                                                                                                                                                              |
| `metadata`   | object           | Map ekstensi cadangan dari kunci string ke nilai string, yang saat ini dikirim dalam keadaan kosong. Jangan mengandalkan isinya. Server Anda harus tetap berfungsi baik saat field ini tidak ada, saat ada, maupun saat berisi kunci apa pun.                                                                   |

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

Setiap entri dalam `messages` memiliki `role` bernilai `user` atau `assistant`. Hasil alat muncul di bawah role `user`, sesuai dengan model konten Messages API publik. Setiap entri juga memiliki array `content` berisi blok yang dibedakan berdasarkan `type`:

| `type` blok   | Field                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text`        | `text`: konten teks.                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `tool_use`    | `id`: pengidentifikasi yang dirujuk oleh hasil alat yang bersesuaian. `tool_name`: nama alat. `input`: argumen yang diteruskan model ke alat.                                                                                                                                                                                                                                                                                                         |
| `tool_result` | `content`: output alat sebagai teks, dengan bagian-bagiannya digabungkan menggunakan baris baru. Bagian biner seperti gambar diganti dengan penanda placeholder, dan byte mentah tidak pernah dikirim. `is_error`: apakah panggilan alat gagal. `tool_name`: nama alat, sehingga kebijakan dapat menggunakan identitas alat sebagai kondisi tanpa perlu merujuk silang ke blok sebelumnya. `tool_use_id`: `id` dari blok `tool_use` yang bersesuaian. |
| `attachment`  | `file_name`: nama file atau path asli. `media_type`: tipe media lampiran. `size_bytes`: ukuran file asli. `text`: konten teks lampiran jika tersedia, seperti teks dokumen yang diekstrak, transkrip audio, atau metadata tautan. Byte mentah lampiran tidak pernah dikirim.                                                                                                                                                                          |

Sebagian besar field ini dapat bernilai `null` jika nilainya tidak diketahui. Pengecualiannya adalah `type`, `text` pada blok `text`, serta `content` dan `is_error` pada blok `tool_result`. Misalnya, gambar dikirim sebagai blok `attachment` dengan `file_name` dan `text` bernilai `null`.

Blok dengan `type` yang tidak Anda kenali merupakan tambahan yang kompatibel ke depan. Satu-satunya field yang dijamin ada pada blok tersebut adalah `type`. Kebijakan Anda boleh memeriksa field lain yang ada, tetapi tidak boleh menolak permintaan karena tipe yang tidak dikenali.

### Isi transkrip

Transkrip adalah percakapan sebagaimana dilihat oleh pengguna akhir, hingga titik inferensi. Isinya meliputi teks transkrip, panggilan alat beserta hasilnya, teks lampiran yang diekstrak, dan giliran sebelumnya. Transkrip tidak pernah menyertakan "system prompt" (prompt sistem), definisi alat, konteks internal Anthropic, penalaran tersembunyi Claude, atau byte file mentah.

Giliran yang seluruh bloknya dikecualikan akan dihilangkan sepenuhnya. Karena itu, jangan berasumsi bahwa giliran user dan assistant selalu bergantian secara ketat.

Transkrip dikirim tanpa dipotong, sehingga percakapan panjang dengan lampiran besar menghasilkan body permintaan yang besar. Dalam praktiknya, "context window" (jendela konteks) model menjaga ukuran body di bawah sekitar 10 MB, tetapi protokol mengizinkan hingga 64 MiB. Beberapa nilai default yang umum jauh lebih kecil, termasuk `client_max_body_size` nginx sebesar 1 MB dan `express.json()` Express sebesar 100 kB. Body yang ditolak dihitung sebagai kegagalan webhook. Jika penanganan kegagalan diatur ke **Allow the request**, prompt yang terlalu besar akan sampai ke model tanpa diperiksa.

### Nilai source

`source.application` adalah string terbuka, bukan enum tertutup. Nilai yang umum adalah `claude-ai`, `claude-code`, dan `cowork`. [Uji koneksi](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration) dan [pemeriksaan pemulihan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#circuit-breaker) otomatis circuit breaker menggunakan `config-test`. Nilai baru dapat muncul, dan server Anda tidak boleh menolak permintaan karena nilai yang tidak dikenalinya.

Perlakukan `source.application` sebagai metadata perutean yang bersifat anjuran, bukan batas kepercayaan. Jangan mendasarkan keputusan kebijakan yang kritis bagi keamanan hanya pada nilai ini.

## Mengembalikan putusan

Untuk kedua hasil, respons dengan HTTP 200 dan body putusan JSON. Field `action` menentukan hasilnya. Untuk mengizinkan permintaan:

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

| Field          | Batasan                                                                         | Semantik                                                                                                                                                                                                                                                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `action`       | `"allow"` atau `"deny"`; wajib                                                  | `allow` mengizinkan inferensi berlanjut; `deny` menolaknya.                                                                                                                                                                                                                                                                                                                 |
| `deny_reason`  | string atau null; maksimal 500 karakter, nilai yang lebih panjang akan dipotong | Ditampilkan kepada pengguna akhir saat `action` bernilai `deny`; diabaikan pada `allow`.                                                                                                                                                                                                                                                                                    |
| `reference_id` | string atau null; maksimal 50 karakter dari `[A-Za-z0-9._:/-]`                  | Pengidentifikasi milik Anda sendiri untuk evaluasi ini. Nilai ini dicatat pada [aktivitas kepatuhan](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) `inference_hooks_request_denied` untuk penolakan tersebut dan tidak pernah ditampilkan kepada pengguna akhir. Jaga agar tetap opak: jangan sertakan konten permintaan maupun data pribadi. |

Putusan deny tidak pernah dibuang karena masalah format. `deny_reason` yang terlalu panjang akan dipotong, `reference_id` yang formatnya salah akan dibuang tanpa pemberitahuan, dan `action` tetap dihormati.

Hal sebaliknya tidak berlaku. Respons apa pun selain HTTP 200 dengan putusan yang dapat di-parse dianggap sebagai kegagalan webhook. Dalam kasus ini, [penanganan kegagalan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration) organisasi Anda yang berlaku, bukan putusan. Secara khusus:

* Jangan menandakan deny dengan status error. Respons non-200 adalah kegagalan, bukan deny.
* Nilai `action` apa pun selain `allow` atau `deny` diperlakukan sebagai kegagalan webhook.

Anthropic membaca paling banyak 64 KiB dari body respons, dan body tersebut harus tidak terkompresi. Pengalihan tidak diikuti, dan cookie diabaikan. Field yang tidak dikenal dalam body putusan diabaikan, sehingga Anda dapat mengembalikan objek yang lebih kaya di samping field yang didokumentasikan di sini.

## Memverifikasi tanda tangan

Permintaan ditandatangani sesuai spesifikasi [Standard Webhooks](https://www.standardwebhooks.com/) menggunakan tiga header. Anthropic mengirimkan nama header dalam huruf kecil, tetapi proksi dapat mengubah kapitalisasinya. Karena itu, cari header tersebut tanpa membedakan huruf besar dan kecil.

| Header              | Isi                                                                                                                                                                                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `webhook-id`        | Pengidentifikasi unik untuk pengiriman ini. Nilainya sama dengan `request_id` pada body. Gunakan sebagai "idempotency key" (kunci idempotensi) dan sebagai komponen pertama dari payload yang ditandatangani.                                                  |
| `webhook-timestamp` | Waktu Unix dalam detik, sebagai string desimal, saat permintaan ditandatangani. Tolak timestamp yang berselisih lebih dari lima menit dari jam server Anda, baik lebih awal maupun lebih lambat.                                                               |
| `webhook-signature` | Satu atau beberapa nilai `v1,<base64>` yang dipisahkan spasi. Setiap nilai adalah HMAC-SHA256 atas `{webhook-id}.{webhook-timestamp}.{raw body bytes}`. Terima permintaan jika ada nilai yang cocok dengan milik Anda, menggunakan perbandingan waktu-konstan. |

Dua detail berikut menjadi penyebab sebagian besar bug verifikasi:

* **Verifikasi byte mentah.** Hitung HMAC atas body persis seperti yang diterima, sebelum parsing JSON atau pengodean ulang apa pun.
* **Dekode secret dengan dekoder base64 standar.** "Signing secret" (rahasia penandatanganan) adalah nilai setelah prefiks `whsec_`. Nilai ini dikodekan dengan alfabet base64 standar (`+` dan `/`), sama seperti tanda tangan di header. Dekoder yang aman untuk URL akan menghasilkan byte kunci yang salah setiap kali secret mengandung `+` atau `/`, dan hal ini hampir selalu terjadi.

Setelah organisasi Anda memiliki rahasia penandatanganan, setiap permintaan yang dikirim Anthropic akan ditandatangani, termasuk uji koneksi. Hal ini karena alur penyiapan membuat secret sebelum uji pertama dijalankan. [Mengaktifkan Inference hooks memerlukan secret](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration), jadi tolak setiap permintaan yang datang tanpa tanda tangan.

Ada satu pengecualian. Organisasi yang mengaktifkan Inference hooks sebelum secret diwajibkan akan terus mengirim permintaan tanpa tanda tangan hingga administratornya membuat secret. Terima permintaan tanpa tanda tangan hanya sampai administrator Anda mengonfirmasi bahwa secret sudah ada, lalu tolak permintaan tersebut.

[Merotasi secret](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#rotate-your-signing-secret) berlaku seketika. Namun, permintaan yang ditandatangani dengan secret sebelumnya masih dapat tiba selama sekitar satu menit setelahnya, ditambah permintaan yang sudah dalam perjalanan. Konfigurasikan server keamanan AI Anda agar menerima tanda tangan dari kedua secret selama masa peralihan, sehingga permintaan yang terlambat tersebut tidak ditolak.

Contoh-contoh berikut adalah implementasi server, sehingga tidak ada tab shell. Server keamanan AI adalah layanan HTTPS yang berjalan lama, bukan permintaan sekali jalan. Setiap contoh hanya menggunakan pustaka standar bahasa yang bersangkutan. Proyek [Standard Webhooks](https://www.standardwebhooks.com/) juga menerbitkan pustaka verifikasi untuk sebagian besar bahasa.

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

      # Bandingkan bytes: compare_digest pada str memunculkan error untuk input non-ASCII.
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
          // TryAdd mempertahankan nilai pertama jika proxy mengirim nama yang duplikat
          // beda kapitalisasi; konstruktor penyalin justru akan melempar exception.
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

          // Alfabet base64 standar: decoder URL-safe menghasilkan byte kunci yang salah.
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

          // FixedTimeEquals berjalan dalam waktu konstan dan mengembalikan false jika panjang berbeda.
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
  // net/http mengkanonikalisasi nama header saat pencarian, jadi nama dengan kapitalisasi berbeda tetap cocok.
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

  	// Alfabet base64 standar: decoder yang aman untuk URL akan menghasilkan byte kunci yang salah.
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

          // Alfabet base64 standar: decoder yang aman untuk URL akan menghasilkan byte kunci yang salah.
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

      // Alfabet base64 standar: decoder yang aman untuk URL akan menghasilkan byte kunci yang salah.
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
  # mengubah kapitalisasinya, jadi normalisasikan pencarian ke huruf kecil.
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

    # Alfabet base64 standar: decoder yang aman untuk URL menghasilkan byte kunci yang salah.
    begin
      key = Base64.strict_decode64(secret.delete_prefix("whsec_"))
    rescue ArgumentError
      return false # misconfigured secret: reject rather than crash
    end

    # Masukkan body secara terpisah agar encoding-nya tidak perlu sama dengan encoding prefiks.
    hmac = OpenSSL::HMAC.new(key, "SHA256")
    hmac.update("#{message_id}.#{timestamp}.")
    hmac.update(body)
    expected = "v1," + Base64.strict_encode64(hmac.digest)

    signatures.split(" ").any? do |candidate|
      # fixed_length_secure_compare memunculkan error jika panjang tidak cocok, jadi periksa panjang dulu.
      candidate.bytesize == expected.bytesize &&
        OpenSSL.fixed_length_secure_compare(candidate, expected)
    end
  end
  ```
</CodeGroup>

## Semantik operasional

### Batas waktu dan percobaan ulang

Administrator Anda menetapkan batas waktu putusan antara 1 dan 10.000ms (default 5.000ms). Batas waktu ini mencakup seluruh pertukaran: koneksi, TLS handshake, permintaan, dan respons.

Anthropic mencoba ulang tepat satu kali setelah jeda 100ms, dan hanya jika upaya koneksi gagal. Percobaan ulang menggunakan batas waktu yang sama serta membawa `webhook-id` dan tanda tangan yang sama. Setelah server keamanan AI Anda merespons, pertukaran tidak akan pernah dicoba ulang.

### Kegagalan webhook

Semua kondisi berikut merupakan kegagalan webhook:

* Batas waktu habis.
* Status non-200, termasuk pengalihan.
* Body respons yang tidak dapat di-parse atau terlalu besar.
* Endpoint yang tidak dapat dijangkau.

Kegagalan webhook tidak pernah menjadi deny. Sebagai gantinya, pengaturan [penanganan kegagalan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration) organisasi Anda menentukan apakah permintaan yang terdampak diblokir atau dilanjutkan tanpa pemeriksaan.

### Circuit breaker

Kegagalan webhook berkelanjutan yang disebabkan oleh server keamanan AI Anda akan memicu "circuit breaker" (pemutus sirkuit) yang menghentikan penegakan. Anthropic berhenti menghubungi server Anda, dan penanganan kegagalan berlaku untuk setiap permintaan.

Mulai 10 menit setelah circuit breaker terpicu, Anthropic memeriksa apakah server Anda telah pulih. Paling sering sekitar sekali per menit, Anthropic mengirimkan permintaan uji sintetis yang sama dengan yang dikirim oleh **Test connection** (`source.application` bernilai `config-test`). Permintaan ini ditandatangani seperti permintaan lainnya dan tidak membawa konten pengguna. Respons permintaan tersebut seperti biasa:

* Putusan yang valid, baik allow maupun deny, akan mereset circuit breaker dan penegakan dilanjutkan.
* Kegagalan webhook membuat circuit breaker tetap terpicu, dan pemeriksaan terus berlanjut.

Administrator juga dapat mereset circuit breaker kapan saja, dan perubahan konfigurasi oleh administrator akan menghentikan pemeriksaan otomatis. Lihat [Circuit breaker](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#circuit-breaker).

Setiap kali circuit breaker terpicu, kejadian tersebut dicatat sebagai satu aktivitas `inference_hooks_circuit_breaker_tripped` di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed). Selama circuit breaker terpicu, tidak ada aktivitas Inference hooks per permintaan yang dicatat. Karena itu, aktivitas pemicu tersebut adalah satu-satunya catatan di feed untuk periode saat circuit breaker terpicu.

### Latensi

Penegakan menambahkan waktu bolak-balik server keamanan AI Anda ke "latency" (latensi) setiap permintaan yang diatur di organisasi Anda. Jaga agar putusan tetap cepat, dan lakukan uji beban pada server Anda sebelum meluncurkannya ke organisasi besar.

### Alamat IP sumber

Permintaan ke server keamanan AI Anda berasal dari `160.79.106.0/24`, yang merupakan bagian dari [rentang IP keluar](https://platform.claude.com/docs/id/api/ip-addresses) yang dipublikasikan Anthropic. Masukkan blok tersebut ke allowlist, bukan rentang masuk di halaman yang sama, karena rentang masuk tidak mencakup blok ini. Allowlist mempersempit paparan server Anda, tetapi tidak menggantikan verifikasi tanda tangan, karena blok tersebut juga membawa lalu lintas keluar Anthropic di luar Inference hooks.

## Kompatibilitas ke depan

Protokol ini berkembang tanpa merusak server yang ditulis dengan benar. Server Anda harus mengabaikan:

* Field tingkat atas yang tidak dikenal pada prompt frame.
* Kunci yang tidak dikenal dalam `metadata`.
* Nilai `source.application` yang baru.
* Nilai `actor.type` yang baru. `actor` adalah union yang dibedakan berdasarkan `type`, dan `"user"` adalah satu-satunya jenis yang dikirim saat ini. Jenis di masa mendatang hanya menjamin bahwa `type` ada.
* Blok konten dengan `type` yang tidak dikenali.

Jangan pernah menolak permintaan karena tipe blok atau field yang tidak dikenali. Baca field yang Anda ketahui dan lewati sisanya.

Jenis event hook lain akan diperkenalkan di masa mendatang. Jenis event baru tidak dapat ditangani hanya dengan melewati field, karena permintaan tetap memerlukan putusan. Jika `type` tingkat atas bernilai sesuatu yang tidak Anda kenali, kembalikan putusan allow, bukan status error. Respons error merupakan [kegagalan webhook](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#webhook-failures), dan kegagalan yang berkelanjutan akan memicu [circuit breaker](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#circuit-breaker).

## Merancang integrasi Anda

Server keamanan AI untuk produksi memerlukan beberapa keputusan desain di luar protokol komunikasi.

**Lakukan deduplikasi berdasarkan `webhook-id`.** Header `webhook-id` bersifat unik per pengiriman dan nilainya sama dengan `request_id` pada body. Percobaan ulang akibat kegagalan koneksi menggunakan kembali nilai ini, sehingga header ini dapat berfungsi sebagai kunci idempotensi. Jika Anda mencatat putusan, gunakan nilai ini sebagai kunci catatan.

**Catat putusan dan gabungkan data penolakan.** Simpan setiap putusan yang Anda kembalikan beserta `reference_id`-nya. Setiap penolakan dicatat sebagai aktivitas kepatuhan `inference_hooks_request_denied` yang membawa `reference_id` yang dikembalikan server Anda. Dengan begitu, Anda dapat menggabungkan data penolakan di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) dengan catatan yang bersesuaian di sistem Anda sendiri.

**Arsipkan dengan server yang selalu mengizinkan.** Untuk merekam transkrip secara real-time tanpa mengawasinya, kembalikan `{"action": "allow"}` tanpa syarat dan simpan frame setelah merespons. Ini adalah alternatif berbasis push untuk polling [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api). Dengan menjawab sebelum menyimpan, waktu bolak-balik Anda tidak berada di jalur kritis pengguna.

**Tulis `deny_reason` untuk pengguna akhir.** Teks yang Anda kembalikan adalah pesan yang dilihat pengguna saat permintaannya diblokir, dan dipotong pada 500 karakter. Beri tahu pengguna apa yang perlu diubah, misalnya jenis konten yang harus dihapus, alih-alih menampilkan kode pemindai yang hanya dapat dipahami oleh tim Anda.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mengonfigurasi Inference hooks" href="https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration">
    Aktifkan Inference hooks, hubungkan dan uji endpoint Anda, serta kendalikan penegakan, penanganan kegagalan, dan peluncuran.
  </Card>

  <Card title="Ikhtisar Inference hooks" href="https://platform.claude.com/docs/id/manage-claude/inference-hooks">
    Apa itu Inference hooks, cara kerja putusan secara bolak-balik, dan kapan menggunakannya.
  </Card>
</CardGroup>
