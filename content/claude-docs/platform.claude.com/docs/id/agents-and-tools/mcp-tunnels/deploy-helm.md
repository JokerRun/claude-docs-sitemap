---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-helm
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: 56dc68b136d1cdc9b1b21becd30cd6b50b7b4ea3d7d3439466f81c4ae93c0a52
---

# Deploy tunnel MCP dengan Helm

Instal tunnel stack pada cluster Kubernetes menggunakan Helm chart Anthropic.

---

<Note>
  Tunnel MCP sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Note>

Helm chart Anthropic menginstal [tunnel stack](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) sebagai satu Deployment dan melampirkannya ke tunnel Anda: tunnel yang dibuat oleh setup hook chart untuk Anda, atau tunnel yang sudah ada yang Anda buat di [Console](/docs/id/agents-and-tools/mcp-tunnels/console#create-a-tunnel).

## Sebelum Anda mulai

Anda memerlukan:

* **Sebuah tunnel.** Dengan akses programatik, setup hook chart membuatnya untuk Anda ketika Anda tidak menyediakan ID tunnel; untuk melampirkan ke tunnel yang sudah ada, [buat di Console](/docs/id/agents-and-tools/mcp-tunnels/console#create-a-tunnel) dan catat ID tunnel (`tnl_...`). Provisioning manual selalu dimulai dari tunnel yang dibuat di Console; Anda juga memerlukan token tunnel dan domain tunnel-nya.

* **Cara bagi chart untuk melakukan autentikasi ke Tunnels API.**

  * **[Akses programatik](/docs/id/agents-and-tools/mcp-tunnels/concepts#credential-provisioning) (direkomendasikan).** [Komponen setup](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) melakukan autentikasi melalui Workload Identity Federation, mengambil token tunnel, menghasilkan CA, mendaftarkannya ke Anthropic, dan menyimpan semuanya dalam sebuah Secret. Anda memerlukan aturan federasi dengan cakupan `workspace:manage_tunnels`.
  * **[Manual](/docs/id/agents-and-tools/mcp-tunnels/concepts#credential-provisioning).** Lewati akses programatik. Anda akan [mendapatkan token tunnel dari Console](/docs/id/agents-and-tools/mcp-tunnels/console#get-the-connection-details), menghasilkan CA dan sertifikat server sendiri, [mendaftarkan CA di Console](/docs/id/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate), dan menyediakan kredensial ke cluster sebagai Secrets.

* **Cluster Kubernetes** yang dapat Anda gunakan untuk deploy dengan `helm` dan `kubectl`. Tab **Tanpa akses programatik** juga menggunakan `openssl` (1.1.1 atau lebih baru).

* **Konektivitas jaringan keluar** dari cluster ke `api.anthropic.com` (443 TCP) dan [tunnel edge](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) (7844 TCP dan UDP). Lihat [persyaratan jaringan](/docs/id/agents-and-tools/mcp-tunnels/overview#network-requirements) lengkap.

* **Satu atau lebih server MCP** yang berjalan dan dapat dijangkau dari cluster pada alamat yang akan Anda konfigurasikan di bawah `gateway.config.routes`. Jika Anda belum memilikinya, [gunakan server contoh](#optional-use-a-sample-mcp-server).

## Opsional: Gunakan server MCP contoh

Jika Anda tidak memiliki server MCP yang tersedia untuk pengujian, gunakan server minimal ini:

```bash
kubectl create namespace mcp-tunnel --dry-run=client -o yaml | kubectl apply -f -
kubectl -n mcp-tunnel apply -f - <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: hello-mcp-src
data:
  hello_server.py: |
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("hello-server", host="0.0.0.0", port=9000)


    @mcp.tool()
    def hello(name: str = "world") -> str:
        """Say hello to someone."""
        return f"Hello, {name}!"


    if __name__ == "__main__":
        mcp.run(transport="streamable-http")
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-mcp
spec:
  replicas: 1
  selector:
    matchLabels: { app: hello-mcp }
  template:
    metadata:
      labels: { app: hello-mcp }
    spec:
      containers:
        - name: hello-mcp
          image: python:3.13-slim
          command: ["sh", "-c", "pip install --quiet mcp && python /app/hello_server.py"]
          volumeMounts:
            - { name: src, mountPath: /app }
          ports:
            - { containerPort: 9000 }
      volumes:
        - name: src
          configMap: { name: hello-mcp-src }
---
apiVersion: v1
kind: Service
metadata:
  name: hello-mcp
spec:
  selector: { app: hello-mcp }
  ports:
    - { port: 9000, targetPort: 9000 }
EOF
```

Langkah-langkah Instal berikutnya mencatat di mana harus menambahkan route yang sesuai.

## Instal

<Tabs>
  <Tab title="Dengan akses programatik">
    Komponen setup menukar token ServiceAccount yang diproyeksikan dari cluster melalui aturan federasi Anda, mengambil token tunnel, menghasilkan CA dan sertifikat server, dan mendaftarkan CA ke Anthropic. CronJob harian memperbarui sertifikat server sesuai kebutuhan, sehingga Anda tidak menangani secret apa pun secara manual.

    <Steps>
      <Step title="Siapkan Workload Identity Federation untuk cluster">
        Ikuti [Gunakan WIF dengan Kubernetes](/docs/id/manage-claude/wif-providers/kubernetes) untuk mendaftarkan OIDC issuer cluster Anda dan membuat aturan federasi. Komponen setup berjalan di bawah ServiceAccount-nya sendiri di namespace release; nama persisnya mengikuti konvensi `fullname` Helm, jadi untuk nama release apa pun selain `mcp-tunnel`, jalankan `helm template <release> ... | grep -A2 'kind: ServiceAccount'` untuk mengonfirmasinya sebelum membuat aturan. Sisa panduan ini mengasumsikan nama release `mcp-tunnel` di namespace `mcp-tunnel`, di mana ServiceAccount-nya adalah `mcp-tunnel-setup`.

        | Field    | Nilai                                               |
        | -------- | --------------------------------------------------- |
        | Subject  | `system:serviceaccount:mcp-tunnel:mcp-tunnel-setup` |
        | Audience | `api.anthropic.com` (default chart; tanpa skema)    |
        | Scope    | `workspace:manage_tunnels`                          |

        <Note>
          Audience default chart adalah `api.anthropic.com` tanpa skema, tetapi formulir aturan federasi di Console menyarankan `https://api.anthropic.com`. Keduanya harus cocok byte-per-byte atau autentikasi akan gagal. Atur audience aturan ke `api.anthropic.com`, atau atur `api.wif.audience` di `values.yaml` ke `https://api.anthropic.com`.
        </Note>

        Jika tunnel berada di workspace selain workspace default organisasi, tambahkan juga service account aturan tersebut sebagai anggota workspace itu di bawah **Settings > Workspaces** (Tunnels API melakukan otorisasi berdasarkan keanggotaan workspace dari service account).

        Catat ID aturan (`fdrl_...`); Anda akan mengaturnya sebagai `api.wif.federationRuleId`.

        <Note>
          CronJob pembaruan sertifikat harian menggunakan ServiceAccount terpisah (juga diturunkan dari `fullname` Helm) tetapi tidak memanggil Tunnels API; CronJob ini memperbarui sertifikat secara lokal dan hanya memerlukan RBAC Kubernetes, yang diberikan oleh chart. Aturan federasi tidak perlu mencakupnya.
        </Note>
      </Step>

      <Step title="Ambil nilai default">
        ```bash
        helm show values \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 > values.yaml
        ```
      </Step>

      <Step title="Konfigurasikan pelampiran tunnel dan route">
        Edit `values.yaml` dan atur kunci `api.wif.*` dengan ID aturan federasi dan ID organisasi, ditambah entri `routes` untuk setiap [server MCP upstream](/docs/id/agents-and-tools/mcp-tunnels/concepts#components):

        ```yaml values.yaml
        api:
          wif:
            federationRuleId: "fdrl_..."
            organizationId: "00000000-0000-0000-0000-000000000000"
            # Set when the tunnel is in a non-default workspace and the
            # rule's service account is a member of that workspace.
            # workspaceId: "wrkspc_..."

        tunnel:
          # Leave empty to have the setup hook create a tunnel during install.
          # Set to attach to an existing tunnel from the Console.
          id: ""
          # Increment to rotate the tunnel token on the next upgrade.
          # See the "Rotate the tunnel token" section.
          tokenVersion: "1"

        gateway:
          config:
            routes:
              docs: http://docs-mcp.internal:8080
              search: http://search-mcp.internal:8080
        ```

        Dengan route ini, Claude menjangkau server di `docs.<your-tunnel-domain>` dan `search.<your-tunnel-domain>`. Beberapa distribusi Kubernetes terkelola mengalokasikan Service CIDR di luar rentang privat standar; jika route Anda menargetkan Service di dalam cluster, tambahkan `gateway.config.upstream.allowed_ips` di sini sesuai [Validasi IP upstream](/docs/id/agents-and-tools/mcp-tunnels/troubleshooting#upstream-ip-validation).

        <Note>
          Jika Anda menggunakan [server MCP contoh](#optional-use-a-sample-mcp-server), atur `routes` ke `echo: http://hello-mcp:9000` sebagai gantinya.
        </Note>
      </Step>

      <Step title="Tinjau manifest yang dirender">
        Render chart dan tinjau output sesuai dengan praktik pemeriksaan organisasi Anda:

        ```bash
        helm template mcp-tunnel \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 \
          -n mcp-tunnel \
          -f values.yaml > rendered.yaml
        ```
      </Step>

      <Step title="Instal">
        ```bash
        helm install mcp-tunnel \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 \
          --namespace mcp-tunnel --create-namespace \
          -f values.yaml
        ```

        Komponen setup berjalan sebagai Job pre-install hook Helm, sehingga `helm install` memblokir hingga selesai. Jika berhasil, Helm menghapus Job secara otomatis. Jika `helm install` gagal dengan error hook, lihat [Kegagalan autentikasi komponen setup](/docs/id/agents-and-tools/mcp-tunnels/troubleshooting#setup-component-authentication-failures).

        Ketika `tunnel.id` kosong, komponen setup membuat tunnel di workspace yang ditargetkan aturan federasi Anda (workspace default organisasi kecuali Anda mengatur `api.wif.workspaceId`) dan menyimpan ID serta domainnya di Secret `mcp-tunnel`. Temukan domain yang Anda perlukan untuk [verifikasi](#verify-the-deployment) di halaman detail tunnel di Console di bawah **Manage > MCP tunnels**, atau baca dari Secret:

        ```bash
        kubectl -n mcp-tunnel get secret mcp-tunnel \
          -o jsonpath='{.data.tunnel-domain}' | base64 -d
        ```

        Menjalankan ulang komponen setup (selama [upgrade](#upgrades) atau [rotasi token](#rotate-the-tunnel-token)) menggunakan kembali ID tunnel yang disimpan di Secret ini; komponen ini tidak pernah membuat tunnel kedua.

        <Warning>
          Nilai `api.wif.*` adalah pengidentifikasi, bukan secret, jadi menyimpannya di Secret riwayat release Helm bukanlah risiko. Data sensitif yang tersimpan adalah Secret `mcp-tunnel` yang dibuat oleh komponen setup, yang menyimpan token tunnel dan kunci privat TLS. Terapkan praktik standar organisasi Anda untuk melindungi Secret Kubernetes pada namespace ini.
        </Warning>
      </Step>
    </Steps>
  </Tab>

  <Tab title="Tanpa akses programatik">
    Dalam mode ini (`setup.enabled: false`) chart tidak melakukan panggilan API; komponen setup tidak berjalan dan tidak ada CronJob cert-renew. Gunakan jalur ini jika Anda tidak ingin menyiapkan Workload Identity Federation.

    <Steps>
      <Step title="Dapatkan token dan domain tunnel">
        [Buat tunnel](/docs/id/agents-and-tools/mcp-tunnels/console#create-a-tunnel) dan [dapatkan token tunnel dari Console](/docs/id/agents-and-tools/mcp-tunnels/console#get-the-connection-details).

        <Note>
          Catat domain tunnel dari halaman detail. Anda akan mengaturnya sebagai `gateway.config.tunnel_domain`.
        </Note>
      </Step>

      <Step title="Hasilkan CA dan sertifikat server">
        Proxy mendengarkan pada WebSocket biasa, dengan [inner TLS](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) yang dibawa di dalam stream tersebut menggunakan sertifikat yang Anda hasilkan di sini. SAN sertifikat server harus menyertakan `*.<tunnel-domain>` sesuai [persyaratan sertifikat](/docs/id/agents-and-tools/mcp-tunnels/reference#certificate-requirements).

        ```bash
        export TUNNEL_DOMAIN=YOUR_TUNNEL_DOMAIN_HERE
        mkdir -p mcp-tunnel/data
        cd mcp-tunnel

        # CA self-signed. Ekstensi eksplisit agar memenuhi persyaratan
        # sertifikat terlepas dari default openssl.cnf distro.
        openssl req -x509 -newkey rsa:2048 -nodes \
          -keyout data/ca.key -out data/ca.crt \
          -days 3650 -subj "/CN=mcp-tunnel-ca" \
          -addext "basicConstraints=critical,CA:TRUE" \
          -addext "keyUsage=critical,keyCertSign,cRLSign" \
          -addext "subjectKeyIdentifier=hash"

        # File ekstensi untuk sertifikat server. Menggunakan -extfile (alih-alih
        # -copy_extensions, yang hanya ada di OpenSSL 3.0+) agar tetap berfungsi di
        # OpenSSL 1.1.x.
        cat > data/tls.ext <<EOF
        subjectAltName = DNS:${TUNNEL_DOMAIN},DNS:*.${TUNNEL_DOMAIN}
        authorityKeyIdentifier = keyid,issuer
        extendedKeyUsage = serverAuth
        EOF

        # Sertifikat server yang ditandatangani oleh CA
        openssl req -newkey rsa:2048 -nodes \
          -keyout data/tls.key -out /tmp/server.csr \
          -subj "/CN=${TUNNEL_DOMAIN}"
        openssl x509 -req -in /tmp/server.csr \
          -CA data/ca.crt -CAkey data/ca.key -CAcreateserial \
          -out data/tls.crt -days 90 \
          -extfile data/tls.ext
        ```

        [Daftarkan `data/ca.crt` di Console](/docs/id/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate). Simpan `data/ca.key` di tempat yang tahan lama dan aman; Anda akan memerlukannya untuk menandatangani sertifikat server baru saat waktu pembaruan.
      </Step>

      <Step title="Buat dua Secret">
        Chart membaca kunci tertentu; nama Secret dapat dikonfigurasi tetapi kuncinya tidak. Perintah pembuatan namespace berikut tidak berpengaruh jika namespace sudah ada (misalnya, dari langkah [server MCP contoh](#optional-use-a-sample-mcp-server)).

        ```bash
        kubectl create namespace mcp-tunnel --dry-run=client -o yaml | kubectl apply -f -
        kubectl -n mcp-tunnel create secret generic mcp-tunnel-token \
          --from-literal=tunnel-token='eyJ...'
        kubectl -n mcp-tunnel create secret generic mcp-tunnel-cert \
          --from-file=tls.crt=data/tls.crt \
          --from-file=tls.key=data/tls.key
        ```
      </Step>

      <Step title="Ambil nilai default">
        ```bash
        helm show values \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 > values.yaml
        ```
      </Step>

      <Step title="Konfigurasikan nilai untuk provisioning manual">
        Edit `values.yaml` dan atur kunci-kunci berikut:

        ```yaml values.yaml
        setup:
          enabled: false

        external:
          tunnelTokenSecretName: mcp-tunnel-token   # must contain key: tunnel-token
          serverCertSecretName: mcp-tunnel-cert     # must contain keys: tls.crt, tls.key

        gateway:
          config:
            # Required when setup.enabled is false. Replace the placeholder with
            # the $TUNNEL_DOMAIN value you exported earlier. When setup.enabled
            # is true the chart injects this from the Secret as a -tunnel-domain
            # flag instead.
            tunnel_domain: YOUR_TUNNEL_DOMAIN_HERE
            routes:
              docs: http://docs-mcp.internal:8080
              search: http://search-mcp.internal:8080
        ```

        Beberapa distribusi Kubernetes terkelola mengalokasikan Service CIDR di luar rentang privat standar; jika route Anda menargetkan Service di dalam cluster, tambahkan `gateway.config.upstream.allowed_ips` di sini sesuai [Validasi IP upstream](/docs/id/agents-and-tools/mcp-tunnels/troubleshooting#upstream-ip-validation).

        <Note>
          Jika Anda menggunakan [server MCP contoh](#optional-use-a-sample-mcp-server), atur `routes` ke `echo: http://hello-mcp:9000` sebagai gantinya.
        </Note>
      </Step>

      <Step title="Tinjau manifest yang dirender">
        ```bash
        helm template mcp-tunnel \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 \
          -n mcp-tunnel \
          -f values.yaml > rendered.yaml
        ```
      </Step>

      <Step title="Instal">
        ```bash
        helm install mcp-tunnel \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 \
          --namespace mcp-tunnel --create-namespace \
          -f values.yaml
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Verifikasi deployment

Verifikasi secara end-to-end dari sisi Anthropic: gunakan `https://<route>.<your-tunnel-domain>/<path>` dalam sesi Managed Agent atau permintaan Messages API, di mana `<route>` adalah kunci dari `gateway.config.routes` dan `<path>` adalah apa pun yang dilayani oleh server MCP upstream. Dengan [server MCP contoh](#optional-use-a-sample-mcp-server), itu adalah `https://echo.<your-tunnel-domain>/mcp`. Lihat [Gunakan server MCP yang di-tunnel](/docs/id/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers) untuk bentuk permintaannya.

Jika gagal, periksa log pod (`kubectl -n mcp-tunnel logs deploy/mcp-tunnel -c mcp-proxy` dan `-c cloudflared`) dan lihat [Pemecahan Masalah](/docs/id/agents-and-tools/mcp-tunnels/troubleshooting).

## Konfigurasi opsional

### Batasi egress dengan NetworkPolicy

Ingress ke pod proxy ditolak secara default (`networkPolicy.ingress.enabled: true`). Untuk membatasi egress pod lebih lanjut, atur `networkPolicy.egress.enabled: true` dan isi `networkPolicy.egress.mcpServers` dengan selector label pod atau rentang CIDR yang mencakup server MCP upstream Anda. Egress dari cloudflared ke tunnel edge diizinkan secara terpisah melalui `networkPolicy.egress.cloudflaredEgressCIDRs`.

### Sesuaikan proxy

Field di bawah `gateway.config.*` diteruskan ke file konfigurasi proxy. Penyesuaian umum meliputi `upstream.allowed_ips`, `log_level`, dan `upstream.tls`. Lihat referensi [konfigurasi proxy](/docs/id/agents-and-tools/mcp-tunnels/reference#proxy-configuration) untuk daftar field lengkap. Chart selalu mengatur `listen_addr`, `tls.cert_file`, dan `tls.key_file`; mengaturnya di `gateway.config` tidak berpengaruh.

### Sediakan token OIDC Anda sendiri

Secara default chart memproyeksikan token ServiceAccount Kubernetes untuk komponen setup. Untuk menggunakan token dari penyedia identitas yang berbeda (seperti [SPIFFE](/docs/id/manage-claude/wif-providers/spiffe), Vault, atau sidecar cloud-SDK), mount token tersebut dengan `setup.extraVolumes` dan `setup.extraVolumeMounts`. Kemudian arahkan `api.wif.tokenFile` ke path mount tersebut. Chart mengatur `ANTHROPIC_IDENTITY_TOKEN_FILE` ke path tersebut, dan komponen setup membaca token dari sana.

## Upgrade

Selalu berikan `--version` ke `helm upgrade` agar Anda tidak menarik chart yang lebih baru secara tidak terduga.

### Upgrade dari chart 1.x

Chart 2.0.0 memindahkan ID tunnel dari `api.wif.tunnelId` ke `tunnel.id`. Sebelum melakukan upgrade, edit `values.yaml` Anda: pindahkan nilai `tnl_...` ke `tunnel.id` dan hapus `api.wif.tunnelId`. Membiarkan `tunnel.id` tidak diatur adalah aman (komponen setup menggunakan kembali ID tunnel yang sudah disimpan di Secret `mcp-tunnel` saat dijalankan ulang), tetapi pemindahan eksplisit menjaga `values.yaml` Anda tetap akurat. Perbarui juga cakupan aturan federasi Anda dari `org:manage_tunnels` ke `workspace:manage_tunnels` di Console.

### Ubah konfigurasi

Untuk perubahan rutin seperti route, jumlah replika, atau NetworkPolicy:

```bash
helm upgrade mcp-tunnel \
  oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
  --version 2.0.1 \
  -n mcp-tunnel \
  -f values.yaml
```

<Warning>
  Pertahankan `values.yaml` yang lengkap daripada mengandalkan `--reuse-values`. Perilaku deep-merge Helm dapat gagal secara diam-diam dalam menghapus route yang telah dihapus.
</Warning>

### Rotasi token tunnel

Dengan akses programatik, naikkan `tunnel.tokenVersion` di `values.yaml` dan lakukan upgrade dengan `--set setup.force=true`. Komponen setup hanya berjalan ulang saat upgrade jika dipaksa:

```bash
helm upgrade mcp-tunnel \
  oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
  --version 2.0.1 \
  -n mcp-tunnel \
  -f values.yaml \
  --set setup.force=true
```

Komponen setup melakukan autentikasi dengan Workload Identity Federation; tidak ada token API yang perlu dicabut.

Tanpa akses programatik, klik **Rotate token** di halaman detail tunnel di Console, lalu perbarui Secret `mcp-tunnel-token`:

```bash
kubectl -n mcp-tunnel create secret generic mcp-tunnel-token \
  --from-literal=tunnel-token='eyJ...' --dry-run=client -o yaml | kubectl apply -f -
kubectl -n mcp-tunnel rollout restart deploy/mcp-tunnel
```

<Warning>
  Mengklik **Rotate token** langsung membatalkan token saat ini. Hingga Secret diperbarui dan rollout selesai, pod apa pun yang restart dengan token lama (eviction, node drain, OOM) tidak dapat terhubung kembali. Perbarui Secret segera setelah rotasi; untuk persyaratan ketersediaan yang lebih ketat, gunakan akses programatik agar chart menangani rotasi secara atomik.
</Warning>

### Pembaruan sertifikat

Chart menyediakan otomatisasi, tetapi Anda tetap bertanggung jawab untuk memantau kedaluwarsa dan memastikan pembaruan selesai.

Dengan akses programatik, pembaruan sertifikat bersifat otomatis. Chart men-deploy CronJob (dinamai berdasarkan `fullname` Helm, dengan akhiran `-cert-renew`) yang menjalankan `setup renew-cert` setiap hari (pada `serverCert.cronSchedule`, default `0 0 * * *` UTC). Job ini tidak berpengaruh kecuali sertifikat berada dalam rentang `serverCert.renewBefore` dari kedaluwarsa (default 30 hari). Pembaruan bersifat lokal: job menandatangani sertifikat baru dengan CA yang sudah disimpan di Secret, tidak melakukan panggilan API, dan hanya memerlukan RBAC Kubernetes yang diberikan oleh chart. Proxy melakukan hot-reload sertifikat dari mount Secret, sehingga tidak diperlukan restart Deployment.

Tanpa akses programatik tidak ada CronJob. Dari dalam direktori `mcp-tunnel/` yang Anda simpan setelah instalasi, tandatangani sertifikat server baru dengan CA yang sudah ada (jangan menghasilkan ulang CA):

```bash
export TUNNEL_DOMAIN=YOUR_TUNNEL_DOMAIN_HERE
openssl req -new -key data/tls.key -out /tmp/server.csr \
  -subj "/CN=${TUNNEL_DOMAIN}"
openssl x509 -req -in /tmp/server.csr \
  -CA data/ca.crt -CAkey data/ca.key -CAcreateserial \
  -out data/tls.crt -days 90 -extfile data/tls.ext

kubectl -n mcp-tunnel create secret generic mcp-tunnel-cert \
  --from-file=tls.crt=data/tls.crt --from-file=tls.key=data/tls.key \
  --dry-run=client -o yaml | kubectl apply -f -
```

Proxy melakukan hot-reload sertifikat dari mount Secret.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Gunakan server MCP yang di-tunnel" icon="link" href="/docs/id/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers">
    Lampirkan server MCP upstream ke Managed Agent atau Messages API.
  </Card>

  <Card title="Keamanan" icon="lock" href="/docs/id/agents-and-tools/mcp-tunnels/security">
    Panduan hardening, rotasi kredensial, dan respons pelanggaran.
  </Card>

  <Card title="Pemecahan Masalah" icon="wrench" href="/docs/id/agents-and-tools/mcp-tunnels/troubleshooting">
    Diagnosis masalah konektivitas, TLS, dan routing.
  </Card>
</CardGroup>
