---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/quickstart
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 88a6b4382238005da6abad42d23398b975e731a6f957f95ed063206dd6f00cc7
---

# Panduan Cepat

Mulai dengan Python atau TypeScript Agent SDK untuk membangun agen AI yang bekerja secara mandiri

---

Gunakan Agent SDK untuk membangun agen AI yang membaca kode Anda, menemukan bug, dan memperbaikinya, semuanya tanpa intervensi manual.

**Yang akan Anda lakukan:**
1. Siapkan proyek dengan Agent SDK
2. Buat file dengan beberapa kode yang berisi bug
3. Jalankan agen yang menemukan dan memperbaiki bug secara otomatis

## Prasyarat

- **Node.js 18+** atau **Python 3.10+**
- Akun **Anthropic** ([daftar di sini](https://platform.claude.com/))

## Pengaturan

<Steps>
  <Step title="Buat folder proyek">
    Buat direktori baru untuk panduan cepat ini:

    ```bash
    mkdir my-agent && cd my-agent
    ```

    Untuk proyek Anda sendiri, Anda dapat menjalankan SDK dari folder apa pun; SDK akan memiliki akses ke file di direktori tersebut dan subdirektorinya secara default.
  </Step>

  <Step title="Instal SDK">
    Instal paket Agent SDK untuk bahasa Anda:

    <Tabs>
      <Tab title="TypeScript">
        ```bash
        npm install @anthropic-ai/claude-agent-sdk
        ```
      </Tab>
      <Tab title="Python (uv)">
        [uv Python package manager](https://docs.astral.sh/uv/) adalah pengelola paket Python yang cepat dan menangani lingkungan virtual secara otomatis:
        ```bash
        uv init && uv add claude-agent-sdk
        ```
      </Tab>
      <Tab title="Python (pip)">
        Buat lingkungan virtual terlebih dahulu, kemudian instal:
        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        pip3 install claude-agent-sdk
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Atur kunci API Anda">
    Dapatkan kunci API dari [Claude Console](https://platform.claude.com/), kemudian buat file `.env` di direktori proyek Anda:

    ```bash
    ANTHROPIC_API_KEY=your-api-key
    ```

    SDK juga mendukung autentikasi melalui penyedia API pihak ketiga:

    - **Amazon Bedrock**: atur variabel lingkungan `CLAUDE_CODE_USE_BEDROCK=1` dan konfigurasi kredensial AWS
    - **Google Vertex AI**: atur variabel lingkungan `CLAUDE_CODE_USE_VERTEX=1` dan konfigurasi kredensial Google Cloud
    - **Microsoft Azure**: atur variabel lingkungan `CLAUDE_CODE_USE_FOUNDRY=1` dan konfigurasi kredensial Azure

    Lihat panduan pengaturan untuk [Bedrock](https://code.claude.com/docs/id/amazon-bedrock), [Vertex AI](https://code.claude.com/docs/id/google-vertex-ai), atau [Azure AI Foundry](https://code.claude.com/docs/id/azure-ai-foundry) untuk detail.

    <Note>
    Kecuali telah disetujui sebelumnya, Anthropic tidak mengizinkan pengembang pihak ketiga untuk menawarkan login claude.ai atau batas laju untuk produk mereka, termasuk agen yang dibangun di Agent SDK Claude. Silakan gunakan metode autentikasi kunci API yang dijelaskan dalam dokumen ini.
    </Note>
  </Step>
</Steps>

## Buat file dengan bug

Panduan cepat ini memandu Anda membangun agen yang dapat menemukan dan memperbaiki bug dalam kode. Pertama, Anda memerlukan file dengan beberapa bug yang disengaja untuk diperbaiki oleh agen. Buat `utils.py` di direktori `my-agent` dan tempel kode berikut:

```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

def get_user_name(user):
    return user["name"].upper()
```

Kode ini memiliki dua bug:
1. `calculate_average([])` mogok dengan pembagian oleh nol
2. `get_user_name(None)` mogok dengan TypeError

## Bangun agen yang menemukan dan memperbaiki bug

Buat `agent.py` jika Anda menggunakan Python SDK, atau `agent.ts` untuk TypeScript:

<CodeGroup>
```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async def main():
    # Agentic loop: streams messages as Claude works
    async for message in query(
        prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],  # Tools Claude can use
            permission_mode="acceptEdits"            # Auto-approve file edits
        )
    ):
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)              # Claude's reasoning
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")   # Tool being called
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")      # Final result

asyncio.run(main())
```

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Agentic loop: streams messages as Claude works
for await (const message of query({
  prompt: "Review utils.py for bugs that would cause crashes. Fix any issues you find.",
  options: {
    allowedTools: ["Read", "Edit", "Glob"],  // Tools Claude can use
    permissionMode: "acceptEdits"            // Auto-approve file edits
  }
})) {
  // Print human-readable output
  if (message.type === "assistant" && message.message?.content) {
    for (const block of message.message.content) {
      if ("text" in block) {
        console.log(block.text);             // Claude's reasoning
      } else if ("name" in block) {
        console.log(`Tool: ${block.name}`);  // Tool being called
      }
    }
  } else if (message.type === "result") {
    console.log(`Done: ${message.subtype}`); // Final result
  }
}
```
</CodeGroup>

Kode ini memiliki tiga bagian utama:

1. **`query`**: titik masuk utama yang membuat loop agentic. Ini mengembalikan iterator async, jadi Anda menggunakan `async for` untuk streaming pesan saat Claude bekerja. Lihat API lengkap di referensi SDK [Python](/docs/id/agent-sdk/python#query) atau [TypeScript](/docs/id/agent-sdk/typescript#query).

2. **`prompt`**: apa yang ingin Anda lakukan Claude. Claude mengetahui alat mana yang digunakan berdasarkan tugas.

3. **`options`**: konfigurasi untuk agen. Contoh ini menggunakan `allowedTools` untuk membatasi Claude ke `Read`, `Edit`, dan `Glob`, dan `permissionMode: "acceptEdits"` untuk auto-approve perubahan file. Opsi lainnya termasuk `systemPrompt`, `mcpServers`, dan lainnya. Lihat semua opsi untuk [Python](/docs/id/agent-sdk/python#claudeagentoptions) atau [TypeScript](/docs/id/agent-sdk/typescript#claudeagentoptions).

Loop `async for` terus berjalan saat Claude berpikir, memanggil alat, mengamati hasil, dan memutuskan apa yang harus dilakukan selanjutnya. Setiap iterasi menghasilkan pesan: penalaran Claude, panggilan alat, hasil alat, atau hasil akhir. SDK menangani orkestrasi (eksekusi alat, manajemen konteks, percobaan ulang) sehingga Anda hanya mengonsumsi aliran. Loop berakhir ketika Claude menyelesaikan tugas atau mengalami kesalahan.

Penanganan pesan di dalam loop memfilter output yang dapat dibaca manusia. Tanpa pemfilteran, Anda akan melihat objek pesan mentah termasuk inisialisasi sistem dan status internal, yang berguna untuk debugging tetapi berisik sebaliknya.

<Note>
Contoh ini menggunakan streaming untuk menampilkan kemajuan secara real-time. Jika Anda tidak memerlukan output langsung (misalnya untuk pekerjaan latar belakang atau pipeline CI), Anda dapat mengumpulkan semua pesan sekaligus. Lihat [Streaming vs. single-turn mode](/docs/id/agent-sdk/streaming-vs-single-mode) untuk detail.
</Note>

### Jalankan agen Anda

Agen Anda siap. Jalankan dengan perintah berikut:

<Tabs>
  <Tab title="Python">
    ```bash
    python3 agent.py
    ```
  </Tab>
  <Tab title="TypeScript">
    ```bash
    npx tsx agent.ts
    ```
  </Tab>
</Tabs>

Setelah menjalankan, periksa `utils.py`. Anda akan melihat kode defensif menangani daftar kosong dan pengguna null. Agen Anda secara mandiri:

1. **Membaca** `utils.py` untuk memahami kode
2. **Menganalisis** logika dan mengidentifikasi kasus tepi yang akan mogok
3. **Mengedit** file untuk menambahkan penanganan kesalahan yang tepat

Inilah yang membuat Agent SDK berbeda: Claude menjalankan alat secara langsung alih-alih meminta Anda untuk mengimplementasikannya.

<Note>
Jika Anda melihat "API key not found", pastikan Anda telah menetapkan variabel lingkungan `ANTHROPIC_API_KEY` di file `.env` atau lingkungan shell Anda. Lihat [panduan pemecahan masalah lengkap](https://code.claude.com/docs/id/troubleshooting) untuk bantuan lebih lanjut.
</Note>

### Coba prompt lain

Sekarang agen Anda sudah diatur, coba beberapa prompt berbeda:

- `"Add docstrings to all functions in utils.py"`
- `"Add type hints to all functions in utils.py"`
- `"Create a README.md documenting the functions in utils.py"`

### Sesuaikan agen Anda

Anda dapat mengubah perilaku agen dengan mengubah opsi. Berikut adalah beberapa contoh:

**Tambahkan kemampuan pencarian web:**

<CodeGroup>
```python Python
options=ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Glob", "WebSearch"],
    permission_mode="acceptEdits"
)
```

```typescript TypeScript
options: {
  allowedTools: ["Read", "Edit", "Glob", "WebSearch"],
  permissionMode: "acceptEdits"
}
```
</CodeGroup>

**Berikan Claude prompt sistem kustom:**

<CodeGroup>
```python Python
options=ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Glob"],
    permission_mode="acceptEdits",
    system_prompt="You are a senior Python developer. Always follow PEP 8 style guidelines."
)
```

```typescript TypeScript
options: {
  allowedTools: ["Read", "Edit", "Glob"],
  permissionMode: "acceptEdits",
  systemPrompt: "You are a senior Python developer. Always follow PEP 8 style guidelines."
}
```
</CodeGroup>

**Jalankan perintah di terminal:**

<CodeGroup>
```python Python
options=ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Glob", "Bash"],
    permission_mode="acceptEdits"
)
```

```typescript TypeScript
options: {
  allowedTools: ["Read", "Edit", "Glob", "Bash"],
  permissionMode: "acceptEdits"
}
```
</CodeGroup>

Dengan `Bash` diaktifkan, coba: `"Write unit tests for utils.py, run them, and fix any failures"`

## Konsep kunci

**Alat** mengontrol apa yang dapat dilakukan agen Anda:

| Alat | Apa yang dapat dilakukan agen |
|-------|----------------------|
| `Read`, `Glob`, `Grep` | Analisis hanya-baca |
| `Read`, `Edit`, `Glob` | Analisis dan modifikasi kode |
| `Read`, `Edit`, `Bash`, `Glob`, `Grep` | Otomasi penuh |

**Mode izin** mengontrol berapa banyak pengawasan manusia yang Anda inginkan:

| Mode | Perilaku | Kasus penggunaan |
|------|----------|----------|
| `acceptEdits` | Auto-approves file edits, asks for other actions | Alur kerja pengembangan terpercaya |
| `bypassPermissions` | Runs without prompts | Pipeline CI/CD, otomasi |
| `default` | Requires a `canUseTool` callback to handle approval | Alur persetujuan kustom |

Contoh di atas menggunakan mode `acceptEdits`, yang auto-approve operasi file sehingga agen dapat berjalan tanpa prompt interaktif. Jika Anda ingin meminta pengguna untuk persetujuan, gunakan mode `default` dan sediakan callback [`canUseTool`](/docs/id/agent-sdk/user-input) yang mengumpulkan input pengguna. Untuk kontrol lebih lanjut, lihat [Permissions](/docs/id/agent-sdk/permissions).

## Langkah berikutnya

Sekarang Anda telah membuat agen pertama Anda, pelajari cara memperluas kemampuannya dan menyesuaikannya dengan kasus penggunaan Anda:

- **[Permissions](/docs/id/agent-sdk/permissions)**: kontrol apa yang dapat dilakukan agen Anda dan kapan memerlukan persetujuan
- **[Hooks](/docs/id/agent-sdk/hooks)**: jalankan kode kustom sebelum atau sesudah panggilan alat
- **[Sessions](/docs/id/agent-sdk/sessions)**: bangun agen multi-turn yang mempertahankan konteks
- **[MCP servers](/docs/id/agent-sdk/mcp)**: terhubung ke database, browser, API, dan sistem eksternal lainnya
- **[Hosting](/docs/id/agent-sdk/hosting)**: deploy agen ke Docker, cloud, dan CI/CD
- **[Example agents](https://github.com/anthropics/claude-agent-sdk-demos)**: lihat contoh lengkap: asisten email, agen penelitian, dan lainnya