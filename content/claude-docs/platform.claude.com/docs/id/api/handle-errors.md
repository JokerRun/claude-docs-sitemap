---
source: platform
url: https://platform.claude.com/docs/id/api/handle-errors
fetched_at: 2026-11-26T02:13:38.275404Z
sha256: a9aeb4f19936cbd6c570fa09c9a787de0775ce6d0f64f11b656ecb3a9d3a849d
---

---
title: Menangani error
url: https://platform.claude.com/docs/id/api/handle-errors
description: Gunakan SDK untuk menangkap error Claude API berdasarkan kode error, status HTTP, atau kegagalan koneksi, dan untuk menangani error yang datang dalam stream.
---

Gunakan SDK untuk menangkap error Claude API berdasarkan kode error, status HTTP, atau kegagalan koneksi, dan untuk menangani error yang datang dalam stream. Untuk mempelajari arti setiap error atau untuk memanggil API tanpa SDK, lihat [Error Claude API](https://platform.claude.com/docs/id/api/errors).

<Note>
  Contoh-contoh di halaman ini memerlukan [versi terbaru SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview#latest-versions).
</Note>

## Menangkap error berdasarkan jenisnya

Contoh ini menangani satu [kode error](https://platform.claude.com/docs/id/api/errors#error-codes), satu status HTTP, kegagalan koneksi, dan setiap respons error lainnya:

<CodeGroup exclude="shell:cURL, shell:CLI">
  ```python Python
  client = anthropic.Anthropic()

  try:
      client.messages.create(
          model="claude-opus-5-5",
          max_tokens=1024,
          messages=[{"role": "user", "content": "Hello, Claude"}],
      )
  except anthropic.EnforcedSpendLimitReachedError as e:
      # Satu kode error: enforced_spend_limit_reached
      print("Monthly spend cap reached:", e.api_message)
  except anthropic.RateLimitError as e:
      # Satu status HTTP: 429 lainnya
      print("Rate limited. Request ID:", e.request_id)
  except anthropic.APIConnectionError:
      # Error tanpa respons, seperti kegagalan jaringan atau timeout
      print("Connection failed")
  except anthropic.APIStatusError as e:
      # Semua respons error lainnya
      print(e.status_code)  # HTTP status
      print(e.type)  # error.type
      print(e.api_message)  # error.message
      print(e.error_code)  # error.details.error_code if any
      print(e.details)  # error.details if any
      print(e.request_id)  # request_id
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  try {
    await client.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    });
  } catch (err) {
    if (err instanceof Anthropic.EnforcedSpendLimitReachedError) {
      // Satu kode error: enforced_spend_limit_reached
      console.log("Monthly spend cap reached:", err.apiMessage);
    } else if (err instanceof Anthropic.RateLimitError) {
      // Satu status HTTP: 429 lainnya
      console.log("Rate limited. Request ID:", err.requestID);
    } else if (err instanceof Anthropic.APIConnectionError) {
      // Error tanpa respons, seperti kegagalan jaringan atau timeout
      console.log("Connection failed");
    } else if (err instanceof Anthropic.APIError) {
      // Semua respons error lainnya
      console.log(err.status); // HTTP status
      console.log(err.type); // error.type
      console.log(err.apiMessage); // error.message
      console.log(err.errorCode); // error.details.error_code if any
      console.log(err.details); // error.details if any
      console.log(err.requestID); // request_id
    } else {
      throw err;
    }
  }
  ```

  ```csharp C#
  using Anthropic.Exceptions;
  using Anthropic.Models;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  try
  {
      await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new UserMessageParam { Content = "Hello, Claude" }]
      });
  }
  catch (AnthropicEnforcedSpendLimitReachedException e)
  {
      // Satu kode error: enforced_spend_limit_reached
      Console.WriteLine($"Monthly spend cap reached: {e.ApiMessage}");
  }
  catch (AnthropicRateLimitException e)
  {
      // Satu status HTTP: 429 lainnya
      Console.WriteLine($"Rate limited. Request ID: {e.RequestID}");
  }
  catch (Exception e) when (e is AnthropicIOException or TaskCanceledException)
  {
      // Error tanpa respons, seperti kegagalan jaringan atau timeout
      Console.WriteLine("Connection failed");
  }
  catch (AnthropicApiException e)
  {
      // Semua respons error lainnya
      Console.WriteLine((int)e.StatusCode); // HTTP status
      Console.WriteLine(e.Type?.Raw()); // error.type
      Console.WriteLine(e.ApiMessage); // error.message
      Console.WriteLine(e.ErrorCode); // error.details.error_code if any
      Console.WriteLine(e.Details); // error.details if any
      Console.WriteLine(e.RequestID); // request_id
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  _, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  })

  // Go SDK hanya memiliki satu tipe error. Buat percabangan berdasarkan kode dan status error.
  var apierr *anthropic.Error
  if errors.As(err, &apierr) {
  	switch {
  	case apierr.ErrorCode() == anthropic.ErrorCodeEnforcedSpendLimitReached:
  		// Satu kode error: enforced_spend_limit_reached
  		fmt.Println("Monthly spend cap reached:", apierr.Message)
  	case apierr.StatusCode == http.StatusTooManyRequests:
  		// Satu status HTTP: 429 lainnya
  		fmt.Println("Rate limited. Request ID:", apierr.RequestID)
  	default:
  		// Semua respons error lainnya
  		fmt.Println(apierr.StatusCode)        // HTTP status
  		fmt.Println(apierr.Type())            // error.type
  		fmt.Println(apierr.Message)           // error.message
  		fmt.Println(apierr.ErrorCode())       // error.details.error_code if any
  		fmt.Println(apierr.Details.RawJSON()) // error.details if any
  		fmt.Println(apierr.RequestID)         // request_id
  	}
  } else if err != nil {
  	// Error lain apa pun, seperti kegagalan jaringan atau timeout
  	fmt.Println("Connection failed")
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.errors.AnthropicIoException;
  import com.anthropic.errors.AnthropicServiceException;
  import com.anthropic.errors.RateLimitException;
  import com.anthropic.models.EnforcedSpendLimitReachedException;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024L)
          .addUserMessage("Hello, Claude")
          .build();

      try {
          client.messages().create(params);
      } catch (EnforcedSpendLimitReachedException e) {
          // Satu kode error: enforced_spend_limit_reached
          IO.println("Monthly spend cap reached: " + e.apiMessage().orElse(""));
      } catch (RateLimitException e) {
          // Satu status HTTP: 429 lainnya
          IO.println("Rate limited. Request ID: " + e.requestId().orElse(""));
      } catch (AnthropicIoException e) {
          // Error tanpa respons, seperti kegagalan jaringan atau timeout
          IO.println("Connection failed");
      } catch (AnthropicServiceException e) {
          // Semua respons error lainnya
          IO.println(e.statusCode()); // HTTP status
          IO.println(e.type().orElse(null)); // error.type
          IO.println(e.apiMessage().orElse(null)); // error.message
          IO.println(e.errorCode().orElse(null)); // error.details.error_code if any
          IO.println(e.errorDetails().orElse(null)); // error.details if any
          IO.println(e.requestId().orElse(null)); // request_id
      }
  }
  ```

  ```php PHP
  use Anthropic\Core\Exceptions\APIConnectionException;
  use Anthropic\Core\Exceptions\APIStatusException;
  use Anthropic\Core\Exceptions\RateLimitException;
  use Anthropic\EnforcedSpendLimitReachedException;
  use Anthropic\Messages\Model;

  $client = new Client();

  try {
      $client->messages->create(
          model: Model::CLAUDE_OPUS_5_5,
          maxTokens: 1024,
          messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      );
  } catch (EnforcedSpendLimitReachedException $e) {
      // Satu kode error: enforced_spend_limit_reached
      echo 'Monthly spend cap reached: ', $e->getAPIMessage(), PHP_EOL;
  } catch (RateLimitException $e) {
      // Satu status HTTP: 429 lainnya
      echo 'Rate limited. Request ID: ', $e->getRequestID(), PHP_EOL;
  } catch (APIConnectionException) {
      // Error tanpa respons, seperti kegagalan jaringan atau timeout
      echo 'Connection failed', PHP_EOL;
  } catch (APIStatusException $e) {
      // Semua respons error lainnya
      echo $e->status, PHP_EOL; // HTTP status
      echo $e->getType(), PHP_EOL; // error.type
      echo $e->getAPIMessage(), PHP_EOL; // error.message
      echo $e->getErrorCode(), PHP_EOL; // error.details.error_code if any
      echo json_encode($e->getDetails()), PHP_EOL; // error.details if any
      echo $e->getRequestID(), PHP_EOL; // request_id
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  begin
    client.messages.create(
      model: Anthropic::Model::CLAUDE_OPUS_5_5,
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    )
  rescue Anthropic::EnforcedSpendLimitReachedError => e
    # Satu kode error: enforced_spend_limit_reached
    puts "Monthly spend cap reached: #{e.api_message}"
  rescue Anthropic::Errors::RateLimitError => e
    # Satu status HTTP: 429 lainnya
    puts "Rate limited. Request ID: #{e.request_id}"
  rescue Anthropic::Errors::APIConnectionError
    # Error tanpa respons, seperti kegagalan jaringan atau timeout
    puts "Connection failed"
  rescue Anthropic::Errors::APIStatusError => e
    # Semua respons error lainnya
    puts e.status # HTTP status
    puts e.type # error.type as a symbol
    puts e.api_message # error.message
    puts e.error_code # error.details.error_code as a symbol if any
    puts e.details # error.details if any
    puts e.request_id # request_id
  end
  ```
</CodeGroup>

Error sampai ke kode Anda setelah percobaan ulang milik SDK sendiri, jika ada, gagal (lihat [Percobaan ulang](https://platform.claude.com/docs/id/api/errors#retries)). Untuk arti setiap status, lihat [Error HTTP](https://platform.claude.com/docs/id/api/errors#http-errors).

Letakkan kasus yang sempit sebelum kasus yang luas. Messages API mengembalikan `enforced_spend_limit_reached`, kode untuk [batas pengeluaran bulanan](https://platform.claude.com/docs/id/api/rate-limits#reaching-your-spend-cap), dengan status 429. Jika cabang untuk status 429 diletakkan lebih dulu, cabang tersebut juga akan menangkap kode itu.

Untuk menangani kasus lain, seperti 404, lihat [Tipe error SDK](https://platform.claude.com/docs/id/api/errors#sdk-error-types).

## Menangani kode error tertentu

Untuk menangani kode error lain, tambahkan cabangnya ke [Menangkap error berdasarkan jenisnya](https://platform.claude.com/docs/id/api/handle-errors#catch-errors-by-kind) sebelum cabang yang lebih luas.

Setiap kode memiliki kelas atau konstantanya sendiri yang dinamai sesuai kodenya, seperti `anthropic.EnforcedSpendLimitReachedError` (typescript: `Anthropic.EnforcedSpendLimitReachedError`; ruby: `Anthropic::EnforcedSpendLimitReachedError`; java: `com.anthropic.models.EnforcedSpendLimitReachedException`; php: `Anthropic\EnforcedSpendLimitReachedException`; csharp: `Anthropic.Models.AnthropicEnforcedSpendLimitReachedException`; go: `anthropic.ErrorCodeEnforcedSpendLimitReached`). Kelas untuk kode lain mungkin berada di namespace lain. Untuk menemukannya, cari nama kelas tersebut di kode sumber SDK. Komentar dokumentasi sebuah metode mencantumkan kelas atau konstanta untuk setiap kode yang dapat dikembalikan oleh metode tersebut.

Untuk daftar lengkap kode, lihat [`ErrorDetails`](https://platform.claude.com/docs/id/api/$shared#error_details) di referensi API.

## Menangani error dalam stream

Setelah stream dimulai, API telah mengembalikan status 200, sehingga API mengirimkan error sebagai [event error](https://platform.claude.com/docs/id/build-with-claude/streaming#error-events). SDK tidak mencoba ulang permintaan tersebut.

Setiap event error sampai kepada Anda sebagai `APIStatusError` (typescript: `APIError`; csharp: `AnthropicSseException`; java: `SseException`; php: `APIStatusException`; go: `*anthropic.Error`). Status HTTP-nya adalah 200 milik stream atau tidak ada. Jadi cabang untuk satu status atau untuk kelas satu kode tidak akan menangkapnya. Sebagai gantinya, periksa apakah `error.type`-nya merupakan salah satu tipe di [Error HTTP](https://platform.claude.com/docs/id/api/errors#http-errors):

<CodeGroup exclude="shell:cURL, shell:CLI">
  ```python Python
  client = anthropic.Anthropic()

  try:
      with client.messages.stream(
          model="claude-opus-5-5",
          max_tokens=1024,
          messages=[{"role": "user", "content": "Hello, Claude"}],
      ) as stream:
          for text in stream.text_stream:
              print(text, end="", flush=True)
  except anthropic.APIStatusError as e:
      if e.type == "overloaded_error":
          # Satu error.type: overloaded_error
          print("\nOverloaded:", e.api_message)
      else:
          raise
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  try {
    await client.messages
      .stream({
        model: "claude-opus-5-5",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hello, Claude" }]
      })
      .on("text", (text) => {
        process.stdout.write(text);
      })
      .finalMessage();
  } catch (err) {
    if (err instanceof Anthropic.APIError && err.type === "overloaded_error") {
      // Satu error.type: overloaded_error
      console.log("\nOverloaded:", err.apiMessage);
    } else {
      throw err;
    }
  }
  ```

  ```csharp C#
  using Anthropic.Exceptions;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new UserMessageParam { Content = "Hello, Claude" }]
  };

  try
  {
      await foreach (var streamEvent in client.Messages.CreateStreaming(parameters))
      {
          if (
              streamEvent.TryPickContentBlockDelta(out var deltaEvent)
              && deltaEvent.Delta.TryPickText(out var textDelta)
          )
          {
              Console.Write(textDelta.Text);
          }
      }
  }
  // Kelas dasar dari AnthropicSseException (event error)
  // dan AnthropicApiException (respons error)
  catch (AnthropicServiceException e) when (e.Type?.Raw() == "overloaded_error")
  {
      // Satu error.type: overloaded_error
      Console.WriteLine($"\nOverloaded: {e.ApiMessage}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  })

  for stream.Next() {
  	event := stream.Current()
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.ContentBlockDeltaEvent:
  		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
  		case anthropic.TextDelta:
  			fmt.Print(deltaVariant.Text)
  		}
  	}
  }

  err := stream.Err()
  var apierr *anthropic.Error
  if errors.As(err, &apierr) && apierr.Type() == anthropic.ErrorTypeOverloadedError {
  	// Satu error.type: overloaded_error
  	fmt.Println("\nOverloaded:", apierr.Message)
  } else if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.errors.AnthropicServiceException;
  import com.anthropic.models.ErrorType;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024L)
          .addUserMessage("Hello, Claude")
          .build();

      try (var streamResponse = client.messages().createStreaming(params)) {
          streamResponse.stream().forEach(event -> {
              event.contentBlockDelta().ifPresent(deltaEvent ->
                  deltaEvent.delta().text().ifPresent(textDelta ->
                      IO.print(textDelta.text())
                  )
              );
          });
      } catch (AnthropicServiceException e) {
          // Menangkap event error (SseException) dan respons error
          if (ErrorType.OVERLOADED_ERROR.equals(e.type().orElse(null))) {
              // Satu error.type: overloaded_error
              IO.println("\nOverloaded: " + e.apiMessage().orElse(""));
          } else {
              throw e;
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Core\Exceptions\APIStatusException;
  use Anthropic\Messages\Model;
  use Anthropic\Messages\RawContentBlockDeltaEvent;
  use Anthropic\Messages\TextDelta;

  $client = new Client();

  try {
      $stream = $client->messages->createStream(
          model: Model::CLAUDE_OPUS_5_5,
          maxTokens: 1024,
          messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      );

      foreach ($stream as $event) {
          if (
              $event instanceof RawContentBlockDeltaEvent
              && $event->delta instanceof TextDelta
          ) {
              echo $event->delta->text;
          }
      }
  } catch (APIStatusException $e) {
      if ($e->getType() === 'overloaded_error') {
          // Satu error.type: overloaded_error
          echo PHP_EOL, 'Overloaded: ', $e->getAPIMessage(), PHP_EOL;
      } else {
          throw $e;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  begin
    stream = client.messages.stream(
      model: Anthropic::Model::CLAUDE_OPUS_5_5,
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    )

    stream.text.each { |text| print(text) }
  rescue Anthropic::Errors::APIStatusError => e
    if e.type == :overloaded_error
      # Satu error.type: overloaded_error
      puts "\nOverloaded: #{e.api_message}"
    else
      raise
    end
  end
  ```
</CodeGroup>

Event error juga dapat memiliki [kode error](https://platform.claude.com/docs/id/api/errors#error-codes). Baca kode tersebut dari `error_code` (typescript: `errorCode`; csharp: `ErrorCode`; java: `errorCode().orElse(null)`; php: `getErrorCode()`; go: `ErrorCode()`) dan bandingkan dengan kode yang ingin Anda tangani, seperti `"enforced_spend_limit_reached"` (ruby: `:enforced_spend_limit_reached`; go: `anthropic.ErrorCodeEnforcedSpendLimitReached`).

Stream dapat gagal dengan dua cara lain:

* **Permintaan gagal sebelum stream dimulai:** Anda mendapatkan error yang ada di [Menangkap error berdasarkan jenisnya](https://platform.claude.com/docs/id/api/handle-errors#catch-errors-by-kind).
* **Koneksi terputus di tengah stream:** Tidak ada event error yang datang, dan cabang koneksi di [Menangkap error berdasarkan jenisnya](https://platform.claude.com/docs/id/api/handle-errors#catch-errors-by-kind) mungkin tidak menangkap error tersebut. Untuk mengetahui apa yang menangkapnya, lihat [Tipe error SDK](https://platform.claude.com/docs/id/api/errors#sdk-error-types).

Untuk melanjutkan respons setelah stream gagal, lihat [Pemulihan error](https://platform.claude.com/docs/id/build-with-claude/streaming#error-recovery).
