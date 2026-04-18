---
source: platform
url: https://platform.claude.com/docs/id/get-started
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 045d81a96496b38ab2b606079f8d869cebe90d395fb3d3b0751945545480a3f6
---

# Mulai dengan Claude

Buat panggilan API pertama Anda ke Claude dan bangun asisten pencarian web sederhana.

---

## Prasyarat

- Akun Anthropic [Console](/)
- [API key](/settings/keys)

## Panggil API

<Tabs>
  <Tab title="cURL">
    <Steps>
      <Step title="Atur API key Anda">
        Dapatkan API key Anda dari [Claude Console](/settings/keys) dan atur sebagai variabel lingkungan:

        ```bash
        export ANTHROPIC_API_KEY='your-api-key-here'
        ```

        Untuk mempertahankan kunci di seluruh sesi shell, tambahkan baris ke profil shell Anda (seperti `~/.zshrc` atau `~/.bashrc`).
      </Step>

      <Step title="Buat panggilan API pertama Anda">
        Jalankan perintah ini untuk membuat asisten pencarian web sederhana:

        ```bash
        curl https://api.anthropic.com/v1/messages \
          -H "Content-Type: application/json" \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -d '{
            "model": "claude-opus-4-7",
            "max_tokens": 1000,
            "messages": [
              {
                "role": "user",
                "content": "What should I search for to find the latest developments in renewable energy?"
              }
            ]
          }'
        ```

        **Contoh output:**
        ```json Output
        {
          "id": "msg_01HCDu5LRGeP2o7s2xGmxyx8",
          "type": "message",
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "Here are some effective search strategies to find the latest renewable energy developments:\n\n## Search Terms to Use:\n- \"renewable energy news 2024\"\n- \"clean energy breakthrough\"\n- \"solar/wind/battery technology advances\"\n- \"green energy innovations\"\n- \"climate tech developments\"\n- \"energy storage solutions\"\n\n## Best Sources to Check:\n\n**News & Industry Sites:**\n- Renewable Energy World\n- GreenTech Media (now Wood Mackenzie)\n- Energy Storage News\n- CleanTechnica\n- PV Magazine (for solar)\n- WindPower Engineering & Development..."
            }
          ],
          "model": "claude-opus-4-7",
          "stop_reason": "end_turn",
          "usage": {
            "input_tokens": 21,
            "output_tokens": 305
          }
        }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="CLI">
    <Steps>
      <Step title="Atur API key Anda">
        Dapatkan API key Anda dari [Claude Console](/settings/keys) dan atur sebagai variabel lingkungan:

        ```bash
        export ANTHROPIC_API_KEY='your-api-key-here'
        ```

        Untuk mempertahankan kunci di seluruh sesi shell, tambahkan baris ke profil shell Anda (seperti `~/.zshrc` atau `~/.bashrc`).
      </Step>

      <Step title="Instal CLI">
        Instal Anthropic CLI dengan Homebrew:

        ```bash
        brew install anthropics/tap/ant
        ```

        Untuk metode instalasi lainnya, lihat [Installation](/docs/id/api/sdks/cli#installation) dalam referensi CLI.
      </Step>

      <Step title="Buat panggilan API pertama Anda">
        Jalankan perintah ini untuk membuat asisten pencarian web sederhana:

        ```bash
        ant messages create \
          --model claude-opus-4-7 \
          --max-tokens 1000 \
          --message '{
            role: user,
            content: "What should I search for to find the latest developments in renewable energy?"
          }'
        ```

        **Contoh output:**
        ```json Output
        {
          "id": "msg_01HCDu5LRGeP2o7s2xGmxyx8",
          "type": "message",
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "Here are some effective search strategies to find the latest renewable energy developments:\n\n## Search Terms to Use:\n- \"renewable energy news 2024\"\n- \"clean energy breakthrough\"\n- \"solar/wind/battery technology advances\"\n- \"green energy innovations\"\n- \"climate tech developments\"\n- \"energy storage solutions\"\n\n## Best Sources to Check:\n\n**News & Industry Sites:**\n- Renewable Energy World\n- GreenTech Media (now Wood Mackenzie)\n- Energy Storage News\n- CleanTechnica\n- PV Magazine (for solar)\n- WindPower Engineering & Development..."
            }
          ],
          "model": "claude-opus-4-7",
          "stop_reason": "end_turn",
          "usage": {
            "input_tokens": 21,
            "output_tokens": 305
          }
        }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Python">
    <Steps>
      <Step title="Atur API key Anda">
        Dapatkan API key Anda dari [Claude Console](/settings/keys) dan atur sebagai variabel lingkungan:

        ```bash
        export ANTHROPIC_API_KEY='your-api-key-here'
        ```

        Untuk mempertahankan kunci di seluruh sesi shell, tambahkan baris ke profil shell Anda (seperti `~/.zshrc` atau `~/.bashrc`).
      </Step>

      <Step title="Instal SDK">
        Instal Anthropic Python SDK:

        ```bash
        pip install anthropic
        ```
      </Step>

      <Step title="Buat kode Anda">
        Simpan ini sebagai `quickstart.py`:

        ```python
        import anthropic

        client = anthropic.Anthropic()

        message = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": "What should I search for to find the latest developments in renewable energy?",
                }
            ],
        )
        print(message.content)
        ```
      </Step>

      <Step title="Jalankan kode Anda">
        ```bash
        python quickstart.py
        ```

        **Contoh output:**
        ```text Output
        [
            TextBlock(
                text='Here are some effective search strategies for finding the latest renewable energy developments:\n\n**Search Terms to Use:**\n- "renewable energy news 2024"\n- "clean energy breakthroughs"\n- "solar/wind/battery technology advances"\n- "energy storage innovations"\n- "green hydrogen developments"\n- "renewable energy policy updates"\n\n**Reliable Sources to Check:**\n- **News & Analysis:** Reuters Energy, Bloomberg New Energy Finance, Greentech Media, Energy Storage News\n- **Industry Publications:** Renewable Energy World, PV Magazine, Wind Power Engineering\n- **Research Organizations:** International Energy Agency (IEA), National Renewable Energy Laboratory (NREL)\n- **Government Sources:** Department of Energy websites, EPA clean energy updates\n\n**Specific Topics to Explore:**\n- Perovskite and next-gen solar cells\n- Offshore wind expansion\n- Grid-scale battery storage\n- Green hydrogen production\n- Carbon capture technologies\n- Smart grid innovations\n- Energy policy changes and incentives...',
                type="text",
            )
        ]
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="TypeScript">
    <Steps>
      <Step title="Atur API key Anda">
        Dapatkan API key Anda dari [Claude Console](/settings/keys) dan atur sebagai variabel lingkungan:

        ```bash
        export ANTHROPIC_API_KEY='your-api-key-here'
        ```

        Untuk mempertahankan kunci di seluruh sesi shell, tambahkan baris ke profil shell Anda (seperti `~/.zshrc` atau `~/.bashrc`).
      </Step>

      <Step title="Instal SDK">
        Instal Anthropic TypeScript SDK:

        ```bash
        npm install @anthropic-ai/sdk
        ```
      </Step>

      <Step title="Buat kode Anda">
        Simpan ini sebagai `quickstart.ts`:

```typescript
import Anthropic from "@anthropic-ai/sdk";

async function main() {
  const anthropic = new Anthropic();

  const msg = await anthropic.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1000,
    messages: [
      {
        role: "user",
        content:
          "What should I search for to find the latest developments in renewable energy?"
      }
    ]
  });
  console.log(msg);
}

main().catch(console.error);
        ```
      </Step>

      <Step title="Jalankan kode Anda">
        ```bash
        npx tsx quickstart.ts
        ```

        **Contoh output:**
        ```javascript Output hidelines={1..2}
        const _ =
          // output
          {
            id: "msg_01ThFHzad6Bh4TpQ6cHux9t8",
            type: "message",
            role: "assistant",
            model: "claude-opus-4-7",
            content: [
              {
                type: "text",
                text:
                  "Here are some effective search strategies to find the latest renewable energy developments:\n\n" +
                  "## Search Terms to Use:\n" +
                  '- "renewable energy news 2024"\n' +
                  '- "clean energy breakthroughs"\n' +
                  '- "solar wind technology advances"\n' +
                  '- "energy storage innovations"\n' +
                  '- "green hydrogen developments"\n' +
                  '- "offshore wind projects"\n' +
                  '- "battery technology renewable"\n\n' +
                  "## Best Sources to Check:\n\n" +
                  "**News & Industry Sites:**\n" +
                  "- Renewable Energy World\n" +
                  "- CleanTechnica\n" +
                  "- GreenTech Media (now Wood Mackenzie)\n" +
                  "- Energy Storage News\n" +
                  "- PV Magazine (for solar)..."
              }
            ],
            stop_reason: "end_turn",
            usage: {
              input_tokens: 21,
              output_tokens: 302
            }
          }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Java">
    <Steps>
      <Step title="Atur API key Anda">
        Dapatkan API key Anda dari [Claude Console](/settings/keys) dan atur sebagai variabel lingkungan:

        ```bash
        export ANTHROPIC_API_KEY='your-api-key-here'
        ```

        Untuk mempertahankan kunci di seluruh sesi shell, tambahkan baris ke profil shell Anda (seperti `~/.zshrc` atau `~/.bashrc`).
      </Step>

      <Step title="Instal SDK">
        Tambahkan Anthropic Java SDK ke proyek Anda. Pertama temukan versi terbaru di [Maven Central](https://central.sonatype.com/artifact/com.anthropic/anthropic-java).

        **Gradle:**
        ```groovy
        implementation("com.anthropic:anthropic-java:2.20.0")
        ```

        **Maven:**
        ```xml
        <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java</artifactId>
          <version>2.20.0</version>
        </dependency>
        ```
      </Step>

      <Step title="Buat kode Anda">
        Simpan ini sebagai `QuickStart.java`:

        ```java
        import com.anthropic.client.AnthropicClient;
        import com.anthropic.client.okhttp.AnthropicOkHttpClient;
        import com.anthropic.models.messages.Message;
        import com.anthropic.models.messages.MessageCreateParams;

        public class QuickStart {

          public static void main(String[] args) {
            AnthropicClient client = AnthropicOkHttpClient.fromEnv();

            MessageCreateParams params = MessageCreateParams.builder()
              .model("claude-opus-4-7")
              .maxTokens(1000)
              .addUserMessage(
                "What should I search for to find the latest developments in renewable energy?"
              )
              .build();

            Message message = client.messages().create(params);
            System.out.println(message.content());
          }
        }
        ```
      </Step>

      <Step title="Jalankan kode Anda">
        ```bash
        javac QuickStart.java
        java QuickStart
        ```

        **Contoh output:**
        ```text Output
        [ContentBlock{text=TextBlock{text=Here are some effective search strategies to find the latest renewable energy developments:

        ## Search Terms to Use:
        - "renewable energy news 2024"
        - "clean energy breakthroughs"
        - "solar/wind/battery technology advances"
        - "energy storage innovations"
        - "green hydrogen developments"
        - "renewable energy policy updates"

        ## Best Sources to Check:
        - **News & Analysis:** Reuters Energy, Bloomberg New Energy Finance, Greentech Media
        - **Industry Publications:** Renewable Energy World, PV Magazine, Wind Power Engineering
        - **Research Organizations:** International Energy Agency (IEA), National Renewable Energy Laboratory (NREL)
        - **Government Sources:** Department of Energy websites, EPA clean energy updates

        ## Specific Topics to Explore:
        - Perovskite and next-gen solar cells
        - Offshore wind expansion
        - Grid-scale battery storage
        - Green hydrogen production..., type=text}}]
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Langkah berikutnya

Anda telah membuat panggilan API pertama. Selanjutnya, pelajari pola Messages API yang akan Anda gunakan dalam setiap integrasi Claude.

<Card title="Bekerja dengan Messages API" icon="messages" href="/docs/id/build-with-claude/working-with-messages">
  Pelajari percakapan multi-putaran, prompt sistem, alasan berhenti, dan pola inti lainnya.
</Card>

Setelah Anda nyaman dengan dasar-dasarnya, jelajahi lebih lanjut:

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="brain" href="/docs/id/about-claude/models/overview">
    Bandingkan model Claude berdasarkan kemampuan dan biaya.
  </Card>
  <Card title="Ikhtisar fitur" icon="list" href="/docs/id/build-with-claude/overview">
    Jelajahi semua kemampuan Claude: alat, manajemen konteks, output terstruktur, dan lainnya.
  </Card>
  <Card title="Client SDKs" icon="code-brackets" href="/docs/id/api/client-sdks">
    Dokumentasi referensi untuk Python, TypeScript, Java, dan perpustakaan klien lainnya.
  </Card>
</CardGroup>