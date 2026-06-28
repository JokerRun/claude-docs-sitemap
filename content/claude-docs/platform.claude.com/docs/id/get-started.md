---
source: platform
url: https://platform.claude.com/docs/id/get-started
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 9e98e6b5d0f3ca2dc768ae5b9dafd2ab34375200df8bffea85623e6d814a9494
---

# Memulai dengan Claude

Lakukan panggilan API pertama Anda ke Claude dan bangun asisten pencarian web sederhana.

---

## Prasyarat

* Akun [Console](/) Anthropic
* [Kunci API](/settings/keys)

## Memanggil API

<Tabs>
  <Tab title="cURL">
    <Steps>
      <Step title="Atur kunci API Anda">
        Ekspor kunci API Anda sebagai variabel lingkungan. Perintah cURL di bawah ini membacanya dari `$ANTHROPIC_API_KEY`.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Lakukan panggilan API pertama Anda">
        Kirim permintaan `POST` ke Messages API:

        ```bash cURL
        curl https://api.anthropic.com/v1/messages \
          -H "content-type: application/json" \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -d '{
            "model": "claude-opus-4-8",
            "max_tokens": 1000,
            "messages": [
              {
                "role": "user",
                "content": "What should I search for to find the latest developments in renewable energy?"
              }
            ]
          }'
        ```

        Claude mengembalikan respons JSON yang berisi pesan asisten:

        ```json Output
        {
          "id": "msg_013mHbppMPd2PrVJzGMZPt2D",
          "type": "message",
          "role": "assistant",
          "model": "claude-opus-4-8",
          "content": [
            {
              "type": "text",
              "text": "Here are some effective search strategies to find the latest developments in renewable energy:\n\n## General Search Terms\n- \"Renewable energy news 2025\"\n- ..."
            }
          ],
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
      <Step title="Instal CLI">
        Instal Anthropic CLI dengan Homebrew:

        ```bash
        brew install anthropics/tap/ant
        ```

        Untuk metode instalasi lainnya, lihat [Instalasi](/docs/id/cli-sdks-libraries/cli/quickstart#installation) di panduan cepat CLI.
      </Step>

      <Step title="Autentikasi">
        Masuk dengan akun Anthropic Anda:

        ```bash
        ant auth login
        ```

        Ini akan membuka alur OAuth berbasis browser. Setelah memberikan otorisasi, konfirmasi kredensial Anda dengan:

        ```bash
        ant auth status
        ```

        Pada host jarak jauh tanpa browser, berikan `--no-browser` untuk mendapatkan URL yang dapat Anda buka di perangkat lain, lalu tempelkan kode yang dikembalikan ke terminal. Jika `ANTHROPIC_API_KEY` diatur di lingkungan Anda, variabel tersebut akan diutamakan daripada kredensial login. Untuk lingkungan non-interaktif seperti CI, lihat [opsi autentikasi CLI](/docs/id/cli-sdks-libraries/cli/authentication).
      </Step>

      <Step title="Lakukan panggilan API pertama Anda">
        Jalankan `ant messages create` dari terminal Anda:

        ```bash CLI
        ant messages create \
          --model claude-opus-4-8 \
          --max-tokens 1000 \
          --message '{
            role: user,
            content: "What should I search for to find the latest developments in renewable energy?"
          }'
        ```

        CLI akan mencetak respons JSON:

        ```json Output
        {
          "id": "msg_01N1ycuCkM5Mzd7WhTU4fwST",
          "type": "message",
          "role": "assistant",
          "model": "claude-opus-4-8",
          "content": [
            {
              "type": "text",
              "text": "Here are some effective search strategies to find the latest developments in renewable energy:\n\n## General Search Terms\n- \"Renewable energy news 2025\"\n- ..."
            }
          ],
          "stop_reason": "end_turn",
          "usage": { "input_tokens": 21, "output_tokens": 305 }
        }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Python">
    <Steps>
      <Step title="Atur kunci API Anda">
        Ekspor kunci API Anda sebagai variabel lingkungan. SDK membaca `ANTHROPIC_API_KEY` secara otomatis.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Buat proyek dan instal SDK">
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        python3 -m venv .venv && source .venv/bin/activate
        pip install anthropic
        ```
      </Step>

      <Step title="Buat kode Anda">
        Buat file bernama `quickstart.py`:

        ```python Python
        import anthropic

        client = anthropic.Anthropic()

        message = client.messages.create(
            model="claude-opus-4-8",
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

        ```text Output wrap
        [TextBlock(citations=None, text='Here are some effective search strategies to find the latest developments in renewable energy:\n\n## General Search Terms\n- "Renewable energy news 2025"\n- ...', type='text')]
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="TypeScript">
    <Steps>
      <Step title="Atur kunci API Anda">
        Ekspor kunci API Anda sebagai variabel lingkungan. SDK membaca `ANTHROPIC_API_KEY` secara otomatis.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Buat proyek dan instal SDK">
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        npm init -y
        npm pkg set type=module
        npm install @anthropic-ai/sdk
        ```
      </Step>

      <Step title="Buat kode Anda">
        Buat file bernama `quickstart.ts`:

        ```typescript TypeScript
        import Anthropic from "@anthropic-ai/sdk";

        const client = new Anthropic();

        const message = await client.messages.create({
          model: "claude-opus-4-8",
          max_tokens: 1000,
          messages: [
            {
              role: "user",
              content: "What should I search for to find the latest developments in renewable energy?"
            }
          ]
        });
        console.log(message.content);
        ```
      </Step>

      <Step title="Jalankan kode Anda">
        ```bash
        npx tsx quickstart.ts
        ```

        ```text Output wrap
        [
          {
            type: 'text',
            text: 'Here are some effective search strategies to find the latest developments in renewable energy:\n' +
              '\n' +
              '## General Search Terms\n' +
              '- "Renewable energy news 2025"\n' +
              '- ...'
          }
        ]
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="C#">
    <Steps>
      <Step title="Atur kunci API Anda">
        Ekspor kunci API Anda sebagai variabel lingkungan. SDK membaca `ANTHROPIC_API_KEY` secara otomatis.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Buat proyek dan instal SDK">
        Buat proyek konsol baru dan tambahkan paket Anthropic:

        ```bash
        dotnet new console -n ClaudeQuickstart
        cd ClaudeQuickstart
        dotnet add package Anthropic
        ```
      </Step>

      <Step title="Buat kode Anda">
        Ganti isi `Program.cs`:

        ```csharp C#
        using Anthropic;
        using Anthropic.Models.Messages;

        var client = new AnthropicClient();

        var message = await client.Messages.Create(new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 1000,
            Messages =
            [
                new()
                {
                    Role = Role.User,
                    Content = "What should I search for to find the latest developments in renewable energy?",
                },
            ],
        });

        foreach (var block in message.Content)
        {
            Console.WriteLine(block);
        }
        ```
      </Step>

      <Step title="Jalankan kode Anda">
        ```bash
        dotnet run
        ```

        ```text Output wrap
        {
          "type": "text",
          "text": "Here are some effective search strategies to find the latest developments in renewable energy:\n\n## General Search Terms\n- \"Renewable energy news 2025\"\n- ..."
        }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Go">
    <Steps>
      <Step title="Atur kunci API Anda">
        Ekspor kunci API Anda sebagai variabel lingkungan. SDK membaca `ANTHROPIC_API_KEY` secara otomatis.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Buat proyek dan instal SDK">
        Buat modul baru dan tambahkan Anthropic SDK:

        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        go mod init claude-quickstart
        go get github.com/anthropics/anthropic-sdk-go
        ```
      </Step>

      <Step title="Buat kode Anda">
        Buat file bernama `main.go`:

        ```go Go
        package main

        import (
        	"context"
        	"fmt"
        	"log"

        	"github.com/anthropics/anthropic-sdk-go"
        )

        func main() {
        	client := anthropic.NewClient()

        	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
        		Model:     anthropic.ModelClaudeOpus4_8,
        		MaxTokens: 1000,
        		Messages: []anthropic.MessageParam{
        			anthropic.NewUserMessage(anthropic.NewTextBlock("What should I search for to find the latest developments in renewable energy?")),
        		},
        	})
        	if err != nil {
        		log.Fatal(err)
        	}

        	fmt.Println(message.JSON.Content.Raw())
        }
        ```
      </Step>

      <Step title="Jalankan kode Anda">
        ```bash
        go run .
        ```

        ```text Output wrap
        [{"type":"text","text":"Here are some effective search strategies to find the latest developments in renewable energy:\n\n## General Search Terms\n- \"Renewable energy news 2025\"\n- ..."}]
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Java">
    <Steps>
      <Step title="Atur kunci API Anda">
        Ekspor kunci API Anda sebagai variabel lingkungan. SDK membaca `ANTHROPIC_API_KEY` secara otomatis.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Siapkan proyek Anda">
        Anda memerlukan JDK (25 atau lebih baru) dan [Gradle](https://gradle.org/install/) atau [Maven](https://maven.apache.org/install.html) pada `PATH` Anda. Buat direktori untuk proyek Anda dengan direktori sumber Java di dalamnya:

        ```bash
        mkdir -p claude-quickstart/src/main/java && cd claude-quickstart
        ```

        Kemudian tambahkan file build. Temukan versi SDK terkini di [Maven Central](https://central.sonatype.com/artifact/com.anthropic/anthropic-java).

        <Tabs>
          <Tab title="Gradle">
            Simpan ini sebagai `build.gradle.kts`:

            ```kotlin
            plugins {
                application
            }

            repositories {
                mavenCentral()
            }

            java {
                toolchain {
                    languageVersion = JavaLanguageVersion.of(25)
                }
            }

            dependencies {
                implementation("com.anthropic:anthropic-java:2.40.0")
            }

            application {
                mainClass = "QuickStart"
            }
            ```
          </Tab>

          <Tab title="Maven">
            Simpan ini sebagai `pom.xml`:

            ```xml
            <project xmlns="http://maven.apache.org/POM/4.0.0">
              <modelVersion>4.0.0</modelVersion>
              <groupId>com.example</groupId>
              <artifactId>quickstart</artifactId>
              <version>1.0-SNAPSHOT</version>
              <properties>
                <maven.compiler.release>25</maven.compiler.release>
                <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
              </properties>
              <dependencies>
                <dependency>
                  <groupId>com.anthropic</groupId>
                  <artifactId>anthropic-java</artifactId>
                  <version>2.40.0</version>
                </dependency>
              </dependencies>
            </project>
            ```
          </Tab>
        </Tabs>
      </Step>

      <Step title="Buat kode Anda">
        Simpan ini sebagai `QuickStart.java` di direktori sumber Java proyek Anda (biasanya `src/main/java/`):

        ```java Java
        import com.anthropic.client.okhttp.AnthropicOkHttpClient;
        import com.anthropic.models.messages.Message;
        import com.anthropic.models.messages.MessageCreateParams;
        import com.anthropic.models.messages.Model;

        static void main() {
            var client = AnthropicOkHttpClient.fromEnv();

            var params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_8)
                .maxTokens(1000)
                .addUserMessage(
                    "What should I search for to find the latest developments in renewable energy?"
                )
                .build();

            Message message = client.messages().create(params);
            IO.println(message.content());
        }
        ```
      </Step>

      <Step title="Jalankan kode Anda">
        <Tabs>
          <Tab title="Gradle">
            ```bash
            gradle run
            ```
          </Tab>

          <Tab title="Maven">
            ```bash
            mvn compile exec:java -Dexec.mainClass=QuickStart
            ```
          </Tab>
        </Tabs>

        ```text Output wrap
        [ContentBlock{text=TextBlock{citations=, text=Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ..., type=text, additionalProperties={}}}]
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="PHP">
    <Steps>
      <Step title="Atur kunci API Anda">
        Ekspor kunci API Anda sebagai variabel lingkungan. SDK membaca `ANTHROPIC_API_KEY` secara otomatis.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Buat proyek dan instal SDK">
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        composer require "anthropic-ai/sdk" "guzzlehttp/guzzle:^7"
        ```
      </Step>

      <Step title="Buat kode Anda">
        Buat file bernama `quickstart.php`:

        ```php PHP
        <?php
        require 'vendor/autoload.php';

        use Anthropic\Client;
        use Anthropic\Messages\Model;

        $client = new Client();

        $message = $client->messages->create(
            model: Model::CLAUDE_OPUS_4_8,
            maxTokens: 1000,
            messages: [
                [
                    'role' => 'user',
                    'content' => 'What should I search for to find the latest developments in renewable energy?',
                ],
            ],
        );

        print_r($message->content);
        ```
      </Step>

      <Step title="Jalankan kode Anda">
        ```bash
        php quickstart.php
        ```

        ```text Output wrap
        Array
        (
            [0] => Anthropic\Messages\TextBlock Object
                (
                    [type] => text
                    [citations] =>
                    [text] => Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
                )

        )
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Ruby">
    <Steps>
      <Step title="Atur kunci API Anda">
        Ekspor kunci API Anda sebagai variabel lingkungan. SDK membaca `ANTHROPIC_API_KEY` secara otomatis.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Buat proyek dan instal SDK">
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        bundle init
        bundle add anthropic
        ```
      </Step>

      <Step title="Buat kode Anda">
        Buat file bernama `quickstart.rb`:

        ```ruby Ruby
        require "anthropic"

        client = Anthropic::Client.new

        message = client.messages.create(
          model: Anthropic::Model::CLAUDE_OPUS_4_8,
          max_tokens: 1000,
          messages: [
            {
              role: "user",
              content: "What should I search for to find the latest developments in renewable energy?"
            }
          ]
        )

        pp message.content
        ```
      </Step>

      <Step title="Jalankan kode Anda">
        ```bash
        bundle exec ruby quickstart.rb
        ```

        ```text Output wrap
        [#<Anthropic::Models::TextBlock:0xc8 {text: "Here are some effective search strategies to find the latest developments in renewable energy:\n\n## General Search Terms\n- \"Renewable energy news 2025\"\n- ...", type: :text}>]
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Langkah selanjutnya

Anda telah melakukan panggilan API pertama Anda. Selanjutnya, pelajari pola Messages API yang akan Anda gunakan di setiap integrasi Claude.

<Card title="Bekerja dengan Messages API" icon="messages" href="/docs/id/build-with-claude/working-with-messages">
  Pelajari percakapan multi-giliran, prompt sistem, alasan berhenti, dan pola inti lainnya.
</Card>

Setelah Anda terbiasa dengan dasar-dasarnya, jelajahi lebih lanjut:

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="brain" href="/docs/id/about-claude/models/overview">
    Bandingkan model Claude berdasarkan kemampuan dan biaya.
  </Card>

  <Card title="Ikhtisar fitur" icon="list" href="/docs/id/build-with-claude/overview">
    Jelajahi semua kemampuan Claude: alat, manajemen konteks, output terstruktur, dan lainnya.
  </Card>

  <Card title="SDK Klien" icon="code-brackets" href="/docs/id/cli-sdks-libraries/overview">
    Dokumentasi referensi untuk Python, TypeScript, C#, dan pustaka klien lainnya.
  </Card>
</CardGroup>
