---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/memory
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 17862f1b7510463482d273b8c375bfd74f864c975ff4c245f9ccab8ba5acd9bb
---

# Menggunakan memori

Berikan agen Anda memori persisten yang bertahan di seluruh sesi menggunakan penyimpan memori.

---

<Tip>
Agent Memory adalah fitur Research Preview. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Tip>

Sesi API Managed Agents bersifat sementara secara default. Ketika sesi berakhir, apa pun yang dipelajari agen hilang. Penyimpan memori memungkinkan agen membawa pembelajaran di seluruh sesi: preferensi pengguna, konvensi proyek, kesalahan sebelumnya, dan konteks domain.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. Header beta tambahan diperlukan untuk fitur research preview. SDK menetapkan header beta ini secara otomatis.
</Note>

## Gambaran Umum
**Penyimpan memori** adalah koleksi dokumen teks yang dibatasi ruang kerja dan dioptimalkan untuk Claude. Ketika satu atau lebih penyimpan memori dilampirkan ke sesi, agen secara otomatis memeriksa penyimpan sebelum memulai tugas dan menulis pembelajaran yang tahan lama setelah selesai - tidak perlu prompting atau konfigurasi tambahan dari pihak Anda.

Setiap **memori** dalam penyimpan dapat diakses dan diedit langsung melalui API atau Console, memungkinkan penyetelan, impor, dan ekspor memori.

Setiap perubahan pada memori membuat **memory_version** yang tidak dapat diubah untuk mendukung audit dan rollback perubahan memori.

## Buat penyimpan memori

Berikan penyimpan nama `name` dan `description`. Deskripsi dilewatkan ke agen, memberi tahu apa yang berisi penyimpan.

<CodeGroup>
  ```bash curl
  store=$(curl -fsS https://api.anthropic.com/v1/memory_stores \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<EOF
  {
    "name": "User Preferences",
    "description": "Per-user preferences and project context."
  }
  EOF
  )
  store_id=$(jq -r '.id' <<< "$store")
  echo "$store_id"  # memstore_01Hx...
  ```
  ```bash CLI
  store_id=$(ant beta:memory-stores create \
    --name "User Preferences" \
    --description "Per-user preferences and project context." \
    --transform id --format yaml)
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
  $store = $client->beta->memoryStores->create(
      name: 'User Preferences',
      description: 'Per-user preferences and project context.',
  );
  echo "{$store->id}\n"; // memstore_01Hx...
  ```
  ```ruby Ruby
  store = client.beta.memory_stores.create(
    name: "User Preferences",
    description: "Per-user preferences and project context."
  )
  puts store.id # memstore_01Hx...
  ```
</CodeGroup>

`id` penyimpan memori (`memstore_...`) adalah apa yang Anda lewatkan saat melampirkan penyimpan ke sesi.

### Isi dengan konten (opsional)

Pra-muat penyimpan dengan materi referensi sebelum agen apa pun berjalan:

<CodeGroup>
  
  ```bash curl
  curl -fsS "https://api.anthropic.com/v1/memory_stores/$store_id/memories" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- > /dev/null <<EOF
  {
    "path": "/formatting_standards.md",
    "content": "All reports use GAAP formatting. Dates are ISO-8601..."
  }
  EOF
  ```
  
  ```bash CLI
  ant beta:memory-stores:memories write \
    --memory-store-id "$store_id" \
    --path "/formatting_standards.md" \
    --content "All reports use GAAP formatting. Dates are ISO-8601..." \
    > /dev/null
  ```
  ```python Python
  client.beta.memory_stores.memories.write(
      memory_store_id=store.id,
      path="/formatting_standards.md",
      content="All reports use GAAP formatting. Dates are ISO-8601...",
  )
  ```
  ```typescript TypeScript
  await client.beta.memoryStores.memories.write(store.id, {
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
  		Content: "All reports use GAAP formatting. Dates are ISO-8601...",
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
Memori individual dalam penyimpan dibatasi pada 100KB (~25K token). Struktur memori sebagai banyak file kecil yang terfokus, bukan beberapa file besar.
</Tip>

## Lampirkan memori ke sesi

Penyimpan memori dilampirkan dalam array `resources[]` sesi.

Secara opsional sertakan `prompt` jika Anda ingin memberikan instruksi khusus sesi kepada Claude tentang cara menggunakan penyimpan memori ini. Ini disediakan kepada Claude selain `name` dan `description` penyimpan memori, dan dibatasi pada 4.096 karakter.

Anda juga dapat mengonfigurasi `access`. Defaultnya adalah `read_write`, tetapi `read_only` juga didukung (ditampilkan secara eksplisit dalam contoh di bawah).

<CodeGroup>
  
  ```bash curl
  session=$(curl -fsS https://api.anthropic.com/v1/sessions \
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
        "prompt": "User preferences and project context. Check before starting any task."
      }
    ]
  }
  EOF
  )
  ```
  
  ```bash CLI
  ant beta:sessions create <<YAML
  agent: $agent_id
  environment_id: $environment_id
  resources:
    - type: memory_store
      memory_store_id: $store_id
      access: read_write
      prompt: User preferences and project context. Check before starting any task.
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
              "prompt": "User preferences and project context. Check before starting any task.",
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
        prompt: "User preferences and project context. Check before starting any task."
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
          new BetaManagedAgentsMemoryStoreResourceParams
          {
              Type = "memory_store",
              MemoryStoreID = store.ID,
              Access = "read_write",
              Prompt = "User preferences and project context. Check before starting any task.",
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
  			OfMemoryStore: &anthropic.BetaManagedAgentsMemoryStoreResourceParams{
  				MemoryStoreID: store.ID,
  				Access:        anthropic.BetaManagedAgentsMemoryStoreResourceParamsAccessReadWrite,
  				Prompt:        anthropic.String("User preferences and project context. Check before starting any task."),
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
                  BetaManagedAgentsMemoryStoreResourceParams.builder()
                      .memoryStoreId(store.id())
                      .access(BetaManagedAgentsMemoryStoreResourceParams.Access.READ_WRITE)
                      .prompt("User preferences and project context. Check before starting any task.")
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
              'prompt' => 'User preferences and project context. Check before starting any task.',
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
        prompt: "User preferences and project context. Check before starting any task."
      }
    ]
  )
  ```
</CodeGroup>

Maksimal **8 penyimpan memori** didukung per sesi. Lampirkan beberapa penyimpan ketika bagian berbeda dari memori memiliki pemilik atau aturan akses yang berbeda. Alasan umum:

- **Materi referensi bersama** - satu penyimpan read-only dilampirkan ke banyak sesi (standar, konvensi, pengetahuan domain), dipisahkan dari pembelajaran read-write sesi masing-masing.
- **Pemetaan ke struktur produk Anda** - satu penyimpan per pengguna akhir, per-tim, atau per-proyek, sambil berbagi konfigurasi agen tunggal.
- **Siklus hidup berbeda** - penyimpan yang bertahan lebih lama dari sesi apa pun, atau yang ingin Anda arsipkan sesuai jadwal Anda sendiri.

### Alat memori
Ketika penyimpan memori dilampirkan ke sesi, agen secara otomatis mendapatkan akses ke alat memori. Interaksi agen dengan penyimpan memori terdaftar sebagai acara `agent.tool_use` dalam [aliran acara](/docs/id/managed-agents/events-and-streaming).

| Alat | Deskripsi |
| --- | --- |
| `memory_list` | Daftar dokumen dalam penyimpan, secara opsional disaring berdasarkan awalan jalur. |
| `memory_search` | Pencarian teks lengkap di seluruh konten dokumen. |
| `memory_read` | Baca konten dokumen. |
| `memory_write` | Buat atau timpa dokumen di jalur. |
| `memory_edit` | Ubah dokumen yang ada. |
| `memory_delete` | Hapus dokumen. |

## Inspeksi dan perbaiki memori

Penyimpan memori dapat dikelola langsung melalui API. Gunakan ini untuk membangun alur kerja tinjauan, memperbaiki memori buruk, atau menyemai penyimpan sebelum sesi apa pun berjalan.

### Daftar memori
Daftar tidak mengembalikan konten memori, hanya metadata objek. Gunakan `path_prefix` untuk daftar yang dibatasi direktori (sertakan garis miring trailing: `/notes/` cocok dengan `/notes/a.md` tetapi bukan `/notes_backup/old.md`).

<CodeGroup>
  
  ```bash curl
  page=$(curl -fsS "https://api.anthropic.com/v1/memory_stores/$store_id/memories?path_prefix=/" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")
  jq -r '.data[] | "\(.path)  (\(.size_bytes) bytes, sha=\(.content_sha256[0:8]))"' <<< "$page"
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
  for memory in page.data:
      print(
          f"{memory.path}  ({memory.size_bytes} bytes, sha={memory.content_sha256[:8]})"
      )
  ```
  ```typescript TypeScript
  const page = await client.beta.memoryStores.memories.list(store.id, {
    path_prefix: "/"
  });
  for (const memory of page.data) {
    console.log(
      `${memory.path}  (${memory.size_bytes} bytes, sha=${memory.content_sha256.slice(0, 8)})`
    );
  }
  ```
  ```csharp C#
  var page = await client.Beta.MemoryStores.Memories.List(store.ID, new() { PathPrefix = "/" });
  foreach (var memory in page.Data)
  {
      Console.WriteLine($"{memory.Path}  ({memory.SizeBytes} bytes, sha={memory.ContentSha256[..8]})");
  }
  ```
  ```go Go
  	page, err := client.Beta.MemoryStores.Memories.List(ctx, store.ID, anthropic.BetaMemoryStoreMemoryListParams{
  		PathPrefix: anthropic.String("/"),
  	})
  	if err != nil {
  		panic(err)
  	}
  	for _, memory := range page.Data {
  		fmt.Printf("%s  (%d bytes, sha=%s)\n", memory.Path, memory.SizeBytes, memory.ContentSha256[:8])
  	}
  ```
  ```java Java
      var page = client.beta().memoryStores().memories().list(
          store.id(),
          MemoryListParams.builder().pathPrefix("/").build()
      );
      for (var memory : page.data()) {
          IO.println("%s  (%d bytes, sha=%s)".formatted(
              memory.path(), memory.sizeBytes(), memory.contentSha256().substring(0, 8)
          ));
      }
  ```
  ```php PHP
  $page = $client->beta->memoryStores->memories->list($store->id, pathPrefix: '/');
  foreach ($page->data as $memory) {
      printf("%s  (%d bytes, sha=%s)\n", $memory->path, $memory->sizeBytes, substr($memory->contentSha256, 0, 8));
  }
  ```
  ```ruby Ruby
  page = client.beta.memory_stores.memories.list(
    store.id,
    path_prefix: "/"
  )
  page.data.each do
    puts "#{it.path}  (#{it.size_bytes} bytes, sha=#{it.content_sha256[0, 8]})"
  end
  ```
</CodeGroup>

### Baca memori
Mengambil memori individual mengembalikan konten dokumen lengkap.

<CodeGroup>
  
  ```bash curl
  mem=$(curl -fsS "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$memory_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")
  jq -r '.content' <<< "$mem"
  ```
  
  ```bash CLI
  ant beta:memory-stores:memories retrieve \
    --memory-store-id "$store_id" \
    --memory-id "$memory_id"
  ```
  ```python Python
  mem = client.beta.memory_stores.memories.retrieve(
      memory_id,
      memory_store_id=store.id,
  )
  print(mem.content)
  ```
  ```typescript TypeScript
  const memory = await client.beta.memoryStores.memories.retrieve(memoryId, {
    memory_store_id: store.id
  });
  console.log(memory.content);
  ```
  ```csharp C#
  var mem = await client.Beta.MemoryStores.Memories.Retrieve(memoryId, new()
  {
      MemoryStoreID = store.ID,
  });
  Console.WriteLine(mem.Content);
  ```
  ```go Go
  	memory, err := client.Beta.MemoryStores.Memories.Get(ctx, memoryID, anthropic.BetaMemoryStoreMemoryGetParams{
  		MemoryStoreID: store.ID,
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(memory.Content)
  ```
  ```java Java
      var mem = client.beta().memoryStores().memories().retrieve(
          memoryId,
          MemoryRetrieveParams.builder().memoryStoreId(store.id()).build()
      );
      IO.println(mem.content());
  ```
  ```php PHP
  $memory = $client->beta->memoryStores->memories->retrieve($memoryId, memoryStoreID: $store->id);
  echo "{$memory->content}\n";
  ```
  ```ruby Ruby
  mem = client.beta.memory_stores.memories.retrieve(
    memory_id,
    memory_store_id: store.id
  )
  puts mem.content
  ```
</CodeGroup>

### Tulis dokumen

Gunakan `memories.write` untuk upsert dokumen **berdasarkan jalur**. Jika tidak ada yang ada di jalur, itu dibuat; jika dokumen sudah ada di sana, kontennya diganti. Untuk mutasi dokumen yang ada **berdasarkan ID `mem_...`** (misalnya, untuk mengganti nama jalurnya atau dengan aman menerapkan edit konten), gunakan `memories.update` sebagai gantinya (lihat [Update](#update) di bawah).

<CodeGroup>
  
  ```bash curl
  mem=$(curl -fsS "https://api.anthropic.com/v1/memory_stores/$store_id/memories" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<EOF
  {
    "path": "/preferences/formatting.md",
    "content": "Always use tabs, not spaces."
  }
  EOF
  )
  ```
  
  ```bash CLI
  mem_sha=$(ant beta:memory-stores:memories write \
    --memory-store-id "$store_id" \
    --path "/preferences/formatting.md" \
    --content "Always use tabs, not spaces." \
    --transform content_sha256 --format yaml)
  ```
  ```python Python
  mem = client.beta.memory_stores.memories.write(
      memory_store_id=store.id,
      path="/preferences/formatting.md",
      content="Always use tabs, not spaces.",
  )
  ```
  ```typescript TypeScript
  const mem = await client.beta.memoryStores.memories.write(store.id, {
    path: "/preferences/formatting.md",
    content: "Always use tabs, not spaces."
  });
  ```
  ```csharp C#
  mem = await client.Beta.MemoryStores.Memories.Create(store.ID, new()
  {
      Path = "/preferences/formatting.md",
      Content = "Always use tabs, not spaces.",
  });
  ```
  ```go Go
  	mem, err := client.Beta.MemoryStores.Memories.New(ctx, store.ID, anthropic.BetaMemoryStoreMemoryNewParams{
  		Path:    "/preferences/formatting.md",
  		Content: "Always use tabs, not spaces.",
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

### Buat hanya jika jalur bebas

Lewatkan `precondition={"type": "not_exists"}` ke `memories.write` untuk menjadikannya penjaga create-only. Jika dokumen sudah ada di jalur, penulisan mengembalikan `409 memory_precondition_failed` alih-alih menggantinya. Gunakan ini saat menyemai penyimpan dan Anda ingin menghindari menimpa konten yang ada.

<CodeGroup>
  
  ```bash curl
  curl -fsS "https://api.anthropic.com/v1/memory_stores/$store_id/memories" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- > /dev/null <<EOF
  {
    "path": "/preferences/formatting.md",
    "content": "Always use 2-space indentation.",
    "precondition": {"type": "not_exists"}
  }
  EOF
  ```
  
  ```bash CLI
  ant beta:memory-stores:memories write \
    --memory-store-id "$store_id" \
    > /dev/null <<YAML
  path: /preferences/formatting.md
  content: "CORRECTED: Always use 2-space indentation."
  precondition:
    type: content_sha256
    content_sha256: $mem_sha
  YAML
  ```
  ```python Python
  client.beta.memory_stores.memories.write(
      memory_store_id=store.id,
      path="/preferences/formatting.md",
      content="Always use 2-space indentation.",
      precondition={"type": "not_exists"},
  )
  ```
  ```typescript TypeScript
  await client.beta.memoryStores.memories.write(store.id, {
    path: "/preferences/formatting.md",
    content: "Always use 2-space indentation.",
    precondition: { type: "not_exists" }
  });
  ```
  ```csharp C#
  await client.Beta.MemoryStores.Memories.Create(store.ID, new()
  {
      Path = "/preferences/formatting.md",
      Content = "Always use 2-space indentation.",
      Precondition = new NotExistsPrecondition { Type = "not_exists" },
  });
  ```
  ```go Go
  	_, err = client.Beta.MemoryStores.Memories.New(ctx, store.ID, anthropic.BetaMemoryStoreMemoryNewParams{
  		Path:    "/preferences/formatting.md",
  		Content: "Always use 2-space indentation.",
  		Precondition: anthropic.BetaMemoryStoreMemoryNewParamsPreconditionUnion{
  			OfNotExists: &anthropic.BetaManagedAgentsNotExistsPreconditionParams{},
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  ```
  ```java Java
      client.beta().memoryStores().memories().create(
          store.id(),
          MemoryCreateParams.builder()
              .path("/preferences/formatting.md")
              .content("Always use 2-space indentation.")
              .precondition(
                  MemoryCreateParams.Precondition.builder()
                      .type(MemoryCreateParams.Precondition.Type.NOT_EXISTS)
                      .build()
              )
              .build()
      );
  ```
  ```php PHP
  $client->beta->memoryStores->memories->create(
      $store->id,
      path: '/preferences/formatting.md',
      content: 'Always use 2-space indentation.',
      precondition: ['type' => 'not_exists'],
  );
  ```
  ```ruby Ruby
  client.beta.memory_stores.memories.create(
    store.id,
    path: "/preferences/formatting.md",
    content: "Always use 2-space indentation.",
    precondition: {type: "not_exists"}
  )
  ```
</CodeGroup>

Untuk dengan aman mengedit dokumen yang ada (baca, ubah, tulis kembali tanpa menimpa perubahan bersamaan), gunakan `memories.update` dengan kondisi awal `content_sha256` sebagai gantinya. Lihat [Update](#update) di bawah.

### Update

`memories.update()` memodifikasi dokumen yang ada berdasarkan ID `mem_...` nya. Anda dapat mengubah `content`, `path` (penggantian nama), atau keduanya dalam satu panggilan.

Mengganti nama ke jalur yang ditempati mengembalikan `409 conflict`. Pemanggil harus menghapus atau mengganti nama pemblokir terlebih dahulu, atau meneruskan `precondition={"type": "not_exists"}` untuk membuat penggantian nama menjadi no-op jika ada yang sudah ada di target.

Contoh di bawah mengganti nama dokumen ke jalur arsip:

<CodeGroup>
  
  ```bash curl
  curl -fsS -X PATCH "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
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

#### Edit konten yang aman (keselarasan optimis)

Untuk mengedit konten dokumen tanpa menimpa penulisan bersamaan, lewatkan kondisi awal `content_sha256`. Pembaruan hanya berlaku jika hash yang disimpan masih cocok dengan yang Anda baca; pada ketidakcocokan itu mengembalikan `409 memory_precondition_failed`, di mana titik Anda membaca ulang dokumen dan mencoba lagi terhadap status segar.

<CodeGroup>
  ```bash curl
  curl -fsS -X PATCH "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- > /dev/null <<EOF
  {
    "content": "CORRECTED: Always use 2-space indentation.",
    "precondition": {"type": "content_sha256", "content_sha256": "$mem_sha"}
  }
  EOF
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
      Precondition = new ContentSha256Precondition
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
  		Precondition: anthropic.BetaMemoryStoreMemoryUpdateParamsPreconditionUnion{
  			OfContentSha256: &anthropic.BetaManagedAgentsContentSha256PreconditionParams{
  				ContentSha256: mem.ContentSha256,
  			},
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
                  MemoryUpdateParams.Precondition.builder()
                      .type(MemoryUpdateParams.Precondition.Type.CONTENT_SHA256)
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

### Hapus dokumen

<CodeGroup>
  
  ```bash curl
  curl -fsS -X DELETE "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" > /dev/null
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

Secara opsional lewatkan `expected_content_sha256` untuk penghapusan bersyarat.

## Versi memori

Setiap mutasi ke memori membuat **memory version** yang tidak dapat diubah (`memver_...`). Versi terakumulasi untuk seumur hidup memori induk dan membentuk permukaan audit dan rollback di bawahnya. Panggilan `memories.retrieve` langsung selalu mengembalikan kepala saat ini; titik akhir versi memberi Anda riwayat lengkap.

Versi baru ditulis pada setiap mutasi:

- `memories.write` pertama ke jalur membuat versi dengan `operation: "created"`.
- `memories.update` yang mengubah `content`, `path`, atau keduanya membuat versi dengan `operation: "modified"`.
- `memories.delete` membuat versi dengan `operation: "deleted"`.

Gunakan titik akhir versi untuk mengaudit pengguna atau agen mana yang mengubah apa dan kapan, untuk memeriksa atau mengembalikan snapshot sebelumnya, dan untuk menghapus konten sensitif dari riwayat dengan redact.

### Daftar versi

Daftar metadata versi yang dipaginasi untuk sebuah toko, terbaru terlebih dahulu. Filter berdasarkan `memory_id`, `operation` (`created`, `modified`, atau `deleted`), `session_id`, `api_key_id`, atau rentang waktu `created_at_gte`/`created_at_lte`. Respons daftar tidak menyertakan badan `content`; ambil versi individual dengan `retrieve` ketika Anda memerlukan konten lengkap.

<CodeGroup>
  ```bash curl
  curl -fsS "https://api.anthropic.com/v1/memory_stores/$store_id/memory_versions?memory_id=$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    | jq -r '.data[] | "\(.id): \(.operation)"'
  ```
  ```python Python
  for v in client.beta.memory_stores.memory_versions.list(
      store.id,
      memory_id=mem.id,
  ):
      print(f"{v.id}: {v.operation}")
  ```
  ```typescript TypeScript
  const versions = await client.beta.memoryStores.memoryVersions.list(store.id, {
    memory_id: mem.id
  });
  for await (const v of versions) {
    console.log(`${v.id}: ${v.operation}`);
  }
  ```
  ```csharp C#
  var versions = await client.Beta.MemoryStores.MemoryVersions.List(store.ID, new()
  {
      MemoryID = mem.ID,
  });
  await foreach (var v in versions.Paginate())
  {
      Console.WriteLine($"{v.ID}: {v.Operation.Raw()}");
  }
  ```
  ```go Go
  	page := client.Beta.MemoryStores.MemoryVersions.ListAutoPaging(ctx, store.ID, anthropic.BetaMemoryStoreMemoryVersionListParams{
  		MemoryID: anthropic.String(mem.ID),
  	})
  	for page.Next() {
  		v := page.Current()
  		fmt.Printf("%s: %s\n", v.ID, v.Operation)
  	}
  	if err := page.Err(); err != nil {
  		panic(err)
  	}
  ```
  ```java Java
      for (var v : client.beta().memoryStores().memoryVersions().list(
          store.id(),
          MemoryVersionListParams.builder().memoryId(mem.id()).build()
      ).autoPager()) {
          IO.println(v.id() + ": " + v.operation());
      }
  ```
  ```php PHP
  foreach ($client->beta->memoryStores->memoryVersions->list(
      $store->id,
      memoryID: $mem->id,
  )->pagingEachItem() as $v) {
      echo "{$v->id}: {$v->operation}\n";
  }
  ```
  ```ruby Ruby
  client.beta.memory_stores.memory_versions.list(
    store.id,
    memory_id: mem.id
  ).auto_paging_each do |v|
    puts "#{v.id}: #{v.operation}"
  end
  ```
</CodeGroup>

### Ambil sebuah versi

Mengambil versi individual mengembalikan bidang yang sama dengan respons daftar ditambah badan `content` lengkap.

<CodeGroup>
  ```bash curl
  curl -fsS "https://api.anthropic.com/v1/memory_stores/$store_id/memory_versions/$version_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
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

### Redaksi sebuah versi

Redaksi menghapus konten dari versi historis sambil mempertahankan jejak audit (siapa yang melakukan apa, kapan). Gunakan untuk alur kerja kepatuhan seperti menghapus rahasia yang bocor, PII, atau permintaan penghapusan pengguna. Redaksi dengan keras menghapus `content`, `content_sha256`, `content_size_bytes`, dan `path`; semua bidang lainnya, termasuk aktor dan stempel waktu, dipertahankan.

<CodeGroup>
  ```bash curl
  curl -fsS -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/memory_versions/$version_id/redact" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{}'
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