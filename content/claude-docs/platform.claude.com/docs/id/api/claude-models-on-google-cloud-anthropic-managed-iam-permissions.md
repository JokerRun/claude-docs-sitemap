---
source: platform
url: https://platform.claude.com/docs/id/api/claude-models-on-google-cloud-anthropic-managed-iam-permissions
fetched_at: 2026-10-30T02:15:26.914079Z
sha256: 9242d841b811f3f368f61643ce88bef60cafb18f1fce39dd5901ef2fbc9ddedd
---

---
title: Izin IAM untuk Claude Models on Google Cloud (Anthropic managed)
url: https://platform.claude.com/docs/id/api/claude-models-on-google-cloud-anthropic-managed-iam-permissions
description: Cari izin IAM Google Cloud, peran bawaan, dan jenis log audit untuk Claude Models on Google Cloud (Anthropic managed).
---

Claude Models on Google Cloud (Anthropic managed) menggunakan IAM Google Cloud untuk kontrol akses. Setiap rute API memerlukan satu izin dari layanan `claude.googleapis.com`. Jika pemanggil tidak memiliki izin tersebut, Google Cloud mengembalikan error HTTP 403. Tiga peran bawaan menggabungkan izin-izin tersebut. Untuk penyiapan dan autentikasi, lihat [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed).

## Detail layanan

Tabel berikut menjelaskan layanan Google Cloud untuk Claude Models on Google Cloud (Anthropic managed).

| Atribut                   | Nilai                                                                                                                                                                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Layanan**               | `claude.googleapis.com`                                                                                                                                                                                                            |
| **Tempat izin diperiksa** | Sebuah workspace atau organisasi Anthropic                                                                                                                                                                                         |
| **Jenis log audit**       | Data Access, Admin Activity<br />Untuk mengaktifkan log Data Access, lihat [Pemantauan dan logging](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#monitoring-and-logging). |

Berikan peran pada proyek Google Cloud. Untuk mengetahui bagaimana proyek, organisasi, dan workspace saling berhubungan, lihat [Workspace](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#workspaces).

Izin di halaman ini ditulis dalam bentuk singkat `resource.verb`, seperti `messages.create`.

## Peran bawaan

Tabel berikut mencantumkan peran bawaan (“predefined roles”) untuk Claude Models on Google Cloud (Anthropic managed).

| Peran                 | Nama tampilan | Izin                                                                                                                                                                                     |
| --------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `roles/claude.viewer` | Claude Viewer | Setiap izin `get` dan `list` pada sumber daya workspace.                                                                                                                                 |
| `roles/claude.user`   | Claude User   | Semua yang ada di `roles/claude.viewer`, ditambah setiap izin lain pada sumber daya workspace.<br />Misalnya, `messages.create`, `messages.countTokens`, dan `environments.processWork`. |
| `roles/claude.admin`  | Claude Admin  | Semua yang ada di `roles/claude.user`, ditambah izin yang diperiksa pada organisasi Anthropic Anda.<br />Misalnya, `externalKeys.*` dan `usageAnalytics.list`.                           |

Dalam tabel-tabel berikut, **Admin**, **User**, dan **Viewer** mewakili ketiga peran ini.

## Izin

Tabel-tabel berikut mencantumkan 69 izin di 113 rute.

Izin `get` dan `list` adalah izin yang bersifat hanya-baca.

Kecuali suatu bagian menyatakan lain, jenis log audit setiap rute adalah Data Access.

`roles/claude.viewer` tidak dapat mengirim pesan atau menghitung token. Mengirim pesan memerlukan `messages.create`. Menghitung token memerlukan `messages.countTokens`.

Beberapa rute dalam tabel-tabel berikut mungkin tidak tersedia untuk organisasi Anda. Untuk memeriksa fitur mana yang tersedia, lihat [Dukungan fitur](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#feature-support).

### Messages

| Izin                   | Peran       | Rute yang diotorisasi            |
| ---------------------- | ----------- | -------------------------------- |
| `messages.create`      | Admin, User | `POST /v1/messages`              |
| `messages.countTokens` | Admin, User | `POST /v1/messages/count_tokens` |

### Message batches

| Izin                    | Peran               | Rute yang diotorisasi                                                                                    |
| ----------------------- | ------------------- | -------------------------------------------------------------------------------------------------------- |
| `messageBatches.create` | Admin, User         | `POST /v1/messages/batches`                                                                              |
| `messageBatches.get`    | Admin, User, Viewer | `GET /v1/messages/batches/{message_batch_id}`<br />`GET /v1/messages/batches/{message_batch_id}/results` |
| `messageBatches.list`   | Admin, User, Viewer | `GET /v1/messages/batches`                                                                               |
| `messageBatches.delete` | Admin, User         | `DELETE /v1/messages/batches/{message_batch_id}`                                                         |
| `messageBatches.cancel` | Admin, User         | `POST /v1/messages/batches/{message_batch_id}/cancel`                                                    |

`roles/claude.viewer` dapat membaca hasil batch. `messageBatches.get` mengotorisasi pembacaan metadata batch sekaligus pengunduhan hasilnya.

### Models

| Izin          | Peran               | Rute yang diotorisasi       |
| ------------- | ------------------- | --------------------------- |
| `models.get`  | Admin, User, Viewer | `GET /v1/models/{model_id}` |
| `models.list` | Admin, User, Viewer | `GET /v1/models`            |

### Files

| Izin           | Peran               | Rute yang diotorisasi                                            |
| -------------- | ------------------- | ---------------------------------------------------------------- |
| `files.create` | Admin, User         | `POST /v1/files`                                                 |
| `files.get`    | Admin, User, Viewer | `GET /v1/files/{file_id}`<br />`GET /v1/files/{file_id}/content` |
| `files.list`   | Admin, User, Viewer | `GET /v1/files`                                                  |
| `files.delete` | Admin, User         | `DELETE /v1/files/{file_id}`                                     |

`roles/claude.viewer` dapat mengunduh file. `files.get` mengotorisasi pembacaan metadata file sekaligus pengunduhan kontennya.

### Skills

| Izin            | Peran               | Rute yang diotorisasi                                                                                                                                                                 |
| --------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skills.create` | Admin, User         | `POST /v1/skills`                                                                                                                                                                     |
| `skills.get`    | Admin, User, Viewer | `GET /v1/skills/{skill_id}`<br />`GET /v1/skills/{skill_id}/versions`<br />`GET /v1/skills/{skill_id}/versions/{version}`<br />`GET /v1/skills/{skill_id}/versions/{version}/content` |
| `skills.list`   | Admin, User, Viewer | `GET /v1/skills`                                                                                                                                                                      |
| `skills.update` | Admin, User         | `POST /v1/skills/{skill_id}/versions`<br />`DELETE /v1/skills/{skill_id}/versions/{version}`                                                                                          |
| `skills.delete` | Admin, User         | `DELETE /v1/skills/{skill_id}`                                                                                                                                                        |

Membuat atau menghapus versi skill memerlukan `skills.update`, bukan `skills.create` atau `skills.delete`.

### Agents

| Izin             | Peran               | Rute yang diotorisasi                                                 |
| ---------------- | ------------------- | --------------------------------------------------------------------- |
| `agents.create`  | Admin, User         | `POST /v1/agents`                                                     |
| `agents.get`     | Admin, User, Viewer | `GET /v1/agents/{agent_id}`<br />`GET /v1/agents/{agent_id}/versions` |
| `agents.list`    | Admin, User, Viewer | `GET /v1/agents`                                                      |
| `agents.update`  | Admin, User         | `POST /v1/agents/{agent_id}`                                          |
| `agents.archive` | Admin, User         | `POST /v1/agents/{agent_id}/archive`                                  |

Anda dapat mengarsipkan agent tetapi tidak dapat menghapusnya.

### Sessions

| Izin               | Peran               | Rute yang diotorisasi                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------ | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sessions.create`  | Admin, User         | `POST /v1/sessions`                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `sessions.get`     | Admin, User, Viewer | `GET /v1/sessions/{session_id}`<br />`GET /v1/sessions/{session_id}/events`<br />`GET /v1/sessions/{session_id}/events/stream`<br />`GET /v1/sessions/{session_id}/resources`<br />`GET /v1/sessions/{session_id}/resources/{resource_id}`<br />`GET /v1/sessions/{session_id}/threads`<br />`GET /v1/sessions/{session_id}/threads/{thread_id}`<br />`GET /v1/sessions/{session_id}/threads/{thread_id}/events`<br />`GET /v1/sessions/{session_id}/threads/{thread_id}/stream` |
| `sessions.list`    | Admin, User, Viewer | `GET /v1/sessions`                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `sessions.update`  | Admin, User         | `POST /v1/sessions/{session_id}`<br />`POST /v1/sessions/{session_id}/events`<br />`POST /v1/sessions/{session_id}/resources`<br />`POST /v1/sessions/{session_id}/resources/{resource_id}`<br />`DELETE /v1/sessions/{session_id}/resources/{resource_id}`                                                                                                                                                                                                                      |
| `sessions.archive` | Admin, User         | `POST /v1/sessions/{session_id}/archive`<br />`POST /v1/sessions/{session_id}/threads/{thread_id}/archive`                                                                                                                                                                                                                                                                                                                                                                       |
| `sessions.delete`  | Admin, User         | `DELETE /v1/sessions/{session_id}`                                                                                                                                                                                                                                                                                                                                                                                                                                               |

`sessions.get` mengotorisasi pembacaan sesi, riwayat event dan stream event-nya, sumber dayanya, serta thread-nya. Akibatnya, `roles/claude.viewer` dapat membaca riwayat event lengkap dari setiap sesi.

Operasi sesi lainnya memerlukan izin berikut:

* Mengirim event: `sessions.update`
* Menambahkan, mengubah, atau menghapus sumber daya sesi: `sessions.update`
* Mengarsipkan thread: `sessions.archive`

### Environments

| Izin                       | Peran               | Rute yang diotorisasi                                                                                                                                                                                                                                                                                                    |
| -------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `environments.create`      | Admin, User         | `POST /v1/environments`                                                                                                                                                                                                                                                                                                  |
| `environments.get`         | Admin, User, Viewer | `GET /v1/environments/{environment_id}`<br />`GET /v1/environments/{environment_id}/work`<br />`GET /v1/environments/{environment_id}/work/stats`<br />`GET /v1/environments/{environment_id}/work/{work_id}`                                                                                                            |
| `environments.list`        | Admin, User, Viewer | `GET /v1/environments`                                                                                                                                                                                                                                                                                                   |
| `environments.update`      | Admin, User         | `POST /v1/environments/{environment_id}`                                                                                                                                                                                                                                                                                 |
| `environments.archive`     | Admin, User         | `POST /v1/environments/{environment_id}/archive`                                                                                                                                                                                                                                                                         |
| `environments.delete`      | Admin, User         | `DELETE /v1/environments/{environment_id}`                                                                                                                                                                                                                                                                               |
| `environments.processWork` | Admin, User         | `GET /v1/environments/{environment_id}/work/poll`<br />`POST /v1/environments/{environment_id}/work/{work_id}`<br />`POST /v1/environments/{environment_id}/work/{work_id}/ack`<br />`POST /v1/environments/{environment_id}/work/{work_id}/heartbeat`<br />`POST /v1/environments/{environment_id}/work/{work_id}/stop` |

`roles/claude.user` dan `roles/claude.admin` mencakup setiap izin yang diperlukan oleh worker [sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes). `environments.processWork` mengotorisasi tindakan worker berikut:

* Melakukan polling untuk pekerjaan
* Mengonfirmasi item pekerjaan
* Mengirim heartbeat untuk item pekerjaan
* Menghentikan item pekerjaan
* Memperbarui item pekerjaan

Izin ini terpisah dari `environments.update`. Membaca antrean pekerjaan dan statistiknya hanya memerlukan `environments.get`.

Selain `environments.processWork`, worker memerlukan izin lain untuk menjalankan sesi, seperti `sessions.get` untuk membaca sesi dan event-nya, `sessions.update` untuk mengirim hasil alat, dan `skills.get` untuk mengunduh skill milik agen.

### Vaults

Google Cloud mencatat rute-rute ini dalam log audit Admin Activity, kecuali rute untuk `vaults.verify`, yang jenis log auditnya adalah Data Access.

| Izin             | Peran               | Rute yang diotorisasi                                                                                                                                                                                    |
| ---------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `vaults.create`  | Admin, User         | `POST /v1/vaults`                                                                                                                                                                                        |
| `vaults.get`     | Admin, User, Viewer | `GET /v1/vaults/{vault_id}`<br />`GET /v1/vaults/{vault_id}/credentials`<br />`GET /v1/vaults/{vault_id}/credentials/{credential_id}`                                                                    |
| `vaults.list`    | Admin, User, Viewer | `GET /v1/vaults`                                                                                                                                                                                         |
| `vaults.update`  | Admin, User         | `POST /v1/vaults/{vault_id}`<br />`POST /v1/vaults/{vault_id}/credentials`<br />`POST /v1/vaults/{vault_id}/credentials/{credential_id}`<br />`DELETE /v1/vaults/{vault_id}/credentials/{credential_id}` |
| `vaults.archive` | Admin, User         | `POST /v1/vaults/{vault_id}/archive`<br />`POST /v1/vaults/{vault_id}/credentials/{credential_id}/archive`                                                                                               |
| `vaults.delete`  | Admin, User         | `DELETE /v1/vaults/{vault_id}`                                                                                                                                                                           |
| `vaults.verify`  | Admin, User         | `POST /v1/vaults/{vault_id}/credentials/{credential_id}/mcp_oauth_validate`                                                                                                                              |

Operasi kredensial memerlukan izin berikut:

* Membuat, mengubah, atau menghapus kredensial: `vaults.update`
* Mengarsipkan kredensial: `vaults.archive`
* Membaca kredensial: `vaults.get`
* Memeriksa kredensial MCP OAuth yang tersimpan: `vaults.verify`

Dengan `vaults.get`, `roles/claude.viewer` dapat mencantumkan kredensial sebuah vault. Claude Models on Google Cloud (Anthropic managed) tidak pernah mengembalikan field rahasia dari sebuah kredensial. Untuk mempelajari lebih lanjut, lihat [Autentikasi dengan vault](https://platform.claude.com/docs/id/managed-agents/vaults).

### Memory stores

| Izin                   | Peran               | Rute yang diotorisasi                                                                                                                                                                                                                                                                                                                      |
| ---------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `memoryStores.create`  | Admin, User         | `POST /v1/memory_stores`                                                                                                                                                                                                                                                                                                                   |
| `memoryStores.get`     | Admin, User, Viewer | `GET /v1/memory_stores/{memory_store_id}`<br />`GET /v1/memory_stores/{memory_store_id}/memories`<br />`GET /v1/memory_stores/{memory_store_id}/memories/{memory_id}`<br />`GET /v1/memory_stores/{memory_store_id}/memory_versions`<br />`GET /v1/memory_stores/{memory_store_id}/memory_versions/{memory_version_id}`                    |
| `memoryStores.list`    | Admin, User, Viewer | `GET /v1/memory_stores`                                                                                                                                                                                                                                                                                                                    |
| `memoryStores.update`  | Admin, User         | `POST /v1/memory_stores/{memory_store_id}`<br />`POST /v1/memory_stores/{memory_store_id}/memories`<br />`POST /v1/memory_stores/{memory_store_id}/memories/{memory_id}`<br />`DELETE /v1/memory_stores/{memory_store_id}/memories/{memory_id}`<br />`POST /v1/memory_stores/{memory_store_id}/memory_versions/{memory_version_id}/redact` |
| `memoryStores.archive` | Admin, User         | `POST /v1/memory_stores/{memory_store_id}/archive`                                                                                                                                                                                                                                                                                         |
| `memoryStores.delete`  | Admin, User         | `DELETE /v1/memory_stores/{memory_store_id}`                                                                                                                                                                                                                                                                                               |

Operasi memory store memerlukan izin berikut:

* Membaca store, memori-memorinya, atau riwayat versinya: `memoryStores.get`
* Membuat, mengubah, atau menghapus memori: `memoryStores.update`
* Meredaksi versi memori: `memoryStores.update`

### Deployments

| Izin                  | Peran               | Rute yang diotorisasi                                                                                                   |
| --------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `deployments.create`  | Admin, User         | `POST /v1/deployments`                                                                                                  |
| `deployments.get`     | Admin, User, Viewer | `GET /v1/deployment_runs`<br />`GET /v1/deployment_runs/{deployment_run_id}`<br />`GET /v1/deployments/{deployment_id}` |
| `deployments.list`    | Admin, User, Viewer | `GET /v1/deployments`                                                                                                   |
| `deployments.update`  | Admin, User         | `POST /v1/deployments/{deployment_id}`                                                                                  |
| `deployments.archive` | Admin, User         | `POST /v1/deployments/{deployment_id}/archive`                                                                          |
| `deployments.run`     | Admin, User         | `POST /v1/deployments/{deployment_id}/run`                                                                              |
| `deployments.pause`   | Admin, User         | `POST /v1/deployments/{deployment_id}/pause`                                                                            |
| `deployments.unpause` | Admin, User         | `POST /v1/deployments/{deployment_id}/unpause`                                                                          |

Membaca deployment run memerlukan `deployments.get`.

### Dreams

| Izin             | Peran               | Rute yang diotorisasi                |
| ---------------- | ------------------- | ------------------------------------ |
| `dreams.create`  | Admin, User         | `POST /v1/dreams`                    |
| `dreams.get`     | Admin, User, Viewer | `GET /v1/dreams/{dream_id}`          |
| `dreams.list`    | Admin, User, Viewer | `GET /v1/dreams`                     |
| `dreams.archive` | Admin, User         | `POST /v1/dreams/{dream_id}/archive` |
| `dreams.cancel`  | Admin, User         | `POST /v1/dreams/{dream_id}/cancel`  |

Dreams adalah fitur pratinjau riset. Untuk meminta akses, lihat [Dreams](https://platform.claude.com/docs/id/managed-agents/dreams).

### Kunci enkripsi

Google Cloud mencatat rute-rute ini dalam log audit Admin Activity.

| Izin                  | Peran | Rute yang diotorisasi                                      |
| --------------------- | ----- | ---------------------------------------------------------- |
| `externalKeys.create` | Admin | `POST /v1/organizations/external_keys`                     |
| `externalKeys.get`    | Admin | `GET /v1/organizations/external_keys/{external_key_id}`    |
| `externalKeys.list`   | Admin | `GET /v1/organizations/external_keys`                      |
| `externalKeys.update` | Admin | `POST /v1/organizations/external_keys/{external_key_id}`   |
| `externalKeys.delete` | Admin | `DELETE /v1/organizations/external_keys/{external_key_id}` |

Izin-izin ini mengelola pendaftaran kunci enkripsi organisasi Anda. Dari ketiga peran bawaan, hanya `roles/claude.admin` yang menyertakannya.

### Laporan penggunaan

| Izin                  | Peran | Rute yang diotorisasi                                                                      |
| --------------------- | ----- | ------------------------------------------------------------------------------------------ |
| `usageAnalytics.list` | Admin | `GET /v1/organizations/usage_report/messages`<br />`GET /v1/organizations/analytics/usage` |
| `costAnalytics.list`  | Admin | `GET /v1/organizations/analytics/cost`                                                     |

Dari ketiga peran bawaan, hanya `roles/claude.admin` yang menyertakan `usageAnalytics.list` dan `costAnalytics.list`.

## Lihat juga

* [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed)
* [Peran IAM](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles)
* [Pemantauan dan logging](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#monitoring-and-logging)
