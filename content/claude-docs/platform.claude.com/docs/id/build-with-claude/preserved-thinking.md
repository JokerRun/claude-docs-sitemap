---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 240324f31316bfe7515b96a365fde3582a60f6b9d1a8ab46b612218d84608d28
---

---
title: Pemikiran yang dipertahankan
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking
description: Pada model Claude yang menjalankan pemeriksaan prefiks, pemikiran yang dipertahankan menentukan apakah model dapat menggunakan blok pemikiran yang Anda kirim kembali dari giliran sebelumnya.
featureMetadata:
  status: stable
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-opus-5-5
    - claude-sonnet-5-5
    - claude-haiku-5-5
  supportedPlatforms:
    Claude API: stable
    Amazon Bedrock: stable
    Amazon Bedrock (bedrock-runtime): stable
    Claude Platform on AWS: stable
    Claude Models on Google Cloud (Anthropic managed): stable
    Claude Models on Google Cloud (Google managed): stable
    Microsoft Foundry: stable
---

Claude dapat melanjutkan penalarannya dari giliran sebelumnya ketika kode Anda mengirim kembali “thinking block” (blok pemikiran). *Preserved thinking* (pemikiran yang dipertahankan) menentukan blok mana yang dapat digunakan Claude. Pada [model dengan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes), blok yang dapat digunakan tetap berada dalam konteks dan ditagih sebagai input. [Kirim kembali giliran asisten persis apa adanya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#append-assistant-turns-exactly-as-returned) seperti yang dikembalikan API.

Jika sebuah permintaan sudah gagal dengan `The block is bound to a different conversation`, mulailah dari [Perbaiki blok pemikiran yang terikat ke percakapan lain](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation).

## Blok pemikiran terikat pada apa

Pada model-model ini, sebuah blok pemikiran terikat pada hal-hal berikut:

* **Apa yang ada sebelumnya:** `system`, `tools`, dan setiap pesan sebelumnya. Jika salah satunya berubah, blok tersebut gagal dalam [“prefix check” (pemeriksaan prefiks)](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check), dan permintaan dapat mendapatkan error 400. Jadi, hanya tambahkan ke percakapan (lihat [Ubah alat atau instruksi tanpa gagal dalam pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions)).
* **Model:** sebuah model hanya membaca blok pemikiran dari sebagian model lain (lihat [Peralihan model mana yang mempertahankan penalaran di Claude API](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#which-model-switches-keep-reasoning)).
* **Akun:** blok dari beberapa model terikat pada sebuah akun (lihat [Akun dan platform cloud](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking)).

[`prefix_mismatch_behavior`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#preserved-thinking-controls) memilih apakah permintaan yang gagal dalam pemeriksaan prefiks mendapatkan error 400 atau API tidak menyertakan blok yang gagal dalam pemeriksaan prefiks. [`input_transformations`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#input-transformations) pada respons mencantumkan blok pemikiran yang tidak disertakan atau diloloskan oleh API. Tidak menyertakan pemikiran memiliki biaya (lihat [Biaya tidak menyertakan pemikiran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#drop-block-cost)).

## Beralih model dan kembali lagi

Ubah `model` dan tetap kirim seluruh percakapan. Blok pemikiran yang tidak dapat digunakan oleh model atau akun baru tidak pernah menyebabkan error. API tidak menyertakannya dalam permintaan tersebut dan tidak menagihnya, dan Claude menjawab tanpa penalaran tersebut.

Pada [model dengan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes), [`thinking: {"type": "enabled"}`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#thinking-type-on-switch) menghasilkan error 400, dan permintaan yang gagal dalam [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check) dapat mendapatkan error tersebut.

<Frame>
  ![Satu riwayat dikirim ke Claude Fable 5.1, Claude Opus 5.5, lalu Claude Fable 5.1: bloknya tidak disertakan sekali, lalu dibaca lagi](https://platform.claude.com/docs/id/images/preserved-thinking-switch-and-back.svg)
</Frame>

Claude Opus 5.5 tidak dapat membaca blok Claude Fable 5.1, sehingga API tidak menyertakannya dalam permintaan Claude Opus 5.5. Kembali ke Claude Fable 5.1, blok-blok tersebut dibaca lagi, karena API tidak pernah mengubah `messages` Anda. Saat beralih, penalaran hilang secara permanen hanya jika kode Anda menghapusnya. Jadi, jangan hapus pemikiran, dan jangan simpan riwayat terpisah untuk setiap model.

Blok yang tidak disertakan tidak dihitung sebagai perubahan pada percakapan, sehingga blok dari kedua model tetap valid.

## Peralihan yang tidak dilakukan oleh kode Anda

Router, [fallback setelah penolakan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#after-a-refusal), atau fallback sisi server dapat mengalihkan model untuk Anda, dan [model dari penyedia lain dapat mengambil satu giliran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#other-provider-turns). Tetap kirim seluruh percakapan. Giliran yang memuat blok `fallback` memiliki aturannya sendiri. Untuk blok mana yang tidak perlu disertakan, lihat [Melanjutkan percakapan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#continuing-the-conversation).

Peralihan apa pun dapat memilih model yang tidak menerima pesan sistem. Lihat [Ketika model tidak menerima pesan sistem](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#unchosen-switches-details).

## Akun dan platform cloud

Perpindahan ke akun atau platform cloud lain bekerja dengan cara yang sama: tetap kirim riwayat lengkap.

Blok pemikiran dari Claude Fable 5.2, Claude Mythos 5.2, Claude Sonnet 5.5, dan Claude Haiku 5.5 hanya berfungsi di akun yang menghasilkannya atau di akun yang tertaut dengannya. Di akun lain mana pun, API tidak menyertakannya, tanpa error.

[Apa yang dihitung sebagai akun Anda](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#accounts-by-platform) bergantung pada platform.

## Rahasia dan teks yang tidak tepercaya

Kirim [file yang tidak akan diharapkan pengguna Anda untuk dipercaya oleh Claude](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#untrusted-text) hanya dalam blok `tool_result`. Ketika Anda [menghapus rahasia, data pribadi, atau teks yang disuntikkan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#remove-sensitive-content) dari riwayat Anda, hapus juga setiap blok pemikiran setelah tempat pertama kemunculannya. Claude kemudian bekerja tanpa penalaran tersebut.

## Minta agen memeriksa kode Anda

Di Claude Code, jalankan `claude update`, lalu prompt ini di repositori yang membangun permintaan Anda:

Biarkan Claude Code memeriksa kode Anda untuk Anda

```text
/claude-api preserved-thinking-migration
```

Dengan agen lain, berikan [Ubah alat atau instruksi tanpa gagal dalam pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions) kepadanya, dan minta agen tersebut memperbaiki setiap tempat di mana kode Anda mengubah `system`, `tools`, atau pesan sebelumnya di antara permintaan.

## Detail teknis

### Peralihan model mana yang mempertahankan penalaran di Claude API

Tanda pisah berarti model tujuan tidak dapat membaca blok tersebut. Setelah beberapa kali peralihan, baca satu baris untuk setiap model dalam riwayat Anda.

| Model asal                              | Ke Claude Fable 5.2 atau Claude Mythos 5.2 | Ke Claude Fable 5.1 atau Claude Mythos 5.1 | Ke Claude Opus 5.5 | Ke Claude Sonnet 5.5 | Ke Claude Haiku 5.5 |
| --------------------------------------- | ------------------------------------------ | ------------------------------------------ | ------------------ | -------------------- | ------------------- |
| Claude Haiku 5.5                        | ✅                                          | —                                          | ✅                  | ✅                    | ✅                   |
| Claude Sonnet 5.5                       | ✅                                          | —                                          | ✅                  | ✅                    | —                   |
| Claude Opus 5                           | ✅                                          | ✅                                          | ✅                  | —                    | —                   |
| Claude Opus 5.5                         | ✅                                          | ✅                                          | ✅                  | —                    | —                   |
| Claude Fable 5 atau Claude Mythos 5     | ✅                                          | ✅                                          | —                  | —                    | —                   |
| Claude Fable 5.1 atau Claude Mythos 5.1 | ✅                                          | ✅                                          | —                  | —                    | —                   |
| Claude Fable 5.2 atau Claude Mythos 5.2 | ✅                                          | —                                          | —                  | —                    | —                   |

Jika sebuah model tidak memiliki baris atau kolom, gunakan [Model sebelumnya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#earlier-models).

### Model sebelumnya, seperti Claude Opus 5 dan Claude Sonnet 5

Setiap model Claude membaca blok dari Claude Opus 4.8, Claude Sonnet 5, Claude Haiku 4.5, serta model Claude Opus, Claude Sonnet, dan Claude Haiku sebelumnya.

| Model tujuan                                                                                                            | Hanya membaca blok dari                                                                |
| ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Claude Opus 4.8, Claude Sonnet 5, Claude Haiku 4.5, serta model Claude Opus, Claude Sonnet, dan Claude Haiku sebelumnya | Satu sama lain                                                                         |
| Claude Opus 5                                                                                                           | Dirinya sendiri, dan model-model di baris pertama                                      |
| Claude Fable 5 dan Claude Mythos 5                                                                                      | Satu sama lain, Claude Mythos Preview, Claude Opus 5, dan model-model di baris pertama |

### Pengaturan pemikiran pada model baru

[Model dengan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes) menolak `thinking: {"type": "enabled"}` dengan error 400. Ketika Anda memindahkan percakapan ke salah satu model tersebut dari model yang permintaannya menetapkan `"enabled"`, kirim `"adaptive"` sebagai gantinya. Tidak menyertakan `thinking` juga memberikan pemikiran adaptif pada model-model ini.

### Ketika model tidak menerima pesan sistem

Jika sebuah model tidak ada dalam [daftar model yang menerima pesan sistem](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages), jangan sertakan pesan sistem hanya dalam permintaan ke model tersebut. Tetap simpan pesan-pesan itu dalam riwayat tersimpan Anda. Kembali ke model yang menerimanya, kirim lagi riwayat tersimpan lengkap. Kembali tanpa pesan-pesan tersebut merupakan perubahan, dan permintaan dapat mendapatkan error 400 tersebut.

### Setelah penolakan

Tidak satu pun dari [model fallback yang diizinkan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#naming-your-own-fallback-models) dapat membaca pemikiran model yang menolak, sehingga model fallback menjawab tanpa pemikiran tersebut. Kembali ke model yang Anda minta, Claude membaca pemikiran dari kedua model.

### Giliran dari model penyedia lain

Giliran dari model penyedia lain ditempatkan di akhir, sebagai konten `text` dan `tool_use`. Pemikiran Claude sebelumnya tetap valid.

### Apa yang dihitung sebagai akun Anda di setiap platform

| Tempat Anda memanggil Claude                                                                                  | Akun Anda                |
| ------------------------------------------------------------------------------------------------------------- | ------------------------ |
| Claude API, Claude Platform on AWS, Claude Models on Google Cloud (Anthropic managed), atau Microsoft Foundry | Organisasi Anda          |
| Amazon Bedrock                                                                                                | Akun AWS Anda            |
| Claude Models on Google Cloud (Google managed)                                                                | Proyek Google Cloud Anda |

API juga dapat tidak menyertakan blok pemikiran yang dihasilkan oleh akun lain, jika akun tersebut tidak lagi dalam status baik. Hal ini berlaku untuk permintaan ke model Claude Fable dan Claude Mythos, Claude Opus 5, Claude Opus 5.5, Claude Sonnet 5.5, dan Claude Haiku 5.5. Permintaan tetap berhasil, dan model menjawab tanpa penalaran dari blok tersebut.

## Ketersediaan

Pemikiran yang dipertahankan tersedia di model tertentu.

### Dukungan API

Model dengan pemikiran yang dipertahankan tercantum di [Apa yang dilakukan setiap model ketika pemeriksaan prefiks gagal](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes).

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Selalu aktif

| Status   | Platform cloud                                                                                                                                                                                                                                                                                                                                                                   | Model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tersedia | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | [Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/overview), [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview), [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview), [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview) |
| Tersedia | [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)                                                                                                                                                                                                                                                                                 | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview)                                                                                                                                                                                                                                                              |
| Tersedia | [Amazon Bedrock (bedrock-runtime)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)                                                                                                                                                                                                                                                        | [Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/overview), [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview)                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Tersedia | [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed)                                                                                                                                                                                                                       | [Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/overview), [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview)                                                                                                                                                                                                                                                                                                                                                                                                                                  |

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Selalu aktif

| Status   | Platform cloud                                                                                                                                                                                                                                                                 | Model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tersedia | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) | [Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/overview), [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview), [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview), [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview) |

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Pemeriksaan prefiks pada blok pemikiran" icon="shield" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks">
    Apa yang dibandingkan oleh pemeriksaan prefiks, apa yang terjadi ketika sebuah permintaan gagal dalam pemeriksaan prefiks, dan cara menangani kedua kasus.
  </Card>

  <Card title="Ubah alat atau instruksi tanpa gagal dalam pemeriksaan prefiks" icon="edit" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions">
    Apa yang harus dikirim sebagai pengganti setiap perubahan yang dilakukan kode Anda pada percakapan.
  </Card>

  <Card title="Perbaiki blok pemikiran yang terikat ke percakapan lain" icon="wrench" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation">
    Pulihkan percakapan yang gagal, dan lihat biaya tidak menyertakan pemikiran.
  </Card>
</CardGroup>
