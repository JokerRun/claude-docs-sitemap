---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/memory
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: e451fa552452354ca908a78fd92d739fd5c5e3d2d2a7ff7535d3884dcedc5260
---

# Menggunakan memori agen

Berikan agen Anda memori persisten yang bertahan di seluruh sesi menggunakan memory store.

---

Setiap sesi Managed Agents dimulai dengan konteks baru secara default. Ketika sesi berakhir, semua state yang dibangun agen akan hilang. Memory store memungkinkan agen membawa informasi di seluruh sesi: preferensi pengguna, konvensi proyek, kesalahan sebelumnya, dan konteks domain.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

<Note>
  Jangan menggabungkan `agent-memory-2026-07-22` dengan `managed-agents-2026-04-01` pada permintaan memory store: mengirim keduanya akan mengembalikan error `400`. Jika kode Anda menetapkan header beta secara eksplisit, ganti `managed-agents-2026-04-01` dengan `agent-memory-2026-07-22` pada panggilan memory store alih-alih menambahkan nilai kedua. Endpoint sesi, termasuk melampirkan memory store ke sesi, tetap menggunakan `managed-agents-2026-04-01`.

  Pada 22 Juli 2026, header `managed-agents-2026-04-01` akan mengadopsi perilaku daftar yang sama pada `GET /v1/memory_stores/{memory_store_id}/memories`; mengirim `agent-memory-2026-07-22` membuat Anda memilih perilaku tersebut sekarang. Kursor halaman dari permintaan yang dibuat tanpa header tersebut tidak valid dengannya, jadi mulai ulang dari halaman pertama.
</Note>

## Ikhtisar

**Memory store** adalah kumpulan dokumen teks dengan cakupan workspace yang dioptimalkan untuk Claude. Ketika Anda melampirkan store ke sebuah sesi, store tersebut dipasang (mount) sebagai direktori di dalam sandbox sesi. Agen membaca dan menulisnya dengan alat file yang sama yang digunakan untuk sisa filesystem, dan catatan yang menjelaskan setiap mount secara otomatis ditambahkan ke prompt sistem, memberi tahu agen di mana harus mencari. [Toolset agen](/docs/id/managed-agents/tools) diperlukan untuk interaksi ini; pastikan untuk mengaktifkannya selama [pembuatan agen](/docs/id/managed-agents/agent-setup).

Setiap **memori** dalam sebuah store dialamatkan dengan path dan dapat dibaca serta diedit langsung melalui API atau Console, memungkinkan penyetelan, impor, dan ekspor.

Setiap perubahan pada memori membuat **versi memori** yang tidak dapat diubah (immutable), memberi Anda jejak audit dan pemulihan point-in-time untuk semua yang ditulis agen.

## Membuat memory store

Berikan store sebuah `name` dan `description`. Deskripsi tersebut diteruskan ke agen, memberi tahu apa isi store tersebut.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  store=$(curl -s https://api.anthropic.com/v1/memory_stores \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    -d '{"name": "User Preferences", "description": "Per-user preferences and project context."}')
  store_id=$(jq -r '.id' <<< "$store")
  echo "$store_id"  # memstore_01Hx...
  ```

  ```bash CLI
  store_id=$(ant beta:memory-stores create \
    --name "User Preferences" \
    --description "Per-user preferences and project context." \
    --transform id --raw-output)
  ```

  ```python Python
  store = client.beta.memory_stores.create(
      name="User Preferences",
      description="Per-user preferences and project context.",
  )
  print(store.id)  # memstore_01Hx...
  ```

  ```typescript TypeScript
  const store = await client.beta.memoryStores.create({
    name: "User Preferences",
    description: "Per-user preferences and project context."
  });
  console.log(store.id); // memstore_01Hx...
  ```

  ```csharp C#
  var store = await client.Beta.MemoryStores.Create(new()
  {
      Name = "User Preferences",
      Description = "Per-user preferences and project context.",
  });
  Console.WriteLine(store.ID);  // memstore_01Hx...
  ```

  ```go Go
  store, err := client.Beta.MemoryStores.New(ctx, anthropic.BetaMemoryStoreNewParams{
  	Name:        "User Preferences",
  	Description: anthropic.String("Per-user preferences and project context."),
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(store.ID) // memstore_01Hx...
  ```

  ```java Java
  var store = client.beta().memoryStores().create(
      MemoryStoreCreateParams.builder()
          .name("User Preferences")
          .description("Per-user preferences and project context.")
          .build()
  );
  IO.println(store.id());  // memstore_01Hx...
  ```

  ```php PHP
  use Anthropic\Client;

  $client = new Client();

  $store = $client->beta->memoryStores->create(
      name: 'User Preferences',
      description: 'Per-user preferences and project context.',
  );
  echo "{$store->id}\n"; // memstore_01Hx...
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  store = client.beta.memory_stores.create(
    name: "User Preferences",
    description: "Per-user preferences and project context."
  )
  puts store.id # memstore_01Hx...
  ```
</CodeGroup>

`id` memory store (`memstore_...`) adalah yang Anda teruskan saat melampirkan store ke sebuah sesi.

### Mengisinya dengan konten (opsional)

Muat store terlebih dahulu dengan materi referensi sebelum agen apa pun berjalan:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memories" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    -d '{"path": "/formatting_standards.md", "content": "All reports use GAAP formatting. Dates are ISO-8601..."}' > /dev/null
  ```

  ```bash CLI
  ant beta:memory-stores:memories create \
    --memory-store-id "$store_id" \
    --path "/formatting_standards.md" \
    --content "All reports use GAAP formatting. Dates are ISO-8601..." \
    > /dev/null
  ```

  ```python Python
  client.beta.memory_stores.memories.create(
      store.id,
      path="/formatting_standards.md",
      content="All reports use GAAP formatting. Dates are ISO-8601...",
  )
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.memories.create(store.id, {
    path: "/formatting_standards.md",
    content: "All reports use GAAP formatting. Dates are ISO-8601..."
  });
  ```

  ```csharp C#
  await client.Beta.MemoryStores.Memories.Create(store.ID, new()
  {
      Path = "/formatting_standards.md",
      Content = "All reports use GAAP formatting. Dates are ISO-8601...",
  });
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.Memories.New(ctx, store.ID, anthropic.BetaMemoryStoreMemoryNewParams{
  	Path:    "/formatting_standards.md",
  	Content: anthropic.String("All reports use GAAP formatting. Dates are ISO-8601..."),
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().memories().create(
      store.id(),
      MemoryCreateParams.builder()
          .path("/formatting_standards.md")
          .content("All reports use GAAP formatting. Dates are ISO-8601...")
          .build()
  );
  ```

  ```php PHP
  $client->beta->memoryStores->memories->create(
      $store->id,
      path: '/formatting_standards.md',
      content: 'All reports use GAAP formatting. Dates are ISO-8601...',
  );
  ```

  ```ruby Ruby
  client.beta.memory_stores.memories.create(
    store.id,
    path: "/formatting_standards.md",
    content: "All reports use GAAP formatting. Dates are ISO-8601..."
  )
  ```
</CodeGroup>

<Tip>
  Memori individual dalam store dibatasi hingga 100 kB (\~25k token). Sebuah store menampung maksimum 2.000 memori. Susun memori sebagai banyak file kecil yang terfokus, bukan beberapa file besar.
</Tip>

## Melampirkan memory store ke sesi

Memory store dilampirkan dalam array `resources[]` sesi saat sesi dibuat. Tidak seperti sumber daya file dan repositori, memory store hanya dapat dilampirkan pada saat pembuatan sesi; menambahkan atau menghapusnya dari sesi yang sedang berjalan tidak didukung.

Secara opsional sertakan `instructions` untuk memberikan panduan khusus sesi tentang bagaimana agen harus menggunakan store ini. Ini ditampilkan kepada agen bersama dengan `name` dan `description` store, dan dibatasi hingga 4.096 karakter.

Anda juga dapat mengonfigurasi `access`. Nilai defaultnya adalah `read_write` (ditampilkan secara eksplisit dalam contoh berikut), tetapi `read_only` juga didukung.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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
      {
        "type": "memory_store",
        "memory_store_id": "$store_id",
        "access": "read_write",
        "instructions": "User preferences and project context. Check before starting any task."
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  ant beta:sessions create <<YAML
  agent: $agent_id
  environment_id: $environment_id
  resources:
    - type: memory_store
      memory_store_id: $store_id
      access: read_write
      instructions: User preferences and project context. Check before starting any task.
  YAML
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      resources=[
          {
              "type": "memory_store",
              "memory_store_id": store.id,
              "access": "read_write",
              "instructions": "User preferences and project context. Check before starting any task.",
          }
      ],
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "memory_store",
        memory_store_id: store.id,
        access: "read_write",
        instructions: "User preferences and project context. Check before starting any task."
      }
    ]
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Resources =
      [
          new BetaManagedAgentsMemoryStoreResourceParam
          {
              Type = "memory_store",
              MemoryStoreID = store.ID,
              Access = "read_write",
              Instructions = "User preferences and project context. Check before starting any task.",
          },
      ],
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  	Resources: []anthropic.BetaSessionNewParamsResourceUnion{{
  		OfMemoryStore: &anthropic.BetaManagedAgentsMemoryStoreResourceParam{
  			Type:          anthropic.BetaManagedAgentsMemoryStoreResourceParamTypeMemoryStore,
  			MemoryStoreID: store.ID,
  			Access:        anthropic.BetaManagedAgentsMemoryStoreResourceParamAccessReadWrite,
  			Instructions:  anthropic.String("User preferences and project context. Check before starting any task."),
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(
      SessionCreateParams.builder()
          .agent(agent.id())
          .environmentId(environment.id())
          .addResource(
              BetaManagedAgentsMemoryStoreResourceParam.builder()
                  .type(BetaManagedAgentsMemoryStoreResourceParam.Type.MEMORY_STORE)
                  .memoryStoreId(store.id())
                  .access(BetaManagedAgentsMemoryStoreResourceParam.Access.READ_WRITE)
                  .instructions("User preferences and project context. Check before starting any task.")
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      resources: [
          [
              'type' => 'memory_store',
              'memory_store_id' => $store->id,
              'access' => 'read_write',
              'instructions' => 'User preferences and project context. Check before starting any task.',
          ],
      ],
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "memory_store",
        memory_store_id: store.id,
        access: "read_write",
        instructions: "User preferences and project context. Check before starting any task."
      }
    ]
  )
  ```
</CodeGroup>

<Warning>
  Memory store dilampirkan dengan akses `read_write` secara default. Jika agen memproses input yang tidak tepercaya (prompt yang diberikan pengguna, konten web yang diambil, atau output alat pihak ketiga), prompt injection yang berhasil dapat menulis konten berbahaya ke dalam store. Sesi berikutnya kemudian membaca konten tersebut sebagai memori tepercaya. Gunakan `read_only` untuk materi referensi, pencarian bersama, dan store apa pun yang tidak perlu dimodifikasi oleh agen.
</Warning>

Maksimum **8 memory store** didukung per sesi. Lampirkan beberapa store ketika bagian memori yang berbeda memiliki pemilik atau aturan akses yang berbeda. Alasan umum:

* **Materi referensi bersama:** satu store read-only yang dilampirkan ke banyak sesi (standar, konvensi, pengetahuan domain), dipisahkan dari store read-write milik masing-masing sesi.
* **Pemetaan ke struktur produk Anda:** satu store per pengguna akhir, per tim, atau per proyek, sambil berbagi satu konfigurasi agen.
* **Siklus hidup yang berbeda:** store yang bertahan lebih lama dari satu sesi mana pun, atau yang ingin Anda arsipkan dengan jadwalnya sendiri.

### Bagaimana agen mengakses memori

Setiap store yang dilampirkan dipasang di dalam sandbox sesi sebagai direktori di bawah `/mnt/memory/`. Nama direktori adalah nama tampilan store yang disanitasi menjadi slug yang aman untuk filesystem (huruf kecil; rangkaian karakter non-alfanumerik menjadi satu tanda hubung), jadi store bernama "Demo Memory" dipasang di `/mnt/memory/demo-memory/`. Path yang tepat dikembalikan dalam field `mount_path` pada sumber daya memory-store sesi; baca dari sana alih-alih membangunnya sendiri. Agen membaca dan menulis store dengan [toolset agen](/docs/id/managed-agents/tools) standar. Penulisan di bawah mount path dipersistenkan kembali ke store dan tetap sinkron di seluruh sesi yang membagikannya; penulisan ke path lain di bawah `/mnt/memory/` masuk ke scratch lokal container dan hilang ketika sesi berakhir. Deskripsi singkat dari setiap mount (nama tampilan, mount path, mode akses, `description` store, dan `instructions` apa pun) secara otomatis ditambahkan ke prompt sistem.

`access` diberlakukan di tingkat filesystem: mount `read_only` menolak penulisan, sementara penulisan ke mount `read_write` menghasilkan [versi memori](#audit-memory-changes) yang diatribusikan ke sesi tersebut.

Pembacaan dan penulisan agen muncul di [event stream](/docs/id/managed-agents/events-and-streaming) sebagai event `agent.tool_use` dan `agent.tool_result` biasa untuk alat mana pun yang menyentuh mount tersebut.

## Melihat dan mengedit memori

Memory store dapat dikelola langsung melalui API. Gunakan ini untuk membangun alur kerja peninjauan, memperbaiki memori yang buruk, atau mengisi store sebelum sesi apa pun berjalan.

### Mendaftar memori

Daftarkan memori dalam sebuah store. Hasil dikembalikan dalam urutan stabil yang ditentukan server.

* `path_prefix` membatasi daftar ke satu direktori. Harus diakhiri dengan `/` dan mencocokkan segmen path utuh, jadi `path_prefix=/notes/` mengembalikan `/notes/todo.md` tetapi tidak `/notes-archive/todo.md`.
* `depth` mengontrol seberapa dalam daftar berjalan di bawah `path_prefix`: hilangkan (atau berikan `0`) untuk mendaftar seluruh subtree, atau berikan `1` untuk mendaftar hanya anak langsung. Nilai lain mengembalikan error `400`.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memories?path_prefix=/" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" | jq -r '.data[] | "\(.type)  \(.path)"'
  ```

  ```bash CLI
  ant beta:memory-stores:memories list \
    --memory-store-id "$store_id" \
    --path-prefix "/"
  ```

  ```python Python
  page = client.beta.memory_stores.memories.list(
      store.id,
      path_prefix="/",
  )
  for item in page.data:
      print(item.type, item.path)
  ```

  ```typescript TypeScript
  const page = await client.beta.memoryStores.memories.list(store.id, {
    path_prefix: "/"
  });
  for (const item of page.data) {
    console.log(item.type, item.path);
  }
  ```

  ```csharp C#
  var page = await client.Beta.MemoryStores.Memories.List(store.ID, new()
  {
      PathPrefix = "/",
  });
  await foreach (var item in page.Paginate())
  {
      var line = item.Match(m => $"memory  {m.Path}", p => $"memory_prefix  {p.Path}");
      Console.WriteLine(line);
  }
  ```

  ```go Go
  page, err := client.Beta.MemoryStores.Memories.List(ctx, store.ID, anthropic.BetaMemoryStoreMemoryListParams{
  	PathPrefix: anthropic.String("/"),
  })
  if err != nil {
  	panic(err)
  }
  for _, item := range page.Data {
  	fmt.Println(item.Type, item.Path)
  }
  ```

  ```java Java
  var page = client.beta().memoryStores().memories().list(
      store.id(),
      MemoryListParams.builder()
          .pathPrefix("/")
          .build()
  );
  for (var item : page.data()) {
      item.memory().ifPresent(m -> IO.println("memory  " + m.path()));
      item.memoryPrefix().ifPresent(p -> IO.println("memory_prefix  " + p.path()));
  }
  ```

  ```php PHP
  $page = $client->beta->memoryStores->memories->list(
      $store->id,
      pathPrefix: '/',
  );
  foreach ($page->data as $item) {
      echo "{$item->type}  {$item->path}\n";
  }
  ```

  ```ruby Ruby
  page = client.beta.memory_stores.memories.list(
    store.id,
    path_prefix: "/"
  )
  page.data.each do |entry|
    puts "#{entry.type}  #{entry.path}"
  end
  ```
</CodeGroup>

Lihat [referensi List memories](/docs/id/api/beta/memory_stores/memories/list) untuk parameter lengkap dan skema respons.

### Membaca memori

Mengambil memori individual mengembalikan konten lengkap.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" | jq -r '.content'
  ```

  ```bash CLI
  ant beta:memory-stores:memories retrieve \
    --memory-store-id "$store_id" \
    --memory-id "$mem_id"
  ```

  ```python Python
  retrieved = client.beta.memory_stores.memories.retrieve(
      mem.id,
      memory_store_id=store.id,
  )
  print(retrieved.content)
  ```

  ```typescript TypeScript
  const retrieved = await client.beta.memoryStores.memories.retrieve(mem.id, {
    memory_store_id: store.id
  });
  console.log(retrieved.content);
  ```

  ```csharp C#
  var retrieved = await client.Beta.MemoryStores.Memories.Retrieve(mem.ID, new()
  {
      MemoryStoreID = store.ID,
  });
  Console.WriteLine(retrieved.Content);
  ```

  ```go Go
  retrieved, err := client.Beta.MemoryStores.Memories.Get(ctx, mem.ID, anthropic.BetaMemoryStoreMemoryGetParams{
  	MemoryStoreID: store.ID,
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(retrieved.Content)
  ```

  ```java Java
  var retrieved = client.beta().memoryStores().memories().retrieve(
      mem.id(),
      MemoryRetrieveParams.builder().memoryStoreId(store.id()).build()
  );
  IO.println(retrieved.content());
  ```

  ```php PHP
  $retrieved = $client->beta->memoryStores->memories->retrieve($mem->id, memoryStoreID: $store->id);
  echo "{$retrieved->content}\n";
  ```

  ```ruby Ruby
  retrieved = client.beta.memory_stores.memories.retrieve(
    mem.id,
    memory_store_id: store.id
  )
  puts retrieved.content
  ```
</CodeGroup>

Lihat [referensi Retrieve a memory](/docs/id/api/beta/memory_stores/memories/retrieve) untuk parameter lengkap dan skema respons.

### Membuat memori

`memories.create` membuat memori pada `path` tertentu. Create tidak menimpa; untuk mengubah memori yang sudah ada, gunakan [`memories.update`](#update-a-memory).

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  mem=$(curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memories" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    -d '{"path": "/preferences/formatting.md", "content": "Always use tabs, not spaces."}')
  mem_id=$(jq -r '.id' <<< "$mem")
  mem_sha=$(jq -r '.content_sha256' <<< "$mem")
  ```

  ```bash CLI
  mem=$(ant beta:memory-stores:memories create \
    --memory-store-id "$store_id" \
    --path "/preferences/formatting.md" \
    --content "Always use tabs, not spaces." \
    --format json)
  mem_id=$(jq -r '.id' <<< "$mem")
  mem_sha=$(jq -r '.content_sha256' <<< "$mem")
  ```

  ```python Python
  mem = client.beta.memory_stores.memories.create(
      store.id,
      path="/preferences/formatting.md",
      content="Always use tabs, not spaces.",
  )
  ```

  ```typescript TypeScript
  const mem = await client.beta.memoryStores.memories.create(store.id, {
    path: "/preferences/formatting.md",
    content: "Always use tabs, not spaces."
  });
  ```

  ```csharp C#
  var mem = await client.Beta.MemoryStores.Memories.Create(store.ID, new()
  {
      Path = "/preferences/formatting.md",
      Content = "Always use tabs, not spaces.",
  });
  ```

  ```go Go
  mem, err := client.Beta.MemoryStores.Memories.New(ctx, store.ID, anthropic.BetaMemoryStoreMemoryNewParams{
  	Path:    "/preferences/formatting.md",
  	Content: anthropic.String("Always use tabs, not spaces."),
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var mem = client.beta().memoryStores().memories().create(
      store.id(),
      MemoryCreateParams.builder()
          .path("/preferences/formatting.md")
          .content("Always use tabs, not spaces.")
          .build()
  );
  ```

  ```php PHP
  $mem = $client->beta->memoryStores->memories->create(
      $store->id,
      path: '/preferences/formatting.md',
      content: 'Always use tabs, not spaces.',
  );
  ```

  ```ruby Ruby
  mem = client.beta.memory_stores.memories.create(
    store.id,
    path: "/preferences/formatting.md",
    content: "Always use tabs, not spaces."
  )
  ```
</CodeGroup>

Lihat [referensi Create a memory](/docs/id/api/beta/memory_stores/memories/create) untuk parameter lengkap dan skema respons.

### Memperbarui memori

`memories.update` memodifikasi memori yang sudah ada berdasarkan ID. Anda dapat mengubah `content`, `path` (penggantian nama), atau keduanya. Contoh ini mengganti nama memori ke path arsip:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    -d '{"path": "/archive/2026_q1_formatting.md"}' > /dev/null
  ```

  ```bash CLI
  ant beta:memory-stores:memories update \
    --memory-store-id "$store_id" \
    --memory-id "$mem_id" \
    --path "/archive/2026_q1_formatting.md" \
    > /dev/null
  ```

  ```python Python
  client.beta.memory_stores.memories.update(
      mem.id,
      memory_store_id=store.id,
      path="/archive/2026_q1_formatting.md",
  )
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.memories.update(mem.id, {
    memory_store_id: store.id,
    path: "/archive/2026_q1_formatting.md"
  });
  ```

  ```csharp C#
  await client.Beta.MemoryStores.Memories.Update(mem.ID, new()
  {
      MemoryStoreID = store.ID,
      Path = "/archive/2026_q1_formatting.md",
  });
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.Memories.Update(ctx, mem.ID, anthropic.BetaMemoryStoreMemoryUpdateParams{
  	MemoryStoreID: store.ID,
  	Path:          anthropic.String("/archive/2026_q1_formatting.md"),
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().memories().update(
      mem.id(),
      MemoryUpdateParams.builder()
          .memoryStoreId(store.id())
          .path("/archive/2026_q1_formatting.md")
          .build()
  );
  ```

  ```php PHP
  $client->beta->memoryStores->memories->update(
      $mem->id,
      memoryStoreID: $store->id,
      path: '/archive/2026_q1_formatting.md',
  );
  ```

  ```ruby Ruby
  client.beta.memory_stores.memories.update(
    mem.id,
    memory_store_id: store.id,
    path: "/archive/2026_q1_formatting.md"
  )
  ```
</CodeGroup>

Lihat [referensi Update a memory](/docs/id/api/beta/memory_stores/memories/update) untuk parameter lengkap dan skema respons.

#### Pengeditan konten yang aman (optimistic concurrency)

Untuk menghindari menimpa penulisan yang bersamaan, berikan prasyarat `content_sha256`. Pembaruan hanya diterapkan jika hash konten yang tersimpan masih cocok dengan yang Anda baca; jika tidak cocok, baca ulang memori dan coba lagi terhadap state yang baru.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    --data @- > /dev/null <<EOF
  {
    "content": "CORRECTED: Always use 2-space indentation.",
    "precondition": {"type": "content_sha256", "content_sha256": "$mem_sha"}
  }
  EOF
  ```

  ```bash CLI
  ant beta:memory-stores:memories update \
    --memory-store-id "$store_id" \
    --memory-id "$mem_id" \
    --content "CORRECTED: Always use 2-space indentation." \
    --precondition "{type: content_sha256, content_sha256: $mem_sha}" \
    > /dev/null
  ```

  ```python Python
  client.beta.memory_stores.memories.update(
      memory_id=mem.id,
      memory_store_id=store.id,
      content="CORRECTED: Always use 2-space indentation.",
      precondition={"type": "content_sha256", "content_sha256": mem.content_sha256},
  )
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.memories.update(mem.id, {
    memory_store_id: store.id,
    content: "CORRECTED: Always use 2-space indentation.",
    precondition: { type: "content_sha256", content_sha256: mem.content_sha256 }
  });
  ```

  ```csharp C#
  await client.Beta.MemoryStores.Memories.Update(mem.ID, new()
  {
      MemoryStoreID = store.ID,
      Content = "CORRECTED: Always use 2-space indentation.",
      Precondition = new BetaManagedAgentsPrecondition
      {
          Type = "content_sha256",
          ContentSha256 = mem.ContentSha256,
      },
  });
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.Memories.Update(ctx, mem.ID, anthropic.BetaMemoryStoreMemoryUpdateParams{
  	MemoryStoreID: store.ID,
  	Content:       anthropic.String("CORRECTED: Always use 2-space indentation."),
  	Precondition: anthropic.BetaManagedAgentsPreconditionParam{
  		Type:          anthropic.BetaManagedAgentsPreconditionTypeContentSha256,
  		ContentSha256: anthropic.String(mem.ContentSha256),
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().memories().update(
      mem.id(),
      MemoryUpdateParams.builder()
          .memoryStoreId(store.id())
          .content("CORRECTED: Always use 2-space indentation.")
          .precondition(
              BetaManagedAgentsPrecondition.builder()
                  .type(BetaManagedAgentsPrecondition.Type.CONTENT_SHA256)
                  .contentSha256(mem.contentSha256())
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $client->beta->memoryStores->memories->update(
      $mem->id,
      memoryStoreID: $store->id,
      content: 'CORRECTED: Always use 2-space indentation.',
      precondition: ['type' => 'content_sha256', 'content_sha256' => $mem->contentSha256],
  );
  ```

  ```ruby Ruby
  client.beta.memory_stores.memories.update(
    mem.id,
    memory_store_id: store.id,
    content: "CORRECTED: Always use 2-space indentation.",
    precondition: {type: "content_sha256", content_sha256: mem.content_sha256}
  )
  ```
</CodeGroup>

### Menghapus memori

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s -X DELETE "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" > /dev/null
  ```

  ```bash CLI
  ant beta:memory-stores:memories delete \
    --memory-store-id "$store_id" \
    --memory-id "$mem_id" \
    > /dev/null
  ```

  ```python Python
  client.beta.memory_stores.memories.delete(
      mem.id,
      memory_store_id=store.id,
  )
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.memories.delete(mem.id, {
    memory_store_id: store.id
  });
  ```

  ```csharp C#
  await client.Beta.MemoryStores.Memories.Delete(mem.ID, new()
  {
      MemoryStoreID = store.ID,
  });
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.Memories.Delete(ctx, mem.ID, anthropic.BetaMemoryStoreMemoryDeleteParams{
  	MemoryStoreID: store.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().memories().delete(
      mem.id(),
      MemoryDeleteParams.builder().memoryStoreId(store.id()).build()
  );
  ```

  ```php PHP
  $client->beta->memoryStores->memories->delete($mem->id, memoryStoreID: $store->id);
  ```

  ```ruby Ruby
  client.beta.memory_stores.memories.delete(
    mem.id,
    memory_store_id: store.id
  )
  ```
</CodeGroup>

Lihat [referensi Delete a memory](/docs/id/api/beta/memory_stores/memories/delete) untuk parameter lengkap dan skema respons.

## Audit perubahan memori

Setiap mutasi pada memori membuat **versi memori** yang tidak dapat diubah (`memver_...`). Gunakan endpoint versi untuk mengaudit siapa mengubah apa dan kapan, untuk memeriksa atau memulihkan snapshot sebelumnya, dan untuk membersihkan konten sensitif dari riwayat dengan redact.

Versi dimiliki oleh store (bukan memori individual) dan tetap ada bahkan setelah memori itu sendiri dihapus, sehingga jejak audit tetap lengkap. Versi disimpan selama 30 hari; namun, versi terbaru selalu disimpan terlepas dari usianya, jadi memori yang jarang berubah mungkin mempertahankan riwayat lebih dari 30 hari. Panggilan `memories.retrieve` langsung selalu mengembalikan versi terbaru; endpoint versi memberi Anda riwayat yang disimpan.

Tidak ada endpoint pemulihan khusus; untuk melakukan rollback, ambil versi yang Anda inginkan dan tulis kembali `content`-nya dengan `memories.update` (atau `memories.create` jika memori induknya telah dihapus, karena versi bertahan lebih lama dari induknya).

Versi memori lama mungkin dihapus setelah 30 hari. Untuk mempertahankan riwayat memori lebih lama, ekspor versi melalui API.

### Mendaftar versi

Daftarkan riwayat versi untuk sebuah store, yang terbaru lebih dulu. Contoh ini memfilter ke riwayat satu memori:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  versions=$(curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memory_versions?memory_id=$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22")
  jq -r '.data[] | "\(.id): \(.operation)"' <<< "$versions"
  version_id=$(jq -r '.data[1].id' <<< "$versions")
  ```

  ```bash CLI
  versions=$(ant beta:memory-stores:memory-versions list \
    --memory-store-id "$store_id" \
    --memory-id "$mem_id" \
    --format json)
  jq -r '.data[] | "\(.id): \(.operation)"' <<< "$versions"
  version_id=$(jq -r '.data[1].id' <<< "$versions")
  ```

  ```python Python
  versions = client.beta.memory_stores.memory_versions.list(
      store.id,
      memory_id=mem.id,
  )
  for v in versions:
      print(f"{v.id}: {v.operation}")

  version_id = versions.data[1].id
  ```

  ```typescript TypeScript
  const versions = await client.beta.memoryStores.memoryVersions.list(store.id, {
    memory_id: mem.id
  });
  for await (const v of versions) {
    console.log(`${v.id}: ${v.operation}`);
  }

  const versionId = versions.data[1].id;
  ```

  ```csharp C#
  var versions = await client.Beta.MemoryStores.MemoryVersions.List(store.ID, new()
  {
      MemoryID = mem.ID,
  });
  var versionIds = new List<string>();
  await foreach (var v in versions.Paginate())
  {
      Console.WriteLine($"{v.ID}: {v.Operation.Raw()}");
      versionIds.Add(v.ID);
  }

  var versionId = versionIds[1];
  ```

  ```go Go
  versions := client.Beta.MemoryStores.MemoryVersions.ListAutoPaging(ctx, store.ID, anthropic.BetaMemoryStoreMemoryVersionListParams{
  	MemoryID: anthropic.String(mem.ID),
  })
  for versions.Next() {
  	v := versions.Current()
  	fmt.Printf("%s: %s\n", v.ID, v.Operation)
  }
  if err := versions.Err(); err != nil {
  	panic(err)
  }

  vpage, err := client.Beta.MemoryStores.MemoryVersions.List(ctx, store.ID, anthropic.BetaMemoryStoreMemoryVersionListParams{
  	MemoryID: anthropic.String(mem.ID),
  })
  if err != nil {
  	panic(err)
  }
  versionID := vpage.Data[1].ID
  ```

  ```java Java
  var versions = client.beta().memoryStores().memoryVersions().list(
      store.id(),
      MemoryVersionListParams.builder().memoryId(mem.id()).build()
  );
  for (var v : versions.autoPager()) {
      IO.println(v.id() + ": " + v.operation());
  }

  var versionId = versions.data().get(1).id();
  ```

  ```php PHP
  $versions = $client->beta->memoryStores->memoryVersions->list(
      $store->id,
      memoryID: $mem->id,
  );
  foreach ($versions->pagingEachItem() as $v) {
      echo "{$v->id}: {$v->operation}\n";
  }

  $versionId = $versions->data[1]->id;
  ```

  ```ruby Ruby
  versions = client.beta.memory_stores.memory_versions.list(
    store.id,
    memory_id: mem.id
  )
  versions.auto_paging_each do |v|
    puts "#{v.id}: #{v.operation}"
  end

  version_id = versions.data[1].id
  ```
</CodeGroup>

Lihat [referensi List memory versions](/docs/id/api/beta/memory_stores/memory_versions/list) untuk parameter lengkap dan skema respons.

### Mengambil versi

Mengambil versi individual mengembalikan field yang sama dengan respons daftar ditambah isi `content` lengkap.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memory_versions/$version_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22"
  ```

  ```bash CLI
  ant beta:memory-stores:memory-versions retrieve \
    --memory-store-id "$store_id" \
    --memory-version-id "$version_id"
  ```

  ```python Python
  version = client.beta.memory_stores.memory_versions.retrieve(
      version_id,
      memory_store_id=store.id,
  )
  print(version.content)
  ```

  ```typescript TypeScript
  const version = await client.beta.memoryStores.memoryVersions.retrieve(versionId, {
    memory_store_id: store.id
  });
  console.log(version.content);
  ```

  ```csharp C#
  var version = await client.Beta.MemoryStores.MemoryVersions.Retrieve(versionId, new()
  {
      MemoryStoreID = store.ID,
  });
  Console.WriteLine(version.Content);
  ```

  ```go Go
  version, err := client.Beta.MemoryStores.MemoryVersions.Get(ctx, versionID, anthropic.BetaMemoryStoreMemoryVersionGetParams{
  	MemoryStoreID: store.ID,
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(version.Content)
  ```

  ```java Java
  var version = client.beta().memoryStores().memoryVersions().retrieve(
      versionId,
      MemoryVersionRetrieveParams.builder().memoryStoreId(store.id()).build()
  );
  IO.println(version.content());
  ```

  ```php PHP
  $version = $client->beta->memoryStores->memoryVersions->retrieve(
      $versionId,
      memoryStoreID: $store->id,
  );
  echo "{$version->content}\n";
  ```

  ```ruby Ruby
  version = client.beta.memory_stores.memory_versions.retrieve(
    version_id,
    memory_store_id: store.id
  )
  puts version.content
  ```
</CodeGroup>

Lihat [referensi Retrieve a memory version](/docs/id/api/beta/memory_stores/memory_versions/retrieve) untuk parameter lengkap dan skema respons.

### Meredaksi versi

Redact membersihkan konten dari versi historis sambil mempertahankan jejak audit (siapa melakukan apa, kapan). Gunakan untuk alur kerja kepatuhan seperti menghapus rahasia yang bocor, PII, atau permintaan penghapusan pengguna.

Versi yang merupakan head saat ini dari memori yang masih aktif tidak dapat diredaksi. Tulis versi baru terlebih dahulu (atau hapus memorinya), lalu redaksi versi yang lama.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/memory_versions/$version_id/redact" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    -d '{}'
  ```

  ```bash CLI
  ant beta:memory-stores:memory-versions redact \
    --memory-store-id "$store_id" \
    --memory-version-id "$version_id"
  ```

  ```python Python
  client.beta.memory_stores.memory_versions.redact(
      version_id,
      memory_store_id=store.id,
  )
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.memoryVersions.redact(versionId, {
    memory_store_id: store.id
  });
  ```

  ```csharp C#
  await client.Beta.MemoryStores.MemoryVersions.Redact(versionId, new()
  {
      MemoryStoreID = store.ID,
  });
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.MemoryVersions.Redact(ctx, versionID, anthropic.BetaMemoryStoreMemoryVersionRedactParams{
  	MemoryStoreID: store.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().memoryVersions().redact(
      versionId,
      MemoryVersionRedactParams.builder().memoryStoreId(store.id()).build()
  );
  ```

  ```php PHP
  $client->beta->memoryStores->memoryVersions->redact(
      $versionId,
      memoryStoreID: $store->id,
  );
  ```

  ```ruby Ruby
  client.beta.memory_stores.memory_versions.redact(
    version_id,
    memory_store_id: store.id
  )
  ```
</CodeGroup>

Lihat [referensi Redact a memory version](/docs/id/api/beta/memory_stores/memory_versions/redact) untuk parameter lengkap dan skema respons.

## Mengelola memory store

Selain [`create`](/docs/id/api/beta/memory_stores/create), memory store mendukung [`retrieve`](/docs/id/api/beta/memory_stores/retrieve), [`update`](/docs/id/api/beta/memory_stores/update), [`list`](/docs/id/api/beta/memory_stores/list), [`archive`](/docs/id/api/beta/memory_stores/archive), dan [`delete`](/docs/id/api/beta/memory_stores/delete).

### Mendaftar store

Daftarkan store dalam workspace. Store yang diarsipkan dikecualikan secara default; berikan `include_archived: true` untuk menyertakannya.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s "https://api.anthropic.com/v1/memory_stores?include_archived=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" | jq '.data[] | {id, name, archived_at}'
  ```

  ```bash CLI
  ant beta:memory-stores list --include-archived
  ```

  ```python Python
  for s in client.beta.memory_stores.list(include_archived=True):
      print(s.id, s.name, s.archived_at)
  ```

  ```typescript TypeScript
  for await (const s of client.beta.memoryStores.list({ include_archived: true })) {
    console.log(s.id, s.name, s.archived_at);
  }
  ```

  ```csharp C#
  var stores = await client.Beta.MemoryStores.List(new() { IncludeArchived = true });
  await foreach (var s in stores.Paginate())
  {
      Console.WriteLine($"{s.ID} {s.Name} {s.ArchivedAt}");
  }
  ```

  ```go Go
  stores := client.Beta.MemoryStores.ListAutoPaging(ctx, anthropic.BetaMemoryStoreListParams{
  	IncludeArchived: anthropic.Bool(true),
  })
  for stores.Next() {
  	s := stores.Current()
  	fmt.Println(s.ID, s.Name, s.ArchivedAt)
  }
  if err := stores.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  for (var s : client.beta().memoryStores().list(
      MemoryStoreListParams.builder().includeArchived(true).build()
  ).autoPager()) {
      IO.println(s.id() + " " + s.name() + " " + s.archivedAt());
  }
  ```

  ```php PHP
  foreach ($client->beta->memoryStores->list(includeArchived: true)->pagingEachItem() as $s) {
      echo "{$s->id} {$s->name} {$s->archivedAt}\n";
  }
  ```

  ```ruby Ruby
  client.beta.memory_stores.list(include_archived: true).auto_paging_each do |s|
    puts "#{s.id} #{s.name} #{s.archived_at}"
  end
  ```
</CodeGroup>

Lihat [referensi List memory stores](/docs/id/api/beta/memory_stores/list) untuk parameter lengkap dan skema respons.

### Mengarsipkan store

Pengarsipan membuat store menjadi read-only dan mencegahnya dilampirkan ke sesi baru. Pengarsipan bersifat satu arah; tidak ada unarchive.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" > /dev/null
  ```

  ```bash CLI
  ant beta:memory-stores archive --memory-store-id "$store_id"
  ```

  ```python Python
  client.beta.memory_stores.archive(store.id)
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.archive(store.id);
  ```

  ```csharp C#
  await client.Beta.MemoryStores.Archive(store.ID);
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.Archive(ctx, store.ID, anthropic.BetaMemoryStoreArchiveParams{})
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().archive(store.id());
  ```

  ```php PHP
  $client->beta->memoryStores->archive($store->id);
  ```

  ```ruby Ruby
  client.beta.memory_stores.archive(store.id)
  ```
</CodeGroup>

Lihat [referensi Archive a memory store](/docs/id/api/beta/memory_stores/archive) untuk parameter lengkap dan skema respons.

Untuk menghapus store secara permanen beserta semua memori dan versinya, gunakan [`memory_stores.delete`](/docs/id/api/beta/memory_stores/delete).

## Praktik terbaik untuk manajemen memori

Ketika sebuah store mencapai batas 2.000 memorinya, penulisan ke memori baru akan gagal: baik panggilan `memories.create` langsung maupun penulisan file agen ke path yang belum dipetakan. Memori yang sudah ada tetap dapat dibaca dan diedit. Praktik berikut membantu Anda tetap jauh di bawah batas dan pulih dengan baik jika Anda mencapainya.

* **Gunakan store yang terfokus.** Alih-alih satu store besar serbaguna, gunakan store yang lebih kecil dan dibuat untuk tujuan tertentu: satu per pengguna, satu untuk pengetahuan domain bersama, dan satu untuk konteks khusus proyek. Setiap store memiliki batas 2.000 memorinya sendiri, jadi menjaga store tetap terbatas cakupannya mengurangi kemungkinan salah satunya penuh.

* **Padatkan atau pangkas sebelum store penuh.** Hapus memori yang usang atau berlebihan dengan `memories.delete`. Anda juga dapat menjalankan [sesi dreaming](/docs/id/managed-agents/dreams), yang mengonsolidasikan konten yang terfragmentasi ke dalam store output baru yang terpisah alih-alih memodifikasi yang asli. Alihkan sesi Anda ke store output tersebut, lalu arsipkan atau hapus yang asli.

* **Lampirkan store baru ketika masuk akal.** Jika sebuah store telah tumbuh melampaui cakupan yang berguna, lampirkan yang baru untuk konten baru dan lampirkan yang asli dengan akses `read_only`. Agen dapat membaca dari keduanya sambil hanya menulis ke yang baru.

* **Batasi akses tulis jika sesuai.** Sesi yang hanya membaca materi referensi bersama tidak memerlukan `read_write`. Menjaga akses tulis terbatas pada sesi yang benar-benar menambahkan memori baru memudahkan pelacakan dari mana pertumbuhan berasal.
