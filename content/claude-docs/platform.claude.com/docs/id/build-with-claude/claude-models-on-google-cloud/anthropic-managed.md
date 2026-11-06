---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed
fetched_at: 2026-11-06T02:14:07.030986Z
sha256: 658457e48675e45c55237757c65edcb55c35306505be2a97fb25f57315813fbd
---

---
title: Claude Models on Google Cloud (Anthropic managed)
url: https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed
description: Claude Models on Google Cloud (Anthropic managed) adalah Claude API, yang dijalankan oleh Anthropic dan diakses melalui proyek Google Cloud Anda.
---

Google Cloud menangani akses dan penagihan untuk Claude Models on Google Cloud (Anthropic managed). Untuk membandingkan kedua penawaran Google Cloud, atau untuk memeriksa mana yang Anda gunakan, lihat [Claude Models on Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/overview).

## Menyiapkan akun Anda

Untuk menyiapkan akun Anda untuk Claude Models on Google Cloud (Anthropic managed), Anda memerlukan hal-hal berikut:

* Izin untuk melakukan pembelian di Google Cloud Marketplace pada akun penagihan Anda
* Izin untuk mengaktifkan layanan pada proyek
* [Peran IAM yang memungkinkan Anda membuka Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#using-the-claude-console), yang Anda perlukan untuk langkah 4

Langkah-langkah ini membuat organisasi Anthropic baru untuk proyek Google Cloud Anda. Organisasi ini terpisah dari organisasi Anthropic mana pun yang sudah dimiliki perusahaan Anda. Itu termasuk organisasi Claude Enterprise. Untuk berpindah dari organisasi yang sudah ada, lihat [Berpindah dari organisasi Anthropic yang sudah ada](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#moving-from-an-existing-anthropic-organization).

Jika Anda memiliki diskon yang sudah ada, hubungi perwakilan akun Anthropic atau Google Cloud Anda sebelum memulai langkah-langkah ini. Diskon tidak dapat diterapkan pada penggunaan sebelumnya.

<Steps>
  <Step title="Berlangganan di Marketplace">
    1. Buka [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) dan temukan listing **Claude Models on Google Cloud (Anthropic managed)**.
    2. Klik **Subscribe** dan selesaikan alur pembelian.
    3. Kembali ke listing dan klik **Manage on Console**. Ini akan membuka halaman Claude di Google Cloud console.

    Untuk kembali ke halaman Claude nanti, pilih proyek Anda di Google Cloud console. Lalu buka **Agent Platform > Models > Claude Platform** dan pilih **Anthropic managed**.
  </Step>

  <Step title="Mengaktifkan layanan">
    Aktifkan dua layanan pada setiap proyek yang memanggil Claude Models on Google Cloud (Anthropic managed):

    * `claude.googleapis.com` menyajikan API untuk Claude Models on Google Cloud (Anthropic managed). Layanan ini juga mendefinisikan izin IAM. Panggilan akan gagal tanpanya.
    * `anthropic-managed-claude.cloudpartnerservices.goog` adalah layanan Marketplace yang mengatribusikan penggunaan proyek ke langganan Anda.

    ```bash CLI
    gcloud services enable claude.googleapis.com \
      anthropic-managed-claude.cloudpartnerservices.goog \
      --project=my-project-id
    ```

    Ganti `my-project-id` dengan ID proyek Anda.

    Anda juga dapat mengaktifkan keduanya dari halaman Claude atau dari **APIs & Services**. Pengaktifan adalah langkah satu kali untuk setiap proyek. Untuk memeriksa bahwa kedua layanan telah diaktifkan, jalankan `gcloud services list --enabled --project=my-project-id` dan cari kedua nama tersebut.
  </Step>

  <Step title="Menyiapkan organisasi Anthropic Anda">
    1. Di halaman Claude, klik **Activate**.
    2. Dalam alur penyiapan Anthropic, masukkan alamat email kontak.
    3. Buka tautan penyiapan yang dikirim ke alamat tersebut.
    4. Isi nama organisasi, jenis entitas, negara, dan tujuan penggunaan.
    5. Terima Ketentuan Layanan Komersial dan Kebijakan Penggunaan Anthropic.

    Alamat kontak hanya digunakan untuk penyiapan dan pemberitahuan layanan. Untuk cara orang membuka Claude Console setelah penyiapan, lihat [Menggunakan Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#using-the-claude-console).
  </Step>

  <Step title="Membuka Claude Console">
    Ketika organisasi Anthropic Anda aktif, tombol di halaman Claude berubah menjadi **Open Claude Console**. Klik tombol tersebut. Google Cloud memeriksa akses IAM Anda. Kemudian browser Anda dialihkan ke `platform.claude.com`. Anda masuk ke organisasi baru tersebut.

    Selagi Anda berada di Claude Console, [temukan ID workspace Anda](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id) dan salin. Setiap orang yang memanggil Claude Models on Google Cloud (Anthropic managed) memerlukannya. Teruskan ID tersebut kepada developer Anda.
  </Step>
</Steps>

Untuk menambahkan proyek lain, ulangi langkah-langkah ini di proyek tersebut, mulai dari langkah 2.

### Pemecahan masalah penyiapan akun

Jika Anda mengalami salah satu masalah berikut saat menyiapkan Claude Models on Google Cloud (Anthropic managed), terapkan perbaikannya:

* **`gcloud services enable` tidak dapat menemukan `anthropic-managed-claude.cloudpartnerservices.goog`:** Jalankan perintah sebagai akun yang menyelesaikan pembelian Marketplace, atau hubungi perwakilan akun Anthropic Anda.
* **Error izin pada panggilan API pertama Anda:** Periksa bahwa `claude.googleapis.com` telah diaktifkan pada proyek yang Anda panggil. Periksa bahwa pemanggil memiliki `roles/claude.user` atau `roles/claude.admin` pada proyek tersebut. Untuk apa yang diizinkan setiap peran, lihat [Peran IAM](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles). Pemberian izin baru atau layanan yang baru diaktifkan dapat memerlukan waktu sejenak untuk berlaku.
* **“Sudah masuk dengan akun lain” setelah mengikuti tautan penyiapan:** Klik **Keluar dan lanjutkan**. Lalu gunakan alamat email yang Anda masukkan di langkah 3.
* **Tombol menampilkan “Finish Setup” alih-alih “Open Claude Console”:** Organisasi Anthropic Anda sudah ada, tetapi penyiapannya belum selesai. Seorang administrator harus menyelesaikan formulir detail organisasi.
* **Halaman Penggunaan tidak menampilkan data setelah panggilan API pertama Anda:** Data penggunaan dapat memerlukan beberapa menit untuk muncul di Claude Console.

## Mengelola akses

### Peran IAM

Claude Models on Google Cloud (Anthropic managed) memiliki tiga peran IAM yang telah ditentukan sebelumnya. Berikan peran pada proyek.

| Peran                 | Nama tampilan | Apa yang diizinkan                                                                                                                                                                                                                            |
| --------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `roles/claude.viewer` | Claude Viewer | Setiap izin `get` dan `list` pada sumber daya workspace<br />Peran ini bersifat hanya-baca.                                                                                                                                                   |
| `roles/claude.user`   | Claude User   | Semua yang diizinkan `roles/claude.viewer`, ditambah membuat dan mengubah sumber daya workspace<br />Ini termasuk mengirim pesan dan menghitung token. Ini juga termasuk mengelola batch, file, skill, dan sumber daya Claude Managed Agents. |
| `roles/claude.admin`  | Claude Admin  | Semua yang diizinkan `roles/claude.user`, ditambah izin yang diperiksa pada organisasi Anthropic Anda<br />Rute tingkat organisasi bertindak pada organisasi Anthropic Anda secara keseluruhan, bukan pada satu workspace.                    |

Sebagai contoh, perintah berikut memungkinkan akun layanan memanggil Claude Models on Google Cloud (Anthropic managed):

```bash CLI
gcloud projects add-iam-policy-binding my-project-id \
  --member="serviceAccount:my-app@my-project-id.iam.gserviceaccount.com" \
  --role="roles/claude.user"
```

Untuk izin, peran yang telah ditentukan sebelumnya, dan jenis log audit, lihat [Izin IAM untuk Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/api/claude-models-on-google-cloud-anthropic-managed-iam-permissions).

Mengaktifkan `claude.googleapis.com` akan membuat service agent untuk proyek. Jangan hapus pemberian perannya. Menghapusnya akan menghentikan Claude Models on Google Cloud (Anthropic managed) agar tidak berfungsi di proyek tersebut.

### Menggunakan Claude Console

Dengan Claude Models on Google Cloud (Anthropic managed), Anda tidak dapat menggunakan alamat email untuk masuk ke organisasi Anthropic Anda. Sebagai gantinya, klik **Open Claude Console** di [halaman Claude](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account) di Google Cloud console. Google Cloud IAM mengontrol siapa yang dapat membuka Claude Console. Dari tiga [peran IAM](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles) yang telah ditentukan sebelumnya, hanya `roles/claude.admin` pada proyek yang memungkinkan Anda membuka Claude Console.

### Workspace

Di Claude Models on Google Cloud (Anthropic managed), penyiapan membuat organisasi Anthropic Anda dengan satu workspace, yaitu workspace default. Untuk membuat lebih banyak workspace, [buka Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#using-the-claude-console) dan buka **Pengaturan > Ruang kerja**. Di halaman yang sama, Anda dapat mengganti nama atau mengarsipkan workspace mana pun kecuali workspace default. Setiap workspace memiliki [ID workspace](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id) sendiri. File, skill, batch, sesi Claude Managed Agents, dan sumber daya workspace lainnya menjadi milik workspace yang ID-nya Anda [tetapkan untuk permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution).

Anda memberikan [peran IAM](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles) pada proyek, sehingga sebuah peran berlaku untuk setiap workspace di proyek tersebut. Ketika tim memerlukan akses terpisah, berikan setiap tim proyek Google Cloud sendiri. Setiap proyek memiliki organisasi Anthropic sendiri, jadi ulangi [langkah-langkah penyiapan](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account) di setiap proyek, mulai dari langkah 2.

## Sebelum melakukan panggilan API

Untuk memanggil Claude Models on Google Cloud (Anthropic managed), Anda memerlukan hal-hal berikut:

1. Proyek Google Cloud dengan langganan aktif dan organisasi Anthropic yang penyiapannya telah selesai. Lihat [Menyiapkan akun Anda](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account).
2. [gcloud CLI](https://cloud.google.com/sdk/docs/install) yang terinstal, untuk pengembangan lokal.
3. Peran `roles/claude.user`, yang diberikan pada proyek kepada identitas yang melakukan panggilan.
4. Application Default Credentials untuk identitas tersebut. Lihat [Autentikasi](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#authentication).
5. ID proyek dan [ID workspace](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id) Anda.

Untuk memberikan peran tersebut ke akun Anda sendiri untuk pengembangan lokal, jalankan perintah berikut. Anda memerlukan izin untuk mengubah kebijakan IAM proyek.

```bash CLI
gcloud projects add-iam-policy-binding my-project-id \
  --member="user:you@example.com" \
  --role="roles/claude.user"
```

Ganti `my-project-id` dengan ID proyek Anda. Ganti `you@example.com` dengan alamat email akun Google Anda. Untuk melihat proyek yang digunakan gcloud, jalankan `gcloud config get-value project`. Untuk service account dan peran lainnya, lihat [Peran IAM](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles).

### Menemukan ID workspace Anda

Untuk menemukan ID workspace Anda untuk Claude Models on Google Cloud (Anthropic managed), [buka Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#using-the-claude-console) dan buka **Pengaturan > Ruang kerja**. ID tersebut diawali dengan `wrkspc_`. Jika Anda tidak dapat membuka Claude Console, minta seseorang yang dapat membukanya untuk mengirimkan ID tersebut kepada Anda.

Tetapkan proyek dan workspace sebagai variabel lingkungan agar klien SDK dan [CLI `ant`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart) dapat membacanya:

```bash CLI
export ANTHROPIC_GOOGLE_CLOUD_PROJECT="my-project-id"
export ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID="wrkspc_01AbCdEf23GhIj"
```

### Menginstal SDK

[Klien SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) untuk Claude Models on Google Cloud (Anthropic managed) adalah `AnthropicGoogleCloud` (csharp: `AnthropicGoogleCloudClient`; go: `googlecloud.NewClient()`; java: `GoogleCloudBackend`; php: `Anthropic\GoogleCloud\Client`; ruby: `Anthropic::GoogleCloudClient`). Klien ini menyelesaikan kredensial Google Anda. Klien ini juga membangun base URL dari proyek, lokasi, dan ID workspace Anda.

<Note>
  Klien SDK untuk Claude Models on Google Cloud (Anthropic managed) masih dalam tahap beta.
</Note>

Instal paket yang menyediakan klien tersebut:

<Tabs>
  <Tab title="Python">
    ```bash
    pip install -U "anthropic[google_cloud]"
    ```
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/google-cloud-sdk
    ```
  </Tab>

  <Tab title="C#">
    ```bash
    dotnet add package Anthropic.GoogleCloud
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    go get github.com/anthropics/anthropic-sdk-go/v2/googlecloud
    ```
  </Tab>

  <Tab title="Java">
    <Tabs>
      <Tab title="Gradle">
        ```kotlin
        implementation("com.anthropic:anthropic-java:3.6.0")
        implementation("com.anthropic:anthropic-java-google-cloud:3.6.0")
        ```
      </Tab>

      <Tab title="Maven">
        ```xml
        <dependency>
            <groupId>com.anthropic</groupId>
            <artifactId>anthropic-java</artifactId>
            <version>3.6.0</version>
        </dependency>
        <dependency>
            <groupId>com.anthropic</groupId>
            <artifactId>anthropic-java-google-cloud</artifactId>
            <version>3.6.0</version>
        </dependency>
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="PHP">
    ```bash
    composer require anthropic-ai/sdk google/auth
    ```
  </Tab>

  <Tab title="Ruby">
    ```bash
    gem install anthropic googleauth
    ```
  </Tab>
</Tabs>

Untuk menggunakan `ant` CLI sebagai gantinya, [instal atau perbarui CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart#installation) ke versi terbaru. Versi tanpa dukungan untuk Claude Models on Google Cloud (Anthropic managed) akan mengabaikan variabel `ANTHROPIC_GOOGLE_CLOUD_*`. Versi tersebut kemudian melakukan salah satu hal berikut:

* Mengirim permintaan ke Claude API dengan kredensial lain yang telah Anda siapkan
* Gagal dengan error autentikasi

## Melakukan permintaan

Claude Models on Google Cloud (Anthropic managed) menyajikan endpoint Claude API di bawah base URL yang menyebutkan proyek Anda, sebuah lokasi, dan workspace Anda:

```text wrap
https://claude.googleapis.com/v1/projects/{project}/locations/global/workspaces/{workspace}/invoke
```

[Rute tingkat organisasi](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles), yang path-nya diawali dengan `/v1/organizations/`, dan rute [profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) di bawah `/v1/user_profiles` menggunakan base URL tanpa workspace:

```text wrap
https://claude.googleapis.com/v1/projects/{project}/locations/global/claudeOrganization/invoke
```

Jika Anda tidak [menetapkan base URL](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution), klien SDK akan memilih di antara keduanya untuk setiap permintaan.

Tambahkan path Claude API ke base URL. Sebagai contoh, [Messages API](https://platform.claude.com/docs/id/api/messages/create) berada di `.../invoke/v1/messages`. Tiga hal berbeda dari permintaan Claude API:

* **Base URL:** URL dengan cakupan proyek yang ditunjukkan sebelumnya, sebagai pengganti `https://api.anthropic.com`.
* **Autentikasi:** Header `Authorization: Bearer` dengan token akses Google. Jangan kirim header `x-api-key`.
* **Workspace:** ID workspace merupakan bagian dari URL. Jangan kirim header `anthropic-workspace-id`.

Semua hal lainnya sama seperti di Claude API, termasuk yang berikut:

* Header `anthropic-version` dan `anthropic-beta`
* Body permintaan
* Streaming
* Respons

Contoh kode di bagian lain dokumentasi ini membuat klien Claude API dan membaca kunci API. Untuk menjalankannya dengan Claude Models on Google Cloud (Anthropic managed), ganti impor dan konstruktor kliennya dengan yang ada di contoh berikut. Untuk contoh cURL, terapkan tiga perbedaan yang tercantum sebelumnya.

Sebelum menjalankan contoh-contoh ini, selesaikan langkah-langkah di [Sebelum melakukan panggilan API](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#before-making-api-calls).

<CodeGroup>
  ```bash cURL
  curl "https://claude.googleapis.com/v1/projects/$ANTHROPIC_GOOGLE_CLOUD_PROJECT/locations/global/workspaces/$ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID/invoke/v1/messages" \
    -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
    -H "content-type: application/json" \
    -H "anthropic-version: 2026-10-21" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello, Claude"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  from anthropic import AnthropicGoogleCloud

  client = AnthropicGoogleCloud()

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(message)
  ```

  ```typescript TypeScript
  import { AnthropicGoogleCloud } from "@anthropic-ai/google-cloud-sdk";

  const client = new AnthropicGoogleCloud();

  const message = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  console.log(message);
  ```

  ```csharp C#
  using Anthropic.GoogleCloud;
  using Anthropic.Models.Messages;

  var client = new AnthropicGoogleCloudClient();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new UserMessageParam { Content = "Hello, Claude" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go/v2"
  	"github.com/anthropics/anthropic-sdk-go/v2/googlecloud"
  )

  func main() {
  	client, err := googlecloud.NewClient(context.Background(), googlecloud.ClientConfig{})
  	if err != nil {
  		panic(err)
  	}

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}

  	fmt.Println(message)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.googlecloud.backends.GoogleCloudBackend;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(GoogleCloudBackend.fromEnv())
          .build();

      Message message = client.messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024)
              .addUserMessage("Hello, Claude")
              .build()
      );

      IO.println(message);
  }
  ```

  ```php PHP
  use Anthropic\GoogleCloud\Client;
  use Anthropic\Messages\Model;

  $client = new Client();

  $message = $client->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );

  echo $message;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::GoogleCloudClient.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  )

  puts message
  ```
</CodeGroup>

Contoh cURL meminta token Application Default Credentials dari gcloud. Access token berumur pendek. Buat token untuk setiap sesi alih-alih menyimpannya.

### ID model API

Claude Models on Google Cloud (Anthropic managed) menggunakan ID model yang sama dengan Claude API, misalnya `claude-opus-5-5`. Untuk model dan ID-nya, lihat [Ikhtisar model](https://platform.claude.com/docs/id/models/overview).

Di Claude Models on Google Cloud (Anthropic managed), permintaan untuk model yang tidak tersedia bagi organisasi Anthropic Anda akan mengembalikan error. Pesan error-nya berbunyi `Model {model} is not available for this organization's inference configuration.`

## Resolusi proyek, lokasi, dan workspace

Klien untuk Claude Models on Google Cloud (Anthropic managed) menerima pengaturan dalam tabel berikut. Nilai yang Anda berikan saat membuat klien lebih diutamakan daripada variabel lingkungan. Untuk menetapkan proyek dan ID workspace secara eksplisit, berikan `project` (go: `Project`; java: `.project()`; csharp: `GoogleCloudClientOptions.Project`; cli: `--google-cloud-project`) dan `workspace_id` (typescript, php: `workspaceId`; go: `WorkspaceID`; java: `.workspaceId()`; csharp: `GoogleCloudClientOptions.WorkspaceId`; cli: `--google-cloud-workspace-id`).

| Pengaturan   | Variabel lingkungan                                           | Jika tidak ditetapkan                                                                                                                                                                                                                                                                                                           |
| ------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID proyek    | `ANTHROPIC_GOOGLE_CLOUD_PROJECT`, lalu `GOOGLE_CLOUD_PROJECT` | Proyek yang dilaporkan Application Default Credentials, jika jenis kredensial membawanya                                                                                                                                                                                                                                        |
| ID workspace | `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID`                         | Klien memunculkan error kecuali Anda menetapkan base URL. [Rute tingkat organisasi](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles) dan rute [profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) tidak memerlukan ID workspace. |
| Lokasi       | `ANTHROPIC_GOOGLE_CLOUD_LOCATION`                             | `global`                                                                                                                                                                                                                                                                                                                        |
| Base URL     | `ANTHROPIC_GOOGLE_CLOUD_BASE_URL`                             | Diturunkan dari proyek, lokasi, dan ID workspace                                                                                                                                                                                                                                                                                |

Biarkan lokasi tetap `global`. Lokasi terpisah dari tempat inferensi dijalankan, jadi untuk inferensi khusus AS, tetapkan `inference_geo: "us"` pada setiap permintaan, seperti yang dijelaskan di [Residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency#inference-geo).

`ant` CLI menerima pengaturan yang sama sebagai flag:

* **ID proyek:** `--google-cloud-project`
* **ID workspace:** `--google-cloud-workspace-id`
* **Lokasi:** `--google-cloud-location`
* **Base URL:** `--google-cloud-base-url`

CLI menggunakan Claude Models on Google Cloud (Anthropic managed) ketika proyek, ID workspace, atau lokasi ditetapkan. Menetapkan `GOOGLE_CLOUD_PROJECT`, base URL, atau keduanya tidaklah cukup.

## Autentikasi

Setiap permintaan ke Claude Models on Google Cloud (Anthropic managed) membawa token akses Google OAuth 2.0 dalam header `Authorization: Bearer`. Token tersebut memiliki cakupan `https://www.googleapis.com/auth/cloud-platform`.

Google Cloud menangani akses. Gateway-nya di `claude.googleapis.com` melakukan hal berikut untuk setiap permintaan:

1. Memeriksa kredensial Google Cloud Anda.
2. Memeriksa bahwa pemanggil memiliki izin IAM yang diperlukan permintaan. Jika pemanggil tidak memilikinya, Google Cloud mengembalikan error HTTP 403.
3. Meneruskan permintaan ke Anthropic. Anthropic memvalidasi permintaan tersebut.

Untuk memberikan izin, lihat [Peran IAM](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles).

Klien SDK mendapatkan token dari [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials) (ADC). Sumber kredensial apa pun yang didukung ADC dapat digunakan:

* **Pengembangan lokal:** Jalankan `gcloud auth application-default login`.
* **Di Google Cloud:** Klien secara otomatis menggunakan akun layanan yang terpasang pada workload, misalnya di Compute Engine, GKE, atau Cloud Run.
* **File kunci akun layanan:** Tetapkan `GOOGLE_APPLICATION_CREDENTIALS` ke path-nya.
* **Workload Identity Federation dan impersonasi akun layanan:** Konfigurasikan seperti yang Anda lakukan untuk Google Cloud API mana pun.

Periksa bahwa ADC berfungsi:

```bash CLI
gcloud auth application-default print-access-token
```

Claude Models on Google Cloud (Anthropic managed) tidak menggunakan kunci API. Di Claude Console, Anda tidak dapat membuat kunci API untuk organisasi Anthropic yang dibuat oleh penyiapan. Klien SDK untuk Claude Models on Google Cloud (Anthropic managed) mengabaikan variabel lingkungan berikut:

* `ANTHROPIC_API_KEY`
* `ANTHROPIC_AUTH_TOKEN`
* `ANTHROPIC_BASE_URL`

### Prioritas kredensial

Klien SDK untuk Claude Models on Google Cloud (Anthropic managed) memeriksa kredensial dalam urutan berikut. Klien menggunakan yang pertama kali ditemukannya:

1. Penyedia token yang Anda berikan sebagai `token_provider` (typescript: `bearerTokenProvider`; csharp: `GoogleCloudClientOptions.TokenProvider`; go: `TokenSource`; java: `.bearerTokenSupplier()`; php: `tokenProvider`) saat Anda membuat klien. Ini adalah fungsi atau sumber token yang mengembalikan token akses. Klien memintanya untuk token pada setiap permintaan. Caching dan penyegaran token menjadi tanggung jawab Anda.
2. Objek kredensial Google yang Anda berikan sebagai `credentials` (typescript: `googleAuth`; csharp: `GoogleCloudClientOptions.GoogleCredential`; java: `.googleCredentials()`; php: `googleCredentials`; ruby: `google_credentials`) saat Anda membuat klien. Go SDK tidak memiliki opsi ini.
3. Application Default Credentials.

Go dan Java berbeda dari SDK lainnya:

* **Go:** Untuk opsi 1, klien menerima `oauth2.TokenSource`. Klien melakukan caching token hingga token kedaluwarsa.
* **Java:** Gunakan `GoogleCloudBackend.fromEnv()` untuk membaca Application Default Credentials dan variabel lingkungan di [Resolusi proyek, lokasi, dan workspace](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution).

Klien tidak memiliki variabel lingkungan sendiri untuk kredensial. Gunakan `GOOGLE_APPLICATION_CREDENTIALS` milik ADC sebagai gantinya.

Jika permintaan Anda melewati proxy yang melampirkan token untuk Anda, tetapkan `skip_auth` (typescript, php: `skipAuth`; go: `SkipAuth`; java: `.skipAuth()`; csharp: `GoogleCloudClientOptions.SkipAuth`). Klien kemudian tidak mengirim header `Authorization`. Anda tidak dapat menggabungkan pengaturan ini dengan opsi kredensial sebelumnya.

Ketika `ant` CLI menggunakan Claude Models on Google Cloud (Anthropic managed), CLI selalu mendapatkan token dari Application Default Credentials. CLI tidak menerima penyedia token, objek kredensial, atau pengaturan untuk melewati autentikasi.

Sebelum Anda menggunakan `ant` dengan Claude Models on Google Cloud (Anthropic managed), pastikan tidak ada satu pun dari berikut ini yang ditetapkan:

* Kunci API

* Token autentikasi

* `--profile` atau `ANTHROPIC_PROFILE`, jika menyebutkan [profil konfigurasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#profile-configuration-file) yang dapat digunakan CLI untuk autentikasi

* Salah satu variabel federasi Anthropic:

  * `ANTHROPIC_FEDERATION_RULE_ID`
  * `ANTHROPIC_ORGANIZATION_ID`
  * `ANTHROPIC_SERVICE_ACCOUNT_ID`
  * `ANTHROPIC_IDENTITY_TOKEN`
  * `ANTHROPIC_IDENTITY_TOKEN_FILE`

Jika salah satunya ditetapkan, CLI menggunakan kredensial tersebut alih-alih pengaturan Google Cloud dari [Menemukan ID workspace Anda](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id). Jika hanya sebagian variabel federasi yang ditetapkan, CLI berhenti dengan error. Ketika lebih dari satu kredensial ditetapkan, CLI mencetak catatan yang menyebutkan kredensial yang digunakannya.

Biarkan juga `ANTHROPIC_WORKSPACE_ID` dan flag `--workspace-id` tidak ditetapkan. CLI tetap mengirim nilai tersebut sebagai header `anthropic-workspace-id`. Permintaan ke Claude Models on Google Cloud (Anthropic managed) tidak boleh membawa header tersebut. Tetapkan workspace dengan `--google-cloud-workspace-id` atau `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID` sebagai gantinya.

Seperti klien SDK, CLI tidak mengirim permintaan untuk Claude Models on Google Cloud (Anthropic managed) ke `--base-url` atau `ANTHROPIC_BASE_URL`.

## Dukungan fitur

Bagian ini mencantumkan fitur yang berfungsi di Claude Models on Google Cloud (Anthropic managed) dan fitur yang tidak didukung di sana. Bagian ini tidak mencantumkan setiap fitur Claude API, dan tidak menyatakan apakah fitur yang tidak tercantum berfungsi.

Models API dan fitur-fitur berikut tersedia di Claude Models on Google Cloud (Anthropic managed):

* [Alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) (Beta)
* [Agent Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview)
  * [Skill Kustom](https://platform.claude.com/docs/id/build-with-claude/skills-guide#managing-custom-skills)
  * [Agent Skills siap pakai](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview#pre-built-agent-skills)
* [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing)
* [Penolakan pengklasifikasi](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback)
  * [Fallback sisi klien](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback) (Beta)
  * [Fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) (Beta)
* [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool)
* [Alat kustom](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools)
* [Residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency)
* [Effort](https://platform.claude.com/docs/id/build-with-claude/effort)
  * [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) (Beta)
* [Mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode)
* [Files API](https://platform.claude.com/docs/id/build-with-claude/files)
* [Konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector) (Beta)
  * [Helper MCP sisi klien](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#client-side-mcp-helpers) (Beta)
* [Alat memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool)
  * [Helper alat memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool#implement-the-memory-handler) (Beta)
* [Streaming pesan](https://platform.claude.com/docs/id/build-with-claude/streaming)
* [Thread pesan](https://platform.claude.com/docs/id/build-with-claude/message-threads) (Beta)
* [Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages)
  * [Perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) (Beta)
  * [Pesan sistem lingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) (Beta)
* [OpenTelemetry](https://platform.claude.com/docs/id/manage-claude/opentelemetry) (Beta)
* [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support)
* [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)
  * [Durasi 1 jam](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration)
  * [Durasi 5 menit (default)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#how-prompt-caching-works)
  * [Caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching)
* [Middleware SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/middleware)
* [Output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs)
  * [Helper output terstruktur bertipe](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#usage)
* [Pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking)
  * [Pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost)
  * [Pemikiran diperpanjang](https://platform.claude.com/docs/id/build-with-claude/extended-thinking)
* [Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting)
* [Tool runner](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner) (Beta)
* [Vision (gambar)](https://platform.claude.com/docs/id/build-with-claude/vision)
* [Alat web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool)
* [Alat pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool)

Jika suatu fitur beta dibatasi hanya untuk organisasi tertentu di Claude API, organisasi Anthropic yang dibuat oleh proses penyiapan memerlukan akses yang sama.

Untuk mengaktifkan atau menonaktifkan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) untuk organisasi Anthropic yang dibuat oleh penyiapan, [buka Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#using-the-claude-console), buka **Pengaturan > Kepatuhan**, dan gunakan toggle **Compliance API**.

“Customer-managed encryption keys” (kunci enkripsi yang dikelola pelanggan), atau CMEK, tersedia dengan kunci Google Cloud KMS. Untuk mengaktifkan CMEK untuk organisasi Anthropic yang dibuat oleh penyiapan, lihat [Siapa yang dapat menggunakan CMEK](https://platform.claude.com/docs/id/manage-claude/cmek#availability). Untuk menyiapkan kunci, ikuti [Menyiapkan CMEK dengan Google Cloud KMS](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms). Kemudian daftarkan, verifikasi, dan lampirkan kunci di [Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#using-the-claude-console), seperti yang dijelaskan tab **Claude Platform** di halaman penyiapan.

### Claude Managed Agents

[Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) tersedia melalui Claude Models on Google Cloud (Anthropic managed), termasuk [sesi](https://platform.claude.com/docs/id/managed-agents/sessions) dan fitur-fitur berikut:

* [Konfigurasi agen](https://platform.claude.com/docs/id/managed-agents/agent-setup) (Beta)
* [Sandbox cloud](https://platform.claude.com/docs/id/managed-agents/environments) (Beta)
* [Delta event](https://platform.claude.com/docs/id/managed-agents/event-deltas) (Beta)
* [Akses GitHub](https://platform.claude.com/docs/id/managed-agents/github) (Beta)
* [Memory store](https://platform.claude.com/docs/id/managed-agents/memory) (Beta)
* [Orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) (Beta)
  * [Alur kerja dinamis](https://platform.claude.com/docs/id/managed-agents/workflow-runs) (Beta)
  * [Thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads) (Beta)
* [Outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) (Beta)
* [Kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) (Beta)
* [Pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking)
* [Deployment terjadwal](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments) (Beta)
* [Sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) (Beta)
* [Anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets) (Beta)
* [Vault](https://platform.claude.com/docs/id/managed-agents/vaults) (Beta)
* [Pembatasan domain web](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions) (Beta)

Akses diperiksa saat sesi atau deployment dibuat, bukan saat sedang berjalan:

* **Sesi yang sedang berjalan tetap berjalan.** Jika Anda mencabut akses Google Cloud dari identitas yang membuat sesi, sesi tersebut tidak berhenti. Untuk menghentikannya, kirimkan [event `user.interrupt`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#integrating-events) secara tersendiri. Setelah sesi berstatus `idle`, Anda dapat mengarsipkan atau menghapusnya.
* **Deployment terjadwal tetap berjalan.** Deployment tidak memeriksa ulang akses pembuatnya pada setiap eksekusi terjadwal. Untuk menghentikannya, jeda, perbarui, atau arsipkan deployment tersebut.

Ketika Anda menghapus pengguna atau merotasi akun layanan, tinjau sesi dan deployment yang dibuat oleh identitas tersebut.

### Fitur yang tidak didukung

Hal-hal berikut tidak didukung di Claude Models on Google Cloud (Anthropic managed):

* **Kunci API:** Autentikasi hanya melalui kredensial Google Cloud.
* **Tunnel MCP:** [Tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview) tidak tersedia di Claude Models on Google Cloud (Anthropic managed).
* **[Memory store pada environment self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory):** Memory store tidak didukung untuk sesi pada environment self-hosted.
* **Worker sandbox yang di-host sendiri yang sudah jadi:** [Worker yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers) di `ant` CLI dan di SDK Python, TypeScript, dan Go tidak mendukung Claude Models on Google Cloud (Anthropic managed). Sebagai gantinya, implementasikan worker Anda sendiri yang memanggil [endpoint Environments Work](https://platform.claude.com/docs/id/api/beta/environments/work) secara langsung. Untuk peran dan izin yang dibutuhkan worker Anda, lihat [izin IAM untuk environment](https://platform.claude.com/docs/id/api/claude-models-on-google-cloud-anthropic-managed-iam-permissions#environments).

### Jendela konteks

Ukuran “context window” (jendela konteks) di Claude Models on Google Cloud (Anthropic managed) sama dengan di Claude API. Untuk batas setiap model, lihat [Jendela konteks](https://platform.claude.com/docs/id/build-with-claude/context-windows).

## Penagihan, batas laju, dan logging

### Batas laju

Anthropic mengelola “rate limit” (batas laju) untuk Claude Models on Google Cloud (Anthropic managed). Untuk meminta batas yang lebih tinggi, hubungi perwakilan akun Anthropic Anda atau [hubungi tim penjualan](https://claude.com/contact-sales). Untuk cara batas laju diukur dan dilaporkan, lihat [Batas laju](https://platform.claude.com/docs/id/api/rate-limits).

### Penagihan

Claude Models on Google Cloud (Anthropic managed) ditagih melalui Google Cloud Marketplace. Anthropic mengukur penggunaan Anda. Anthropic melaporkan penggunaan tersebut ke Google Cloud dalam satuan Claude Consumption Unit. Satu Claude Consumption Unit bernilai $0,01 USD. Biaya tersebut muncul pada tagihan Google Cloud Anda. Anthropic tidak mengirimkan faktur terpisah.

Lihat data penggunaan dan biaya di halaman **Penggunaan** dan **Biaya** di [Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#using-the-claude-console), atau kueri data tersebut dengan [Usage and Cost Analytics API](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api).

Jika Anda memiliki komitmen pembelanjaan Google Cloud, penggunaan dihitung terhadap komitmen tersebut seperti pembelian Marketplace lainnya.

### Retensi data

Anthropic adalah pemroses data untuk Claude Models on Google Cloud (Anthropic managed). Beberapa layanan pendukung, seperti sistem kepercayaan dan keamanan Anthropic, memproses data di luar Google Cloud.

Claude Models on Google Cloud (Anthropic managed) mengikuti kebijakan retensi data yang sama dengan Claude API. Lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention). “Zero Data Retention” (retensi data nol), atau ZDR, tersedia berdasarkan permintaan. Hubungi perwakilan akun Anthropic Anda.

Pengaturan ZDR pada organisasi Anthropic lain tidak berlaku untuk organisasi Anda untuk Claude Models on Google Cloud (Anthropic managed).

### Pemantauan dan logging

[Cloud Audit Logs](https://cloud.google.com/logging/docs/audit) mencatat aktivitas API untuk Claude Models on Google Cloud (Anthropic managed) di proyek Anda. Entri muncul di bawah layanan `claude.googleapis.com`. Setiap rute API termasuk dalam salah satu dari dua jenis log:

* **Log Data Access:** Log ini mencakup sebagian besar rute, termasuk pesan, batch, file, skill, model, dan sebagian besar sumber daya Claude Managed Agents. Log ini nonaktif secara default.
* **Log Admin Activity:** Log ini mencakup rute lainnya, termasuk rute kunci enkripsi dan sebagian besar rute vault kredensial. Pengecualiannya adalah rute untuk `vaults.verify`, yang termasuk Data Access. Log Admin Activity selalu aktif.

Untuk menyimpan catatan permintaan, aktifkan log Data Access untuk `claude.googleapis.com` di pengaturan log audit proyek Anda.

Untuk jenis log audit berdasarkan rute, lihat [Izin IAM untuk Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/api/claude-models-on-google-cloud-anthropic-managed-iam-permissions).

#### ID permintaan

Respons yang berhasil dari Claude Models on Google Cloud (Anthropic managed) membawa header [`request-id`](https://platform.claude.com/docs/id/api/errors#request-id).

## Berpindah dari organisasi Anthropic yang sudah ada

Anda tidak dapat mengonversi organisasi Anthropic yang sudah ada menjadi organisasi untuk Claude Models on Google Cloud (Anthropic managed). Itu termasuk organisasi yang Anda gunakan dengan Claude API secara langsung.

Rencanakan perpindahan sebagai cutover ke organisasi baru:

* **Buat organisasi baru terlebih dahulu.** Ikuti [Menyiapkan akun Anda](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account).
* **Buat ulang akses dan konfigurasi.** Kunci API, workspace, dan pengaturan Claude Console tidak ikut terbawa. Berikan [peran IAM](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles) pada proyek alih-alih membuat kunci API. Untuk membuat ulang workspace Anda, lihat [Workspace](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#workspaces). Untuk pengaturan ZDR, lihat [Retensi data](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#data-retention).
* **Rencanakan untuk sumber daya yang tersimpan.** File, skill, batch, dan sumber daya Claude Managed Agents tetap berada di organisasi yang sudah ada.
* **Perbarui integrasi Anda.** Untuk apa yang berubah dan apa yang tetap sama, lihat [Melakukan permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#making-requests). Untuk fitur yang tidak didukung, lihat [Fitur yang tidak didukung](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#features-not-supported).
* **Lakukan cutover sesuai jadwal Anda sendiri.** Kedua organisasi bersifat independen dan dapat melayani lalu lintas secara paralel. Anda dapat memindahkan workload secara bertahap. Organisasi yang sudah ada tetap menggunakan penagihannya saat ini. Sebelum Anda mengalihkan lalu lintas produksi, periksa [batas laju untuk Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#rate-limits).

## Bermigrasi dari Claude Models on Google Cloud (Google managed)

Untuk beralih ke Claude Models on Google Cloud (Anthropic managed), selesaikan langkah-langkah berikut. Sebelum Anda memindahkan beban kerja yang bergantung pada pengaturan ZDR, lihat [Retensi data](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#data-retention). Untuk mengetahui apa yang berubah saat Anda beralih, lihat [Perbedaan kedua penawaran Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/overview#how-the-two-google-cloud-offerings-differ).

<Steps>
  <Step title="Siapkan akun Anda">
    Selesaikan setiap langkah di [Siapkan akun Anda](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account).
  </Step>

  <Step title="Siapkan akses">
    Berikan `roles/claude.user` kepada setiap identitas yang memanggil Claude Models on Google Cloud (Anthropic managed). Tetapkan proyek dan ID workspace Anda sebagai variabel lingkungan. Untuk keduanya, lihat [Sebelum melakukan panggilan API](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#before-making-api-calls).
  </Step>

  <Step title="Instal paket SDK">
    Instal paket yang menyediakan klien untuk Claude Models on Google Cloud (Anthropic managed). Lihat [Instal SDK](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#install-an-sdk).
  </Step>

  <Step title="Ganti impor dan klien">
    Ubah kode yang mengimpor dan membuat klien Anda. Gunakan `AnthropicGoogleCloud` (csharp: `AnthropicGoogleCloudClient`; go: `googlecloud.NewClient()`; java: `GoogleCloudBackend`; php: `Anthropic\GoogleCloud\Client`; ruby: `Anthropic::GoogleCloudClient`) sebagai pengganti `AnthropicVertex` (csharp: `AnthropicVertexClient`; go: `vertex.WithGoogleAuth()`; java: `VertexBackend`; php: `Anthropic\Vertex\Client`; ruby: `Anthropic::VertexClient`). Dalam permintaan cURL, ubah URL, header, dan body. Kode Anda saat ini membuat klien untuk Claude Models on Google Cloud (Google managed). Misalnya, kode berikut membuat klien tersebut dengan endpoint global:

    <CodeGroup exclude="shell:CLI">
      ```bash cURL
      curl https://aiplatform.googleapis.com/v1/projects/MY_PROJECT_ID/locations/global/publishers/anthropic/models/claude-opus-5-5:rawPredict \
        -H "Authorization: Bearer $(gcloud auth print-access-token)" \
        -H "Content-Type: application/json" \
        -d '{
          "anthropic_version": "2026-10-21",
          "messages": [{"role": "user", "content": "Hey Claude!"}],
          "max_tokens": 100
        }'
      ```

      <CodeGroupItem language="CLI">
        CLI `ant` tidak mendukung Claude Models on Google Cloud (Google managed).
      </CodeGroupItem>

      ```python Python
      from anthropic import AnthropicVertex

      project_id = "MY_PROJECT_ID"
      region = "global"

      client = AnthropicVertex(project_id=project_id, region=region)
      ```

      ```typescript TypeScript
      import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

      const projectId = "MY_PROJECT_ID";
      const region = "global";

      const client = new AnthropicVertex({
        projectId,
        region
      });
      ```

      ```csharp C#
      using Anthropic.Vertex;

      var projectId = "MY_PROJECT_ID";
      var region = "global";

      var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));
      ```

      ```go Go
      import (
      	"context"

      	"github.com/anthropics/anthropic-sdk-go/v2"
      	"github.com/anthropics/anthropic-sdk-go/v2/vertex"
      )
      // ...
      	// Menggunakan kredensial default Google Cloud
      	client := anthropic.NewClient(
      		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
      	)
      ```

      ```java Java
      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.vertex.backends.VertexBackend;
      import com.google.auth.oauth2.GoogleCredentials;

      void main() throws Exception {
          AnthropicClient client = AnthropicOkHttpClient.builder()
              .backend(
                  VertexBackend.builder()
                      .googleCredentials(GoogleCredentials.getApplicationDefault())
                      .region("global")
                      .project("MY_PROJECT_ID")
                      .build()
              )
              .build();
      }
      ```

      ```php PHP
      use Anthropic\Vertex;

      $client = Vertex\Client::fromEnvironment(
          region: 'global',
          projectId: 'MY_PROJECT_ID',
      );
      ```

      ```ruby Ruby
      require "anthropic"

      client = Anthropic::VertexClient.new(
        region: "global",
        project_id: "MY_PROJECT_ID"
      )
      ```
    </CodeGroup>

    Kode berikut membuat klien untuk Claude Models on Google Cloud (Anthropic managed):

    <CodeGroup>
      ```bash cURL
      curl "https://claude.googleapis.com/v1/projects/$ANTHROPIC_GOOGLE_CLOUD_PROJECT/locations/global/workspaces/$ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID/invoke/v1/messages" \
        -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
        -H "content-type: application/json" \
        -H "anthropic-version: 2026-10-21" \
        -d '{
          "model": "claude-opus-5-5",
          "max_tokens": 1024,
          "messages": [
            {"role": "user", "content": "Hello, Claude"}
          ]
        }'
      ```

      ```bash CLI
      ant messages create \
        --model claude-opus-5-5 \
        --max-tokens 1024 \
        --message '{role: user, content: "Hello, Claude"}'
      ```

      ```python Python
      from anthropic import AnthropicGoogleCloud

      client = AnthropicGoogleCloud()
      ```

      ```typescript TypeScript
      import { AnthropicGoogleCloud } from "@anthropic-ai/google-cloud-sdk";

      const client = new AnthropicGoogleCloud();
      ```

      ```csharp C#
      using Anthropic.GoogleCloud;

      var client = new AnthropicGoogleCloudClient();
      ```

      ```go Go
      import (
      	"context"

      	"github.com/anthropics/anthropic-sdk-go/v2"
      	"github.com/anthropics/anthropic-sdk-go/v2/googlecloud"
      )
      // ...
      	client, err := googlecloud.NewClient(context.Background(), googlecloud.ClientConfig{})
      	if err != nil {
      		panic(err)
      	}
      ```

      ```java Java
      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.googlecloud.backends.GoogleCloudBackend;

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.builder()
              .backend(GoogleCloudBackend.fromEnv())
              .build();
      }
      ```

      ```php PHP
      use Anthropic\GoogleCloud\Client;

      $client = new Client();
      ```

      ```ruby Ruby
      require "anthropic"

      client = Anthropic::GoogleCloudClient.new
      ```
    </CodeGroup>

    Klien baru membaca proyek dan ID workspace Anda dari variabel lingkungan yang Anda tetapkan di [Temukan ID workspace Anda](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id). Anda tidak meneruskannya saat membuat klien. Panggilan Messages API Anda tetap seperti semula, kecuali untuk ID model dan fitur pada langkah berikutnya.
  </Step>

  <Step title="Periksa ID model dan fitur">
    * **ID model:** Jika Anda menggunakan model yang lebih lama dari Claude 4.6, ganti `@` sebelum tanggal snapshot dalam ID-nya dengan tanda hubung. Misalnya, `claude-haiku-4-5@20251001` menjadi `claude-haiku-4-5-20251001`. Untuk model dan ID-nya, lihat [ID model API](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#api-model-ids).
    * **Fitur:** Periksa [Dukungan fitur](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#feature-support) untuk setiap fitur yang digunakan kode Anda.
    * **Lokasi:** Jika saat ini Anda menggunakan endpoint multi-region atau regional, periksa lokasi mana yang digunakan Claude Models on Google Cloud (Anthropic managed). Lihat [Resolusi proyek, lokasi, dan workspace](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution).
  </Step>

  <Step title="Jalankan permintaan uji">
    Jalankan permintaan di [Membuat permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#making-requests) untuk memeriksa bahwa penyiapan Anda berfungsi. Kemudian jalankan kode Anda sendiri. Jika panggilan gagal dengan kesalahan izin, lihat [Pemecahan masalah penyiapan akun](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#troubleshooting-account-setup). Sebelum Anda memindahkan lalu lintas produksi, periksa [batas laju untuk Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#rate-limits).
  </Step>
</Steps>

## Dukungan

[Dukungan Google Cloud](https://cloud.google.com/support) menangani akun, akses, dan penagihan Google Cloud Anda. [Dukungan Anthropic](https://support.claude.com/en/articles/9015913-how-to-get-support) menangani Claude itu sendiri, termasuk model, kesalahan API, dan batas laju. Untuk meminta batas laju yang lebih tinggi, lihat [Batas laju](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#rate-limits).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ikhtisar fitur" icon="stack" href="https://platform.claude.com/docs/id/build-with-claude/overview">
    Jelajahi fitur-fitur Claude.
  </Card>

  <Card title="Izin IAM" icon="lock" href="https://platform.claude.com/docs/id/api/claude-models-on-google-cloud-anthropic-managed-iam-permissions">
    Cari izin, peran, dan jenis log audit.
  </Card>

  <Card title="Penghentian model" icon="arrow-clockwise" href="https://platform.claude.com/docs/id/about-claude/model-deprecations">
    Seiring diluncurkannya model yang lebih aman dan lebih mumpuni, Anthropic secara berkala menghentikan model yang lebih lama. Lihat semua penghentian API, beserta pengganti yang direkomendasikan.
  </Card>

  <Card title="Google Cloud Marketplace" icon="coins" href="https://console.cloud.google.com/marketplace">
    Kelola langganan dan penagihan Anda.
  </Card>
</CardGroup>
