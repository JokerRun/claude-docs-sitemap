---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool
fetched_at: 2026-03-27T03:10:39.282195Z
sha256: dd4f118321cef33e1c2d63c0f2d14a4161f8b0baa919edeaee3ed2dd8ff7362a
---

# Alat penggunaan komputer

Pelajari cara Claude berinteraksi dengan lingkungan desktop melalui alat penggunaan komputer, yang menyediakan kemampuan tangkapan layar dan kontrol mouse/keyboard.

---

Claude dapat berinteraksi dengan lingkungan komputer melalui alat penggunaan komputer, yang menyediakan kemampuan tangkapan layar dan kontrol mouse/keyboard untuk interaksi desktop otonom. Di [WebArena](https://webarena.dev/), sebuah tolok ukur untuk navigasi web otonom di berbagai situs web nyata, Claude mencapai hasil terdepan di antara sistem agen tunggal, menunjukkan kemampuan yang kuat untuk menyelesaikan tugas browser multi-langkah dari awal hingga akhir.

<Note>
Penggunaan komputer masih dalam versi beta dan memerlukan [header beta](/docs/id/api/beta-headers):
- `"computer-use-2025-11-24"` untuk Claude Opus 4.6, Claude Sonnet 4.6, Claude Opus 4.5
- `"computer-use-2025-01-24"` untuk Sonnet 4.5, Haiku 4.5, Opus 4.1, Sonnet 4, Opus 4, dan Sonnet 3.7 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations))

Hubungi kami melalui [formulir umpan balik](https://forms.gle/H6UFuXaaLywri9hz6) untuk berbagi masukan Anda tentang fitur ini.
</Note>

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

## Ikhtisar

Penggunaan komputer adalah fitur beta yang memungkinkan Claude berinteraksi dengan lingkungan desktop. Alat ini menyediakan:

- **Pengambilan tangkapan layar**: Melihat apa yang sedang ditampilkan di layar
- **Kontrol mouse**: Klik, seret, dan gerakkan kursor
- **Input keyboard**: Mengetik teks dan menggunakan pintasan keyboard
- **Otomasi desktop**: Berinteraksi dengan aplikasi atau antarmuka apa pun

Meskipun penggunaan komputer dapat ditingkatkan dengan alat lain seperti bash dan editor teks untuk alur kerja otomasi yang lebih komprehensif, penggunaan komputer secara khusus mengacu pada kemampuan alat penggunaan komputer untuk melihat dan mengontrol lingkungan desktop.

## Kompatibilitas model

Penggunaan komputer tersedia untuk model Claude berikut:

| Model | Versi Alat | Flag Beta |
|-------|--------------|-----------|
| Claude Opus 4.6, Claude Sonnet 4.6, Claude Opus 4.5 | `computer_20251124` | `computer-use-2025-11-24` |
| Semua model yang didukung lainnya | `computer_20250124` | `computer-use-2025-01-24` |

<Note>
Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Opus 4.5 memperkenalkan versi alat `computer_20251124` dengan kemampuan baru termasuk aksi zoom untuk inspeksi wilayah layar secara detail. Semua model lainnya (Sonnet 4.5, Haiku 4.5, Sonnet 4, Opus 4, Opus 4.1, dan Sonnet 3.7) menggunakan versi alat `computer_20250124`.
</Note>

<Warning>
Versi alat yang lebih lama tidak dijamin kompatibel ke belakang dengan model yang lebih baru. Selalu gunakan versi alat yang sesuai dengan versi model Anda.
</Warning>

## Pertimbangan keamanan

Penggunaan komputer adalah fitur beta dengan risiko unik yang berbeda dari fitur API standar. Risiko ini meningkat saat berinteraksi dengan internet.

<Warning>
Untuk meminimalkan risiko, pertimbangkan untuk mengambil tindakan pencegahan seperti:

1. Menggunakan mesin virtual atau kontainer khusus dengan hak istimewa minimal untuk mencegah serangan sistem langsung atau kecelakaan.
2. Menghindari pemberian akses model ke data sensitif, seperti informasi login akun, untuk mencegah pencurian informasi.
3. Membatasi akses internet ke daftar izin domain untuk mengurangi paparan terhadap konten berbahaya.
4. Meminta manusia untuk mengonfirmasi keputusan yang dapat mengakibatkan konsekuensi nyata yang berarti serta tugas apa pun yang memerlukan persetujuan afirmatif, seperti menerima cookie, melakukan transaksi keuangan, atau menyetujui ketentuan layanan.
</Warning>

Dalam beberapa keadaan, Claude akan mengikuti perintah yang ditemukan dalam konten meskipun bertentangan dengan instruksi pengguna. Misalnya, instruksi Claude di halaman web atau yang terdapat dalam gambar dapat mengesampingkan instruksi atau menyebabkan Claude membuat kesalahan. Ambil tindakan pencegahan untuk mengisolasi Claude dari data dan tindakan sensitif guna menghindari risiko terkait injeksi prompt.

Model telah dilatih untuk menolak injeksi prompt ini, dan lapisan pertahanan tambahan telah ditambahkan. Jika Anda menggunakan alat penggunaan komputer, pengklasifikasi akan secara otomatis berjalan pada prompt Anda untuk menandai potensi contoh injeksi prompt. Ketika pengklasifikasi ini mengidentifikasi potensi injeksi prompt dalam tangkapan layar, mereka akan secara otomatis mengarahkan model untuk meminta konfirmasi pengguna sebelum melanjutkan dengan tindakan berikutnya. Perlindungan tambahan ini tidak akan ideal untuk setiap kasus penggunaan (misalnya, kasus penggunaan tanpa manusia dalam loop), jadi jika Anda ingin memilih keluar dan mematikannya, silakan [hubungi dukungan](https://support.claude.com/en/).

Tindakan pencegahan ini tetap penting bahkan dengan lapisan pertahanan pengklasifikasi yang ada.

Informasikan pengguna akhir tentang risiko yang relevan dan dapatkan persetujuan mereka sebelum mengaktifkan penggunaan komputer di produk Anda sendiri.

<Card
  title="Implementasi referensi penggunaan komputer"
  icon="computer"
  href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo"
>

Mulai dengan cepat menggunakan implementasi referensi penggunaan komputer yang mencakup antarmuka web, kontainer Docker, contoh implementasi alat, dan loop agen.

**Catatan:** Implementasi telah diperbarui untuk menyertakan alat baru untuk model Claude 4 dan Claude Sonnet 3.7. Pastikan untuk mengambil versi terbaru dari repo untuk mengakses fitur-fitur baru ini.

</Card>

<Tip>
  Gunakan [formulir ini](https://forms.gle/BT1hpBrqDPDUrCqo7) untuk memberikan
  umpan balik tentang kualitas respons model, API itu sendiri, atau kualitas
  dokumentasi.
</Tip>

## Mulai cepat

Berikut cara memulai dengan penggunaan komputer:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: computer-use-2025-11-24" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "tools": [
      {
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": 1024,
        "display_height_px": 768,
        "display_number": 1
      },
      {
        "type": "text_editor_20250728",
        "name": "str_replace_based_edit_tool"
      },
      {
        "type": "bash_20250124",
        "name": "bash"
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "Save a picture of a cat to my desktop."
      }
    ]
  }'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-6",  # or another compatible model
    max_tokens=1024,
    tools=[
        {
            "type": "computer_20251124",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
            "display_number": 1,
        },
        {"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"},
        {"type": "bash_20250124", "name": "bash"},
    ],
    messages=[{"role": "user", "content": "Save a picture of a cat to my desktop."}],
    betas=["computer-use-2025-11-24"],
)
print(response)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [
    {
      type: "computer_20251124",
      name: "computer",
      display_width_px: 1024,
      display_height_px: 768,
      display_number: 1
    },
    {
      type: "text_editor_20250728",
      name: "str_replace_based_edit_tool"
    },
    {
      type: "bash_20250124",
      name: "bash"
    }
  ],
  messages: [{ role: "user", content: "Save a picture of a cat to my desktop." }],
  betas: ["computer-use-2025-11-24"]
});

console.log(response);
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        var client = new AnthropicClient();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_6,
            MaxTokens = 1024,
            Tools = new BetaToolUnion[]
            {
                new BetaToolComputerUse20251124
                {
                    DisplayWidthPx = 1024,
                    DisplayHeightPx = 768,
                    DisplayNumber = 1
                },
                new BetaToolTextEditor20250728(),
                new BetaToolBash20250124()
            },
            Messages = new[]
            {
                new BetaMessageParam
                {
                    Role = Role.User,
                    Content = "Save a picture of a cat to my desktop."
                }
            },
            Betas = new[] { "computer-use-2025-11-24" }
        };

        var response = await client.Beta.Messages.Create(parameters);
        Console.WriteLine(response);
    }
}
```

```go Go nocheck hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_6,
		MaxTokens: 1024,
		Tools: []anthropic.BetaToolUnionParam{
			{OfComputerUseTool20251124: &anthropic.BetaToolComputerUse20251124Param{
				DisplayWidthPx:  1024,
				DisplayHeightPx: 768,
				DisplayNumber:   anthropic.Int(1),
			}},
			{OfTextEditor20250728: &anthropic.BetaToolTextEditor20250728Param{}},
			{OfBashTool20250124: &anthropic.BetaToolBash20250124Param{}},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Save a picture of a cat to my desktop.")),
		},
		Betas: []anthropic.AnthropicBeta{
			anthropic.AnthropicBetaComputerUse2025_11_24,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..3,7..10,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaToolBash20250124;
import com.anthropic.models.beta.messages.BetaToolComputerUse20251124;
import com.anthropic.models.beta.messages.BetaToolTextEditor20250728;
import com.anthropic.models.beta.messages.MessageCreateParams;

public class ComputerUseExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-opus-4-6")
            .maxTokens(1024L)
            .addTool(BetaToolComputerUse20251124.builder()
                .displayWidthPx(1024L)
                .displayHeightPx(768L)
                .displayNumber(1L)
                .build())
            .addTool(BetaToolTextEditor20250728.builder().build())
            .addTool(BetaToolBash20250124.builder().build())
            .addUserMessage("Save a picture of a cat to my desktop.")
            .addBeta("computer-use-2025-11-24")
            .build();

        BetaMessage response = client.beta().messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->beta->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Save a picture of a cat to my desktop.'],
    ],
    model: 'claude-opus-4-6',
    tools: [
        [
            'type' => 'computer_20251124',
            'name' => 'computer',
            'display_width_px' => 1024,
            'display_height_px' => 768,
            'display_number' => 1,
        ],
        [
            'type' => 'text_editor_20250728',
            'name' => 'str_replace_based_edit_tool',
        ],
        [
            'type' => 'bash_20250124',
            'name' => 'bash',
        ],
    ],
    betas: ['computer-use-2025-11-24'],
);

echo $response;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [
    {
      type: "computer_20251124",
      name: "computer",
      display_width_px: 1024,
      display_height_px: 768,
      display_number: 1
    },
    {
      type: "text_editor_20250728",
      name: "str_replace_based_edit_tool"
    },
    {
      type: "bash_20250124",
      name: "bash"
    }
  ],
  messages: [
    { role: "user", content: "Save a picture of a cat to my desktop." }
  ],
  betas: ["computer-use-2025-11-24"]
)

puts response
```
</CodeGroup>

<Note>
Header beta hanya diperlukan untuk alat penggunaan komputer.

Contoh di atas menunjukkan ketiga alat yang digunakan bersama, yang memerlukan header beta karena mencakup alat penggunaan komputer.
</Note>

---

## Cara kerja penggunaan komputer

<Steps>
  <Step
    title="Berikan Claude alat penggunaan komputer dan prompt pengguna"
    icon="tool"
  >
    - Tambahkan alat penggunaan komputer (dan opsional alat lainnya) ke permintaan API Anda.
    - Sertakan prompt pengguna yang memerlukan interaksi desktop, misalnya, "Simpan gambar kucing ke desktop saya."
  </Step>
  <Step title="Claude memutuskan untuk menggunakan alat penggunaan komputer" icon="wrench">
    - Claude menilai apakah alat penggunaan komputer dapat membantu dengan kueri pengguna.
    - Jika ya, Claude membuat permintaan penggunaan alat yang diformat dengan benar.
    - Respons API memiliki `stop_reason` berupa `tool_use`, menandakan niat Claude.
  </Step>
  <Step
    title="Ekstrak input alat, evaluasi alat di komputer, dan kembalikan hasilnya"
    icon="computer"
  >
    - Di pihak Anda, ekstrak nama alat dan input dari permintaan Claude.
    - Gunakan alat di kontainer atau Mesin Virtual.
    - Lanjutkan percakapan dengan pesan `user` baru yang berisi blok konten `tool_result`.
  </Step>
  <Step
    title="Claude terus memanggil alat penggunaan komputer hingga tugas selesai"
    icon="arrows-clockwise"
  >
    - Claude menganalisis hasil alat untuk menentukan apakah diperlukan penggunaan alat lebih lanjut atau tugas telah selesai.
    - Jika Claude memutuskan perlu alat lain, ia merespons dengan `stop_reason` `tool_use` lainnya dan Anda harus kembali ke langkah 3.
    - Jika tidak, ia membuat respons teks untuk pengguna.
  </Step>
</Steps>

Pengulangan langkah 3 dan 4 tanpa input pengguna disebut sebagai "loop agen" (yaitu, Claude merespons dengan permintaan penggunaan alat dan aplikasi Anda merespons Claude dengan hasil evaluasi permintaan tersebut).

### Lingkungan komputasi

Penggunaan komputer memerlukan lingkungan komputasi yang terisolasi di mana Claude dapat berinteraksi dengan aman dengan aplikasi dan web. Lingkungan ini mencakup:

1. **Tampilan virtual**: Server tampilan X11 virtual (menggunakan Xvfb) yang merender antarmuka desktop yang akan dilihat Claude melalui tangkapan layar dan dikontrol dengan tindakan mouse/keyboard.

2. **Lingkungan desktop**: UI ringan dengan manajer jendela (Mutter) dan panel (Tint2) yang berjalan di Linux, yang menyediakan antarmuka grafis yang konsisten bagi Claude untuk berinteraksi.

3. **Aplikasi**: Aplikasi Linux yang sudah terinstal seperti Firefox, LibreOffice, editor teks, dan manajer file yang dapat digunakan Claude untuk menyelesaikan tugas.

4. **Implementasi alat**: Kode integrasi yang menerjemahkan permintaan alat abstrak Claude (seperti "gerakkan mouse" atau "ambil tangkapan layar") menjadi operasi aktual di lingkungan virtual.

5. **Loop agen**: Program yang menangani komunikasi antara Claude dan lingkungan, mengirimkan tindakan Claude ke lingkungan dan mengembalikan hasilnya (tangkapan layar, output perintah) kembali ke Claude.

Saat Anda menggunakan penggunaan komputer, Claude tidak terhubung langsung ke lingkungan ini. Sebaliknya, aplikasi Anda:

1. Menerima permintaan penggunaan alat Claude
2. Menerjemahkannya menjadi tindakan di lingkungan komputasi Anda
3. Menangkap hasilnya (tangkapan layar, output perintah, dll.)
4. Mengembalikan hasil ini ke Claude

Untuk keamanan dan isolasi, implementasi referensi menjalankan semua ini di dalam kontainer Docker dengan pemetaan port yang sesuai untuk melihat dan berinteraksi dengan lingkungan.

---

## Cara mengimplementasikan penggunaan komputer

### Mulai dengan implementasi referensi

[Implementasi referensi](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) tersedia yang mencakup semua yang Anda butuhkan untuk memulai dengan cepat menggunakan penggunaan komputer:

- [Lingkungan terkontainerisasi](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/Dockerfile) yang cocok untuk penggunaan komputer dengan Claude
- Implementasi [alat penggunaan komputer](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo/computer_use_demo/tools)
- [Loop agen](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/computer_use_demo/loop.py) yang berinteraksi dengan API Claude dan mengeksekusi alat penggunaan komputer
- Antarmuka web untuk berinteraksi dengan kontainer, loop agen, dan alat.

### Memahami loop multi-agen

Inti dari penggunaan komputer adalah "loop agen" - siklus di mana Claude meminta tindakan alat, aplikasi Anda mengeksekusinya, dan mengembalikan hasilnya ke Claude. Berikut contoh yang disederhanakan:

```python nocheck
async def sampling_loop(
    *,
    model: str,
    messages: list[dict],
    api_key: str,
    max_tokens: int = 4096,
    tool_version: str,
    thinking_budget: int | None = None,
    max_iterations: int = 10,  # Add iteration limit to prevent infinite loops
):
    """
    A simple agent loop for Claude computer use interactions.

    This function handles the back-and-forth between:
    1. Sending user messages to Claude
    2. Claude requesting to use tools
    3. Your app executing those tools
    4. Sending tool results back to Claude
    """
    # Set up tools and API parameters
    client = Anthropic(api_key=api_key)
    beta_flag = (
        "computer-use-2025-11-24"
        if "20251124" in tool_version
        else "computer-use-2025-01-24"
        if "20250124" in tool_version
        else "computer-use-2024-10-22"
    )

    # Configure tools - you should already have these initialized elsewhere
    tools = [
        {
            "type": f"computer_{tool_version}",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
        },
        {"type": f"text_editor_{tool_version}", "name": "str_replace_editor"},
        {"type": f"bash_{tool_version}", "name": "bash"},
    ]

    # Main agent loop (with iteration limit to prevent runaway API costs)
    iterations = 0
    while True and iterations < max_iterations:
        iterations += 1
        # Set up optional thinking parameter (for Claude Sonnet 3.7)
        thinking = None
        if thinking_budget:
            thinking = {"type": "enabled", "budget_tokens": thinking_budget}

        # Call the Claude API
        response = client.beta.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
            tools=tools,
            betas=[beta_flag],
            thinking=thinking,
        )

        # Add Claude's response to the conversation history
        response_content = response.content
        messages.append({"role": "assistant", "content": response_content})

        # Check if Claude used any tools
        tool_results = []
        for block in response_content:
            if block.type == "tool_use":
                # In a real app, you would execute the tool here
                # For example: result = run_tool(block.name, block.input)
                result = {"result": "Tool executed successfully"}

                # Format the result for Claude
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": result}
                )

        # If no tools were used, Claude is done - return the final messages
        if not tool_results:
            return messages

        # Add tool results to messages for the next iteration with Claude
        messages.append({"role": "user", "content": tool_results})
```

Loop berlanjut hingga Claude merespons tanpa meminta alat apa pun (penyelesaian tugas) atau batas iterasi maksimum tercapai. Pengaman ini mencegah potensi loop tak terbatas yang dapat mengakibatkan biaya API yang tidak terduga.

Coba implementasi referensi sebelum membaca sisa dokumentasi ini.

### Optimalkan performa model dengan prompting

Berikut beberapa tips tentang cara mendapatkan output berkualitas terbaik:

1. Tentukan tugas yang sederhana dan terdefinisi dengan baik serta berikan instruksi eksplisit untuk setiap langkah.
2. Claude terkadang mengasumsikan hasil tindakannya tanpa secara eksplisit memeriksa hasilnya. Untuk mencegah ini, Anda dapat meminta Claude dengan `After each step, take a screenshot and carefully evaluate if you have achieved the right outcome. Explicitly show your thinking: "I have evaluated step X..." If not correct, try again. Only when you confirm a step was executed correctly should you move on to the next one.`
3. Beberapa elemen UI (seperti dropdown dan scrollbar) mungkin sulit bagi Claude untuk dimanipulasi menggunakan gerakan mouse. Jika Anda mengalami ini, coba minta model untuk menggunakan pintasan keyboard.
4. Untuk tugas yang dapat diulang atau interaksi UI, sertakan contoh tangkapan layar dan panggilan alat dari hasil yang berhasil dalam prompt Anda.
5. Jika Anda perlu model untuk masuk, berikan nama pengguna dan kata sandi dalam prompt Anda di dalam tag xml seperti `<robot_credentials>`. Menggunakan penggunaan komputer dalam aplikasi yang memerlukan login meningkatkan risiko hasil yang buruk akibat injeksi prompt. Tinjau [panduan tentang mitigasi injeksi prompt](/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) sebelum memberikan kredensial login kepada model.

<Tip>
  Jika Anda berulang kali menemukan serangkaian masalah yang jelas atau mengetahui sebelumnya tugas
  yang perlu diselesaikan Claude, gunakan system prompt untuk memberikan Claude
  tips atau instruksi eksplisit tentang cara menyelesaikan tugas dengan sukses.
</Tip>

<Tip>
  Untuk agen yang mencakup beberapa sesi, jalankan verifikasi end-to-end di
  awal setiap sesi, bukan hanya setelah implementasi. Pemeriksaan berbasis browser
  menangkap regresi dari sesi sebelumnya yang tidak terdeteksi oleh tinjauan tingkat kode saja. Lihat
  [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  untuk detailnya.
</Tip>

### System prompt

Ketika salah satu alat yang didefinisikan oleh Anthropic diminta melalui API Claude, system prompt khusus penggunaan komputer dibuat. Ini mirip dengan [system prompt penggunaan alat](/docs/id/agents-and-tools/tool-use/implement-tool-use#tool-use-system-prompt) tetapi dimulai dengan:

> You have access to a set of functions you can use to answer the user's question. This includes access to a sandboxed computing environment. You do NOT currently have the ability to inspect files or interact with external resources, except by invoking the below functions.

Seperti halnya penggunaan alat biasa, bidang `system_prompt` yang disediakan pengguna tetap dihormati dan digunakan dalam konstruksi system prompt gabungan.

### Tindakan yang tersedia

Alat penggunaan komputer mendukung tindakan-tindakan berikut:

**Tindakan dasar (semua versi)**
- **screenshot** - Mengambil tampilan saat ini
- **left_click** - Klik pada koordinat `[x, y]`
- **type** - Mengetik string teks
- **key** - Menekan tombol atau kombinasi tombol (misalnya, "ctrl+s")
- **mouse_move** - Memindahkan kursor ke koordinat

**Tindakan yang ditingkatkan (`computer_20250124`)**
Tersedia di model Claude 4 dan Claude Sonnet 3.7:
- **scroll** - Gulir ke arah mana pun dengan kontrol jumlah
- **left_click_drag** - Klik dan seret antara koordinat
- **right_click**, **middle_click** - Tombol mouse tambahan
- **double_click**, **triple_click** - Beberapa klik
- **left_mouse_down**, **left_mouse_up** - Kontrol klik yang lebih halus
- **hold_key** - Tahan tombol selama durasi tertentu (dalam detik)
- **wait** - Jeda antara tindakan

**Tindakan yang ditingkatkan (`computer_20251124`)**
Tersedia di Claude Opus 4.6 dan Claude Opus 4.5:
- Semua tindakan dari `computer_20250124`
- **zoom** - Melihat wilayah layar tertentu pada resolusi penuh. Memerlukan `enable_zoom: true` dalam definisi alat. Mengambil parameter `region` dengan koordinat `[x1, y1, x2, y2]` yang mendefinisikan sudut kiri atas dan kanan bawah area yang akan diperiksa.

<section title="Contoh tindakan">

Ambil tangkapan layar:

```json
{
  "action": "screenshot"
}
```

Klik pada posisi:

```json
{
  "action": "left_click",
  "coordinate": [500, 300]
}
```

Ketik teks:

```json
{
  "action": "type",
  "text": "Hello, world!"
}
```

Gulir ke bawah (Claude 4/3.7):

```json
{
  "action": "scroll",
  "coordinate": [500, 400],
  "scroll_direction": "down",
  "scroll_amount": 3
}
```

Zoom untuk melihat wilayah secara detail (Opus 4.5):

```json
{
  "action": "zoom",
  "region": [100, 200, 400, 350]
}
```

</section>

<section title="Tombol modifier dengan tindakan klik dan gulir">

Untuk menahan tombol modifier (seperti Shift, Ctrl, atau Alt) saat melakukan tindakan klik atau gulir, gunakan parameter `text` pada tindakan tersebut. Ini berbeda dari `hold_key`, yang hanya menahan tombol selama durasi tanpa melakukan tindakan lain.

Shift+klik (misalnya, untuk memilih rentang item):

```json
{
  "action": "left_click",
  "coordinate": [500, 300],
  "text": "shift"
}
```

Ctrl+klik (misalnya, untuk multi-pilih di Windows/Linux):

```json
{
  "action": "left_click",
  "coordinate": [500, 300],
  "text": "ctrl"
}
```

Cmd+klik (misalnya, untuk multi-pilih di macOS):

```json
{
  "action": "left_click",
  "coordinate": [500, 300],
  "text": "super"
}
```

Shift+gulir (misalnya, untuk gulir horizontal):

```json
{
  "action": "scroll",
  "coordinate": [500, 400],
  "scroll_direction": "down",
  "scroll_amount": 3,
  "text": "shift"
}
```

Parameter `text` dalam tindakan klik/gulir menerima tombol modifier seperti `shift`, `ctrl`, `alt`, dan `super` (untuk tombol Command/Windows).

</section>

### Parameter alat

| Parameter | Diperlukan | Deskripsi |
|-----------|----------|-------------|
| `type` | Ya | Versi alat (`computer_20251124`, `computer_20250124`, atau `computer_20241022`) |
| `name` | Ya | Harus "computer" |
| `display_width_px` | Ya | Lebar tampilan dalam piksel |
| `display_height_px` | Ya | Tinggi tampilan dalam piksel |
| `display_number` | Tidak | Nomor tampilan untuk lingkungan X11 |
| `enable_zoom` | Tidak | Aktifkan aksi zoom (hanya `computer_20251124`). Atur ke `true` untuk mengizinkan Claude memperbesar wilayah layar tertentu. Default: `false` |

<Note>
**Penting:** Alat penggunaan komputer harus dieksekusi secara eksplisit oleh aplikasi Anda - Claude tidak dapat mengeksekusinya secara langsung. Anda bertanggung jawab untuk mengimplementasikan pengambilan tangkapan layar, gerakan mouse, input keyboard, dan tindakan lainnya berdasarkan permintaan Claude.
</Note>

### Aktifkan kemampuan berpikir di model Claude 4 dan Claude Sonnet 3.7

Claude Sonnet 3.7 memperkenalkan kemampuan "berpikir" baru yang memungkinkan Anda melihat proses penalaran model saat mengerjakan tugas-tugas kompleks. Fitur ini membantu Anda memahami bagaimana Claude mendekati suatu masalah dan dapat sangat berharga untuk tujuan debugging atau pendidikan.

Untuk mengaktifkan berpikir, tambahkan parameter `thinking` ke permintaan API Anda:

```json hidelines={1,-1}
{
  "thinking": {
    "type": "enabled",
    "budget_tokens": 1024
  }
}
```

Parameter `budget_tokens` menentukan berapa banyak token yang dapat digunakan Claude untuk berpikir. Ini dikurangi dari anggaran `max_tokens` keseluruhan Anda.

Ketika berpikir diaktifkan, Claude akan mengembalikan proses penalarannya sebagai bagian dari respons, yang dapat membantu Anda:

1. Memahami proses pengambilan keputusan model
2. Mengidentifikasi potensi masalah atau kesalahpahaman
3. Belajar dari pendekatan Claude dalam pemecahan masalah
4. Mendapatkan visibilitas lebih besar ke dalam operasi multi-langkah yang kompleks

Berikut contoh tampilan output berpikir:

```text
[Thinking]
I need to save a picture of a cat to the desktop. Let me break this down into steps:

1. First, I'll take a screenshot to see what's on the desktop
2. Then I'll look for a web browser to search for cat images
3. After finding a suitable image, I'll need to save it to the desktop

Let me start by taking a screenshot to see what's available...
```

### Menggabungkan penggunaan komputer dengan alat lain

Alat penggunaan komputer dapat dikombinasikan dengan alat lain untuk membuat alur kerja otomatisasi yang lebih canggih. Ini sangat berguna ketika Anda perlu:
- Menjalankan perintah sistem ([alat bash](/docs/id/agents-and-tools/tool-use/bash-tool))
- Mengedit file konfigurasi atau skrip ([alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool))
- Mengintegrasikan dengan API atau layanan kustom (alat kustom)

<CodeGroup>
  ```bash Shell
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: computer-use-2025-11-24" \
    -d '{
      "model": "claude-opus-4-6",
      "max_tokens": 2000,
      "tools": [
        {
          "type": "computer_20251124",
          "name": "computer",
          "display_width_px": 1024,
          "display_height_px": 768,
          "display_number": 1
        },
        {
          "type": "text_editor_20250728",
          "name": "str_replace_based_edit_tool"
        },
        {
          "type": "bash_20250124",
          "name": "bash"
        },
        {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              },
              "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
              }
            },
            "required": ["location"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Find flights from San Francisco to a place with warmer weather."
        }
      ],
      "thinking": {
        "type": "enabled",
        "budget_tokens": 1024
      }
    }'
  ```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=2000,
    tools=[
        {
            "type": "computer_20251124",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
            "display_number": 1,
        },
        {"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"},
        {"type": "bash_20250124", "name": "bash"},
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature, either 'celsius' or 'fahrenheit'",
                    },
                },
                "required": ["location"],
            },
        },
    ],
    messages=[
        {
            "role": "user",
            "content": "Find flights from San Francisco to a place with warmer weather.",
        }
    ],
    betas=["computer-use-2025-11-24"],
    thinking={"type": "enabled", "budget_tokens": 1024},
)
print(response)
```

  ```typescript TypeScript hidelines={1..2}
  import Anthropic from "@anthropic-ai/sdk";

  const anthropic = new Anthropic();

  const message = await anthropic.beta.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 4096,
    tools: [
      {
        type: "computer_20251124",
        name: "computer",
        display_width_px: 1024,
        display_height_px: 768,
        display_number: 1
      },
      {
        type: "text_editor_20250728",
        name: "str_replace_based_edit_tool"
      },
      {
        type: "bash_20250124",
        name: "bash"
      },
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            },
            unit: {
              type: "string",
              enum: ["celsius", "fahrenheit"],
              description: "The unit of temperature, either 'celsius' or 'fahrenheit'"
            }
          },
          required: ["location"]
        }
      }
    ],
    messages: [
      {
        role: "user",
        content: "Find flights from San Francisco to a place with warmer weather."
      }
    ],
    betas: ["computer-use-2025-11-24"],
    thinking: { type: "enabled", budget_tokens: 1024 }
  });
  console.log(message);
  ```

  
  ```csharp C# nocheck
  using System;
  using System.Collections.Generic;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Beta.Messages;

  public class Program
  {
      public static async Task Main(string[] args)
      {
          AnthropicClient client = new()
          {
              ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
          };

          var parameters = new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_6,
              MaxTokens = 2000,
              Tools = new BetaToolUnion[]
              {
                  new BetaToolComputerUse20251124
                  {
                      DisplayWidthPx = 1024,
                      DisplayHeightPx = 768,
                      DisplayNumber = 1
                  },
                  new BetaToolTextEditor20250728(),
                  new BetaToolBash20250124(),
                  new BetaTool
                  {
                      Name = "get_weather",
                      Description = "Get the current weather in a given location",
                      InputSchema = new InputSchema
                      {
                          Properties = new Dictionary<string, JsonElement>
                          {
                              ["location"] = JsonSerializer.SerializeToElement(new
                              {
                                  type = "string",
                                  description = "The city and state, e.g. San Francisco, CA"
                              }),
                              ["unit"] = JsonSerializer.SerializeToElement(new
                              {
                                  type = "string",
                                  @enum = new[] { "celsius", "fahrenheit" },
                                  description = "The unit of temperature, either 'celsius' or 'fahrenheit'"
                              })
                          },
                          Required = ["location"]
                      }
                  }
              },
              Messages = new BetaMessageParam[]
              {
                  new()
                  {
                      Role = Role.User,
                      Content = "Find flights from San Francisco to a place with warmer weather."
                  }
              },
              Betas = ["computer-use-2025-11-24"],
              Thinking = new BetaThinkingConfigParam(new BetaThinkingConfigEnabled(1024))
          };

          var message = await client.Beta.Messages.Create(parameters);
          Console.WriteLine(message);
      }
  }
  ```

  
  ```go Go nocheck hidelines={1..11,-1}
  package main

  import (
  	"context"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	client := anthropic.NewClient()

  	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_6,
  		MaxTokens: 16384,
  		Tools: []anthropic.BetaToolUnionParam{
  			{OfComputerUseTool20251124: &anthropic.BetaToolComputerUse20251124Param{
  				DisplayWidthPx:  1024,
  				DisplayHeightPx: 768,
  				DisplayNumber:   anthropic.Int(1),
  			}},
  			{OfTextEditor20250728: &anthropic.BetaToolTextEditor20250728Param{}},
  			{OfBashTool20250124: &anthropic.BetaToolBash20250124Param{}},
  			{OfTool: &anthropic.BetaToolParam{
  				Name:        "get_weather",
  				Description: anthropic.String("Get the current weather in a given location"),
  				InputSchema: anthropic.BetaToolInputSchemaParam{
  					Properties: map[string]any{
  						"location": map[string]any{
  							"type":        "string",
  							"description": "The city and state, e.g. San Francisco, CA",
  						},
  						"unit": map[string]any{
  							"type":        "string",
  							"enum":        []string{"celsius", "fahrenheit"},
  							"description": "The unit of temperature, either 'celsius' or 'fahrenheit'",
  						},
  					},
  					Required: []string{"location"},
  				},
  			}},
  		},
  		Messages: []anthropic.BetaMessageParam{
  			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Find flights from San Francisco to a place with warmer weather.")),
  		},
  		Thinking: anthropic.BetaThinkingConfigParamOfEnabled(1024),
  		Betas:    []anthropic.AnthropicBeta{anthropic.AnthropicBetaComputerUse2025_11_24},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  	fmt.Println(response)
  }
  ```

```java Java hidelines={1..5,9..15,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaTool;
import com.anthropic.models.beta.messages.BetaToolBash20250124;
import com.anthropic.models.beta.messages.BetaToolComputerUse20251124;
import com.anthropic.models.beta.messages.BetaToolTextEditor20250728;
import com.anthropic.models.beta.messages.MessageCreateParams;
import java.util.List;
import java.util.Map;

public class MultipleToolsExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
      .model("claude-opus-4-6")
      .maxTokens(16384L)
      .addTool(
        BetaToolComputerUse20251124.builder()
          .displayWidthPx(1024L)
          .displayHeightPx(768L)
          .displayNumber(1L)
          .build()
      )
      .addTool(BetaToolTextEditor20250728.builder().build())
      .addTool(BetaToolBash20250124.builder().build())
      .addTool(
        BetaTool.builder()
          .name("get_weather")
          .description("Get the current weather in a given location")
          .inputSchema(
            BetaTool.InputSchema.builder()
              .properties(
                BetaTool.InputSchema.Properties.builder()
                  .putAdditionalProperty(
                    "location",
                    JsonValue.from(
                      Map.of(
                        "type", "string",
                        "description", "The city and state, e.g. San Francisco, CA"
                      )
                    )
                  )
                  .putAdditionalProperty(
                    "unit",
                    JsonValue.from(
                      Map.of(
                        "type", "string",
                        "enum", List.of("celsius", "fahrenheit"),
                        "description", "The unit of temperature, either 'celsius' or 'fahrenheit'"
                      )
                    )
                  )
                  .build()
              )
              .build()
          )
          .build()
      )
      .enabledThinking(1024L)
      .addUserMessage("Find flights from San Francisco to a place with warmer weather.")
      .addBeta("computer-use-2025-11-24")
      .build();

    BetaMessage message = client.beta().messages().create(params);
    System.out.println(message);
  }
}
```

  
  ```php PHP hidelines={1..4} nocheck
  <?php

  use Anthropic\Client;

  $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

  $message = $client->beta->messages->create(
      maxTokens: 2000,
      messages: [
          ['role' => 'user', 'content' => 'Find flights from San Francisco to a place with warmer weather.'],
      ],
      model: 'claude-opus-4-6',
      tools: [
          [
              'type' => 'computer_20251124',
              'name' => 'computer',
              'display_width_px' => 1024,
              'display_height_px' => 768,
              'display_number' => 1,
          ],
          [
              'type' => 'text_editor_20250728',
              'name' => 'str_replace_based_edit_tool',
          ],
          [
              'type' => 'bash_20250124',
              'name' => 'bash',
          ],
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather in a given location',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'The city and state, e.g. San Francisco, CA',
                      ],
                      'unit' => [
                          'type' => 'string',
                          'enum' => ['celsius', 'fahrenheit'],
                          'description' => 'The unit of temperature, either \'celsius\' or \'fahrenheit\'',
                      ],
                  ],
                  'required' => ['location'],
              ],
          ],
      ],
      betas: ['computer-use-2025-11-24'],
      thinking: ['type' => 'enabled', 'budget_tokens' => 1024],
  );

  echo $message;
  ```

  ```ruby Ruby hidelines={1..2}
    require "anthropic"

    client = Anthropic::Client.new

    message = client.beta.messages.create(
      model: "claude-opus-4-6",
      max_tokens: 2000,
      tools: [
        {
          type: "computer_20251124",
          name: "computer",
          display_width_px: 1024,
          display_height_px: 768,
          display_number: 1
        },
        {
          type: "text_editor_20250728",
          name: "str_replace_based_edit_tool"
        },
        {
          type: "bash_20250124",
          name: "bash"
        },
        {
          name: "get_weather",
          description: "Get the current weather in a given location",
          input_schema: {
            type: "object",
            properties: {
              location: {
                type: "string",
                description: "The city and state, e.g. San Francisco, CA"
              },
              unit: {
                type: "string",
                enum: ["celsius", "fahrenheit"],
                description: "The unit of temperature, either 'celsius' or 'fahrenheit'"
              }
            },
            required: ["location"]
          }
        }
      ],
      messages: [
        {
          role: "user",
          content: "Find flights from San Francisco to a place with warmer weather."
        }
      ],
      betas: ["computer-use-2025-11-24"],
      thinking: {
        type: "enabled",
        budget_tokens: 1024
      }
    )
    puts message
  ```
</CodeGroup>

### Membangun lingkungan penggunaan komputer kustom

[Implementasi referensi](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) dimaksudkan untuk membantu Anda memulai penggunaan komputer. Ini mencakup semua komponen yang diperlukan agar Claude dapat menggunakan komputer. Namun, Anda dapat membangun lingkungan Anda sendiri untuk penggunaan komputer sesuai kebutuhan Anda. Anda akan memerlukan:

- Lingkungan virtual atau terkontainer yang sesuai untuk penggunaan komputer dengan Claude
- Implementasi setidaknya satu alat penggunaan komputer yang didefinisikan oleh Anthropic
- Loop agen yang berinteraksi dengan API Claude dan menjalankan hasil `tool_use` menggunakan implementasi alat Anda
- API atau UI yang memungkinkan input pengguna untuk memulai loop agen

#### Mengimplementasikan alat penggunaan komputer

Alat penggunaan komputer diimplementasikan sebagai alat tanpa skema. Saat menggunakan alat ini, Anda tidak perlu menyediakan skema input seperti alat lainnya; skema sudah tertanam dalam model Claude dan tidak dapat dimodifikasi.

<Steps>
  <Step title="Siapkan lingkungan komputasi Anda">
    Buat tampilan virtual atau sambungkan ke tampilan yang sudah ada yang akan berinteraksi dengan Claude. Ini biasanya melibatkan pengaturan Xvfb (X Virtual Framebuffer) atau teknologi serupa.
  </Step>
  <Step title="Implementasikan penangan aksi">
    Buat fungsi untuk menangani setiap jenis aksi yang mungkin diminta Claude:
    
    ```python nocheck
    def handle_computer_action(action_type, params):
        if action_type == "screenshot":
            return capture_screenshot()
        elif action_type == "left_click":
            x, y = params["coordinate"]
            return click_at(x, y)
        elif action_type == "type":
            return type_text(params["text"])
        # ... handle other actions
    ```
  </Step>
  <Step title="Proses panggilan alat Claude">
    Ekstrak dan jalankan panggilan alat dari respons Claude:
    
    ```python nocheck
    for content in response.content:
        if content.type == "tool_use":
            action = content.input["action"]
            result = handle_computer_action(action, content.input)

            # Return result to Claude
            tool_result = {
                "type": "tool_result",
                "tool_use_id": content.id,
                "content": result,
            }
    ```
  </Step>
  <Step title="Implementasikan loop agen">
    Buat loop yang berlanjut hingga Claude menyelesaikan tugas:
    
    ```python nocheck
    while True:
        response = client.beta.messages.create(...)

        # Check if Claude used any tools
        tool_results = process_tool_calls(response)

        if not tool_results:
            # No more tool use, task complete
            break

        # Continue conversation with tool results
        messages.append({"role": "user", "content": tool_results})
    ```
  </Step>
</Steps>

#### Menangani kesalahan

Saat mengimplementasikan alat penggunaan komputer, berbagai kesalahan mungkin terjadi. Berikut cara menanganinya:

<section title="Kegagalan pengambilan tangkapan layar">

Jika pengambilan tangkapan layar gagal, kembalikan pesan kesalahan yang sesuai:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Failed to capture screenshot. Display may be locked or unavailable.",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Koordinat tidak valid">

Jika Claude memberikan koordinat di luar batas tampilan:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Coordinates (1200, 900) are outside display bounds (1024x768).",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Kegagalan eksekusi aksi">

Jika suatu aksi gagal dijalankan:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Failed to perform click action. The application may be unresponsive.",
      "is_error": true
    }
  ]
}
```

</section>

#### Menangani penskalaan koordinat untuk resolusi lebih tinggi

API membatasi gambar hingga maksimum 1568 piksel pada sisi terpanjang dan sekitar 1,15 megapiksel total (lihat [pengubahan ukuran gambar](/docs/id/build-with-claude/vision#evaluate-image-size) untuk detailnya). Misalnya, layar 1512x982 disampling turun menjadi sekitar 1330x864. Claude menganalisis gambar yang lebih kecil ini dan mengembalikan koordinat dalam ruang tersebut, tetapi alat Anda menjalankan klik di ruang layar asli.

Hal ini dapat menyebabkan koordinat klik Claude meleset dari targetnya kecuali Anda menangani transformasi koordinat.

Untuk memperbaikinya, ubah ukuran tangkapan layar sendiri dan skalakan kembali koordinat Claude:

<CodeGroup>

```python Python nocheck
import math


def get_scale_factor(width, height):
    """Calculate scale factor to meet API constraints."""
    long_edge = max(width, height)
    total_pixels = width * height

    long_edge_scale = 1568 / long_edge
    total_pixels_scale = math.sqrt(1_150_000 / total_pixels)

    return min(1.0, long_edge_scale, total_pixels_scale)


# When capturing screenshot
scale = get_scale_factor(screen_width, screen_height)
scaled_width = int(screen_width * scale)
scaled_height = int(screen_height * scale)

# Resize image to scaled dimensions before sending to Claude
screenshot = capture_and_resize(scaled_width, scaled_height)


# When handling Claude's coordinates, scale them back up
def execute_click(x, y):
    screen_x = x / scale
    screen_y = y / scale
    perform_click(screen_x, screen_y)
```

```typescript TypeScript nocheck
const MAX_LONG_EDGE = 1568;
const MAX_PIXELS = 1_150_000;

function getScaleFactor(width: number, height: number): number {
  const longEdge = Math.max(width, height);
  const totalPixels = width * height;

  const longEdgeScale = MAX_LONG_EDGE / longEdge;
  const totalPixelsScale = Math.sqrt(MAX_PIXELS / totalPixels);

  return Math.min(1.0, longEdgeScale, totalPixelsScale);
}

// When capturing screenshot
const scale = getScaleFactor(screenWidth, screenHeight);
const scaledWidth = Math.floor(screenWidth * scale);
const scaledHeight = Math.floor(screenHeight * scale);

// Resize image to scaled dimensions before sending to Claude
const screenshot = captureAndResize(scaledWidth, scaledHeight);

// When handling Claude's coordinates, scale them back up
function executeClick(x: number, y: number): void {
  const screenX = x / scale;
  const screenY = y / scale;
  performClick(screenX, screenY);
}
```
</CodeGroup>

#### Ikuti praktik terbaik implementasi

<section title="Gunakan resolusi tampilan yang sesuai">

Atur dimensi tampilan yang sesuai dengan kasus penggunaan Anda sambil tetap dalam batas yang direkomendasikan:
- Untuk tugas desktop umum: 1024x768 atau 1280x720
- Untuk aplikasi web: 1280x800 atau 1366x768
- Hindari resolusi di atas 1920x1080 untuk mencegah masalah performa

</section>

<section title="Implementasikan penanganan tangkapan layar yang tepat">

Saat mengembalikan tangkapan layar ke Claude:
- Enkode tangkapan layar sebagai PNG atau JPEG base64
- Pertimbangkan mengompresi tangkapan layar besar untuk meningkatkan performa
- Sertakan metadata yang relevan seperti stempel waktu atau status tampilan
- Jika menggunakan resolusi lebih tinggi, pastikan koordinat diskalakan dengan akurat

</section>

<section title="Tambahkan penundaan aksi">

Beberapa aplikasi membutuhkan waktu untuk merespons aksi:

```python nocheck
def click_and_wait(x, y, wait_time=0.5):
    click_at(x, y)
    time.sleep(wait_time)  # Allow UI to update
```

</section>

<section title="Validasi aksi sebelum eksekusi">

Periksa bahwa aksi yang diminta aman dan valid:

```python nocheck
def validate_action(action_type, params):
    if action_type == "left_click":
        x, y = params.get("coordinate", (0, 0))
        if not (0 <= x < display_width and 0 <= y < display_height):
            return False, "Coordinates out of bounds"
    return True, None
```

</section>

<section title="Catat aksi untuk debugging">

Simpan log semua aksi untuk pemecahan masalah:

```python nocheck
import logging


def log_action(action_type, params, result):
    logging.info(f"Action: {action_type}, Params: {params}, Result: {result}")
```

</section>

---

## Memahami keterbatasan penggunaan komputer

Fungsionalitas penggunaan komputer masih dalam tahap beta. Meskipun kemampuan Claude mutakhir, pengembang harus menyadari keterbatasannya:

1. **Latensi**: latensi penggunaan komputer saat ini untuk interaksi manusia-AI mungkin terlalu lambat dibandingkan dengan tindakan komputer yang diarahkan manusia secara langsung. Fokus pada kasus penggunaan di mana kecepatan tidak kritis (misalnya, pengumpulan informasi latar belakang, pengujian perangkat lunak otomatis) di lingkungan tepercaya.
2. **Akurasi dan keandalan visi komputer**: Claude mungkin membuat kesalahan atau berhalusinasi saat mengeluarkan koordinat spesifik saat menghasilkan aksi. Claude Sonnet 3.7 memperkenalkan kemampuan berpikir yang dapat membantu Anda memahami penalaran model dan mengidentifikasi potensi masalah.
3. **Akurasi dan keandalan pemilihan alat**: Claude mungkin membuat kesalahan atau berhalusinasi saat memilih alat saat menghasilkan aksi atau mengambil tindakan tak terduga untuk memecahkan masalah. Selain itu, keandalan mungkin lebih rendah saat berinteraksi dengan aplikasi khusus atau beberapa aplikasi sekaligus. Beri prompt model dengan hati-hati saat meminta tugas kompleks.
4. **Keandalan pengguliran**: Claude Sonnet 3.7 memperkenalkan aksi gulir khusus dengan kontrol arah yang meningkatkan keandalan. Model sekarang dapat secara eksplisit menggulir ke arah mana pun (atas/bawah/kiri/kanan) sebesar jumlah yang ditentukan.
5. **Interaksi spreadsheet**: Klik mouse untuk interaksi spreadsheet telah ditingkatkan di Claude Sonnet 3.7 dengan penambahan aksi kontrol mouse yang lebih presisi seperti `left_mouse_down`, `left_mouse_up`, dan dukungan tombol modifier baru. Pemilihan sel dapat lebih andal dengan menggunakan kontrol berbutir halus ini dan menggabungkan tombol modifier dengan klik.
6. **Pembuatan akun dan pembuatan konten di platform sosial dan komunikasi**: Meskipun Claude akan mengunjungi situs web, kemampuan Claude untuk membuat akun atau menghasilkan dan berbagi konten atau terlibat dalam peniruan identitas manusia di seluruh situs web dan platform media sosial terbatas. Kemampuan ini mungkin diperbarui di masa mendatang.
7. **Kerentanan**: Kerentanan seperti jailbreaking atau injeksi prompt mungkin tetap ada di seluruh sistem AI frontier, termasuk API penggunaan komputer beta. Dalam beberapa keadaan, Claude akan mengikuti perintah yang ditemukan dalam konten, terkadang bahkan bertentangan dengan instruksi pengguna. Misalnya, instruksi Claude di halaman web atau yang terkandung dalam gambar mungkin mengesampingkan instruksi atau menyebabkan Claude membuat kesalahan. Pertimbangkan hal berikut:
   a. Membatasi penggunaan komputer ke lingkungan tepercaya seperti mesin virtual atau kontainer dengan hak istimewa minimal
   b. Menghindari pemberian akses penggunaan komputer ke akun atau data sensitif tanpa pengawasan ketat
   c. Menginformasikan pengguna akhir tentang risiko yang relevan dan mendapatkan persetujuan mereka sebelum mengaktifkan atau meminta izin yang diperlukan untuk fitur penggunaan komputer di aplikasi Anda
8. **Tindakan tidak pantas atau ilegal**: Sesuai ketentuan layanan Anthropic, Anda tidak boleh menggunakan penggunaan komputer untuk melanggar hukum apa pun atau Kebijakan Penggunaan yang Dapat Diterima.

Selalu tinjau dan verifikasi dengan cermat tindakan dan log penggunaan komputer Claude. Jangan gunakan Claude untuk tugas yang memerlukan presisi sempurna atau informasi pengguna sensitif tanpa pengawasan manusia.

## Retensi data

Penggunaan komputer adalah alat sisi klien. Semua tangkapan layar, aksi mouse, input keyboard, dan file apa pun yang terlibat dalam sesi ditangkap dan disimpan di lingkungan Anda, bukan oleh Anthropic. Anthropic memproses gambar tangkapan layar dan permintaan aksi secara real time sebagai bagian dari panggilan API tetapi tidak menyimpannya setelah respons dikembalikan.

Karena aplikasi Anda mengontrol di mana dan bagaimana data penggunaan komputer disimpan, penggunaan komputer memenuhi syarat ZDR. Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/build-with-claude/api-and-data-retention).

## Harga

Computer use follows the standard [tool use pricing](/docs/en/agents-and-tools/tool-use/overview#pricing). When using the computer use tool:

**System prompt overhead**: The computer use beta adds 466-499 tokens to the system prompt

**Computer use tool token usage**:
| Model | Input tokens per tool definition |
| ----- | -------------------------------- |
| Claude 4.x models | 735 tokens |
| Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)) | 735 tokens |

**Additional token consumption**:
- Screenshot images (see [Vision pricing](/docs/en/build-with-claude/vision))
- Tool execution results returned to Claude

<Note>
If you're also using bash or text editor tools alongside computer use, those tools have their own token costs as documented in their respective pages.
</Note>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card
    title="Implementasi referensi"
    icon="github-logo"
    href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo"
  >
    Mulai dengan cepat menggunakan implementasi berbasis Docker yang lengkap
  </Card>
  <Card
    title="Dokumentasi alat"
    icon="tool"
    href="/docs/id/agents-and-tools/tool-use/overview"
  >
    Pelajari lebih lanjut tentang penggunaan alat dan membuat alat kustom
  </Card>
</CardGroup>