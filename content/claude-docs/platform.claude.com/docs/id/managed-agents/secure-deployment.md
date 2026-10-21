---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/secure-deployment
fetched_at: 2026-10-21T02:21:05.363362Z
sha256: 194a101f0ee13a260b43d5c84b1d02cddabfcb03d70e0a8daac30b91359b8b78
---

---
title: Amankan deployment Managed Agents Anda
url: https://platform.claude.com/docs/id/managed-agents/secure-deployment
description: Pengaturan yang membatasi apa yang dapat dijangkau dan dilakukan oleh agen Anda, diurutkan dari yang paling penting.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Panduan ini mencantumkan pengaturan yang membatasi apa yang dapat dijangkau dan dilakukan oleh agen di Claude Managed Agents, diurutkan dari yang paling penting. Setiap bagian menautkan ke halaman yang membahas pengaturan tersebut secara lengkap.

| Bagian                                                                                                                                                                                                        | Pengaturan atau keputusan                                                        | Rekomendasi                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Pilih tempat agen berjalan](https://platform.claude.com/docs/id/managed-agents/secure-deployment#choose-where-the-agent-runs)                                                                                | Sandbox cloud atau self-hosted                                                   | Cloud, kecuali alat harus berjalan di infrastruktur yang Anda kendalikan                                                                                                                                                                                                  |
| [Batasi jaringan](https://platform.claude.com/docs/id/managed-agents/secure-deployment#limit-the-network)                                                                                                     | `networking.type` pada environment                                               | `limited`, hanya dengan host yang dibutuhkan agen                                                                                                                                                                                                                         |
| [Simpan kredensial di vault](https://platform.claude.com/docs/id/managed-agents/secure-deployment#keep-credentials-in-vaults)                                                                                 | `injection_location` dan `networking` pada setiap kredensial variabel lingkungan | Hanya header permintaan, dan jaringan `limited` hanya dengan host yang menjadi tujuan kunci tersebut                                                                                                                                                                      |
| [Simpan kredensial di vault](https://platform.claude.com/docs/id/managed-agents/secure-deployment#keep-credentials-in-vaults)                                                                                 | Cara aplikasi Anda melakukan autentikasi ke Claude API                           | Jika memungkinkan, aturan Workload Identity Federation yang diaktifkan hanya di satu workspace, jika tidak, kunci API yang cakupannya terbatas pada satu workspace                                                                                                        |
| [Batasi web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/secure-deployment#restrict-web-search-and-web-fetch)                                                                     | `allowed_domains` pada setiap alat web                                           | Daftar izin (allowlist) pada setiap alat. Pada `web_fetch`, cantumkan hanya situs yang dibutuhkan agen. Pada `web_search`, cantumkan situs yang hasilnya Anda inginkan                                                                                                    |
| [Setujui tindakan berisiko](https://platform.claude.com/docs/id/managed-agents/secure-deployment#approve-risky-actions)                                                                                       | `permission_policy` pada setiap alat                                             | `auto` pada `bash`, `write`, `edit`, `web_fetch`, dan alat MCP yang hanya membaca data. Gunakan `always_ask` pada alat jika Anda tidak dapat membatalkan perubahannya di luar sandbox, atau jika teks pengguna akhir yang diteruskan saja tidak boleh membuatnya berjalan |
| [Berikan agen set alat terkecil](https://platform.claude.com/docs/id/managed-agents/secure-deployment#give-the-agent-the-smallest-tool-set)                                                                   | `default_config.enabled` pada toolset agen                                       | `false`, lalu aktifkan alat yang dibutuhkan agen                                                                                                                                                                                                                          |
| [Jauhkan input tidak tepercaya dari alat yang kuat](https://platform.claude.com/docs/id/managed-agents/secure-deployment#keep-untrusted-input-away-from-powerful-tools)                                       | Alat dan kredensial mana yang dimiliki agen saat membaca input tidak tepercaya   | Tidak ada agen pembaca input tidak tepercaya yang memiliki alat dengan `always_allow` yang menulis file, menjalankan perintah, atau mengubah catatan                                                                                                                      |
| [Tetapkan batas dan cara untuk menghentikan](https://platform.claude.com/docs/id/managed-agents/secure-deployment#set-limits-and-a-way-to-stop)                                                               | `budget` pada setiap sesi dan deployment                                         | Batas yang disesuaikan dengan perkiraan biaya satu kali eksekusi                                                                                                                                                                                                          |
| [Secara opsional, minta peninjau offline membaca setiap transkrip](https://platform.claude.com/docs/id/managed-agents/secure-deployment-monitoring#optionally-have-an-offline-reviewer-read-every-transcript) | Job tinjauan offline yang Anda jalankan untuk membaca event setiap sesi          | Opsional. Peninjauan terjadwal atas setiap sesi yang menjadi idle atau dihentikan                                                                                                                                                                                         |
| [Pantau sesi dan tinjau retensi](https://platform.claude.com/docs/id/managed-agents/secure-deployment-monitoring#monitor-sessions-and-review-retention)                                                       | Webhook dan penghapusan sesi                                                     | Peringatan saat sesi menjadi idle, mencapai anggarannya, atau dihentikan, serta pemeriksaan mengapa sesi menjadi idle. Simpan event yang ingin Anda pertahankan di log Anda sendiri, dan hapus sesi yang tidak lagi Anda perlukan                                         |

[Risiko keamanan dan batasan sandbox](https://platform.claude.com/docs/id/managed-agents/secure-deployment-risks) menjelaskan mengapa pengaturan ini penting dan apa yang tidak dilindunginya. Untuk meninjau dan memantau sesi, lihat [Tinjau dan pantau sesi agen](https://platform.claude.com/docs/id/managed-agents/secure-deployment-monitoring).

## Pilih tempat agen berjalan

Tempat alat agen berjalan menentukan siapa yang mengamankan sandbox: Anthropic, dengan environment cloud, atau Anda, dengan sandbox self-hosted. Untuk memilih di antara keduanya dan mempelajari apa yang sampai ke Anthropic pada masing-masing opsi, lihat [Memilih lingkungan agen](https://platform.claude.com/docs/id/managed-agents/choosing-an-environment).

Jika Anda menggunakan [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes), perhatikan empat poin berikut:

* **Jaringan:** [Batasi jaringan](https://platform.claude.com/docs/id/managed-agents/secure-deployment#limit-the-network) berlaku untuk environment cloud. Untuk sandbox self-hosted, tetapkan batas yang setara pada lalu lintasnya di firewall Anda sendiri. Firewall Anda tidak membatasi server MCP yang dideklarasikan agen, jadi tinjau server tersebut, serta server apa pun yang ditetapkan aplikasi Anda untuk sebuah sesi.
* **Alat web:** Alat web berjalan di server Anthropic, sehingga firewall Anda tidak membatasinya. Batasi alat tersebut dengan daftar domainnya. Lihat [Batasi web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/secure-deployment#restrict-web-search-and-web-fetch).
* **Kredensial:** Kredensial variabel lingkungan belum didukung pada sandbox self-hosted.
* **Isolasi dan hardening:** Anda bertanggung jawab atas keduanya. Lihat [Model keamanan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security).

Tidak ada opsi yang mengubah cakupan kepatuhan Managed Agents atau berapa lama riwayat sesi disimpan. Lihat [Pantau sesi dan tinjau retensi](https://platform.claude.com/docs/id/managed-agents/secure-deployment-monitoring#monitor-sessions-and-review-retention).

## Batasi jaringan

Tetapkan `networking.type` ke `limited` dan cantumkan hanya host yang dibutuhkan agen di `allowed_hosts`. Permintaan pembuatan environment yang tidak menyertakan `networking` mungkin mendapatkan `unrestricted`, jadi tetapkan `networking` di setiap permintaan pembuatan. Lihat [Risiko jaringan tanpa batasan](https://platform.claude.com/docs/id/managed-agents/environments#risks-of-unrestricted-networking).

File, memory store, dan repositori GitHub yang Anda lampirkan tetap tersedia bagi agen terlepas dari `allowed_hosts`.

Contoh di halaman ini menggunakan agen dukungan. Agen ini membaca tiket pelanggan, mencari pesanan, membaca pusat bantuan Anda, dan menyusun draf balasan. Aplikasi Anda menjalankan pencarian pesanan, yang tidak memerlukan host, sehingga environment ini mengizinkan satu host, yaitu pusat bantuan, untuk `web_fetch`:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsS https://api.anthropic.com/v1/environments \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "support-agent",
      "config": {
        "type": "cloud",
        "networking": {
          "type": "limited",
          "allowed_hosts": ["help.example.com"]
        }
      }
    }'
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply environment.yaml
    ```

    <File filename="environment.yaml">
      ```yaml
      # yaml-language-server: $schema=https://platform.claude.com/schemas/ant/beta/environment.json
      name: support-agent
      config:
        type: cloud
        networking:
          type: limited
          allowed_hosts:
            - help.example.com
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  environment = client.beta.environments.create(
      name="support-agent",
      config={
          "type": "cloud",
          "networking": {
              "type": "limited",
              "allowed_hosts": ["help.example.com"],
          },
      },
  )
  ```

  ```typescript TypeScript
  const environment = await client.beta.environments.create({
    name: "support-agent",
    config: {
      type: "cloud",
      networking: {
        type: "limited",
        allowed_hosts: ["help.example.com"]
      }
    }
  });
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Environments;

  var environment = await client.Beta.Environments.Create(new()
  {
      Name = "support-agent",
      Config = new BetaCloudConfigParams
      {
          Networking = new BetaLimitedNetworkParams
          {
              AllowedHosts = ["help.example.com"],
          },
      },
  });
  ```

  ```go Go
  environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
  	Name: "support-agent",
  	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
  		OfCloud: &anthropic.BetaCloudConfigParams{
  			Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
  				OfLimited: &anthropic.BetaLimitedNetworkParams{
  					AllowedHosts: []string{"help.example.com"},
  				},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  _ = environment
  ```

  ```java Java
  import com.anthropic.models.beta.environments.*;
  import java.util.List;

  var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
      .name("support-agent")
      .config(BetaCloudConfigParams.builder()
          .networking(BetaLimitedNetworkParams.builder()
              .allowedHosts(List.of("help.example.com"))
              .build())
          .build())
      .build());
  ```

  ```php PHP
  $environment = $client->beta->environments->create(
      name: 'support-agent',
      config: [
          'type' => 'cloud',
          'networking' => [
              'type' => 'limited',
              'allowed_hosts' => ['help.example.com'],
          ],
      ],
  );
  ```

  ```ruby Ruby
  environment = client.beta.environments.create(
    name: "support-agent",
    config: {
      type: "cloud",
      networking: {
        type: "limited",
        allowed_hosts: ["help.example.com"]
      }
    }
  )
  ```
</CodeGroup>

Environment `limited` memiliki tiga pengaturan jaringan:

| Pengaturan               | Apa yang dibukanya bagi kode di sandbox                                                                                                                                                                                                                                                                  | Rekomendasi                                                                                                                                                                                                                        |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowed_hosts`          | Host yang Anda cantumkan, untuk permintaan apa pun                                                                                                                                                                                                                                                       | Hanya host yang dibutuhkan agen, termasuk host setiap server MCP yang Anda operasikan atau percayai                                                                                                                                |
| `allow_package_managers` | [Host package manager](https://platform.claude.com/docs/id/managed-agents/environments#package-manager-hosts). Ini mencakup setiap repositori dan path di `github.com`, `gitlab.com`, dan `bitbucket.org`, tempat siapa pun dapat memublikasikan konten dan tempat kode di sandbox dapat mengunggah file | `false`, kecuali pengaturan `packages` pada environment mencantumkan paket, yang memerlukan `true`. Jika agen menginstal paket saat berjalan, cantumkan hanya host registry yang dibutuhkannya di `allowed_hosts` sebagai gantinya |
| `allow_mcp_servers`      | Tidak ada host. Managed Agents terhubung ke server MCP dari server Anthropic                                                                                                                                                                                                                             | `false`, dengan host setiap server MCP yang Anda operasikan atau percayai dicantumkan di `allowed_hosts`                                                                                                                           |

Pengaturan `allow_package_managers` dan `allow_mcp_servers` tidak menambahkan host untuk web search dan web fetch.

Biarkan `allow_mcp_servers` nonaktif, yang merupakan default, dan cantumkan host setiap server MCP yang Anda operasikan atau percayai di `allowed_hosts`. Setiap host yang Anda cantumkan juga terbuka bagi kode di sandbox. Dengan `allow_mcp_servers` nonaktif, pemeriksaan saat pembuatan sesi menolak permintaan jika host server MCP tidak tercantum. Lihat [Menyediakan autentikasi saat pembuatan sesi](https://platform.claude.com/docs/id/managed-agents/mcp-connector#provide-authentication-at-session-creation). Pemeriksaan yang sama dijalankan saat pembaruan sesi mengubah `mcp_servers`.

<Warning>
  Akses jaringan diberikan per host, bukan per operasi. Sandbox dapat mengirim permintaan apa pun ke host yang diizinkan, termasuk unggahan seperti `git push` dan publikasi paket. Sandbox juga dapat menggunakan kredensial apa pun yang diberikan oleh perintah, bahkan kredensial yang disembunyikan seseorang dalam teks yang dibaca agen.
</Warning>

Saat Anda memilih host untuk `allowed_hosts`, ikuti dua aturan berikut:

* Cantumkan hanya host yang Anda operasikan atau percayai.
* Hindari wildcard `*.` dan domain shared-hosting tempat siapa pun dapat memublikasikan konten.

Jika agen tetap memiliki `bash`, tetapkan [kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) alat `bash` seperti yang dijelaskan di [Setujui tindakan berisiko](https://platform.claude.com/docs/id/managed-agents/secure-deployment#approve-risky-actions).

<Note>
  Setelah Anda memperketat environment, mulai sesi baru dan hentikan sesi yang sudah berjalan. Sesi yang sudah berjalan dapat mempertahankan batas lama hingga berakhir. Lihat [Tetapkan batas dan cara untuk menghentikan](https://platform.claude.com/docs/id/managed-agents/secure-deployment#set-limits-and-a-way-to-stop).
</Note>

Lihat [Penyiapan environment cloud](https://platform.claude.com/docs/id/managed-agents/environments#networking) untuk setiap pengaturan jaringan.

## Simpan kredensial di vault

Simpan setiap rahasia di vault. Untuk setiap kredensial variabel lingkungan, tetapkan lokasi injeksi hanya ke header permintaan dan cantumkan hanya host yang menjadi tujuan rahasia tersebut. Kode di sandbox melihat placeholder alih-alih rahasia. Managed Agents menukar placeholder dengan rahasia asli hanya dalam permintaan HTTPS keluar ke host yang diizinkan kredensial. Dengan demikian, rahasia tetap berada di luar jangkauan langsung model, kecuali jika suatu layanan mengirimkannya kembali, seperti endpoint yang menggemakan header permintaan. Jika `networking` kredensial adalah `unrestricted`, Managed Agents memasukkan rahasia asli ke dalam permintaan ke host mana pun yang dapat dijangkau sandbox menurut environment. Untuk menggunakan vault, teruskan ID-nya di `vault_ids` saat Anda membuat sesi atau deployment.

| Pengaturan                                    | Tetapkan ke                                                                                                           | Alasan                                                                                                                                                                                                                                                          | Apa yang tidak dilakukannya                                                                                                                                      |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `injection_location`                          | `{"header": true, "body": false}`, setelah Anda memeriksa bahwa layanan membaca kunci dari header                     | Body permintaan sering dibangun dari konten yang dibaca agen, sehingga kunci di body lebih terekspos. Sebutkan kedua field: permintaan pembuatan yang tidak menyertakan objek ini mengaktifkan kedua lokasi, dan pembaruan hanya mengubah field yang Anda kirim | Kode tetap dapat menggunakan kunci di setiap host yang diizinkan kredensial. Layanan yang mengharapkan kunci di body menerima placeholder dan menolak permintaan |
| `networking` pada kredensial                  | `limited`, dengan host persis yang menjadi tujuan kunci                                                               | Respons sampai ke sandbox tanpa disensor, jadi hindari wildcard, domain shared-hosting, dan host yang menggemakan header permintaan                                                                                                                             | Tidak membuka host. Environment juga harus mengizinkannya                                                                                                        |
| Izin kunci, di layanan yang menerbitkan kunci | Hanya izin yang dibutuhkan agen                                                                                       | Agen dapat melakukan apa pun yang diizinkan kunci                                                                                                                                                                                                               | Tidak berlaku                                                                                                                                                    |
| Token GitHub repositori yang di-mount         | [Token fine-grained](https://platform.claude.com/docs/id/managed-agents/github#token-permissions) dengan izin minimum | Kode di sandbox dapat melakukan fetch dari dan push ke repositori yang di-mount dengan token ini selama seluruh sesi. Berikan akses tulis hanya jika agen harus melakukan push                                                                                  | Tidak berlaku                                                                                                                                                    |

Agen dukungan tidak memerlukan kredensial vault, karena aplikasi Anda memegang kunci API untuk API pesanan Anda. Jika agen Anda memegang kredensial vault, lihat [Menambahkan kredensial](https://platform.claude.com/docs/id/managed-agents/vaults#add-a-credential) untuk permintaan dalam setiap bahasa.

Jauhkan kunci dari prompt sistem, definisi agen, dan pesan. Jangan berikan kunci API Claude atau token akses Claude API kepada agen. Bahkan ketika salah satunya berada di vault, kode di sandbox dapat menggunakannya untuk memanggil Claude API secara langsung. Kode tersebut dapat melakukan apa pun yang diizinkan kredensial itu, seperti memulai atau menghapus sesi, atau menggunakan web search dan web fetch. Pengaturan alat, persetujuan, dan anggaran agen tidak berlaku untuk panggilan tersebut. Dalam environment `limited`, kode dapat melakukan panggilan ini hanya jika `allowed_hosts` memungkinkan sandbox menjangkau `api.anthropic.com`.

Ambil sendiri token pihak ketiga dan simpan di vault. Token yang diambil oleh kode di sandbox dengan rahasia yang tersimpan akan kembali tanpa disensor.

Simpan vault untuk beban kerja dengan tingkat kepercayaan berbeda di [workspace](https://platform.claude.com/docs/id/manage-claude/workspaces) terpisah, karena siapa pun yang dapat memulai sesi di suatu workspace dapat mereferensikan vault-nya. Batasi setiap beban kerja ke satu workspace: jika memungkinkan, aturan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) yang diaktifkan hanya di workspace tersebut, jika tidak, kunci API yang cakupannya terbatas pada workspace tersebut. Workload Identity Federation memberi aplikasi Anda token akses Claude API berumur pendek, sehingga tidak ada kunci API Claude berumur panjang yang dapat bocor.

Lihat [Autentikasi dengan vault](https://platform.claude.com/docs/id/managed-agents/vaults) untuk kredensial MCP dan rotasi.

## Batasi web search dan web fetch

Tetapkan `allowed_domains` pada `web_fetch` ke situs yang dibutuhkan agen. URL apa pun yang diambil agen dapat membawa data ke situs yang ditujunya, sehingga daftar ini merupakan kontrol keamanan. Pada `web_search`, tetapkan `allowed_domains` ke situs yang hasilnya Anda inginkan, sehingga hasil hanya berasal dari situs yang Anda percayai keakuratannya. Daftar ini tidak mencegah kueri pencarian sampai ke penyedia pencarian. Hasil pencarian menyertakan teks dari halaman, sehingga daftar ini juga membatasi teks dari situs mana yang sampai ke agen. Tetapkan `allowed_domains` pada kedua alat untuk setiap jenis environment.

Daftar `blocked_domains` memblokir host yang Anda cantumkan beserta subdomainnya, dan tidak ada host lain. Konten yang sama masih dapat sampai ke agen dari arsip web, cache, mirror, atau domain terkait yang tidak Anda cantumkan. Jangan mengandalkan `blocked_domains` untuk keamanan. Gunakan `allowed_domains` dan sebutkan host yang Anda percayai.

Dalam environment `limited`, daftar `allowed_hosts` dari [Batasi jaringan](https://platform.claude.com/docs/id/managed-agents/secure-deployment#limit-the-network) juga membatasi alat web. Environment `unrestricted` atau sandbox self-hosted tidak membatasi alat web.

| Dalam environment `limited`                                                          | Hasil                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Entri `allowed_domains` pada alat web yang diaktifkan berada di luar `allowed_hosts` | Pembuatan sesi gagal dengan error 400, begitu pula pembaruan sesi yang menambahkan entri tersebut. Sesi yang dimulai oleh deployment, sesuai jadwalnya atau melalui eksekusi manual, tetap dibuat. Alat kemudian tidak mengembalikan apa pun dari host di luar `allowed_hosts` |
| Alat web tidak memiliki daftarnya sendiri                                            | Alat mengembalikan halaman dan hasil hanya dari host di `allowed_hosts`. Tetapkan juga `allowed_domains` pada alat tersebut                                                                                                                                                    |
| `allowed_hosts` tidak memiliki entri                                                 | Tidak ada alat web yang mengembalikan halaman atau hasil pencarian                                                                                                                                                                                                             |
| Anda menambahkan host ke `allowed_hosts` untuk alat web                              | Host tersebut juga terbuka bagi kode di sandbox                                                                                                                                                                                                                                |

Kedua daftar mencocokkan host secara berbeda:

| Daftar                        | Entri           | Cocok dengan                       | Tidak cocok dengan |
| ----------------------------- | --------------- | ---------------------------------- | ------------------ |
| `allowed_hosts` (environment) | `example.com`   | `example.com`                      | `www.example.com`  |
| `allowed_hosts` (environment) | `*.example.com` | Setiap subdomain                   | `example.com`      |
| `allowed_domains` (alat web)  | `example.com`   | `example.com` dan setiap subdomain | Domain lain        |

Jika agen membutuhkan sebuah situs beserta semua subdomainnya, cantumkan `example.com` dan `*.example.com` di `allowed_hosts`, dan jika tidak, cantumkan host yang persis. Jika sebuah alat mencantumkan `example.com` dan `allowed_hosts` hanya mencantumkan `*.example.com`, sesi tetap dibuat. Pemeriksaan saat pembuatan sesi menganggap `example.com` berada dalam `*.example.com`, tetapi alat tidak mengembalikan apa pun dari `example.com` itu sendiri. Lihat [Menetapkan daftar domain pada agen](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#set-domain-lists-on-an-agent) untuk cara kedua daftar melakukan pencocokan.

Alat `web_fetch` juga hanya membuka URL yang sudah muncul dalam sesi:

| Tempat URL muncul                                                                                 | `web_fetch` dapat membukanya                   |
| ------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Teks pesan pengguna, termasuk teks pengguna akhir yang Anda teruskan                              | Ya                                             |
| Deskripsi event `user.define_outcome`                                                             | Ya                                             |
| Alamat hasil web search                                                                           | Ya                                             |
| Teks halaman yang dikembalikan `web_fetch` sebelumnya (bukan PDF), tempat URL lengkap ditampilkan | Ya                                             |
| Teks hasil alat kustom, ketika Claude memanggil alat tersebut secara langsung                     | Ya, kecuali hasilnya ditandai `is_error: true` |
| Prompt sistem                                                                                     | Tidak                                          |
| Konfigurasi agen, termasuk entri `allowed_domains`                                                | Tidak                                          |
| Output Claude sendiri                                                                             | Tidak                                          |
| Output `bash` dan alat sandbox lainnya                                                            | Tidak                                          |
| Hasil alat MCP                                                                                    | Tidak                                          |
| File yang dilampirkan ke pesan pengguna                                                           | Tidak                                          |

Dalam sesi multiagen, `web_fetch` membuka URL dari agen lain hanya jika URL tersebut sampai ke agen itu melalui sumber yang ditandai Ya. Hasil alat kustom dari panggilan langsung dihitung sebagai sumber yang ditandai Ya. Ini berlaku bahkan jika Claude yang menulis teksnya, misalnya ketika alat mengulang inputnya. URL dapat dihitung bahkan ketika ditulis tanpa `https://`, seperti `example.com/docs`. Alat `web_fetch` tidak selalu dapat membuka tautan yang menampilkan kata-kata alih-alih URL-nya, seperti "Hubungi dukungan." Jika agen harus mengambil URL yang belum muncul dalam sesi, kirimkan URL tersebut dalam pesan pengguna.

Aturan ini mengurangi kemungkinan teks yang diinjeksi membangun URL yang membawa data pribadi. Teks pengguna akhir, hasil pencarian, halaman yang diambil, dan hasil alat kustom masih dapat menambahkan URL, jadi tetap tetapkan `allowed_domains`. Messages API menerapkan aturan serupa dengan daftar sumber yang berbeda. Lihat [Validasi URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#url-validation).

Daftar domain pada `web_fetch` tidak membatasi alat `bash`. [Batasi jaringan](https://platform.claude.com/docs/id/managed-agents/secure-deployment#limit-the-network) juga. Lihat [Aturan daftar domain](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#domain-list-rules).

## Setujui tindakan berisiko

Tetapkan `auto` pada `bash`, `write`, `edit`, dan `web_fetch`, serta pada alat MCP yang hanya membaca data. Gunakan `always_ask` sebagai gantinya pada alat jika Anda tidak dapat membatalkan perubahannya di luar sandbox. Gunakan juga pada alat yang tidak boleh berjalan hanya karena teks pengguna akhir yang Anda teruskan memintanya. [Kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) menentukan apakah panggilan alat berjalan, menunggu persetujuan Anda, atau dievaluasi oleh server.

| Alat                             | Kebijakan yang direkomendasikan                                                                                                                                                  | Alasan                                                                                                            |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `read`, `glob`, `grep`           | `always_allow`                                                                                                                                                                   | Alat ini membaca file di sandbox dan tidak mengubah apa pun                                                       |
| `bash`, `write`, `edit`          | `auto`. Gunakan `always_ask` pada alat jika Anda tidak dapat membatalkan perubahannya di luar sandbox. Gunakan `always_ask` pada `bash` jika Anda meneruskan teks pengguna akhir | Default toolset agen adalah `always_allow`, yang menjalankan setiap panggilan tanpa persetujuan                   |
| `web_fetch`                      | `auto`                                                                                                                                                                           | URL yang diambil agen dapat membawa data ke situs yang ditujunya                                                  |
| `web_search`                     | `always_ask` jika agen menangani data yang tidak ingin Anda kirim dalam kueri pencarian. Jika tidak, `always_allow`                                                              | `allowed_domains` membatasi situs asal hasil, bukan isi kueri                                                     |
| Alat MCP yang hanya membaca data | `auto`, ditetapkan untuk setiap alat di `configs` toolset                                                                                                                        | Default toolset tetap `always_ask`, sehingga alat yang ditambahkan server MCP kemudian tetap menunggu persetujuan |
| Alat MCP yang mengubah data      | `always_ask`                                                                                                                                                                     | Ini adalah default toolset MCP. Pertahankan                                                                       |
| Alat kustom                      | Kode Anda yang memutuskan apakah setiap panggilan berjalan                                                                                                                       | Kebijakan izin tidak berlaku                                                                                      |

Toolset di [Berikan agen set alat terkecil](https://platform.claude.com/docs/id/managed-agents/secure-deployment#give-the-agent-the-smallest-tool-set) menerapkan kebijakan ini.

[Kebijakan `auto`](https://platform.claude.com/docs/id/managed-agents/permission-policies#let-the-server-evaluate-each-call-with-auto) memungkinkan server menjalankan panggilan, menolaknya, atau menjeda untuk persetujuan. Seseorang tidak dapat menyetujui setiap panggilan dalam eksekusi yang panjang, sehingga server memeriksa setiap panggilan sebagai gantinya. Pasangkan `auto` dengan jaringan terbatas, kunci dengan izin sempit, anggaran, dan peringatan pada sesi idle. `auto` bukan titik pemeriksaan manusia, jadi jika seseorang harus meninjau panggilan suatu alat sebelum berjalan, konfigurasikan `always_ask` pada alat tersebut.

`auto` memperlakukan teks dalam event `user.message` dan deskripsi dalam event `user.define_outcome` sebagai instruksi Anda, termasuk teks pengguna akhir yang Anda teruskan.

Sesi yang dijeda menunggu tanpa batas waktu, sehingga sesi tanpa pengawasan memerlukan klien yang menjawab panggilan yang dijeda atau menginterupsi sesi.

Tinjau setiap panggilan yang dijeda sebelum Anda mengizinkannya. Klien yang mengizinkan setiap panggilan tanpa menunjukkannya kepada seseorang sama dengan `always_allow`. Lihat [Merespons permintaan konfirmasi](https://platform.claude.com/docs/id/managed-agents/permission-policies#respond-to-confirmation-requests) dan [Melihat bagaimana setiap panggilan dievaluasi](https://platform.claude.com/docs/id/managed-agents/permission-policies#see-how-each-call-was-evaluated).

## Berikan agen set alat terkecil

Tetapkan `default_config.enabled` ke `false` dan [aktifkan hanya alat yang dibutuhkan agen](https://platform.claude.com/docs/id/managed-agents/tools#enabling-only-specific-tools). Toolset agen mengaktifkan kedelapan alat bawaan secara default.

| Alat                      | Fungsinya                                                                    |
| ------------------------- | ---------------------------------------------------------------------------- |
| `bash`                    | Menjalankan perintah apa pun, termasuk permintaan ke host yang diizinkan     |
| `write`, `edit`           | Mengubah file di sandbox                                                     |
| `read`, `glob`, `grep`    | Membaca file di sandbox                                                      |
| `web_fetch`, `web_search` | Mengembalikan halaman dan hasil pencarian dari web, melalui server Anthropic |

Agen dukungan membutuhkan tiga alat bawaan: `read` dan `write` untuk drafnya, dan `web_fetch` untuk pusat bantuan. Agen ini mencari pesanan melalui [alat kustom](https://platform.claude.com/docs/id/managed-agents/tools#custom-tools), `lookup_order`, yang dijalankan aplikasi Anda. Aplikasi Anda memegang kunci API untuk API pesanan Anda, sehingga agen tidak memerlukan `bash` maupun kredensial.

Contoh berikut membatasi `web_fetch` ke `help.example.com` dengan `allowed_domains`. Contoh ini menetapkan `auto` pada `write` dan `web_fetch`, seperti yang direkomendasikan di [Setujui tindakan berisiko](https://platform.claude.com/docs/id/managed-agents/secure-deployment#approve-risky-actions). Jika tiket pelanggan mendorong agen menggunakan alat ini, agen hanya dapat mengubah file di sandbox atau membuka halaman pusat bantuan. Itulah sebabnya kedua alat tidak memerlukan `always_ask`. Contoh ini juga menetapkan `always_ask` di `default_config`, sehingga alat yang Anda aktifkan kemudian tanpa kebijakannya sendiri menggunakan `always_ask`:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Support Agent",
      "model": "claude-opus-5-5",
      "tools": [
        {
          "type": "agent_toolset_20260401",
          "default_config": {
            "enabled": false,
            "permission_policy": {"type": "always_ask"}
          },
          "configs": [
            {"name": "read", "enabled": true, "permission_policy": {"type": "always_allow"}},
            {"name": "write", "enabled": true, "permission_policy": {"type": "auto"}},
            {
              "name": "web_fetch",
              "enabled": true,
              "allowed_domains": ["help.example.com"],
              "permission_policy": {"type": "auto"}
            }
          ]
        },
        {
          "type": "custom",
          "name": "lookup_order",
          "description": "Look up one order by its ID. Returns the status, the items, and the delivery date.",
          "input_schema": {
            "type": "object",
            "properties": {
              "order_id": {"type": "string", "description": "The order ID from the ticket"}
            },
            "required": ["order_id"]
          }
        }
      ]
    }'
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply agent.md
    ```

    <File filename="agent.md">
      ```markdown
      ---
      name: Support Agent
      model: claude-opus-5-5
      tools:
        - type: agent_toolset_20260401
          default_config:
            enabled: false
            permission_policy:
              type: always_ask
          configs:
            - name: read
              enabled: true
              permission_policy:
                type: always_allow
            - name: write
              enabled: true
              permission_policy:
                type: auto
            - name: web_fetch
              enabled: true
              allowed_domains: [help.example.com]
              permission_policy:
                type: auto
        - type: custom
          name: lookup_order
          description: Look up one order by its ID. Returns the status, the items, and the delivery date.
          input_schema:
            type: object
            properties:
              order_id:
                type: string
                description: The order ID from the ticket
            required:
              - order_id
      ---
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  tools = [
      {
          "type": "agent_toolset_20260401",
          "default_config": {
              "enabled": False,
              "permission_policy": {"type": "always_ask"},
          },
          "configs": [
              {
                  "name": "read",
                  "enabled": True,
                  "permission_policy": {"type": "always_allow"},
              },
              {
                  "name": "write",
                  "enabled": True,
                  "permission_policy": {"type": "auto"},
              },
              {
                  "name": "web_fetch",
                  "enabled": True,
                  "allowed_domains": ["help.example.com"],
                  "permission_policy": {"type": "auto"},
              },
          ],
      },
      {
          "type": "custom",
          "name": "lookup_order",
          "description": "Look up one order by its ID. Returns the status, the items, and the delivery date.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "order_id": {
                      "type": "string",
                      "description": "The order ID from the ticket",
                  },
              },
              "required": ["order_id"],
          },
      },
  ]
  ```

  ```typescript TypeScript
  const tools = [
    {
      type: "agent_toolset_20260401",
      default_config: {
        enabled: false,
        permission_policy: { type: "always_ask" }
      },
      configs: [
        {
          name: "read",
          enabled: true,
          permission_policy: { type: "always_allow" }
        },
        {
          name: "write",
          enabled: true,
          permission_policy: { type: "auto" }
        },
        {
          name: "web_fetch",
          enabled: true,
          allowed_domains: ["help.example.com"],
          permission_policy: { type: "auto" }
        }
      ]
    },
    {
      type: "custom",
      name: "lookup_order",
      description:
        "Look up one order by its ID. Returns the status, the items, and the delivery date.",
      input_schema: {
        type: "object",
        properties: {
          order_id: { type: "string", description: "The order ID from the ticket" }
        },
        required: ["order_id"]
      }
    }
  ] satisfies Anthropic.Beta.AgentCreateParams["tools"];
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic.Models.Beta.Agents;
  using Tool = Anthropic.Models.Beta.Agents.Tool;

  Tool[] tools =
  [
      new BetaManagedAgentsAgentToolset20260401Params
      {
          Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
          DefaultConfig = new()
          {
              Enabled = false,
              PermissionPolicy = new BetaManagedAgentsAlwaysAskPolicy { Type = "always_ask" },
          },
          Configs =
          [
              new BetaManagedAgentsReadToolConfigParams
              {
                  Enabled = true,
                  PermissionPolicy = new BetaManagedAgentsAlwaysAllowPolicy { Type = "always_allow" },
              },
              new BetaManagedAgentsWriteToolConfigParams
              {
                  Enabled = true,
                  PermissionPolicy = new BetaManagedAgentsAutoPolicy(),
              },
              new BetaManagedAgentsWebFetchToolConfigParams
              {
                  Enabled = true,
                  AllowedDomains = ["help.example.com"],
                  PermissionPolicy = new BetaManagedAgentsAutoPolicy(),
              },
          ],
      },
      new BetaManagedAgentsCustomToolParams
      {
          Type = "custom",
          Name = "lookup_order",
          Description = "Look up one order by its ID. Returns the status, the items, and the delivery date.",
          InputSchema = new()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["order_id"] = JsonSerializer.SerializeToElement(
                      new { type = "string", description = "The order ID from the ticket" }
                  ),
              },
              Required = ["order_id"],
          },
      },
  ];
  ```

  ```go Go
  tools := []anthropic.BetaAgentNewParamsToolUnion{{
  	OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  		Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		DefaultConfig: anthropic.BetaManagedAgentsAgentToolsetDefaultConfigParams{
  			Enabled: anthropic.Bool(false),
  			PermissionPolicy: anthropic.BetaManagedAgentsAgentToolsetDefaultConfigParamsPermissionPolicyUnion{
  				OfAlwaysAsk: &anthropic.BetaManagedAgentsAlwaysAskPolicyParam{
  					Type: anthropic.BetaManagedAgentsAlwaysAskPolicyTypeAlwaysAsk,
  				},
  			},
  		},
  		Configs: []anthropic.BetaManagedAgentsAgentToolConfigParamsUnion{
  			{OfRead: &anthropic.BetaManagedAgentsReadToolConfigParams{
  				Enabled: anthropic.Bool(true),
  				PermissionPolicy: anthropic.BetaManagedAgentsReadToolConfigParamsPermissionPolicyUnion{
  					OfAlwaysAllow: &anthropic.BetaManagedAgentsAlwaysAllowPolicyParam{
  						Type: anthropic.BetaManagedAgentsAlwaysAllowPolicyTypeAlwaysAllow,
  					},
  				},
  			}},
  			{OfWrite: &anthropic.BetaManagedAgentsWriteToolConfigParams{
  				Enabled: anthropic.Bool(true),
  				PermissionPolicy: anthropic.BetaManagedAgentsWriteToolConfigParamsPermissionPolicyUnion{
  					OfAuto: &anthropic.BetaManagedAgentsAutoPolicyParam{},
  				},
  			}},
  			{OfWebFetch: &anthropic.BetaManagedAgentsWebFetchToolConfigParams{
  				AllowedDomains: []string{"help.example.com"},
  				Enabled:        anthropic.Bool(true),
  				PermissionPolicy: anthropic.BetaManagedAgentsWebFetchToolConfigParamsPermissionPolicyUnion{
  					OfAuto: &anthropic.BetaManagedAgentsAutoPolicyParam{},
  				},
  			}},
  		},
  	},
  }, {
  	OfCustom: &anthropic.BetaManagedAgentsCustomToolParams{
  		Type:        anthropic.BetaManagedAgentsCustomToolParamsTypeCustom,
  		Name:        "lookup_order",
  		Description: "Look up one order by its ID. Returns the status, the items, and the delivery date.",
  		InputSchema: anthropic.BetaManagedAgentsCustomToolInputSchemaParam{
  			Properties: map[string]any{
  				"order_id": map[string]any{
  					"type":        "string",
  					"description": "The order ID from the ticket",
  				},
  			},
  			Required: []string{"order_id"},
  		},
  	},
  }}
  _ = tools
  ```

  ```java Java
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.beta.agents.*;
  import java.util.List;
  import java.util.Map;

  var tools = List.of(
      AgentCreateParams.Tool.ofAgentToolset20260401(
          BetaManagedAgentsAgentToolset20260401Params.builder()
              .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
              .defaultConfig(
                  BetaManagedAgentsAgentToolsetDefaultConfigParams.builder()
                      .enabled(false)
                      .permissionPolicy(
                          BetaManagedAgentsAlwaysAskPolicy.builder()
                              .type(BetaManagedAgentsAlwaysAskPolicy.Type.ALWAYS_ASK)
                              .build()
                      )
                      .build()
              )
              .addConfig(
                  BetaManagedAgentsReadToolConfigParams.builder()
                      .enabled(true)
                      .permissionPolicy(
                          BetaManagedAgentsAlwaysAllowPolicy.builder()
                              .type(BetaManagedAgentsAlwaysAllowPolicy.Type.ALWAYS_ALLOW)
                              .build()
                      )
                      .build()
              )
              .addConfig(
                  BetaManagedAgentsWriteToolConfigParams.builder()
                      .enabled(true)
                      .permissionPolicy(BetaManagedAgentsAutoPolicy.builder().build())
                      .build()
              )
              .addConfig(
                  BetaManagedAgentsWebFetchToolConfigParams.builder()
                      .enabled(true)
                      .allowedDomains(List.of("help.example.com"))
                      .permissionPolicy(BetaManagedAgentsAutoPolicy.builder().build())
                      .build()
              )
              .build()
      ),
      AgentCreateParams.Tool.ofCustom(
          BetaManagedAgentsCustomToolParams.builder()
              .type(BetaManagedAgentsCustomToolParams.Type.CUSTOM)
              .name("lookup_order")
              .description("Look up one order by its ID. Returns the status, the items, and the delivery date.")
              .inputSchema(
                  BetaManagedAgentsCustomToolInputSchema.builder()
                      .properties(
                          BetaManagedAgentsCustomToolInputSchema.Properties.builder()
                              .putAdditionalProperty("order_id", JsonValue.from(Map.of(
                                  "type", "string",
                                  "description", "The order ID from the ticket")))
                              .build()
                      )
                      .addRequired("order_id")
                      .build()
              )
              .build()
      )
  );
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolsetDefaultConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsAlwaysAllowPolicy;
  use Anthropic\Beta\Agents\BetaManagedAgentsAlwaysAskPolicy;
  use Anthropic\Beta\Agents\BetaManagedAgentsAutoPolicy;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolInputSchema;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsReadToolConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsWebFetchToolConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsWriteToolConfigParams;

  $tools = [
      BetaManagedAgentsAgentToolset20260401Params::with(
          type: 'agent_toolset_20260401',
          defaultConfig: BetaManagedAgentsAgentToolsetDefaultConfigParams::with(
              enabled: false,
              permissionPolicy: BetaManagedAgentsAlwaysAskPolicy::with(type: 'always_ask'),
          ),
          configs: [
              BetaManagedAgentsReadToolConfigParams::with(
                  enabled: true,
                  permissionPolicy: BetaManagedAgentsAlwaysAllowPolicy::with(type: 'always_allow'),
              ),
              BetaManagedAgentsWriteToolConfigParams::with(
                  enabled: true,
                  permissionPolicy: BetaManagedAgentsAutoPolicy::with(),
              ),
              BetaManagedAgentsWebFetchToolConfigParams::with(
                  allowedDomains: ['help.example.com'],
                  enabled: true,
                  permissionPolicy: BetaManagedAgentsAutoPolicy::with(),
              ),
          ],
      ),
      BetaManagedAgentsCustomToolParams::with(
          type: 'custom',
          name: 'lookup_order',
          description: 'Look up one order by its ID. Returns the status, the items, and the delivery date.',
          inputSchema: BetaManagedAgentsCustomToolInputSchema::with(
              properties: ['order_id' => ['type' => 'string', 'description' => 'The order ID from the ticket']],
              required: ['order_id'],
          ),
      ),
  ];
  ```

  ```ruby Ruby
  tools = [
    {
      type: "agent_toolset_20260401",
      default_config: {
        enabled: false,
        permission_policy: {type: "always_ask"}
      },
      configs: [
        {
          name: "read",
          enabled: true,
          permission_policy: {type: "always_allow"}
        },
        {
          name: "write",
          enabled: true,
          permission_policy: {type: "auto"}
        },
        {
          name: "web_fetch",
          enabled: true,
          allowed_domains: ["help.example.com"],
          permission_policy: {type: "auto"}
        }
      ]
    },
    {
      type: "custom",
      name: "lookup_order",
      description: "Look up one order by its ID. Returns the status, the items, and the delivery date.",
      input_schema: {
        type: "object",
        properties: {order_id: {type: "string", description: "The order ID from the ticket"}},
        required: ["order_id"]
      }
    }
  ]
  ```
</CodeGroup>

[Pembaruan agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-semantics) menggantikan seluruh array `tools`, jadi kirimkan setiap entri yang ingin Anda pertahankan.

Pembaruan agen hanya menjangkau sesi baru, jadi periksa juga deployment, agen yang mencantumkan agen ini, dan sesi yang sudah ada:

* Deployment menyematkan versi agen, jadi arahkan setiap deployment ke versi yang baru.
* Agen yang mencantumkan agen ini di [`subagents.predefined_agents`](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#list-the-subagents) atau `workflows.predefined_agents` mempertahankan versi yang disematkannya, jadi perbarui agen tersebut juga.
* Untuk memperketat sesi yang sudah ada, [perbarui alat sesi tersebut](https://platform.claude.com/docs/id/managed-agents/session-operations#updating-the-agent-configuration). Sesi harus dalam status `idle`, dan pembaruan menggantikan seluruh array `tools`. Dalam sesi multiagen, daftar `allowed_domains` dan `blocked_domains` baru pada alat web agen yang dijalankan sesi juga berlaku untuk setiap agen lainnya. Daftar tersebut berlaku mulai giliran berikutnya dari setiap agen. Alat yang diaktifkan dan kebijakan izin agen-agen tersebut tidak berubah. Untuk mengubahnya, perbarui setiap agen, lalu mulai sesi baru.

Batasi juga server MCP dan alat kustom sesuai kebutuhan agen:

* **Server MCP:** Toolset MCP mengaktifkan setiap alat yang diekspos server secara default. Tetapkan `default_config.enabled` ke `false` dan aktifkan alat yang disebutkan namanya, sehingga alat yang ditambahkan server kemudian tetap nonaktif. Hapus server yang tidak digunakan agen. Lihat [Konektor MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector#configure-which-mcp-tools-are-available).
* **Alat kustom:** Aplikasi Anda yang menjalankannya, dan kebijakan izin tidak berlaku. Validasi input setiap panggilan di aplikasi Anda dan batasi apa yang dapat disentuh alat tersebut.

## Jauhkan input tidak tepercaya dari alat yang kuat

Periksa alat dan kredensial mana yang dimiliki agen setiap kali agen membaca input tidak tepercaya, yaitu teks yang dapat ditulis oleh seseorang di luar tim Anda. Bagian ini menggunakan dua istilah:

* **Input tidak tepercaya:** Halaman web, hasil pencarian, tiket dukungan, email, file repositori, unggahan, hasil server MCP, dan pesan pengguna akhir yang Anda teruskan.
* **Alat yang kuat:** `bash`, `write`, `edit`, `web_fetch`, `web_search`, alat MCP dan alat kustom yang menulis atau mengirim data, serta alat apa pun yang menggunakan kredensial.

Teks dalam input tidak tepercaya dapat memerintahkan agen untuk menggunakan alat kuat yang dimilikinya. Agen dukungan membaca tiket, sehingga agen ini menjangkau API pesanan Anda hanya melalui alat kustom `lookup_order`. Aplikasi Anda memeriksa bahwa pesanan tersebut milik pengirim tiket.

| Input yang dibaca agen           | Kemampuan yang juga dimilikinya                                                                                         | Lakukan ini                                                                                                                                                                                                                                                                                                         |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tiket, email, atau unggahan      | `bash` dengan kredensial                                                                                                | Ganti `bash` dengan alat kustom yang melakukan satu hal. Jika agen harus tetap memiliki `bash`, setujui setiap panggilan dengan `always_ask`                                                                                                                                                                        |
| Halaman web atau hasil pencarian | Menulis file atau mengubah catatan                                                                                      | Nonaktifkan alat web, atau batasi ke situs yang Anda operasikan atau percayai                                                                                                                                                                                                                                       |
| Hasil MCP atau file repositori   | Alat MCP yang menulis                                                                                                   | Pertahankan toolset MCP pada `always_ask`, dan aktifkan hanya alat yang dibutuhkan agen                                                                                                                                                                                                                             |
| Repositori GitHub yang di-mount  | Alat apa pun                                                                                                            | Mount hanya repositori yang Anda percayai. Agen dengan `read` memuat skill dari direktori `.claude/skills` repositori sebagai instruksi agen, tanpa langkah peninjauan. Lihat [Memuat skill dari repositori GitHub](https://platform.claude.com/docs/id/managed-agents/skills#load-skills-from-a-github-repository) |
| Input tidak tepercaya apa pun    | Menulis ke [memory store](https://platform.claude.com/docs/id/managed-agents/memory#attach-a-memory-store-to-a-session) | Lampirkan store sebagai `read_only` kecuali agen harus menulis. Default-nya adalah `read_write`, dan sesi berikutnya membaca teks yang disimpan sebagai memori tepercaya                                                                                                                                            |

Dalam environment cloud, membaca file dengan `read` juga dapat memuat file `CLAUDE.md` dan `AGENTS.md` sebagai instruksi. File tersebut dimuat dari direktori file dan direktori induknya, hingga direktori kerja sandbox. File yang direferensikannya dengan `@` dan sebuah path, seperti `@docs/setup.md`, juga dimuat, hingga kedalaman lima referensi. Referensi dapat menunjuk ke mana saja di sandbox, misalnya `@/etc/hosts`. Tidak ada pengaturan yang menonaktifkan ini selain menonaktifkan `read`, jadi perlakukan repositori, paket, atau arsip yang dapat ditulis oleh seseorang di luar tim Anda sebagai input tidak tepercaya.

Ketika agen harus membaca input tidak tepercaya sekaligus bertindak, panduan ini merekomendasikan salah satu dari tiga desain:

* **Pisahkan membaca dari bertindak.** Dalam satu sesi multiagen, [agen utama](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#list-the-subagents) memberikan tugas kepada fetcher, yang membaca web, dan writer, yang mengubah file atau catatan.
* **Berikan agen satu alat kustom yang sempit.** Aplikasi Anda menjalankan alat tersebut, memeriksa inputnya, dan memegang kredensial. Agen dukungan menggunakan desain ini, bukan pemisahan. Lihat [Menjawab panggilan alat yang menjeda sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#answer-tool-calls-that-pause-the-session).
* **Libatkan seseorang dalam prosesnya.** Gunakan `always_ask` pada alat yang kuat sehingga seseorang menyetujui setiap panggilan.

Pemisahan menggunakan tiga agen:

| Agen                              | Membaca                                                 | Memegang                                                                                                           | Meneruskan                                                      |
| --------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| Utama (agen yang dijalankan sesi) | Pesan Anda, dan apa yang dikirim kembali oleh agen lain | Tidak ada alat bawaan. Daftar `subagents.predefined_agents`-nya menyebutkan fetcher dan writer                     | Tugas untuk setiap agen                                         |
| Fetcher                           | Halaman web dan hasil pencarian                         | Hanya `web_fetch` dan `web_search`, masing-masing dengan `allowed_domains`                                         | Hasil singkat, dalam format yang Anda minta di prompt sistemnya |
| Writer                            | Tugas dari agen utama                                   | Alat yang menulis file, menjalankan perintah, atau mengubah catatan, pada `auto` atau `always_ask`. Tanpa alat web | Hasilnya                                                        |

Hasil fetcher dibangun dari halaman tidak tepercaya, dan agen utama dapat meneruskan teksnya ke writer. Pertahankan `auto` atau `always_ask` pada alat writer. Fetcher masih dapat mengirim sebagian dari apa yang dibacanya ke situs dalam daftar `web_fetch`-nya, dan ke penyedia pencarian dalam kuerinya.

Agen dalam satu sesi multiagen [berbagi sandbox](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#how-it-works), file-nya, dan kredensial vault, sehingga pemisahan ini hanya memisahkan alat dan percakapan mereka. Untuk pemisahan yang lebih kuat, gunakan dua sesi dengan environment dan vault terpisah. Minta aplikasi Anda hanya meneruskan field tetap, seperti ID pesanan, di antara kedua sesi.

## Tetapkan batas dan cara untuk menghentikan

Tetapkan anggaran saat Anda membuat setiap sesi, dan tentukan sebelumnya bagaimana Anda menghentikan agen.

| Kontrol                                                                                                               | Fungsinya                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Anggaran sesi                                                                                                         | Batas pengeluaran berdasarkan harga daftar publik. Saat mencapai batas, sesi dan setiap [thread](https://platform.claude.com/docs/id/managed-agents/session-threads) dijeda. Permintaan yang sedang berlangsung dapat selesai dan panggilan alatnya tetap berjalan, sehingga pengeluaran dapat melewati batas. Lihat [Ketika sesi mencapai anggarannya](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget) |
| Anggaran deployment                                                                                                   | Batas yang sama, diterapkan pada setiap sesi yang dimulai deployment                                                                                                                                                                                                                                                                                                                                                                                  |
| [Event `user.interrupt`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#interrupt-the-agent) | Menghentikan respons model segera. Panggilan alat yang sedang berjalan dapat selesai terlebih dahulu. Sesi menjadi `idle`, kecuali eksekusi workflow membuatnya tetap `running`, dan dilanjutkan pada pesan Anda berikutnya. Interupsi tidak mengakhiri eksekusi workflow                                                                                                                                                                             |
| Arsipkan atau hapus sesi                                                                                              | Pengarsipan menyimpan riwayat dan memblokir event baru. Penghapusan menghapus catatan, event, dan sandbox                                                                                                                                                                                                                                                                                                                                             |
| Jeda atau arsipkan deployment                                                                                         | Penjedaan menghentikan eksekusi terjadwal baru tetapi tetap mengizinkan eksekusi manual. Pengarsipan mengakhiri jadwal secara permanen. Sesi yang sudah berjalan tetap berjalan                                                                                                                                                                                                                                                                       |
| Arsipkan atau hapus vault atau kredensial                                                                             | Menghapus rahasia dari sesi yang sedang berjalan tanpa restart. Perhitungkan adanya penundaan. Sesi tetap berjalan, jadi interupsi juga sesi tersebut. Token yang sudah diambil agen dengan rahasia tersebut tetap berada di sandbox                                                                                                                                                                                                                  |

Untuk menghentikan agen yang sedang berjalan, ikuti langkah-langkah berikut:

1. Kirim `user.interrupt` saja.
2. Untuk agen terjadwal, jeda juga deployment agar tidak ada eksekusi terjadwal baru yang dimulai. Untuk mengakhiri jadwal secara permanen, arsipkan deployment.
3. Jika sebuah kunci mungkin terekspos, rotasikan kunci tersebut di layanan yang menerbitkannya.
4. Jika agen memiliki eksekusi workflow yang terbuka, kirim juga `user.message` yang memintanya menghentikan eksekusi tersebut, karena interupsi tidak mengakhiri eksekusi. Lihat [Menginterupsi sesi dengan eksekusi yang terbuka](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open) untuk panggilan alat yang perlu dibatalkan terlebih dahulu.
5. Tunggu hingga sesi menjadi `idle`. Sesi yang sedang berjalan tidak dapat diarsipkan atau dihapus.
6. Arsipkan sesi untuk menyimpan riwayatnya. Hapus sesi saat Anda tidak lagi memerlukan riwayatnya.

Interupsi tidak membatalkan apa yang sudah dilakukan atau dikirim agen. Mengarsipkan agen tidak menghentikan sesinya yang sedang berjalan.

`max_list_cost.amount` pada anggaran adalah bilangan bulat dalam sen AS yang ditulis sebagai string, sehingga `"125"` berarti $1,25. Lihat [Menetapkan anggaran saat pembuatan sesi](https://platform.claude.com/docs/id/managed-agents/budgets#set-a-budget-at-session-creation).

Anda tidak dapat menambahkan anggaran ke sesi yang dibuat tanpa anggaran. Untuk mengubah atau menghapus batas, lihat [Melanjutkan sesi yang mencapai anggarannya](https://platform.claude.com/docs/id/managed-agents/budgets#resume-a-session-at-its-budget). Setelah Anda menghapus batas sesi, Anda tidak dapat menetapkan batas baru.

Anggaran membatasi pengeluaran, tetapi tidak membatasi apa yang dilakukan agen sebelum mencapai batas. Untuk memisahkan beban kerja dengan tingkat kepercayaan berbeda, gunakan [workspace](https://platform.claude.com/docs/id/manage-claude/workspaces) terpisah. Batasi setiap beban kerja ke satu workspace: jika memungkinkan, aturan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) yang diaktifkan hanya di workspace tersebut, jika tidak, kunci API yang cakupannya terbatas pada workspace tersebut. Akses ke beberapa workspace memungkinkan beban kerja bertindak di workspace mana pun di antaranya.

Lihat [Anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets), [Operasi sesi](https://platform.claude.com/docs/id/managed-agents/session-operations#archiving-a-session), dan [Deployment terjadwal](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments#managing-deployment-lifecycle).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Penyiapan environment cloud" icon="cloud" href="https://platform.claude.com/docs/id/managed-agents/environments">
    Mode jaringan, host yang diizinkan, dan package manager.
  </Card>

  <Card title="Kebijakan izin" icon="check" href="https://platform.claude.com/docs/id/managed-agents/permission-policies">
    Kebijakan persetujuan dan permintaan konfirmasi.
  </Card>

  <Card title="Autentikasi dengan vault" icon="lock" href="https://platform.claude.com/docs/id/managed-agents/vaults">
    Jenis kredensial, lokasi injeksi, dan rotasi.
  </Card>

  <Card title="Anggaran sesi" icon="coins" href="https://platform.claude.com/docs/id/managed-agents/budgets">
    Batas, melanjutkan pada anggaran, dan anggaran pada deployment.
  </Card>
</CardGroup>
