---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 2a44dc8643cafbfc69b5b06473dbe753fe3250acbf8c74e0bb3e4e95573e3361
---

# Alat computer use

Claude dapat berinteraksi dengan lingkungan desktop melalui alat computer use yang menyediakan kemampuan screenshot dan kontrol mouse/keyboard untuk interaksi desktop otonom.

---

Claude dapat berinteraksi dengan lingkungan komputer melalui alat computer use, yang menyediakan kemampuan screenshot dan kontrol mouse/keyboard untuk interaksi desktop otonom. Di [WebArena](https://webarena.dev/), sebuah benchmark untuk navigasi web otonom di seluruh situs web nyata, Claude mencapai hasil terdepan di antara sistem single-agent, menunjukkan kemampuan kuat untuk menyelesaikan tugas browser multi-langkah dari awal hingga akhir.

<Note>
Computer use sedang dalam beta dan memerlukan [beta header](/docs/id/api/beta-headers):
- `"computer-use-2025-11-24"` untuk Claude Opus 4.6, Claude Sonnet 4.6, Claude Opus 4.5
- `"computer-use-2025-01-24"` untuk Sonnet 4.5, Haiku 4.5, Opus 4.1, Sonnet 4, Opus 4, dan Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations))

Hubungi kami melalui [formulir umpan balik](https://forms.gle/H6UFuXaaLywri9hz6) untuk berbagi umpan balik Anda tentang fitur ini.
</Note>

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

## Ikhtisar

Computer use adalah fitur beta yang memungkinkan Claude berinteraksi dengan lingkungan desktop. Alat ini menyediakan:

- **Penangkapan screenshot**: Lihat apa yang saat ini ditampilkan di layar
- **Kontrol mouse**: Klik, seret, dan pindahkan kursor
- **Input keyboard**: Ketik teks dan gunakan pintasan keyboard
- **Otomasi desktop**: Berinteraksi dengan aplikasi atau antarmuka apa pun

Meskipun computer use dapat ditingkatkan dengan alat lain seperti bash dan editor teks untuk alur kerja otomasi yang lebih komprehensif, computer use secara khusus mengacu pada kemampuan alat computer use untuk melihat dan mengontrol lingkungan desktop.

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Pertimbangan keamanan

Computer use adalah fitur beta dengan risiko unik yang berbeda dari fitur API standar. Risiko ini meningkat ketika berinteraksi dengan internet.

<Warning>
Untuk meminimalkan risiko, pertimbangkan untuk mengambil tindakan pencegahan seperti:

1. Menggunakan mesin virtual atau kontainer khusus dengan hak istimewa minimal untuk mencegah serangan sistem langsung atau kecelakaan.
2. Menghindari pemberian model akses ke data sensitif, seperti informasi login akun, untuk mencegah pencurian informasi.
3. Membatasi akses internet ke daftar putih domain untuk mengurangi paparan terhadap konten berbahaya.
4. Meminta manusia untuk mengonfirmasi keputusan yang mungkin menghasilkan konsekuensi dunia nyata yang bermakna serta tugas apa pun yang memerlukan persetujuan afirmatif, seperti menerima cookie, menjalankan transaksi keuangan, atau menyetujui syarat layanan.
</Warning>

Dalam beberapa keadaan, Claude akan mengikuti perintah yang ditemukan dalam konten bahkan jika bertentangan dengan instruksi pengguna. Misalnya, instruksi Claude di halaman web atau yang terdapat dalam gambar dapat mengganti instruksi atau menyebabkan Claude membuat kesalahan. Ambil tindakan pencegahan untuk mengisolasi Claude dari data dan tindakan sensitif untuk menghindari risiko yang terkait dengan prompt injection.

Model telah dilatih untuk menahan prompt injection ini, dan lapisan pertahanan tambahan telah ditambahkan. Jika Anda menggunakan alat computer use, pengklasifikasi akan secara otomatis berjalan pada prompt Anda untuk menandai kemungkinan instance prompt injection. Ketika pengklasifikasi ini mengidentifikasi prompt injection potensial dalam screenshot, mereka akan secara otomatis mengarahkan model untuk meminta konfirmasi pengguna sebelum melanjutkan dengan tindakan berikutnya. Perlindungan tambahan ini tidak akan ideal untuk setiap kasus penggunaan (misalnya, kasus penggunaan tanpa manusia dalam loop), jadi jika Anda ingin menolak dan mematikannya, silakan [hubungi dukungan](https://support.claude.com/en/).

Tindakan pencegahan ini tetap penting bahkan dengan lapisan pertahanan pengklasifikasi yang ada.

Informasikan pengguna akhir tentang risiko yang relevan dan dapatkan persetujuan mereka sebelum mengaktifkan computer use di produk Anda sendiri.

<Card
  title="Implementasi referensi computer use"
  icon="computer"
  href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo"
>

Mulai dengan cepat dengan implementasi referensi computer use yang mencakup antarmuka web, kontainer Docker, implementasi alat contoh, dan loop agen.

**Catatan:** Implementasi telah diperbarui untuk menyertakan alat baru untuk model Claude 4 dan Claude Sonnet 3.7. Pastikan untuk menarik versi terbaru repo untuk mengakses fitur-fitur baru ini.

</Card>

## Mulai cepat

Berikut cara memulai dengan computer use:

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

```bash CLI
ant beta:messages create --beta computer-use-2025-11-24 <<'YAML'
model: claude-opus-4-6
max_tokens: 1024
tools:
  - type: computer_20251124
    name: computer
    display_width_px: 1024
    display_height_px: 768
    display_number: 1
  - type: text_editor_20250728
    name: str_replace_based_edit_tool
  - type: bash_20250124
    name: bash
messages:
  - role: user
    content: Save a picture of a cat to my desktop.
YAML
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

```csharp C#
using Anthropic;
using Anthropic.Models.Beta.Messages;
using Messages = Anthropic.Models.Messages;

var client = new AnthropicClient();

var parameters = new MessageCreateParams
{
    Model = Messages::Model.ClaudeOpus4_6,
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
    Messages =
    [
        new BetaMessageParam
        {
            Role = Role.User,
            Content = "Save a picture of a cat to my desktop."
        }
    ],
    Betas = ["computer-use-2025-11-24"]
};

var response = await client.Beta.Messages.Create(parameters);
Console.WriteLine(response);
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
Beta header hanya diperlukan untuk alat computer use.

Contoh di atas menunjukkan ketiga alat digunakan bersama-sama, yang memerlukan beta header karena mencakup alat computer use.
</Note>

---

## Cara kerja computer use

<Steps>
  <Step
    title="Berikan Claude dengan alat computer use dan prompt pengguna"
    icon="tool"
  >
    - Tambahkan alat computer use (dan secara opsional alat lain) ke permintaan API Anda.
    - Sertakan prompt pengguna yang memerlukan interaksi desktop, misalnya, "Simpan gambar kucing ke desktop saya."
  </Step>
  <Step title="Claude memutuskan untuk menggunakan alat computer use" icon="wrench">
    - Claude menilai apakah alat computer use dapat membantu dengan pertanyaan pengguna.
    - Jika ya, Claude membuat permintaan penggunaan alat yang diformat dengan benar.
    - Respons API memiliki `stop_reason` dari `tool_use`, menandakan niat Claude.
  </Step>
  <Step
    title="Ekstrak input alat, evaluasi alat di komputer, dan kembalikan hasil"
    icon="computer"
  >
    - Di pihak Anda, ekstrak nama alat dan input dari permintaan Claude.
    - Gunakan alat di kontainer atau Mesin Virtual.
    - Lanjutkan percakapan dengan pesan `user` baru yang berisi blok konten `tool_result`.
  </Step>
  <Step
    title="Claude terus memanggil alat computer use sampai menyelesaikan tugas"
    icon="arrows-clockwise"
  >
    - Claude menganalisis hasil alat untuk menentukan apakah penggunaan alat lebih lanjut diperlukan atau tugas telah selesai.
    - Jika Claude memutuskan memerlukan alat lain, ia merespons dengan `stop_reason` `tool_use` lain dan Anda harus kembali ke langkah 3.
    - Jika tidak, ia membuat respons teks kepada pengguna.
  </Step>
</Steps>

Pengulangan langkah 3 dan 4 tanpa input pengguna disebut sebagai "agent loop" (yaitu, Claude merespons dengan permintaan penggunaan alat dan aplikasi Anda merespons Claude dengan hasil evaluasi permintaan tersebut).

### Lingkungan komputasi

Computer use memerlukan lingkungan komputasi bersandal di mana Claude dapat dengan aman berinteraksi dengan aplikasi dan web. Lingkungan ini mencakup:

1. **Tampilan virtual**: Server tampilan X11 virtual (menggunakan Xvfb) yang merender antarmuka desktop yang akan Claude lihat melalui screenshot dan kontrol dengan tindakan mouse/keyboard.

2. **Lingkungan desktop**: UI ringan dengan window manager (Mutter) dan panel (Tint2) yang berjalan di Linux, yang menyediakan antarmuka grafis yang konsisten untuk Claude berinteraksi.

3. **Aplikasi**: Aplikasi Linux pra-instal seperti Firefox, LibreOffice, editor teks, dan file manager yang dapat Claude gunakan untuk menyelesaikan tugas.

4. **Implementasi alat**: Kode integrasi yang menerjemahkan permintaan alat abstrak Claude (seperti "pindahkan mouse" atau "ambil screenshot") menjadi operasi aktual di lingkungan virtual.

5. **Agent loop**: Program yang menangani komunikasi antara Claude dan lingkungan, mengirim tindakan Claude ke lingkungan dan mengembalikan hasil (screenshot, output perintah) kembali ke Claude.

Ketika Anda menggunakan computer use, Claude tidak terhubung langsung ke lingkungan ini. Sebaliknya, aplikasi Anda:

1. Menerima permintaan penggunaan alat Claude
2. Menerjemahkannya menjadi tindakan di lingkungan komputasi Anda
3. Menangkap hasil (screenshot, output perintah, dll.)
4. Mengembalikan hasil ini ke Claude

Untuk keamanan dan isolasi, implementasi referensi menjalankan semua ini di dalam kontainer Docker dengan pemetaan port yang sesuai untuk melihat dan berinteraksi dengan lingkungan.

---

## Cara mengimplementasikan computer use

### Mulai dengan implementasi referensi

[Implementasi referensi](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) tersedia yang mencakup semua yang Anda butuhkan untuk memulai dengan cepat dengan computer use:

- [Lingkungan terkontainerisasi](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/Dockerfile) yang cocok untuk computer use dengan Claude
- Implementasi [alat computer use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo/computer_use_demo/tools)
- [Agent loop](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/computer_use_demo/loop.py) yang berinteraksi dengan Claude API dan menjalankan alat computer use
- Antarmuka web untuk berinteraksi dengan kontainer, agent loop, dan alat.

### Memahami agentic loop

Inti dari computer use adalah "agent loop" - siklus di mana Claude meminta tindakan alat, aplikasi Anda menjalankannya, dan mengembalikan hasil ke Claude. Berikut adalah contoh yang disederhanakan:

```python hidelines={1}
from anthropic import Anthropic


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
    )
    text_editor_type = (
        "text_editor_20250728"
        if "20251124" in tool_version
        else f"text_editor_{tool_version}"
    )

    # Configure tools - you should already have these initialized elsewhere
    tools = [
        {
            "type": f"computer_{tool_version}",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
        },
        {"type": text_editor_type, "name": "str_replace_based_edit_tool"},
        {"type": "bash_20250124", "name": "bash"},
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

Loop berlanjut sampai Claude merespons tanpa meminta alat apa pun (penyelesaian tugas) atau batas iterasi maksimal tercapai. Perlindungan ini mencegah loop tak terbatas potensial yang dapat menghasilkan biaya API yang tidak terduga.

Coba implementasi referensi sebelum membaca sisa dokumentasi ini.

### Optimalkan kinerja model dengan prompting

Berikut adalah beberapa tips tentang cara mendapatkan output berkualitas terbaik:

1. Tentukan tugas sederhana dan terdefinisi dengan baik serta berikan instruksi eksplisit untuk setiap langkah.
2. Claude kadang-kadang mengasumsikan hasil tindakannya tanpa secara eksplisit memeriksa hasilnya. Untuk mencegah ini, Anda dapat memberi prompt Claude dengan `After each step, take a screenshot and carefully evaluate if you have achieved the right outcome. Explicitly show your thinking: "I have evaluated step X..." If not correct, try again. Only when you confirm a step was executed correctly should you move on to the next one.`
3. Beberapa elemen UI (seperti dropdown dan scrollbar) mungkin sulit bagi Claude untuk dimanipulasi menggunakan gerakan mouse. Jika Anda mengalami ini, coba beri prompt model untuk menggunakan pintasan keyboard.
4. Untuk tugas yang dapat diulang atau interaksi UI, sertakan contoh screenshot dan panggilan alat hasil yang berhasil dalam prompt Anda.
5. Jika Anda perlu model untuk login, berikan nama pengguna dan kata sandi dalam prompt Anda di dalam tag xml seperti `<robot_credentials>`. Menggunakan computer use dalam aplikasi yang memerlukan login meningkatkan risiko hasil buruk karena prompt injection. Tinjau [panduan tentang mitigasi prompt injection](/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) sebelum memberikan model kredensial login.

<Tip>
  Jika Anda berulang kali mengalami serangkaian masalah yang jelas atau mengetahui sebelumnya tugas yang perlu Claude selesaikan, gunakan system prompt untuk memberikan Claude tips atau instruksi eksplisit tentang cara menyelesaikan tugas dengan sukses.
</Tip>

<Tip>
  Untuk agen yang mencakup beberapa sesi, jalankan verifikasi end-to-end di awal setiap sesi, bukan hanya setelah implementasi. Pemeriksaan berbasis browser menangkap regresi dari sesi sebelumnya yang tinjauan tingkat kode saja melewatkan. Lihat [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) untuk detail.
</Tip>

### System prompts

Ketika salah satu alat skema Anthropic diminta melalui Claude API, system prompt khusus computer use dihasilkan. Ini mirip dengan [tool use system prompt](/docs/id/agents-and-tools/tool-use/define-tools#tool-use-system-prompt) tetapi dimulai dengan:

> You have access to a set of functions you can use to answer the user's question. This includes access to a sandboxed computing environment. You do NOT currently have the ability to inspect files or interact with external resources, except by invoking the below functions.

Seperti dengan tool use reguler, field `system_prompt` yang disediakan pengguna tetap dihormati dan digunakan dalam konstruksi system prompt gabungan.

### Tindakan yang tersedia

Alat computer use mendukung tindakan berikut:

**Tindakan dasar (semua versi)**
- **screenshot** - Tangkap tampilan saat ini
- **left_click** - Klik pada koordinat `[x, y]`
- **type** - Ketik string teks
- **key** - Tekan tombol atau kombinasi tombol (misalnya, "ctrl+s")
- **mouse_move** - Pindahkan kursor ke koordinat

**Tindakan yang ditingkatkan (`computer_20250124`)**
Tersedia di model Claude 4 dan Claude Sonnet 3.7:
- **scroll** - Gulir ke arah mana pun dengan kontrol jumlah
- **left_click_drag** - Klik dan seret antara koordinat
- **right_click**, **middle_click** - Tombol mouse tambahan
- **double_click**, **triple_click** - Klik ganda
- **left_mouse_down**, **left_mouse_up** - Kontrol klik terperinci
- **hold_key** - Tahan tombol untuk durasi tertentu (dalam detik)
- **wait** - Jeda antara tindakan

**Tindakan yang ditingkatkan (`computer_20251124`)**
Tersedia di Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Opus 4.5:
- Semua tindakan dari `computer_20250124`
- **zoom** - Lihat wilayah tertentu dari layar pada resolusi penuh. Memerlukan `enable_zoom: true` dalam definisi alat. Mengambil parameter `region` dengan koordinat `[x1, y1, x2, y2]` yang menentukan sudut kiri atas dan kanan bawah area untuk diperiksa.

<section title="Contoh tindakan">

Ambil screenshot:

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

Zoom untuk melihat wilayah secara detail (Opus 4.6, Sonnet 4.6, Opus 4.5):

```json
{
  "action": "zoom",
  "region": [100, 200, 400, 350]
}
```

</section>

<section title="Tombol pengubah dengan tindakan klik dan gulir">

Untuk menahan tombol pengubah (seperti Shift, Ctrl, atau Alt) saat melakukan tindakan klik atau gulir, gunakan parameter `text` pada tindakan tersebut. Ini berbeda dari `hold_key`, yang hanya menahan tombol untuk durasi tanpa melakukan tindakan lain.

Shift+click (misalnya, untuk memilih rentang item):

```json
{
  "action": "left_click",
  "coordinate": [500, 300],
  "text": "shift"
}
```

Ctrl+click (misalnya, untuk multi-select di Windows/Linux):

```json
{
  "action": "left_click",
  "coordinate": [500, 300],
  "text": "ctrl"
}
```

Cmd+click (misalnya, untuk multi-select di macOS):

```json
{
  "action": "left_click",
  "coordinate": [500, 300],
  "text": "super"
}
```

Shift+scroll (misalnya, untuk scrolling horizontal):

```json
{
  "action": "scroll",
  "coordinate": [500, 400],
  "scroll_direction": "down",
  "scroll_amount": 3,
  "text": "shift"
}
```

Parameter `text` dalam tindakan klik/gulir menerima tombol pengubah seperti `shift`, `ctrl`, `alt`, dan `super` (untuk tombol Command/Windows).

</section>

### Parameter alat

| Parameter | Diperlukan | Deskripsi |
|-----------|----------|-------------|
| `type` | Ya | Versi alat (`computer_20251124` atau `computer_20250124`) |
| `name` | Ya | Harus "computer" |
| `display_width_px` | Ya | Lebar tampilan dalam piksel |
| `display_height_px` | Ya | Tinggi tampilan dalam piksel |
| `display_number` | Tidak | Nomor tampilan untuk lingkungan X11 |
| `enable_zoom` | Tidak | Aktifkan tindakan zoom (`computer_20251124` saja). Atur ke `true` untuk memungkinkan Claude zoom ke wilayah layar tertentu. Default: `false` |

<Note>
**Penting:** Alat computer use harus secara eksplisit dijalankan oleh aplikasi Anda - Claude tidak dapat menjalankannya secara langsung. Anda bertanggung jawab untuk mengimplementasikan penangkapan screenshot, gerakan mouse, input keyboard, dan tindakan lain berdasarkan permintaan Claude.
</Note>

### Menggabungkan dengan extended thinking

Untuk menggabungkan computer use dengan extended thinking, lihat [Extended thinking](/docs/id/build-with-claude/extended-thinking).

### Menambah computer use dengan alat lain

Untuk menambahkan alat lain bersama computer use, sertakan mereka dalam array `tools` yang sama. Mulai cepat di atas menunjukkan pola ini dengan [alat bash](/docs/id/agents-and-tools/tool-use/bash-tool) dan [alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool). Anda dapat menambahkan [definisi alat kustom](/docs/id/agents-and-tools/tool-use/define-tools) Anda sendiri dengan cara yang sama.

### Bangun lingkungan penggunaan komputer khusus

[Implementasi referensi](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) dimaksudkan untuk membantu Anda memulai dengan penggunaan komputer. Ini mencakup semua komponen yang diperlukan agar Claude dapat menggunakan komputer. Namun, Anda dapat membangun lingkungan Anda sendiri untuk penggunaan komputer sesuai kebutuhan Anda. Anda akan memerlukan:

- Lingkungan virtual atau terkontainerisasi yang sesuai untuk penggunaan komputer dengan Claude
- Implementasi setidaknya satu dari alat penggunaan komputer skema Anthropic
- Loop agen yang berinteraksi dengan API Claude dan mengeksekusi hasil `tool_use` menggunakan implementasi alat Anda
- API atau UI yang memungkinkan input pengguna untuk memulai loop agen

#### Implementasikan alat penggunaan komputer

Alat penggunaan komputer diimplementasikan sebagai alat tanpa skema. Saat menggunakan alat ini, Anda tidak perlu memberikan skema input seperti alat lainnya; skema dibangun ke dalam model Claude dan tidak dapat dimodifikasi.

<Steps>
  <Step title="Siapkan lingkungan komputasi Anda">
    Buat tampilan virtual atau sambungkan ke tampilan yang ada yang akan berinteraksi dengan Claude. Ini biasanya melibatkan pengaturan Xvfb (X Virtual Framebuffer) atau teknologi serupa.
  </Step>
  <Step title="Implementasikan penanganan tindakan">
    Buat fungsi untuk menangani setiap jenis tindakan yang mungkin diminta Claude:
    ```python hidelines={1..3}
    def capture_screenshot(): ...
    def click_at(x, y): ...
    def type_text(text): ...
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
    ```python hidelines={1..11}
    from types import SimpleNamespace as _SN

    response = _SN(
        content=[_SN(type="tool_use", input={"action": "screenshot"}, id="toolu_01")]
    )


    def handle_computer_action(a, p):
        return "ok"


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
    Buat loop yang berlanjut sampai Claude menyelesaikan tugas:
    ```python hidelines={1..18}
    import anthropic

    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": "Take a screenshot"}]
    tools = [
        {
            "type": "computer_20251124",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
        }
    ]


    def process_tool_calls(r):
        return []


    while True:
        response = client.beta.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            messages=messages,
            tools=tools,
            betas=["computer-use-2025-11-24"],
        )

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

#### Tangani kesalahan

Saat mengimplementasikan alat penggunaan komputer, berbagai kesalahan dapat terjadi. Berikut cara menanganinya:

<section title="Kegagalan penangkapan tangkapan layar">

Jika penangkapan tangkapan layar gagal, kembalikan pesan kesalahan yang sesuai:

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

<section title="Kegagalan eksekusi tindakan">

Jika tindakan gagal dieksekusi:

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

#### Tangani penskalaan koordinat untuk resolusi yang lebih tinggi

API membatasi gambar hingga maksimal 1568 piksel pada tepi terpanjang dan sekitar 1,15 megapiksel total (lihat [pengubahan ukuran gambar](/docs/id/build-with-claude/vision#evaluate-image-size) untuk detail). Misalnya, layar 1512x982 dikecilkan menjadi sekitar 1330x864. Claude menganalisis gambar yang lebih kecil ini dan mengembalikan koordinat dalam ruang itu, tetapi alat Anda mengeksekusi klik dalam ruang layar asli.

Ini dapat menyebabkan koordinat klik Claude melewatkan target mereka kecuali Anda menangani transformasi koordinat.

Untuk memperbaikinya, ubah ukuran tangkapan layar sendiri dan skalakan koordinat Claude kembali:

<CodeGroup>
```python Python hidelines={1..7}
screen_width, screen_height = 1512, 982


def capture_and_resize(w, h): ...
def perform_click(x, y): ...


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

```typescript TypeScript hidelines={1..6}
const screenWidth = 1512;
const screenHeight = 982;
function captureAndResize(w: number, h: number): string {
  return "";
}
function performClick(x: number, y: number): void {}
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

Atur dimensi tampilan yang sesuai dengan kasus penggunaan Anda sambil tetap berada dalam batas yang direkomendasikan:
- Untuk tugas desktop umum: 1024x768 atau 1280x720
- Untuk aplikasi web: 1280x800 atau 1366x768
- Hindari resolusi di atas 1920x1080 untuk mencegah masalah kinerja

</section>

<section title="Implementasikan penanganan tangkapan layar yang tepat">

Saat mengembalikan tangkapan layar ke Claude:
- Enkode tangkapan layar sebagai PNG atau JPEG base64
- Pertimbangkan untuk mengompresi tangkapan layar besar untuk meningkatkan kinerja
- Sertakan metadata yang relevan seperti stempel waktu atau status tampilan
- Jika menggunakan resolusi yang lebih tinggi, pastikan koordinat diskalakan dengan akurat

</section>

<section title="Tambahkan penundaan tindakan">

Beberapa aplikasi memerlukan waktu untuk merespons tindakan:
```python hidelines={1..4}
import time


def click_at(x, y): ...
def click_and_wait(x, y, wait_time=0.5):
    click_at(x, y)
    time.sleep(wait_time)  # Allow UI to update
```

</section>

<section title="Validasi tindakan sebelum eksekusi">

Periksa bahwa tindakan yang diminta aman dan valid:
```python hidelines={1}
display_width, display_height = 1024, 768


def validate_action(action_type, params):
    if action_type == "left_click":
        x, y = params.get("coordinate", (0, 0))
        if not (0 <= x < display_width and 0 <= y < display_height):
            return False, "Coordinates out of bounds"
    return True, None
```

</section>

<section title="Catat tindakan untuk debugging">

Simpan log semua tindakan untuk pemecahan masalah:
```python
import logging


def log_action(action_type, params, result):
    logging.info(f"Action: {action_type}, Params: {params}, Result: {result}")
```

</section>

---

## Pahami keterbatasan penggunaan komputer

Fungsionalitas penggunaan komputer masih dalam beta. Meskipun kemampuan Claude terdepan, pengembang harus menyadari keterbatasannya:

1. **Latensi**: latensi penggunaan komputer saat ini untuk interaksi manusia-AI mungkin terlalu lambat dibandingkan dengan tindakan komputer yang diarahkan manusia biasa. Fokus pada kasus penggunaan di mana kecepatan tidak kritis (misalnya, pengumpulan informasi latar belakang, pengujian perangkat lunak otomatis) di lingkungan terpercaya.
2. **Akurasi dan keandalan visi komputer**: Claude mungkin membuat kesalahan atau berhalusinasi saat mengeluarkan koordinat spesifik sambil menghasilkan tindakan. Claude Sonnet 3.7 memperkenalkan kemampuan pemikiran yang dapat membantu Anda memahami penalaran model dan mengidentifikasi potensi masalah.
3. **Akurasi dan keandalan pemilihan alat**: Claude mungkin membuat kesalahan atau berhalusinasi saat memilih alat sambil menghasilkan tindakan atau mengambil tindakan yang tidak terduga untuk menyelesaikan masalah. Selain itu, keandalan mungkin lebih rendah saat berinteraksi dengan aplikasi niche atau beberapa aplikasi sekaligus. Prompt model dengan hati-hati saat meminta tugas kompleks.
4. **Keandalan pengguliran**: Claude Sonnet 3.7 memperkenalkan tindakan pengguliran khusus dengan kontrol arah yang meningkatkan keandalan. Model sekarang dapat secara eksplisit menggulir ke arah mana pun (atas/bawah/kiri/kanan) dengan jumlah yang ditentukan.
5. **Interaksi spreadsheet**: Klik mouse untuk interaksi spreadsheet telah ditingkatkan di Claude Sonnet 3.7 dengan penambahan tindakan kontrol mouse yang lebih presisi seperti `left_mouse_down`, `left_mouse_up`, dan dukungan tombol pengubah baru. Pemilihan sel dapat lebih andal dengan menggunakan kontrol butir halus ini dan menggabungkan tombol pengubah dengan klik.
6. **Pembuatan akun dan pembuatan konten di platform media sosial dan komunikasi**: Meskipun Claude akan mengunjungi situs web, kemampuan Claude untuk membuat akun atau menghasilkan dan berbagi konten atau sebaliknya terlibat dalam penyamaran manusia di seluruh situs web dan platform media sosial terbatas. Kemampuan ini mungkin diperbarui di masa depan.
7. **Kerentanan**: Kerentanan seperti jailbreaking atau injeksi prompt mungkin tetap ada di seluruh sistem AI frontier, termasuk API penggunaan komputer beta. Dalam beberapa keadaan, Claude akan mengikuti perintah yang ditemukan dalam konten, kadang-kadang bahkan bertentangan dengan instruksi pengguna. Misalnya, instruksi Claude di halaman web atau yang terdapat dalam gambar dapat mengganti instruksi atau menyebabkan Claude membuat kesalahan. Pertimbangkan hal berikut:
   a. Membatasi penggunaan komputer ke lingkungan terpercaya seperti mesin virtual atau kontainer dengan hak istimewa minimal
   b. Menghindari pemberian akses penggunaan komputer ke akun atau data sensitif tanpa pengawasan ketat
   c. Menginformasikan pengguna akhir tentang risiko yang relevan dan mendapatkan persetujuan mereka sebelum mengaktifkan atau meminta izin yang diperlukan untuk fitur penggunaan komputer di aplikasi Anda
8. **Tindakan yang tidak pantas atau ilegal**: Sesuai dengan syarat layanan Anthropic, Anda tidak boleh menggunakan penggunaan komputer untuk melanggar hukum apa pun atau Kebijakan Penggunaan yang Dapat Diterima.

Selalu tinjau dan verifikasi dengan hati-hati tindakan dan log penggunaan komputer Claude. Jangan gunakan Claude untuk tugas yang memerlukan presisi sempurna atau informasi pengguna sensitif tanpa pengawasan manusia.

## Retensi data

Penggunaan komputer adalah alat sisi klien. Semua tangkapan layar, tindakan mouse, input keyboard, dan file apa pun yang terlibat dalam sesi ditangkap dan disimpan di lingkungan Anda, bukan oleh Anthropic. Anthropic memproses gambar tangkapan layar dan permintaan tindakan secara real-time sebagai bagian dari panggilan API tetapi tidak menyimpannya setelah respons dikembalikan.

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

## Langkah berikutnya

<CardGroup cols={2}>
  <Card
    title="Implementasi referensi"
    icon="github-logo"
    href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo"
  >
    Mulai dengan cepat dengan implementasi berbasis Docker yang lengkap
  </Card>
  <Card
    title="Dokumentasi alat"
    icon="tool"
    href="/docs/id/agents-and-tools/tool-use/overview"
  >
    Pelajari lebih lanjut tentang penggunaan alat dan membuat alat khusus
  </Card>
</CardGroup>