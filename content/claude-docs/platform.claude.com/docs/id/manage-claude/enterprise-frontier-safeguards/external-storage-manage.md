---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage
fetched_at: 2026-11-24T02:13:59.956186Z
sha256: 8bd287de6b0733d9cb55d8051896b60901d58568145559be00591c565224e931
---

---
title: Mengelola penyimpanan milik pelanggan
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage
description: Periksa status bucket Anda, perbaiki bucket jika berhenti berfungsi, serta ubah atau berhenti menggunakannya.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Gunakan halaman ini setelah sebuah workspace menggunakan [penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage) dengan [Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) (EFS). Halaman ini menjelaskan cara memeriksa status bucket Anda, memperbaiki bucket jika berhenti berfungsi, serta mengubah atau berhenti menggunakannya.

## Status bucket

Temukan status setiap bucket di bawah **Storage destinations** di halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console, dengan **Organization** dipilih di bagian atas:

| Status | Arti |
| ----- | ----- |
| **Needs setup** | <Where bucket="s3" label="Amazon S3">[**Test setup**](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#test-the-setup)</Where> <Where bucket="gcs" label="Google Cloud Storage">[**Test setup**](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-create-the-bucket)</Where> belum lolos. |
| **Ready** | Bucket Anda lolos **Test setup**, dan tidak ada workspace yang menggunakannya. |
| **Active** | Sebuah workspace diatur untuk menggunakannya. |
| **Failed last check** | Pemeriksaan terbaru tidak lolos. Lihat [Jika bucket Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#if-your-bucket-stops-working). |
| **Draining** | Tidak ada workspace yang menggunakannya sekarang, tetapi pernah ada. <Where bucket="s3" label="Amazon S3">[Simpan bucket Anda, dan akses Anthropic ke bucket tersebut](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-or-stop-using-your-bucket).</Where> <Where bucket="gcs" label="Google Cloud Storage">[Simpan bucket Anda, dan akses Anthropic ke bucket tersebut](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-stop-using-your-bucket).</Where> |
| **Deleting** | <Where bucket="s3" label="Amazon S3">Anthropic sedang [menyelesaikan penghapusan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#delete-a-storage-destination) tujuan penyimpanan ini.</Where> <Where bucket="gcs" label="Google Cloud Storage">Anthropic sedang menyelesaikan penghapusan tujuan penyimpanan ini.</Where> Anda tidak dapat menggunakannya. |

Anthropic memeriksa bucket sebelum sebuah workspace pertama kali menggunakannya. Sekali sehari, Anthropic juga memeriksa setiap bucket yang digunakan oleh sebuah workspace atau yang ditampilkan sebagai **Draining**. Pemeriksaan harian dapat lolos meskipun peran IAM bucket Anda untuk [transkrip dan Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage) gagal.

Jika pemeriksaan harian tidak dapat memastikan hasilnya, status dan waktu pemeriksaan terakhir tidak berubah, meskipun bucket Anda telah berhenti berfungsi. Bucket berstatus **Draining** tetap **Draining** meskipun gagal dalam pemeriksaan.

Jika sebuah pemeriksaan gagal, bahkan untuk bucket berstatus **Draining**, Anthropic biasanya mengirim email kepada anggota organisasi Anda yang dapat mengelola kunci enkripsi. Di [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account) dan [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#set-up-your-account), Anthropic biasanya mengirim email kepada orang yang menyelesaikan penyiapan organisasi Anda sebagai gantinya.

<Where method="api" label="Admin API">

<Where bucket="s3" label="Amazon S3">

## Periksa bucket Anda

Permintaan Admin API ini menggunakan kredensial di [Autentikasi permintaan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-authenticate) pada halaman Menyiapkan penyimpanan milik pelanggan.

Ambil satu bucket untuk melihat statusnya:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/organizations/external_storage/estrg_01SDCCSbTxrXDpWc1phhtcfK \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: efs-2026-10-01"
  ```

  ```bash CLI
  ant beta:organization:external-storage retrieve \
    --external-storage-id estrg_01SDCCSbTxrXDpWc1phhtcfK
  ```

  ```python Python
  client = anthropic.Anthropic()

  storage = client.beta.organization.external_storage.retrieve(
      "estrg_01SDCCSbTxrXDpWc1phhtcfK"
  )

  print(f"status: {storage.status.type}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const storage = await client.beta.organization.externalStorage.retrieve(
    "estrg_01SDCCSbTxrXDpWc1phhtcfK"
  );

  console.log(`status: ${storage.status.type}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var storage = await client.Beta.Organization.ExternalStorage.Retrieve(
      "estrg_01SDCCSbTxrXDpWc1phhtcfK"
  );

  Console.WriteLine($"status: {storage.Status.Type.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  storage, err := client.Beta.Organization.ExternalStorage.Get(
  	context.Background(),
  	"estrg_01SDCCSbTxrXDpWc1phhtcfK",
  	anthropic.BetaOrganizationExternalStorageGetParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("status: %s\n", storage.Status.Type)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var storage = client.beta().organization().externalStorage()
      .retrieve("estrg_01SDCCSbTxrXDpWc1phhtcfK");

  IO.println("status: " + storage.status().type());
  ```

  ```php PHP
  $client = new Client();

  $storage = $client->beta->organization->externalStorage->retrieve(
      externalStorageID: 'estrg_01SDCCSbTxrXDpWc1phhtcfK',
  );

  echo "status: {$storage->status->type}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  storage = client.beta.organization.external_storage.retrieve("estrg_01SDCCSbTxrXDpWc1phhtcfK")

  puts "status: #{storage.status.type}"
  ```
</CodeGroup>

Untuk mencantumkan semua bucket Anda, panggil `GET /v1/organizations/external_storage`. Hasil ditampilkan dari yang terbaru, 20 per halaman, atau hingga 1.000 per halaman jika Anda meneruskan `?limit=`. Untuk mendapatkan halaman berikutnya, teruskan `next_page` dari respons sebagai `?page=`.

`status.type` memberi tahu Anda posisi bucket Anda dalam siklus hidupnya. Setiap nilai sesuai dengan status yang ditampilkan Claude Console di bawah [Status bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#bucket-health):

| Status API | Status Console | Arti |
| ----- | ----- | ----- |
| `pending_configuration` | Needs setup | Terdaftar, belum diaktifkan. |
| `available` | Ready | Diaktifkan, dan tidak ada workspace yang menggunakannya. |
| `active` | Active | Setidaknya satu workspace diatur untuk menggunakannya. |
| `draining` | Draining | Tidak ada workspace yang menggunakannya sekarang, tetapi setidaknya satu workspace pernah menggunakannya sebelumnya. Simpan bucket Anda, dan akses Anthropic ke bucket tersebut, seperti yang dijelaskan di [Ubah atau berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-or-stop-using-your-bucket). |

Untuk `available`, `active`, dan `draining`, `status` juga memiliki dua field. `healthy` menyatakan apakah bucket Anda lolos pemeriksaan terakhirnya, dan `last_checked_at` menyatakan kapan pemeriksaan tersebut dijalankan. Untuk `draining`, `status` juga memiliki `removal_started`, yang bernilai `true` setelah penghapusan dimulai. Claude Console kemudian menampilkan **Deleting**. Untuk `available` dan `active`, nilai `healthy` sebesar `false` ditampilkan sebagai **Failed last check** di Claude Console. Lihat [Jika bucket Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#if-your-bucket-stops-working).

`healthy` dan `last_checked_at` diatur saat bucket Anda diaktifkan, dan saat bucket lolos pemeriksaan Anthropic sebelum dilampirkan sebagai `safeguards_storage`. Di Claude Platform, pemeriksaan harian juga mengaturnya saat pemeriksaan mencapai hasil (lihat [Status bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#bucket-health)). Jika pemeriksaan suatu hari tidak mencapai hasil, nilainya tetap seperti sebelumnya, sehingga `healthy` dapat tetap `true` meskipun bucket Anda berhenti berfungsi. Jangan hanya mengandalkan field ini. Untuk mengetahui adanya kegagalan, perhatikan objek baru di bawah `slab/` atau `safeguards-data/slab/` saat Anda mengirim permintaan.

</Where>

</Where>

## Jika bucket Anda berhenti berfungsi

<Where bucket="s3" label="Amazon S3">

Untuk memperbaiki bucket yang berhenti berfungsi, periksa [status bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#bucket-health), lalu pulihkan bucket Anda atau peran IAM-nya seperti yang dijelaskan di bagian ini.

Jika Anda memilih tujuan penyimpanan untuk sebuah workspace dalam beberapa jam terakhir dan belum ada yang masuk di bawah `slab/` atau `safeguards-data/slab/`, [perubahan tersebut mungkin belum berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#how-long-changes-take).

Selama Anthropic tidak dapat menulis ke bucket yang menyimpan [data keselamatan tersegel](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage#what-is-stored), hal berikut terjadi:

* **Permintaan:** Permintaan tetap berjalan selama masa tenggang hingga 24 jam. Setelah itu, Anthropic mungkin menolak permintaan ke workspace tersebut.
* **Data keselamatan tersegel Anda:** Anthropic mencoba ulang penulisan selama waktu terbatas. Anthropic tidak mengirim data tersebut ke penyimpanan yang dikelola Anthropic sebagai gantinya.

Untuk menghindari kehilangan data, perhatikan hal-hal berikut:

* Untuk mengetahui adanya kegagalan, pantau objek baru di bawah `slab/` atau `safeguards-data/slab/` saat Anda mengirim permintaan. Jangan menunggu email tentang kegagalan, dan jangan hanya mengandalkan [status bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#bucket-health).
* Pulihkan bucket Anda secepat mungkin. Jika Anthropic tidak dapat menulis ke bucket Anda selama lebih dari sekitar satu jam, segera beri tahu tim akun Anthropic Anda, dan beri tahu lagi saat bucket Anda sudah berfungsi. Setelah Anda memulihkan bucket Anda, Anthropic harus menjalankan pemulihan, yang tidak dijamin berhasil.
* Di Claude Platform, sekitar 72 jam setelah data keselamatan tersegel dikirim, Anthropic menghapus data apa pun yang belum dipulihkannya. Di Claude Platform on AWS, waktunya dapat lebih singkat, jadi beri tahu tim akun Anthropic Anda segera setelah Anda mengetahui adanya kegagalan.

Cara Anda memulihkan bucket bergantung pada apa yang berubah:

* **Peran IAM:** Jika sesuatu menghapus akses Anthropic ke bucket Anda, pulihkan peran-peran tersebut persis seperti sebelumnya.

  * **CloudFormation:** Jangan hapus atau perbarui stack Anda, dan jangan buat stack kedua untuk bucket ini. Sebagai gantinya, segera hubungi tim akun Anthropic Anda.
  * **Terraform:** Jalankan lagi perintah apply dari header file Terraform bucket Anda, di folder yang sama seperti sebelumnya, dengan region dan nilai-nilai yang sama. Jika Anda tidak memiliki folder tersebut, segera hubungi tim akun Anthropic Anda.
  * **Tooling Anda sendiri:** Buat ulang peran-peran tersebut dengan nama yang sama, serta dengan kebijakan kepercayaan dan izin di file dari dialog **Connect storage**. Jika Anda tidak menyimpan file tersebut, hubungi tim akun Anthropic Anda.

* **Kunci KMS bucket Anda, jika seseorang menonaktifkannya:** Aktifkan kembali.

* **Kunci KMS bucket Anda, jika seseorang menjadwalkan penghapusannya:** Batalkan penghapusan sebelum masa tunggu yang dipilih, 7 hingga 30 hari, berakhir. Lalu aktifkan kunci tersebut, karena AWS membiarkannya dalam keadaan nonaktif. Setelah masa tunggu berakhir, AWS KMS menghapus kunci tersebut, dan tidak ada yang dapat membaca apa yang dienkripsinya.

* **Kebijakan organisasi AWS:** Jika sebuah kebijakan kini menghalangi Anthropic, [tambahkan akun AWS Anthropic ke kebijakan tersebut](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#add-anthropic-to-the-rcp).

* **Kunci yang dikelola pelanggan Anda, jika workspace memilikinya:** Ikuti [Jika kunci Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#if-your-key-stops-working).

Jika peran-peran Anda memiliki nama tetap, seperti `anthropic-efs-ingest`, pulihkan penyiapan yang sama tersebut, seperti yang dijelaskan dalam daftar ini. Jangan pindahkan ke file penyiapan lain. Sebagai referensi, gunakan file yang Anda deploy.

</Where>

<Where bucket="gcs" label="Google Cloud Storage">

Lihat [Jika bucket Cloud Storage Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-if-your-bucket-stops-working).

</Where>

## Ubah atau berhenti menggunakan bucket Anda

<Where bucket="s3" label="Amazon S3">

Untuk pindah ke bucket baru atau berhenti menggunakan bucket Anda, ikuti langkah-langkah di bagian ini. Dalam kedua kasus, simpan bucket lama Anda, dan akses Anthropic ke bucket tersebut, hingga semua isi bucket Anda melewati [periode retensi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage#retention-period) dan bucket Anda tidak lagi tercantum di bawah [**Storage destinations**](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#bucket-health). [Beberapa objek tetap berada di bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#what-removes-data) setelah itu.

Sebelum Anda mengubah atau menghapus bucket sebuah workspace, [tanggapi Safety Cases yang masih terbuka di workspace tersebut](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#respond-to-a-case) dan [tunggu hingga Safety Cases tersebut ditutup](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#after-you-respond). Jika Anda mengubah atau menghapus bucket terlebih dahulu, Anthropic mungkin tidak membaca [file tanggapan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#response-file) Anda.

Selama bucket Anda ditampilkan sebagai **Draining**, pertahankan bucket tersebut, pembuatan versinya, aturan siklus hidupnya, kunci KMS-nya, dan peran-peran IAM-nya. Status **Draining** tidak berakhir dengan sendirinya. Status ini berakhir saat Anda [menghapus tujuan penyimpanan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#delete-a-storage-destination) atau memilih bucket tersebut lagi untuk sebuah workspace. Jika Anda tidak dapat menghapusnya, bicarakan dengan tim akun Anthropic Anda sebelum Anda menghapus akses Anthropic. Di Claude Platform on AWS, Anda tidak dapat menghapus tujuan penyimpanan setelah sebuah workspace menggunakannya, sehingga tujuan penyimpanan tersebut tetap ditampilkan sebagai **Draining**. Rencanakan untuk menyimpan bucket Anda dan akses Anthropic ke bucket tersebut.

Selama Anda menyimpan bucket Anda, jangan nonaktifkan kunci KMS-nya atau jadwalkan penghapusan kunci tersebut. Jika Anda melakukannya, penulisan ke bucket Anda dan pembacaan darinya mulai gagal, jadi [pulihkan kunci tersebut](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#if-your-bucket-stops-working).

Jika Anda menghapus bucket yang pernah digunakan oleh sebuah workspace, jangan buat bucket tersebut lagi dengan nama yang sama selama tujuan penyimpanannya masih tercantum. Sebagai gantinya, [siapkan bucket baru](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-your-bucket) dengan nama baru.

### Ubah bucket Anda

Untuk memindahkan workspace Anda ke bucket baru, ikuti langkah-langkah berikut. Untuk pindah ke bucket Google Cloud Storage sebagai gantinya, bicarakan dengan tim akun Anthropic Anda, karena [Anthropic membatasi jumlah bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-use-your-bucket-in-a-workspace). Di Claude Platform on AWS, tanyakan kepada tim akun Anthropic Anda sebelum Anda mengubah bucket Anda.

<Warning>
  Perpindahan tidak langsung berlaku, seperti yang dijelaskan di [Pastikan perubahan telah berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#how-long-changes-take). Data keselamatan tersegel yang baru masih dapat dikirim ke bucket lama Anda untuk sementara waktu, bahkan setelah objek masuk ke bucket baru Anda. Simpan bucket lama Anda, dan akses Anthropic ke bucket tersebut, seperti yang dijelaskan di [Ubah atau berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-or-stop-using-your-bucket). Jika Anda menghapus salah satunya lebih awal, Anda dapat kehilangan data baru.
</Warning>

1. [Buat dan hubungkan bucket baru Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles). Buat bucket tersebut dengan stack tersendiri atau, dengan Terraform, di folder tersendiri. Jangan perbarui stack yang sudah ada agar mengarah ke bucket baru, atau Anthropic kehilangan akses ke bucket lama Anda selagi bucket tersebut masih menyimpan data Anda.
2. Di setiap workspace yang menggunakan bucket lama Anda, [pilih bucket baru Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#turn-on-efs-for-a-workspace) di bawah **Sealed Safety Data storage** di Claude Console. Jangan lepaskan bucket lama Anda dari workspace terlebih dahulu, atau data keselamatan tersegel yang baru dapat dikirim ke penyimpanan yang dikelola Anthropic. Jika workspace tersebut juga menggunakan bucket lama Anda di bawah **Safety Case and Transcript storage**, pilih juga bucket baru Anda di bawah pengaturan tersebut. Lalu, simpan.

<Where method="api" label="Admin API">

Pada langkah 1, [daftarkan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-register) dan [aktifkan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-activate) bucket baru Anda. Pada langkah 2, [kirim permintaan attach](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-attach) dengan ID bucket baru Anda sebagai gantinya. Jika `transcripts_storage` menyebut bucket lama Anda, atur ke ID bucket baru dalam permintaan yang sama.

</Where>

<Where method="console" label="Claude Console">

### Berhenti menggunakan bucket Anda

Untuk berhenti menggunakan bucket Anda, lepaskan bucket tersebut dari setiap workspace terlebih dahulu, dan hapus akses Anthropic ke bucket Anda paling akhir. Workspace yang berhenti mengirim data keselamatan tersegel ke bucket Anda akan keluar dari EFS.

<Steps>
  <Step title="Lepaskan bucket Anda dari setiap workspace">
    Di halaman [Retensi data](https://platform.claude.com/settings/privacy) workspace tersebut, pilih kartu selain **Enterprise Frontier Safeguards**, lalu simpan. Secara default, kartu **Anthropic managed** mengaktifkan kembali [Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review). [Glosarium](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#glossary) menjelaskan setiap kartu.

    Untuk menghentikan hanya transkrip dan Safety Cases, pilih **Not copied to your storage** di bawah **Safety Case and Transcript storage** sebagai gantinya. Jika bucket tersebut masih menerima data keselamatan tersegel, jangan ikuti sisa langkah-langkah ini.
  </Step>

  <Step title="Simpan bucket Anda selama masa Draining">
    Setelah Anda melepaskannya dari setiap workspace, bucket Anda ditampilkan sebagai **Draining** di **Storage destinations**. Simpan bucket Anda, dan akses Anthropic ke bucket tersebut, selama statusnya masih **Draining**. Untuk mengakhiri **Draining**, [hapus tujuan penyimpanan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#delete-a-storage-destination). Di Claude Platform on AWS, bucket Anda tetap **Draining**, jadi rencanakan untuk menyimpannya dan akses Anthropic ke bucket tersebut. Jangan lakukan langkah berikutnya hingga penghapusan selesai atau tim akun Anthropic Anda memintanya. Transkrip dan Safety Cases yang sudah ada di bucket Anda tetap berada di sana hingga aturan siklus hidup bucket Anda membuatnya kedaluwarsa. Lihat [Isi bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#whats-in-the-bucket).
  </Step>

  <Step title="Hapus akses Anthropic">
    Untuk menghapus akses Anthropic, hapus peran IAM bucket Anda dengan alat yang Anda gunakan untuk membuatnya. Setelah Anda menghapus akses Anthropic, data keselamatan tersegel tetap berada di bucket Anda hingga Anda menghapusnya.

    <Tabs>
      <Tab title="CloudFormation">
        Hapus stack bucket Anda. Nama stack tersebut ada di perintah deploy Anda: `anthropic-storage-<RoleDigest>`, atau `anthropic-storage-<organization ID>` untuk penyiapan dengan nama peran tetap. Menghapus stack tetap mempertahankan bucket dan kuncinya.
      </Tab>

      <Tab title="Terraform">
        Hapus hanya peran-peran bucket Anda dan kebijakannya, agar data Anda tetap tersimpan. Di folder yang menyimpan file Terraform bucket Anda, jalankan perintah penghapusan dari header file Terraform tersebut dengan region dan nilai-nilai yang Anda gunakan saat penyiapan.

        Anda akan melihat peringatan tentang `-target`. Pastikan setiap sumber daya yang dicantumkan plan adalah `aws_iam_role` atau `aws_iam_role_policy`, lalu ketik `yes`. Apply berikutnya akan membuat ulang peran-peran tersebut.
      </Tab>

      <Tab title="Your own tooling">
        Hapus peran IAM bucket tersebut.
      </Tab>
    </Tabs>

    <Warning>
      Setelah peran-peran tersebut dihapus, jangan pilih bucket Anda lagi untuk sebuah workspace hingga peran-peran tersebut dikembalikan. Di Claude Platform on AWS, atau jika peran-peran Anda memiliki nama tetap, Anthropic tidak memeriksa bucket berstatus **Draining** sebelum Anda menyimpan, sehingga proses simpan dapat berhasil meskipun Anthropic tidak dapat menulis ke bucket Anda. Jika Anda menggunakan CloudFormation, men-deploy template lagi tidak memulihkan akses Anthropic, jadi hubungi tim akun Anthropic Anda sebelum Anda memilih bucket Anda.
    </Warning>
  </Step>
</Steps>

</Where>

<Where method="api" label="Admin API">

### Berhenti menggunakan bucket Anda

Permintaan Admin API ini menggunakan kredensial di [Autentikasi permintaan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-authenticate) pada halaman Menyiapkan penyimpanan milik pelanggan.

Untuk berhenti menggunakan bucket Anda, ikuti langkah-langkah berikut secara berurutan:

1. Lepas bucket Anda dari setiap workspace.
2. Simpan bucket Anda selama masa draining.
3. Hapus External Storage-nya.
4. [Hapus akses Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#api-remove-access).

Untuk melepas bucket Anda dari workspace, atur setiap field penyimpanan yang menyebut bucket Anda ke tipe `internal`. Field-field tersebut adalah `inference_data_privacy.safeguards_storage` dan `inference_data_privacy.transcripts_storage`, dan Anda dapat mengatur keduanya dalam permintaan yang sama. Jika Anda mengatur `safeguards_storage` ke tipe `internal`, workspace beralih ke penyimpanan yang dikelola Anthropic dan keluar dari EFS. Anthropic mungkin menolak pelepasan yang membiarkan [Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) tetap nonaktif, sehingga permintaan berikut juga mengatur `inference_data_privacy.human_review` ke tipe `enabled`, yang mengaktifkan kembali Anthropic Human Review:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: efs-2026-10-01" \
    -H "content-type: application/json" \
    -d '{
      "inference_data_privacy": {
        "safeguards_storage": {
          "type": "internal"
        },
        "human_review": {
          "type": "enabled"
        }
      }
    }'
  ```

  ```bash CLI
  ant beta:organization:workspaces update \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --beta efs-2026-10-01 <<YAML
  inference_data_privacy:
    safeguards_storage:
      type: internal
    human_review:
      type: enabled
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspace = client.beta.organization.workspaces.update(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      inference_data_privacy={
          "safeguards_storage": {"type": "internal"},
          "human_review": {"type": "enabled"},
      },
      betas=["efs-2026-10-01"],
  )

  privacy = workspace.inference_data_privacy
  if privacy and privacy.safeguards_storage:
      print(f"safeguards_storage: {privacy.safeguards_storage.type}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspace = await client.beta.organization.workspaces.update(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    {
      inference_data_privacy: {
        safeguards_storage: { type: "internal" },
        human_review: { type: "enabled" }
      },
      betas: ["efs-2026-10-01"]
    }
  );

  const type = workspace.inference_data_privacy?.safeguards_storage?.type;
  console.log(`safeguards_storage: ${type}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Workspaces;

  AnthropicClient client = new();

  var workspace = await client.Beta.Organization.Workspaces.Update(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      new()
      {
          InferenceDataPrivacy = new()
          {
              SafeguardsStorage = new BetaInternalStorageParam(),
              HumanReview = new() { Type = BetaAnthropicHumanReviewParamType.Enabled },
          },
          Betas = ["efs-2026-10-01"],
      }
  );

  var type = workspace.InferenceDataPrivacy?.SafeguardsStorage?.Type.Raw();
  Console.WriteLine($"safeguards_storage: {type}");
  ```

  ```go Go
  client := anthropic.NewClient()

  internal := anthropic.NewBetaInternalStorageParam()
  workspace, err := client.Beta.Organization.Workspaces.Update(
  	context.Background(),
  	"wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  	anthropic.BetaOrganizationWorkspaceUpdateParams{
  		InferenceDataPrivacy: anthropic.BetaInferenceDataPrivacyUpdateParam{
  			SafeguardsStorage: anthropic.BetaStorageMemberParamUnion{OfInternal: &internal},
  			HumanReview: anthropic.BetaAnthropicHumanReviewParam{
  				Type: anthropic.BetaAnthropicHumanReviewParamTypeEnabled,
  			},
  		},
  		Betas: []anthropic.AnthropicBeta{"efs-2026-10-01"},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("safeguards_storage: %s\n", workspace.InferenceDataPrivacy.SafeguardsStorage.Type)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.workspaces.BetaAnthropicHumanReviewParam;
  import com.anthropic.models.beta.organization.workspaces.BetaInferenceDataPrivacyUpdateParam;
  import com.anthropic.models.beta.organization.workspaces.BetaInternalStorageParam;
  import com.anthropic.models.beta.organization.workspaces.WorkspaceUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = WorkspaceUpdateParams.builder()
          .inferenceDataPrivacy(BetaInferenceDataPrivacyUpdateParam.builder()
              .safeguardsStorage(BetaInternalStorageParam.builder().build())
              .humanReview(BetaAnthropicHumanReviewParam.builder()
                  .type(BetaAnthropicHumanReviewParam.Type.ENABLED)
                  .build())
              .build())
          .addBeta("efs-2026-10-01")
          .build();
      var workspace = client.beta().organization().workspaces()
          .update("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ", params);

      IO.println("safeguards_storage: " + workspace.inferenceDataPrivacy()
          .flatMap(privacy -> privacy.safeguardsStorage())
          .map(storage -> storage.type().asString())
          .orElse(null));
  }
  ```

  ```php PHP
  $client = new Client();

  $workspace = $client->beta->organization->workspaces->update(
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
      inferenceDataPrivacy: [
          'safeguardsStorage' => ['type' => 'internal'],
          'humanReview' => ['type' => 'enabled'],
      ],
      betas: ['efs-2026-10-01'],
  );

  echo "safeguards_storage: {$workspace->inferenceDataPrivacy?->safeguardsStorage?->type}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace = client.beta.organization.workspaces.update(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    inference_data_privacy: {
      safeguards_storage: {
        type: :internal
      },
      human_review: {
        type: :enabled
      }
    },
    betas: ["efs-2026-10-01"]
  )

  puts "safeguards_storage: #{workspace.inference_data_privacy&.safeguards_storage&.type}"
  ```
</CodeGroup>

Jika [kebijakan organisasi Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#set-organization-defaults) mewajibkan penyimpanan milik pelanggan atau mewajibkan Anthropic Human Review dinonaktifkan, Anthropic menolak permintaan ini dengan `workspace_policy_violation` untuk workspace yang menyimpan data keselamatan tersegel. Ubah kebijakan tersebut terlebih dahulu, lalu kirim permintaan.

Seperti pelampiran, pelepasan [tidak langsung berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#how-long-changes-take).

Setelah pelepasan terakhir, status bucket Anda menjadi `draining`. Status tidak keluar dari `draining` dengan sendirinya. Status ini berubah saat Anda melampirkan bucket tersebut lagi atau menghapus External Storage-nya. Pertahankan bucket Anda dan akses Anthropic ke bucket tersebut hingga penghapusan selesai. Jika Anda tidak dapat menghapus External Storage, bicarakan dengan tim akun Anthropic Anda sebelum Anda menghapus akses Anthropic. [Hapus tujuan penyimpanan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#delete-a-storage-destination) menjelaskan siapa yang dapat menghapusnya dan apa yang harus dilakukan terlebih dahulu.

Kemudian hapus External Storage bucket Anda. External Storage adalah catatan Anthropic tentang bucket Anda, bukan bucket Anda itu sendiri. Apa yang terjadi bergantung pada status bucket Anda:

* `pending_configuration` atau `available`: Anthropic langsung menghapus External Storage.
* `active`: Anthropic menolak penghapusan.
* `draining`: Panggilan pertama mengembalikan error 400 dengan `external_storage_in_use`. [Ambil External Storage tersebut](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#api-check). Jika `status.removal_started` bernilai `false`, pesan error tersebut menjelaskan apa yang harus dilakukan. Jika bernilai `true`, Anda tidak dapat membatalkan penghapusan. Kirim permintaan penghapusan lagi setiap beberapa menit hingga berhasil, yang dapat memakan waktu sekitar 30 menit. Jika masih ditolak setelah satu jam, hubungi tim akun Anthropic Anda. Error 503 berarti tidak ada yang berubah, jadi coba lagi nanti.

Jika [kebijakan organisasi Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#set-organization-defaults) mencantumkan bucket ini, Anthropic menolak penghapusan sampai Anda menghapus bucket tersebut dari kebijakan. Setelah sebuah workspace menggunakan bucket Anda, anggap nama bucket, kunci KMS, dan peran IAM Anda [terikat ke organisasi Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#before-you-begin).

<CodeGroup>
  ```bash cURL
  curl -X DELETE https://api.anthropic.com/v1/organizations/external_storage/estrg_01SDCCSbTxrXDpWc1phhtcfK \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: efs-2026-10-01"
  ```

  ```bash CLI
  ant beta:organization:external-storage delete \
    --external-storage-id estrg_01SDCCSbTxrXDpWc1phhtcfK
  ```

  ```python Python
  client = anthropic.Anthropic()

  deleted = client.beta.organization.external_storage.delete(
      "estrg_01SDCCSbTxrXDpWc1phhtcfK"
  )

  print(f"id: {deleted.id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const deleted = await client.beta.organization.externalStorage.delete(
    "estrg_01SDCCSbTxrXDpWc1phhtcfK"
  );

  console.log(`id: ${deleted.id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var deleted = await client.Beta.Organization.ExternalStorage.Delete(
      "estrg_01SDCCSbTxrXDpWc1phhtcfK"
  );

  Console.WriteLine($"id: {deleted.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  deleted, err := client.Beta.Organization.ExternalStorage.Delete(
  	context.Background(),
  	"estrg_01SDCCSbTxrXDpWc1phhtcfK",
  	anthropic.BetaOrganizationExternalStorageDeleteParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", deleted.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var deleted = client.beta().organization().externalStorage()
      .delete("estrg_01SDCCSbTxrXDpWc1phhtcfK");

  IO.println("id: " + deleted.id());
  ```

  ```php PHP
  $client = new Client();

  $deleted = $client->beta->organization->externalStorage->delete(
      externalStorageID: 'estrg_01SDCCSbTxrXDpWc1phhtcfK',
  );

  echo "id: {$deleted->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  deleted = client.beta.organization.external_storage.delete("estrg_01SDCCSbTxrXDpWc1phhtcfK")

  puts "id: #{deleted.id}"
  ```
</CodeGroup>

#### Hapus akses Anthropic

Untuk menghapus akses Anthropic, hapus peran IAM bucket Anda dengan alat yang Anda gunakan untuk membuatnya. Setelah Anda menghapus akses Anthropic, data keselamatan tersegel tetap berada di bucket Anda hingga Anda menghapusnya. Di bucket yang menyimpan transkrip dan Safety Cases, aturan siklus hidup terus membuat file-file tersebut kedaluwarsa hingga Anda mengubah aturan tersebut.

<Tabs>
  <Tab title="CloudFormation">
    Hapus stack bucket Anda. Nama stack tersebut ada di perintah deploy Anda: `anthropic-storage-<RoleDigest>`, atau `anthropic-storage-<organization ID>` untuk penyiapan dengan nama peran tetap. Menghapus stack tetap mempertahankan bucket dan kuncinya.
  </Tab>

  <Tab title="Terraform">
    Hapus hanya peran-peran bucket Anda dan kebijakannya, agar data Anda tetap tersimpan. Di folder yang menyimpan file Terraform bucket Anda, jalankan perintah penghapusan dari header file Terraform tersebut dengan region dan nilai-nilai yang Anda gunakan saat penyiapan.

    Anda akan melihat peringatan tentang `-target`. Pastikan setiap sumber daya yang dicantumkan plan adalah `aws_iam_role` atau `aws_iam_role_policy`, lalu ketik `yes`. Apply berikutnya akan membuat ulang peran-peran tersebut.

    `terraform destroy` tanpa `-target` gagal dan tidak menghapus apa pun, karena kunci, bucket, pengaturannya, dan kebijakan bucket-nya ditandai `prevent_destroy`.
  </Tab>

  <Tab title="Your own tooling">
    Hapus peran IAM bucket tersebut.
  </Tab>
</Tabs>

<Warning>
  Setelah peran-peran tersebut dihapus, jangan pilih bucket Anda lagi untuk sebuah workspace hingga peran-peran tersebut dikembalikan. Di Claude Platform on AWS, atau jika peran-peran Anda memiliki nama tetap, Anthropic tidak memeriksa bucket berstatus **Draining** sebelum Anda menyimpan, sehingga proses simpan dapat berhasil meskipun Anthropic tidak dapat menulis ke bucket Anda. Jika Anda menggunakan CloudFormation, men-deploy template lagi tidak memulihkan akses Anthropic, jadi hubungi tim akun Anthropic Anda sebelum Anda memilih bucket Anda.
</Warning>

</Where>

</Where>

<Where bucket="gcs" label="Google Cloud Storage">

Bicarakan dengan tim akun Anthropic Anda sebelum Anda pindah ke bucket baru, karena [Anthropic membatasi jumlah bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-use-your-bucket-in-a-workspace).

Lihat [cara berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-stop-using-your-bucket).

</Where>

<Where bucket="s3" label="Amazon S3">

## Hapus tujuan penyimpanan

Untuk mengakhiri penggunaan Anthropic atas bucket yang ditampilkan sebagai **Draining**, hapus tujuan penyimpanannya. Di Claude Platform on AWS, Anda tidak dapat menghapus tujuan penyimpanan setelah sebuah workspace menggunakannya. Di Claude Platform, Anda dapat menghapus tujuan penyimpanan untuk bucket Amazon S3 hanya jika catatan Anthropic menunjukkan bahwa organisasi Anda menggunakan Claude hanya untuk alat internal. Jika Anda tidak dapat menghapusnya, bicarakan dengan tim akun Anthropic Anda sebelum Anda menghapus akses Anthropic. Anda tidak dapat membatalkan penghapusan.

<Where cloud="claude" label="Claude Platform">

Sebelum Anda menghapusnya, lakukan hal berikut:

* **Tunggu hingga `slab/` dan `media/` kosong,** di tingkat teratas bucket dan di bawah `safeguards-data/`. Sebagian besar isinya akan hilang dengan sendirinya beberapa hari setelah [periode retensi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage#retention-period) berakhir untuk data terakhir yang dikirim ke sana. Jangan menghapus apa pun sebelum itu. Anda akan kehilangan data, dan Anthropic tidak memperingatkan Anda. Jika [objek tetap ada](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#what-removes-data) setelah itu, hapus objek tersebut tanpa ID versi. Versi lama dan penanda hapus juga dihitung, jadi tunggu hingga aturan siklus hidup membersihkannya, setidaknya 3 hari setelah setiap penghapusan.
* **Pertahankan akses Anthropic** hingga penghapusan selesai, karena Anthropic memeriksa bucket terlebih dahulu.

<Warning>
  Menghapus tujuan penyimpanan tidak menghapus apa pun dari bucket Anda. Transkrip, Safety Cases, dan tanggapan tim Anda mungkin masih ada di sana, dan siapa pun yang memiliki akses ke bucket dan kuncinya dapat membacanya. Kosongkan bucket, termasuk versi file sebelumnya, sebelum siapa pun menggunakannya lagi untuk penyimpanan milik pelanggan.
</Warning>

<Where method="console" label="Claude Console">

Di bawah **Storage destinations** di halaman [Retensi data](https://platform.claude.com/settings/privacy), pilih **Delete** di menu baris tersebut. Jika Claude Console menolak penghapusan, pesannya menjelaskan alasannya. Jika baris tersebut masih tercantum setelah beberapa menit, pilih **Finish deleting** di menunya. Jika masih tercantum setelah satu jam, hubungi tim akun Anthropic Anda. Setelah baris tersebut hilang, ikuti langkah terakhir di [Berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#stop-using-your-bucket) untuk menghapus akses Anthropic. Anda kemudian dapat menghapus bucket Anda.

</Where>

<Where method="api" label="Admin API">

Kirim permintaan penghapusan, seperti yang dijelaskan di [Berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#api-stop). Proses ini memerlukan lebih dari satu panggilan. Setelah berhasil, [hapus akses Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#api-remove-access). Anda kemudian dapat menghapus bucket Anda.

</Where>

</Where>

</Where>

## Apa yang menghapus data dari bucket Anda

<Where bucket="s3" label="Amazon S3">

<Where cloud="claude" label="Claude Platform">

Anthropic menghapus objek di bawah `slab/` dan `media/` melalui [peran maintenance](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-roles). Anthropic menghapus objek di bawah `slab/` hanya setelah semua isi objek tersebut melewati periode retensinya.

</Where>

Jika bucket Anda menggunakan `safeguards-data/`, bagian ini dan [Apa yang melindungi versi objek di bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#what-protects-object-versions) berlaku untuk prefiks yang sama di bawah `safeguards-data/`.

Karena bucket Anda menyimpan versi, penghapusan oleh peran maintenance hanya menambahkan penanda hapus, dan versi lama tetap ada. Aturan siklus hidup menghapus setiap versi lama secara permanen setidaknya 3 hari kemudian, lalu menghapus penanda hapus tersebut.

Beberapa objek tetap berada di bucket Anda, karena tidak ada aturan siklus hidup dalam file penyiapan yang menghapusnya:

* **Di bawah `slab/`:** Anthropic menelusuri objek dari setiap hari untuk mencari objek yang akan dihapus, tetapi hanya selama sejumlah hari terbatas. Objek yang belum dihapusnya hingga saat itu tetap berada di bucket Anda.
* **Di bawah `slab-manifest/`:** Perangkat lunak Anthropic tidak pernah menghapus objek di bawah prefiks ini, sehingga objek-objek itu terus bertambah.
* **Di bawah `media/`:** Penulisan yang terputus atau berulang dapat meninggalkan objek yang tidak lagi dilacak oleh Anthropic. Objek-objek tersebut tetap terenkripsi. Pembersihan bulanan mencarinya, tetapi dapat membiarkannya tetap di tempatnya.

Biarkan objek yang ditulis Anthropic apa adanya, termasuk objek-objek sisa ini selama sebuah workspace menggunakan bucket Anda. Jika Anda tidak dapat menyimpannya, hubungi tim akun Anthropic Anda, kecuali Anda sedang [menghapus tujuan penyimpanan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#delete-a-storage-destination).

Ubah aturan siklus hidup bucket Anda hanya dengan mengatur [`ReviewExpiryDays`](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#template-reference). Jangan aktifkan S3 Object Lock atau menambahkan aturan siklus hidup yang membuat objek kedaluwarsa atau mengarsipkannya. Jika Anda melakukannya, bucket Anda gagal dalam [**Test setup**](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#test-the-setup) dan [pemeriksaan harian Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#bucket-health).

### Apa yang melindungi versi objek di bucket Anda

Hanya aturan siklus hidup yang dapat menghapus versi objek di bawah `slab/` secara permanen. Hal ini berlaku selama pembuatan versi aktif dan kebijakan bucket mempertahankan pernyataan `NobodyHardDeletesSlabVersions`-nya. Pernyataan tersebut menolak `s3:DeleteObjectVersion` di bawah `slab/` untuk setiap orang dan peran, termasuk milik Anthropic.

Peran-peran Anthropic tidak dapat mengubah kebijakan bucket, pembuatan versi, maupun aturan siklus hidup.

Kebijakan bucket tidak memiliki pernyataan seperti `NobodyHardDeletesSlabVersions` untuk prefiks lain. Peran media-erasure dapat menghapus versi objek di bawah `media/` secara permanen. Peran transcripts dan review dapat menghapus transkrip, Safety Cases, ringkasan, dan Safety Notices secara permanen, tetapi tidak dapat menghapus tanggapan tim Anda.

</Where>

<Where bucket="gcs" label="Google Cloud Storage">

Aturan siklus hidup milik bucket Anda itu sendiri menghapus setiap objek data keselamatan tersegel setelah objek tersebut berusia 28 hari. Jangan ubah aturan tersebut.

</Where>

<Where bucket="s3" label="Amazon S3">

## Panggilan Anthropic di AWS CloudTrail

Setiap kali Anthropic mengambil alih salah satu peran Anda, AWS CloudTrail mencatat panggilan tersebut di akun Anda. Anda dapat menemukan catatan tersebut di **Event history** CloudTrail:

* **Tempat mencari:** Cari di `us-east-2`. **Event history** menampilkan satu region AWS dalam satu waktu dan menyimpan catatan tersebut selama 90 hari tanpa penyiapan.
* **Apa yang ditampilkan sebuah catatan:** Setiap catatan membawa source identity yang menyebutkan jenis pekerjaan, dan setiap panggilan berikutnya dalam sesi tersebut juga membawanya.
* **Apa yang tidak ditampilkan Event history:** **Event history** tidak menampilkan pembacaan, penulisan, dan penghapusan objek, yang merupakan data event Amazon S3. Agar CloudTrail mencatatnya, aktifkan pencatatan data event untuk bucket Anda. AWS mengenakan biaya untuk pencatatan tersebut.

### Panggilan dari Test setup dan pemeriksaan harian

**Test setup** dan [pemeriksaan harian](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#bucket-health) mengirim permintaan dengan external ID atau source identity yang tidak ada atau salah. Peran Anda harus menolaknya, sehingga penolakan tersebut memang diperkirakan. Jika sebuah peran menolak permintaan yang memiliki external ID Anda dan source identity yang diterima peran tersebut, penolakan itu tidak diperkirakan. Hal itu mungkin berarti bahwa [kebijakan organisasi AWS memblokir Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#if-an-aws-organization-policy-blocks-anthropic).

</Where>

<Where method="api" label="Admin API">

## Pemecahan masalah

<AccordionGroup>
  <Accordion title="Setiap permintaan penyiapan mengembalikan error atau menyatakan bahwa inference_data_privacy bukan field yang valid">
    Permintaan yang menyiapkan External Storage mengembalikan error sampai organisasi Anda memiliki [akses ke Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#get-access). Permintaan tersebut juga mengembalikan error jika tidak mengirim header beta. Dengan token bearer OAuth, permintaan tersebut juga mengembalikan error jika token tidak memiliki cakupan `org:admin`. Tanpa header tersebut, permintaan melampirkan dan melepas mengembalikan error yang berbeda, yang menyatakan bahwa `inference_data_privacy` bukan field yang valid. Jika hal itu terjadi saat akses dan header sudah tersedia, hubungi tim akun Anthropic Anda.
  </Accordion>

  <Accordion title="Permintaan activate mengembalikan pemeriksaan yang gagal">
    Jika suatu pemeriksaan gagal, permintaan mengembalikan error 400 dengan `error.details.error_code` bernilai `storage_verification_failed`. `error.details.failed_checks` mencantumkan setiap masalah sebagai objek dengan `check`, `role`, dan `message`. Perbaiki setiap masalah yang dicantumkan `failed_checks` dan panggil activate lagi. Pemeriksaan `already_registered` memiliki cara perbaikan tersendiri, yang dijelaskan nanti di bagian ini.

    Jika `message` pertama diawali dengan “Anthropic could not assume the verify role”, periksa hal-hal berikut secara berurutan:

    1. Lihat nama peran IAM Anda. Bucket baru yang perannya memiliki nama tetap, seperti `anthropic-efs-ingest`, gagal dalam pemeriksaan ini. Untuk bucket seperti itu, hapus External Storage ini, [daftarkan nama bucket baru](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-register), dan gunakan file dari bagian [Dapatkan file penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?method=api#get-the-setup-file).
    2. Jika tidak demikian, periksa bahwa Anda membuat penyiapan Anda dari file di bagian [Dapatkan file penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?method=api#get-the-setup-file).
    3. Periksa apakah [kebijakan organisasi AWS memblokir Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#if-an-aws-organization-policy-blocks-anthropic).

    Jika `failed_checks` berisi satu objek dengan `check` bernilai `already_registered`, organisasi Anthropic lain telah menggunakan sebagian dari penyiapan ini, atau nama bucket tersebut sedang digunakan di akun AWS yang berbeda. External Storage milik organisasi yang telah dihapus tetap dapat terhitung sebagai salah satu penggunaan tersebut.

    Jika organisasi lain telah menggunakan akun AWS ini, Anda dapat tetap menggunakan akun tersebut. Pertama, periksa bahwa Anda telah men-deploy file dari bagian [Dapatkan file penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?method=api#get-the-setup-file) untuk bucket ini, lalu panggil activate lagi.

    Jika pemeriksaan masih gagal, atau tidak ada organisasi lain yang telah menggunakan akun AWS ini, gunakan nama bucket baru, dengan kunci dan peran tersendiri, lalu [daftarkan bucket baru](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-register). Jika bucket baru gagal dengan cara yang sama, beri tahu tim akun Anthropic Anda.

    [Permintaan attach](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-attach) juga dapat gagal dengan pemeriksaan `already_registered`. Jika pemeriksaan gagal untuk `safeguards_storage`, cara memperbaikinya sama. Jika pemeriksaan gagal untuk `transcripts_storage`, hubungi tim akun Anthropic Anda. Jika peran Anda memiliki nama tetap, kegagalan `already_registered` saat attach juga dapat berarti bahwa organisasi lain telah menggunakan akun AWS ini.

    Jika permintaan activate atau [permintaan attach](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-attach) mengembalikan error 503 tanpa `error.details.error_code`, Anthropic tidak dapat menjalankan pemeriksaannya, jadi coba lagi dalam beberapa menit. Jika hal ini terus terjadi, beri tahu tim akun Anthropic Anda.
  </Accordion>

  <Accordion title="Permintaan lampirkan mengembalikan error tentang persetujuan Anthropic">
    Anthropic dapat menyetujui penyimpanan milik pelanggan untuk seluruh organisasi Anda atau untuk workspace tertentu. Permintaan ini dapat mengembalikan dua error terkait persetujuan tersebut, dan dalam kedua kasus tidak ada yang diubah. Mendaftarkan bucket Anda dan mengaktifkannya dapat mengembalikan dua kode yang sama. Tidak ada workspace yang terlibat pada langkah-langkah tersebut, sehingga pesannya menyangkut persetujuan organisasi Anda, bukan persetujuan workspace.

    | Yang Anda terima | Artinya | Yang harus dilakukan |
    | ----- | ----- | ----- |
    | Error 400 dengan `error.details.error_code` bernilai `grant_required` | Persetujuan Anthropic tidak mencakup workspace ini. Pesannya menyatakan bahwa workspace tersebut tidak disetujui untuk menggunakan External Storage dan meminta Anda menghubungi tim akun Anthropic Anda. | Minta tim akun Anthropic Anda agar workspace tersebut disetujui, lalu kirim permintaan lagi. |
    | Error 503 dengan `error.details.error_code` bernilai `authorization_check_unavailable`, dan header `Retry-After` | Persetujuan Anthropic tidak dapat diperiksa pada saat itu. | Tunggu selama jumlah detik di header `Retry-After`, lalu kirim permintaan yang sama lagi. |

    Sebelum Anda menghubungi tim akun Anthropic Anda, pastikan seorang Organization Admin telah [menerima ketentuan EFS dan Enterprise Data Controls](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#get-access). Persetujuan baru dapat memerlukan sedikit waktu untuk sampai ke API, sehingga permintaan yang dikirim tepat setelah Anda mendapatkannya masih dapat mengembalikan `grant_required`. Kirim lagi, dan hubungi tim akun Anthropic Anda jika hal ini terus terjadi.

    Permintaan attach juga dapat mengembalikan `approval_required`. Untuk mendapatkan persetujuan Anthropic untuk menonaktifkan Anthropic Human Review, lihat [Menyiapkan Enterprise Frontier Safeguards di Claude Platform](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#get-access).
  </Accordion>

  <Accordion title="Permintaan lampirkan menolak bucket Anda di transcripts_storage">
    Permintaan mengembalikan error 400. Pemeriksaan yang gagal tidak mengubah apa pun, sehingga `safeguards_storage` dalam permintaan yang sama juga tidak dilampirkan. Apa yang harus dilakukan bergantung pada error-nya:

    * Jika `error.details.error_code` bernilai `storage_verification_failed` dan `error.details.failed_checks` berisi satu objek yang `check`-nya bernilai `transcripts_support`, mengirim permintaan lagi tidak membantu. `message` objek tersebut menjelaskan alasannya. [Pemecahan masalah untuk penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#troubleshooting) menjelaskan apa yang harus dilakukan.
    * Jika `check` bernilai `already_registered`, atau error menyatakan bahwa penyimpanan belum dapat dilampirkan untuk transkrip, hubungi tim akun Anthropic Anda.
    * Untuk pemeriksaan lainnya, perbaiki apa yang dinyatakan oleh `message`-nya dan kirim permintaan lagi.

    Dalam setiap kasus, Anda dapat mengirim permintaan yang sama tanpa `transcripts_storage`. Jika Anthropic menerima permintaan tersebut, hanya `safeguards_storage` yang dilampirkan. Jika permintaan tanpa `transcripts_storage` mengembalikan `transcripts_storage_required`, gunakan bucket yang dapat menerima transkrip dan Safety Cases, atau hubungi tim akun Anthropic Anda.
  </Accordion>

  <Accordion title="Kunci enkripsi default bucket Anda berubah">
    Jika kunci enkripsi default bucket Anda berubah setelah Anda mengaktifkan bucket dan belum ada workspace yang menggunakan bucket tersebut, Anthropic menolak pelampiran, karena Anthropic memeriksa bucket lagi pada saat itu. Untuk menggunakan kunci lain dengan peran IAM yang Anda buat dengan tooling Anda sendiri, ikuti langkah-langkah berikut:

    1. Hapus External Storage ini.
    2. Izinkan setiap peran kecuali `media-erasure` menggunakan kunci baru, termasuk di tempat kondisi penulisan peran `transcripts` dan `review` menyebutkan kunci tersebut.
    3. Dalam kebijakan kunci baru, izinkan Amazon S3 memanggil `kms:GenerateDataKey`, seperti yang dilakukan kebijakan kunci di file penyiapan Anda, agar S3 Inventory dapat mengirimkan laporan hariannya.
    4. Atur enkripsi default bucket Anda ke kunci baru, yang disebutkan berdasarkan ARN kuncinya. Kunci tersebut harus memenuhi persyaratan untuk kunci bucket di tab **Your own tooling** pada [Buat bucket Anda dan kunci KMS-nya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket).
    5. Daftarkan bucket Anda lagi dan aktifkan.

    Template CloudFormation dan file Terraform dari Anthropic menyiapkan peran untuk satu kunci dan tidak memiliki cara yang didukung untuk menggunakan kunci lain. Untuk penyiapan dengan nama peran tetap, seperti `anthropic-efs-ingest`, jangan daftarkan bucket yang sama lagi. Buat bucket baru dengan file dari bagian [Dapatkan file penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?method=api#get-the-setup-file).
  </Accordion>

  <Accordion title="Hanya sebagian perubahan permintaan workspace yang tersimpan">
    Jika respons menyatakan bahwa sebagian perubahan dalam permintaan mungkin telah disimpan dan sebagian lainnya tidak, kirim permintaan yang sama lagi. Perubahan yang sudah disimpan tidak diulang.

    Jangan mengirim ulang permintaan pembuatan yang mengembalikan `workspace_created_incomplete`, karena workspace tersebut sudah ada dan permintaan pembuatan kedua akan membuat workspace kedua. Sebagai gantinya, ikuti pesan dalam respons, yang biasanya meminta Anda memperbarui workspace yang disebutkan oleh `error.details.workspace_id`. Di organisasi yang memiliki pengaturan Legacy Zero Data Retention (ZDR), jika pesan tersebut meminta Anda memperbarui `inference_data_privacy`, arsipkan workspace tersebut dan buat ulang.
  </Accordion>
</AccordionGroup>

</Where>
