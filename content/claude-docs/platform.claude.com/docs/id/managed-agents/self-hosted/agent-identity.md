---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: d270685935c2bf1f12b731b70ae3f970c78f8259875c05649486dce59fab6380
---

---
title: Identitas dan kredensial agen
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity
description: Minta server Claude Managed Agents yang Anda hosting sendiri menandatangani token berumur pendek yang menyebutkan nama setiap agen, simpan kredensial vault di pengelola rahasia Anda, dan jauhkan rahasia dari sandbox dengan gateway egress.
---

<Note>
  Untuk meminta akses ke Claude Managed Agents yang di-host sendiri, hubungi tim akun Anthropic Anda.
</Note>

Halaman ini menunjukkan cara agar sistem di luar server Anda dapat memercayai sebuah agen, dan tempat menyimpan kredensial yang digunakan agen Anda:

* [Identitas agen](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#agent-identity): Izinkan server MCP atau gateway memberikan akses tersendiri kepada setiap agen. Server menandatangani token berumur pendek yang menyebutkan nama agen.
* [Pengelola rahasia](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#secret-manager): Server menyimpan kredensial vault di AWS Secrets Manager, Google Cloud Secret Manager, HashiCorp Vault, atau Azure Key Vault.
* [Kredensial variabel lingkungan](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#environment-variable-credentials): Izinkan perintah-perintah agen memanggil sebuah layanan sementara sandbox hanya menyimpan placeholder. “Egress gateway” (gateway keluar) memasukkan nilai sebenarnya ke dalam permintaan agen.

## Identitas agen

Server Anda dapat menandatangani “JSON Web Token” (token web JSON), atau JWT, berumur pendek yang menyebutkan nama sebuah agen, dan mengirimkannya bersama panggilan MCP agen tersebut. Penerima, yaitu server MCP atau gateway, memeriksa token tersebut terhadap kunci publik yang Anda publikasikan, lalu dapat memberikan akses tersendiri kepada setiap agen.

### Siapkan issuer

1. **Pilih URL issuer.** Anda mempublikasikan kunci publik Anda di URL ini pada langkah 3, dan penerima mengambilnya dari URL ini. Host web statis dapat digunakan. Jangan gunakan alamat server Anda, karena server tidak menyajikan kunci di path yang diambil oleh penerima. Gunakan URL `https://` tanpa path atau garis miring di akhir, pada hostname yang dapat Anda pertahankan.

2. **Buat kunci penandatanganan.** Jalankan perintah-perintah ini di direktori teratas arsip yang telah diekstrak:

   ```bash
   mkdir -m 700 agent-identity
   openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out agent-identity/signing-key.pem
   ```

3. **Publikasikan kunci publik.** Perintah ini menulis kunci tersebut ke `issuer-files/.well-known/`. Sajikan `issuer-files` di root hostname issuer, dengan tipe konten `application/json`.

   ```bash
   CMA_AGENT_IDENTITY__ISSUER=https://agents.example.com \
   CMA_AGENT_IDENTITY__KEY_FILE=./agent-identity/signing-key.pem \
     ./cma-server export-issuer -out issuer-files
   ```

4. **Berikan kunci kepada server.**

   <Tabs>
     <Tab title="Docker Compose">
       1. Jika arsip memiliki direktori `compose`, pindahkan direktori kunci ke dalamnya: `mv agent-identity compose/agent-identity`.
       2. Di `docker-compose.yml`, hapus baris `volumes: *server_mounts` pada layanan `cma-server`, dan hapus komentar pada blok `volumes:` di bawahnya. Jika Anda mengubah daftar `x-server-mounts`, lakukan perubahan yang sama di blok tersebut, karena layanan `cma-server` tidak lagi membaca daftar tersebut.
       3. Di direktori yang berisi `agent-identity`, jalankan `sudo chown -R root:root agent-identity`, kecuali jika Anda menggunakan Docker Desktop di macOS atau Docker rootless.
     </Tab>

     <Tab title="Kubernetes">
       Jalankan `kubectl -n cma-server create secret generic cma-agent-identity --from-file=agent-identity/signing-key.pem`. Kemudian atur `server.agentIdentity.secretName` ke `cma-agent-identity` di file values chart server.
     </Tab>
   </Tabs>

5. **Ubah [file pengaturan](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#where-settings-go).** Cantumkan hostname penerima di [`mcp.allowed_hostnames`](https://platform.claude.com/docs/id/managed-agents/self-hosted/differences#mcp-servers-need-an-allowlist-entry), dan tambahkan bagian ini:

   ```yaml
   agent_identity:
     issuer: https://agents.example.com
     key_file: /run/cma-server/agent-identity/signing-key.pem
     direct:
       audiences:
         - audience: https://mcp-gateway.example.com
           urls:
             - https://mcp-gateway.example.com
   ```

   Setiap `audience` menyebutkan satu penerima, sebagai URL `https://`. `urls`-nya adalah prefiks URL dari server MCP yang dapat menerima token untuknya.

6. **Mulai ulang server.** Di stack Compose, jalankan `docker compose up -d` dari direktori file Compose alih-alih memulai ulang.

Agar kunci privat tidak disimpan dalam file, gunakan `key_secret` ([secret manager](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#secret-manager) Anda) atau `kms_key` (AWS KMS atau Google Cloud KMS). [Referensi konfigurasi](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#agent-identity) menjelaskan kedua pengaturan tersebut.

### Kirim token ke server MCP

[Konektor MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector) menjelaskan field dari entri server MCP milik agen. Tambahkan field `auth` ke entri tersebut:

```yaml
mcp_servers:
  - type: url
    name: tickets
    url: https://mcp-gateway.example.com/tickets
    auth:
      type: agent_token
      audience: https://mcp-gateway.example.com
```

Untuk setiap daftar alat atau panggilan alat, server Anda menandatangani token baru. Server mengirimkan token sebagai `Authorization: Bearer <token>`, sebagai pengganti kredensial vault. Baik model maupun worker tidak menerimanya.

Untuk mengirimkan token sekaligus [kredensial vault](https://platform.claude.com/docs/id/managed-agents/vaults), ganti field `auth` dengan field `agent_token_header`:

```yaml
mcp_servers:
  - type: url
    name: tickets
    url: https://mcp-gateway.example.com/tickets
    agent_token_header:
      audience: https://mcp-gateway.example.com
```

Kredensial vault dikirim dalam header `Authorization`, seperti pada entri yang tidak memiliki kedua field tersebut. Token dikirim dalam header `Agent-Identity-Token`, tanpa prefiks `Bearer`.

SDK tidak memiliki field `auth` dan `agent_token_header`. Dalam kode SDK, tambahkan field tersebut ke entri server MCP sebagai field tambahan, atau kirimkan permintaan sebagai JSON biasa.

Halaman-halaman ini menunjukkan cara mengirimkan field tambahan:

[Python SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python#undocumented-request-params) · [TypeScript SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript#undocumented-request-params) · [Go SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go#request-fields) · [Java SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#undocumented-parameters) · [PHP SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php#undocumented-request-parameters) · [Ruby SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/ruby#undocumented-request-params)

Beberapa halaman tersebut hanya menunjukkan field tambahan di tingkat teratas permintaan, bukan di dalam entri daftar. Dalam hal ini, jadikan `mcp_servers` itu sendiri sebagai field tambahan. Kirimkan seluruh daftar dengan cara tersebut, dengan `auth` atau `agent_token_header` di entrinya.

Untuk menghentikan token sebuah agen, hapus entri tersebut dari agen, atau arsipkan agen tersebut. Token yang sudah terkirim tetap valid hingga `exp`-nya, paling lama 5 menit secara default.

### Apa yang diperiksa penerima

Minta penerima hanya menerima permintaan jika semua kondisi berikut terpenuhi:

* Tanda tangan terverifikasi dengan sebuah kunci di set kunci Anda, `<issuer>/.well-known/jwks.json`. Kunci yang tepat adalah kunci yang ID-nya cocok dengan `kid` di header token. Untuk kunci RSA, algoritmanya adalah `RS256`.
* `iss` sama dengan URL issuer Anda, dan `aud` sama dengan audience penerima.
* `exp` berada di masa depan, dan `iat` tidak berada di masa depan.
* `typ` di header token adalah `agent+jwt`, dan `token_use` adalah `agent`.

Kemudian terapkan aturan-aturan berikut:

* Dasarkan aturan akses setiap agen pada klaim `agent_id`, yaitu ID agen di API.
* Terimalah `jti` yang berulang, karena satu daftar atau panggilan dapat memerlukan beberapa permintaan dengan token yang sama.
* Minta gateway memanggil setiap alat dengan kredensialnya sendiri, dan jangan pernah meneruskan token tersebut.

Dengan [single sign-on](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#single-sign-on), token dari panggilan alat juga menyebutkan pemanggil yang membuat sesi tersebut, dalam klaim `actor_sub` dan `actor_iss`. `actor_sub` tidak berarti bahwa pemanggil menyetujui panggilan tersebut. Model yang memilih setiap panggilan.

Token-token berikut tidak memiliki `actor_sub`:

* Token dari daftar alat
* Token dari panggilan subagen
* Setiap token dari sesi yang dibuat oleh kunci API server

Jika suatu aturan bergantung pada pemanggil, tolak panggilan alat yang tidak memiliki `actor_sub`.

### Menguji gateway MCP

Perintah `check-gateway` mengirimkan token valid dan tidak valid ke gateway MCP. Berikan perintah tersebut file pengaturan tersendiri, di sini `check-gateway.yaml`:

1. Salin ke dalam file hanya bagian `mcp` dan `agent_identity` dari pengaturan server, serta `limits.mcp_call_timeout` jika server mengaturnya.
2. Di salinan tersebut, ubah `key_file` menjadi path kunci di mesin tempat Anda menjalankan perintah, seperti `./agent-identity/signing-key.pem`. Jika Anda memindahkan direktori tersebut ke dalam `compose`, path-nya adalah `./compose/agent-identity/signing-key.pem`.

Untuk `-agent`, berikan ID agen yang diizinkan oleh gateway. Jika kunci dimiliki oleh root, gunakan `sudo`.

```bash
./cma-server check-gateway -config check-gateway.yaml -agent agent_011CYm1BLqPXpQRk5khsSXrs \
  -url https://mcp-gateway.example.com/tickets
```

Perintah ini mencetak satu baris untuk setiap permintaan yang dikirimnya, beserta jawaban gateway. Eksekusi yang lolos kemudian mencetak baris yang diawali dengan `check-gateway: PASS`, dan keluar dengan kode `0`. Eksekusi yang gagal menyebutkan apa yang salah, pada baris yang diawali dengan `check-gateway:`, dan keluar dengan kode `1`.

## Pengelola rahasia

Secara default, server menyimpan rahasia dari [kredensial vault](https://platform.claude.com/docs/id/managed-agents/vaults) di database-nya. Dengan bagian `secret_store`, server menulis rahasia setiap kredensial vault baru ke “secret manager” (pengelola rahasia) Anda, di bawah prefiks nama yang Anda khususkan untuknya. Database hanya menyimpan referensi.

Tambahkan blok untuk pengelola rahasia Anda ke [file pengaturan](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#where-settings-go):

<Tabs>
  <Tab title="AWS Secrets Manager">
    ```yaml
    secret_store:
      type: aws_secrets_manager
      region: us-east-1
      prefix: cma-server/prod/
    ```
  </Tab>

  <Tab title="Google Cloud Secret Manager">
    ```yaml
    secret_store:
      type: gcp_secret_manager
      project: my-project        # the project ID, not its number
      prefix: cma-server-prod--
    ```
  </Tab>

  <Tab title="Azure Key Vault">
    ```yaml
    secret_store:
      type: azure_key_vault
      vault_url: https://my-vault.vault.azure.net
      prefix: cma-server-prod--
    ```
  </Tab>

  <Tab title="HashiCorp Vault">
    ```yaml
    secret_store:
      type: hashicorp_vault
      address: https://vault.internal:8200
      prefix: cma-server/prod/
      approle:
        role_id: <role-id>
        secret_id_file: /run/vault/secret-id
      #kubernetes: { role: cma-server }
      #token_file: /run/vault/token
    ```

    Atur tepat satu dari tiga metode login:

    * **`approle`:** Gunakan dengan Docker Compose, di sebuah host, atau dengan Helm chart server. Server login dengan role ID, dan dengan secret ID yang dibacanya dari sebuah file.
    * **`kubernetes`:** Gunakan hanya pada instalasi Kubernetes Anda sendiri, yang pod server-nya memiliki token service account. Server login dengan token tersebut. Helm chart server tidak memberikan token seperti itu kepada pod server, sehingga metode ini tidak berfungsi dengan chart tersebut.
    * **`token_file`:** Gunakan untuk metode login Vault lainnya. Jalankan Vault Agent di samping server, dan minta Vault Agent menulis token-nya ke file ini.

    Dengan Helm chart server, berikan secret ID kepada server dalam sebuah Secret:

    1. Masukkan secret ID ke dalam sebuah Secret di namespace server, dan sebutkan nama Secret tersebut di `server.extensionFiles.secretName` milik chart.
    2. Atur `approle.secret_id_file` ke path secret ID tersebut. Chart me-mount setiap kunci dari Secret tersebut sebagai file di bawah `/run/cma-server/extension-files/`, sehingga kunci bernama `secret-id` berada di `/run/cma-server/extension-files/secret-id`.

    Untuk metode `kubernetes`, ikat role Kubernetes Vault ke namespace dan service account server, bukan ke namespace sandbox, `cma`.
  </Tab>
</Tabs>

### Memberikan akses

Berikan server satu identitas, dan batasi identitas tersebut pada prefiks. Direktori `iam/` di arsip memiliki file untuk setiap pengelola rahasia:

* **AWS Secrets Manager:** Ganti placeholder di `aws-secrets-manager-policy.json`, dan lampirkan policy ke identitas yang digunakan untuk menjalankan server.
* **Google Cloud Secret Manager:** Jalankan perintah-perintah yang ada di komentar `gcp-secret-manager-role.yaml`.
* **Azure Key Vault:** Role Azure mencakup seluruh key vault, bukan sebuah prefiks. Jadi berikan deployment key vault tersendiri, yang menggunakan kontrol akses berbasis role Azure. Ganti `SUBSCRIPTION_ID` di `azure-key-vault-role.json`, dan buat custom role darinya. Tetapkan role tersebut pada key vault ke identitas yang digunakan untuk menjalankan server.
* **HashiCorp Vault:** Ganti placeholder di `hashicorp-vault-policy.hcl`, dan lampirkan policy ke identitas yang digunakan untuk menjalankan server.

Terhadap AWS dan Google Cloud, server melakukan autentikasi seperti yang dilakukannya untuk inferensi. Terhadap Azure Key Vault, server melakukan autentikasi dengan Microsoft Entra ID, seperti yang dilakukannya untuk [Microsoft Foundry](https://platform.claude.com/docs/id/managed-agents/self-hosted/inference-provider#microsoft-foundry).

### Memeriksa penyiapan

Jalankan `validate-store` sebelum start pertama dan setelah setiap perubahan policy. Perintah ini membuat, membaca, dan menghapus secret uji di bawah prefiks, tanpa memulai server. Jalankan perintah tersebut di tempat server berjalan, dengan lingkungan server:

* **Docker Compose:** Jalankan di container server. Di Arm, ganti `linux_amd64` dalam perintah ini dengan `linux_arm64`:

  ```bash
  docker compose exec cma-server /opt/cma-server/bin/linux_amd64/cma-server validate-store -config /etc/cma-server/config.yaml
  ```

* **Di sebuah host:**

  ```bash
  ./cma-server validate-store -config /etc/cma-server/config.yaml
  ```

* **Kubernetes:** Jalankan perintah yang sama sebagai Job di bawah service account server.

Eksekusi yang lolos diakhiri dengan baris yang bertuliskan `pass`, dan keluar dengan kode `0`.

Dengan Azure Key Vault, jalankan pemeriksaan ini terhadap key vault Anda sebelum Anda mengandalkannya.

### Batasan pengelola rahasia

* **Pilih pengaturan sekali saja.** Setelah salah satu perubahan berikut, server tidak lagi menemukan secret yang ditulisnya sebelum perubahan:

  * Anda menghapus bagian `secret_store`.
  * Anda mengubah `type`, `prefix`, `region`, `project`, `vault_url`, `mount`, atau `namespace`. Dua yang terakhir adalah pengaturan HashiCorp Vault opsional.
  * Anda mengarahkan `address` ke Vault lain.

  Server menemukan secret tersebut kembali hanya jika Anda memulihkan nilai lama.

* **Satu identitas membaca seluruh prefiks.** Jika dua kelompok tidak boleh dapat menjangkau kredensial satu sama lain, berikan setiap kelompok deployment tersendiri. Setiap deployment memerlukan prefiks atau key vault dan identitasnya sendiri.

## Kredensial variabel lingkungan

Dengan [kredensial variabel lingkungan](https://platform.claude.com/docs/id/managed-agents/vaults#add-a-credential), perintah-perintah agen dapat memanggil sebuah layanan sementara sandbox hanya menyimpan placeholder untuk rahasia tersebut. Gateway egress memasukkan nilai sebenarnya ke dalam permintaan ke host yang dicantumkan oleh kredensial.

Gateway, `cma-egress`, adalah proxy dalam arsip rilis yang berada di antara sandbox Anda dan internet. Gateway ini nonaktif secara default, dan server Anda hanya menerima kredensial ini jika gateway diaktifkan.

Dengan gateway aktif, dua batasan berlaku untuk sandbox Anda:

* Sandbox hanya menjangkau internet melalui gateway.
* Gateway hanya terhubung ke host yang Anda cantumkan di pengaturan `egress.allowed_hostnames` server.

Cantumkan hostname publik yang persis, tanpa wildcard. Sertakan setiap host tempat perintah-perintah agen Anda mengunduh sesuatu.

Jika Anda membangun image sandbox sendiri, mulai worker melalui `cma-with-egress`, seperti yang ditunjukkan di [Membangun image sandbox Anda sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api#what-an-image-of-your-own-needs).

### Aktifkan gateway di stack Compose

Dari direktori yang berisi `docker-compose.yml`, tambahkan dua baris ke `.env`. Baris pertama mencantumkan host yang dihubungi gateway, dipisahkan koma. Baris kedua memuat file Compose gateway. Kemudian jalankan stack:

```bash
echo 'CMA_EGRESS__ALLOWED_HOSTNAMES=api.github.com' >> .env
echo 'COMPOSE_FILE=docker-compose.yml:docker-compose.egress.yml' >> .env
docker compose up --build -d
```

Jika Anda juga menggunakan file Compose lain, tambahkan ke baris `COMPOSE_FILE`. Variabel `COMPOSE_FILE` di shell Anda menimpa variabel yang ada di `.env`, jadi hapus variabel di shell tersebut.

File gateway mengatur pengaturan `egress` server lainnya, jadi jangan tambahkan bagian `egress` ke `compose.config.yaml`.

### Aktifkan gateway di Kubernetes

Langkah-langkah ini dimulai dari deployment di [Menerapkan di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes). Langkah-langkah ini menggunakan variabel `REGISTRY`, `TAG`, dan `PLATFORM` dari halaman tersebut serta kedua file values-nya. Jalankan perintah dari direktori teratas arsip, dengan OpenSSL 3.0 atau yang lebih baru. Chart sandbox tidak menyediakan gateway di Azure Kubernetes Service (AKS).

Upgrade chart server dalam langkah-langkah ini juga menambahkan network policy atas pod-pod server. Periksa dua port yang dicakupnya sebelum Anda memulai:

* **Port 9464, port metrik:** Policy ini menutupnya. Jika Prometheus melakukan scraping pada port tersebut, atur `server.telemetry.prometheus.scraper.namespace` di `cma-server-values.yaml` ke namespace tempat Prometheus berjalan.
* **Port 8400, port API:** Policy ini mengizinkan semua sumber. Jika policy Anda sendiri membatasi siapa yang dapat menjangkau port 8400, batasan tersebut berhenti berfungsi. Network policy bersifat akumulatif, sehingga koneksi dapat lolos jika salah satu policy mengizinkannya.

<Steps>
  <Step title="Build dan push image gateway">
    ```bash
    docker buildx build --platform "$PLATFORM" -f kubernetes/egress/Dockerfile -t "$REGISTRY/cma-egress:$TAG" --push .
    ```
  </Step>

  <Step title="Buat certificate authority dan kunci gateway">
    ```bash
    (umask 077 && openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 -nodes -days 825 \
      -subj "/CN=cma-server egress gateway" \
      -addext "basicConstraints=critical,CA:TRUE,pathlen:0" \
      -addext "keyUsage=critical,keyCertSign,cRLSign" \
      -keyout egress-ca.key -out egress-ca.crt)
    kubectl -n cma create secret tls cma-egress-ca --cert=egress-ca.crt --key=egress-ca.key
    kubectl -n cma-server create configmap cma-egress-ca --from-file=ca.crt=egress-ca.crt
    GATEWAY_KEY=$(openssl rand -hex 32)
    printf %s "$GATEWAY_KEY" | kubectl -n cma create secret generic cma-egress-gateway-key --from-file=gateway-key=/dev/stdin
    printf %s "$GATEWAY_KEY" | kubectl -n cma-server create secret generic cma-egress-gateway-key --from-file=gateway-key=/dev/stdin
    unset GATEWAY_KEY
    ```

    Kemudian hapus `egress-ca.key`, kunci privat certificate authority. Siapa pun yang memegangnya dapat menyamar sebagai situs web mana pun terhadap sandbox Anda. Sertifikat berlaku selama 825 hari. Lihat [Perbarui sertifikat](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#renew-the-certificate).
  </Step>

  <Step title="Hapus sandbox dari sesi-sesi sebelumnya">
    Jika environment belum menjalankan sesi apa pun, lewati langkah ini. Sandbox dari sebelum perubahan tidak dapat memulai worker-nya setelahnya. Perintah-perintah ini juga menghapus workspace setiap sandbox:

    ```bash
    kubectl -n cma scale deployment cma-dispatcher --replicas=0
    kubectl -n cma delete sandboxwarmpool cma-sandbox
    kubectl -n cma delete sandboxclaims --all
    ```

    Di Google Kubernetes Engine (GKE), jalankan juga perintah ini:

    ```bash
    kubectl -n cma delete sandboxes --all
    ```

    Ulangi `kubectl -n cma get sandboxes,pods,pvc` hingga tidak menemukan apa pun. `helm upgrade` di langkah “Aktifkan sisi sandbox” menjalankan dispatcher kembali.
  </Step>

  <Step title="Aktifkan sisi server">
    Pilih alamat IPv4 yang bebas dalam rentang Service klaster untuk gateway. Kolom `CLUSTER-IP` dari `kubectl get svc -A` menampilkan alamat dalam rentang tersebut. Tambahkan ini ke `cma-server-values.yaml`. Jika file sudah memiliki blok `server`, gabungkan baris-baris ini ke dalamnya:

    ```yaml
    egressGateway:
      enabled: true
      proxyAddress: 34.118.224.53:3128   # the address that you chose, and port 3128
    server:
      config:
        egress:
          allowed_hostnames:
            - api.github.com
    ```

    Kemudian jalankan upgrade:

    ```bash
    helm upgrade cma-server kubernetes/server/chart --namespace cma-server -f cma-server-values.yaml --wait
    ```
  </Step>

  <Step title="Aktifkan sisi sandbox">
    Jalankan `kubectl -n cma-server get svc` untuk menampilkan dua Service milik server. Pada instalasi baru, keduanya bernama `cma-server` dan `cma-server-egress`.

    Di `cma-values.yaml`, ubah `egress.mode` menjadi `gateway`, dan tambahkan blok `gateway` di bawah `egress`. Berikan blok tersebut dua nama yang ditampilkan oleh perintah tadi:

    ```yaml
    egress:
      mode: gateway
      gateway:
        serviceIP: 34.118.224.53   # the address that you chose
        serverService: cma-server
        serverEgressService: cma-server-egress
        apiServerCIDRs:
          - 203.0.113.10/32        # the cluster's API endpoint
    ```

    Pertahankan nilai `egress` lainnya di file tersebut. Untuk mencetak alamat dan port endpoint API, jalankan `kubectl get endpoints kubernetes -n default`. Jika port-nya bukan 443, atur juga `egress.gateway.apiServerPort`.

    ```bash
    helm upgrade cma kubernetes/chart --namespace cma -f cma-values.yaml --wait
    ```

    Jika upgrade berhenti karena konflik pada `.spec.replicas`, jalankan `kubectl -n cma scale deployment cma-dispatcher --replicas=1`, lalu jalankan upgrade lagi.
  </Step>
</Steps>

### Tambahkan kredensial

Buat kredensial variabel lingkungan seperti yang ditunjukkan di [Tambahkan kredensial](https://platform.claude.com/docs/id/managed-agents/vaults#add-a-credential). Panduan layanan yang di-hosting menyatakan bahwa kredensial ini tidak didukung dengan sandbox yang di-host sendiri. Hal tersebut menjelaskan layanan yang di-hosting, bukan server Anda.

Server Anda menambahkan aturannya sendiri. Server menolak permintaan yang melanggar salah satunya dengan error `400` yang menyebutkan field-nya. Dua dari aturan tersebut adalah sebagai berikut:

* `networking` (csharp, go: `Networking`) harus bertipe `limited`, dan setiap host di `allowed_hosts` (java, php: `allowedHosts`; csharp, go: `AllowedHosts`) harus ada di daftar `egress.allowed_hostnames` server.
* `injection_location` (java, php: `injectionLocation`; csharp, go: `InjectionLocation`) harus berupa `{"header": true}` dalam JSON, dan tidak boleh dihilangkan.

Setelah Anda menambahkan host ke daftar server, terapkan perubahan tersebut. Di Docker Compose, jalankan `docker compose up -d`. Di Kubernetes, jalankan perintah `helm upgrade` server dan `kubectl -n cma-server rollout restart deployment -l anthropic.com/role=server`.

### Periksa gateway egress

Buat sesi dengan vault kredensial tersebut, dan minta agen menjalankan dua perintah. Contoh ini untuk kredensial bernama `GITHUB_TOKEN` yang mencantumkan `api.github.com`:

```bash
printenv GITHUB_TOKEN
curl -sS -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user
```

Perintah pertama mencetak placeholder yang diawali dengan `cma_ph_`. Perintah kedua mencetak profil akun GitHub milik token tersebut, karena gateway mengganti placeholder dengan token. Gateway menolak permintaan ke host yang tidak ada di daftar Anda dengan error `403`.

Di Kubernetes, jika setiap permintaan mendapatkan error `503`, jaringan klaster Anda kemungkinan menulis ulang alamat pod, seperti yang dilakukan opsi `--masquerade-all` dari kube-proxy. Gateway membedakan sandbox berdasarkan alamat pod-nya, jadi alamat tersebut harus sampai ke gateway tanpa diubah.

### Perbarui sertifikat

Di Kubernetes, perbarui sertifikat saat tidak ada sesi yang berjalan. Ulangi seluruh langkah “Buat certificate authority dan kunci gateway” di [Aktifkan gateway di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#turn-on-the-gateway-on-kubernetes). Langkah tersebut membuat certificate authority dan kunci gateway kembali, sehingga Anda tidak memerlukan file `egress-ca.key` yang telah Anda hapus. Lakukan satu perubahan: tambahkan `--dry-run=client -o yaml | kubectl apply -f -` di akhir masing-masing dari empat baris yang menjalankan `kubectl create`. Misalnya, baris yang diakhiri dengan `--from-file=gateway-key=/dev/stdin` kemudian diakhiri dengan `--from-file=gateway-key=/dev/stdin --dry-run=client -o yaml | kubectl apply -f -`.

Kemudian mulai ulang server dan gateway:

```bash
kubectl -n cma-server rollout restart deployment -l anthropic.com/role=server
kubectl -n cma rollout restart deployment/cma-egress
```

### Batasan gateway egress

* **Header:** Gateway hanya memasukkan nilai ke dalam header permintaan, tidak pernah ke dalam URL atau body. Secara default, satu-satunya header adalah `Authorization`. Untuk mengizinkan header lain, cantumkan bersama `Authorization` di `egress.swap_header_names`, atau di `CMA_EGRESS__SWAP_HEADER_NAMES` di `.env` untuk stack Compose.
* **Program yang mengabaikan variabel proxy:** Sandbox menemukan gateway melalui `HTTPS_PROXY` dan variabel terkait. Alat Java seperti Maven dan Gradle tidak membaca variabel tersebut, sehingga alat-alat tersebut tidak dapat menjangkau apa pun.
