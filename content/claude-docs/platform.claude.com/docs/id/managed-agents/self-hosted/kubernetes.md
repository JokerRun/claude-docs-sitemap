---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: fe1986a089774d7ed6b24536add9d8cebc8a66f9838e9bcedba728ee47fa2736
---

---
title: Menerapkan di Kubernetes
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes
description: Instal server Claude Managed Agents yang di-host sendiri dan sandbox-nya pada klaster Kubernetes dengan dua Helm chart dalam arsip rilis, lalu jalankan sesi pertama di pod sandbox.
---

<Note>
  Untuk meminta akses ke Claude Managed Agents yang di-host sendiri, hubungi tim akun Anthropic Anda.
</Note>

Halaman ini membawa “cluster” (klaster) Google Kubernetes Engine (GKE) yang kosong hingga menjadi sesi yang menjalankan alat di pod sandbox. Halaman ini menggunakan dua Helm chart dalam arsip rilis, yang menjalankan seluruh stack pada klaster:

* **`cma-server`:** Menerapkan skema database dan menjalankan dua server di belakang sebuah Service, di “namespace” (ruang nama) `cma-server`.
* **`cma-sandboxes`:** Menjalankan sebuah dispatcher dan pod sandbox di namespace `cma`. Dispatcher melakukan polling ke server untuk mencari pekerjaan dan memberi setiap sesi pod sandbox-nya sendiri, tempat sebuah worker menjalankan alat shell dan file milik agen.

Database PostgreSQL Anda tetap berada di luar keduanya. Pada jenis klaster lain, langkah-langkahnya sama, tetapi prasyarat klaster dan beberapa nilai chart berbeda. Lihat [Klaster lain](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#other-clusters).

## Prasyarat

* **Sebuah klaster:** Kubernetes 1.30 atau lebih baru, dengan:

  * Controller Agent Sandbox (di GKE, [add-on Agent Sandbox](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/how-install-agent-sandbox))
  * Node yang menjalankan gVisor (di GKE, [node pool GKE Sandbox](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/sandbox-pods))
  * Plugin jaringan yang menerapkan NetworkPolicy (di GKE, Dataplane V2 atau Calico)

* **Sebuah database:** PostgreSQL 16 atau lebih baru yang dapat dijangkau oleh klaster.

* **Sebuah registry:** Registry tempat klaster dapat menarik image. Anda membangun image sendiri.

* **Sebuah kunci API Claude:** Server menggunakannya untuk panggilan model. Untuk menggunakan penyedia lain, lihat [Penyedia inferensi](https://platform.claude.com/docs/id/managed-agents/self-hosted/inference-provider).

* **Izin:** Hak cluster-admin atau yang setara. Instalasi membuat namespace, Role, dan sebuah ClusterRoleBinding.

* **Alat di mesin Anda:** `helm`, `kubectl`, `docker buildx`, `openssl`, dan [CLI `ant`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart#installation).

* **Arsip rilis:** Untuk meminta akses ke unduhan, hubungi tim akun Anthropic Anda. Ekstrak arsip tersebut. Jalankan setiap perintah di halaman ini dari direktori teratasnya.

## Menginstal stack

<Steps>
  <Step title="Membangun dan mendorong image">
    Atur variabel-variabel ini ke nilai milik Anda. `PLATFORM` adalah arsitektur node Anda. `TAG` adalah versi rilis, yang ada di nama arsip setelah `v`. Kedua chart mengharapkan image yang menggunakan versi ini sebagai tag-nya.

    ```bash
    REGISTRY=us-docker.pkg.dev/my-project/cma
    TAG=1.2.3
    PLATFORM=linux/amd64
    ```

    Kemudian bangun dan dorong ketiga image tersebut:

    ```bash
    docker buildx build --platform "$PLATFORM" -f kubernetes/server/Dockerfile -t "$REGISTRY/cma-server-image:$TAG" --push .
    docker buildx build --platform "$PLATFORM" -f kubernetes/dispatcher/Dockerfile -t "$REGISTRY/cma-dispatcher:$TAG" --push .
    docker buildx build --platform "$PLATFORM" -t "$REGISTRY/cma-sandbox:$TAG" --push kubernetes/sandbox
    ```
  </Step>

  <Step title="Membuat file secrets dan database">
    Buat sebuah file berisi kata sandi database yang dihasilkan dan placeholder untuk kunci API Claude Anda:

    ```bash
    cat > secrets.env <<EOF
    PG_PASSWORD=$(openssl rand -hex 32)
    UPSTREAM_KEY=sk-ant-...
    EOF
    chmod 600 secrets.env
    ```

    Buka `secrets.env` di editor dan ganti `sk-ant-...` dengan kunci API Claude Anda. Kemudian hubungkan ke server database Anda sebagai administrator, misalnya dengan `psql`. Jalankan SQL ini, dengan nilai `PG_PASSWORD` sebagai pengganti `...`:

    ```sql
    CREATE ROLE cma_server LOGIN PASSWORD '...';
    GRANT cma_server TO CURRENT_USER;
    CREATE DATABASE cma_server OWNER cma_server;
    ```
  </Step>

  <Step title="Membuat namespace dan Secret untuk server">
    Buat namespace milik server dan Secret-nya:

    ```bash
    source secrets.env
    ENCRYPTION_KEY=$(openssl rand -base64 32)
    kubectl create namespace cma-server
    kubectl label namespace cma-server pod-security.kubernetes.io/enforce=restricted pod-security.kubernetes.io/enforce-version=latest
    kubectl -n cma-server create secret generic cma-server-db \
      --from-literal=PGPASSWORD="$PG_PASSWORD"
    kubectl -n cma-server create secret generic cma-server-keys \
      --from-literal=CMA_SERVER__API_KEY="$(openssl rand -hex 32)" \
      --from-literal=CMA_STORE__CREDENTIALS_ENCRYPTION_KEY="$ENCRYPTION_KEY"
    kubectl -n cma-server create secret generic cma-server-upstream \
      --from-literal=ANTHROPIC_API_KEY="$UPSTREAM_KEY"
    ```

    Cetak kunci enkripsi dengan `echo "$ENCRYPTION_KEY"`, dan simpan salinannya di luar klaster. Server menggunakan kunci ini untuk mengenkripsi kredensial yang disimpannya, dan database yang dipulihkan membutuhkannya. Kemudian hapus `secrets.env`. Secret `cma-server-db` menyimpan kata sandi database.
  </Step>

  <Step title="Membuat namespace dan sertifikat untuk sandbox">
    Buat namespace untuk sandbox, serta sertifikat yang disajikan oleh dispatcher dan dipercaya oleh sandbox:

    ```bash
    kubectl create namespace cma
    kubectl label namespace cma pod-security.kubernetes.io/enforce=restricted pod-security.kubernetes.io/enforce-version=latest
    openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 -nodes -days 825 \
      -subj "/CN=cma-dispatcher.cma.svc" \
      -addext "subjectAltName=DNS:cma-dispatcher.cma.svc,DNS:cma-dispatcher.cma.svc.cluster.local" \
      -keyout tls.key -out tls.crt
    kubectl -n cma create secret tls cma-dispatcher-tls --cert=tls.crt --key=tls.key --dry-run=client -o yaml | kubectl apply -f -
    kubectl -n cma create configmap cma-dispatcher-ca --from-file=ca.crt=tls.crt --dry-run=client -o yaml | kubectl apply -f -
    ```
  </Step>

  <Step title="Menginstal server">
    Simpan ini sebagai `cma-server-values.yaml`, dengan registry Anda dan alamat database Anda:

    ```yaml
    earlierNames: false   # a new install
    image:
      registry: us-docker.pkg.dev/my-project/cma   # REGISTRY in the build commands
    database:
      url: host=10.20.0.5 port=5432 user=cma_server dbname=cma_server sslmode=require   # your database's address
    environments:
      - name: default
        namespace: cma
    ```

    Kemudian instal chart tersebut:

    ```bash
    helm install cma-server kubernetes/server/chart --namespace cma-server -f cma-server-values.yaml --wait
    kubectl -n cma-server logs job/cma-server-environment-default
    ```

    Instalasi ini membuat environment `default` dan menyimpan kuncinya di Secret `cma-environment` di namespace `cma`. Perintah kedua mencetak satu baris yang diawali `filled Secret cma/cma-environment`. Jika `helm install` pertama gagal, jalankan `helm uninstall` untuk rilis tersebut sebelum Anda menginstal lagi.
  </Step>

  <Step title="Menemukan alamat klaster yang akan diblokir">
    Instalasi ini memungkinkan sandbox menjangkau internet publik. Endpoint API klaster biasanya memiliki alamat publik, sehingga sandbox juga dapat menjangkaunya. Untuk memblokirnya, Anda mencantumkan alamatnya di bawah `egress.clusterCIDRs` pada langkah berikutnya.

    Untuk mencetak alamat tersebut, jalankan `gcloud container clusters describe my-cluster --format 'value(endpoint)'` dengan nama klaster Anda.

    Chart itu sendiri memblokir rentang privat `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, dan `100.64.0.0/10`. Jika klaster Anda memiliki rentang pod, service, atau node di luar keempat rentang tersebut, cantumkan juga rentang itu.
  </Step>

  <Step title="Menginstal sandbox">
    Simpan ini sebagai `cma-values.yaml`, dengan registry Anda dan alamat dari langkah sebelumnya:

    ```yaml
    platform: gke
    image:
      registry: us-docker.pkg.dev/my-project/cma   # REGISTRY in the build commands
    egress:
      mode: publicInternet
      clusterCIDRs:
        - 203.0.113.10/32                          # the cluster's API endpoint
      cmaServer:
        pods:
          namespace: cma-server
          matchLabels:
            anthropic.com/role: server
        port: 8400
    ```

    `egress.cmaServer` membuka jalur ke server Anda. Untuk membandingkan `publicInternet` dengan dua mode lainnya, lihat [Apa yang dapat dijangkau sandbox](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#what-sandboxes-can-reach).

    Jika klaster Anda menggunakan salah satu penyiapan DNS ini, tambahkan satu baris ke file tersebut:

    * **Cloud DNS for GKE, yang digunakan oleh klaster Autopilot:** `gke: {dns: cloudDns}`
    * **NodeLocal DNSCache:** `gke: {dns: nodeLocalCache, kubeDnsUpstreamIP: <address>}`. Untuk mencetak alamat tersebut, jalankan `kubectl -n kube-system get svc kube-dns-upstream -o jsonpath='{.spec.clusterIP}'`.

    Kemudian instal chart tersebut:

    ```bash
    helm install cma kubernetes/chart --namespace cma -f cma-values.yaml --wait
    ```
  </Step>
</Steps>

## Menjalankan sesi

Langkah-langkah ini menggunakan nama dari instalasi baru. Jika file values server Anda memiliki `earlierNames: true`, temukan nama yang harus digunakan sebagai gantinya di [Kubernetes: nama objek Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade#object-names).

<Steps>
  <Step title="Meneruskan port server">
    Di satu terminal, teruskan port server ke mesin Anda:

    ```bash
    kubectl -n cma-server port-forward svc/cma-server 8400:8400
    ```
  </Step>

  <Step title="Mengarahkan CLI ke server Anda">
    Di terminal kedua, arahkan `ant` CLI ke port yang di-forward dan baca kunci API server dari Secret `cma-server-keys`:

    ```bash
    export ANTHROPIC_BASE_URL=http://127.0.0.1:8400
    export ANTHROPIC_API_KEY=$(kubectl -n cma-server get secret cma-server-keys -o jsonpath='{.data.CMA_SERVER__API_KEY}' | base64 -d)
    ```
  </Step>

  <Step title="Membuat agen dan memintanya menjalankan perintah">
    Ikuti tiga langkah dari [Jalankan sesi pertama Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/quickstart#run-your-first-session) di quickstart: Buat agen, Mulai sesi, dan Minta agen menjalankan perintah. Di Mulai sesi, ganti `compose-sandbox` dengan `default`, nama environment yang dibuat oleh chart.
  </Step>

  <Step title="Menemukan pod sandbox">
    Agen membalas dengan hostname pod yang menjalankan perintah tersebut. Di terminal ketiga, `kubectl -n cma get pods` menampilkan pod dengan nama itu di samping pod milik dispatcher. Secara default, pod tersebut hilang sekitar 5 menit setelah giliran agen berakhir. Jika pod tersebut tidak ada dalam daftar, minta agen menjalankan `hostname` lagi.

    Untuk keluar dari chat, tekan Ctrl+C.
  </Step>
</Steps>

## Menempatkan TLS di depan server

Server berbicara HTTP biasa pada port 8400, dan permintaan dari aplikasi Anda membawa kunci API server. Sebelum klien di luar klaster terhubung, tempatkan “load balancer” (penyeimbang beban) atau ingress yang melakukan terminasi TLS di depan Service `cma-server`. Komponen tersebut harus:

* Meneruskan path permintaan tanpa perubahan.
* Menerima body permintaan hingga 32 MiB.
* Meneruskan respons tanpa buffer.
* Menetapkan batas waktu baca default 2 menit. Untuk permintaan Git, tetapkan batas waktu baca 10 menit untuk path yang cocok dengan `^/cma-[a-z]+/git/`.
* Mengirim lalu lintas hanya ke server yang siap. Service `cma-server` sudah melakukan ini. Load balancer yang menjangkau pod secara langsung harus memeriksa `/cma-server/readyz` pada setiap pod dan melewati pod yang mengembalikan `503`.
* Tidak pernah mengirim ulang `POST` yang sudah diterima oleh server.
* Tidak pernah menyimpan respons dalam cache.

Untuk memeriksanya dari luar klaster, jalankan `curl -s https://<host>/cma-server/healthz`. Responsnya adalah `{"status":"ok"}`.

## Apa yang dapat dijangkau sandbox

Di `cma-values.yaml`, `egress.mode: publicInternet` memungkinkan sandbox menjangkau internet publik.

Tabel ini membandingkannya dengan dua mode lainnya:

| `egress.mode`           | Apa yang dapat dijangkau sandbox                                                                                                                                                                                                         |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `closed`, nilai default | Server Anda dan dispatcher, tanpa server DNS                                                                                                                                                                                             |
| `publicInternet`        | Server Anda, dispatcher, server DNS, dan internet publik                                                                                                                                                                                 |
| `gateway`               | Server Anda, dispatcher, dan, melalui egress gateway, host yang Anda cantumkan. Lihat [Aktifkan gateway di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#turn-on-the-gateway-on-kubernetes). |

## Klaster lain

Atur `platform` di `cma-values.yaml` ke `eks` untuk Amazon EKS, ke `aks` untuk Azure Kubernetes Service (AKS), atau ke `generic` untuk klaster lain mana pun. Ketiganya memerlukan controller Agent Sandbox upstream beserta ekstensinya, dan plugin jaringan yang menerapkan NetworkPolicy. Semuanya juga memerlukan:

* **Amazon EKS:** Node group dengan `runsc` milik gVisor yang terdaftar sebagai handler containerd bernama `runsc`. Beri label pada node dengan `cma.anthropic.com/sandbox-node=true`, dan beri taint dengan `cma.anthropic.com/sandbox-node=true:NoSchedule`. Chart mendaftarkan RuntimeClass `gvisor` terhadap handler tersebut.
* **AKS:** Node pool dengan Pod Sandboxing, dengan label dan taint yang sama seperti di Amazon EKS. Masukkan nama mesin kebijakan jaringan klaster (`cilium`, `calico`, atau `azure`) di `aks.networkPolicy`. Pertahankan `egress.mode: publicInternet`, satu-satunya mode yang diterima chart di AKS. Ujilah chart ini di klaster Anda sebelum agen melakukan pekerjaan nyata di sana.
* **Klaster lain mana pun:** Sebuah RuntimeClass untuk gVisor atau runtime tersandbox lainnya. Masukkan namanya di `runtimeClass.name`.

Folder `kubernetes/chart/examples/` di dalam arsip berisi file values lengkap untuk setiap jenis klaster.

## Membebaskan volume sesi

Dengan default chart, setiap sesi memiliki volume 10 GiB untuk `/workspace`. Volume tersebut tetap ada setelah pod sesi hilang, sehingga pesan berikutnya dari sesi tersebut menemukan file-filenya.

| Untuk membebaskan                                | Lakukan ini                                                                                                                                                                                                                                                                      |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Volume satu sesi                                 | Arsipkan sesi setelah gilirannya berakhir. Dispatcher biasanya menghapus volume tersebut dalam sekitar 5 menit.                                                                                                                                                                  |
| Volume sesi yang tidak diarsipkan oleh siapa pun | Atur `dispatcher.retentionDays` di `cma-values.yaml`. Dispatcher kemudian menghapus volume setelah sesinya menganggur selama jumlah hari tersebut, dan pesan berikutnya dari sesi tersebut dimulai dengan `/workspace` yang kosong. Default chart, `0`, menyimpan setiap volume. |

Perintah-perintah di bagian ini ditujukan untuk GKE. Di klaster lain, gunakan `sandboxclaims` sebagai pengganti `sandboxes`.

Menghapus sesi tidak membebaskan volumenya. Arsipkan sesi terlebih dahulu. Hapus sesi tersebut hanya setelah `kubectl -n cma get sandboxes -l anthropic.com/session-id=<session-id>` tidak menampilkan apa pun.

Jika Anda menghapus sesi tanpa mengarsipkannya, bebaskan volumenya sendiri:

1. Temukan ID sesi di log dispatcher. Perintah ini mencetak satu baris untuk setiap sesi yang tampaknya telah dihapus dan masih memiliki volume, dengan ID setelah `session_id`:

   ```bash
   kubectl -n cma logs deployment/cma-dispatcher --since=6m \
     | grep "could not check the claim's session" | grep "403 Forbidden"
   ```

   Dispatcher menulis baris-baris ini setiap 5 menit. Jika sesi tersebut tidak tercantum, tunggu 5 menit lalu jalankan perintah itu lagi.

2. Pastikan bahwa sesi tersebut telah dihapus. Dengan port yang di-forward dan `ANTHROPIC_API_KEY` yang diatur seperti di [Menjalankan sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#run-a-session), jalankan `ant --base-url http://127.0.0.1:8400 beta:sessions retrieve --session-id <session-id>`. Lanjutkan hanya jika jawabannya adalah `404 Not Found` dengan `Session not found`. Jika perintah tersebut mencetak sebuah sesi, berhenti: sesi tersebut belum dihapus.

3. Hapus objek Kubernetes yang memiliki volume tersebut. File-file sesi ikut terhapus bersamanya:

   ```bash
   kubectl -n cma delete sandboxes -l anthropic.com/session-id=<session-id>
   ```

## Memperbarui kunci dan sertifikat

Kunci environment berlaku selama 365 hari, dan sertifikat dispatcher berlaku selama 825 hari. Perbarui masing-masing sebelum kedaluwarsa.

Dalam 30 hari terakhir masa berlaku kunci environment, server mencatat peringatan pada setiap permintaan yang menggunakan kunci tersebut. Peringatan tersebut diawali `environment key is within 30 days of expiry`.

### Memperbarui kunci environment yang dibuat oleh chart

Untuk melihat kapan kunci tersebut kedaluwarsa, jalankan `kubectl -n cma describe secret cma-environment`.

Jalankan dua perintah ini setidaknya sekali dalam 60 hari terakhir masa berlaku kunci, dari direktori teratas arsip rilis yang terinstal:

```bash
helm upgrade cma-server kubernetes/server/chart --namespace cma-server -f cma-server-values.yaml --wait
kubectl -n cma rollout restart deployment/cma-dispatcher
```

Setiap kali perintah `helm upgrade` milik chart server dijalankan, perintah tersebut menyimpan kunci baru di Secret jika kunci kedaluwarsa dalam 60 hari. Tidak ada hal lain yang memperbarui kunci. Perintah kedua memulai ulang dispatcher agar membaca kunci baru.

### Memperbarui sertifikat dispatcher

Kembali ke langkah “Membuat namespace dan sertifikat untuk sandbox”. Ulangi perintah `openssl`-nya dan dua perintah `kubectl` setelahnya. Lalu mulai ulang dispatcher dengan `kubectl -n cma rollout restart deployment/cma-dispatcher`.

### Mengganti kunci environment untuk worker Anda sendiri

Chart hanya memperbarui kuncinya sendiri. Jika Anda membuat kunci sendiri, seperti di [Membuat environment dan kuncinya](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api#create-an-environment-and-its-key), ganti kunci tersebut dengan CLI admin. CLI tersebut berada di direktori teratas arsip rilis.

Jalankan perintah-perintah tersebut di terminal kedua dari [Menjalankan sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#run-a-session), tempat `ANTHROPIC_API_KEY` berisi kunci API server. Biarkan port-forward tetap berjalan di terminal pertama. Jika Anda menjangkau server Anda di alamat lain, berikan alamat tersebut sebagai `-base-url`, dan Anda tidak memerlukan port-forward.

<Steps>
  <Step title="Membuat kunci baru untuk environment yang sama">
    Untuk `-env`, berikan ID environment:

    ```bash
    echo "$ANTHROPIC_API_KEY" | ./cma-server-admin mint-key \
      -base-url http://127.0.0.1:8400 -env env_01595EKxaaTTGwwY3kyXdtbs -key-file -
    ```

    Perintah ini mencetak kunci baru, dan mencetak ID serta waktu kedaluwarsa kunci pada standard error.
  </Step>

  <Step title="Memindahkan worker Anda ke kunci baru">
    Atur kunci baru sebagai `ANTHROPIC_ENVIRONMENT_KEY` untuk setiap proses yang melakukan polling, lalu mulai ulang proses tersebut.
  </Step>

  <Step title="Mencabut kunci lama">
    Worker yang masih menggunakan kunci yang telah dicabut akan menerima error `401` dan melepaskan sesi yang sedang dilayaninya. Untuk menemukan ID kunci lama, jalankan `list-keys` dengan flag `-base-url`, `-env`, dan `-key-file` yang sama. Ketika tidak ada lagi worker yang menggunakan kunci lama, cabut kunci tersebut berdasarkan ID itu:

    ```bash
    echo "$ANTHROPIC_API_KEY" | ./cma-server-admin revoke-key \
      -base-url http://127.0.0.1:8400 -env env_01595EKxaaTTGwwY3kyXdtbs \
      -key-id etok_01AbCdEfGhIjKlMnOpQrStUv -key-file -
    ```
  </Step>
</Steps>

## Menghapus instalasi stack

Hapus sandbox terlebih dahulu. `helm uninstall` menghapus kebijakan jaringan yang membatasi sandbox, tetapi sandbox yang dibuat oleh dispatcher untuk sesi tetap berjalan.

Langkah-langkah ini tidak menyentuh database Anda, tetapi menghapus Secret. Untuk menggunakan database lagi, Anda memerlukan salinan kunci enkripsi Anda.

<Steps>
  <Step title="Menghentikan dispatcher dan menghapus sandbox">
    ```bash
    kubectl -n cma scale deployment/cma-dispatcher --replicas=0
    kubectl -n cma delete sandboxwarmpool cma-sandbox
    kubectl -n cma delete sandboxclaims --all
    ```

    Di GKE, jalankan juga perintah ini:

    ```bash
    kubectl -n cma delete sandboxes --all
    ```
  </Step>

  <Step title="Menunggu hingga sandbox hilang">
    Ulangi perintah ini hingga sandbox, pod-nya, dan volume-nya hilang:

    ```bash
    kubectl -n cma get sandboxes,pods,pvc
    ```
  </Step>

  <Step title="Menghapus instalasi chart dan menghapus namespace">
    ```bash
    helm uninstall cma --namespace cma
    helm uninstall cma-server --namespace cma-server
    kubectl delete namespace cma cma-server
    ```
  </Step>
</Steps>

## Langkah selanjutnya

* **Meningkatkan:** [Meningkatkan Claude Managed Agents yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade) berisi perintah-perintah `helm upgrade`.
* **Mengubah nilai chart lainnya:** Lihat komentar di `kubernetes/server/chart/values.yaml` untuk server dan `kubernetes/chart/values.yaml` untuk sandbox.
* **Memanggil API dari kode Anda:** Lihat [Memanggil API pada server yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api).
* **Bekerja di browser:** Lihat [Gunakan konsol di server Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/console).
