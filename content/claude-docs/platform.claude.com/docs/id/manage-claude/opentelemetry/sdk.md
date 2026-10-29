---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk
fetched_at: 2026-10-29T02:15:48.406163Z
sha256: f50d1973fcfc8a83c45550022d5ff0a087ec74e662f0a95cd95712be81cbc4fa
---

---
title: Menyiapkan OpenTelemetry dengan Claude SDK
url: https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk
description: Lacak permintaan dan penggunaan alat Claude SDK di Python, TypeScript, C#, Go, Java, PHP, atau Ruby, lalu kirim span ke platform observabilitas Anda.
featureMetadata:
  topic:
    title: OpenTelemetry
    url: https://platform.claude.com/docs/en/manage-claude/opentelemetry
  status: beta
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: beta
    Claude Platform on AWS: beta
    Amazon Bedrock: beta
    Amazon Bedrock (InvokeModel): beta
    Claude Models on Google Cloud (Google managed): beta
    Microsoft Foundry: beta
---

Dengan OpenTelemetry, Claude SDK dapat memancarkan “span” (rentang) untuk setiap permintaan yang dikirimnya dan setiap penggunaan alat yang dijalankan oleh [tool runner](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner). Anda dapat melihat span ini di platform observabilitas Anda, bersarang di dalam trace Anda sendiri.

SDK memancarkan span di aplikasi Anda. “Exporter” (pengekspor) OpenTelemetry aplikasi Anda mengirimkannya ke platform observabilitas Anda.

<Note>
  Selama masa beta, opsi SDK dan skema span dapat berubah dengan cara yang merusak kode, kueri, atau dasbor Anda. Misalnya, versi baru SDK dapat mengganti nama span, atribut, opsi, atau variabel lingkungan. Sematkan versi SDK di dependensi Anda untuk memilih kapan Anda mengadopsi perubahan tersebut.
</Note>

## 1. Instal SDK

Instal atau tingkatkan ke versi terbaru Claude SDK:

<Tabs>
  <Tab title="Python">
    ```bash
    pip install --upgrade anthropic
    ```

    Jika aplikasi Anda belum menggunakan OpenTelemetry SDK, instal bersama console exporter, yang Anda gunakan pada langkah berikutnya untuk mencetak span:

    ```bash
    pip install opentelemetry-sdk
    ```
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/sdk@latest
    ```

    Jika aplikasi Anda belum menggunakan OpenTelemetry SDK, instal bersama console exporter, yang Anda gunakan pada langkah berikutnya untuk mencetak span:

    ```bash
    npm install @opentelemetry/sdk-trace-node
    ```
  </Tab>

  <Tab title="C#">
    ```bash
    dotnet add package Anthropic
    ```

    Jika aplikasi Anda belum menggunakan OpenTelemetry SDK, instal bersama console exporter, yang Anda gunakan pada langkah berikutnya untuk mencetak span:

    ```bash
    dotnet add package OpenTelemetry.Exporter.Console
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    go get github.com/anthropics/anthropic-sdk-go@latest
    ```

    Jika aplikasi Anda belum menggunakan OpenTelemetry SDK, instal bersama console exporter, yang Anda gunakan pada langkah berikutnya untuk mencetak span:

    ```bash
    go get go.opentelemetry.io/otel/sdk go.opentelemetry.io/otel/exporters/stdout/stdouttrace
    ```
  </Tab>

  <Tab title="Java">
    Tambahkan Claude SDK ke dependensi Anda, atau perbarui setidaknya ke versi berikut jika file build Anda sudah mendeklarasikannya:

    <CodeGroup exclude="shell, python, typescript, csharp, go, php, ruby">
      ```kotlin Gradle
      implementation("com.anthropic:anthropic-java:3.3.0")
      ```

      ```xml Maven
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java</artifactId>
          <version>3.3.0</version>
      </dependency>
      ```
    </CodeGroup>

    Jika aplikasi Anda belum menggunakan SDK OpenTelemetry, instal SDK tersebut beserta exporter konsol, yang Anda gunakan pada langkah berikutnya untuk mencetak span. Tambahkan `io.opentelemetry:opentelemetry-sdk` dan `io.opentelemetry:opentelemetry-exporter-logging` ke build Anda, keduanya pada versi terbaru di [Maven Central](https://central.sonatype.com/artifact/io.opentelemetry/opentelemetry-sdk).
  </Tab>

  <Tab title="PHP">
    ```bash
    composer require "anthropic-ai/sdk" "guzzlehttp/guzzle:^7"
    ```

    Jika aplikasi Anda belum menggunakan OpenTelemetry SDK, instal bersama console exporter, yang Anda gunakan pada langkah berikutnya untuk mencetak span:

    ```bash
    composer require open-telemetry/sdk
    ```
  </Tab>

  <Tab title="Ruby">
    Jika `Gemfile` Anda belum mencantumkan `anthropic`, tambahkan gem tersebut:

    ```bash
    bundle add anthropic
    ```

    Jika `Gemfile` Anda sudah mencantumkan `anthropic`, perbarui gem tersebut:

    ```bash
    bundle update anthropic
    ```

    Jika aplikasi Anda belum menggunakan OpenTelemetry SDK, instal bersama console exporter, yang Anda gunakan pada langkah berikutnya untuk mencetak span:

    ```bash
    bundle add opentelemetry-sdk
    ```
  </Tab>
</Tabs>

## 2. Daftarkan tracer provider

*Tracer provider* (penyedia tracer) adalah objek OpenTelemetry yang membuat span dan meneruskannya ke exporter Anda. SDK menggunakan tracer provider yang didaftarkan oleh aplikasi Anda, sehingga panggilan SDK Anda tetap sama. Daftarkan tracer provider sebelum panggilan pertama yang ingin Anda telusuri.

Contoh berikut mendaftarkan tracer provider yang mencetak setiap span ke konsol lalu melakukan satu panggilan. Gunakan contoh ini untuk melihat span sebelum Anda menghubungkan platform observabilitas:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic import Anthropic
  from opentelemetry import trace
  from opentelemetry.sdk.trace import TracerProvider
  from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

  # Daftarkan tracer provider yang mencetak setiap span ke konsol.
  provider = TracerProvider()
  provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
  trace.set_tracer_provider(provider)

  client = Anthropic()

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(message.content)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import {
    ConsoleSpanExporter,
    NodeTracerProvider,
    SimpleSpanProcessor
  } from "@opentelemetry/sdk-trace-node";

  // Daftarkan tracer provider yang mencetak setiap span ke konsol.
  const provider = new NodeTracerProvider({
    spanProcessors: [new SimpleSpanProcessor(new ConsoleSpanExporter())]
  });
  // register() juga memasang context manager, yang memungkinkan span SDK bersarang di bawah span Anda.
  provider.register();

  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  console.log(message.content);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;
  using OpenTelemetry;
  using OpenTelemetry.Trace;

  // Daftarkan tracer provider yang mencetak setiap span ke konsol.
  using var tracerProvider = Sdk.CreateTracerProviderBuilder()
      .AddSource("com.anthropic.sdk.csharp*")
      .AddConsoleExporter()
      .Build();

  AnthropicClient client = new();

  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new UserMessageParam { Content = "Hello, Claude" }],
  });
  Console.WriteLine(message);
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"go.opentelemetry.io/otel"
  	"go.opentelemetry.io/otel/exporters/stdout/stdouttrace"
  	"go.opentelemetry.io/otel/propagation"
  	sdktrace "go.opentelemetry.io/otel/sdk/trace"
  )

  func main() {
  	ctx := context.Background()

  	// Daftarkan tracer provider yang mencetak setiap span ke konsol.
  	exporter, err := stdouttrace.New(stdouttrace.WithPrettyPrint())
  	if err != nil {
  		panic(err)
  	}
  	provider := sdktrace.NewTracerProvider(sdktrace.WithSyncer(exporter))
  	defer provider.Shutdown(ctx)
  	otel.SetTracerProvider(provider)
  	// OpenTelemetry untuk Go tidak mendaftarkan propagator secara default, jadi
  	// daftarkan propagator W3C trace context.
  	otel.SetTextMapPropagator(propagation.TraceContext{})

  	client := anthropic.NewClient()

  	message, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(message.Content)
  }
  ```

  ```java Java
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import io.opentelemetry.api.trace.propagation.W3CTraceContextPropagator;
  import io.opentelemetry.context.propagation.ContextPropagators;
  import io.opentelemetry.exporter.logging.LoggingSpanExporter;
  import io.opentelemetry.sdk.OpenTelemetrySdk;
  import io.opentelemetry.sdk.trace.SdkTracerProvider;
  import io.opentelemetry.sdk.trace.export.SimpleSpanProcessor;

  void main() {
      // Daftarkan tracer provider yang menulis setiap span ke log.
      var tracerProvider = SdkTracerProvider.builder()
          .addSpanProcessor(SimpleSpanProcessor.create(LoggingSpanExporter.create()))
          .build();
      OpenTelemetrySdk.builder()
          .setTracerProvider(tracerProvider)
          // OpenTelemetry untuk Java tidak mendaftarkan propagator saat Anda membangunnya
          // di dalam kode, jadi daftarkan propagator W3C trace context.
          .setPropagators(ContextPropagators.create(W3CTraceContextPropagator.getInstance()))
          .buildAndRegisterGlobal();

      var client = AnthropicOkHttpClient.fromEnv();

      var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .build());
      IO.println(message.content());

      tracerProvider.close();
  }
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Messages\Model;
  use OpenTelemetry\API\Trace\Propagation\TraceContextPropagator;
  use OpenTelemetry\SDK\Sdk;
  use OpenTelemetry\SDK\Trace\SpanExporter\ConsoleSpanExporterFactory;
  use OpenTelemetry\SDK\Trace\SpanProcessor\SimpleSpanProcessor;
  use OpenTelemetry\SDK\Trace\TracerProvider;

  // Daftarkan tracer provider yang mencetak setiap span ke konsol.
  $tracerProvider = new TracerProvider(
      new SimpleSpanProcessor((new ConsoleSpanExporterFactory())->create()),
  );
  Sdk::builder()
      ->setTracerProvider($tracerProvider)
      // OpenTelemetry untuk PHP tidak mendaftarkan propagator saat Anda membangunnya
      // di dalam kode, jadi daftarkan propagator W3C trace context.
      ->setPropagator(TraceContextPropagator::getInstance())
      ->buildAndRegisterGlobal();

  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: Model::CLAUDE_OPUS_5_5,
  );
  echo $message;
  ```

  ```ruby Ruby
  require "anthropic"
  require "opentelemetry/sdk"

  # Daftarkan tracer provider yang mencetak setiap span ke konsol.
  OpenTelemetry::SDK.configure do |config|
    config.add_span_processor(
      OpenTelemetry::SDK::Trace::Export::SimpleSpanProcessor.new(
        OpenTelemetry::SDK::Trace::Export::ConsoleSpanExporter.new
      )
    )
  end

  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}]
  )
  puts(message.content)
  ```
</CodeGroup>

Konsol menampilkan satu span [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create).

## 3. Kirim span ke platform observabilitas Anda

Ganti console exporter dengan OTLP exporter yang mengarah ke platform observabilitas Anda. Untuk penyiapan dalam bahasa Anda, lihat dokumentasi OpenTelemetry tentang [exporter Python](https://opentelemetry.io/docs/languages/python/exporters/), [exporter TypeScript](https://opentelemetry.io/docs/languages/js/exporters/), [exporter .NET](https://opentelemetry.io/docs/languages/dotnet/exporters/), [exporter Go](https://opentelemetry.io/docs/languages/go/exporters/), [konfigurasi Java SDK](https://opentelemetry.io/docs/languages/java/configuration/), [exporter PHP](https://opentelemetry.io/docs/languages/php/exporters/), atau [exporter Ruby](https://opentelemetry.io/docs/languages/ruby/exporters/).

## 4. Konfigurasikan SDK

Gunakan opsi berikut untuk menentukan apa yang masuk ke span Anda dan ke mana span tersebut dikirim. Anda dapat mengatur opsi di kode Anda atau, jika tersedia, dengan variabel lingkungan di bawah namanya.

<Note>
  Jika Anda meneruskan `open_telemetry` (typescript, java, php: `openTelemetry`; csharp: `OpenTelemetry`; go: `option.With…()`) ke klien, opsi tersebut menimpa variabel lingkungan opsi itu secara keseluruhan, termasuk kunci bersarang. Setiap kunci bersarang yang Anda hilangkan menggunakan nilai default-nya dari tabel, meskipun variabel lingkungannya diatur.
</Note>

| Opsi                                                                                                                                                                                                                           | Gunakan untuk                                                                                                                                                                                                                       | Default                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `traces.content_mode` (typescript, java, php: `traces.contentMode`; csharp: `Traces.ContentMode`; go: `option.WithOpenTelemetryTracesContentMode()`)<br />`ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE=content`               | Menyertakan prompt dan respons dalam span. Lihat [Mode konten](https://platform.claude.com/docs/id/manage-claude/opentelemetry#choose-a-content-mode).                                                                              | `metadata_only`                                                                                                                                                  |
| `traces.max_content_bytes` (typescript, java, php: `traces.maxContentBytes`; csharp: `Traces.MaxContentBytes`; go: `option.WithOpenTelemetryTracesMaxContentBytes()`)<br />`ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES` | Mengubah batas konten setiap span. Lihat [Batas konten](https://platform.claude.com/docs/id/manage-claude/opentelemetry#content-limits).                                                                                            | 0,75 MB                                                                                                                                                          |
| `conversation_id` (typescript, java, php: `conversationId`; csharp: `ConversationId`; go: `option.WithOpenTelemetryConversationID()`)                                                                                          | Menautkan beberapa panggilan menjadi satu percakapan. SDK menulis ID tersebut ke `gen_ai.conversation.id`. ID diekspor di kedua mode konten, jadi jangan masukkan data pribadi atau rahasia ke dalamnya.                            | Tidak ada                                                                                                                                                        |
| `tracer_provider` (typescript, java, php: `tracerProvider`; csharp: `AddSource("com.anthropic.sdk.csharp*")`; go: `option.WithTracerProvider()`)                                                                               | Memilih tracer provider yang menerima span dari SDK.                                                                                                                                                                                | Tracer provider yang Anda siapkan di [Daftarkan tracer provider](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#register-a-tracer-provider) |
| `propagation` (go: `option.WithOpenTelemetryPropagation()`)<br />`ANTHROPIC_OPEN_TELEMETRY_PROPAGATION=false`                                                                                                                  | Berhenti mengirim header konteks trace dan baggage bersama permintaan, misalnya ketika instrumentasi klien HTTP Anda sudah mengirimkannya. SDK tetap memancarkan span. Tersedia di SDK Python, TypeScript, Go, Java, Ruby, dan PHP. | Aktif                                                                                                                                                            |
| `open_telemetry` (typescript, java, php: `openTelemetry`; csharp: `OpenTelemetry`; go: `option.WithoutOpenTelemetry()`)<br />`ANTHROPIC_OPEN_TELEMETRY=false`                                                                  | Menonaktifkan span untuk satu klien, misalnya ketika pustaka lain sudah melacak SDK.                                                                                                                                                | Aktif                                                                                                                                                            |

Contoh berikut menunjukkan cara menggunakan setiap opsi:

<CodeGroup exclude="shell">
  ```python Python
  # Gunakan tracer provider tertentu dan rekam konten.
  # Mengatur open_telemetry akan menimpa semua variabel lingkungan ANTHROPIC_OPEN_TELEMETRY*.
  client = Anthropic(
      open_telemetry={"tracer_provider": provider, "traces": {"content_mode": "content"}}
  )

  # Nonaktifkan span untuk satu klien.
  quiet_client = Anthropic(open_telemetry=False)

  # Atur ID percakapan dengan with_options(), yang mengembalikan salinan klien.
  # with_options() mengganti seluruh opsi, jadi mulailah dari client.open_telemetry.
  message = client.with_options(
      open_telemetry={**client.open_telemetry, "conversation_id": "conv_42"}
  ).messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  ```

  ```typescript TypeScript
  // Gunakan tracer provider tertentu dan rekam konten.
  // Mengatur openTelemetry akan menimpa semua variabel lingkungan ANTHROPIC_OPEN_TELEMETRY*.
  const client = new Anthropic({
    openTelemetry: { tracerProvider: provider, traces: { contentMode: "content" } }
  });

  // Nonaktifkan span untuk satu klien.
  const quietClient = new Anthropic({ openTelemetry: false });

  // Atur ID percakapan di opsi permintaan untuk satu panggilan.
  const message = await client.messages.create(
    {
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    },
    { openTelemetry: { conversationId: "conv_42" } }
  );
  ```

  ```csharp C#
  // Gunakan tracer provider tertentu: tambahkan source SDK ke dalamnya.
  using var tracerProvider = Sdk.CreateTracerProviderBuilder()
      .AddSource("com.anthropic.sdk.csharp*")
      .AddConsoleExporter()
      .Build();

  // Rekam konten.
  // Mengatur OpenTelemetry akan menimpa semua variabel lingkungan ANTHROPIC_OPEN_TELEMETRY*.
  AnthropicClient client = new()
  {
      OpenTelemetry = new() { Traces = new() { ContentMode = OpenTelemetryContentMode.Content } },
  };

  // Nonaktifkan span untuk satu klien.
  AnthropicClient quietClient = new() { OpenTelemetry = false };

  // Tetapkan ID percakapan untuk panggilan dalam satu percakapan.
  var conversation = client.WithOptions(options => options with
  {
      OpenTelemetryRequest = new() { ConversationId = "conv_42" },
  });
  var message = await conversation.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new UserMessageParam { Content = "Hello, Claude" }],
  });
  ```

  ```go Go
  // Gunakan tracer provider tertentu dan rekam kontennya.
  client := anthropic.NewClient(
  	option.WithTracerProvider(provider),
  	option.WithOpenTelemetryTracesContentMode(option.OpenTelemetryContentModeContent),
  )

  // Nonaktifkan span untuk satu klien.
  quietClient := anthropic.NewClient(option.WithoutOpenTelemetry())

  // Tetapkan ID percakapan di opsi permintaan pada satu panggilan.
  message, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  }, option.WithOpenTelemetryConversationID("conv_42"))
  ```

  ```java Java
  // Klien hanya membaca variabel lingkungan saat Anda membangunnya dengan fromEnv().
  // Properti sistem anthropic.openTelemetry, anthropic.openTelemetryTracesContentMode,
  // dan anthropic.openTelemetryTracesMaxContentBytes lebih diutamakan daripada variabel
  // lingkungan.

  // Gunakan tracer provider tertentu dan rekam konten. Mulai dari
  // OpenTelemetryOptions.fromEnv() untuk mempertahankan opsi yang dibaca fromEnv().
  var envOptions = OpenTelemetryOptions.fromEnv();
  var client = AnthropicOkHttpClient.builder()
      .fromEnv()
      .openTelemetry(envOptions.toBuilder()
          .tracerProvider(tracerProvider)
          .traces(envOptions.traces().toBuilder()
              .contentMode(OpenTelemetryContentMode.CONTENT)
              .build())
          .build())
      .build();

  // Nonaktifkan span untuk satu klien.
  var quietClient = AnthropicOkHttpClient.builder().fromEnv().openTelemetry(false).build();

  // Tetapkan ID percakapan di opsi permintaan untuk satu panggilan.
  var params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024)
      .addUserMessage("Hello, Claude")
      .build();
  var message = client.messages().create(params, RequestOptions.builder()
      .openTelemetry(OpenTelemetryRequestOptions.builder().conversationId("conv_42").build())
      .build());
  ```

  ```php PHP
  // Gunakan tracer provider tertentu dan rekam konten.
  // Mengatur openTelemetry akan menimpa semua variabel lingkungan ANTHROPIC_OPEN_TELEMETRY*.
  $client = new Client(
      openTelemetry: ['tracerProvider' => $tracerProvider, 'traces' => ['contentMode' => 'content']],
  );

  // Nonaktifkan span untuk satu klien.
  $quietClient = new Client(openTelemetry: false);

  // Atur ID percakapan di opsi permintaan untuk satu panggilan.
  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: Model::CLAUDE_OPUS_5_5,
      requestOptions: ['openTelemetry' => ['conversationId' => 'conv_42']],
  );
  ```

  ```ruby Ruby
  # Gunakan tracer provider tertentu dan rekam konten.
  # Mengatur open_telemetry akan menimpa semua variabel lingkungan ANTHROPIC_OPEN_TELEMETRY*.
  client = Anthropic::Client.new(
    open_telemetry: {
      tracer_provider: OpenTelemetry.tracer_provider,
      traces: {content_mode: :content}
    }
  )

  # Nonaktifkan span untuk satu klien.
  quiet_client = Anthropic::Client.new(open_telemetry: false)

  # Atur ID percakapan di opsi permintaan untuk satu panggilan.
  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    request_options: {open_telemetry: {conversation_id: "conv_42"}}
  )
  ```
</CodeGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Siapkan tracing API" icon="cloud" href="https://platform.claude.com/docs/id/manage-claude/opentelemetry/api">
    Dapatkan observabilitas ke dalam Claude API.
  </Card>

  <Card title="Lihat contoh trace" icon="sitemap" href="https://platform.claude.com/docs/id/manage-claude/opentelemetry#example-traces-and-how-to-read-them">
    Ikuti permintaan dari klien Anda hingga ke Claude API.
  </Card>
</CardGroup>

## Penelusuran stream

Span `anthropic.messages.create` dari sebuah stream berakhir ketika kode Anda telah membaca seluruh stream atau menutupnya, jadi tutuplah stream yang berhenti Anda baca lebih awal. Dalam mode konten, span berisi respons model hanya ketika Anda membaca stream dengan `messages.stream()` (go: `Messages.NewStreaming()`; java: `messages().createStreaming()`; csharp: `Messages.CreateStreaming()`; php: `messages->createStream()`).

Span yang Anda mulai saat membaca stream adalah saudara (sibling) dari span SDK, bukan turunannya. Untuk mengelompokkannya dengan permintaan, mulailah span Anda sendiri yang mencakup panggilan dan loop pembacaan.

## Penelusuran sandbox self-hosted Managed Agents

Dalam [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) Managed Agents, sandbox Anda yang menjalankan alat, sehingga span alat berasal dari SDK, bukan dari API. Environment worker di SDK Python, TypeScript, dan Go memancarkan span untuk setiap alat yang dijalankannya dan setiap permintaan yang dikirimnya. Worker mengelompokkannya di bawah satu span [`anthropic.environment.work`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-environment-work) untuk setiap item pekerjaan.

Untuk mendapatkan span ini:

1. Dalam proses yang menjalankan worker, [siapkan tracing SDK](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#install-the-sdk) seperti pada langkah 1 hingga 4.
2. Izinkan lalu lintas jaringan dari sandbox ke platform observabilitas Anda atau OpenTelemetry Collector.

Ketika worker mengirim hasil alat, span API dari permintaan tersebut bersarang di bawah span SDK-nya.

## Konteks trace dan baggage

Pada setiap permintaan, SDK menggunakan propagator aplikasi Anda untuk mengirim konteks trace ke API dalam header seperti `traceparent`. Jika propagator tersebut juga menulis baggage, SDK juga mengirim baggage Anda. Untuk mengirim konteks trace tanpa baggage, daftarkan hanya propagator konteks trace W3C.

Agar SDK tidak mengirim header ini, misalnya ketika instrumentasi klien HTTP Anda sudah mengirimnya, nonaktifkan propagasi SDK:

<CodeGroup exclude="shell">
  ```python Python
  client = Anthropic(open_telemetry={"propagation": False})
  ```

  <CodeGroupItem>
    ```typescript TypeScript
    const client = new Anthropic({ openTelemetry: { propagation: false } });
    ```

    <Warning>
      Tetapkan 

      `propagation: false`

       jika Anda menggunakan 

      `@opentelemetry/instrumentation-undici`

      , yang disertakan dalam 

      `@opentelemetry/auto-instrumentations-node`

      . Jika tidak, 

      [bug di paket tersebut](https://github.com/open-telemetry/opentelemetry-js-contrib/issues/3711)

       menambahkan header 

      `traceparent`

       kedua ke setiap permintaan, sehingga konteks trace menjadi tidak valid.
    </Warning>
  </CodeGroupItem>

  ```csharp C#
  using System.Diagnostics;

  // SDK menulis header ini dengan DistributedContextPropagator milik .NET.
  // Propagator tanpa output menghentikan header ini untuk setiap HttpClient dalam proses.
  // Atur sebelum Anda membuat klien apa pun.
  DistributedContextPropagator.Current = DistributedContextPropagator.CreateNoOutputPropagator();

  AnthropicClient client = new();
  ```

  ```go Go
  client := anthropic.NewClient(option.WithOpenTelemetryPropagation(false))
  ```

  ```java Java
  var envOptions = OpenTelemetryOptions.fromEnv();
  var client = AnthropicOkHttpClient.builder()
      .fromEnv()
      .openTelemetry(envOptions.toBuilder().propagation(false).build())
      .build();
  ```

  ```php PHP
  $client = new Client(openTelemetry: ['propagation' => false]);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new(open_telemetry: {propagation: false})
  ```
</CodeGroup>

Saat SDK memanggil [alat MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#client-side-mcp-helpers), span alat milik SDK adalah span saat ini. Beberapa pustaka klien MCP mengirim konteks trace ke server MCP di `_meta`, sehingga server yang membacanya dapat menambahkan span-nya ke trace Anda di bawah span alat tersebut. Paket Python `mcp` mulai versi 2.0 dan paket C# `ModelContextProtocol` melakukannya. SDK MCP untuk TypeScript, Go, Java, Ruby, dan PHP tidak melakukannya sendiri.

## Pemecahan masalah

| Masalah                                                                                                         | Yang perlu diperiksa                                                                                                                                                                                                                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tidak ada span dari SDK                                                                                         | Daftarkan tracer provider sebelum panggilan pertama. Pastikan Anda menginstal SDK seperti pada [Instal SDK](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#install-the-sdk) dan bahwa `ANTHROPIC_OPEN_TELEMETRY` tidak bernilai `false`.                                                                         |
| Java SDK tidak mengirim span ke tracer provider yang terdaftar, atau tidak mengirim konteks trace ke API        | Dependensi lain menetapkan `opentelemetry-api` di bawah 1.57.0. Tingkatkan `opentelemetry-api` ke 1.57.0 atau lebih baru.                                                                                                                                                                                                             |
| Span SDK tidak bersarang di bawah span Anda, atau span yang dibuat alat Anda tidak bersarang di bawah span alat | Panggil SDK dari dalam salah satu span Anda sendiri, seperti yang dilakukan [contoh di Hubungkan span API ke trace Anda sendiri](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#connect-api-spans-to-your-own-traces). Di Go, mulai span yang dibuat alat Anda dari `ctx` yang diteruskan tool runner kepadanya. |
| Permintaan dari SDK tidak memiliki header `traceparent`                                                         | Daftarkan propagator W3C trace context dengan OpenTelemetry. SDK menulis header dengan propagator aplikasi Anda.                                                                                                                                                                                                                      |
| Span SDK dari sebuah stream tidak berakhir atau tidak berisi respons                                            | Lihat [Penelusuran stream](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#trace-a-stream).                                                                                                                                                                                                                       |
| Setiap permintaan muncul dua kali                                                                               | Span SDK dan span API dari sebuah permintaan memiliki nama yang sama. Gunakan span kind atau `service.name` untuk membedakannya. Jika pustaka lain juga melacak SDK, nonaktifkan salah satu dari keduanya.                                                                                                                            |

## Availability

SDK tracing is in beta on every model.

### API support

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Availability: Available

| Status | Cloud platforms                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Beta   | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Amazon Bedrock (InvokeModel)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) |

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Availability: Available
* Usage: The SDK traces the requests that your code sends, such as the events you send to a session; spans for the agent’s model requests and tool calls come from API tracing. In a self-hosted sandbox, the SDK’s environment worker also traces each tool it runs.

| Status | Cloud platforms                                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------------------ |
| Beta   | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |
