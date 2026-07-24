---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/webhooks
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: b799e1fcb8beeef4cd457c80b01d25a93e58d1a412eae20a46587fcd799d52f3
---

# Berlangganan webhook

Dapatkan notifikasi saat peristiwa penting terjadi tanpa polling.

---

Sesi adalah interaksi yang berjalan lama. Meskipun sebagian besar interaksi real-time terjadi melalui [event stream SSE](/docs/id/managed-agents/events-and-streaming), webhook memberi tahu Anda tentang perubahan status yang penting.

Event webhook mengembalikan `type` dan `id` event, bukan objek lengkapnya. Saat Anda menerima event webhook, Anda perlu mengambil objek tersebut secara langsung dengan panggilan `GET`. Ini menghindari pengiriman data usang saat percobaan ulang dan menjaga setiap pengiriman tetap kecil.

## Tipe event yang didukung

<Tabs>
  <Tab title="Event sesi">
    | Event                              | Pemicu                                                                                                                                                                                                                                                                                 |
    | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `session.status_run_started`       | Eksekusi agen dimulai. Ini terpicu pada setiap transisi status sesi ke `running`.                                                                                                                                                                                                      |
    | `session.status_idled`             | Agen menunggu input, misalnya persetujuan izin alat atau pesan pengguna baru.                                                                                                                                                                                                          |
    | `session.status_rescheduled`       | Terjadi error sementara dan sesi sedang mencoba ulang secara otomatis.                                                                                                                                                                                                                 |
    | `session.status_terminated`        | Sesi berakhir, baik karena error maupun karena selesai.                                                                                                                                                                                                                                |
    | `session.thread_created`           | [Thread multiagen](/docs/id/managed-agents/multiagent-orchestration) baru dibuka, yang berarti agen tambahan yang dipanggil oleh koordinator mulai bekerja.                                                                                                                            |
    | `session.thread_idled`             | Sebuah agen dalam [interaksi multiagen](/docs/id/managed-agents/multiagent-orchestration) sedang menunggu input.                                                                                                                                                                       |
    | `session.thread_terminated`        | Sebuah [thread multiagen](/docs/id/managed-agents/multiagent-orchestration) berakhir, baik karena agen anak menyelesaikan pekerjaannya maupun karena thread tersebut diarsipkan. Hanya terpicu untuk thread anak; berakhirnya thread utama muncul sebagai `session.status_terminated`. |
    | `session.outcome_evaluation_ended` | [Evaluasi hasil](/docs/id/managed-agents/define-outcomes) untuk satu iterasi selesai.                                                                                                                                                                                                  |
    | `session.updated`                  | Properti sesi berubah (misalnya, nama atau konfigurasinya diperbarui).                                                                                                                                                                                                                 |
    | `session.deleted`                  | Sesi dihapus secara permanen. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan event itu sendiri sebagai final.                                                                                                                                                             |
  </Tab>

  <Tab title="Event vault">
    | Event                             | Pemicu                                                                                                                                                                                             |
    | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `vault.created`                   | Vault dibuat.                                                                                                                                                                                      |
    | `vault.archived`                  | Vault diarsipkan. Event `vault_credential.archived` juga dikeluarkan untuk setiap kredensial di dalamnya.                                                                                          |
    | `vault.deleted`                   | Vault dihapus. Event `vault_credential.deleted` juga dikeluarkan untuk setiap kredensial di dalamnya. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan event itu sendiri sebagai final. |
    | `vault_credential.created`        | Kredensial dibuat.                                                                                                                                                                                 |
    | `vault_credential.archived`       | Kredensial diarsipkan, baik secara langsung maupun sebagai akibat dari pengarsipan vault.                                                                                                          |
    | `vault_credential.deleted`        | Kredensial dihapus, baik secara langsung maupun sebagai akibat dari penghapusan vault. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan event itu sendiri sebagai final.                |
    | `vault_credential.refresh_failed` | Kredensial `mcp_oauth` tidak dapat disegarkan (refresh token tidak valid, atau error yang tidak dapat dipulihkan dari server OAuth).                                                               |
  </Tab>

  <Tab title="Event agen">
    Event ini melacak siklus hidup sumber daya agen di workspace Anda, dan berbeda dari event agen yang dikirimkan pada event stream sebuah sesi.

    | Event            | Pemicu                                                                                                                                                 |
    | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | `agent.created`  | Agen dibuat.                                                                                                                                           |
    | `agent.updated`  | [Versi baru agen](/docs/id/managed-agents/agent-setup#update-an-agent) dipublikasikan. Pembaruan yang tidak membuat versi baru tidak memicu event ini. |
    | `agent.archived` | Agen diarsipkan.                                                                                                                                       |
    | `agent.deleted`  | Agen dihapus secara permanen. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan event itu sendiri sebagai final.                             |
  </Tab>

  <Tab title="Event deployment">
    | Event                 | Pemicu                                                                                                                                                                                                                                                                                                                                                                                          |
    | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `deployment.created`  | [Deployment terjadwal](/docs/id/managed-agents/scheduled-deployments) dibuat.                                                                                                                                                                                                                                                                                                                   |
    | `deployment.updated`  | Properti deployment berubah (misalnya, jadwalnya diperbarui).                                                                                                                                                                                                                                                                                                                                   |
    | `deployment.paused`   | Deployment dijeda, baik berdasarkan permintaan maupun secara otomatis ketika sebuah run terjadwal gagal dengan error yang tidak dapat dipulihkan, seperti subagen yang diarsipkan atau environment yang diarsipkan. Kegagalan yang dapat dipulihkan, termasuk batas laju, tidak menjeda deployment. Lihat [Perilaku kegagalan](/docs/id/managed-agents/scheduled-deployments#failure-behavior). |
    | `deployment.unpaused` | Jeda deployment dicabut, melanjutkan jadwalnya.                                                                                                                                                                                                                                                                                                                                                 |
    | `deployment.archived` | Deployment diarsipkan, baik secara langsung maupun sebagai akibat dari agennya yang diarsipkan atau dihapus.                                                                                                                                                                                                                                                                                    |
    | `deployment.deleted`  | Deployment dihapus secara permanen. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan event itu sendiri sebagai final.                                                                                                                                                                                                                                                                |
  </Tab>

  <Tab title="Event deployment run">
    | Event                      | Pemicu                                                                                                                                                                                                                                                                                                                                                        |
    | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `deployment_run.started`   | Sebuah run terjadwal dimulai. Hanya run terjadwal yang mengeluarkan event `deployment_run`; [run manual](/docs/id/managed-agents/scheduled-deployments#trigger-a-manual-run) tidak.                                                                                                                                                                           |
    | `deployment_run.succeeded` | Sebuah run terjadwal membuat sesinya. Event ini membawa `data.id` yang sama (ID run) dengan event `deployment_run.started` milik run tersebut. Untuk mengikuti pekerjaan sesi, berlangganan ke event sesinya (tab Event sesi), atau ambil [deployment run](/docs/id/managed-agents/scheduled-deployments#deployment-runs) untuk mendapatkan `session_id`-nya. |
    | `deployment_run.failed`    | Sebuah run terjadwal tidak membuat sesi. Event ini membawa `data.id` yang sama dengan event `deployment_run.started` milik run tersebut. Ambil [deployment run](/docs/id/managed-agents/scheduled-deployments#deployment-runs) untuk detail errornya.                                                                                                         |
  </Tab>

  <Tab title="Event environment">
    | Event                  | Pemicu                                                                                                                                                                    |
    | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `environment.created`  | Environment dibuat.                                                                                                                                                       |
    | `environment.updated`  | Environment diperbarui dengan setidaknya satu field yang berubah. Pembaruan tanpa perubahan tidak mengeluarkan apa pun.                                                   |
    | `environment.archived` | Environment diarsipkan. Mengarsipkan ulang environment yang sudah diarsipkan tidak mengeluarkan apa pun.                                                                  |
    | `environment.deleted`  | Environment dihapus, termasuk penghapusan environment yang sudah diarsipkan. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan event itu sendiri sebagai final. |

    [Work item](/docs/id/managed-agents/self-hosted-sandboxes) milik sebuah environment tidak mengeluarkan event webhook.
  </Tab>

  <Tab title="Event memory store">
    | Event                   | Pemicu                                                                                                                                                                                                                                                                                                                                       |
    | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `memory_store.created`  | Memory store dibuat, baik oleh Anda maupun oleh proses yang dioperasikan Anthropic yang mengkloning salah satu store Anda yang sudah ada.                                                                                                                                                                                                    |
    | `memory_store.archived` | Memory store diarsipkan. Mengarsipkan ulang store yang sudah diarsipkan tidak mengeluarkan apa pun.                                                                                                                                                                                                                                          |
    | `memory_store.deleted`  | Memory store dihapus, termasuk penghapusan store yang sudah diarsipkan. Menghapus sebuah store berlanjut secara berantai ke memori dan versi memorinya tanpa mengeluarkan event per memori; satu event `memory_store.deleted` adalah sinyalnya. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan event itu sendiri sebagai final. |

    [Memori](/docs/id/managed-agents/memory) individual dan versi memori tidak mengeluarkan event webhook.
  </Tab>
</Tabs>

## Daftarkan endpoint

Kunjungi **Manage > Webhooks** di [Console](https://platform.claude.com/settings/workspaces/default/webhooks).

Sebuah endpoint webhook terdiri dari:

* **URL:** Harus HTTPS pada port 443 dengan hostname yang dapat di-resolve secara publik.
* **Tipe event:** Daftar nilai `data.type` yang diterima endpoint ini. Sebuah endpoint hanya menerima event yang dilanggannya.
* **Signing secret:** Secret 32-byte berawalan `whsec_` yang dihasilkan saat pembuatan. Secret ini hanya ditampilkan sekali, jadi simpan dengan aman untuk memverifikasi pengiriman webhook.

## Verifikasi tanda tangan

Setiap pengiriman membawa header `webhook-id`, `webhook-timestamp`, dan `webhook-signature`. Gunakan helper `unwrap()` dari SDK untuk memverifikasi tanda tangan dan mem-parsing event dalam satu langkah. Helper ini akan melempar error jika tanda tangan tidak valid atau payload berusia lebih dari lima menit.

Atur `ANTHROPIC_WEBHOOK_SIGNING_KEY` ke secret berawalan `whsec_` yang ditampilkan saat pembuatan endpoint.

<CodeGroup>
  ```python Python
  from flask import Flask, request
  import anthropic

  client = anthropic.Anthropic()  # reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
  app = Flask(__name__)


  @app.route("/webhook", methods=["POST"])
  def webhook():
      try:
          # unwrap() akan memunculkan error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
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

  ```typescript TypeScript
  import express from "express";
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic(); // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
  const app = express();

  // PENTING: gunakan express.raw(), bukan express.json(). Signature dihitung dari byte mentah.
  app.post("/webhook", express.raw({ type: "application/json" }), (req, res) => {
    let event;
    try {
      // unwrap() melempar error jika signature tidak valid atau payload sudah kedaluwarsa
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

  ```csharp C#
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
          // Unwrap() melempar exception jika signature tidak valid atau payload sudah kedaluwarsa
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

  ```go Go
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

  	// Unwrap mengembalikan error jika signature tidak valid atau payload sudah kedaluwarsa
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

  ```java Java
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
              // unwrap() melempar error jika signature tidak valid atau payload sudah kedaluwarsa
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

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Core\Exceptions\WebhookException;

  $client = new Client(); // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env

  $body = file_get_contents('php://input');
  $headers = getallheaders();

  try {
      // unwrap() melempar error jika signature tidak valid atau payload sudah kedaluwarsa
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

  ```ruby Ruby
  require "sinatra"
  require "anthropic"

  client = Anthropic::Client.new # reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env

  post "/webhook" do
    headers = request.env
      .select { |key, _| key.start_with?("HTTP_") }
      .transform_keys { it.delete_prefix("HTTP_").downcase.tr("_", "-") }

    begin
      # unwrap akan memunculkan error jika signature tidak valid atau payload sudah kedaluwarsa
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

## Tangani event

Parse body, lakukan switch pada `data.type`, dan ambil sumber daya berdasarkan ID. Kembalikan `2xx` apa pun untuk mengonfirmasi. Respons lain apa pun dihitung terhadap endpoint: `3xx` menonaktifkannya segera (redirect tidak pernah diikuti), sementara kegagalan lain akan dicoba ulang; lihat [Perilaku pengiriman](#delivery-behavior) untuk aturan percobaan ulang dan penonaktifan otomatis.

Setiap payload event memiliki struktur yang sama, termasuk tipe event, pengidentifikasi, dan timestamp kapan event terjadi.

```json
{
  "type": "event",
  "id": "whe_9d5c1f7e...",
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
  ```python Python
  if event.data.type == "session.status_idled":
      session = client.beta.sessions.retrieve(event.data.id)
      notify_user(session)
  return "", 204
  ```

  ```typescript TypeScript
  if (event.data.type === "session.status_idled") {
    const session = await client.beta.sessions.retrieve(event.data.id);
    notifyUser(session);
  }
  res.sendStatus(204);
  ```

  ```csharp C#
  if (webhookEvent.Data.TryPickSessionStatusIdled(out var idled))
  {
      var session = await client.Beta.Sessions.Retrieve(idled.ID);
      NotifyUser(session);
  }
  return Results.StatusCode(204);
  ```

  ```go Go
  if event.Data.Type == "session.status_idled" {
  	session, err := client.Beta.Sessions.Get(r.Context(), event.Data.ID, anthropic.BetaSessionGetParams{})
  	if err != nil {
  		panic(err)
  	}
  	notifyUser(session)
  }
  w.WriteHeader(http.StatusNoContent)
  ```

  ```java Java
  event.data().sessionStatusIdled().ifPresent(idled -> {
      var session = client.beta().sessions().retrieve(idled.id());
      notifyUser(session);
  });
  exchange.sendResponseHeaders(204, -1);
  ```

  ```php PHP
  if ($event->data->type === 'session.status_idled') {
      $session = $client->beta->sessions->retrieve($event->data->id);
      notifyUser($session);
  }
  http_response_code(204);
  ```

  ```ruby Ruby
  if event.data.type == "session.status_idled"
    session = client.beta.sessions.retrieve(event.data.id)
    notify_user(session)
  end
  status 204
  ```
</CodeGroup>

`event.id` tingkat atas bersifat unik per event, bukan per pengiriman. Jika Anda menerima `event.id` yang sama dua kali, itu adalah percobaan ulang dan Anda dapat mengabaikannya.

## Perilaku pengiriman

* **Duplikat:** Sebuah endpoint dapat menerima event yang sama lebih dari sekali, dan setiap percobaan mengirimkan `event.id` tingkat atas yang sama (nilai yang sama dengan header `webhook-id`). Lakukan deduplikasi berdasarkan nilai tersebut.

* **Cakupan langganan:** Sebuah event hanya dikirimkan ke endpoint yang berlangganan tipenya pada saat event tersebut dikeluarkan. Event yang dikeluarkan saat tidak ada endpoint yang berlangganan tipenya tidak akan pernah dikirimkan, dan berlangganan kemudian tidak akan mengisi ulang event tersebut, jadi berlanggananlah ke suatu tipe event sebelum Anda membutuhkannya.

* **Urutan tidak dijamin.** Event tidak dikirimkan sesuai urutan terjadinya: `session.status_idled` dapat tiba sebelum `session.outcome_evaluation_ended` meskipun hasilnya diproduksi lebih dulu, dan event `.deleted` dapat tiba sebelum event `.archived` untuk sumber daya yang sama. Kendalikan state Anda dari sumber daya yang Anda ambil, bukan dari urutan kedatangan event.

* **Percobaan ulang:** Untuk setiap endpoint dan event, Anthropic melakukan hingga tiga percobaan pengiriman (respons yang memicu penonaktifan otomatis, yang dijelaskan nanti di bagian ini, tidak pernah dicoba ulang) dengan exponential backoff ber-jitter antara 5 dan 120 detik. Setiap percobaan mengirimkan `event.id` yang sama. Setelah percobaan terakhir gagal, event tersebut dibuang: event tidak diantrekan untuk pengiriman nanti dan tidak ada sinyal bahwa event tersebut hilang. Webhook bukanlah log yang tahan lama, jadi jika Anda perlu mengamati setiap transisi, lakukan rekonsiliasi dengan mendaftar atau mengambil sumber daya melalui API.

* **Timestamp:** Header `webhook-timestamp` dicap saat percobaan pengiriman ditandatangani dan dibuat ulang pada setiap percobaan ulang, sehingga percobaan ulang tidak ditolak oleh pemeriksaan kesegaran SDK. Ini adalah jam untuk percobaan pengiriman, bukan untuk event: gunakan `created_at` dari payload event untuk mengetahui kapan event terjadi.

* **Penonaktifan otomatis:** Sebuah endpoint secara otomatis diatur ke `disabled` dengan `disabled_reason` yang dapat dibaca mesin dalam tiga kasus:

  * Endpoint mengembalikan respons `3xx`. Redirect tidak pernah diikuti; ini menonaktifkan endpoint segera, pada percobaan pertama, dengan alasan `auto-disabled: endpoint URL returned a redirect (3xx)`. Jika endpoint Anda berpindah, perbarui URL di Console dan aktifkan kembali endpoint tersebut.
  * URL endpoint ter-resolve ke alamat IP non-publik saat Anthropic terhubung. Ini menonaktifkan endpoint segera, dengan alasan `auto-disabled: endpoint URL resolved to an invalid address`.
  * Pengiriman ke endpoint gagal terus-menerus selama periode yang berkelanjutan, dengan alasan `auto-disabled after sustained delivery failures`. Pemicunya adalah berapa lama endpoint telah gagal tanpa gangguan, bukan jumlah pengiriman. Satu `2xx` mengatur ulang jendela tersebut, sehingga satu event yang tidak stabil tidak dapat menonaktifkan endpoint.

  Ketiganya dapat dibalikkan: aktifkan kembali endpoint di Console setelah Anda menyelesaikan masalahnya. Event yang dikeluarkan saat endpoint dinonaktifkan tidak diputar ulang.
