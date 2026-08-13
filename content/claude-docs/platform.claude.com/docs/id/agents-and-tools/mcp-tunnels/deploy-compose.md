---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: d3a524f1d1db794225cc7baadb2a3e45ad1ae6afba5d5d729a8ae86c3d41f077
---

---
title: Men-deploy MCP tunnel dengan Docker Compose
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose
description: Instal tunnel stack MCP pada VM menggunakan Docker Compose.
---

<Note>
  Tunnel MCP sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Note>

Panduan ini men-deploy [tunnel stack](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) sebagai container yang diperkuat (hardened) pada satu host. Konfigurasi yang sama dapat direplikasi di beberapa host untuk ketersediaan (availability).

## Sebelum Anda mulai

Anda memerlukan:

* **Sebuah tunnel.** Dengan akses programatik, [komponen setup](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) akan membuatkan satu untuk Anda jika Anda tidak menyediakan tunnel ID; untuk menghubungkan ke tunnel yang sudah ada, [buat tunnel di Console](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#create-a-tunnel) dan catat tunnel ID (`tnl_...`). Penyediaan manual selalu dimulai dari tunnel yang dibuat di Console.

* **Cara bagi host untuk mengautentikasi ke Tunnels API.**

  * **Akses programatik (direkomendasikan).** Aktifkan **Set up programmatic access** saat membuat tunnel (atau buat federation rule secara langsung di **Settings > Workload identity** jika Anda membiarkan komponen setup membuat tunnel) sehingga komponen setup dapat mengautentikasi melalui Workload Identity Federation. Catat federation rule ID (`fdrl_...`) dan organization ID Anda.
  * **Manual.** Lewati akses programatik. Anda akan [mendapatkan tunnel token dari Console](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#get-the-connection-details), membuat CA dan sertifikat server sendiri, dan [mendaftarkan CA di Console](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate).

* **Host dengan Docker dan Docker Compose** terinstal. Alur manual juga memerlukan `openssl` (1.1.1 atau lebih baru).

* **Konektivitas jaringan keluar** dari host ke `api.anthropic.com` (443 TCP) dan [tunnel edge](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) (7844 TCP dan UDP). Lihat [persyaratan jaringan](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#network-requirements) lengkap.

* **Satu atau lebih server MCP** yang berjalan dan dapat dijangkau dari host pada alamat yang akan Anda konfigurasikan di bawah `routes`. Jika Anda belum memilikinya, [gunakan server sampel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server).

## Opsional: Gunakan server MCP sampel

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
  <Tab title="Dengan akses programatik">
    Jalur ini mengharuskan host memiliki penyedia identitas OIDC (seperti metadata server VM cloud atau SPIFFE). Jika tidak ada, gunakan tab **Tanpa akses programatik** sebagai gantinya.

    Komponen setup menggunakan Workload Identity Federation untuk mengambil tunnel token, membuat CA dan sertifikat server, serta mendaftarkan CA ke Anthropic.

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
        File compose ini mengunci (pin) image berdasarkan digest SHA-256, menjalankan setiap container sebagai non-root dengan filesystem read-only, menghapus semua Linux capabilities, dan menonaktifkan eskalasi privilege.

        ```bash
        cat > docker-compose.yaml <<'EOF'
        services:
          setup:
            image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:efb27b299d627e4134815663cb8896641eeaee025d734c0f695582b4df38f013
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
            image: cloudflare/cloudflared@sha256:6b599ca3e974349ead3286d178da61d291961182ec3fe9c505e1dd02c8ac31b0
            command: tunnel --no-autoupdate run --url http://localhost:8080
            environment:
              - TUNNEL_TOKEN
            # Bagikan netns proxy agar localhost:8080 dapat menjangkaunya.
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
            image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:efb27b299d627e4134815663cb8896641eeaee025d734c0f695582b4df38f013
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

        Jika Anda menggunakan [server MCP sampel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server), tambahkan sebagai service:

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
        Atur identifier. Biarkan `TUNNEL_ID` tidak diatur agar komponen setup membuat tunnel; atur nilainya untuk menghubungkan ke tunnel yang sudah ada dari [Console](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#create-a-tunnel):

        ```bash
        # export TUNNEL_ID=tnl_...   # atur untuk terhubung ke tunnel yang sudah ada
        export ANTHROPIC_FEDERATION_RULE_ID=fdrl_...
        export ANTHROPIC_ORGANIZATION_ID=00000000-0000-0000-0000-000000000000
        ```

        Jika federation rule Anda dibatasi ke workspace selain default organisasi Anda, atur juga `ANTHROPIC_WORKSPACE_ID=wrkspc_...`; komponen setup menggunakan workspace default jika tidak diatur. Tunnel yang dibuat otomatis akan dibuat di workspace tersebut.

        Atur `ANTHROPIC_IDENTITY_TOKEN` ke JWT OIDC dari penyedia identitas host ini. Ikuti [panduan WIF untuk penyedia Anda](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#identity-providers) untuk mendaftarkan issuer, mengatur subject pada rule, dan membuat token; audience pada rule harus cocok dengan audience yang Anda minta saat membuat token.

        Jalankan komponen setup:

        ```bash
        docker compose run --rm setup
        ```

        `setup init` bersifat idempoten terhadap `data/`: menjalankannya kembali akan menggunakan ulang tunnel ID dan CA yang sudah tersimpan di sana dan tidak pernah membuat tunnel kedua. CA baru dibuat dan didaftarkan hanya ketika `data/` kosong atau `TUNNEL_ID` telah berubah; dalam kasus tersebut batas maksimal dua sertifikat aktif berlaku, jadi cabut (revoke) salah satunya di Console terlebih dahulu jika kedua slot sudah terisi.

        Lihat [Kegagalan autentikasi komponen setup](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/troubleshooting#setup-component-authentication-failures) jika terjadi error.

        Ambil tunnel domain Anda dan ekspor untuk langkah-langkah selanjutnya:

        ```bash
        export TUNNEL_DOMAIN=$(sudo cat data/tunnel-domain)
        echo "$TUNNEL_DOMAIN"
        ```

        <Note>
          Token Workload Identity Federation berumur pendek (1 jam secara default) dan kedaluwarsa secara otomatis; tidak ada yang perlu dicabut setelah setup selesai.
        </Note>
      </Step>

      <Step title="Tulis konfigurasi proxy">
        `tunnel_domain` bersifat **wajib**: [proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) menggunakannya untuk menghapus sufiks domain dari hostname yang masuk sebelum mencari subdomain di `routes`. `routes` adalah map datar dari subdomain ke URL upstream, bukan sebuah list.

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

        Route `echo:` menargetkan [server MCP sampel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server); ganti dengan (atau tambahkan) route Anda sendiri. Lihat referensi [konfigurasi proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#proxy-configuration) untuk semua field yang tersedia.
      </Step>

      <Step title="Mulai deployment">
        ```bash
        export TUNNEL_TOKEN=$(sudo cat data/tunnel-token)
        docker compose up -d
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Tanpa akses programatik">
    Gunakan alur ini jika Anda tidak mengaktifkan **Set up programmatic access**, atau untuk pengembangan dan pengujian lokal. Tidak ada service `setup`.

    <Steps>
      <Step title="Dapatkan tunnel token dan domain dari Console">
        Pada halaman detail tunnel, salin **Domain** (bentuknya `abcd1234.tunnel.anthropic.com`), lalu klik ikon mata di samping **Token** untuk mengambil tunnel token dan gunakan ikon salin untuk menyalinnya.

        Atur keduanya sebagai variabel shell untuk sisa panduan ini:

        ```bash
        export TUNNEL_DOMAIN=YOUR_TUNNEL_DOMAIN_HERE
        export TUNNEL_TOKEN='eyJ...'
        ```
      </Step>

      <Step title="Buat scaffold dan hasilkan sertifikat">
        ```bash
        mkdir -p mcp-tunnel/{data,config}
        cd mcp-tunnel
        ```

        Proxy mendengarkan pada `:8080` melalui WebSocket biasa; handshake [inner TLS](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) terjadi **di dalam** stream WebSocket tersebut menggunakan sertifikat ini. Anthropic memverifikasi inner handshake terhadap CA yang Anda daftarkan di Console. Subject Alternative Name (SAN) pada sertifikat server harus menyertakan `*.<tunnel-domain>` sesuai [persyaratan sertifikat](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#certificate-requirements).

        ```bash
        # CA yang ditandatangani sendiri. Ekstensi eksplisit agar memenuhi persyaratan
        # sertifikat terlepas dari default openssl.cnf distro.
        openssl req -x509 -newkey rsa:2048 -nodes \
          -keyout data/ca.key -out data/ca.crt \
          -days 3650 -subj "/CN=mcp-tunnel-ca" \
          -addext "basicConstraints=critical,CA:TRUE" \
          -addext "keyUsage=critical,keyCertSign,cRLSign" \
          -addext "subjectKeyIdentifier=hash"

        # File ekstensi untuk sertifikat server. Menggunakan -extfile (alih-alih
        # -copy_extensions, yang hanya ada di OpenSSL 3.0+) membuat ini tetap berfungsi
        # pada OpenSSL 1.1.x.
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

        # Izinkan kontainer proxy non-root (UID 65532) membaca kunci dari
        # bind mount. Tanpa bit world-read, kontainer tidak dapat membuka
        # file yang dimiliki host.
        chmod 644 data/tls.key
        ```
      </Step>

      <Step title="Daftarkan sertifikat CA di Console">
        Pada halaman detail tunnel, gulir ke bagian **Certificates** dan klik **Add certificate**. Unggah `data/ca.crt` secara langsung dengan **Choose file** (modal menerima `.pem`, `.crt`, dan `.cer`), atau tempel isinya:

        ```bash
        cat data/ca.crt
        ```

        Status tunnel berubah menjadi **Active** setelah sertifikat didaftarkan. Lihat [Menambahkan sertifikat CA](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate).
      </Step>

      <Step title="Tulis konfigurasi proxy">
        `tunnel_domain` bersifat **wajib**: proxy menggunakannya untuk menghapus sufiks domain dari hostname yang masuk sebelum mencari subdomain di `routes`. `routes` adalah map datar dari subdomain ke URL upstream, bukan sebuah list.

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

        Route `echo:` menargetkan [server MCP sampel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server); ganti dengan (atau tambahkan) route Anda sendiri. Lihat referensi [konfigurasi proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#proxy-configuration) untuk semua field yang tersedia.
      </Step>

      <Step title="Tulis docker-compose.yaml">
        Pengaturan `network_mode: "service:mcp-proxy"` menempatkan [cloudflared](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) di network namespace milik proxy sehingga `localhost:8080` di dalam container cloudflared menjangkau proxy. Flag `--url http://localhost:8080` memberikan target penerusan kepada cloudflared; tanpa flag tersebut, cloudflared tidak memiliki route untuk permintaan masuk dan mengembalikan 503.

        ```bash
        cat > docker-compose.yaml <<'EOF'
        services:
          cloudflared:
            image: cloudflare/cloudflared@sha256:6b599ca3e974349ead3286d178da61d291961182ec3fe9c505e1dd02c8ac31b0
            # --url wajib diisi: tidak ada aturan ingress yang di-push pada alur manual,
            # jadi tanpanya cloudflared mengembalikan 503 untuk setiap permintaan.
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
            image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:efb27b299d627e4134815663cb8896641eeaee025d734c0f695582b4df38f013
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

        Jika Anda menggunakan [server MCP sampel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server), tambahkan sebagai service:

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

File compose membaca `TUNNEL_TOKEN` dari environment host tanpa nilai default, sehingga ekspor harus diulang di setiap shell baru dan setelah reboot.

Untuk deployment multi-VM, salin direktori `mcp-tunnel/` ke setiap host, atur `TUNNEL_TOKEN`, dan jalankan `docker compose up -d`. Dalam alur programatik, `TUNNEL_TOKEN` adalah `$(sudo cat data/tunnel-token)`; dalam alur manual, nilainya adalah yang Anda salin dari Console. Tunnel token dan sertifikat yang sama berfungsi di semua replika.

## Verifikasi deployment

Verifikasi secara end-to-end dengan memanggil [server MCP upstream](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) dari sisi Anthropic: lihat [Menggunakan server MCP yang di-tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers). Dengan [server MCP sampel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose#optional-use-a-sample-mcp-server), URL yang di-route adalah `https://echo.<your-tunnel-domain>/mcp`. Jika verifikasi gagal, lihat [Pemecahan Masalah](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/troubleshooting).

## Upgrade

Jalankan perintah di bagian ini dari dalam direktori deployment `mcp-tunnel/`.

### Merotasi tunnel token

Dengan akses programatik, naikkan `--token-version` pada command service `setup`, atur identifier Workload Identity Federation, buat JWT OIDC baru, dan jalankan kembali komponen setup:

```bash
# Edit docker-compose.yaml: naikkan nilai integer pada argumen --token-version
# di layanan setup (misalnya, --token-version=1 menjadi
# --token-version=2). Biner setup menolak melakukan rotasi jika nilainya
# tidak berubah.

# export TUNNEL_ID=tnl_...   # atur hanya jika Anda mengaturnya saat instalasi
export ANTHROPIC_FEDERATION_RULE_ID=fdrl_...
export ANTHROPIC_ORGANIZATION_ID=00000000-0000-0000-0000-000000000000
# export ANTHROPIC_WORKSPACE_ID=wrkspc_...   # jika aturan Anda dibatasi pada workspace
# Buat ulang ANTHROPIC_IDENTITY_TOKEN sesuai panduan penyedia WIF untuk
# lingkungan Anda (token tersebut sudah kedaluwarsa sejak instalasi).
export ANTHROPIC_IDENTITY_TOKEN=...

docker compose run --rm setup

export TUNNEL_TOKEN=$(sudo cat data/tunnel-token)
docker compose up -d cloudflared
```

Argumen `--token-version` diedit di `docker-compose.yaml` alih-alih diteruskan pada command line agar nilai baru tetap tersimpan untuk eksekusi komponen setup berikutnya. Komponen setup mengautentikasi dengan Workload Identity Federation; tidak ada token API yang perlu dicabut.

Tanpa akses programatik, klik **Rotate token** pada halaman detail tunnel di Console, lalu perbarui variabel environment `TUNNEL_TOKEN` pada setiap host dan restart cloudflared (`docker compose up -d cloudflared`).

<Warning>
  Mengklik **Rotate token** langsung membatalkan token saat ini. Antara momen tersebut dan pembaruan `TUNNEL_TOKEN` pada setiap host serta restart cloudflared, host mana pun yang cloudflared-nya restart (crash, reboot host) tidak dapat terhubung kembali. Perbarui setiap host segera setelah merotasi.
</Warning>

### Pembaruan sertifikat

Anda bertanggung jawab untuk memantau masa berlaku dan memperbarui sertifikat server sebelum kedaluwarsa.

Dengan akses programatik:

```bash
docker compose run --rm setup renew-cert --output=dir:/data
```

Argumen CLI menggantikan `command` service `setup` (argumen `init`) tetapi mempertahankan `entrypoint`-nya, sehingga ini menjalankan `/setup renew-cert --output=dir:/data`.

<Tip>
  Teruskan `--renew-before=720h` agar perintah menjadi no-op ketika masa berlaku yang tersisa lebih dari 30 hari. Ini membuatnya aman untuk dijalankan pada jadwal tetap.
</Tip>

Tanpa akses programatik, tanda tangani sertifikat server baru dengan CA Anda yang sudah ada (CA yang terdaftar di Console tidak berubah) dan ganti `data/tls.crt`. Atur `TUNNEL_DOMAIN` terlebih dahulu jika Anda menjalankan ini dari shell baru.

```bash
export TUNNEL_DOMAIN=YOUR_TUNNEL_DOMAIN_HERE
openssl req -new -key data/tls.key -out /tmp/server.csr \
  -subj "/CN=${TUNNEL_DOMAIN}"
openssl x509 -req -in /tmp/server.csr \
  -CA data/ca.crt -CAkey data/ca.key -CAcreateserial \
  -out data/tls.crt -days 90 \
  -extfile data/tls.ext
```

Dalam kedua alur, proxy melakukan polling terhadap `tls.cert_file` dan memuat ulang secara otomatis, sehingga tidak diperlukan restart.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Menggunakan server MCP yang di-tunnel" icon="link" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers">
    Hubungkan server MCP upstream ke Managed Agent atau Messages API.
  </Card>

  <Card title="Keamanan" icon="lock" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/security">
    Panduan hardening, rotasi kredensial, dan respons terhadap pelanggaran keamanan.
  </Card>

  <Card title="Pemecahan Masalah" icon="wrench" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/troubleshooting">
    Diagnosis masalah konektivitas, TLS, dan routing.
  </Card>
</CardGroup>
