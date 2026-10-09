---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations
fetched_at: 2026-10-09T02:29:51.005508Z
sha256: 9c51b63ff2b1697e5bb88ea42b52acaeaf343a7ae2d52803cf9a349d3a13a12a
---

---
title: Memantau dan memecahkan masalah worker self-hosted
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations
description: Baca kedalaman antrean, hentikan sesi dan worker tanpa kehilangan pekerjaan, dan perbaiki kegagalan umum sandbox self-hosted.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Panggilan pemantauan di halaman ini dijalankan dari alat pemantauan atau operasional Anda, diautentikasi dengan kunci API Claude Anda. Helper worker menangani loop klaim dan keep-alive, sehingga Anda tidak memanggil endpoint tersebut secara langsung.

<Warning>
  Endpoint ini menerima kunci API organisasi Anda atau environment key. Panggil endpoint ini dari luar host worker dengan kunci API organisasi Anda. Menetapkan `ANTHROPIC_API_KEY` pada host worker akan mengekspos kredensial berlingkup organisasi ke panggilan alat agen.
</Warning>

## Membaca kedalaman antrean

`GET /v1/environments/{environment_id}/work/stats` (curl; python, typescript, ruby: `client.beta.environments.work.stats()`; go, csharp: `client.Beta.Environments.Work.Stats()`; java: `client.beta().environments().work().stats()`; php: `$client->beta->environments->work->stats()`; cli: `ant beta:environments:work stats`) mengembalikan status antrean untuk sebuah environment:

| Field              | Arti                                                                                                                                                                                                     | Gunakan untuk                                                                                                                     |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `depth`            | Item yang menunggu untuk diklaim.                                                                                                                                                                        | Menskalakan armada worker Anda atau memberi peringatan saat terjadi backlog.                                                      |
| `pending`          | Item yang telah diklaim oleh worker tetapi belum di-acknowledge. Helper worker melakukan acknowledge pada setiap item sebelum memprosesnya, sehingga nilai ini tetap mendekati nol dalam operasi normal. | Mendeteksi worker yang macet antara mengklaim dan melakukan acknowledge: beri peringatan pada nilai bukan nol yang bertahan lama. |
| `oldest_queued_at` | Timestamp item tertua yang masih ada di antrean, baik yang menunggu untuk diklaim maupun yang sudah diklaim tetapi belum di-acknowledge. `null` jika tidak ada.                                          | Melihat berapa lama item tertua telah menunggu.                                                                                   |
| `workers_polling`  | Worker yang telah melakukan polling dalam 30 detik terakhir.                                                                                                                                             | Memberi peringatan terkait liveness.                                                                                              |

<CodeGroup>
  ```bash cURL
  curl -sS "https://api.anthropic.com/v1/environments/$ANTHROPIC_ENVIRONMENT_ID/work/stats" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:environments:work stats --environment-id "$ANTHROPIC_ENVIRONMENT_ID"
  ```

  ```python Python
  import os

  import anthropic

  client = anthropic.Anthropic()

  stats = client.beta.environments.work.stats(os.environ["ANTHROPIC_ENVIRONMENT_ID"])
  print(f"depth={stats.depth} pending={stats.pending}")
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const stats = await client.beta.environments.work.stats(process.env.ANTHROPIC_ENVIRONMENT_ID!);

  console.log(`depth=${stats.depth} pending=${stats.pending}`);
  ```

  ```csharp C#
  using Anthropic;

  var client = new AnthropicClient();

  var environmentId = Environment.GetEnvironmentVariable("ANTHROPIC_ENVIRONMENT_ID")!;

  var stats = await client.Beta.Environments.Work.Stats(environmentId);

  Console.WriteLine($"depth={stats.Depth} pending={stats.Pending}");
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	client := anthropic.NewClient()
  	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

  	stats, err := client.Beta.Environments.Work.Stats(
  		context.Background(),
  		environmentID,
  		anthropic.BetaEnvironmentWorkStatsParams{},
  	)
  	if err != nil {
  		panic(err)
  	}

  	fmt.Printf("depth=%d pending=%d\n", stats.Depth, stats.Pending)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.beta.environments.work.BetaSelfHostedWorkQueueStats;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BetaSelfHostedWorkQueueStats stats = client.beta()
          .environments()
          .work()
          .stats(System.getenv("ANTHROPIC_ENVIRONMENT_ID"));

      IO.println("depth=" + stats.depth() + " pending=" + stats.pending());
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Client;

  $client = new Client();

  $stats = $client->beta->environments->work->stats(getenv('ANTHROPIC_ENVIRONMENT_ID'));

  printf("depth=%d pending=%d\n", $stats->depth, $stats->pending);
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  stats = client.beta.environments.work.stats(ENV.fetch("ANTHROPIC_ENVIRONMENT_ID"))

  puts "depth=#{stats.depth} pending=#{stats.pending}"
  ```
</CodeGroup>

```text wrap
{
  "type": "work_queue_stats",
  "depth": 0,
  "pending": 0,
  "oldest_queued_at": null,
  "workers_polling": 0
}
```

## Menghentikan sesi dengan baik

Gunakan `POST /v1/environments/{environment_id}/work/{work_id}/stop` (curl; python, typescript, ruby: `client.beta.environments.work.stop()`; go, csharp: `client.Beta.Environments.Work.Stop()`; java: `client.beta().environments().work().stop()`; php: `$client->beta->environments->work->stop()`; cli: `ant beta:environments:work stop`) untuk meminta worker yang menangani sesi tertentu agar mematikannya.

Secara default, work item berpindah ke `stopping`. Worker menyadarinya pada heartbeat lease berikutnya, membatalkan panggilan alat sesi yang sedang berjalan, dan mengonfirmasi penghentian. Work item kemudian menjadi `stopped`.

Berikan `force: true` (python: `force=True`; cli: `--force`) untuk menandai work item sebagai `stopped` secara langsung alih-alih menunggu konfirmasi dari worker.

Karena panggilan ini dijalankan dari alat operasional Anda, bukan dari host worker, `ANTHROPIC_WORK_ID` tidak ditetapkan secara otomatis. Tetapkan ke ID work item target sebelum menjalankan contoh berikut. Untuk menemukan ID work item, ambil daftar work item environment melalui [endpoint Environments Work](https://platform.claude.com/docs/id/api/beta/environments/work).

<CodeGroup>
  ```bash cURL
  curl -sS "https://api.anthropic.com/v1/environments/$ANTHROPIC_ENVIRONMENT_ID/work/$ANTHROPIC_WORK_ID/stop" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{}'
  ```

  ```bash CLI
  ant beta:environments:work stop \
    --environment-id "$ANTHROPIC_ENVIRONMENT_ID" \
    --work-id "$ANTHROPIC_WORK_ID"
  ```

  ```python Python
  import os

  import anthropic

  client = anthropic.Anthropic()

  work = client.beta.environments.work.stop(
      os.environ["ANTHROPIC_WORK_ID"],
      environment_id=os.environ["ANTHROPIC_ENVIRONMENT_ID"],
  )
  print(work.state)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const work = await client.beta.environments.work.stop(process.env.ANTHROPIC_WORK_ID!, {
    environment_id: process.env.ANTHROPIC_ENVIRONMENT_ID!
  });

  console.log(work.state);
  ```

  ```csharp C#
  using Anthropic;

  var client = new AnthropicClient();

  var work = await client.Beta.Environments.Work.Stop(
      Environment.GetEnvironmentVariable("ANTHROPIC_WORK_ID")!,
      new()
      {
          EnvironmentID = Environment.GetEnvironmentVariable("ANTHROPIC_ENVIRONMENT_ID")!
      }
  );

  Console.WriteLine(work.State);
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	client := anthropic.NewClient()

  	work, err := client.Beta.Environments.Work.Stop(
  		context.Background(),
  		os.Getenv("ANTHROPIC_WORK_ID"),
  		anthropic.BetaEnvironmentWorkStopParams{
  			EnvironmentID: os.Getenv("ANTHROPIC_ENVIRONMENT_ID"),
  		},
  	)
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(work.State)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.beta.environments.work.BetaSelfHostedWork;
  import com.anthropic.models.beta.environments.work.BetaSelfHostedWorkStopRequest;
  import com.anthropic.models.beta.environments.work.WorkStopParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BetaSelfHostedWork work = client.beta().environments().work().stop(
          WorkStopParams.builder()
              .environmentId(System.getenv("ANTHROPIC_ENVIRONMENT_ID"))
              .workId(System.getenv("ANTHROPIC_WORK_ID"))
              .betaSelfHostedWorkStopRequest(BetaSelfHostedWorkStopRequest.builder().build())
              .build()
      );

      IO.println(work.state());
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Client;

  $client = new Client();

  $work = $client->beta->environments->work->stop(
      getenv('ANTHROPIC_WORK_ID'),
      environmentID: getenv('ANTHROPIC_ENVIRONMENT_ID'),
  );

  echo $work->state . "\n";
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  work = client.beta.environments.work.stop(
    ENV.fetch("ANTHROPIC_WORK_ID"),
    environment_id: ENV.fetch("ANTHROPIC_ENVIRONMENT_ID")
  )

  puts work.state
  ```
</CodeGroup>

## Menghentikan worker dengan baik

Worker yang dibatalkan saat sebuah sesi berjalan akan menghentikan pekerjaan yang sedang berlangsung sebelum keluar. Jika sesi memiliki [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory) yang terlampir, worker melewati sinkronisasi akhir tetapi tetap mengunggah file yang berubah dan menghapus direktori store.

Proses yang di-kill tidak menjalankan teardown. Untuk menghentikan worker dengan bersih:

1. **Pastikan SIGTERM dan SIGINT membatalkan worker.** Caranya bergantung pada worker:

   | Worker                                      | Yang harus dilakukan                                                                                                                                           |
   | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | CLI `ant`                                   | Tidak ada. CLI menangani kedua sinyal itu sendiri: CLI membatalkan panggilan alat yang sedang berjalan, mengirimkan hasil error-nya, dan melepaskan work item. |
   | Worker SDK yang merupakan prosesnya sendiri | `EnvironmentWorker` tidak memasang signal handler. Batalkan worker dari signal handler, seperti yang dilakukan contoh worker mandiri.                          |
   | Worker SDK di dalam server webhook          | Batalkan worker dari shutdown hook milik server itu sendiri, seperti yang dilakukan contoh webhook. Worker tidak boleh mengambil alih sinyal server.           |

2. **Hentikan worker dengan SIGTERM, dan beri waktu setidaknya 30 detik sebelum hard kill apa pun.** Unggahan akhir dapat memakan waktu selama itu. Docker mengirim SIGKILL 10 detik setelah sinyal stop secara default. Naikkan batas tersebut dengan `--stop-timeout` pada `docker run`, atau dengan termination grace period dari orchestrator Anda.

Jika worker di-kill sebelum teardown-nya berjalan, setiap suntingan memori yang belum tersinkronisasi akan hilang. Pada host yang berumur panjang, hapus juga direktori store sisa di bawah `/mnt/memory/` sebelum sesi berikutnya yang melampirkan store tersebut. Sandbox yang melayani satu sesi lalu dibuang tidak memerlukan pembersihan.

## Pemecahan masalah

### Worker tidak terhubung

Jika `workers_polling` tetap 0, worker tidak menjangkau antrean. Pastikan bahwa `ANTHROPIC_ENVIRONMENT_KEY` dan `ANTHROPIC_ENVIRONMENT_ID` telah ditetapkan pada host worker.

### Sesi tetap dalam antrean

Tidak ada worker yang mengklaim pekerjaan. Sesi yang berada dalam antrean akan menunggu alih-alih gagal. Periksa `workers_polling` dan `depth` di [Membaca kedalaman antrean](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#read-queue-depth).

### Memory store gagal di-mount

Worker mencatat kegagalan mount dan sinkronisasi latar belakang di log alih-alih melaporkannya ke sesi. Hanya penolakan read-only yang mencapai agen, sebagai error alat (lihat [Store read-only dan konflik](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#read-only-stores-and-conflicts)).

Jika worker tidak dapat me-mount memory store saat mengklaim sesi, worker akan menggagalkan work item. Sesi tidak memancarkan event error dan tetap idle.

| Gejala                                                                                                                           | Penyebab                                                                                                                                                                         | Perbaikan                                                                                                                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Log worker berisi `the work item carried no sessions token` (di Go, error `ErrSessionMemoryNoToken`) dan work item gagal.        | `secret` per sesi dari work item tidak sampai ke worker. Entah kode Anda tidak meneruskannya, atau memory store pada sandbox self-hosted tidak diaktifkan untuk organisasi Anda. | [Meneruskan secret work item](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#forward-the-work-items-secret). Jika worker melakukan polling dan menjalankan sesi dalam satu proses dan masih mencatat ini, hubungi dukungan.                  |
| Log worker berisi `something already exists at the memory store's path`.                                                         | Direktori sisa dari sesi sebelumnya, biasanya sesi yang worker-nya di-kill sebelum teardown-nya berjalan.                                                                        | Hapus direktori sisa yang disebutkan oleh baris log. Suntingan di dalamnya yang belum tersinkronisasi akan hilang.                                                                                                                                                             |
| Log worker berisi `cannot create the memory store's folder` dan `the worker host must make this mount path writable`.            | Pengguna yang menjalankan worker tidak dapat membuat direktori di bawah `/mnt/memory`.                                                                                           | Buat `/mnt/memory` dan `chown` ke pengguna tersebut. Lihat [Menyiapkan host](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#prepare-the-host).                                                                                                |
| Sesi berada dalam status `idle` dengan stop reason `requires_action` dan tanpa event error tak lama setelah worker mengklaimnya. | Worker menggagalkan work item karena tidak dapat me-mount memory store, karena salah satu alasan sebelumnya.                                                                     | Perbaiki penyebabnya di host, lalu kirim event [`user.interrupt`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#interrupt-the-agent). Pekerjaan sesi dimasukkan kembali ke antrean, dan worker berikutnya yang mengklaimnya akan mencoba mount lagi. |

### Panggilan alat kustom tidak pernah kembali

Jika sesi berada dalam keadaan dijeda dengan stop reason `requires_action`, tidak ada worker atau klien yang melayani alat tersebut. Lihat [Melayani alat kustom](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools#serve-a-custom-tool).

### Panggilan alat MCP yang dibungkus macet

Tanpa timeout pada klien MCP, panggilan yang macet ke [server MCP yang dibungkus](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools#wrap-an-mcp-server-as-custom-tools) baru menjadi hasil alat error ketika sebuah backstop terpicu:

| SDK        | Backstop                                                           | Terpicu setelah            |
| ---------- | ------------------------------------------------------------------ | -------------------------- |
| Python     | Batas panggilan alat milik worker itu sendiri                      | Sekitar dua setengah menit |
| TypeScript | Timeout permintaan default dari MCP SDK                            | Sekitar satu menit         |
| Go         | Worker membatalkan panggilan alat yang melampaui batas default-nya | 120 detik                  |
