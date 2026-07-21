---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 7cb080d9d08b603e754858659e8cfe01cf7af55556d551ecfe33dab367dd07c4
---

# Scripting dan otomatisasi CLI

Kelola versi sumber daya API sebagai YAML, rangkai perintah CLI ant dalam skrip, dan operasikan sumber daya dari Claude Code.

---

Halaman ini membahas alur kerja berorientasi tugas yang dibangun di atas CLI `ant`. Untuk flag dan opsi output yang mendasarinya, lihat [Menggunakan CLI](/docs/id/cli-sdks-libraries/cli/using).

## Mengelola versi sumber daya API

Anda dapat menggunakan CLI untuk mengelola versi sumber daya API seperti skill, agen, environment, atau deployment sebagai file YAML di repositori Anda dan menjaganya tetap sinkron dengan Claude API.

<Note>
  Untuk informasi lebih lanjut tentang sumber daya ini, lihat [Managed Agents](/docs/id/managed-agents/overview).
</Note>

<Steps>
  <Step title="Definisikan agen Anda">
    Tulis definisi agen ke `summarizer.agent.yaml`:

    ```yaml summarizer.agent.yaml
    name: Summarizer
    model: claude-sonnet-4-6
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
      "model": "claude-sonnet-4-6"
      /* ... */
    }
    ```

    Catat `id` dari respons. Anda akan meneruskannya ke perintah pembuatan sesi pada langkah berikutnya.

    <Tip>
      Masukkan `summarizer.agent.yaml` ke dalam repositori Anda dan jaga agar tetap sinkron dengan API di pipeline CI Anda. Perintah update memerlukan ID agen dan versi saat ini sebagai flag:

      ```bash CLI
      ant beta:agents update --agent-id agent_011CYm1BLqPXpQRk5khsSXrs --version 1 < summarizer.agent.yaml
      ```
    </Tip>
  </Step>

  <Step title="Definisikan environment">
    Sebuah sesi berjalan di dalam [environment](/docs/id/api/cli/beta/environments), yang mendefinisikan sandbox tempat sesi tersebut dieksekusi. Tulis definisi environment ke `summarizer.environment.yaml`:

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

    Catat `id` dari respons. Anda akan meneruskannya ke perintah pembuatan sesi pada langkah berikutnya.

    <Tip>
      Masukkan `summarizer.environment.yaml` ke dalam repositori Anda dan jaga agar tetap sinkron dengan API di pipeline CI Anda. Perintah update memerlukan ID environment sebagai flag:

      ```bash CLI
      ant beta:environments update --environment-id env_01595EKxaaTTGwwY3kyXdtbs < summarizer.environment.yaml
      ```
    </Tip>
  </Step>

  <Step title="Mulai sesi">
    Tempelkan `id` agen dan `id` environment dari output sebelumnya ke dalam perintah pembuatan sesi:

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
    Salin `id` sesi dari output sebelumnya ke dalam `--session-id`:

    ```bash
    ant beta:sessions:events send \
      --session-id session_01JZCh78XvmxJjiXVy3oSi7K \
      --event '{type: user.message, content: [{type: text, text: "Summarize the benefits of type safety in one sentence."}]}'
    ```
  </Step>

  <Step title="Baca percakapan">
    `--transform` dijalankan terhadap setiap event yang terdaftar, sehingga ini mencetak teks dari setiap pesan secara berurutan. `--format auto` menggantikan explorer interaktif yang secara default dibuka oleh perintah list di terminal:

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
      Untuk memantau sesi saat berjalan, gunakan `ant beta:sessions:events stream --session-id session_01JZCh78XvmxJjiXVy3oSi7K`. Event ditulis ke stdout saat event tersebut tiba.
    </Tip>
  </Step>
</Steps>

## Pola scripting

CLI dirancang untuk dapat dikomposisikan dengan perkakas shell standar.

### Merangkai output list ke perintah kedua

`--transform id --raw-output` pada endpoint list menghasilkan satu ID polos per baris, sehingga alat standar seperti `head` dan `xargs` dapat langsung diterapkan. Tangkap hasil pertama, lalu teruskan ke perintah lanjutan:

```bash
FIRST_AGENT=$(ant beta:agents list \
  --transform id --raw-output | head -1)

ant beta:agents:versions list \
  --agent-id "$FIRST_AGENT" \
  --transform "{version,created_at}" --format jsonl
```

### Memeriksa error

Flag `--transform-error` dan `--format-error` menerapkan penyaringan yang sama pada respons error. `--raw-output` tidak berlaku untuk error, jadi gunakan `--format-error yaml` untuk skalar tanpa tanda kutip. Ekstrak hanya pesan error:

```bash
ant beta:agents retrieve --agent-id bogus \
  --transform-error error.message --format-error yaml 2>&1
```

```text Output wrap
GET "https://api.anthropic.com/v1/agents/bogus?beta=true": 404 Not Found
Agent not found.
```

## Menggunakan CLI dari Claude Code

[Claude Code](https://code.claude.com/docs/en/overview) dapat menggunakan CLI `ant` secara langsung. Dengan CLI yang sudah terpasang dan terautentikasi, Anda dapat meminta Claude Code untuk mengoperasikan sumber daya API Anda secara langsung. Sebagai contoh:

* "Daftar sesi agen terbaru saya dan rangkum mana saja yang mengalami error."
* "Unggah setiap PDF di `./reports` ke Files API dan cetak ID yang dihasilkan."
* "Ambil event untuk sesi `session_01...` dan beri tahu saya di mana agen mengalami kebuntuan."

Claude Code menjalankan `ant` melalui shell, mem-parsing output terstruktur, dan melakukan penalaran atas hasilnya (tanpa memerlukan kode integrasi khusus).
