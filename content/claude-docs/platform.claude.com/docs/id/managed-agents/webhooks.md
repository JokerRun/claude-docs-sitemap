---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/webhooks
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 81725d60af0415968aae3a7d2892f446b36c5482769a5268b29993c5467e164d
---

# Berlangganan webhook

Dapatkan notifikasi saat peristiwa penting terjadi tanpa perlu melakukan polling.

---

Sesi adalah interaksi yang berjalan lama. Meskipun sebagian besar interaksi real-time terjadi melalui [aliran peristiwa SSE](/docs/id/managed-agents/events-and-streaming), webhook memberi tahu Anda tentang perubahan status utama.

Peristiwa webhook mengembalikan `type` dan `id` peristiwa, bukan objek lengkapnya. Saat Anda menerima peristiwa webhook, Anda perlu mengambil objek tersebut secara langsung dengan panggilan `GET`. Hal ini menghindari pengiriman data usang pada percobaan ulang dan menjaga setiap pengiriman tetap kecil.

## Jenis peristiwa yang didukung \{#supported-event-types}

<Tabs>
  <Tab title="Peristiwa sesi">
    | Peristiwa | Pemicu |
    | ----- | ------- |
    | `session.status_run_started` | Eksekusi agen dimulai. Ini dipicu pada setiap transisi status sesi ke `running`. |
    | `session.status_idled` | Agen menunggu input, misalnya persetujuan izin alat atau pesan pengguna baru. |
    | `session.status_rescheduled` | Terjadi kesalahan sementara dan sesi mencoba ulang secara otomatis. |
    | `session.status_terminated` | Sesi mengalami kesalahan terminal. |
    | `session.thread_created` | [Thread multiagen](/docs/id/managed-agents/multi-agent) baru dibuka, yang berarti agen tambahan yang dipanggil oleh koordinator mulai menjalankan pekerjaan. |
    | `session.thread_idled` | Sebuah agen dalam [interaksi multiagen](/docs/id/managed-agents/multi-agent) sedang menunggu input. |
    | `session.thread_terminated` | Sebuah [thread multiagen](/docs/id/managed-agents/multi-agent) diarsipkan. |
    | `session.outcome_evaluation_ended` | [Evaluasi hasil](/docs/id/managed-agents/define-outcomes) untuk satu iterasi telah selesai. |
  </Tab>
  <Tab title="Peristiwa vault">
    | Peristiwa | Pemicu |
    | ----- | ------- |
    | `vault.created` | Vault berhasil dibuat. |
    | `vault.archived` | Vault diarsipkan. Peristiwa `vault_credential.archived` juga dikirimkan untuk setiap kredensial yang mendasarinya. |
    | `vault.deleted` | Vault dihapus. Peristiwa `vault_credential.deleted` juga dikirimkan untuk setiap kredensial yang mendasarinya. |
    | `vault_credential.created` | Kredensial berhasil dibuat. |
    | `vault_credential.archived` | Kredensial diarsipkan, baik secara langsung maupun sebagai akibat dari pengarsipan vault. |
    | `vault_credential.deleted` | Kredensial dihapus, baik secara langsung maupun sebagai akibat dari penghapusan vault. |
    | `vault_credential.refresh_failed` | Kredensial `mcp_oauth` tidak dapat di-refresh (refresh token tidak valid, atau kesalahan yang tidak dapat dipulihkan dari server OAuth). |
  </Tab>
</Tabs>

## Mendaftarkan endpoint \{#register-an-endpoint}

Kunjungi **Manage > Webhooks** di [Console](https://platform.claude.com/settings/workspaces/default/webhooks).

Sebuah endpoint webhook terdiri dari:

- **URL:** Harus HTTPS pada port 443 dengan hostname yang dapat di-resolve secara publik.
- **Jenis peristiwa:** Daftar nilai `data.type` yang diterima endpoint ini. Sebuah endpoint hanya menerima peristiwa yang dilanggannya, ditambah peristiwa uji (lihat [Perilaku pengiriman](#perilaku-pengiriman)).
- **Signing secret:** Secret 32-byte dengan prefiks `whsec_` yang dihasilkan saat pembuatan. Secret ini hanya ditampilkan sekali, jadi simpan dengan aman untuk memverifikasi pengiriman webhook.

## Memverifikasi signature \{#verify-the-signature}

Setiap pengiriman membawa header `X-Webhook-Signature`. Gunakan helper `unwrap()` dari SDK untuk memverifikasi signature dan mem-parse peristiwa dalam satu langkah. Helper ini akan melempar error jika signature tidak valid atau payload berusia lebih dari lima menit.

Atur `ANTHROPIC_WEBHOOK_SIGNING_KEY` ke secret dengan prefiks `whsec_` yang ditampilkan saat pembuatan endpoint.

<CodeGroup>
```python Python nocheck
from flask import Flask, request
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # unwrap() memunculkan error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
        event = client.beta.webhooks.unwrap(
            request.get_data(as_text=True),
            headers=dict(request.headers),
        )
    except Exception:
        return "invalid signature", 400

    if event.data.type == "session.status_idled":
        print("session idled:", event.data.id)
    # tangani tipe event lainnya

    return "", 200
```

```typescript TypeScript nocheck
import express from "express";
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
const app = express();

// PENTING: gunakan express.raw(), bukan express.json(). Tanda tangan dihitung dari byte mentah.
app.post("/webhook", express.raw({ type: "application/json" }), (req, res) => {
  let event;
  try {
    // unwrap() melempar error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
    event = client.beta.webhooks.unwrap(req.body.toString("utf8"), {
      headers: req.headers as Record<string, string>
    });
  } catch {
    return res.status(400).send("invalid signature");
  }

  switch (event.data.type) {
    case "session.status_idled":
      console.log("session idled:", event.data.id);
      break;
    // tangani tipe event lainnya
  }

  res.sendStatus(200);
});
```

```csharp C# nocheck
using Anthropic;

var client = new AnthropicClient(); // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
var app = WebApplication.Create(args);

app.MapPost("/webhook", async (HttpRequest request) =>
{
    using var reader = new StreamReader(request.Body);
    var body = await reader.ReadToEndAsync();
    var headers = request.Headers.ToDictionary(header => header.Key, header => header.Value.ToString());

    UnwrapWebhookEvent webhookEvent;
    try
    {
        // Unwrap() melempar exception jika tanda tangan tidak valid atau payload sudah kedaluwarsa
        webhookEvent = client.Beta.Webhooks.Unwrap(body, headers);
    }
    catch
    {
        return Results.BadRequest("invalid signature");
    }

    if (webhookEvent.Data.TryPickSessionStatusIdled(out var idled))
    {
        Console.WriteLine($"session idled: {idled.ID}");
    }
    // tangani tipe event lainnya

    return Results.Ok();
});
```

```go Go nocheck
package main

import (
	"fmt"
	"io"
	"net/http"

	"github.com/anthropics/anthropic-sdk-go"
)

var client = anthropic.NewClient() // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env

func webhook(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "could not read body", http.StatusBadRequest)
		return
	}

	// Unwrap mengembalikan error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
	event, err := client.Beta.Webhooks.Unwrap(body, r.Header)
	if err != nil {
		http.Error(w, "invalid signature", http.StatusBadRequest)
		return
	}

	switch event.Data.Type {
	case "session.status_idled":
		fmt.Println("session idled:", event.Data.ID)
		// tangani tipe event lainnya
	}

	w.WriteHeader(http.StatusOK)
}

func main() {
	http.HandleFunc("/webhook", webhook)
}
```

```java Java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.UnwrapWebhookParams;
import com.anthropic.core.http.Headers;
import com.sun.net.httpserver.HttpServer;

// membaca ANTHROPIC_WEBHOOK_SIGNING_KEY dari env
AnthropicClient client = AnthropicOkHttpClient.fromEnv();

void main() throws Exception {
    var server = HttpServer.create(new InetSocketAddress(8000), 0);
    server.createContext("/webhook", exchange -> {
        var body = new String(exchange.getRequestBody().readAllBytes());
        var headers = Headers.builder();
        exchange.getRequestHeaders().forEach(headers::put);

        try {
            // unwrap() melempar error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
            var event = client.beta().webhooks().unwrap(
                UnwrapWebhookParams.builder()
                    .body(body)
                    .headers(headers.build())
                    .build());

            event.data().sessionStatusIdled().ifPresent(idled ->
                IO.println("session idled: " + idled.id()));
            // tangani tipe event lainnya

            exchange.sendResponseHeaders(200, -1);
        } catch (Exception _) {
            exchange.sendResponseHeaders(400, -1);
        }
        exchange.close();
    });
}
```

```php PHP nocheck
use Anthropic\Client;
use Anthropic\Core\Exceptions\WebhookException;

$client = new Client(); // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env

$body = file_get_contents('php://input');
$headers = getallheaders();

try {
    // unwrap() melempar error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
    $event = $client->beta->webhooks->unwrap($body, headers: $headers);
} catch (WebhookException) {
    http_response_code(400);
    exit('invalid signature');
}

match ($event->data->type) {
    'session.status_idled' => print "session idled: {$event->data->id}\n",
    // tangani tipe event lainnya
    default => null,
};

http_response_code(200);
```

```ruby Ruby nocheck
require "sinatra"
require "anthropic"

client = Anthropic::Client.new # reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env

post "/webhook" do
  headers = request.env
    .select { |key, _| key.start_with?("HTTP_") }
    .transform_keys { it.delete_prefix("HTTP_").downcase.tr("_", "-") }

  begin
    # unwrap memunculkan error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
    event = client.beta.webhooks.unwrap(request.body.read, headers: headers)
  rescue StandardError
    halt 400, "invalid signature"
  end

  if event.data.type == "session.status_idled"
    puts "session idled: #{event.data.id}"
  end
  # tangani tipe event lainnya

  status 200
end
```
</CodeGroup>

## Menangani peristiwa \{#handle-an-event}

Parse body, lakukan switch pada `data.type`, dan ambil resource berdasarkan ID. Kembalikan `2xx` apa pun untuk mengonfirmasi. Apa pun selain itu (termasuk `3xx`) dihitung sebagai kegagalan dan memicu percobaan ulang.

Setiap payload peristiwa memiliki struktur yang sama, termasuk jenis peristiwa, identifier, dan timestamp kapan objek dibuat.

```json
{
  "type": "event",
  "id": "event_01ABC...",
  "created_at": "2026-03-18T14:05:22Z",
  "data": {
    "type": "session.status_idled",
    "id": "sesn_01XYZ...",
    "organization_id": "8a3d2f1e-...",
    "workspace_id": "c7b0e4d9-..."
  }
}
```

<CodeGroup>
```python Python nocheck
if event.data.type == "session.status_idled":
    session = client.beta.sessions.retrieve(event.data.id)
    notify_user(session)
return "", 204
```

```typescript TypeScript nocheck
if (event.data.type === "session.status_idled") {
  const session = await client.beta.sessions.retrieve(event.data.id);
  notifyUser(session);
}
res.sendStatus(204);
```

```csharp C# nocheck
if (webhookEvent.Data.TryPickSessionStatusIdled(out var idled))
{
    var session = await client.Beta.Sessions.Retrieve(idled.ID);
    NotifyUser(session);
}
return Results.StatusCode(204);
```

```go Go nocheck
if event.Data.Type == "session.status_idled" {
	session, err := client.Beta.Sessions.Get(r.Context(), event.Data.ID, anthropic.BetaSessionGetParams{})
	if err != nil {
		panic(err)
	}
	notifyUser(session)
}
w.WriteHeader(http.StatusNoContent)
```

```java Java nocheck
event.data().sessionStatusIdled().ifPresent(idled -> {
    var session = client.beta().sessions().retrieve(idled.id());
    notifyUser(session);
});
exchange.sendResponseHeaders(204, -1);
```

```php PHP nocheck
if ($event->data->type === 'session.status_idled') {
    $session = $client->beta->sessions->retrieve($event->data->id);
    notifyUser($session);
}
http_response_code(204);
```

```ruby Ruby nocheck
if event.data.type == "session.status_idled"
  session = client.beta.sessions.retrieve(event.data.id)
  notify_user(session)
end
status 204
```
</CodeGroup>

`event.id` tingkat atas bersifat unik per peristiwa, bukan per pengiriman. Jika Anda menerima `event.id` yang sama dua kali, itu adalah percobaan ulang dan Anda dapat mengabaikannya.

## Perilaku pengiriman \{#delivery-behavior}

- **Urutan tidak dijamin.** `session.status_idled` mungkin tiba sebelum `session.outcome_evaluation_ended` meskipun hasil dihasilkan terlebih dahulu. Gunakan timestamp `created_at` untuk mengurutkan jika urutan penting.
- **Percobaan ulang:** Anthropic mencoba ulang setidaknya sekali. Percobaan ulang mengirimkan `event.id` yang sama.
- **Redirect tidak diikuti.** `3xx` diperlakukan sebagai kegagalan. Jika endpoint Anda berpindah, perbarui URL di Console.
- **Penonaktifan otomatis:** Sebuah endpoint secara otomatis diatur ke `disabled` dengan `disabled_reason` yang dapat dibaca mesin setelah sekitar 20 pengiriman gagal berturut-turut, atau segera jika hostname di-resolve ke IP privat atau endpoint mengembalikan redirect. Aktifkan kembali secara manual di Console setelah menyelesaikan masalah.