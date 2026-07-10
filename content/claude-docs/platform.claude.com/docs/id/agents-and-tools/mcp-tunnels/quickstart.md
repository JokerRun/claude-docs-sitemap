---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/quickstart
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: 731fe78119cd02a50491dbf0cf4d2c354c74404b492d3decc3b6ba8d64b719a6
---

# Quickstart tunnel MCP

Hubungkan Claude ke server MCP privat menggunakan deployment Docker Compose lokal.

---

<Note>
  Tunnel MCP sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Note>

Quickstart ini membawa Anda dari nol hingga Claude memanggil server MCP privat melalui tunnel. Quickstart ini menggunakan Docker Compose dengan provisioning kredensial [manual](/docs/id/agents-and-tools/mcp-tunnels/concepts#credential-provisioning), yang merupakan jalur terpendek untuk pengujian lokal. Untuk deployment produksi, lihat [Deploy dengan Helm](/docs/id/agents-and-tools/mcp-tunnels/deploy-helm) atau [Deploy dengan Docker Compose](/docs/id/agents-and-tools/mcp-tunnels/deploy-compose).

## Apa yang akan Anda bangun

Sebuah [tunnel stack](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) dua kontainer ([proxy](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) dan [cloudflared](/docs/id/agents-and-tools/mcp-tunnels/concepts#components)) ditambah sebuah server MCP contoh yang berjalan bersamanya. Ketika semuanya berjalan, server contoh dapat dijangkau dari Claude di `https://echo.<your-tunnel-domain>/mcp` meskipun tidak ada yang mendengarkan pada port publik.

## Apa yang Anda butuhkan

* [Docker dan Docker Compose](https://docs.docker.com/get-docker/) pada mesin dengan akses internet keluar.
* Peran di [Claude Console](https://platform.claude.com) yang dapat mengelola tunnel MCP. Lihat [prasyarat panduan Console](/docs/id/agents-and-tools/mcp-tunnels/console#prerequisites).
* [OpenSSL](https://openssl-library.org/source/) 1.1.1 atau yang lebih baru. Sudah terpasang di macOS dan sebagian besar distribusi Linux; di Windows, instal secara terpisah (binary `openssl` harus ada di `PATH` Anda).

<Steps>
  <Step title="Buat tunnel">
    Di sidebar Claude Console, buka **Manage > MCP tunnels** dan klik **New tunnel**. Beri nama. Biarkan **Set up programmatic access** nonaktif; quickstart ini menggunakan provisioning kredensial manual.

    Setelah dibuat, buka tunnel tersebut. Salin dua nilai dari bagian **Connection**:

    * **Domain** (terlihat seperti `abcd1234.tunnel.anthropic.com`)
    * **Token** (klik ikon mata, lalu salin)
  </Step>

  <Step title="Siapkan direktori deployment">
    <Tabs>
      <Tab title="macOS / Linux">
        ```bash
        mkdir -p mcp-tunnel/{config,data}
        cd mcp-tunnel
        export TUNNEL_DOMAIN=YOUR_TUNNEL_DOMAIN_HERE   # from step 1
        export TUNNEL_TOKEN='eyJ...'            # from step 1
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        ```powershell
        New-Item -ItemType Directory -Force -Path mcp-tunnel/config, mcp-tunnel/data | Out-Null
        Set-Location mcp-tunnel
        $env:TUNNEL_DOMAIN = "YOUR_TUNNEL_DOMAIN_HERE"   # from step 1
        $env:TUNNEL_TOKEN  = "eyJ..."             # from step 1
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Hasilkan CA dan sertifikat server">
    Proxy mengakhiri [inner TLS](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) menggunakan sertifikat yang ditandatangani oleh CA yang Anda kendalikan. Hasilkan keduanya:

    <Tabs>
      <Tab title="macOS / Linux">
        ```bash
        openssl req -x509 -newkey rsa:2048 -nodes \
          -keyout data/ca.key -out data/ca.crt \
          -days 3650 -subj "/CN=mcp-tunnel-ca" \
          -addext "basicConstraints=critical,CA:TRUE" \
          -addext "keyUsage=critical,keyCertSign,cRLSign" \
          -addext "subjectKeyIdentifier=hash"

        cat > data/tls.ext <<EOF
        subjectAltName = DNS:${TUNNEL_DOMAIN},DNS:*.${TUNNEL_DOMAIN}
        authorityKeyIdentifier = keyid,issuer
        extendedKeyUsage = serverAuth
        EOF

        openssl req -newkey rsa:2048 -nodes \
          -keyout data/tls.key -out /tmp/server.csr \
          -subj "/CN=${TUNNEL_DOMAIN}"
        openssl x509 -req -in /tmp/server.csr \
          -CA data/ca.crt -CAkey data/ca.key -CAcreateserial \
          -out data/tls.crt -days 90 -extfile data/tls.ext

        chmod 644 data/tls.key
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        ```powershell
        openssl req -x509 -newkey rsa:2048 -nodes `
          -keyout data/ca.key -out data/ca.crt `
          -days 3650 -subj "/CN=mcp-tunnel-ca" `
          -addext "basicConstraints=critical,CA:TRUE" `
          -addext "keyUsage=critical,keyCertSign,cRLSign" `
          -addext "subjectKeyIdentifier=hash"

        @"
        subjectAltName = DNS:$env:TUNNEL_DOMAIN,DNS:*.$env:TUNNEL_DOMAIN
        authorityKeyIdentifier = keyid,issuer
        extendedKeyUsage = serverAuth
        "@ | Set-Content -NoNewline -Encoding ascii -Path data/tls.ext

        openssl req -newkey rsa:2048 -nodes `
          -keyout data/tls.key -out data/server.csr `
          -subj "/CN=$env:TUNNEL_DOMAIN"
        openssl x509 -req -in data/server.csr `
          -CA data/ca.crt -CAkey data/ca.key -CAcreateserial `
          -out data/tls.crt -days 90 -extfile data/tls.ext
        ```
      </Tab>
    </Tabs>

    Kembali ke Console, pada halaman detail tunnel, klik **Add certificate** dan unggah `data/ca.crt` (atau tempel isinya). Status tunnel berubah menjadi **Active**.
  </Step>

  <Step title="Tulis server MCP contoh">
    <Tabs>
      <Tab title="macOS / Linux">
        ```bash
        cat > hello_server.py <<'EOF'
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
      </Tab>

      <Tab title="Windows (PowerShell)">
        ```powershell
        @'
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP("hello-server", host="0.0.0.0", port=9000)


        @mcp.tool()
        def hello(name: str = "world") -> str:
            """Say hello to someone."""
            return f"Hello, {name}!"


        if __name__ == "__main__":
            mcp.run(transport="streamable-http")
        '@ | Set-Content -NoNewline -Encoding ascii -Path hello_server.py
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Tulis konfigurasi proxy dan file compose">
    <Tabs>
      <Tab title="macOS / Linux">
        ```bash
        cat > config/mcp-proxy.yaml <<EOF
        listen_addr: ":8080"
        tunnel_domain: ${TUNNEL_DOMAIN}
        tls:
          cert_file: /data/tls.crt
          key_file: /data/tls.key
        routes:
          echo: http://hello-mcp:9000
        EOF

        cat > docker-compose.yaml <<'EOF'
        services:
          mcp-proxy:
            image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:9d4c80593b559fc3ca3814866418744fa94858b02a4d4a4cc52d423e732ccc81
            volumes:
              - ./config/mcp-proxy.yaml:/etc/mcp-gateway/config.yaml:ro
              - ./data:/data:ro
            restart: unless-stopped

          cloudflared:
            image: cloudflare/cloudflared@sha256:6b599ca3e974349ead3286d178da61d291961182ec3fe9c505e1dd02c8ac31b0
            command: tunnel --no-autoupdate run --url http://localhost:8080
            environment:
              - TUNNEL_TOKEN
            network_mode: "service:mcp-proxy"
            restart: unless-stopped

          hello-mcp:
            image: python:3.13-slim
            working_dir: /app
            volumes:
              - ./hello_server.py:/app/hello_server.py:ro
            command: sh -c "pip install --quiet mcp && python hello_server.py"
            restart: unless-stopped
        EOF
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        ```powershell
        @"
        listen_addr: ":8080"
        tunnel_domain: $env:TUNNEL_DOMAIN
        tls:
          cert_file: /data/tls.crt
          key_file: /data/tls.key
        routes:
          echo: http://hello-mcp:9000
        "@ | Set-Content -NoNewline -Encoding ascii -Path config/mcp-proxy.yaml

        @'
        services:
          mcp-proxy:
            image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:9d4c80593b559fc3ca3814866418744fa94858b02a4d4a4cc52d423e732ccc81
            volumes:
              - ./config/mcp-proxy.yaml:/etc/mcp-gateway/config.yaml:ro
              - ./data:/data:ro
            restart: unless-stopped

          cloudflared:
            image: cloudflare/cloudflared@sha256:6b599ca3e974349ead3286d178da61d291961182ec3fe9c505e1dd02c8ac31b0
            command: tunnel --no-autoupdate run --url http://localhost:8080
            environment:
              - TUNNEL_TOKEN
            network_mode: "service:mcp-proxy"
            restart: unless-stopped

          hello-mcp:
            image: python:3.13-slim
            working_dir: /app
            volumes:
              - ./hello_server.py:/app/hello_server.py:ro
            command: sh -c "pip install --quiet mcp && python hello_server.py"
            restart: unless-stopped
        '@ | Set-Content -NoNewline -Encoding ascii -Path docker-compose.yaml
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Jalankan">
    <Tabs>
      <Tab title="macOS / Linux">
        ```bash
        docker compose up -d
        docker compose logs mcp-proxy | grep "route configured"
        docker compose logs cloudflared | grep "Registered tunnel connection"
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        ```powershell
        docker compose up -d
        docker compose logs mcp-proxy | Select-String "route configured"
        docker compose logs cloudflared | Select-String "Registered tunnel connection"
        ```
      </Tab>
    </Tabs>

    Anda seharusnya melihat satu baris `route configured` untuk `echo` dan empat baris `Registered tunnel connection`. Kontainer membutuhkan beberapa detik untuk mulai; jalankan ulang perintah log jika hasilnya kosong.
  </Step>

  <Step title="Panggil dari Claude">
    Di Console, buka **Managed Agents > Sessions** dan buat sebuah sesi. Di pemilih agen pilih **Create new agent**, beri nama agen tersebut, dan pertahankan model yang sudah terisi. Klik **+ MCP Server**, pilih tunnel Anda, atur **Subdomain** ke `echo` dan **Path** ke `mcp`. Lalu tanyakan:

    > Use the hello tool to greet tunnel.

    Anda seharusnya melihat pemanggilan alat diikuti oleh hasilnya.
  </Step>
</Steps>

## Langkah selanjutnya

Tunnel telah diverifikasi dari ujung ke ujung. Untuk mengganti dengan server MCP Anda sendiri, tambahkan ke `docker-compose.yaml` (atau jalankan di jaringan Docker yang sama), tambahkan route untuknya di `config/mcp-proxy.yaml`, lalu mulai ulang proxy (`docker compose restart mcp-proxy`).

Untuk deployment produksi:

<CardGroup cols={2}>
  <Card title="Deploy dengan Docker Compose" icon="cube" href="/docs/id/agents-and-tools/mcp-tunnels/deploy-compose">
    Deployment single-host yang diperkuat, dengan atau tanpa akses programatik.
  </Card>

  <Card title="Deploy dengan Helm" icon="stack" href="/docs/id/agents-and-tools/mcp-tunnels/deploy-helm">
    Deployment Kubernetes dengan manajemen kredensial otomatis.
  </Card>
</CardGroup>
