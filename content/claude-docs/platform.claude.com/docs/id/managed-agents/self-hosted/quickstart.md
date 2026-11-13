---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/quickstart
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 1c549892bf8288a76612a12f7015d23a0cc75aa7d1124235ad3f3e0f46e39082
---

---
title: Memulai dengan Claude Managed Agents yang di-host sendiri
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/quickstart
description: Jalankan Claude Managed Agents yang di-host sendiri di satu mesin dengan Docker Compose dan jalankan sesi pertama di dalam container sandbox.
---

<Note>
  Untuk meminta akses ke Claude Managed Agents yang di-host sendiri, hubungi tim akun Anthropic Anda.
</Note>

Dalam quickstart ini, Anda menjalankan Claude Managed Agents yang di-host sendiri di satu mesin dengan Docker Compose. Stack Compose terdiri dari server, database PostgreSQL-nya, dan sekumpulan worker yang menjalankan setiap sesi di “sandbox container” (container sandbox) miliknya sendiri. Setelah itu, Anda mengobrol dengan agen dari terminal Anda dan memastikan bahwa “tool calls” (panggilan alat) agen tersebut berjalan di dalam sandbox container. Anda kemudian dapat membuka sesi di [konsol di server Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/console).

<Warning>
  Stack Compose ditujukan untuk pengembangan, bukan untuk produksi. Stack ini melayani HTTP biasa, dan secara default memublikasikan port 8400 hanya pada alamat loopback host Docker, `127.0.0.1`. Pada beberapa rilis Docker Engine sebelum 28.3.3, mesin di jaringan lokal host juga dapat menjangkau port tersebut. Alat agen berjalan di container pada host tersebut, jadi gunakan mesin yang tidak menyimpan apa pun yang perlu Anda lindungi.
</Warning>

Untuk produksi, Anthropic merekomendasikan dua Helm chart dari rilis ini. Lihat [Menerapkan di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes).

Biarkan Claude Code menjalankan quickstart ini untuk Anda

```text
Siapkan Claude Managed Agents yang di-host sendiri di mesin ini dengan mengikuti https://platform.claude.com/docs/en/managed-agents/self-hosted/quickstart.md. Saya sudah mengunduh arsip rilisnya.
```

Jika Anda adalah agen yang menjalankan langkah-langkah ini untuk seseorang:

* **Arsip rilis:** Tanyakan kepada orang tersebut di mana arsipnya berada. Hanya mereka yang dapat mengunduhnya.
* **Kunci API Claude:** Minta orang tersebut mengedit `.env` sendiri. Jangan meminta kuncinya, dan jangan mencetak `.env`.
* **Variabel:** Jika shell Anda tidak mempertahankan variabel di antara perintah, atur `ANTHROPIC_BASE_URL` dan `ANTHROPIC_API_KEY` lagi di setiap perintah `ant`. Tanpa keduanya, `ant` memanggil layanan yang di-hosting.
* **Compose:** Letakkan `env -u ANTHROPIC_BASE_URL -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN` di depan setiap perintah `docker compose`, agar nilai dari shell Anda tidak sampai ke server.
* **Obrolan:** `ant beta:sessions connect` memerlukan terminal interaktif. Tanpa terminal interaktif, kirim pesan dengan `ant beta:sessions:events send`, dan baca balasannya dengan `ant beta:sessions:events list`. [Mengirim event](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#send-events) dan [Menampilkan daftar event sebelumnya](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#list-past-events) memiliki contohnya.
* **Konsol:** Lakukan bagian “Coba konsol di server Anda” hanya jika orang tersebut memintanya. Jika shell Anda tidak mempertahankan variabel di antara perintah, letakkan juga `COMPOSE_FILE=docker-compose.yml:docker-compose.oidc.yml` di depan setiap perintah `docker compose` mulai dari bagian tersebut.

## Prasyarat

* **Arsip rilis:** Untuk meminta akses ke unduhan, hubungi tim akun Anthropic Anda.
* **Kunci API Claude:** Server menggunakannya untuk panggilan model. Buat kunci di [Claude Console](https://platform.claude.com/settings/keys).
* **Docker:** [Versi terbaru Docker Engine](https://docs.docker.com/engine/install/) dengan plugin Compose (`docker compose`, bukan `docker-compose` versi lama).
* **Host dengan setidaknya dua CPU:** x86-64 atau Arm. Pada host yang lebih kecil, atur `CMA_SANDBOX_CPUS` ke jumlah CPU host tersebut saat Anda membuat `.env`.
* **Akses jaringan saat pertama kali dijalankan:** Build pertama mengambil dari Docker Hub, repositori paket Alpine, dan rilis GitHub.
* **Alat:** Di mesin tempat Anda menjalankan Docker, Anda memerlukan `openssl` dan [CLI `ant`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart#installation).

## Menjalankan stack

<Steps>
  <Step title="Ekstrak arsip">
    Ekstrak arsip, dan bekerjalah dari direktori `compose` di dalamnya. Dalam perintah tersebut, ganti `<archive>` dengan nama arsip Anda, tanpa `.tar.gz`.

    ```bash
    tar -xzf <archive>.tar.gz && cd <archive>/compose
    ```

    Jika umask Anda lebih ketat dari `022`, binary kehilangan izin eksekusinya untuk pengguna lain, dan container server tidak dapat menjalankannya. Dalam hal ini, atur umask ke `022` lalu ekstrak arsip lagi.
  </Step>

  <Step title="Buat file .env">
    Compose membaca secret stack dari file `.env` di sebelah `docker-compose.yml`. Buat file-nya:

    ```bash
    cat > .env <<EOF
    CMA_PG_PASSWORD=$(openssl rand -hex 32)
    ANTHROPIC_API_KEY=sk-ant-...
    CMA_SERVER__API_KEY=$(openssl rand -hex 32)
    CMA_STORE__CREDENTIALS_ENCRYPTION_KEY=$(openssl rand -base64 32)
    EOF
    chmod 600 .env
    ```

    Buka `.env` di editor dan ganti `sk-ant-...` dengan kunci API Claude Anda. Blok tersebut menghasilkan sisanya: kata sandi database, kunci API server yang dikirim aplikasi Anda, dan kunci yang mengenkripsi secret yang disimpan server.
  </Step>

  <Step title="Jalankan container">
    Build dan jalankan stack, lalu ikuti log server:

    ```bash
    docker compose up --build -d
    docker compose logs -f cma-server
    ```

    Ketika log menampilkan baris dengan `msg="cma-server listening"`, tekan Ctrl+C untuk berhenti mengikutinya.
  </Step>

  <Step title="Periksa bahwa server sudah siap">
    ```bash
    curl -s http://127.0.0.1:8400/cma-server/readyz
    ```

    Server yang siap menjawab dengan `"status":"ready"`. Tepat setelah dimulai, server dapat menjawab `"status":"degraded"` selama beberapa detik sementara pemeriksaan pertamanya berjalan. Jika statusnya tetap `degraded` atau server menjawab `"status":"not_ready"`, lihat [Pemecahan masalah](https://platform.claude.com/docs/id/managed-agents/self-hosted/quickstart#troubleshooting).
  </Step>
</Steps>

## Jalankan sesi pertama Anda

Buat agen dan mengobrollah dengannya dari terminal Anda menggunakan CLI `ant`.

<Steps>
  <Step title="Arahkan CLI ke server Anda">
    Buka terminal kedua di direktori yang sama, dan gunakan terminal itu khusus untuk `ant`. Perintah-perintah berikut mengatur `ANTHROPIC_API_KEY` ke kunci API server Anda, bukan kunci API Claude Anda, seperti yang dijelaskan di [Memanggil API pada server yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api):

    ```bash
    export ANTHROPIC_BASE_URL=http://127.0.0.1:8400
    export ANTHROPIC_API_KEY=$(grep '^CMA_SERVER__API_KEY=' .env | cut -d= -f2)
    ```

    Tetap jalankan perintah `docker compose` di terminal pertama. Jika Anda menjalankan `docker compose up` di terminal ini, Compose meneruskan variabel-variabel ini ke server, dan server memanggil dirinya sendiri alih-alih Claude API.
  </Step>

  <Step title="Buat agen">
    Simpan file yang ditampilkan setelah perintah sebagai `quickstart-agent.md`, lalu jalankan perintah tersebut. File ini memberikan alat bawaan kepada agen dan mengizinkannya menjalankan alat tersebut tanpa meminta persetujuan Anda terlebih dahulu.

    <CodeGroup>
      <CodeGroupItem>
        ```bash CLI
        ant apply --yes quickstart-agent.md
        ```

        <File filename="quickstart-agent.md">
          ```markdown
          ---
          name: Quickstart agent
          model: claude-opus-5-5
          tools:
            - type: agent_toolset_20260401
          ---

          You are a helpful assistant.
          ```
        </File>
      </CodeGroupItem>
    </CodeGroup>

    Perintah ini pertama-tama mencetak peringatan bahwa perintah tersebut `could not determine the organization and workspace`, dengan error `404`, lalu membuat agen. Hal itu memang diharapkan di server Anda sendiri.
  </Step>

  <Step title="Mulai sesi">
    Perintah-perintah ini menemukan agen dan environment milik stack, memulai sesi, dan menyimpan ID sesi di `SESSION_ID`. Stack menamai environment-nya `compose-sandbox`.

    ```bash
    AGENT_ID=$(ant beta:agents list --format raw \
      --transform 'data.#(name=="Quickstart agent").id' --raw-output)
    ENVIRONMENT_ID=$(ant beta:environments list --format raw \
      --transform 'data.#(name=="compose-sandbox").id' --raw-output)
    SESSION_ID=$(ant beta:sessions create --agent "$AGENT_ID" \
      --environment-id "$ENVIRONMENT_ID" --transform id --raw-output)
    ```
  </Step>

  <Step title="Minta agen menjalankan perintah">
    Hubungkan terminal Anda ke sesi:

    ```bash
    ant beta:sessions connect "$SESSION_ID"
    ```

    Perintah ini membuka [tampilan obrolan](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/sessions-connect) dari sesi. Kirim pesan ini:

    ```text wrap
    Run `hostname` with the bash tool and tell me the output.
    ```

    Agen membalas dengan hostname yang diawali `cma-sandbox-`. Itu adalah nama container sandbox yang menjalankan perintah tersebut, yang memastikan bahwa alat berjalan di sandbox dan bukan di mesin Anda.
  </Step>

  <Step title="Temukan container sandbox">
    Biarkan obrolan tetap terbuka. Di terminal pertama, tampilkan daftar sandbox container:

    ```bash
    docker ps --filter label=cma-server.sandbox
    ```

    Daftar menampilkan container yang dilaporkan agen. Container keluar sekitar satu menit setelah sebuah giliran berakhir, dan pesan berikutnya dalam sesi memulai container baru. Jika daftarnya kosong, minta agen menjalankan `hostname` lagi, dan tampilkan daftar container lagi selagi agen membalas.

    Untuk keluar dari obrolan, tekan Ctrl+C di terminalnya. Sesi tetap berjalan.
  </Step>
</Steps>

## Coba konsol di server Anda

Bagian ini opsional. Konsol memerlukan single sign-on. Untuk mencobanya, mulai ulang stack dengan penyedia sign-in tiruan dari rilis. Port 8080 di mesin Anda harus kosong.

<Warning>
  Gunakan penyedia tiruan hanya dengan data sekali pakai. Penyedia ini memberikan token administrator kepada siapa pun yang menjangkaunya. Di Docker Desktop, itu termasuk sandbox container. Pada beberapa rilis Docker Engine sebelum 28.3.3, itu termasuk mesin di jaringan Anda.
</Warning>

<Steps>
  <Step title="Mulai ulang stack dengan penyedia sign-in tiruan">
    Jalankan perintah-perintah ini di terminal pertama:

    ```bash
    export COMPOSE_FILE=docker-compose.yml:docker-compose.oidc.yml
    docker compose up --build -d
    ```

    Baris `export` hanya berlaku untuk terminal pertama, jadi jalankan lagi di terminal baru mana pun yang Anda buka untuk `docker compose`. Untuk mengubah pengaturan server di stack ini, edit `compose.config.oidc.yaml`, bukan `compose.config.yaml`, lalu jalankan `docker compose restart cma-server`.
  </Step>

  <Step title="Buka sesi">
    Di browser pada mesin yang sama, buka `http://127.0.0.1:8400/`, klik **Continue with SSO**, lalu pilih **alice**, administrator demo. Di sidebar, pilih **Sessions**, lalu pilih sesi tersebut.

    Halaman diperbarui seiring agen bekerja, dan Anda dapat mengirim pesan ke agen dari halaman tersebut.
  </Step>
</Steps>

Untuk juga membuat agen dan memulai sesi di konsol, lihat [Menjalankan agen dari konsol](https://platform.claude.com/docs/id/managed-agents/self-hosted/console#run-an-agent-from-the-console).

## Menghentikan stack

Di terminal pertama, jalankan perintah ini:

```bash
docker compose down --remove-orphans
```

Perintah ini menghapus container dan mempertahankan database. Untuk juga menghapus database, beserta setiap agen, sesi, dan riwayat sesi di dalamnya, jalankan `docker compose down --remove-orphans -v`.

## Pemecahan masalah

* **Arsip Anda tidak memiliki direktori `compose`:** Arsip tersebut berisi rilis yang lebih lama, dan perintah di halaman ini tidak sesuai dengannya. Mintalah rilis terbaru kepada tim akun Anthropic Anda. Untuk memindahkan deployment yang sedang berjalan ke rilis terbaru, lihat [Meningkatkan Claude Managed Agents yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/upgrade).

* **Server tidak pernah aktif:** Jalankan `docker compose logs migrate`. Container `migrate` sekali jalan membuat tabel database. Container tersebut harus keluar dengan status `0` sebelum server dimulai.

* **Pemeriksaan kesiapan tetap `degraded`, atau setiap giliran gagal:** Jika Anda menjalankan `docker compose up` di terminal tempat `ANTHROPIC_BASE_URL` bernilai `http://127.0.0.1:8400`, server memanggil dirinya sendiri alih-alih Claude API. Jalankan `docker compose up -d` lagi di terminal pertama, tempat variabel tersebut tidak diatur. Jika tidak demikian, log server menunjukkan apa yang gagal. Untuk membacanya, jalankan `docker compose logs -f cma-server` lagi.

* **Pemeriksaan kesiapan menjawab `not_ready`:** Dalam jawaban tersebut, temukan pemeriksaan dengan status `failed`:

  * **`upstream`:** Claude API menolak kunci API Claude Anda. Perbaiki `ANTHROPIC_API_KEY` di `.env`, lalu jalankan `docker compose up -d` lagi di terminal pertama. Jika shell Anda juga mengatur `ANTHROPIC_API_KEY`, Compose menggunakan nilai dari shell, jadi jalankan `unset ANTHROPIC_API_KEY` terlebih dahulu.
  * **`database`:** Database menolak login server, misalnya karena kata sandi salah, atau koneksi terbuka ke database terputus. Untuk mengetahui penyebabnya, jalankan `docker compose logs -f cma-server` lagi.

* **Agen membalas tetapi panggilan alatnya tidak pernah selesai:** Tidak ada worker yang melakukan polling ke environment. Periksa log worker dengan `docker compose logs sandbox`. Worker yang tidak dapat menjangkau socket daemon Docker keluar dengan pesan yang menyebutkan `CMA_DOCKER_SOCKET`. Atur variabel tersebut di `.env` ke path socket daemon Anda, lalu jalankan `docker compose up -d` lagi di terminal pertama.

* **Worker berjalan, tetapi panggilan alat tetap tidak pernah selesai:** Stack menjalankan 10 worker, dan masing-masing menjalankan container dari satu sesi pada satu waktu. Sebuah sesi mengambil satu worker yang kosong saat Anda membuatnya, dan sesi yang tidak pernah menerima pesan mempertahankan worker-nya hingga satu jam. Jika kesepuluh worker sudah terpakai, panggilan alat dari sesi lain menunggu worker. Jika perintah `docker ps` pada langkah “Temukan container sandbox” menampilkan 10 container, arsipkan sesi yang tidak Anda gunakan:

  1. Di terminal pertama, jalankan `docker ps --filter label=cma-server.sandbox --format '{{.Label "cma-server.session"}}'`. Perintah ini mencetak ID sesi di balik setiap container. Sesi yang sedang menunggu belum memiliki container, jadi sesi tersebut tidak ada di daftar.
  2. Di terminal kedua, tekan Ctrl+C untuk keluar dari obrolan, lalu jalankan `ant beta:sessions archive --session-id <session-id>` untuk setiap sesi dalam daftar yang tidak Anda gunakan.
  3. Jalankan `ant beta:sessions connect "$SESSION_ID"` lagi. Panggilan alat selesai ketika sebuah worker mengambil sesinya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Memanggil API" icon="code-brackets" href="https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api">
    Arahkan SDK dan CLI `ant` ke server Anda.
  </Card>

  <Card title="Perbedaan dari layanan yang di-hosting" icon="arrows-left-right" href="https://platform.claude.com/docs/id/managed-agents/self-hosted/differences">
    Periksa fitur mana yang berperilaku berbeda atau tidak tersedia.
  </Card>

  <Card title="Konsol di server Anda" icon="browser" href="https://platform.claude.com/docs/id/managed-agents/self-hosted/console">
    Siapkan sign-in, lalu buat agen dan jalankan sesi di browser.
  </Card>
</CardGroup>
