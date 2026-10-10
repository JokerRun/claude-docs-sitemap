---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: 196cfa93a5bbb32c8d1caff2e96dd4cb9e3d6f6adbdd0dad63b5206387d0764e
---

---
title: Orkestrasi multiagen
url: https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration
description: Koordinasikan beberapa agen dalam satu sesi.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Orkestrasi multiagen memungkinkan satu agen berkoordinasi dengan agen lain untuk menyelesaikan pekerjaan yang kompleks. Agen dapat bertindak secara paralel dengan konteks terisolasi masing-masing, yang membantu meningkatkan kualitas output dan juga dapat mempercepat waktu penyelesaian.

Tidak yakin apakah pengaturan multiagen cocok untuk masalah Anda? Lihat [kapan menggunakan sistem multiagen (dan kapan tidak)](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them).

## Serahkan pekerjaan ke agen lain

Agen yang dijalankan oleh sebuah sesi dapat menyerahkan pekerjaan ke agen lain dengan dua cara. Dengan **subagents** (subagen), agen mendelegasikan tugas sendiri dan membaca apa yang dilaporkan setiap subagen. Dengan **dynamic workflows** (alur kerja dinamis), agen menulis sebuah workflow: program yang menjalankan banyak agen di latar belakang dan menggabungkan hasilnya. Agen juga dapat berkonsultasi dengan model **advisor** (penasihat) untuk mendapatkan panduan sementara ia mengerjakan pekerjaannya sendiri.

Anda menentukan mana di antara ini yang dapat digunakan agen, dan agen menentukan kapan menggunakannya. Untuk memandu pilihan tersebut, beri tahu agen dalam prompt sistemnya kapan harus menggunakan eksekusi workflow. Lihat [Beri tahu agen kapan menggunakan eksekusi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#tell-the-agent-when-to-use-a-run). Anda juga dapat membatasi agen hanya pada agen-agen yang Anda cantumkan.

Dengan subagen, agen itu sendiri yang menentukan apa yang terjadi selanjutnya. [Thread subagen](https://platform.claude.com/docs/id/managed-agents/session-threads) tetap tersedia hingga Anda mengarsipkannya, sehingga agen dapat mengirimkan pesan lanjutan kepadanya. Dengan alur kerja dinamis, Claude menulis program untuk mengorkestrasi agen tanpa keterlibatan langsung Claude. Konteks dan hasil diteruskan secara terprogram dari satu agen ke agen lain, sehingga thread sesi utama bebas untuk berkomunikasi dengan pengguna dan memeriksa satu atau beberapa workflow yang sedang berjalan untuk melaporkan kemajuan. Agen tidak dapat mengirim pesan lanjutan ke thread milik sebuah eksekusi, dan server mengarsipkan masing-masing thread tersebut paling lambat saat eksekusinya berakhir.

| Pendekatan                                                                                                                           | Apa yang terjadi                                                                                                                                                                                                                                                                                      | Gunakan ketika                                                                                                                                                                                                                                     | Pertimbangkan                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Subagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#delegate-to-subagents)                         | Agen mendelegasikan tugas ke subagennya. Setiap subagen bekerja di [thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads) miliknya sendiri, yang dapat Anda cantumkan dan stream.                                                                                          | Agen perlu menindaklanjuti subagen setelah subagen melapor, atau agen membutuhkan spesialis yang Anda cantumkan, dengan prompt sistem dan alat mereka sendiri.                                                                                     | Delegasi hanya sedalam satu tingkat, dan sebuah sesi dapat memiliki paling banyak 25 thread anak sekaligus, termasuk yang idle. Thread advisor dan thread milik eksekusi workflow tidak dihitung.                                                                                                                                                                 |
| [Alur kerja dinamis](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#dynamic-workflows)                  | Agen menulis sebuah workflow: program yang menjalankan banyak agen dalam beberapa fase dan menggabungkan hasilnya. Server menjalankannya di latar belakang sebagai satu eksekusi workflow, yang dapat Anda ikuti. Workflow mendefinisikan agen-agennya atau memilihnya dari daftar yang Anda berikan. | Sebagian besar pekerjaan yang membutuhkan lebih dari satu agen: pekerjaan dengan banyak bagian, pekerjaan paralel, atau tugas panjang yang sebaiknya selesai lebih cepat. Contohnya adalah audit, migrasi, riset mendalam, dan pemeriksaan silang. | Setiap agen dalam sebuah eksekusi menggunakan token, jadi tetapkan [anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets) untuk membatasi pengeluaran sesi, termasuk eksekusi. Beri tahu agen dalam prompt sistemnya kapan harus menggunakan eksekusi. Anda mengikuti eksekusi berdasarkan fase-fasenya dan dapat membaca setiap thread-nya. |
| [Berikan advisor pada sesi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor) | [Thread utama](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#how-it-works) sesi berkonsultasi dengan model advisor di tengah giliran untuk mendapatkan panduan, seperti merencanakan pendekatan atau meninjau pekerjaan, dan tetap mengerjakan pekerjaannya sendiri.    | Satu agen sebaiknya mengerjakan pekerjaan, dengan penilaian model advisor pada momen-momen penting seperti perencanaan atau tinjauan akhir.                                                                                                        | Hanya thread utama yang dapat berkonsultasi dengan advisor, dan konsultasi ditagih sesuai tarif model advisor.                                                                                                                                                                                                                                                    |

Anda mengatur ini di blok `multiagent` pada definisi agen, yang memiliki sebuah `type`. Dengan tipe `multiagent_20261001`, sebuah agen dapat menggunakan ketiganya bersama-sama, dan Anda dapat mengaktifkan atau menonaktifkan masing-masing. Secara default, `subagents` dan `workflows` keduanya diaktifkan. `subagents` dan `workflows` masing-masing memiliki `inline_agents` yang diaktifkan, yaitu pengaturan untuk [agen yang didefinisikan sendiri oleh agen atau workflow](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#predefined-and-inline-agents):

```json
{
  "multiagent": { "type": "multiagent_20261001" }
}
```

Untuk mengatur agen mana yang dapat dipanggil oleh agen, lihat [Agen predefined dan inline](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#predefined-and-inline-agents). Untuk menonaktifkan sebuah pengaturan, lihat [Aktifkan alur kerja dinamis](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#turn-on-dynamic-workflows).

## Agen predefined dan inline

Setiap subagen, dan setiap agen dalam sebuah eksekusi workflow, adalah salah satu dari dua jenis:

* **Agen predefined (agen yang telah ditentukan sebelumnya):** Agen yang telah Anda [buat](https://platform.claude.com/docs/id/managed-agents/agent-setup), dan yang Anda cantumkan di blok `multiagent`. Agen ini menggunakan konfigurasinya sendiri: model, prompt sistem, alat, server MCP, dan skill.
* **Agen inline:** Agen yang tidak disimpan. Agen yang dijalankan sesi, atau sebuah workflow, mendefinisikannya saat membagikan pekerjaan. Agen ini menggunakan model, alat, server MCP, dan skill milik agen tersebut.

Kedua jenis berfungsi di bawah `subagents` dan di bawah `workflows`:

| Jenis agen | Di bawah `subagents`                                                                                                      | Di bawah `workflows`                                                                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Predefined | Agen dapat mendelegasikan ke agen-agen yang Anda cantumkan di `subagents.predefined_agents`.                              | Sebuah workflow dapat menggunakan agen-agen yang Anda cantumkan di `workflows.predefined_agents`.                                                               |
| Inline     | Agen dapat mendefinisikan agen inline saat mendelegasikan. `subagents.inline_agents` mengaktifkan atau menonaktifkan ini. | Sebuah workflow dapat mendefinisikan agen inline, dan menulis prompt sistem untuk masing-masing. `workflows.inline_agents` mengaktifkan atau menonaktifkan ini. |

`subagents.predefined_agents` dan `workflows.predefined_agents` adalah dua daftar terpisah. Agen di satu daftar tidak ditambahkan ke daftar lainnya. Kedua daftar kosong secara default. Entri di salah satu daftar mengambil salah satu bentuk berikut:

* `{"type": "agent", "id": agent.id}` mereferensikan `agent` yang telah dibuat sebelumnya berdasarkan ID. Jika tidak ada `version` yang ditentukan, referensi disematkan ke versi terbaru agen saat agen yang mencantumkannya dibuat, atau saat sebuah pembaruan mengirimkan daftar tersebut.
* `{"type": "agent", "id": agent.id, "version": agent.version}` menyematkan versi agen tertentu.
* `agent.id` saja, sebagai string, adalah singkatan dari `{"type": "agent", "id": agent.id}`.
* `{"type": "self"}` mencantumkan agen itu sendiri, sehingga salinan dirinya dapat mengerjakan pekerjaan. Jika sesi dibuat dengan [override konfigurasi agen](https://platform.claude.com/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session), override tersebut juga berlaku untuk salinan-salinan ini. Entri yang direferensikan berdasarkan ID tidak terpengaruh.

Aturan untuk entri-entri ini, dan untuk agen yang disebutkannya, berlaku untuk kedua daftar. Lihat [Cantumkan subagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#list-the-subagents).

Agen inline aktif secara default di bawah kedua pengaturan. Untuk hanya mengizinkan agen yang Anda cantumkan, atur `inline_agents` ke `{"type": "disabled"}` di bawah `subagents`, di bawah `workflows`, atau di bawah keduanya. Pengaturan dengan agen inline dinonaktifkan memerlukan setidaknya satu agen dalam daftar `predefined_agents`-nya. Dengan daftar kosong, permintaan gagal dengan error 400. Pada pembaruan, server memeriksa pengaturan sebagaimana adanya setelah pembaruan.

Agen berikut hanya mengizinkan agen yang dicantumkannya. Agen ini dapat mendelegasikan ke satu agen dan ke salinan dirinya sendiri, dan sebuah workflow dapat menggunakan versi 2 dari agen lain:

```json
{
  "multiagent": {
    "type": "multiagent_20261001",
    "subagents": {
      "type": "enabled",
      "inline_agents": { "type": "disabled" },
      "predefined_agents": ["agent_01J8XkN5uT3vHpLqRfWdY2", { "type": "self" }]
    },
    "workflows": {
      "type": "enabled",
      "inline_agents": { "type": "disabled" },
      "predefined_agents": [
        { "type": "agent", "id": "agent_01Lm4cV8yQ2tNs7XbKdR5h", "version": 2 }
      ]
    }
  }
}
```

## Delegasikan ke subagen

### Apa yang perlu didelegasikan

Koordinasi multiagen paling cocok untuk tugas kompleks yang memerlukan pekerjaan di berbagai permukaan, atau di mana beberapa tugas dengan cakupan yang jelas berkontribusi pada tujuan keseluruhan.

Pola yang bekerja dengan baik:

* **Paralelisasi:** Sebarkan subtugas independen secara bersamaan (mencari di beberapa sumber, menganalisis file terpisah) dan minta agen menyintesis hasilnya.
* **Spesialisasi:** Rutekan ke agen dengan prompt sistem dan alat yang berfokus pada domain, seperti agen keamanan atau agen dokumentasi, alih-alih membebani satu agen dengan setiap kemampuan.
* **Eskalasi:** Konsultasikan dengan agen atau model yang lebih mampu untuk sebagian subtugas yang kompleks. Untuk berkonsultasi dengan model, [berikan advisor pada sesi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor).

### Cara kerjanya

Semua agen berbagi sandbox, sistem file, dan [kredensial vault](https://platform.claude.com/docs/id/managed-agents/vaults) yang sama, tetapi setiap agen berjalan di **session thread** (thread sesi) miliknya sendiri, yaitu aliran event dengan konteks terisolasi yang memiliki riwayat percakapannya sendiri. Agen yang dijalankan sesi melaporkan aktivitas di **primary thread** (thread utama), yang merupakan [aliran event](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) tingkat sesi. Thread tambahan dibuat saat runtime ketika agen mendelegasikan pekerjaan. Sebuah eksekusi workflow juga membuat thread.

Thread subagen bersifat persisten. Agen dapat mengirim tindak lanjut ke subagen yang dipanggilnya sebelumnya, dan subagen tersebut mempertahankan semua hal dari giliran-giliran sebelumnya.

Konfigurasi mana yang digunakan subagen bergantung pada apakah ia merupakan [agen predefined atau inline](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#predefined-and-inline-agents). [Override konfigurasi agen](https://platform.claude.com/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session) tingkat sesi berlaku untuk agen yang dijalankan sesi dan untuk salinan `self`-nya. Setiap agen mempertahankan riwayat percakapannya sendiri.

### Cantumkan subagen

Saat [mendefinisikan agen Anda](https://platform.claude.com/docs/id/managed-agents/agent-setup), atur `subagents.predefined_agents` di blok `multiagent` untuk mencantumkan agen-agen yang dapat menjadi tujuan delegasinya:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  lead_agent=$(curl -fsS https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "name": "Engineering Lead",
    "model": "claude-opus-5-5",
    "system": "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
    "tools": [
      {
        "type": "agent_toolset_20260401"
      }
    ],
    "multiagent": {
      "type": "multiagent_20261001",
      "subagents": {
        "type": "enabled",
        "predefined_agents": [
          {"type": "agent", "id": "$REVIEWER_AGENT_ID"},
          {"type": "agent", "id": "$TEST_WRITER_AGENT_ID"}
        ]
      }
    }
  }
  EOF
  )
  ```

  <CodeGroupItem>
    ```bash CLI
    # Buat subagent, lalu baca ID-nya dari lockfile.
    ant apply reviewer.md test-writer.md
    REVIEWER_AGENT_ID=$(jq -er '.resources["./reviewer.md"].id' claude-lock.json)
    TEST_WRITER_AGENT_ID=$(jq -er '.resources["./test-writer.md"].id' claude-lock.json)

    # Tulis definisi agent, dengan mencantumkan setiap subagent berdasarkan ID.
    cat > engineering-lead.md <<EOF
    ---
    name: Engineering Lead
    model: claude-opus-5-5
    tools:
      - type: agent_toolset_20260401
    multiagent:
      type: multiagent_20261001
      subagents:
        type: enabled
        predefined_agents:
          - type: agent
            id: $REVIEWER_AGENT_ID
          - type: agent
            id: $TEST_WRITER_AGENT_ID
    ---

    You coordinate engineering work. Delegate code review to the reviewer agent
    and test writing to the test agent.
    EOF

    # Buat agent.
    ant apply engineering-lead.md reviewer.md test-writer.md
    ```

    <File filename="reviewer.md">
      ```markdown
      ---
      name: reviewer
      model: claude-haiku-5-5
      ---

      You are a code reviewer.
      ```
    </File>

    <File filename="test-writer.md">
      ```markdown
      ---
      name: test-writer
      model: claude-haiku-5-5
      ---

      You write unit tests.
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  lead_agent = client.beta.agents.create(
      name="Engineering Lead",
      model="claude-opus-5-5",
      system="You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
      tools=[
          {"type": "agent_toolset_20260401"},
      ],
      multiagent={
          "type": "multiagent_20261001",
          "subagents": {
              "type": "enabled",
              "predefined_agents": [
                  {"type": "agent", "id": reviewer_agent.id},
                  {"type": "agent", "id": test_writer_agent.id},
              ],
          },
      },
  )
  ```

  ```typescript TypeScript
  const leadAgent = await client.beta.agents.create({
    name: "Engineering Lead",
    model: "claude-opus-5-5",
    system:
      "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
    tools: [{ type: "agent_toolset_20260401" }],
    multiagent: {
      type: "multiagent_20261001",
      subagents: {
        type: "enabled",
        predefined_agents: [
          { type: "agent", id: reviewerAgent.id },
          { type: "agent", id: testWriterAgent.id },
        ],
      },
    },
  });
  ```

  ```csharp C#
  var leadAgent = await client.Beta.Agents.Create(new()
  {
      Name = "Engineering Lead",
      Model = BetaManagedAgentsModel.ClaudeOpus5_5,
      System = "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
          },
      ],
      Multiagent = new BetaManagedAgentsMultiagent20261001Params
      {
          Subagents = new BetaManagedAgentsMultiagentSubagentsEnabledParams
          {
              PredefinedAgents = [reviewerAgent.ID, testWriterAgent.ID],
          },
      },
  });
  ```

  ```go Go
  leadAgent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name:   "Engineering Lead",
  	Model:  anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeOpus5_5},
  	System: anthropic.String("You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent."),
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		},
  	}},
  	Multiagent: anthropic.BetaManagedAgentsMultiagentParamsUnion{
  		OfMultiagent20261001: &anthropic.BetaManagedAgentsMultiagent20261001Params{
  			Subagents: anthropic.BetaManagedAgentsMultiagentSubagentsParamsUnion{
  				OfEnabled: &anthropic.BetaManagedAgentsMultiagentSubagentsEnabledParams{
  					PredefinedAgents: []anthropic.BetaManagedAgentsMultiagentPredefinedAgentParamsUnion{
  						{OfString: anthropic.String(reviewerAgent.ID)},
  						{OfString: anthropic.String(testWriterAgent.ID)},
  					},
  				},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var leadAgent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Engineering Lead")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5_5)
          .system("You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.")
          .addTool(
              BetaManagedAgentsAgentToolset20260401Params.builder()
                  .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                  .build()
          )
          .multiagent(BetaManagedAgentsMultiagent20261001Params.builder()
              .subagents(BetaManagedAgentsMultiagentSubagentsEnabledParams.builder()
                  .addPredefinedAgent(BetaManagedAgentsAgentParams.builder()
                      .type(BetaManagedAgentsAgentParams.Type.AGENT)
                      .id(reviewerAgent.id())
                      .build())
                  .addPredefinedAgent(BetaManagedAgentsAgentParams.builder()
                      .type(BetaManagedAgentsAgentParams.Type.AGENT)
                      .id(testWriterAgent.id())
                      .build())
                  .build())
              .build())
          .build()
  );
  ```

  ```php PHP
  $leadAgent = $client->beta->agents->create(
      name: 'Engineering Lead',
      model: 'claude-opus-5-5',
      system: 'You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.',
      tools: [
          ['type' => 'agent_toolset_20260401'],
      ],
      multiagent: [
          'type' => 'multiagent_20261001',
          'subagents' => [
              'type' => 'enabled',
              'predefined_agents' => [
                  ['type' => 'agent', 'id' => $reviewerAgent->id],
                  ['type' => 'agent', 'id' => $testWriterAgent->id],
              ],
          ],
      ],
  );
  ```

  ```ruby Ruby
  lead_agent = client.beta.agents.create(
    name: "Engineering Lead",
    model: "claude-opus-5-5",
    system: "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
    tools: [
      {type: "agent_toolset_20260401"}
    ],
    multiagent: {
      type: "multiagent_20261001",
      subagents: {
        type: "enabled",
        predefined_agents: [
          {type: "agent", id: reviewer_agent.id},
          {type: "agent", id: test_writer_agent.id}
        ]
      }
    }
  )
  ```
</CodeGroup>

Agen juga dapat mendelegasikan ke agen inline kecuali Anda menonaktifkannya. Untuk pengaturan tersebut, dan untuk bentuk-bentuk yang dapat diambil oleh entri `subagents.predefined_agents`, lihat [Agen predefined dan inline](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#predefined-and-inline-agents).

`"advisor": {"type": "enabled", "model": "<model id>"}` memberi thread utama sesi sebuah advisor yang dapat dikonsultasikan di tengah giliran. Advisor adalah pengaturan di blok `multiagent`, bukan entri dalam daftar ini. Lihat [Berikan advisor pada sesi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor).

Alur kerja dinamis juga diaktifkan secara default dengan tipe ini, sehingga agen ini dapat merencanakan pekerjaan besar yang menjalankan banyak agen di latar belakang. Untuk menonaktifkannya, atau untuk mencantumkan agen yang dapat digunakan workflow, lihat [Aktifkan alur kerja dinamis](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#turn-on-dynamic-workflows).

Aturan berikut berlaku untuk agen yang Anda cantumkan di `subagents.predefined_agents`, dan juga untuk agen yang Anda cantumkan di `workflows.predefined_agents`:

* **Penyematan:** Konfigurasi agen, termasuk daftar `subagents.predefined_agents`-nya, diambil snapshot-nya saat agen dibuat atau diperbarui. Agen yang direferensikan tetap disematkan ke versi yang diresolusi saat itu dan tidak mengambil pembaruan selanjutnya pada definisinya. Pembaruan yang tidak mengirimkan daftar tersebut mempertahankan versi yang sudah disematkan. Untuk mendelegasikan ke versi yang lebih baru dari agen yang direferensikan, [perbarui agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-an-agent) sehingga daftar `subagents.predefined_agents`-nya mereferensikan versi tersebut.
* **Satu tingkat:** Agen hanya dapat mendelegasikan ke satu tingkat agen. Mereferensikan agen lain yang memiliki `multiagent` yang diatur akan membuat permintaan pembuatan atau pembaruan gagal dengan error validasi 400.
* **Hingga 20 agen:** `subagents.predefined_agents` dapat mencantumkan hingga 20 agen unik. Batas ini berlaku per daftar: `workflows.predefined_agents` juga dapat mencantumkan hingga 20. Agen dapat memanggil beberapa salinan dari setiap agen, dalam [batas thread](https://platform.claude.com/docs/id/managed-agents/session-threads) sesi.
* **Geografi inferensi:** Agen dan setiap agen yang Anda cantumkan, di `subagents.predefined_agents` atau di `workflows.predefined_agents`, harus menyematkan [geografi inferensi](https://platform.claude.com/docs/id/manage-claude/data-residency) yang sama (`model.inference_geo` dalam [definisi agen](https://platform.claude.com/docs/id/managed-agents/agent-setup)), atau tidak satu pun dari mereka boleh menyematkannya. Ketidakcocokan di salah satu daftar ditolak dengan error validasi 400. Pemeriksaan tersebut dijalankan baik saat agen disimpan maupun saat [override pembuatan sesi](https://platform.claude.com/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session) mengubah salah satu sematan.

### Buat sesi

Buat sesi yang mereferensikan agen. Agen mendelegasikan ke agen-agen yang Anda cantumkan di `subagents.predefined_agents` sesuai kebutuhan. Agen juga dapat mendelegasikan ke [agen inline](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#predefined-and-inline-agents) kecuali Anda menonaktifkannya.

<CodeGroup>
  ```bash cURL
  session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$LEAD_AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID"
  }
  EOF
  )
  SESSION_ID=$(jq -r '.id' <<< "$session")
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent "$LEAD_AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID"
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=lead_agent.id,
      environment_id=environment.id,
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: leadAgent.id,
    environment_id: environment.id,
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = leadAgent.ID,
      EnvironmentID = environment.ID,
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(leadAgent.ID),
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(leadAgent.id())
      .environmentId(environment.id())
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $leadAgent->id,
      environmentID: $environment->id,
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: lead_agent.id,
    environment_id: environment.id
  )
  ```
</CodeGroup>

### Hubungkan agen ke server MCP

Server MCP memiliki cakupan agen: setiap definisi agen mendeklarasikan server dan alatnya sendiri. Agen inline tidak memiliki definisi agen, sehingga ia menggunakan server MCP dan alat milik agen yang dijalankan sesi. Kredensial vault memiliki cakupan sesi: `vault_ids` yang diteruskan saat pembuatan sesi berlaku untuk setiap thread. Dua implikasi untuk integrasi Anda:

* Untuk mengautentikasi server MCP, sertakan kredensial vault untuk setiap server MCP yang digunakan di semua agen.
* Untuk membatasi akses sebuah agen, deklarasikan hanya server yang dibutuhkannya dalam definisi agennya. Anda tidak dapat membatasi agen inline dengan cara ini. Untuk hanya mengizinkan agen yang Anda cantumkan, nonaktifkan `inline_agents` di `subagents` dan `workflows`, dan cantumkan setidaknya satu agen di masing-masing. Lihat [Agen predefined dan inline](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#predefined-and-inline-agents).

[Override konfigurasi agen](https://platform.claude.com/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session) saat pembuatan sesi dapat menggantikan server MCP milik agen yang dijalankan sesi dan milik salinan `self`-nya.

Dengan [environment](https://platform.claude.com/docs/id/managed-agents/environments#networking) `limited`, pembuatan sesi gagal dengan error 400 ketika agen, atau agen yang Anda cantumkan di `subagents.predefined_agents` atau `workflows.predefined_agents`, mendeklarasikan server MCP yang host-nya tidak ada di `allowed_hosts`. Mengatur `allow_mcp_servers: true` dalam pengaturan jaringan environment akan menonaktifkan pemeriksaan ini.

Buat researcher, yang mendeklarasikan server MCP GitHub, dan agen yang mendelegasikan ke researcher:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  research_agent_id=$(curl --fail-with-body -sS "$BASE/v1/agents" "${H[@]}" --data @- <<'EOF' | jq -er '.id'
  {
    "name": "researcher",
    "model": "claude-haiku-5-5",
    "mcp_servers": [{"type": "url", "name": "github", "url": "https://api.githubcopilot.com/mcp/"}],
    "tools": [{"type": "mcp_toolset", "mcp_server_name": "github"}]
  }
  EOF
  )

  lead_agent_id=$(curl --fail-with-body -sS "$BASE/v1/agents" "${H[@]}" --data @- <<EOF | jq -er '.id'
  {
    "name": "lead",
    "model": "claude-opus-5-5",
    "tools": [{"type": "agent_toolset_20260401"}],
    "multiagent": {
      "type": "multiagent_20261001",
      "subagents": {
        "type": "enabled",
        "predefined_agents": [{"type": "agent", "id": "$research_agent_id"}]
      }
    }
  }
  EOF
  )
  ```

  <CodeGroupItem>
    ```bash CLI
    # Buat researcher, lalu baca ID-nya dari lockfile.
    ant apply researcher.md
    research_agent_id=$(jq -er '.resources["./researcher.md"].id' claude-lock.json)

    # Tulis definisi agen, dengan mencantumkan researcher berdasarkan ID.
    cat > lead.md <<EOF
    ---
    name: lead
    model: claude-opus-5-5
    tools:
      - type: agent_toolset_20260401
    multiagent:
      type: multiagent_20261001
      subagents:
        type: enabled
        predefined_agents:
          - type: agent
            id: $research_agent_id
    ---
    EOF

    # Buat agen.
    ant apply lead.md researcher.md
    ```

    <File filename="researcher.md">
      ```markdown
      ---
      name: researcher
      model: claude-haiku-5-5
      mcp_servers:
        - type: url
          name: github
          url: https://api.githubcopilot.com/mcp/
      tools:
        - type: mcp_toolset
          mcp_server_name: github
      ---
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  research_agent = client.beta.agents.create(
      name="researcher",
      model="claude-haiku-5-5",
      mcp_servers=[
          {"type": "url", "name": "github", "url": "https://api.githubcopilot.com/mcp/"},
      ],
      tools=[{"type": "mcp_toolset", "mcp_server_name": "github"}],
  )

  lead_agent = client.beta.agents.create(
      name="lead",
      model="claude-opus-5-5",
      tools=[{"type": "agent_toolset_20260401"}],
      multiagent={
          "type": "multiagent_20261001",
          "subagents": {
              "type": "enabled",
              "predefined_agents": [{"type": "agent", "id": research_agent.id}],
          },
      },
  )
  ```

  ```typescript TypeScript
  const researchAgent = await client.beta.agents.create({
    name: "researcher",
    model: "claude-haiku-5-5",
    mcp_servers: [
      { type: "url", name: "github", url: "https://api.githubcopilot.com/mcp/" },
    ],
    tools: [{ type: "mcp_toolset", mcp_server_name: "github" }],
  });

  const leadAgent = await client.beta.agents.create({
    name: "lead",
    model: "claude-opus-5-5",
    tools: [{ type: "agent_toolset_20260401" }],
    multiagent: {
      type: "multiagent_20261001",
      subagents: {
        type: "enabled",
        predefined_agents: [{ type: "agent", id: researchAgent.id }],
      },
    },
  });
  ```

  ```csharp C#
  var researchAgent = await client.Beta.Agents.Create(new()
  {
      Name = "researcher",
      Model = BetaManagedAgentsModel.ClaudeHaiku5_5,
      McpServers =
      [
          new()
          {
              Type = BetaManagedAgentsUrlMcpServerParamsType.Url,
              Name = "github",
              Url = "https://api.githubcopilot.com/mcp/",
          },
      ],
      Tools =
      [
          new BetaManagedAgentsMcpToolsetParams
          {
              Type = BetaManagedAgentsMcpToolsetParamsType.McpToolset,
              McpServerName = "github",
          },
      ],
  });

  var leadAgent = await client.Beta.Agents.Create(new()
  {
      Name = "lead",
      Model = BetaManagedAgentsModel.ClaudeOpus5_5,
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
          },
      ],
      Multiagent = new BetaManagedAgentsMultiagent20261001Params
      {
          Subagents = new BetaManagedAgentsMultiagentSubagentsEnabledParams
          {
              PredefinedAgents =
              [
                  new BetaManagedAgentsAgentParams
                  {
                      Type = BetaManagedAgentsAgentParamsType.Agent,
                      ID = researchAgent.ID,
                  },
              ],
          },
      },
  });
  ```

  ```go Go
  researcher, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name:  "researcher",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeHaiku5_5},
  	MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{{
  		Type: anthropic.BetaManagedAgentsURLMCPServerParamsTypeURL,
  		Name: "github",
  		URL:  "https://api.githubcopilot.com/mcp/",
  	}},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfMCPToolset: &anthropic.BetaManagedAgentsMCPToolsetParams{
  			Type:          anthropic.BetaManagedAgentsMCPToolsetParamsTypeMCPToolset,
  			MCPServerName: "github",
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }

  leadAgent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name:  "lead",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeOpus5_5},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		},
  	}},
  	Multiagent: anthropic.BetaManagedAgentsMultiagentParamsUnion{
  		OfMultiagent20261001: &anthropic.BetaManagedAgentsMultiagent20261001Params{
  			Subagents: anthropic.BetaManagedAgentsMultiagentSubagentsParamsUnion{
  				OfEnabled: &anthropic.BetaManagedAgentsMultiagentSubagentsEnabledParams{
  					PredefinedAgents: []anthropic.BetaManagedAgentsMultiagentPredefinedAgentParamsUnion{{
  						OfBetaManagedAgentsAgents: &anthropic.BetaManagedAgentsAgentParams{
  							Type: anthropic.BetaManagedAgentsAgentParamsTypeAgent,
  							ID:   researcher.ID,
  						},
  					}},
  				},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var researcher = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("researcher")
          .model(BetaManagedAgentsModel.CLAUDE_HAIKU_5_5)
          .addMcpServer(BetaManagedAgentsUrlMcpServerParams.builder()
              .name("github")
              .type(BetaManagedAgentsUrlMcpServerParams.Type.URL)
              .url("https://api.githubcopilot.com/mcp/")
              .build())
          .addTool(BetaManagedAgentsMcpToolsetParams.builder()
              .type(BetaManagedAgentsMcpToolsetParams.Type.MCP_TOOLSET)
              .mcpServerName("github")
              .build())
          .build()
  );

  var leadAgent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("lead")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5_5)
          .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
              .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
              .build())
          .multiagent(BetaManagedAgentsMultiagent20261001Params.builder()
              .subagents(BetaManagedAgentsMultiagentSubagentsEnabledParams.builder()
                  .addPredefinedAgent(BetaManagedAgentsAgentParams.builder()
                      .type(BetaManagedAgentsAgentParams.Type.AGENT)
                      .id(researcher.id())
                      .build())
                  .build())
              .build())
          .build()
  );
  ```

  ```php PHP
  $researchAgent = $client->beta->agents->create(
      name: 'researcher',
      model: 'claude-haiku-5-5',
      mcpServers: [
          ['type' => 'url', 'name' => 'github', 'url' => 'https://api.githubcopilot.com/mcp/'],
      ],
      tools: [
          ['type' => 'mcp_toolset', 'mcp_server_name' => 'github'],
      ],
  );

  $leadAgent = $client->beta->agents->create(
      name: 'lead',
      model: 'claude-opus-5-5',
      tools: [
          ['type' => 'agent_toolset_20260401'],
      ],
      multiagent: [
          'type' => 'multiagent_20261001',
          'subagents' => [
              'type' => 'enabled',
              'predefined_agents' => [
                  ['type' => 'agent', 'id' => $researchAgent->id],
              ],
          ],
      ],
  );
  ```

  ```ruby Ruby
  research_agent = client.beta.agents.create(
    name: "researcher",
    model: "claude-haiku-5-5",
    mcp_servers: [
      {type: "url", name: "github", url: "https://api.githubcopilot.com/mcp/"}
    ],
    tools: [
      {type: "mcp_toolset", mcp_server_name: "github"}
    ]
  )

  lead_agent = client.beta.agents.create(
    name: "lead",
    model: "claude-opus-5-5",
    tools: [
      {type: "agent_toolset_20260401"}
    ],
    multiagent: {
      type: "multiagent_20261001",
      subagents: {
        type: "enabled",
        predefined_agents: [
          {type: "agent", id: research_agent.id}
        ]
      }
    }
  )
  ```
</CodeGroup>

Kemudian buat sesi dengan vault yang menyimpan kredensial GitHub:

<CodeGroup>
  ```bash cURL
  session_id=$(curl --fail-with-body -sS "$BASE/v1/sessions" "${H[@]}" --data @- <<EOF | jq -er '.id'
  {
    "agent": "$lead_agent_id",
    "environment_id": "$environment_id",
    "vault_ids": ["$vault_id"]
  }
  EOF
  )
  echo "$session_id"
  ```

  ```bash CLI
  session_id=$(ant beta:sessions create \
    --agent "$lead_agent_id" \
    --environment-id "$environment_id" \
    --vault-id "$vault_id" \
    --transform id --raw-output)
  echo "$session_id"
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=lead_agent.id,
      environment_id=environment.id,
      vault_ids=[vault.id],
  )
  print(session.id)
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: leadAgent.id,
    environment_id: environment.id,
    vault_ids: [vault.id],
  });
  console.log(session.id);
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = leadAgent.ID,
      EnvironmentID = environment.ID,
      VaultIds = [vault.ID],
  });
  Console.WriteLine(session.ID);
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(leadAgent.ID),
  	},
  	EnvironmentID: environment.ID,
  	VaultIDs:      []string{vault.ID},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(session.ID)
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(leadAgent.id())
      .environmentId(environment.id())
      .vaultIds(List.of(vault.id()))
      .build());
  IO.println(session.id());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $leadAgent->id,
      environmentID: $environment->id,
      vaultIDs: [$vault->id],
  );
  echo "{$session->id}\n";
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: lead_agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id]
  )
  puts session.id
  ```
</CodeGroup>

Dalam contoh ini, hanya researcher yang mendeklarasikan server MCP GitHub, sehingga agen yang dijalankan sesi tidak memiliki akses. `vault_ids` sesi menyediakan kredensial GitHub ke thread researcher.

<Tip>
  Jika panggilan MCP sebuah agen gagal diautentikasi setelah Anda mendeklarasikan server, pastikan `mcp_server_url` kredensial merujuk ke server yang sama dengan `mcp_servers[].url` milik agen. Kedua URL dinormalisasi sebelum dicocokkan (skema dan host diubah menjadi huruf kecil, port default dan garis miring di akhir dihapus), sehingga perbedaan huruf besar-kecil pada host, port default, atau garis miring di akhir tidak mencegah kecocokan; path, subdomain, atau port non-default yang berbeda akan mencegahnya.
</Tip>

### Thread

Thread sesi setiap agen memiliki aliran event-nya sendiri. Untuk mencantumkan, menginterupsi, atau mengarsipkan thread, membaca event-nya, dan menangani izin alat di seluruh thread, lihat [Thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads).

## Alur kerja dinamis

Dengan alur kerja dinamis, sebuah agen dapat mengerjakan pekerjaan dengan banyak bagian, seperti meninjau ratusan dokumen atau memeriksa silang banyak sumber. Agen menulis sebuah **workflow**: program yang menjalankan banyak agen dalam beberapa fase dan menggabungkan apa yang mereka kembalikan. Server menjalankannya di latar belakang sebagai **workflow run** (eksekusi workflow), sementara agen terus bekerja atau mengakhiri gilirannya. Anda mengaktifkan atau menonaktifkan alur kerja dinamis dengan pengaturan `workflows` di blok `multiagent` agen. Agen-agen dalam sebuah eksekusi dapat bekerja pada saat yang sama, sehingga tugas panjang dapat selesai lebih cepat dibandingkan jika satu agen mengerjakan setiap bagian secara bergiliran.

* **Bagaimana eksekusi dimulai:** Anda mendeskripsikan pekerjaan dalam sebuah `user.message`. Dari situ, agen menentukan apakah dan kapan memulai eksekusi, sehingga tidak ada panggilan API tambahan. Sebagai gantinya, Anda memengaruhi keputusan agen dengan mendeskripsikan kapan menggunakan eksekusi di `user.message` atau di prompt sistem agen. (Kebijakan izin berlaku untuk alat yang dipanggil oleh agen-agen dalam eksekusi, bukan untuk memulai eksekusi.)
* **Agen mana yang digunakannya:** [Agen inline](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#predefined-and-inline-agents) yang didefinisikan workflow, agen predefined yang Anda cantumkan di `workflows.predefined_agents`, atau keduanya. Jika Anda tidak mencantumkan satu pun, workflow mendefinisikan semuanya. Agen inline menggunakan model milik agen yang dijalankan sesi. Agar sebuah eksekusi dapat menggunakan model lain untuk sebagian agennya, buat mereka sebagai agen dan cantumkan di `workflows.predefined_agents`.
* **Bagaimana Anda mengikutinya:** Event eksekusi tiba di aliran event sesi, dan setiap agen dalam eksekusi bekerja di [thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads) yang dapat Anda cantumkan, baca, dan stream. Lihat [Eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs) untuk event, interupsi, batas, dan [apa yang ditampilkan thread milik sebuah eksekusi](https://platform.claude.com/docs/id/managed-agents/workflow-runs#a-runs-threads).

### Aktifkan alur kerja dinamis

Saat [mendefinisikan agen Anda](https://platform.claude.com/docs/id/managed-agents/agent-setup), atur `multiagent.type` ke `"multiagent_20261001"` dan aktifkan `workflows`. Alur kerja dinamis dan pendelegasian (`subagents`) sama-sama aktif secara default dengan tipe ini. Untuk alur kerja dinamis saja, tambahkan `"subagents": {"type": "disabled"}`.

Sebelum Anda mengubah `multiagent.type` milik agen yang sudah ada, lihat [cara memindahkan agen ke tipe ini](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#move-from-the-coordinator-type).

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsS https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "Contract Reviewer",
    "model": "claude-opus-5-5",
    "system": "You review contracts. When you're asked to review more than a few contracts, start a workflow run that reads them in parallel and combines the findings. Review one or two contracts yourself, without a run.",
    "tools": [{"type": "agent_toolset_20260401"}],
    "multiagent": {"type": "multiagent_20261001", "workflows": {"type": "enabled"}}
  }
  EOF
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply contract-reviewer.md
    ```

    <File filename="contract-reviewer.md">
      ```markdown
      ---
      name: Contract Reviewer
      model: claude-opus-5-5
      tools:
        - type: agent_toolset_20260401
      multiagent:
        type: multiagent_20261001
        workflows:
          type: enabled
      ---

      You review contracts. When you're asked to review more than a few contracts, start a workflow run that reads them in parallel and combines the findings. Review one or two contracts yourself, without a run.
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  agent = client.beta.agents.create(
      name="Contract Reviewer",
      model="claude-opus-5-5",
      system="You review contracts. When you're asked to review more than a few contracts, start a workflow run that reads them in parallel and combines the findings. Review one or two contracts yourself, without a run.",
      tools=[{"type": "agent_toolset_20260401"}],
      multiagent={"type": "multiagent_20261001", "workflows": {"type": "enabled"}},
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Contract Reviewer",
    model: "claude-opus-5-5",
    system:
      "You review contracts. When you're asked to review more than a few contracts, start a workflow run that reads them in parallel and combines the findings. Review one or two contracts yourself, without a run.",
    tools: [{ type: "agent_toolset_20260401" }],
    multiagent: { type: "multiagent_20261001", workflows: { type: "enabled" } },
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Contract Reviewer",
      Model = BetaManagedAgentsModel.ClaudeOpus5_5,
      System = "You review contracts. When you're asked to review more than a few contracts, start a workflow run that reads them in parallel and combines the findings. Review one or two contracts yourself, without a run.",
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
          },
      ],
      // Kelas konfigurasi menetapkan tipe untuk Anda.
      Multiagent = new BetaManagedAgentsMultiagent20261001Params
      {
          Workflows = new BetaManagedAgentsMultiagentWorkflowsEnabledParams(),
      },
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name:   "Contract Reviewer",
  	Model:  anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeOpus5_5},
  	System: anthropic.String("You review contracts. When you're asked to review more than a few contracts, start a workflow run that reads them in parallel and combines the findings. Review one or two contracts yourself, without a run."),
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		},
  	}},
  	Multiagent: anthropic.BetaManagedAgentsMultiagentParamsUnion{
  		OfMultiagent20261001: &anthropic.BetaManagedAgentsMultiagent20261001Params{
  			Workflows: anthropic.BetaManagedAgentsMultiagentWorkflowsParamsUnion{
  				OfEnabled: &anthropic.BetaManagedAgentsMultiagentWorkflowsEnabledParams{},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Contract Reviewer")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5_5)
          .system("You review contracts. When you're asked to review more than a few contracts, start a workflow run that reads them in parallel and combines the findings. Review one or two contracts yourself, without a run.")
          .addTool(
              BetaManagedAgentsAgentToolset20260401Params.builder()
                  .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                  .build()
          )
          // Kelas konfigurasi menetapkan tipe untuk Anda.
          .multiagent(BetaManagedAgentsMultiagent20261001Params.builder()
              .workflows(BetaManagedAgentsMultiagentWorkflowsEnabledParams.builder().build())
              .build())
          .build()
  );
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Contract Reviewer',
      model: 'claude-opus-5-5',
      system: "You review contracts. When you're asked to review more than a few contracts, start a workflow run that reads them in parallel and combines the findings. Review one or two contracts yourself, without a run.",
      tools: [
          ['type' => 'agent_toolset_20260401'],
      ],
      multiagent: ['type' => 'multiagent_20261001', 'workflows' => ['type' => 'enabled']],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Contract Reviewer",
    model: "claude-opus-5-5",
    system_: "You review contracts. When you're asked to review more than a few contracts, start a workflow run that reads them in parallel and combines the findings. Review one or two contracts yourself, without a run.",
    tools: [
      {type: "agent_toolset_20260401"}
    ],
    multiagent: {type: "multiagent_20261001", workflows: {type: "enabled"}}
  )
  ```
</CodeGroup>

Agar workflow dapat menggunakan agen yang sudah Anda buat, cantumkan agen-agen tersebut di `workflows.predefined_agents`. Pengaturan `subagents` dan `advisor` ditempatkan di blok `multiagent` yang sama. Untuk mencantumkan subagen, lihat [Delegasikan ke subagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#delegate-to-subagents). Untuk mengatur advisor, lihat [Berikan advisor pada sesi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor). Agen ini memungkinkan workflow menggunakan satu agen yang Anda buat, mencantumkan dua subagen, dan memiliki advisor:

```json
{
  "multiagent": {
    "type": "multiagent_20261001",
    "workflows": {
      "type": "enabled",
      "predefined_agents": [{ "type": "agent", "id": "agent_01Lm4cV8yQ2tNs7XbKdR5h" }]
    },
    "subagents": {
      "type": "enabled",
      "predefined_agents": [
        { "type": "agent", "id": "agent_01J8XkN5uT3vHpLqRfWdY2" },
        { "type": "agent", "id": "agent_01HqR2k7vXbZ9mNpL3wYcT" }
      ]
    },
    "advisor": { "type": "enabled", "model": "claude-opus-5-5" }
  }
}
```

Setiap pengaturan diaktifkan atau dinonaktifkan secara terpisah:

| Pengaturan  | Apa yang diaktifkannya                                                                            | Agen ditempatkan di                      | Default  |
| ----------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------- | -------- |
| `workflows` | Alur kerja dinamis                                                                                | `workflows.predefined_agents`, hingga 20 | Aktif    |
| `subagents` | Pendelegasian ke subagen: agen yang Anda cantumkan, dan agen yang didefinisikan sendiri oleh agen | `subagents.predefined_agents`, hingga 20 | Aktif    |
| `advisor`   | Model advisor                                                                                     | Tidak ada. Atur `model`.                 | Nonaktif |

Untuk mengetahui apa yang dimasukkan ke setiap daftar, dan cara mengizinkan hanya agen yang Anda cantumkan, lihat [Agen predefined dan inline](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#predefined-and-inline-agents).

Perhatikan hal-hal berikut:

* **Pembaruan:** Pembaruan yang mempertahankan tipe `multiagent_20261001` hanya mengubah apa yang dikirimkannya:

  * Pengaturan atau field yang tidak Anda sertakan mempertahankan nilai tersimpannya.
  * Pengaturan atau field yang Anda kirim sebagai `null` mengambil nilai default-nya, begitu pula semua yang ada di dalamnya, apa pun yang telah Anda simpan.
  * Daftar `predefined_agents` yang Anda kirim menggantikan daftar yang tersimpan.
  * Pengaturan yang Anda kirim dengan `type` yang berbeda menggantikan pengaturan yang tersimpan, dan field yang tidak Anda sertakan di dalamnya mengambil nilai default-nya.
  * Setiap objek yang Anda kirim memerlukan `type`-nya, dan `advisor` yang aktif memerlukan `model`-nya.

* **Menonaktifkannya:** Atur `workflows` ke `{"type": "disabled"}`. Pengaturan ini tetap nonaktif hingga ada pembaruan yang mengaktifkannya kembali. Mengirim `null` akan mengaktifkannya, karena default-nya adalah aktif. Hal yang sama berlaku untuk `subagents`.

* **Sesi yang sudah ada:** Sesi menyalin pengaturan saat sesi dibuat, sehingga mengubah agen di kemudian hari tidak mengubah sesi yang sudah ada.

* **Agen yang dapat Anda cantumkan:** Agen yang memiliki pengaturan `multiagent` tidak dapat dicantumkan sebagai subagen dari agen lain, atau di `workflows.predefined_agents` milik agen lain. Agen dapat mencantumkan dirinya sendiri di salah satu daftar dengan `{"type": "self"}`, yang akan terbaca kembali sebagai `id` dan `version` miliknya sendiri.

* **Nama alat:** Prefiks `ant__` dicadangkan. Jika agen Anda sudah memiliki alat kustom yang namanya diawali dengan `ant__`, setiap pembaruan akan gagal dengan error 400 hingga Anda mengirim `tools` tanpa nama tersebut. Sesi baru juga ditolak dengan error 400 jika agennya, atau agen di salah satu daftar, memiliki alat seperti itu. Ganti nama atau hapus alat tersebut dalam pembaruan yang sama yang mengaktifkan alur kerja dinamis. Lihat [Alat kustom](https://platform.claude.com/docs/id/managed-agents/tools#custom-tools).

* **Anggaran:** Atur [anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets) saat Anda membuat sesi untuk membatasi pengeluaran sesi, termasuk eksekusi; Anda tidak dapat menambahkannya ke sesi yang sudah ada. Eksekusi dijeda saat sesi mencapai anggaran, dan eksekusi yang dijeda oleh anggaran akan dilanjutkan saat Anda menaikkan atau menghapusnya, kecuali jika eksekusi tersebut juga dijeda oleh interupsi. Lihat [Anggaran dan batas](https://platform.claude.com/docs/id/managed-agents/workflow-runs#budgets-and-limits).

### Beri tahu agen kapan menggunakan eksekusi

Mengaktifkan alur kerja dinamis memberi agen kemampuan untuk memulai eksekusi workflow. Agen menentukan kapan harus memulainya. Untuk memandu pilihan tersebut, tambahkan instruksi seperti berikut ke prompt sistem agen. Agen peninjau kontrak di [Aktifkan alur kerja dinamis](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#turn-on-dynamic-workflows) menggunakan prompt sistem ini:

```text wrap
You review contracts. When you're asked to review more than a few contracts, start a workflow run that reads them in parallel and combines the findings. Review one or two contracts yourself, without a run.
```

Untuk menyesuaikannya, sebutkan tugas-tugas dalam domain agen Anda yang memerlukan eksekusi, serta tugas-tugas kecil yang harus dikerjakan sendiri oleh agen. Anda juga dapat memandu cara eksekusi mengerjakan pekerjaan, seperti dalam contoh-contoh berikut:

* **Cara membagi pekerjaan:** "Dalam sebuah eksekusi, gunakan satu agen per kontrak. Kemudian minta agen kedua meninjau setiap kontrak, bukan hanya kontrak yang menurut agen pertama bermasalah, dan mencari apa yang terlewat oleh agen pertama. Apa pun yang gagal dalam peninjauan dikerjakan ulang dan ditinjau kembali."
* **Apa yang harus dilakukan saat agen gagal:** "Satu agen yang gagal tidak boleh membuat eksekusi gagal. Jika agen gagal membaca sebuah kontrak, cantumkan kontrak tersebut sebagai tidak tercakup."
* **Batas waktu:** "Berikan eksekusi batas waktu satu jam."

Batasi eksekusi hanya untuk tugas-tugas yang memerlukannya, karena setiap agen dalam eksekusi menggunakan token.

Kemudian [buat sesi](https://platform.claude.com/docs/id/managed-agents/sessions) dengan agen tersebut, seperti yang Anda lakukan dengan agen mana pun, dan jelaskan pekerjaannya dalam `user.message`. Anda juga dapat meminta eksekusi dalam pesan tersebut.

Untuk event eksekusi, menginterupsi sesi dengan eksekusi yang masih terbuka, apa yang berubah selama eksekusi terbuka, serta anggaran dan batas, lihat [Eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs).

## Berikan advisor pada sesi

Pengaturan `advisor` yang aktif di blok `multiagent` milik agen memberikan thread utama sesi sebuah **advisor** (penasihat): model yang dapat dikonsultasikan di tengah giliran untuk panduan strategis, seperti merencanakan pendekatan, keluar dari kebuntuan, atau meninjau pekerjaan sebelum menyelesaikannya. Pengaturan ini nonaktif secara default. Untuk mengaktifkannya, atur `advisor` ke `{"type": "enabled", "model": "..."}`, yang memiliki tepat dua field, `type` dan `model`:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsS https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Backend engineer",
      "model": "claude-sonnet-5",
      "system": "You implement backend features end to end. Consult the advisor before major backend design decisions.",
      "multiagent": {
        "type": "multiagent_20261001",
        "advisor": {"type": "enabled", "model": "claude-opus-5-5"}
      }
    }'
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply backend-engineer.md
    ```

    <File filename="backend-engineer.md">
      ```markdown
      ---
      name: Backend engineer
      model: claude-sonnet-5
      multiagent:
        type: multiagent_20261001
        advisor:
          type: enabled
          model: claude-opus-5-5
      ---

      You implement backend features end to end. Consult the advisor before major backend design decisions.
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  agent = client.beta.agents.create(
      name="Backend engineer",
      model="claude-sonnet-5",
      system="You implement backend features end to end. Consult the advisor before major backend design decisions.",
      multiagent={
          "type": "multiagent_20261001",
          "advisor": {"type": "enabled", "model": "claude-opus-5-5"},
      },
  )
  print(agent.id)
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Backend engineer",
    model: "claude-sonnet-5",
    system:
      "You implement backend features end to end. Consult the advisor before major backend design decisions.",
    multiagent: {
      type: "multiagent_20261001",
      advisor: { type: "enabled", model: "claude-opus-5-5" },
    },
  });
  console.log(agent.id);
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Backend engineer",
      Model = BetaManagedAgentsModel.ClaudeSonnet5,
      System = "You implement backend features end to end. Consult the advisor before major backend design decisions.",
      Multiagent = new BetaManagedAgentsMultiagent20261001Params
      {
          Advisor = new BetaManagedAgentsMultiagentAdvisorEnabledParams { Model = "claude-opus-5-5" },
      },
  });
  Console.WriteLine(agent.ID);
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name:   "Backend engineer",
  	Model:  anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeSonnet5},
  	System: anthropic.String("You implement backend features end to end. Consult the advisor before major backend design decisions."),
  	Multiagent: anthropic.BetaManagedAgentsMultiagentParamsUnion{
  		OfMultiagent20261001: &anthropic.BetaManagedAgentsMultiagent20261001Params{
  			Advisor: anthropic.BetaManagedAgentsMultiagentAdvisorParamsUnion{
  				OfEnabled: &anthropic.BetaManagedAgentsMultiagentAdvisorEnabledParams{
  					Model: "claude-opus-5-5",
  				},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(agent.ID)
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Backend engineer")
          .model(BetaManagedAgentsModel.CLAUDE_SONNET_5)
          .system("You implement backend features end to end. Consult the advisor before major backend design decisions.")
          .multiagent(BetaManagedAgentsMultiagent20261001Params.builder()
              .advisor(BetaManagedAgentsMultiagentAdvisorEnabledParams.builder()
                  .model("claude-opus-5-5")
                  .build())
              .build())
          .build()
  );
  IO.println(agent.id());
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Backend engineer',
      model: 'claude-sonnet-5',
      system: 'You implement backend features end to end. Consult the advisor before major backend design decisions.',
      multiagent: [
          'type' => 'multiagent_20261001',
          'advisor' => ['type' => 'enabled', 'model' => 'claude-opus-5-5'],
      ],
  );
  echo $agent->id, PHP_EOL;
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Backend engineer",
    model: "claude-sonnet-5",
    system_: "You implement backend features end to end. Consult the advisor before major backend design decisions.",
    multiagent: {
      type: "multiagent_20261001",
      advisor: {type: "enabled", model: "claude-opus-5-5"}
    }
  )
  puts agent.id
  ```
</CodeGroup>

Contoh ini hanya mengatur `advisor`. Dua pengaturan lainnya, `subagents` dan `workflows`, mempertahankan nilai default-nya, sehingga keduanya aktif, dan agen juga dapat mendelegasikan ke agen inline serta memulai eksekusi workflow. Untuk agen yang berkonsultasi dengan advisor dan mengerjakan semua pekerjaan sendiri, atur keduanya ke `{"type": "disabled"}`.

Anda tidak dapat mencantumkan advisor di `subagents.predefined_agents` atau `workflows.predefined_agents`. `advisor` yang aktif mencadangkan nama `anthropic.advisor`. Selama advisor aktif, tidak satu pun dari kedua daftar tersebut dapat memuat agen yang secara harfiah bernama `anthropic.advisor`: permintaan akan ditolak dengan error validasi 400.

Model advisor harus memenuhi batas kemampuan minimum, dan model milik agen itu sendiri tidak boleh lebih mampu daripada advisor-nya; model dengan kemampuan yang setara dapat dipasangkan. Pasangan yang tidak valid ditolak dengan error validasi 400 saat agen disimpan, dan sekali lagi saat sesi dibuat. Pasangan tersebut juga diperiksa saat setiap konsultasi dimulai: jika sudah tidak valid, konsultasi tersebut gagal dan sesi tetap berlanjut. Pasangan yang valid mengikuti tabel [kompatibilitas model](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#model-compatibility) pada alat advisor.

Advisor juga tersedia sebagai [alat server di Messages API](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool). Permukaan Managed Agents berbeda dalam konfigurasi dan penyampaian: pengaturan `advisor` tidak memiliki field `max_uses`, `max_tokens`, atau `caching`, dan saran disampaikan melalui event thread, bukan blok `advisor_tool_result`.

### Cara kerja konsultasi

Setiap konsultasi berjalan sebagai thread yang dibuat oleh platform bernama `anthropic.advisor` yang menghentikan dirinya sendiri saat konsultasi selesai, dan saran disampaikan ke thread utama sebagai event `agent.thread_message_received`. Konsultasi memancarkan event thread standar, yang diidentifikasi dengan nama cadangan `anthropic.advisor` (event siklus hidup thread membawanya sebagai `agent_name`, dan penyampaian saran membawanya sebagai `from_agent_name`), biasanya dalam urutan berikut:

1. `session.thread_created`
2. `session.thread_status_running`
3. `agent.thread_message_received` (saran)
4. `session.thread_status_idle` (`stop_reason: end_turn`)
5. `session.thread_status_terminated`

Tidak ada event `agent.tool_use` yang dipancarkan untuk konsultasi, dan tidak ada event `agent.thread_message_sent` yang muncul di aliran event sesi, karena input konsultasi disusun oleh platform, bukan dikirim oleh agen. Jika Anda mencantumkan event milik thread advisor itu sendiri, saran juga muncul di sana sebagai event `agent.thread_message_sent`. Penyampaian saran (event 3) tidak dijamin tiba sebelum event idle dan terminated milik thread advisor, jadi jangan perlakukan event-event tersebut sebagai sinyal bahwa saran sudah disampaikan.

Apakah klien Anda dapat membaca saran bergantung pada kebijakan model advisor. Hal ini mencerminkan pembagian [varian hasil](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#result-variants) pada alat advisor di Messages API. Model advisor yang mengembalikan hasil plaintext di sana akan menyampaikan teks yang dapat dibaca di sini. Model yang mengembalikan hasil yang disunting (redacted) akan menyampaikan placeholder `[{"type": "redacted"}]` di setiap permukaan klien, sementara agen tetap membaca saran lengkap di sisi server. Contoh sebelumnya menggunakan model Opus terbaru yang tersedia bagi Anda sebagai advisor. Claude Opus 5 dan Claude Opus 5.5 mengembalikan hasil yang disunting, sehingga dengan salah satu dari keduanya klien Anda hanya melihat placeholder. Untuk membaca saran di aliran event, gunakan advisor yang mengembalikan plaintext, seperti Claude Opus 4.8. Kebijakan model dapat berubah tanpa perubahan pada API, jadi tangani blok `text` maupun `redacted`. Beberapa model agen hanya dapat dipasangkan dengan advisor yang mengembalikan hasil yang disunting; lihat [tabel kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#model-compatibility) alat advisor. Pemikiran advisor tidak pernah ditampilkan. Klien tidak dapat mengirim blok `redacted` sendiri; event yang memuat blok tersebut ditolak dengan error validasi 400.

Konsultasi yang gagal atau terinterupsi tidak pernah membuat giliran agen gagal: agen melanjutkan setelah pemberitahuan umum bahwa konsultasi gagal. `user.interrupt` tingkat sesi selama konsultasi akan menghentikan thread advisor tanpa saran yang disampaikan; `user.interrupt` dengan `session_thread_id` milik thread advisor hanya membatalkan konsultasi tersebut.

### Thread advisor

Advisor bukan subagen. Alat `list_agents` milik agen tidak menampilkannya, dan `send_to_agent`, yang mengirimkan pesan lanjutan ke subagen, tidak dapat menjangkaunya. Hanya thread utama sesi yang dapat berkonsultasi dengannya; subagen tidak dapat.

Thread advisor dikecualikan dari batas 25 thread anak. Thread ini muncul di [daftar thread](https://platform.claude.com/docs/id/managed-agents/session-threads) sesi. `agent`-nya berbentuk advisor, `{"type": "advisor", "model": ...}`, dengan model yang Anda konfigurasikan, dan `parent_thread_id`-nya adalah thread utama.

Caching prompt di sisi advisor berlangsung otomatis; tidak ada yang perlu dikonfigurasi. Konsultasi ditagih sesuai tarif model advisor, dan token-nya muncul di penggunaan thread advisor serta di total penggunaan sesi. Konsultasi juga dihitung terhadap [anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets), dengan harga daftar model advisor. Setiap konsultasi mengirimkan percakapan thread utama sejauh ini kepada advisor, sehingga konsultasi di akhir sesi yang panjang menggunakan lebih banyak token input.

### Menghapus advisor

Untuk menghapus advisor, [perbarui agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-an-agent) dengan `advisor` diatur ke `{"type": "disabled"}`. Pada agen yang sudah memiliki tipe `multiagent_20261001`, pengaturan yang tidak disertakan dalam pembaruan mempertahankan nilai tersimpannya, sehingga Anda tidak perlu mengirim `subagents` atau `workflows` lagi. Dengan alasan yang sama, pembaruan yang tidak menyertakan `advisor` akan mempertahankan advisor. Sebelum Anda mengubah `multiagent.type` milik agen yang sudah ada, lihat [cara memindahkan agen ke tipe ini](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#move-from-the-coordinator-type).

## Pindah dari tipe `coordinator`

Seperti `multiagent_20261001`, tipe `coordinator` memungkinkan agen mendelegasikan ke subagen yang Anda cantumkan dan berkonsultasi dengan model advisor. Dengan tipe `coordinator`, agen tidak dapat memulai eksekusi workflow atau mendefinisikan subagen sendiri. API menerima kedua tipe tersebut.

Untuk memindahkan agen ke `multiagent_20261001`, [perbarui agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-an-agent) dengan blok `multiagent` bertipe tersebut:

1. Atur `type` ke `"multiagent_20261001"`.
2. Cantumkan agen-agen yang dapat dipanggil oleh agen di `subagents.predefined_agents`. Entri-entrinya mempertahankan bentuk yang dimilikinya saat ini.
3. Jika agen memiliki advisor, atur `advisor` ke `{"type": "enabled", "model": "..."}` dengan model advisor tersebut.
4. Kirim seluruh blok dalam satu pembaruan.

Sebagai contoh, blok ini memberikan agen dua subagen dan satu advisor:

```json
{
  "multiagent": {
    "type": "multiagent_20261001",
    "subagents": {
      "type": "enabled",
      "predefined_agents": [
        { "type": "agent", "id": "agent_01J8XkN5uT3vHpLqRfWdY2" },
        { "type": "agent", "id": "agent_01HqR2k7vXbZ9mNpL3wYcT" }
      ]
    },
    "advisor": { "type": "enabled", "model": "claude-opus-5-5" }
  }
}
```

Blok tersebut tidak menyertakan `workflows` dan `subagents.inline_agents`, sehingga keduanya mengambil nilai default-nya dan aktif. Agen yang dipindahkan juga dapat memulai eksekusi workflow dan mendefinisikan subagen sendiri. Untuk menjaga salah satunya tetap nonaktif, atur ke `{"type": "disabled"}` dalam pembaruan yang sama. Lihat [Aktifkan alur kerja dinamis](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#turn-on-dynamic-workflows) dan [Agen predefined dan inline](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#predefined-and-inline-agents).

Jika agen memiliki advisor dan tidak memiliki subagen, atur `subagents` ke `{"type": "disabled"}` untuk menjaga pendelegasian tetap nonaktif. Permintaan yang menonaktifkan `subagents.inline_agents` dan tidak mencantumkan agen apa pun akan gagal dengan error 400.

Pembaruan menggantikan seluruh blok `multiagent`, jadi kirim kembali daftar agen dan advisor, seperti yang dilakukan contoh tersebut. Apa yang tidak Anda sertakan akan mengambil nilai default-nya:

* **`subagents.predefined_agents`:** Daftarnya kosong, sehingga agen kehilangan subagen yang telah Anda cantumkan.
* **`advisor`:** Advisor dinonaktifkan.

Setelah agen memiliki tipe `multiagent_20261001`, pengaturan yang tidak disertakan dalam pembaruan berikutnya mempertahankan nilai tersimpannya.

Pembaruan tidak mengubah sesi yang sudah ada. Untuk menggunakan blok yang baru, buat sesi setelah pembaruan.
