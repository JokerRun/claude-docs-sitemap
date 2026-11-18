---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections
fetched_at: 2026-11-18T02:14:00.973041Z
sha256: 8fbcd0824bb3ed3faf409f9d629ff81b9f0c55bf71bbd53b12bedb0f38d6c336
---

---
title: Linked billing
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections
description: Izinkan pelanggan Anda menautkan organisasi Claude Platform mereka ke aplikasi Anda dengan OAuth, dan tagihkan penggunaan Claude ke organisasi pelanggan.
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Fitur ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Linked billing memungkinkan pelanggan Anda membayar penggunaan Claude di aplikasi Anda melalui organisasi Claude mereka sendiri. Pelanggan menautkan organisasi Claude mereka ke aplikasi Anda satu kali. API menyebut tautan ini sebagai koneksi. Setelah pelanggan menautkan, Anda memilih pada setiap permintaan Claude API apakah pelanggan atau Anda yang membayar. Pelanggan dapat membatalkan tautan aplikasi Anda kapan saja. Jika permintaan yang Anda tandai untuk pelanggan tidak dapat ditagihkan kepada mereka, Claude API akan menolaknya alih-alih menagih Anda.

Panduan ini ditujukan bagi pengembang yang pengguna aplikasinya sebagian besar adalah pelanggan Claude Platform. Anda menambahkan tombol “Link your Claude organization” ke aplikasi Anda. Pengguna Anda mengkliknya, masuk ke Claude, dan menyetujui aplikasi Anda untuk menagih organisasi Claude mereka atas permintaan Claude API yang diarahkan pelanggan untuk Anda buat. Aplikasi Anda kemudian menambahkan field [`billing_policy`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#step-3-update-calls-to-claude) ke permintaan yang dibayar oleh pelanggan.

## Pelanggan dan endpoint yang memenuhi syarat

**Pelanggan yang memenuhi syarat:** Pelanggan dapat ditagih dengan cara ini hanya jika organisasi Claude Platform mereka membayar Anthropic secara langsung untuk penggunaan API-nya. Kredit prabayar dan penagihan berbasis faktur sama-sama termasuk. Organisasi yang ditagih melalui marketplace cloud (AWS, Google Cloud, atau Azure) tidak dapat ditagih melalui integrasi ini. Hal yang sama berlaku untuk organisasi yang hanya memiliki paket langganan Claude. Permintaan untuk mereka ditolak dengan 403 `user_profile_not_billable`.

Permintaan berjalan di organisasi Anda, sehingga “rate limit” (batas laju), akses model, tingkat layanan, retensi data, dan kunci enkripsi Anda yang berlaku. Pengaturan data milik pelanggan Anda sendiri tidak berlaku untuk permintaan ini, termasuk [“zero data retention” (retensi data nol), atau ZDR](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope), “business associate agreement” (perjanjian rekanan bisnis), atau BAA, dan “customer-managed encryption keys” (kunci enkripsi yang dikelola pelanggan), atau CMEK. Jangan tautkan pelanggan yang memerlukan cakupan HIPAA, FERPA, atau CMEK untuk penggunaan ini.

**Endpoint yang didukung:** `billing_policy` didukung pada:

* `/v1/messages`
  * Keterbatasan yang diketahui: permintaan yang menagih pelanggan Anda (`bill_to: "user_profile"`) tidak dapat menggunakan [fitur eksekusi kode yang dapat ditagih](https://platform.claude.com/docs/id/about-claude/pricing#code-execution-tool) (API mengembalikan 400), jadi kirim permintaan tersebut dengan `bill_to: "self"` atau tanpa `billing_policy`.
* `/v1/chat/completions`
* `/v1/messages/count_tokens` menerima field `billing_policy` dan mengabaikannya, sehingga Anda dapat menghitung token pada body persis yang akan Anda kirim.

[Message Batches](https://platform.claude.com/docs/id/build-with-claude/batch-processing) (`/v1/messages/batches`) saat ini belum mendukung penagihan ke pelanggan Anda. Kirim permintaan dalam batch dengan `bill_to: "self"` atau tanpa `billing_policy`, dan permintaan tersebut akan ditagihkan kepada Anda seperti biasa. Permintaan dalam batch yang menetapkan `bill_to: "user_profile"` akan ditolak: hasilnya adalah `errored` dengan `invalid_request_error`, baik Anda maupun pelanggan Anda tidak ditagih untuk permintaan tersebut, dan permintaan lain dalam batch tetap berjalan seperti biasa.

Untuk meminta dukungan pada endpoint lain, hubungi tim akun Anthropic Anda.

### Kredit yang dapat membayar

Tidak semua kredit dapat membayar permintaan yang ditagihkan platform ke pelanggan. Apa yang dapat membayar bergantung pada organisasi yang ditagih: pelanggan jika Anda menagih pelanggan, atau organisasi Anda jika sebuah platform menagih Anda.

Kredit yang dibeli di Claude Console untuk organisasi tersebut dapat membayar permintaan ini. Jika organisasi tersebut menggunakan penagihan berbasis faktur, organisasi tersebut akan ditagih melalui faktur untuk permintaan ini.

Sebagian kredit promosi dari Anthropic tidak dapat membayar permintaan ini. Termasuk di antaranya kredit API bulanan yang disertakan dengan paket Claude Max, Ultra, dan Team. Kredit dari program mitra, VC, dan startup Anthropic tidak memenuhi syarat untuk membayar permintaan ini.

Ketika tidak ada apa pun di akun organisasi tersebut yang dapat membayar suatu permintaan, Claude API dapat menolaknya dengan 402. Respons tidak menyebutkan apakah penolakan tersebut disebabkan oleh kurangnya kredit atau batas pengeluaran. Lihat [Error yang diharapkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#expected-errors).

## Proses penyiapan

Anda melakukan tiga langkah ini satu kali. Langkah-langkah ini mendaftarkan aplikasi Anda ke Anthropic. Setelahnya, [Profil pengguna mana yang ditautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#which-user-profile-to-link) menjelaskan aturan yang perlu Anda ketahui sebelum membuat profil pengguna.

### Langkah 1: Buat aplikasi

Buat aplikasi OAuth di Claude Console. Aplikasi ini adalah pendaftaran yang mengidentifikasi produk Anda kepada Anthropic: aplikasi ini mengaitkan redirect URI Anda dengan client ID, dan namanya adalah yang dilihat pengguna Anda di halaman persetujuan.

Anggota organisasi Anda dengan peran Admin membuka halaman [aplikasi OAuth](https://platform.claude.com/settings/oauth-apps) di Console dan mengklik **Create**. Masukkan nama aplikasi Anda dan redirect URI (alamat di aplikasi Anda tempat browser kembali setelah persetujuan). Di bawah **What the app can do**, pilih **Bill and link to organizations**.

Halaman aplikasi baru akan terbuka. Salin client ID yang ditampilkan Console untuk aplikasi tersebut. Aplikasi Anda mengirimkannya di Langkah 5 saat meminta halaman persetujuan, di Langkah 6 saat mengalihkan browser, dan di Langkah 8 saat menukarkan kode, sehingga Anthropic mengetahui aplikasi mana yang meminta. Client ID bersifat publik. Pada tab **Appearance**, atur nama, halaman beranda, dan URL logo aplikasi Anda.

Pada tab **Settings**, **Who can link** bertuliskan **Test users only** untuk aplikasi baru, yang dimulai dalam mode pengujian. Setelah Anda [memublikasikan aplikasi Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#publish-your-app) dan aplikasi tersebut aktif, pengaturan tersebut bertuliskan **Any Claude user**.

<Note>
  Sebuah organisasi dapat mendaftarkan beberapa aplikasi OAuth, misalnya satu untuk produksi dan satu untuk pengujian. Setiap aplikasi memiliki koneksinya sendiri: pelanggan yang menautkan aplikasi pengujian Anda tidak tertaut ke aplikasi produksi Anda. Pertahankan Linked billing pada satu aplikasi produksi selama masa pakai integrasi Anda.
</Note>

### Langkah 2: Siapkan autentikasi klien

Siapkan cara back end Anda membuktikan kepada `auth.claude.com` bahwa permintaannya berasal dari aplikasi Anda. Ini menggantikan client secret: Anthropic tidak menerbitkan client secret untuk aplikasi OAuth.

Pada tab **Client authentication** aplikasi, pilih **Identity provider** Anda (penerbit yang menandatangani token back end Anda). Untuk menambahkannya, klik **Register a new issuer**. Kemudian atur **Subject pattern**, atau kondisi klaim di bawah **Advanced match options**, yang harus dipenuhi oleh token tersebut. Setelah Anda menyimpan, tab tersebut menampilkan audience yang diharapkan. Klaim `aud` pada client assertion Anda harus persis bernilai tersebut.

<Note>
  Aplikasi Anda melakukan autentikasi ke endpoint PAR, token, dan pencabutan dengan variasi metode `private_key_jwt` (RFC 7523): pada setiap permintaan, back end Anda mengirimkan “client assertion” (asersi klien), yaitu JWT yang diterbitkan oleh penyedia identitas Anda. `auth.claude.com` memeriksa tanda tangan token dengan kunci yang terdaftar untuk penerbit tersebut, dan mencocokkannya dengan kondisi subject atau klaim yang Anda atur di sini. Untuk klaim yang harus dimuat oleh client assertion, lihat [Klaim client assertion](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#client-assertion-claims).
</Note>

### Langkah 3: Siapkan identitas back end Anda

Back end Anda memerlukan identitasnya sendiri untuk memanggil Claude API. Buat dua hal:

* **“Service account” (akun layanan).** Ini adalah akun non-manusia di organisasi Claude Anda. Back end Anda melakukan autentikasi sebagai akun ini saat memanggil Claude API.
* **Aturan federasi kedua.** Seperti aturan untuk autentikasi klien aplikasi di Langkah 2, aturan ini memungkinkan back end Anda melakukan autentikasi dengan token dari penyedia identitas Anda sendiri.

Untuk menyiapkannya di Claude Console, ikuti panduan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation).

Kemudian, pada tab **Client authentication** aplikasi, pilih akun layanan tersebut sebagai akun layanan operator aplikasi. Hanya akun layanan tersebut yang berwenang mengirim permintaan inferensi dan mengatribusikan penagihan ke profil pengguna yang tertaut. Sebuah akun layanan hanya dapat menjadi operator untuk satu aplikasi OAuth.

Secara default, setiap permintaan yang diautentikasi sebagai akun layanan tersebut dapat menagih setiap pelanggan yang tertaut, dengan mengatur header profil pengguna dan `bill_to` di Messages API. Untuk mendapatkan token autentikasi yang dibatasi hanya pada koneksi tertentu, lihat [Token OAuth untuk setiap koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#oauth-tokens-for-each-connection). Sebelum Anda menautkan pelanggan, [atur workspace](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#settings-for-a-connections-oauth-tokens) untuk aplikasi Anda. Langkah 8 mengembalikan token semacam itu untuk setiap pelanggan, dan mengharuskan aplikasi menentukan workspace default di organisasi Anda tempat inferensi dijalankan. Jika Anda menginginkan “refresh token” (token penyegaran) untuk setiap koneksi, aktifkan juga **Offline access** untuk aplikasi Anda. Lalu minta `offline_access` dalam alur otorisasi, di Langkah 5, sebelum Anda menautkan pelanggan.

### Profil pengguna mana yang ditautkan

“User profile” (profil pengguna) adalah catatan di organisasi Claude Anda sendiri yang mewakili salah satu pelanggan Anda. Setiap permintaan yang menagih pelanggan menyertakan ID profil tersebut, sehingga Anthropic mengetahui pelanggan mana yang harus ditagih. Untuk fungsi profil lainnya, lihat [Profil pengguna untuk atribusi pelanggan akhir](https://platform.claude.com/docs/id/manage-claude/user-profiles).

Tetapkan profil pengguna mana yang mewakili setiap pelanggan sebelum Anda menautkan pelanggan pertama Anda. Dalam satu aplikasi, koneksi bersifat satu-ke-satu:

* Organisasi Claude pelanggan hanya dapat ditautkan ke satu profil pengguna Anda.
* Profil pengguna hanya dapat ditautkan ke satu organisasi Claude.

Organisasi Claude pelanggan adalah organisasi yang dipilih pengguna saat menyetujui aplikasi Anda. Untuk mengetahui bagaimana tim-tim pelanggan menggunakan organisasi Claude, tanyakan kepada pelanggan. Untuk menerapkan aturan satu-ke-satu pada catatan pelanggan Anda:

* **Beberapa tim dari satu pelanggan berbagi satu organisasi Claude:** Gunakan satu profil pengguna untuk semua tim tersebut.
* **Setiap tim memiliki organisasi Claude sendiri:** Buat profil pengguna untuk setiap organisasi.

Profil pengguna aktif mana pun di organisasi Anda dapat ditautkan, selama aturan satu-ke-satu terpenuhi. Menautkan tidak mengubah profil tersebut, ID-nya, maupun riwayat penggunaannya. Jika Anda menautkan profil pengguna kedua ke organisasi Claude yang sudah tertaut, persetujuan akan ditolak: lihat [`user_profile_already_linked`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#user-profile-already-linked).

#### Profil pengguna untuk setiap orang

Anda mungkin sudah memiliki profil pengguna untuk setiap orang yang menggunakan produk Anda. Beberapa di antara orang-orang tersebut mungkin bekerja untuk pelanggan yang sama. Dalam hal itu, Anthropic menyarankan agar Anda membuat satu profil pengguna lagi untuk organisasi Claude pelanggan dan menautkan profil tersebut.

ID profil yang dikirim bergantung pada siapa yang membayar permintaan:

* **Permintaan yang Anda tagihkan ke pelanggan:** Kirim ID profil pelanggan. Untuk juga mengidentifikasi orang tersebut pada permintaan `/v1/messages`, atur [`metadata.user_id`](https://platform.claude.com/docs/id/api/messages/create) ke pengenal untuk orang tersebut. Pengenal ini bersifat opsional, dan membantu Anthropic mendeteksi penyalahgunaan oleh satu orang. Gunakan nilai yang buram (opaque), bukan nama, alamat email, atau nomor telepon.
* **Permintaan yang Anda bayar:** Anda tetap dapat mengirim ID profil milik orang tersebut.

## Tautkan setiap pelanggan

Anda melakukan Langkah 4 hingga 8 untuk setiap pelanggan yang menautkan organisasinya. Cuplikan kode Python berikut memerlukan Anthropic SDK dan beberapa import standar; lihat [Inisialisasi cuplikan kode](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#code-snippet-initialization). Contoh dalam bahasa lain dan CLI mengambil kredensialnya dari environment. Pastikan `ANTHROPIC_API_KEY` tidak diatur, karena aplikasi Anda perlu melakukan autentikasi dengan Workload Identity Federation.

Tambahkan tombol “Link your Claude organization” di tempat pelanggan Anda mengelola penagihan atau integrasi di produk Anda (untuk HTML, warna, dan logo tombol, lihat [Contoh branding](https://platform.claude.com/docs/id/manage-claude/oauth-apps/branding-samples#buttons)). Beri tahu mereka bahwa untuk menautkan, mereka harus memiliki peran Admin atau Billing di organisasi Claude mereka.

Untuk menjalankan langkah-langkah ini sendiri terlebih dahulu, lihat [Menguji sebagai pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#test-as-a-customer).

<Frame>
  ![Diagram urutan Langkah 5 hingga 8: "approval request" (permintaan persetujuan), "user's approval" (persetujuan pengguna), dan "exchange for a connection ID" (penukaran untuk ID koneksi)](https://platform.claude.com/docs/id/images/oauth-apps-billing-connection-flow.svg)
</Frame>

### Langkah 4: Buat profil pengguna untuk pelanggan

Buat satu profil pengguna untuk setiap organisasi Claude pelanggan, dan simpan ID profil tersebut pada catatan pelanggan di produk Anda.

Jika Anda sudah memiliki profil pengguna untuk organisasi Claude pelanggan ini, lewati langkah ini dan gunakan ID profil tersebut. Untuk menentukan profil mana itu, lihat [Profil pengguna mana yang ditautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#which-user-profile-to-link).

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/user_profiles \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "content-type: application/json" \
    -d '{
      "name": "Example Customer Inc.",
      "external_user_details": {"reference_id": "your-customer-id-123"}
    }'
  ```

  ```bash CLI
  ant user-profiles create \
    --name "Example Customer Inc." \
    --external-user-details.reference-id your-customer-id-123
  ```

  ```python Python
  def create_user_profile(name: str, customer_id: str) -> str:
      profile = client.user_profiles.create(
          name=name,
          external_user_details={"reference_id": customer_id},
      )
      return profile.id  # "uprof_..."


  user_profile_id = create_user_profile("Example Customer Inc.", "your-customer-id-123")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const profile = await client.userProfiles.create({
    name: "Example Customer Inc.",
    external_user_details: { reference_id: "your-customer-id-123" }
  });

  console.log(profile.id); // "uprof_..."
  ```

  ```csharp C#
  AnthropicClient client = new();

  var profile = await client.UserProfiles.Create(
      new()
      {
          Name = "Example Customer Inc.",
          ExternalUserDetails = new() { ReferenceID = "your-customer-id-123" },
      }
  );

  Console.WriteLine(profile.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  profile, err := client.UserProfiles.New(context.Background(), anthropic.UserProfileNewParams{
  	Name: anthropic.String("Example Customer Inc."),
  	ExternalUserDetails: anthropic.UserProfileExternalUserDetailsParams{
  		ReferenceID: anthropic.String("your-customer-id-123"),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(profile.ID)
  ```

  ```java Java
  import com.anthropic.models.userprofiles.UserProfileCreateParams;
  import com.anthropic.models.userprofiles.UserProfileExternalUserDetailsParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UserProfileCreateParams.builder()
          .name("Example Customer Inc.")
          .externalUserDetails(UserProfileExternalUserDetailsParams.builder()
              .referenceId("your-customer-id-123")
              .build())
          .build();
      var profile = client.userProfiles().create(params);

      IO.println(profile.id());
  }
  ```

  ```php PHP
  $client = new Client();

  $profile = $client->userProfiles->create(
      name: 'Example Customer Inc.',
      externalUserDetails: ['referenceID' => 'your-customer-id-123'],
  );

  echo $profile->id, PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  profile = client.user_profiles.create(
    name: "Example Customer Inc.",
    external_user_details: { reference_id: "your-customer-id-123" }
  )

  puts(profile.id)
  ```
</CodeGroup>

Jika organisasi Anda menjual kembali akses API, kirim juga `"access_type": "passthrough"` saat Anda membuat profil ini. Contoh-contoh ini tidak menyertakan `access_type`, sehingga membuat profil `application`. Untuk kedua jenis tersebut, lihat [Tentukan siapa yang mendapatkan profil](https://platform.claude.com/docs/id/manage-claude/user-profiles#decide-who-gets-a-profile).

Respons berisi `id` profil, misalnya `uprof_01HV9Z`.

<Note>
  Setiap permintaan pembuatan menghasilkan profil baru, bahkan dengan `reference_id` yang sama (ID Anda sendiri untuk pelanggan), jadi gunakan kembali ID yang tersimpan alih-alih membuat profil pada setiap upaya koneksi.
</Note>

### Langkah 5: Buat URL pushed authorization request

Buat “pushed authorization request” (permintaan otorisasi yang didorong) yang mereferensikan profil pengguna pelanggan dari Langkah 4. Respons memberi Anda sebuah `request_uri`. Di langkah berikutnya, Anda menggunakannya untuk mengarahkan pengguna Anda ke halaman persetujuan.

Sebelum mengirim permintaan, back end Anda membuat dua nilai acak dan menyimpannya pada sesi browser dan catatan pelanggan. Back end menggunakan keduanya lagi di Langkah 8:

* Nilai `state`, yang memungkinkan Anda memeriksa bahwa browser yang kembali ke aplikasi Anda adalah browser yang memulai permintaan ini.
* PKCE code verifier, yaitu rahasia yang hanya diketahui oleh back end Anda. Permintaan membawa hash darinya (code challenge), dan Langkah 8 mengirimkan verifier itu sendiri, sehingga hanya back end Anda yang dapat menggunakan kode yang dikembalikan.

<CodeGroup exclude="shell:CLI, typescript, csharp, go, java, php, ruby">
  ```bash cURL
  curl https://auth.claude.com/v1/oauth/par \
    -H "content-type: application/json" \
    -d '{
      "response_type": "code",
      "client_id": "YOUR_CLIENT_ID",
      "redirect_uri": "https://app.example.com/claude/billing/callback",
      "scope": "billing:attribution",
      "connection_type": "organization_shared",
      "connection_auth_target": "platform",
      "user_profile_id": "uprof_01HV9Z",
      "state": "RANDOM_STATE",
      "code_challenge": "BASE64URL_SHA256_OF_VERIFIER",
      "code_challenge_method": "S256",
      "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      "client_assertion": "YOUR_CLIENT_ASSERTION_JWT"
    }'
  ```

  ```python Python
  def push_authorization_request(user_profile_id: str) -> dict:
      state = secrets.token_urlsafe(32)
      code_verifier = secrets.token_urlsafe(64)
      code_challenge = create_s256_code_challenge(code_verifier)

      response = httpx.post(
          f"{AUTH}/v1/oauth/par",
          json={
              "response_type": "code",
              "client_id": CLIENT_ID,
              "redirect_uri": REDIRECT_URI,
              "scope": "billing:attribution",
              "connection_type": "organization_shared",
              "connection_auth_target": "platform",
              "user_profile_id": user_profile_id,
              "state": state,
              "code_challenge": code_challenge,
              "code_challenge_method": "S256",
              "client_assertion_type": JWT_BEARER,
              "client_assertion": client_assertion(),
          },
      )
      response.raise_for_status()  # on an error, do not redirect the browser

      return {
          "state": state,
          "code_verifier": code_verifier,
          "request_uri": response.json()["request_uri"],  # valid for 600 seconds
          "user_profile_id": user_profile_id,
      }


  par = push_authorization_request(user_profile_id)
  ```
</CodeGroup>

`auth.claude.com` merespons dengan HTTP 201, sebuah `request_uri`, dan `expires_in` sebesar 600 detik. `request_uri` mengidentifikasi halaman persetujuan untuk permintaan ini. `scope` harus persis `billing:attribution` atau `billing:attribution offline_access`. Lihat [Scope untuk koneksi penagihan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#scopes-for-a-billing-connection) untuk detailnya. Contoh-contoh mengirimkan `billing:attribution`. Jika aplikasi Anda tidak memiliki scope ini, tambahkan di bawah **Billing** pada tab **Permissions** aplikasi.

`connection_auth_target` harus berupa `platform`: permintaan inferensi berjalan di organisasi Anda sendiri dan diautentikasi sebagai akun layanan operator, tetapi dapat menagih pelanggan.

`user_profile_id` harus berupa ID dari profil pengguna aktif di organisasi Anda. Jika pushed authorization request gagal, `auth.claude.com` mengembalikan respons error OAuth ke back end Anda. Jangan alihkan browser dalam kasus tersebut.

### Langkah 6: Arahkan pengguna Anda ke halaman persetujuan Claude

Pertama, tunjukkan kepada pengguna Anda akun mana di produk Anda yang sedang mereka tautkan, dan minta mereka untuk memeriksa akun Claude yang ditampilkan halaman persetujuan. Halaman tersebut menampilkan akun Claude mana yang sedang masuk dan memungkinkan pengguna beralih ke akun lain. Halaman persetujuan hanya menawarkan organisasi milik akun Claude yang sedang masuk di browser, sehingga akun yang salah dapat menautkan organisasi yang salah. Organisasi yang ditautkan pengguna adalah yang membayar.

<Note>
  Orang yang menyetujui harus merupakan administrator organisasi Claude pelanggan: anggota dengan peran Admin atau Billing.
</Note>

Kemudian, alihkan pengguna Anda ke endpoint otorisasi, yang menampilkan halaman persetujuan. Sertakan hanya `client_id` Anda dan `request_uri` dari Langkah 5.

```python
def authorize_url(par: dict) -> str:
    query = urlencode({"client_id": CLIENT_ID, "request_uri": par["request_uri"]})
    return f"{AUTH}/oauth/authorize?{query}"


redirect_to = authorize_url(par)  # answer the click with a 302 to this URL
```

### Langkah 7: Pengguna menyetujui

Aplikasi Anda tidak melakukan apa pun pada langkah ini. Pengguna menjalani langkah-langkah berikut di `auth.claude.com`:

1. Pengguna masuk ke Claude, kecuali browser sudah dalam keadaan masuk.

2. Halaman persetujuan menampilkan layar-layar berikut, masing-masing dengan nama aplikasi Anda. Untuk apa yang dilakukan pengguna di setiap layar, lihat [Menautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#connecting).

   1. **Select an organization**, hanya jika pengguna dapat memilih organisasi.
   2. **How billing works**.
   3. **Set a monthly spend limit**.
   4. Layar terakhir dengan tombol **Link and authorize**.

3. Ketika pengguna mengklik **Link and authorize**, `auth.claude.com` mengirim browser kembali ke aplikasi Anda. Halaman persetujuan tidak menampilkan layar konfirmasi.

Jika pengguna membatalkan atau tidak dapat menyetujui, tidak ada koneksi yang dibuat: lihat [Jika penautan tidak selesai](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#if-linking-doesnt-complete).

<Note>
  Koneksi dimiliki oleh seluruh organisasi Claude, bukan oleh pengguna yang menyetujuinya. Jika pengguna tersebut keluar dari organisasi, koneksi tetap aktif. Administrator mana pun dari organisasi pelanggan atau organisasi Anda dapat mengakhiri koneksi kapan saja, demikian pula back end Anda.
</Note>

### Langkah 8: Tangani callback dan simpan koneksi

Setelah persetujuan, `auth.claude.com` mengirim browser kembali ke redirect URI Anda dengan kode sekali pakai dan nilai `state` Anda. Permintaan ke redirect URI Anda ini disebut “callback” (panggilan balik). Back end Anda menukarkan kode tersebut dengan ID koneksi dan menyimpannya pada catatan pelanggan. Ini menyelesaikan koneksi. Callback dapat membawa parameter `error` tanpa kode. Dalam hal itu, tidak ada koneksi yang dibuat: lihat [Jika penautan tidak selesai](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#if-linking-doesnt-complete).

Periksa bahwa `state` cocok dengan nilai yang Anda simpan di Langkah 5, lalu segera tukarkan kode dari back end Anda, bersama dengan PKCE code verifier. Kode bersifat sekali pakai dan kedaluwarsa setelah 5 menit.

<CodeGroup exclude="shell:CLI, typescript, csharp, go, java, php, ruby">
  ```bash cURL
  curl https://auth.claude.com/v1/oauth/token \
    -H "content-type: application/json" \
    -d '{
      "grant_type": "authorization_code",
      "code": "AUTH_CODE",
      "code_verifier": "ORIGINAL_CODE_VERIFIER",
      "redirect_uri": "https://app.example.com/claude/billing/callback",
      "client_id": "YOUR_CLIENT_ID",
      "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      "client_assertion": "YOUR_CLIENT_ASSERTION_JWT"
    }'
  ```

  ```python Python
  def handle_callback(par: dict, params: dict) -> str:
      if not secrets.compare_digest(
          params.get("state", "").encode(), par["state"].encode()
      ):
          raise ValueError("state does not match")
      if "error" in params:  # for example access_denied
          raise PermissionError(params["error"])
      code = params["code"]  # single-use, expires after 5 minutes
      response = httpx.post(
          f"{AUTH}/v1/oauth/token",
          json={
              "grant_type": "authorization_code",
              "code": code,
              "code_verifier": par["code_verifier"],
              "redirect_uri": REDIRECT_URI,
              "client_id": CLIENT_ID,
              "client_assertion_type": JWT_BEARER,
              "client_assertion": client_assertion(),
          },
          timeout=10,  # a response that times out loses the tokens in it
      )
      response.raise_for_status()
      tokens = response.json()
      # Untuk memakai token koneksi, simpan tokens["access_token"], waktu kedaluwarsanya
      # (dari tokens["expires_in"]), dan, dengan offline_access,
      # tokens["refresh_token"] sebagai secret di sini: kode tidak dapat ditukar lagi.
      # "ocon_..."; simpan di catatan pelanggan
      return tokens["connection_id"]
  ```
</CodeGroup>

Respons berisi ID koneksi dan [token akses koneksi tersebut](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#oauth-tokens-for-each-connection), yang dapat mengautentikasi dan menagih pelanggan yang menyetujui. Jika pelanggan menyetujui `offline_access`, respons juga berisi refresh token. Simpan `connection_id` dan token-token tersebut sekarang: penukaran hanya mengembalikan token satu kali. [Simpan token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#keep-the-tokens-from-step-8) menjelaskan respons tersebut.

Contoh-contoh di halaman ini yang memanggil Claude API melakukan autentikasi sebagai akun layanan dari Langkah 3, bukan dengan token dari respons ini. [Panggil Claude dengan token akses koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#call-claude-with-a-connections-access-token) menjelaskan cara menggunakan token tersebut sebagai gantinya.

Respons tidak mengidentifikasi organisasi Claude mana yang ditautkan oleh pengguna.

Koneksi yang telah selesai tidak menjamin bahwa Anthropic dapat menagih pelanggan. Misalnya, organisasi pelanggan mungkin tidak termasuk [pelanggan yang memenuhi syarat](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#eligible-customers-and-endpoints). Lihat [Perbarui panggilan ke Claude](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#step-3-update-calls-to-claude) dan [Error yang diharapkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#expected-errors) untuk mengetahui cara Claude API memeriksa hal ini. Karena pemeriksaan tersebut, gunakan kata “tertaut” dalam pesan keberhasilan Anda alih-alih “penagihan aktif”.

Jika penukaran ditolak dengan `unauthorized_client`, lihat [Penukaran kode mengembalikan `unauthorized_client`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#code-exchange-unauthorized-client).

<Note>
  Pengguna dapat menyetujui lagi untuk profil pengguna yang sudah tertaut. Hasilnya bergantung pada scope:

  * Disetujui lagi untuk profil pengguna yang sama dan scope yang sama: koneksi tetap ada, dan respons token mengembalikan `connection_id` yang sama serta token akses baru. Pengecualiannya adalah koneksi dengan `billing:attribution offline_access`: penukaran kode mengembalikan `invalid_grant`, koneksi tetap seperti semula, dan [Menautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#connect-a-customer-again) menjelaskan apa yang harus dilakukan.
  * Disetujui lagi untuk profil pengguna yang sama dengan scope lain, misalnya `billing:attribution offline_access` setelah `billing:attribution`: penukaran kode baru oleh Anda membuat koneksi baru dengan `connection_id` baru, yang menggantikan koneksi sebelumnya. Token dari koneksi `billing:attribution` sebelumnya dicabut. Simpan `connection_id` baru sebagai pengganti yang sebelumnya. Jika penukaran gagal dengan respons 5xx, jalankan lagi Langkah 5 hingga 8. [Scope untuk koneksi penagihan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#scopes-for-a-billing-connection) menjelaskan kapan Anda memerlukan hal ini.
  * Setelah koneksi dicabut, Anda dapat menautkan profil pengguna yang sama lagi.
</Note>

### Menguji sebagai pelanggan

Untuk memeriksa bahwa penautan berfungsi, tautkan organisasi milik Anda sendiri. Anda memerlukan hal-hal berikut terlebih dahulu:

* Organisasi Claude kedua milik Anda untuk berperan sebagai pelanggan. Anda tidak dapat menautkan aplikasi Anda ke organisasi yang memilikinya. Halaman persetujuan tidak menawarkan organisasi tersebut. Organisasi kedua harus termasuk [pelanggan yang memenuhi syarat](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#eligible-customers-and-endpoints).
* Seseorang dengan peran Admin atau Billing di organisasi tersebut untuk menyetujui tautan.
* Hingga aplikasi Anda aktif, orang tersebut harus ada dalam daftar **Test users** aplikasi Anda. Daftar tersebut ada di tab **Settings** aplikasi di bawah **Who can link**. Tambahkan orang tersebut berdasarkan alamat email akun Claude-nya dan klik **Save changes**. [Selama aplikasi Anda dalam tahap pengujian](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#while-your-app-is-in-testing) menjelaskan batas atas pengeluaran yang berlaku. Menghapus seseorang dari daftar mengakhiri tautan yang telah disetujuinya.

Kemudian, jalankan Langkah 4 hingga 8, dan minta orang tersebut menyetujui di Langkah 7. Ketika tautan dibuat, profil pengguna bertuliskan **Linked** di halaman [User profiles](https://platform.claude.com/user-profiles) Anda di Console.

### Jika penautan tidak selesai

Ketika pengguna tidak menyelesaikan persetujuan, atau `auth.claude.com` menolaknya, tidak ada koneksi yang dibuat. Entri-entri berikut mencakup hasil yang khusus untuk Linked billing. Untuk setiap error lainnya, lihat [Error](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#errors) di Referensi OAuth.

#### Redirect URI Anda menerima `error=access_denied`

Permintaan tersebut juga membawa nilai `state` Anda. Redirect URI Anda menerima error ini dalam kasus-kasus seperti berikut:

1. Pengguna mengklik **Cancel** pada layar persetujuan mana pun.

2. Halaman persetujuan tidak memiliki organisasi untuk ditawarkan kepada pengguna, dan pengguna mengklik tombol yang kembali ke aplikasi Anda. Misalnya:

   * Pengguna tidak memiliki peran Admin atau Billing di organisasi Claude Platform mana pun.
   * Satu-satunya organisasi pengguna adalah organisasi yang memiliki aplikasi Anda. Lihat [Menguji sebagai pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#test-as-a-customer).
   * Profil pengguna sudah tertaut ke organisasi Claude lain, dan pengguna tidak memiliki peran Admin atau Billing di organisasi tersebut.
   * Hingga aplikasi Anda aktif, pengguna tidak ada dalam daftar **Test users**-nya.

Dalam setiap kasus dalam daftar ini, `error_description` berbunyi `the user declined the request`, sehingga Anda tidak dapat menggunakannya untuk membedakan kasus-kasus tersebut.

Satu penyebab lagi ada di pengaturan aplikasi Anda. Jika aplikasi Anda aktif dan **Who can link** hanya menampilkan organisasi Anda, tidak ada orang di luar organisasi Anda yang dapat menautkan aplikasi tersebut. Pilih **Any Claude user** dan klik **Save changes**.

Beri tahu pengguna bahwa penautan tidak selesai, dan jangan berasumsi bahwa mereka menolak. Minta mereka untuk memeriksa akun Claude mana yang mereka gunakan untuk masuk serta peran mereka di organisasi yang ingin mereka tautkan. `request_uri` tidak dapat digunakan lagi setelah pengguna membatalkan atau kembali, jadi untuk memungkinkan pengguna mencoba lagi, mulai lagi dari Langkah 5.

#### Aplikasi Anda menerima `user_profile_already_linked`

Organisasi Claude pelanggan sudah tertaut ke aplikasi Anda melalui profil pengguna Anda yang lain. `auth.claude.com` meminta pengguna untuk menghubungi Anda. Jika pengguna kembali ke aplikasi Anda, redirect URI Anda menerima `error=user_profile_already_linked` dan nilai `state` Anda. Endpoint token juga dapat mengembalikan error ini saat Anda menukarkan kode di Langkah 8. Hal itu terjadi, misalnya, ketika organisasi tersebut ditautkan melalui profil pengguna lain sementara itu.

Anthropic tidak memberi tahu Anda organisasi Claude mana yang ditautkan pelanggan, jadi Anda tidak dapat melihat hal ini sebelumnya. Pushed authorization request di Langkah 5 berhasil, dan `auth.claude.com` menolak koneksi hanya saat pengguna menyetujui.

Error tersebut tidak menyebutkan profil pengguna yang memegang koneksi. Pemegang yang paling mungkin adalah profil lain milik pelanggan ini yang sudah tertaut. Anthropic tidak menampilkan organisasi mana yang ditautkan ke sebuah profil, jadi konfirmasikan dengan pelanggan sebelum Anda bertindak. Jika profil tersebut memegang koneksi, lakukan salah satu hal berikut:

* Pada permintaan yang Anda tagihkan ke pelanggan ini, kirim ID profil pengguna tersebut.
* Akhiri koneksi tersebut, seperti dijelaskan dalam [Membatalkan tautan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#disconnecting-a-customer), lalu jalankan lagi Langkah 5 hingga 8 dengan profil pengguna yang ditolak.

Jika tidak ada profil pelanggan ini yang tertaut, pengguna mungkin telah memilih organisasi milik pelanggan Anda yang lain. Mulai lagi dari Langkah 5, dan minta pengguna untuk memeriksa organisasi mana yang mereka pilih.

#### Redirect URI Anda tidak menerima apa pun

Aplikasi Anda tidak dapat mendeteksi dua kasus berikut:

* Pengguna menutup halaman persetujuan.
* `request_uri` telah kedaluwarsa atau sudah digunakan. Halaman persetujuan kemudian menampilkan error dan tidak mengirim browser kembali ke aplikasi Anda.

Jika pengguna kembali ke produk Anda tanpa callback, mulai lagi dari Langkah 5. `request_uri` yang tidak digunakan kedaluwarsa 10 menit setelah Anda membuatnya.

#### Penukaran kode mengembalikan `unauthorized_client`

Aplikasi Anda belum disiapkan untuk permintaan ini. Untuk masalah workspace, `error_description` menyebutkan penyebabnya. Untuk akun layanan operator yang tidak ada, nilainya hanya berbunyi `the client is not registered for this grant`. Penolakan tidak menghabiskan kode, sehingga Anda dapat menukarkan kode yang sama lagi hingga kedaluwarsa. Pertama, periksa hal-hal berikut di Claude Console:

| Pemeriksaan                                     | Lokasi                                                                                                                                                         | Perbaikan                                                                                                |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Aplikasi memiliki akun layanan operator         | **Operator service account** pada tab **Client authentication** aplikasi                                                                                       | Pilih satu dan klik **Save**. Langkah 3 menjelaskan cara menyiapkannya.                                  |
| Workspace aplikasi tidak hilang atau diarsipkan | [Siapkan aplikasi Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#settings-for-a-connections-oauth-tokens) | Pilih workspace. Selama aplikasi belum memilikinya, penukaran juga ditolak dengan `unauthorized_client`. |

Akun layanan yang disimpan dapat memerlukan waktu satu atau dua menit untuk sampai ke `auth.claude.com`, jadi jika penukaran ditolak lagi, tunggu selama itu lalu coba lagi. Jika kode sudah kedaluwarsa pada saat itu, minta pengguna untuk menyetujui lagi (Langkah 5 hingga 8). Untuk penyebab yang disebutkan `error_description` terkait token koneksi, lihat [Simpan token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#keep-the-tokens-from-step-8) dan [Segarkan token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#refresh-the-connection).

Dalam kasus lain, hubungi tim akun Anthropic Anda. Lakukan hal yang sama jika Console menyatakan bahwa akun layanan tersebut sudah tidak ada.

### Publikasikan aplikasi Anda

Hingga aplikasi Anda aktif, hanya orang-orang dalam daftar **Test users** aplikasi tersebut yang dapat menautkannya, sehingga pelanggan Anda tidak dapat melakukannya. Untuk memublikasikan aplikasi, klik **Publish app** di halaman aplikasi di Claude Console. Sebuah kotak dialog akan terbuka.

* Jika organisasi Anda menggunakan penagihan berbasis faktur, aplikasi langsung aktif begitu Anda mengonfirmasi di kotak dialog tersebut.
* Jika tidak, Anda terlebih dahulu membuktikan di kotak dialog tersebut bahwa Anda mengendalikan domain aplikasi, lalu Anthropic meninjau aplikasi tersebut.

**Bukti domain:** Domain yang dimaksud adalah domain halaman beranda aplikasi Anda. Setiap redirect URI harus berada di domain tersebut atau di subdomainnya, kecuali redirect URI di `localhost`, `127.0.0.1`, atau `[::1]`. Buktinya berupa record DNS TXT. Perubahan DNS dapat memerlukan waktu hingga 48 jam, jadi mulailah sebelum Anda membutuhkan pelanggan untuk menautkan. Jika organisasi Anda sudah membuktikan domain yang mencakup halaman beranda dan redirect URI tersebut, kotak dialog melewati langkah pembuktian. Domain yang telah dibuktikan mencakup subdomainnya.

Anda mengonfirmasi pada langkah terakhir kotak dialog. Jika langkah tersebut menampilkan kotak centang untuk menerima Linked Billing Terms, pilih kotak centang tersebut. Kemudian, klik **Publish app** di kotak dialog.

**Peninjauan:** Selama peninjauan, status aplikasi di Console bertuliskan **In review**. Aplikasi aktif ketika Anthropic menyetujuinya. Jika Anthropic tidak menyetujuinya, status bertuliskan **Not approved**, dan Anda tidak dapat memublikasikan aplikasi tersebut lagi sendiri. Untuk menanyakan keputusan tersebut, hubungi dukungan.

Kecuali organisasi Anda menggunakan penagihan berbasis faktur, perubahan pada nama, logo, halaman beranda, atau redirect URI aplikasi yang sudah aktif akan mengembalikan aplikasi ke peninjauan. Pelanggan yang sudah tertaut tetap tertaut dan mempertahankan batas atas yang telah mereka simpan. Hingga Anthropic menyetujui perubahan tersebut, hanya orang-orang dalam daftar **Test users** yang dapat menautkan aplikasi.

## Perbarui panggilan ke Claude

Kirim header `anthropic-user-profile-id` pada setiap panggilan ke `/v1/messages` dan `/v1/chat/completions` untuk pelanggan yang tertaut. Pada permintaan yang Anda tagihkan ke pelanggan, nilai header tersebut adalah ID profil pengguna yang memegang koneksi pelanggan tersebut. Panggilan yang mengatur `billing_policy` juga harus mengirimkan header beta `user-profiles-billing-2026-10-01`.

Setiap permintaan untuk pelanggan yang tertaut ditagihkan ke pelanggan atau ke Anda, dan Anda memilih yang mana pada setiap permintaan. Contoh berikut menunjukkan keduanya.

[Token OAuth untuk setiap koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#oauth-tokens-for-each-connection) menjelaskan cara lain untuk mengautentikasi permintaan pelanggan: token akses yang hanya dapat menagih pelanggan tersebut. Pada `/v1/messages` dan `/v1/chat/completions`, permintaan dengan token semacam itu tidak dapat ditagihkan kepada Anda. Permintaan tersebut ditagihkan ke pelanggan tersebut, bahkan tanpa `billing_policy` atau header `anthropic-user-profile-id`, jika keduanya bersifat opsional: lihat catatan di [Panggil Claude dengan token akses koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#call-claude-with-a-connections-access-token). Jika permintaan tersebut menyebutkan profil pengguna lain atau menetapkan `bill_to: "self"`, permintaan tersebut ditolak. Jangan pernah menggunakan token semacam itu untuk permintaan yang Anda bayar.

### Pelanggan Anda yang membayar

Tambahkan `billing_policy` dengan `bill_to: "user_profile"` ke body permintaan, dan kirimkan header beta penagihan serta header ID profil.

<Warning>
  Periksa bahwa header menyebutkan profil pelanggan yang menjadi tujuan permintaan tersebut. Secara default, kredensial milik akun layanan operator Anda sendiri dapat menagih setiap pelanggan yang tertaut melalui aplikasi ini. Jika permintaan dengan kredensial tersebut menyebutkan profil lain yang tertaut melalui aplikasi ini, Anthropic menagih organisasi profil tersebut, dan tidak ada error yang memberi tahu Anda. [Token akses koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#oauth-tokens-for-each-connection) hanya dapat menagih pelanggannya sendiri.
</Warning>

Tetapkan `bill_to: "user_profile"` hanya pada permintaan yang diarahkan pelanggan untuk Anda buat: penggunaan Claude yang ditimbulkan oleh pelanggan dan pengguna mereka di produk Anda. Jangan menagih pelanggan atas penggunaan Anda sendiri, seperti pengujian, evaluasi, atau pekerjaan untuk pelanggan lain. Claude API tidak dapat memeriksa hal ini untuk Anda, jadi ini merupakan tanggung jawab Anda.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: user-profiles-billing-2026-10-01" \
    -H "anthropic-user-profile-id: uprof_01HV9Z" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}],
      "billing_policy": {"type": "billing_policy", "bill_to": "user_profile"}
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta user-profiles-billing-2026-10-01 \
    --user-profile-id uprof_01HV9Z \
    --model claude-sonnet-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}' <<'YAML'
  billing_policy:
    type: billing_policy
    bill_to: user_profile
  YAML
  ```

  ```python Python
  def message_billed_to_user(user_profile_id: str, prompt: str) -> BetaMessage:
      return client.beta.messages.create(
          model="claude-opus-5-5",
          max_tokens=1024,
          messages=[{"role": "user", "content": prompt}],
          betas=[BILLING_BETA],
          extra_headers={"anthropic-user-profile-id": user_profile_id},
          extra_body={
              "billing_policy": {"type": "billing_policy", "bill_to": "user_profile"}
          },
      )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.beta.messages.create({
    model: "claude-sonnet-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["user-profiles-billing-2026-10-01"],
    user_profile_id: "uprof_01HV9Z",
    // @ts-expect-error: billing_policy isn't in the SDK's types yet
    billing_policy: { type: "billing_policy", bill_to: "user_profile" }
  });

  console.log(message.content);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Messages;
  using System.Text.Json;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5_5,
      MaxTokens = 1024,
      Messages = [new BetaUserMessageParam { Content = "Hello, Claude" }],
      Betas = ["user-profiles-billing-2026-10-01"],
      UserProfileID = "uprof_01HV9Z",
  };
  // billing_policy belum ada di tipe SDK
  var body = new Dictionary<string, JsonElement>(parameters.RawBodyData)
  {
      ["billing_policy"] = JsonSerializer.SerializeToElement(
          new { type = "billing_policy", bill_to = "user_profile" }
      ),
  };

  var message = await client.Beta.Messages.Create(
      MessageCreateParams.FromRawUnchecked(parameters.RawHeaderData, parameters.RawQueryData, body)
  );

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  client := anthropic.NewClient()

  params := anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Betas:         []anthropic.AnthropicBeta{"user-profiles-billing-2026-10-01"},
  	UserProfileID: anthropic.String("uprof_01HV9Z"),
  }
  params.SetExtraFields(map[string]any{
  	"billing_policy": map[string]string{
  		"type":    "billing_policy",
  		"bill_to": "user_profile",
  	},
  })

  message, err := client.Beta.Messages.New(context.Background(), params)
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import java.util.Map;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_5_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .addBeta("user-profiles-billing-2026-10-01")
          .userProfileId("uprof_01HV9Z")
          .putAdditionalBodyProperty("billing_policy", JsonValue.from(Map.of(
              "type", "billing_policy",
              "bill_to", "user_profile")))
          .build();
      var message = client.beta().messages().create(params);

      IO.println(message.content());
  }
  ```

  ```php PHP
  use Anthropic\Messages\Model;

  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: Model::CLAUDE_SONNET_5_5,
      betas: ['user-profiles-billing-2026-10-01'],
      userProfileID: 'uprof_01HV9Z',
      requestOptions: [
          'extraBodyParams' => [
              'billing_policy' => ['type' => 'billing_policy', 'bill_to' => 'user_profile'],
          ],
      ],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_SONNET_5_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["user-profiles-billing-2026-10-01"],
    user_profile_id: "uprof_01HV9Z",
    request_options: {
      extra_body: { billing_policy: { type: "billing_policy", bill_to: "user_profile" } }
    }
  )

  puts(message.content)
  ```
</CodeGroup>

Jika permintaan ditolak, lihat [Error yang diharapkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#expected-errors).

### Anda yang membayar

Untuk membayar sendiri, hilangkan `billing_policy` sepenuhnya (dalam hal ini header beta penagihan bersifat opsional):

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-user-profile-id: uprof_01HV9Z" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```bash CLI
  ant messages create \
    --user-profile-id uprof_01HV9Z \
    --model claude-sonnet-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  def message_billed_to_you(user_profile_id: str, prompt: str) -> Message:
      return client.messages.create(
          model="claude-opus-5-5",
          max_tokens=1024,
          messages=[{"role": "user", "content": prompt}],
          user_profile_id=user_profile_id,
      )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-sonnet-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    user_profile_id: "uprof_01HV9Z"
  });

  console.log(message.content);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var message = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeSonnet5_5,
          MaxTokens = 1024,
          Messages = [new UserMessageParam { Content = "Hello, Claude" }],
          UserProfileID = "uprof_01HV9Z",
      }
  );

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  	UserProfileID: anthropic.String("uprof_01HV9Z"),
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_5_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .userProfileId("uprof_01HV9Z")
          .build();
      var message = client.messages().create(params);

      IO.println(message.content());
  }
  ```

  ```php PHP
  use Anthropic\Messages\Model;

  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: Model::CLAUDE_SONNET_5_5,
      userProfileID: 'uprof_01HV9Z',
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_SONNET_5_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    user_profile_id: "uprof_01HV9Z"
  )

  puts(message.content)
  ```
</CodeGroup>

atau gunakan `bill_to: "self"`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: user-profiles-billing-2026-10-01" \
    -H "anthropic-user-profile-id: uprof_01HV9Z" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}],
      "billing_policy": {"type": "billing_policy", "bill_to": "self"}
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta user-profiles-billing-2026-10-01 \
    --user-profile-id uprof_01HV9Z \
    --model claude-sonnet-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}' <<'YAML'
  billing_policy:
    type: billing_policy
    bill_to: self
  YAML
  ```

  ```python Python
  def message_billed_to_self(user_profile_id: str, prompt: str) -> BetaMessage:
      return client.beta.messages.create(
          model="claude-opus-5-5",
          max_tokens=1024,
          messages=[{"role": "user", "content": prompt}],
          betas=[BILLING_BETA],
          extra_headers={"anthropic-user-profile-id": user_profile_id},
          extra_body={"billing_policy": {"type": "billing_policy", "bill_to": "self"}},
      )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.beta.messages.create({
    model: "claude-sonnet-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["user-profiles-billing-2026-10-01"],
    user_profile_id: "uprof_01HV9Z",
    // @ts-expect-error: billing_policy isn't in the SDK's types yet
    billing_policy: { type: "billing_policy", bill_to: "self" }
  });

  console.log(message.content);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Messages;
  using System.Text.Json;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5_5,
      MaxTokens = 1024,
      Messages = [new BetaUserMessageParam { Content = "Hello, Claude" }],
      Betas = ["user-profiles-billing-2026-10-01"],
      UserProfileID = "uprof_01HV9Z",
  };
  // billing_policy belum ada di tipe SDK
  var body = new Dictionary<string, JsonElement>(parameters.RawBodyData)
  {
      ["billing_policy"] = JsonSerializer.SerializeToElement(
          new { type = "billing_policy", bill_to = "self" }
      ),
  };

  var message = await client.Beta.Messages.Create(
      MessageCreateParams.FromRawUnchecked(parameters.RawHeaderData, parameters.RawQueryData, body)
  );

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  client := anthropic.NewClient()

  params := anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Betas:         []anthropic.AnthropicBeta{"user-profiles-billing-2026-10-01"},
  	UserProfileID: anthropic.String("uprof_01HV9Z"),
  }
  params.SetExtraFields(map[string]any{
  	"billing_policy": map[string]string{
  		"type":    "billing_policy",
  		"bill_to": "self",
  	},
  })

  message, err := client.Beta.Messages.New(context.Background(), params)
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import java.util.Map;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_5_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .addBeta("user-profiles-billing-2026-10-01")
          .userProfileId("uprof_01HV9Z")
          .putAdditionalBodyProperty("billing_policy", JsonValue.from(Map.of(
              "type", "billing_policy",
              "bill_to", "self")))
          .build();
      var message = client.beta().messages().create(params);

      IO.println(message.content());
  }
  ```

  ```php PHP
  use Anthropic\Messages\Model;

  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: Model::CLAUDE_SONNET_5_5,
      betas: ['user-profiles-billing-2026-10-01'],
      userProfileID: 'uprof_01HV9Z',
      requestOptions: [
          'extraBodyParams' => [
              'billing_policy' => ['type' => 'billing_policy', 'bill_to' => 'self'],
          ],
      ],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_SONNET_5_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["user-profiles-billing-2026-10-01"],
    user_profile_id: "uprof_01HV9Z",
    request_options: {
      extra_body: { billing_policy: { type: "billing_policy", bill_to: "self" } }
    }
  )

  puts(message.content)
  ```
</CodeGroup>

## Token OAuth untuk setiap koneksi

Back end Anda memanggil Claude API sebagai akun layanan operator aplikasi Anda (Langkah 3). Secara default, setiap permintaan yang diautentikasi sebagai akun layanan tersebut dapat menagih setiap pelanggan yang tertaut, dengan mengirimkan header ID profil pengguna dan menyertakan `bill_to` dalam permintaan Messages API. Perilaku default ini disebut “operator-only tokenless authentication” (autentikasi tanpa token khusus operator).

Untuk menangani deployment produk Anda yang bersifat single-tenant, atau lingkungan sandbox yang dikendalikan pelanggan, Anda dapat memperoleh token akses dan “refresh token” (token penyegaran) OAuth yang terikat pada koneksi alih-alih menggunakan autentikasi tanpa token khusus operator.

Untuk setiap koneksi, penukaran kode di Langkah 8 mengembalikan token akses milik koneksi tersebut sendiri. Token tersebut melakukan autentikasi sebagai akun layanan operator Anda, tetapi hanya dapat menagih pelanggan dari koneksi tersebut. Token tersebut kedaluwarsa dalam 1 jam.

Untuk mengautentikasi setiap koneksi secara terpisah:

* **Gunakan akses offline.** Aktifkan [**Offline access**](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#settings-for-a-connections-oauth-tokens) untuk aplikasi Anda, dan minta `offline_access` di Langkah 5. Setiap koneksi kemudian juga mendapatkan refresh token, yang digunakan back end Anda untuk meminta token akses baru. Tanpanya, pelanggan harus menyetujui lagi untuk memberi Anda token akses baru: jalankan lagi Langkah 5 hingga 8 dengan `scope` yang sama.
* **Atur workspace default.** [Pilih workspace](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#settings-for-a-connections-oauth-tokens) di organisasi Anda tempat permintaan dengan token-token ini dijalankan.
* **Secara opsional, nonaktifkan autentikasi tanpa token khusus operator.** Secara default, Anda tetap dapat menagih pelanggan yang tertaut sebagai akun layanan operator Anda (dengan mengirimkan header profil pengguna dan `bill_to`), bahkan setelah token akses pelanggan kedaluwarsa. Setelah Anda [menonaktifkan autentikasi khusus operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#turn-off-operator-only-authentication), setiap permintaan yang menagih pelanggan harus melakukan autentikasi dengan token akses pelanggan tersebut.
* **Gunakan `billing:attribution`.** Hanya scope ini yang memberikan token tersendiri kepada koneksi. Anda tetap dapat menagih pelanggan yang tertaut sebagai akun layanan operator Anda, seperti halnya dengan `org:billing_attribution`, yang sudah usang. Lihat [Scope untuk koneksi penagihan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#scopes-for-a-billing-connection).

### Siapkan aplikasi Anda

Permintaan dengan token akses koneksi berjalan di satu workspace organisasi Anda. Setiap aplikasi memerlukannya, bahkan jika Anda tidak menggunakan token-token ini: selama aplikasi Anda belum memiliki workspace, penukaran kode di Langkah 8 ditolak dengan `unauthorized_client`.

Anggota organisasi Anda dengan peran Admin membuka tab **Client authentication** aplikasi di Console. Di bawah akun layanan operator, temukan **Default workspace for platform auth mode OAuth tokens** (pengaturan `connection_token_workspace_id` aplikasi) dan klik **Choose workspace**. Pilih workspace yang keanggotaannya mencakup akun layanan operator (Langkah 3). Workspace tersebut tidak boleh diarsipkan.

Untuk mendapatkan refresh token, aktifkan **Offline access** pada tab **Permissions** aplikasi. Perubahan pada scope aplikasi memerlukan beberapa menit untuk sampai ke `auth.claude.com`.

<Note>
  Mengarsipkan workspace default mencabut setiap token yang berjalan di dalamnya, dan tindakan ini tidak dapat dibatalkan. Untuk berpindah ke workspace lain, atur workspace yang baru dan tunggu beberapa menit. Penyegaran sebelum perubahan tersebut sampai ke `auth.claude.com` dapat mengembalikan token yang masih berjalan di workspace sebelumnya. Kemudian, segarkan setiap koneksi yang memiliki refresh token, dan baru setelah itu arsipkan workspace sebelumnya. Jika Anda mengarsipkan workspace terlebih dahulu, hentikan penyegaran koneksinya sebelum Anda mengatur workspace lain: penyegaran berikutnya akan mengakhiri koneksi.

  Jangan mengubah atau mengarsipkan akun layanan operator aplikasi selama ada pelanggan yang tertaut. Setelah Anda mengubah atau mengarsipkannya, `auth.claude.com` menolak setiap penyegaran, dan token yang Anda pegang segera berhenti menagih pelanggan. Setiap pelanggan yang tokennya Anda gunakan kemudian harus menautkan lagi: untuk bantuan, [hubungi dukungan](https://support.claude.com/en/articles/9015913-how-to-get-support).
</Note>

### Scope untuk koneksi penagihan

Di Langkah 5, kirim `scope` sebagai `billing:attribution`. Untuk juga mendapatkan refresh token, kirim `billing:attribution offline_access`.

Untuk mengubah scope pelanggan yang sudah tertaut, misalnya untuk menambahkan `offline_access`, jalankan lagi Langkah 5 hingga 8 dengan profil pengguna pelanggan yang sudah ada dan `scope` yang baru. Anda tidak perlu membatalkan tautan terlebih dahulu. Penukaran kode mengembalikan `connection_id` baru, dan koneksi baru menggantikan koneksi sebelumnya. Lihat catatan di Langkah 8.

Sebuah aplikasi dapat memiliki `billing:attribution` dan `org:billing_attribution` yang sudah usang sekaligus. Anda menambahkan `billing:attribution` di bawah **Billing** pada tab **Permissions** aplikasi. Jika Anda menghapus `org:billing_attribution` di sana, Anda tidak dapat menambahkannya lagi. Koneksi yang disetujui pelanggan dengan `org:billing_attribution` tetap menagih melalui akun layanan operator Anda hingga koneksi berakhir atau Anda [menonaktifkan autentikasi khusus operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#turn-off-operator-only-authentication).

### Simpan token

Penukaran kode mengembalikan token hanya satu kali, jadi simpan token tersebut di Langkah 8. Respons berisi `access_token`, `expires_in` (paling lama 1 jam, dalam detik), dan `connection_id`. Jika pelanggan menyetujui `offline_access`, respons juga berisi `refresh_token` dan `refresh_token_expires_in`. Refresh token berlaku paling lama 1 tahun, dan penyegaran tidak memperpanjang masa tersebut. Setelah itu, [tautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#connect-a-customer-again).

Simpan token dan waktu kedaluwarsanya di penyimpanan rahasia yang hanya dapat dibaca oleh layanan yang melakukan penyegaran.

Jika penukaran ditolak dengan `unauthorized_client`, `error_description` menyebutkan penyebabnya, seperti workspace yang tidak ada atau telah diarsipkan. Kode tersebut tidak terpakai: perbaiki penyebabnya, dan kirim kode yang sama lagi sebelum kedaluwarsa.

### Panggil Claude dengan token akses koneksi

<Note>
  Selama beta, tanyakan kepada tim akun Anthropic Anda apakah permintaan Claude API dengan token akses koneksi telah diaktifkan untuk organisasi Anda. Selama belum diaktifkan, setiap permintaan semacam itu gagal, apa pun yang dikirimkannya. Tanyakan juga apakah header `anthropic-user-profile-id` dan `billing_policy` bersifat opsional. Selama belum opsional, kirim setiap permintaan `/v1/messages` dan `/v1/chat/completions` yang menggunakan token akses koneksi seperti yang ditunjukkan di [Pelanggan Anda yang membayar](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#your-customer-pays), dengan header tersebut, `bill_to: "user_profile"`, dan header beta penagihan.
</Note>

Kirim token akses koneksi sebagai bearer token di header `Authorization`, sebagai pengganti kredensial milik akun layanan operator Anda sendiri. Jangan kirim header `x-api-key`. Di Anthropic SDK, teruskan token sebagai `auth_token` (typescript, php: `authToken`; java: `.authToken()`; csharp: `AuthToken`; go: `option.WithAuthToken()`), atau atur variabel environment `ANTHROPIC_AUTH_TOKEN`.

Pada `/v1/messages` dan `/v1/chat/completions`, permintaan ditagihkan ke pelanggan dari koneksi tersebut. Header `anthropic-user-profile-id` dan `billing_policy` bersifat opsional. Anda memerlukan header beta penagihan hanya bersama `billing_policy`.

Pada kedua endpoint ini, Anda tidak dapat membayar permintaan dengan token ini. Gunakan token hanya pada kedua endpoint ini, `/v1/messages/count_tokens`, dan endpoint Models. Kirim setiap permintaan lain, dan setiap permintaan yang Anda bayar, sebagai akun layanan operator Anda, dari back end Anda sendiri. Itu termasuk permintaan yang menggunakan [fitur eksekusi kode yang dapat ditagih](https://platform.claude.com/docs/id/about-claude/pricing#code-execution-tool), yang tidak dapat menagih pelanggan.

Claude API menolak permintaan berikut:

* `400 invalid_request_error`, tanpa kode error: permintaan menyebutkan profil pengguna lain atau mengatur `bill_to: "self"`.
* `403 permission_error`, tanpa kode error: permintaan dikirim ke endpoint [Message Batches](https://platform.claude.com/docs/id/build-with-claude/batch-processing).
* `401 authentication_error`: token telah kedaluwarsa, penyegaran telah menggantikannya, atau koneksinya telah berakhir. Setelah koneksi berakhir, respons juga dapat berupa `403 user_profile_not_billable`.

### Segarkan token

Untuk memperbarui token akses koneksi, kirim refresh token-nya ke endpoint token, `https://auth.claude.com/v1/oauth/token`, dengan [autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#client-authentication) aplikasi Anda. Jangan kirim parameter `scope`.

<CodeGroup exclude="shell:CLI, typescript, csharp, go, java, php, ruby">
  ```bash cURL
  curl https://auth.claude.com/v1/oauth/token \
    -H "content-type: application/json" \
    -d @- <<JSON
  {
    "grant_type": "refresh_token",
    "refresh_token": "$CONNECTION_REFRESH_TOKEN",
    "client_id": "YOUR_CLIENT_ID",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": "$CLIENT_ASSERTION"
  }
  JSON
  ```

  ```python Python
  connection_locks: defaultdict[str, threading.Lock] = defaultdict(threading.Lock)


  def error_body(response: httpx.Response) -> dict:
      try:
          body = response.json()
      except ValueError:
          return {}
      return body if isinstance(body, dict) else {}


  def is_lost(response: httpx.Response) -> bool:
      """True for a 5xx response that can follow a refresh that took effect."""
      if response.status_code < 500:
          return False
      # 503 dalam format Claude API dengan header retry-after adalah penolakan
      # yang tidak memakai refresh token. Setiap respons 5xx lainnya dianggap hilang.
      paused = (
          response.status_code == 503
          and error_body(response).get("type") == "error"
          and "retry-after" in response.headers
      )
      return not paused


  def hold_error(connection_id: str, reason: str) -> RefreshOnHold:
      return RefreshOnHold(
          f"Connection {connection_id} is on hold. {reason} Don't send its refresh token"
          ' again: that can end the connection. See "Link a customer again" in the'
          " Linked billing guide."
      )


  def refresh_connection(connection_id: str, *, force: bool = False) -> tuple[str, int]:
      """Refreshes the connection if its access token is close to its expiry.

      Returns the current access token and its expiry time in Unix seconds. Call
      this from your schedule, and pass force=True to refresh a token that isn't
      close to its expiry. Raises RefreshOnHold when the refresh token can't be sent
      again, now and on every later call, and httpx.HTTPStatusError for a refusal
      that keeps the refresh token. After RefreshOnHold for a lost refresh, pause
      your schedule. Resume with one connection, and resume the others only after
      that refresh succeeds or gets a 4xx.
      """
      # Lock ini bekerja dalam satu proses. Jika layanan memiliki replika, gunakan lock
      # yang dibagikan oleh semuanya.
      with connection_locks[connection_id]:
          tokens = load_tokens(connection_id)
          if tokens.on_hold:
              raise hold_error(
                  connection_id, "An earlier refresh might have used its refresh token."
              )
          if not force and tokens.expires_at - time.time() > REFRESH_MARGIN_SECONDS:
              return tokens.access_token, tokens.expires_at  # not close to expiry
          request = {
              "grant_type": "refresh_token",
              "refresh_token": tokens.refresh_token,
              "client_id": CLIENT_ID,
              "client_assertion_type": JWT_BEARER,
              "client_assertion": client_assertion(),
          }
          url = f"{AUTH}/v1/oauth/token"
          # Tahan koneksi sebelum refresh token keluar dari proses ini.
          # Jika proses berhenti sebelum token baru disimpan, penahanan tetap berlaku.
          save_tokens(connection_id, replace(tokens, on_hold=True))
          issued_at = int(time.time())
          started = time.monotonic()
          # httpx tidak melakukan retry sendiri. Jangan tambahkan retry: retry yang terlambat mengakhiri
          # koneksi.
          try:
              response = httpx.post(url, json=request, timeout=REQUEST_TIMEOUT)
              lost = is_lost(response)
          except (httpx.ConnectError, httpx.ConnectTimeout):
              # Tidak ada koneksi yang dibuat, jadi refresh token tidak pernah keluar dari proses ini.
              save_tokens(connection_id, tokens)
              raise
          except httpx.TransportError:
              lost = True
          if lost:
              # Request pertama mungkin telah memakai refresh token. Request kedua
              # hanya aman dalam batas di atas, jadi kirim satu segera atau tidak
              # sama sekali.
              if time.monotonic() - started > SECOND_REQUEST_DEADLINE_SECONDS:
                  raise hold_error(connection_id, "A refresh got no usable answer.")
              try:
                  response = httpx.post(url, json=request, timeout=REQUEST_TIMEOUT)
              except httpx.TransportError:
                  raise hold_error(
                      connection_id, "Two refreshes got no answer."
                  ) from None
              if response.status_code != 200:
                  # Setelah jawaban apa pun selain token baru, Anda tidak dapat tahu apakah
                  # request pertama berlaku, dan request berikutnya tidak aman.
                  raise hold_error(connection_id, "The second refresh failed.")
          if error_body(response).get("error") == "invalid_grant":
              # Kedaluwarsa, sudah digunakan, atau koneksi berakhir. Mengirimnya lagi
              # dapat mengakhiri koneksi.
              raise hold_error(connection_id, "The refresh returned invalid_grant.")
          if response.status_code != 200:
              # Penolakan yang mempertahankan refresh token, jadi lepaskan penahanan.
              save_tokens(connection_id, tokens)
              response.raise_for_status()
          body = response.json()
          tokens = ConnectionTokens(
              refresh_token=body["refresh_token"],
              access_token=body["access_token"],
              expires_at=issued_at + body["expires_in"],
              refresh_expires_at=issued_at + body["refresh_token_expires_in"],
          )
          # Jika penulisan gagal, coba tulis lagi. Jangan refresh lagi.
          for attempt in range(5):
              try:
                  save_tokens(connection_id, tokens)
                  return tokens.access_token, tokens.expires_at
              except OSError:  # your secret store's error type
                  if attempt < 4:
                      time.sleep(2**attempt)
          # Token baru hanya ada di proses ini, dan refresh token yang tersimpan
          # sudah terpakai. Record tersimpan masih ditahan. Error membawa token baru,
          # agar pemanggil dapat menyimpannya saat secret store kembali tersedia.
          error = hold_error(
              connection_id,
              "The refresh succeeded, but the new tokens could not be saved.",
          )
          error.new_tokens = tokens
          raise error
  ```
</CodeGroup>

Respons berisi `access_token` baru dan `refresh_token` baru. Refresh token yang Anda kirim telah digantikan: jangan kirim lagi, kecuali sebagaimana dinyatakan dalam daftar kegagalan di bawah. Token akses sebelumnya berhenti berfungsi dalam beberapa menit. [Inisialisasi cuplikan token OAuth](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#oauth-token-snippet-initialization) mendefinisikan fungsi-fungsi yang dipanggil oleh contoh tersebut.

* Simpan refresh token baru sebelum Anda menggunakan token akses baru.
* Segarkan token setiap koneksi dari satu layanan, satu penyegaran pada satu waktu. Jika layanan tersebut memiliki replika, gunakan lock yang digunakan bersama oleh semuanya. Refresh token yang sudah digunakan dan tiba lagi lebih dari 30 detik setelah penggunaan pertamanya akan mengakhiri koneksi. Setiap token dicabut, pelanggan ditampilkan sebagai **Unlinked**, dan tidak ada kredensial yang dapat menagih mereka hingga mereka menautkan lagi.
* Nonaktifkan percobaan ulang otomatis untuk permintaan penyegaran, di klien HTTP Anda dan di proxy mana pun.

Jika permintaan pertama dengan refresh token gagal:

* Permintaan tidak dapat tersambung: refresh token tidak terkirim. Coba lagi nanti.

* Koneksi terputus, atau respons 5xx apa pun selain `503` dalam daftar ini: Anda tidak dapat mengetahui apakah permintaan tersebut telah berlaku, jadi kirim refresh token yang sama sekali lagi.

  1. Kirim segera, dan hanya jika kurang dari 30 detik telah berlalu sejak Anda mengirim permintaan pertama.
  2. Jika permintaan tersebut mengembalikan token baru, simpan token tersebut dan gunakan hanya token tersebut. Jika permintaan pertama ternyata telah berlaku, token darinya, yang tidak pernah sampai kepada Anda, dicabut.
  3. Jika permintaan tersebut mengembalikan hal lain atau tidak mendapat jawaban, atau jika 30 detik telah berlalu, jangan kirim refresh token tersebut lagi. Hentikan penyegaran koneksi tersebut, dan [tautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#connect-a-customer-again).

* Timeout: permintaan mungkin masih berjalan. Jangan kirim refresh token tersebut lagi. Hentikan penyegaran koneksi tersebut, dan [tautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#connect-a-customer-again).

* `429`, atau `503` dengan header `retry-after` dan `"type": "error"` di tingkat teratas body-nya: tidak ada yang dicabut. Tunggu setidaknya selama yang dinyatakan header, dan kirim refresh token yang sama lagi.

* `unauthorized_client` atau `invalid_client`: tidak ada yang dicabut. `error_description` menyebutkan penyebabnya, seperti workspace yang tidak ada, `offline_access` yang tidak lagi terdaftar untuk aplikasi Anda, atau client assertion yang gagal. Perbaiki, dan kirim refresh token yang sama lagi.

* `invalid_scope`: permintaan mengirim parameter `scope`, atau `billing:attribution` tidak lagi terdaftar untuk aplikasi Anda. Tidak ada yang dicabut. Perbaiki penyebabnya, dan kirim refresh token yang sama lagi.

* `invalid_grant`: refresh token telah kedaluwarsa atau sudah digunakan, koneksi telah berakhir, atau organisasi pelanggan ditangguhkan. Hentikan penyegaran koneksi tersebut, dan ikuti [Menautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#connect-a-customer-again), yang dimulai dengan pemeriksaan penangguhan.

Jika koneksi yang terputus, respons 5xx, atau timeout membuat Anda menghentikan penyegaran sebuah koneksi, jeda juga penyegaran koneksi Anda yang lain. Saat Anda melanjutkan, segarkan satu koneksi terlebih dahulu, dan lanjutkan yang lain hanya setelah penyegaran tersebut berhasil atau mendapatkan respons 4xx.

### Jalankan agen di sandbox

Berikan “sandbox” (lingkungan terisolasi) hanya token akses, jangan pernah refresh token. Back end Anda melakukan penyegaran, dan mengirimkan setiap token akses baru ke sandbox. Back end menentukan pelanggan mana yang dilayani sandbox berdasarkan identitas sandbox itu sendiri, seperti identitas pod-nya, dan tidak pernah berdasarkan nilai yang dikirim sandbox. Back end hanya mengirimkan token pelanggan tersebut ke sandbox. Sandbox tidak boleh dapat memperoleh JWT yang cocok dengan salah satu aturan federasi Anda atau autentikasi klien aplikasi Anda. Jangan berikan token identitas yang di-mount maupun akses ke server metadata cloud.

Claude Code, [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), dan Anthropic SDK dapat membaca token dari file kredensial dalam profil konfigurasi (lihat [File konfigurasi profil](https://platform.claude.com/docs/id/manage-claude/wif-reference#profile-configuration-file)). Di sandbox, buat direktori konfigurasi dengan profil ini. Jangan tambahkan `client_id` ke dalamnya: jika ada, SDK akan mencoba menyegarkan token sendiri.

```json configs/customer.json
{
  "version": "1.0",
  "authentication": {
    "type": "user_oauth"
  }
}
```

Tulis token akses sebagai `credentials/customer.json` di direktori yang sama, sebelum agen dimulai dan setelah setiap penyegaran. `expires_at` adalah waktu kedaluwarsa dalam detik Unix. Tulis file baru dengan mode `0600`, lalu ganti nama file tersebut untuk menimpa file yang lama:

```json credentials/customer.json
{
  "type": "oauth_token",
  "access_token": "sk-ant-oat01-...",
  "expires_at": 1793635200
}
```

Atur `ANTHROPIC_CONFIG_DIR` ke direktori konfigurasi dan `ANTHROPIC_PROFILE` ke `customer`. Hapus setiap kredensial lain di sandbox, seperti `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN`, dan pengaturan `apiKeyHelper` milik Claude Code, karena masing-masing dapat didahulukan di atas profil. Agen membaca file lagi dalam 2 menit terakhir sebelum `expires_at`, dan setelah respons 401.

```python
def write_credentials_file(
    config_dir: Path, profile: str, token: str, expires_at: int
) -> None:
    credentials_dir = config_dir / "credentials"
    credentials_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    body = {"type": "oauth_token", "access_token": token, "expires_at": expires_at}
    # Ganti nama file yang sudah selesai ke tempatnya, agar agen tidak membaca file setengah jadi.
    # mkstemp menetapkan mode 0600 dengan pengguna saat ini sebagai pemilik, jadi jalankan ini sebagai
    # pengguna agen.
    handle, temporary_path = tempfile.mkstemp(dir=credentials_dir)
    with os.fdopen(handle, "w") as temporary_file:
        json.dump(body, temporary_file)
    os.replace(temporary_path, credentials_dir / f"{profile}.json")
```

### Menautkan pelanggan lagi

Tautkan pelanggan lagi dalam kasus-kasus berikut:

* Penyegaran mengembalikan `invalid_grant`.
* Anda kehilangan refresh token, atau refresh token bocor.
* Anda kehilangan respons di Langkah 8 untuk `billing:attribution offline_access`, atau Langkah 8 mengembalikan `invalid_grant` untuk koneksi semacam itu.
* Refresh token mendekati masa kedaluwarsanya.

Ikuti langkah-langkah berikut:

1. Di halaman [User profiles](https://platform.claude.com/user-profiles) Anda, periksa apakah pelanggan ditampilkan sebagai **Linked**. Setelah `invalid_grant`, tanyakan terlebih dahulu kepada tim akun Anthropic Anda apakah organisasi pelanggan ditangguhkan: setelah penangguhan berakhir, refresh token yang Anda pegang berfungsi lagi. Jika setiap koneksi mengembalikan `invalid_grant` pada saat yang sama, cari penyebab di sisi Anda, seperti workspace yang diarsipkan, sebelum Anda membatalkan tautan siapa pun.
2. Jika pelanggan ditampilkan sebagai **Linked**, batalkan tautannya, seperti dijelaskan dalam [Membatalkan tautan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#disconnecting-a-customer). Membatalkan tautan mencabut token koneksi. Lakukan ini saat administrator organisasi pelanggan siap menyetujui, karena penagihan melalui koneksi berhenti hingga mereka menyetujui.
3. Jalankan lagi Langkah 5 hingga 8 dengan profil pengguna pelanggan yang sudah ada. Simpan ID koneksi baru dan token baru sebagai pengganti yang sebelumnya.

### Nonaktifkan autentikasi khusus operator

<Note>
  Selama beta, tanyakan kepada tim akun Anthropic Anda apakah pengaturan ini tersedia untuk organisasi Anda. Selama belum tersedia, Anda tidak dapat mengaktifkannya.
</Note>

Untuk mencegah permintaan yang hanya melakukan autentikasi sebagai akun layanan operator Anda menagih pelanggan, aktifkan **Disable operator-only tokenless authentication** (pengaturan `disable_operator_only_auth` aplikasi). Pengaturan ini ada di tab **Client authentication** aplikasi, di bawah akun layanan operator. Aplikasi Anda harus memiliki scope `billing:attribution` dan `offline_access` serta [workspace untuk token OAuth-nya](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#settings-for-a-connections-oauth-tokens). Sebelum Anda mengaktifkannya, pastikan setiap pelanggan yang tertaut telah menyetujui `billing:attribution offline_access` dan permintaan Anda dengan token akses mereka berfungsi. Selama pengaturan ini aktif, hanya token akses dari koneksi `billing:attribution` yang dapat menagih pelanggan dari koneksi tersebut. Permintaan yang melakukan autentikasi hanya sebagai akun layanan dan mengatur `bill_to: "user_profile"` ditolak dengan `403 user_profile_not_billable`. Pelanggan tetap ditampilkan sebagai **Linked**, jadi pantau error ini di log Anda. Akun layanan tetap dapat mengelola profil pengguna dan mengirim permintaan yang Anda bayar. Anda dapat menonaktifkan pengaturan ini lagi.

### Inisialisasi cuplikan token OAuth

Contoh di bagian ini berbagi penyiapan berikut. Penyiapan ini mendefinisikan:

* import, yang mencakup paket `httpx`
* client ID aplikasi Anda dan jenis client assertion
* `ConnectionTokens`, yang menyimpan token koneksi, waktu kedaluwarsanya, dan tanda `on_hold`-nya
* `RefreshOnHold`, error yang dimunculkan `refresh_connection()` ketika refresh token tidak boleh dikirim lagi: token tersebut mungkin sudah digunakan, atau endpoint token menjawab `invalid_grant`. `refresh_connection()` juga memunculkannya pada setiap panggilan berikutnya, hingga Anda menghapus `on_hold` pada token yang tersimpan, misalnya setelah penangguhan berakhir. Ketika penyegaran berhasil dan hanya penyimpanan rahasia Anda yang menolak penulisan, `new_tokens`-nya menyimpan token yang harus disimpan.
* `client_assertion()`, yang membaca JWT penyedia identitas Anda dari file yang disebutkan oleh `ANTHROPIC_IDENTITY_TOKEN_FILE`. Klaim `aud` JWT tersebut harus berupa audience dalam pengaturan autentikasi klien aplikasi Anda.
* `load_tokens()` dan `save_tokens()`, yang Anda tulis untuk penyimpanan rahasia Anda sendiri

```python
import json
import os
import tempfile
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field, replace
from pathlib import Path

import httpx

AUTH = "https://auth.claude.com"
# salin dari platform.claude.com setelah Anda mendaftarkan aplikasi OAuth Anda.
CLIENT_ID = "YOUR_CLIENT_ID"
JWT_BEARER = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
REFRESH_MARGIN_SECONDS = 600
# Refresh yang timeout di sini kehilangan token barunya, jadi beri waktu 10 detik untuk
# jawaban. Koneksi yang tidak dapat dibuat gagal dalam 2 detik.
REQUEST_TIMEOUT = httpx.Timeout(10, connect=2)
# Request kedua harus dimulai sesegera ini setelah yang pertama, atau tidak sama sekali.
# Halaman memberi 30 detik, tetapi jaga di bawah read timeout REQUEST_TIMEOUT:
# request yang timeout tidak boleh dikirim lagi.
SECOND_REQUEST_DEADLINE_SECONDS = 4


@dataclass
class ConnectionTokens:
    refresh_token: str = field(repr=False)
    access_token: str = field(repr=False)
    expires_at: int  # the access token's expiry time, in Unix seconds
    refresh_expires_at: int  # the refresh token's expiry time, in Unix seconds
    # True: refresh token mungkin sudah digunakan. Jangan kirim lagi.
    on_hold: bool = False


class RefreshOnHold(Exception):
    """The refresh token might have been used, so a person decides what to do next.

    Don't catch this to try again. If new_tokens is set, the refresh succeeded and
    only the write failed: store those tokens.
    """

    new_tokens: ConnectionTokens | None = None


def client_assertion() -> str:
    """Reads your identity provider's JWT on every call, because its file rotates."""
    return Path(os.environ["ANTHROPIC_IDENTITY_TOKEN_FILE"]).read_text().strip()


def load_tokens(connection_id: str) -> ConnectionTokens:
    """Reads the connection's newest tokens from your secret store."""
    raise NotImplementedError("Read the tokens from your secret store.")


def save_tokens(connection_id: str, tokens: ConnectionTokens) -> None:
    """Writes the connection's newest tokens to your secret store."""
    raise NotImplementedError("Write the tokens to your secret store.")
```

## Mengelola koneksi Anda

### Melihat pelanggan di Console

Selain halaman aplikasi OAuth, Anda dapat melihat semua profil pengguna Anda di halaman [User profiles](https://platform.claude.com/user-profiles) di Console. Pada daftar tersebut dan pada halaman detail setiap profil pengguna, **Your spend** adalah biaya Anda sendiri untuk permintaan profil pengguna tersebut. Ini adalah biaya sebelum Anthropic menerapkan kredit apa pun. Halaman-halaman ini menyebut koneksi sebagai tautan: profil pengguna dengan koneksi aktif bertuliskan **Linked**, dan profil yang koneksinya telah berakhir bertuliskan **Unlinked**.

Klik profil pengguna untuk tampilan yang lebih mendetail tentang penggunaannya selama 7, 28, atau 90 hari terakhir.

### Memantau penggunaan setiap pelanggan

Claude Console dan [Usage and Cost Analytics API](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api) sama-sama melaporkan penggunaan untuk setiap profil pengguna. Keduanya menghitung permintaan yang Anda bayar dan permintaan yang dibayar oleh pelanggan Anda. Tidak satu pun dari keduanya menampilkan apa yang dibayar pelanggan atau tarif pelanggan.

Di Console, halaman [User profiles](https://platform.claude.com/user-profiles) mencantumkan **Requests**, **Tokens**, dan **Your spend** untuk setiap profil pengguna selama 28 hari terakhir. Permintaan yang dibayar oleh pelanggan Anda menambah **Requests** dan **Tokens** profil tersebut dan tidak menambah apa pun ke **Your spend**.

Panggil API dengan [kredensial Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication), seperti token akses OAuth dengan scope `org:admin` atau kunci Admin API. Jangan gunakan akun layanan operator Anda (Langkah 3). Aturan federasinya memberikan `workspace:developer` secara default, bukan `org:admin`. Scope `org:admin` mencakup seluruh Admin API, jadi jangan tambahkan scope tersebut ke akun layanan operator.

Untuk membuat laporan per profil pengguna melalui API, panggil [endpoint penggunaan](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#usage-endpoint) atau [endpoint biaya](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#cost-endpoint)-nya. Untuk mendapatkan satu baris untuk setiap profil pengguna, kelompokkan hanya berdasarkan `user_profile_id` dan hilangkan `time_bucket_width`. Hanya profil pengguna yang memiliki penggunaan dalam rentang waktu yang Anda minta yang mendapatkan baris. Satu baris tambahan memiliki `user_profile_id` bernilai null. Baris tersebut memuat penggunaan yang tidak menyebutkan profil apa pun dan penggunaan yang diukur di luar permintaan, seperti waktu container eksekusi kode.

Pada endpoint biaya, permintaan yang dibayar oleh pelanggan Anda menambahkan 0 ke `amount` dan harga daftarnya ke `list_amount`. Field `amount` adalah ukuran yang sama dengan **Your spend**. API tidak memiliki field, filter, maupun nilai `group_by[]` untuk siapa yang membayar. Baris dengan `amount` bernilai 0 dan `list_amount` di atas 0 biasanya berarti pelanggan membayar setiap permintaan dalam baris tersebut.

Jangan gunakan angka-angka ini untuk menghentikan penggunaan pelanggan pada jumlah yang Anda pilih. Baik Console maupun API tidak melaporkan secara real-time. Angka di Console diperbarui sekitar sekali per jam, dan sebuah permintaan dapat memerlukan waktu beberapa jam untuk muncul. Untuk penundaan API, lihat [Kesegaran data](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#data-freshness). [Batas atas pengeluaran](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#spend-caps) menjelaskan fungsi batas milik pelanggan sendiri.

### Membaca status tautan pelanggan

Untuk membaca status tautan pelanggan dari back end Anda, minta profil pengguna mereka dengan client ID aplikasi Anda di `oauth_app_id`, dan kirim header beta `user-profiles-search-2026-08-30`. Lakukan autentikasi sebagai akun layanan operator Anda (Langkah 3), dengan token aksesnya atau kunci API yang terikat padanya. Token akses harus berasal dari aturan federasi dengan scope `workspace:developer`, yang merupakan default.

<CodeGroup exclude="shell:CLI, python, typescript, csharp, go, java, php, ruby">
  ```bash cURL
  curl "https://api.anthropic.com/v1/user_profiles/uprof_01HV9Z?oauth_app_id=YOUR_CLIENT_ID" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: user-profiles-search-2026-08-30"
  ```
</CodeGroup>

Dalam respons, `connection_status` menjelaskan tautan profil pengguna ke aplikasi Anda:

| `connection_status.type` | Arti                                                                                                                                                                                                                                                                                                                        |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `connected`              | Setidaknya satu koneksi antara profil pengguna dan aplikasi Anda aktif.                                                                                                                                                                                                                                                     |
| `disconnected`           | Profil pengguna pernah ditautkan, dan setiap koneksi telah berakhir. `last_revoked_at` menyatakan kapan koneksi terakhir berakhir. `last_revoked_reason.type` menyatakan alasannya, misalnya `revoked_by_admin` (administrator organisasi pelanggan) atau `revoked_by_app_owner` (organisasi Anda, termasuk back end Anda). |
| `not_connected`          | Profil pengguna belum pernah ditautkan ke aplikasi Anda.                                                                                                                                                                                                                                                                    |

Perlakukan `connection_status` bernilai `null`, atau `type` yang tidak Anda kenali, sebagai tidak diketahui. Perlakukan alasan yang tidak Anda kenali sebagai `other`. `oauth_connections.data` mencantumkan koneksi-koneksi itu sendiri.

`connected` tidak menjamin bahwa permintaan akan berhasil. Nilai ini hanya menyatakan bahwa sebuah koneksi aktif. Claude API tetap memeriksa setiap permintaan yang mengatur `bill_to: "user_profile"`. Claude API dapat menolak permintaan tersebut, misalnya karena organisasi pelanggan tidak termasuk [pelanggan yang memenuhi syarat](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#eligible-customers-and-endpoints) atau telah mencapai batas pengeluaran. Jadi tangani [error yang diharapkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#expected-errors) pada setiap permintaan, bahkan untuk profil pengguna yang bertuliskan `connected`.

400 berarti header beta tidak ada atau `oauth_app_id` tidak berbentuk client ID. 403 berarti pemanggil bukan akun layanan operator dari aplikasi di `oauth_app_id`. 404 berarti profil pengguna tidak ada. Pada 503, coba ulang dengan backoff.

### Membatalkan tautan pelanggan

Untuk membatalkan tautan pelanggan di Console, gunakan daftar di [halaman User profiles](https://platform.claude.com/user-profiles) atau tombol **Unlink** di kanan atas halaman detail profil pengguna.

Untuk membatalkan tautan pelanggan dari back end Anda, kirim ID koneksi yang Anda simpan di Langkah 8 ke [endpoint pencabutan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#revocation), dengan autentikasi klien yang sama seperti pada penukaran kode. Untuk menyebutkan koneksi berdasarkan profil penggunanya, kirim `user_profile_id` sebagai pengganti `connection_id`.

<CodeGroup exclude="shell:CLI">
  ```bash cURL
  curl https://auth.claude.com/v1/oauth/revoke \
    -H "content-type: application/json" \
    -d @- <<'JSON'
  {
    "connection_id": "ocon_01HV9Z",
    "client_id": "YOUR_CLIENT_ID",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": "YOUR_CLIENT_ASSERTION_JWT"
  }
  JSON
  ```

  ```python Python
  def revoke_connection(connection_id: str) -> list[str]:
      response = httpx.post(
          f"{AUTH}/v1/oauth/revoke",
          json={
              "connection_id": connection_id,
              "client_id": CLIENT_ID,
              "client_assertion_type": JWT_BEARER,
              "client_assertion": client_assertion(),
          },
      )
      response.raise_for_status()
      # ID koneksi yang diakhiri oleh permintaan ini. Daftar kosong jika
      # koneksi sudah berakhir atau ID tidak dikenal.
      return response.json()["revoked_connection_ids"]
  ```

  ```typescript TypeScript
  // Tidak ada SDK yang mencakup auth.claude.com, jadi contoh ini memanggilnya secara langsung.
  import { readFile } from "node:fs/promises";

  // ID koneksi yang Anda simpan pada Langkah 8.
  const connectionId = "ocon_01HV9Z";

  // Client assertion: JWT di file token identitas. Baca untuk setiap permintaan, karena file dirotasi.
  // Jika autentikasi klien aplikasi Anda mengharapkan audience berbeda dari milik JWT tersebut, gunakan file token kedua.
  const clientAssertion = (
    await readFile(process.env.ANTHROPIC_IDENTITY_TOKEN_FILE!, "utf8")
  ).trim();

  const response = await fetch("https://auth.claude.com/v1/oauth/revoke", {
    method: "POST",
    redirect: "error",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      connection_id: connectionId,
      client_id: "YOUR_CLIENT_ID",
      client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      client_assertion: clientAssertion
    })
  });
  if (!response.ok) {
    throw new Error(`revoke failed: ${response.status}`);
  }

  const { revoked_connection_ids: revokedConnectionIds } = (await response.json()) as {
    revoked_connection_ids: string[];
  };
  console.log(revokedConnectionIds); // IDs of the connections this request ended. The list is empty if the connection had already ended or the ID is unknown.
  ```

  ```csharp C#
  // Tidak ada SDK yang mencakup auth.claude.com, jadi contoh ini memanggilnya secara langsung.
  using System.Net.Http.Json;
  using System.Text.Json;

  // ID koneksi yang Anda simpan pada Langkah 8.
  var connectionId = "ocon_01HV9Z";

  // Client assertion: JWT dalam file token identitas. Baca untuk setiap permintaan karena file ini dirotasi.
  // Jika autentikasi klien aplikasi Anda mengharapkan audience berbeda dari yang dimiliki JWT itu, gunakan file token kedua.
  var tokenFile = Environment.GetEnvironmentVariable("ANTHROPIC_IDENTITY_TOKEN_FILE")!;
  var clientAssertion = (await File.ReadAllTextAsync(tokenFile)).Trim();

  using var http = new HttpClient();
  using var response = await http.PostAsJsonAsync(
      "https://auth.claude.com/v1/oauth/revoke",
      new Dictionary<string, string>
      {
          ["connection_id"] = connectionId,
          ["client_id"] = "YOUR_CLIENT_ID",
          ["client_assertion_type"] = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
          ["client_assertion"] = clientAssertion,
      }
  );
  response.EnsureSuccessStatusCode();

  var result = await response.Content.ReadFromJsonAsync<JsonElement>();
  Console.WriteLine(result.GetProperty("revoked_connection_ids")); // IDs of the connections this request ended. The list is empty if the connection had already ended or the ID is unknown.
  ```

  ```go Go
  // Tidak ada SDK yang mencakup auth.claude.com, jadi contoh ini memanggilnya secara langsung.

  import (
  	"bytes"
  	"encoding/json"
  	"fmt"
  	"net/http"
  	"os"
  	"strings"
  )

  func main() {
  	// ID koneksi yang Anda simpan pada Langkah 8.
  	connectionID := "ocon_01HV9Z"

  	// Client assertion: JWT dalam file token identitas. Baca untuk setiap permintaan, karena file tersebut dirotasi.
  	// Jika autentikasi klien aplikasi Anda mengharapkan audience yang berbeda dari milik JWT tersebut, gunakan file token kedua.
  	token, err := os.ReadFile(os.Getenv("ANTHROPIC_IDENTITY_TOKEN_FILE"))
  	if err != nil {
  		panic(err)
  	}

  	body, err := json.Marshal(map[string]string{
  		"connection_id":         connectionID,
  		"client_id":             "YOUR_CLIENT_ID",
  		"client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
  		"client_assertion":      strings.TrimSpace(string(token)),
  	})
  	if err != nil {
  		panic(err)
  	}

  	response, err := http.Post("https://auth.claude.com/v1/oauth/revoke", "application/json", bytes.NewReader(body))
  	if err != nil {
  		panic(err)
  	}
  	defer response.Body.Close()
  	if response.StatusCode < 200 || response.StatusCode > 299 {
  		panic(fmt.Sprintf("revoke failed: %d", response.StatusCode))
  	}

  	var result struct {
  		RevokedConnectionIDs []string `json:"revoked_connection_ids"`
  	}
  	if err := json.NewDecoder(response.Body).Decode(&result); err != nil {
  		panic(err)
  	}
  	fmt.Println(result.RevokedConnectionIDs) // IDs of the connections this request ended. The list is empty if the connection had already ended or the ID is unknown.
  }
  ```

  ```java Java
  // Tidak ada SDK yang mencakup auth.claude.com, jadi contoh ini memanggilnya secara langsung. SDK Java menyertakan Jackson.
  import com.fasterxml.jackson.databind.ObjectMapper;
  import java.net.URI;
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;
  import java.nio.file.Files;
  import java.nio.file.Path;

  void main() throws Exception {
      // ID koneksi yang Anda simpan pada Langkah 8.
      String connectionId = "ocon_01HV9Z";

      // Client assertion: JWT dalam file token identitas. Baca file ini untuk setiap permintaan, karena file tersebut dirotasi.
      // Jika autentikasi klien aplikasi Anda mengharapkan audience yang berbeda dari yang dimiliki JWT tersebut, gunakan file token kedua.
      String clientAssertion = Files.readString(
          Path.of(System.getenv("ANTHROPIC_IDENTITY_TOKEN_FILE"))).strip();

      var mapper = new ObjectMapper();
      String body = mapper.createObjectNode()
          .put("connection_id", connectionId)
          .put("client_id", "YOUR_CLIENT_ID")
          .put("client_assertion_type", "urn:ietf:params:oauth:client-assertion-type:jwt-bearer")
          .put("client_assertion", clientAssertion)
          .toString();

      var request = HttpRequest.newBuilder(URI.create("https://auth.claude.com/v1/oauth/revoke"))
          .header("content-type", "application/json")
          .POST(HttpRequest.BodyPublishers.ofString(body))
          .build();
      var response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
      if (response.statusCode() / 100 != 2) {
          throw new IllegalStateException("revoke failed: " + response.statusCode());
      }

      // ID koneksi yang diakhiri oleh permintaan ini. Daftar kosong jika koneksi sudah berakhir atau ID tidak dikenal.
      IO.println(mapper.readTree(response.body()).get("revoked_connection_ids"));
  }
  ```

  ```php PHP
  // Tidak ada SDK yang mencakup auth.claude.com, jadi contoh ini memanggilnya secara langsung.

  // ID koneksi yang Anda simpan pada Langkah 8.
  $connectionId = 'ocon_01HV9Z';

  // Client assertion: JWT di file token identitas. Baca untuk setiap permintaan karena file tersebut dirotasi.
  // Jika autentikasi klien aplikasi Anda mengharapkan audience berbeda dari milik JWT tersebut, gunakan file token kedua.
  $clientAssertion = trim(
      file_get_contents((string) getenv('ANTHROPIC_IDENTITY_TOKEN_FILE'))
          ?: throw new \RuntimeException('the file named by ANTHROPIC_IDENTITY_TOKEN_FILE cannot be read or is empty')
  );

  $body = json_encode([
      'connection_id' => $connectionId,
      'client_id' => 'YOUR_CLIENT_ID',
      'client_assertion_type' => 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
      'client_assertion' => $clientAssertion,
  ], JSON_THROW_ON_ERROR);

  $context = stream_context_create(['http' => [
      'method' => 'POST',
      'header' => 'content-type: application/json',
      'content' => $body,
  ]]);
  $response = file_get_contents('https://auth.claude.com/v1/oauth/revoke', context: $context);
  if ($response === false) {
      throw new \RuntimeException('revoke failed');
  }

  /** @var array{revoked_connection_ids: list<string>} $result */
  $result = json_decode($response, associative: true, flags: JSON_THROW_ON_ERROR);
  // ID koneksi yang diakhiri oleh permintaan ini. Daftar kosong jika koneksi sudah berakhir atau ID tidak dikenal.
  echo implode(', ', $result['revoked_connection_ids']), PHP_EOL;
  ```

  ```ruby Ruby
  # Tidak ada SDK yang mencakup auth.claude.com, jadi contoh ini memanggilnya secara langsung.
  require "json"
  require "net/http"

  # ID koneksi yang Anda simpan pada Langkah 8.
  connection_id = "ocon_01HV9Z"

  # Client assertion: JWT dalam file token identitas. Baca untuk setiap permintaan, karena file tersebut dirotasi.
  # Jika autentikasi klien aplikasi Anda mengharapkan audience yang berbeda dari milik JWT tersebut, gunakan file token kedua.
  client_assertion = File.read(ENV.fetch("ANTHROPIC_IDENTITY_TOKEN_FILE")).strip

  response = Net::HTTP.post(
    URI("https://auth.claude.com/v1/oauth/revoke"),
    {
      connection_id: connection_id,
      client_id: "YOUR_CLIENT_ID",
      client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      client_assertion: client_assertion
    }.to_json,
    "content-type" => "application/json"
  )
  response.value # raises on an error

  # ID koneksi yang diakhiri oleh permintaan ini. Daftar kosong jika koneksi sudah berakhir atau ID tidak dikenal.
  puts(JSON.parse(response.body).fetch("revoked_connection_ids"))
  ```
</CodeGroup>

`auth.claude.com` merespons dengan HTTP 200 dan `revoked_connection_ids`, yaitu ID koneksi yang diakhiri oleh permintaan ini. Daftar tersebut kosong jika koneksi sudah berakhir, sehingga Anda dapat dengan aman mengulangi permintaan yang mengirimkan `connection_id`. Daftar tersebut juga kosong jika ID tidak dikenal, sehingga daftar kosong tidak membuktikan bahwa koneksi tersebut pernah ada. Lihat [Pencabutan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#revocation) untuk parameter lainnya dan [Error dari endpoint pencabutan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#errors-from-the-revocation-endpoint).

Untuk membatalkan tautan pelanggan melalui Claude API sebagai gantinya, kirim client ID aplikasi Anda di `oauth_app_id` ke `POST /v1/user_profiles/{id}/unlink`. Ini mengakhiri koneksi yang sama seperti endpoint pencabutan dengan `user_profile_id`. Kedua permintaan tersebut berbeda sebagai berikut:

|                   | Endpoint pencabutan                                                      | Unlink                                                                                                                                                                                                  |
| ----------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Host**          | `auth.claude.com`                                                        | `api.anthropic.com`                                                                                                                                                                                     |
| **Autentikasi**   | Autentikasi klien aplikasi Anda (Langkah 2)                              | Akun layanan operator Anda (Langkah 3): token aksesnya, atau kunci API yang terikat padanya. Token akses harus berasal dari aturan federasi dengan scope `workspace:developer`, yang merupakan default. |
| **Header beta**   | Tidak ada                                                                | `user-profiles-search-2026-08-30`                                                                                                                                                                       |
| **Yang diakhiri** | Satu koneksi, atau semua koneksi aplikasi Anda pada satu profil pengguna | Semua koneksi aplikasi Anda pada satu profil pengguna                                                                                                                                                   |

<CodeGroup exclude="shell:CLI, python, typescript, csharp, go, java, php, ruby">
  ```bash cURL
  curl https://api.anthropic.com/v1/user_profiles/uprof_01HV9Z/unlink \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: user-profiles-search-2026-08-30" \
    -H "content-type: application/json" \
    -d '{"oauth_app_id": "YOUR_CLIENT_ID"}'
  ```
</CodeGroup>

Respons berisi `revoked_connection_ids`, yaitu ID koneksi yang diakhiri oleh permintaan ini. Daftar tersebut kosong jika tidak ada koneksi yang aktif. 400 berarti `oauth_app_id` tidak ada atau tidak berbentuk client ID. 403 berarti pemanggil bukan akun layanan operator dari aplikasi di `oauth_app_id`. 404 berarti profil pengguna tidak ada atau header beta tidak ada.

Setelah koneksi berakhir, profil pengguna ditampilkan sebagai **Unlinked**, dan permintaan yang mengatur `bill_to: "user_profile"` untuk pelanggan ini menerima `user_profile_not_billable`. Anda tetap dapat melayani pelanggan dengan biaya Anda sendiri dengan `bill_to: "self"`. [Setelah menautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#after-connecting) menjelaskan apa yang dilihat pelanggan Anda, dan [Email tentang penautan dan pembatalan tautan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#emails-to-your-customer) menjelaskan cara pembatalan tautan mana yang mengirimi mereka email.

Jika permintaan unlink mengembalikan 503, permintaan tersebut mungkin hanya mengakhiri sebagian koneksi. Dalam satu hari sejak permintaan pertama, ulangi permintaan tersebut dengan backoff hingga Anda mendapatkan 200. Setelah satu hari, kirim setiap `connection_id` yang Anda simpan sebelum permintaan pertama ke endpoint pencabutan sebagai gantinya. Itu menyelesaikan apa yang tersisa, meskipun `revoked_connection_ids` kosong. Pengulangan yang selambat itu dapat mengembalikan 200 dengan daftar kosong dan melewatkan koneksi yang telah berakhir tetapi masih menyisakan token atau akses penagihan. Kirim juga `connection_id` dengan cara ini jika pelanggan mungkin telah menautkan lagi sejak permintaan pertama, karena pengulangan juga mengakhiri koneksi yang baru.

### Menautkan pelanggan ke organisasi Claude yang berbeda

Untuk menautkan profil pengguna pelanggan ke organisasi Claude yang berbeda, batalkan tautan pelanggan tersebut, lalu tautkan mereka lagi.

Setelah Anda membatalkan tautan, permintaan yang Anda tagihkan ke pelanggan ini ditolak. Hal ini berlangsung hingga seorang pengguna menyetujui untuk organisasi lain tersebut dan Anda menukarkan kode di Langkah 8. Ikuti langkah-langkah berikut saat pengguna tersebut siap menyetujui:

1. Lewati langkah ini jika pelanggan Anda sudah membatalkan tautan aplikasi Anda di halaman [Linked platforms](https://platform.claude.com/linked-platforms) mereka. Jika belum, batalkan tautan pelanggan, seperti dijelaskan dalam [Membatalkan tautan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#disconnecting-a-customer). Profil pengguna kemudian ditampilkan sebagai **Unlinked** di halaman [User profiles](https://platform.claude.com/user-profiles) Anda.
2. Jalankan lagi [Langkah 5 hingga 8](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#runtime-step-2) dengan profil pengguna yang sama. Untuk [Langkah 7](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#the-administrator-approves), pengguna memerlukan akun yang memiliki peran Admin atau Billing di organisasi lain tersebut. Minta pengguna menyetujui untuk organisasi tersebut.
3. Simpan ID koneksi baru sebagai pengganti yang sebelumnya. Jika Anda menggunakan token koneksi, lakukan hal yang sama dengan token baru.

Hingga tautan pelanggan dibatalkan, halaman persetujuan hanya memungkinkan pengguna menyetujui untuk organisasi yang sudah tertaut.

Batas atas pengeluaran dimiliki oleh satu organisasi pelanggan dan aplikasi Anda, sehingga batas atas organisasi pertama tidak terbawa. [Batas atas pengeluaran](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#spend-caps) menjelaskan aturannya.

## Error yang diharapkan

Ketika permintaan mengatur `bill_to: "user_profile"`, Anthropic menagih pelanggan Anda atau menolak permintaan. Anthropic tidak pernah diam-diam menagih Anda sebagai gantinya. Pada `/v1/messages`, kode dalam daftar berikut berada di `error.details.error_code`. Pada `/v1/chat/completions`, Anda mendapatkan status HTTP dan pesan yang sama dalam format OpenAI, tanpa kode:

* `403 permission_error, user_profile_not_billable`: Anthropic tidak dapat menagih pelanggan ini untuk permintaan ini, dan respons tidak menyebutkan alasannya. Tidak dapat dicoba ulang, kecuali dalam 10 detik pertama setelah koneksi baru. Sebelum Anda meminta pelanggan untuk menautkan kembali, lihat [Penyebab `user_profile_not_billable`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#user-profile-not-billable): menautkan kembali hanya memperbaiki sebagian penyebabnya. Anda tetap dapat melayani pelanggan dengan biaya Anda sendiri dengan mengirim ulang menggunakan `bill_to: "self"`. Di Anthropic SDK, tangani `user_profile_not_billable` berdasarkan [kelas error](https://platform.claude.com/docs/id/api/errors#sdk-error-types) untuk status 403, yaitu `PermissionDeniedError` (java, php: `PermissionDeniedException`; csharp: `AnthropicForbiddenException`; go: `apierr.StatusCode == http.StatusForbidden`). Kelas ini juga cocok dengan error 403 lainnya, jadi periksa juga kode error-nya.

* `402 billing_error, linked_organization_billing_unavailable`: Anthropic saat ini tidak dapat menagih organisasi pelanggan (misalnya, organisasi tersebut ditangguhkan, atau kreditnya habis setelah Claude mulai membalas). Respons tidak menyebutkan alasannya. Pelanggan yang tidak memiliki kredit saat permintaan tiba akan mendapatkan `linked_organization_spend_limit_reached` sebagai gantinya. Tidak dapat dicoba ulang. Minta pelanggan untuk memeriksa akun Claude Platform mereka. Anda tetap dapat melayani mereka dengan biaya Anda sendiri dengan mengirim ulang menggunakan `bill_to: "self"`.

* `402 billing_error, linked_organization_spend_limit_reached`: organisasi pelanggan telah mencapai batas pengeluaran yang ditetapkannya. Batas tersebut adalah [batas atas pengeluaran](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#spend-caps) yang berlaku untuk aplikasi Anda atau batas pengeluaran bulanan untuk seluruh organisasi. Claude API mengirim kode yang sama ketika organisasi tidak memiliki kredit yang dapat membayar permintaan tersebut. Respons tidak menyebutkan yang mana. Permintaan ditolak sebelum Claude mulai membalas. Tidak dapat dicoba ulang. Anda tetap dapat melayani pelanggan dengan biaya Anda sendiri dengan mengirim ulang menggunakan `bill_to: "self"`. Minta pelanggan untuk memeriksa hal-hal berikut di Claude Console:

  * **Batas atas pengeluaran untuk aplikasi Anda:** Di halaman untuk aplikasi Anda di bawah [Linked platforms](https://platform.claude.com/linked-platforms), mereka dapat menetapkan atau menaikkan batas atas pengeluaran. Batas atas yang ditetapkan di sana menggantikan batas atas default apa pun yang mereka tetapkan untuk semua platform yang tertaut.
  * **Batas pengeluaran bulanan organisasi:** Di bagian [Batas pengeluaran](https://platform.claude.com/settings/billing#spend-limits), mereka dapat menaikkannya.
  * **Saldo kredit:** Di halaman [Penagihan](https://platform.claude.com/settings/billing) mereka, mereka dapat melihat saldo kredit dan membeli kredit. Sebagian kredit tidak dapat membayar permintaan ini: lihat [Kredit yang dapat membayar](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#which-credits-can-pay).

* `503 overloaded_error`: Anthropic saat ini tidak dapat memastikan apakah pelanggan dapat ditagih. Coba ulang dengan backoff dan patuhi header `retry-after`. Permintaan tidak dilayani maupun ditagih.

* `400 invalid_request_error, user_profile_required`: Anda mengatur `bill_to: "user_profile"` tanpa header `anthropic-user-profile-id`. Permintaan semacam itu memerlukan header tersebut, kecuali jika permintaan menggunakan token akses koneksi dan header tersebut bersifat opsional. Untuk mengetahui apakah header tersebut opsional, lihat catatan di [Panggil Claude dengan token akses koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#call-claude-with-a-connections-access-token).

* `400 invalid_request_error`, tanpa kode error: header `anthropic-user-profile-id` memuat ID yang formatnya salah atau bukan profil pengguna organisasi Anda.

* `400 invalid_request_error`, tanpa kode error: permintaan melakukan autentikasi dengan token akses koneksi, dan mengatur `bill_to: "self"` atau menyebutkan profil pengguna selain profil yang menjadi batasan token tersebut. Lihat [Panggil Claude dengan token akses koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#call-claude-with-a-connections-access-token).

Pada `/v1/messages` dan `/v1/chat/completions`, token akses koneksi tidak dapat mengirim permintaan yang Anda bayar. Untuk mengirim ulang permintaan yang ditolak dengan `bill_to: "self"`, lakukan autentikasi dari back end Anda sendiri dengan kredensial milik akun layanan operator Anda sendiri. [Panggil Claude dengan token akses koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#call-claude-with-a-connections-access-token) mencantumkan penolakan terhadap token itu sendiri.

Respons yang berhasil tidak menyebutkan siapa yang ditagih, jadi simpan catatan Anda sendiri tentang permintaan mana yang Anda kirim dengan `bill_to: "user_profile"`.

### Penyebab `user_profile_not_billable`

Periksa hal-hal berikut secara berurutan:

* **Permintaan Anda.** Permintaan harus melakukan autentikasi sebagai akun layanan operator aplikasi OAuth Anda (Langkah 3). [Token akses koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#oauth-tokens-for-each-connection) juga melakukan autentikasi sebagai akun layanan tersebut. Permintaan yang melakukan autentikasi dengan cara lain akan ditolak. Contohnya adalah akun layanan yang berbeda dan kunci API yang tidak terikat ke akun layanan tersebut. Jika header `anthropic-user-profile-id` menyebutkan salah satu profil Anda yang tidak tertaut, permintaan akan ditolak. Jika kredensial atau header salah, perbaiki permintaan tersebut. Koneksi baru tidak membantu.
* **Koneksi.** Pelanggan belum menautkan melalui aplikasi ini, atau koneksi tersebut telah berakhir: administrator organisasi mereka atau organisasi Anda telah mengakhirinya, atau back end Anda yang mengakhirinya. Koneksi yang telah berakhir ditampilkan sebagai **Unlinked** di halaman [User profiles](https://platform.claude.com/user-profiles) Anda. Profil yang hanya tertaut melalui aplikasi pengujian Anda tidak tertaut ke aplikasi produksi Anda. Hentikan penagihan pelanggan tersebut hingga mereka menautkan. Token akses koneksi terbatas pada koneksi tersebut, jadi setelah pelanggan menautkan lagi, gunakan token akses dari koneksi yang baru. Jika aplikasi Anda telah [menonaktifkan autentikasi khusus operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#turn-off-operator-only-authentication), Anda hanya dapat menagih pelanggan dengan token akses koneksi mereka. Dalam hal itu, pelanggan yang token koneksi `billing:attribution`-nya yang berfungsi tidak Anda pegang ditampilkan sebagai **Linked**, tetapi harus menyetujui lagi, seperti dijelaskan dalam [Menautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#connect-a-customer-again).
* **Organisasi pelanggan.** Organisasi tersebut harus merupakan [pelanggan yang memenuhi syarat](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#eligible-customers-and-endpoints). Anda tidak dapat melihatnya dari sisi Anda, jadi tanyakan kepada tim akun Anthropic Anda.

Koneksi baru biasanya langsung berfungsi, tetapi dapat memerlukan waktu sekitar 10 detik setelah penukaran di Langkah 8. Jika permintaan ditolak dengan `user_profile_not_billable` dalam 10 detik tersebut, kirim lagi. Setelah itu, menunggu atau mencoba ulang tidak mengubah hasilnya. Catat seluruh `error.message` dan header respons `request-id` dari setiap permintaan yang ditolak. Jika pelanggan yang koneksinya ditampilkan sebagai **Linked** masih ditolak dan permintaan Anda sudah benar, kirimkan `request-id` dari permintaan yang ditolak ke tim akun Anthropic Anda, sehingga Anthropic dapat menelusuri alasan penolakannya.

## Tampilan dari sisi pelanggan Anda

### Menautkan

Pengguna Anda menyetujui di `auth.claude.com` setelah aplikasi Anda mengalihkan mereka di Langkah 6. [Langkah 7](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#the-administrator-approves) mencantumkan layar-layar halaman persetujuan. Setiap layar menampilkan nama aplikasi Anda dan memiliki tombol **Cancel**. Yang dilakukan pengguna di setiap layar:

* **Select an organization:** Pengguna memilih organisasi Claude mana miliknya yang akan ditautkan. Halaman menampilkan layar ini hanya jika pengguna memiliki lebih dari satu pilihan organisasi.
* **How billing works:** Pengguna membaca layar tersebut dan mengklik **Continue**.
* **Set a monthly spend limit:** Pengguna memasukkan batas untuk aplikasi Anda dalam dolar AS bulat dan mengklik **Continue**. Field jumlah dimulai dalam keadaan kosong, sehingga halaman tidak memilihkan batas untuk pengguna. **Continue without a limit** tidak menyimpan batas baru, dan batas atas atau default yang telah disimpan pelanggan sebelumnya tetap berlaku. Batas yang dimasukkan pengguna adalah batas atas pengeluaran yang dijelaskan di [Batas atas pengeluaran](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#spend-caps). Layar ini berbeda selama aplikasi Anda dalam tahap pengujian: lihat [Selama aplikasi Anda dalam tahap pengujian](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#while-your-app-is-in-testing).
* **Layar terakhir:** Layar ini mencantumkan apa saja yang dapat dilakukan aplikasi Anda, termasuk batas yang dipilih pengguna. Pengguna mengklik **Link and authorize**.

Halaman persetujuan menggunakan akun Claude mana pun yang sedang masuk di browser, dan hanya menawarkan organisasi Claude milik akun tersebut. Akun tersebut mungkin bukan akun yang diharapkan pengguna Anda, misalnya akun pribadi alih-alih akun kerja. Aplikasi Anda tidak dapat memilih akun tersebut. Parameter OpenID Connect `prompt=select_account` dan `login_hint` tidak mengubah akun yang digunakan halaman tersebut.

### Setelah menautkan

Pelanggan Anda mengelola koneksi mereka di halaman [Linked platforms](https://platform.claude.com/linked-platforms) di Claude Console. Mereka dapat membatalkan tautan aplikasi Anda kapan saja. Anthropic tidak memberi tahu Anda saat mereka melakukannya: Anda tidak menerima event webhook maupun email. Untuk memeriksa status pelanggan, lihat [Membaca status tautan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#reading-link-status).

Setelah pelanggan membatalkan tautan, permintaan yang Anda tagihkan ke pelanggan tersebut ditolak dengan 403 `user_profile_not_billable` (lihat [Penyebab `user_profile_not_billable`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#user-profile-not-billable)). Profil pengguna pelanggan tersebut ditampilkan sebagai **Unlinked** di halaman [User profiles](https://platform.claude.com/user-profiles) Anda di Console. Untuk menautkan kembali, jalankan lagi [Langkah 5 hingga 8](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#runtime-step-2) dengan profil pengguna pelanggan yang sudah ada.

### Email tentang penautan dan pembatalan tautan

Email Anthropic tentang penautan dan pembatalan tautan dikirim ke anggota organisasi pelanggan Anda yang memiliki peran Admin atau Billing. Setiap email berisi tautan ke halaman Linked platforms pelanggan. Apakah Anthropic mengirim email bergantung pada peristiwanya:

* **Saat pelanggan menautkan aplikasi Anda:** Anthropic mengirim email saat Anda menukarkan kode di Langkah 8. Anthropic tidak mengirim apa pun untuk persetujuan yang kodenya tidak pernah Anda tukarkan. Anthropic juga tidak mengirim apa pun saat pengguna menyetujui lagi selagi pelanggan masih tertaut.
* **Saat pelanggan membatalkan tautan aplikasi Anda:** Anthropic mengirim email. Email tersebut tidak menyebutkan orang yang membatalkan tautan aplikasi Anda.
* **Saat Anda membatalkan tautan pelanggan dari back end Anda:** Anthropic mengirim email.
* **Saat Anda membatalkan tautan pelanggan di Console:** Anthropic tidak mengirim email.

Anthropic tidak menjamin bahwa email terkirim atau sampai. Beri tahu sendiri pelanggan Anda saat Anda membatalkan tautan mereka. Jangan mengandalkan email ini untuk memberi tahu pelanggan bahwa mereka telah tertaut.

### Batas atas pengeluaran

Pelanggan Anda dapat menetapkan “spend cap” (batas atas pengeluaran) bulanan untuk aplikasi Anda, dalam dolar AS (USD). Halaman persetujuan menyebut batas atas ini sebagai batas pengeluaran bulanan, dan pengguna yang menautkan dapat menetapkannya di sana (lihat [Menautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#connecting)). Batas atas ini terpisah dari **Batas pengeluaran bulanan** organisasi, yang berlaku untuk seluruh organisasi. Anda tidak dapat membaca batas atas pelanggan, maupun berapa banyak yang telah mereka gunakan darinya.

Ketika pengeluaran pelanggan melalui aplikasi Anda mencapai batas atas, Claude API menolak permintaan yang Anda tagihkan kepada mereka dengan 402. Lihat [Error yang diharapkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#expected-errors). Penolakan berlangsung hingga pukul 00.00 UTC pada hari pertama bulan berikutnya, atau hingga pelanggan menaikkan atau menghapus batas atas tersebut. Perubahan pada batas atas dapat memerlukan waktu sekitar satu menit untuk berlaku.

Setelah menautkan, anggota organisasi pelanggan dengan peran Admin atau Billing mengelola batas atas di halaman [Linked platforms](https://platform.claude.com/linked-platforms) di Console:

* **Menetapkan atau mengubah batas atas:** Mereka mengklik aplikasi Anda, lalu **Set spend cap** atau **Edit spend cap**.
* **Menetapkan default:** Di bawah **Default spend cap**, mereka mengklik **Set default** atau **Edit**. Setiap aplikasi tertaut yang tidak memiliki batas atas sendiri dapat membelanjakan hingga nilai default tersebut setiap bulan. Aplikasi-aplikasi tersebut tidak berbagi nilai tersebut.
* **Menghapus batas atas:** Mereka mengklik aplikasi Anda, **Edit spend cap**, lalu **Remove cap**. Aplikasi Anda kemudian menggunakan nilai default. Jika tidak ada default, aplikasi Anda tidak memiliki batas atas.

Batas atas terkecil adalah $0 USD, yang menolak setiap permintaan yang Anda tagihkan ke pelanggan tersebut. Console menerima nilai dolar bulat, tanpa batas maksimum praktis. Batas atas menghitung biaya token dan biaya pencarian web berdasarkan harga daftar, sebelum diskon apa pun yang dinegosiasikan. Tagihan pelanggan dapat berbeda dari jumlah yang dihitung oleh batas atas.

Batas atas dapat lebih tinggi daripada **Batas pengeluaran bulanan** organisasi, yang ditetapkan pelanggan di bawah [Batas pengeluaran](https://platform.claude.com/settings/billing#spend-limits). Claude API menolak permintaan yang Anda tagihkan ke pelanggan ketika salah satu dari keduanya tercapai.

#### Selama aplikasi Anda dalam tahap pengujian

Batasan berikut berlaku setiap kali seseorang menautkan aplikasi Anda atau mengubah batas atasnya selama aplikasi dalam tahap pengujian, dalam peninjauan, atau tidak disetujui:

|                                                     | Dalam pengujian, dalam peninjauan, atau tidak disetujui | Setelah aplikasi aktif       |
| --------------------------------------------------- | ------------------------------------------------------- | ---------------------------- |
| Batas pengeluaran bulanan di halaman persetujuan    | Wajib, $50 USD atau kurang                              | Opsional                     |
| Field jumlah di halaman persetujuan                 | Dimulai dari $50 USD                                    | Dimulai dalam keadaan kosong |
| **Continue without a limit** di halaman persetujuan | Tidak ditawarkan                                        | Ditawarkan                   |
| Menghapus batas atas di Console                     | Tidak bisa                                              | Bisa                         |
| Batas atas terbesar yang dapat ditetapkan pelanggan | $50 USD                                                 | Tanpa batas maksimum praktis |

Setelah aplikasi Anda aktif, batas atas yang telah disimpan pelanggan sebelum itu tetap berlaku. Pelanggan kemudian dapat menaikkan atau menghapusnya.

### Memberikan dukungan kepada pelanggan Anda

Anda memberikan dukungan kepada pelanggan Anda untuk segala hal terkait aplikasi Anda, termasuk penggunaan Claude yang Anda tagihkan kepada mereka. Anthropic menyediakan halaman persetujuan dan halaman Linked platforms di Claude Console bagi pelanggan Anda. Di halaman Linked platforms, anggota dengan peran Admin atau Billing dapat melihat biaya yang ditimbulkan aplikasi Anda bagi organisasi bulan ini. Mereka juga dapat menetapkan [batas atas pengeluaran](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#spend-caps) bulanan untuk aplikasi Anda, dan membatalkan tautannya. Semua pertanyaan lain tentang aplikasi Anda harus diajukan kepada Anda, jadi beri tahu pelanggan Anda cara menghubungi Anda.

## Inisialisasi cuplikan kode

Contoh Python di halaman ini berbagi penyiapan berikut, yang Anda tulis satu kali. Penyiapan ini mendefinisikan:

* import
* client ID dan redirect URI aplikasi Anda
* nilai header beta penagihan
* klien Claude API yang melakukan autentikasi sebagai akun layanan Anda
* `client_assertion`, yang mengembalikan client assertion yang dikirim back end Anda ke `auth.claude.com`

```python
# Contoh Python mengasumsikan inisialisasi dan variabel berikut
import secrets
from urllib.parse import urlencode

import anthropic
import httpx
from anthropic.lib.credentials import IdentityTokenFile
from anthropic.types import Message
from anthropic.types.beta import BetaMessage
from authlib.oauth2.rfc7636 import create_s256_code_challenge

AUTH = "https://auth.claude.com"
# salin dari platform.claude.com setelah Anda mendaftarkan aplikasi OAuth Anda.
CLIENT_ID = "YOUR_CLIENT_ID"
REDIRECT_URI = "https://app.example.com/claude/billing/callback"
JWT_BEARER = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
BILLING_BETA = "user-profiles-billing-2026-10-01"

# Klien API. SDK menukar JWT identitas workload Anda dengan token akses
# dan memperbaruinya, sehingga Anda tidak perlu menangani "Bearer <access token>" sendiri.
client = anthropic.Anthropic()

# Client assertion untuk auth.claude.com: JWT identitas itu sendiri, dibaca ulang di
# setiap panggilan karena file dirotasi. Jika pengaturan autentikasi klien aplikasi Anda
# menyebut audience yang berbeda dari aturan federasi Anda, arahkan ini ke
# file token kedua: IdentityTokenFile("/path/to/other/token").
client_assertion = IdentityTokenFile()
```
