---
source: platform
url: https://platform.claude.com/docs/id/get-started
fetched_at: 2026-11-10T02:13:26.049428Z
sha256: 3c00bfb6507c1106664c6062955066e92254e8584c392bb4603e2ecc014603fc
---

---
title: Memulai dengan Claude
url: https://platform.claude.com/docs/id/get-started
description: Lakukan panggilan API pertama Anda ke Claude dan bangun asisten pencarian web sederhana.
---

## Sebelum Anda memulai

<Steps continues>
  <Step title="Buat akun Claude Console">
    [Daftar](https://platform.claude.com/) untuk akun Claude Console, atau masuk ke akun yang sudah Anda miliki.
  </Step>

  <Step title="Pilih cara autentikasi">
    Masuk dengan CLI direkomendasikan untuk pengembangan lokal.

    Follow the steps for one of the following options.
  </Step>
</Steps>

**CLI**

<Steps continued>
  <Step title="Instal CLI" stepNumber={3}>
    <Tabs noDeepLinks>
      <Tab title="Homebrew (macOS)">
        ```bash
        brew install anthropics/tap/ant
        ```
      </Tab>

      <Tab title="curl (Linux/WSL)">
        Untuk lingkungan Linux, unduh biner rilis secara langsung.

        ```bash
        VERSION=2.8.0
        OS=$(uname -s | tr '[:upper:]' '[:lower:]')
        case $(uname -m) in
          x86_64) ARCH=amd64 ;;
          aarch64) ARCH=arm64 ;;
        esac
        curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${VERSION}/ant_${VERSION}_${OS}_${ARCH}.tar.gz" \
          | sudo tar -xz -C /usr/local/bin ant
        ```

        Anda dapat menemukan semua rilis di [halaman rilis GitHub](https://github.com/anthropics/anthropic-cli/releases).
      </Tab>

      <Tab title="go install">
        Anda juga dapat menginstal CLI dari kode sumber menggunakan `go install`, yang memerlukan Go 1.26.10 atau yang lebih baru.

        ```bash
        go install github.com/anthropics/anthropic-cli/v2/cmd/ant@latest
        ```

        `go install` menempatkan biner di `$(go env GOPATH)/bin`. Tambahkan direktori tersebut ke `PATH` Anda jika belum ada:

        ```bash
        export PATH="$PATH:$(go env GOPATH)/bin"
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Masuk" stepNumber={4}>
    ```bash
    ant auth login
    ```

    Setelah login selesai, SDK dan CLI akan mengambil kredensial Anda secara otomatis.
  </Step>
</Steps>

**Kunci API**

<Steps continued>
  <Step title="Buat kunci API" stepNumber={3}>
    Buat [kunci API](https://platform.claude.com/settings/keys) di Claude Console.
  </Step>

  <Step title="Atur variabel lingkungan" stepNumber={4}>
    SDK dan CLI membaca kunci Anda dari `ANTHROPIC_API_KEY`:

    ```bash
    export ANTHROPIC_API_KEY="your-api-key-here"
    ```
  </Step>
</Steps>

## Memanggil API

<Tabs>
  <Tab title="cURL">
    <Steps>
      <Step title="Lakukan panggilan API pertama Anda" stepNumber={5}>
        **CLI**

        Kirim permintaan `POST` ke Messages API, dengan [token akses dari proses masuk CLI Anda](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting#authenticate-curl-requests-with-cli-credentials) sebagai bearer token:

        ```bash cURL
        curl https://api.anthropic.com/v1/messages \
          -H "content-type: application/json" \
          -H "Authorization: Bearer $(ant auth print-credentials --access-token)" \
          -H "anthropic-version: 2026-10-21" \
          -d '{
            "model": "claude-opus-5-5",
            "max_tokens": 1000,
            "messages": [
              {
                "role": "user",
                "content": "What should I search for to find the latest developments in renewable energy?"
              }
            ]
          }'
        ```

        **Kunci API**

        Kirim permintaan `POST` ke Messages API:

        ```bash cURL
        curl https://api.anthropic.com/v1/messages \
          -H "content-type: application/json" \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2026-10-21" \
          -d '{
            "model": "claude-opus-5-5",
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
          "model": "claude-opus-5-5",
          "id": "msg_013mHbppMPd2PrVJzGMZPt2D",
          "type": "message",
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "Here are some effective search strategies to find the latest developments in renewable energy:\n\n## General Search Terms\n- \"Renewable energy news 2025\"\n- ..."
            }
          ],
          "stop_reason": "end_turn",
          "stop_sequence": null,
          "stop_details": null,
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
      <Step title="Lakukan panggilan API pertama Anda" stepNumber={5}>
        **Kunci API**

        Jika sebelumnya Anda memilih kunci API, instal CLI terlebih dahulu:

        <Tabs noDeepLinks>
          <Tab title="Homebrew (macOS)">
            ```bash
            brew install anthropics/tap/ant
            ```
          </Tab>

          <Tab title="curl (Linux/WSL)">
            Untuk lingkungan Linux, unduh biner rilis secara langsung.

            ```bash
            VERSION=2.8.0
            OS=$(uname -s | tr '[:upper:]' '[:lower:]')
            case $(uname -m) in
              x86_64) ARCH=amd64 ;;
              aarch64) ARCH=arm64 ;;
            esac
            curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${VERSION}/ant_${VERSION}_${OS}_${ARCH}.tar.gz" \
              | sudo tar -xz -C /usr/local/bin ant
            ```

            Anda dapat menemukan semua rilis di [halaman rilis GitHub](https://github.com/anthropics/anthropic-cli/releases).
          </Tab>

          <Tab title="go install">
            Anda juga dapat menginstal CLI dari kode sumber menggunakan `go install`, yang memerlukan Go 1.26.10 atau yang lebih baru.

            ```bash
            go install github.com/anthropics/anthropic-cli/v2/cmd/ant@latest
            ```

            `go install` menempatkan biner di `$(go env GOPATH)/bin`. Tambahkan direktori tersebut ke `PATH` Anda jika belum ada:

            ```bash
            export PATH="$PATH:$(go env GOPATH)/bin"
            ```
          </Tab>
        </Tabs>

        Jalankan `ant messages create` dari terminal Anda:

        ```bash CLI
        ant messages create \
          --model claude-opus-5-5 \
          --max-tokens 1000 \
          --message '{
            role: user,
            content: "What should I search for to find the latest developments in renewable energy?"
          }'
        ```

        CLI mencetak respons JSON:

        ```json Output
        {
          "model": "claude-opus-5-5",
          "id": "msg_01N1ycuCkM5Mzd7WhTU4fwST",
          "type": "message",
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "Here are some effective search strategies to find the latest developments in renewable energy:\n\n## General Search Terms\n- \"Renewable energy news 2025\"\n- ..."
            }
          ],
          "stop_reason": "end_turn",
          "stop_sequence": null,
          "stop_details": null,
          "usage": { "input_tokens": 21, "output_tokens": 305 }
        }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Python">
    <Steps>
      <Step title="Buat proyek dan instal SDK" stepNumber={5}>
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        python3 -m venv .venv && source .venv/bin/activate
        pip install anthropic
        ```
      </Step>

      <Step title="Buat kode Anda" stepNumber={6}>
        Buat file bernama `quickstart.py`:

        ```python Python
        import anthropic

        client = anthropic.Anthropic()

        message = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": "What should I search for to find the latest developments in renewable energy?",
                }
            ],
        )

        for block in message.content:
            if block.type == "text":
                print(block.text)
        ```
      </Step>

      <Step title="Jalankan kode Anda" stepNumber={7}>
        ```bash
        python quickstart.py
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="TypeScript">
    <Steps>
      <Step title="Buat proyek dan instal SDK" stepNumber={5}>
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        npm init -y
        npm pkg set type=module
        npm install @anthropic-ai/sdk
        ```
      </Step>

      <Step title="Buat kode Anda" stepNumber={6}>
        Buat file bernama `quickstart.ts`:

        ```typescript TypeScript
        import Anthropic from "@anthropic-ai/sdk";

        const client = new Anthropic();

        const message = await client.messages.create({
          model: "claude-opus-5-5",
          max_tokens: 1000,
          messages: [
            {
              role: "user",
              content: "What should I search for to find the latest developments in renewable energy?"
            }
          ]
        });

        for (const block of message.content) {
          if (block.type === "text") {
            console.log(block.text);
          }
        }
        ```
      </Step>

      <Step title="Jalankan kode Anda" stepNumber={7}>
        ```bash
        npx tsx quickstart.ts
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="C#">
    <Steps>
      <Step title="Buat proyek dan instal SDK" stepNumber={5}>
        Buat proyek konsol baru dan tambahkan paket Anthropic:

        ```bash
        dotnet new console -n ClaudeQuickstart
        cd ClaudeQuickstart
        dotnet add package Anthropic
        ```
      </Step>

      <Step title="Buat kode Anda" stepNumber={6}>
        Ganti isi `Program.cs`:

        ```csharp C#
        using Anthropic;
        using Anthropic.Models.Messages;

        var client = new AnthropicClient();

        var message = await client.Messages.Create(new MessageCreateParams
        {
            Model = Model.ClaudeOpus5_5,
            MaxTokens = 1000,
            Messages =
            [
                new UserMessageParam
                {
                    Content = "What should I search for to find the latest developments in renewable energy?",
                },
            ],
        });

        foreach (var block in message.Content)
        {
            if (block.TryPickText(out var textBlock))
            {
                Console.WriteLine(textBlock.Text);
            }
        }
        ```
      </Step>

      <Step title="Jalankan kode Anda" stepNumber={7}>
        ```bash
        dotnet run
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Go">
    <Steps>
      <Step title="Buat proyek dan instal SDK" stepNumber={5}>
        Buat modul baru dan tambahkan Anthropic SDK:

        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        go mod init claude-quickstart
        go get github.com/anthropics/anthropic-sdk-go/v2
        ```
      </Step>

      <Step title="Buat kode Anda" stepNumber={6}>
        Buat file bernama `main.go`:

        ```go Go
        package main

        import (
        	"context"
        	"fmt"
        	"log"

        	"github.com/anthropics/anthropic-sdk-go/v2"
        )

        func main() {
        	client := anthropic.NewClient()

        	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
        		Model:     anthropic.ModelClaudeOpus5_5,
        		MaxTokens: 1000,
        		Messages: []anthropic.MessageParam{
        			anthropic.NewUserMessage(anthropic.NewTextBlock("What should I search for to find the latest developments in renewable energy?")),
        		},
        	})
        	if err != nil {
        		log.Fatal(err)
        	}

        	for _, block := range message.Content {
        		if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
        			fmt.Println(textBlock.Text)
        		}
        	}
        }
        ```
      </Step>

      <Step title="Jalankan kode Anda" stepNumber={7}>
        ```bash
        go run .
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Java">
    <Steps>
      <Step title="Siapkan proyek Anda" stepNumber={5}>
        Anda memerlukan JDK (25 atau lebih baru) dan [Gradle](https://gradle.org/install/) atau [Maven](https://maven.apache.org/install.html) di `PATH` Anda. Buat direktori untuk proyek Anda dengan direktori sumber Java di dalamnya:

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
                implementation("com.anthropic:anthropic-java:3.7.0")
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
                  <version>3.7.0</version>
                </dependency>
              </dependencies>
            </project>
            ```
          </Tab>
        </Tabs>
      </Step>

      <Step title="Buat kode Anda" stepNumber={6}>
        Simpan ini sebagai `QuickStart.java` di direktori sumber Java proyek Anda (biasanya `src/main/java/`):

        ```java Java
        import com.anthropic.client.okhttp.AnthropicOkHttpClient;
        import com.anthropic.models.messages.Message;
        import com.anthropic.models.messages.MessageCreateParams;
        import com.anthropic.models.messages.Model;

        static void main() {
            var client = AnthropicOkHttpClient.fromEnv();

            var params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_5_5)
                .maxTokens(1000)
                .addUserMessage(
                    "What should I search for to find the latest developments in renewable energy?"
                )
                .build();

            Message message = client.messages().create(params);
            for (var block : message.content()) {
                block.text().ifPresent(textBlock -> IO.println(textBlock.text()));
            }
        }
        ```
      </Step>

      <Step title="Jalankan kode Anda" stepNumber={7}>
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
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="PHP">
    <Steps>
      <Step title="Buat proyek dan instal SDK" stepNumber={5}>
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        composer require "anthropic-ai/sdk" "guzzlehttp/guzzle:^7"
        ```
      </Step>

      <Step title="Buat kode Anda" stepNumber={6}>
        Buat file bernama `quickstart.php`:

        ```php PHP
        <?php
        require 'vendor/autoload.php';

        use Anthropic\Client;
        use Anthropic\Messages\Model;
        use Anthropic\Messages\TextBlock;

        $client = new Client();

        $message = $client->messages->create(
            model: Model::CLAUDE_OPUS_5_5,
            maxTokens: 1000,
            messages: [
                [
                    'role' => 'user',
                    'content' => 'What should I search for to find the latest developments in renewable energy?',
                ],
            ],
        );

        foreach ($message->content as $block) {
            if ($block instanceof TextBlock) {
                echo $block->text . PHP_EOL;
            }
        }
        ```
      </Step>

      <Step title="Jalankan kode Anda" stepNumber={7}>
        ```bash
        php quickstart.php
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Ruby">
    <Steps>
      <Step title="Buat proyek dan instal SDK" stepNumber={5}>
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        bundle init
        bundle add anthropic
        ```
      </Step>

      <Step title="Buat kode Anda" stepNumber={6}>
        Buat file bernama `quickstart.rb`:

        ```ruby Ruby
        require "anthropic"

        client = Anthropic::Client.new

        message = client.messages.create(
          model: Anthropic::Model::CLAUDE_OPUS_5_5,
          max_tokens: 1000,
          messages: [
            {
              role: "user",
              content: "What should I search for to find the latest developments in renewable energy?"
            }
          ]
        )

        message.content.each do |block|
          puts block.text if block.type == :text
        end
        ```
      </Step>

      <Step title="Jalankan kode Anda" stepNumber={7}>
        ```bash
        bundle exec ruby quickstart.rb
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Langkah selanjutnya

Anda telah melakukan panggilan API pertama Anda. Selanjutnya, pelajari pola Messages API yang akan Anda gunakan di setiap integrasi Claude.

<Card title="Bekerja dengan Messages API" icon="messages" href="https://platform.claude.com/docs/id/build-with-claude/working-with-messages">
  Pelajari percakapan multi-giliran, prompt sistem, alasan berhenti, dan pola inti lainnya.
</Card>

Setelah Anda nyaman dengan dasar-dasarnya, jelajahi lebih lanjut:

<CardGroup cols={2}>
  <Card title="Ikhtisar model" icon="brain" href="https://platform.claude.com/docs/id/models/overview">
    Bandingkan model Claude berdasarkan kemampuan dan biaya.
  </Card>

  <Card title="Ikhtisar fitur" icon="list" href="https://platform.claude.com/docs/id/build-with-claude/overview">
    Telusuri semua kemampuan Claude: alat, manajemen konteks, output terstruktur, dan lainnya.
  </Card>

  <Card title="SDK Klien" icon="code-brackets" href="https://platform.claude.com/docs/id/cli-sdks-libraries/overview">
    Dokumentasi referensi untuk Python, TypeScript, C#, dan pustaka klien lainnya.
  </Card>

  <Card title="Autentikasi" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/authentication">
    Bandingkan kunci API dan Workload Identity Federation, serta atur masa berlaku kunci.
  </Card>
</CardGroup>
