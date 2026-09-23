---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting
fetched_at: 2026-09-23T02:21:59.104890Z
sha256: 9d5ff17a5e5a638097cd645a82606ace5123c0e6d5825cd53222c45fbe806ada
---

---
title: Scripting dan otomatisasi CLI
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting
description: Kelola versi sumber daya API sebagai file dengan ant apply, rangkai perintah CLI ant dalam skrip, operasikan sumber daya dari Claude Code, dan autentikasi panggilan curl dengan kredensial CLI.
---

Halaman ini membahas alur kerja berorientasi tugas yang dibangun di atas CLI `ant`. Untuk flag dan opsi output yang mendasarinya, lihat [Menggunakan CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/using).

## Mengelola versi sumber daya API

Untuk menyimpan agen, lingkungan, dan sumber daya Claude Managed Agents lainnya sebagai file di repositori Anda, lihat [Mengelola sumber daya sebagai kode dengan ant apply](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply).

### Menjalankan agen yang telah diterapkan dari shell

Setelah agen dan lingkungan tersedia, Anda dapat menjalankan sesi dari shell:

<Steps>
  <Step title="Memulai sesi">
    Berikan ID agen dan ID lingkungan ke perintah pembuatan sesi. Setelah `ant apply`, baca ID tersebut dari `claude-lock.json`: setiap entri di bawah `resources` memiliki `id`, dan untuk proyek di [Mengelola sumber daya sebagai kode dengan ant apply](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply) entrinya adalah `./agents/summarizer.md` dan `./environments/cloud.yaml`.

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
    Setelah agen membalas, tampilkan daftar event. `--transform` dijalankan terhadap setiap event yang terdaftar, sehingga perintah ini mencetak teks dari setiap pesan secara berurutan. `--format auto` menggantikan penjelajah interaktif yang secara default dibuka oleh perintah list di terminal:

    ```bash
    ant beta:sessions:events list \
      --session-id session_01JZCh78XvmxJjiXVy3oSi7K \
      --transform 'content.0.text' \
      --raw-output \
      --format auto
    ```

    ```text Output wrap
    Summarize the benefits of type safety in one sentence.
    Type safety catches errors at compile time rather than runtime, reducing bugs, improving code clarity, enabling better tooling support, and making codebases easier to maintain and refactor with confidence.
    ```

    <Tip>
      Untuk memantau sesi saat berjalan, gunakan `ant beta:sessions:events stream --session-id session_01JZCh78XvmxJjiXVy3oSi7K --format jsonl`, yang menulis setiap event ke stdout saat event tersebut tiba. Tanpa `--format`, terminal akan membuka penjelajah interaktif sebagai gantinya.
    </Tip>
  </Step>
</Steps>

## Pola scripting

CLI dirancang agar dapat dikombinasikan dengan perangkat shell standar.

### Merangkai output list ke perintah kedua

`--transform id --raw-output` pada endpoint list menghasilkan satu ID polos per baris, sehingga alat standar seperti `head` dan `xargs` dapat langsung diterapkan. Ambil hasil pertama, lalu teruskan ke perintah lanjutan:

```bash
FIRST_AGENT=$(ant beta:agents list --transform id --raw-output | head -1)

ant beta:agents:versions list \
  --agent-id "$FIRST_AGENT" \
  --transform "{version,created_at}" --format jsonl
```

### Memeriksa error

Flag `--transform-error` dan `--format-error` menerapkan pemfilteran yang sama pada respons error. `--raw-output` tidak berlaku untuk error, jadi gunakan `--format-error yaml` untuk skalar tanpa tanda kutip. Ekstrak hanya pesan error-nya:

```bash
ant beta:agents retrieve --agent-id bogus \
  --transform-error error.message --format-error yaml 2>&1
```

```text Output wrap
GET "https://api.anthropic.com/v1/agents/bogus?beta=true": 404 Not Found
Agent not found.
```

## Menggunakan CLI dari Claude Code

[Claude Code](https://code.claude.com/docs/id/overview) dapat menggunakan CLI `ant` secara langsung tanpa konfigurasi tambahan. Dengan CLI yang sudah terinstal dan terautentikasi, Anda dapat meminta Claude Code untuk mengoperasikan sumber daya API Anda secara langsung. Misalnya:

* "Tampilkan daftar sesi agen terbaru saya dan rangkum mana saja yang mengalami error."
* "Unggah setiap PDF di `./reports` ke Files API dan cetak ID yang dihasilkan."
* "Ambil event untuk sesi `session_01...` dan beri tahu saya di mana agen tersebut macet."

Claude Code memanggil `ant` melalui shell, mem-parsing output terstrukturnya, dan menalar hasilnya (tanpa memerlukan kode integrasi khusus).

## Mengautentikasi permintaan curl dengan kredensial CLI

Skrip yang memanggil API dengan `curl` atau klien HTTP lain dapat menggunakan kredensial yang disimpan oleh [`ant auth login`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart#authentication) alih-alih "API key" (kunci API) statis. Token akses OAuth ditempatkan di header `Authorization` sebagai bearer token; header `x-api-key` hanya untuk kunci API statis.

`ant auth print-credentials --access-token` mencetak token akses profil aktif, dengan memperbaruinya terlebih dahulu jika sudah kedaluwarsa atau hampir kedaluwarsa:

```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "Authorization: Bearer $(ant auth print-credentials --access-token)" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-5-5",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "hi"}]
  }'
```

<Note>
  Biarkan `ANTHROPIC_API_KEY` dan `ANTHROPIC_AUTH_TOKEN` tidak disetel saat bekerja dari login CLI. Kedua variabel tersebut lebih diutamakan daripada login untuk perintah `ant` (lihat [Prioritas kredensial](https://platform.claude.com/docs/id/manage-claude/wif-reference#credential-precedence)) dan dapat secara diam-diam mengarahkannya ke organisasi atau workspace yang berbeda.
</Note>

Jalankan [`ant auth status`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication#check-authentication-status) untuk memastikan organisasi dan workspace mana yang sedang Anda gunakan untuk login; perintah ini memberi peringatan ketika sebuah variabel environment menimpa login Anda.
