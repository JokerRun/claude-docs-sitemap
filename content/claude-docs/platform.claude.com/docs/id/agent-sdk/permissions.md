---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/permissions
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 8f2e424f30014bb00e32cc90582e0a2cc501a22ae1dd59e565d44bd6b427ff6c
---

# Konfigurasi izin

Kontrol bagaimana agen Anda menggunakan alat dengan mode izin, hook, dan aturan allow/deny deklaratif.

---

Claude Agent SDK menyediakan kontrol izin untuk mengelola bagaimana Claude menggunakan alat. Gunakan mode izin dan aturan untuk menentukan apa yang diizinkan secara otomatis, dan callback [`canUseTool`](/docs/id/agent-sdk/user-input) untuk menangani segalanya di runtime.

<Note>
Halaman ini mencakup mode izin dan aturan. Untuk membangun alur persetujuan interaktif di mana pengguna menyetujui atau menolak permintaan alat di runtime, lihat [Tangani persetujuan dan input pengguna](/docs/id/agent-sdk/user-input).
</Note>

## Bagaimana izin dievaluasi

Ketika Claude meminta alat, SDK memeriksa izin dalam urutan ini:

<Steps>
  <Step title="Hook">
    Jalankan [hook](/docs/id/agent-sdk/hooks) terlebih dahulu, yang dapat mengizinkan, menolak, atau melanjutkan ke langkah berikutnya
  </Step>
  <Step title="Aturan izin">
    Periksa aturan yang ditentukan dalam [settings.json](https://code.claude.com/docs/en/settings#permission-settings) dalam urutan ini: aturan `deny` terlebih dahulu (blokir terlepas dari aturan lain), kemudian aturan `allow` (izinkan jika cocok), kemudian aturan `ask` (minta persetujuan). Aturan deklaratif ini memungkinkan Anda untuk pra-menyetujui, memblokir, atau memerlukan persetujuan untuk alat tertentu tanpa menulis kode.
  </Step>
  <Step title="Mode izin">
    Terapkan [mode izin](#permission-modes) aktif (`bypassPermissions`, `acceptEdits`, `dontAsk`, dll.)
  </Step>
  <Step title="Callback canUseTool">
    Jika tidak diselesaikan oleh aturan atau mode, panggil callback [`canUseTool`](/docs/id/agent-sdk/user-input) Anda untuk keputusan
  </Step>
</Steps>

![Permission evaluation flow diagram](/docs/images/agent-sdk/permissions-flow.svg)

Halaman ini berfokus pada **mode izin** (langkah 3), konfigurasi statis yang mengontrol perilaku default. Untuk langkah-langkah lainnya:

- **Hook**: jalankan kode khusus untuk mengizinkan, menolak, atau memodifikasi permintaan alat. Lihat [Kontrol eksekusi dengan hook](/docs/id/agent-sdk/hooks).
- **Aturan izin**: konfigurasi aturan allow/deny deklaratif dalam `settings.json`. Lihat [Pengaturan izin](https://code.claude.com/docs/en/settings#permission-settings).
- **Callback canUseTool**: minta persetujuan pengguna di runtime. Lihat [Tangani persetujuan dan input pengguna](/docs/id/agent-sdk/user-input).

## Mode izin

Mode izin menyediakan kontrol global atas bagaimana Claude menggunakan alat. Anda dapat mengatur mode izin saat memanggil `query()` atau mengubahnya secara dinamis selama sesi streaming.

### Mode yang tersedia

SDK mendukung mode izin ini:

| Mode | Deskripsi | Perilaku alat |
| :--- | :---------- | :------------ |
| `default` | Perilaku izin standar | Tidak ada persetujuan otomatis; alat yang tidak cocok memicu callback `canUseTool` Anda |
| `acceptEdits` | Terima otomatis edit file | Edit file dan [operasi sistem file](#accept-edits-mode-acceptedits) (`mkdir`, `rm`, `mv`, dll.) disetujui secara otomatis |
| `bypassPermissions` | Lewati semua pemeriksaan izin | Semua alat berjalan tanpa prompt izin (gunakan dengan hati-hati) |
| `plan` | Mode perencanaan | Tidak ada eksekusi alat; Claude merencanakan tanpa membuat perubahan |

<Warning>
**Warisan subagen**: Saat menggunakan `bypassPermissions`, semua subagen mewarisi mode ini dan tidak dapat ditimpa. Subagen mungkin memiliki prompt sistem yang berbeda dan perilaku yang kurang terbatas daripada agen utama Anda. Mengaktifkan `bypassPermissions` memberikan mereka akses sistem penuh dan otonom tanpa prompt persetujuan apa pun.
</Warning>

### Atur mode izin

Anda dapat mengatur mode izin sekali saat memulai kueri, atau mengubahnya secara dinamis saat sesi aktif.

<Tabs>
  <Tab title="Pada waktu kueri">
    Lewatkan `permission_mode` (Python) atau `permissionMode` (TypeScript) saat membuat kueri. Mode ini berlaku untuk seluruh sesi kecuali diubah secara dinamis.

    <CodeGroup>

    ```python Python
    import asyncio
    from claude_agent_sdk import query, ClaudeAgentOptions

    async def main():
        async for message in query(
            prompt="Help me refactor this code",
            options=ClaudeAgentOptions(
                permission_mode="default",  # Set the mode here
            ),
        ):
            if hasattr(message, "result"):
                print(message.result)

    asyncio.run(main())
    ```

    ```typescript TypeScript
    import { query } from "@anthropic-ai/claude-agent-sdk";

    async function main() {
      for await (const message of query({
        prompt: "Help me refactor this code",
        options: {
          permissionMode: "default",  // Set the mode here
        },
      })) {
        if ("result" in message) {
          console.log(message.result);
        }
      }
    }

    main();
    ```

    </CodeGroup>
  </Tab>
  <Tab title="Selama streaming">
    Panggil `set_permission_mode()` (Python) atau `setPermissionMode()` (TypeScript) untuk mengubah mode di tengah sesi. Mode baru berlaku segera untuk semua permintaan alat berikutnya. Ini memungkinkan Anda untuk memulai dengan pembatasan dan melonggarkan izin seiring kepercayaan berkembang, misalnya beralih ke `acceptEdits` setelah meninjau pendekatan awal Claude.

    <CodeGroup>

    ```python Python
    import asyncio
    from claude_agent_sdk import query, ClaudeAgentOptions

    async def main():
        q = query(
            prompt="Help me refactor this code",
            options=ClaudeAgentOptions(
                permission_mode="default",  # Start in default mode
            ),
        )

        # Change mode dynamically mid-session
        await q.set_permission_mode("acceptEdits")

        # Process messages with the new permission mode
        async for message in q:
            if hasattr(message, "result"):
                print(message.result)

    asyncio.run(main())
    ```

    ```typescript TypeScript
    import { query } from "@anthropic-ai/claude-agent-sdk";

    async function main() {
      const q = query({
        prompt: "Help me refactor this code",
        options: {
          permissionMode: "default",  // Start in default mode
        },
      });

      // Change mode dynamically mid-session
      await q.setPermissionMode("acceptEdits");

      // Process messages with the new permission mode
      for await (const message of q) {
        if ("result" in message) {
          console.log(message.result);
        }
      }
    }

    main();
    ```

    </CodeGroup>
  </Tab>
</Tabs>

### Detail mode

#### Mode terima edit (`acceptEdits`)

Menyetujui operasi file secara otomatis sehingga Claude dapat mengedit kode tanpa meminta. Alat lain (seperti perintah Bash yang bukan operasi sistem file) masih memerlukan izin normal.

**Operasi yang disetujui otomatis:**
- Edit file (alat Edit, Write)
- Perintah sistem file: `mkdir`, `touch`, `rm`, `mv`, `cp`

**Gunakan saat:** Anda mempercayai edit Claude dan menginginkan iterasi lebih cepat, seperti selama prototyping atau saat bekerja di direktori terisolasi.

#### Mode lewati izin (`bypassPermissions`)

Menyetujui semua penggunaan alat tanpa prompt. Hook masih dijalankan dan dapat memblokir operasi jika diperlukan.

<Warning>
Gunakan dengan sangat hati-hati. Claude memiliki akses sistem penuh dalam mode ini. Hanya gunakan di lingkungan terkontrol di mana Anda mempercayai semua operasi yang mungkin.
</Warning>

#### Mode rencana (`plan`)

Mencegah eksekusi alat sepenuhnya. Claude dapat menganalisis kode dan membuat rencana tetapi tidak dapat membuat perubahan. Claude dapat menggunakan `AskUserQuestion` untuk memperjelas persyaratan sebelum menyelesaikan rencana. Lihat [Tangani persetujuan dan input pengguna](/docs/id/agent-sdk/user-input#handle-clarifying-questions) untuk menangani prompt ini.

**Gunakan saat:** Anda ingin Claude mengusulkan perubahan tanpa menjalankannya, seperti selama tinjauan kode atau ketika Anda perlu menyetujui perubahan sebelum dibuat.

## Sumber daya terkait

Untuk langkah-langkah lain dalam alur evaluasi izin:

- [Tangani persetujuan dan input pengguna](/docs/id/agent-sdk/user-input): prompt persetujuan interaktif dan pertanyaan klarifikasi
- [Panduan hook](/docs/id/agent-sdk/hooks): jalankan kode khusus di titik-titik kunci dalam siklus hidup agen
- [Aturan izin](https://code.claude.com/docs/en/settings#permission-settings): aturan allow/deny deklaratif dalam `settings.json`