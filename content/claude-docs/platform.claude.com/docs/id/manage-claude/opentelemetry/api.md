---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/opentelemetry/api
fetched_at: 2026-10-17T02:19:22.559852Z
sha256: 20501f8fa1d7c70525c96cae145bd77accb0a070fa9b22176170e05e61fb22c6
---

---
title: Menyiapkan OpenTelemetry dengan Claude API
url: https://platform.claude.com/docs/id/manage-claude/opentelemetry/api
description: Tambahkan tujuan di Claude Console untuk mengirim trace OpenTelemetry dari permintaan Messages API dan sesi Managed Agents Anda ke platform observabilitas Anda.
featureMetadata:
  topic:
    title: OpenTelemetry
    url: https://platform.claude.com/docs/en/manage-claude/opentelemetry
  status: beta
  zdr:
    eligibility: eligible
    note: Excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements). Hanya untuk fitur yang memang memenuhi syarat ZDR, seperti Messages API. Claude Managed Agents tidak memenuhi syarat ZDR.
  supportedPlatforms:
    Claude API: beta
    Claude Platform on AWS: beta
  rows:
    - label: Berfungsi dengan
      value: Messages API, Claude Managed Agents
  details:
    - Setelah dikirimkan, data disimpan oleh layanan yang Anda pilih, di luar Anthropic, di bawah kontrol retensi dan akses layanan tersebut.
---

Dengan OpenTelemetry, Claude API dapat memancarkan *Span* (rentang) untuk setiap permintaan model dan setiap penggunaan alat yang dijalankannya. Anda dapat melihat span ini di platform observabilitas Anda tanpa mengubah kode Anda.

API memancarkan span untuk permintaan Messages API dan sesi Managed Agents Anda. Untuk menerimanya, tambahkan *destination* (tujuan) di Claude Console. Tujuan memberi tahu API endpoint OTLP dari platform observabilitas Anda dan cara melakukan autentikasi dengannya.

## Yang Anda butuhkan

* **Peran admin** di organisasi Claude Console, untuk menambahkan dan mengubah tujuan. Dengan peran developer, Anda dapat melihatnya. Jika organisasi Anda berada di Claude Platform on AWS, masuk ke Console melalui AWS Console, seperti yang dijelaskan di [Masuk](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#signing-in).
* **Endpoint OTLP/HTTP** yang menerima encoding protobuf di URL HTTPS pada port 443. Jika Anda menjalankan [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) sendiri, receiver OTLP/HTTP-nya mendengarkan pada port 4318 secara default. Konfigurasikan receiver untuk menerima HTTPS pada port 443, atau tempatkan load balancer atau reverse proxy di depan Collector.
* **Kredensial untuk endpoint**, seperti kunci API.

## 1. Tambahkan tujuan

<Info>
  Saat Anda menambahkan tujuan telemetri, Anthropic akan mengirimkan trace aktivitas Claude Platform di organisasi Anda ke endpoint OTLP/HTTP penyedia pihak ketiga yang Anda tentukan, sesuai dengan ketentuan penyedia dan kontrol akses Anda. Setelah dikirimkan, data disimpan oleh layanan yang Anda pilih, di luar Anthropic, di bawah kontrol retensi dan akses layanan tersebut.
</Info>

1. Di Console, buka [halaman pengaturan OpenTelemetry](https://platform.claude.com/settings/telemetry-destinations) organisasi Anda dan klik **Add destination**.

2. Konfigurasikan tujuan:

   | Kolom                          | Yang dimasukkan                                                                                                                                                                                                                                                                                                                                                                                                                                              |
   | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
   | **Provider**                   | Platform observabilitas Anda, atau **Custom** jika tidak tercantum. Jika Anda memilih platform yang tercantum, Console akan meminta detailnya, seperti kunci API, sebagai pengganti **OTLP endpoint URL**, **Request headers**, dan **OTLP traces endpoint URL**.                                                                                                                                                                                            |
   | **Name**                       | Opsional. Misalnya, "Platform observabilitas Acme."                                                                                                                                                                                                                                                                                                                                                                                                          |
   | **OTLP endpoint URL**          | URL HTTPS dasar dari endpoint OTLP/HTTP platform observabilitas Anda, dengan hostname, bukan alamat IP. URL ini dapat memiliki prefiks path, misalnya `https://gateway.example.com/otlp`. Jangan tambahkan `/v1/traces`, karena API akan menambahkannya. Jika Anda menetapkan **OTLP traces endpoint URL**, API akan menggunakan URL tersebut sebagai gantinya.                                                                                              |
   | **Request headers**            | Header yang dikirim API bersama setiap permintaan, misalnya header kunci API dari platform observabilitas Anda. Letakkan kredensial hanya di nilai header. Setelah Anda menyimpan, Console tidak menampilkan nilai tersebut lagi.                                                                                                                                                                                                                            |
   | **Content mode**               | **Metadata only** atau **Full content**. Lihat [perbedaan mode konten](https://platform.claude.com/docs/id/manage-claude/opentelemetry#choose-a-content-mode).                                                                                                                                                                                                                                                                                               |
   | **Workspaces**                 | Workspace yang span-nya diterima oleh tujuan: **All**, **Selected**, atau **All except**. Lihat [Pilih workspace untuk tujuan](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#choose-workspaces-for-a-destination).                                                                                                                                                                                                                     |
   | **OTLP traces endpoint URL**   | Opsional, di bawah **Advanced settings**. URL lengkap endpoint trace platform observabilitas Anda, misalnya `https://gateway.example.com/custom/traces`. Tetapkan ini ketika platform tersebut menerima trace di URL selain OTLP endpoint URL ditambah `/v1/traces`. URL ini harus memiliki host yang sama dengan OTLP endpoint URL.                                                                                                                         |
   | **Maximum content size in MB** | Opsional, di bawah **Advanced settings** jika mode konten adalah **Full content**. Jumlah konten maksimum yang dikirim API di setiap span. Console mengisinya berdasarkan **Provider** yang Anda pilih. Ubah nilainya agar sesuai dengan yang diterima platform observabilitas Anda. Biarkan kosong untuk mengirim konten sebanyak yang diizinkan API. Lihat [Batas konten](https://platform.claude.com/docs/id/manage-claude/opentelemetry#content-limits). |

3. Klik **Add destination** untuk menyimpan.

4. Klik **Test** di menu **More actions** milik tujuan tersebut. Anda akan melihat pesan bahwa span pengujian telah terkirim ke kolektor Anda, atau bagaimana pengiriman gagal (lihat [Kesalahan pengiriman](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#delivery-errors)).

5. Periksa apakah span `anthropic.test` telah sampai di platform observabilitas Anda.

### Admin API dan CLI

Anda juga dapat menambahkan tujuan melalui [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) sebagai pengganti Console. Masuk ke CLI sebagai admin, atau gunakan [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys) di `ANTHROPIC_API_KEY`. Di Claude Platform on AWS, kirim permintaan ke `https://aws-external-anthropic.{region}.api.aws` sebagai gantinya, ditandatangani dengan kredensial AWS Anda seperti di [Membuat permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#making-requests). Di sana, [kebijakan IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions) Anda menentukan siapa yang dapat mengelola tujuan. Sebuah permintaan hanya dapat menyertakan workspace dari akun AWS Anda di Region tersebut.

<CodeGroup>
  ```bash CLI
  # Masuk sekali sebagai admin, yang akan membuka browser. Biarkan ANTHROPIC_API_KEY tidak diatur, karena variabel ini menimpa profil.
  ant auth login --profile admin --scope "org:admin"
  ant --profile admin beta:organization:telemetry-destinations create \
    --endpoint-url https://gateway.example.com/otlp \
    --headers '{authorization: "Bearer YOUR_OBSERVABILITY_API_KEY"}' \
    --traces.content-mode metadata_only \
    --workspaces.type all
  ```

  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/telemetry_destinations" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: telemetry-destinations-2026-08-11" \
    -H "content-type: application/json" \
    -d '{
      "endpoint_url": "https://gateway.example.com/otlp",
      "headers": {"authorization": "Bearer YOUR_OBSERVABILITY_API_KEY"},
      "traces": {"content_mode": "metadata_only"},
      "workspaces": {"type": "all"}
    }'
  ```

  ```python Python
  client = anthropic.Anthropic()

  destination = client.beta.organization.telemetry_destinations.create(
      endpoint_url="https://gateway.example.com/otlp",
      headers={"authorization": "Bearer YOUR_OBSERVABILITY_API_KEY"},
      traces={"content_mode": "metadata_only"},
      workspaces={"type": "all"},
  )

  print(destination.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const destination = await client.beta.organization.telemetryDestinations.create({
    endpoint_url: "https://gateway.example.com/otlp",
    headers: { authorization: "Bearer YOUR_OBSERVABILITY_API_KEY" },
    traces: { content_mode: "metadata_only" },
    workspaces: { type: "all" }
  });

  console.log(destination.id);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.TelemetryDestinations;

  AnthropicClient client = new();

  var destination = await client.Beta.Organization.TelemetryDestinations.Create(
      new()
      {
          EndpointUrl = "https://gateway.example.com/otlp",
          Headers = new Dictionary<string, string>
          {
              ["authorization"] = "Bearer YOUR_OBSERVABILITY_API_KEY",
          },
          Traces = new() { ContentMode = BetaTelemetryDestinationContentMode.MetadataOnly },
          Workspaces = new BetaTelemetryDestinationWorkspacesAllParams(),
      }
  );

  Console.WriteLine(destination.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  destination, err := client.Beta.Organization.TelemetryDestinations.New(
  	context.Background(),
  	anthropic.BetaOrganizationTelemetryDestinationNewParams{
  		EndpointURL: "https://gateway.example.com/otlp",
  		Headers: map[string]string{
  			"authorization": "Bearer YOUR_OBSERVABILITY_API_KEY",
  		},
  		Traces: anthropic.BetaTelemetryDestinationTracesParams{
  			ContentMode: anthropic.BetaTelemetryDestinationContentModeMetadataOnly,
  		},
  		Workspaces: anthropic.BetaTelemetryDestinationWorkspacesParamsUnion{
  			OfAll: &anthropic.BetaTelemetryDestinationWorkspacesAllParams{},
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(destination.ID)
  ```

  ```java Java
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.beta.organization.telemetrydestinations.BetaTelemetryDestinationContentMode;
  import com.anthropic.models.beta.organization.telemetrydestinations.BetaTelemetryDestinationTracesParams;
  import com.anthropic.models.beta.organization.telemetrydestinations.BetaTelemetryDestinationWorkspacesAllParams;
  import com.anthropic.models.beta.organization.telemetrydestinations.TelemetryDestinationCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = TelemetryDestinationCreateParams.builder()
          .endpointUrl("https://gateway.example.com/otlp")
          .headers(TelemetryDestinationCreateParams.Headers.builder()
              .putAdditionalProperty("authorization", JsonValue.from("Bearer YOUR_OBSERVABILITY_API_KEY"))
              .build())
          .traces(BetaTelemetryDestinationTracesParams.builder()
              .contentMode(BetaTelemetryDestinationContentMode.METADATA_ONLY)
              .build())
          .workspaces(BetaTelemetryDestinationWorkspacesAllParams.builder().build())
          .build();
      var destination = client.beta().organization().telemetryDestinations().create(params);

      IO.println(destination.id());
  }
  ```

  ```php PHP
  $client = new Client();

  $destination = $client->beta->organization->telemetryDestinations->create(
      endpointURL: 'https://gateway.example.com/otlp',
      headers: ['authorization' => 'Bearer YOUR_OBSERVABILITY_API_KEY'],
      traces: ['contentMode' => 'metadata_only'],
      workspaces: ['type' => 'all'],
  );

  echo "{$destination->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  destination = client.beta.organization.telemetry_destinations.create(
    endpoint_url: "https://gateway.example.com/otlp",
    headers: {authorization: "Bearer YOUR_OBSERVABILITY_API_KEY"},
    traces: {content_mode: :metadata_only},
    workspaces: {type: :all}
  )

  puts destination.id
  ```
</CodeGroup>

Permintaan create menerima pengaturan Console kecuali **Provider**, jadi masukkan sendiri URL endpoint dan header platform observabilitas Anda. Atur `traces.max_content_bytes` (csharp, go: `Traces.MaxContentBytes`; java, php: `traces.maxContentBytes`), dalam byte, agar sesuai dengan yang diterima platform observabilitas Anda (lihat [Batas konten](https://platform.claude.com/docs/id/manage-claude/opentelemetry#content-limits)). Untuk mencantumkan, mengubah, atau menghapus tujuan, atau untuk menambahkan atau menghapus satu workspace, gunakan metode lain dari [API tujuan telemetri](https://platform.claude.com/docs/id/api/beta/organization/telemetry_destinations).

## 2. Pilih workspace untuk tujuan

Tujuan menerima span dari workspace yang dicakupnya. Pilih workspace tersebut saat Anda menambahkan tujuan. Untuk **Workspaces**, pilih salah satu dari berikut ini:

* **All:** Setiap workspace di organisasi, termasuk [Default Workspace](https://platform.claude.com/docs/id/manage-claude/workspaces#how-workspaces-work) dan workspace yang dibuat kemudian.
* **Selected:** Hanya workspace yang Anda pilih.
* **All except:** Seperti **All**, tetapi tanpa workspace yang Anda pilih.

Untuk **Selected** atau **All except**, pilih workspace di kotak pencarian yang muncul di bawah opsi. Untuk mengubah workspace suatu tujuan nanti, buka menu **More actions** miliknya di [halaman pengaturan OpenTelemetry](https://platform.claude.com/settings/telemetry-destinations) saat filter **Workspace** menampilkan **All**. Klik **Edit**, lalu pilih opsi **Workspaces** lain atau ubah workspace di kotak pencarian.

Jika Anda memiliki peran developer di organisasi dan peran Workspace Admin di sebuah workspace, Anda dapat menambahkan workspace tersebut ke tujuan **Selected** atau menghapusnya dari tujuan itu. Atur filter **Workspace** ke workspace tersebut, lalu buka menu **More actions** tujuan. Di Claude Platform on AWS, Console tidak memiliki peran Workspace Admin. Di sana, [kebijakan IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions) Anda yang menentukan siapa yang dapat menambahkan workspace ke tujuan atau menghapusnya dari tujuan itu.

API mengirimkan span ke setiap tujuan aktif yang mencakup [workspace tempat permintaan atau sesi berjalan](https://platform.claude.com/docs/id/manage-claude/workspaces#api-keys-and-resource-scoping).

## 3. Periksa bahwa span tiba

1. Di Console, pilih workspace yang dicakup oleh tujuan tersebut dan kirim permintaan Messages API di [playground](https://platform.claude.com/playground). Anda juga dapat mengirim permintaan Messages API dari aplikasi Anda atau memulai sesi Managed Agents di workspace tersebut. Untuk memulai sesi, Anda dapat mengikuti langkah-langkah di [Memulai dengan Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/quickstart).
2. Di Console, pada [halaman pengaturan OpenTelemetry](https://platform.claude.com/settings/telemetry-destinations), periksa bahwa kolom **Delivery** dari tujuan menampilkan **Healthy**. Ini dapat memakan waktu sekitar satu menit.
3. Di platform observabilitas Anda, filter berdasarkan `service.name` = `claude-platform` untuk menemukan span dari permintaan tersebut.

Jika kolom menampilkan **Failing**, arahkan penunjuk ke atasnya untuk melihat kesalahan terakhir. Untuk menemukan kemungkinan penyebabnya, lihat [Kesalahan pengiriman](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#delivery-errors).

## 4. Hubungkan span API ke trace Anda sendiri

Secara default, span API dari permintaan Messages API atau sesi Managed Agents berada di trace-nya sendiri. Hubungkan span tersebut ke trace aplikasi Anda, sehingga span tersebut bersarang di bawah span Anda sendiri.

API membaca konteks trace dari setiap permintaan dari [header `traceparent`](https://www.w3.org/TR/trace-context/) W3C. Jika flag sampled di header tersebut nonaktif, API tidak memancarkan span dari permintaan tersebut maupun span di bawahnya.

<Tabs>
  <Tab title="Dengan Claude SDK">
    Untuk menghubungkan span API, [siapkan tracing SDK](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk) di aplikasi Anda dan panggil SDK dari dalam salah satu span Anda sendiri. Span Anda kemudian berisi span SDK, yang berisi span API. Kirim semua span ini ke platform observabilitas yang sama, sehingga platform tersebut dapat menampilkannya sebagai satu trace. Lihat contoh trace dari [permintaan Messages API](https://platform.claude.com/docs/id/manage-claude/opentelemetry#a-messages-api-request) dan [sesi Managed Agents](https://platform.claude.com/docs/id/manage-claude/opentelemetry#a-managed-agents-session).

    Contoh berikut mengirimkan pesan pengguna ke sebuah sesi di dalam span Anda sendiri:

    <CodeGroup exclude="shell">
      ```python Python
      from opentelemetry import trace

      tracer = trace.get_tracer("my-service")

      with tracer.start_as_current_span("summarize_issues"):
          client.beta.sessions.events.send(
              session.id,
              events=[
                  {
                      "type": "user.message",
                      "content": [{"type": "text", "text": "Summarize the open issues"}],
                  },
              ],
          )
      ```

      ```typescript TypeScript
      import { trace } from "@opentelemetry/api";

      const tracer = trace.getTracer("my-service");

      await tracer.startActiveSpan("summarize_issues", async (span) => {
        try {
          await client.beta.sessions.events.send(session.id, {
            events: [
              {
                type: "user.message",
                content: [{ type: "text", text: "Summarize the open issues" }]
              }
            ]
          });
        } finally {
          span.end();
        }
      });
      ```

      ```csharp C#
      using System.Diagnostics;

      // Tambahkan sumber ini ke tracer provider Anda, di samping com.anthropic.sdk.csharp.
      var source = new ActivitySource("MyService");

      using (source.StartActivity("summarize_issues"))
      {
          // parameters berisi event user.message.
          await client.Beta.Sessions.Events.Send(session.ID, parameters);
      }
      ```

      ```go Go
      // Teruskan context yang berisi span Anda.
      ctx, span := otel.Tracer("my-service").Start(ctx, "summarize_issues")
      defer span.End()

      // params berisi event user.message.
      _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, params)
      ```

      ```java Java
      Tracer tracer = GlobalOpenTelemetry.getTracer("my-service");
      Span span = tracer.spanBuilder("summarize_issues").startSpan();

      try (Scope scope = span.makeCurrent()) {
          // params berisi event user.message.
          client.beta().sessions().events().send(session.id(), params);
      } finally {
          span.end();
      }
      ```

      ```php PHP
      use OpenTelemetry\API\Globals;

      $tracer = Globals::tracerProvider()->getTracer('my-service');
      $span = $tracer->spanBuilder('summarize_issues')->startSpan();
      $scope = $span->activate();

      try {
          $client->beta->sessions->events->send(
              $session->id,
              events: [
                  [
                      'type' => 'user.message',
                      'content' => [
                          ['type' => 'text', 'text' => 'Summarize the open issues'],
                      ],
                  ],
              ],
          );
      } finally {
          $scope->detach();
          $span->end();
      }
      ```

      ```ruby Ruby
      tracer = OpenTelemetry.tracer_provider.tracer("my-service")

      tracer.in_span("summarize_issues") do
        client.beta.sessions.events.send_(
          session.id,
          events: [
            {
              type: "user.message",
              content: [{type: "text", text: "Summarize the open issues"}]
            }
          ]
        )
      end
      ```
    </CodeGroup>

    SDK menulis header `traceparent` dengan propagator aplikasi Anda, dan flag sampled di dalamnya mengikuti sampler Anda. Jika aplikasi Anda menggunakan propagator selain W3C trace context, seperti B3, tambahkan juga propagator W3C trace context.
  </Tab>

  <Tab title="Dengan klien lain">
    Salin konteks trace dari span saat ini ke header permintaan, misalnya saat Anda membuat sesi Managed Agents atau mengirim pesan pengguna:

    <CodeGroup exclude="shell:CLI">
      ```bash cURL
      # TRACEPARENT adalah traceparent dari span aktif di layanan Anda sendiri,
      # misalnya 00-<trace-id>-<span-id>-01.
      curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID/events" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -H "traceparent: $TRACEPARENT" \
        -d '{
          "events": [
            {
              "type": "user.message",
              "content": [{"type": "text", "text": "Summarize the open issues"}]
            }
          ]
        }'
      ```

      ```python Python
      import os
      import httpx2
      from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

      headers = {
          "x-api-key": os.environ["ANTHROPIC_API_KEY"],
          "anthropic-version": "2023-06-01",
          "anthropic-beta": "managed-agents-2026-04-01",
          "content-type": "application/json",
      }
      # Salin konteks trace dari span aktif ke dalam header permintaan.
      TraceContextTextMapPropagator().inject(headers)

      httpx2.post(
          f"https://api.anthropic.com/v1/sessions/{os.environ['SESSION_ID']}/events",
          headers=headers,
          json={
              "events": [
                  {
                      "type": "user.message",
                      "content": [{"type": "text", "text": "Summarize the open issues"}],
                  },
              ],
          },
      )
      ```

      ```typescript TypeScript
      import { context, defaultTextMapSetter } from "@opentelemetry/api";
      import { W3CTraceContextPropagator } from "@opentelemetry/core";

      const headers: Record<string, string> = {
        "x-api-key": process.env.ANTHROPIC_API_KEY!,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "managed-agents-2026-04-01",
        "content-type": "application/json"
      };
      // Salin konteks trace dari span aktif ke dalam header permintaan.
      new W3CTraceContextPropagator().inject(context.active(), headers, defaultTextMapSetter);

      await fetch(`https://api.anthropic.com/v1/sessions/${process.env.SESSION_ID}/events`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          events: [
            {
              type: "user.message",
              content: [{ type: "text", text: "Summarize the open issues" }]
            }
          ]
        })
      });
      ```

      ```csharp C#
      using System.Diagnostics;
      using System.Net.Http.Json;
      using OpenTelemetry;
      using OpenTelemetry.Context.Propagation;

      using var httpClient = new HttpClient();
      using var request = new HttpRequestMessage(
          HttpMethod.Post,
          $"https://api.anthropic.com/v1/sessions/{Environment.GetEnvironmentVariable("SESSION_ID")}/events")
      {
          // JsonContent mengatur header content-type.
          Content = JsonContent.Create(new
          {
              events = new[]
              {
                  new
                  {
                      type = "user.message",
                      content = new[] { new { type = "text", text = "Summarize the open issues" } },
                  },
              },
          }),
      };
      request.Headers.Add("x-api-key", Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY"));
      request.Headers.Add("anthropic-version", "2023-06-01");
      request.Headers.Add("anthropic-beta", "managed-agents-2026-04-01");

      // Salin konteks trace dari span aktif ke dalam header permintaan.
      new TraceContextPropagator().Inject(
          new PropagationContext(Activity.Current?.Context ?? default, Baggage.Current),
          request,
          (carrier, key, value) => carrier.Headers.Add(key, value));

      await httpClient.SendAsync(request);
      ```

      ```go Go
      import (
      	"context"
      	"net/http"
      	"os"
      	"strings"

      	"go.opentelemetry.io/otel/propagation"
      )

      func sendMessage(ctx context.Context) error {
      	body := strings.NewReader(`{
      		"events": [
      			{
      				"type": "user.message",
      				"content": [{"type": "text", "text": "Summarize the open issues"}]
      			}
      		]
      	}`)
      	req, err := http.NewRequestWithContext(ctx, http.MethodPost,
      		"https://api.anthropic.com/v1/sessions/"+os.Getenv("SESSION_ID")+"/events", body)
      	if err != nil {
      		return err
      	}
      	req.Header.Set("x-api-key", os.Getenv("ANTHROPIC_API_KEY"))
      	req.Header.Set("anthropic-version", "2023-06-01")
      	req.Header.Set("anthropic-beta", "managed-agents-2026-04-01")
      	req.Header.Set("content-type", "application/json")

      	// Salin konteks trace dari span aktif ke dalam header permintaan.
      	propagation.TraceContext{}.Inject(ctx, propagation.HeaderCarrier(req.Header))

      	resp, err := http.DefaultClient.Do(req)
      	if err != nil {
      		return err
      	}
      	return resp.Body.Close()
      }
      ```

      ```java Java
      import io.opentelemetry.api.trace.propagation.W3CTraceContextPropagator;
      import io.opentelemetry.context.Context;
      import java.net.URI;
      import java.net.http.HttpClient;
      import java.net.http.HttpRequest;
      import java.net.http.HttpResponse;

      void main() throws Exception {
          var request = HttpRequest.newBuilder(URI.create(
                  "https://api.anthropic.com/v1/sessions/" + System.getenv("SESSION_ID") + "/events"))
              .header("x-api-key", System.getenv("ANTHROPIC_API_KEY"))
              .header("anthropic-version", "2023-06-01")
              .header("anthropic-beta", "managed-agents-2026-04-01")
              .header("content-type", "application/json")
              .POST(HttpRequest.BodyPublishers.ofString("""
                  {
                    "events": [
                      {
                        "type": "user.message",
                        "content": [{"type": "text", "text": "Summarize the open issues"}]
                      }
                    ]
                  }
                  """));

          // Salin konteks trace dari span aktif ke dalam header permintaan.
          W3CTraceContextPropagator.getInstance()
              .inject(Context.current(), request, HttpRequest.Builder::header);

          HttpClient.newHttpClient().send(request.build(), HttpResponse.BodyHandlers.ofString());
      }
      ```

      ```php PHP
      use OpenTelemetry\API\Trace\Propagation\TraceContextPropagator;

      $headers = [
          'x-api-key' => getenv('ANTHROPIC_API_KEY'),
          'anthropic-version' => '2023-06-01',
          'anthropic-beta' => 'managed-agents-2026-04-01',
          'content-type' => 'application/json',
      ];
      // Salin konteks trace dari span aktif ke dalam header permintaan.
      TraceContextPropagator::getInstance()->inject($headers);

      $ch = curl_init('https://api.anthropic.com/v1/sessions/' . getenv('SESSION_ID') . '/events');
      curl_setopt_array($ch, [
          CURLOPT_RETURNTRANSFER => true,
          CURLOPT_HTTPHEADER => array_map(
              static fn ($name, $value) => "$name: $value",
              array_keys($headers),
              $headers,
          ),
          CURLOPT_POSTFIELDS => json_encode([
              'events' => [
                  [
                      'type' => 'user.message',
                      'content' => [
                          ['type' => 'text', 'text' => 'Summarize the open issues'],
                      ],
                  ],
              ],
          ]),
      ]);
      curl_exec($ch);
      ```

      ```ruby Ruby
      require "json"
      require "net/http"
      require "opentelemetry"

      headers = {
        "x-api-key" => ENV.fetch("ANTHROPIC_API_KEY"),
        "anthropic-version" => "2023-06-01",
        "anthropic-beta" => "managed-agents-2026-04-01",
        "content-type" => "application/json"
      }
      # Salin konteks trace dari span aktif ke dalam header permintaan.
      OpenTelemetry::Trace::Propagation::TraceContext.text_map_propagator.inject(headers)

      Net::HTTP.post(
        URI("https://api.anthropic.com/v1/sessions/#{ENV.fetch("SESSION_ID")}/events"),
        {
          events: [
            {
              type: "user.message",
              content: [{type: "text", text: "Summarize the open issues"}]
            }
          ]
        }.to_json,
        headers
      )
      ```
    </CodeGroup>
  </Tab>
</Tabs>

Messages API juga meneruskan trace ke server MCP Anda saat Anda menghubungkannya dengan [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector), sehingga server tersebut dapat menempatkan span-nya sendiri di bawah span API. Setiap permintaan dan notifikasi yang dikirim API ke server MCP Anda memiliki `traceparent` W3C di `params._meta`. Dalam permintaan `tools/call`, `traceparent` tersebut merujuk span [`anthropic.mcp_tool_use`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use) dari penggunaan alat tersebut. Dalam pesan lainnya, `traceparent` tersebut merujuk span [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create). Untuk permintaan yang tidak di-trace oleh API, seperti permintaan yang header `traceparent`-nya memiliki flag sampled tidak aktif, API tidak mengirimkan `traceparent`.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Siapkan tracing SDK" icon="code-brackets" href="https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk">
    Dapatkan observabilitas ke dalam klien Anda.
  </Card>

  <Card title="Lihat contoh trace" icon="sitemap" href="https://platform.claude.com/docs/id/manage-claude/opentelemetry#example-traces-and-how-to-read-them">
    Ikuti permintaan dari klien Anda hingga ke Claude API.
  </Card>
</CardGroup>

## Pengiriman dan kesehatan

Aturan berikut berlaku untuk span yang dikirim API ke tujuan Anda.

* **Setidaknya sekali:** Sebuah tujuan dapat menerima span yang sama lebih dari sekali. Untuk menghapus duplikat, gunakan trace ID dan span ID.
* **Upaya terbaik:** Sebuah span dapat hilang sebelum dikirimkan. API tidak dapat mengirim ulang span yang hilang.
* **Kompresi:** API mengompresi permintaan pertama dari setiap pengiriman dengan gzip dan mengatur header `Content-Encoding: gzip`. Jika endpoint Anda menjawab permintaan tersebut dengan respons `400` atau `415`, API segera mengirim ulang span yang sama tanpa kompresi.
* **Percobaan ulang:** API mencoba pengiriman lagi nanti, dalam jumlah terbatas, setelah timeout, kegagalan koneksi, TLS, atau DNS, atau respons `408`, `429`, atau `5xx`. API tidak mencoba ulang kegagalan lainnya.
* **Timeout:** Untuk setiap permintaan, endpoint Anda harus menyelesaikan handshake TLS dalam 5 detik dan mengirim header respons dalam 5 detik. Setiap pengiriman mengalami timeout setelah total 10 detik, termasuk pengiriman ulang tanpa kompresi.
* **User agent:** Setiap permintaan memiliki header `User-Agent: Claude-Platform`.

Kolom **Delivery** menampilkan status setiap tujuan. Status dapat terlambat hingga satu menit.

| Status pengiriman | Arti                                                                                         |
| ----------------- | -------------------------------------------------------------------------------------------- |
| **Healthy**       | Pengiriman terakhir berhasil.                                                                |
| **Failing**       | Pengiriman terakhir gagal. Untuk melihat kesalahannya, arahkan penunjuk ke atas **Failing**. |
| **No data**       | API belum mencoba pengiriman.                                                                |
| **Disabled**      | Tujuan tidak menerima span. Untuk melihat alasannya, arahkan penunjuk ke atas **Disabled**.  |

API menonaktifkan tujuan ketika:

* Endpoint mengirimkan redirect `3xx`.
* Nama host endpoint di-resolve ke alamat IP yang tidak publik.
* Semua pengiriman gagal selama 24 jam.

API tidak mengirim span ke tujuan yang dinonaktifkan. Untuk melanjutkan ekspor, perbaiki penyebabnya. Kemudian, dengan filter **Workspace** di [halaman pengaturan OpenTelemetry](https://platform.claude.com/settings/telemetry-destinations) menampilkan **All**, klik **Enable** di menu **More actions** milik tujuan tersebut. Ekspor dimulai lagi dalam sekitar satu menit.

Untuk mengubah sebuah tujuan, buka menu **More actions** miliknya saat filter **Workspace** menampilkan **All**. Kemudian klik **Edit**, **Disable**, **Enable**, atau **Delete**. Jika Anda mengubah host dari **OTLP endpoint URL**, masukkan kembali nilai header. Jika tujuan memiliki **OTLP traces endpoint URL**, berikan host baru yang sama, atau kosongkan.

## Batas

| Batas                                                       | Nilai          |
| ----------------------------------------------------------- | -------------- |
| Tujuan untuk setiap organisasi, termasuk yang dinonaktifkan | 10             |
| Workspace yang Anda pilih untuk sebuah tujuan               | 1.000          |
| Header permintaan untuk setiap tujuan                       | 20             |
| Panjang nama header                                         | 128 byte       |
| Panjang nilai header                                        | 4.096 byte     |
| Panjang semua nama dan nilai header secara keseluruhan      | 16.384 byte    |
| Panjang URL endpoint                                        | 2.048 karakter |

## Pemecahan masalah

| Masalah                                                                           | Yang perlu diperiksa                                                                                                                                                                                                                                                                                                          |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tidak ada span API                                                                | Workspace memerlukan tujuan aktif yang mencakupnya. Lihat [Pilih workspace untuk tujuan](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#choose-workspaces-for-a-destination). Setelah tujuan mulai mencakup workspace, span dari workspace tersebut dapat memerlukan waktu hingga satu menit untuk tiba. |
| Kolom **Delivery** menampilkan **Failing**                                        | Arahkan pointer ke atasnya untuk melihat error terakhir. Untuk menemukan kemungkinan penyebabnya, lihat [Error pengiriman](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#delivery-errors).                                                                                                              |
| Kolom **Delivery** menampilkan **Disabled**                                       | Arahkan pointer ke atasnya untuk melihat alasannya. Untuk alasan-alasannya, lihat [kapan API menonaktifkan tujuan](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#delivery-and-health).                                                                                                                  |
| Span tidak memiliki prompt atau respons, tetapi tujuan diatur ke **Full content** | Organisasi Anda mungkin memiliki pembatasan penanganan data HIPAA, FERPA, atau K-12 dengan Anthropic. Lihat [Mode konten](https://platform.claude.com/docs/id/manage-claude/opentelemetry#choose-a-content-mode).                                                                                                             |

### Error pengiriman

Ketika pengiriman gagal, kolom **Delivery** menampilkan **Failing**. Arahkan pointer ke atasnya untuk melihat error-nya, lalu temukan kemungkinan penyebabnya:

| Error                                                | Kemungkinan penyebab                                                                                                                                          |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HTTP error (status 401) atau HTTP error (status 403) | Header autentikasi yang salah                                                                                                                                 |
| HTTP error (status 404)                              | Path yang salah di **OTLP endpoint URL** atau **OTLP traces endpoint URL**                                                                                    |
| DNS resolution failure                               | Hostname endpoint tidak dapat di-resolve                                                                                                                      |
| TLS failure                                          | Masalah TLS, misalnya dengan sertifikat endpoint                                                                                                              |
| Timeout                                              | Endpoint tidak merespons tepat waktu. Lihat [batas waktu pengiriman](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#delivery-and-health) |
| Connection failure                                   | API tidak dapat terhubung ke endpoint                                                                                                                         |
