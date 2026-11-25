---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 569517228386fbb0e180b266e5e19377cbf5a65c0cf5569f7c1637b315c7f8e8
---

---
title: Kelola pelanggan tertaut
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers
description: "Periksa dan kelola pelanggan yang ditautkan: lihat penggunaan mereka, batalkan tautan atau tautkan kembali, serta pindahkan mereka ke organisasi lain atau dari kunci API mereka."
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Setelah pelanggan menautkan, Anda mengelola mereka dari Claude Console dan dari back end Anda. Setiap pelanggan memiliki [profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) di organisasi Anda, yang Anda buat untuk menautkan mereka. Penautan membuat koneksi, yaitu catatan yang mengikat organisasi Claude pelanggan ke profil tersebut.

## Sebelum Anda memulai

* **ID pelanggan:** ID profil pengguna (`uprof_…`) dan `connection_id` (`ocon_…`) yang Anda simpan saat Anda [menautkan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#save-the-connection-and-its-tokens).
* **Untuk memeriksa status pelanggan atau menggunakan endpoint pembatalan tautan:** [akun layanan operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#service-account) aplikasi Anda dengan token akses dari [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Token tersebut harus berasal dari aturan federasi dengan scope `workspace:developer`, yang merupakan default.
* **Untuk membatalkan tautan melalui `auth.claude.com`:** [autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#set-up-client-authentication) aplikasi Anda. Contoh-contoh membaca client assertion dari file yang dinamai oleh variabel lingkungan `CLIENT_ASSERTION_FILE`, atau Anda menempelkannya sebagai pengganti `YOUR_CLIENT_ASSERTION_JWT`. Ini adalah JWT untuk **Expected audience** aplikasi Anda.
* **Untuk membaca penggunaan dari back end Anda:** [kredensial Admin API](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#if-you-read-usage-from-your-back-end).

## Melihat pelanggan dan penggunaan

Buka halaman [User profiles](https://platform.claude.com/user-profiles) di Console. Tab **Overview** aplikasi Anda juga mencantumkan pelanggan yang ditautkan. Untuk setiap profil pengguna, halaman User profiles mencantumkan **Requests**, **Tokens**, dan **Your spend** selama 28 hari terakhir. Klik sebuah profil untuk melihat penggunaannya selama 7, 28, atau 90 hari terakhir.

* Profil dengan koneksi aktif bertuliskan **Linked**, profil yang koneksinya telah berakhir bertuliskan **Unlinked**, dan profil yang tidak pernah ditautkan bertuliskan **Not linked**. Hanya anggota dengan peran Admin yang melihat status-status ini dan **Unlink**.
* **Your spend** adalah biaya Anda sendiri untuk permintaan profil tersebut, sebelum Anthropic menerapkan kredit apa pun.
* Permintaan yang dibayar oleh pelanggan menambah **Requests** dan **Tokens** dan tidak menambah apa pun ke **Your spend**.
* Halaman ini tidak menampilkan apa yang dibayar pelanggan atau tarif pelanggan.

Angka-angka diperbarui sekitar sekali per jam, dan sebuah permintaan dapat memerlukan beberapa jam untuk muncul.

Jangan gunakan angka-angka ini untuk menghentikan penggunaan pelanggan pada jumlah yang Anda pilih. [Batas atas pengeluaran](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#spend-caps) milik pelanggan sendiri yang melakukannya.

## Memeriksa apakah pelanggan ditautkan

Dari back end Anda, panggil `GET /v1/user_profiles/{id}` dengan ID profil pengguna pelanggan. Kirim client ID aplikasi Anda di `oauth_app_id`, dan kirim beta header `user-profiles-search-2026-08-30`. Lakukan autentikasi sebagai akun layanan operator Anda. SDK tidak mengirim `oauth_app_id`, sehingga contoh ini memanggil endpoint melalui HTTP.

Dalam contoh ini, `ANTHROPIC_AUTH_TOKEN` menyimpan token akses akun layanan, yang Anda [dapatkan dari workload Anda](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#authenticate-from-your-workload). Atur variabel ini hanya di tempat Anda menjalankan cURL: SDK dan CLI akan menggunakannya sebagai pengganti federasi.

<CodeGroup exclude="shell:CLI, python, typescript, csharp, go, java, php, ruby">
  ```bash cURL
  curl "https://api.anthropic.com/v1/user_profiles/uprof_01HV9Z?oauth_app_id=clid_01ABcDeFgHiJkLmNoPqRsTuV" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: user-profiles-search-2026-08-30"
  ```
</CodeGroup>

Dalam respons, `connection_status.type` menjelaskan koneksi profil ke aplikasi Anda:

| `connection_status.type` | Di Console | Arti |
| ----- | ----- | ----- |
| `connected` | **Linked** | Koneksi ke aplikasi Anda aktif |
| `disconnected` | **Unlinked** | Profil pernah ditautkan, dan koneksinya telah berakhir |
| `not_connected` | **Not linked** | Profil tidak pernah ditautkan ke aplikasi Anda |

Status `connected` tidak menjamin bahwa permintaan akan ditagihkan ke pelanggan. Pada setiap permintaan yang ditagihkan ke pelanggan, tangani kedua kode `403` dan kedua [kesalahan penagihan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#while-billing) `402`.

Untuk profil `disconnected`, field-field berikut memberikan informasi lebih lanjut. Alasan yang tercantum adalah contoh:

| Field | Apa yang dinyatakannya |
| ----- | ----- |
| `last_revoked_at` | Kapan koneksi terakhir berakhir |
| `last_revoked_reason.type` | Alasannya. `revoked_by_admin`: anggota organisasi pelanggan dengan peran Admin atau Billing membatalkan tautan aplikasi Anda. `revoked_by_app_owner`: organisasi Anda atau back end Anda membatalkan tautan pelanggan. |

Untuk status apa pun, `oauth_connections.data` mencantumkan koneksi profil ke aplikasi Anda, hingga 100, dengan `truncated` diatur ketika daftar mungkin tidak lengkap.

## Membatalkan tautan pelanggan

<Warning>
  Membatalkan tautan menghentikan permintaan baru yang ditagihkan ke pelanggan hingga Anda menukar kode dari persetujuan baru.
</Warning>

Di Console, Anda dapat membatalkan tautan pelanggan di dua tempat:

* **Tab Overview aplikasi Anda:** Di bawah **Linked customers**, **Unlink** di menu baris pelanggan hanya mengakhiri koneksi mereka ke aplikasi tersebut.
* **Halaman User profiles:** **Unlink** ada di menu baris profil dan di kanan atas halamannya. Ini mengakhiri koneksi profil ke semua aplikasi Anda, termasuk aplikasi uji.

Dari back end Anda, kirim permintaan pencabutan ke `auth.claude.com` dengan autentikasi klien aplikasi Anda dan salah satu dari berikut ini:

* **`connection_id`:** Mengakhiri satu koneksi tersebut. Gunakan jika Anda memilikinya.
* **`user_profile_id`:** Dikirim sebagai pengganti `connection_id`, ini mengakhiri setiap koneksi aplikasi Anda pada profil tersebut. Termasuk koneksi yang dibuat pelanggan setelah Anda menyimpan ID Anda.

<CodeGroup exclude="shell:CLI">
  ```bash cURL
  curl https://auth.claude.com/v1/oauth/revoke \
    -H "content-type: application/json" \
    -d @- <<'JSON'
  {
    "connection_id": "ocon_01HV9Z",
    "client_id": "clid_01ABcDeFgHiJkLmNoPqRsTuV",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": "YOUR_CLIENT_ASSERTION_JWT"
  }
  JSON
  ```

  <CodeGroupItem language="CLI">
    CLI `ant` tidak memiliki perintah untuk `auth.claude.com`. Kirim permintaan dengan cURL atau dalam bahasa aplikasi Anda.
  </CodeGroupItem>

  ```python Python
  import os
  from pathlib import Path

  import httpx2  # comes with the Anthropic SDK

  # ID koneksi yang Anda simpan saat menautkan pelanggan
  connection_id = "ocon_01HV9Z"

  assertion_file = Path(os.environ["CLIENT_ASSERTION_FILE"])

  response = httpx2.post(
      "https://auth.claude.com/v1/oauth/revoke",
      json={
          "connection_id": connection_id,
          "client_id": "clid_01ABcDeFgHiJkLmNoPqRsTuV",
          "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
          "client_assertion": assertion_file.read_text().strip(),
      },
      timeout=10,
  )
  if not response.is_success:
      raise RuntimeError(f"Revoke failed: {response.status_code} {response.text}")

  print(response.json()["revoked_connection_ids"])
  ```

  ```typescript TypeScript
  import { readFile } from "node:fs/promises";

  // ID koneksi yang Anda simpan saat menautkan pelanggan
  const connectionId = "ocon_01HV9Z";

  const jwt = await readFile(process.env.CLIENT_ASSERTION_FILE!, "utf8");

  const response = await fetch("https://auth.claude.com/v1/oauth/revoke", {
    method: "POST",
    redirect: "error",
    signal: AbortSignal.timeout(10_000),
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      connection_id: connectionId,
      client_id: "clid_01ABcDeFgHiJkLmNoPqRsTuV",
      client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      client_assertion: jwt.trim()
    })
  });
  if (!response.ok) {
    throw new Error(`Revoke failed: ${response.status} ${await response.text()}`);
  }

  const result = (await response.json()) as { revoked_connection_ids: string[] };
  console.log(result.revoked_connection_ids);
  ```

  ```csharp C#
  using System.Net.Http.Json;
  using System.Text.Json;

  // ID koneksi yang Anda simpan saat menautkan pelanggan
  var connectionId = "ocon_01HV9Z";

  var assertionFile = Environment.GetEnvironmentVariable("CLIENT_ASSERTION_FILE")!;
  var jwt = await File.ReadAllTextAsync(assertionFile);

  using var http = new HttpClient { Timeout = TimeSpan.FromSeconds(10) };
  using var response = await http.PostAsJsonAsync(
      "https://auth.claude.com/v1/oauth/revoke",
      new Dictionary<string, string>
      {
          ["connection_id"] = connectionId,
          ["client_id"] = "clid_01ABcDeFgHiJkLmNoPqRsTuV",
          ["client_assertion_type"] = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
          ["client_assertion"] = jwt.Trim(),
      }
  );
  if (!response.IsSuccessStatusCode)
  {
      var details = await response.Content.ReadAsStringAsync();
      throw new HttpRequestException($"Revoke failed: {(int)response.StatusCode} {details}");
  }

  var result = await response.Content.ReadFromJsonAsync<JsonElement>();
  Console.WriteLine(result.GetProperty("revoked_connection_ids"));
  ```

  ```go Go
  import (
  	"bytes"
  	"encoding/json"
  	"fmt"
  	"io"
  	"log"
  	"net/http"
  	"os"
  	"strings"
  	"time"
  )

  func main() {
  	// ID koneksi yang Anda simpan saat menautkan pelanggan
  	connectionID := "ocon_01HV9Z"

  	jwt, err := os.ReadFile(os.Getenv("CLIENT_ASSERTION_FILE"))
  	if err != nil {
  		log.Fatal(err)
  	}

  	body, err := json.Marshal(map[string]string{
  		"connection_id":         connectionID,
  		"client_id":             "clid_01ABcDeFgHiJkLmNoPqRsTuV",
  		"client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
  		"client_assertion":      strings.TrimSpace(string(jwt)),
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	httpClient := &http.Client{Timeout: 10 * time.Second}
  	endpoint := "https://auth.claude.com/v1/oauth/revoke"
  	response, err := httpClient.Post(endpoint, "application/json", bytes.NewReader(body))
  	if err != nil {
  		log.Fatal(err)
  	}
  	defer response.Body.Close()
  	if response.StatusCode/100 != 2 {
  		details, _ := io.ReadAll(response.Body)
  		log.Fatalf("revoke failed: %d %s", response.StatusCode, details)
  	}

  	var result struct {
  		RevokedConnectionIDs []string `json:"revoked_connection_ids"`
  	}
  	if err := json.NewDecoder(response.Body).Decode(&result); err != nil {
  		log.Fatal(err)
  	}
  	fmt.Println(result.RevokedConnectionIDs)
  }
  ```

  ```java Java
  import module java.base;
  import module java.net.http;
  import com.fasterxml.jackson.databind.ObjectMapper; // Jackson comes with the Anthropic SDK

  void main() throws Exception {
      // ID koneksi yang Anda simpan saat menautkan pelanggan
      var connectionId = "ocon_01HV9Z";

      var jwt = Files.readString(Path.of(System.getenv("CLIENT_ASSERTION_FILE")));

      var mapper = new ObjectMapper();
      var body = mapper.createObjectNode()
          .put("connection_id", connectionId)
          .put("client_id", "clid_01ABcDeFgHiJkLmNoPqRsTuV")
          .put("client_assertion_type", "urn:ietf:params:oauth:client-assertion-type:jwt-bearer")
          .put("client_assertion", jwt.strip());

      var request = HttpRequest.newBuilder(URI.create("https://auth.claude.com/v1/oauth/revoke"))
          .header("content-type", "application/json")
          .timeout(Duration.ofSeconds(10))
          .POST(HttpRequest.BodyPublishers.ofString(body.toString()))
          .build();
      var response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
      if (response.statusCode() / 100 != 2) {
          throw new IOException("Revoke failed: " + response.statusCode() + " " + response.body());
      }

      IO.println(mapper.readTree(response.body()).get("revoked_connection_ids"));
  }
  ```

  ```php PHP
  // ID koneksi yang Anda simpan saat menautkan pelanggan
  $connectionId = 'ocon_01HV9Z';

  $jwt = file_get_contents((string) getenv('CLIENT_ASSERTION_FILE'))
      ?: throw new \RuntimeException('Cannot read the client assertion file');

  $body = json_encode([
      'connection_id' => $connectionId,
      'client_id' => 'clid_01ABcDeFgHiJkLmNoPqRsTuV',
      'client_assertion_type' => 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
      'client_assertion' => trim($jwt),
  ], JSON_THROW_ON_ERROR);

  $context = stream_context_create(['http' => [
      'method' => 'POST',
      'header' => 'content-type: application/json',
      'content' => $body,
      'timeout' => 10,
      'ignore_errors' => true, // keep the body of an error response
  ]]);
  $response = file_get_contents('https://auth.claude.com/v1/oauth/revoke', context: $context);
  $status = http_get_last_response_headers()[0] ?? '';
  if ($response === false || !preg_match('{^HTTP/\S+ 2}', $status)) {
      throw new \RuntimeException("Revoke failed: {$status} {$response}");
  }

  /** @var array{revoked_connection_ids: list<string>} $result */
  $result = json_decode($response, associative: true, flags: JSON_THROW_ON_ERROR);
  echo implode(', ', $result['revoked_connection_ids']), PHP_EOL;
  ```

  ```ruby Ruby
  require "json"
  require "net/http"

  # ID koneksi yang Anda simpan saat menautkan pelanggan
  connection_id = "ocon_01HV9Z"

  jwt = File.read(ENV.fetch("CLIENT_ASSERTION_FILE"))

  body = {
    connection_id:,
    client_id: "clid_01ABcDeFgHiJkLmNoPqRsTuV",
    client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    client_assertion: jwt.strip
  }
  response = Net::HTTP.start("auth.claude.com", 443, use_ssl: true, read_timeout: 10) do |http|
    http.post("/v1/oauth/revoke", body.to_json, "content-type" => "application/json")
  end
  raise "Revoke failed: #{response.code} #{response.body}" unless response.is_a?(Net::HTTPSuccess)

  puts(JSON.parse(response.body).fetch("revoked_connection_ids"))
  ```
</CodeGroup>

`revoked_connection_ids` dalam respons mencantumkan koneksi yang diakhiri oleh permintaan tersebut. Daftar kosong berarti tidak ditemukan koneksi untuk diakhiri: biasanya koneksi sudah berakhir, atau ID tidak dikenal. Ini berarti Anda dapat dengan aman mengulangi permintaan yang mengirim `connection_id`. Untuk memastikan, [periksa apakah pelanggan ditautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#check-a-links-status). Untuk membatalkan tautan melalui Claude API, lihat [Jika Anda membatalkan tautan melalui Claude API](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#if-you-unlink-through-the-claude-api).

Setelah Anda membatalkan tautan, hal-hal berikut terjadi:

* Profil ditampilkan sebagai **Unlinked**. Membatalkan tautan tidak menghapusnya.
* Token OAuth koneksi berhenti berfungsi, sehingga Anda dapat menghapusnya dari penyimpanan rahasia Anda.
* Permintaan baru yang ditagihkan ke pelanggan biasanya berhenti dalam sekitar 10 detik, siapa pun yang membatalkan tautan. Permintaan yang sudah berjalan akan selesai dan ditagihkan ke pelanggan.
* Permintaan yang ditagihkan ke pelanggan mendapatkan [`403 user_profile_billing_not_authorized`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-billing-not-authorized). Permintaan yang dikirim dengan token akses pelanggan dapat mendapatkan [`401 authentication_error`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#authentication-error) sebagai gantinya.
* Anthropic mengirim email ke anggota Admin dan Billing pelanggan ketika Anda membatalkan tautan dari back end Anda melalui salah satu rute. Anthropic tidak mengirim email kepada mereka ketika Anda membatalkan tautan di Console. Lihat [email mana yang diterima pelanggan Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#emails).

Anda tetap dapat melayani pelanggan dengan biaya Anda sendiri menggunakan [`bill_to: "self"`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#you-pay). Beri tahu pelanggan sendiri setiap kali Anda membatalkan tautan mereka, karena Anthropic tidak menjamin bahwa email dikirim atau diterima.

## Menautkan pelanggan kembali

Jika koneksi pelanggan telah berakhir (**Unlinked**), [arahkan mereka untuk menyetujui](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#send-them-to-approve) kembali dengan profil pengguna mereka yang sudah ada. Tidak ada yang perlu dibatalkan tautannya, dan profil baru akan memecah riwayat penggunaan mereka.

Selama koneksi aktif, apa yang Anda lakukan bergantung pada apakah koneksi tersebut memiliki refresh token, yang dimilikinya jika pelanggan menyetujui `offline_access`:

* **Koneksi tidak memiliki refresh token:** Jangan membatalkan tautan. Arahkan mereka untuk menyetujui kembali dengan `scope` yang sama, yang [memberi Anda token akses baru](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#if-a-customer-approves-again). Jika token akses bocor, [batalkan tautan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#unlink-a-customer) terlebih dahulu, karena menyetujui kembali tidak mencabutnya.
* **Koneksi memiliki refresh token, bahkan yang Anda hilangkan:** Batalkan tautan pelanggan, lalu minta mereka menyetujui kembali, seperti yang dijelaskan dalam langkah-langkah berikut.

Ketika koneksi pelanggan memiliki refresh token, tautkan pelanggan kembali dalam kasus-kasus berikut:

* Penyegaran mengembalikan `invalid_grant`, atau penyegaran yang gagal membuat Anda berhenti menyegarkan pelanggan tersebut. Pertama, [pastikan bukan karena penangguhan atau penyebab di pihak Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#if-a-refresh-fails).
* Anda kehilangan refresh token, refresh token bocor, atau Anda kehilangan respons dari penukaran kode.
* Refresh token mendekati masa kedaluwarsa 1 tahunnya.
* Anda mengubah akun layanan operator, dan Anda menggunakan token OAuth pelanggan ini.

Penagihan melalui koneksi berhenti sejak pembatalan tautan hingga penukaran kode baru Anda berhasil. Pertama, sepakati waktu dengan orang yang memiliki peran Admin atau Billing di organisasi pelanggan. Kemudian:

1. Jika profil ditampilkan sebagai **Linked**, [batalkan tautan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#unlink-a-customer).
2. [Arahkan pelanggan untuk memberikan persetujuan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#send-them-to-approve) kembali dengan profil pengguna mereka yang sudah ada dan scope yang sama, yang mencakup `offline_access`.
3. Simpan `connection_id` baru dan token OAuth baru sebagai pengganti yang sebelumnya. Profil kemudian ditampilkan sebagai **Linked** lagi.

## Memindahkan pelanggan ke organisasi lain

Untuk menagih pelanggan melalui organisasi Claude mereka yang lain, batalkan tautan mereka dan tautkan kembali. Sampai Anda membatalkan tautan, halaman persetujuan hanya menawarkan organisasi yang sudah ditautkan. Sejak pembatalan tautan hingga Anda menukar kode dari persetujuan untuk organisasi lain tersebut, permintaan yang ditagihkan ke pelanggan akan ditolak.

Mulailah ketika orang dengan peran Admin atau Billing di organisasi lain siap untuk menyetujui. Kemudian:

1. Kecuali pelanggan sudah membatalkan tautan aplikasi Anda di halaman [Linked platforms](https://platform.claude.com/linked-platforms) mereka, [batalkan tautan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#unlink-a-customer).
2. [Arahkan mereka untuk menyetujui](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#send-them-to-approve) kembali dengan profil pengguna dan scope yang sama, dan minta orang tersebut menyetujui untuk organisasi lain.
3. Simpan `connection_id` baru sebagai pengganti yang sebelumnya, dan simpan token OAuth baru jika Anda menggunakannya. Profil kemudian ditampilkan sebagai **Linked** lagi, melalui organisasi lain.

Batas atas pengeluaran organisasi pertama untuk aplikasi Anda tidak terbawa. Untuk batas yang berlaku pada organisasi lain, lihat [Batas atas pengeluaran di halaman Apa yang dilihat pelanggan Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#spend-caps).

## Memindahkan pelanggan dari kunci API mereka ke Linked billing

Sebelum Anda memindahkan pelanggan dari kunci API mereka sendiri, pertimbangkan dua biaya:

* **Anda membayar untuk apa yang tidak dapat ditagihkan ke pelanggan:** [Message Batches](https://platform.claude.com/docs/id/build-with-claude/batch-processing), Claude Managed Agents, dan eksekusi kode yang dapat ditagih.
* **Permintaan berjalan di organisasi Anda:** Batas laju dan ketentuan data Anda yang berlaku. Zero data retention, business associate agreement (BAA), customer-managed encryption keys (CMEK), dan daftar IP yang diizinkan milik pelanggan tidak berlaku. Lihat [Ketentuan dan batasan siapa yang berlaku](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#whose-data-terms-and-rate-limits-apply).

Untuk memindahkan pelanggan:

1. [Tautkan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer), dan simpan `connection_id` mereka.
2. Alih-alih menggunakan kunci mereka, tagihkan permintaan mereka sebagai akun layanan operator Anda, dan atur `bill_to: "user_profile"` di [`billing_policy`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#bill-a-request).
3. Hapus kunci API yang tersimpan, dan beri tahu pelanggan bahwa Anda telah melakukannya.

Permintaan mereka kemudian menambah **Requests** profil mereka di halaman [User profiles](https://platform.claude.com/user-profiles) Anda. Permintaan tersebut tidak menambah apa pun ke **Your spend**.

## Menentukan seberapa sering memeriksa apakah pelanggan ditautkan

Pelanggan dapat membatalkan tautan aplikasi Anda kapan saja di halaman [Linked platforms](https://platform.claude.com/linked-platforms) mereka, dan Anthropic tidak memberi tahu Anda. Tentukan kapan produk Anda mengetahuinya:

* **Ketika permintaan ditolak:** Temukan [penyebab penolakan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#while-billing), dan [periksa apakah pelanggan masih ditautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#check-a-links-status).
* **Sebelum Anda menagih:** Periksa ketika pelanggan memulai sesuatu di produk Anda yang ditagihkan kepada mereka.
* **Secara terjadwal:** Periksa setiap pelanggan, dan jaga agar tampilan produk Anda tentang siapa yang ditautkan tetap terkini.

Memeriksa lebih sering menunjukkan pembatalan tautan lebih cepat, dengan konsekuensi lebih banyak permintaan.

## Detail implementasi, aturan, dan kasus khusus

Sisa halaman ini mencakup detail API di balik tugas-tugas ini. Halaman ini juga mencakup kasus khusus, seperti pembatalan tautan yang gagal.

### Jika Anda membatalkan tautan melalui Claude API

Sebagai alternatif, Anda dapat membatalkan tautan melalui endpoint pembatalan tautan Claude API: kirim client ID aplikasi Anda di `oauth_app_id` ke `POST /v1/user_profiles/{id}/unlink`. Ini mengakhiri koneksi yang sama seperti permintaan pencabutan dengan `user_profile_id`.

| Detail | Permintaan pencabutan | Endpoint pembatalan tautan |
| ----- | ----- | ----- |
| Host | `auth.claude.com` | `api.anthropic.com` |
| Autentikasi | Autentikasi klien aplikasi Anda | Akun layanan operator Anda |
| Beta header | Tidak ada | `user-profiles-search-2026-08-30` |
| Apa yang diakhirinya | Satu koneksi atau setiap koneksi aplikasi Anda pada sebuah profil | Setiap koneksi aplikasi Anda pada sebuah profil |

Dalam contoh ini, `ANTHROPIC_AUTH_TOKEN` menyimpan token akses akun layanan operator Anda, seperti dalam [Memeriksa apakah pelanggan ditautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#check-a-links-status).

<CodeGroup exclude="shell:CLI, python, typescript, csharp, go, java, php, ruby">
  ```bash cURL
  curl https://api.anthropic.com/v1/user_profiles/uprof_01HV9Z/unlink \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: user-profiles-search-2026-08-30" \
    -H "content-type: application/json" \
    -d '{"oauth_app_id": "clid_01ABcDeFgHiJkLmNoPqRsTuV"}'
  ```
</CodeGroup>

Respons memiliki `revoked_connection_ids`, yang kosong jika tidak ada koneksi yang aktif.

### Jika endpoint pembatalan tautan mengembalikan 503

`503` dari endpoint pembatalan tautan berarti endpoint tersebut mungkin hanya mengakhiri sebagian koneksi. Kirim permintaan pencabutan untuk setiap `connection_id` yang telah Anda simpan sebelum permintaan yang gagal. Itu berfungsi kapan saja. Ini mengakhiri apa yang tersisa dan tidak menyentuh koneksi yang dibuat pelanggan sejak saat itu.

Mengulangi pembatalan tautan dengan backoff juga berfungsi dalam satu hari sejak permintaan pertama, tetapi juga mengakhiri koneksi yang dibuat pelanggan sejak saat itu. Setelah satu hari, pengulangan dapat mengembalikan `200` dengan daftar kosong. Pengulangan yang lebih lambat itu juga tidak mencabut sisa dari koneksi yang diakhiri oleh permintaan yang gagal, sehingga koneksi tersebut dapat mempertahankan token OAuth atau akses penagihan.

### Jika pemeriksaan status atau endpoint pembatalan tautan menolak permintaan

| Status | Pemeriksaan status | Endpoint pembatalan tautan |
| ----- | ----- | ----- |
| `400` | `oauth_app_id` tidak dalam bentuk client ID, atau beta header tidak ada | `oauth_app_id` tidak ada atau tidak dalam bentuk client ID |
| `401` | Kredensial tidak ada atau tidak valid, atau aturan federasinya tidak memberikan `workspace:developer` | Sama |
| `403` | Pemanggil bukan akun layanan operator dari aplikasi di `oauth_app_id`, atau menggunakan token akun tersebut yang terbatas pada satu sesi | Sama |
| `404` | Profil pengguna tidak ada | Profil pengguna tidak ada, atau beta header tidak ada |
| `503` | Coba lagi dengan backoff | Lihat [Jika endpoint pembatalan tautan mengembalikan 503](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#if-an-unlink-returns-a-503) |

Kesalahan milik permintaan pencabutan itu sendiri ada di [Error dari endpoint pencabutan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#errors-from-the-revocation-endpoint).

### Jika Anda membaca penggunaan dari back end Anda

[Usage and Cost Analytics API](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api) melaporkan penggunaan untuk setiap profil pengguna. Seperti Console, API ini menghitung baik permintaan yang Anda bayar maupun yang dibayar oleh pelanggan Anda.

Panggil API ini dengan kredensial Admin API, seperti token akses OAuth dengan scope `org:admin` atau [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication). Jangan gunakan akun layanan operator Anda: aturan federasinya memberikan `workspace:developer` secara default, bukan `org:admin`. Jangan tambahkan `org:admin` ke akun tersebut, karena scope itu meliputi seluruh Admin API.

Untuk mendapatkan satu baris untuk setiap profil pengguna, panggil [endpoint penggunaan](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#usage-endpoint) atau [endpoint biaya](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#cost-endpoint). Kelompokkan hanya berdasarkan `user_profile_id`, dan hilangkan `time_bucket_width`. Hanya profil dengan penggunaan dalam rentang waktu tersebut yang mendapatkan baris. Baris dengan `user_profile_id` bernilai null menyimpan penggunaan yang tidak menyebutkan profil, serta penggunaan yang diukur di luar permintaan, seperti waktu container eksekusi kode.

Pada endpoint biaya, Anda dapat mengetahui siapa yang membayar dari dua field:

| Field | Permintaan yang Anda bayar | Permintaan yang dibayar pelanggan Anda |
| ----- | ----- | ----- |
| `amount` | Biayanya, ukuran yang sama dengan **Your spend** | 0 |
| `list_amount` | Harga daftarnya | Harga daftarnya |

API tidak memiliki field atau filter untuk siapa yang membayar. Baris yang `amount`-nya 0 dan `list_amount`-nya di atas 0 biasanya berarti pelanggan membayar seluruhnya. Untuk seberapa terlambat data dapat muncul, lihat [Kesegaran data](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#data-freshness).

### Untuk agen

* Perlakukan `connection_status` bernilai `null` atau `type` yang tidak Anda kenali sebagai tidak diketahui.
* Perlakukan `last_revoked_reason.type` yang tidak Anda kenali sebagai `other`.

## Langkah selanjutnya

<CardGroup cols={1}>
  <Card title="Uji dan publikasikan aplikasi Anda" icon="rocket" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish">
    Tambahkan pengguna uji, publikasikan aplikasi Anda, dan ubah atau hapus aplikasi tersebut
  </Card>
</CardGroup>
