---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 3e8d647baad3732798163e28e393ce5524224a0d1f3520a978bec5e4dbd07859
---

---
title: Scripting dan otomatisasi CLI
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting
description: Kelola versi sumber daya API sebagai YAML, rangkai perintah CLI ant dalam skrip, operasikan sumber daya dari Claude Code, dan autentikasi panggilan curl dengan kredensial CLI.
---

Halaman ini membahas alur kerja berorientasi tugas yang dibangun di atas CLI `ant`. Untuk flag dan opsi output yang mendasarinya, lihat [Menggunakan CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/using).

## Mengelola versi sumber daya API

Anda dapat menggunakan CLI untuk mengelola versi (version control) sumber daya API seperti skill, agen, environment, atau deployment sebagai file YAML di repositori Anda dan menjaganya tetap sinkron dengan Claude API.

<Note>
  Untuk informasi lebih lanjut tentang sumber daya ini, lihat [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview).
</Note>

<Steps>
  <Step title="Definisikan agen Anda">
    Tulis definisi agen ke `summarizer.agent.yaml`:

    ```yaml summarizer.agent.yaml
    name: Summarizer
    model: claude-opus-5
    system: |
      You are a helpful assistant that writes concise summaries.
    tools:
      - type: agent_toolset_20260401
    ```
  </Step>

  <Step title="Buat agen">
    ```bash
    ant beta:agents create < summarizer.agent.yaml
    ```

    ```json Output
    {
      "id": "agent_011CYm1BLqPXpQRk5khsSXrs",
      "version": 1,
      "name": "Summarizer",
      "model": "claude-opus-5"
      /* ... */
    }
    ```

    Catat `id` dari respons. Anda akan meneruskannya ke perintah pembuatan sesi pada langkah selanjutnya.

    <Tip>
      Masukkan `summarizer.agent.yaml` ke repositori Anda dan jaga agar tetap sinkron dengan API di pipeline CI Anda. Perintah update memerlukan ID agen dan versi saat ini sebagai flag:

      ```bash CLI
      ant beta:agents update --agent-id agent_011CYm1BLqPXpQRk5khsSXrs --version 1 < summarizer.agent.yaml
      ```
    </Tip>
  </Step>

  <Step title="Definisikan environment">
    Sebuah sesi berjalan di dalam [environment](https://platform.claude.com/docs/id/api/cli/beta/environments), yang mendefinisikan sandbox tempat sesi tersebut dieksekusi. Tulis definisi environment ke `summarizer.environment.yaml`:

    ```yaml summarizer.environment.yaml
    name: summarizer-env
    config:
      type: cloud
      networking:
        type: unrestricted
    ```
  </Step>

  <Step title="Buat environment">
    ```bash
    ant beta:environments create < summarizer.environment.yaml
    ```

    ```json Output
    {
      "id": "env_01595EKxaaTTGwwY3kyXdtbs",
      "name": "summarizer-env"
      /* ... */
    }
    ```

    Catat `id` dari respons. Anda akan meneruskannya ke perintah pembuatan sesi pada langkah selanjutnya.

    <Tip>
      Masukkan `summarizer.environment.yaml` ke repositori Anda dan jaga agar tetap sinkron dengan API di pipeline CI Anda. Perintah update memerlukan ID environment sebagai flag:

      ```bash CLI
      ant beta:environments update --environment-id env_01595EKxaaTTGwwY3kyXdtbs < summarizer.environment.yaml
      ```
    </Tip>
  </Step>

  <Step title="Mulai sesi">
    Tempelkan `id` agen dan `id` environment dari output sebelumnya ke perintah pembuatan sesi:

    ```bash
    ant beta:sessions create \
      --agent agent_011CYm1BLqPXpQRk5khsSXrs \
      --environment-id env_01595EKxaaTTGwwY3kyXdtbs \
      --title "Summarization task"
    ```

    ```json Output
    {
      "id": "session_01JZCh78XvmxJjiXVy3oSi7K",
      "status": "running"
      /* ... */
    }
    ```
  </Step>

  <Step title="Kirim pesan pengguna">
    Salin `id` sesi dari output sebelumnya ke `--session-id`:

    ```bash
    ant beta:sessions:events send \
      --session-id session_01JZCh78XvmxJjiXVy3oSi7K \
      --event '{type: user.message, content: [{type: text, text: "Summarize the benefits of type safety in one sentence."}]}'
    ```
  </Step>

  <Step title="Baca percakapan">
    `--transform` dijalankan terhadap setiap event yang terdaftar, sehingga ini mencetak teks setiap pesan secara berurutan. `--format auto` menimpa explorer interaktif yang dibuka oleh perintah list secara default di terminal:

    ```bash
    ant beta:sessions:events list \
      --session-id session_01JZCh78XvmxJjiXVy3oSi7K \
      --transform 'content.0.text' --format auto --raw-output
    ```

    ```text Output wrap
    Summarize the benefits of type safety in one sentence.
    Type safety catches errors at compile time rather than runtime, reducing bugs, improving code clarity, enabling better tooling support, and making codebases easier to maintain and refactor with confidence.
    ```

    <Tip>
      Untuk memantau sesi saat berjalan, gunakan `ant beta:sessions:events stream --session-id session_01JZCh78XvmxJjiXVy3oSi7K`. Event ditulis ke stdout saat tiba.
    </Tip>
  </Step>
</Steps>

## Pola scripting

CLI dirancang agar dapat dikombinasikan dengan perangkat shell standar.

### Rangkai output list ke perintah kedua

`--transform id --raw-output` pada endpoint list menghasilkan satu ID polos per baris, sehingga alat standar seperti `head` dan `xargs` dapat langsung diterapkan. Ambil hasil pertama, lalu teruskan ke perintah lanjutan:

```bash
FIRST_AGENT=$(ant beta:agents list --transform id --raw-output | head -1)

ant beta:agents:versions list \
  --agent-id "$FIRST_AGENT" \
  --transform "{version,created_at}" --format jsonl
```

### Periksa error

Flag `--transform-error` dan `--format-error` menerapkan pemfilteran yang sama pada respons error. `--raw-output` tidak berlaku untuk error, jadi gunakan `--format-error yaml` untuk skalar tanpa tanda kutip. Ekstrak hanya pesan error-nya:

```bash
ant beta:agents retrieve --agent-id bogus \
  --transform-error error.message --format-error yaml 2>&1
```

```text Output wrap
GET "https://api.anthropic.com/v1/agents/bogus?beta=true": 404 Not Found
Agent not found.
```

## Gunakan CLI dari Claude Code

[Claude Code](https://code.claude.com/docs/en/overview) dapat menggunakan CLI `ant` secara langsung tanpa konfigurasi tambahan. Dengan CLI yang sudah terinstal dan terautentikasi, Anda dapat meminta Claude Code untuk mengoperasikan sumber daya API Anda secara langsung. Misalnya:

* "Tampilkan daftar sesi agen terbaru saya dan rangkum mana saja yang mengalami error."
* "Unggah setiap PDF di `./reports` ke Files API dan cetak ID yang dihasilkan."
* "Ambil event untuk sesi `session_01...` dan beri tahu saya di mana agen tersebut macet."

Claude Code memanggil `ant` melalui shell, mem-parsing output terstrukturnya, dan bernalar atas hasilnya (tanpa memerlukan kode integrasi khusus).

## Autentikasi permintaan curl dengan kredensial CLI

Skrip yang memanggil API dengan `curl` atau klien HTTP lain dapat menggunakan kredensial yang disimpan oleh [`ant auth login`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart#authentication) alih-alih "API key" (kunci API) statis. Token akses OAuth ditempatkan di header `Authorization` sebagai bearer token; header `x-api-key` hanya untuk kunci API statis.

`ant auth print-credentials --access-token` mencetak token akses profil aktif, dengan memperbaruinya terlebih dahulu jika sudah kedaluwarsa atau hampir kedaluwarsa:

```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "Authorization: Bearer $(ant auth print-credentials --access-token)" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-5",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "hi"}]
  }'
```

<Note>
  Biarkan `ANTHROPIC_API_KEY` dan `ANTHROPIC_AUTH_TOKEN` tidak disetel saat bekerja dari login CLI. Kedua variabel tersebut lebih diutamakan daripada login untuk perintah `ant` (lihat [Prioritas kredensial](https://platform.claude.com/docs/id/manage-claude/wif-reference#credential-precedence)) dan dapat secara diam-diam mengarahkannya ke organisasi atau workspace yang berbeda.
</Note>

Jalankan [`ant auth status`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication#check-authentication-status) untuk memastikan organisasi dan workspace mana yang Anda gunakan untuk login; perintah ini memberi peringatan ketika sebuah variabel environment menimpa login Anda.
