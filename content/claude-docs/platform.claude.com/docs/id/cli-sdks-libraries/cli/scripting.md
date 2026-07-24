---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 4727bbda13c4f4b9ae9ce7f4930e06891171adb286a5193c83ee9df53e052d22
---

# Scripting dan otomatisasi CLI

Kontrol versi sumber daya API sebagai YAML, rangkai perintah CLI ant dalam skrip, operasikan sumber daya dari Claude Code, dan autentikasi panggilan curl dengan kredensial CLI.

---

Halaman ini membahas alur kerja berorientasi tugas yang dibangun di atas CLI `ant`. Untuk flag dan opsi output yang mendasarinya, lihat [Menggunakan CLI](/docs/id/cli-sdks-libraries/cli/using).

## Kontrol versi sumber daya API

Anda dapat menggunakan CLI untuk mengontrol versi sumber daya API seperti skill, agen, environment, atau deployment sebagai file YAML di repositori Anda dan menjaganya tetap sinkron dengan Claude API.

<Note>
  Untuk informasi lebih lanjut tentang sumber daya ini, lihat [Managed Agents](/docs/id/managed-agents/overview).
</Note>

<Steps>
  <Step title="Definisikan agen Anda">
    Tulis definisi agen ke `summarizer.agent.yaml`:

    ```yaml summarizer.agent.yaml
    name: Summarizer
    model: claude-opus-4-8
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
      "model": "claude-opus-4-8"
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
    Sebuah sesi berjalan dalam sebuah [environment](/docs/id/api/cli/beta/environments), yang mendefinisikan sandbox tempat sesi tersebut dieksekusi. Tulis definisi environment ke `summarizer.environment.yaml`:

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
    `--transform` dijalankan terhadap setiap event yang terdaftar, sehingga ini mencetak teks dari setiap pesan secara berurutan. `--format auto` menggantikan explorer interaktif yang dibuka secara default oleh perintah list di terminal:

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

[Claude Code](https://code.claude.com/docs/id/overview) dapat menggunakan CLI `ant` secara langsung. Dengan CLI yang terpasang dan terautentikasi, Anda dapat meminta Claude Code untuk mengoperasikan sumber daya API Anda secara langsung. Sebagai contoh:

* "Daftarkan sesi agen terbaru saya dan rangkum mana saja yang mengalami error."
* "Unggah setiap PDF di `./reports` ke Files API dan cetak ID yang dihasilkan."
* "Ambil event untuk sesi `session_01...` dan beri tahu saya di mana agen mengalami kebuntuan."

Claude Code menjalankan `ant` melalui shell, mengurai output terstruktur, dan melakukan penalaran atas hasilnya (tidak memerlukan kode integrasi khusus).

## Autentikasi permintaan curl dengan kredensial CLI

Skrip yang memanggil API dengan `curl` atau klien HTTP lainnya dapat menggunakan kredensial yang disimpan oleh [`ant auth login`](/docs/id/cli-sdks-libraries/cli/quickstart#authentication) alih-alih kunci API statis. Token akses OAuth ditempatkan di header `Authorization` sebagai bearer token; header `x-api-key` hanya untuk kunci API statis.

`ant auth print-credentials --access-token` mencetak token akses dari profil aktif, menyegarkannya terlebih dahulu jika sudah kedaluwarsa atau mendekati kedaluwarsa:

```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "Authorization: Bearer $(ant auth print-credentials --access-token)" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "hi"}]
  }'
```

<Note>
  Biarkan `ANTHROPIC_API_KEY` dan `ANTHROPIC_AUTH_TOKEN` tidak diatur saat bekerja dari login CLI. Salah satu variabel tersebut akan diprioritaskan di atas login untuk perintah `ant` (lihat [Prioritas kredensial](/docs/id/manage-claude/wif-reference#credential-precedence)) dan dapat secara diam-diam mengarahkannya ke organisasi atau workspace yang berbeda.
</Note>

Jalankan [`ant auth status`](/docs/id/cli-sdks-libraries/cli/authentication#check-authentication-status) untuk mengonfirmasi organisasi dan workspace mana yang sedang Anda gunakan untuk login; perintah ini akan memberi peringatan ketika sebuah variabel lingkungan menimpa login Anda.
