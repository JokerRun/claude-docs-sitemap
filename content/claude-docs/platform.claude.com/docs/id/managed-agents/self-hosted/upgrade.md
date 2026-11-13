---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: b7d97a5f7a3201ce60f6a7e6a04c4e240cfd157a0c0e5dd3d82fff9491c587f9
---

---
title: Meningkatkan Claude Managed Agents yang di-host sendiri
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade
description: Tingkatkan deployment Claude Managed Agents yang di-host sendiri di Kubernetes atau Docker Compose, dan kembali ke rilis lama jika rilis baru tidak berfungsi.
---

<Note>
  Untuk meminta akses ke Claude Managed Agents yang di-host sendiri, hubungi tim akun Anthropic Anda.
</Note>

Halaman ini menunjukkan cara meningkatkan deployment di Kubernetes atau Docker Compose, dan cara kembali ke rilis lama. Di Kubernetes, downtime bergantung pada seberapa jauh peningkatan tersebut:

| Peningkatan                                                                        | Cadangkan database terlebih dahulu | Downtime di Kubernetes                                                                   |
| ---------------------------------------------------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------- |
| Patch: hanya angka ketiga yang berubah                                             | Tidak. Skema database tetap sama.  | Tidak ada                                                                                |
| Minor: angka kedua naik satu, seperti `1.2.0` ke `1.3.0`                           | Ya. Skema berubah.                 | Tidak ada, kecuali sebuah bagian `CHANGELOG.md` menyatakan bahwa server harus dihentikan |
| Melewati satu rilis minor, seperti `1.1.0` ke `1.3.0`, atau mengubah angka pertama | Ya. Skema berubah.                 | Sejak Anda menghentikan server lama hingga server baru siap                              |

Stack Docker Compose mati selama dimulai ulang, untuk setiap jenis peningkatan.

## Sebelum Anda meningkatkan

Baca bagian rilis baru di `CHANGELOG.md`, di tingkat teratas arsip yang diekstrak. Bagian tersebut dimulai dengan langkah-langkah peningkatan yang khusus untuk rilis itu. Jika Anda melewati beberapa rilis, ikuti setiap bagian yang lebih baru dari versi Anda, dimulai dari yang terlama.

Kemudian telusuri [Pengaturan dan path yang perlu diperiksa](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#settings-and-paths-to-check).

Peningkatan minor atau mayor mencakup pencadangan database. Dump tersebut menyimpan setiap percakapan dalam bentuk plaintext, sehingga perintah di halaman ini mengenkripsinya dengan [alat enkripsi age](https://age-encryption.org). Buat pasangan kunci sekali saja, dan simpan kunci privat, `cma-backup.agekey`, terpisah dari cadangan:

```bash
age-keygen -o cma-backup.agekey
age-keygen -y cma-backup.agekey > cma-backup.agepub
```

## Meningkatkan di Kubernetes

Perintah `kubectl` di halaman ini membaca nama Deployment server dari sebuah variabel shell. Jalankan dua baris ini di setiap terminal tempat Anda menjalankan perintah. Baris pertama mencari nama tersebut, dan baris kedua mencetaknya:

```bash
server=$(kubectl -n cma-server get deployment -l anthropic.com/role=server -o jsonpath='{.items[*].metadata.name}')
echo "$server"
```

Jika baris kedua mencetak `cma-server`, lanjutkan. Jika perintah mencetak nama lain, baca [nama objek Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#object-names) sebelum Anda meningkatkan. Jika perintah tidak mencetak apa pun, periksa bahwa `kubectl` mengarah ke cluster yang benar, lalu jalankan kedua baris tersebut lagi.

<Steps>
  <Step title="Bangun dan dorong image baru">
    Ekstrak arsip baru. Bangun dan dorong ketiga image-nya dengan versi baru, seperti di [Membangun dan mendorong image](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#build-and-push-the-images). Jika Anda menjalankan [egress gateway](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#environment-variable-credentials), bangun dan dorong juga image-nya.

    Jika Anda membangun image sandbox sendiri, bangun ulang dan dorong juga image tersebut, dengan versi baru. Bandingkan Dockerfile-nya dengan `kubernetes/sandbox/Dockerfile` di arsip baru, dan lihat [apa yang dibutuhkan image Anda sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api#what-an-image-of-your-own-needs).
  </Step>

  <Step title="Atur versi baru di file values Anda">
    Jika sebuah file values mengatur `image.tag`, ubah nilainya ke versi baru.
  </Step>

  <Step title="Hentikan setiap server, jika peningkatan memerlukannya">
    Lakukan langkah ini hanya dalam kasus-kasus berikut:

    * Server yang Anda jalankan tertinggal lebih dari satu rilis minor dari rilis baru.
    * Angka pertama, yaitu versi mayor, naik.
    * Sebuah bagian `CHANGELOG.md` yang lebih baru dari rilis yang Anda jalankan menyatakan bahwa server harus dihentikan.

    Sejak langkah ini hingga server baru siap, klien tidak dapat menjangkau deployment, jadi rencanakan jendela pemeliharaan.

    ```bash
    kubectl -n cma-server scale deployment/$server --replicas=0
    kubectl -n cma-server wait --for=delete pod -l anthropic.com/role=server --timeout=90s
    ```
  </Step>

  <Step title="Cadangkan database">
    Lakukan ini sebelum peningkatan minor atau mayor, atau jika Anda menghentikan server. Jika rilis lama tidak dapat berjalan pada skema yang telah diubah, cadangan ini adalah satu-satunya jalan kembali.

    Gunakan `pg_dump` dari versi mayor PostgreSQL yang sama dengan server database Anda. Untuk `<role>` dan `<database>`, gunakan nilai `user` dan `dbname` dari `database.url` di `cma-server-values.yaml`. `pg_dump` meminta kata sandi role.

    ```bash
    set -o pipefail
    PGSSLMODE=require pg_dump -h <database-host> -U <role> -d <database> -Fc \
      | age -r "$(cat cma-backup.agepub)" -o cma_server-<old-version>.dump.age
    ```

    Jika salah satu perintah mencetak error, file yang ditinggalkannya bukanlah cadangan. Perbaiki penyebabnya dan jalankan perintah tersebut lagi sebelum Anda melanjutkan.

    Jika server sedang berjalan, cadangan hanya memuat apa yang ditulis klien sebelum dump dimulai.
  </Step>

  <Step title="Tingkatkan server, lalu sandbox">
    Jalankan perintah-perintah ini dari direktori teratas arsip baru, menggunakan file values dari instalasi Anda:

    ```bash
    helm upgrade cma-server kubernetes/server/chart --namespace cma-server -f cma-server-values.yaml --wait
    helm upgrade cma kubernetes/chart --namespace cma -f cma-values.yaml --wait
    ```

    Jika Anda menjalankan lebih dari satu environment, jalankan perintah kedua untuk setiap rilis sandbox, dengan nama, namespace, dan file values rilis tersebut.

    Jika Anda menghentikan server, perintah pertama memigrasikan skema, memulihkan jumlah server, dan kembali setelah server baru siap.
  </Step>
</Steps>

Dengan server berjalan, Helm memulai setiap server baru sebelum menghentikan server lama, sehingga jumlah server yang siap tidak pernah berkurang. Dalam peningkatan minor, perintah pertama mengubah skema selama server lama tetap melayani permintaan, lalu menggantinya. Aliran event yang terbuka pada server yang sedang diganti akan berakhir dengan bersih, sehingga klien yang mengikuti aliran harus menyambung ulang.

Jika sebuah perintah gagal, lihat [Jika peningkatan gagal](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#if-the-upgrade-fails).

## Meningkatkan di Docker Compose

Langkah-langkahnya sama untuk setiap jenis peningkatan. Jalankan setiap perintah `docker compose` dari direktori Compose sebuah rilis, yaitu direktori yang berisi `docker-compose.yml`. Di arsip yang diekstrak, direktori tersebut adalah `compose`. Gunakan terminal yang tidak mengatur `ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`, dan `ANTHROPIC_AUTH_TOKEN`, karena Compose meneruskan nilai variabel-variabel tersebut dari shell ke server.

<Steps>
  <Step title="Cadangkan database">
    Lakukan ini sebelum peningkatan minor atau mayor, dari direktori Compose rilis lama:

    ```bash
    set -o pipefail
    docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' \
      | age -r "$(cat cma-backup.agepub)" -o cma_server-<old-version>.dump.age
    ```

    Dalam perintah tersebut, biarkan `$POSTGRES_USER` dan `$POSTGRES_DB` apa adanya. Teks di dalam tanda kutip tunggal berjalan di dalam container `postgres`, yang menyimpan nama role dan database-nya dalam variabel-variabel tersebut.

    Stack tetap melayani permintaan selama pencadangan, sehingga dump tidak memuat apa pun yang ditulis klien setelah dump dimulai. Jika salah satu perintah mencetak error, file yang ditinggalkannya bukanlah cadangan. Perbaiki penyebabnya dan jalankan perintah tersebut lagi sebelum Anda melanjutkan.
  </Step>

  <Step title="Ekstrak arsip baru">
    Letakkan arsip baru di direktori tempat rilis baru dapat tetap berada, seperti direktori induk rilis lama. Perintah-perintah berikut mengekstrak arsip di sana, dan stack baru berjalan dari file hasil ekstraksi.

    Jika umask Anda lebih ketat dari `022`, jalankan `umask 022` terlebih dahulu. Kemudian jalankan ini dari direktori Compose rilis lama. Sebagai pengganti `<directory>`, tulis path lengkap direktori yang berisi arsip baru. Sebagai pengganti `<archive>`, tulis nama arsip tanpa `.tar.gz`.

    ```bash
    releases="<directory>"
    tar -xzf "$releases/<archive>.tar.gz" -C "$releases" && cp .env compose.config.yaml "$releases/<archive>/compose/"
    ```

    Baris kedua juga menyalin `.env` dan `compose.config.yaml` Anda ke direktori `compose` hasil ekstraksi. Stack lama tetap berjalan selama kedua baris tersebut. Jika sebuah baris mencetak error, perbaiki penyebabnya dan jalankan kedua baris lagi.
  </Step>

  <Step title="Ulangi perubahan Anda lainnya">
    Hanya `.env` dan `compose.config.yaml` yang terbawa. Lakukan kembali perubahan Anda lainnya di direktori Compose rilis baru:

    * **File yang Anda tambahkan:** Salin file tersebut.
    * **File bawaan yang Anda edit:** Lakukan edit yang sama pada salinan di rilis baru. Jangan timpa dengan file lama, karena hal itu membatalkan perubahan rilis pada file tersebut.
    * **Identitas agen:** Salin direktori `agent-identity` dengan `cp -a`, menggunakan `sudo` jika direktori tersebut dimiliki oleh root, lalu edit lagi blok `volumes:` di `docker-compose.yml`.
    * **File Compose milik Anda sendiri:** Salin file tersebut, dan periksa path relatifnya.

    Kemudian lakukan perubahan Docker Compose di [Pengaturan dan path yang perlu diperiksa](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#settings-and-paths-to-check).
  </Step>

  <Step title="Hentikan stack lama dan jalankan yang baru">
    Jalankan baris-baris ini di terminal tempat Anda mengekstrak arsip, karena baris-baris tersebut menggunakan variabel `$releases` dari terminal itu. Tetap berada di direktori Compose rilis lama, dan tulis nama yang sama sebagai pengganti `<archive>`. Jika Anda mengekspor `COMPOSE_FILE` untuk stack lama, ekspor nilai yang sama terlebih dahulu.

    ```bash
    ls "$releases/<archive>/compose/.env" && docker compose down
    cd "$releases/<archive>/compose" && docker compose up --build -d
    ```

    Baris pertama menghentikan stack lama hanya jika `.env` rilis baru sudah ada di tempatnya. `docker compose down` mempertahankan database. Jangan tambahkan `-v`, yang akan menghapusnya. Stack baru menggunakan database tersebut, dan container `migrate`-nya memperbarui skema sebelum server dimulai.
  </Step>
</Steps>

Jika sebuah perintah gagal, lihat [Jika peningkatan gagal](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#if-the-upgrade-fails).

## Jika peningkatan gagal

Sebelum Anda kembali ke rilis lama, temukan penyebabnya di log:

* **Kubernetes:** Jika Job migrasi gagal, `helm upgrade` menunggu beberapa menit selama Job mencoba ulang, lalu gagal. Selama menunggu tersebut, jalankan `kubectl -n cma-server logs job/$server-migrate` di terminal kedua, dengan `$server` diatur seperti di [Meningkatkan di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#upgrade-on-kubernetes). Kubernetes menghapus log tersebut ketika Job berhenti mencoba ulang. Jika Anda melewatkannya, jalankan `helm upgrade` lagi, yang akan memulai Job kembali.
* **Docker Compose:** Output `docker compose up --build -d` mungkin tidak menunjukkan alasannya. Jalankan `docker compose logs` untuk menemukannya.

| Apa yang ditampilkan log                                                                                    | Artinya                                                                                                                                              | Yang harus dilakukan                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Baris yang berisi `refusing to migrate: servers of another release are still running against this database` | Beberapa peningkatan memerlukan setiap server dihentikan terlebih dahulu, dan server dari rilis lama masih berjalan. Migrasi tidak mengubah apa pun. | Hentikan setiap server, seperti di [Meningkatkan di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#upgrade-on-kubernetes), lalu jalankan `helm upgrade` lagi. Jika sebuah server tidak dimatikan dengan bersih, tunggu 20 detik terlebih dahulu: hingga saat itu, migrasi masih menganggap server tersebut berjalan. |
| Baris yang berisi `cannot downgrade`, saat Anda menerapkan ulang rilis lama                                 | Rilis lama tidak dapat berjalan pada skema yang telah diubah.                                                                                        | Pulihkan cadangan, seperti di [Kembali ke rilis lama](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#roll-back).                                                                                                                                                                                                                 |
| Error lain dari migrasi                                                                                     | Anda tidak perlu kembali ke rilis lama. Di Kubernetes, server tetap seperti semula sampai migrasi berhasil.                                          | Perbaiki penyebabnya, lalu jalankan `helm upgrade` atau `docker compose up --build -d` lagi.                                                                                                                                                                                                                                                             |

Migrasi dapat berhasil sementara server baru tidak menjadi siap. Untuk menemukan penyebabnya, baca log server:

* **Kubernetes:** `kubectl -n cma-server logs -l anthropic.com/role=server --prefix --tail=20`
* **Docker Compose:** `docker compose logs cma-server`

Misalnya, di Kubernetes, baris yang berisi `has invalid keys` menyebutkan pengaturan di bawah `server.config` yang tidak diterima oleh rilis baru. Perbaiki penyebabnya dan jalankan perintah peningkatan lagi sebelum Anda mempertimbangkan pemulihan, karena pemulihan menghilangkan data. Di Kubernetes, setelah skema berubah, server rilis lama yang sedang berjalan tetap melayani permintaan, tetapi mungkin tidak dapat dimulai lagi jika berhenti.

## Kembali ke rilis lama

Perintah `kubectl` di bagian ini menggunakan variabel `$server` dari [Meningkatkan di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#upgrade-on-kubernetes). Sebelum Anda kembali ke rilis lama, periksa [Jika peningkatan gagal](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#if-the-upgrade-fails). Kemudian kembali ke rilis lama sesuai jenis peningkatan:

* **Setelah peningkatan patch:** [Terapkan ulang rilis lama](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#deploy-the-old-release-again). Kedua rilis menggunakan skema yang sama.

* **Setelah peningkatan minor atau mayor:** Buka `CHANGELOG.md` di arsip baru. Baca bagian setiap rilis yang muncul setelah rilis yang ingin Anda kembalikan.

  * Jika sebuah bagian menyatakan bahwa rilis lama tidak dapat dimulai pada database yang telah dimigrasi, pulihkan cadangan.
  * Jika tidak, terapkan ulang rilis lama. Jika itu gagal dengan `cannot downgrade`, pulihkan cadangan.

<Warning>
  Pemulihan menghilangkan semua yang ditulis klien setelah pencadangan dimulai.
</Warning>

### Menerapkan ulang rilis lama

* **Kubernetes:** Buka direktori teratas arsip lama. Jalankan dua perintah `helm upgrade` dari [Meningkatkan di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#upgrade-on-kubernetes), dengan file values seperti untuk rilis tersebut. Misalnya, jika Anda menambahkan `earlierNames` untuk peningkatan, hapus kembali. Jalankan perintah kedua hanya jika perintah pertama berhasil.
* **Docker Compose:** Jalankan `docker compose down` di direktori Compose rilis baru, lalu `docker compose up --build -d` di direktori rilis lama.

Jika rilis lama tidak dapat berjalan pada skema yang diubah, log menampilkan `cannot downgrade`:

* **Kubernetes:** Job migrasi gagal, dan server tetap seperti semula. [Jika peningkatan gagal](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#if-the-upgrade-fails) menjelaskan cara membaca log Job tersebut.
* **Docker Compose:** Server tidak mulai. Baca log dengan `docker compose logs migrate`.

Di Docker Compose, output `docker compose logs` mungkin justru menampilkan `stored value is encrypted but no encryption key is configured`. Dalam kasus tersebut, `.env` rilis lama tidak memiliki baris `CMA_STORE__CREDENTIALS_ENCRYPTION_KEY`. Salin baris tersebut dari `.env` rilis baru, lalu jalankan `docker compose up --build -d` lagi.

### Memulihkan cadangan di Kubernetes

Server database Anda memerlukan ruang untuk salinan kedua database. Untuk `<role>` dan `<database>`, gunakan nilai `user` dan `dbname` dari `database.url` di `cma-server-values.yaml`.

<Steps>
  <Step title="Pulihkan cadangan ke database baru">
    Hubungkan ke database `postgres` di server database Anda sebagai administrator, lalu jalankan:

    ```sql
    CREATE DATABASE <database>_restored OWNER <role>;
    ```

    Kemudian, di mesin yang menyimpan cadangan, jalankan perintah ini dengan path kunci dan file cadangan Anda. Gunakan `pg_restore` dengan versi mayor yang sama dengan server database Anda. Perintah ini meminta kata sandi role, dan tidak mencetak apa pun jika berhasil.

    ```bash
    age -d -i cma-backup.agekey cma_server-<old-version>.dump.age \
      | PGSSLMODE=require pg_restore -h <database-host> -U <role> -d <database>_restored --no-owner --exit-on-error
    ```

    Jika perintah ini mencetak error, berhenti. Database Anda tidak berubah. Jalankan `DROP DATABASE <database>_restored;` sebagai administrator, lalu ulangi langkah ini dari awal.
  </Step>

  <Step title="Hentikan setiap server">
    ```bash
    kubectl -n cma-server scale deployment/$server --replicas=0
    kubectl -n cma-server wait --for=delete pod -l anthropic.com/role=server --timeout=90s
    ```
  </Step>

  <Step title="Beralih ke database hasil pemulihan">
    Hubungkan ke database `postgres` sebagai administrator, lalu jalankan:

    ```sql
    ALTER DATABASE <database> RENAME TO <database>_upgraded;
    ALTER DATABASE <database>_restored RENAME TO <database>;
    ```

    Jika pernyataan pertama menyebutkan bahwa sesi lain sedang menggunakan database, tutup sesi-sesi tersebut lalu jalankan kedua pernyataan lagi. Connection pooler dapat menahan sesi semacam itu.
  </Step>

  <Step title="Terapkan rilis lama">
    Ikuti butir Kubernetes di [Menerapkan ulang rilis lama](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#deploy-the-old-release-again). Perintah pertama juga memulihkan jumlah server. Jika perintah tersebut gagal tetapi `kubectl -n cma-server get pods` menunjukkan bahwa server lama sudah siap, lihat [Jika pemeriksaan kunci gagal](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#if-the-key-check-fails).
  </Step>

  <Step title="Hapus database yang Anda sisihkan">
    Database tersebut masih berisi apa yang ditulis klien setelah cadangan dibuat. Setelah rilis lama berfungsi, hapus database tersebut dengan `DROP DATABASE <database>_upgraded;`.
  </Step>
</Steps>

#### Jika pemeriksaan kunci gagal

Pada langkah “Terapkan rilis lama”, perintah `helm upgrade` pertama menunggu hingga server lama siap. Kemudian perintah tersebut memeriksa kunci yang digunakan sandbox untuk terhubung. Jika perintah gagal tetapi `kubectl -n cma-server get pods` menunjukkan bahwa server lama sudah siap, pemeriksaan tersebut gagal.

Data Anda telah dipulihkan dan server berfungsi, tetapi sandbox belum dapat terhubung ke server. Sandbox terhubung dengan kunci dari Secret `cma-environment` di namespace-nya sendiri, `cma`. Kunci tersebut lebih baru daripada cadangan Anda, sehingga database hasil pemulihan tidak mengenalinya.

Untuk memastikan penyebabnya, jalankan perintah pertama lagi. Selama perintah menunggu, buka terminal kedua dan atur juga `$server` di sana. Kemudian jalankan `kubectl -n cma-server logs job/$server-environment-default`, dengan nama environment Anda sebagai pengganti `default`. Cari baris yang berisi `Secret cma/cma-environment records key`. Jika log menampilkan error lain, perbaiki apa yang disebutkannya.

Jika log menampilkan baris tersebut, hapus Secret dengan `kubectl -n cma delete secret cma-environment`, lalu jalankan perintah pertama lagi. Perintah tersebut membuat Secret kembali, dengan kunci baru. Kemudian jalankan perintah kedua.

### Memulihkan cadangan di Docker Compose

<Steps>
  <Step title="Jalankan hanya database">
    Jalankan `docker compose down` di direktori Compose rilis baru. Lalu jalankan `docker compose up -d --wait postgres` di direktori Compose rilis lama. Tetap berada di direktori tersebut untuk langkah-langkah berikutnya.
  </Step>

  <Step title="Pulihkan cadangan ke database baru">
    Dari direktori Compose rilis lama, jalankan perintah ini dengan path kunci dan file cadangan Anda:

    ```bash
    docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER" -d postgres \
        -c "DROP DATABASE IF EXISTS ${POSTGRES_DB}_restored" -c "CREATE DATABASE ${POSTGRES_DB}_restored"' \
      && age -d -i cma-backup.agekey cma_server-<old-version>.dump.age \
      | docker compose exec -T postgres sh -c 'pg_restore -U "$POSTGRES_USER" -d "${POSTGRES_DB}_restored" --no-owner --exit-on-error'
    ```

    Pemulihan berhasil jika perintah mencetak `DROP DATABASE` dan `CREATE DATABASE`, tanpa error.

    Biarkan `$POSTGRES_USER` dan `$POSTGRES_DB` apa adanya, di sini dan pada langkah-langkah berikutnya. Teks di dalam tanda kutip tunggal berjalan di dalam container `postgres`, yang menyimpan nama role dan database-nya dalam variabel-variabel tersebut.

    Jika perintah mencetak error, database Anda tidak berubah, sehingga Anda dapat menjalankan seluruh perintah lagi. Jika cadangan tidak dapat dipulihkan, jalankan `docker compose up --build -d` di direktori Compose rilis baru untuk menjalankan rilis tersebut lagi.
  </Step>

  <Step title="Beralih ke database hasil pemulihan">
    ```bash
    docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER" -d postgres \
        -c "ALTER DATABASE $POSTGRES_DB RENAME TO ${POSTGRES_DB}_upgraded" \
        -c "ALTER DATABASE ${POSTGRES_DB}_restored RENAME TO $POSTGRES_DB"'
    ```
  </Step>

  <Step title="Jalankan rilis lama">
    Jalankan `docker compose up --build -d`.
  </Step>

  <Step title="Hapus database yang Anda sisihkan">
    Database tersebut masih berisi apa yang ditulis klien setelah cadangan dibuat. Setelah rilis lama berfungsi, hapus database tersebut:

    ```bash
    docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER" -d postgres -c "DROP DATABASE ${POSTGRES_DB}_upgraded"'
    ```
  </Step>
</Steps>

### Setelah pemulihan

Pemulihan mengembalikan kunci environment ke kondisi saat cadangan dibuat:

* **Kunci yang Anda cabut setelah pencadangan:** Kunci tersebut berfungsi lagi. Cabut kembali.
* **Kunci yang Anda buat setelah pencadangan:** Kunci tersebut hilang. Buat kunci baru untuk worker yang menggunakannya.

[Mengganti kunci environment untuk worker Anda sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#replace-an-environment-key-for-your-own-workers) berisi perintahnya, yang juga berfungsi di Docker Compose. Sandbox yang dijalankan oleh stack Docker Compose tidak memerlukan tindakan apa pun, karena stack mengganti kuncinya saat dimulai.

Untuk mencantumkan kunci sebuah environment, termasuk yang telah dicabut, jalankan `list-keys` sebagai berikut:

* Gunakan terminal yang Anda siapkan di [Memanggil API pada server yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api). Jangan gunakan terminal yang menjalankan `docker compose`.
* Di Kubernetes, jalankan terlebih dahulu `kubectl -n cma-server port-forward svc/$server 8400:8400` di terminal lain, dengan `$server` juga diatur di sana.
* Jalankan perintah dari direktori teratas arsip, sekali untuk setiap environment, dengan ID environment tersebut.

```bash
echo "$ANTHROPIC_API_KEY" | ./cma-server-admin list-keys \
  -base-url http://127.0.0.1:8400 -env env_01595EKxaaTTGwwY3kyXdtbs \
  -key-file - -all
```

### Menguji cadangan

Untuk membuktikan bahwa sebuah dump dapat dipulihkan, jalankan hanya langkah “Pulihkan cadangan ke database baru”. Langkah tersebut ada di [Memulihkan cadangan di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#restore-the-backup-on-kubernetes) dan di [Memulihkan cadangan di Docker Compose](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#restore-the-backup-on-docker-compose). Langkah tersebut tidak mengubah database yang sedang digunakan. Kemudian hapus database baru tersebut. Di Docker Compose, namanya adalah nama database Anda dengan `_restored` di bagian akhir.

## Pengaturan dan path yang perlu diperiksa

Baca bagian ini sebelum Anda menjalankan perintah peningkatan.

Periksa bagian `web_tools` di [file pengaturan](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#where-settings-go) Anda. Jika file tersebut tidak memiliki bagian itu, atau bagian tersebut tidak mengatur kunci apa pun, alat `web_search` dan `web_fetch` akan nonaktif setelah peningkatan. Agen yang menggunakan toolset default kemudian berjalan tanpa alat-alat tersebut, tanpa error. Agen yang toolset-nya mengaktifkan salah satu alat tersebut tidak dapat memulai sesi. Untuk mempertahankan alat-alat tersebut, lihat [Alat web memerlukan pengaturan server](https://platform.claude.com/docs/id/managed-agents/self-hosted/differences#web-tools-need-a-server-setting).

Di Kubernetes, periksa bahwa setiap file values sandbox, seperti `cma-values.yaml`, mengatur `egress.mode`. Untuk mempertahankan akses sandbox Anda ke internet publik, tambahkan `mode: publicInternet` di bawah `egress`. Jika sebuah file tidak mengatur mode, chart menerapkan mode default-nya, `closed`. Perintah `helm upgrade` untuk chart sandbox kemudian berhenti dengan error seperti `egress.mode is closed and egress.closed.hosts is empty`, dan tidak mengubah apa pun.

Periksa `sandbox.idleTimeout` di file yang sama. Jika sebuah file tidak mengaturnya, pod sebuah sesi akan hilang sekitar 5 menit setelah giliran agen berakhir. Proses yang dibiarkan berjalan oleh agen akan berhenti bersama pod tersebut. Secara default, file di `/workspace` tetap ada. Untuk mempertahankan pod selama 30 menit, tambahkan `idleTimeout: 30m` di bawah `sandbox`.

Periksa file pengaturan untuk `inference.attribution`, dan environment server untuk `CMA_INFERENCE__ATTRIBUTION`. Hapus barisnya jika Anda menemukannya. Rilis tujuan peningkatan Anda tidak memiliki pengaturan tersebut, dan server-nya tidak akan mulai jika salah satunya diatur.

Ketika Claude API adalah penyedia inferensi Anda, setiap panggilan model membawa ID sesinya serta ID agen dan environment sesi tersebut setelah peningkatan. Lihat [Apa yang dikirim server ke penyedia inferensinya](https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access#what-the-server-sends-to-its-inference-provider).

### Kubernetes: nama objek Anda

`cma-server-values.yaml` harus menyatakan nama mana yang dimiliki instalasi Anda, dalam pengaturan `earlierNames`-nya. Untuk menemukan nama Deployment server, jalankan `kubectl -n cma-server get deployment -l anthropic.com/role=server`.

| Nama Deployment | Baris di `cma-server-values.yaml` |
| --------------- | --------------------------------- |
| `cma-onprem`    | `earlierNames: true`              |
| `cma-server`    | `earlierNames: false`             |

Jika file tersebut tidak memiliki baris itu, tambahkan sebelum Anda meningkatkan, dan pertahankan untuk setiap peningkatan berikutnya. Tanpa baris tersebut, perintah `helm upgrade` untuk chart server berhenti dengan error yang menyebutkan `earlierNames`, dan tidak mengubah apa pun.

Dengan `earlierNames: true`, objek chart mempertahankan nama `cma-onprem`-nya, dan server tetap menemukan Secret yang Anda buat dengan nama-nama tersebut. Halaman-halaman ini menggunakan nama di kolom tengah. Dengan `earlierNames: true`, gunakan nama di kolom terakhir sebagai gantinya:

| Objek                                             | Nama di halaman-halaman ini     | Nama dengan `earlierNames: true` |
| ------------------------------------------------- | ------------------------------- | -------------------------------- |
| Deployment dan Service server                     | `cma-server`                    | `cma-onprem`                     |
| Job migrasi                                       | `cma-server-migrate`            | `cma-onprem-migrate`             |
| Job setiap environment                            | `cma-server-environment-<name>` | `cma-onprem-environment-<name>`  |
| Secret dengan kata sandi database                 | `cma-server-db`                 | `cma-onprem-db`                  |
| Secret dengan kredensial penyedia inferensi       | `cma-server-upstream`           | `cma-onprem-upstream`            |
| Secret dengan kunci API server dan kunci enkripsi | `cma-server-keys`               | `cma-onprem-server`              |

Apa pun nilai `earlierNames`, namespace-nya bernama `cma-server`, dan image server bernama `cma-server-image`.

Setiap file values sandbox yang mengatur `egress.mode: gateway` harus menyebutkan dua Service server, di bawah `egress.gateway`. Jika sebuah file tidak melakukannya, tambahkan kedua baris tersebut. Contoh ini berisi nama-nama untuk instalasi dengan `earlierNames: true`:

```yaml
egress:
  gateway:
    serverService: cma-onprem
    serverEgressService: cma-onprem-egress
```

### Docker Compose: tata letak arsip dan path

Jika rilis yang Anda tingkatkan tidak memiliki direktori `compose`, `docker-compose.yml`-nya berada di tingkat teratas arsip, di samping `bin`. Di arsip baru, file tersebut berada satu tingkat lebih dalam, di `compose`.

Pada langkah “Ulangi perubahan Anda lainnya”, lakukan juga perubahan berikut:

* **File Compose milik Anda sendiri:** Jika arsip lama tidak memiliki direktori `compose`, file Anda juga berpindah satu tingkat lebih dalam. Path seperti `./bin` di dalamnya menjadi `../bin`. Jika file tersebut menyebutkan layanan `cma-onprem`, ubah nama tersebut menjadi `cma-server`.
* **Path di bawah `/etc/cma-onprem/` atau `/run/cma-onprem/`:** Ubah masing-masing agar diawali dengan `/etc/cma-server/` atau `/run/cma-server/`. Periksa `.env` dan `compose.config.yaml` rilis baru, file Compose milik Anda sendiri, dan setiap baris `volumes:` yang Anda tambahkan. Pada baris `volumes:`, ubah hanya bagian setelah titik dua pertama, yaitu path di dalam container.
