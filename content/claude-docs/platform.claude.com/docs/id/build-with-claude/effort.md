---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/effort
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: 4c7e149bb714f93a01a3987aa5069de1fc64a1d67f21bfb37bdc6182b0083944
---

# Effort

Kontrol berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menukar antara kelengkapan respons dan efisiensi token.

---

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Parameter effort memungkinkan Anda mengontrol seberapa bersemangat Claude dalam menggunakan token saat merespons permintaan. Anda dapat menukar antara kelengkapan respons dan efisiensi token dengan satu model. Parameter effort tersedia pada semua model yang didukung tanpa memerlukan header beta.

<Note>
  Parameter effort didukung oleh Claude Fable 5, [Claude Mythos 5](https://anthropic.com/glasswing), Claude Opus 4.8, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Opus 4.5.
</Note>

<Tip>
Untuk Claude Opus 4.6 dan Sonnet 4.6, effort menggantikan `budget_tokens` sebagai cara yang direkomendasikan untuk mengontrol kedalaman pemikiran. Kombinasikan effort dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) untuk pengalaman terbaik. Meskipun `budget_tokens` masih diterima pada Opus 4.6 dan Sonnet 4.6, parameter ini sudah tidak digunakan lagi (deprecated) dan akan dihapus pada rilis model mendatang. Pada effort `high` (default) dan `max`, Claude hampir selalu akan berpikir. Pada tingkat effort yang lebih rendah, Claude mungkin melewati pemikiran untuk masalah yang lebih sederhana.
</Tip>

## Cara kerja effort \{#how-effort-works}

Secara default, Claude menggunakan effort tinggi, menghabiskan token sebanyak yang diperlukan untuk hasil yang sangat baik. Anda dapat menaikkan tingkat effort ke `max` untuk kemampuan tertinggi mutlak, atau menurunkannya agar lebih konservatif dalam penggunaan token, mengoptimalkan kecepatan dan biaya sambil menerima sedikit pengurangan kemampuan.

<Tip>
Mengatur `effort` ke `"high"` menghasilkan perilaku yang persis sama dengan menghilangkan parameter `effort` sepenuhnya.
</Tip>

Parameter effort memengaruhi **semua token** dalam respons, termasuk:

- Respons teks dan penjelasan
- Pemanggilan alat dan argumen fungsi
- Pemikiran diperpanjang (jika diaktifkan)

Pendekatan ini memiliki dua keuntungan utama:

1. Tidak memerlukan pemikiran untuk diaktifkan.
2. Dapat memengaruhi semua penggunaan token termasuk pemanggilan alat. Misalnya, effort yang lebih rendah berarti Claude membuat lebih sedikit pemanggilan alat. Ini memberikan tingkat kontrol yang jauh lebih besar atas efisiensi.

### Tingkat effort \{#effort-levels}

| Tingkat  | Deskripsi                                                                                                                      | Kasus penggunaan umum                                                                      |
| -------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `max`    | Kemampuan maksimum mutlak tanpa batasan pada penggunaan token. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6. | Tugas yang memerlukan penalaran sedalam mungkin dan analisis paling menyeluruh |
| `xhigh`  | Kemampuan diperluas untuk pekerjaan jangka panjang. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, dan Claude Opus 4.7. | Tugas agentik dan pengodean yang berjalan lama (lebih dari 30 menit) dengan anggaran token dalam jutaan |
| `high`   | Kemampuan tinggi. Setara dengan tidak mengatur parameter. | Penalaran kompleks, masalah pengodean yang sulit, tugas agentik                           |
| `medium` | Pendekatan seimbang dengan penghematan token moderat. | Tugas agentik yang memerlukan keseimbangan kecepatan, biaya, dan performa                                                         |
| `low`    | Paling efisien. Penghematan token signifikan dengan sedikit pengurangan kemampuan. | Tugas yang lebih sederhana yang membutuhkan kecepatan terbaik dan biaya terendah, seperti subagent                     |

<Note>
Effort adalah sinyal perilaku, bukan anggaran token yang ketat. Pada tingkat effort yang lebih rendah, Claude tetap akan berpikir pada masalah yang cukup sulit, tetapi akan berpikir lebih sedikit dibandingkan pada tingkat effort yang lebih tinggi untuk masalah yang sama.
</Note>

### Tingkat effort yang direkomendasikan untuk Sonnet 4.6 \{#recommended-effort-levels-for-sonnet-4-6}

Sonnet 4.6 secara default menggunakan effort `high`. Atur effort secara eksplisit saat menggunakan Sonnet 4.6 untuk menghindari latensi yang tidak terduga:

- **Effort medium** (default yang direkomendasikan): Keseimbangan terbaik antara kecepatan, biaya, dan performa untuk sebagian besar aplikasi. Cocok untuk pengodean agentik, alur kerja yang banyak menggunakan alat, dan pembuatan kode.
- **Effort low:** Untuk beban kerja bervolume tinggi atau sensitif terhadap latensi. Cocok untuk chat dan kasus penggunaan non-pengodean di mana waktu penyelesaian yang lebih cepat diprioritaskan.
- **Effort high:** Untuk penalaran kompleks dan tugas di mana kualitas lebih penting daripada kecepatan atau biaya.
- **Effort max:** Untuk tugas yang memerlukan kemampuan tertinggi mutlak tanpa batasan pada penggunaan token.

### Tingkat effort yang direkomendasikan untuk Claude Opus 4.7 \{#recommended-effort-levels-for-claude-opus-4-7}

**Mulai dengan `xhigh` untuk kasus penggunaan pengodean dan agentik**, dan gunakan `high` sebagai minimum untuk sebagian besar beban kerja yang sensitif terhadap kecerdasan. Turunkan ke `medium` untuk beban kerja yang sensitif terhadap biaya, atau naikkan ke `max` hanya ketika evaluasi Anda menunjukkan ruang peningkatan yang terukur pada `xhigh`.

Default API adalah `high`. Untuk menggunakan `xhigh`, atur `effort` secara eksplisit; nilai yang Anda berikan akan menggantikan default.

| Effort | Panduan untuk Claude Opus 4.7 |
|--------|------------------------------|
| `low`    | Efisien, tetapi paling cocok untuk tugas singkat dan terbatas cakupannya. Pasangkan `low` dengan daftar periksa eksplisit jika tugas Anda memiliki beberapa bagian. |
| `medium` | Pilihan langsung untuk alur kerja rata-rata di mana Anda menginginkan hasil yang baik sambil mengurangi biaya. |
| `high`   | Kasus penggunaan tingkat lanjut yang masih memerlukan keseimbangan antara kecerdasan dan konsumsi token. Ini sering kali merupakan titik optimal yang menyeimbangkan kualitas dan efisiensi token. |
| `xhigh`  | Titik awal yang direkomendasikan untuk pekerjaan pengodean dan agentik, serta untuk tugas eksploratif seperti pemanggilan alat berulang, pencarian web terperinci, dan pencarian basis pengetahuan. Harapkan penggunaan token yang jauh lebih tinggi daripada `high`. |
| `max`    | Simpan untuk masalah yang benar-benar di garis depan. Pada sebagian besar beban kerja, `max` menambah biaya signifikan untuk peningkatan kualitas yang relatif kecil, dan pada beberapa tugas output terstruktur atau yang kurang sensitif terhadap kecerdasan, ini dapat menyebabkan pemikiran berlebihan. |

Claude Opus 4.7 juga mematuhi tingkat effort dengan lebih ketat daripada Claude Opus 4.6, terutama pada `low` dan `medium`. Pada tingkat effort yang lebih rendah, model membatasi pekerjaannya pada apa yang diminta daripada melakukan lebih dari yang diharapkan. Jika Anda mengamati penalaran yang dangkal pada masalah kompleks dengan Claude Opus 4.7, naikkan effort daripada mengatasinya melalui prompt. Jika Anda harus menjaga effort tetap rendah untuk latensi, tambahkan panduan yang ditargetkan seperti "Tugas ini melibatkan penalaran multi-langkah. Pikirkan dengan cermat sebelum merespons."

Saat menjalankan Claude Opus 4.7 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagent dan pemanggilan alat. Memulai dari 64k token dan menyesuaikan dari sana adalah default yang wajar.

### Tingkat effort yang direkomendasikan untuk Claude Opus 4.8 \{#recommended-effort-levels-for-claude-opus-4-8}

Panduan untuk Claude Opus 4.7 juga berlaku untuk Claude Opus 4.8. **Mulai dengan `xhigh` untuk kasus penggunaan pengodean dan agentik**, gunakan `high` untuk sebagian besar beban kerja lain yang sensitif terhadap kecerdasan, dan turunkan ke `medium` atau `low` hanya ketika Anda telah mengukur bahwa tingkat yang lebih rendah mempertahankan kualitas pada evaluasi Anda.

Default adalah `high` pada semua antarmuka, termasuk Claude API dan Claude Code. Atur `effort` secara eksplisit untuk menggunakan tingkat yang berbeda; nilai yang Anda berikan akan menggantikan default.

Saat menjalankan Claude Opus 4.8 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagent dan pemanggilan alat. Memulai dari 64k token dan menyesuaikan dari sana adalah default yang wajar.

### Tingkat effort yang direkomendasikan untuk Claude Fable 5 \{#recommended-effort-levels-for-claude-fable-5}

Effort adalah kontrol utama untuk menukar antara kecerdasan, latensi, dan biaya pada Claude Fable 5. **Mulai dengan `high`, default, untuk sebagian besar tugas**, gunakan `xhigh` untuk beban kerja yang paling sensitif terhadap kemampuan, dan turunkan ke `medium` atau `low` untuk pekerjaan rutin. Pengaturan effort yang lebih rendah pada Claude Fable 5 tetap berkinerja baik dan sering kali melampaui performa `xhigh` pada model sebelumnya. Pada `high` dan `xhigh`, atur `max_tokens` yang besar: ini adalah batas keras pada total output, pemikiran ditambah teks respons. Lihat [Kontrol biaya](/docs/id/build-with-claude/adaptive-thinking#cost-control).

Kurangi effort jika tugas selesai tetapi memakan waktu lebih lama dari yang diperlukan, atau jika Anda menginginkan gaya kerja yang lebih cepat dan lebih interaktif. Rekomendasi yang sama berlaku untuk Claude Mythos 5. Untuk panduan yang lebih lengkap, lihat [Membuat prompt untuk Claude Fable 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5).

## Penggunaan dasar \{#basic-usage}

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-8",
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
ant messages create \
  --transform 'content.0.text' \
  --raw-output <<'YAML'
model: claude-opus-4-8
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
    model="claude-opus-4-8",
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
  model: "claude-opus-4-8",
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
            Model = Model.ClaudeOpus4_8,
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
		Model:     anthropic.ModelClaudeOpus4_8,
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
            .model(Model.CLAUDE_OPUS_4_8)
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

$client = new Client();

$message = $client->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Analyze the trade-offs between microservices and monolithic architectures']
    ],
    model: 'claude-opus-4-8',
    outputConfig: ['effort' => 'medium'],
);

echo $message->content[0]->text;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
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

## Kapan menyesuaikan parameter effort \{#when-to-adjust-the-effort-parameter}

- Gunakan **effort max** ketika Anda membutuhkan kemampuan tertinggi mutlak tanpa batasan: penalaran paling menyeluruh dan analisis terdalam. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6.
- Gunakan **effort xhigh** untuk pengodean tingkat lanjut dan pekerjaan agentik kompleks yang memerlukan eksplorasi diperluas, seperti pemanggilan alat berulang dan pencarian terperinci. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, dan Claude Opus 4.7.
- Gunakan **effort high** (default) untuk penalaran kompleks, analisis bernuansa, masalah pengodean yang sulit, atau tugas apa pun di mana kualitas lebih penting daripada kecepatan atau biaya.
- Gunakan **effort medium** sebagai opsi seimbang ketika Anda menginginkan performa yang solid tanpa pengeluaran token penuh dari effort tinggi.
- Gunakan **effort low** ketika Anda mengoptimalkan kecepatan (karena Claude menjawab dengan lebih sedikit token) atau biaya. Misalnya, tugas klasifikasi sederhana, pencarian cepat, atau kasus penggunaan bervolume tinggi di mana peningkatan kualitas marginal tidak sebanding dengan latensi atau pengeluaran tambahan.

<Note>
**Mode ultracode Claude Code:** ultracode muncul di menu effort Claude Code, tetapi ini bukan tingkat effort API tambahan. Nilai-nilai yang didokumentasikan di halaman ini adalah kumpulan lengkap yang diterima API. Ultracode memasangkan tingkat effort `xhigh` dengan izin tetap bagi Claude Code untuk meluncurkan alur kerja multi-agen, yang diberikan melalui [Pesan sistem di tengah percakapan](/docs/id/build-with-claude/mid-conversation-system-messages). Untuk membangun perilaku serupa dengan API, lihat [Membangun mode orkestrasi](/docs/id/build-with-claude/mid-conversation-effort-example).
</Note>

## Effort dengan penggunaan alat \{#effort-with-tool-use}

Saat menggunakan alat, parameter effort memengaruhi baik penjelasan di sekitar pemanggilan alat maupun pemanggilan alat itu sendiri. Tingkat effort yang lebih rendah cenderung:

- Menggabungkan beberapa operasi menjadi lebih sedikit pemanggilan alat
- Membuat lebih sedikit pemanggilan alat
- Langsung melanjutkan ke tindakan tanpa pembukaan
- Menggunakan pesan konfirmasi singkat setelah selesai

Tingkat effort yang lebih tinggi mungkin:

- Membuat lebih banyak pemanggilan alat
- Menjelaskan rencana sebelum mengambil tindakan
- Memberikan ringkasan perubahan yang terperinci
- Menyertakan komentar kode yang lebih komprehensif

## Effort dengan pemikiran diperpanjang \{#effort-with-extended-thinking}

Parameter effort bekerja bersama dengan "extended thinking" (pemikiran diperpanjang). Perilakunya bergantung pada model:

- **Claude Fable 5 dan Claude Mythos 5** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), yang selalu aktif (tidak memerlukan konfigurasi `thinking`). `thinking: {type: "disabled"}` ditolak. Effort mengontrol kedalaman pemikiran dengan cara yang sama seperti pada Opus 4.8 dan Opus 4.7.
- **Claude Opus 4.8** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana effort adalah kontrol yang direkomendasikan untuk kedalaman pemikiran. Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung dan mengembalikan error 400. Model memutuskan kapan dan seberapa banyak berpikir berdasarkan setiap permintaan, sehingga memicu pemikiran hanya jika diperlukan. Pada effort `high`, `xhigh`, dan `max`, Claude hampir selalu berpikir secara mendalam. Pada tingkat yang lebih rendah, Claude mungkin melewati pemikiran untuk masalah yang lebih sederhana. Atur `thinking: {type: "adaptive"}` untuk mengaktifkan pemikiran; tanpa itu, permintaan berjalan tanpa pemikiran.
- **Claude Mythos Preview** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) secara default (tidak memerlukan konfigurasi `thinking`). `thinking: {type: "disabled"}` ditolak. Effort mengontrol kedalaman pemikiran dengan cara yang sama seperti pada Opus 4.7 dan Opus 4.6.
- **Claude Opus 4.7** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana effort adalah kontrol yang direkomendasikan untuk kedalaman pemikiran. Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak lagi didukung pada Opus 4.7; gunakan adaptive thinking dengan effort sebagai gantinya. Pada effort `high`, `xhigh`, dan `max`, Claude hampir selalu berpikir secara mendalam. Pada tingkat yang lebih rendah, Claude mungkin melewati pemikiran untuk masalah yang lebih sederhana.
- **Claude Opus 4.6** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana effort adalah kontrol yang direkomendasikan untuk kedalaman pemikiran. Meskipun `budget_tokens` masih diterima pada Opus 4.6, parameter ini sudah tidak digunakan lagi (deprecated) dan akan dihapus pada rilis mendatang. Pada effort `high` dan `max`, Claude hampir selalu berpikir secara mendalam. Pada tingkat yang lebih rendah, Claude mungkin melewati pemikiran untuk masalah yang lebih sederhana.
- **Claude Sonnet 4.6** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (di mana effort mengontrol kedalaman pemikiran). Pemikiran manual dengan [mode interleaved](/docs/id/build-with-claude/extended-thinking#interleaved-thinking) (`thinking: {type: "enabled", budget_tokens: N}`) masih berfungsi tetapi sudah tidak digunakan lagi (deprecated).
- **Claude Opus 4.5** menggunakan pemikiran manual (`thinking: {type: "enabled", budget_tokens: N}`), di mana effort bekerja bersama dengan anggaran token pemikiran. Atur tingkat effort untuk tugas Anda, lalu atur anggaran token pemikiran berdasarkan kompleksitas tugas.

Parameter effort dapat digunakan dengan atau tanpa pemikiran diperpanjang diaktifkan. Ketika digunakan tanpa pemikiran, parameter ini tetap mengontrol penggunaan token secara keseluruhan untuk respons teks dan pemanggilan alat.

## Praktik terbaik \{#best-practices}

1. **Atur effort secara eksplisit:** API secara default menggunakan `high`, tetapi titik awal yang tepat bergantung pada model dan beban kerja Anda.
2. **Gunakan low untuk tugas yang sensitif terhadap kecepatan atau sederhana:** Ketika latensi penting atau tugas bersifat sederhana, effort rendah dapat secara signifikan mengurangi waktu respons dan biaya.
3. **Uji kasus penggunaan Anda:** Dampak tingkat effort bervariasi berdasarkan jenis tugas. Evaluasi performa pada kasus penggunaan spesifik Anda sebelum menerapkan.
4. **Pertimbangkan effort dinamis:** Sesuaikan effort berdasarkan kompleksitas tugas. Kueri sederhana mungkin memerlukan effort rendah sementara pengodean agentik dan penalaran kompleks mendapat manfaat dari effort tinggi.

## Langkah selanjutnya \{#next-steps}

<CardGroup>
  <Card title="Anggaran tugas" icon="gauge" href="/docs/id/build-with-claude/task-budgets">
    Berikan Claude anggaran token yang bersifat saran untuk seluruh loop agentik guna membantu model mengatur dirinya sendiri pada tugas agentik yang panjang.
  </Card>
  <Card title="Adaptive thinking" icon="brain" href="/docs/id/build-with-claude/adaptive-thinking">
    Biarkan Claude secara dinamis menentukan kapan dan seberapa banyak menggunakan pemikiran diperpanjang dengan mode adaptive thinking.
  </Card>
  <Card title="Membangun dengan pemikiran diperpanjang" icon="settings" href="/docs/id/build-with-claude/extended-thinking">
    Berikan Claude penalaran yang ditingkatkan untuk tugas kompleks dengan anggaran pemikiran manual, penggunaan alat, dan caching prompt.
  </Card>
</CardGroup>