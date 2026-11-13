---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/inference-provider
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 52919688f0967ee17e4e08c7efcbe14994f5f80f9276d1ed416834e60864021b
---

---
title: Penyedia inferensi
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/inference-provider
description: Kirim panggilan model dari server Claude Managed Agents yang Anda hosting sendiri ke Amazon Bedrock, Claude Models on Google Cloud (Google managed), Microsoft Foundry, atau model gateway yang Anda jalankan, alih-alih ke Claude API.
---

<Note>
  Untuk meminta akses ke Claude Managed Agents yang di-host sendiri, hubungi tim akun Anthropic Anda.
</Note>

Secara default, server Anda mengirim panggilan model ke Claude API. Halaman ini menunjukkan cara mengirimnya ke penyedia cloud, atau ke model gateway yang Anda jalankan. Untuk mengubah penyedia:

1. Letakkan contoh dari bagian penyedia Anda di halaman ini di [file pengaturan](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#where-settings-go) server.
2. Berikan kredensial penyedia kepada server, seperti yang ditunjukkan di bagian yang sama.
3. Mulai ulang server, seperti yang ditunjukkan di [Tempat pengaturan disimpan](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#where-settings-go). Di Docker Compose, jika langkah 2 mengubah `.env` atau `docker-compose.yml`, jalankan `docker compose up -d` sebagai gantinya, karena memulai ulang tidak membaca ulang file tersebut.
4. [Periksa penyedia](https://platform.claude.com/docs/id/managed-agents/self-hosted/inference-provider#check-the-provider).

Pengaturan `inference.provider` menerima nilai-nilai ini:

| `inference.provider`  | Panggilan model dikirim ke                     | Server melakukan autentikasi dengan         |
| --------------------- | ---------------------------------------------- | ------------------------------------------- |
| `anthropic` (default) | Claude API                                     | `ANTHROPIC_API_KEY`                         |
| `bedrock`             | Amazon Bedrock                                 | Kredensial AWS Anda                         |
| `vertex`              | Claude Models on Google Cloud (Google managed) | Google Application Default Credentials      |
| `foundry`             | Microsoft Foundry                              | Kunci API Foundry, atau Microsoft Entra ID  |
| `gateway`             | Model gateway yang Anda jalankan               | Kunci atau token yang diterima gateway Anda |

Untuk setiap nilai kecuali `anthropic`, server tidak memerlukan kunci API Claude. Server mengabaikan `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, dan `ANTHROPIC_BASE_URL`. Satu-satunya pengecualian adalah [model gateway](https://platform.claude.com/docs/id/managed-agents/self-hosted/inference-provider#model-gateway) yang kuncinya Anda minta untuk dibaca server dari salah satu variabel tersebut.

Agen menamai model berdasarkan ID Claude API-nya, seperti `claude-opus-5-5`. Server menerjemahkan ID tersebut, sehingga definisi agen tetap berfungsi tanpa perubahan di bawah penyedia mana pun yang menyediakan model tersebut.

Beberapa alat dan pengaturan agen bergantung pada penyedia. Lihat [Perbedaan yang bergantung pada penyedia inferensi Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/differences#differences-that-depend-on-your-inference-provider).

## Memberikan kredensial cloud kepada server

Cara kredensial penyedia cloud sampai ke server bergantung pada instalasi Anda:

* **Docker Compose:** [Teruskan setiap variabel dan file ke server](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#pass-a-credential-to-the-compose-stack).
* **Kubernetes:** Chart server tidak meneruskan variabel AWS, Google Cloud, atau Azure apa pun, jadi gunakan workload identity milik cloud Anda. Buat service account dengan anotasi workload identity milik cloud Anda, lalu atur `server.serviceAccountName` ke nama service account tersebut. `values.yaml` milik chart menyebutkan anotasi tersebut. Di Azure Kubernetes Service, atur juga `server.azureWorkloadIdentity: true`.

## Amazon Bedrock

```yaml
inference:
  provider: bedrock
  region: us-east-1
  #model_id_prefix: global.anthropic.
  #model_id_overrides:
  #  claude-opus-5-5: us.anthropic.claude-opus-5-5
```

Server menandatangani panggilannya dengan kredensial apa pun yang ditemukan oleh rantai kredensial default AWS SDK di host. Kredensial tersebut dapat berupa task role atau pod identity. Di workstation, kredensial tersebut dapat berupa `AWS_PROFILE` atau `AWS_ACCESS_KEY_ID`.

Aktifkan model yang Anda gunakan di akun. Identitas AWS yang digunakan server untuk menandatangani memerlukan izin berikut:

* `bedrock:InvokeModel` dan `bedrock:InvokeModelWithResponseStream` pada model dan inference profile yang Anda gunakan.
* `bedrock:ListFoundationModels` dan `bedrock:ListInferenceProfiles` pada resource `*`. Server membaca daftar model Amazon Bedrock, sehingga agen dapat menggunakan model yang lebih baru daripada rilis server Anda. Untuk melewati ini, atur `inference.list_models: false`.

Secara default, server menambahkan `us.anthropic.` di depan setiap ID model, yang menyebutkan sebuah “cross-region inference profile” (profil inferensi lintas wilayah). Untuk menggunakan keluarga profil lain, hapus komentar pada `model_id_prefix`.

## Claude Models on Google Cloud (Google managed)

```yaml
inference:
  provider: vertex
  region: us-east5
  project_id: my-project
  #model_id_overrides:
  #  claude-haiku-4-5: claude-haiku-4-5@20251001
```

`region` wajib diisi. Nilainya adalah lokasi Google Cloud’s Agent Platform yang menawarkan model yang Anda gunakan, atau `global`. `project_id` adalah proyek tempat panggilan dilakukan dan ditagihkan.

Server menggunakan Google Application Default Credentials: file yang disebutkan oleh `GOOGLE_APPLICATION_CREDENTIALS`, atau service account yang dilampirkan oleh Compute Engine, Cloud Run, atau GKE. Identitas tersebut memerlukan role `roles/aiplatform.user` pada proyek. Proyek memerlukan API `aiplatform.googleapis.com` dan model Claude yang Anda gunakan dalam keadaan aktif.

## Microsoft Foundry

```yaml
inference:
  provider: foundry
  foundry:
    resource: my-resource
  #model_id_overrides:
  #  claude-opus-5-5: team-a-opus
```

`resource` adalah nama resource Foundry Anda, bagian pertama dari hostname-nya: `<resource>.services.ai.azure.com`.

Kredensial berasal dari environment server:

* **Kunci API Foundry:** Atur `ANTHROPIC_FOUNDRY_API_KEY`. Di stack Compose, [teruskan variabel tersebut ke server](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#pass-a-credential-to-the-compose-stack). Di Kubernetes, letakkan di Secret `cma-server-upstream`. Dengan `earlierNames: true` di file values server Anda, Secret tersebut memiliki nama lain. Temukan nama tersebut di [Kubernetes: nama objek Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#object-names).
* **Microsoft Entra ID:** Biarkan `ANTHROPIC_FOUNDRY_API_KEY` tidak diatur. Server kemudian mendapatkan token untuk service principal, workload identity di Azure Kubernetes Service, atau managed identity. Identitas tersebut memerlukan role Azure pada resource Foundry yang mengizinkan panggilan ke deployment modelnya. Untuk service principal, atur `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, dan `AZURE_CLIENT_SECRET`.

Permintaan ke Foundry menyebutkan sebuah deployment, dan server mengirim ID model sebagai nama deployment. Jika sebuah deployment memiliki nama lain, petakan dengan [`model_id_overrides`](https://platform.claude.com/docs/id/managed-agents/self-hosted/inference-provider#map-a-model-id-that-differs).

## Memetakan ID model yang berbeda

Akun cloud Anda dapat memiliki model dengan ID yang berbeda dari ID yang dikirim server. Dalam hal ini, hapus komentar pada baris `model_id_overrides` di contoh penyedia tersebut, lalu petakan ID Claude API ke ID akun Anda. Kedua ID harus menyebutkan model yang sama, karena server membangun setiap permintaan untuk model yang disebutkan agen.

## Model gateway

Pertama, periksa permintaan mana yang diterima oleh gateway Anda:

* **Permintaan yang sama dengan Claude API, dengan satu kredensial berumur panjang:** Pertahankan penyedia default. Atur `ANTHROPIC_BASE_URL` ke alamat gateway, dan atur `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN` ke kredensial yang diharapkan gateway.
* **Permintaan yang sama dengan Claude API, tetapi dengan token berumur pendek, kredensial di header lain, atau ID modelnya sendiri:** Atur `inference.provider: gateway` dengan `format: anthropic-messages`.
* **Format InvokeModel milik Amazon Bedrock:** Atur `inference.provider: gateway` dengan `format: bedrock-invoke`.
* **Format `rawPredict` milik Claude Models on Google Cloud (Google managed):** Atur `inference.provider: gateway` dengan `format: vertex-raw-predict`.

Contoh ini mengatur `inference.provider: gateway` dengan `format: bedrock-invoke`, untuk gateway yang menerima satu kunci berumur panjang. Letakkan kunci di variabel environment dan sebutkan nama variabelnya, jangan pernah nilainya:

```yaml
inference:
  provider: gateway
  gateway:
    url: "https://llm-gateway.example.com/v1/model/{model}/invoke"
    format: bedrock-invoke
    # Quote every model_map value.
    model_map:
      claude-opus-5-5: "us.anthropic.claude-opus-5-5"
      claude-sonnet-5: "us.anthropic.claude-sonnet-5"
  credentials:
    supplier: env
    env: { var: LLM_GATEWAY_KEY }
    send_as: { header: x-api-key }
```

* `url` adalah rute model gateway. `{model}` menandai tempat ID model dimasukkan. URL harus `https://` dan berakhiran `/invoke`.

* `model_map` memetakan setiap ID model yang dapat disebutkan agen ke ID yang diharapkan gateway. Server menolak model yang tidak memiliki entri.

* `send_as` menyebutkan header yang membawa kunci. Tanpanya, server mengirim `Authorization: Bearer <key>`.

* Di stack Compose, [teruskan variabel tersebut](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#pass-a-credential-to-the-compose-stack) ke server.

* Di Kubernetes, chart server tidak dapat meneruskan variabel milik Anda sendiri. Chart tersebut memang meneruskan `ANTHROPIC_AUTH_TOKEN`, yang dibacanya dari Secret `cma-server-upstream`, jadi gunakan nama tersebut:

  1. Atur `env: { var: ANTHROPIC_AUTH_TOKEN }`.
  2. Letakkan kunci gateway di Secret `cma-server-upstream`, dengan nama `ANTHROPIC_AUTH_TOKEN`. Dengan `earlierNames: true` di file values server Anda, Secret tersebut memiliki nama lain. Temukan nama tersebut di [Kubernetes: nama objek Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#object-names).

Untuk `format: anthropic-messages`, ganti blok `gateway` dengan blok ini:

```yaml
inference:
  gateway:
    url: "https://llm-gateway.example.com/v1/messages"
    format: anthropic-messages
    # Quote every model_map value.
    model_map:
      claude-opus-5-5: "corp-claude-opus"
      claude-sonnet-5: "corp-claude-sonnet"
```

Di sini, `url` adalah URL lengkap dari rute Messages gateway, tanpa `{model}`.

Untuk `format: vertex-raw-predict`, ganti blok `gateway` dengan blok ini:

```yaml
inference:
  gateway:
    url: "https://llm-gateway.example.com/v1/projects/my-project/locations/global/publishers/anthropic/models/{model}:rawPredict"
    format: vertex-raw-predict
    # Quote every model_map value.
    model_map:
      claude-opus-5-5: "claude-opus-5-5"
      claude-sonnet-5: "claude-sonnet-5"
```

Di sini, `url` adalah rute `rawPredict` milik gateway, dan URL tersebut harus berakhiran `/{model}:rawPredict`. Nilai `model_map` tidak boleh berisi titik dua. Blok `credentials` tetap seperti apa adanya. Server mengirim kredensial milik gateway Anda sendiri dan tidak mendapatkan kredensial Google.

[Referensi konfigurasi](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#model-gateway) mencantumkan pengaturan gateway lainnya, seperti `streaming`, dan pengaturan `inference.headers`.

### Token berumur pendek

Jika gateway Anda menerima token berumur pendek, ganti blok `credentials` dengan blok ini:

```yaml
inference:
  credentials:
    supplier: oauth_exchange
    assertion:
      url: "https://app.example.com/assertion"
      auth: { type: mtls, cert_file: /etc/callback/client.pem, key_file: /etc/callback/client.key }
    exchange:
      token_url: "https://login.example.com/oauth2/token"
      grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer"
```

Server kemudian mendapatkan setiap token dalam dua langkah. Pertama, server memanggil callback HTTP yang Anda buat. Callback mengembalikan sebuah assertion, yaitu pernyataan bertanda tangan yang biasanya berupa “JSON Web Token” (token web JSON), atau JWT. Kemudian server menukar assertion tersebut di endpoint token OAuth Anda dengan access token yang dikirimkannya ke gateway.

* `auth` adalah cara server melakukan autentikasi ke callback. Contoh ini menggunakan sertifikat klien. Untuk menggunakan bearer token yang dibaca server dari file, atur `auth: { type: bearer_file, token_file: /etc/callback/token }`.
* `exchange` menyebutkan endpoint token OAuth Anda. Server hanya mengirim `grant_type` dan assertion ke endpoint tersebut, tanpa client ID atau secret.
* Jika endpoint token Anda memerlukan lebih dari itu, hilangkan `exchange`. Minta callback Anda mendapatkan access token itu sendiri dan mengembalikannya di field `assertion`, yang kemudian dikirim server ke gateway.
* Di Kubernetes, letakkan file sertifikat di sebuah Secret, sebutkan Secret tersebut di `server.extensionFiles.secretName` milik chart, dan arahkan `cert_file` dan `key_file` ke `/run/cma-server/extension-files/`.

Server mengirim permintaan `POST` ke callback dengan body ini:

```json
{
  "version": 1,
  "purpose": "inference",
  "session": {
    "id": "sesn_011CZkZAtmR3yMPDzynEDxu7",
    "agent_id": "agent_011CYm1BLqPXpQRk5khsSXrs",
    "environment_id": "env_01595EKxaaTTGwwY3kyXdtbs"
  },
  "principal": {
    "issuer": "https://login.example.com/oauth2/default",
    "subject": "00u1a2b3c4d5e6f7g8h9"
  },
  "request_id": "req_011CSHoEeqs5C35K2UUqR7Fy"
}
```

`principal` adalah pemanggil yang membuat sesi. Untuk pemanggil [single sign-on](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#single-sign-on), `issuer` adalah `issuer_url` milik pemanggil tersebut, dan `subject` adalah subject pemanggil. Untuk kunci API server, `principal` adalah `{"issuer": "cma", "subject": "server"}`. Minta callback mengabaikan field yang tidak dikenalinya.

Callback menjawab dengan status `200` dan body ini:

```json
{ "assertion": "<signed JWT>", "reuse": "session" }
```

`reuse` menyatakan sesi mana yang dapat menggunakan token. Dengan `session`, nilai default, hanya sesi dalam permintaan yang dapat menggunakannya, yang cocok untuk token yang menyebutkan satu pengguna. Dengan `deployment`, sesi-sesi berbagi token, jadi kembalikan `deployment` hanya untuk token yang menyebutkan organisasi Anda dan bukan orang tertentu.

Jika callback atau endpoint token gagal, giliran berakhir dengan event `session.error` bertipe `model_request_failed_error`, dan sesi tetap dapat digunakan. Alasannya ada di log server, pada baris yang berisi `credential supplier failed`.

Jika balasan endpoint token tidak memiliki `expires_in` dan token tidak memiliki klaim `exp`, server mengirim token tetapi tidak menyimpannya. Server kemudian meminta token lain pada setiap panggilan model.

Untuk pengaturan lainnya, seperti `renew_before` dan `ca_file`, lihat tabel [pengaturan model gateway](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#model-gateway) dan [pengaturan token berumur pendek](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#short-lived-gateway-tokens) di Referensi konfigurasi.

### Token Microsoft Entra ID

Jika gateway Anda memeriksa token Microsoft Entra ID terhadap “app registration” (pendaftaran aplikasi) miliknya sendiri, ganti blok `credentials` dengan blok ini:

```yaml
inference:
  credentials:
    supplier: azure
    azure: { scope: "api://11111111-2222-3333-4444-555555555555/.default" }
```

`scope` adalah application ID URI atau application ID dari app registration gateway, diikuti dengan `/.default`. Sebutkan hanya registration milik gateway itu sendiri. Token untuk resource lain akan memungkinkan siapa pun yang menjalankan gateway bertindak sebagai server di sana.

Token diterbitkan untuk identitas Azure milik server sendiri, yang disiapkan seperti untuk Microsoft Entra ID di bawah [Microsoft Foundry](https://platform.claude.com/docs/id/managed-agents/self-hosted/inference-provider#microsoft-foundry). Jika registration tersebut memerlukan app role, tetapkan role tersebut ke identitas sebelum Anda memulai server. Penetapan yang dilakukan kemudian baru berlaku saat server mendapatkan token lain.

Token tersebut menyebutkan identitas itu dan bukan orang tertentu, sehingga gateway yang harus mengetahui orang mana yang memanggil memerlukan `oauth_exchange`. Jalankan satu giliran melalui gateway Anda, dengan identitas yang akan digunakan server Anda, sebelum Anda mengandalkan supplier ini.

## Memeriksa penyedia

Setelah Anda mengubah pengaturan dan memulai ulang server, cari baris ini di log server. Baris ini menyatakan bahwa server menemukan kredensial untuk penyedia:

```text wrap
level=INFO msg="upstream credential resolved" provider=bedrock
```

Baris tersebut tidak membuktikan bahwa akun Anda telah mengaktifkan suatu model. Model yang tidak tersedia akan muncul sebagai `session.error` pada giliran pertama yang menggunakannya.

Gateway yang Anda sebutkan di `ANTHROPIC_BASE_URL` mungkin menolak field atau header [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback). Jika setiap giliran gagal karena alasan tersebut, atur `inference.model_fallback: false` di [file pengaturan](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#where-settings-go).
