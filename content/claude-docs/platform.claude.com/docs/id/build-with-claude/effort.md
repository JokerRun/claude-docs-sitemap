---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/effort
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: d838ab4f23ac97bdc46339abfc996488d3c9ea6db739c8e5151e9a4c0c2fa79e
---

# Effort

Kontrol berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menukar antara kelengkapan respons dan efisiensi token.

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Parameter effort memungkinkan Anda mengontrol seberapa bersemangat Claude dalam menghabiskan token saat merespons permintaan. Ini memberi Anda kemampuan untuk menukar antara kelengkapan respons dan efisiensi token, semuanya dengan satu model. Parameter effort secara umum tersedia di semua model yang didukung tanpa memerlukan header beta.

<Note>
  Parameter effort didukung oleh [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Opus 4.5.
</Note>

<Tip>
Untuk Claude Opus 4.6 dan Sonnet 4.6, effort menggantikan `budget_tokens` sebagai cara yang direkomendasikan untuk mengontrol kedalaman pemikiran. Gabungkan effort dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) untuk pengalaman terbaik. Meskipun `budget_tokens` masih diterima di Opus 4.6 dan Sonnet 4.6, ini sudah usang dan akan dihapus dalam rilis model di masa depan. Pada effort `high` (default) dan `max`, Claude hampir selalu akan berpikir. Pada tingkat effort yang lebih rendah, mungkin akan melewati pemikiran untuk masalah yang lebih sederhana.
</Tip>

## Cara effort bekerja

Secara default, Claude menggunakan high effort, menghabiskan sebanyak token yang diperlukan untuk hasil yang sangat baik. Anda dapat menaikkan tingkat effort ke `max` untuk kemampuan tertinggi yang mutlak, atau menurunkannya untuk lebih konservatif dengan penggunaan token, mengoptimalkan kecepatan dan biaya sambil menerima beberapa pengurangan dalam kemampuan.

<Tip>
Mengatur `effort` ke `"high"` menghasilkan perilaku yang persis sama dengan menghilangkan parameter `effort` sepenuhnya.
</Tip>

Parameter effort mempengaruhi **semua token** dalam respons, termasuk:

- Respons teks dan penjelasan
- Panggilan alat dan argumen fungsi
- Pemikiran yang diperluas (ketika diaktifkan)

Pendekatan ini memiliki dua keuntungan utama:

1. Tidak memerlukan pemikiran untuk diaktifkan agar dapat menggunakannya.
2. Dapat mempengaruhi semua pengeluaran token termasuk panggilan alat. Misalnya, effort yang lebih rendah berarti Claude membuat lebih sedikit panggilan alat. Ini memberikan tingkat kontrol yang jauh lebih besar atas efisiensi.

### Tingkat effort

| Level    | Deskripsi                                                                                                                      | Kasus penggunaan umum                                                                      |
| -------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `max`    | Kemampuan maksimum mutlak tanpa batasan pada pengeluaran token. Tersedia di Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6. | Tugas yang memerlukan penalaran paling mendalam dan analisis paling menyeluruh |
| `xhigh`  | Kemampuan yang diperluas untuk pekerjaan jangka panjang. Tersedia di Claude Opus 4.7. | Tugas agentic dan coding yang berjalan lama (lebih dari 30 menit) dengan anggaran token dalam jutaan |
| `high`   | Kemampuan tinggi. Setara dengan tidak mengatur parameter. | Penalaran kompleks, masalah coding yang sulit, tugas agentic                           |
| `medium` | Pendekatan seimbang dengan penghematan token moderat. | Tugas agentic yang memerlukan keseimbangan kecepatan, biaya, dan kinerja                                                         |
| `low`    | Paling efisien. Penghematan token signifikan dengan beberapa pengurangan kemampuan. | Tugas yang lebih sederhana yang membutuhkan kecepatan terbaik dan biaya terendah, seperti subagents                     |

<Note>
Effort adalah sinyal perilaku, bukan anggaran token yang ketat. Pada tingkat effort yang lebih rendah, Claude masih akan berpikir pada masalah yang cukup sulit, tetapi akan berpikir lebih sedikit daripada yang akan dilakukan pada tingkat effort yang lebih tinggi untuk masalah yang sama.
</Note>

### Tingkat effort yang direkomendasikan untuk Sonnet 4.6

Sonnet 4.6 default ke effort `high`. Atur effort secara eksplisit saat menggunakan Sonnet 4.6 untuk menghindari latensi yang tidak terduga:

- **Medium effort** (default yang direkomendasikan): Keseimbangan terbaik antara kecepatan, biaya, dan kinerja untuk sebagian besar aplikasi. Cocok untuk coding agentic, alur kerja yang kaya alat, dan pembuatan kode.
- **Low effort:** Untuk beban kerja dengan volume tinggi atau sensitif latensi. Cocok untuk chat dan kasus penggunaan non-coding di mana turnaround yang lebih cepat diprioritaskan.
- **High effort:** Untuk tugas yang memerlukan intelijen maksimum dari Sonnet 4.6.
- **Max effort:** Untuk tugas yang memerlukan kemampuan tertinggi yang mutlak tanpa batasan pada pengeluaran token.

### Tingkat effort yang direkomendasikan untuk Claude Opus 4.7

**Mulai dengan `xhigh` untuk kasus penggunaan coding dan agentic**, dan gunakan `high` sebagai minimum untuk sebagian besar beban kerja yang sensitif terhadap intelijen. Turun ke `medium` untuk beban kerja yang sensitif terhadap biaya, atau naik ke `max` hanya ketika eval Anda menunjukkan ruang kepala yang terukur di `xhigh`.

Default API adalah `high`. Untuk menggunakan `xhigh`, atur `effort` secara eksplisit; nilai yang Anda berikan menggantikan default.

| Effort | Panduan untuk Claude Opus 4.7 |
|--------|------------------------------|
| `low`    | Efisien, tetapi terbaik untuk tugas yang singkat dan terbatas. Pasangkan `low` dengan daftar periksa eksplisit jika tugas Anda memiliki beberapa bagian. |
| `medium` | Pengganti untuk alur kerja rata-rata di mana Anda menginginkan hasil yang baik sambil mengurangi biaya. |
| `high`   | Kasus penggunaan lanjutan yang masih memerlukan keseimbangan intelijen dan konsumsi token. Ini sering kali menjadi sweet spot yang menyeimbangkan kualitas dan efisiensi token. |
| `xhigh`  | Titik awal yang direkomendasikan untuk pekerjaan coding dan agentic, dan untuk tugas eksplorasi seperti panggilan alat berulang, pencarian web terperinci, dan pencarian basis pengetahuan. Harapkan penggunaan token yang jauh lebih tinggi daripada `high`. |
| `max`    | Cadangkan untuk masalah perbatasan yang benar-benar asli. Pada sebagian besar beban kerja `max` menambah biaya signifikan untuk keuntungan kualitas yang relatif kecil, dan pada beberapa tugas output terstruktur atau kurang sensitif terhadap intelijen, dapat menyebabkan overthinking. |

Claude Opus 4.7 juga menghormati tingkat effort lebih ketat daripada Claude Opus 4.6, terutama di `low` dan `medium`. Pada tingkat effort yang lebih rendah, model membatasi pekerjaan ke apa yang diminta daripada melampaui. Jika Anda mengamati penalaran dangkal pada masalah kompleks dengan Claude Opus 4.7, naikkan effort daripada meminta di sekitarnya. Jika Anda harus menjaga effort tetap rendah untuk latensi, tambahkan panduan yang ditargetkan seperti "Tugas ini melibatkan penalaran multi-langkah. Pikirkan dengan hati-hati sebelum merespons."

Saat menjalankan Claude Opus 4.7 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar sehingga model memiliki ruang untuk berpikir dan bertindak di seluruh subagents dan panggilan alat. Mulai dari 64k token dan menyesuaikan dari sana adalah default yang masuk akal.

## Penggunaan dasar

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-7",
        "max_tokens": 4096,
        "messages": [{
            "role": "user",
            "content": "Analyze the trade-offs between microservices and monolithic architectures"
        }],
        "output_config": {
            "effort": "medium"
        }
    }'
```

```bash CLI
ant messages create --transform 'content.0.text' --format yaml <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
messages:
  - role: user
    content: Analyze the trade-offs between microservices and monolithic architectures
output_config:
  effort: medium
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Analyze the trade-offs between microservices and monolithic architectures",
        }
    ],
    output_config={"effort": "medium"},
)

print(response.content[0].text)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content: "Analyze the trade-offs between microservices and monolithic architectures"
    }
  ],
  output_config: {
    effort: "medium"
  }
});

const textBlock = response.content.find(
  (block): block is Anthropic.TextBlock => block.type === "text"
);
console.log(textBlock?.text);
```

```csharp C#
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_7,
            MaxTokens = 4096,
            Messages = [new() { Role = Role.User, Content = "Analyze the trade-offs between microservices and monolithic architectures" }],
            OutputConfig = new OutputConfig
            {
                Effort = Effort.Medium
            }
        };

        var message = await client.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 4096,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the trade-offs between microservices and monolithic architectures")),
		},
		OutputConfig: anthropic.OutputConfigParam{
			Effort: anthropic.OutputConfigEffortMedium,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Content[0].Text)
}
```

```java Java hidelines={1..5,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.OutputConfig;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(4096L)
            .addUserMessage("Analyze the trade-offs between microservices and monolithic architectures")
            .outputConfig(OutputConfig.builder()
                .effort(OutputConfig.Effort.MEDIUM)
                .build())
            .build();

        Message response = client.messages().create(params);
        response.content().stream()
            .flatMap(block -> block.text().stream())
            .forEach(textBlock -> System.out.println(textBlock.text()));
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Analyze the trade-offs between microservices and monolithic architectures']
    ],
    model: 'claude-opus-4-7',
    outputConfig: ['effort' => 'medium'],
);

echo $message->content[0]->text;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  messages: [
    { role: "user", content: "Analyze the trade-offs between microservices and monolithic architectures" }
  ],
  output_config: {
    effort: "medium"
  }
)

puts message.content.first.text
```

</CodeGroup>

## Kapan menyesuaikan parameter effort

- Gunakan **max effort** ketika Anda memerlukan kemampuan tertinggi yang mutlak tanpa batasan: penalaran paling menyeluruh dan analisis paling mendalam. Tersedia di Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6.
- Gunakan **xhigh effort** untuk pekerjaan coding lanjutan dan agentic kompleks yang memerlukan eksplorasi yang diperluas, seperti panggilan alat berulang dan pencarian terperinci. Tersedia di Claude Opus 4.7.
- Gunakan **high effort** (default) ketika Anda memerlukan pekerjaan terbaik Claude: penalaran kompleks, analisis bernuansa, masalah coding yang sulit, atau tugas apa pun di mana kualitas adalah prioritas utama.
- Gunakan **medium effort** sebagai opsi seimbang ketika Anda menginginkan kinerja solid tanpa pengeluaran token penuh dari high effort.
- Gunakan **low effort** ketika Anda mengoptimalkan untuk kecepatan (karena Claude menjawab dengan lebih sedikit token) atau biaya. Misalnya, tugas klasifikasi sederhana, pencarian cepat, atau kasus penggunaan volume tinggi di mana peningkatan kualitas marginal tidak membenarkan latensi atau pengeluaran tambahan.

## Effort dengan penggunaan alat

Saat menggunakan alat, parameter effort mempengaruhi penjelasan di sekitar panggilan alat dan panggilan alat itu sendiri. Tingkat effort yang lebih rendah cenderung:

- Menggabungkan beberapa operasi menjadi lebih sedikit panggilan alat
- Membuat lebih sedikit panggilan alat
- Melanjutkan langsung ke tindakan tanpa pembukaan
- Menggunakan pesan konfirmasi yang ringkas setelah penyelesaian

Tingkat effort yang lebih tinggi mungkin:

- Membuat lebih banyak panggilan alat
- Menjelaskan rencana sebelum mengambil tindakan
- Memberikan ringkasan perubahan yang terperinci
- Menyertakan komentar kode yang lebih komprehensif

## Effort dengan pemikiran yang diperluas

Parameter effort bekerja bersama pemikiran yang diperluas. Perilakunya tergantung pada model:

- **Claude Mythos Preview** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) secara default (tidak ada konfigurasi `thinking` yang diperlukan). `thinking: {type: "disabled"}` ditolak. Effort mengontrol kedalaman pemikiran dengan cara yang sama seperti di Opus 4.7 dan Opus 4.6.
- **Claude Opus 4.7** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana effort adalah kontrol yang direkomendasikan untuk kedalaman pemikiran. Pemikiran yang diperluas manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak lagi didukung di Opus 4.7; gunakan adaptive thinking dengan effort sebagai gantinya. Pada effort `high`, `xhigh`, dan `max`, Claude hampir selalu berpikir mendalam. Pada tingkat yang lebih rendah, mungkin akan melewati pemikiran untuk masalah yang lebih sederhana.
- **Claude Opus 4.6** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana effort adalah kontrol yang direkomendasikan untuk kedalaman pemikiran. Meskipun `budget_tokens` masih diterima di Opus 4.6, ini sudah usang dan akan dihapus dalam rilis di masa depan. Pada effort `high` dan `max`, Claude hampir selalu berpikir mendalam. Pada tingkat yang lebih rendah, mungkin akan melewati pemikiran untuk masalah yang lebih sederhana.
- **Claude Sonnet 4.6** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (di mana effort mengontrol kedalaman pemikiran). Pemikiran manual dengan [interleaved mode](/docs/id/build-with-claude/extended-thinking#interleaved-thinking) (`thinking: {type: "enabled", budget_tokens: N}`) masih berfungsi tetapi sudah usang.
- **Claude Opus 4.5 dan model Claude 4 lainnya** menggunakan pemikiran manual (`thinking: {type: "enabled", budget_tokens: N}`), di mana effort bekerja bersama anggaran token pemikiran. Atur tingkat effort untuk tugas Anda, kemudian atur anggaran token pemikiran berdasarkan kompleksitas tugas.

Parameter effort dapat digunakan dengan atau tanpa pemikiran yang diperluas diaktifkan. Ketika digunakan tanpa pemikiran, itu masih mengontrol pengeluaran token keseluruhan untuk respons teks dan panggilan alat.

## Praktik terbaik

1. **Atur effort secara eksplisit:** API default ke `high`, tetapi titik awal yang tepat tergantung pada model dan beban kerja Anda.
2. **Gunakan low untuk tugas yang sensitif terhadap kecepatan atau sederhana:** Ketika latensi penting atau tugas sederhana, low effort dapat secara signifikan mengurangi waktu respons dan biaya.
3. **Uji kasus penggunaan Anda:** Dampak tingkat effort bervariasi menurut jenis tugas. Evaluasi kinerja pada kasus penggunaan spesifik Anda sebelum melakukan deployment.
4. **Pertimbangkan effort dinamis:** Sesuaikan effort berdasarkan kompleksitas tugas. Kueri sederhana mungkin memerlukan low effort sementara coding agentic dan penalaran kompleks mendapat manfaat dari high effort.