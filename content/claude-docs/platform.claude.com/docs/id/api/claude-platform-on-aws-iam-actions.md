---
source: platform
url: https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 98a26f0039ea597aed35125b4b3210f01ad5b29b3527fd779a4160c660e381dc
---

---
title: Tindakan IAM untuk Claude Platform on AWS
url: https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions
description: Referensi tindakan IAM untuk mengontrol akses ke Claude Platform on AWS melalui kebijakan AWS.
---

Claude Platform on AWS menggunakan AWS IAM untuk kontrol akses. Setiap rute API dipetakan ke sebuah tindakan IAM dalam namespace `aws-external-anthropic`. Halaman ini mencantumkan semua tindakan, rute yang diotorisasi oleh setiap tindakan, dan "managed policies" (kebijakan terkelola) yang tersedia untuk pola akses umum. Untuk penyiapan platform dan autentikasi, lihat [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws).

## Detail layanan

| Atribut                 | Nilai                    |
| ----------------------- | ------------------------ |
| **Prefiks layanan IAM** | `aws-external-anthropic` |
| **Tipe sumber daya**    | `workspace`              |

Format ARN workspace:

```text wrap
arn:aws:aws-external-anthropic:{region}:{account-id}:workspace/{workspace-id}
```

Region ARN selalu terisi dan sesuai dengan region tempat workspace terikat. Segmen sumber daya adalah ID workspace bertag (`wrkspc_...`), nilai yang sama dengan yang Anda kirimkan dalam header `anthropic-workspace-id`.

## Tindakan

Layanan ini mendefinisikan 71 tindakan. Tindakan mengikuti konvensi `VerbNoun` AWS dan menggunakan disiplin kata kerja sehingga wildcard `Get*` dan `List*` menghasilkan batas hanya-baca yang bersih.

### Inferensi

| Tindakan          | Rute yang diotorisasi            |
| ----------------- | -------------------------------- |
| `CreateInference` | `POST /v1/messages`              |
| `CountTokens`     | `POST /v1/messages/count_tokens` |

### Pemrosesan batch

| Tindakan               | Rute yang diotorisasi                                                   |
| ---------------------- | ----------------------------------------------------------------------- |
| `CreateBatchInference` | `POST /v1/messages/batches`                                             |
| `GetBatchInference`    | `GET /v1/messages/batches/{id}` `GET /v1/messages/batches/{id}/results` |
| `ListBatchInferences`  | `GET /v1/messages/batches`                                              |
| `CancelBatchInference` | `POST /v1/messages/batches/{id}/cancel`                                 |
| `DeleteBatchInference` | `DELETE /v1/messages/batches/{id}`                                      |

<Note>
  `GetBatchInference` mengotorisasi pembacaan metadata batch maupun pengunduhan hasil batch. Wildcard `Get*` pada kebijakan `AnthropicReadOnlyAccess`, `AnthropicInferenceAccess`, dan `AnthropicLimitedAccess` mencakup tindakan ini.
</Note>

### Model

| Tindakan     | Rute yang diotorisasi |
| ------------ | --------------------- |
| `GetModel`   | `GET /v1/models/{id}` |
| `ListModels` | `GET /v1/models`      |

### File

| Tindakan     | Rute yang diotorisasi                             |
| ------------ | ------------------------------------------------- |
| `CreateFile` | `POST /v1/files`                                  |
| `GetFile`    | `GET /v1/files/{id}` `GET /v1/files/{id}/content` |
| `ListFiles`  | `GET /v1/files`                                   |
| `DeleteFile` | `DELETE /v1/files/{id}`                           |

<Note>
  `GetFile` mengotorisasi pengunduhan metadata maupun konten. Principal dengan akses hanya-baca dapat mengunduh byte file, bukan hanya mencantumkan file.
</Note>

### Skill

| Tindakan      | Rute yang diotorisasi                                                                                                                          |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `CreateSkill` | `POST /v1/skills`                                                                                                                              |
| `GetSkill`    | `GET /v1/skills/{id}` `GET /v1/skills/{id}/versions` `GET /v1/skills/{id}/versions/{version}` `GET /v1/skills/{id}/versions/{version}/content` |
| `ListSkills`  | `GET /v1/skills`                                                                                                                               |
| `UpdateSkill` | `POST /v1/skills/{id}/versions` `DELETE /v1/skills/{id}/versions/{version}`                                                                    |
| `DeleteSkill` | `DELETE /v1/skills/{id}`                                                                                                                       |

<Note>
  `GetSkill` mengotorisasi pengunduhan metadata skill maupun konten skill. Principal dengan akses hanya-baca dapat mengunduh byte skill, bukan hanya mencantumkan skill.
</Note>

<Note>
  Membuat atau menghapus versi skill individual dipetakan ke `UpdateSkill`, bukan `CreateSkill` atau `DeleteSkill`. Kebijakan yang menolak `aws-external-anthropic:Delete*` tetap mengizinkan penghapusan versi, dan kebijakan yang menolak `aws-external-anthropic:Create*` tetap mengizinkan pembuatan versi. Tolak juga `UpdateSkill` dan `CreateSkill` jika Anda perlu mencegah mutasi skill apa pun.
</Note>

### Agen

| Tindakan       | Rute yang diotorisasi                                |
| -------------- | ---------------------------------------------------- |
| `CreateAgent`  | `POST /v1/agents`                                    |
| `GetAgent`     | `GET /v1/agents/{id}` `GET /v1/agents/{id}/versions` |
| `ListAgents`   | `GET /v1/agents`                                     |
| `UpdateAgent`  | `POST /v1/agents/{id}`                               |
| `ArchiveAgent` | `POST /v1/agents/{id}/archive`                       |

<Note>
  Agen hanya mendukung pengarsipan, bukan penghapusan permanen. Kebijakan yang menolak `aws-external-anthropic:Delete*` tidak memblokir `ArchiveAgent`. Tolak `ArchiveAgent`, `UpdateAgent`, dan `CreateAgent` jika Anda perlu mencegah mutasi agen apa pun.
</Note>

### Sesi

| Tindakan         | Rute yang diotorisasi                                                                                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CreateSession`  | `POST /v1/sessions`                                                                                                                                                           |
| `GetSession`     | `GET /v1/sessions/{id}` `GET /v1/sessions/{id}/events` `GET /v1/sessions/{id}/events/stream` `GET /v1/sessions/{id}/resources` `GET /v1/sessions/{id}/resources/{id}`         |
| `ListSessions`   | `GET /v1/sessions`                                                                                                                                                            |
| `UpdateSession`  | `POST /v1/sessions/{id}` `POST /v1/sessions/{id}/events` `POST /v1/sessions/{id}/resources` `POST /v1/sessions/{id}/resources/{id}` `DELETE /v1/sessions/{id}/resources/{id}` |
| `ArchiveSession` | `POST /v1/sessions/{id}/archive`                                                                                                                                              |
| `DeleteSession`  | `DELETE /v1/sessions/{id}`                                                                                                                                                    |

<Note>
  `GetSession` mengotorisasi pembacaan metadata sesi, aliran event lengkap (riwayat percakapan), dan sumber daya sesi. Wildcard `Get*` pada kebijakan `AnthropicReadOnlyAccess`, `AnthropicInferenceAccess`, dan `AnthropicLimitedAccess` mencakup tindakan ini.
</Note>

<Note>
  Membuat, memperbarui, atau menghapus sub-sumber daya sesi individual (event atau sumber daya sesi) dipetakan ke `UpdateSession`, bukan `CreateSession` atau `DeleteSession`. Kebijakan yang menolak `aws-external-anthropic:Delete*` tetap mengizinkan penghapusan sub-sumber daya, dan kebijakan yang menolak `aws-external-anthropic:Create*` tetap mengizinkan pembuatan sub-sumber daya. Tolak juga `UpdateSession`, `CreateSession`, dan `ArchiveSession` jika Anda perlu mencegah mutasi sesi apa pun.
</Note>

### Environment

| Tindakan                 | Rute yang diotorisasi                                                                                                                                                                                                                    |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CreateEnvironment`      | `POST /v1/environments`                                                                                                                                                                                                                  |
| `GetEnvironment`         | `GET /v1/environments/{id}` `GET /v1/environments/{id}/work` `GET /v1/environments/{id}/work/{work_id}` `GET /v1/environments/{id}/work/stats`                                                                                           |
| `ListEnvironments`       | `GET /v1/environments`                                                                                                                                                                                                                   |
| `UpdateEnvironment`      | `POST /v1/environments/{id}`                                                                                                                                                                                                             |
| `ArchiveEnvironment`     | `POST /v1/environments/{id}/archive`                                                                                                                                                                                                     |
| `DeleteEnvironment`      | `DELETE /v1/environments/{id}`                                                                                                                                                                                                           |
| `ProcessEnvironmentWork` | `GET /v1/environments/{id}/work/poll` `POST /v1/environments/{id}/work/{work_id}` `POST /v1/environments/{id}/work/{work_id}/ack` `POST /v1/environments/{id}/work/{work_id}/heartbeat` `POST /v1/environments/{id}/work/{work_id}/stop` |

<Note>
  Kebijakan yang menolak `aws-external-anthropic:Delete*` tidak memblokir `ArchiveEnvironment`. `ProcessEnvironmentWork` tidak dicocokkan oleh wildcard `Create*`, `Update*`, `Delete*`, atau `Archive*`. Tolak juga `ArchiveEnvironment`, `UpdateEnvironment`, `CreateEnvironment`, dan `ProcessEnvironmentWork` jika Anda perlu mencegah mutasi environment apa pun.
</Note>

<Note>
  `ProcessEnvironmentWork` mengotorisasi worker [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) untuk melakukan polling, mengakui (acknowledge), mengirim heartbeat, menghentikan, dan memposting hasil pada item pekerjaan environment. Berikan hanya kepada principal yang menjalankan worker environment self-hosted. Kebijakan terkelola `AnthropicSelfHostedEnvironmentAccess` mencakup tindakan ini.
</Note>

### Vault

| Tindakan       | Rute yang diotorisasi                                                                                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CreateVault`  | `POST /v1/vaults`                                                                                                                                                                           |
| `GetVault`     | `GET /v1/vaults/{id}` `GET /v1/vaults/{id}/credentials` `GET /v1/vaults/{id}/credentials/{id}`                                                                                              |
| `ListVaults`   | `GET /v1/vaults`                                                                                                                                                                            |
| `UpdateVault`  | `POST /v1/vaults/{id}` `POST /v1/vaults/{id}/credentials` `POST /v1/vaults/{id}/credentials/{id}` `POST /v1/vaults/{id}/credentials/{id}/archive` `DELETE /v1/vaults/{id}/credentials/{id}` |
| `ArchiveVault` | `POST /v1/vaults/{id}/archive`                                                                                                                                                              |
| `DeleteVault`  | `DELETE /v1/vaults/{id}`                                                                                                                                                                    |

<Note>
  Membuat, memperbarui, mengarsipkan, atau menghapus kredensial vault individual dipetakan ke `UpdateVault`. Membaca kredensial dipetakan ke `GetVault`. Rahasia kredensial vault tidak diekspos: field rahasia bersifat hanya-tulis dan tidak pernah dikembalikan oleh `GetVault` (lihat [Autentikasi dengan vault](https://platform.claude.com/docs/id/managed-agents/vaults)). Kebijakan yang menolak `aws-external-anthropic:Delete*` tetap mengizinkan penghapusan kredensial, dan kebijakan yang menolak `aws-external-anthropic:Create*` tetap mengizinkan pembuatan kredensial. Tolak juga `UpdateVault`, `CreateVault`, dan `ArchiveVault` jika Anda perlu mencegah mutasi vault apa pun.
</Note>

### Memory store

| Tindakan             | Rute yang diotorisasi                                                                                                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `CreateMemoryStore`  | `POST /v1/memory_stores`                                                                                                                                                                                                 |
| `GetMemoryStore`     | `GET /v1/memory_stores/{id}` `GET /v1/memory_stores/{id}/memories` `GET /v1/memory_stores/{id}/memories/{id}` `GET /v1/memory_stores/{id}/memory_versions` `GET /v1/memory_stores/{id}/memory_versions/{id}`             |
| `ListMemoryStores`   | `GET /v1/memory_stores`                                                                                                                                                                                                  |
| `UpdateMemoryStore`  | `POST /v1/memory_stores/{id}` `POST /v1/memory_stores/{id}/memories` `POST /v1/memory_stores/{id}/memories/{id}` `DELETE /v1/memory_stores/{id}/memories/{id}` `POST /v1/memory_stores/{id}/memory_versions/{id}/redact` |
| `ArchiveMemoryStore` | `POST /v1/memory_stores/{id}/archive`                                                                                                                                                                                    |
| `DeleteMemoryStore`  | `DELETE /v1/memory_stores/{id}`                                                                                                                                                                                          |

<Note>
  `GetMemoryStore` mengotorisasi pembacaan metadata store, semua memori, dan riwayat versi memori. Wildcard `Get*` pada kebijakan `AnthropicReadOnlyAccess`, `AnthropicInferenceAccess`, dan `AnthropicLimitedAccess` mencakup tindakan ini.
</Note>

<Note>
  Membuat, memperbarui, atau menghapus memori individual dan meredaksi versi memori keduanya dipetakan ke `UpdateMemoryStore`, bukan `CreateMemoryStore` atau `DeleteMemoryStore`. Kebijakan yang menolak `aws-external-anthropic:Delete*` tetap mengizinkan penghapusan memori individual dan redaksi versi memori, dan kebijakan yang menolak `aws-external-anthropic:Create*` tetap mengizinkan pembuatan memori individual. Tolak juga `UpdateMemoryStore`, `CreateMemoryStore`, dan `ArchiveMemoryStore` jika Anda perlu mencegah mutasi memory store apa pun.
</Note>

### Webhook

| Tindakan              | Rute yang diotorisasi                              |
| --------------------- | -------------------------------------------------- |
| `CreateWebhook`       | `POST /v1/webhooks`                                |
| `GetWebhook`          | `GET /v1/webhooks/{id}`                            |
| `ListWebhooks`        | `GET /v1/webhooks`                                 |
| `UpdateWebhook`       | `POST /v1/webhooks/{id}`                           |
| `DeleteWebhook`       | `DELETE /v1/webhooks/{id}`                         |
| `RotateWebhookSecret` | `POST /v1/webhooks/{id}/regenerate_signing_secret` |

<Note>
  Rahasia penandatanganan webhook bersifat hanya-tulis. `GetWebhook` hanya mengembalikan metadata webhook; tidak mengembalikan rahasia penandatanganan.
</Note>

<Note>
  `RotateWebhookSecret` tidak dicocokkan oleh wildcard `aws-external-anthropic:Create*`, `Update*`, atau `Delete*`. Kebijakan yang menolak pola-pola tersebut tetap mengizinkan rotasi rahasia. Tolak `RotateWebhookSecret`, `UpdateWebhook`, `CreateWebhook`, dan `DeleteWebhook` jika Anda perlu mencegah mutasi webhook apa pun.
</Note>

### Profil pengguna

| Tindakan            | Rute yang diotorisasi         |
| ------------------- | ----------------------------- |
| `CreateUserProfile` | `POST /v1/user_profiles`      |
| `GetUserProfile`    | `GET /v1/user_profiles/{id}`  |
| `ListUserProfiles`  | `GET /v1/user_profiles`       |
| `UpdateUserProfile` | `POST /v1/user_profiles/{id}` |

<Warning>
  Pencocokan tindakan IAM tidak peka huruf besar/kecil. Wildcard `aws-external-anthropic:*File` cocok dengan `CreateFile`, `GetFile`, dan `DeleteFile`, tetapi tidak cocok dengan `ListFiles` (yang berakhiran "files", bukan "file"). Wildcard ini juga secara berlebihan cocok dengan `CreateUserProfile`, `GetUserProfile`, dan `UpdateUserProfile` karena "Profile" berakhiran "file". Jika Anda bermaksud memberikan atau menolak hanya tindakan Files API, sebutkan secara eksplisit (`CreateFile`, `GetFile`, `ListFiles`, `DeleteFile`) alih-alih menggunakan pola sufiks `*File`.
</Warning>

### Workspace

| Tindakan           | Rute yang diotorisasi                            |
| ------------------ | ------------------------------------------------ |
| `CreateWorkspace`  | `POST /v1/organizations/workspaces`              |
| `GetWorkspace`     | `GET /v1/organizations/workspaces/{id}`          |
| `ListWorkspaces`   | `GET /v1/organizations/workspaces`               |
| `UpdateWorkspace`  | `POST /v1/organizations/workspaces/{id}`         |
| `ArchiveWorkspace` | `POST /v1/organizations/workspaces/{id}/archive` |

<Note>
  Workspace hanya mendukung pengarsipan, bukan penghapusan permanen. Kebijakan yang menolak `aws-external-anthropic:Delete*` tidak memblokir `ArchiveWorkspace`. Tolak `ArchiveWorkspace`, `UpdateWorkspace`, dan `CreateWorkspace` jika Anda perlu mencegah mutasi workspace apa pun.
</Note>

### Kunci enkripsi

| Tindakan      | Rute yang diotorisasi                         |
| ------------- | --------------------------------------------- |
| `RegisterKey` | `POST /v1/organizations/external_keys`        |
| `GetKey`      | `GET /v1/organizations/external_keys/{id}`    |
| `ListKeys`    | `GET /v1/organizations/external_keys`         |
| `UpdateKey`   | `POST /v1/organizations/external_keys/{id}`   |
| `DisableKey`  | `DELETE /v1/organizations/external_keys/{id}` |

<Note>
  Tindakan-tindakan ini mengelola registrasi [customer-managed encryption key (CMEK)](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws) organisasi Anda, yaitu catatan tentang ARN kunci AWS KMS mana yang terdaftar. Tindakan ini tidak membuat, mengubah, atau menonaktifkan kunci di AWS KMS. `DisableKey` menghapus registrasi dan ditolak selama masih ada workspace yang menggunakan kunci tersebut. `RegisterKey` dan `DisableKey` tidak dicocokkan oleh wildcard `Create*`, `Update*`, atau `Delete*`; tolak `RegisterKey`, `UpdateKey`, dan `DisableKey` jika Anda perlu mencegah perubahan apa pun pada registrasi kunci. Dalam rute-rute ini, `{id}` adalah ARN kunci KMS yang di-URL-encode. Melampirkan kunci terdaftar ke workspace adalah operasi workspace, yang diotorisasi oleh `CreateWorkspace` atau `UpdateWorkspace`; principal yang melampirkan kunci juga memerlukan `kms:DescribeKey`, `kms:Encrypt`, dan `kms:Decrypt` pada kunci tersebut (lihat [prasyarat](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws)). Tindakan kunci eksternal bercakupan akun: menentukan ARN workspace pada tindakan tersebut tidak berpengaruh; gunakan `Resource: "*"`.
</Note>

### Kepatuhan

| Tindakan                   | Rute yang diotorisasi           |
| -------------------------- | ------------------------------- |
| `ListComplianceActivities` | `GET /v1/compliance/activities` |

<Note>
  `ListComplianceActivities` mengotorisasi pembacaan [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) dari [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api), yaitu log audit seluruh organisasi yang mencakup event transparansi akses. Rute ini mengembalikan error hingga Compliance API [diaktifkan untuk organisasi Anda](https://platform.claude.com/docs/id/manage-claude/compliance-api-access); pengaktifan dilakukan atas permintaan melalui tim akun Anthropic Anda. Wildcard `List*` pada kebijakan `AnthropicReadOnlyAccess`, `AnthropicInferenceAccess`, dan `AnthropicLimitedAccess` mencakup tindakan ini.
</Note>

<Note>
  `ListComplianceActivities` bercakupan akun, seperti `ListWorkspaces`. Menentukan ARN workspace pada tindakan ini tidak berpengaruh; gunakan `Resource: "*"`.
</Note>

### Autentikasi

| Tindakan              | Rute yang diotorisasi |
| --------------------- | --------------------- |
| `CallWithBearerToken` | (tidak ada)           |

`CallWithBearerToken` adalah izin lapisan autentikasi yang mengotorisasi principal untuk melakukan autentikasi melalui kunci API (bearer token) alih-alih AWS SigV4. Tindakan ini tidak dipetakan ke rute. Berikan bersama tindakan-tindakan yang dipetakan ke rute yang Anda inginkan dapat dilakukan oleh pemegang kunci API.

### Akses konsol

| Tindakan        | Rute yang diotorisasi |
| --------------- | --------------------- |
| `AssumeConsole` | (tidak ada)           |

`AssumeConsole` mengotorisasi principal untuk membuka Claude Console untuk workspace Claude Platform on AWS melalui alur federasi AWS Console. Tindakan ini tidak dipetakan ke rute. Berikan kepada principal yang seharusnya dapat mengklik **Open Claude Console** pada halaman layanan Claude Platform on AWS di AWS Console. Peran Claude Console (Admin atau Developer) ditetapkan secara terpisah oleh perwakilan akun Anthropic Anda; peran tersebut tidak diturunkan dari izin IAM principal. Lihat [Menggunakan Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console) untuk alur masuk dan deskripsi peran.

## Pemetaan rute ke tindakan

Tabel berikut mencantumkan setiap rute pada Claude Platform on AWS dan tindakan IAM yang diperlukan untuk memanggilnya. Setiap tindakan IAM juga mengotorisasi permintaan yang menggunakan header `anthropic-beta`; varian beta dari suatu rute tidak memerlukan tindakan IAM terpisah. CloudTrail mengklasifikasikan setiap tindakan sebagai Data event (operasi data-plane bervolume tinggi) atau Management event (operasi control-plane). Tindakan vault dan webhook diklasifikasikan sebagai Management event karena menyimpan rahasia (kredensial vault dan rahasia penandatanganan webhook) dan mendapat manfaat dari pencatatan audit yang aktif secara default. Tindakan workspace, kunci eksternal, dan kepatuhan juga diklasifikasikan sebagai Management event karena merupakan operasi control-plane bercakupan organisasi. Semua tindakan lainnya, termasuk inferensi, batch, model, file, skill, profil pengguna, dan tindakan Claude Managed Agents lainnya, diklasifikasikan sebagai Data event.

| Metode   | Rute                                                 | Tindakan IAM               | Tipe event CloudTrail |
| -------- | ---------------------------------------------------- | -------------------------- | --------------------- |
| `POST`   | `/v1/messages`                                       | `CreateInference`          | Data                  |
| `POST`   | `/v1/messages/count_tokens`                          | `CountTokens`              | Data                  |
| `POST`   | `/v1/messages/batches`                               | `CreateBatchInference`     | Data                  |
| `GET`    | `/v1/messages/batches`                               | `ListBatchInferences`      | Data                  |
| `GET`    | `/v1/messages/batches/{id}`                          | `GetBatchInference`        | Data                  |
| `GET`    | `/v1/messages/batches/{id}/results`                  | `GetBatchInference`        | Data                  |
| `POST`   | `/v1/messages/batches/{id}/cancel`                   | `CancelBatchInference`     | Data                  |
| `DELETE` | `/v1/messages/batches/{id}`                          | `DeleteBatchInference`     | Data                  |
| `GET`    | `/v1/models`                                         | `ListModels`               | Data                  |
| `GET`    | `/v1/models/{id}`                                    | `GetModel`                 | Data                  |
| `POST`   | `/v1/files`                                          | `CreateFile`               | Data                  |
| `GET`    | `/v1/files`                                          | `ListFiles`                | Data                  |
| `GET`    | `/v1/files/{id}`                                     | `GetFile`                  | Data                  |
| `GET`    | `/v1/files/{id}/content`                             | `GetFile`                  | Data                  |
| `DELETE` | `/v1/files/{id}`                                     | `DeleteFile`               | Data                  |
| `POST`   | `/v1/skills`                                         | `CreateSkill`              | Data                  |
| `GET`    | `/v1/skills`                                         | `ListSkills`               | Data                  |
| `GET`    | `/v1/skills/{id}`                                    | `GetSkill`                 | Data                  |
| `DELETE` | `/v1/skills/{id}`                                    | `DeleteSkill`              | Data                  |
| `POST`   | `/v1/skills/{id}/versions`                           | `UpdateSkill`              | Data                  |
| `GET`    | `/v1/skills/{id}/versions`                           | `GetSkill`                 | Data                  |
| `GET`    | `/v1/skills/{id}/versions/{version}`                 | `GetSkill`                 | Data                  |
| `GET`    | `/v1/skills/{id}/versions/{version}/content`         | `GetSkill`                 | Data                  |
| `DELETE` | `/v1/skills/{id}/versions/{version}`                 | `UpdateSkill`              | Data                  |
| `POST`   | `/v1/user_profiles`                                  | `CreateUserProfile`        | Data                  |
| `GET`    | `/v1/user_profiles`                                  | `ListUserProfiles`         | Data                  |
| `GET`    | `/v1/user_profiles/{id}`                             | `GetUserProfile`           | Data                  |
| `POST`   | `/v1/user_profiles/{id}`                             | `UpdateUserProfile`        | Data                  |
| `POST`   | `/v1/organizations/workspaces`                       | `CreateWorkspace`          | Management            |
| `GET`    | `/v1/organizations/workspaces`                       | `ListWorkspaces`           | Management            |
| `GET`    | `/v1/organizations/workspaces/{id}`                  | `GetWorkspace`             | Management            |
| `POST`   | `/v1/organizations/workspaces/{id}`                  | `UpdateWorkspace`          | Management            |
| `POST`   | `/v1/organizations/workspaces/{id}/archive`          | `ArchiveWorkspace`         | Management            |
| `POST`   | `/v1/organizations/external_keys`                    | `RegisterKey`              | Management            |
| `GET`    | `/v1/organizations/external_keys`                    | `ListKeys`                 | Management            |
| `GET`    | `/v1/organizations/external_keys/{id}`               | `GetKey`                   | Management            |
| `POST`   | `/v1/organizations/external_keys/{id}`               | `UpdateKey`                | Management            |
| `DELETE` | `/v1/organizations/external_keys/{id}`               | `DisableKey`               | Management            |
| `GET`    | `/v1/compliance/activities`                          | `ListComplianceActivities` | Management            |
| `POST`   | `/v1/agents`                                         | `CreateAgent`              | Data                  |
| `GET`    | `/v1/agents`                                         | `ListAgents`               | Data                  |
| `GET`    | `/v1/agents/{id}`                                    | `GetAgent`                 | Data                  |
| `POST`   | `/v1/agents/{id}`                                    | `UpdateAgent`              | Data                  |
| `POST`   | `/v1/agents/{id}/archive`                            | `ArchiveAgent`             | Data                  |
| `GET`    | `/v1/agents/{id}/versions`                           | `GetAgent`                 | Data                  |
| `POST`   | `/v1/sessions`                                       | `CreateSession`            | Data                  |
| `GET`    | `/v1/sessions`                                       | `ListSessions`             | Data                  |
| `GET`    | `/v1/sessions/{id}`                                  | `GetSession`               | Data                  |
| `POST`   | `/v1/sessions/{id}`                                  | `UpdateSession`            | Data                  |
| `POST`   | `/v1/sessions/{id}/archive`                          | `ArchiveSession`           | Data                  |
| `DELETE` | `/v1/sessions/{id}`                                  | `DeleteSession`            | Data                  |
| `GET`    | `/v1/sessions/{id}/events`                           | `GetSession`               | Data                  |
| `POST`   | `/v1/sessions/{id}/events`                           | `UpdateSession`            | Data                  |
| `GET`    | `/v1/sessions/{id}/events/stream`                    | `GetSession`               | Data                  |
| `GET`    | `/v1/sessions/{id}/resources`                        | `GetSession`               | Data                  |
| `GET`    | `/v1/sessions/{id}/resources/{id}`                   | `GetSession`               | Data                  |
| `POST`   | `/v1/sessions/{id}/resources`                        | `UpdateSession`            | Data                  |
| `POST`   | `/v1/sessions/{id}/resources/{id}`                   | `UpdateSession`            | Data                  |
| `DELETE` | `/v1/sessions/{id}/resources/{id}`                   | `UpdateSession`            | Data                  |
| `POST`   | `/v1/environments`                                   | `CreateEnvironment`        | Data                  |
| `GET`    | `/v1/environments`                                   | `ListEnvironments`         | Data                  |
| `GET`    | `/v1/environments/{id}`                              | `GetEnvironment`           | Data                  |
| `POST`   | `/v1/environments/{id}`                              | `UpdateEnvironment`        | Data                  |
| `POST`   | `/v1/environments/{id}/archive`                      | `ArchiveEnvironment`       | Data                  |
| `DELETE` | `/v1/environments/{id}`                              | `DeleteEnvironment`        | Data                  |
| `GET`    | `/v1/environments/{id}/work`                         | `GetEnvironment`           | Data                  |
| `GET`    | `/v1/environments/{id}/work/poll`                    | `ProcessEnvironmentWork`   | Data                  |
| `GET`    | `/v1/environments/{id}/work/{work_id}`               | `GetEnvironment`           | Data                  |
| `GET`    | `/v1/environments/{id}/work/stats`                   | `GetEnvironment`           | Data                  |
| `POST`   | `/v1/environments/{id}/work/{work_id}`               | `ProcessEnvironmentWork`   | Data                  |
| `POST`   | `/v1/environments/{id}/work/{work_id}/ack`           | `ProcessEnvironmentWork`   | Data                  |
| `POST`   | `/v1/environments/{id}/work/{work_id}/heartbeat`     | `ProcessEnvironmentWork`   | Data                  |
| `POST`   | `/v1/environments/{id}/work/{work_id}/stop`          | `ProcessEnvironmentWork`   | Data                  |
| `POST`   | `/v1/vaults`                                         | `CreateVault`              | Management            |
| `GET`    | `/v1/vaults`                                         | `ListVaults`               | Management            |
| `GET`    | `/v1/vaults/{id}`                                    | `GetVault`                 | Management            |
| `POST`   | `/v1/vaults/{id}`                                    | `UpdateVault`              | Management            |
| `POST`   | `/v1/vaults/{id}/archive`                            | `ArchiveVault`             | Management            |
| `DELETE` | `/v1/vaults/{id}`                                    | `DeleteVault`              | Management            |
| `GET`    | `/v1/vaults/{id}/credentials`                        | `GetVault`                 | Management            |
| `POST`   | `/v1/vaults/{id}/credentials`                        | `UpdateVault`              | Management            |
| `GET`    | `/v1/vaults/{id}/credentials/{id}`                   | `GetVault`                 | Management            |
| `POST`   | `/v1/vaults/{id}/credentials/{id}`                   | `UpdateVault`              | Management            |
| `POST`   | `/v1/vaults/{id}/credentials/{id}/archive`           | `UpdateVault`              | Management            |
| `DELETE` | `/v1/vaults/{id}/credentials/{id}`                   | `UpdateVault`              | Management            |
| `POST`   | `/v1/memory_stores`                                  | `CreateMemoryStore`        | Data                  |
| `GET`    | `/v1/memory_stores`                                  | `ListMemoryStores`         | Data                  |
| `GET`    | `/v1/memory_stores/{id}`                             | `GetMemoryStore`           | Data                  |
| `POST`   | `/v1/memory_stores/{id}`                             | `UpdateMemoryStore`        | Data                  |
| `POST`   | `/v1/memory_stores/{id}/archive`                     | `ArchiveMemoryStore`       | Data                  |
| `DELETE` | `/v1/memory_stores/{id}`                             | `DeleteMemoryStore`        | Data                  |
| `POST`   | `/v1/memory_stores/{id}/memories`                    | `UpdateMemoryStore`        | Data                  |
| `GET`    | `/v1/memory_stores/{id}/memories`                    | `GetMemoryStore`           | Data                  |
| `GET`    | `/v1/memory_stores/{id}/memories/{id}`               | `GetMemoryStore`           | Data                  |
| `POST`   | `/v1/memory_stores/{id}/memories/{id}`               | `UpdateMemoryStore`        | Data                  |
| `DELETE` | `/v1/memory_stores/{id}/memories/{id}`               | `UpdateMemoryStore`        | Data                  |
| `GET`    | `/v1/memory_stores/{id}/memory_versions`             | `GetMemoryStore`           | Data                  |
| `GET`    | `/v1/memory_stores/{id}/memory_versions/{id}`        | `GetMemoryStore`           | Data                  |
| `POST`   | `/v1/memory_stores/{id}/memory_versions/{id}/redact` | `UpdateMemoryStore`        | Data                  |
| `GET`    | `/v1/webhooks`                                       | `ListWebhooks`             | Management            |
| `GET`    | `/v1/webhooks/{id}`                                  | `GetWebhook`               | Management            |
| `POST`   | `/v1/webhooks`                                       | `CreateWebhook`            | Management            |
| `POST`   | `/v1/webhooks/{id}`                                  | `UpdateWebhook`            | Management            |
| `DELETE` | `/v1/webhooks/{id}`                                  | `DeleteWebhook`            | Management            |
| `POST`   | `/v1/webhooks/{id}/regenerate_signing_secret`        | `RotateWebhookSecret`      | Management            |

Rute yang tidak ada dalam tabel ini tidak tersedia di Claude Platform on AWS. Gateway secara default menolak rute apa pun yang tidak tercantum di sini.

<Note>
  Rute workspace dan kunci eksternal adalah satu-satunya rute Admin API yang tersedia di Claude Platform on AWS. Anda juga dapat membuat, memperbarui, atau mengarsipkan workspace di AWS Console atau, dengan peran Admin, di Claude Console. Kunci enkripsi juga dapat didaftarkan dan dilampirkan di Claude Console.
</Note>

## Kebijakan terkelola

AWS menyediakan lima kebijakan terkelola untuk Claude Platform on AWS. Semua kebijakan terkelola berlaku untuk `Resource: "*"`.

| Kebijakan                              | Memberikan                                                                                                                                                                              |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AnthropicFullAccess`                  | `aws-external-anthropic:*`                                                                                                                                                              |
| `AnthropicReadOnlyAccess`              | `Get*`, `List*`, `CallWithBearerToken`                                                                                                                                                  |
| `AnthropicInferenceAccess`             | `Get*`, `List*`, `CreateInference`, `CreateBatchInference`, `CancelBatchInference`, `DeleteBatchInference`, `CountTokens`, `CallWithBearerToken`                                        |
| `AnthropicLimitedAccess`               | Semua tindakan `AnthropicInferenceAccess`, ditambah semua tindakan Claude Managed Agents (agen, sesi, environment, vault, memory store, webhook, dan pekerjaan environment self-hosted) |
| `AnthropicSelfHostedEnvironmentAccess` | `GetEnvironment`, `ProcessEnvironmentWork`, `GetSession`, `UpdateSession`, `GetSkill`, `CallWithBearerToken`                                                                            |

`AnthropicInferenceAccess` adalah kebijakan terkelola paling sempit yang cukup untuk menjalankan inferensi. Kebijakan ini mencakup inferensi sinkron maupun batch dan, melalui wildcard `Get*` dan `List*`, memberikan akses baca ke setiap sumber daya API dalam namespace, termasuk sumber daya Claude Managed Agents (CMA) (agen, sesi, environment, vault, memory store, dan webhook). Ini mencakup pengunduhan konten file melalui `GetFile` (lihat catatan [File](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#files)), pengunduhan konten skill melalui `GetSkill` (lihat catatan [Skill](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#skills)), dan isi memori melalui `GetMemoryStore`. Rahasia kredensial vault dan rahasia penandatanganan webhook tidak diekspos: field tersebut bersifat hanya-tulis dan tidak pernah dikembalikan oleh `GetVault` atau `GetWebhook` (lihat [Autentikasi dengan vault](https://platform.claude.com/docs/id/managed-agents/vaults)). `AnthropicInferenceAccess` tidak memberikan pembuatan atau penghapusan file, manajemen skill, manajemen profil pengguna, mutasi workspace, manajemen kunci enkripsi, atau tindakan tulis Claude Managed Agents apa pun (create, update, archive, delete, process, atau rotate). Untuk mengecualikan pembacaan CMA, ganti `AnthropicInferenceAccess` dengan kebijakan kustom yang hanya menyebutkan tindakan non-CMA spesifik yang Anda perlukan.

<Note>
  `AnthropicReadOnlyAccess`, `AnthropicInferenceAccess`, dan `AnthropicLimitedAccess` semuanya membawa wildcard `Get*` dan `List*`, yang memberikan akses baca ke semua konten dalam workspace: byte file, konten skill, hasil batch, riwayat percakapan sesi, dan isi memori. Wildcard tersebut juga memberikan `GetKey` dan `ListKeys`, yang membaca konfigurasi kunci enkripsi terdaftar milik organisasi (ARN kunci dan metadata, tidak pernah materi kunci). Wildcard `List*` juga memberikan `ListComplianceActivities`, yang membaca [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) kepatuhan organisasi setelah Compliance API diaktifkan untuk organisasi (lihat [Kepatuhan](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#compliance)). Rahasia kredensial vault dan rahasia penandatanganan webhook tidak diekspos; field tersebut bersifat hanya-tulis dan tidak pernah dikembalikan oleh `GetVault` atau `GetWebhook`. Jika principal Anda tidak seharusnya membaca konten yang ada, gunakan kebijakan kustom yang hanya menyebutkan tindakan yang Anda perlukan.
</Note>

`AnthropicLimitedAccess` mencakup semua tindakan Claude Managed Agents selain tindakan inferensi.

`AnthropicSelfHostedEnvironmentAccess` adalah kebijakan terkelola paling sempit yang cukup untuk menjalankan worker [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes). Lampirkan ke principal yang digunakan worker environment Anda untuk autentikasi.

`AssumeConsole` tidak termasuk dalam `AnthropicReadOnlyAccess`, `AnthropicInferenceAccess`, `AnthropicLimitedAccess`, atau `AnthropicSelfHostedEnvironmentAccess`. Principal yang memerlukan akses Claude Console membutuhkan `AnthropicFullAccess` atau kebijakan kustom yang memberikan `aws-external-anthropic:AssumeConsole`. Lihat [Akses konsol](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#console-access).

<Note>
  `CreateInference` dan `CreateBatchInference` adalah tindakan terpisah. Menolak salah satunya tidak memblokir yang lain. Jika Anda bermaksud mencegah semua pemanggilan model, tolak keduanya.
</Note>

## Contoh kebijakan

### Inferensi sinkron pada satu workspace

Memberikan izin minimal untuk principal IAM yang menjalankan inferensi terhadap satu workspace produksi:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "aws-external-anthropic:CreateInference",
        "aws-external-anthropic:CountTokens",
        "aws-external-anthropic:GetModel",
        "aws-external-anthropic:ListModels",
        "aws-external-anthropic:GetWorkspace"
      ],
      "Resource": "arn:aws:aws-external-anthropic:us-west-2:123456789012:workspace/wrkspc_01AbCdEf23GhIj"
    }
  ]
}
```

<Note>
  `ListWorkspaces` bercakupan akun (lihat [Otomatisasi provisioning](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#provisioning-automation)). Jika akun layanan Anda perlu mengenumerasi workspace, tambahkan pernyataan `Allow` terpisah untuk `ListWorkspaces` dengan `Resource: "*"`.

  Kebijakan ini mengasumsikan autentikasi AWS SigV4. Jika principal melakukan autentikasi dengan kunci API, tambahkan pernyataan `Allow` terpisah untuk `aws-external-anthropic:CallWithBearerToken` dengan `Resource: "*"`. `CallWithBearerToken` adalah tindakan tanpa rute yang tidak terikat ke ARN workspace. Lihat [Isolasi workspace per pelanggan](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#per-customer-workspace-isolation) untuk pola dua pernyataan.
</Note>

### Isolasi workspace per pelanggan

Membatasi sebuah role ke satu workspace:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "aws-external-anthropic:*",
      "Resource": "arn:aws:aws-external-anthropic:us-west-2:123456789012:workspace/wrkspc_01AbCdEf23GhIj"
    },
    {
      "Effect": "Allow",
      "Action": [
        "aws-external-anthropic:CallWithBearerToken",
        "aws-external-anthropic:AssumeConsole"
      ],
      "Resource": "*"
    }
  ]
}
```

<Note>
  Wildcard `aws-external-anthropic:*` dalam pernyataan pertama mencakup tindakan bercakupan akun (`CreateWorkspace`, `ListWorkspaces`, `ListComplianceActivities`, dan tindakan kunci eksternal) yang secara diam-diam disaring oleh batasan ARN workspace. Ini konsisten dengan maksud "isolasi" (role tidak dapat membuat workspace, mengenumerasi workspace, mengelola registrasi kunci enkripsi, atau membaca Activity Feed kepatuhan; role tetap dapat melampirkan kunci yang sudah terdaftar ke workspace-nya sendiri melalui `UpdateWorkspace`), tetapi kebijakan tersebut berisi izin yang tidak berpengaruh. Lihat [Otomatisasi provisioning](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#provisioning-automation) untuk pola bercakupan akun.

  `CallWithBearerToken` dan `AssumeConsole` adalah tindakan tanpa rute yang tidak terikat ke ARN workspace. Pernyataan kedua memberikannya pada `Resource: "*"` sehingga role dapat melakukan autentikasi dengan kunci API dan membuka Claude Console. Hilangkan pernyataan ini jika role hanya menggunakan SigV4 dan tidak memerlukan akses Claude Console.
</Note>

### Penguncian fitur untuk workspace yang sensitif terhadap ZDR

Memblokir pemrosesan batch dan unggahan file pada workspace tertentu sambil tetap menyediakan inferensi sinkron. Berguna ketika workspace menangani data [Zero Data Retention (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention) yang tidak boleh tersimpan di sisi server. Lampirkan kebijakan ini bersama kebijakan Allow seperti `AnthropicInferenceAccess` atau [contoh satu workspace](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#synchronous-inference-on-a-single-workspace); jika berdiri sendiri, kebijakan yang hanya berisi Deny tidak memberikan izin apa pun:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": [
        "aws-external-anthropic:CreateBatchInference",
        "aws-external-anthropic:CreateFile"
      ],
      "Resource": "arn:aws:aws-external-anthropic:us-west-2:123456789012:workspace/wrkspc_01AbCdEf23GhIj"
    }
  ]
}
```

<Note>
  Penolakan ini hanya memblokir pembuatan. Tindakan file dan batch lainnya tidak ditolak kecuali Anda mencantumkannya juga. Untuk penguncian lengkap di mana workspace tidak boleh pernah menyimpan file atau batch, tolak juga `aws-external-anthropic:GetFile`, `aws-external-anthropic:ListFiles`, `aws-external-anthropic:DeleteFile`, `aws-external-anthropic:GetBatchInference`, `aws-external-anthropic:ListBatchInferences`, `aws-external-anthropic:CancelBatchInference`, dan `aws-external-anthropic:DeleteBatchInference`.
</Note>

### Otomatisasi provisioning

<Note>
  Selain Admin API, Anda dapat membuat, memperbarui, atau mengarsipkan workspace di AWS Console atau, dengan peran Admin, di Claude Console.
</Note>

Memberikan peran CI/CD tindakan yang diperlukan untuk membuat dan mengelola workspace, tanpa izin inferensi apa pun:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "aws-external-anthropic:CreateWorkspace",
        "aws-external-anthropic:GetWorkspace",
        "aws-external-anthropic:ListWorkspaces",
        "aws-external-anthropic:UpdateWorkspace",
        "aws-external-anthropic:ArchiveWorkspace"
      ],
      "Resource": "*"
    }
  ]
}
```

`CreateWorkspace` dan `ListWorkspaces` adalah operasi dengan cakupan akun. Menentukan ARN workspace pada tindakan ini tidak berpengaruh apa pun; gunakan `Resource: "*"`.

## Lihat juga

* [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) untuk penyiapan, autentikasi, dan ikhtisar platform
* [Panduan Pengguna AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) untuk sintaks kebijakan IAM dan logika evaluasi
* [Panduan Pengguna AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/) untuk konfigurasi pencatatan audit
