---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws
fetched_at: 2026-08-23T02:32:19.757524Z
sha256: 833a0387eb555d08a4501d27012cb300ba5ec9d98f6ae835723529d6f91bc680
---

---
title: Claude Platform on AWS
url: https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws
description: Akses kemampuan platform Claude secara penuh melalui AWS dengan infrastruktur yang dikelola Anthropic.
---

Claude Platform on AWS memberi Anda pengalaman platform Anthropic secara penuh, termasuk Messages API, Agent Skills, eksekusi kode, dan fitur beta, yang dapat diakses melalui akun AWS Anda. Berbeda dengan [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), di mana AWS mengoperasikan stack inferensi, Anthropic mengoperasikan Claude Platform on AWS. AWS menyediakan lapisan autentikasi (SigV4 atau kunci API), kontrol akses berbasis IAM, dan integrasi penagihan melalui AWS Marketplace.

<Note>
  SDK Anthropic mendukung Claude Platform on AWS.
</Note>

## Cara kerja integrasi platform

Model Claude berjalan di infrastruktur yang dikelola Anthropic. Ini adalah integrasi komersial untuk penagihan dan akses melalui AWS. Anthropic adalah pemroses data untuk input dan output inferensi. AWS memproses metadata penagihan dan identitas berdasarkan model marketplace. Pelanggan yang menggunakan Claude melalui Claude Platform on AWS tunduk pada [ketentuan penggunaan data](https://www.anthropic.com/legal) Anthropic.

Claude Platform on AWS memiliki karakteristik operasional berikut: data mungkin tidak berada di AWS, inferensi mungkin dirutekan ke cloud utama Anthropic, dan sublayanan dapat berubah tanpa pemberitahuan. Tetapkan parameter [`inference_geo`](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#data-residency) per permintaan untuk mengunci inferensi ke geografi tertentu.

Claude Platform on AWS mengikuti kebijakan retensi data yang sama dengan Claude API pihak pertama. Zero Data Retention (ZDR) tersedia berdasarkan permintaan. Hubungi perwakilan akun Anthropic Anda untuk mengaktifkannya bagi organisasi Anda.

## Claude Platform on AWS vs Amazon Bedrock

Kedua penawaran memungkinkan Anda menggunakan Claude melalui AWS, tetapi keduanya berbeda dalam arsitektur, permukaan API, dan ketersediaan fitur.

| Aspek                               | Claude Platform on AWS                                                                                                                                                           | [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) | [Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Siapa yang mengoperasikan stack** | Anthropic                                                                                                                                                                        | AWS                                                                                                        | AWS                                                                                                                               |
| **Permukaan API**                   | Claude API (`/v1/{endpoint}`)                                                                                                                                                    | Messages API di `/anthropic/v1/messages`                                                                   | Bedrock Converse / InvokeModel                                                                                                    |
| **Ketersediaan fitur**              | Biasanya pada hari yang sama dengan Claude API (lihat [keterbatasan fitur](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#features-not-supported)) | Sesuai jadwal rilis Amazon Bedrock                                                                         | Sesuai jadwal rilis Amazon Bedrock                                                                                                |
| **Agent Skills**                    | Tersedia (beta)                                                                                                                                                                  | Tidak tersedia (memerlukan eksekusi kode)                                                                  | Tidak tersedia                                                                                                                    |
| **Fitur beta**                      | Diteruskan dengan header `anthropic-beta` (lihat [keterbatasan fitur](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#features-not-supported))      | Header `anthropic-beta` tidak didukung                                                                     | Header `anthropic-beta` tidak didukung                                                                                            |
| **Autentikasi**                     | AWS IAM / SigV4 atau kunci API                                                                                                                                                   | AWS IAM / SigV4                                                                                            | AWS IAM / SigV4 atau bearer token                                                                                                 |
| **Penagihan**                       | AWS Marketplace                                                                                                                                                                  | AWS (layanan native)                                                                                       | AWS (layanan native)                                                                                                              |
| **Base URL**                        | `aws-external-anthropic.{region}.api.aws`                                                                                                                                        | `bedrock-mantle.{region}.api.aws`                                                                          | `bedrock-runtime.{region}.amazonaws.com`                                                                                          |
| **Klien SDK**                       | Kelas klien khusus platform (misalnya, `AnthropicAWS` di Python), dalam beta                                                                                                     | `AnthropicBedrockMantle`                                                                                   | `AnthropicBedrock` / Bedrock SDK                                                                                                  |
| **Konsol**                          | Claude Console (`platform.claude.com`, akses melalui AWS Console)                                                                                                                | Bedrock Console                                                                                            | Bedrock Console                                                                                                                   |
| **Batas laju dan kuota**            | Dikelola oleh Anthropic                                                                                                                                                          | Dikelola oleh AWS                                                                                          | Dikelola oleh AWS                                                                                                                 |
| **Pemroses data inferensi**         | Anthropic                                                                                                                                                                        | AWS                                                                                                        | AWS                                                                                                                               |

Jika Anda memerlukan Claude yang dioperasikan AWS, lihat [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock). Claude Platform on AWS menggunakan pool kapasitas yang terpisah dari Claude API pihak pertama maupun Amazon Bedrock. Anda dapat menjalankan beban kerja di lebih dari satu platform dan melakukan failover di antaranya.

[AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) didukung untuk menghubungkan VPC Anda ke endpoint Claude Platform on AWS.

**Kapan memilih Bedrock:** Organisasi di industri yang diregulasi yang memerlukan kepatuhan FedRAMP High, IL4, IL5, atau HIPAA-ready, atau yang memerlukan AWS sebagai satu-satunya pemroses data, sebaiknya menggunakan [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock). Bedrock berjalan sepenuhnya di infrastruktur yang dikendalikan AWS dengan AWS sebagai pihak yang mengoperasikan.

**Penawaran mana yang Anda gunakan?** Claude tersedia melalui beberapa produk yang berbeda:

* **Claude Platform on AWS** (halaman ini): Platform Claude API yang ditagih melalui AWS Marketplace. Dikelola di [Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console) dan AWS Console.
* **[Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock):** Layanan native AWS. Dikelola di konsol Amazon Bedrock dan ditagih sebagai penggunaan layanan AWS.
* **Claude Enterprise yang diperoleh melalui AWS Marketplace:** Paket [claude.ai](https://claude.ai) (produk chat Claude), bukan platform API. Dikelola di claude.ai, dan perilaku akun serta migrasinya berbeda dari yang dijelaskan halaman ini. Lihat [Pusat Bantuan Claude](https://support.claude.com).
* **Akun Anthropic langsung:** Claude API pihak pertama dan paket claude.ai yang ditagih oleh Anthropic. Dikelola di Claude Console dan di claude.ai.

## Menyiapkan akun Anda

Penyiapan Claude Platform on AWS berlangsung dalam empat fase: mendaftar di halaman layanan AWS Console, menyelesaikan penyiapan organisasi Anthropic Anda, mencatat ID workspace Anda, dan masuk ke Claude Console.

<Note>
  Mendaftar melalui AWS Console akan menyediakan organisasi Anthropic baru yang terikat dengan akun AWS Anda. Organisasi ini terpisah dari organisasi apa pun yang sudah dimiliki perusahaan Anda dengan Anthropic, termasuk organisasi Claude Enterprise yang diperoleh melalui AWS Marketplace. Kunci API, workspace, dan pengaturan Claude Console dari organisasi Anthropic pihak pertama tidak terbawa.

  Jika Anda memiliki private offer Amazon Bedrock yang sudah ada, hubungi perwakilan akun Anthropic atau AWS Anda sebelum mendaftar agar diskon Anda berlaku sejak permintaan pertama Anda. Diskon tidak dapat diterapkan secara retroaktif pada penggunaan yang terjadi sebelum private offer Anda diterima. Lihat [Private offer](https://platform.claude.com/docs/id/about-claude/pricing#private-offers).
</Note>

<Steps>
  <Step title="Mendaftar di AWS Console">
    1. Buka [AWS Console](https://console.aws.amazon.com/) dan navigasikan ke halaman layanan **Claude Platform on AWS**.
    2. Pilih **Sign up**.
    3. Di halaman Sign-up, tinjau ketentuannya (End User License Agreement Anthropic, AWS Privacy Notice, dan AWS Customer Agreement) lalu centang kotak persetujuan.
    4. Pilih **Continue**.

    Halaman menampilkan banner **Sign-up in progress**. Tetaplah di halaman tersebut. Pendaftaran memerlukan beberapa menit sementara AWS menangani langganan AWS Marketplace untuk Anda, lalu mengalihkan Anda secara otomatis.

    Jika organisasi Anda memiliki private offer dari Anthropic, Console akan mencarinya dan meminta Anda untuk menerimanya di AWS Marketplace. Lihat [Private offer](https://platform.claude.com/docs/id/about-claude/pricing#private-offers) untuk detailnya.

    <Note>
      Jika Anda menggunakan Claude Platform on AWS, konten Anda (seperti prompt dan completion) diproses oleh Anthropic di luar AWS. Lihat [kebijakan penggunaan data](https://www.anthropic.com/legal) Anthropic untuk detail tentang bagaimana konten dan metadata diproses dan disimpan.
    </Note>
  </Step>

  <Step title="Menyiapkan organisasi Anthropic Anda">
    Setelah pendaftaran selesai, Anda dialihkan ke `platform.claude.com/partner-signup`.

    1. Masukkan alamat email pemilik organisasi Anda dan pilih **Get started**.
    2. Periksa kotak masuk email tersebut untuk tautan penyiapan dan ikuti tautannya. Jika browser Anda menampilkan halaman **Signed in as a different account**, pilih **Log out and continue**.
    3. Lengkapi formulir detail organisasi (nama organisasi, jenis entitas, negara, tujuan penggunaan) dan pilih **Complete setup**.

    Menyelesaikan penyiapan akan membuat organisasi Anthropic Anda dan menerima Commercial Terms of Service serta Usage Policy Anthropic. Halaman layanan AWS Console kini menampilkan navigasi kiri dengan **Home**, **API keys**, **Quickstart**, dan **Workspaces**.
  </Step>

  <Step title="Membuat workspace Anda dan mencatat ID-nya">
    Setelah Anda menyelesaikan penyiapan, AWS Console meminta Anda membuat workspace. Lihat [Workspace](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#workspaces) untuk detail tentang pengikatan region, pelingkupan resource IAM, dan pembuatan workspace tambahan.

    Temukan ID workspace di bawah **Workspaces** pada halaman layanan **Claude Platform on AWS** di AWS Console atau di [Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console). ID workspace menggunakan format `wrkspc_` diikuti pengenal alfanumerik.
  </Step>

  <Step title="Masuk ke Claude Console">
    Akses ke Claude Console difederasikan melalui AWS IAM:

    1. Asumsikan IAM role dengan izin `aws-external-anthropic:AssumeConsole`. Lihat [Aksi IAM untuk Claude Platform on AWS](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#console-access).
    2. Dari halaman layanan **Claude Platform on AWS**, pilih **Open Claude Console**. AWS Console menerbitkan JWT dan mengalihkan Anda ke `platform.claude.com`.
    3. Pada saat masuk pertama kali, Anda diminta memasukkan alamat email. Masukkan email kerja Anda. Platform menyediakan pengguna Claude Console Anda secara just-in-time.

    Saat Anda masuk melalui AWS Console, Claude Console dilingkupkan ke organisasi Claude Platform on AWS Anda. Indikator **Account managed by AWS** muncul di kiri bawah sidebar Claude Console.
  </Step>
</Steps>

### Berpindah dari organisasi Anthropic yang sudah ada

Mendaftar ke Claude Platform on AWS selalu menyediakan organisasi Anthropic baru yang terikat dengan akun AWS Anda. Tidak ada konversi di tempat: organisasi yang sudah ada, seperti organisasi Claude API pihak pertama, tidak dapat menjadi organisasi Claude Platform on AWS.

Rencanakan perpindahan dari organisasi yang sudah ada sebagai cutover ke organisasi baru:

* **Buat organisasi baru terlebih dahulu.** Daftar melalui AWS Console (lihat [Menyiapkan akun Anda](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#set-up-your-account)). Jika perpindahan Anda melibatkan private offer, selesaikan pendaftaran sebelum offer diterima: diskon berlaku sejak penerimaan, tidak secara retroaktif. Lihat [Private offer](https://platform.claude.com/docs/id/about-claude/pricing#private-offers).
* **Buat ulang akses dan konfigurasi.** Kunci API, workspace, dan pengaturan Claude Console tidak terbawa dari organisasi yang sudah ada. Buat workspace di organisasi baru dan alihkan aplikasi Anda ke [autentikasi Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#authentication).
* **Perbarui integrasi Anda.** Claude Platform on AWS melayani Claude API (`/v1/{endpoint}`), sehingga bentuk permintaan dan respons tidak berubah dari Claude API pihak pertama. Yang berubah adalah base URL, metode autentikasi, dan header `anthropic-workspace-id` yang wajib; lihat [Membuat permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#making-requests). Beberapa fitur platform berbeda; lihat [Fitur yang tidak didukung](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#features-not-supported).
* **Lakukan cutover sesuai jadwal Anda sendiri.** Organisasi baru bersifat independen dari organisasi Anda yang sudah ada, dan keduanya dapat melayani lalu lintas secara paralel. Tidak perlu cutover keras: pindahkan beban kerja secara bertahap hingga seluruh lalu lintas Anda berada di organisasi baru.

Setelah organisasi baru berjalan, perbedaannya terkonsentrasi pada penagihan dan autentikasi, yang ditangani melalui AWS:

* **Penagihan** berpindah ke AWS Marketplace: penggunaan ditagih dalam Claude Consumption Units, bukan kredit prabayar (lihat [Penagihan](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#billing)), dan batas pengeluaran dikelola di halaman Billing, bukan halaman Limits (lihat [Batas pengeluaran](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#spend-limits)). Selama transisi, penagihan tetap terpisah: organisasi yang sudah ada terus ditagih seperti saat ini.
* **Autentikasi dan akses** berpindah ke AWS: permintaan diautentikasi dengan kredensial AWS atau dengan kunci API yang dibuat di AWS Console, bukan Claude Console (lihat [Autentikasi](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#authentication)). Keanggotaan organisasi dikelola melalui AWS IAM, bukan Claude Console (lihat [Halaman yang tersedia](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#available-pages)), dan SDK klien Anthropic menyediakan kelas klien khusus platform (lihat [Menginstal SDK](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#install-an-sdk)).
* **Penggunaan API sehari-hari** bekerja seperti pada Claude API pihak pertama, kecuali jika disebutkan dalam [keterbatasan fitur](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#features-not-supported). Sebelum memindahkan lalu lintas produksi, periksa batas laju Anda: organisasi baru ditempatkan pada tier Start, dan peningkatan batas dilakukan melalui perwakilan akun Anthropic Anda (lihat [Batas laju dan kuota](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas)).

Untuk organisasi Claude Enterprise (claude.ai), yang berperilaku berbeda, lihat [perbandingan penawaran](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#claude-platform-on-aws-vs-amazon-bedrock).

### Pemecahan masalah penyiapan akun

* **"Sign-up failed: Failed to enable OutboundWebIdentityFederation":** Jika Anda melihat banner ini pada pengiriman pertama, pilih **Continue** lagi. Pengaktifan IAM dapat memerlukan waktu sejenak untuk berlaku.
* **Tidak ada indikator progres selama pendaftaran:** Pendaftaran memerlukan beberapa menit. Halaman menampilkan banner statis **Sign-up in progress** tanpa bilah progres sementara AWS menyediakan akun Anda.
* **"Signed in as a different account" setelah mengikuti tautan penyiapan:** Pilih **Log out and continue**. Halaman mengautentikasi ulang Anda dengan alamat email yang Anda masukkan.
* **Pesan "Not found" saat masuk:** Pesan ini mungkin muncul sebentar selama pengalihan. Anda dapat mengabaikannya.
* **Halaman Usage tidak menampilkan data setelah panggilan API pertama Anda:** Data penggunaan dapat memerlukan beberapa menit untuk muncul di Claude Console.
* **"Outbound web identity federation is disabled" pada panggilan API pertama Anda:** Aktifkan federasi sekali per akun. Lihat [Mengaktifkan outbound web identity federation](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#enable-outbound-web-identity-federation).

## Sebelum melakukan panggilan API

Pastikan Anda memiliki:

1. Akun AWS aktif dengan langganan Claude Platform on AWS (lihat [Menyiapkan akun Anda](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#set-up-your-account))
2. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) yang terinstal dan terkonfigurasi
3. **Outbound web identity federation yang diaktifkan** di akun AWS Anda, langkah penyiapan satu kali (lihat [Mengaktifkan outbound web identity federation](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#enable-outbound-web-identity-federation))
4. ID workspace Anda (lihat [Mendapatkan ID workspace Anda](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#obtain-your-workspace-id))
5. Izin IAM untuk memanggil API: aksi `aws-external-anthropic:CreateInference` pada workspace Anda, ditambah `aws-external-anthropic:CallWithBearerToken` jika Anda mengautentikasi dengan kunci API (lihat [Kebijakan IAM](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#iam-policies))

### Mengaktifkan outbound web identity federation

Gateway Claude Platform on AWS memanggil `sts:GetWebIdentityToken` di sisi server untuk mencetak JWT yang diteruskannya ke Anthropic. Kemampuan STS ini **dinonaktifkan secara default** di setiap akun AWS. Aktifkan sekali per akun:

```bash CLI
aws iam enable-outbound-web-identity-federation
```

Jika responsnya adalah `[ERROR] (FeatureEnabled) ... already enabled`, pengaturan tersebut sudah aktif untuk akun Anda dan Anda dapat melanjutkan. Verifikasi dan ambil URL issuer akun Anda:

```bash CLI
aws iam get-outbound-web-identity-federation-info
```

<Warning>
  Tanpa langkah ini, setiap permintaan mengembalikan `"Outbound web identity federation is disabled for your account"`. Ini adalah kesalahan penyiapan yang paling umum.
</Warning>

### Mendapatkan ID workspace Anda

Anda membuat workspace dari AWS Console setelah menyelesaikan penyiapan akun (lihat [Menyiapkan akun Anda](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#set-up-your-account)). Workspace terikat pada satu region AWS. Anda dapat menemukan ID workspace di [Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console) di bawah **Workspaces** atau di bagian **Workspaces** pada halaman layanan AWS Console.

Tetapkan variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID` dan `AWS_REGION` agar klien SDK membacanya secara otomatis:

```bash CLI
export ANTHROPIC_AWS_WORKSPACE_ID='wrkspc_01AbCdEf23GhIj'
export AWS_REGION='us-west-2'  # Your workspace's AWS region
```

Region wajib diisi. Klien SDK memunculkan error jika tidak ada region yang ditetapkan. Teruskan `aws_region`/`awsRegion` ke konstruktor, atau tetapkan `AWS_REGION` (atau `AWS_DEFAULT_REGION`). Semua region komersial AWS didukung.

## Autentikasi

Claude Platform on AWS mendukung dua metode autentikasi: AWS IAM dengan penandatanganan permintaan Signature Version 4 (SigV4) (utama) dan autentikasi kunci API. Keduanya menggunakan base URL dan format permintaan yang sama.

### Autentikasi SigV4

SigV4 adalah jalur native enterprise dan terintegrasi dengan kebijakan, role, dan audit AWS IAM Anda yang sudah ada. Konfigurasikan kredensial AWS menggunakan metode apa pun yang didukung oleh [rantai penyedia kredensial default AWS](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html):

* Variabel lingkungan (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`)
* File kredensial bersama (`~/.aws/credentials`)
* File konfigurasi bersama (`~/.aws/config`) termasuk SSO dan `credential_process`
* Web identity (`AWS_WEB_IDENTITY_TOKEN_FILE` dan `AWS_ROLE_ARN`) untuk IRSA dan GitHub Actions
* Kredensial container ECS
* Layanan metadata instance EC2 (IMDS)

Verifikasi bahwa kredensial Anda berfungsi:

```bash CLI
aws sts get-caller-identity
```

### Autentikasi kunci API

Untuk jalur integrasi yang lebih sederhana (pengembangan lokal dan skrip), Anda dapat mengautentikasi dengan kunci API alih-alih SigV4. Tetapkan variabel lingkungan `ANTHROPIC_AWS_API_KEY` atau teruskan `apiKey` ke konstruktor SDK.

Buat kunci API di **AWS Console** di bawah **Claude Platform on AWS → API keys**. Pilih **Generate a key**, lalu salin nilai kuncinya. Berikan aksi IAM `aws-external-anthropic:CallWithBearerToken` kepada principal yang diizinkan menggunakan autentikasi kunci API.

<Note>
  Kunci API untuk Claude Platform on AWS dikelola di AWS Console, bukan Claude Console. Kunci yang dibuat di [Claude Console](https://platform.claude.com/) standar (untuk akses API pihak pertama) tidak berfungsi dengan endpoint Claude Platform on AWS.
</Note>

#### Kunci API jangka pendek

Untuk beban kerja yang perlu menyerahkan kredensial ke proses terpisah (seperti gateway LLM, fungsi serverless, atau alat yang mendukung autentikasi bearer-token tetapi tidak SigV4), buat kunci API jangka pendek dari kredensial AWS Anda alih-alih menyediakan kunci berumur panjang di AWS Console.

AWS menerbitkan library token-generator untuk [JavaScript](https://github.com/aws/token-generator-for-aws-external-anthropic-js), [Python](https://github.com/aws/token-generator-for-aws-external-anthropic-python), dan [Java](https://github.com/aws/token-generator-for-aws-external-anthropic-java). Setiap library membaca kredensial AWS Anda melalui rantai penyedia standar dan mengembalikan token berbatas waktu yang berfungsi dengan header `x-api-key`. Masa berlaku token secara default adalah 12 jam dan dibatasi pada nilai terkecil di antara durasi yang Anda minta, masa kedaluwarsa kredensial AWS Anda, dan 12 jam. Lihat README repositori yang ditautkan untuk instalasi dan opsi konfigurasi lengkap.

Teruskan token yang dihasilkan ke SDK dengan cara yang sama seperti Anda meneruskan kunci API yang dibuat di AWS Console:

<CodeGroup exclude="shell, csharp, go, php, ruby">
  ```python Python
  from token_generator_for_aws_external_anthropic import TokenGenerator
  from anthropic import AnthropicAWS

  token = TokenGenerator(region="us-west-2").get_token()

  client = AnthropicAWS(api_key=token, aws_region="us-west-2")
  ```

  ```typescript TypeScript
  import { getTokenProvider } from "@aws/token-generator-for-aws-external-anthropic";
  import AnthropicAws from "@anthropic-ai/aws-sdk";

  const tokenProvider = getTokenProvider({ region: "us-west-2" });
  const token = await tokenProvider();

  const client = new AnthropicAws({ apiKey: token, awsRegion: "us-west-2" });
  ```

  ```java Java
  import software.amazon.awsexternalanthropic.TokenGenerator;
  import software.amazon.awssdk.regions.Region;
  import com.anthropic.aws.backends.AwsBackend;
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;

  void main() {
      String token = TokenGenerator.builder().region(Region.US_WEST_2).build().getToken();

      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(AwsBackend.builder()
              .apiKey(token)
              .region(Region.US_WEST_2)
              .workspaceId(System.getenv("ANTHROPIC_AWS_WORKSPACE_ID"))
              .build())
          .build();
  }
  ```
</CodeGroup>

Jika Anda dapat membuat token secara lokal, proses Anda sudah memiliki kredensial SigV4, dan autentikasi SigV4 biasanya merupakan pilihan yang lebih sederhana. Gunakan kunci jangka pendek ketika proses yang melakukan panggilan API terpisah dari proses yang memegang kredensial AWS.

SDK tidak memperbarui kunci jangka pendek secara otomatis. Ketika token kedaluwarsa, buat token baru dan buat klien baru. Principal yang menggunakan token tetap memerlukan aksi IAM `aws-external-anthropic:CallWithBearerToken`.

### Prioritas kredensial

Klien khusus platform menyelesaikan autentikasi dalam urutan berikut. Nama argumen bervariasi menurut konvensi bahasa: TypeScript dan PHP menggunakan camelCase seperti yang ditunjukkan, Python dan Ruby menggunakan snake\_case, Go menggunakan PascalCase dengan akronim berhuruf kapital, dan C# serta Java menggunakan idiom properti atau builder bahasa tersebut.

1. Argumen konstruktor `apiKey` → header `x-api-key`
2. Argumen konstruktor `awsAccessKey` + `awsSecretAccessKey` → AWS SigV4
3. Argumen konstruktor `awsProfile` → AWS SigV4 dengan profil bernama
4. Variabel lingkungan `ANTHROPIC_AWS_API_KEY` → header `x-api-key`
5. Rantai penyedia kredensial default AWS → AWS SigV4

### Resolusi region

Klien membaca `AWS_REGION` dari lingkungan jika `aws_region`/`awsRegion` tidak diteruskan ke konstruktor, dengan fallback ke `AWS_DEFAULT_REGION` untuk kompatibilitas dengan AWS SDK standar. Region wajib diisi. Tidak ada default fallback. Berbeda dengan `AnthropicBedrock`, yang melakukan fallback ke `us-east-1`, klien `AnthropicAWS`/`AnthropicAws` memunculkan error jika argumen konstruktor maupun variabel lingkungan tidak ditetapkan.

## Menginstal SDK

[SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) Anthropic mendukung Claude Platform on AWS. Setiap SDK menyediakan kelas klien khusus platform yang menangani penandatanganan SigV4, konstruksi base URL berbasis region, dan header `anthropic-workspace-id`.

<Tabs>
  <Tab title="Python">
    ```bash
    pip install -U "anthropic[aws]"
    ```

    <Tip>
      Di macOS dengan Python Homebrew atau lingkungan Python lain yang dikelola secara eksternal, `pip install` dapat gagal dengan error PEP 668 `externally-managed-environment`. Buat dan aktifkan virtual environment terlebih dahulu: `python3 -m venv .venv && source .venv/bin/activate`.
    </Tip>
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/aws-sdk
    ```
  </Tab>

  <Tab title="C#">
    ```bash
    dotnet add package Anthropic.Aws
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    go get github.com/anthropics/anthropic-sdk-go
    ```
  </Tab>

  <Tab title="Java">
    ```kotlin Gradle
    implementation("com.anthropic:anthropic-java-aws:2.57.0")
    ```

    ```xml Maven
    <dependency>
      <groupId>com.anthropic</groupId>
      <artifactId>anthropic-java-aws</artifactId>
      <version>2.57.0</version>
    </dependency>
    ```
  </Tab>

  <Tab title="PHP">
    ```bash
    composer require anthropic-ai/sdk aws/aws-sdk-php
    ```
  </Tab>

  <Tab title="Ruby">
    ```bash
    gem install anthropic aws-sdk-core
    ```
  </Tab>
</Tabs>

<Note>
  Klien SDK untuk Claude Platform on AWS berada dalam beta.
</Note>

## Model yang tersedia

Model berikut tersedia di Claude Platform on AWS:

| Model             | ID Model          |
| ----------------- | ----------------- |
| Claude Fable 5    | claude-fable-5    |
| Claude Opus 4.8   | claude-opus-4-8   |
| Claude Opus 4.7   | claude-opus-4-7   |
| Claude Opus 4.6   | claude-opus-4-6   |
| Claude Sonnet 5   | claude-sonnet-5   |
| Claude Sonnet 4.6 | claude-sonnet-4-6 |
| Claude Opus 4.5   | claude-opus-4-5   |
| Claude Sonnet 4.5 | claude-sonnet-4-5 |
| Claude Haiku 4.5  | claude-haiku-4-5  |

ID model identik dengan Claude API pihak pertama. Tidak ada ARN bergaya Bedrock atau prefiks `anthropic.`.

Model baru biasanya diluncurkan di Claude Platform on AWS pada hari yang sama dengan Claude API pihak pertama.

<Tip>
  Melakukan upgrade ke model Claude yang lebih baru? Di Claude Code, jalankan `/claude-api migrate` untuk menerapkan penggantian ID model dan perubahan parameter yang bersifat breaking di seluruh codebase Anda. Skill ini mendeteksi platform cloud mana yang ditargetkan oleh kode Anda dan menyesuaikan format ID model serta perubahan fitur untuk platform tersebut. Lihat [Migrasi ke model Claude yang lebih baru](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

## Membuat permintaan

Claude Platform on AWS menggunakan endpoint API yang sama dengan Claude API pihak pertama. Perbedaannya adalah base URL, metode autentikasi, dan header `anthropic-workspace-id` wajib yang mengidentifikasi [workspace](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#workspaces) mana yang menjadi target permintaan.

Sebelum menjalankan contoh-contoh ini, selesaikan langkah-langkah di [Sebelum melakukan panggilan API](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#before-making-api-calls).

<CodeGroup>
  ```bash cURL
  # Ganti us-west-2 dengan region AWS Anda di URL dan --aws-sigv4
  # Hilangkan header x-amz-security-token jika Anda menggunakan kredensial pengguna IAM jangka panjang
  curl "https://aws-external-anthropic.us-west-2.api.aws/v1/messages" \
    --aws-sigv4 "aws:amz:us-west-2:aws-external-anthropic" \
    --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
    -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
    -H "content-type: application/json" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-workspace-id: $ANTHROPIC_AWS_WORKSPACE_ID" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    }'
  ```

  ```bash CLI
  # Ganti us-west-2 dengan region AWS Anda
  # ant membaca ANTHROPIC_API_KEY dan mengirimkannya sebagai x-api-key. Buat kunci di
  # AWS Console (lihat autentikasi kunci API).
  export ANTHROPIC_API_KEY="YOUR_AWS_API_KEY"

  ant messages create \
    --base-url https://aws-external-anthropic.us-west-2.api.aws \
    --workspace-id "$ANTHROPIC_AWS_WORKSPACE_ID" \
    --model claude-sonnet-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello!"}' \
    --transform content
  ```

  ```python Python
  from anthropic import AnthropicAWS

  client = AnthropicAWS()

  message = client.messages.create(
      model="claude-sonnet-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  )
  print(message)
  ```

  ```typescript TypeScript
  import AnthropicAws from "@anthropic-ai/aws-sdk";

  const client = new AnthropicAws();

  const message = await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  });
  console.log(message);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Aws;

  var client = new AnthropicAwsClient();

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }]
  });

  Console.WriteLine(message);
  ```

  ```go Go
  client, err := anthropicaws.NewClient(context.Background(), anthropicaws.ClientConfig{})
  if err != nil {
  	panic(err)
  }

  message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Println(message)
  ```

  ```java Java
  import com.anthropic.aws.backends.AwsBackend;
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(AwsBackend.fromEnv())
          .build();

      Message message = client.messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_5)
              .maxTokens(1024)
              .addUserMessage("Hello!")
              .build()
      );

      IO.println(message);
  }
  ```

  ```php PHP
  use Anthropic\Aws\Client;

  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-sonnet-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello!']],
  );

  echo $message;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::AWSClient.new

  message = client.messages.create(
    model: "claude-sonnet-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  )

  puts message
  ```
</CodeGroup>

Klien membaca `AWS_REGION` (atau `AWS_DEFAULT_REGION`) dan `ANTHROPIC_AWS_WORKSPACE_ID` dari lingkungan. Anda dapat menimpa salah satunya dengan meneruskan `aws_region` / `awsRegion` atau `workspace_id` / `workspaceId` ke konstruktor. Region dan ID workspace keduanya wajib. Konstruktor memunculkan error jika salah satunya tidak dapat diselesaikan.

<Note>
  Header `x-amz-security-token` (cURL) hanya diperlukan untuk kredensial sementara seperti IAM role, SSO, atau STS. Hilangkan header ini saat menggunakan kredensial pengguna IAM jangka panjang. Klien SDK menangani hal ini secara otomatis berdasarkan sumber kredensial.
</Note>

Nilai `--aws-sigv4` mengikuti format `aws:amz:<region>:<service>`. Nama layanan SigV4 adalah `aws-external-anthropic`, dan region harus cocok dengan region di URL endpoint Anda. Ketidakcocokan pada salah satunya menghasilkan error penolakan tanda tangan generik, bukan diagnostik yang spesifik.

### Jendela konteks

Ukuran "context window" (jendela konteks) di Claude Platform on AWS identik dengan Claude API pihak pertama. Lihat [Jendela konteks](https://platform.claude.com/docs/id/build-with-claude/context-windows) untuk batas per model.

## Dukungan fitur

Claude Platform on AWS menggunakan endpoint Claude API secara langsung, yang berarti Anda mendapatkan paritas fitur penuh dengan Claude API pihak pertama (kecuali jika disebutkan dalam [keterbatasan fitur](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#features-not-supported)):

* **Akses fitur:** Karena Anthropic mengoperasikan kedua platform, sebagian besar fitur baru dan header beta tersedia di Claude Platform on AWS tanpa langkah integrasi terpisah. Lihat [keterbatasan fitur](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#features-not-supported) untuk pengecualian.
* **Fitur beta:** Teruskan header `anthropic-beta` standar untuk mengakses fitur beta, sama seperti yang Anda lakukan dengan Claude API.
* **Agent Skills:** Gunakan [Agent Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview) bawaan dan kustom dengan parameter `container.skills` yang sama seperti Claude API. Semua Skills bawaan (PowerPoint, Excel, Word, PDF) langsung berfungsi.
* **Eksekusi kode:** Jalankan kode di sandbox terkelola Anthropic menggunakan [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool).
* **Penggunaan alat:** Computer use dan semua [kemampuan "tool use" (penggunaan alat)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) lainnya tersedia.
* **Pemikiran diperpanjang:** Aktifkan "extended thinking" (pemikiran diperpanjang) dengan parameter yang sama seperti Claude API.
* **Streaming:** Dukungan streaming SSE penuh untuk respons real-time.
* **Pemrosesan batch:** Kirim permintaan batch untuk beban kerja throughput tinggi.
* **Caching prompt:** Cache alat, prompt sistem, dan riwayat pesan untuk mengurangi latensi dan biaya. Semua kemampuan "prompt caching" (caching prompt) (TTL 5 menit, TTL 1 jam, dan caching otomatis) tersedia.
* **Files API:** Unggah dan referensikan file di berbagai permintaan.
* **Customer-managed encryption keys (CMEK):** [CMEK](https://platform.claude.com/docs/id/manage-claude/cmek) tersedia hanya dengan kunci [AWS KMS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms). Kunci Google Cloud KMS dan Azure Key Vault tidak dapat didaftarkan. Buat, validasi, dan lampirkan kunci di [Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console). Endpoint Admin API `external_keys` saat ini tidak tersedia. Kunci harus berada di region AWS yang sama dengan workspace tempat kunci tersebut dilampirkan.
* **Compliance API:** [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) tersedia. Akses diotorisasi melalui [aksi `ListComplianceActivities`](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#compliance) AWS IAM.

Lihat [tabel perbandingan](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#claude-platform-on-aws-vs-amazon-bedrock) untuk perbedaan ketersediaan fitur dari Amazon Bedrock.

### Claude Managed Agents

[Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) tersedia di Claude Platform on AWS, termasuk [agen](https://platform.claude.com/docs/id/managed-agents/agent-setup), [environment](https://platform.claude.com/docs/id/managed-agents/environments), [sesi](https://platform.claude.com/docs/id/managed-agents/sessions), [credential vault](https://platform.claude.com/docs/id/managed-agents/vaults), [memory store](https://platform.claude.com/docs/id/managed-agents/memory), [webhook](https://platform.claude.com/docs/id/managed-agents/webhooks), [orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), dan [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes).

Perilaku sesi di Claude Platform on AWS berbeda dari Claude Managed Agents pihak pertama dalam satu hal:

* **Autentikasi ulang sesi otonom:** Sebuah sesi dapat berjalan secara otonom, tanpa [event pengguna](https://platform.claude.com/docs/id/managed-agents/reference#event-types) apa pun, hingga 6 jam. Setelah 6 jam, sesi memerlukan autentikasi ulang sebelum berlanjut. Untuk mengautentikasi ulang, kirim event user-role apa pun ke sesi tersebut (lihat [Event dan streaming](https://platform.claude.com/docs/id/managed-agents/events-and-streaming)). Claude Managed Agents pihak pertama tidak memiliki batas waktu berjalan untuk sesi otonom.

### Fitur yang tidak didukung

Kemampuan berikut saat ini tidak tersedia di Claude Platform on AWS:

* **Kesiapan HIPAA:** Program HIPAA-ready Anthropic tidak tersedia. Lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

- **Admin API:** Endpoint workspace (create, get, list, update, dan archive pada `/v1/organizations/workspaces`) tersedia. Endpoint Admin API lainnya (anggota organisasi, anggota workspace, undangan, kunci API, laporan penggunaan, laporan biaya, laporan batas laju, dan external keys) saat ini tidak tersedia. Kelola kunci [CMEK](https://platform.claude.com/docs/id/manage-claude/cmek) di Claude Console sebagai gantinya. Lihat data penggunaan dan biaya di [Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console) sebagai gantinya. AWS IAM mengelola keanggotaan organisasi.
- **Manajemen anggota workspace:** Menambahkan atau menghapus pengguna dari workspace individual tidak tersedia. Kebijakan AWS IAM pada ARN workspace mengontrol akses.
- **Workspace Claude Code dan Analytics API:** Workspace Claude Code dengan batas laju otomatis tidak tersedia. Penggunaan Claude Code muncul di tampilan penggunaan umum, bukan di layar khusus.
- **Autentikasi OAuth:** Tidak didukung. Gunakan autentikasi SigV4 atau kunci API.
- **Fast mode:** Tidak tersedia di Claude Platform on AWS.
- **Endpoint API yang kompatibel dengan OpenAI:** Tidak tersedia di Claude Platform on AWS.
- **MCP tunnel:** Hanya server MCP yang diekspos melalui internet publik yang didukung.

## Residensi data

Claude Platform on AWS mendukung geografi inferensi berikut:

* **US:** Inferensi tetap berada di dalam pusat data AS. Berlaku pengali harga 1,1x.
* **Global:** Inferensi dapat dirutekan ke pusat data mana pun yang dioperasikan Anthropic di seluruh dunia. Berlaku harga standar.

<Note>
  Region AWS tempat workspace Anda terikat mengontrol endpoint gateway mana yang Anda panggil dan di mana sumber daya sisi AWS (IAM, CloudTrail, penagihan) dicakup. Region tersebut tidak menetapkan di mana inferensi model dijalankan. Untuk menetapkan inferensi ke geografi tertentu, atur `inference_geo` pada setiap permintaan atau konfigurasikan default workspace.
</Note>

Atur geografi inferensi per permintaan dengan parameter `inference_geo`:

<Note>
  Parameter `inference_geo` didukung pada model Claude 4.6 dan yang lebih baru. Permintaan dengan `inference_geo` pada Claude Opus 4.5, Claude Sonnet 4.5, atau Claude Haiku 4.5 mengembalikan error 400. Lihat [Residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency) untuk detail ketersediaan model.
</Note>

<CodeGroup>
  ```bash cURL
  # Ganti us-west-2 dengan region AWS Anda di URL dan --aws-sigv4
  # Hilangkan header x-amz-security-token jika Anda menggunakan kredensial pengguna IAM jangka panjang
  curl "https://aws-external-anthropic.us-west-2.api.aws/v1/messages" \
    --aws-sigv4 "aws:amz:us-west-2:aws-external-anthropic" \
    --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
    -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
    -H "content-type: application/json" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-workspace-id: $ANTHROPIC_AWS_WORKSPACE_ID" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 1024,
      "inference_geo": "us",
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    }'
  ```

  ```bash CLI
  # Ganti us-west-2 dengan region AWS Anda
  # ant membaca ANTHROPIC_API_KEY dan mengirimkannya sebagai x-api-key. Buat kunci di
  # AWS Console (lihat autentikasi kunci API).
  export ANTHROPIC_API_KEY="YOUR_AWS_API_KEY"

  ant messages create \
    --base-url https://aws-external-anthropic.us-west-2.api.aws \
    --workspace-id "$ANTHROPIC_AWS_WORKSPACE_ID" \
    --model claude-sonnet-5 \
    --max-tokens 1024 \
    --inference-geo us \
    --message '{role: user, content: "Hello!"}' \
    --transform content
  ```

  ```python Python
  from anthropic import AnthropicAWS

  client = AnthropicAWS()
  message = client.messages.create(
      model="claude-sonnet-5",
      max_tokens=1024,
      inference_geo="us",
      messages=[{"role": "user", "content": "Hello!"}],
  )
  print(message)
  ```

  ```typescript TypeScript
  import AnthropicAws from "@anthropic-ai/aws-sdk";
  const client = new AnthropicAws();
  const message = await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 1024,
    inference_geo: "us",
    messages: [{ role: "user", content: "Hello!" }]
  });
  console.log(message);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Aws;

  var client = new AnthropicAwsClient();

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 1024,
      InferenceGeo = "us",
      Messages = [new() { Role = Role.User, Content = "Hello!" }]
  });

  Console.WriteLine(message);
  ```

  ```go Go
  client, err := anthropicaws.NewClient(context.Background(), anthropicaws.ClientConfig{})
  if err != nil {
  	panic(err)
  }

  message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:        anthropic.ModelClaudeSonnet5,
  	MaxTokens:    1024,
  	InferenceGeo: anthropic.String("us"),
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Println(message)
  ```

  ```java Java
  import com.anthropic.aws.backends.AwsBackend;
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(AwsBackend.fromEnv())
          .build();

      Message message = client.messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_5)
              .maxTokens(1024)
              .inferenceGeo("us")
              .addUserMessage("Hello!")
              .build()
      );

      IO.println(message);
  }
  ```

  ```php PHP
  use Anthropic\Aws\Client;

  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-sonnet-5',
      maxTokens: 1024,
      inferenceGeo: 'us',
      messages: [['role' => 'user', 'content' => 'Hello!']],
  );

  echo $message;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::AWSClient.new

  message = client.messages.create(
    model: "claude-sonnet-5",
    max_tokens: 1024,
    inference_geo: "us",
    messages: [{ role: "user", content: "Hello!" }]
  )

  puts message
  ```
</CodeGroup>

Jika Anda menghilangkan `inference_geo`, permintaan menggunakan `default_inference_geo` milik workspace jika telah dikonfigurasi, jika tidak maka `global`.

Kontrol geografi inferensi tingkat workspace (`allowed_inference_geos` dan `default_inference_geo`) juga tersedia di Claude Platform on AWS. Lihat [Pembatasan tingkat workspace](https://platform.claude.com/docs/id/manage-claude/data-residency#workspace-level-restrictions).

## Workspace

Permintaan inferensi dan sumber daya di Claude Platform on AWS menargetkan sebuah workspace. Anda meneruskan ID workspace dalam header `anthropic-workspace-id` pada panggilan API ini. ID workspace menggunakan format bertag `wrkspc_` diikuti pengenal alfanumerik (misalnya, `wrkspc_01AbCdEf23GhIj`). Lihat [Dapatkan ID workspace Anda](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#obtain-your-workspace-id) jika Anda belum memilikinya.

### Cakupan workspace

Workspace terikat pada satu region AWS. Workspace yang dibuat di `us-west-2` hanya dapat diakses melalui endpoint `us-west-2`. Penggunaan, kuota, biaya, file, batch, dan Skills semuanya diakumulasikan per workspace, sehingga memberi Anda rincian per region di Claude Console.

Workspace juga berfungsi sebagai sumber daya IAM utama untuk Claude Platform on AWS. Anda memberikan atau menolak akses ke workspace tertentu melalui kebijakan AWS IAM menggunakan ARN workspace. Segmen sumber daya pada ARN adalah ID berawalan `wrkspc_` yang sama dengan yang Anda teruskan dalam header `anthropic-workspace-id`:

```text wrap
arn:aws:aws-external-anthropic:{region}:{account-id}:workspace/{workspace-id}
```

Sebagai contoh:

```text wrap
arn:aws:aws-external-anthropic:us-west-2:123456789012:workspace/wrkspc_01AbCdEf23GhIj
```

Lihat [Kebijakan IAM](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#iam-policies) untuk contoh kebijakan.

### Mengelola workspace

Buat workspace tambahan, ubah nama workspace, atau arsipkan workspace dari halaman **Workspaces** di AWS Console atau dengan endpoint workspace [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api). Workspace baru terikat pada region AWS dari endpoint yang Anda panggil untuk membuatnya (lihat [Cakupan workspace](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#workspace-scoping)). Halaman Workspaces di Claude Console bersifat hanya-baca.

## Menggunakan Claude Console

Claude Platform on AWS menggunakan Claude Console standar di [platform.claude.com](https://platform.claude.com). Saat Anda masuk dari AWS Console, indikator **Account managed by AWS** muncul di kiri bawah sidebar Claude Console dan Console dicakup ke organisasi Claude Platform on AWS Anda. Console menyediakan analitik penggunaan, rincian biaya, visibilitas batas laju, visibilitas workspace, serta halaman untuk mengelola file, Agent Skills, pekerjaan batch, dan sumber daya Claude Managed Agents (agen, sesi, lingkungan, credential vault, memory store, dan webhook).

### Masuk

Akses ke Claude Console difederasikan melalui AWS IAM. Lihat [Siapkan akun Anda](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#set-up-your-account) untuk alur masuk pertama kali secara lengkap. Singkatnya:

1. Asumsikan peran IAM dengan izin `aws-external-anthropic:AssumeConsole`. Lihat [Aksi IAM untuk Claude Platform on AWS](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#console-access).
2. Buka halaman Claude Platform on AWS di [AWS Console](https://console.aws.amazon.com/).
3. Pilih **Open Claude Console**. AWS Console menerbitkan JWT dan mengarahkan Anda ke `platform.claude.com`.
4. Pada saat masuk pertama kali, Anda diminta memasukkan alamat email. Masukkan email kerja Anda. Platform menyediakan pengguna Claude Console Anda secara just-in-time.

Tersedia dua peran Claude Console: **Admin** dan **Developer**. Peran Admin memberikan akses ke semua halaman dan pengaturan Claude Console yang tersedia untuk Claude Platform on AWS. Peran Developer memberikan akses baca ke informasi penggunaan, biaya, batas laju, dan workspace. Hubungi perwakilan akun Anthropic Anda untuk menetapkan peran Admin atau Developer kepada suatu principal.

### Halaman yang tersedia

Kolom **Melalui gateway AWS** menunjukkan apakah halaman tersebut membaca dan menulis data melalui gateway AWS (dan karenanya diatur oleh [aksi IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions)). Halaman yang ditandai **Tidak** membaca metadata tingkat organisasi langsung dari Anthropic dan melewati pemeriksaan aksi IAM.

| Halaman               | Tersedia      | Melalui gateway AWS | Catatan                                                                                                                                                                                                                                           |
| --------------------- | ------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usage**             | Ya            | Tidak               | Lihat penggunaan token berdasarkan model, workspace, dan dimensi. Data dapat memerlukan beberapa menit untuk muncul setelah permintaan.                                                                                                           |
| **Cost**              | Ya            | Tidak               | Lihat rincian biaya berdasarkan model dan workspace. AWS Cost Explorer menampilkan item baris [Claude Consumption Unit (CCU)](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#billing) yang diagregasi.              |
| **Rate limits**       | Ya            | Tidak               | Lihat batas laju (hanya-baca). Kenaikan tier dilakukan melalui perwakilan akun Anthropic Anda; lihat [Batas laju dan kuota](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas).                 |
| **Workspaces**        | Ya            | Tidak               | Lihat workspace per region (hanya-baca).                                                                                                                                                                                                          |
| **Files**             | Ya            | Ya                  | Lihat dan kelola file yang diunggah.                                                                                                                                                                                                              |
| **Skills**            | Ya            | Ya                  | Lihat dan kelola Agent Skills.                                                                                                                                                                                                                    |
| **Batches**           | Ya            | Ya                  | Lihat dan kelola pekerjaan pemrosesan batch.                                                                                                                                                                                                      |
| **Agents**            | Ya            | Ya                  | Lihat dan kelola definisi agen.                                                                                                                                                                                                                   |
| **Sessions**          | Ya            | Ya                  | Lihat sesi agen dan riwayat event.                                                                                                                                                                                                                |
| **Environments**      | Ya            | Ya                  | Lihat dan kelola konfigurasi sandbox cloud untuk sesi.                                                                                                                                                                                            |
| **Credential vaults** | Ya            | Ya                  | Lihat dan kelola credential vault untuk autentikasi sesi.                                                                                                                                                                                         |
| **Memory stores**     | Ya            | Ya                  | Lihat dan kelola memori agen persisten.                                                                                                                                                                                                           |
| **Webhooks**          | Ya            | Ya                  | Lihat dan kelola endpoint webhook di bawah **Settings → Webhooks**.                                                                                                                                                                               |
| **API keys**          | Tidak         | N/A                 | Kelola kunci API di AWS Console (**Claude Platform on AWS → API keys**). Lihat [Autentikasi kunci API](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#api-key-authentication).                                      |
| **Members**           | Tidak         | N/A                 | Tidak berlaku. AWS IAM mengelola akses.                                                                                                                                                                                                           |
| **Billing**           | Ya (terbatas) | Tidak               | Atur batas pengeluaran bulanan organisasi; lihat [Batas pengeluaran](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#spend-limits). AWS Marketplace mengelola penagihan faktur. Lihat rincian biaya di halaman Cost. |
| **Claude Code**       | Tidak         | N/A                 | Lihat penggunaan Claude Code di halaman Usage.                                                                                                                                                                                                    |

### Berpindah organisasi

Claude Console tidak mendukung perpindahan organisasi untuk Claude Platform on AWS. Untuk mengakses organisasi lain, keluar lalu autentikasi ulang melalui AWS Console menggunakan peran IAM untuk akun AWS organisasi tersebut.

## Batas laju dan kuota

Organisasi di Claude Platform on AWS ditempatkan pada tier Start. Anthropic mengelola "rate limit" (batas laju) secara langsung, bukan melalui sistem kuota AWS.

Organisasi di Claude Platform on AWS tidak berpindah antar tier penggunaan secara otomatis. Kenaikan tier berbasis penggunaan berlaku untuk organisasi Claude API pihak pertama, bukan untuk organisasi yang ditagih melalui AWS Marketplace. Alur swalayan **Request rate limit increase** di Claude Console juga tidak tersedia: halaman Rate limits mengarahkan Anda ke perwakilan akun Anthropic Anda sebagai gantinya.

Untuk meminta batas yang lebih tinggi, hubungi perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com). Sertakan hal berikut dalam permintaan Anda:

* Model yang batasnya perlu dinaikkan
* Puncak token input per menit dan token output per menit untuk setiap model (bukan total harian)
* Perkiraan porsi input Anda yang berupa konteks yang di-cache atau berulang (pembacaan cache tidak dihitung terhadap batas token input untuk sebagian besar model; lihat [ITPM sadar-cache](https://platform.claude.com/docs/id/api/rate-limits#cache-aware-itpm))

Tier penggunaan adalah tahapan tetap: setiap tier memasangkan batas laju dengan [batas pengeluaran bulanan](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#spend-limits), dan berpindah ke tier yang lebih tinggi menaikkan keduanya. Untuk detail tier dan batas per model, lihat [Batas laju](https://platform.claude.com/docs/id/api/rate-limits).

## Penagihan

Claude Platform on AWS menagih melalui [AWS Marketplace](https://aws.amazon.com/marketplace). Penggunaan dinyatakan dalam Claude Consumption Unit (CCU), diukur per jam, dan ditagihkan bulanan di akhir periode pada tagihan AWS Anda. CCU bukan kredit prabayar. Tidak ada saldo atau komitmen CCU.

Untuk harga CCU, mekanisme konversi, penerapan diskon, dan tarif token per model, lihat [harga Claude Platform on AWS](https://platform.claude.com/docs/id/about-claude/pricing#claude-platform-on-aws-pricing).

### Batas pengeluaran

Tier penggunaan Start, Build, dan Scale masing-masing memiliki batas pengeluaran bulanan; lihat [batas pengeluaran per tier](https://platform.claude.com/docs/id/api/rate-limits#spend-limits) untuk nilai terkini. Batas pengeluaran dan batas laju termasuk dalam tier yang sama, sehingga untuk menaikkan batas pengeluaran, mintalah kenaikan tier melalui perwakilan akun Anthropic Anda atau [dukungan](https://support.claude.com) (lihat [Batas laju dan kuota](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas)).

Anda juga dapat menetapkan batas pengeluaran bulanan Anda sendiri untuk membatasi pengeluaran organisasi Anda:

* **Batas pengeluaran organisasi:** Buka [Settings > Billing](https://platform.claude.com/settings/billing) di [Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console) untuk menetapkan batas pengeluaran bulanan.
* **Batas pengeluaran workspace:** Tetapkan batas pengeluaran bulanan untuk masing-masing workspace dari pengaturan **Spend limits** setiap workspace.

Batas pengeluaran yang Anda tetapkan adalah batas lunak: pengeluaran dihitung berdasarkan harga daftar dan dapat memerlukan sekitar dua jam untuk mencerminkan penggunaan terbaru.

## Pemantauan dan pencatatan log

AWS CloudTrail dapat menangkap semua permintaan ke Claude Platform on AWS. Operasi workspace, kepatuhan, vault, dan webhook dicatat sebagai Management event secara default. Operasi inferensi, batch, file, skill, model, profil pengguna, dan Claude Managed Agents (selain vault dan webhook) diklasifikasikan sebagai Data event dan memerlukan konfigurasi pencatatan data event secara eksplisit, yang menimbulkan biaya CloudTrail tambahan. Lihat [referensi aksi IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#route-to-action-mapping) untuk klasifikasi jenis event lengkap dan [dokumentasi AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/) untuk detail konfigurasi.

### ID permintaan

Setiap respons menyertakan dua ID permintaan dalam header respons:

* **ID permintaan AWS (`x-amzn-requestid`):** ID utama, diindeks di CloudTrail. Gunakan ini saat menyelidiki permintaan melalui perangkat AWS atau saat menghubungi dukungan AWS.
* **ID permintaan Anthropic (`request-id`):** ID sekunder. Gunakan ini saat menghubungi dukungan Anthropic.

<CodeGroup>
  ```bash cURL
  # Ganti us-west-2 dengan region AWS Anda di URL dan --aws-sigv4
  # -i menyertakan header respons dalam output
  # Hilangkan header x-amz-security-token jika Anda menggunakan kredensial pengguna IAM jangka panjang
  curl -i "https://aws-external-anthropic.us-west-2.api.aws/v1/messages" \
    --aws-sigv4 "aws:amz:us-west-2:aws-external-anthropic" \
    --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
    -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
    -H "content-type: application/json" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-workspace-id: $ANTHROPIC_AWS_WORKSPACE_ID" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    }'
  ```

  ```bash CLI
  # Format output CLI ant mencetak body respons, bukan header respons.
  # Untuk membaca x-amzn-requestid, gunakan contoh cURL (-i) atau contoh SDK.
  ```

  ```python Python
  from anthropic import AnthropicAWS

  client = AnthropicAWS()

  response = client.messages.with_raw_response.create(
      model="claude-sonnet-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  )

  print(response.headers.get("x-amzn-requestid"))  # AWS request ID
  print(response.headers.get("request-id"))  # Anthropic request ID

  message = response.parse()
  print(message.content)
  ```

  ```typescript TypeScript
  import AnthropicAws from "@anthropic-ai/aws-sdk";

  const client = new AnthropicAws();

  const { data: message, response } = await client.messages
    .create({
      model: "claude-sonnet-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello!" }]
    })
    .withResponse();

  console.log(response.headers.get("x-amzn-requestid")); // AWS request ID
  console.log(response.headers.get("request-id")); // Anthropic request ID
  console.log(message.content);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Aws;

  var client = new AnthropicAwsClient();

  var response = await client.WithRawResponse.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }]
  });

  Console.WriteLine(response.Headers.GetValues("x-amzn-requestid").First()); // AWS request ID
  Console.WriteLine(response.Headers.GetValues("request-id").First()); // Anthropic request ID
  Console.WriteLine(response.Value.Content);
  ```

  ```go Go
  client, err := anthropicaws.NewClient(context.Background(), anthropicaws.ClientConfig{})
  if err != nil {
  	panic(err)
  }

  var response *http.Response
  message, err := client.Messages.New(
  	context.Background(),
  	anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeSonnet5,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  		},
  	},
  	option.WithResponseInto(&response),
  )
  if err != nil {
  	panic(err)
  }

  fmt.Println(response.Header.Get("x-amzn-requestid")) // AWS request ID
  fmt.Println(response.Header.Get("request-id"))       // Anthropic request ID
  fmt.Println(message.Content)
  ```

  ```java Java
  import com.anthropic.aws.backends.AwsBackend;
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.http.HttpResponseFor;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(AwsBackend.fromEnv())
          .build();

      HttpResponseFor<Message> response = client.messages().withRawResponse().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_5)
              .maxTokens(1024)
              .addUserMessage("Hello!")
              .build()
      );

      IO.println(response.headers().values("x-amzn-requestid").get(0)); // AWS request ID
      IO.println(response.requestId().orElse(null)); // Anthropic request ID
      IO.println(response.parse().content());
  }
  ```

  ```php PHP
  use Anthropic\Aws\Client;

  $client = new Client();

  $response = $client->messages->raw->create(
      model: 'claude-sonnet-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello!']],
  );

  echo $response->getHeaderLine('x-amzn-requestid') . "\n"; // AWS request ID
  echo $response->getHeaderLine('request-id') . "\n"; // Anthropic request ID
  echo $response->parse()->content;
  ```

  ```ruby Ruby
  # Mengakses header respons mentah saat ini belum didukung di Ruby SDK.
  # Untuk memeriksa header x-amzn-requestid, gunakan salah satu contoh SDK lainnya.
  ```
</CodeGroup>

Anthropic merekomendasikan pencatatan log aktivitas Anda setidaknya dalam periode bergulir 30 hari untuk memahami pola penggunaan dan menyelidiki masalah.

<Note>
  AWS CloudTrail dikonfigurasi di dalam akun AWS Anda. Mengaktifkan pencatatan log tidak memberikan AWS atau Anthropic akses ke konten Anda di luar yang diperlukan untuk penagihan dan operasi layanan.
</Note>

## Migrasi dari Amazon Bedrock

Jika saat ini Anda menggunakan Claude di Bedrock, migrasi ke Claude Platform on AWS memerlukan perubahan di seluruh integrasi Anda. Penandatanganan SigV4 tetap didukung, tetapi konteks penandatanganan, base URL, format API, ID model, klien dan paket SDK, format streaming, header permintaan, dan ketersediaan region semuanya berubah. Claude Platform on AWS juga menyediakan organisasi Anthropic baru. Tabel berikut merangkum perbedaannya.

### Apa yang berubah

Delta migrasi bergantung pada integrasi Bedrock mana yang Anda gunakan sebelumnya. Tabel berikut menampilkan [integrasi Bedrock saat ini](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) (Messages API di `bedrock-mantle.{region}.api.aws`) dan [integrasi InvokeModel lama](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy).

| Aspek                    | Dari [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) | Dari [Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) | Ke Claude Platform on AWS                                                                                                                                                                                                                                                           |
| ------------------------ | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Base URL**             | `bedrock-mantle.{region}.api.aws`                                                                               | `bedrock-runtime.{region}.amazonaws.com`                                                                                               | `aws-external-anthropic.{region}.api.aws`                                                                                                                                                                                                                                           |
| **Format API**           | Messages API di `/anthropic/v1/messages`                                                                        | Bedrock Converse / InvokeModel                                                                                                         | Claude API (`/v1/{endpoint}`)                                                                                                                                                                                                                                                       |
| **ID model**             | anthropic.claude-haiku-4-5                                                                                      | anthropic.claude-haiku-4-5-20251001-v1:0(dengan awalan profil inferensi `us.` atau `global.`)                                          | claude-haiku-4-5                                                                                                                                                                                                                                                                    |
| **Klien SDK**            | `AnthropicBedrockMantle`                                                                                        | `AnthropicBedrock` / Bedrock SDK                                                                                                       | Klien khusus platform (lihat [Instal SDK](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#install-an-sdk)), dalam beta                                                                                                                                 |
| **Paket SDK**            | `anthropic[bedrock]`, `@anthropic-ai/bedrock-sdk`, dan lainnya                                                  | `anthropic[bedrock]`, `@anthropic-ai/bedrock-sdk`, atau AWS SDK                                                                        | `anthropic[aws]`, `@anthropic-ai/aws-sdk`, dan lainnya (lihat [Instal SDK](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#install-an-sdk))                                                                                                            |
| **Nama layanan SigV4**   | `bedrock-mantle`                                                                                                | `bedrock`                                                                                                                              | `aws-external-anthropic`                                                                                                                                                                                                                                                            |
| **Format streaming**     | SSE                                                                                                             | AWS EventStream                                                                                                                        | SSE (sama dengan Claude API)                                                                                                                                                                                                                                                        |
| **Header workspace**     | Tidak berlaku                                                                                                   | Tidak berlaku                                                                                                                          | `anthropic-workspace-id` wajib                                                                                                                                                                                                                                                      |
| **Ketersediaan region**  | Lihat [region Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html)        | Lihat [region Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html)                               | Semua region komersial AWS                                                                                                                                                                                                                                                          |
| **Organisasi Anthropic** | Tidak diperlukan                                                                                                | Tidak diperlukan                                                                                                                       | Organisasi baru dibuat saat pendaftaran. Organisasi yang sudah ada tidak dapat dikonversi (lihat [Berpindah dari organisasi Anthropic yang sudah ada](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#moving-from-an-existing-anthropic-organization)) |

Jika Anda menggunakan integrasi Bedrock saat ini, format body permintaan sudah berupa Messages API. Perubahannya adalah base URL, nama layanan SigV4, ID model, dan penambahan header `anthropic-workspace-id`. Jika Anda menggunakan InvokeModel atau Converse API lama, Anda juga perlu menulis ulang bentuk permintaan dan respons ke format Messages API. Lihat [Claude di Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) untuk pemetaan bentuk permintaan.

### Apa yang Anda dapatkan

* Akses ke model dan fitur baru yang biasanya tersedia di hari yang sama (lihat [keterbatasan fitur](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#features-not-supported))
* Agent Skills untuk pembuatan dokumen (PowerPoint, Excel, Word, PDF)
* Eksekusi kode di sandbox terkelola Anthropic
* Fitur beta melalui header `anthropic-beta` (lihat [keterbatasan fitur](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#features-not-supported))
* Claude Console untuk visibilitas kuota dan analitik penggunaan
* Dukungan langsung dari Anthropic
* Autentikasi kunci API sebagai alternatif SigV4 (lihat [Autentikasi kunci API](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#api-key-authentication))

### Apa yang tetap sama

* Autentikasi AWS IAM (SigV4)
* AWS sebagai pihak penerbit faktur. Saluran penagihan berubah dari layanan AWS native ke AWS Marketplace (lihat [Pertimbangan komersial](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#commercial-considerations)).
* Pemenuhan komitmen AWS

### Jebakan migrasi

<Warning>
  **Aktifkan outbound web identity federation terlebih dahulu.** Jika akun AWS Anda belum pernah menggunakan Claude Platform on AWS, Anda harus [mengaktifkan outbound web identity federation](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#enable-outbound-web-identity-federation) sekali per akun sebelum membuat permintaan. Tanpa langkah ini, semua permintaan gagal dengan error federasi (lihat [Aktifkan outbound web identity federation](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#enable-outbound-web-identity-federation) untuk error persisnya dan cara perbaikannya). Langkah ini tidak diperlukan untuk Bedrock.
</Warning>

<Warning>
  **Zero Data Retention (ZDR) bersifat opt-in di Claude Platform on AWS.** Di Bedrock, AWS adalah pemroses data dan Anthropic tidak menyimpan input atau output inferensi. Program ZDR Anthropic tidak berlaku di sana. Di Claude Platform on AWS, Anthropic memproses data inferensi sebagai pemroses data independen, dan ZDR mengikuti model Claude API pihak pertama: tersedia atas permintaan melalui perwakilan akun Anthropic Anda. Konfirmasikan pendaftaran ZDR sebelum memigrasikan beban kerja produksi yang bergantung pada jaminan retensi data.
</Warning>

### Pertimbangan komersial

* **Ketentuan layanan Anthropic:** Menggunakan Claude Platform on AWS mengharuskan Anda menerima Commercial Terms of Service dan Usage Policy Anthropic. Jika organisasi Anda belum menerimanya (misalnya, jika Anda hanya pernah menggunakan Claude melalui Bedrock), Anda akan diminta saat penyiapan akun. Lihat [Siapkan akun Anda](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#set-up-your-account).
* **Diskon dan penawaran privat:** Diskon yang dinegosiasikan dan penawaran privat AWS Marketplace tidak berpindah secara otomatis antara Bedrock dan Claude Platform on AWS. Bekerja samalah dengan perwakilan akun Anthropic Anda untuk menyiapkan ketentuan komersial untuk Claude Platform on AWS.

## Kebijakan IAM

Claude Platform on AWS terintegrasi dengan AWS IAM untuk kontrol akses. Anda memberikan atau menolak akses ke aksi API tertentu pada workspace tertentu menggunakan sintaks kebijakan IAM standar.

Nama layanan SigV4 dan namespace aksi IAM adalah `aws-external-anthropic`. Aksi mengikuti pola `aws-external-anthropic:<Action>` (misalnya, `aws-external-anthropic:CreateInference`).

### Contoh: tolak inferensi batch

Kebijakan berikut mengizinkan inferensi real-time sambil memblokir pemrosesan batch:

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
      "Resource": "arn:aws:aws-external-anthropic:*:*:workspace/*"
    },
    {
      "Effect": "Allow",
      "Action": "aws-external-anthropic:ListWorkspaces",
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": [
        "aws-external-anthropic:CreateBatchInference",
        "aws-external-anthropic:GetBatchInference",
        "aws-external-anthropic:ListBatchInferences"
      ],
      "Resource": "*"
    }
  ]
}
```

Aksi `GetBatchInference` mengotorisasi rute metadata batch dan rute hasil batch. Menolaknya memblokir kedua pembacaan tersebut. Untuk kebijakan khusus-Deny yang cocok untuk beban kerja sensitif ZDR, lihat [Penguncian fitur untuk workspace sensitif ZDR](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#feature-lockdown-for-a-zdr-sensitive-workspace).

<Note>
  `ListWorkspaces` bercakupan akun, sehingga muncul dalam pernyataan Allow terpisah dengan `"Resource": "*"`. Menentukan ARN workspace pada aksi bercakupan akun tidak berpengaruh (lihat [Otomatisasi penyediaan](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#provisioning-automation)).

  Kebijakan ini mengasumsikan autentikasi AWS SigV4. Jika principal melakukan autentikasi dengan kunci API, tambahkan juga `aws-external-anthropic:CallWithBearerToken` ke pernyataan Allow `"Resource": "*"`. `CallWithBearerToken` adalah aksi lapisan autentikasi tanpa rute yang tidak terikat pada ARN workspace. Lihat [Isolasi workspace per pelanggan](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#per-customer-workspace-isolation) untuk pola dua pernyataan.
</Note>

### Kebijakan terkelola

AWS menyediakan lima kebijakan terkelola (`AnthropicFullAccess`, `AnthropicReadOnlyAccess`, `AnthropicInferenceAccess`, `AnthropicLimitedAccess`, dan `AnthropicSelfHostedEnvironmentAccess`) untuk pola akses umum. Untuk aksi yang diberikan setiap kebijakan, daftar lengkap aksi IAM, pemetaan rute-ke-aksi, dan contoh kebijakan tambahan, lihat [Aksi IAM untuk Claude Platform on AWS](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#managed-policies).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ikhtisar fitur" icon="stack" href="https://platform.claude.com/docs/id/build-with-claude/overview">
    Jelajahi fitur dan kemampuan lanjutan Claude.
  </Card>

  <Card title="Harga" icon="chart" href="https://platform.claude.com/docs/id/about-claude/pricing#claude-platform-on-aws-pricing">
    Pelajari harga Claude Platform on AWS dan tarif Claude Consumption Unit.
  </Card>

  <Card title="Penghentian model" icon="arrow-clockwise" href="https://platform.claude.com/docs/id/about-claude/model-deprecations">
    Seiring diluncurkannya model yang lebih aman dan lebih mumpuni, Anthropic secara rutin menghentikan model lama. Lihat semua penghentian API, beserta pengganti yang direkomendasikan.
  </Card>
</CardGroup>

## Sumber daya tambahan

<CardGroup cols={2}>
  <Card title="Claude Console" icon="browser" href="https://platform.claude.com">
    Lihat penggunaan, biaya, dan workspace di Claude Console. Masuk melalui AWS Console.
  </Card>

  <Card title="Claude in Amazon Bedrock" icon="cloud" href="https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock">
    Gunakan Claude yang dioperasikan AWS jika Anda memerlukan AWS sebagai satu-satunya pemroses data.
  </Card>

  <Card title="AWS Marketplace" icon="coins" href="https://aws.amazon.com/marketplace">
    Kelola langganan dan penagihan AWS Marketplace Anda.
  </Card>
</CardGroup>
