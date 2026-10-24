---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: 7d960659238357e7d2440e0059d877fab682490e50eb9293f2bcfbd3248e9ff2
---

---
title: Menerapkan MCP tunnel dengan Docker Compose
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose
description: Instal stack MCP tunnel pada VM menggunakan Docker Compose.
---

<Note>
  MCP tunnels (terowongan MCP) sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/mcp-tunnels) untuk mencobanya.
</Note>

Panduan ini menerapkan [stack tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) sebagai container yang diperkuat (hardened) pada satu host. Konfigurasi yang sama dapat direplikasi di beberapa host untuk ketersediaan.

## Sebelum Anda mulai

Anda memerlukan:

* **Sebuah tunnel.** Dengan akses terprogram, [komponen setup](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) membuatkan tunnel untuk Anda ketika Anda tidak menyediakan ID tunnel; untuk terhubung ke tunnel yang sudah ada, [buat tunnel tersebut di Claude Console](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#create-a-tunnel) dan catat ID tunnel (`tnl_...`). Penyediaan manual selalu dimulai dari tunnel yang dibuat di Console.

* **Cara bagi host untuk mengautentikasi ke Tunnels API.**

  * **Akses terprogram (direkomendasikan).** Aktifkan **Set up programmatic access** saat membuat tunnel agar komponen setup dapat mengautentikasi melalui Workload Identity Federation. Jika Anda membiarkan komponen setup membuat tunnel, buat aturan federasi langsung di halaman [Workload identity](https://platform.claude.com/settings/workload-identity-federation) (`platform.claude.com/settings/workload-identity-federation`) di Claude Console sebagai gantinya. Catat ID aturan federasi (`fdrl_...`) dan ID organisasi Anda.
  * **Manual.** Lewati akses terprogram. Anda akan [mendapatkan token tunnel dari Console](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#get-the-connection-details), membuat CA dan sertifikat server sendiri, dan [mendaftarkan CA di Console](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate).

* **Host dengan Docker dan Docker Compose** yang terinstal. Alur manual juga memerlukan `openssl` (1.1.1 atau lebih baru).

* **Konektivitas jaringan keluar** dari host ke `api.anthropic.com` (443 TCP) dan [tunnel edge](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) (7844 TCP dan UDP). Lihat [persyaratan jaringan](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#network-requirements) selengkapnya.

* **Satu atau lebih server MCP** yang berjalan dan dapat dijangkau dari host pada alamat yang akan Anda konfigurasikan di bawah `routes`. Jika Anda belum memilikinya, [gunakan server contoh](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server).

## Opsional: Gunakan server MCP contoh

Jika Anda tidak memiliki server MCP yang tersedia untuk pengujian, gunakan server minimal ini:

```bash
mkdir -p mcp-tunnel
cat > mcp-tunnel/hello_server.py <<'EOF'
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hello-server", host="0.0.0.0", port=9000)


@mcp.tool()
def hello(name: str = "world") -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
EOF
```

Langkah-langkah Instal berikut melakukan `cd` ke `mcp-tunnel/` dan mencatat di mana harus menambahkan service dan route yang sesuai.

## Instal

Panduan ini menyediakan satu pendekatan referensi menggunakan Docker Compose. Anda bertanggung jawab untuk menyesuaikannya agar memenuhi persyaratan keamanan organisasi Anda.

<Tabs>
  <Tab title="Dengan akses terprogram">
    Jalur ini mengharuskan host memiliki penyedia identitas OIDC (seperti server metadata VM cloud atau SPIFFE). Jika tidak, gunakan tab **Tanpa akses terprogram** sebagai gantinya.

    Komponen setup menggunakan Workload Identity Federation untuk mengambil token tunnel, membuat CA dan sertifikat server, serta mendaftarkan CA ke Anthropic.

    <Steps>
      <Step title="Siapkan direktori deployment">
        ```bash
        mkdir -p mcp-tunnel/{config,data}
        cd mcp-tunnel
        sudo chown 65532:65532 data
        ```

        Container berjalan sebagai UID non-root `65532` dan memerlukan akses tulis ke `data/`.
      </Step>

      <Step title="Tulis docker-compose.yaml">
        File compose menyematkan image berdasarkan digest SHA-256, menjalankan setiap container sebagai non-root dengan sistem file read-only, menghapus semua kapabilitas Linux, dan menonaktifkan eskalasi hak istimewa.

        ```bash
        cat > docker-compose.yaml <<'EOF'
        services:
          setup:
            image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:d243d30642d39857a0579e465cb3b9bf3ae7c1141e83143bb6856777a31467a5
            entrypoint: ["/setup"]
            command:
              - init
              - --api-url=https://api.anthropic.com
              - --output=dir:/data
              - --token-version=1
            environment:
              - TUNNEL_ID
              - ANTHROPIC_FEDERATION_RULE_ID
              - ANTHROPIC_ORGANIZATION_ID
              - ANTHROPIC_WORKSPACE_ID
              - ANTHROPIC_IDENTITY_TOKEN
            volumes:
              - ./data:/data
            user: "65532:65532"
            read_only: true
            security_opt:
              - no-new-privileges:true
            cap_drop:
              - ALL
            profiles: ["setup"]

          cloudflared:
            image: cloudflare/cloudflared@sha256:0e56c13c7058fcef9c4f0e7d83372f82330548dbf8f8b366f3d8b506526d93b2
            command: tunnel --no-autoupdate run --url http://localhost:8080
            environment:
              - TUNNEL_TOKEN
            # Bagikan netns milik proxy agar localhost:8080 dapat menjangkaunya.
            network_mode: "service:mcp-proxy"
            restart: unless-stopped
            user: "65532:65532"
            read_only: true
            security_opt:
              - no-new-privileges:true
            cap_drop:
              - ALL
            stop_grace_period: 30s
            logging:
              options:
                max-size: "10m"
                max-file: "3"

          mcp-proxy:
            image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:d243d30642d39857a0579e465cb3b9bf3ae7c1141e83143bb6856777a31467a5
            volumes:
              - ./config/mcp-proxy.yaml:/etc/mcp-gateway/config.yaml:ro
              - ./data:/data:ro
            restart: unless-stopped
            user: "65532:65532"
            read_only: true
            security_opt:
              - no-new-privileges:true
            cap_drop:
              - ALL
            stop_grace_period: 30s
            logging:
              options:
                max-size: "10m"
                max-file: "3"
        EOF
        ```

        Jika Anda menggunakan [server MCP contoh](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server), tambahkan sebagai service:

        ```bash
        cat >> docker-compose.yaml <<'EOF'

          hello-mcp:
            image: python:3.13-slim
            working_dir: /app
            volumes:
              - ./hello_server.py:/app/hello_server.py:ro
            command: sh -c "pip install --quiet mcp && python hello_server.py"
            restart: unless-stopped
        EOF
        ```
      </Step>

      <Step title="Sediakan tunnel">
        Atur pengidentifikasi. Biarkan `TUNNEL_ID` tidak diatur agar komponen setup membuat tunnel; atur untuk menghubungkan ke tunnel yang sudah ada dari [Console](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#create-a-tunnel):

        ```bash
        # export TUNNEL_ID=tnl_...   # atur untuk terhubung ke tunnel yang sudah ada
        export ANTHROPIC_FEDERATION_RULE_ID=fdrl_...
        export ANTHROPIC_ORGANIZATION_ID=00000000-0000-0000-0000-000000000000
        ```

        Jika aturan federasi Anda dibatasi pada workspace selain workspace default organisasi Anda, atur juga `ANTHROPIC_WORKSPACE_ID=wrkspc_...`; jika tidak, komponen setup menggunakan workspace default. Tunnel yang dibuat otomatis akan dibuat di workspace tersebut.

        Atur `ANTHROPIC_IDENTITY_TOKEN` ke JWT OIDC dari penyedia identitas host ini. Ikuti [panduan WIF untuk penyedia Anda](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#identity-providers) untuk mendaftarkan issuer, mengatur subject aturan, dan membuat token; audience aturan harus cocok dengan audience yang Anda minta saat membuat token.

        Jalankan komponen setup:

        ```bash
        docker compose run --rm setup
        ```

        `setup init` bersifat idempoten terhadap `data/`: menjalankannya ulang akan menggunakan kembali ID tunnel dan CA yang sudah tersimpan di sana dan tidak pernah membuat tunnel kedua. CA baru dibuat dan didaftarkan hanya ketika `data/` kosong atau `TUNNEL_ID` telah berubah; dalam kasus tersebut batas dua sertifikat aktif berlaku, jadi cabut salah satunya di Console terlebih dahulu jika kedua slot sudah terisi.

        Lihat [Kegagalan autentikasi komponen setup](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/troubleshooting#setup-component-authentication-failures) jika terjadi error.

        Ambil domain tunnel Anda dan ekspor untuk langkah-langkah selanjutnya:

        ```bash
        export TUNNEL_DOMAIN=$(sudo cat data/tunnel-domain)
        echo "$TUNNEL_DOMAIN"
        ```

        <Note>
          Token Workload Identity Federation berumur pendek (1 jam secara default) dan kedaluwarsa secara otomatis; tidak ada yang perlu dicabut setelah setup selesai.
        </Note>
      </Step>

      <Step title="Tulis konfigurasi proxy">
        `tunnel_domain` **wajib**: [proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) menggunakannya untuk menghapus sufiks domain dari hostname yang masuk sebelum mencari subdomain di `routes`. `routes` adalah map datar dari subdomain ke URL upstream, bukan list.

        ```bash
        cat > config/mcp-proxy.yaml <<EOF
        listen_addr: ":8080"
        log_level: info
        shutdown_timeout: 30s
        tunnel_domain: ${TUNNEL_DOMAIN}
        tls:
          cert_file: /data/tls.crt
          key_file: /data/tls.key
        routes:
          echo: http://hello-mcp:9000
        EOF
        ```

        Route `echo:` menargetkan [server MCP contoh](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server); ganti dengan (atau tambahkan) route Anda sendiri. Lihat referensi [konfigurasi proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#proxy-configuration) untuk semua field yang tersedia.
      </Step>

      <Step title="Mulai deployment">
        ```bash
        export TUNNEL_TOKEN=$(sudo cat data/tunnel-token)
        docker compose up -d
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Tanpa akses terprogram">
    Gunakan alur ini jika Anda tidak mengaktifkan **Set up programmatic access**, atau untuk pengembangan dan pengujian lokal. Tidak ada service `setup`.

    <Steps>
      <Step title="Dapatkan token dan domain tunnel dari Console">
        Di halaman detail tunnel, salin **Domain** (berbentuk `abcd1234.tunnel.anthropic.com`), lalu klik ikon mata di samping **Token** untuk mengambil token tunnel dan gunakan ikon salin untuk menyalinnya.

        Atur keduanya sebagai variabel shell untuk sisa panduan ini:

        ```bash
        export TUNNEL_DOMAIN=YOUR_TUNNEL_DOMAIN_HERE
        export TUNNEL_TOKEN='eyJ...'
        ```
      </Step>

      <Step title="Buat kerangka dan hasilkan sertifikat">
        ```bash
        mkdir -p mcp-tunnel/{data,config}
        cd mcp-tunnel
        ```

        Proxy mendengarkan di `:8080` melalui WebSocket biasa; handshake [TLS dalam](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) terjadi **di dalam** stream WebSocket tersebut menggunakan sertifikat ini. Anthropic memverifikasi handshake dalam terhadap CA yang Anda daftarkan di Console. Subject Alternative Name (SAN) sertifikat server harus mencakup `*.<tunnel-domain>` seperti yang dijelaskan dalam [persyaratan sertifikat](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#certificate-requirements).

        ```bash
        # CA yang ditandatangani sendiri. Ekstensi eksplisit agar memenuhi persyaratan
        # sertifikat terlepas dari default openssl.cnf pada distro.
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

        # Izinkan container proxy non-root (UID 65532) membaca kunci dari
        # bind mount. Tanpa bit world-read, container tidak dapat membuka
        # file milik host.
        chmod 644 data/tls.key
        ```
      </Step>

      <Step title="Daftarkan sertifikat CA di Console">
        Di halaman detail tunnel, gulir ke bagian **Certificates** dan klik **Add certificate**. Unggah `data/ca.crt` secara langsung dengan **Choose file** (jendela modal menerima `.pem`, `.crt`, dan `.cer`), atau tempelkan isinya:

        ```bash
        cat data/ca.crt
        ```

        Badge **Needs certificate** di samping nama tunnel akan hilang setelah sertifikat didaftarkan. Lihat [Menambahkan sertifikat CA](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate).
      </Step>

      <Step title="Tulis konfigurasi proxy">
        `tunnel_domain` **wajib**: proxy menggunakannya untuk menghapus sufiks domain dari hostname yang masuk sebelum mencari subdomain di `routes`. `routes` adalah map datar dari subdomain ke URL upstream, bukan list.

        ```bash
        cat > config/mcp-proxy.yaml <<EOF
        listen_addr: ":8080"
        log_level: info
        tunnel_domain: ${TUNNEL_DOMAIN}
        tls:
          cert_file: /data/tls.crt
          key_file: /data/tls.key
        routes:
          echo: http://hello-mcp:9000
        EOF
        ```

        Route `echo:` menargetkan [server MCP contoh](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server); ganti dengan (atau tambahkan) route Anda sendiri. Lihat referensi [konfigurasi proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#proxy-configuration) untuk semua field yang tersedia.
      </Step>

      <Step title="Tulis docker-compose.yaml">
        Pengaturan `network_mode: "service:mcp-proxy"` menempatkan [cloudflared](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) di namespace jaringan proxy sehingga `localhost:8080` di dalam container cloudflared menjangkau proxy. Flag `--url http://localhost:8080` memberikan target penerusan kepada cloudflared; tanpa flag tersebut, cloudflared tidak memiliki route untuk permintaan masuk dan mengembalikan 503.

        ```bash
        cat > docker-compose.yaml <<'EOF'
        services:
          cloudflared:
            image: cloudflare/cloudflared@sha256:0e56c13c7058fcef9c4f0e7d83372f82330548dbf8f8b366f3d8b506526d93b2
            # --url wajib diisi: tidak ada aturan ingress yang dikirim dalam alur manual,
            # sehingga tanpanya cloudflared mengembalikan 503 untuk setiap permintaan.
            command: tunnel --no-autoupdate run --url http://localhost:8080
            environment:
              - TUNNEL_TOKEN
            # Bagikan netns milik proxy agar localhost:8080 dapat menjangkaunya.
            network_mode: "service:mcp-proxy"
            restart: unless-stopped
            user: "65532:65532"
            read_only: true
            security_opt:
              - no-new-privileges:true
            cap_drop:
              - ALL
            stop_grace_period: 30s
            logging:
              options:
                max-size: "10m"
                max-file: "3"

          mcp-proxy:
            image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:d243d30642d39857a0579e465cb3b9bf3ae7c1141e83143bb6856777a31467a5
            volumes:
              - ./config/mcp-proxy.yaml:/etc/mcp-gateway/config.yaml:ro
              - ./data:/data:ro
            restart: unless-stopped
            user: "65532:65532"
            read_only: true
            security_opt:
              - no-new-privileges:true
            cap_drop:
              - ALL
            stop_grace_period: 30s
            logging:
              options:
                max-size: "10m"
                max-file: "3"
        EOF
        ```

        Jika Anda menggunakan [server MCP contoh](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server), tambahkan sebagai service:

        ```bash
        cat >> docker-compose.yaml <<'EOF'

          hello-mcp:
            image: python:3.13-slim
            working_dir: /app
            volumes:
              - ./hello_server.py:/app/hello_server.py:ro
            command: sh -c "pip install --quiet mcp && python hello_server.py"
            restart: unless-stopped
        EOF
        ```
      </Step>

      <Step title="Mulai deployment">
        ```bash
        docker compose up -d
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

File compose membaca `TUNNEL_TOKEN` dari lingkungan host tanpa nilai default, jadi Anda harus mengulangi export di setiap shell baru dan setelah reboot.

Untuk deployment multi-VM, salin direktori `mcp-tunnel/` ke setiap host, atur `TUNNEL_TOKEN`, dan jalankan `docker compose up -d`. Dalam alur terprogram, `TUNNEL_TOKEN` adalah `$(sudo cat data/tunnel-token)`; dalam alur manual, nilainya adalah yang Anda salin dari Console. Token tunnel dan sertifikat yang sama berfungsi di semua replika.

## Verifikasi deployment

Verifikasi secara end-to-end dengan memanggil [server MCP upstream](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) dari sisi Anthropic: lihat [Menggunakan server MCP yang di-tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers). Dengan [server MCP contoh](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server), URL yang dirutekan adalah `https://echo.<your-tunnel-domain>/mcp`. Jika verifikasi gagal, lihat [Pemecahan masalah](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/troubleshooting).

## Pembaruan

Jalankan perintah di bagian ini dari dalam direktori deployment `mcp-tunnel/`.

### Merotasi token tunnel

Dengan akses terprogram, naikkan `--token-version` di perintah service `setup`, atur pengidentifikasi Workload Identity Federation, buat JWT OIDC baru, dan jalankan ulang komponen setup:

```bash
# Edit docker-compose.yaml: naikkan bilangan bulat pada argumen layanan setup
# --token-version (misalnya, --token-version=1 menjadi
# --token-version=2). Biner setup menolak melakukan rotasi jika nilainya
# tidak berubah.

# export TUNNEL_ID=tnl_...   # atur hanya jika Anda mengaturnya saat instalasi
export ANTHROPIC_FEDERATION_RULE_ID=fdrl_...
export ANTHROPIC_ORGANIZATION_ID=00000000-0000-0000-0000-000000000000
# export ANTHROPIC_WORKSPACE_ID=wrkspc_...   # jika aturan Anda berlingkup workspace
# Buat ulang ANTHROPIC_IDENTITY_TOKEN sesuai panduan penyedia WIF untuk
# lingkungan Anda (token tersebut sudah kedaluwarsa sejak instalasi).
export ANTHROPIC_IDENTITY_TOKEN=...

docker compose run --rm setup

export TUNNEL_TOKEN=$(sudo cat data/tunnel-token)
docker compose up -d cloudflared
```

Argumen `--token-version` diedit di `docker-compose.yaml` alih-alih diteruskan di baris perintah agar nilai baru tetap tersimpan untuk eksekusi komponen setup berikutnya. Komponen setup mengautentikasi dengan Workload Identity Federation; tidak ada token API yang perlu dicabut.

Tanpa akses terprogram, klik **Rotate token** di halaman detail tunnel di Console, lalu perbarui variabel environment `TUNNEL_TOKEN` di setiap host dan restart cloudflared (`docker compose up -d cloudflared`).

<Warning>
  Mengklik **Rotate token** langsung membatalkan token saat ini. Antara saat itu dan pembaruan `TUNNEL_TOKEN` di setiap host serta restart cloudflared, host mana pun yang cloudflared-nya restart (crash, reboot host) tidak dapat terhubung kembali. Perbarui setiap host segera setelah merotasi.
</Warning>

### Pembaruan sertifikat

Anda bertanggung jawab untuk memantau masa berlaku dan memperbarui sertifikat server sebelum kedaluwarsa.

Dengan akses terprogram:

```bash
docker compose run --rm setup renew-cert --output=dir:/data
```

Argumen CLI menggantikan `command` service `setup` (argumen `init`) tetapi mempertahankan `entrypoint`-nya, sehingga ini menjalankan `/setup renew-cert --output=dir:/data`.

<Tip>
  Teruskan `--renew-before=720h` agar perintah tidak melakukan apa pun ketika masa berlaku yang tersisa lebih dari 30 hari. Ini membuatnya aman untuk dijalankan sesuai jadwal tetap.
</Tip>

Tanpa akses terprogram, tandatangani sertifikat server baru dengan CA Anda yang sudah ada (CA yang terdaftar di Console tidak berubah) dan ganti `data/tls.crt`. Atur `TUNNEL_DOMAIN` terlebih dahulu jika Anda menjalankan ini dari shell baru.

```bash
export TUNNEL_DOMAIN=YOUR_TUNNEL_DOMAIN_HERE
openssl req -new -key data/tls.key -out /tmp/server.csr \
  -subj "/CN=${TUNNEL_DOMAIN}"
openssl x509 -req -in /tmp/server.csr \
  -CA data/ca.crt -CAkey data/ca.key -CAcreateserial \
  -out data/tls.crt -days 90 \
  -extfile data/tls.ext
```

Dalam kedua alur, proxy melakukan polling terhadap `tls.cert_file` dan memuatnya ulang secara otomatis, sehingga tidak diperlukan restart.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Menggunakan server MCP yang di-tunnel" icon="link" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers">
    Hubungkan server MCP upstream ke Managed Agent atau Messages API.
  </Card>

  <Card title="Keamanan" icon="lock" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/security">
    Panduan hardening, rotasi kredensial, dan respons terhadap pelanggaran.
  </Card>

  <Card title="Pemecahan masalah" icon="wrench" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/troubleshooting">
    Diagnosis masalah konektivitas, TLS, dan routing.
  </Card>
</CardGroup>
