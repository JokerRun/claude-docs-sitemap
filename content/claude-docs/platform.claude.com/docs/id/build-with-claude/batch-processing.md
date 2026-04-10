---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/batch-processing
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 8f0301d4b539b67accbe6768cf1ea0ddbad5c65f8fd82210df62405dbbf076f9
---

# Pemrosesan batch

Pelajari cara menggunakan Message Batches API untuk memproses volume besar permintaan secara asinkron dengan efisien biaya.

---

Pemrosesan batch adalah pendekatan yang kuat untuk menangani volume besar permintaan secara efisien. Alih-alih memproses permintaan satu per satu dengan respons langsung, pemrosesan batch memungkinkan Anda mengirimkan beberapa permintaan sekaligus untuk pemrosesan asinkron. Pola ini sangat berguna ketika:

- Anda perlu memproses volume besar data
- Respons langsung tidak diperlukan
- Anda ingin mengoptimalkan efisiensi biaya
- Anda menjalankan evaluasi atau analisis skala besar

Message Batches API adalah implementasi pertama Anthropic dari pola ini.

<Note>
This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

---

# Message Batches API

Message Batches API adalah cara yang kuat dan hemat biaya untuk memproses secara asinkron volume besar permintaan [Messages](/docs/id/api/messages/create). Pendekatan ini sangat cocok untuk tugas yang tidak memerlukan respons langsung, dengan sebagian besar batch selesai dalam waktu kurang dari 1 jam sambil mengurangi biaya sebesar 50% dan meningkatkan throughput.

Anda dapat [menjelajahi referensi API secara langsung](/docs/id/api/creating-message-batches), selain panduan ini.

## Cara kerja Message Batches API

Ketika Anda mengirimkan permintaan ke Message Batches API:

1. Sistem membuat Message Batch baru dengan permintaan Messages yang disediakan.
2. Batch kemudian diproses secara asinkron, dengan setiap permintaan ditangani secara independen.
3. Anda dapat melakukan polling untuk status batch dan mengambil hasil ketika pemrosesan telah berakhir untuk semua permintaan.

Ini sangat berguna untuk operasi massal yang tidak memerlukan hasil langsung, seperti:
- Evaluasi skala besar: Proses ribuan kasus uji secara efisien.
- Moderasi konten: Analisis volume besar konten buatan pengguna secara asinkron.
- Analisis data: Hasilkan wawasan atau ringkasan untuk dataset besar.
- Pembuatan konten massal: Buat jumlah besar teks untuk berbagai tujuan (misalnya, deskripsi produk, ringkasan artikel).

### Batasan batch
- Message Batch dibatasi hingga 100.000 permintaan Message atau 256 MB ukuran, mana pun yang tercapai terlebih dahulu.
- Sistem memproses setiap batch secepat mungkin, dengan sebagian besar batch selesai dalam 1 jam. Anda dapat mengakses hasil batch ketika semua pesan telah selesai atau setelah 24 jam, mana pun yang lebih dulu. Batch kedaluwarsa jika pemrosesan tidak selesai dalam 24 jam.
- Hasil batch tersedia selama 29 hari setelah pembuatan. Setelah itu, Anda mungkin masih dapat melihat Batch, tetapi hasilnya tidak akan lagi tersedia untuk diunduh.
- Batch dibatasi pada [Workspace](/settings/workspaces). Anda dapat melihat semua batch (dan hasilnya) yang dibuat dalam Workspace yang kunci API Anda miliki.
- Batas laju berlaku untuk permintaan HTTP Batches API dan jumlah permintaan dalam batch yang menunggu untuk diproses. Lihat [batas laju Message Batches API](/docs/id/api/rate-limits#message-batches-api). Selain itu, pemrosesan dapat diperlambat berdasarkan permintaan saat ini dan volume permintaan Anda. Dalam hal itu, Anda mungkin melihat lebih banyak permintaan kedaluwarsa setelah 24 jam.
- Karena throughput tinggi dan pemrosesan bersamaan, batch mungkin sedikit melampaui [batas pengeluaran](/settings/limits) yang dikonfigurasi Workspace Anda.

### Model yang didukung

Semua [model aktif](/docs/id/about-claude/models/overview) mendukung Message Batches API.

### Apa yang dapat di-batch
Permintaan apa pun yang dapat Anda buat ke Messages API dapat disertakan dalam batch. Ini termasuk:

- Vision
- Tool use
- Pesan sistem
- Percakapan multi-turn
- Fitur beta apa pun

Karena setiap permintaan dalam batch diproses secara independen, Anda dapat mencampur berbagai jenis permintaan dalam satu batch.

<Tip>
Karena batch dapat memakan waktu lebih lama dari 5 menit untuk diproses, pertimbangkan menggunakan [durasi cache 1 jam](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) dengan prompt caching untuk tingkat cache hit yang lebih baik saat memproses batch dengan konteks bersama.
</Tip>

---
## Harga

Batches API menawarkan penghematan biaya yang signifikan. Semua penggunaan dikenakan biaya pada 50% dari harga API standar.

| Model             | Batch input      | Batch output    |
|-------------------|------------------|-----------------|
| Claude Opus 4.6       | $2.50 / MTok     | $12.50 / MTok   |
| Claude Opus 4.5     | $2.50 / MTok     | $12.50 / MTok   |
| Claude Opus 4.1     | $7.50 / MTok     | $37.50 / MTok   |
| Claude Opus 4     | $7.50 / MTok     | $37.50 / MTok   |
| Claude Sonnet 4.6   | $1.50 / MTok     | $7.50 / MTok    |
| Claude Sonnet 4.5   | $1.50 / MTok     | $7.50 / MTok    |
| Claude Sonnet 4   | $1.50 / MTok     | $7.50 / MTok    |
| Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)) | $1.50 / MTok     | $7.50 / MTok    |
| Claude Haiku 4.5  | $0.50 / MTok     | $2.50 / MTok    |
| Claude Haiku 3.5  | $0.40 / MTok     | $2 / MTok       |
| Claude Opus 3 ([deprecated](/docs/en/about-claude/model-deprecations))  | $7.50 / MTok     | $37.50 / MTok   |
| Claude Haiku 3    | $0.125 / MTok    | $0.625 / MTok   |

---
## Cara menggunakan Message Batches API

### Siapkan dan buat batch Anda

Message Batch terdiri dari daftar permintaan untuk membuat Message. Bentuk permintaan individual terdiri dari:
- `custom_id` unik untuk mengidentifikasi permintaan Messages
- Objek `params` dengan parameter [Messages API](/docs/id/api/messages/create) standar

Anda dapat [membuat batch](/docs/id/api/creating-message-batches) dengan melewatkan daftar ini ke parameter `requests`:

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages/batches \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "requests": [
        {
            "custom_id": "my-first-request",
            "params": {
                "model": "claude-opus-4-6",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "Hello, world"}
                ]
            }
        },
        {
            "custom_id": "my-second-request",
            "params": {
                "model": "claude-opus-4-6",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "Hi again, friend"}
                ]
            }
        }
    ]
}'
```

```bash CLI
ant messages:batches create <<'YAML'
requests:
  - custom_id: my-first-request
    params:
      model: claude-opus-4-6
      max_tokens: 1024
      messages:
        - role: user
          content: Hello, world
  - custom_id: my-second-request
    params:
      model: claude-opus-4-6
      max_tokens: 1024
      messages:
        - role: user
          content: Hi again, friend
YAML
```

```python Python hidelines={1}
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

client = anthropic.Anthropic()

message_batch = client.messages.batches.create(
    requests=[
        Request(
            custom_id="my-first-request",
            params=MessageCreateParamsNonStreaming(
                model="claude-opus-4-6",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello, world",
                    }
                ],
            ),
        ),
        Request(
            custom_id="my-second-request",
            params=MessageCreateParamsNonStreaming(
                model="claude-opus-4-6",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": "Hi again, friend",
                    }
                ],
            ),
        ),
    ]
)

print(message_batch)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const messageBatch = await anthropic.messages.batches.create({
  requests: [
    {
      custom_id: "my-first-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hello, world" }]
      }
    },
    {
      custom_id: "my-second-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hi again, friend" }]
      }
    }
  ]
});

console.log(messageBatch);
```

```csharp C#
using Anthropic;
using Anthropic.Models.Messages;
using Anthropic.Models.Messages.Batches;

AnthropicClient client = new();

var batch = await client.Messages.Batches.Create(new BatchCreateParams
{
    Requests =
    [
        new()
        {
            CustomID = "my-first-request",
            Params = new()
            {
                Model = Model.ClaudeOpus4_6,
                MaxTokens = 1024,
                Messages =
                [
                    new() { Role = Role.User, Content = "Hello, world" }
                ]
            }
        },
        new()
        {
            CustomID = "my-second-request",
            Params = new()
            {
                Model = Model.ClaudeOpus4_6,
                MaxTokens = 1024,
                Messages =
                [
                    new() { Role = Role.User, Content = "Hi again, friend" }
                ]
            }
        }
    ]
});

Console.WriteLine(batch);
```

```go Go hidelines={1..10,-1}
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	batch, _ := client.Messages.Batches.New(context.Background(),
		anthropic.MessageBatchNewParams{
			Requests: []anthropic.MessageBatchNewParamsRequest{
				{
					CustomID: "my-first-request",
					Params: anthropic.MessageBatchNewParamsRequestParams{
						Model:     anthropic.ModelClaudeOpus4_6,
						MaxTokens: 1024,
						Messages: []anthropic.MessageParam{
							anthropic.NewUserMessage(
								anthropic.NewTextBlock("Hello, world"),
							),
						},
					},
				},
				{
					CustomID: "my-second-request",
					Params: anthropic.MessageBatchNewParamsRequestParams{
						Model:     anthropic.ModelClaudeOpus4_6,
						MaxTokens: 1024,
						Messages: []anthropic.MessageParam{
							anthropic.NewUserMessage(
								anthropic.NewTextBlock("Hi again, friend"),
							),
						},
					},
				},
			},
		})

	fmt.Println(batch.ID)
}
```

```java Java hidelines={1..3,5..8,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.batches.*;

public class BatchExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    BatchCreateParams params = BatchCreateParams.builder()
      .addRequest(
        BatchCreateParams.Request.builder()
          .customId("my-first-request")
          .params(
            BatchCreateParams.Request.Params.builder()
              .model(Model.CLAUDE_OPUS_4_6)
              .maxTokens(1024)
              .addUserMessage("Hello, world")
              .build()
          )
          .build()
      )
      .addRequest(
        BatchCreateParams.Request.builder()
          .customId("my-second-request")
          .params(
            BatchCreateParams.Request.Params.builder()
              .model(Model.CLAUDE_OPUS_4_6)
              .maxTokens(1024)
              .addUserMessage("Hi again, friend")
              .build()
          )
          .build()
      )
      .build();

    MessageBatch messageBatch = client.messages().batches().create(params);

    System.out.println(messageBatch);
  }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(
    apiKey: getenv("ANTHROPIC_API_KEY")
);

$batch = $client->messages->batches->create(
    requests: [
        [
            'custom_id' => 'my-first-request',
            'params' => [
                'model' => 'claude-opus-4-6',
                'max_tokens' => 1024,
                'messages' => [
                    ['role' => 'user', 'content' => 'Hello, world']
                ]
            ]
        ],
        [
            'custom_id' => 'my-second-request',
            'params' => [
                'model' => 'claude-opus-4-6',
                'max_tokens' => 1024,
                'messages' => [
                    ['role' => 'user', 'content' => 'Hi again, friend']
                ]
            ]
        ]
    ],
);

print_r($batch);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

batch = client.messages.batches.create(
  requests: [
    {
      custom_id: "my-first-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 1024,
        messages: [
          { role: "user", content: "Hello, world" }
        ]
      }
    },
    {
      custom_id: "my-second-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 1024,
        messages: [
          { role: "user", content: "Hi again, friend" }
        ]
      }
    }
  ]
)

puts batch
```

</CodeGroup>

Dalam contoh ini, dua permintaan terpisah di-batch bersama untuk pemrosesan asinkron. Setiap permintaan memiliki `custom_id` unik dan berisi parameter standar yang akan Anda gunakan untuk panggilan Messages API.

<Tip>
  **Uji permintaan batch Anda dengan Messages API**

Validasi objek `params` untuk setiap permintaan pesan dilakukan secara asinkron, dan kesalahan validasi dikembalikan ketika pemrosesan seluruh batch telah berakhir. Anda dapat memastikan bahwa Anda membangun input dengan benar dengan memverifikasi bentuk permintaan Anda dengan [Messages API](/docs/id/api/messages/create) terlebih dahulu.
</Tip>

Ketika batch pertama kali dibuat, respons akan memiliki status pemrosesan `in_progress`.

```json Output
{
  "id": "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d",
  "type": "message_batch",
  "processing_status": "in_progress",
  "request_counts": {
    "processing": 2,
    "succeeded": 0,
    "errored": 0,
    "canceled": 0,
    "expired": 0
  },
  "ended_at": null,
  "created_at": "2024-09-24T18:37:24.100435Z",
  "expires_at": "2024-09-25T18:37:24.100435Z",
  "cancel_initiated_at": null,
  "results_url": null
}
```

### Melacak batch Anda

Bidang `processing_status` Message Batch menunjukkan tahap pemrosesan batch. Dimulai sebagai `in_progress`, kemudian diperbarui ke `ended` setelah semua permintaan dalam batch selesai diproses, dan hasil siap. Anda dapat memantau status batch Anda dengan mengunjungi [Console](/settings/workspaces/default/batches), atau menggunakan [endpoint pengambilan](/docs/id/api/retrieving-message-batches).

#### Polling untuk penyelesaian Message Batch

Untuk melakukan polling Message Batch, Anda memerlukan `id`-nya, yang disediakan dalam respons saat membuat batch atau dengan membuat daftar batch. Anda dapat mengimplementasikan loop polling yang memeriksa status batch secara berkala hingga pemrosesan berakhir:

<CodeGroup>
```bash Shell hidelines={2..16,23}
#!/bin/sh
MESSAGE_BATCH_ID=$(curl -s https://api.anthropic.com/v1/messages/batches \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "requests": [{
      "custom_id": "test-1",
      "params": {
        "model": "claude-opus-4-6",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "Hi"}]
      }
    }]
  }' | jq -r '.id')

until [[ $(curl -s "https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID" \
          --header "x-api-key: $ANTHROPIC_API_KEY" \
          --header "anthropic-version: 2023-06-01" \
          | grep -o '"processing_status":[[:space:]]*"[^"]*"' \
          | cut -d'"' -f4) == "ended" ]]; do
    echo "Batch $MESSAGE_BATCH_ID is still processing..."
    break
    sleep 60
done

echo "Batch $MESSAGE_BATCH_ID has finished processing"
```

```bash CLI hidelines={2..14,19}
#!/bin/bash
MESSAGE_BATCH_ID=$(ant messages:batches create \
  --transform id --format yaml <<'YAML'
requests:
  - custom_id: test-1
    params:
      model: claude-opus-4-6
      max_tokens: 100
      messages:
        - role: user
          content: Hi
YAML
)

until [[ $(ant messages:batches retrieve \
          --message-batch-id "$MESSAGE_BATCH_ID" \
          --transform processing_status --format yaml) == "ended" ]]; do
    echo "Batch $MESSAGE_BATCH_ID is still processing..."
    break
    sleep 60
done

echo "Batch $MESSAGE_BATCH_ID has finished processing"
```

```python Python nocheck hidelines={1}
import anthropic
import time

client = anthropic.Anthropic()

MESSAGE_BATCH_ID = "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d"

message_batch = None
while True:
    message_batch = client.messages.batches.retrieve(MESSAGE_BATCH_ID)
    if message_batch.processing_status == "ended":
        break

    print(f"Batch {MESSAGE_BATCH_ID} is still processing...")
    time.sleep(60)
print(message_batch)
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const messageBatchId = "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d";

let messageBatch;
while (true) {
  messageBatch = await anthropic.messages.batches.retrieve(messageBatchId);
  if (messageBatch.processing_status === "ended") {
    break;
  }

  console.log(`Batch ${messageBatchId} is still processing... waiting`);
  await new Promise((resolve) => setTimeout(resolve, 60_000));
}
console.log(messageBatch);
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages.Batches;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();
        string messageBatchId = Environment.GetEnvironmentVariable("MESSAGE_BATCH_ID");

        MessageBatch messageBatch = null;
        while (true)
        {
            messageBatch = await client.Messages.Batches.Retrieve(messageBatchId);
            if (messageBatch.ProcessingStatus == "ended")
            {
                break;
            }

            Console.WriteLine($"Batch {messageBatchId} is still processing...");
            await Task.Delay(60000);
        }
        Console.WriteLine(messageBatch);
    }
}
```

```go Go nocheck hidelines={1..14,-1}
package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()
	messageBatchID := os.Getenv("MESSAGE_BATCH_ID")

	var messageBatch *anthropic.MessageBatch
	for {
		var err error
		messageBatch, err = client.Messages.Batches.Get(context.TODO(), messageBatchID)
		if err != nil {
			log.Fatal(err)
		}
		if messageBatch.ProcessingStatus == "ended" {
			break
		}

		fmt.Printf("Batch %s is still processing...\n", messageBatchID)
		time.Sleep(60 * time.Second)
	}
	fmt.Println(messageBatch)
}
```

```java Java nocheck hidelines={1..2,4..6,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.batches.MessageBatch;

public class MessageBatchPolling {
    public static void main(String[] args) throws InterruptedException {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();
        String messageBatchId = "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d";

        MessageBatch messageBatch = null;
        while (true) {
            messageBatch = client.messages().batches().retrieve(messageBatchId);
            if (messageBatch.processingStatus().equals(MessageBatch.ProcessingStatus.ENDED)) {
                break;
            }

            System.out.println("Batch " + messageBatchId + " is still processing...");
            Thread.sleep(60000);
        }
        System.out.println(messageBatch);
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));
$messageBatchId = getenv("MESSAGE_BATCH_ID");

$messageBatch = null;
while (true) {
    $messageBatch = $client->messages->batches->retrieve(
        messageBatchID: $messageBatchId,
    );
    if ($messageBatch->processingStatus === "ended") {
        break;
    }

    echo "Batch {$messageBatchId} is still processing...\n";
    sleep(60);
}
echo json_encode($messageBatch, JSON_PRETTY_PRINT);
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message_batch_id = ENV["MESSAGE_BATCH_ID"]
message_batch = nil
loop do
  message_batch = client.messages.batches.retrieve(message_batch_id)
  break if message_batch.processing_status == :ended

  puts "Batch #{message_batch_id} is still processing..."
  sleep 60
end
puts message_batch
```

</CodeGroup>

### Membuat daftar semua Message Batches

Anda dapat membuat daftar semua Message Batches di Workspace Anda menggunakan [endpoint daftar](/docs/id/api/listing-message-batches). API mendukung paginasi, secara otomatis mengambil halaman tambahan sesuai kebutuhan:

<CodeGroup>
```bash Shell
#!/bin/sh

if ! command -v jq &> /dev/null; then
    echo "Error: This script requires jq. Please install it first."
    exit 1
fi

BASE_URL="https://api.anthropic.com/v1/messages/batches"

has_more=true
after_id=""

while [ "$has_more" = true ]; do
    # Construct URL with after_id if it exists
    if [ -n "$after_id" ]; then
        url="${BASE_URL}?limit=20&after_id=${after_id}"
    else
        url="$BASE_URL?limit=20"
    fi

    response=$(curl -s "$url" \
              --header "x-api-key: $ANTHROPIC_API_KEY" \
              --header "anthropic-version: 2023-06-01")

    # Extract values using jq
    has_more=$(echo "$response" | jq -r '.has_more')
    after_id=$(echo "$response" | jq -r '.last_id')

    # Process and print each entry in the data array
    echo "$response" | jq -c '.data[]' | while read -r entry; do
        echo "$entry" | jq '.'
    done
done
```

```bash CLI
# Automatically fetches more pages as needed
ant messages:batches list --limit 20
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Automatically fetches more pages as needed.
for message_batch in client.messages.batches.list(limit=20):
    print(message_batch)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

// Automatically fetches more pages as needed.
for await (const messageBatch of anthropic.messages.batches.list({
  limit: 20
})) {
  console.log(messageBatch);
}
```

```csharp C# hidelines={1..11,-2..}
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages.Batches;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new BatchListParams
        {
            Limit = 20
        };

        // Automatically fetches more pages as needed
        var page = await client.Messages.Batches.List(parameters);
        await foreach (var messageBatch in page.Paginate())
        {
            Console.WriteLine(messageBatch);
        }
    }
}
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	// Automatically fetches more pages as needed
	iter := client.Messages.Batches.ListAutoPaging(context.TODO(), anthropic.MessageBatchListParams{
		Limit: anthropic.Int(20),
	})

	for iter.Next() {
		messageBatch := iter.Current()
		fmt.Println(messageBatch)
	}

	if err := iter.Err(); err != nil {
		log.Fatal(err)
	}
}
```

```java Java hidelines={1..2,4..7,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.batches.*;

public class BatchListExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Automatically fetches more pages as needed
    for (MessageBatch messageBatch : client
      .messages()
      .batches()
      .list(BatchListParams.builder().limit(20).build())
      .autoPager()) {
      System.out.println(messageBatch);
    }
  }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

// Automatically fetches more pages as needed
foreach ($client->messages->batches->list(limit: 20)->pagingEachItem() as $messageBatch) {
    echo $messageBatch->id . "\n";
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Automatically fetches more pages as needed
client.messages.batches.list(limit: 20).auto_paging_each do |message_batch|
  puts message_batch
end
```

</CodeGroup>

### Mengambil hasil batch

Setelah pemrosesan batch selesai, setiap permintaan Messages dalam batch memiliki hasil. Ada 4 jenis hasil:

| Jenis Hasil | Deskripsi |
|-------------|-------------|
| `succeeded` | Permintaan berhasil. Mencakup hasil pesan. |
| `errored`   | Permintaan mengalami kesalahan dan pesan tidak dibuat. Kemungkinan kesalahan termasuk permintaan yang tidak valid dan kesalahan server internal. Anda tidak akan ditagih untuk permintaan ini. |
| `canceled`  | Pengguna membatalkan batch sebelum permintaan ini dapat dikirim ke model. Anda tidak akan ditagih untuk permintaan ini. |
| `expired`   | Batch mencapai kedaluwarsa 24 jam sebelum permintaan ini dapat dikirim ke model. Anda tidak akan ditagih untuk permintaan ini. |

Anda akan melihat ringkasan hasil Anda dengan `request_counts` batch, yang menunjukkan berapa banyak permintaan yang mencapai masing-masing dari empat status ini.

Hasil batch tersedia untuk diunduh di properti `results_url` pada Message Batch, dan jika izin organisasi memungkinkan, di Console. Karena ukuran hasil yang berpotensi besar, disarankan untuk [streaming hasil](/docs/id/api/retrieving-message-batch-results) kembali daripada mengunduhnya sekaligus.

<CodeGroup>

```bash Shell
#!/bin/sh
curl "https://api.anthropic.com/v1/messages/batches/msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  | grep -o '"results_url":[[:space:]]*"[^"]*"' \
  | cut -d'"' -f4 \
  | while read -r url; do
    curl -s "$url" \
      --header "anthropic-version: 2023-06-01" \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      | sed 's/}{/}\n{/g' \
      | while IFS= read -r line
    do
      result_type=$(echo "$line" | sed -n 's/.*"result":[[:space:]]*{[[:space:]]*"type":[[:space:]]*"\([^"]*\)".*/\1/p')
      custom_id=$(echo "$line" | sed -n 's/.*"custom_id":[[:space:]]*"\([^"]*\)".*/\1/p')
      error_type=$(echo "$line" | sed -n 's/.*"error":[[:space:]]*{[[:space:]]*"type":[[:space:]]*"\([^"]*\)".*/\1/p')

      case "$result_type" in
        "succeeded")
          echo "Success! $custom_id"
          ;;
        "errored")
          if [ "$error_type" = "invalid_request_error" ]; then
            # Request body must be fixed before re-sending request
            echo "Validation error: $custom_id"
          else
            # Request can be retried directly
            echo "Server error: $custom_id"
          fi
          ;;
        "expired")
          echo "Expired: $line"
          ;;
      esac
    done
  done

```

```bash CLI
ant messages:batches results \
  --message-batch-id msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d \
  --transform '{custom_id,"type":result.type,"error":result.error.error.type}' \
  --format jsonl \
  | while IFS= read -r line; do
    custom_id=${line#*'"custom_id":"'}; custom_id=${custom_id%%'"'*}
    case "$line" in
      *'"type":"succeeded"'*)
        printf 'Success! %s\n' "$custom_id" ;;
      *'"type":"errored"'*)
        case "$line" in
          *'"error":"invalid_request_error"'*)
            printf 'Validation error %s\n' "$custom_id" ;;
          *)
            printf 'Server error %s\n' "$custom_id" ;;
        esac ;;
      *'"type":"expired"'*)
        printf 'Request expired %s\n' "$custom_id" ;;
    esac
  done
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Stream results file in memory-efficient chunks, processing one at a time
for result in client.messages.batches.results(
    "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d",
):
    match result.result.type:
        case "succeeded":
            print(f"Success! {result.custom_id}")
        case "errored":
            if result.result.error.error.type == "invalid_request_error":
                # Request body must be fixed before re-sending request
                print(f"Validation error {result.custom_id}")
            else:
                # Request can be retried directly
                print(f"Server error {result.custom_id}")
        case "expired":
            print(f"Request expired {result.custom_id}")
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

// Stream results file in memory-efficient chunks, processing one at a time
for await (const result of await anthropic.messages.batches.results(
  "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d"
)) {
  switch (result.result.type) {
    case "succeeded":
      console.log(`Success! ${result.custom_id}`);
      break;
    case "errored":
      if (result.result.error.type === "invalid_request_error") {
        // Request body must be fixed before re-sending request
        console.log(`Validation error: ${result.custom_id}`);
      } else {
        // Request can be retried directly
        console.log(`Server error: ${result.custom_id}`);
      }
      break;
    case "expired":
      console.log(`Request expired: ${result.custom_id}`);
      break;
  }
}
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages.Batches;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        await foreach (var result in client.Messages.Batches.ResultsStreaming("msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d"))
        {
            switch (result.Result.Type)
            {
                case "succeeded":
                    Console.WriteLine($"Success! {result.CustomID}");
                    break;
                case "errored":
                    if (result.Result.Error?.Type == "invalid_request")
                    {
                        Console.WriteLine($"Validation error: {result.CustomID}");
                    }
                    else
                    {
                        Console.WriteLine($"Server error: {result.CustomID}");
                    }
                    break;
                case "expired":
                    Console.WriteLine($"Request expired: {result.CustomID}");
                    break;
            }
        }
    }
}
```

```go Go nocheck hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	stream := client.Messages.Batches.ResultsStreaming(context.TODO(), "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d")

	for stream.Next() {
		result := stream.Current()

		switch variant := result.Result.AsAny().(type) {
		case anthropic.MessageBatchSucceededResult:
			fmt.Printf("Success! %s\n", result.CustomID)
		case anthropic.MessageBatchErroredResult:
			fmt.Printf("Error: %s - %s\n", result.CustomID, variant.Error.Error.Message)
		case anthropic.MessageBatchExpiredResult:
			fmt.Printf("Request expired: %s\n", result.CustomID)
		}
	}

	if err := stream.Err(); err != nil {
		log.Fatal(err)
	}
}
```

```java Java nocheck hidelines={1..2,6..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.http.StreamResponse;
import com.anthropic.models.messages.batches.BatchResultsParams;
import com.anthropic.models.messages.batches.MessageBatchIndividualResponse;

public class BatchResultsExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Stream results file in memory-efficient chunks, processing one at a time
    try (
      StreamResponse<MessageBatchIndividualResponse> streamResponse = client
        .messages()
        .batches()
        .resultsStreaming(
          BatchResultsParams.builder()
            .messageBatchId("msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d")
            .build()
        )
    ) {
      streamResponse
        .stream()
        .forEach(result -> {
          if (result.result().isSucceeded()) {
            System.out.println("Success! " + result.customId());
          } else if (result.result().isErrored()) {
            if (result.result().asErrored().error().error().isInvalidRequestError()) {
              // Request body must be fixed before re-sending request
              System.out.println("Validation error: " + result.customId());
            } else {
              // Request can be retried directly
              System.out.println("Server error: " + result.customId());
            }
          } else if (result.result().isExpired()) {
            System.out.println("Request expired: " + result.customId());
          }
        });
    }
  }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

foreach ($client->messages->batches->resultsStream(messageBatchID: 'msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d') as $result) {
    switch ($result->result->type) {
        case "succeeded":
            echo "Success! {$result->customID}\n";
            break;
        case "errored":
            if ($result->result->error->error->type === "invalid_request_error") {
                echo "Validation error: {$result->customID}\n";
            } else {
                echo "Server error: {$result->customID}\n";
            }
            break;
        case "expired":
            echo "Request expired: {$result->customID}\n";
            break;
    }
}
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

client.messages.batches.results_streaming("msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d").each do |result|
  case result.result.type
  when :succeeded
    puts "Success! #{result.custom_id}"
  when :errored
    if result.result.error.type == :invalid_request
      puts "Validation error: #{result.custom_id}"
    else
      puts "Server error: #{result.custom_id}"
    end
  when :expired
    puts "Request expired: #{result.custom_id}"
  end
end
```

</CodeGroup>

Hasil berada dalam format `.jsonl`, di mana setiap baris adalah objek JSON yang valid yang mewakili hasil dari satu permintaan dalam Message Batch. Untuk setiap hasil yang di-stream, Anda dapat melakukan sesuatu yang berbeda tergantung pada `custom_id` dan jenis hasilnya. Berikut adalah contoh set hasil:

```jsonl .jsonl file
{"custom_id":"my-second-request","result":{"type":"succeeded","message":{"id":"msg_014VwiXbi91y3JMjcpyGBHX5","type":"message","role":"assistant","model":"claude-opus-4-6","content":[{"type":"text","text":"Hello again! It's nice to see you. How can I assist you today? Is there anything specific you'd like to chat about or any questions you have?"}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":11,"output_tokens":36}}}}
{"custom_id":"my-first-request","result":{"type":"succeeded","message":{"id":"msg_01FqfsLoHwgeFbguDgpz48m7","type":"message","role":"assistant","model":"claude-opus-4-6","content":[{"type":"text","text":"Hello! How can I assist you today? Feel free to ask me any questions or let me know if there's anything you'd like to chat about."}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":10,"output_tokens":34}}}}
```

Jika hasil Anda memiliki kesalahan, `result.error` akan diatur ke [bentuk kesalahan](/docs/id/api/errors#error-shapes) standar.

<Tip>
  **Hasil batch mungkin tidak sesuai urutan input**

Hasil batch dapat dikembalikan dalam urutan apa pun, dan mungkin tidak sesuai dengan urutan permintaan saat batch dibuat. Dalam contoh di atas, hasil untuk permintaan batch kedua dikembalikan sebelum yang pertama. Untuk mencocokkan hasil dengan permintaan yang sesuai dengan benar, selalu gunakan bidang `custom_id`.
</Tip>

### Membatalkan Message Batch

Anda dapat membatalkan Message Batch yang sedang diproses menggunakan [endpoint pembatalan](/docs/id/api/canceling-message-batches). Segera setelah pembatalan, `processing_status` batch akan menjadi `canceling`. Anda dapat menggunakan teknik polling yang sama seperti yang dijelaskan di atas untuk menunggu sampai pembatalan selesai. Batch yang dibatalkan berakhir dengan status `ended` dan mungkin berisi hasil parsial untuk permintaan yang diproses sebelum pembatalan.

<CodeGroup>
```bash Shell hidelines={2..15}
#!/bin/sh
MESSAGE_BATCH_ID=$(curl -s https://api.anthropic.com/v1/messages/batches \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "requests": [{
      "custom_id": "test-1",
      "params": {
        "model": "claude-opus-4-6",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "Hi"}]
      }
    }]
  }' | jq -r '.id')
curl --request POST https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID/cancel \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01"
```

```bash CLI hidelines={2..13}
#!/bin/bash
MESSAGE_BATCH_ID=$(ant messages:batches create \
  --transform id --format yaml <<'YAML'
requests:
  - custom_id: test-1
    params:
      model: claude-opus-4-6
      max_tokens: 100
      messages:
        - role: user
          content: Hi
YAML
)
ant messages:batches cancel --message-batch-id "$MESSAGE_BATCH_ID"
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

MESSAGE_BATCH_ID = "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d"

message_batch = client.messages.batches.cancel(
    MESSAGE_BATCH_ID,
)
print(message_batch)
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const messageBatch = await anthropic.messages.batches.cancel(MESSAGE_BATCH_ID);
console.log(messageBatch);
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages.Batches;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var messageBatch = await client.Messages.Batches.Cancel(MESSAGE_BATCH_ID);
        Console.WriteLine(messageBatch);
    }
}
```

```go Go nocheck hidelines={1..12,-1}
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()
	messageBatchID := os.Getenv("MESSAGE_BATCH_ID")

	messageBatch, err := client.Messages.Batches.Cancel(context.TODO(), messageBatchID)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(messageBatch)
}
```

```java Java nocheck hidelines={1..2,4..7,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.batches.*;

public class BatchCancelExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageBatch messageBatch = client
      .messages()
      .batches()
      .cancel("msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d");
    System.out.println(messageBatch);
  }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$messageBatch = $client->messages->batches->cancel(
    messageBatchID: 'msgbatch_example_id',
);
echo $messageBatch;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message_batch_id = ENV.fetch("MESSAGE_BATCH_ID")
message_batch = client.messages.batches.cancel(message_batch_id)
puts message_batch
```

</CodeGroup>

Respons akan menunjukkan batch dalam status `canceling`:

```json Output
{
  "id": "msgbatch_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message_batch",
  "processing_status": "canceling",
  "request_counts": {
    "processing": 2,
    "succeeded": 0,
    "errored": 0,
    "canceled": 0,
    "expired": 0
  },
  "ended_at": null,
  "created_at": "2024-09-24T18:37:24.100435Z",
  "expires_at": "2024-09-25T18:37:24.100435Z",
  "cancel_initiated_at": "2024-09-24T18:39:03.114875Z",
  "results_url": null
}
```

### Menggunakan prompt caching dengan Message Batches

Message Batches API mendukung prompt caching, memungkinkan Anda untuk berpotensi mengurangi biaya dan waktu pemrosesan untuk permintaan batch. Diskon harga dari prompt caching dan Message Batches dapat ditumpuk, memberikan penghematan biaya yang lebih besar ketika kedua fitur digunakan bersama. Namun, karena permintaan batch diproses secara asinkron dan bersamaan, cache hits disediakan dengan basis best-effort. Pengguna biasanya mengalami tingkat cache hit berkisar dari 30% hingga 98%, tergantung pada pola lalu lintas mereka.

Untuk memaksimalkan kemungkinan cache hits dalam permintaan batch Anda:

1. Sertakan blok `cache_control` yang identik di setiap permintaan Message dalam batch Anda
2. Pertahankan aliran permintaan yang stabil untuk mencegah entri cache kedaluwarsa setelah masa hidup 5 menit mereka
3. Struktur permintaan Anda untuk berbagi sebanyak mungkin konten yang di-cache

Contoh implementasi prompt caching dalam batch:

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages/batches \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "requests": [
        {
            "custom_id": "my-first-request",
            "params": {
                "model": "claude-opus-4-6",
                "max_tokens": 1024,
                "system": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                    },
                    {
                        "type": "text",
                        "text": "<the entire contents of Pride and Prejudice>",
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                "messages": [
                    {"role": "user", "content": "Analyze the major themes in Pride and Prejudice."}
                ]
            }
        },
        {
            "custom_id": "my-second-request",
            "params": {
                "model": "claude-opus-4-6",
                "max_tokens": 1024,
                "system": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                    },
                    {
                        "type": "text",
                        "text": "<the entire contents of Pride and Prejudice>",
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                "messages": [
                    {"role": "user", "content": "Write a summary of Pride and Prejudice."}
                ]
            }
        }
    ]
}'
```

```bash CLI
ant messages:batches create <<'YAML'
requests:
  - custom_id: my-first-request
    params:
      model: claude-opus-4-6
      max_tokens: 1024
      system:
        - type: text
          text: >
            You are an AI assistant tasked with analyzing literary works. Your
            goal is to provide insightful commentary on themes, characters, and
            writing style.
        - type: text
          text: "<the entire contents of Pride and Prejudice>"
          cache_control:
            type: ephemeral
      messages:
        - role: user
          content: Analyze the major themes in Pride and Prejudice.
  - custom_id: my-second-request
    params:
      model: claude-opus-4-6
      max_tokens: 1024
      system:
        - type: text
          text: >
            You are an AI assistant tasked with analyzing literary works. Your
            goal is to provide insightful commentary on themes, characters, and
            writing style.
        - type: text
          text: "<the entire contents of Pride and Prejudice>"
          cache_control:
            type: ephemeral
      messages:
        - role: user
          content: Write a summary of Pride and Prejudice.
YAML
```

```python Python hidelines={1}
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

client = anthropic.Anthropic()

message_batch = client.messages.batches.create(
    requests=[
        Request(
            custom_id="my-first-request",
            params=MessageCreateParamsNonStreaming(
                model="claude-opus-4-6",
                max_tokens=1024,
                system=[
                    {
                        "type": "text",
                        "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
                    },
                    {
                        "type": "text",
                        "text": "<the entire contents of Pride and Prejudice>",
                        "cache_control": {"type": "ephemeral"},
                    },
                ],
                messages=[
                    {
                        "role": "user",
                        "content": "Analyze the major themes in Pride and Prejudice.",
                    }
                ],
            ),
        ),
        Request(
            custom_id="my-second-request",
            params=MessageCreateParamsNonStreaming(
                model="claude-opus-4-6",
                max_tokens=1024,
                system=[
                    {
                        "type": "text",
                        "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
                    },
                    {
                        "type": "text",
                        "text": "<the entire contents of Pride and Prejudice>",
                        "cache_control": {"type": "ephemeral"},
                    },
                ],
                messages=[
                    {
                        "role": "user",
                        "content": "Write a summary of Pride and Prejudice.",
                    }
                ],
            ),
        ),
    ]
)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const messageBatch = await anthropic.messages.batches.create({
  requests: [
    {
      custom_id: "my-first-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 1024,
        system: [
          {
            type: "text",
            text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
          },
          {
            type: "text",
            text: "<the entire contents of Pride and Prejudice>",
            cache_control: { type: "ephemeral" }
          }
        ],
        messages: [
          { role: "user", content: "Analyze the major themes in Pride and Prejudice." }
        ]
      }
    },
    {
      custom_id: "my-second-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 1024,
        system: [
          {
            type: "text",
            text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
          },
          {
            type: "text",
            text: "<the entire contents of Pride and Prejudice>",
            cache_control: { type: "ephemeral" }
          }
        ],
        messages: [
          { role: "user", content: "Write a summary of Pride and Prejudice." }
        ]
      }
    }
  ]
});
```

```csharp C#
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;
using Anthropic.Models.Messages.Batches;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new()
        {
            ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
        };

        var messageBatch = await client.Messages.Batches.Create(new BatchCreateParams
        {
            Requests =
            [
                new()
                {
                    CustomID = "my-first-request",
                    Params = new()
                    {
                        Model = Model.ClaudeOpus4_6,
                        MaxTokens = 1024,
                        System = new List<TextBlockParam>
                        {
                            new()
                            {
                                Text = "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                            },
                            new()
                            {
                                Text = "<the entire contents of Pride and Prejudice>",
                                CacheControl = new()
                            }
                        },
                        Messages =
                        [
                            new() { Role = Role.User, Content = "Analyze the major themes in Pride and Prejudice." }
                        ]
                    }
                },
                new()
                {
                    CustomID = "my-second-request",
                    Params = new()
                    {
                        Model = Model.ClaudeOpus4_6,
                        MaxTokens = 1024,
                        System = new List<TextBlockParam>
                        {
                            new()
                            {
                                Text = "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                            },
                            new()
                            {
                                Text = "<the entire contents of Pride and Prejudice>",
                                CacheControl = new()
                            }
                        },
                        Messages =
                        [
                            new() { Role = Role.User, Content = "Write a summary of Pride and Prejudice." }
                        ]
                    }
                }
            ]
        });
    }
}
```

```go Go hidelines={1..10,-1}
package main

import (
	"context"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	messageBatch, err := client.Messages.Batches.New(context.TODO(), anthropic.MessageBatchNewParams{
		Requests: []anthropic.MessageBatchNewParamsRequest{
			{
				CustomID: "my-first-request",
				Params: anthropic.MessageBatchNewParamsRequestParams{
					Model:     anthropic.ModelClaudeOpus4_6,
					MaxTokens: 1024,
					System: []anthropic.TextBlockParam{
						{
							Text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
						},
						{
							Text:         "<the entire contents of Pride and Prejudice>",
							CacheControl: anthropic.NewCacheControlEphemeralParam(),
						},
					},
					Messages: []anthropic.MessageParam{
						anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the major themes in Pride and Prejudice.")),
					},
				},
			},
			{
				CustomID: "my-second-request",
				Params: anthropic.MessageBatchNewParamsRequestParams{
					Model:     anthropic.ModelClaudeOpus4_6,
					MaxTokens: 1024,
					System: []anthropic.TextBlockParam{
						{
							Text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
						},
						{
							Text:         "<the entire contents of Pride and Prejudice>",
							CacheControl: anthropic.NewCacheControlEphemeralParam(),
						},
					},
					Messages: []anthropic.MessageParam{
						anthropic.NewUserMessage(anthropic.NewTextBlock("Write a summary of Pride and Prejudice.")),
					},
				},
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("%+v\n", messageBatch)
}
```

```java Java hidelines={1..2,4..5,7..11,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import com.anthropic.models.messages.batches.*;
import java.util.List;

public class BatchExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    BatchCreateParams createParams = BatchCreateParams.builder()
      .addRequest(
        BatchCreateParams.Request.builder()
          .customId("my-first-request")
          .params(
            BatchCreateParams.Request.Params.builder()
              .model(Model.CLAUDE_OPUS_4_6)
              .maxTokens(1024)
              .systemOfTextBlockParams(
                List.of(
                  TextBlockParam.builder()
                    .text(
                      "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                    )
                    .build(),
                  TextBlockParam.builder()
                    .text("<the entire contents of Pride and Prejudice>")
                    .cacheControl(CacheControlEphemeral.builder().build())
                    .build()
                )
              )
              .addUserMessage("Analyze the major themes in Pride and Prejudice.")
              .build()
          )
          .build()
      )
      .addRequest(
        BatchCreateParams.Request.builder()
          .customId("my-second-request")
          .params(
            BatchCreateParams.Request.Params.builder()
              .model(Model.CLAUDE_OPUS_4_6)
              .maxTokens(1024)
              .systemOfTextBlockParams(
                List.of(
                  TextBlockParam.builder()
                    .text(
                      "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                    )
                    .build(),
                  TextBlockParam.builder()
                    .text("<the entire contents of Pride and Prejudice>")
                    .cacheControl(CacheControlEphemeral.builder().build())
                    .build()
                )
              )
              .addUserMessage("Write a summary of Pride and Prejudice.")
              .build()
          )
          .build()
      )
      .build();

    MessageBatch messageBatch = client.messages().batches().create(createParams);
  }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$messageBatch = $client->messages->batches->create(
    requests: [
        [
            'custom_id' => 'my-first-request',
            'params' => [
                'model' => 'claude-opus-4-6',
                'max_tokens' => 1024,
                'system' => [
                    [
                        'type' => 'text',
                        'text' => 'You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n'
                    ],
                    [
                        'type' => 'text',
                        'text' => '<the entire contents of Pride and Prejudice>',
                        'cache_control' => ['type' => 'ephemeral']
                    ]
                ],
                'messages' => [
                    ['role' => 'user', 'content' => 'Analyze the major themes in Pride and Prejudice.']
                ]
            ]
        ],
        [
            'custom_id' => 'my-second-request',
            'params' => [
                'model' => 'claude-opus-4-6',
                'max_tokens' => 1024,
                'system' => [
                    [
                        'type' => 'text',
                        'text' => 'You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n'
                    ],
                    [
                        'type' => 'text',
                        'text' => '<the entire contents of Pride and Prejudice>',
                        'cache_control' => ['type' => 'ephemeral']
                    ]
                ],
                'messages' => [
                    ['role' => 'user', 'content' => 'Write a summary of Pride and Prejudice.']
                ]
            ]
        ]
    ],
);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message_batch = client.messages.batches.create(
  requests: [
    {
      custom_id: "my-first-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 1024,
        system: [
          {
            type: "text",
            text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
          },
          {
            type: "text",
            text: "<the entire contents of Pride and Prejudice>",
            cache_control: { type: "ephemeral" }
          }
        ],
        messages: [
          { role: "user", content: "Analyze the major themes in Pride and Prejudice." }
        ]
      }
    },
    {
      custom_id: "my-second-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 1024,
        system: [
          {
            type: "text",
            text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
          },
          {
            type: "text",
            text: "<the entire contents of Pride and Prejudice>",
            cache_control: { type: "ephemeral" }
          }
        ],
        messages: [
          { role: "user", content: "Write a summary of Pride and Prejudice." }
        ]
      }
    }
  ]
)
```

</CodeGroup>

Dalam contoh ini, kedua permintaan dalam batch mencakup pesan sistem yang identik dan teks lengkap Pride and Prejudice yang ditandai dengan `cache_control` untuk meningkatkan kemungkinan cache hits.

### Extended output (beta)

Header beta `output-300k-2026-03-24` menaikkan batas `max_tokens` menjadi 300.000 untuk permintaan batch menggunakan Claude Opus 4.6 atau Claude Sonnet 4.6. Sertakan header untuk menghasilkan output jauh lebih panjang dari batas standar (64k hingga 128k tergantung model) dalam satu putaran.

<Note>
Extended output tersedia hanya pada Message Batches API, bukan Messages API sinkron. Ini didukung pada Claude API dan tidak tersedia di Amazon Bedrock, Vertex AI, atau Microsoft Foundry.
</Note>

Gunakan extended output untuk generasi bentuk panjang seperti draf panjang buku dan dokumentasi teknis, ekstraksi data terstruktur yang komprehensif, scaffold pembuatan kode besar, dan rantai penalaran panjang.

Generasi token 300k tunggal dapat memakan waktu lebih dari satu jam untuk diselesaikan, jadi rencanakan pengiriman batch Anda dengan jendela pemrosesan 24 jam dalam pikiran. Harga batch standar (50% dari harga API standar) berlaku.

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages/batches \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: output-300k-2026-03-24" \
     --header "content-type: application/json" \
     --data \
'{
    "requests": [
        {
            "custom_id": "long-form-request",
            "params": {
                "model": "claude-opus-4-6",
                "max_tokens": 300000,
                "messages": [
                    {"role": "user", "content": "Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices."}
                ]
            }
        }
    ]
}'
```

```bash CLI
ant beta:messages:batches create --beta output-300k-2026-03-24 <<'YAML'
requests:
  - custom_id: long-form-request
    params:
      model: claude-opus-4-6
      max_tokens: 300000
      messages:
        - role: user
          content: >-
            Write a comprehensive technical guide to building distributed
            systems, covering architecture patterns, consistency models,
            fault tolerance, and operational best practices.
YAML
```

```python Python hidelines={1}
import anthropic
from anthropic.types.beta.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.beta.messages.batch_create_params import Request

client = anthropic.Anthropic()

message_batch = client.beta.messages.batches.create(
    betas=["output-300k-2026-03-24"],
    requests=[
        Request(
            custom_id="long-form-request",
            params=MessageCreateParamsNonStreaming(
                model="claude-opus-4-6",
                max_tokens=300_000,
                messages=[
                    {
                        "role": "user",
                        "content": "Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices.",
                    }
                ],
            ),
        ),
    ],
)

print(message_batch)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const messageBatch = await anthropic.beta.messages.batches.create({
  betas: ["output-300k-2026-03-24"],
  requests: [
    {
      custom_id: "long-form-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 300000,
        messages: [
          {
            role: "user",
            content:
              "Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices."
          }
        ]
      }
    }
  ]
});

console.log(messageBatch);
```

```csharp C#
using Anthropic;
using Anthropic.Models.Beta.Messages;
using Anthropic.Models.Beta.Messages.Batches;

AnthropicClient client = new();

var batch = await client.Beta.Messages.Batches.Create(new BatchCreateParams
{
    Betas = ["output-300k-2026-03-24"],
    Requests =
    [
        new()
        {
            CustomID = "long-form-request",
            Params = new()
            {
                Model = "claude-opus-4-6",
                MaxTokens = 300_000,
                Messages =
                [
                    new() { Role = Role.User, Content = "Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices." }
                ]
            }
        }
    ]
});

Console.WriteLine(batch);
```

```go Go hidelines={1..10,-1}
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	batch, err := client.Beta.Messages.Batches.New(context.Background(),
		anthropic.BetaMessageBatchNewParams{
			Betas: []anthropic.AnthropicBeta{"output-300k-2026-03-24"},
			Requests: []anthropic.BetaMessageBatchNewParamsRequest{
				{
					CustomID: "long-form-request",
					Params: anthropic.BetaMessageBatchNewParamsRequestParams{
						Model:     anthropic.ModelClaudeOpus4_6,
						MaxTokens: 300_000,
						Messages: []anthropic.BetaMessageParam{
							anthropic.NewBetaUserMessage(
								anthropic.NewBetaTextBlock("Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices."),
							),
						},
					},
				},
			},
		})
	if err != nil {
		panic(err)
	}

	fmt.Println(batch.ID)
}
```

```java Java hidelines={1..3,5..6,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Model;
import com.anthropic.models.beta.messages.batches.*;

void main() {
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  BatchCreateParams params = BatchCreateParams.builder()
    .addBeta("output-300k-2026-03-24")
    .addRequest(
      BatchCreateParams.Request.builder()
        .customId("long-form-request")
        .params(
          BatchCreateParams.Request.Params.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(300_000L)
            .addUserMessage("Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices.")
            .build()
        )
        .build()
    )
    .build();

  BetaMessageBatch messageBatch = client.beta().messages().batches().create(params);

  IO.println(messageBatch);
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$batch = $client->beta->messages->batches->create(
    betas: ['output-300k-2026-03-24'],
    requests: [
        [
            'custom_id' => 'long-form-request',
            'params' => [
                'model' => 'claude-opus-4-6',
                'max_tokens' => 300_000,
                'messages' => [
                    ['role' => 'user', 'content' => 'Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices.']
                ]
            ]
        ]
    ],
);

print_r($batch);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

batch = client.beta.messages.batches.create(
  betas: ["output-300k-2026-03-24"],
  requests: [
    {
      custom_id: "long-form-request",
      params: {
        model: "claude-opus-4-6",
        max_tokens: 300_000,
        messages: [
          { role: "user", content: "Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices." }
        ]
      }
    }
  ]
)

puts batch
```

</CodeGroup>

### Praktik terbaik untuk batching yang efektif

Untuk mendapatkan hasil maksimal dari Batches API:

- Pantau status pemrosesan batch secara teratur dan implementasikan logika retry yang sesuai untuk permintaan yang gagal.
- Gunakan nilai `custom_id` yang bermakna untuk dengan mudah mencocokkan hasil dengan permintaan, karena urutan tidak dijamin.
- Pertimbangkan untuk memecah dataset yang sangat besar menjadi beberapa batch untuk manajemen yang lebih baik.
- Dry run bentuk permintaan tunggal dengan Messages API untuk menghindari kesalahan validasi.

### Pemecahan masalah untuk masalah umum

Jika mengalami perilaku yang tidak terduga:

- Verifikasi bahwa ukuran permintaan batch total tidak melebihi 256 MB. Jika ukuran permintaan terlalu besar, Anda mungkin mendapatkan kesalahan `request_too_large` 413.
- Periksa bahwa Anda menggunakan [model yang didukung](#supported-models) untuk semua permintaan dalam batch.
- Pastikan setiap permintaan dalam batch memiliki `custom_id` yang unik.
- Pastikan bahwa kurang dari 29 hari telah berlalu sejak waktu batch `created_at` (bukan `ended_at` pemrosesan). Jika lebih dari 29 hari telah berlalu, hasil tidak akan lagi dapat dilihat.
- Konfirmasi bahwa batch belum dibatalkan.

Perhatikan bahwa kegagalan satu permintaan dalam batch tidak mempengaruhi pemrosesan permintaan lain.

---
## Penyimpanan batch dan privasi

- **Isolasi Workspace**: Batch diisolasi dalam Workspace tempat mereka dibuat. Mereka hanya dapat diakses oleh kunci API yang terkait dengan Workspace itu, atau pengguna dengan izin untuk melihat batch Workspace di Console.

- **Ketersediaan hasil**: Hasil batch tersedia selama 29 hari setelah batch dibuat, memberikan waktu yang cukup untuk pengambilan dan pemrosesan.

---
## Retensi data

Pemrosesan batch menyimpan data permintaan dan respons hingga 29 hari setelah pembuatan batch. Anda dapat menghapus batch pesan kapan saja setelah pemrosesan menggunakan endpoint `DELETE /v1/messages/batches/{batch_id}`. Untuk menghapus batch yang sedang berlangsung, batalkan terlebih dahulu. Pemrosesan asinkron memerlukan penyimpanan sisi server dari input dan output hingga penyelesaian batch dan pengambilan hasil.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/build-with-claude/api-and-data-retention).

## FAQ

  <section title="Berapa lama waktu yang diperlukan untuk batch diproses?">

    Batch dapat memakan waktu hingga 24 jam untuk diproses, tetapi banyak yang selesai lebih cepat. Waktu pemrosesan aktual tergantung pada ukuran batch, permintaan saat ini, dan volume permintaan Anda. Dimungkinkan untuk batch kedaluwarsa dan tidak selesai dalam 24 jam.
  
</section>

  <section title="Apakah Batches API tersedia untuk semua model?">

    Lihat [di atas](#supported-models) untuk daftar model yang didukung.
  
</section>

  <section title="Bisakah saya menggunakan Message Batches API dengan fitur API lainnya?">

    Ya, Message Batches API mendukung semua fitur yang tersedia di Messages API, termasuk fitur beta. Namun, streaming tidak didukung untuk permintaan batch.
  
</section>

  <section title="Bagaimana Message Batches API mempengaruhi harga?">

    Message Batches API menawarkan diskon 50% pada semua penggunaan dibandingkan dengan harga API standar. Ini berlaku untuk token input, token output, dan token khusus apa pun. Untuk informasi lebih lanjut tentang harga, kunjungi [halaman harga](https://claude.com/pricing#anthropic-api).
  
</section>

  <section title="Bisakah saya memperbarui batch setelah dikirimkan?">

    Tidak, setelah batch dikirimkan, batch tidak dapat dimodifikasi. Jika Anda perlu membuat perubahan, Anda harus membatalkan batch saat ini dan mengirimkan yang baru. Perhatikan bahwa pembatalan mungkin tidak langsung berlaku.
  
</section>

  <section title="Apakah ada batas laju Message Batches API dan apakah mereka berinteraksi dengan batas laju Messages API?">

    Message Batches API memiliki batas laju berbasis permintaan HTTP selain batas pada jumlah permintaan yang memerlukan pemrosesan. Lihat [batas laju Message Batches API](/docs/id/api/rate-limits#message-batches-api). Penggunaan Batches API tidak mempengaruhi batas laju di Messages API.
  
</section>

  <section title="Bagaimana cara menangani kesalahan dalam permintaan batch saya?">

    Ketika Anda mengambil hasil, setiap permintaan akan memiliki bidang `result` yang menunjukkan apakah itu `succeeded`, `errored`, `canceled`, atau `expired`. Untuk hasil `errored`, informasi kesalahan tambahan akan disediakan. Lihat objek respons kesalahan di [referensi API](/docs/id/api/creating-message-batches).
  
</section>

  <section title="Bagaimana Message Batches API menangani privasi dan pemisahan data?">

    Message Batches API dirancang dengan langkah-langkah privasi dan pemisahan data yang kuat:

    1. Batch dan hasilnya diisolasi dalam Workspace tempat mereka dibuat. Ini berarti mereka hanya dapat diakses oleh kunci API dari Workspace yang sama.
    2. Setiap permintaan dalam batch diproses secara independen, tanpa kebocoran data antara permintaan.
    3. Hasil hanya tersedia untuk waktu terbatas (29 hari), dan mengikuti [kebijakan retensi data](https://support.claude.com/en/articles/7996866-how-long-do-you-store-personal-data) Anthropic.
    4. Mengunduh hasil batch di Console dapat dinonaktifkan pada tingkat organisasi atau per-workspace.
  
</section>

  <section title="Bisakah saya menggunakan prompt caching di Message Batches API?">

    Ya, dimungkinkan untuk menggunakan prompt caching dengan Message Batches API. Namun, karena permintaan batch asinkron dapat diproses secara bersamaan dan dalam urutan apa pun, cache hits disediakan dengan basis best-effort.
  
</section>