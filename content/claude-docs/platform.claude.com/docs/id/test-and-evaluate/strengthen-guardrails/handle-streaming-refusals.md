---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: fc2da31055bbc4bd16d40e31c8b47ed47dfd8d4126163242d7800e396aef1089
---

# Penolakan streaming

Deteksi dan tangani stop reason penolakan dalam respons streaming, dan coba ulang permintaan yang ditolak pada model fallback.

---

Mulai dari model Claude 4, respons streaming dari API Claude mengembalikan **`stop_reason`: `"refusal"`** ketika classifier streaming melakukan intervensi untuk menangani potensi pelanggaran kebijakan. Fitur keamanan ini membantu menjaga kepatuhan konten selama streaming real-time.

<Tip>
  Halaman ini membahas bagaimana penolakan muncul dalam respons streaming. Untuk setiap nilai `stop_reason` dan cara menanganinya, lihat [Stop reason dan fallback](/docs/id/build-with-claude/handling-stop-reasons). Untuk mencoba ulang permintaan yang ditolak pada model Claude lain, lihat [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback).
</Tip>

## Format respons API

Ketika classifier streaming mendeteksi konten yang melanggar kebijakan Anthropic, API mengembalikan respons ini:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello.."
    }
  ],
  "stop_reason": "refusal",
  "stop_details": {
    "type": "refusal",
    "category": "cyber",
    "explanation": "This request was declined because it could enable cyber harm."
  }
}
```

Dalam event stream, `stop_details` tiba pada event `message_delta` bersama dengan `stop_reason`.

<Note>
  Respons `refusal` dari classifier streaming dapat menyertakan objek `stop_details` dengan `category` dan `explanation` yang dapat dibaca manusia yang dapat Anda tampilkan kepada pengguna. Lihat [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk bentuk respons lengkap dan kategori yang tersedia.

  `stop_details` (dan `category` / `explanation`-nya) dapat bernilai `null`, misalnya ketika penolakan tidak terpetakan ke kategori bernama mana pun, atau pada model yang lebih lama. Lakukan percabangan pada `stop_reason` alih-alih mengasumsikan `stop_details` terisi, dan sediakan pesan Anda sendiri untuk pengguna ketika nilainya `null`.
</Note>

## Reset konteks setelah penolakan

Ketika Anda menerima **`stop_reason`: `refusal`**, Anda harus mereset konteks percakapan sebelum melanjutkan. Anda dapat menghapus atau menyusun ulang giliran yang memicu penolakan, atau menghapus riwayat percakapan sepenuhnya. Mencoba melanjutkan tanpa mereset akan mengakibatkan penolakan yang berkelanjutan.

<Note>
  Metrik penggunaan tetap disediakan dalam respons, bahkan ketika respons ditolak.

  Ketika penolakan tiba sebelum Claude menghasilkan output apa pun, Anda tidak ditagih untuk permintaan tersebut pada API Claude, dan jumlah penggunaan dalam respons tersebut hanya bersifat informasional. Ketika Claude menghasilkan output sebelum penolakan, Anda ditagih untuk permintaan tersebut.
</Note>

<Tip>
  Mereset konteks bukan satu-satunya cara untuk pulih. Anda juga dapat mencoba ulang permintaan yang ditolak pada model Claude yang berbeda, dan halaman [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback) menunjukkan cara mengaturnya dengan fallback sisi server, middleware SDK, atau percobaan ulang manual.
</Tip>

## Panduan implementasi

Berikut cara mendeteksi dan menangani penolakan streaming dalam aplikasi Anda:

<CodeGroup>
  ```bash cURL
  # Lakukan streaming permintaan dan periksa adanya penolakan
  response=$(curl -N https://api.anthropic.com/v1/messages \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --data '{
      "model": "claude-opus-4-8",
      "messages": [{"role": "user", "content": "Hello"}],
      "max_tokens": 1024,
      "stream": true
    }')

  # Periksa adanya penolakan dalam stream
  if echo "$response" | grep -q '"stop_reason":"refusal"'; then
    echo "Response refused - resetting conversation context"
    # Reset status percakapan Anda di sini
  fi
  ```

  ```python Python
  client = anthropic.Anthropic()
  messages = []


  def reset_conversation():
      """Reset conversation context after refusal"""
      global messages
      messages = []
      print("Conversation reset due to refusal")


  try:
      with client.messages.stream(
          max_tokens=1024,
          messages=messages + [{"role": "user", "content": "Hello"}],
          model="claude-opus-4-8",
      ) as stream:
          for event in stream:
              # Periksa penolakan dalam delta pesan
              if event.type == "message_delta":
                  if event.delta.stop_reason == "refusal":
                      reset_conversation()
                      break
  except Exception as e:
      print(f"Error: {e}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  let messages: any[] = [];

  function resetConversation() {
    // Reset konteks percakapan setelah penolakan
    messages = [];
    console.log("Conversation reset due to refusal");
  }

  try {
    const stream = await client.messages.stream({
      messages: [...messages, { role: "user", content: "Hello" }],
      model: "claude-opus-4-8",
      max_tokens: 1024
    });

    for await (const event of stream) {
      // Periksa penolakan dalam delta pesan
      if (event.type === "message_delta" && event.delta.stop_reason === "refusal") {
        resetConversation();
        break;
      }
    }
  } catch (error) {
    console.error("Error:", error);
  }
  ```

  ```csharp C#
  using System;
  using System.Collections.Generic;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  class Program
  {
      private static List<Message> messages = new();

      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          var parameters = new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 1024,
              Messages = [new() { Role = Role.User, Content = "Hello" }]
          };

          try
          {
              await foreach (var msg in client.Messages.CreateStreaming(parameters))
              {
                  if (msg.Type == "message_delta" && msg.Delta?.StopReason == "refusal")
                  {
                      ResetConversation();
                      break;
                  }
              }
          }
          catch (Exception e)
          {
              Console.WriteLine($"Error: {e.Message}");
          }
      }

      private static void ResetConversation()
      {
          messages.Clear();
          Console.WriteLine("Conversation reset due to refusal");
      }
  }
  ```

  ```go Go
  var messages []anthropic.MessageParam

  func resetConversation() {
  	messages = []anthropic.MessageParam{}
  	fmt.Println("Conversation reset due to refusal")
  }
  // ...
  	client := anthropic.NewClient()

  	stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
  		},
  	})

  streamLoop:
  	for stream.Next() {
  		event := stream.Current()
  		switch eventVariant := event.AsAny().(type) {
  		case anthropic.MessageDeltaEvent:
  			if eventVariant.Delta.StopReason == "refusal" {
  				resetConversation()
  				break streamLoop
  			}
  		}
  	}

  	if err := stream.Err(); err != nil {
  		log.Fatal(err)
  	}
  ```

  ```java Java
  import com.anthropic.core.http.StreamResponse;
  import com.anthropic.models.messages.RawMessageStreamEvent;
  import com.anthropic.models.messages.StopReason;
  // ...

  List<MessageParam> messages = new ArrayList<>();

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addUserMessage("Hello")
          .build();

      try (StreamResponse<RawMessageStreamEvent> stream = client.messages().createStreaming(params)) {
          stream.stream().forEach(event -> {
              event.messageDelta().ifPresent(deltaEvent -> {
                  deltaEvent.delta().stopReason().ifPresent(stopReason -> {
                      if (stopReason.equals(StopReason.REFUSAL)) {
                          resetConversation();
                      }
                  });
              });
          });
      } catch (Exception e) {
          System.err.println("Error: " + e.getMessage());
      }
  }

  void resetConversation() {
      messages.clear();
      IO.println("Conversation reset due to refusal");
  }
  ```

  ```php PHP
  $client = new Client();
  $messages = [];

  function resetConversation(&$messages) {
      $messages = [];
      echo "Conversation reset due to refusal\n";
  }

  try {
      $stream = $client->messages->createStream(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Hello']
          ],
          model: 'claude-opus-4-8',
      );

      foreach ($stream as $event) {
          if (isset($event->type) && $event->type === 'message_delta') {
              if (isset($event->delta->stopReason) && $event->delta->stopReason === 'refusal') {
                  resetConversation($messages);
                  break;
              }
          }
      }
  } catch (Exception $e) {
      echo "Error: " . $e->getMessage() . "\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  messages = []

  def reset_conversation(messages)
    messages.clear
    puts "Conversation reset due to refusal"
  end

  begin
    stream = client.messages.stream(
      model: :"claude-opus-4-8",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello" }]
    )

    stream.each do |event|
      if event.type == :message_delta && event.delta.stop_reason == :refusal
        reset_conversation(messages)
        break
      end
    end
  rescue => e
    puts "Error: #{e.message}"
  end
  ```
</CodeGroup>

## Jenis penolakan saat ini

API saat ini menangani penolakan dengan tiga cara berbeda:

| Jenis Penolakan                  | Format Respons               | Kapan Terjadi                                      |
| -------------------------------- | ---------------------------- | -------------------------------------------------- |
| Penolakan classifier streaming   | **`stop_reason`: `refusal`** | Selama streaming ketika konten melanggar kebijakan |
| Validasi input API dan hak cipta | Kode error 400               | Ketika input gagal dalam pemeriksaan validasi      |
| Penolakan yang dihasilkan model  | Respons teks standar         | Ketika model itu sendiri memutuskan untuk menolak  |

<Note>
  Versi API mendatang akan memperluas pola **`stop_reason`: `refusal`** untuk menyatukan penanganan penolakan di semua jenis.
</Note>

## Praktik terbaik

* **Pantau penolakan:** Sertakan pemeriksaan **`stop_reason`: `refusal`** dalam penanganan error Anda
* **Reset secara otomatis:** Implementasikan reset konteks otomatis ketika penolakan terdeteksi
* **Fallback ke model lain:** Konfigurasikan [fallback sisi server atau middleware SDK](/docs/id/build-with-claude/refusals-and-fallback) sehingga permintaan yang ditolak dicoba ulang pada model Claude lain alih-alih menampilkan penolakan kepada pengguna
* **Tukarkan fallback credit pada percobaan ulang manual:** Jika Anda membangun percobaan ulang sendiri, teruskan token [fallback credit](/docs/id/build-with-claude/fallback-credit) dari penolakan sehingga percobaan ulang tidak membayar biaya prompt-cache dua kali
* **Sediakan pesan kustom:** Buat pesan yang ramah pengguna untuk UX yang lebih baik ketika penolakan terjadi
* **Lacak pola penolakan:** Pantau frekuensi penolakan untuk mengidentifikasi potensi masalah dengan prompt Anda

## Catatan migrasi

Jika Anda membangun penanganan penolakan ketika fitur ini pertama kali dirilis, atau Anda menambahkannya ke integrasi yang sudah ada, periksa hal-hal berikut:

* **Penolakan adalah respons, bukan error.** Penolakan tiba sebagai respons HTTP 200 yang berhasil dengan `stop_reason`: `"refusal"`, sehingga pemantauan yang hanya dibangun berdasarkan tingkat error tidak akan menampilkannya. Lacak penolakan sebagai sinyal tersendiri.
* **Model yang lebih baru mengembalikan detail lebih banyak.** Pada Claude Fable 5, penolakan juga menyertakan objek `stop_details` yang mengidentifikasi kategori kebijakan di balik penolakan tersebut. Lihat [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk bentuk respons lengkap.
* **Coba ulang pada model yang berbeda.** Mengirim ulang permintaan yang ditolak ke model yang sama biasanya menghasilkan penolakan lain. Alih-alih hanya mereset konteks, coba ulang pada model fallback dengan [fallback sisi server, middleware SDK, atau percobaan ulang manual](/docs/id/build-with-claude/refusals-and-fallback), dan tukarkan [fallback credit](/docs/id/build-with-claude/fallback-credit) ketika Anda membangun percobaan ulang sendiri.
* **Periksa hasil batch untuk penolakan.** Permintaan yang ditolak dalam [Message Batch](/docs/id/build-with-claude/batch-processing) dikembalikan sebagai hasil yang berhasil dengan `stop_reason`: `"refusal"`, bukan sebagai hasil yang error.
* **Pusatkan penanganan pada `stop_reason`.** API terus mengonsolidasikan penanganan penolakan di sekitar `stop_reason`: `"refusal"`, jadi lakukan percabangan pada stop reason alih-alih pada perilaku spesifik model.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Penolakan dan fallback" icon="arrows-clockwise" href="/docs/id/build-with-claude/refusals-and-fallback">
    Coba ulang permintaan yang ditolak pada model Claude lain, di sisi server atau di klien Anda.
  </Card>

  <Card title="Stop reason dan fallback" icon="code" href="/docs/id/build-with-claude/handling-stop-reasons">
    Setiap nilai `stop_reason` dan cara menanganinya.
  </Card>

  <Card title="Streaming pesan" icon="lightning" href="/docs/id/build-with-claude/streaming">
    Lakukan streaming respons dan baca `stop_reason` dari event `message_delta` saat tiba.
  </Card>

  <Card title="Dukungan multibahasa" icon="text-aa" href="/docs/id/build-with-claude/multilingual-support">
    Layani pengguna lintas bahasa dengan kemampuan lintas bahasa Claude.
  </Card>
</CardGroup>
