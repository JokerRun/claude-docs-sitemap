---
source: platform
url: https://platform.claude.com/docs/id/api/migration-2026-10-21
fetched_at: 2026-11-06T02:14:07.030986Z
sha256: 85940b2e23398005ef6f5aab1b861ad52fad8bffc0fe8daf22f8310ab99e74dd
---

---
title: Migrasi ke versi API 2026-10-21
url: https://platform.claude.com/docs/id/api/migration-2026-10-21
description: "Tingkatkan integrasi Claude API dari versi API 2023-06-01 ke 2026-10-21: versi SDK yang perlu dipasang dan perubahan kode yang perlu dilakukan."
---

Panduan ini mencantumkan perubahan kode untuk berpindah dari versi API `2023-06-01` ke `2026-10-21`. [Langkah-langkah peningkatan](https://platform.claude.com/docs/id/api/migration-2026-10-21#migration-checklist) menjelaskan apa yang harus dilakukan, secara berurutan.

Cara termudah untuk meningkatkan kode Anda

```text
/claude-api api-version
```

## Langkah-langkah peningkatan

<Steps>
  <Step title="Beralih ke 2026-10-21">
    Jika Anda menggunakan SDK, permintaan Anda menggunakan versi API yang berlaku saat versi mayor SDK Anda dirilis. Versi yang ditampilkan untuk bahasa Anda adalah versi pertama yang menggunakan `2026-10-21`, jadi tingkatkan ke versi tersebut. Jika Anda memanggil API tanpa SDK, atur header `anthropic-version` ke `2026-10-21`.

    <Tabs>
      <Tab title="cURL">
        Atur header `anthropic-version` ke `2026-10-21`:

        ```bash
        curl https://api.anthropic.com/v1/messages \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2026-10-21" \
          -H "content-type: application/json" \
          -d '{
            "model": "claude-opus-5-5",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Hello, Claude"}]
          }'
        ```
      </Tab>

      <Tab title="CLI">
        Tingkatkan CLI `ant` ke versi 2.0.0. Perintah Homebrew dan unduhan rilis tetap sama.

        Go mengharuskan path modul pada versi mayor 2 atau lebih baru diakhiri dengan versi tersebut, sehingga path modul CLI sekarang adalah `github.com/anthropics/anthropic-cli/v2`. Jika Anda menginstal dengan `go install`, tambahkan `/v2` ke path:

        ```bash
        # Sebelum
        go install 'github.com/anthropics/anthropic-cli/cmd/ant@latest'

        # Sesudah
        go install 'github.com/anthropics/anthropic-cli/v2/cmd/ant@latest'
        ```

        Path lama tetap menginstal rilis v1 terbaru, tanpa error atau peringatan.
      </Tab>

      <Tab title="Python">
        Tingkatkan paket `anthropic` ke versi 2.0.0.
      </Tab>

      <Tab title="TypeScript">
        Tingkatkan paket `@anthropic-ai/sdk` ke versi 1.0.0.

        v1 dari `@anthropic-ai/bedrock-sdk`, `@anthropic-ai/vertex-sdk`, `@anthropic-ai/foundry-sdk`, `@anthropic-ai/aws-sdk`, dan `@anthropic-ai/google-cloud-sdk` memerlukan v1 dari `@anthropic-ai/sdk`, dan versi-versi sebelumnya memerlukan versi di bawah 1. Jika Anda menggunakan salah satunya, pindahkan ke v1 dalam peningkatan yang sama. Jika tidak, manajer paket Anda akan menginstal salinan kedua `@anthropic-ai/sdk` yang lebih lama untuknya.
      </Tab>

      <Tab title="C#">
        Tingkatkan paket `Anthropic` ke versi 13.0.0.

        Versi 1.0.0 dari `Anthropic.Bedrock`, `Anthropic.Vertex`, `Anthropic.Foundry`, `Anthropic.Aws`, `Anthropic.GoogleCloud`, dan `Anthropic.Mcp` memerlukan versi 13.0.0 dari `Anthropic`. Jika Anda menggunakan salah satunya, pindahkan ke 1.0.0 dalam peningkatan yang sama. Versi sebelumnya masih terinstal di samping 13.0.0, tetapi dapat gagal saat dijalankan.
      </Tab>

      <Tab title="Go">
        Tingkatkan ke versi 2.0.0 dari Go SDK, yang path modulnya adalah `github.com/anthropics/anthropic-sdk-go/v2`. Versi mayor baru dari modul Go memiliki path impor baru, jadi ubah setiap impor `github.com/anthropics/anthropic-sdk-go`, dan paket-paketnya seperti `github.com/anthropics/anthropic-sdk-go/option`, agar diawali dengan `github.com/anthropics/anthropic-sdk-go/v2`. Kemudian jalankan `go get github.com/anthropics/anthropic-sdk-go/v2`.
      </Tab>

      <Tab title="Java">
        Tingkatkan artefak `com.anthropic:anthropic-java` ke versi 3.0.0.

        Versi 3.0.0 dari `anthropic-java-bedrock`, `anthropic-java-vertex`, `anthropic-java-aws`, `anthropic-java-foundry`, `anthropic-java-google-cloud`, dan `anthropic-java-mcp` dipasangkan dengan `anthropic-java` 3.0.0. Jika Anda menggunakan salah satunya, pindahkan ke 3.0.0 dalam peningkatan yang sama.
      </Tab>

      <Tab title="PHP">
        Jalankan `composer require "anthropic-ai/sdk"` untuk meningkatkan paket ke versi 1.0.0. `composer update` saja tetap berada dalam batasan versi Anda saat ini.
      </Tab>

      <Tab title="Ruby">
        Tingkatkan gem `anthropic` ke versi 2.0.0.
      </Tab>
    </Tabs>

    <Warning>
      Di Amazon Bedrock, `2026-10-21` hanya tersedia untuk model Claude 4.7 dan yang lebih baru. Jika Anda memanggil model lama di Bedrock, yang tercantum dalam [Claude di Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), tetaplah pada versi SDK yang Anda gunakan saat ini, atau, jika Anda mengatur versi API sendiri, tetap kirim versi yang Anda kirim saat ini. Untuk memindahkan panggilan tersebut ke `2026-10-21`, alihkan terlebih dahulu ke model Claude 4.7 atau yang lebih baru.
    </Warning>

    Rilis peningkatan ini bersamaan dengan perbaikan Anda dari langkah berikutnya.
  </Step>

  <Step title="Perbarui kode Anda untuk perubahan yang merusak kompatibilitas">
    Telusuri [“breaking changes” (perubahan yang merusak kompatibilitas)](https://platform.claude.com/docs/id/api/migration-2026-10-21#breaking-changes), dan perbarui kode Anda untuk setiap perubahan yang memengaruhi Anda. Lakukan juga [perubahan kode yang diperlukan oleh versi SDK atau CLI baru](https://platform.claude.com/docs/id/api/migration-2026-10-21#sdk-changes).
  </Step>

  <Step title="Uji terhadap 2026-10-21">
    Uji integrasi Anda terhadap `2026-10-21` sebelum Anda merilis.
  </Step>
</Steps>

## Perubahan yang merusak kompatibilitas

### Messages API

Perubahan ini berlaku untuk permintaan ke Messages API (`POST /v1/messages`), untuk [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting), dan untuk setiap permintaan dalam [Message Batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) yang dibuat dengan `2026-10-21`.

#### Blok dokumen dalam pesan assistant mengembalikan error

Memengaruhi Anda jika Anda mengirim blok `document` secara langsung dalam pesan `assistant`.

Di `2026-10-21`, permintaan yang menempatkan blok `document` secara langsung dalam pesan `assistant` mengembalikan error 400. Kirim dokumen dalam pesan `user` sebagai gantinya. Dokumen yang bersarang di dalam blok lain, seperti hasil alat web fetch yang dikembalikan Claude, tetap diterima.

#### Sitasi dalam pesan user mengembalikan error

Memengaruhi Anda jika Anda mengirim `citations` pada blok `text` dalam pesan `user`, termasuk di dalam blok `search_result`.

Di `2026-10-21`, permintaan yang mengirim blok `text` dengan array `citations` yang tidak kosong dalam pesan `user` mengembalikan error 400. Hapus `citations` dari blok-blok tersebut. Sitasi pada blok `text` dalam pesan `assistant`, seperti balasan Claude sebelumnya yang Anda kirim kembali, tetap diterima, begitu pula pengaturan `"citations": {"enabled": true}` pada dokumen dan hasil pencarian.

#### Parameter sampling dihapus

Memengaruhi Anda jika Anda mengirim `temperature`, `top_p`, atau `top_k` dalam permintaan Messages atau permintaan Message Batch.

Di `2026-10-21`, permintaan yang mengirim `temperature`, `top_p`, atau `top_k` mengembalikan error 400, bahkan pada nilai default parameter tersebut.

Hapus ketiga parameter tersebut dari permintaan Anda.

Sejak versi mayor terbaru, SDK dan CLI tidak lagi memiliki ketiga parameter tersebut.

Tanpa parameter ini, permintaan melakukan sampling dengan nilai default-nya, termasuk `temperature` sebesar 1.0, sama seperti permintaan `2023-06-01` yang tidak menyertakannya. Model yang sudah hanya menerima nilai default, seperti model Claude 4.7 dan yang lebih baru, melakukan sampling seperti sebelumnya. Pada model yang menerima nilai lain, seperti Claude Sonnet 4.6, permintaan yang menurunkan `temperature` untuk output yang lebih konsisten kehilangan efek tersebut. Tidak ada pengaturan lain yang menggantikannya. Jika suatu permintaan bergantung pada nilai non-default, hentikan pengiriman parameter tersebut, atau pertahankan permintaan itu pada `2023-06-01`.

### Admin API dan Claude Enterprise Analytics API

Memengaruhi Anda jika kode Anda membaca field respons Admin API atau Claude Enterprise Analytics API dalam tabel berikut.

Di `2026-10-21`, respons dari Admin API dan [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api) tidak lagi menyertakan nama lama dari field yang diganti namanya. Gunakan nama baru sebagai gantinya.

Admin API:

| Endpoint                                                                                                                                                                                                                                                                                                                                          | Nama lama      | Nama baru                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Grup RBAC](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/list): pembuatan, daftar, pengambilan, dan pembaruan                                                                                                                                                                                                            | `roles`        | `role_ids`                                                                                                                                        |
| [Anggota grup RBAC](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/members/list): daftar dan penambahan, serta respons untuk [menghapus anggota](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/members/remove)                                                                                     | `group_id`     | `rbac_group_id`                                                                                                                                   |
| [Peran RBAC](https://platform.claude.com/docs/id/api/beta/organization/rbac_roles/list): daftar dan pengambilan                                                                                                                                                                                                                                   | `name`         | `display_name`                                                                                                                                    |
| Batas laju [organisasi](https://platform.claude.com/docs/id/api/organization/rate_limits/list) dan [workspace](https://platform.claude.com/docs/id/api/organization/workspaces/rate_limits/list): daftar, serta respons untuk [mengatur batas laju workspace](https://platform.claude.com/docs/id/api/organization/workspaces/rate_limits/update) | `group_type`   | `group.type`                                                                                                                                      |
| [Kunci API](https://platform.claude.com/docs/id/api/organization/api_keys/list): daftar, pengambilan, dan pembaruan                                                                                                                                                                                                                               | `workspace_id` | `scope` (nilai berbeda; lihat [`workspace_id` pada kunci API](https://platform.claude.com/docs/id/api/migration-2026-10-21#api-key-workspace-id)) |

Claude Enterprise Analytics API:

| Endpoint                                                                                                                                                                                                                             | Nama lama     | Nama baru             |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------- | --------------------- |
| Laporan [penggunaan](https://platform.claude.com/docs/id/api/beta/organization/analytics/user_usage_report/list) dan [biaya](https://platform.claude.com/docs/id/api/beta/organization/analytics/user_cost_report/list) per pengguna | `actor.email` | `actor.email_address` |
| [Ringkasan aktivitas](https://platform.claude.com/docs/id/api/beta/organization/analytics/summaries/list)                                                                                                                            | `summaries`   | `data`                |

Parameter query `group_type` pada endpoint list batas laju dan filter `workspace_id` pada endpoint list kunci API tidak berubah.

#### `workspace_id` pada kunci API

Memengaruhi Anda jika kode Anda membaca `workspace_id` pada kunci API.

Di `2023-06-01`, `workspace_id` dari kunci API adalah ID workspace tempat kunci tersebut terikat, atau `null` untuk kunci yang terikat ke workspace default dan untuk kunci yang tidak terikat ke satu workspace (kunci semua workspace).

Di `2026-10-21`, `workspace_id` dihapus. Baca `scope` sebagai gantinya: untuk kunci yang terikat ke workspace, termasuk workspace default, `scope.workspace_id` adalah ID sebenarnya dari workspace tersebut, dan kunci semua workspace memiliki `scope` berupa `{"type": "organization"}`, tanpa `workspace_id`.

Jika kode Anda memperlakukan `workspace_id` yang bernilai `null` sebagai workspace default, bandingkan `scope.workspace_id` dengan ID workspace default Anda sebagai gantinya. Untuk menemukan ID tersebut, panggil [Daftar Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/list) dengan `include_default=true` dan ambil workspace bernama `"Default"`.

## Perubahan SDK dan CLI

Versi SDK dan CLI sebelumnya mengirim `anthropic-version: 2023-06-01` pada setiap permintaan. Versi di bawah [Beralih ke 2026-10-21](https://platform.claude.com/docs/id/api/migration-2026-10-21#upgrade) mengirim `2026-10-21`, termasuk klien Amazon Bedrock dan Google Cloud mereka. Perubahan dalam [Perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/api/migration-2026-10-21#breaking-changes) juga berlaku untuk versi tersebut: parameter yang dihapus dan nama field lama juga hilang dari tipe SDK serta dari flag dan output CLI.

### `MessageParam` adalah union dengan satu tipe untuk setiap peran

Pada versi sebelumnya, `MessageParam` adalah satu tipe untuk semua peran. Setiap peran kini memiliki tipenya sendiri: `UserMessageParam`, `AssistantMessageParam`, dan `SystemMessageParam`. `BetaMessageParam` dipecah dengan cara yang sama, menjadi `BetaUserMessageParam`, `BetaAssistantMessageParam`, dan `BetaSystemMessageParam`. Permintaan yang dikirim SDK memiliki field dan nilai yang sama seperti sebelumnya.

<Tabs exclude="shell">
  <Tab title="Python">
    Pesan yang ditulis sebagai literal dict, seperti `{"role": "user", "content": "Hello"}`, tidak memerlukan perubahan.

    Di v1, `anthropic.types.MessageParam` adalah satu `TypedDict`. Di v2 ia adalah union dari ketiga tipe tersebut, dan `anthropic.types.beta.BetaMessageParam` adalah union dari ketiga tipenya. Kedua nama tersebut masih berfungsi dalam anotasi, seperti `list[MessageParam]`.

    Memanggil salah satu nama tersebut kini memunculkan `TypeError`, dan pemeriksa tipe menandainya. Tulis pesan sebagai dict:

    ```python
    # Sebelum
    message = MessageParam(role="user", content="Hello")

    # Sesudah
    message: MessageParam = {"role": "user", "content": "Hello"}
    ```

    Membuat subclass dari salah satu nama tersebut juga memunculkan `TypeError`. Buat subclass dari tipe untuk peran tersebut, seperti `UserMessageParam`.

    Perubahan lainnya hanya memengaruhi pemeriksaan tipe. Dict yang `role`-nya berupa variabel yang dapat menampung lebih dari satu peran tidak cocok dengan tipe mana pun dalam union, jadi buat dict untuk satu peran pada satu waktu:

    ```python
    # Sebelum
    def to_message(role: Literal["user", "assistant"], text: str) -> MessageParam:
        return {"role": role, "content": text}


    # Sesudah
    def to_message(role: Literal["user", "assistant"], text: str) -> MessageParam:
        if role == "user":
            return {"role": "user", "content": text}
        return {"role": "assistant", "content": text}
    ```

    Dua perubahan lagi hanya berlaku untuk `BetaMessageParam`:

    * `clear_at` dan `output_config` adalah key dari `BetaSystemMessageParam`, sehingga pesan user atau assistant tidak dapat memilikinya.
    * `content` bersifat opsional di `BetaSystemMessageParam`, sehingga pyright melaporkan `message["content"]`. Bacalah dengan `message.get("content")`, atau periksa terlebih dahulu bahwa `message["role"]` bukan `"system"`.
  </Tab>

  <Tab title="TypeScript">
    `MessageParam` dahulu adalah satu interface. Sekarang ia adalah `UserMessageParam | AssistantMessageParam | SystemMessageParam`, dan `BetaMessageParam` adalah union yang sama dari ketiga tipenya. Hanya tipenya yang berubah. Literal pesan yang menyebutkan perannya, seperti `{ role: "user", content: "Hello, Claude" }`, lolos pemeriksaan tipe seperti sebelumnya, sehingga sebagian besar kode tidak memerlukan perubahan.

    Tipe system berbeda dari dua lainnya. `content`-nya berupa string atau blok teks, ditambah blok `tool_addition` dan `tool_removal` di `beta`, sehingga blok gambar di sana tidak lagi dapat dikompilasi. Di `beta`, hanya tipe ini yang memiliki `clear_at` dan `output_config`, dan `content`-nya bersifat opsional.

    Kode yang menangani pesan dengan peran apa pun harus memeriksa `role` sebelum mengganti atau menambahkan blok konten, dan sebelum membaca `clear_at` atau `output_config`:

    ```typescript
    // Sebelum
    const copy: Anthropic.MessageParam = { ...message, content: blocks };

    // Sesudah
    const copy: Anthropic.MessageParam =
      message.role === "system" ? message : { ...message, content: blocks };
    ```

    `content` dari `BetaMessageParam` dapat bernilai `undefined`:

    ```typescript
    // Sebelum
    const types =
      typeof message.content === "string" ? [] : message.content.map((block) => block.type);

    // Sesudah
    const types = Array.isArray(message.content) ? message.content.map((block) => block.type) : [];
    ```

    Tipe `BetaMessageParam["content"]` juga mencakup `undefined`. Untuk konten pesan user atau assistant, gunakan `BetaMessageContentParam`.

    Interface tidak dapat meng-extend union, dan class tidak dapat mengimplementasikannya. Gunakan alias tipe, atau sebutkan tipe untuk satu peran saja.

    ```typescript
    // Sebelum
    interface StoredMessage extends Anthropic.MessageParam {
      id: string;
    }

    // Sesudah
    type StoredMessage = Anthropic.MessageParam & { id: string };
    ```
  </Tab>

  <Tab title="C#">
    Di v12, `MessageParam` dan `BetaMessageParam` adalah class yang `Role` dan `Content`-nya Anda atur. Di v13 masing-masing adalah union dari tiga class untuk perannya, dan enum `Role` di `Anthropic.Models.Messages` dan `Anthropic.Models.Beta.Messages` telah dihapus.

    Saat Anda membuat pesan, sebutkan class untuk perannya dan hapus `Role`. Setiap class dikonversi ke union secara implisit:

    ```csharp
    // Sebelum
    Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],

    // Sesudah
    Messages = [new UserMessageParam { Content = "Hello, Claude" }],
    ```

    `new UserMessageParam("Hello, Claude")` juga berfungsi.

    Class yang menampung `Content` juga berubah:

    * `MessageParamContent` sekarang menjadi `MessageContentParam`, dan `BetaMessageParamContent` sekarang menjadi `BetaMessageContentParam`.
    * Pesan system memiliki class kontennya sendiri. `SystemMessageParamContent` menampung string atau daftar `TextBlockParam`, dan `BetaSystemMessageParamContent` menampung string atau daftar `SystemMessageContentBlock`. `List<ContentBlockParam>` atau `List<BetaContentBlockParam>` tidak lagi dikonversi ke sana.
    * `ClearAt` dan `OutputConfig` hanya ada di `BetaSystemMessageParam`.

    Saat Anda membaca pesan, union tersebut masih memiliki `Role` dan `Content`, tetapi Anda tidak dapat mengaturnya, sehingga ekspresi `with` diterapkan pada class untuk perannya. `Role` sekarang menampung `MessageParamRole` atau `BetaMessageParamRole`. `BetaMessageParam.Content` dapat bernilai `null`, karena `Content` bersifat opsional di `BetaSystemMessageParam`.

    ```csharp
    // Sebelum
    if (message.Role.Value() == Role.Assistant) { }

    // Sesudah
    if (message.Role.Value() == MessageParamRole.Assistant) { }
    ```

    `TryPickUser`, `TryPickAssistant`, `TryPickSystem`, `Switch`, dan `Match` memberi Anda class untuk peran tersebut.
  </Tab>

  <Tab title="Go">
    Di v1, `MessageParam` adalah satu struct dengan field `Role` dan `Content`. Di v2 ia adalah union: `OfUser` menampung `*UserMessageParam`, `OfAssistant` menampung `*AssistantMessageParam`, dan `OfSystem` menampung `*SystemMessageParam`. `BetaMessageParam` berubah dengan cara yang sama. SDK mengirim JSON yang sama seperti sebelumnya, kecuali urutan key dalam pesan system beta.

    `NewUserMessage`, `NewAssistantMessage`, `NewBetaUserMessage`, dan metode `ToParam` dari `Message` dan `BetaMessage` berfungsi seperti sebelumnya, sehingga kode yang membuat pesannya dengan fungsi-fungsi tersebut tidak memerlukan perubahan.

    Literal struct menyebutkan tipe untuk perannya. Jangan sertakan `Role`, karena setiap tipe melakukan marshal perannya sendiri:

    ```go
    // Sebelum
    anthropic.MessageParam{
    	Role:    anthropic.MessageParamRoleAssistant,
    	Content: blocks,
    }

    // Sesudah
    anthropic.MessageParam{OfAssistant: &anthropic.AssistantMessageParam{
    	Content: blocks,
    }}
    ```

    Kode yang membaca pesan memeriksa field mana yang diatur:

    ```go
    // Sebelum
    if message.Role == anthropic.MessageParamRoleUser {
    	blocks = message.Content
    }

    // Sesudah
    if message.OfUser != nil {
    	blocks = message.OfUser.Content
    }
    ```

    * Tipe `MessageParamRole` dan `BetaMessageParamRole` beserta konstantanya telah dihapus. `message.GetRole()` mengembalikan pointer ke peran sebagai `string`, atau `nil` jika tidak ada field yang diatur.
    * `ClearAt` dan `OutputConfig` dipindahkan dari `BetaMessageParam` ke `BetaSystemMessageParam`. Nama tipe `BetaMessageParamClearAt` dan konstantanya sekarang diawali dengan `BetaSystemMessageParamClearAt`.
    * `SystemMessageParam.Content` adalah `[]TextBlockParam`. `BetaSystemMessageParam.Content` adalah `[]BetaSystemMessageParamContentUnion`, yang menampung blok `text`, `tool_addition`, dan `tool_removal`. `NewBetaSystemMessage` menerima blok dengan tipe tersebut, sehingga `anthropic.NewBetaTextBlock("Be brief.")` menjadi `anthropic.BetaSystemMessageParamContentUnion{OfText: &anthropic.BetaTextBlockParam{Text: "Be brief."}}`.
    * Salinan `MessageParam` menunjuk ke pesan yang sama dengan aslinya. Mengatur `duplicate.OfUser.Content` mengubah keduanya, sedangkan mengatur `duplicate.Content` di v1 hanya mengubah salinannya.
    * `mcp.ToMessage` mengembalikan `*mcp.UnsupportedValueError` untuk peran selain `user` atau `assistant`. v1 menyalin peran apa pun ke dalam pesan.
  </Tab>

  <Tab title="Java">
    Di v2, `MessageParam` adalah satu class dengan `role` dan `content`. Di v3 ia adalah union dari tiga class, dan `MessageParam.Content` sekarang menjadi `MessageContentParam` tingkat atas. `BetaMessageParam` berubah dengan cara yang sama, dan class-classnya memiliki nama yang sama dengan awalan `Beta`. JSON yang dikirim SDK sama, kecuali bahwa pesan system beta sekarang memiliki `role` sebelum `content`.

    `addUserMessage`, `addAssistantMessage`, dan `addSystemMessage` dengan `String`, `addMessage` dengan `Message` atau `MessageParam`, serta `Message.toParam()` tidak berubah.

    `MessageParam.builder()` dan `toBuilder()` telah dihapus. Panggil metode factory untuk perannya, yaitu `ofUser`, `ofAssistant`, atau `ofSystem`:

    ```java
    // Sebelum
    MessageParam message = MessageParam.builder()
        .role(MessageParam.Role.USER)
        .content("Hello, Claude")
        .build();

    // Sesudah
    MessageParam message = MessageParam.ofUser("Hello, Claude");
    ```

    Metode yang menerima daftar blok konten memiliki nama baru pada builder dari `MessageCreateParams`, `StructuredMessageCreateParams`, `MessageCountTokensParams`, dan `BatchCreateParams.Request.Params`:

    | v2                                 | v2 beta                                       | v3                                        |
    | ---------------------------------- | --------------------------------------------- | ----------------------------------------- |
    | `addUserMessageOfBlockParams`      | `addUserMessageOfBetaContentBlockParams`      | `addUserMessageOfContentBlockParams`      |
    | `addAssistantMessageOfBlockParams` | `addAssistantMessageOfBetaContentBlockParams` | `addAssistantMessageOfContentBlockParams` |
    | `addSystemMessageOfBlockParams`    | `addSystemMessageOfBetaContentBlockParams`    | `addSystemMessageOfBlocks`                |

    Pada class konten, `BlockParams` (`BetaContentBlockParams` di beta) menjadi `ContentBlockParams` di `ofBlockParams`, `blockParams()`, `isBlockParams()`, `asBlockParams()`, dan `visitBlockParams` milik visitor.

    Pesan system memiliki class kontennya sendiri, `SystemMessageParam.Content`, yang sekarang diterima oleh `addSystemMessage`. Bloknya adalah `TextBlockParam`, bukan `ContentBlockParam`. Di beta, bloknya adalah `BetaSystemMessageParam.Content.SystemMessageContentBlock`, yang memiliki `ofText`, `ofToolAddition`, dan `ofToolRemoval`.

    ```java
    // Sebelum
    builder.addSystemMessageOfBlockParams(List.of(ContentBlockParam.ofText(textBlock)));

    // Sesudah
    builder.addSystemMessageOfBlocks(List.of(textBlock));
    ```

    Saat Anda membaca pesan, `role()` tidak berubah. `content()` mengembalikan `MessageContentParam`, atau `Optional<BetaMessageContentParam>` di beta, di mana pesan system dapat tidak memiliki konten. `_role()`, `_content()`, dan `_additionalProperties()` sekarang berada pada class untuk perannya, yang dikembalikan oleh `asUser()`, `asAssistant()`, atau `asSystem()`.
  </Tab>

  <Tab title="PHP">
    Class-classnya berada di `Anthropic\Messages`, dan class beta di `Anthropic\Beta\Messages`. Pesan yang Anda tulis sebagai array tidak berubah, dan masih memerlukan `'role'`-nya.

    `MessageParam::with()` dan `BetaMessageParam::with()` tetap ada, dan mengembalikan class yang sesuai dengan `role`. Panggilan dengan argumen bernama tidak memerlukan perubahan. `role` sekarang menjadi parameter pertama, jadi dalam panggilan posisional tukar `content` dan `role`, atau panggil `with()` pada class peran tersebut, yang tidak menerima `role`. Untuk argumen dengan urutan lama, PHP melempar `UnhandledMatchError`, yang tidak diperingatkan oleh PHPStan, atau `TypeError` jika `content` berupa daftar atau `role` berupa enum case.

    ```php
    // Sebelum
    MessageParam::with('Hello, Claude', 'user');

    // Sesudah
    UserMessageParam::with('Hello, Claude');
    ```

    Tidak ada lagi objek yang merupakan `MessageParam`: `instanceof MessageParam` bernilai false, dan PHP melempar `TypeError` di mana tipe parameter atau tipe kembalian menyebutkannya. Sebutkan ketiga class tersebut sebagai gantinya:

    ```php
    // Sebelum
    function send(MessageParam $message): void {}

    // Sesudah
    function send(UserMessageParam|AssistantMessageParam|SystemMessageParam $message): void {}
    ```

    * `MessageParam::fromArray()` dan `(new MessageParam())->withContent()` melempar “Call to undefined method”. Panggil keduanya pada class peran tersebut, yang mengatur `role` sendiri.
    * `withRole()` sekarang hanya menerima string: PHP melempar `TypeError` untuk case `Role`. Untuk memberi pesan peran lain, buat class peran tersebut.
    * `clearAt` dan `outputConfig` hanya ada di `BetaSystemMessageParam`, dan `BetaMessageParam::with()` membuangnya untuk dua peran lainnya. Enum `BetaMessageParam\ClearAt` sekarang menjadi `BetaSystemMessageParam\ClearAt`.
    * `MessageParam\Content` sekarang menjadi `MessageContentParam`, dan `BetaMessageParam\Content` sekarang menjadi `BetaMessageContentParam`. Tipe PHPStan-nya juga menggunakan nama baru: `ContentShape` sekarang menjadi `MessageContentParamShape`.
    * Array yang `'role'`-nya berupa case `Role` masih berfungsi, tetapi PHPStan sekarang melaporkannya. Tulis string-nya.
  </Tab>

  <Tab title="Ruby">
    Pesan yang Anda tulis sebagai hash tidak berubah.

    Di v2, `Anthropic::MessageParam` adalah union dari `Anthropic::UserMessageParam`, `Anthropic::AssistantMessageParam`, dan `Anthropic::SystemMessageParam`. Dengan cara yang sama, `Anthropic::Beta::BetaMessageParam` adalah union dari ketiga class-nya.

    `Anthropic::MessageParam.new(role: :user, content: "Hello, Claude")` masih berfungsi, dan mengembalikan instance dari class untuk peran tersebut. Anda juga dapat membuat class tersebut sendiri, tanpa `role:`, sebagai `Anthropic::UserMessageParam.new(content: "Hello, Claude")`. Empat hal berubah untuk kode yang membuat atau memeriksa instance ini:

    * `MessageParam.new` hanya menerima keyword, jadi teruskan hash sebagai `MessageParam.new(**hash)`. Ia memunculkan `ArgumentError` ketika `role:` tidak ada atau bukan salah satu dari ketiga peran tersebut.
    * `message.is_a?(Anthropic::MessageParam)` bernilai `false`. Cabang `when Anthropic::MessageParam` dan `messages.grep(Anthropic::MessageParam)` masih cocok.
    * Instance yang dibuat dengan `.new` tidak memiliki `:role` dalam `to_h`-nya, dan `message[:role]` bernilai `nil`. `message.role` masih mengembalikan perannya.
    * Hanya `BetaSystemMessageParam` yang memiliki `clear_at` dan `output_config`. Pada pesan user atau assistant, keduanya dahulu mengembalikan `nil`, dan sekarang memunculkan `NoMethodError`.

    ```ruby
    # Sebelum
    typed = messages.select { _1.is_a?(Anthropic::MessageParam) }
    roles = typed.map { _1[:role] }

    # Sesudah
    typed = messages.grep(Anthropic::MessageParam)
    roles = typed.map(&:role)
    ```

    Modul enum `Role` tetap ada. Konstanta-konstanta berikut dipindahkan. Nama yang diawali dengan `Beta` berada di bawah `Anthropic::Beta`, dan yang lainnya berada di bawah `Anthropic`:

    | Dihapus                     | Gunakan sebagai gantinya                                                             |
    | --------------------------- | ------------------------------------------------------------------------------------ |
    | `MessageParam::Content`     | `MessageContentParam`, atau `SystemMessageParam::Content` untuk pesan system         |
    | `BetaMessageParam::Content` | `BetaMessageContentParam`, atau `BetaSystemMessageParam::Content` untuk pesan system |
    | `BetaMessageParam::ClearAt` | `BetaSystemMessageParam::ClearAt`                                                    |

    Jika Anda melakukan pemeriksaan tipe dengan Sorbet, `MessageParam::OrHash` telah dihapus, dan `Anthropic::MessageParam` sebagai tipe tidak lagi menerima instance. Gunakan `Anthropic::MessageParam::Variants` untuk ketiga class tersebut, yang masing-masing memiliki `OrHash` sendiri. Di RBS, nilai bertipe `Anthropic::MessageParam` tidak memiliki `role` atau `content`. Gunakan alias `Anthropic::Models::message_param`, yang dahulu merupakan bentuk hash dari pesan dan sekarang merupakan union dari ketiga class tersebut. Nama beta-nya adalah `BetaMessageParam::Variants` dan `Anthropic::Models::Beta::beta_message_param`.
  </Tab>
</Tabs>

### Enum bernilai tunggal menjadi konstanta

Ini memengaruhi SDK C#, Go, Java, PHP, dan Ruby serta satu flag CLI. Pada versi sebelumnya, field wajib yang hanya dapat menampung satu nilai memiliki tipe enum sendiri dengan satu anggota. Field-field ini sekarang menjadi konstanta, dan tipe enum tersebut telah dihapus. JSON yang dikirim dan dibaca SDK tetap sama.

<Tabs exclude="shell:cURL, python, typescript">
  <Tab title="CLI">
    `--type` bersifat opsional pada `ant beta:sessions:resources add`. `file` adalah satu-satunya nilai yang dapat diterima `--type` di sana, sehingga v2 mengirimkannya untuk Anda. Perintah yang masih meneruskan `--type file` tetap berfungsi, jadi tidak ada yang perlu diubah.
  </Tab>

  <Tab title="C#">
    Di v12, properti `required` semacam itu memiliki enum dengan satu anggota, seperti `BetaManagedAgentsTextBlockType.Text`. Hampir semuanya adalah properti `Type` dari class di bawah `Anthropic.Models.Beta`: `Agents`, `DeploymentRuns`, `Deployments`, `Dreams`, `Environments`, `MemoryStores`, `Sessions`, `UserProfiles`, dan `Vaults`. Di v13, properti-properti ini berupa `JsonElement` yang diisi oleh constructor, seperti `TextBlockParam.Type` sebelumnya.

    Properti opsional, seperti `BetaManagedAgentsGlobToolConfigParams.Type`, tetap mempertahankan enum-nya. Dua dari enum tersebut memiliki nama baru:

    | v12                                         | v13                                       |
    | ------------------------------------------- | ----------------------------------------- |
    | `BetaManagedAgentsBashToolConfigParamsType` | `Anthropic.Models.Beta.Agents.Type`       |
    | `BetaPackagesType`                          | `Anthropic.Models.Beta.Environments.Type` |

    Saat Anda membuat objek, hapus properti tersebut:

    ```csharp
    // Sebelum
    new BetaManagedAgentsTextBlock
    {
        Type = BetaManagedAgentsTextBlockType.Text,
        Text = "Hello Claude!",
    };

    // Sesudah
    new BetaManagedAgentsTextBlock { Text = "Hello Claude!" };
    ```

    Class yang tersisa dengan satu properti wajib juga mendapatkan constructor yang menerimanya, sehingga `new BetaManagedAgentsTextBlock("Hello Claude!")` juga berfungsi. Class yang tidak tersisa properti wajib apa pun dibuat dengan `new BetaManagedAgentsAlwaysAllowPolicy()`.

    Saat Anda membacanya, bandingkan string-nya:

    ```csharp
    // Sebelum
    if (message.Type.Value() == BetaManagedAgentsAgentMessageEventType.AgentMessage) { }

    // Sesudah
    if (message.Type.GetString() == "agent.message") { }
    ```

    Untuk membedakan varian-varian dari union, tetap gunakan method `TryPick*`, `Switch`, dan `Match`-nya, yang tidak berubah.
  </Tab>

  <Tab title="Go">
    Contoh tipe enum semacam itu beserta konstantanya adalah `BetaManagedAgentsTextBlockType` dan `BetaManagedAgentsTextBlockTypeText`. Hampir semuanya adalah field `Type` dari struct di bawah `client.Beta`: Agents, Deployments, Deployment Runs, Dreams, Environments, Memory Stores, Sessions, User Profiles, dan Vaults. Di v2, field-field ini menggunakan tipe dari paket `shared/constant`, seperti `TextBlockParam.Type` sebelumnya. Field opsional, seperti `BetaManagedAgentsBashToolConfigParams.Type`, tetap mempertahankan enum-nya.

    Dalam permintaan, hapus field tersebut. Field ini di-marshal sebagai satu-satunya nilainya ketika Anda menghilangkannya:

    ```go
    // Sebelum
    anthropic.BetaManagedAgentsTextBlockParam{
    	Type: anthropic.BetaManagedAgentsTextBlockTypeText,
    	Text: "Hello Claude!",
    }

    // Sesudah
    anthropic.BetaManagedAgentsTextBlockParam{
    	Text: "Hello Claude!",
    }
    ```

    Struct yang satu-satunya field-nya adalah `Type` tersebut sekarang memiliki constructor, seperti `NewBetaManagedAgentsAlwaysAllowPolicyParam()`. Sebagai anggota union, pointer ke struct kosong juga berfungsi: `OfAlwaysAllow: &anthropic.BetaManagedAgentsAlwaysAllowPolicyParam{}`.

    Dalam respons, bandingkan dengan string:

    ```go
    // Sebelum
    switch event.Type {
    case string(anthropic.BetaManagedAgentsAgentMessageEventTypeAgentMessage):
    }

    // Sesudah
    switch event.Type {
    case "agent.message":
    }
    ```

    Variabel, field, atau parameter milik Anda yang dideklarasikan dengan salah satu tipe yang dihapus menggunakan tipe baru dari field tersebut, seperti `constant.AgentMessage`. `constant.ValueOf[constant.AgentMessage]()` mengembalikan nilainya.

    Constructor union berubah seiring dengan field-field tersebut. Lima constructor berikut kehilangan argumen `type_`-nya:

    * `BetaManagedAgentsEventParamsOfUserToolConfirmation`
    * `BetaManagedAgentsEventParamsOfUserDefineOutcome`
    * `BetaManagedAgentsDeploymentInitialEventParamsOfUserDefineOutcome`
    * `BetaManagedAgentsMultiagentRosterEntryParamsOfBetaManagedAgentsAgents`
    * `BetaManagedAgentsMultiagentRosterEntryParamsOfBetaManagedAgentsAdvisors`

    Empat constructor berikut tidak menerima argumen lain, sehingga telah dihapus. Atur field union ke pointer ke struct kosong, seperti `BetaManagedAgentsEventParamsUnion{OfUserInterrupt: &anthropic.BetaManagedAgentsUserInterruptEventParams{}}`:

    * `BetaManagedAgentsEventParamsOfUserInterrupt`
    * `BetaManagedAgentsMultiagentRosterEntryParamsOfBetaManagedAgentsMultiagentSelfs`
    * `BetaManagedAgentsCredentialNetworkingParamsOfUnrestricted`
    * `BetaOutputBehaviorParamOfCreateNew`
  </Tab>

  <Tab title="Java">
    Contoh enum semacam itu adalah kelas bersarang `BetaManagedAgentsTextBlock.Type`, dengan satu anggotanya `TEXT`. Hampir semuanya adalah `type` dari class di bawah `com.anthropic.models.beta`: `agents`, `deploymentruns`, `deployments`, `dreams`, `environments`, `memorystores`, `sessions`, `userprofiles`, dan `vaults`. Di v3, field-field ini berupa `JsonValue` yang diisi oleh builder, seperti milik `TextBlockParam` sebelumnya. Field opsional, seperti `type` dari `BetaManagedAgentsBashToolConfigParams`, tetap mempertahankan enum-nya.

    Saat Anda membuat objek, hapus pemanggilan tersebut:

    ```java
    // Sebelum
    BetaManagedAgentsTextBlock block = BetaManagedAgentsTextBlock.builder()
        .type(BetaManagedAgentsTextBlock.Type.TEXT)
        .text("Hello Claude!")
        .build();

    // Sesudah
    BetaManagedAgentsTextBlock block = BetaManagedAgentsTextBlock.builder()
        .text("Hello Claude!")
        .build();
    ```

    Class yang tersisa dengan satu field wajib juga mendapatkan metode factory yang menerimanya, sehingga `BetaManagedAgentsTextBlock.of("Hello Claude!")` juga berfungsi. Class yang tidak tersisa field wajib apa pun kehilangan `of(type)`, dan union-nya kehilangan overload yang menerima enum, seperti `ofAlwaysAllow(type)`. Buat dengan `BetaManagedAgentsAlwaysAllowPolicy.builder().build()`.

    Saat Anda membacanya, `type()` telah dihapus dan `_type()` mengembalikan `com.anthropic.core.JsonValue`:

    ```java
    // Sebelum
    if (message.type().equals(BetaManagedAgentsAgentMessageEvent.Type.AGENT_MESSAGE)) {}

    // Sesudah
    if (message._type().equals(JsonValue.from("agent.message"))) {}
    ```

    Untuk membedakan varian-varian dari union, tetap gunakan method `is*()` dan `as*()` serta visitor-nya, yang tidak berubah.
  </Tab>

  <Tab title="PHP">
    Contoh enum case semacam itu adalah `Anthropic\Beta\Sessions\Events\ManagedAgentsTextBlock\Type::TEXT`. Hampir semuanya adalah `type` dari class Managed Agents di bawah `Anthropic\Beta`. Properti-properti ini sekarang berupa string dengan satu nilai tersebut sebagai default-nya, seperti `type` dari `Anthropic\Messages\TextBlockParam` sebelumnya. Properti opsional, seperti `type` dari `Anthropic\Beta\Environments\BetaPackages`, tetap mempertahankan enum-nya.

    `with()` tidak lagi menerima `type`. Hapus argumen tersebut: PHP melempar “Unknown named parameter” untuk `type:` yang tersisa, dan dalam panggilan posisional argumen setelahnya bergeser maju satu posisi.

    ```php
    // Sebelum
    ManagedAgentsTextBlock::with(text: 'Hello Claude!', type: Type::TEXT);

    // Sesudah
    ManagedAgentsTextBlock::with(text: 'Hello Claude!');
    ```

    Di tempat Anda membandingkan dengan enum case, bandingkan dengan string:

    ```php
    // Sebelum
    $event->type === Type::AGENT_MESSAGE->value;

    // Sesudah
    $event->type === 'agent.message';
    ```

    * `withType()` dan argumen `type` dari `$client->beta->sessions->resources->add()` sekarang hanya menerima string. Di `add()`, nilai default-nya adalah `'file'`, sehingga Anda dapat menghilangkannya.
    * Permintaan yang Anda tulis sebagai array tidak berubah, dan tetap memerlukan `'type'`-nya.
  </Tab>

  <Tab title="Ruby">
    Contoh konstanta enum semacam itu adalah `Anthropic::Beta::Sessions::BetaManagedAgentsTextBlock::Type::TEXT`. Hampir semuanya adalah `type` dari class Managed Agents di bawah `Anthropic::Beta`. Di v2, field-field ini dideklarasikan sebagai konstanta, seperti `type` dari `Anthropic::TextBlockParam` sebelumnya. Field opsional, seperti `type` dari `Anthropic::Beta::BetaManagedAgentsGlobToolConfigParams`, tetap mempertahankan enum-nya.

    Ganti konstanta yang dihapus dengan symbol-nya:

    ```ruby
    # Sebelum
    event.type == Anthropic::Beta::Sessions::BetaManagedAgentsAgentMessageEvent::Type::AGENT_MESSAGE

    # Sesudah
    event.type == :"agent.message"
    ```

    Permintaan yang Anda tulis sebagai hash tidak berubah, dan tetap memerlukan `type`-nya:

    ```ruby
    client.beta.sessions.events.send_(
      session.id,
      events: [{type: "user.message", content: [{type: "text", text: "Hello Claude!"}]}]
    )
    ```

    Saat Anda membuat instance model, `type:` sekarang memiliki nilai default, sehingga Anda dapat menghilangkannya: `Anthropic::Beta::Sessions::BetaManagedAgentsTextBlock.new(text: "Hello Claude!")`. Hal yang sama berlaku untuk kata kunci `type:` dari `client.beta.sessions.resources.add`.

    Jika Anda melakukan pemeriksaan tipe dengan Sorbet, alias `Type::OrSymbol` dan `Type::TaggedSymbol` dari modul-modul ini ikut dihapus, dan field-field tersebut berupa `Symbol`. `OrSymbol` juga mengizinkan `String`, sehingga `.new(type: "text")` tidak lagi lolos pemeriksaan tipe. Hilangkan kata kunci tersebut atau teruskan `:text`. Di RBS, alias `type_` dari setiap class telah dihapus, dan field-nya berupa literal, seperti `:text`.
  </Tab>
</Tabs>

### Compaction sisi klien dihapus dari tool runner

Ini memengaruhi SDK TypeScript dan Ruby. “Client-side compaction” (pemadatan di sisi klien) di tool runner dihapus dan digantikan dengan pemadatan di sisi server, yang merangkum percakapan di dalam API alih-alih dengan permintaan tambahan dari klien.

<Tabs exclude="shell, python, csharp, go, java, php">
  <Tab title="TypeScript">
    Opsi `compactionControl` dan modul `@anthropic-ai/sdk/lib/tools/CompactionControl` telah dihapus. Opsi tersebut berhenti berfungsi di v0.129.0, di mana meneruskannya akan melempar `AnthropicError`. Opsi ini tidak ada dalam tipe parameter tool runner, sehingga TypeScript melaporkannya sebagai properti yang tidak dikenal.

    Untuk tetap melakukan pemadatan secara otomatis pada ambang batas token:

    ```typescript
    // Sebelum
    const runner = client.beta.messages.toolRunner({
      // ...
      compactionControl: { enabled: true, contextTokenThreshold: 100_000 }
    });

    // Sesudah
    const runner = client.beta.messages.toolRunner({
      // ...
      betas: ["compact-2026-01-12"],
      context_management: {
        edits: [{ type: "compact_20260112", trigger: { type: "input_tokens", value: 100_000 } }]
      }
    });
    ```

    Untuk menentukan sendiri kapan percakapan dipadatkan, panggil [`runner.compactBeforeNextTurn()`](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/helpers.md#compaction).
  </Tab>

  <Tab title="Ruby">
    Opsi `compaction_control:` telah dihapus. Opsi tersebut berhenti berfungsi di v1.74.0, di mana meneruskannya akan memunculkan `ArgumentError`.

    Untuk tetap melakukan pemadatan secara otomatis pada ambang batas token:

    ```ruby
    # Sebelum
    runner = client.beta.messages.tool_runner(
      # ...
      compaction_control: {enabled: true, context_token_threshold: 100_000}
    )

    # Sesudah
    runner = client.beta.messages.tool_runner(
      # ...
      betas: ["compact-2026-01-12"],
      context_management: {
        edits: [{type: :compact_20260112, trigger: {type: :input_tokens, value: 100_000}}]
      }
    )
    ```

    Untuk menentukan sendiri kapan percakapan dipadatkan, panggil [`#compact_before_next_turn`](https://github.com/anthropics/anthropic-sdk-ruby/blob/main/helpers.md#compact_before_next_turn---compact-the-conversation) pada runner.
  </Tab>
</Tabs>

Ambang batas pemicu harus setidaknya 50.000 token. Lihat [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold) untuk opsi lainnya (`pause_after_compaction`, `instructions` kustom).

### Text Completions dihapus

Text Completions API lama dihapus dari SDK TypeScript, Go, Java, dan Ruby serta dari CLI. Model dan fitur yang lebih baru tidak mendukungnya. Gunakan [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) sebagai gantinya.

### `betas` dihapus dari metode Models non-beta

Metode Models non-beta tidak lagi menerima `betas` (csharp, go: `Betas`; java: `.addBeta()`), dan perintah `ant models` tidak lagi menerima `--beta`. Untuk mengirim header beta, panggil metode yang sama pada `client.beta.models` (csharp, go: `client.Beta.Models`; java: `client.beta().models()`; php: `$client->beta->models`), atau `ant beta:models` di CLI. Di SDK, metode-metode tersebut mengembalikan `BetaModelInfo` (ruby: `Anthropic::Beta::BetaModelInfo`) sedangkan yang non-beta mengembalikan `ModelInfo` (ruby: `Anthropic::ModelInfo`).

<Tabs exclude="shell:cURL">
  <Tab title="CLI">
    ```bash
    # Sebelum
    ant models list --beta "$BETA"

    # Sesudah
    ant beta:models list --beta "$BETA"
    ```
  </Tab>

  <Tab title="Python">
    `client.models.retrieve()` dan `client.models.list()` tidak lagi menerima `betas` (meneruskannya menghasilkan `TypeError`, dan pemeriksa tipe menandainya), dan `anthropic.types.ModelListParams` tidak lagi memiliki kunci `betas`.

    ```python
    # Sebelum
    page = client.models.list(betas=[beta])

    # Sesudah
    page = client.beta.models.list(betas=[beta])
    ```
  </Tab>

  <Tab title="TypeScript">
    `Anthropic.ModelRetrieveParams` dan `Anthropic.ModelListParams` tidak lagi memiliki properti `betas`.

    ```typescript
    // Sebelum
    const page = await client.models.list({ betas: [beta] });

    // Sesudah
    const page = await client.beta.models.list({ betas: [beta] });
    ```
  </Tab>

  <Tab title="C#">
    `ModelRetrieveParams` dan `ModelListParams` di `Anthropic.Models.Models` tidak lagi memiliki properti `Betas`. Metode pada `client.Beta.Models` menerima class dengan nama yang sama di `Anthropic.Models.Beta.Models`.

    ```csharp
    // Sebelum
    using Anthropic.Models.Models;

    var page = await client.Models.List(new ModelListParams { Betas = [beta] });

    // Sesudah
    using Anthropic.Models.Beta.Models;

    var page = await client.Beta.Models.List(new ModelListParams { Betas = [beta] });
    ```
  </Tab>

  <Tab title="Go">
    `ModelGetParams` dan `ModelListParams` tidak lagi memiliki field `Betas`.

    ```go
    // Sebelum
    page, err := client.Models.List(ctx, anthropic.ModelListParams{
    	Betas: []anthropic.AnthropicBeta{beta},
    })

    // Sesudah
    page, err := client.Beta.Models.List(ctx, anthropic.BetaModelListParams{
    	Betas: []anthropic.AnthropicBeta{beta},
    })
    ```
  </Tab>

  <Tab title="Java">
    `ModelRetrieveParams` dan `ModelListParams` di `com.anthropic.models.models` tidak lagi memiliki `betas()`, dan builder-nya tidak lagi memiliki `betas` dan `addBeta`. Metode pada `client.beta().models()` menerima class dengan nama yang sama di `com.anthropic.models.beta.models`.

    ```java
    // Sebelum
    import com.anthropic.models.models.ModelListPage;
    import com.anthropic.models.models.ModelListParams;

    ModelListPage page = client.models().list(ModelListParams.builder()
        .addBeta(beta)
        .build());

    // Sesudah
    import com.anthropic.models.beta.models.ModelListPage;
    import com.anthropic.models.beta.models.ModelListParams;

    ModelListPage page = client.beta().models().list(ModelListParams.builder()
        .addBeta(beta)
        .build());
    ```
  </Tab>

  <Tab title="PHP">
    `$client->models->retrieve()` dan `$client->models->list()` tidak lagi menerima `betas` (meneruskannya melempar `Error: Unknown named parameter $betas`), dan `Anthropic\Models\ModelRetrieveParams` serta `Anthropic\Models\ModelListParams` tidak lagi memiliki properti `betas`.

    ```php
    // Sebelum
    $page = $client->models->list(betas: [$beta]);

    // Sesudah
    $page = $client->beta->models->list(betas: [$beta]);
    ```

    Jika Anda meneruskan argumen berdasarkan posisi, `workspaceID` dan `requestOptions` masing-masing naik satu posisi di kedua metode.
  </Tab>

  <Tab title="Ruby">
    `client.models.retrieve` dan `client.models.list` tidak lagi menerima `betas:`, dan `Anthropic::ModelRetrieveParams` serta `Anthropic::ModelListParams` tidak lagi memiliki field `betas`.

    ```ruby
    # Sebelum
    page = client.models.list(betas: [beta])

    # Sesudah
    page = client.beta.models.list(betas: [beta])
    ```

    Meneruskan `betas:` ke `client.models` tidak memunculkan error, tetapi tidak lagi mengatur header `anthropic-beta`.
  </Tab>
</Tabs>

### Kunci API dikirim sebagai `Authorization: Bearer`

SDK dan CLI mengirim kunci API Anda sebagai `Authorization: Bearer <key>` alih-alih di header `X-Api-Key`, jadi ubah proxy atau gateway apa pun yang membaca atau mengatur `X-Api-Key` agar menggunakan `Authorization`, atau [kirim kunci di `X-Api-Key` sendiri](https://platform.claude.com/docs/id/api/migration-2026-10-21#sdk-proxy-x-api-key). Ubah juga kode di program Anda sendiri yang membaca `X-Api-Key`, seperti middleware, filter log, atau stub pengujian. Claude API menerima kunci di salah satu header tersebut.

```text wrap
# Before
X-Api-Key: <key>

# After
Authorization: Bearer <key>
```

<Tabs>
  <Tab title="CLI">
    Ini berlaku untuk kunci di `ANTHROPIC_API_KEY` dan kunci yang di-pipe ke `--api-key-stdin`.

    Dengan `--debug`, log permintaan sekarang menampilkan `Authorization: Bearer <REDACTED>` di tempat yang sebelumnya menampilkan `X-Api-Key: <REDACTED>`.
  </Tab>

  <Tab title="Python">
    `Authorization` adalah header yang sudah digunakan oleh `auth_token`.

    Ini berlaku untuk argumen `api_key` dan variabel lingkungan `ANTHROPIC_API_KEY` dari `Anthropic` dan `AsyncAnthropic`, serta untuk `api_key` dan `ANTHROPIC_AWS_API_KEY` dari `AnthropicAWS`. `AnthropicFoundry` masih mengirim kuncinya sebagai `x-api-key`, dan `AnthropicBedrockMantle` sudah mengirim bearer token.
  </Tab>

  <Tab title="TypeScript">
    `Authorization` adalah header yang sudah digunakan oleh opsi `authToken`.

    Ini berlaku untuk opsi `apiKey`, variabel lingkungan `ANTHROPIC_API_KEY`, serta `apiKey` dan `ANTHROPIC_AWS_API_KEY` di `@anthropic-ai/aws-sdk`. `apiKey` di `@anthropic-ai/foundry-sdk` masih dikirim sebagai `X-Api-Key`, dan `apiKey` di `@anthropic-ai/bedrock-sdk` sudah merupakan bearer token.
  </Tab>

  <Tab title="C#">
    `Authorization` adalah header yang sudah digunakan oleh `AuthToken`.

    Ini berlaku untuk `ApiKey` pada `AnthropicClient` dan `ClientOptions` serta untuk variabel lingkungan `ANTHROPIC_API_KEY`. Dalam rilis `Anthropic.Aws` yang bergantung pada v13, ini juga berlaku untuk `ApiKey` di `AwsClientOptions` dan untuk `ANTHROPIC_AWS_API_KEY`. `AnthropicFoundryApiKeyCredentials` masih mengirim kuncinya sebagai `x-api-key`, dan `ApiKey` di `MantleAwsClientOptions` sudah merupakan bearer token.
  </Tab>

  <Tab title="Go">
    Ini berlaku untuk `option.WithAPIKey`, variabel lingkungan `ANTHROPIC_API_KEY`, dan `APIKey` di `aws.ClientConfig` (atau `ANTHROPIC_AWS_API_KEY`). `APIKey` di `foundry.ClientConfig` (atau `ANTHROPIC_FOUNDRY_API_KEY`) masih dikirim sebagai `X-Api-Key`, dan `APIKey` di `bedrock.MantleClientConfig` sudah merupakan bearer token.
  </Tab>

  <Tab title="Java">
    `Authorization` adalah header yang sudah digunakan oleh `authToken`.

    Ini berlaku untuk `apiKey` pada builder `AnthropicOkHttpClient`, `AnthropicOkHttpClientAsync`, dan `AnthropicBackend`, variabel lingkungan `ANTHROPIC_API_KEY`, dan properti sistem `anthropic.apiKey`. `apiKey` pada builder `FoundryBackend` masih dikirim sebagai `x-api-key`. `apiKey` pada builder `AwsBackend`, `BedrockBackend`, dan `BedrockMantleBackend` sudah merupakan bearer token.
  </Tab>

  <Tab title="PHP">
    `Authorization` adalah header yang sudah digunakan oleh `authToken`.

    Ini berlaku untuk argumen `apiKey` dan variabel lingkungan `ANTHROPIC_API_KEY` dari `Anthropic\Client`, serta untuk `apiKey` dan `ANTHROPIC_AWS_API_KEY` dari `Anthropic\Aws\Client`. `Anthropic\Foundry\Client` masih mengirim kuncinya sebagai `x-api-key`, dan `Anthropic\Bedrock\MantleClient` sudah mengirim bearer token.
  </Tab>

  <Tab title="Ruby">
    `Authorization` adalah header yang sudah digunakan oleh `auth_token:`.

    Ini berlaku untuk argumen `api_key:` dan variabel lingkungan `ANTHROPIC_API_KEY` dari `Anthropic::Client`, serta untuk `api_key:` dan `ANTHROPIC_AWS_API_KEY` dari `Anthropic::AWSClient`. `Anthropic::FoundryClient` mengirim kuncinya sebagai `x-api-key`, dan `Anthropic::BedrockMantleClient` sudah mengirim bearer token.

    SDK membuang `Authorization` ketika mengikuti redirect ke origin lain, termasuk redirect dari `http` ke `https` pada host yang sama. Kunci sekarang juga dibuang di sana.
  </Tab>
</Tabs>

#### Jika proxy atau gateway membaca `X-Api-Key`

<Tabs exclude="shell:cURL">
  <Tab title="CLI">
    Jika `--base-url` atau `ANTHROPIC_BASE_URL` mengarahkan `ant` ke proxy atau gateway yang membaca `X-Api-Key`, ubah agar membaca kunci dari `Authorization`. `ant` tidak memiliki flag atau variabel lingkungan untuk menambahkan header Anda sendiri, sehingga tidak dapat mengirim `X-Api-Key`.
  </Tab>

  <Tab title="Python">
    Pindahkan kembali kunci dengan fungsi `auth` pada klien HTTP. Fungsi ini berjalan pada setiap permintaan yang dikirim klien, termasuk percobaan ulang:

    ```python
    import httpx2
    from anthropic import Anthropic, DefaultHttpxClient


    def send_x_api_key(request: httpx2.Request) -> httpx2.Request:
        if request.headers.get("Authorization") == f"Bearer {api_key}":
            del request.headers["Authorization"]
            request.headers["X-Api-Key"] = api_key
        return request


    client = Anthropic(api_key=api_key, http_client=DefaultHttpxClient(auth=send_x_api_key))
    ```

    `AsyncAnthropic` menerima fungsi yang sama, di `http_client=DefaultAsyncHttpxClient(auth=send_x_api_key)`.
  </Tab>

  <Tab title="TypeScript">
    Atur header sendiri. `Authorization: null` juga mencegah kunci dikirim di sana:

    ```typescript
    const client = new Anthropic({
      apiKey,
      defaultHeaders: { "X-Api-Key": apiKey, Authorization: null }
    });
    ```

    Jika proxy menambahkan kredensial dan klien Anda tidak memilikinya, v0 memungkinkan Anda menyatakannya dengan `"X-Api-Key": null` atau `Authorization: null` di `defaultHeaders`. v1 hanya menerima `Authorization: null`.

    Poller dan worker environment work diberi kunci mereka sendiri, sehingga mereka tidak menyertakan default header `X-Api-Key` dan `Authorization` dalam permintaan mereka sendiri.
  </Tab>

  <Tab title="C#">
    Atur header sendiri dengan `ExtraHeaders`. Mengatur `ApiKey` dan `AuthToken` ke `null` juga mencegah kredensial yang ditemukan di `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN` ikut dikirim:

    ```csharp
    AnthropicClient client = new(
        new ClientOptions
        {
            ApiKey = null,
            AuthToken = null,
            ExtraHeaders = new Dictionary<string, string> { ["X-Api-Key"] = apiKey },
        }
    );
    ```
  </Tab>

  <Tab title="Go">
    Atur header sendiri. `option.WithHeaderDel` juga mencegah kunci yang ditemukan di `ANTHROPIC_API_KEY` ikut dikirim:

    ```go
    client := anthropic.NewClient(
    	option.WithHeader("X-Api-Key", apiKey),
    	option.WithHeaderDel("Authorization"),
    )
    ```

    `environments.WorkPoller` dan `environments.EnvironmentWorker` diberi kunci mereka sendiri, sehingga mereka tidak menyertakan `X-Api-Key` yang diatur secara manual dalam permintaan mereka sendiri.
  </Tab>

  <Tab title="Java">
    Atur header sendiri alih-alih memanggil `apiKey`:

    ```java
    AnthropicClient client = AnthropicOkHttpClient.builder()
        .putHeader("X-Api-Key", apiKey)
        .build();
    ```
  </Tab>

  <Tab title="PHP">
    Pindahkan kembali kunci dengan middleware:

    ```php
    use Anthropic\Client;
    use Psr\Http\Message\RequestInterface;
    use Psr\Http\Message\ResponseInterface;

    $sendXApiKey = fn (RequestInterface $request, callable $next): ResponseInterface => $next(
        $request->withoutHeader('Authorization')->withHeader('X-Api-Key', $apiKey)
    );

    $client = new Client(apiKey: $apiKey, requestOptions: ['middleware' => [$sendXApiKey]]);
    ```

    Jangan gunakan `extraHeaders` milik klien untuk ini. Permintaan yang memiliki `extraHeaders` sendiri akan menggantikan milik klien, dan setiap endpoint di bawah `$client->beta` yang memerlukan header beta memilikinya.
  </Tab>

  <Tab title="Ruby">
    Pindahkan kembali kunci dengan middleware:

    ```ruby
    send_x_api_key = lambda do |req, nxt|
      next nxt.call(req) unless req.headers["authorization"] == "Bearer #{api_key}"
      nxt.call(req.with(headers: {**req.headers.except("authorization"), "x-api-key" => api_key}))
    end

    client = Anthropic::Client.new(api_key: api_key, middleware: send_x_api_key)
    ```

    Baris pertama membiarkan permintaan apa adanya ketika permintaan tersebut tidak membawa kunci, seperti permintaan yang di-redirect ke origin lain.

    `Anthropic::AWSClient` tidak menerima argumen `middleware:`. Teruskan middleware dengan setiap permintaan sebagai gantinya, sebagai `request_options: {middleware: send_x_api_key}`.
  </Tab>
</Tabs>

#### Jika Anda mengatur atau menghapus `X-Api-Key` pada permintaan

Ini memengaruhi SDK Python, TypeScript, Go, PHP, dan Ruby.

Jika Anda menghapus `X-Api-Key` agar permintaan hanya mengirim token autentikasi, hapus kode tersebut alih-alih mengubahnya, karena menghapus `Authorization` akan menghapus token. [Klien menyimpan satu kredensial](https://platform.claude.com/docs/id/api/migration-2026-10-21#sdk-one-credential), jadi pastikan kredensial tersebut adalah token: jika tidak ada yang diteruskan dalam kode dan `ANTHROPIC_API_KEY` serta `ANTHROPIC_AUTH_TOKEN` keduanya diatur, klien menggunakan kunci.

<Tabs exclude="shell, csharp, java">
  <Tab title="Python">
    Kode yang meneruskan `extra_headers={"X-Api-Key": omit}` untuk menjauhkan kunci dari permintaan tidak lagi melakukan hal tersebut. Teruskan `extra_headers={"Authorization": omit}` sebagai gantinya.

    `extra_headers={"X-Api-Key": other_key}` tidak lagi menggantikan kunci klien: kedua kunci dikirim. Untuk mengirim kunci lain dengan satu permintaan, teruskan `extra_headers={"Authorization": f"Bearer {other_key}"}`.
  </Tab>

  <Tab title="TypeScript">
    `headers: { "X-Api-Key": otherKey }` dalam opsi permintaan tidak lagi menggantikan kunci klien: kedua kunci dikirim. Untuk mengirim kunci lain dengan satu permintaan, teruskan ``headers: { Authorization: `Bearer $\{otherKey}` }``.
  </Tab>

  <Tab title="Go">
    `option.WithHeaderDel("X-Api-Key")` tidak lagi menjauhkan kunci dari permintaan. Hapus `Authorization` sebagai gantinya:

    ```go
    // Sebelum
    client.Messages.New(ctx, params, option.WithHeaderDel("X-Api-Key"))

    // Sesudah
    client.Messages.New(ctx, params, option.WithHeaderDel("Authorization"))
    ```

    `option.WithHeader("X-Api-Key", otherKey)` tidak lagi menggantikan kunci klien: kedua kunci dikirim. Untuk mengirim kunci lain dengan satu permintaan, teruskan `option.WithAPIKey(otherKey)`.
  </Tab>

  <Tab title="PHP">
    `'extraHeaders' => ['X-Api-Key' => null]` tidak lagi menjauhkan kunci dari permintaan. Untuk mengirim permintaan tanpa kredensial, atur `Authorization` ke `null` sebagai gantinya, atau hapus di middleware jika Anda melakukan ini untuk seluruh klien.

    `'extraHeaders' => ['X-Api-Key' => $otherKey]` tidak lagi menggantikan kunci klien: kedua kunci dikirim. Untuk mengirim kunci lain dengan satu permintaan, atur `Authorization` ke `"Bearer {$otherKey}"`.
  </Tab>

  <Tab title="Ruby">
    `extra_headers: {"x-api-key" => nil}` tidak lagi menjauhkan kunci dari permintaan. Atur `"authorization"` ke `nil` sebagai gantinya. Untuk mengirim kunci lain dengan satu permintaan, atur `"authorization"` ke `"Bearer #{other_key}"`, bukan `"x-api-key"`.
  </Tab>
</Tabs>

### Klien menyimpan satu kredensial

Kunci API dan token autentikasi sekarang berbagi satu header, sehingga klien SDK menyimpan satu kredensial. Jika tidak ada yang diteruskan dalam kode, klien mengikuti urutan [prioritas kredensial](https://platform.claude.com/docs/id/manage-claude/wif-reference#credential-precedence).

<Tabs exclude="shell">
  <Tab title="Python">
    v1 mengirim kunci API dan token autentikasi ketika klien memiliki keduanya, masing-masing di header-nya sendiri. Kredensialnya adalah salah satu dari `api_key`, `auth_token`, `credentials`, `config`, atau `profile`.

    * **Teruskan paling banyak satu.** Dua atau lebih di constructor, atau dalam satu panggilan `copy()` atau `with_options()`, memunculkan `ValueError`. `None` tidak dihitung. v1 memunculkan `TypeError`, dan hanya untuk dua dari `credentials`, `config`, dan `profile`.
    * **Yang Anda teruskan adalah satu-satunya.** Seperti di v1, klien tidak mencari kredensial lain di lingkungan atau di disk.
    * **Jika tidak ada yang diteruskan, hanya yang pertama dari berikut ini yang diatur yang digunakan:** `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, profil yang disebutkan oleh `ANTHROPIC_PROFILE`, variabel workload identity federation, profil aktif di disk (yang disebutkan oleh file `active_config`, jika tidak maka `default`). Ketika dua yang pertama keduanya diatur, klien mencatat peringatan satu kali. v1 menggunakan profil aktif sebelum variabel federation ketika `ANTHROPIC_CONFIG_DIR` diatur atau file `active_config` ada; atur `ANTHROPIC_PROFILE` untuk tetap menggunakannya.
    * **`copy()` dan `with_options()` menggantikan.** Kredensial yang Anda teruskan menggantikan kredensial milik klien, apa pun jenis keduanya. Base URL dan header yang berasal dari konfigurasi atau profil kredensial lama ikut terbuang, dan milik kredensial baru yang digunakan. Base URL yang Anda teruskan tetap ada.

    ```python
    client = Anthropic(api_key=key, auth_token=token)

    # Sebelumnya: mengirim `X-Api-Key: <key>` dan `Authorization: Bearer <token>`
    # Sesudahnya:  memunculkan `ValueError`
    ```

    Klien platform tetap memiliki aturannya sendiri. `AnthropicAWS` menerima `auth_token` di samping `api_key` tanpa error, dan mengirim kuncinya.

    Docstring dari `Anthropic.__init__` dan `Anthropic.copy` di [`_client.py`](https://github.com/anthropics/anthropic-sdk-python/blob/main/src/anthropic/_client.py) berisi detailnya.

    Jika Anda mengandalkan pengiriman keduanya, misalnya token untuk gateway dan kunci untuk API di belakangnya, teruskan token sebagai `auth_token` dan atur `X-Api-Key` di `default_headers`. Minta gateway menghapus header `Authorization`-nya sebelum meneruskan permintaan. Claude API mengharapkan satu kredensial untuk setiap permintaan.
  </Tab>

  <Tab title="TypeScript">
    Di v0, klien yang memiliki kunci API dan token autentikasi mengirim keduanya, masing-masing di header-nya sendiri. Kredensialnya adalah salah satu dari `apiKey`, `authToken`, `credentials`, `config`, atau `profile`.

    * **Teruskan paling banyak satu.** Dua atau lebih di `new Anthropic()`, atau dalam satu panggilan `withOptions()`, melempar `TypeError`. `null` dan `undefined` tidak dihitung.
    * **Yang Anda teruskan adalah satu-satunya.** Klien tidak mencari kredensial lain di lingkungan atau di disk.
    * **Jika tidak ada yang diteruskan, yang pertama dari berikut ini yang digunakan:** `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, profil yang disebutkan oleh `ANTHROPIC_PROFILE`, variabel workload identity federation, profil aktif di disk (yang disebutkan oleh file `active_config`, jika tidak maka `default`). Ketika dua yang pertama keduanya diatur, klien mencatat peringatan satu kali. Di v0, profil aktif didahulukan sebelum variabel federation. `ANTHROPIC_PROFILE` yang menyebutkan profil yang tidak ada dilewati di v0, dan sekarang permintaan pertama melempar `AnthropicError`. `loadConfig()` tanpa argumen mengikuti urutan yang sama dan melempar error yang sama.
    * **`withOptions` menggantikan.** Kredensial yang Anda teruskan menggantikan kredensial milik klien yang Anda salin, sehingga `client.withOptions({ authToken })` tidak lagi memerlukan `apiKey: null` di sampingnya.
    * **Klien platform hanya menerima kredensial platformnya.** Klien AWS, Bedrock, dan Foundry serta `AnthropicVertex` melempar `AnthropicError` untuk opsi kredensial yang tidak mereka gunakan untuk autentikasi, seperti yang sudah dilakukan `AnthropicGoogleCloud`. Pada klien AWS dan Bedrock, `apiKey: null` sekarang menghapus kunci, sehingga klien menandatangani dengan kredensial AWS. `AnthropicBedrock` menyimpan kuncinya di `client.apiKey`, sedangkan v0 menyimpannya di `client.authToken`.

    ```typescript
    // Sebelum: mengirim kunci API dan mengabaikan `credentials`
    const client = new Anthropic({ apiKey, credentials });

    // Sesudah: baris sebelumnya melempar TypeError
    const client = new Anthropic({ credentials });
    ```

    Komentar dokumentasi pada `ClientOptions` di [`client.ts`](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/src/client.ts) menjelaskan perilaku setiap opsi, dan komentar dokumentasi pada constructor setiap klien platform tersebut mencantumkan opsi yang ditolaknya.

    Jika Anda mengandalkan pengiriman keduanya, misalnya token untuk gateway dan kunci untuk API di belakangnya, atur `X-Api-Key` di `defaultHeaders` dan pertahankan `authToken`. Minta gateway menghapus header `Authorization`-nya sebelum meneruskan permintaan. Claude API mengharapkan satu kredensial untuk setiap permintaan.
  </Tab>

  <Tab title="C#">
    Di v12, klien yang memiliki kunci API dan token autentikasi mengirim keduanya, masing-masing di header-nya sendiri. Kredensialnya adalah salah satu dari `ApiKey`, `AuthToken`, atau `ClientOptions.Credentials`.

    * **Meneruskan dua merupakan error.** Mengatur yang kedua melempar `ArgumentException`. `null` tidak dihitung, jadi untuk menukar kredensial di `ClientOptions` yang Anda buat sendiri, atur yang lama ke `null` terlebih dahulu.
    * **Meneruskan satu akan menggunakannya dan mengabaikan lingkungan.** Tidak ada variabel lingkungan kredensial atau profil di disk yang dibaca. Dengan cara yang sama, `AnthropicCredentials.Resolve(profile: "name")` sekarang mengembalikan kredensial profil tersebut ketika `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN` diatur.
    * **Tidak meneruskan apa pun akan menggunakan kecocokan pertama di lingkungan:** `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_PROFILE`, variabel workload identity federation, lalu profil aktif di disk. `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN` yang kosong dianggap tidak diatur. Ketika dua yang pertama keduanya diatur, peringatan dikirim ke stderr satu kali. Klien melakukan pencarian saat pertama kali digunakan, sehingga `ANTHROPIC_PROFILE` yang tidak ada sekarang melempar dari permintaan pertama alih-alih dari constructor.
    * **`WithOptions` menggantikan.** Kredensial yang Anda teruskan di modifier menggantikan kredensial milik klien, apa pun jenisnya, sehingga `AuthToken = token` tidak lagi memerlukan `ApiKey = null` di sampingnya. Jika tidak ada yang diteruskan, salinan mempertahankan kredensial, `BaseUrl`, dan `ExtraHeaders` milik klien, bahkan ketika modifier mengembalikan `ClientOptions` baru.

    ```csharp
    // Sebelumnya: keduanya dikirim, masing-masing dalam header tersendiri
    AnthropicClient client = new() { ApiKey = apiKey, AuthToken = token };

    // Sesudahnya: baris sebelumnya melempar ArgumentException
    AnthropicClient client = new() { AuthToken = token };
    ```

    Dokumentasi XML pada ketiga properti [`ClientOptions`](https://github.com/anthropics/anthropic-sdk-csharp/blob/main/src/Anthropic/Core/ClientOptions.cs) tersebut berisi detailnya.

    Klien platform cloud mempertahankan kredensial yang digunakan saat dibuat. Klien Bedrock, Bedrock Mantle, Foundry, Google Cloud, dan AWS serta `AnthropicVertexClient` menentukan cara autentikasi saat Anda membuatnya, dan sebagian besar menggunakan header `Authorization` untuk itu. Rilis paket-paket ini yang bergantung pada v13 mengabaikan `ApiKey` atau `AuthToken` yang Anda atur melalui `WithOptions`. Untuk menggunakan kunci lain dengan `AnthropicAwsClient`, buat klien baru dengan `ApiKey` di `AwsClientOptions`.

    Jika Anda mengandalkan pengiriman keduanya, misalnya token untuk gateway dan kunci untuk API di belakangnya, atur `X-Api-Key` dengan `ExtraHeaders` dan pertahankan `AuthToken`. Minta gateway menghapus header `Authorization`-nya sebelum meneruskan permintaan. Claude API mengharapkan satu kredensial untuk setiap permintaan.
  </Tab>

  <Tab title="Go">
    Di v1, klien yang memiliki kunci API dan token autentikasi mengirim keduanya, masing-masing di header-nya sendiri. Kredensialnya berasal dari `option.WithAPIKey`, `option.WithAuthToken`, `option.WithConfig`, `option.WithProfile`, atau `option.WithFederationTokenProvider`.

    * **Dua di antaranya yang diteruskan ke `anthropic.NewClient` merupakan error.** `NewClient` tidak mengembalikan error, sehingga setiap permintaan yang dibuat klien gagal dengan error tersebut. `NewClient` sudah menerapkan `anthropic.DefaultClientOptions()`, jadi jangan teruskan hasilnya juga: kredensial yang ditemukannya di lingkungan kemudian dihitung sebagai kredensial yang Anda teruskan.
    * **Satu di antaranya digunakan apa adanya.** Tidak ada kredensial yang dibaca dari lingkungan atau dari profil di disk. Di v1, `ANTHROPIC_API_KEY` dan `ANTHROPIC_AUTH_TOKEN` didahulukan atas tiga yang terakhir.
    * **Jika tidak ada satu pun, yang pertama dari berikut ini yang diatur akan digunakan,** dalam urutan yang sama seperti v1: `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_PROFILE`, variabel workload identity federation, profil aktif di disk. Ketika dua yang pertama keduanya diatur, SDK mencatat peringatan satu kali.
    * **Satu di antaranya pada sebuah permintaan menggantikan kredensial klien untuk permintaan tersebut,** sehingga `option.WithAuthToken` tidak lagi memerlukan `option.WithHeaderDel("X-Api-Key")` di sampingnya.

    ```go
    // Sebelumnya: kunci API dikirim dan sebuah peringatan dicatat ke log
    client := anthropic.NewClient(
    	option.WithAPIKey(apiKey),
    	option.WithProfile("work"),
    )

    // Sesudahnya: setiap permintaan dari klien sebelumnya gagal, jadi teruskan kredensial yang Anda inginkan
    client := anthropic.NewClient(option.WithAPIKey(apiKey))
    ```

    Peringatan yang dicatat v1 telah dihapus, sehingga `option.WithConfigQuiet`, yang menekannya, sekarang melakukan hal yang sama dengan `option.WithConfig` dan sudah deprecated.

    Komentar dokumentasi pada `anthropic.NewClient` dan `anthropic.DefaultClientOptions` di [`client.go`](https://github.com/anthropics/anthropic-sdk-go/blob/main/client.go) berisi detailnya.

    Jika Anda mengandalkan pengiriman keduanya, misalnya token untuk gateway dan kunci untuk API di belakangnya, atur `X-Api-Key` dengan `option.WithHeader` dan pertahankan `option.WithAuthToken`. Minta gateway menghapus header `Authorization`-nya sebelum meneruskan permintaan. Claude API mengharapkan satu kredensial untuk setiap permintaan.

    `ANTHROPIC_CUSTOM_HEADERS` dan `ANTHROPIC_WEBHOOK_SIGNING_KEY` sekarang berlaku untuk setiap klien yang dibuat oleh `anthropic.NewClient`. Di v1, keduanya hanya dibaca ketika baik lingkungan maupun profil di disk tidak menyimpan kredensial.
  </Tab>

  <Tab title="Java">
    Di v2, klien yang memiliki kunci API dan token autentikasi mengirim keduanya, masing-masing di header-nya sendiri. Kredensialnya adalah salah satu dari `apiKey`, `authToken`, atau `configurationProvider` pada builder `AnthropicOkHttpClient`, `AnthropicOkHttpClientAsync`, dan `AnthropicBackend`.

    * **Atur paling banyak satu.** Dengan dua pada satu builder, `build()` melempar `IllegalStateException` yang menyebutkan keduanya. `null` atau `Optional` kosong tidak dihitung.
    * **Yang Anda atur adalah satu-satunya.** `fromEnv()`, yang dipanggil sebelum atau sesudahnya, tidak mengambil kredensial dari lingkungan atau dari profil di disk. Di v2, kunci atau token yang ditemukan `fromEnv()` dapat dikirim juga, atau sebagai gantinya.
    * **Jika tidak ada yang diatur, `fromEnv()` menggunakan yang pertama dari berikut ini yang ditemukannya:** `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_PROFILE`, variabel workload identity federation, profil aktif di disk. Ketika dua yang pertama keduanya diatur, peringatan dikirim ke `System.err` satu kali. Properti sistem `anthropic.apiKey` dan `anthropic.authToken` dihitung sebagai lingkungan. Kunci atau token yang kosong, dalam variabel atau properti sistem, dianggap tidak diatur. Di v2, `fromEnv()` menggunakan nilai kosong sebagai kunci atau token.

    ```java
    // Sebelumnya: keduanya dikirim. Di v3, build() melempar IllegalStateException
    AnthropicClient client = AnthropicOkHttpClient.builder()
        .apiKey(apiKey)
        .authToken(authToken)
        .build();

    // Sesudahnya
    AnthropicClient client = AnthropicOkHttpClient.builder()
        .apiKey(apiKey)
        .build();
    ```

    Dokumentasi `fromEnv()` pada builder-builder tersebut berisi detailnya.

    Jika Anda mengandalkan pengiriman keduanya, misalnya token untuk gateway dan kunci untuk API di belakangnya, atur kedua header sendiri:

    ```java
    AnthropicClient client = AnthropicOkHttpClient.builder()
        .putHeader("Authorization", "Bearer " + gatewayToken)
        .putHeader("X-Api-Key", apiKey)
        .build();
    ```

    Minta gateway menghapus header `Authorization`-nya sebelum meneruskan permintaan. Claude API mengharapkan satu kredensial untuk setiap permintaan.
  </Tab>

  <Tab title="PHP">
    Versi sebelumnya mengirim kunci API dan token autentikasi ketika klien memiliki keduanya, masing-masing di header-nya sendiri. `Anthropic\Client` menerima satu kredensial, dari `apiKey`, `authToken`, atau `credentials`:

    * Meneruskan lebih dari satu di antaranya melempar `\InvalidArgumentException`. Hanya `null` yang dianggap tidak diteruskan. String kosong dianggap diteruskan, sehingga `new Client(apiKey: '')` tidak mengirim kredensial.
    * Meneruskan satu akan menggunakannya, dan tidak ada kredensial yang dibaca dari lingkungan atau dari profil di disk. Dengan `ANTHROPIC_API_KEY` diatur, `new Client(authToken: $token)` mengirim token. Versi sebelumnya mengirim kunci dari lingkungan bersamanya.
    * Tidak meneruskan apa pun akan menggunakan yang pertama dari berikut ini yang diatur: `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, profil yang disebutkan oleh `ANTHROPIC_PROFILE`, variabel workload identity federation, profil aktif di disk (yang disebutkan oleh file `active_config`, jika tidak maka `default`). Versi sebelumnya menggunakan profil aktif sebelum variabel federation, dan tidak menggunakan profil ketika tidak ada file `active_config`. Versi sebelumnya juga melewati `ANTHROPIC_PROFILE` yang menyebutkan profil yang tidak ada atau tidak valid. Untuk hal itu, `new Client()` sekarang melempar `Anthropic\Core\Exceptions\AnthropicException`. Dengan `ANTHROPIC_API_KEY` dan `ANTHROPIC_AUTH_TOKEN` keduanya diatur, klien mengirim kunci dan properti `authToken`-nya kosong. Klien pertama yang dibuat dengan cara itu juga menulis peringatan dengan `error_log()`, satu kali untuk setiap proses, yang pada server web berarti satu kali untuk setiap permintaan: `Anthropic: ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN are both set. Using ANTHROPIC_API_KEY.` Untuk menghentikannya, hapus pengaturan variabel yang tidak Anda gunakan.

    ```php
    // Sebelumnya: mengirim kunci sebagai X-Api-Key dan token sebagai Authorization.
    // Sesudahnya: melempar "Pass at most one of `apiKey`, `authToken`, or `credentials`. Received `apiKey`, `authToken`."
    $client = new Client(apiKey: $key, authToken: $token);
    ```

    Jika Anda mengandalkan pengiriman keduanya, misalnya token untuk gateway dan kunci untuk API di belakangnya, teruskan token sebagai `authToken` dan tambahkan `X-Api-Key` dalam middleware seperti yang ada di bawah [Jika proxy atau gateway membaca `X-Api-Key`](https://platform.claude.com/docs/id/api/migration-2026-10-21#sdk-proxy-x-api-key), tanpa panggilan `withoutHeader`. Minta gateway menghapus header `Authorization`-nya sebelum meneruskan permintaan. Claude API mengharapkan satu kredensial untuk setiap permintaan.
  </Tab>

  <Tab title="Ruby">
    Argumen kredensial dari `Anthropic::Client.new` adalah `api_key:`, `auth_token:`, `credentials:`, dan `config:`. Argumen `nil` dianggap tidak diteruskan. Klien platform tetap memiliki aturannya sendiri.

    * **Dua atau lebih diteruskan:** `Anthropic::Client.new` memunculkan `ArgumentError`. Versi sebelumnya hanya memunculkan error untuk `credentials:` bersama `config:`, dan selain itu mengirim kunci jika ada, atau token jika tidak.
    * **Satu diteruskan:** Klien menggunakannya, dan tidak beralih ke kredensial dari lingkungan atau dari profil di disk.
    * **Tidak ada yang diteruskan:** Klien menggunakan yang pertama dari berikut ini yang ditemukannya: `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_PROFILE`, variabel workload identity federation, profil aktif di disk. Urutannya tidak berubah, tetapi dengan `ANTHROPIC_API_KEY` dan `ANTHROPIC_AUTH_TOKEN` keduanya diatur, `client.auth_token` sekarang bernilai `nil`. `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN` yang kosong sekarang dianggap tidak diatur, sedangkan versi sebelumnya membiarkan `ANTHROPIC_API_KEY` yang kosong menyembunyikan token dan semua yang ada setelahnya.

    Ketika tidak ada kredensial yang diteruskan dan `ANTHROPIC_API_KEY` serta `ANTHROPIC_AUTH_TOKEN` keduanya diatur, SDK juga memberi peringatan satu kali untuk setiap proses, pada standard error melalui `Kernel#warn`: `Anthropic: ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN are both set. Using ANTHROPIC_API_KEY.` Hapus pengaturan variabel yang tidak Anda gunakan untuk membungkamnya.

    ```ruby
    # Sebelumnya: kunci dikirim dan token diabaikan.
    # Sesudahnya: ArgumentError, "Pass at most one of `api_key:`, `auth_token:`, `credentials:`, or `config:`. Received `api_key:`, `auth_token:`."
    Anthropic::Client.new(api_key: api_key, auth_token: auth_token)

    # Teruskan hanya yang ingin Anda kirim.
    Anthropic::Client.new(api_key: api_key)
    ```
  </Tab>
</Tabs>

### Perubahan pada satu SDK atau CLI

Setiap perubahan ini memengaruhi satu SDK atau CLI.

<Tabs exclude="shell:cURL, python, typescript">
  <Tab title="CLI">
    **`--api-key` dan `--auth-token` dihapus.** `ant` tidak lagi menerima kunci API atau token autentikasi sebagai nilai flag, karena nilai di baris perintah terlihat dalam riwayat shell dan daftar proses. Kedua flag telah mencetak peringatan penghentian sejak v1.27.0. Perintah yang masih meneruskan salah satunya akan berhenti dengan `flag provided but not defined`.

    | Dihapus                | Gunakan sebagai gantinya                                      |
    | ---------------------- | ------------------------------------------------------------- |
    | `--api-key <key>`      | `ANTHROPIC_API_KEY`, `--api-key-stdin`, atau `ant auth login` |
    | `--auth-token <token>` | `ANTHROPIC_AUTH_TOKEN` atau `--auth-token-stdin`              |

    ```bash
    # Sebelum
    ant --api-key "$KEY" models list

    # Sesudah, dari environment
    export ANTHROPIC_API_KEY="$KEY"
    ant models list

    # Sesudah, dari pengelola rahasia
    op read op://vault/anthropic/api-key | ant --api-key-stdin models list
    ```

    `--api-key-stdin` dan `--auth-token-stdin` membaca seluruh standard input, sehingga perintah yang menggunakan salah satunya mengambil body permintaannya dari flag.

    `ant auth status`, prompt pertama kali dari `ant apply`, dan catatan tentang beberapa sumber autentikasi sekarang menyebut kredensial ini `ANTHROPIC_API_KEY` dan `ANTHROPIC_AUTH_TOKEN`, di mana sebelumnya mencetak `--api-key / ANTHROPIC_API_KEY` dan `--auth-token / ANTHROPIC_AUTH_TOKEN`.
  </Tab>

  <Tab title="C#">
    **`Type` dari union adalah enum.** Di v12, properti `Type` dari class union, seperti `ContentBlock.Type` atau `RawMessageStreamEvent.Type`, adalah `JsonElement`. Di v13 ia adalah `ApiEnum<string, T>`, di mana `T` adalah enum baru dengan satu anggota untuk setiap varian, seperti `ContentBlockType`. Beberapa union dibedakan berdasarkan `Name` atau `Command`, seperti `BetaMemoryTool20250818Command.Command`, dan properti tersebut berubah dengan cara yang sama. `Type` dari class varian, seperti `TextBlock.Type`, masih berupa `JsonElement`.

    ```csharp
    // Sebelum
    if (block.Type.GetString() == "tool_use") { }

    // Sesudah
    if (block.Type.Value() == ContentBlockType.ToolUse) { }
    ```

    `block.Type.Raw()` mengembalikan string-nya, termasuk string yang tidak memiliki anggota enum di versi SDK ini.

    **`IChatClient` mengabaikan opsi sampling.** Adapter `IChatClient` (`AsIChatClient()`) sekarang mengabaikan `ChatOptions.Temperature`, `ChatOptions.TopK`, dan `ChatOptions.TopP`. Lihat [Parameter sampling dihapus](https://platform.claude.com/docs/id/api/migration-2026-10-21#sampling-parameters).
  </Tab>

  <Tab title="Go">
    **Go 1.25 atau yang lebih baru diperlukan.**

    **`vertex.DefaultVersion` dan `bedrock.DefaultVersion` dihapus.**
  </Tab>

  <Tab title="Java">
    **Getter yang sekarang mengembalikan `Optional`.** `apiKey()` dan `authToken()` pada `AnthropicBackend` sekarang mengembalikan `Optional<String>`, seperti yang sudah dilakukan `apiKey()` pada `AwsBackend` dan `BedrockMantleBackend`. Di v2, masing-masing mengembalikan `String`, yang bernilai `null` ketika `AnthropicBackend` tidak memiliki kredensial jenis tersebut.

    ```java
    // Sebelum
    String apiKey = backend.apiKey();
    if (apiKey != null) {}

    // Sesudah
    Optional<String> apiKey = backend.apiKey();
    if (apiKey.isPresent()) {}
    ```

    Getter berikut sekarang juga mengembalikan `Optional`. Di v2, masing-masing mengembalikan nilainya sendiri, yang bernilai `null` ketika tidak ada:

    * `apiKey()` dan `awsCredentialsProvider()` pada `BedrockBackend`
    * `filename()` dan `mimeType()` pada `McpResourceFile`
    * `detail()` pada `CredentialSource`
    * `body()` pada `HttpRequest`
    * `resource()` pada `FoundryBackend`, yang sebelumnya `getResource()`
    * `responseValidation()`, `timeout()`, `followRedirects()`, `fallbackState()`, dan `openTelemetry()` pada `RequestOptions`, yang sebelumnya `getResponseValidation()`, `getTimeout()`, `getFollowRedirects()`, `getFallbackState()`, dan `getOpenTelemetry()`

    ```java
    // Sebelum
    String filename = file.filename();
    if (filename != null) {}
    String resource = backend.getResource();

    // Sesudah
    Optional<String> filename = file.filename();
    if (filename.isPresent()) {}
    Optional<String> resource = backend.resource();
    ```

    `getBaseUrl()` pada `FoundryBackend` dihapus. Panggil `baseUrl()`, yang mengembalikan URL tujuan permintaan. Itu adalah base URL yang Anda atur, atau yang dibuat dari resource, dan diakhiri dengan `/anthropic`.

    `getBaseUrl()` pada `AnthropicBackend` juga dihapus. Panggil `baseUrl()`, yang mengembalikan nilai yang sama.

    **`HttpRequest` memerlukan base URL.** Jika Anda membuat `HttpRequest` sendiri, seperti dalam pengujian interceptor, atur base URL-nya. Tanpanya, `build()` sekarang melempar `IllegalStateException`. Di v2, ia mengembalikan permintaan yang `baseUrl()`-nya bernilai `null`. Permintaan yang dibuat SDK sudah memilikinya.

    ```java
    // Sebelum
    HttpRequest request = HttpRequest.builder()
        .method(HttpMethod.GET)
        .build();

    // Sesudah
    HttpRequest request = HttpRequest.builder()
        .method(HttpMethod.GET)
        .baseUrl("https://api.anthropic.com")
        .build();
    ```

    `baseUrl()` masih mengembalikan `String`, yang sekarang tidak pernah bernilai `null`. Pada builder, `baseUrl(Optional<String>)` dihapus dan `baseUrl(String)` tidak lagi menerima `null`.

    **Interceptor melihat `anthropic-version`.** Klien sekarang menambahkan header `anthropic-version` default sebelum interceptor berjalan. Di v2, backend menambahkannya setelah interceptor. Jika interceptor Anda mengatur versinya sendiri, panggil `replaceHeaders`, karena `putHeader` sekarang menambahkan nilai kedua:

    ```java
    // Sebelum
    request.toBuilder()
        .putHeader("anthropic-version", version)
        .build();

    // Sesudah
    request.toBuilder()
        .replaceHeaders("anthropic-version", version)
        .build();
    ```
  </Tab>

  <Tab title="PHP">
    **Enum case yang Anda teruskan dibaca kembali sebagai nilainya.** `with()` dan setter seperti `withAllowedCallers()` masih menerima enum case atau nilainya. Versi sebelumnya mempertahankan case sebagaimana Anda meneruskannya. v1 mempertahankan nilai case tersebut, yang memang dideklarasikan oleh tipe properti. Objek yang dibuat SDK dari respons tidak berubah, dan JSON yang dikirim SDK sama. Jika Anda membaca kembali properti dan membandingkannya dengan case, perbandingan sekarang bernilai false dan tidak ada yang dilempar, jadi bandingkan dengan nilai case tersebut:

    ```php
    $tool = CodeExecutionTool20250825::with(allowedCallers: [AllowedCaller::DIRECT]);

    // Sebelum
    in_array(AllowedCaller::DIRECT, $tool->allowedCallers, true);

    // Sesudah
    in_array(AllowedCaller::DIRECT->value, $tool->allowedCallers, true);
    ```
  </Tab>

  <Tab title="Ruby">
    **`Anthropic::VertexClient::DEFAULT_VERSION` dan `Anthropic::BedrockClient::DEFAULT_VERSION` dihapus.**
  </Tab>
</Tabs>

### Lisensinya adalah Apache 2.0

Mulai dari versi-versi di bawah [Beralih ke 2026-10-21](https://platform.claude.com/docs/id/api/migration-2026-10-21#upgrade), SDK dan CLI dilisensikan di bawah Apache License, Version 2.0. Versi sebelumnya tetap berada di bawah MIT License. Tidak ada perubahan kode yang diperlukan. Jika Anda melacak lisensi dependensi Anda, perbarui entrinya.

* **TypeScript:** Paket platform (`@anthropic-ai/bedrock-sdk`, `@anthropic-ai/vertex-sdk`, `@anthropic-ai/foundry-sdk`, `@anthropic-ai/aws-sdk`, dan `@anthropic-ai/google-cloud-sdk`) berganti lisensi dalam rilis 1.0.0 masing-masing.
* **C#:** Paket lainnya (`Anthropic.Bedrock`, `Anthropic.Vertex`, `Anthropic.Foundry`, `Anthropic.Aws`, `Anthropic.GoogleCloud`, dan `Anthropic.Mcp`) berganti lisensi dalam rilis 1.0.0 masing-masing.
* **Java:** Perubahan ini mencakup setiap artefak `com.anthropic`.
