---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/webhooks
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: d216c34913f100238bb2bdbe234280301baf1eb53d645e6d19ce3d934a112ecd
---

---
title: Berlangganan webhook
url: https://platform.claude.com/docs/id/managed-agents/webhooks
description: Dapatkan notifikasi saat peristiwa penting terjadi tanpa perlu polling.
---

Sesi adalah interaksi yang berjalan lama. Meskipun sebagian besar interaksi real-time terjadi melalui [aliran peristiwa SSE](https://platform.claude.com/docs/id/managed-agents/events-and-streaming), webhook memberi tahu Anda tentang perubahan status yang penting.

Peristiwa webhook mengembalikan `type` dan `id` peristiwa, bukan objek lengkapnya. Saat Anda menerima peristiwa webhook, Anda perlu mengambil objek tersebut secara langsung dengan panggilan `GET`. Hal ini menghindari pengiriman data usang saat percobaan ulang dan menjaga setiap pengiriman tetap kecil.

## Jenis peristiwa yang didukung

<Tabs>
  <Tab title="Peristiwa sesi">
    Beberapa peristiwa ini memiliki nama yang berbeda dari peristiwa yang sesuai pada [aliran peristiwa](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) sesi. Misalnya, `session.status_idle` dan `session.status_running` pada aliran sesuai dengan peristiwa webhook `session.status_idled` dan `session.status_run_started`.

    | Peristiwa                          | Pemicu                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
    | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `session.status_run_started`       | Eksekusi agen dimulai. Ini terpicu pada setiap transisi status sesi ke `running`.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
    | `session.status_idled`             | Agen menunggu input, misalnya persetujuan izin alat atau pesan pengguna baru.                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
    | `session.budget_reached`           | Sesi mencapai [anggarannya](https://platform.claude.com/docs/id/managed-agents/budgets) dan dijeda. Terpicu paling banyak satu kali untuk setiap nilai anggaran yang Anda tetapkan; mengubah anggaran akan mengaktifkannya kembali.                                                                                                                                                                                                                                                                                                |
    | `session.status_rescheduled`       | Terjadi kesalahan sementara dan sesi sedang mencoba ulang secara otomatis.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
    | `session.status_terminated`        | Sesi dihentikan, baik karena kesalahan yang tidak dapat dipulihkan maupun karena diarsipkan.                                                                                                                                                                                                                                                                                                                                                                                                                                       |
    | `session.thread_created`           | [Thread multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) baru dibuka: agen tambahan yang dipanggil oleh koordinator mulai bekerja, atau [advisor](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor) sesi sedang dikonsultasikan.                                                                                                                                                                                                     |
    | `session.thread_idled`             | Sebuah agen dalam [interaksi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) sedang menunggu input.                                                                                                                                                                                                                                                                                                                                                                                        |
    | `session.thread_terminated`        | Sebuah [thread multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) dihentikan, baik karena thread tersebut diarsipkan maupun karena telah menghabiskan percobaan ulangnya. Anak yang dibuat oleh koordinator dan telah menyelesaikan pekerjaannya menjadi `idle`, bukan `terminated` (thread advisor dihentikan setelah konsultasinya selesai). Hanya terpicu untuk thread anak; akhir dari thread utama, termasuk pengarsipan seluruh sesi, hanya muncul sebagai `session.status_terminated`. |
    | `session.outcome_evaluation_ended` | [Evaluasi hasil](https://platform.claude.com/docs/id/managed-agents/define-outcomes) untuk satu iterasi selesai.                                                                                                                                                                                                                                                                                                                                                                                                                   |
    | `session.updated`                  | Properti sesi berubah (misalnya, nama atau konfigurasinya diperbarui).                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
    | `session.deleted`                  | Sesi dihapus secara permanen. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan peristiwa itu sendiri sebagai final.                                                                                                                                                                                                                                                                                                                                                                                                     |
  </Tab>

  <Tab title="Peristiwa vault">
    | Peristiwa                         | Pemicu                                                                                                                                                                                                     |
    | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `vault.created`                   | Vault dibuat.                                                                                                                                                                                              |
    | `vault.archived`                  | Vault diarsipkan. Peristiwa `vault_credential.archived` juga dipancarkan untuk setiap kredensial di dalamnya.                                                                                              |
    | `vault.deleted`                   | Vault dihapus. Peristiwa `vault_credential.deleted` juga dipancarkan untuk setiap kredensial di dalamnya. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan peristiwa itu sendiri sebagai final. |
    | `vault_credential.created`        | Kredensial dibuat.                                                                                                                                                                                         |
    | `vault_credential.archived`       | Kredensial diarsipkan, baik secara langsung maupun sebagai akibat dari pengarsipan vault.                                                                                                                  |
    | `vault_credential.deleted`        | Kredensial dihapus, baik secara langsung maupun sebagai akibat dari penghapusan vault. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan peristiwa itu sendiri sebagai final.                    |
    | `vault_credential.refresh_failed` | Kredensial `mcp_oauth` tidak dapat diperbarui (refresh token tidak valid, atau kesalahan yang tidak dapat dipulihkan dari server OAuth).                                                                   |
  </Tab>

  <Tab title="Peristiwa agen">
    Peristiwa ini melacak siklus hidup sumber daya agen di workspace Anda, dan berbeda dari peristiwa agen yang dikirimkan pada aliran peristiwa sesi.

    | Peristiwa        | Pemicu                                                                                                                                                                                |
    | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `agent.created`  | Agen dibuat.                                                                                                                                                                          |
    | `agent.updated`  | [Versi baru agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-an-agent) dipublikasikan. Pembaruan yang tidak membuat versi baru tidak memicu peristiwa ini. |
    | `agent.archived` | Agen diarsipkan.                                                                                                                                                                      |
    | `agent.deleted`  | Agen dihapus secara permanen. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan peristiwa itu sendiri sebagai final.                                                        |
  </Tab>

  <Tab title="Peristiwa deployment">
    | Peristiwa             | Pemicu                                                                                                                                                                                                                                                                                                                                                                                                                |
    | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `deployment.created`  | [Deployment terjadwal](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments) dibuat.                                                                                                                                                                                                                                                                                                              |
    | `deployment.updated`  | Properti deployment berubah (misalnya, jadwalnya diperbarui).                                                                                                                                                                                                                                                                                                                                                         |
    | `deployment.paused`   | Deployment dijeda, baik atas permintaan maupun secara otomatis ketika eksekusi terjadwal gagal dengan kesalahan yang tidak dapat dipulihkan, seperti subagen yang diarsipkan atau environment yang diarsipkan. Kegagalan yang dapat dipulihkan, termasuk batas laju, tidak menjeda deployment. Lihat [Perilaku kegagalan](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments#failure-behavior). |
    | `deployment.unpaused` | Jeda deployment dibatalkan, melanjutkan jadwalnya.                                                                                                                                                                                                                                                                                                                                                                    |
    | `deployment.archived` | Deployment diarsipkan, baik secara langsung maupun karena agennya diarsipkan. Jika agen dihapus, deployment terjadwal akan diarsipkan pada eksekusi terjadwal berikutnya; deployment tanpa jadwal tidak diarsipkan secara otomatis.                                                                                                                                                                                   |
    | `deployment.deleted`  | Deployment dihapus secara permanen. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan peristiwa itu sendiri sebagai final.                                                                                                                                                                                                                                                                                  |
  </Tab>

  <Tab title="Peristiwa eksekusi deployment">
    | Peristiwa                  | Pemicu                                                                                                                                                                                                                                                                                                                                                                                                                           |
    | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `deployment_run.started`   | Eksekusi terjadwal dimulai. Hanya eksekusi terjadwal yang memancarkan peristiwa `deployment_run`; [eksekusi manual](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments#trigger-a-manual-run) tidak.                                                                                                                                                                                                        |
    | `deployment_run.succeeded` | Eksekusi terjadwal berhasil membuat sesinya. Peristiwa ini membawa `data.id` (ID eksekusi) yang sama dengan peristiwa `deployment_run.started` dari eksekusi tersebut. Untuk mengikuti pekerjaan sesi, berlanggananlah ke peristiwa sesinya (tab Peristiwa sesi), atau ambil [eksekusi deployment](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments#deployment-runs) untuk mendapatkan `session_id`-nya. |
    | `deployment_run.failed`    | Eksekusi terjadwal tidak membuat sesi. Peristiwa ini membawa `data.id` yang sama dengan peristiwa `deployment_run.started` dari eksekusi tersebut. Ambil [eksekusi deployment](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments#deployment-runs) untuk detail kesalahannya.                                                                                                                              |
  </Tab>

  <Tab title="Peristiwa environment">
    | Peristiwa              | Pemicu                                                                                                                                                                        |
    | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `environment.created`  | Environment dibuat.                                                                                                                                                           |
    | `environment.updated`  | Environment diperbarui dengan setidaknya satu field yang berubah. Pembaruan tanpa perubahan (no-op) tidak memancarkan apa pun.                                                |
    | `environment.archived` | Environment diarsipkan. Mengarsipkan ulang environment yang sudah diarsipkan tidak memancarkan apa pun.                                                                       |
    | `environment.deleted`  | Environment dihapus, termasuk penghapusan environment yang sudah diarsipkan. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan peristiwa itu sendiri sebagai final. |

    [Work item](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) milik environment tidak memancarkan peristiwa webhook.
  </Tab>

  <Tab title="Peristiwa memory store">
    | Peristiwa               | Pemicu                                                                                                                                                                                                                                                                                                                                 |
    | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `memory_store.created`  | Memory store dibuat, baik oleh Anda maupun oleh proses yang dioperasikan Anthropic yang mengkloning salah satu store Anda yang sudah ada.                                                                                                                                                                                              |
    | `memory_store.archived` | Memory store diarsipkan. Mengarsipkan ulang store yang sudah diarsipkan tidak memancarkan apa pun.                                                                                                                                                                                                                                     |
    | `memory_store.deleted`  | Memory store dihapus, termasuk penghapusan store yang sudah diarsipkan. Menghapus store akan berjenjang ke memori dan versi memorinya tanpa memancarkan peristiwa per memori; satu peristiwa `memory_store.deleted` adalah sinyalnya. Tidak ada objek yang tersisa untuk diambil, jadi perlakukan peristiwa itu sendiri sebagai final. |

    [Memori](https://platform.claude.com/docs/id/managed-agents/memory) individual dan versi memori tidak memancarkan peristiwa webhook.
  </Tab>
</Tabs>

## Mendaftarkan endpoint

Kunjungi **Manage > Webhooks** di [Claude Console](https://platform.claude.com/settings/workspaces/default/webhooks).

Sebuah endpoint webhook terdiri dari:

* **URL:** Harus HTTPS pada port 443 dengan hostname yang dapat di-resolve secara publik.
* **Jenis peristiwa:** Daftar nilai `data.type` yang diterima endpoint ini. Sebuah endpoint hanya menerima peristiwa yang dilangganinya.
* **Signing secret:** Secret 32-byte berawalan `whsec_` yang dihasilkan saat pembuatan. Secret ini hanya ditampilkan sekali, jadi simpan dengan aman untuk memverifikasi pengiriman webhook.

## Memverifikasi tanda tangan

Setiap pengiriman membawa header `webhook-id`, `webhook-timestamp`, dan `webhook-signature`. Gunakan helper `unwrap()` dari SDK untuk memverifikasi tanda tangan dan mem-parse peristiwa dalam satu langkah. Helper ini melempar error jika tanda tangan tidak valid atau payload berusia lebih dari 5 menit.

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
          # unwrap() memunculkan error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
          event = client.beta.webhooks.unwrap(
              request.get_data(as_text=True),
              headers=dict(request.headers),
          )
      except Exception:
          return "invalid signature", 400

      if event.data.type == "session.status_idled":
          print("session idled:", event.data.id)
      # tangani jenis event lainnya

      return "", 200
  ```

  ```typescript TypeScript
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
      // tangani jenis event lainnya
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
          // Unwrap() melempar error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
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
      // tangani jenis event lainnya

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

  	// Unwrap mengembalikan error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
  	event, err := client.Beta.Webhooks.Unwrap(body, r.Header)
  	if err != nil {
  		http.Error(w, "invalid signature", http.StatusBadRequest)
  		return
  	}

  	switch event.Data.Type {
  	case "session.status_idled":
  		fmt.Println("session idled:", event.Data.ID)
  		// tangani jenis event lainnya
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
              // unwrap() melempar error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
              var event = client.beta().webhooks().unwrap(
                  UnwrapWebhookParams.builder()
                      .body(body)
                      .headers(headers.build())
                      .build());

              event.data().sessionStatusIdled().ifPresent(idled ->
                  IO.println("session idled: " + idled.id()));
              // tangani jenis event lainnya

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
      // unwrap() melempar error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
      $event = $client->beta->webhooks->unwrap($body, headers: $headers);
  } catch (WebhookException) {
      http_response_code(400);
      exit('invalid signature');
  }

  match ($event->data->type) {
      'session.status_idled' => print "session idled: {$event->data->id}\n",
      // tangani jenis event lainnya
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
      # unwrap memunculkan error jika tanda tangan tidak valid atau payload sudah kedaluwarsa
      event = client.beta.webhooks.unwrap(request.body.read, headers: headers)
    rescue StandardError
      halt 400, "invalid signature"
    end

    if event.data.type == :"session.status_idled"
      puts "session idled: #{event.data.id}"
    end
    # tangani jenis event lainnya

    status 200
  end
  ```
</CodeGroup>

## Menangani peristiwa

Parse body, lakukan switch pada `data.type`, dan ambil sumber daya berdasarkan ID. Kembalikan `2xx` apa pun untuk mengonfirmasi penerimaan. Respons lain apa pun dihitung sebagai kegagalan endpoint: `3xx` langsung menonaktifkannya (redirect tidak pernah diikuti), sedangkan kegagalan lainnya dicoba ulang; lihat [Perilaku pengiriman](https://platform.claude.com/docs/id/managed-agents/webhooks#delivery-behavior) untuk aturan percobaan ulang dan penonaktifan otomatis.

Setiap payload peristiwa memiliki struktur yang sama, termasuk jenis peristiwa, pengenal, dan timestamp kapan peristiwa tersebut terjadi.

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
  if event.data.type == :"session.status_idled"
    session = client.beta.sessions.retrieve(event.data.id)
    notify_user(session)
  end
  status 204
  ```
</CodeGroup>

`event.id` tingkat atas bersifat unik per peristiwa, bukan per pengiriman. Jika Anda menerima `event.id` yang sama dua kali, itu adalah percobaan ulang dan Anda dapat membuangnya.

## Perilaku pengiriman

* **Duplikat:** Sebuah endpoint dapat menerima peristiwa yang sama lebih dari sekali, dan setiap percobaan mengirimkan `event.id` tingkat atas yang sama (nilai yang sama dengan header `webhook-id`). Lakukan deduplikasi berdasarkan nilai tersebut.

* **Cakupan langganan:** Sebuah peristiwa hanya dikirimkan ke endpoint yang berlangganan jenisnya pada saat peristiwa itu dipancarkan. Peristiwa yang dipancarkan saat tidak ada endpoint yang berlangganan jenisnya tidak akan pernah dikirimkan, dan berlangganan di kemudian hari tidak akan mengisinya kembali, jadi berlanggananlah ke suatu jenis peristiwa sebelum Anda membutuhkannya.

* **Urutan tidak dijamin.** Peristiwa tidak dikirimkan sesuai urutan terjadinya: `session.status_idled` mungkin tiba sebelum `session.outcome_evaluation_ended` meskipun hasilnya diproduksi lebih dulu, dan peristiwa `.deleted` dapat tiba sebelum peristiwa `.archived` untuk sumber daya yang sama. Kendalikan status Anda berdasarkan sumber daya yang Anda ambil, bukan berdasarkan urutan kedatangan peristiwa.

* **Percobaan ulang:** Untuk setiap endpoint dan peristiwa, Anthropic melakukan hingga tiga percobaan pengiriman (respons yang memicu penonaktifan otomatis, yang dijelaskan nanti di bagian ini, tidak pernah dicoba ulang) dengan exponential backoff ber-jitter antara 5 dan 120 detik. Setiap percobaan mengirimkan `event.id` yang sama. Setelah percobaan terakhir gagal, peristiwa tersebut dibuang: tidak diantrekan untuk pengiriman nanti dan tidak ada sinyal bahwa peristiwa itu hilang. Webhook bukanlah log yang tahan lama, jadi jika Anda perlu mengamati setiap transisi, lakukan rekonsiliasi dengan mendaftar atau mengambil sumber daya melalui API.

* **Timestamp:** Header `webhook-timestamp` dicap saat percobaan pengiriman ditandatangani dan dibuat ulang pada setiap percobaan ulang, sehingga percobaan ulang tidak ditolak oleh pemeriksaan kesegaran SDK. Ini adalah jam untuk percobaan pengiriman, bukan untuk peristiwa: gunakan `created_at` pada payload peristiwa untuk mengetahui kapan peristiwa terjadi.

* **Penonaktifan otomatis:** Sebuah endpoint secara otomatis diatur ke `disabled` dengan `disabled_reason` yang dapat dibaca mesin dalam tiga kasus:

  * Endpoint mengembalikan respons `3xx`. Redirect tidak pernah diikuti; ini langsung menonaktifkan endpoint, pada percobaan pertama, dengan alasan `auto-disabled: endpoint URL returned a redirect (3xx)`. Jika endpoint Anda berpindah, perbarui URL di Console dan aktifkan kembali endpoint tersebut.
  * URL endpoint di-resolve ke alamat IP non-publik saat Anthropic terhubung. Ini langsung menonaktifkan endpoint, dengan alasan `auto-disabled: endpoint URL resolved to an invalid address`.
  * Pengiriman ke endpoint gagal terus-menerus selama periode yang berkelanjutan, dengan alasan `auto-disabled after sustained delivery failures`. Pemicunya adalah berapa lama endpoint telah gagal tanpa jeda, bukan jumlah pengiriman. Satu `2xx` saja akan mengatur ulang jendela waktunya, sehingga satu peristiwa yang tidak stabil tidak dapat menonaktifkan endpoint.

  Ketiganya dapat dibalikkan: aktifkan kembali endpoint di Console setelah Anda menyelesaikan masalahnya. Peristiwa yang dipancarkan saat endpoint dinonaktifkan tidak akan diputar ulang.
