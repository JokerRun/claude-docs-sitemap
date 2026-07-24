---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/dreams
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 25fe0885b417e6972463ae3b41b8a48c89bca3569d359a989cab511b7b63340b
---

# Dreams

Biarkan Claude merefleksikan sesi-sesi sebelumnya untuk mengkurasi memori agen dan memunculkan wawasan baru.

---

<Tip>
  Dreaming adalah fitur pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Tip>

Agen menulis ke [memory store](/docs/id/managed-agents/memory) mereka saat bekerja, tetapi penulisan ini bersifat lokal dan inkremental: selama banyak sesi, sebuah memory store mengakumulasi duplikat, kontradiksi, dan entri yang usang.

**Dreams** memungkinkan Claude membersihkan hal tersebut. Sebuah dream membaca memory store yang sudah ada bersama dengan transkrip sesi sebelumnya, lalu menghasilkan memory store baru yang telah direorganisasi: duplikat digabungkan, entri yang usang atau saling bertentangan diganti dengan nilai terbaru, dan wawasan baru dimunculkan.

Store input tidak pernah dimodifikasi, sehingga Anda dapat meninjau output dan membuangnya jika Anda tidak menyukai hasilnya.

<Note>
  Endpoint dream dibatasi oleh header beta `dreaming-2026-04-21`; header `managed-agents-2026-04-01` saja tidak memberikan akses ke dreams. Contoh endpoint dream di halaman ini mengirimkan kedua header; panggilan sesi dan memory-store hanya memerlukan `managed-agents-2026-04-01`. SDK mengatur ini secara otomatis.
</Note>

## Cara kerjanya

Sebuah **dream** adalah pekerjaan asinkron yang menerima:

* sebuah **memory store** yang sudah ada sebelumnya: store yang diverifikasi, dideduplikasi, dan direorganisasi oleh Claude, dan
* 1 hingga 100 **sesi:** transkrip sebelumnya yang ditelusuri Claude untuk menemukan pola dan wawasan yang akan dimasukkan ke dalam output.

Dream menghasilkan **memory store output** lain, terpisah dari input. ID store output muncul di `outputs[]` dream tidak lama setelah dream mulai `running`, setelah alur kerja mengkloning store input; dream yang `running` dapat secara singkat melaporkan `outputs[]` yang kosong.

## Membuat dream

<CodeGroup>
  ```bash curl
  dream=$(curl -s https://api.anthropic.com/v1/dreams \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21" \
    -H "content-type: application/json" \
    --data @- <<EOF
  {
    "inputs": [
      { "type": "memory_store", "memory_store_id": "$store_id" },
      { "type": "sessions", "session_ids": ["$session_a", "$session_b"] }
    ],
    "model": "claude-opus-4-8",
    "instructions": "Focus on coding-style preferences; ignore one-off debugging notes."
  }
  EOF
  )
  dream_id=$(jq -r '.id' <<< "$dream")
  echo "$dream_id"  # drm_01...
  ```

  ```bash CLI
  dream_id=$(ant beta:dreams create --transform id --raw-output <<YAML
  inputs:
    - type: memory_store
      memory_store_id: $store_id
    - type: sessions
      session_ids: [$session_a, $session_b]
  model: claude-opus-4-8
  instructions: Focus on coding-style preferences; ignore one-off debugging notes.
  YAML
  )
  ```

  ```python Python
  dream = client.beta.dreams.create(
      inputs=[
          {"type": "memory_store", "memory_store_id": store_id},
          {"type": "sessions", "session_ids": [session_a, session_b]},
      ],
      model="claude-opus-4-8",
      instructions="Focus on coding-style preferences; ignore one-off debugging notes.",
  )
  print(dream.id)  # drm_01...
  ```

  ```typescript TypeScript
  let dream = await client.beta.dreams.create({
    inputs: [
      { type: "memory_store", memory_store_id: storeId },
      { type: "sessions", session_ids: [sessionA, sessionB] },
    ],
    model: "claude-opus-4-8",
    instructions: "Focus on coding-style preferences; ignore one-off debugging notes.",
  });
  console.log(dream.id); // drm_01...
  ```

  ```csharp C#
  var dream = await client.Beta.Dreams.Create(new()
  {
      Inputs =
      [
          new BetaDreamMemoryStoreInput
          {
              Type = BetaDreamMemoryStoreInputType.MemoryStore,
              MemoryStoreID = storeID,
          },
          new BetaDreamSessionsInput
          {
              Type = BetaDreamSessionsInputType.Sessions,
              SessionIds = [sessionA, sessionB],
          },
      ],
      Model = "claude-opus-4-8",
      Instructions = "Focus on coding-style preferences; ignore one-off debugging notes.",
  });
  Console.WriteLine(dream.ID);  // drm_01...
  ```

  ```go Go
  dream, err := client.Beta.Dreams.New(ctx, anthropic.BetaDreamNewParams{
  	Inputs: []anthropic.BetaDreamInputUnionParam{
  		anthropic.BetaDreamInputParamOfMemoryStore(storeID),
  		anthropic.BetaDreamInputParamOfSessions([]string{sessionA, sessionB}),
  	},
  	Model: anthropic.BetaDreamModelParamsUnion{
  		OfString: anthropic.String("claude-opus-4-8"),
  	},
  	Instructions: anthropic.String("Focus on coding-style preferences; ignore one-off debugging notes."),
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(dream.ID) // drm_01...
  ```

  ```java Java
  var dream = client.beta().dreams().create(
      DreamCreateParams.builder()
          .addMemoryStoreInput(storeId)
          .addSessionsInput(List.of(sessionA, sessionB))
          .model("claude-opus-4-8")
          .instructions("Focus on coding-style preferences; ignore one-off debugging notes.")
          .build()
  );
  IO.println(dream.id());  // drm_01...
  ```

  ```php PHP
  $dream = $client->beta->dreams->create(
      inputs: [
          ['type' => 'memory_store', 'memory_store_id' => $storeId],
          ['type' => 'sessions', 'session_ids' => [$sessionA, $sessionB]],
      ],
      model: 'claude-opus-4-8',
      instructions: 'Focus on coding-style preferences; ignore one-off debugging notes.',
  );
  echo "{$dream->id}\n"; // drm_01...
  ```

  ```ruby Ruby
  dream = client.beta.dreams.create(
    inputs: [
      {type: "memory_store", memory_store_id: store_id},
      {type: "sessions", session_ids: [session_a, session_b]}
    ],
    model: "claude-opus-4-8",
    instructions: "Focus on coding-style preferences; ignore one-off debugging notes."
  )
  puts dream.id # drm_01...
  ```
</CodeGroup>

Input dreaming mencakup memory store yang sudah ada sebelumnya dan sebuah array sesi. Model yang dipilih menjalankan pipeline dreaming; selama pratinjau riset, `claude-fable-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-5`, dan `claude-sonnet-4-6` didukung. Anda dapat secara opsional meneruskan `instructions` untuk mengarahkan proses dreaming; lihat [Mengarahkan dengan instruksi](#steer-with-instructions).

Responsnya adalah resource `dream` lengkap dengan `status: "pending"`:

```json
{
  "type": "dream",
  "id": "drm_01AbCDefGhIjKlMnOpQrStUv",
  "status": "pending",
  "inputs": [
    { "type": "memory_store", "memory_store_id": "memstore_01Hx..." },
    { "type": "sessions", "session_ids": ["sesn_01...", "sesn_02..."] }
  ],
  "outputs": [],
  "model": { "id": "claude-opus-4-8" },
  "instructions": "Focus on coding-style preferences; ignore one-off debugging notes.",
  "session_id": null,
  "created_at": "2026-04-29T17:04:10Z",
  "ended_at": null,
  "archived_at": null,
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0
  },
  "error": null
}
```

<Tip>
  Jika Anda hanya memiliki transkrip sesi dan tidak memiliki store yang sudah ada, [buat memory store kosong](/docs/id/managed-agents/memory#create-a-memory-store) terlebih dahulu dan teruskan sebagai input `memory_store`.
</Tip>

### Mengarahkan dengan instruksi

Field opsional `instructions` mengarahkan apa yang disintesis oleh pipeline dreaming. Field ini diterapkan di seluruh pipeline: apa yang harus dibaca dengan cermat, apa yang harus digabungkan atau dibuang, dan bagaimana menyusun store output.

Gunakan `instructions` untuk panduan sintesis tingkat tinggi seperti area fokus ("fokus pada preferensi gaya penulisan kode"), konten yang harus dipertahankan tanpa perubahan, atau konvensi output yang ingin Anda terapkan di seluruh store. Pipeline adalah proses sintesis atas input, bukan editor yang diterapkan pada teks store, sehingga arahan imperatif yang menargetkan baris tertentu ("ubah kalimat X menjadi Y", "perbaiki hitungan di bagian Z") umumnya tidak menghasilkan perubahan. Untuk membuat pengeditan yang ditargetkan pada memori individual, gunakan [Memory Stores API](/docs/id/managed-agents/memory#view-and-edit-memories) langsung pada store output.

## Melacak kemajuan

Dreams berjalan secara asinkron dan biasanya memakan waktu beberapa menit hingga beberapa jam, tergantung pada jumlah transkrip input. Lakukan polling pada dream berdasarkan ID untuk memeriksa status:

<CodeGroup>
  ```bash curl
  while true; do
    dream=$(curl -s "https://api.anthropic.com/v1/dreams/$dream_id" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21")
    status=$(jq -r '.status' <<< "$dream")
    echo "status=$status input_tokens=$(jq -r '.usage.input_tokens' <<< "$dream")"
    [[ "$status" == "pending" || "$status" == "running" ]] || break
    sleep 10
  done
  ```

  ```bash CLI
  ant beta:dreams retrieve --dream-id "$dream_id"
  ```

  ```python Python
  while dream.status in ("pending", "running"):
      time.sleep(10)
      dream = client.beta.dreams.retrieve(dream.id)
      print(f"status={dream.status} input_tokens={dream.usage.input_tokens}")
  ```

  ```typescript TypeScript
  while (dream.status === "pending" || dream.status === "running") {
    await sleep(10_000);
    dream = await client.beta.dreams.retrieve(dream.id);
    console.log(`status=${dream.status} input_tokens=${dream.usage.input_tokens}`);
  }
  ```

  ```csharp C#
  while (dream.Status.Value() is BetaDreamStatus.Pending or BetaDreamStatus.Running)
  {
      await Task.Delay(TimeSpan.FromSeconds(10));
      dream = await client.Beta.Dreams.Retrieve(dream.ID);
      Console.WriteLine($"status={dream.Status.Raw()} input_tokens={dream.Usage.InputTokens}");
  }
  ```

  ```go Go
  for dream.Status == anthropic.BetaDreamStatusPending || dream.Status == anthropic.BetaDreamStatusRunning {
  	time.Sleep(10 * time.Second)
  	dream, err = client.Beta.Dreams.Get(ctx, dream.ID, anthropic.BetaDreamGetParams{})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("status=%s input_tokens=%d\n", dream.Status, dream.Usage.InputTokens)
  }
  ```

  ```java Java
  while (dream.status().equals(BetaDreamStatus.PENDING)
          || dream.status().equals(BetaDreamStatus.RUNNING)) {
      Thread.sleep(10_000);
      dream = client.beta().dreams().retrieve(dream.id());
      IO.println("status=" + dream.status() + " input_tokens=" + dream.usage().inputTokens());
  }
  ```

  ```php PHP
  while (in_array($dream->status, [BetaDreamStatus::PENDING->value, BetaDreamStatus::RUNNING->value], true)) {
      sleep(10);
      $dream = $client->beta->dreams->retrieve($dream->id);
      echo "status={$dream->status} input_tokens={$dream->usage->inputTokens}\n";
  }
  ```

  ```ruby Ruby
  while %i[pending running].include?(dream.status)
    sleep 10
    dream = client.beta.dreams.retrieve(dream.id)
    puts "status=#{dream.status} input_tokens=#{dream.usage.input_tokens}"
  end
  ```
</CodeGroup>

### Siklus hidup

| `status`    | Arti                                                                                                                                 |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `pending`   | Dream berhasil dibuat dan dimasukkan ke antrean.                                                                                     |
| `running`   | Pipeline sedang memproses. `usage` diperbarui seiring kemajuan pekerjaan.                                                            |
| `completed` | Selesai dengan sukses. Nilai `outputs[]` adalah memory store baru.                                                                   |
| `failed`    | Proses dreaming berakhir dengan error. Memory store output dibiarkan apa adanya dengan apa pun yang telah ditulis sebelum kegagalan. |
| `canceled`  | Proses dreaming dibatalkan. Memory store output dibiarkan apa adanya.                                                                |

### Mengamati pipeline berjalan

Setelah sebuah dream berstatus `running`, field `session_id`-nya menunjuk ke [sesi](/docs/id/managed-agents/sessions) yang mendasari yang menjalankan pipeline. Anda dapat melakukan streaming [event](/docs/id/managed-agents/events-and-streaming) sesi tersebut untuk mengamati apa yang dibaca dan ditulis oleh dream secara real time. Sesi tersebut diarsipkan (tidak dihapus) ketika dream mencapai status terminal, sehingga transkrip tetap tersedia setelahnya.

## Menggunakan output

Ketika `status` mencapai `completed`, entri `memory_store` di `outputs[]` mereferensikan store yang telah terisi penuh. Ini adalah memory store biasa di workspace Anda. Tinjau dengan [Memory Stores API](/docs/id/managed-agents/memory#view-and-edit-memories) atau di Console, lalu pilih salah satu:

* **Manfaatkan:** lampirkan ke sesi mendatang sebagai resource `memory_store` sebagai pengganti (atau bersama dengan) memory store input, atau
* **Buang:** [hapus memory store](/docs/id/api/beta/memory_stores/delete) atau [arsipkan memory store](/docs/id/api/beta/memory_stores/archive).

<CodeGroup>
  ```bash curl
  # Setelah dream berakhir, output memory_store menyimpan store yang dibangun ulang
  output_store_id=$(jq -r 'first(.outputs[] | select(.type == "memory_store")).memory_store_id' <<< "$dream")

  curl -s https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<EOF
  {
    "agent": "$agent_id",
    "environment_id": "$environment_id",
    "resources": [
      { "type": "memory_store", "memory_store_id": "$output_store_id" }
    ]
  }
  EOF
  ```

  ```bash CLI
  output_store_id=$(ant beta:dreams retrieve --dream-id "$dream_id" --format json |
    jq -r 'first(.outputs[] | select(.type == "memory_store")).memory_store_id')

  ant beta:sessions create <<YAML
  agent: $agent_id
  environment_id: $environment_id
  resources:
    - type: memory_store
      memory_store_id: $output_store_id
  YAML
  ```

  ```python Python
  # Setelah dream berakhir, output menyimpan penyimpanan memori yang dibangun ulang
  output_store_id = next(
      output.memory_store_id for output in dream.outputs if output.type == "memory_store"
  )

  session = client.beta.sessions.create(
      agent=agent_id,
      environment_id=environment_id,
      resources=[
          {"type": "memory_store", "memory_store_id": output_store_id},
      ],
  )
  ```

  ```typescript TypeScript
  // Setelah dream berakhir, output menyimpan penyimpanan memori yang dibangun ulang
  const output = dream.outputs.find((entry) => entry.type === "memory_store");
  const outputStoreId = output!.memory_store_id;

  await client.beta.sessions.create({
    agent: agentId,
    environment_id: environmentId,
    resources: [
      { type: "memory_store", memory_store_id: outputStoreId },
    ],
  });
  ```

  ```csharp C#
  var output = dream.Outputs.FirstOrDefault(entry => entry.Type == "memory_store");
  if (output is { MemoryStoreID: var outputStoreID })
  {
      await client.Beta.Sessions.Create(new()
      {
          Agent = agentID,
          EnvironmentID = environmentID,
          Resources =
          [
              new BetaManagedAgentsMemoryStoreResourceParam
              {
                  Type = BetaManagedAgentsMemoryStoreResourceParamType.MemoryStore,
                  MemoryStoreID = outputStoreID,
              },
          ],
      });
  }
  ```

  ```go Go
  for _, output := range dream.Outputs {
  	if output.Type != "memory_store" {
  		continue
  	}
  	outputStoreID := output.MemoryStoreID

  	session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  		Agent: anthropic.BetaSessionNewParamsAgentUnion{
  			OfString: anthropic.String(agentID),
  		},
  		EnvironmentID: environmentID,
  		Resources: []anthropic.BetaSessionNewParamsResourceUnion{{
  			OfMemoryStore: &anthropic.BetaManagedAgentsMemoryStoreResourceParam{
  				MemoryStoreID: outputStoreID,
  			},
  		}},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(session.ID)
  	break
  }
  ```

  ```java Java
  var output = dream.outputs().stream()
      .filter(entry -> entry.type().equals(BetaDreamOutput.Type.MEMORY_STORE))
      .findFirst();
  if (output.isPresent()) {
      var outputStoreId = output.get().memoryStoreId();

      var session = client.beta().sessions().create(
          SessionCreateParams.builder()
              .agent(agentId)
              .environmentId(environmentId)
              .addMemoryStoreResource(outputStoreId)
              .build()
      );
  }
  ```

  ```php PHP
  $matches = array_filter($dream->outputs, fn($output) => $output->type === 'memory_store');
  $output = $matches ? reset($matches) : null;
  if ($output !== null) {
      $session = $client->beta->sessions->create(
          agent: $agentId,
          environmentID: $environmentId,
          resources: [
              ['type' => 'memory_store', 'memory_store_id' => $output->memoryStoreID],
          ],
      );
  }
  ```

  ```ruby Ruby
  output = dream.outputs.find { it.type == :memory_store }
  if output
    client.beta.sessions.create(
      agent: agent_id,
      environment_id: environment_id,
      resources: [
        {type: "memory_store", memory_store_id: output.memory_store_id}
      ]
    )
  end
  ```
</CodeGroup>

Dream itu sendiri tidak pernah menghapus atau memodifikasi inputnya. Pada status `failed` atau `canceled`, store output tetap ada dengan konten parsial sehingga Anda dapat memeriksa apa yang dihasilkan sebelum berhenti; bersihkan melalui Memory Stores API jika Anda tidak membutuhkannya.

<Warning>
  Saat sebuah dream berstatus `pending` atau `running`, penjagaan 400 berlaku untuk pengarsipan dream itu sendiri, bukan store-nya. Mengarsipkan atau menghapus memory store *input* di tengah proses (atau menghapus sesi input) akan menyebabkan dream gagal dengan `input_memory_store_unavailable` atau `input_session_unavailable`.
</Warning>

## Membatalkan dream

Pembatalan memindahkan dream yang berstatus `pending` atau `running` ke `canceled` secara langsung. Membatalkan dream yang sudah berstatus `canceled` adalah no-op yang idempoten; membatalkan dream yang berstatus `completed` atau `failed` mengembalikan 400.

<Note>
  Setelah pembatalan, field `usage` dream mungkin terus diperbarui selama beberapa detik sementara pekerjaan yang sedang berlangsung berakhir. Lakukan polling pada dream hingga `usage` stabil jika Anda memerlukan hitungan akhir.
</Note>

<CodeGroup>
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/dreams/$dream_id/cancel" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21"
  ```

  ```bash CLI
  ant beta:dreams cancel --dream-id "$dream_id"
  ```

  ```python Python
  client.beta.dreams.cancel(dream.id)
  ```

  ```typescript TypeScript
  await client.beta.dreams.cancel(dream.id);
  ```

  ```csharp C#
  await client.Beta.Dreams.Cancel(dream.ID);
  ```

  ```go Go
  dream, err = client.Beta.Dreams.Cancel(ctx, dream.ID, anthropic.BetaDreamCancelParams{})
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().dreams().cancel(dream.id());
  ```

  ```php PHP
  $client->beta->dreams->cancel($dream->id);
  ```

  ```ruby Ruby
  client.beta.dreams.cancel(dream.id)
  ```
</CodeGroup>

## Mengarsipkan dream

Pengarsipan mengatur `archived_at` pada dream yang telah mencapai status terminal (`completed`, `failed`, atau `canceled`); `status` dibiarkan tidak berubah. Dream yang diarsipkan dikecualikan dari respons daftar default tetapi tetap dapat dibaca berdasarkan ID. Mengarsipkan dream yang sudah diarsipkan adalah no-op yang idempoten. Mengarsipkan dream yang berstatus `pending` atau `running` mengembalikan 400; batalkan terlebih dahulu. Tidak ada fitur unarchive.

<CodeGroup>
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/dreams/$dream_id/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21"
  ```

  ```bash CLI
  ant beta:dreams archive --dream-id "$dream_id"
  ```

  ```python Python
  client.beta.dreams.archive(dream.id)
  ```

  ```typescript TypeScript
  await client.beta.dreams.archive(dream.id);
  ```

  ```csharp C#
  await client.Beta.Dreams.Archive(dream.ID);
  ```

  ```go Go
  dream, err = client.Beta.Dreams.Archive(ctx, dream.ID, anthropic.BetaDreamArchiveParams{})
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().dreams().archive(dream.id());
  ```

  ```php PHP
  $client->beta->dreams->archive($dream->id);
  ```

  ```ruby Ruby
  client.beta.dreams.archive(dream.id)
  ```
</CodeGroup>

Mengarsipkan dream tidak menyentuh memory store output-nya; kelola itu secara terpisah melalui [Memory Stores API](/docs/id/managed-agents/memory#view-and-edit-memories).

## Menampilkan daftar dream

Mengembalikan semua dream yang tidak diarsipkan di workspace, yang terbaru terlebih dahulu. Gunakan `limit` (default 20, maksimum 100) dan kursor `page` untuk paginasi. Teruskan `include_archived=true` untuk menyertakan dream yang diarsipkan.

<CodeGroup>
  ```bash curl
  curl -s "https://api.anthropic.com/v1/dreams?limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21"
  ```

  ```bash CLI
  ant beta:dreams list --limit 20
  ```

  ```python Python
  for listed_dream in client.beta.dreams.list(limit=20):
      print(listed_dream.id, listed_dream.status)
  ```

  ```typescript TypeScript
  for await (const listedDream of client.beta.dreams.list({ limit: 20 })) {
    console.log(listedDream.id, listedDream.status);
  }
  ```

  ```csharp C#
  var page = await client.Beta.Dreams.List(new() { Limit = 20 });
  await foreach (var listed in page.Paginate())
  {
      Console.WriteLine($"{listed.ID} {listed.Status.Raw()}");
  }
  ```

  ```go Go
  dreams := client.Beta.Dreams.ListAutoPaging(ctx, anthropic.BetaDreamListParams{
  	Limit: anthropic.Int(20),
  })
  for dreams.Next() {
  	listed := dreams.Current()
  	fmt.Println(listed.ID, listed.Status)
  }
  if err := dreams.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  for (var listedDream : client.beta().dreams().list(
      DreamListParams.builder().limit(20).build()
  ).autoPager()) {
      IO.println(listedDream.id() + " " + listedDream.status());
  }
  ```

  ```php PHP
  foreach ($client->beta->dreams->list(limit: 20)->pagingEachItem() as $dream) {
      echo "{$dream->id} {$dream->status}\n";
  }
  ```

  ```ruby Ruby
  client.beta.dreams.list(limit: 20).auto_paging_each do
    puts "#{it.id} #{it.status}"
  end
  ```
</CodeGroup>

## Error

Berikut adalah daftar tidak lengkap dari kemungkinan error dreaming.

| `error.type`                      | Kapan                                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------------------- |
| `timeout`                         | Pipeline melebihi anggaran waktu eksekusinya.                                                   |
| `internal_error`                  | Kegagalan pipeline yang tidak terklasifikasi.                                                   |
| `memory_store_org_limit_exceeded` | Organisasi Anda mencapai batas memory-store saat pipeline sedang menyediakan penyimpanan kerja. |
| `input_memory_store_too_large`    | Memory store input melebihi batas ukuran pipeline.                                              |
| `input_memory_store_unavailable`  | Memory store input diarsipkan atau dihapus setelah dream dibuat.                                |
| `input_session_unavailable`       | Sebuah sesi input dihapus setelah dream dibuat.                                                 |

## Penagihan

Dreams ditagih dengan tarif token API standar untuk model yang Anda pilih; `usage` pada resource melaporkan total yang tepat. Biaya meningkat secara kurang lebih linear dengan jumlah dan panjang sesi input. Mulailah dengan batch sesi yang kecil dan tingkatkan setelah Anda puas dengan kualitas kurasinya.

## Batasan

| Batasan                | Nilai                                                                                          |
| ---------------------- | ---------------------------------------------------------------------------------------------- |
| Sesi per dream         | 100                                                                                            |
| Panjang `instructions` | 4.096 karakter                                                                                 |
| Model yang didukung    | `claude-fable-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-5`, `claude-sonnet-4-6` |

Batas laju default berlaku untuk pembuatan dream selama fitur ini dalam pratinjau riset. [Hubungi dukungan](https://support.claude.com) jika Anda memerlukan batas yang lebih tinggi.
